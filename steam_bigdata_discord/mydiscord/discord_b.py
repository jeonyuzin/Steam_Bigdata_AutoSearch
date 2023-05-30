# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
import requests
import json
import discord
from discord.ext import commands
import datetime
import asyncio

intents=discord.Intents.all() 
bot = commands.Bot(command_prefix='!',intents=intents)

name_list=[]
appno_list=[]
curr_list=[]
real_price_list=[]
discount_per_list=[]
discount_price_list=[]
url_list=[]



def data_call():
  name_list.clear()
  appno_list.clear()
  curr_list.clear()
  real_price_list.clear()
  discount_per_list.clear
  discount_price_list.clear()
  url_list.clear()            

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
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')        # Head-less 설정
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  broswer = webdriver.Chrome('chromedriver', options=options)
  # 페이지 이동
  url = "https://store.steampowered.com/charts/topselling/KR"
  broswer.get(url)
  time.sleep(5)
  #브라우저페이지를 읽어옴lxml은 구문을 분석하기 위한 파서
  soup = BeautifulSoup(broswer.page_source, "lxml")
  #게임리스트가있는 태그 id를 읽어옴
  games_name = soup.find_all("div", attrs={"class": "weeklytopsellers_GameName_1n_4-"})
  games_href=soup.find_all("a", attrs={"class": "weeklytopsellers_TopChartItem_2C5PJ"})
  total=soup.find_all("tr", attrs={"class": "weeklytopsellers_TableRow_2-RN6"})
  games_curr=soup.find_all("td", attrs={"class": "weeklytopsellers_RankCell_34h48"})
    
  #https://store.steampowered.com/app/1238840/Battlefield_1?snr=1_7001_7005__7003
  for i in games_href:
    temp=i['href']
    url_list.append(temp)
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
    temp_real=g.find("div", attrs={"class": "salepreviewwidgets_StoreSalePriceBox_Wh0L8"})
    if temp_sale!=None:
      temp_sale2=temp_sale.get_text()
      sale=temp_sale2
      temp_dis=g.find("div", attrs={"class": "salepreviewwidgets_StoreOriginalPrice_1EKGZ"})
      temp_dis2=temp_dis.get_text()
      disprice=temp_dis2
    if temp_real==None: #가격이 없는 경우 (미표시인 경우 ==무료 혹은 타 플랫폼 정책) 
      real="Free To Play"
    else:
      real=temp_real.get_text()
    real_price_list.append(real)
    discount_per_list.append(sale)
    discount_price_list.append(disprice)
    
  dif_list_temp=list(set(appno_list)-set((appno_prev)))
  dif_list=list(set(dif_list_temp))
  broswer.quit()
  if len(dif_list)>=1:
    try:
      f=open("./appno_prev_list.txt",'a')
      for no in dif_list:
        f.write(no)
        f.write("\n")
      f.close()
    except Exception as e:
      print(e)
  return dif_list

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
    await schedule_daily_message()


#timer message
async def schedule_daily_message():
  while True:
    now_h=datetime.datetime.now().hour
    now_m=datetime.datetime.now().minute
    if not((now_h==12 or now_h==0) and now_m==0):
      await asyncio.sleep(60)
      continue
    channel=bot.get_channel(채널주소) 
    await channel.send("일일 갓겜 자동 검색 ")
    try:
      await channel.send('데이터 확인중 기다리셈')
      #초기화 및 데이터 로딩
      data_list=data_call()
      #=========================
      if len(data_list)>=1:
        await channel.send(str(len(data_list))+'개 데이터 확인')
        for a in data_list:
          game_index=appno_list.index(a)
          send_name=name_list[game_index]
          send_curr=curr_list[game_index]
          send_real=real_price_list[game_index]#현재가
          send_dis_per=discount_per_list[game_index]#할인률
          send_dis=discount_price_list[game_index]#원가
          send_url=url_list[game_index]
          send_data='게임 명 : '+send_name+' 현재 순위 : '+send_curr+'\n'+'현재가격 : '+send_real+', 원가 : '+send_dis
          await channel.send(send_data)
          await channel.send(send_url)
          asyncio.sleep(2)
      else:
        await channel.send('신규 데이터 없음')
    except Exception as e:
        print(e)
        await channel.send('에러')
    #분 중복방지로 1분대기
    await asyncio.sleep(60)   
    
@bot.command()
async def steam(message):
    if (message.channel.id==특정채널이면 or message.channel.id==특정채널이면):
      try:
        await message.channel.send('데이터 확인중 기다리셈')
        #초기화 및 데이터 로딩
        data_list=data_call()
        #===================
        if len(data_list)>=1:
          await message.channel.send(str(len(data_list))+'개 데이터 확인')
          for a in data_list:
            game_index=appno_list.index(a)
            send_name=name_list[game_index]
            send_curr=curr_list[game_index]
            send_real=real_price_list[game_index]#현재가
            send_dis_per=discount_per_list[game_index]#할인률
            send_dis=discount_price_list[game_index]#원가
            send_url=url_list[game_index]
            send_data='게임 명 : '+send_name+' 현재 순위 : '+send_curr+'\n'+'현재가격 : '+send_real+', 원가 : '+send_dis
            await message.channel.send(send_data)
            await message.channel.send(send_url)
            await asyncio.sleep(2)
        else:
          await message.channel.send('신규 데이터 없음')
      except Exception as e:
        print(e)
        await message.channel.send('에러')
              
 
bot.run('MTA2MDEzMjA1MTI3NTIzOTQyNA.Gc2VA6.wEz71EuH9y7TsGKFuMIrNwTpD294Cu5uBeAKhw')
