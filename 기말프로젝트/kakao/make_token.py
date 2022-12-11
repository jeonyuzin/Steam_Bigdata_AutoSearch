import requests
import json

url = "https://kauth.kakao.com/oauth/token"

data = {
"grant_type" : "authorization_code",
"client_id" : "4bb5c92b4402ad9275000c5e52adf233",
"redirect_uri" : "https://example.com/oauth",
"code" : "9UC__yU5gc8kb5k_8KtPvpI7P5EL3slFGhe1rfcnVhG3tBymlGD7t_eX2krlV5qpITpS0go9dVwAAAGE2RNeeg"
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
