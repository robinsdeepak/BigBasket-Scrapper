import os
import json

for a, b, c in os.walk(os.getcwd()):
	directories.append(a)

for k in directories:
	os.chdir(k)
	try:
		with open('data.txt', 'r') as f:
			x = f.read()
	except:
		continue;
	i=0
	x1=x.replace('{\n"image"', '{"image"').replace('[','').replace(']','').replace('.jpg"}, \n{"large":', '.jpg",\n"large":').replace('.jpg"}, {"large":', '.jpg",\n"large":')
	while '{"image"' in x1:
		i += 1
		ind=x1.find('{"image":')
		x1 = x1[:ind] + '"' + str(i) + '":{"photo' + x1[ind+7:]
	x1 = '{' + x1 + '}'
	last_comma = x1.rfind(',')
	x1 = x1[:last_comma] + x1[last_comma+1:]
	newx = json.loads(x1)
	
	with open('data.txt', 'w') as f:
		f.write(json.dumps(newx, indent=4))
