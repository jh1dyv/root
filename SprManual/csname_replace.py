#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# ======================================================================
#  SYNOPSIS:
#	csname_replace [options] func files
#	    func:	'enc': encode csname to replaced_name
#			'dec': decode replaced_name to csname
#	    files:	Input file names.
#
#	options:
#	    -o fname:	Intermediate file name to place replaced names.
#	    -t suffix:	Suffix of temporary file.
#
#  DESCRIPTION:
#	Replace argument of \chapter,\section,\subsection having kanji
#	to non-kanji random string to avoid lwarpmk compile error, or
#	revive these randomized string to original argument.
#
#  VERSION:
#	Ver 1.0  2018/11/15 F.Kanehori	First release version.
# ======================================================================
version = '1.0'

import sys
import os
import re
import random
import subprocess
from optparse import OptionParser

# ----------------------------------------------------------------------
#  Constants
#
prog = sys.argv[0].split(os.sep)[-1].split('.')[0]
#
verbatim_in = r'\\begin\{sourcecode\}'
verbatim_out = r'\\end\{sourcecode\}'
code_bs = 92	# '\\'
code_ob = 123	# '{'
code_cb = 125	# '}'
code_u = 117	# 'u'
code_r = 114	# 'r'
code_l = 108	# 'l'

# ----------------------------------------------------------------------
#  Options
#
usage = 'Usage: %prog [options]'
parser = OptionParser(usage = usage)
parser.add_option('-o', '--int-file', dest='intfile',
			action='store', default='csname.replace',
			help='intermediate file name (default: %default)')
parser.add_option('-t', '--tmp-suffix', dest='suffix',
			action='store', default='replace.org',
			help='temporary file\'s suffix (default: .%default)')
parser.add_option('-v', '--verbose', dest='verbose',
			action='count', default=0,
			help='set verbose mode')
parser.add_option('-V', '--version', dest='version',
			action='store_true', default=False,
			help='show version')

# ----------------------------------------------------------------------
#  Process for command line
#
(options, args) = parser.parse_args()
if options.version:
	print('%s: Version %s' % (prog, version))
	sys.exit(0)
if len(args) < 2:
	parser.error("incorrect number of arguments")

# get options and input file names
intfile = options.intfile
suffix = options.suffix
verbose = options.verbose
#
func = args[0]
fnames = args[1:]

if verbose:
	print('func:    %s' % func)
	print('intfile: %s' % intfile)
	print('suffix:  %s' % suffix)

# ----------------------------------------------------------------------
#  メソッドの定義
# ----------------------------------------------------------------------

#  指定された長さのランダム文字列を作成する（文字はseedの中から取り出す）
#
def random_str(seed, size):
	strlen = len(seed)
	rand = ''
	for i in range(size):
		n = strlen
		while n >= strlen:
			n = int(random.random() * 100)
		rand += seed[n]
	return rand

#  作業ファイル名を作成する
#
def mktmpfname(basename, suffix):
	tmpfname = '%s.%s' % (basename, suffix)
	if os.path.exists(tmpfname):
		return mktmpfname(tmpfname, suffix)
	return tmpfname

#  ファイル名を変更する
#
def rename(fm , to):
	if is_unix():
		cmnd = 'mv %s %s' % (fm, to)
	else:
		cmnd = 'rename %s %s' % (fm, to)
	proc = subprocess.Popen(cmnd, shell=True)
	rc = proc.wait()
	if not is_unix():
		rc = -(rc & 0b1000000000000000) | (rc & 0b0111111111111111)
	return rc

#  現在のOSを判定する
#
def is_unix():
	return True if os.name == 'posix' else False

#  コマンドシーケンス \chapter, \section, \subsection, \subsubsection の
#  引数を漢字を含まない文字列に変換し、変換情報を中間ファイルに記録する
#
def encode():
	#  対象とするコマンドシーケンス
	patt = r'\\chapter\{(.*)\}|\\section\{(.*)\}|\\subsectio\{(.*)\}'
	#  置き換える
	seed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	replaces = []
	for f in fnames:
		if verbose:
			print('  encoding %s' % f)
		lines = []
		for line in open(f, 'r', encoding='utf-8'):
			m = re.search(patt, line)
			if m:
				if m.group(1): csname = m.group(1)
				if m.group(2): csname = m.group(2)
				if m.group(3): csname = m.group(3)
				randomname = random_str(seed, 16)
				if verbose:
					print('    %s -> %s' % (csname, randomname))
				line = line.replace(csname, randomname)
				replaces.append([csname, randomname])
			lines.append(line)
		if replaces != []:
			print('  -- replacing file: %s' % f)
			tmpfname = mktmpfname(f, suffix)
			if rename(f, tmpfname) != 0:
				msg = 'rename failed: %s -> %s' % (f, tmpfname)
				sys.exit(1)
			outf = open(f, 'w', encoding='utf-8')
			for line in lines:
				outf.write(line)
			outf.close()
	#
	intf = open(intfile, 'w', encoding='utf-8')
	for line in replaces:
		intf.write('%s,%s\n' % (line[1], line[0]))
	intf.close()

#
#
def decode():
	replaces = []
	for line in open(intfile, 'r', encoding='utf-8'):
		if line[-1] == '\n':
			line = line[:-1]
		replaces.append(line.split(','))

	for f in fnames:
		if verbose:
			print('  decoding %s' % f)
		lines = []
		for line in open(f, 'r', encoding='utf-8'):
			for key,val in replaces:
				if line.find(key):
					line = line.replace(key, val)
			lines.append(line)

		tmpfname = mktmpfname(f, suffix)
		if rename(f, tmpfname) != 0:
			msg = 'rename failed: %s -> %s' % (f, tmpfname)
			sys.exit(1)
		outf = open(f, 'w', encoding='utf-8')
		for line in lines:
			outf.write(line)
		outf.close()


# ----------------------------------------------------------------------
#  Main process.
#
if func == 'enc':
	# csname -> random string
	encode()
elif func == 'dec':
	# random string -> csname
	decode()

# ----------------------------------------------------------------------
#  End of process.
#
if verbose:
	print('%s: %s: done' % (prog, func))
sys.exit(0)

# end: csname_replace.py
