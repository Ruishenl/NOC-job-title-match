import json
import os

with open('NOC_jd.json', 'r') as f:
    parsed_json = json.load(f)
for item in parsed_json:
    with open(os.path.join('resources/jds', item['id']+'_'+item['name'].replace('/','_') + '.txt'), 'w') as f:
        f.write(item['row'])
