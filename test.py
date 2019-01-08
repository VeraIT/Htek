import re
serach = re .search(r'Registered', '1008@192.168.0.107:5060 : Registered; UDP')
print(type(serach))
if serach:
	print(serach.group())

match = re .match(r'Registered', 'Registered; UDP')
print(type(match))
if match:
	print(match.group())

findall = re .findall(r'Registered', '1008@192.168.0.107:5060 : Registered; UDP 5060 : Registered; UDP 1008@192.168.0.107:5060 : Registered')
print(len(findall))
for i in range(len(findall)):
	print(i,findall[i])

split = re .split(r'Registered', '1008@192.168.0.107:5060 : Registered; UDP 5060 : Registered; UDP 1008@192.168.0.107:5060 : Registered',maxsplit=2)
for i in range(len(split)):
	print(i,split[i])

finditer = re.finditer(r'Registered', '1008@192.168.0.107:5060 : Registered; UDP 5060 : Registered; UDP 1008@192.168.0.107:5060 : Registered')
print(type(finditer))
for m in finditer:
	print(i,m.group(0))

sub= re.sub(r'Registered','ok', '1008@192.168.0.107:5060 : Registered; UDP 5060 : Registered; UDP 1008@192.168.0.107:5060 : Registered')
print(sub)

pat = re.compile(r'Registered')
search = pat.search('1008@192.168.0.107:5060 : Registered; UDP 5060 : Registered; UDP 1008@192.168.0.107:5060 : Registered')
if serach:
	print(search.group())


import re
pattern = re.compile(r'你好')
str = '你好吗'
print(pattern.search(str))