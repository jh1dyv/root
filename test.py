import sys
import os

verbose = 0
kludge = b'\\KLUDGE '

def codelen(code):
	nb = 1
	if   code >= 240: nb = 4
	elif code >= 224: nb = 3
	elif code >= 192: nb = 2
	return nb

def mark_kanji(string):
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

strs = ['alphabet 漢字 alphabet 漢字 alphabet',
	'漢字 alphabet 漢字 aplphabet 漢字'	]

for n in range(len(strs)):
	print('----')
	in_str = strs[n]
	print('inp: %s' % in_str)
	out_str = mark_kanji(in_str)
	print('out: %s' % out_str)

sys.exit(0)
