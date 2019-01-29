#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# ======================================================================
#  CLASS:	Verbose(indent=2)
#
#  METHODS:
#	verbose(str msg, int level=0)
#	set_indent_amount(int amount)
#
# ----------------------------------------------------------------------
#  VERSION:
#	Ver 1.0  2019/01/29 F.Kanehori	Release version.
# ======================================================================
import sys
import os

##  Verbose message control class.
#
class Verbose:
	##  The initializer.
	#
	def __init__(self, verbose=-1, indent_width=2):
		self.clsname = self.__class__.__name__
		self.version = 1.0
		#
		self.verbose = verbose
		self.indent_width = indent_width
		#
		self.indent_level = 0
		self.indent_stuff = ' '

	def print(self, msg, level=0):
		if self.verbose >= level:
			print('%s%s' % (self.indent(), msg))

	def indent(self):
		width = self.indent_width * self.indent_level
		return self.indent_stuff * width

	def inc(self, value=1):
		self.indent_level += value

	def dec(self, value=1):
		self.indent_level -= value
		if self.indent_level < 0:
			self.indent_level = 0


if __name__ == '__main__':
	def test(level, inc=0, dec=0):
		verbose = Verbose(level)
		for range(inc): verbose.inc()
		for range(dec): verbose.dec()
		verbose.print('level -1', -1)
		verbose.print('level  0', 0)
		verbose.print('level  1', 1)
		verbose.print('level  2', 2)


	print('Verbose(-1)')
	test(-1)
	print()

	print('inc indent')
	print('Verbose(0, inc=1)')
	test(0, inc=1)
	print()

	print('inc indent')
	print('Verbose(1)')
	test(1, inc=2)
	print()

	print('dec indent')
	print('Verbose(2)')
	test(2, inc=2, dec=1)
	print()


# end: Verbose.py
