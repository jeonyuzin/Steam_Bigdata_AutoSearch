from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
import sys



options = webdriver.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
broswer = webdriver.Chrome('chromedriver', options=options)
broswer.set_script_timeout(30)
# 페이지 이동
url = "https://store.steampowered.com/search/Steam?category1=998&supportedlang=koreana%2Cenglish&ndl=1"
broswer.get(url)

interval = 2 # 2초에 한번씩 스크롤 내림

# 현재 문서 높이를 가져와서 저장
prev_height = broswer.execute_script("return document.body.scrollHeight")

# 반복 수행
while True:
    try:
        a=broswer.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
        time.sleep(interval)
        b=curr_height = broswer.execute_script("return document.documentElement.scrollHeight")
        print(a,b)
        if curr_height == prev_height:
            break
        prev_height=curr_height
    except:
        pass



print("스크롤 완")
#브라우저페이지를 읽어옴
#lxml은 구문을 분석하기 위한 파서
soup = BeautifulSoup(broswer.page_source, "lxml")
time.sleep(10)

#게임리스트가있는 태그 id를 읽어옴
games = soup.find_all("div", attrs={"id": "search_resultsRows"})


#공백리스트 생성
appno_list=[]
title_list=[]
released_list=[]
rating_list=[]
rating_per_list=[]
rating_count_list=[]
real_price_list=[]
discount_per_list=[]
discount_price_list=[]


#읽어온 game들을 필요한 정보를 얻기 위해 가공  ~~.find_all("태그",attrs={"속성":"값"})
#find("태그",class)
for game in games:
  appnos=game.find_all("a")
  titles=game.find_all("span",attrs={"class":"title"})
  released=game.find_all("div",attrs={"class":"col search_released responsive_secondrow"})
  reviews_temp=game.find_all("div",attrs={"class":"col search_reviewscore responsive_secondrow"})
  prices=game.find_all("div",attrs={"class":"col search_price_discount_combined responsive_secondrow"})

#리스트 초기화 
appno_list.clear()
title_list.clear()
released_list.clear()
rating_list.clear()
rating_per_list.clear()
rating_count_list.clear()
real_price_list.clear()
discount_per_list.clear()
discount_price_list.clear()

#app넘버
#미출시는 appno가 없을 수 있다.
for i in appnos:
  try:
    temp=i.attrs['data-ds-appid']
    appno_list.append(temp)
  except:
    appno_list.append("")




# 이름
for title in titles:
  title_list.append(title.string)


for i in released:
  temp=i.get_text()
  released_list.append(temp)

#  평가, 비율 ,평가 인원수
for reviews in reviews_temp:
  rating=""
  rating_per=""
  rating_count=""
  if reviews.select("span") == [] :
    #평가가없는건 비인기게임or신작
    rating="Preparing"
    rating_per=" "
    rating_count=" "
  else:
    #평가 존재시 파싱
    temp=reviews.find("span")
    temp2=str(temp.attrs["data-tooltip-html"])
    temp3=temp2.split("<br>")
    temp4=temp3[1].split("%")
    temp5=temp4[1].split("of the ")
    temp6=temp5[1].split(" user")
    temp5=temp4[1].split("of the ")
    temp6=temp5[1].split(" user")
    rating=temp3[0]
    rating_per=temp4[0]+"%"
    rating_count=temp6[0]
  rating_list.append(rating)
  rating_per_list.append(rating_per)
  rating_count_list.append(rating_count)
  
list_str=["Free","FREE","Play"]
split_char=chr(8361)
for price in prices:
  real_price=""
  discount_per=""
  discount_price=""
  if price.select("span")==[]:#span태그 없으면 무료 or 정가
    temp_fn=price.find("div", attrs={"class":"col search_price responsive_secondrow"})
    temp_fn2=str(temp_fn).split("\n")
    temp_fn3=temp_fn2[1].strip()
    temp_fn4=temp_fn3.split(" ")
    if temp_fn4[0]=="Free" or temp_fn4[0]=='</div>':#무료거나 가격이 없을때
      real_price="Free"
    else:
      real_notsale_temp=temp_fn3.split(split_char)
      real_notsale_temp2=real_notsale_temp[1].split(" ")
      real_price=real_notsale_temp2[1]
  else:#할인 시 파싱  
    temp=price.select("span")
    temp_dis=temp[0].get_text().split("-")#할인률
    temp2=price.find("div", attrs={"class":"col search_price discounted responsive_secondrow"})
    temp3=temp2.get_text().strip()
    real_sale_temp=temp2.find("strike").get_text()
    real_sale_temp2=real_sale_temp.split(split_char)
    real_price=real_sale_temp2[1].strip()
    discount_per=temp_dis[1]
    for temp_a in list_str:#할인 시 무료가 되는 경우도 있음 
      if temp3.find(temp_a)==True:
        discount_price="Free"
      else:
        temp4=temp3.split(split_char)
        discount_price=temp4[2].strip()
  real_price_list.append(real_price)
  discount_per_list.append(discount_per)
  discount_price_list.append(discount_price) 



import pandas as pd

data={'appno':appno_list,
        'name':title_list,
        'released_date':released_list,
        'rating':rating_list,
        'rating_count':rating_count_list,
        'price':real_price_list,
        'sale':discount_per_list,
        'discount_price':discount_price_list}
df=pd.DataFrame(data)
df.to_csv("./steam_final.csv",encoding='UTF-8-sig') 
