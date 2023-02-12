#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 11:15:11 2021

@author: jennyhuang
"""

#整理網址結構
category_match={
    "1":"汽車", 
    "2":"教育/職涯規劃",
    "3":"民生消費品",
    "4":"娛樂",
    "5":"金融保險",
    "6":"政府",
    "7":"健康相關",
    "10":"房地產", 
    "11":"零售",
    "12":"科技",
    }
detailed_category_match={
    "1.01":"新車",
    "2.01":"教育",
    "3.01":"美妝",
    "3.02":"個人用品",
    "3.03":"食品",
    "3.04":"飲料",
    "3.05":"家庭用品",
    "3.06":"餐飲",
    "3.07":"其他民生消費品",
    "4.01":"遊戲",
    "4.02":"電影",
    "5.02":"銀行",
    "5.05":"投資理財",
    "5.06":"房屋貸款",
    "6.01":"政府單位相關",
    "7.01":"減肥健身",
    "7.02":"健康產品",
    "7.04":"製藥/藥品",
    "10.01":"建商",
    "11.01":"服飾配件",
    "11.02":"消費電子用品",
    "11.05":"雜貨商店",
    "11.08":"寵物相關",
    "12.01":"硬體",
    }
c_match=["1.01", "2.01", "3.01","3.02", "3.03", "3.04", "3.05","3.06",
         "3.07", "4.01", "4.02","5.02","5.05","5.06","6.01","7.01",
         "7.02","7.04","10.01","11.01","11.02","11.05","11.08","12.01"]

campaign1=["SEARCH", "DISPLAY", "VIDEO"]

search_tag=["Brand", "ProductModel", "Universal", "CompetitiveProduct", "DSA", "RLSA", "SUSC", "SUAC", "SOthers"]
display_tag=["ContextualTargeting", "Interests", "Topics", "Placement", "RMKT", "DUAC", "Gmail", "DOthers"]
video_tag=["Video", "VUAC", "VOthers"]

search_campaign=["CPC", "CTR"]
display_campaign=["CPC", "CTR", "CPM"]
video_campaign=["CPV", "VTR", "CPM"]

url_list=[]
url_list1=[]
url_list2=[]


for i in range(0, 24):
        for j in range(0, 2):
            for k in range(0, 9):
                link = str("https://index.taipeiads.com/select-category.php/year-data.php?type1="+c_match[i]+"&duration=2021-06&campaign1=SEARCH&campaign2="+search_campaign[j]+"&tag=APIndex_"+search_tag[k])
                url_list.append(link)
                print(link)

for i in range(0, 24):
        for j in range(0, 3):
            for k in range(0, 8):
                link = str("https://index.taipeiads.com/select-category.php/year-data.php?type1="+c_match[i]+"&duration=2021-06&campaign1=DISPLAY&campaign2="+display_campaign[j]+"&tag=APIndex_"+display_tag[k])
                url_list1.append(link)
                print(link)

for i in range(0, 24):
        for j in range(0, 3):
            for k in range(0, 3):
                link = str("https://index.taipeiads.com/select-category.php/year-data.php?type1="+c_match[i]+"&duration=2021-06&campaign1=VIDEO&campaign2="+video_campaign[j]+"&tag=APIndex_"+video_tag[k])
                url_list2.append(link)
                print(link)

import pandas as pd
df = pd.DataFrame(url_list)
df.to_excel('output.xlsx', header=False, index=False)

df = pd.DataFrame(url_list1)
df.to_excel('url_display.xlsx', header=False, index=False)

df = pd.DataFrame(url_list2)
df.to_excel('url_video.xlsx', header=False, index=False)

    
import itertools
itertools.product(search_campaign, search_tag)
p_list1=list(itertools.product(search_campaign, search_tag))
list(p_list1)