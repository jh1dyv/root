#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ======================================================================
#  CLASS:	InstallParam(srcdir, fname, insdir)
#
#  METHODS:
#	check_timestamp()
#	src, dst = get(force=False)
#
# ----------------------------------------------------------------------
#  VERSION:
#	Ver 1.0  2018/04/18 F.Kanehori	First release version.
# ======================================================================
import sys
import os

sys.path.append('/usr/local/lib')
from Util import *

##  Class for holding install control parameters.
#
class InstallParam:
	##  The initializer.
	#   @param srcdir	Source directory path (str).
	#   @param fname	File name to be installed (str).
	#   @param insdir	Install directory path (str).
	#   @param verbose	Verbose level (0: silent) (int).
	#
	def __init__(self, srcdir, fname, insdir, verbose=0):
		self.clsname = self.__class__.__name__
		self.version = 1.0
		#
		self.srcdir = Util.upath(srcdir)
		self.fname = Util.upath(fname)
		self.insdir = Util.upath(insdir)
		self.verbose = verbose
		#
		self.srcpath = '%s/%s' % (srcdir, fname)
		self.dstpath = '%s/%s' % (insdir, fname)
		self.is_newer = False
		#
		if self.verbose:
			print('%s:' % self.clsname)
			print('  src_path: %s' % self.srcpath)
			print('  dst_path: %s' % self.dstpath)

	##  Compare source and destination timestamps.
	#
	def check_timestamp(self):
		if not os.path.exists(self.dstpath):
			self.is_newer = True
			if self.verbose:
				print('  destination file does not exist')
			return
		src_mtime = os.stat(self.srcpath).st_mtime
		dst_mtime = os.stat(self.dstpath).st_mtime
		self.is_newer = src_mtime > dst_mtime
		if self.verbose:
			print('  src_mtime: %s' % src_mtime)
			print('  dst_mtime: %s' % dst_mtime)
			print('  is newer ? %s' % self.is_newer)

	##  Get control parameters.
	#
	def get(self, force=False):
		newer = True if force else self.is_newer
		return newer, self.srcpath, self.dstpath

# ----------------------------------------------------------------------
#  Test main
# ----------------------------------------------------------------------
from FileOp import *
if __name__ == '__main__':
	#
	def test(expect, force=False):
		ip.check_timestamp()
		newer, src, dst = ip.get(force)
		judge1 = 'newer' if newer else 'older'
		judge2 = 'OK' if newer == expect else 'NG'
		print('%s: %s, %s -> %s' % (judge1, src, dst, judge2))
		print()

	#
	srcdir = 'test'
	fname = 'ip_test.py'
	insdir = 'test/test'
	verbose = 1
	#
	fop = FileOp()
	fop.touch('%s/%s' % (srcdir, fname))
	fop.touch('%s/%s' % (insdir, fname))
	#
	ip = InstallParam(srcdir, fname, insdir, verbose)
	print()
	#
	print('-- older --')
	test(False)
	#
	print('-- force --')
	test(True, True)
	#
	print('-- newer --')
	fop.touch('%s/%s' % (srcdir, fname))
	test(True)
	#
	sys.exit(0)

# end: install_param.py
