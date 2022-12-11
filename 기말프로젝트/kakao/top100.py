from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
import requests
import json




def token_reload():
    
    # 저장 된 json 파일 읽어오기
    with open("kakao_token.json", "r") as fp:
      token_temp = json.load(fp)
    # 카카오 토큰 갱신하기
    url = "https://kauth.kakao.com/oauth/token"
    data = {"grant_type": "refresh_token",
            "client_id": "4bb5c92b4402ad9275000c5e52adf233",
            "refresh_token": token_temp['refresh_token']
            }
    response = requests.post(url, data=data)
    # 갱신 된 토큰 내용 확인
    result = response.json()
    # 갱신 된 내용으로 파일 업데이트
    if 'access_token' in result:
        token_temp['access_token'] = result['access_token']
    if 'refresh_token' in result:
        token_temp['refresh_token'] = result['refresh_token']
    else:
        pass
    with open("kakao_token.json", "w") as fp:
        json.dump(token_temp, fp)
    return token_temp['access_token']

            
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
url = "https://store.steampowered.com/charts/mostplayed/"
broswer.get(url)

time.sleep(5)
print("스크롤 완")
#브라우저페이지를 읽어옴
#lxml은 구문을 분석하기 위한 파서
soup = BeautifulSoup(broswer.page_source, "lxml")

#게임리스트가있는 태그 id를 읽어옴
titles=soup.find("div",attrs={"class" : "DialogDropDown_CurrentDisplay"})
games_name = soup.find_all("div", attrs={"class": "weeklytopsellers_GameName_1n_4-"})
games_href=soup.find_all("a", attrs={"class": "weeklytopsellers_TopChartItem_2C5PJ"})
total=soup.find_all("tr", attrs={"class": "weeklytopsellers_TableRow_2-RN6"})
games_curr=soup.find_all("td", attrs={"class": "weeklytopsellers_ConcurrentCell_3L0CD"})
games_peck=soup.find_all("td", attrs={"class": "weeklytopsellers_PeakInGameCell_yJB7D"})



name_list=[]
appno_list=[]
real_price_list=[]
discount_per_list=[]
discount_price_list=[]
curr_list=[]
peck_list=[]


#https://store.steampowered.com/app/1238840/Battlefield_1?snr=1_7001_7005__7003
for i in games_href:
  temp=i['href']
  temp_split=temp.split('/')
  appno_list.append(temp_split[4])

for j in games_name:
  name_list.append(j.get_text())

for k in games_curr:
  curr_list.append(k.get_text())


for l in games_peck:
  peck_list.append(l.get_text())

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


    



import pandas as pd
#pandas이용해서 데이터프레임으로 만들고 csv작성
#apex같은 특수문자가 있는 게임명이 깨져서 encoding을 함
data ={'appno':appno_list,
       'name' : name_list,
       'real_price':real_price_list,
       'sale':discount_per_list,
       'discount_price':discount_price_list,
       'curr':curr_list,
       'peck':peck_list}
df=pd.DataFrame(data)
df.to_csv("./steam_top100.csv",encoding='UTF-8-sig')



def send_to_me(token,content):
	url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
	header = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Authorization": 'Bearer ' + token}
	post = {
		"object_type": "text",
		"text": content,
		"link": {
			"web_url": "https://developers.kakao.com",
			"mobile_web_url": "https://developers.kakao.com"
			},
		}
	data = {"template_object": json.dumps(post)}
	returnValue=requests.post(url, headers=header, data=data)
	print(returnValue)
    
token=token_reload()



#pandas이용해서 데이터프레임으로 만들고 csv작성
dif_list_temp=list(set(appno_list)-set((appno_prev)))
dif_list=list(set(dif_list_temp))
print(dif_list)
if len(dif_list)>=1:
    send_dict={}
    for s in dif_list:
        df_temp=df.loc[df['appno']==s]
        print(df_temp)
        send_dict.clear()
        if len(df_temp['sale'].values)==1:
            send_dict['message']="new top100" 
            send_dict['steam_no']=str(df_temp['appno'].values)
            send_dict['name']=str(df_temp['name'].values)
            send_dict['real']=str(df_temp['real_price'].values)
            send_dict['curr']=str(df_temp['curr'].values)
            send_dict['peck']=str(df_temp['peck'].values)
        else:
            send_dict['message']="new top100 sale"
            send_dict['steam_no']=str(df_temp['appno'].values)
            send_dict['name']=str(df_temp['name'].values)
            send_dict['real']=str(df_temp['real_price'].values)
            send_dict['sale']=str(df_temp['sale'].values)
            send_dict['discount']=str(df_temp['discount_price'].values)
            send_dict['curr']=str(df_temp['curr'].values)
            send_dict['peck']=str(df_temp['peck'].values)
        print(send_dict)
        js=json.dumps(send_dict)
        send_to_me(token,js)
    try:
        f=open("./appno_prev_list.txt",'a')
        for no in dif_list:
            f.write(no)
            f.write("\n")
        f.close()
    except Exception as e:
        print(e)
else:
    send_dict={}
    send_dict['message']='no send information'
    js=json.dumps(send_dict)
    send_to_me(token,js)    
broswer.quit()            
