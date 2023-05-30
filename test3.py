import requests
import json

with open("token.json","r") as kakao:
    tokens=json.load(kakao)


url="https://kapi.kakao.com/v2/api/talk/memo/default/send"


headers={
        "Authorization" : "Bearer " + tokens["access_token"]
}


data={
        'object_type': 'text',
        'text': '테스트입니다.',
        'link':
        {'web_url': 'https://developers.kakao.com',
            'mobile_web_url':'https://developers.kakao.com'
            },
        'button_title':'시작'
        }
data={'template_boejct':json.dumps(data)}
response=requests.post(url,headers=headers,data=data)
print(response.status_code)

