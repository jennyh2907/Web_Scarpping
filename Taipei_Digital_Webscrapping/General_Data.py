#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 14:12:15 2021

@author: jennyhuang
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
res = requests.get("https://index.taipeiads.com/")
print(res.text)

from bs4 import BeautifulSoup
soup = BeautifulSoup(res.text, 'lxml')
js = soup.find_all("script")
print(js)

result = []
#print(result)

for item in js:
  if len(item)> 0:
    if "chartData" in item.contents[0]:
      #print(item.contents)
      result.append(item.contents[0])
print(result)

start = result[0].find('{')
end = result[0].find('}')
result_json = eval(result[0][start:end+1])
result_json

result_json['item']

df=pd.DataFrame(result_json['item'], columns=["Date", "Search CPC", "Display CPC", "Video CPV", "what"])
print(df)
df=df.drop('what', axis=1)
print(df)
df.to_excel('file.xlsx')

#import matplotlib.pyplot as plt
df.plot(kind='bar')
plt.xticks(list(range(1,1+len(df))), list(df["Date"]), rotation=60)
plt.tight_layout()
plt.savefig('總體.png') 
plt.show()
