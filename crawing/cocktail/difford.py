import requests
from bs4 import BeautifulSoup
import json
import time
import re
import pandas as pd


#-------------------------------------------------------------------------------------------------------------------------------------------
df = pd.DataFrame(
    columns=['酒名', '酒譜', 'url','圖片','步驟', '介紹', '評論'])
store_details = {'name': '', 'ingredient': '', 'url': '','pic_url': '', 'step': '', 'instruction': '', 'review': ''}
all = []
#-------------------------------------------------------------------------------------------------------------------------------------------

for page in range(0,93):#總共93 16-31
    url = 'https://www.diffordsguide.com/cocktails/search?rating=3%2C3.5%2C4%2C4.5%2C5%2C5.5&sort=name&offset={}&limit=48'.format((str(page*48)))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    res = requests.get(url=url, headers=headers) #
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    info = soup.select('div[class="cell main-content"] div[class="grid-x grid-margin-x grid-margin-y pad-bottom"] a')
    # print(info)
    for c in info:
        c_url = 'https://www.diffordsguide.com' + c['href']
        print(c_url)
        name = c.select('h3[class="box__title"]')[0].text

# 圖片-------------------------------------------------------------------------------------------------------
        pic_url = c.select('div[class="box__image-aspect"] img')[0]['src']

# -----------------------------------------------------------------------------------------------------
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Cookie': 'diffordsguide_com=0qpkkk3iqc27brdiopm0bb5vbu; __asc=ebc9258e17303be738be8dc8998; __auc=ebc9258e17303be738be8dc8998; _ga=GA1.2.331797616.1593495680; _gid=GA1.2.1387957266.1593495680; _fbp=fb.1.1593495680301.1086156574; diffordsguide_com_subscribe=1; _gat_gtag_UA_6108581_5=1',
        'Refer':str(c_url)}
        data = {'display':'fl oz'}

        res = requests.get(url=c_url, headers=headers, data=data)#如果是formdata 就要帶入files
        soup = BeautifulSoup(res.text,'html.parser')

#步驟-------------------------------------------------------------------------------------------------------
        step_info = soup.select('div[class="grid-x grid-margin-y"] div[class="cell small-8 medium-12"] div[class="cell"]')[2:3]
        step = [i.select('p')[0].text.strip() for i in step_info]
        if len(step) == 0:
            try:
                step_info = soup.select(
                    'div[class="grid-x grid-margin-y"] div[class="cell small-8 medium-12"] div[class="cell"]')[1:2]
                step = [i.select('p')[0].text.split('\r')[0] for i in step_info]
            except IndexError as e:
                step = 'null'
# 官方介紹------------------------------------------------------------------------- ------------------------------
        try:
            instruction_info = soup.select('div#sticky-anchor div[class="grid-x grid-margin-x"] article[class="cell small-12 medium-8 long-form long-form--small long-form--item long-form--inline-paragraph pad-bottom"] div[class="grid-x grid-margin-y"]  div[class="cell"]')[5:6]
            instruction = [i.select('p')[0].text.strip() for i in instruction_info]
            store_details['instruction'] = instruction[0]
        except IndexError as e:
            try:
                instruction_info = soup.select('div#sticky-anchor div[class="grid-x grid-margin-x"] article[class="cell small-12 medium-8 long-form long-form--small long-form--item long-form--inline-paragraph pad-bottom"] div[class="grid-x grid-margin-y"]  div[class="cell"]')[6:7]
                instruction = [i.select('p')[0].text.strip() for i in instruction_info]
                store_details['instruction'] = instruction[0]
            except IndexError as e:
                try:
                    instruction_info = soup.select(
                        'div#sticky-anchor div[class="grid-x grid-margin-x"] article[class="cell small-12 medium-8 long-form long-form--small long-form--item long-form--inline-paragraph pad-bottom"] div[class="grid-x grid-margin-y"]  div[class="cell"]')[
                                       11:12]
                    instruction = [i.select('p')[0].text.strip() for i in instruction_info]
                    store_details['instruction'] = instruction[0]
                except IndexError as e:
                    try:
                        instruction_info = soup.select(
                            'div#sticky-anchor div[class="grid-x grid-margin-x"] article[class="cell small-12 medium-8 long-form long-form--small long-form--item long-form--inline-paragraph pad-bottom"] div[class="grid-x grid-margin-y"]  div[class="cell"]')[
                                           12:13]
                        instruction = [i.select('p')[0].text.strip().replace('\'', '') for i in instruction_info]
                        store_details['instruction'] = instruction[0]
                    except IndexError as e:
                        store_details['instruction'] = 'null'

# 酒譜材料-------------------------------------------------------------------------------------------------------
        ing_info = soup.select(' table[class="no-margin ingredients-table"] tbody tr')[:-1]
        ing_amount = [ia.select('td[class="no-wrap td-min-width td-align-top pad-right"]')[0].text.strip().replace('fl oz','oz') for ia in ing_info]
        ing_name_list = []
        for ia in ing_info:
            try:
                iname = ia.select('td[class="td-align-top"]')
                ing_name = [iname[0].text.strip()]
                ing_name_list.append(ing_name[0])
            except IndexError as e :
                ing_namebottom = ia.select('td[class="td-align-top pad-bottom"]')
                ing_name = [ing_namebottom[0].text.strip()]
                ing_name_list.append(ing_name[0])
        ingredient = dict(zip(ing_name_list, ing_amount))
# 網友評論-------------------------------------------------------------------------------------------------------
    #評論在json 檔 取得json位址
        re_id = [m.group() for m in re.finditer(re.compile(r'\d+'), c_url)][0]

        re_url = 'https://www.diffordsguide.com/api/comment/read/cocktails/{}?link_table=cocktails&link_id={}&_a=1'.format(
            str(re_id), str(re_id))

        res = requests.get(re_url, headers=headers)
        json_data = json.loads(res.text)
        try:
            comment_name = [[t['comment']] for t in json_data]
            if len(comment_name) != 0:
                store_details['review'] = comment_name
            else:
                store_details['review'] = 'null'
        except KeyError as k:
            try:
                for t in json_data:
                    comment_name = [[i['comment']] for i in t['replies']]
                    if len(comment_name) != 0:
                        store_details['review'] = comment_name
                    else:
                        store_details['review'] = 'null'
            except KeyError as k:
                store_details['review'] = 'null'

        store_details['name'] = name
        store_details['pic_url'] = pic_url
        store_details['ingredient'] = ingredient
        store_details['url'] = c_url
        store_details['step'] = step[0]
        # store_details['instruction'] = instruction[0]
        # time.sleep(1)
        # print(store_details)
        each = list(store_details.values())  # 取每個網站的資訊

        all.append(each)  # 將所有網站的資訊丟入同一個list中

    print('page:',page)
    dff = df = pd.DataFrame(all,columns=['酒名', '酒譜', 'url','圖片','步驟', '介紹', '評論'])

    a_df = dff.drop_duplicates('url')
    a_df.to_csv(r'./cocktail/cocktail_difford_all.csv', index=False, encoding="utf-8-sig")
