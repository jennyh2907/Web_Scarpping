#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 11:26:25 2021

@author: jennyhuang
"""
import pandas as pd
df = pd.read_excel("url_video.xlsx")
#print(df)
data_list=df.values.tolist()
url=""

import json
import matplotlib.pyplot as plt
import time
import requests
from bs4 import BeautifulSoup  

df_list = []
for i in range(0, 215):
    url = data_list[i][0]
    res = requests.get(url)

    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        } 
    res = requests.get(url, headers=my_headers)
    session = requests.session() 
    response = session.get(url)
    res.history[0].headers

    s = requests.session() 
    resp = s.get('https://index.taipeiads.com/select-category.php', headers=my_headers) 
    #print(resp.request.headers) `
    #print(resp.cookies)
    #print(resp.status_code)
    #print(resp.history)

    resp = s.get(url, headers=my_headers) 
    #print(resp.request.headers) 
    #print(resp.cookies)
    #print(resp.status_code)
    #print(resp.history)
    #print(resp.text)


    soup = BeautifulSoup(resp.text, 'lxml')
    js = soup.find_all("script")
    result = []
    for item in js:
        if len(item)> 0:
            if "chartData" in item.contents[0]:
                raw_string = str(item.contents[0]) 
                right_index = raw_string.rfind("*/") 
                clean_data = raw_string[right_index+2::].strip()
                result.append(clean_data)
                
    data = result[0]
    slice_data = data.split("chartData") 


    start = slice_data[1].find('{')
    end = slice_data[1].rfind('}') 
    result_json = json.loads(slice_data[1][start:end+1]) 
    result_json['item']

    df=pd.DataFrame(result_json['item'], columns=["Date", "what", "Low.", "Avg.", "High.", "what2"])
    df=df.drop('what', axis=1)
    df=df.drop('what2', axis=1)
    
    print(df)
    df_list.append(df.set_index("Date").T)
    print(len(df_list))
    time.sleep(3)

    plt.boxplot(df[df.columns[1:]])
    plt.xticks(list(range(1,1+len(df))), list(df["Date"]), rotation=60)
    plt.tight_layout()
    plt.savefig('video'+str(i)+'.png') 
    plt.show()
    
df_all = pd.concat(df_list,axis = 0)
df_all.to_excel("name.xlsx", index= True)


 
