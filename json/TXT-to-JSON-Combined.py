import os
import json

i = 0
main_dir = os.getcwd()
directories = []
for a, b, c in os.walk(os.getcwd()):
    directories.append(a)
combined_string = ''
for k in directories:
    os.chdir(k)
    try:
        with open('data.txt', 'r') as f:
            x = f.read()
    except:
        continue
    x1=x.replace('{\n"image"', '{"image"').replace('[','').replace(']','').replace('.jpg"}, \n{"large":', '.jpg",\n"large":').replace('.jpg"}, {"large":', '.jpg",\n"large":')
    while '{"image"' in x1:
        i += 1
        ind=x1.find('{"image":')
        x1 = x1[:ind] + '"' + str(i) + '":{"photo' + x1[ind+7:]
    x1 = '{' + x1 + '}'
    last_comma = x1.rfind(',')
    x1 = x1[:last_comma] + x1[last_comma+1:]
    try:
        new_json = json.loads(x1)
        new_string = json.dumps(new_json, indent=4)[1:-1]
        if new_string[-1] != ',':
            new_string = new_string[:-1] + ','
        combined_string += new_string
    except:
        continue
    #print(x1)
os.chdir(main_dir)
try:
    final_json = json.loads('{' + combined_string + '}')
    with open('all_data_combined.txt', 'w') as f:
        f.write(json.dumps(final_json, indent=4))
except:
    print('failled in final')
    with open('combined_string2.txt', 'w') as f:
        f.write(combined_string)
