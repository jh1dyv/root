#!/usr/bin/python
# -*- coding: utf-8 -*-
# ======================================================================
#  SYNOPSIS:
#	install [options] {deffile | source... dest-dir}
#	options:
#	    -d:		Create destination directory if not exist.
#	    -f:		Force all files to install.
#			(available only if deffile is specified)
#	    -n:		Show install command but do not install.
#	    -p:		Preserve last access/modification time stamp.
#	deffile:	Install definition file name.
#	source...:	Source file(s) to install.
#	dest_dir:	Install directory path.
#
#  DESCRIPTION:
#	Install files having newer timestamp than destination.
#	
#	Install definition file is "key-value-pair" file which can be
#	handled by KvFile class.  Key names to be used are;
#	    InsDir	Directory path to install.
#	    SrcDir	Directory path where files are.
#	    Files	File names separated by spaces.
#	There may be multiple sections (section name is arbitrary).
#	See "install.def.template" for example.
#
#  VERSION:
#	Ver 1.0  2018/04/22 F.Kanehori	First version.
#	Ver 1.1  2019/02/04 F.Kanehori	Add: wildcard and $-macro.
# ======================================================================
version = 1.1

import sys
import os
import glob
import datetime
from optparse import OptionParser

from install_param import *

sys.path.append('/usr/local/lib')
from FileOp import *
from KvFile import *
from Proc import *
from Error import *

# ----------------------------------------------------------------------
#  Constants
#
prog = sys.argv[0].split(os.sep)[-1].split('.')[0]

# ----------------------------------------------------------------------
#  Local methods.
#
def time_to_set(path):
	if preserve and path:
		# use original file time
		ftime = os.stat(path)
		at_ns = ftime.st_atime_ns
		mt_ns = ftime.st_mtime_ns
	else:
		# use current time
		d = datetime.datetime.today()
		CC, YY, MM, DD = 20, d.year%100, d.month, d.day
		hh, mm, ss, ms = d.hour, d.minute, d.second, d.microsecond
		yy = CC * 100 + YY
		dt = datetime.datetime(yy, MM, DD, hh, mm, ss, ms)
		at_ns = int(dt.timestamp() * 1000000 + 0.0000005) * 1000
		mt_ns = at_ns
	return at_ns, mt_ns

# ----------------------------------------------------------------------
#  Options
#
usage = 'Usage: %prog [options] {deffile | source... dest}'
parser = OptionParser(usage = usage)
parser.add_option('-d', '--directory', dest='create_dir',
			action='store_true', default=False,
			help='install directory path', metavar='DIR')
parser.add_option('-f', '--force', dest='force',
			action='store_true', default=False,
			help='force all files to be installed')
parser.add_option('-n', '--not-execute', dest='noexec',
			action='store_true', default=False,
			help='show command but do not install')
parser.add_option('-p', '--preserve-timestamps', dest='preserve',
			action='store_true', default=False,
			help='preserve file timestamps')
parser.add_option('-v', '--verbose', dest='verbose',
			action='count', default=0,
			help='set verbose level')
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
if len(args) == 0:
	Error(prog).error("incorrect number of arguments\n")
	Proc().execute('python %s.py --help' % prog).wait()
	sys.exit(1)

# get options and input file name
create_dir = options.create_dir
force_copy = options.force
no_execute = options.noexec
preserve = options.preserve
verbose	= options.verbose

if verbose > 1:
	print('  create-dir: %s' % create_dir)
	print('  preserve:   %s' % preserve)
	print('  force-copy: %s' % force_copy)
	print('  no-execute: %s' % no_execute)

# ----------------------------------------------------------------------
#  Get source files and destination from command line.
#
cwd = os.getcwd()
macro = '$'
params = []
if len(args) == 1:
	# case 1: from definition file.
	kvf = KvFile(args[0], sep='=', overwrite=False)
	kvf.read()
	sections = kvf.sections()
	#
	errflag = False
	for section in kvf.sections():
		idir = kvf.get('InsDir', section)
		sdir = kvf.get('SrcDir', section)
		srcs = kvf.get('Files', section)
		if idir and sdir and srcs:
			if isinstance(srcs, str):
				srcs = [srcs]
			srclist = []
			for src in srcs:
				# space separated file names are OK.
				# also wildcard is OK.
				tmp = src.replace(macro, section).split()
				os.chdir(sdir)
				for f in tmp:
					flist = glob.glob(f)
					srclist.extend(flist)
				os.chdir(cwd)
			for src in srclist:
				param = InstallParam(sdir, src, idir)
				params.append(param)
		else:
			miss  = '' if idir else 'InsDir '
			miss += '' if sdir else 'SrcDir '
			miss += '' if srcs else 'Files '
			msg = '%s: keyword missing (%s)' % (section, miss)
			Error(prog).error(msg)
			errflag = True
	if errflag:
		sys.exit(1)
else:
	# case 2: from command arguments.
	for arg in args[0:-1]:
		sdir = '/'.join(arg.split('/')[:-1])
		name = arg.split('/')[-1]
		param = InstallParam(sdir, name, args[-1])
		params.append(param)
if verbose > 1:
	n = 0
	for param in params:
		n += 1
		newer, src, dst = param.get()
		print('(%2d) src: %s' % (n, src))
		print('     dst: %s' % dst)

# ----------------------------------------------------------------------
#  Compare file timestamps.
#
for param in params:
	param.check_timestamp()

# ----------------------------------------------------------------------
#  Execute command.
#
fop = FileOp(dry_run=no_execute)
for param in params:
	newer, src, dst = param.get(force=force_copy)
	if newer:
		dstdir = '/'.join(dst.split('/')[:-1])
		if not os.path.exists(dstdir):
			if create_dir:
				fop.makedirs(dstdir)
			else:
				msg = 'no such directory: "%s"' % dstdir
				Error(prog).abort(msg)
		if not no_execute:
			print('install %s to %s' % (src, dst))
		at_ns, mt_ns = time_to_set(src)
		fop.cp(src, dst)
		if not no_execute:
			os.utime(dst, ns=(at_ns, mt_ns))

sys.exit(0)

# end: install.py
