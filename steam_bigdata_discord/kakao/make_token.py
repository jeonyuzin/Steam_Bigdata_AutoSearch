import requests
import json

url = "https://kauth.kakao.com/oauth/token"

data = {
"grant_type" : "authorization_code",
"client_id" : "아이디",
"redirect_uri" : "https://example.com/oauth",
"code" : "코드"
}

response = requests.post(url, data=data)
tokens = response.json()

# 토큰을 파일로 저장하기
if "access_token" in tokens:
    with open("kakao_token.json", "w") as fp:
        json.dump(tokens, fp)
        print("Tokens saved successfully")
else:
    print(tokens)
