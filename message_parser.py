#!/usr/bin/python

from bs4 import BeautifulSoup
from lxml import etree
from csv import DictWriter
from os.path import exists
import pandas as pd


fields = ['date', 'time', 'description']

if not exists("messages.csv"):
    with open("messages.csv", "w") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=fields)
        dictwriter_object.writeheader()
        
with open('messages/messages.html', 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    dom = etree.HTML(str(soup))

messages = dom.xpath("//div[@class='history']/div[contains (@class, 'message default clearfix')]")
    
for message in range(1):
    text_clean = []
    
    text_raw = dom.xpath(f"//div[@class='history']/div[contains (@class, 'message default clearfix')][{message + 1}]//div[@class='text']//text()")
    
    for text in text_raw:
        text_clean.append(text.strip().replace("\n", "").replace("  ", ""))
        
    description = " ".join(text_clean)
        
    date, time, _ = dom.xpath("//div[@class='history']/div[contains (@class, 'message default clearfix')][1]//div[@class='pull_right date details']//@title")[0].split(" ")
    
    
    
    dict = {'date': date, 'time': time, 'description': description}      

    with open("messages.csv", "a") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=fields)
        dictwriter_object.writerow(dict)
        
        f_object.close()
        

        
df_state = pd.read_csv("messages.csv")
df_state[df_state.duplicated()]
df_state.drop_duplicates(keep='first',inplace=True)
        
    
print("-------------------------------------")
print(f"text: {description}")
print("-------------------------------------")
print(f"date: {date}")
print("-------------------------------------")
print(f"time: {time}")
print("-------------------------------------")
    