#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# ======================================================================
#  SYNOPSIS:
#	renmae_html [options] files
#	    files:	Input file names.
#
#	options:
#	    -i fname:	Corresponding index file name.
#
#  DESCRIPTION:
#	Replace file names according to corresponding index file.
#	Corresponding index file must be encoded by utf8.
#
#  VERSION:
#	Ver 1.0  2018/11/17 F.Kanehori	First release version.
# ======================================================================
version = '1.0'

import sys
import os
import re
import glob
import random
import subprocess
from optparse import OptionParser

# ----------------------------------------------------------------------
#  Constants
#
prog = sys.argv[0].split(os.sep)[-1].split('.')[0]
#

# ----------------------------------------------------------------------
#  Options
#
usage = 'Usage: %prog [options]'
parser = OptionParser(usage = usage)
parser.add_option('-c', '--correspondence-file', dest='correspondence_file',
			action='store', default='csname.replace',
			help='corresponding file name (default: %default)')
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
if len(args) < 1:
	parser.error("incorrect number of arguments")

# get options and input file names
correspondence_file = options.correspondence_file
verbose = options.verbose
#
fn_args = args
fnames = []
for fn in fn_args:
	fnames.extend(glob.glob(fn))

if verbose:
	print('correspondence: %s' % correspondence_file)
	print('input files:    %s' % fnames)

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
	patt = r'\\chapter\{(.*)\}|\\section\{(.*)\}|\\subsection\{(.*)\}|\\subsubsection\{(.*)\}'
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

#  対応表ファイルを読む
#
if verbose:
	print('reading correspondence from "%s"' % correspondence_file)
correspondence = {}
keys = []
for line in open(correspondence_file, 'r', encoding='utf-8'):
	if line[-1] == '\n':
		line = line[:-1]
	replaced, original = line.split(',')
	keys.append(replaced + '.html')
	correspondence[replaced] = original
if verbose:
	for r,o in correspondence:
		print('  %s -> %s' % (r, o))

#  ファイル名を変更する
#
for f in fnames:
	if not os.path.exists(f):
		continue
	if not f in keys:
		continue
	to_name = correspondence[f.replace('.html', '')]
	rc = mv(f, to_name)
	if rc != 0:
		msg = 'rename failed: %s -> %s' % (f, to_name)
		print(msg)
		sys.exit(1)

# ----------------------------------------------------------------------
#  End of process.
#
if verbose:
	print('%s: done' % prog)
sys.exit(0)

# end: renmae_html.py
