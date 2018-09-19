
import sys
import os
import glob
sys.path.append('../../src/RunSwig/pythonlib')
from FileOp import *
from Proc import *
from Util import *
from Error import *

prog = sys.argv[0].split(os.sep)[-1].split('.')[0]

verbose = 1

wrkdir = 'tmp'
main = 'main_html.tex'
nkf = 'nkf'
python = 'python'
plastex = 'c:/Python36/Scripts/plastex'

shell = True if Util.is_unix() else False

# Create work space.
if os.path.exists(wrkdir) and not os.path.isdir(wrkdir):
	msg = '%s exists but not a directory' % wrkdir
	Error(prog).abort(msg)
os.makedirs(wrkdir, exist_ok=True)

# Clear work space.
fop = FileOp()
fop.rm('%s/*' % wrkdir)

# Copy files to work space.
texsrcs = glob.glob('*.tex')
texsrcs.extend(glob.glob('*.sty'))
for f in texsrcs:
	cmnd = '%s -w %s' % (nkf, f)
	outf = '%s/%s' % (wrkdir, f)
	if verbose:
		print('converting %s' % f)
	rc = Proc().execute(cmnd, stdout=outf, shell=shell).wait()
	if rc != 0:
		msg = 'kanji conversion failed: "%s"' % f
		Error(prog).abort(msg)
#
others = glob.glob('*.cls')
others.extend(['en', 'fig'])
for f in others:
	if verbose:
		print('copying %s' % f)
	rc = FileOp().cp(f, '%s/%s' % (wrkdir, f))
	if rc != 0:
		msg = 'file copy failed: "%s"' % f
		Error(prog).abort(msg)

# Generating htmls.
cwd = os.getcwd()
os.chdir(wrkdir)
cmnd = '%s %s %s' % (python, plastex, main)
rc = Proc().execute(cmnd, shell=shell).wait()
os.chdir(cwd)
if rc != 0:
	msg = 'generating html failed'
	Error(prog).abort(msg)

sys.exit(0)

"""
Dir.chdir("/export/home/WWW/docroots/springhead/doc/SprManual")

Dir.mkdir("tex_orig") unless File.directory?("tex_orig")

system("cp -a *.tex *.sty tex_orig")

Dir["tex_orig/*"].each do |file|
  system("/bin/cat #{file} | /bin/sed -e 's/\{sourcecode\}/\{verbatim\}/' | /usr/bin/nkf -w > #{file[9..-1]}")
end

system("/usr/bin/plastex main_html.tex")

"""
