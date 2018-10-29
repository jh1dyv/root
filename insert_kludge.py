#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# ======================================================================
#  SYNOPSIS:
#	insert_kludge file
#	    file:	Input file name.
#
#  DESCRIPTION:
#	Insert 'kludge' before every location where character code
#	changes from 'ascii' to another multi-byte one.
#
#  VERSION:
#	Ver 1.0  2018/10/29 F.Kanehori	First release version.
# ======================================================================
version = '1.0'

import sys
import os
import re
from optparse import OptionParser

# ----------------------------------------------------------------------
#  Constants
#
prog = sys.argv[0].split(os.sep)[-1].split('.')[0]
#
target_defs = {
	'file': 'chapters.tex',
	'patt': r'\\input\{([a-zA-Z0-9_]+)\}'
}
kludge_code = b'\\KLUDGE '

# ----------------------------------------------------------------------
#  Options
#
usage = 'Usage: %prog [options] file'
parser = OptionParser(usage = usage)
parser.add_option('-v', '--verbose',
			dest='verbose', action='count', default=0,
			help='set verbose mode')
parser.add_option('-V', '--version',
			dest='version', action='store_true', default=False,
			help='show version')

# ----------------------------------------------------------------------
#  Process for command line
#
(options, args) = parser.parse_args()
if options.version:
	print('%s: Version %s' % (prog, version))
	sys.exit(0)
if len(args) != 1:
	parser.error("incorrect number of arguments")

# get options and input file name
verbose = options.verbose
infile = args[0]

if verbose:
	print('file: %s' % infile)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

#  処理の対象となるファイルを"chapters.tex"から読む
#
def read_targets():
	print(target_defs['file'])
	print(target_defs['patt'])
	fnames = []
	for line in open(target_defs['file'], 'r'):
		m = re.match(target_defs['patt'], line)
		if m:
			fname = m.group(1)
			if fname[-4:] != '.tex':
				fname += '.tex'
			fnames.append(fname)
	if verbose:
		print('targets: %s' % fnames)
	return fnames

#  指定された文字列にkludgeコードを挿入する
#
def process_oneline(string):

	# bytes型に変換して処理を行なう
	byte = string.encode('utf-8')
	size = len(list(byte))	# byte数
	if verbose:
		print('utf8: %s' % byte)

	# 各文字を表すutf8のバイト数を求める
	mark = []
	ix = 0
	while ix < size:
		leng = codelen(byte[ix])
		mark.append(leng)
		ix += 1
		for n in range(leng-1):
			mark.append(leng)
			ix += 1
	if verbose:
		print('mark: %s' % mark)

	# マルチバイトに変わる場所にKLUDGEを入れる
	bout = bytearray()
	prev = 0
	ix = 0
	while ix < size:
		curr = mark[ix]
		if curr != prev and curr > 1:
			bout.extend(kludge)
			if verbose:
				print('  kludge inserted at %d' % ix)
		bout.append(byte[ix])
		prev = curr
		ix += 1

	return bout.decode('utf-8')


# ----------------------------------------------------------------------
#  Main process.
#
fnames = read_targets()
for fn in fnames:
	print(fn)



# ----------------------------------------------------------------------
#  End of process.
#
if verbose:
	print('%s: done' % prog)
sys.exit(0)

# end: insert_kludge.py
