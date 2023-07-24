import json
x = input("请输入路径：（不包括后缀名）")
filepath1 = '{}.json'.format(x)
filepath2 = '{}.py'.format(x)
with open(filepath1, 'r', encoding='utf8')as fp:
    json_data = json.load(fp)

with open(filepath2, 'w', encoding='utf8') as fpp:
    for i in range(len(json_data['cells'])):
        tmp = json_data['cells'][i]
        if tmp['cell_type']=='code':
            for s in tmp['source']:
                if s != '\n':
                    fpp.write(s)
            fpp.write('\n\n')
print("done")
