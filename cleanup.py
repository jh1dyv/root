#! C:/Python34/python
# -*- coding: UTF-8 -*-
# ==============================================================================
#  SYNOPSIS:
#       cleanup [options] paths...
#       options:
#           -d N, --days N      N 日より前のファイルを削除する
#           -r, --recurse       サブディレクトリも処理する
#           -e, --execute       削除を実行する（default: リストのみ）
#           
#  DESCRIPTION:
#       引数で指定されたファイルを削除する. 引数 -e を指定しないときは削除は
#       実行せずに, 削除対象となるファイルをリストアップする.
#
#  Version:
#     Ver 1.00  2014/11/20 F.Kanehori	初版
#     Ver 1.01  2015/02/08 F.Kanehori	Displays file time as well as date
#     Ver 1.02  2019/02/04 F.Kanehori	Change python path.
#     Ver 1.021 2020/12/02 F.Kanehori	Bug fixed.
# ==============================================================================
version = 1.021
import os
import sys
import optparse
import glob
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
import errno

#-------------------------------------------------------------------------------
# Globals and Constants
#
prog = os.path.basename(sys.argv[0]).split('.')[0]

#-------------------------------------------------------------------------------
# Options
#
parser = optparse.OptionParser('Usage: %prog [options] paths...')
parser.add_option('-d', '--days', action="store", dest='days', type='int',
                    default=1, metavar='N', help='remove files older than N days')
parser.add_option('-r', '--recurse', action="store_true", dest='recurse',
                    default=False, help='recurse into subdirectories')
parser.add_option('-e', '--execute', action="store_true", dest='execute',
                    default=False, help='execute file removal (default is list only)')
parser.add_option('-v', '--verbose', action="count", dest='verbose',
                    default=0, help='set verbose mode')
parser.add_option('-V', '--version', action="store_true", dest='version',
                    default=False, help='show version info')
options, remainder = parser.parse_args(sys.argv[1:])
#
if options.version:
    print('%s: Version %s' % (prog, version))
    exit(0)

#-------------------------------------------------------------------------------
#
#
def append_uniq(list, elem):
    if not elem in list:
        list.append(elem)
        #print('  append:', elem)

def make_filelist(list, path):
    if options.verbose > 1: print('make_filelist: enter', path, list)
    L = []
    if path.find('*') >= 0:
        for file in glob.glob(path):
            append_uniq(L, file)
    else:
        append_uniq(L, path)
    #
    if options.verbose > 1: print('make_filelist: ----')
    for file in L:
        if os.path.isdir(file):
            if options.recurse:
                make_filelist(files, file + '\*')
                files.append(file)
        else:
            append_uniq(files, file)
    if options.verbose > 1: print('make_filelist: exit ', list)

def comma_separated(num, chunk):
    div = 10 ** chunk
    chunks = []
    while num > 0:
        chunks.append(num % div)
        num = int(num / div)
    chunks.reverse()
    s = ''
    for n in chunks:
        if n == chunks[0]:
            s = str(n)
        else:
            s += ',' + '{0:03d}'.format(n)
    if s == '': s = '0'
    return s

#-------------------------------------------------------------------------------
# Main process
#
if options.verbose:
    print('%s: remove files older than %d day(s)' % (prog, options.days))

# list up target files
#
files = []
for path in remainder:
    make_filelist(files, path)

# prepare comparison
#
oneday = (date(1970,1,2) - date(1970,1,1)).total_seconds()
offset = oneday * options.days
del_date = time.time() - offset
if options.verbose:
    print('today: ', '{0:12.1f}'.format(time.time()))
    print(' days: ', '{0:12.1f}'.format(offset))
    print(' base: ', '{0:12.1f}'.format(del_date))

# determine files to be deleted
#
del_files = []
for file in files:
    if file in remainder: continue
    try:
       	ftime = os.path.getmtime(file)
       	if ftime <= del_date:
       	    del_files.append(file)
    except PermissionError as e:
        	print('PermissionError: "%s": %s' % (file, e))
    except FileNotFoundError as e:
        	print('FileNotFoundError: "%s": %s' % (file, e))

# make listing
#
count = 0
size = 0
count_all = 0
print('target files:')
for file in files:
    try:
        ftime = os.path.getmtime(file)
    except PermissionError:
        print('  access denied: ' + file)
        continue
    except FileNotFoundError:
        print('  file not found: ' + file)
        continue
    ftime_str = str(datetime.fromtimestamp(ftime))[0:19].replace('-', '/')
    mark = ' '
    if file in del_files:
        mark = 'D'
        count += 1
        size += os.path.getsize(file)
    print('  ' + ftime_str + ' ' + mark + '  ' + file)
    count_all += 1

if options.verbose > 1: print('size =', size)
print('total:', count, 'files,', comma_separated(size, 3), 'bytes will be removed'
    + ' (' + str(count_all - count) + ' files remained)')

# execute file deletion
#
if options.execute:
    print('option --execute specified')
    f_count = 0
    d_count = 0
    for f in del_files:
        try:
            if os.path.isdir(f):
                os.rmdir(f)
                print('  removing ' + f + '\\')
                d_count += 1
            else:
                print('  removing ' + f)
                os.unlink(f)
                f_count += 1
        except IOError as e:
            if e.errno == 13:
                print('PermissionError: %d: %s' % (e.errno, e.strerror))
        except exception as e:
            print(repr(e))
    print('total:', f_count, 'files,', d_count, 'directories removed')

# end of process
if options.verbose:
    print(prog + ': done')
exit(0)

# end: cleanup.py
