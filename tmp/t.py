import sys
import re

line = '\\section{SECTION}'
patt = r'\\section\{([^\}]*)\}'
print(patt)

m = re.search(patt, line)
if m:
	print(m.group(0))
	print(m.group(1))

sys.exit(0)
