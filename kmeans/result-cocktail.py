#!/user/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import json
import re
cluster_data = pd.read_csv(r'.\cocktail\model\kmeans_matrix_0824.csv',encoding='utf8')
cluster = cluster_data['cluster']
c = []
for i in cluster:
    if i == 0:
        i = ['Mellow']#香醇
        c.append(i)
    if i == 1:
        i = ['little','simple'] #純酒類、酒感重
        c.append(i)
    if i == 2:
        i =  ['classic','original','rich'] #經典調酒
        c.append(i)
    if i == 3:
        i =['orange','strong'] #苦橙味
        c.append(i)
    if i == 4:
        i = ['refreshing'] #清爽感
        c.append(i)
    if i == 5:
        i =['sour','sweet'] # 酸甜
        c.append(i)
    if i == 6:
        i =['balanced','light'] #輕酒感
        c.append(i)
    if i == 7:
        i = ['bittersweet','herbal'] #藥草苦甜味
        c.append(i)

cluster_data['cluster'] = c
#==================清洗食譜資料====================
base_data = pd.read_csv(r'.\cocktail\cocktail_all_08924_class_combine.csv', encoding='utf8')

base_data['step'] = [str(i).capitalize().replace('[','').replace(']','').strip()  for i in base_data['step']]
base_data['ins'] = [str(i).capitalize().replace('[','').replace(']','').strip()  for i in base_data['ins']]

#==================清洗食譜資料====================
data=[]
for row in base_data['recipe']:
    row = row.replace('{','').replace('}','').replace('"','').replace('[','').replace(']','').strip().split(',')
    recipe = []
    for t in row :
        tmp_dict = {}
        # print(type(t))
        t = t.strip().strip('\'').strip()

        if len(t) != 0:
            t_key = t.split(':')[0].strip()
            if  t_key[-1] == '\'':
                t_key = t_key.strip('\'')

            t_val = t.split(':')[1].strip()
            if t_val[0] == '\'':
                t_val = t_val.strip('\'')
            tmp_dict[t_key] = t_val

        else:
            t_key = t.split(':')[0].strip()

            tmp_dict[t_key] = 'NAN'
            continue
        recipe.append(tmp_dict)
    data.append(recipe)
base_data['recipe'] = [i for i in data]
# print(base_data['recipe'])
# # # #存成csv檔--------------------------------------------------
result = pd.merge(base_data.iloc[:, :7] ,cluster_data.iloc[:, -1] ,left_index = True, right_index = True, how = 'outer')
result = result.drop('comment',axis=1)
result.to_csv(r'.\cocktail\cocktail_all_0828_cluster.csv', encoding='utf-8-sig', index=False)
# # # 刪除沒有照片的資料--------------------------------------------------
indexNames = result[result['pic'].isnull()].index
result.drop(indexNames , inplace=True)
result.to_csv(r'.\cocktail\cocktail_all_0828_cluster_pic.csv',encoding='utf-8-sig',index=False)

# #存成json檔--------------------------------------------------
js001 = result.to_json(force_ascii=False, orient='records',indent = 4)
# print(js001)
# with open(r'.\cocktail\model\cocktail_cluster.json', 'w',encoding='utf-8-sig') as f:
#     f.write(js001)
with open(r'.\cocktail\model\cocktail_cluster_pic.json', 'w',encoding='utf-8-sig') as f:
    f.write(js001)
# #
#存成mongodb--------------------------------------------------
from pymongo import MongoClient
import json

uri = f'mongodb://sh41bee:eb102@35.194.165.27:27017/'
client = MongoClient(uri)
db = client['cocktail'] #db名
collections = db['cocktail_cluster__pic']

with open(r'.\cocktail\model\cocktail_cluster_pic.json', 'r',encoding='utf-8-sig') as f:
    output = json.load(f)
    # print(output)
    data= []
    data.extend(output)
    collections.insert_many(data)
    client.close() #關閉連接


uri = f'mongodb://sh41bee:eb102@35.194.165.27:27017/'
client = MongoClient(uri)
db = client['cocktail'] #db名
collection = db['cocktail_cluster']
#---------------------------------------------------------------

for item in collection.find():
    detail = item['recipe']
    # print(detail[0])