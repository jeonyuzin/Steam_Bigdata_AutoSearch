# 스팀 빅데이터 분석 및 자동화 알림 시스템

# AS-IS
1. 가격을 제외한 정렬 기준이 한 개만 적용된다.

2. 가격도 6만원 제한이 있다. (6만원 이외에는 all)

3. 정렬된 목록이 불규칙 적이다.(내부 로직:태그로 추측)

4. 장르 태그만 수십 가지가 넘으며 그 외에 게임 플레이 형식에 따라서 또 나뉜다.

이러한 이유로 유연한 설정이 어려우며 가장 큰 불편함인 자동화 검색이 불가능하다.

# TO-BE
1. 게임 목록을 크롤링하여 데이터 수집

2. 데이터를 가공, 분석하여 원하는 자료 만들고 시각화

3. 직접 빅데이터를 만들고 알림 봇 만들기

유연한 설정이 가능하도록 데이터를 가져와서 

클라이언트의 요구에 맞게 설정이 가능하며 자동화 검색을 지원한다.

# 데이터 수집 
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/data_get0.png">
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/data_get1.png">
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/data_get2.png">
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/data_get3.png">
# 데이터 가공
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/data_pre1.png">
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/data_pre2.png">

# 데이터 분석 및 시각화
스팀 기준 오래된 게임이면 할인률이 높은가? X 무조건은 아니다.
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/data_vis.png">

# 프로그램 흐름도
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/data_flow.png">


# 알리미 봇 (카카오톡 API 테스팅 및 Discord 배포)
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/kakao.png">
<img src="https://github.com/jeonyuzin/Steam_Bigdata_AutoSearch/blob/main/readimg/discord.png">




