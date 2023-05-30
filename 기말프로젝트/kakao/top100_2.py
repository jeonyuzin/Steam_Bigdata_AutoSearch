# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lA1Rk-X537vqbfoVmDA-M0kQv5xHqzZ1
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
import requests
import json






            
appno_prev=[]
try:
    f=open("./appno_prev_list.txt",'r')
    while True:
        a=f.readline()
        if a=="":
            break
        appno_prev.append(a.strip())
except Exception as e:
    print(e)

print(len(appno_prev))

options = webdriver.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
broswer = webdriver.Chrome('chromedriver', options=options)

# 페이지 이동
url = "https://store.steampowered.com/charts/topselling/KR"
broswer.get(url)

time.sleep(5)
print("스크롤 완")
#브라우저페이지를 읽어옴
#lxml은 구문을 분석하기 위한 파서
soup = BeautifulSoup(broswer.page_source, "lxml")

#게임리스트가있는 태그 id를 읽어옴
games_name = soup.find_all("div", attrs={"class": "weeklytopsellers_GameName_1n_4-"})
games_href=soup.find_all("a", attrs={"class": "weeklytopsellers_TopChartItem_2C5PJ"})
total=soup.find_all("tr", attrs={"class": "weeklytopsellers_TableRow_2-RN6"})
games_curr=soup.find_all("td", attrs={"class": "weeklytopsellers_RankCell_34h48"})



name_list=[]
appno_list=[]
curr_list=[]
real_price_list=[]
discount_per_list=[]
discount_price_list=[]



#https://store.steampowered.com/app/1238840/Battlefield_1?snr=1_7001_7005__7003
for i in games_href:
  temp=i['href']
  temp_split=temp.split('/')
  appno_list.append(temp_split[4])

for j in games_name:
  name_list.append(j.get_text())

for k in games_curr:
  curr_list.append(k.get_text())


for g in total:
  sale=""
  real=""
  disprice=""
  temp_sale=g.find("div", attrs={"class": "salepreviewwidgets_StoreSaleDiscountBox_2fpFv"})#세일유무판단
  if temp_sale!=None:
    temp_sale2=temp_sale.get_text()
    sale=temp_sale2
    temp_dis=g.find("div", attrs={"class": "salepreviewwidgets_StoreOriginalPrice_1EKGZ"})
    temp_dis2=temp_dis.get_text()
    disprice=temp_dis2
  temp_real=g.find("div", attrs={"class": "salepreviewwidgets_StoreSalePriceBox_Wh0L8"})
  if temp_real==None: #가격이 없는 경우 (미표시인 경우 ==무료 혹은 타 플랫폼 정책) 
    real=""
  else:
    real=temp_real.get_text()
  real_price_list.append(real)
  discount_per_list.append(sale)
  discount_price_list.append(disprice)




dif_list_temp=list(set(appno_list)-set((appno_prev)))
dif_list=list(set(dif_list_temp))
print(dif_list)

if len(dif_list)>=1:
  try:
    f=open("./appno_prev_list.txt",'a')
    for no in dif_list:
      f.write(no)
      f.write("\n")
    f.close()
  except Exception as e:
    print(e)
broswer.quit()
for a in dif_list:
  game_index=appno_list.index(a)
  send_name=name_list[game_index]
  send_curr=curr_list[game_index]
  send_real=real_price_list[game_index]
  send_dis_per=discount_per_list[game_index]
  send_dis=discount_price_list[game_index]
  send_data='게임 명 : '+send_name+' 현재 순위 : '+send_curr+'\n'+'현재가격 : '+send_real+' 할인율 : '+send_dis_per+' 할인 전'+send_dis
  send_url='https://store.steampowered.com/app/'+str(a)

