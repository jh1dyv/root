#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# ======================================================================
#  SYNOPSIS:
#	python SlnConv.py [options] slnfile
#	options:
#	    -d version	変換して作成する Visual Studio のバージョン
#	    -s version	変換する元となる Visual Studio のバージョン
#	    -D version	変換して作成する Windows SDK のバージョン
#			又は 'latest' (登録されている最新のバージョン)
#	arguments:
#	    slnfile	ソリューション名 or ソリューションファイル名
#
#  DESCRIPTION:
#	指定されたソリューションファイルを変換して新しいバージョンの
#	ソリューションファイル (Format Version 12.00) を生成する。
#
# ----------------------------------------------------------------------
#  VERSION:
#	Ver 1.0  2018/12/q06 F.Kanehori	First version.
# ======================================================================
version = 1.0

import sys
import os
import re
import glob
import subprocess
from optparse import OptionParser

# ----------------------------------------------------------------------
#  Constants
#
prog = sys.argv[0].split(os.sep)[-1].split('.')[0]
progpath = sys.argv[0]
PIPE = subprocess.PIPE
NULL = subprocess.DEVNULL

# ----------------------------------------------------------------------
#  External tools.
#

# ----------------------------------------------------------------------
#  Helper methods
# ----------------------------------------------------------------------
#
def get_slnname(fname, version, suffix):
	s_len = len(suffix)
	if fname[-s_len:] == suffix:
		fname = fname[:-s_len]
	v_len = len(version)
	if fname[-v_len:] == version:
		fname = fname[:-v_len]
	return fname









#  引用符(')と(")とを相互に入れ替える
#
def exchange_quote(s):
	return s.replace("'", '|').replace('"', "'").replace('|', '"')

#  入力ファイルをutf8に変換したのち、patternsで指定されたパターンすべて
#  についてsedで書き換え処理をする。
#
def fileconv(ifname, patterns, ofname):
	if verbose:
		print('converting %s to %s' % (ifname, ofname))
	#
	inp_cmnd = '%s %s' % (cmndname('cat'), ifname.replace('/', os.sep))
	med_cmnd = []
	for patt in patterns:
		cmnd = "%s -e 's/%s/%s/g'" % (sed, patt[0], patt[1])
		cmnd = exchange_quote(cmnd)
		med_cmnd.append(cmnd)
	out_cmnd = '%s -w -Lu' % nkf
	#
	if verbose > 1:
		print('EXEC: %s' % inp_cmnd)
	inp_proc = execute(inp_cmnd, stdout=PIPE, shell=True)
	out_pipe = inp_proc.stdout
	med_proc = []
	for cmnd in med_cmnd:
		if verbose > 1:
			print('EXEC: %s' % cmnd)
		proc = execute(cmnd, stdin=out_pipe, stdout=PIPE, shell=True)
		out_pipe = proc.stdout
		med_proc.append(proc)
	if verbose > 1:
		print('EXEC: %s' % out_cmnd)
	outf = ofname.replace('/', os.sep)
	out_proc = execute(out_cmnd, stdin=out_pipe, stdout=outf, shell=True)
	#
	inp_proc.wait()
	for proc in med_proc:
		proc.wait()
	rc = out_proc.wait()
	if rc != 0:
		msg = 'file conversion failed: "%s"' % ifname
		abort(msg)

#  指定されたコマンドを実行する
#
def execute(cmnd, stdin=None, stdout=sys.stdout, stderr=sys.stderr, shell=None):
	if stderr is NULL:
		stderr = subprocess.STDOUT
	fd = [ pipe_open(stdin, 'r'),
	       pipe_open(stdout, 'w'),
	       pipe_open(stderr, 'w') ]
	if shell is None:
		shell = False
	#if verbose > 1:
	#	print('exec: %s' % cmnd)
	proc = subprocess.Popen(cmnd,
				stdin=fd[0], stdout=fd[1], stderr=fd[2],
				shell=shell)
	return proc

#  Pipeオブジェクトをオープンする
#
def pipe_open(file, mode):
	if not isinstance(file, str):
		return file
	try:
		f = open(file, mode)
	except IOError as err:
		f = None
	return f

#  プロセスの終了を待つ
#
def wait(proc):
	rc = proc.wait()
	rc = -(rc & 0b1000000000000000) | (rc & 0b0111111111111111)
	return rc

#  指定されたディレクトリ以下をすべて削除する
#
def remove_tree(top, verbose=0):
	cmnd = 'rd /S /Q %s' % top
	if verbose:
		print('remove_tree: %s' % top)
	rc = wait(execute(cmnd, shell=True))
	return rc

#  ファイルをコピーする
#  ※ dstがディレクトリ名のときはcp()を、ファイル名のときはcp0()を使用する
#
def cp(src, dst):
	#  srcとdstの組み合わせ
	#     file to file	N/A
	#     fiel to dir	src -> dst/leaf(src)
	#     dir to file	Error!
	#     dir to dir	src/* -> dst/*
	#  file to file は cp0(src, dst) で扱う

	if os.path.isdir(src) and os.path.isfile(dst):
		msg = 'copying directory to plain file (%s to %s)' % (src, dst)
		abort('Error: %s' % msg)

	if os.path.isdir(src):
		rc = __cp(src, dst)
	else:	
		for s in glob.glob(src):
			rc = __cp(pathconv(s, True), dst)
			if rc != 0: return 1	# copying failed
	return rc

def __cp(src, dst):
	if os.path.isfile(src):
		org_src_cnv = pathconv(src)
		plist = src.split('/')
		if len(plist) > 1:
			src = plist[-1]
			dst = '%s/%s' % (dst, '/'.join(plist[:-1]))
		if not os.path.exists(dst):
			Print('  creating directory %s' % dst)
			os.makedirs(dst)
		if verbose > 1:
			Print('  cp: %s -> %s' % (src, dst))
		src_cnv = pathconv(src)
		dst_cnv = pathconv(dst)
		cmnd = '%s %s %s' % (cmndname('cp'), org_src_cnv, dst_cnv)
		rc = wait(execute(cmnd, stdout=NULL, stderr=NULL, shell=True))

	else:	# both src and dst are directory
		dst = '%s/%s' % (dst, src)
		if not os.path.exists(dst):
			abspath = os.path.abspath(dst)
			Print('  creating directory %s' % pathconv(abspath, True))
			os.makedirs(dst)
		if verbose > 1:
			Print('  cp: %s -> %s' % (src, dst))
		src_cnv = pathconv(src)
		dst_cnv = pathconv(dst)
		cmnd = 'xcopy /I /E /S /Y /Q %s %s' % (src_cnv, dst_cnv)
		rc = wait(execute(cmnd, stdout=NULL, stderr=NULL, shell=True))

	return rc

def cp0(src, dst):
	#  srcとdstの組み合わせ
	#     file to file	src -> dst

	if verbose > 1:
		Print('  cp: %s -> %s' % (src, dst))
	src_cnv = pathconv(src)
	dst_cnv = pathconv(dst)
	cmnd = '%s %s %s' % (cmndname('cp'), src_cnv, dst_cnv)
	rc = wait(execute(cmnd, stdout=NULL, stderr=NULL, shell=True))
	return rc

#  パスセパラータを変換する
#
def upath(path):
	return path.replace(os.sep, '/')

#  現在のOSの元でのコマンド名を返す
#
def cmndname(cmnd):
	nametab = { 'cat':	['cat', 'type'],
		    'cp':	['cp', 'copy'],
		    'rm':	['rm', 'del'],
		}
	indx = 1
	return nametab[cmnd][indx]

#  Error process.
#
def error(msg):
	sys.stderr.write('%s: Error: %s\n' % (prog, msg))
def abort(msg, exitcode=1):
	error(msg)
	sys.exit(exitcode)

#  Show usage.
#
def print_usage():
	print()
	cmnd = 'python %s --help' % progpath
	wait(execute(cmnd))
	sys.exit(1)

# ----------------------------------------------------------------------
#  Options
#
usage = 'Usage: %prog [options] texmain'
parser = OptionParser(usage = usage)
#
parser.add_option('-s', '--src-version', dest='src_version',
			action='store', default='14.0', metavar='VER',
			help='source VS version [default: %default]')
parser.add_option('-d', '--dst-version', dest='dst_version',
			action='store', default='15.0', metavar='VER',
			help='destination VS version [default: %default]')
parser.add_option('-S', '--sdk-version', dest='sdk_version',
			action='store', default='10.0.17763.0', metavar='VER',
			help='SDK version [default: %default]')
parser.add_option('-v', '--verbose', dest='verbose',
			action='count', default=0,
			help='set verbose mode')
parser.add_option('-V', '--version', dest='version',
			action='store_true', default=False,
			help='show version')
#
(options, args) = parser.parse_args()
if options.version:
	print('%s: Version %s' % (prog, version))
	sys.exit(0)
#
src_version = options.src_version
dst_version = options.dst_version
sdk_version = options.sdk_version
verbose = options.verbose
#
if len(args) != 1:
	error('incorrect number of arguments')
	print_usage()
#
slnfile = upath(args[0])
slnname = get_slnname(slnfile, src_version, '.sln')
src_slnfile = '%s%s.sln' % (slnname, src_version)
dst_slnfile = '%s%s.sln' % (slnname, dst_version)

#  ファイルのチェック
#
if not os.path.exists(src_slnfile):
	abort('No such file: "%s"' % src_slnfile)
if os.path.exists(dst_slnfile):
	print('%s: "%s" exists' % (prog, dst_slnfile))
	ans = input('overwrite [y/n] ?')
	if ans.lower() != 'y':
		abort('aborted')

vs_version = '15.0.27703.0'
if verbose:
	print('converting')
	print('  from: %s' % src_slnfile)
	print('  to:   %s' % dst_slnfile)
	print('version info')
	print('  VS:   %s' % vs_version)
	print('  SDK:  %s' % sdk_version)
	print()

# ----------------------------------------------------------------------
#  メイン処理開始
#

# ----------------------------------------------------------------------
#  指定されたソリューションファイルを読み、
#   (1) バージョン情報、プロジェクト情報を書き換える
#   (2) 関連するプロジェクトをリストアップする
#
patt_vsv = r'VisualStudioVersion = ([0-9.]+)'
patt_prj = r'Project\(.*\) = ".*", "(.*)", ".*"'
#
projects = []		# 関連プロジェクトのリスト
out_lines = []		# 書き出すファイルの内容
ifobj = open(src_slnfile)
for line in ifobj:
	m = re.match(patt_vsv, line)
	if m:
		line = line.replace(m.group(1), vs_version)
		if verbose:
			print(line.strip())
	m = re.match(patt_prj, line)
	if m:
		prjname = get_slnname(m.group(1), src_version, '.vcxproj')
		new_prjname = '%s%s.vcxproj' % (prjname, dst_version)
		line = line.replace(m.group(1), new_prjname)
		projects.append(new_prjname)
		if verbose:
			print(line.strip())
	out_lines.append(line)
ifobj.close()
#
ofobj = open(dst_slnfile, 'w')
for line in out_lines:
	ofobj.write(line)
ofobj.close()
#
#  関連するプロジェクトのうち、Springhead ライブラリに関するものは除く
#
excludes = [
	'Base', 'Collision', 'Creature', 'EmbPython', 'FileIO', 'Foundation',
	'Framework', 'Graphics', 'HumanINterface', 'PHysics', 'RunSwig']
#
spr_projs = []
for proj in projects:
	p = proj.split('\\')[-1]
	prjname = get_slnname(proj.split('\\')[-1], dst_version, '.vcxproj')
	if prjname in excludes:
		spr_projs.append(proj)
for proj in spr_projs:
	projects.remove(proj)
if verbose:
	print()
	print('"%s" created' % dst_slnfile)
	print()
	print('related project files are:')
	for proj in projects:
		print('  %s' % proj)
#
#  関連するプロジェクトファイルを書き換える
#







sys.exit(0)

# end: SlnConv.py
