def lfind(s, text, start=""):
	if start == "":
		start = (len(text) - 1) - text.find(s)
	pos = -1
	pos = len(text) -1 - text[::-1].find(s[::-1], start) + len(s) - 1
	return pos


cases = ['dfasdf asdfasdfa asdfasdf sdf@sdff asdfasd sdfasdf',
         'sadfd@jlkj @sfsdf flsjdfk@jkl', '', '@']
for case in cases:
    print(lfind('@', case))
    print(case[lfind('@', case)])
