import csv
import json
import os
import sys
import urllib.request
import re
import pandas as pd

제목 = '전주 노후화시설'
# 제목에 원하는것을 입력해서 파일 이름과 검색에 활용

매체 = 'news'
# blog, news 에서 고르고 입력 

client_id = "v9kzUIAhp8IuffhrgbX8"
client_secret = "DQRwNxzba2"
# 내 네이버 api 발급 아이디

encText = urllib.parse.quote(제목)
for 시작위치 in range(1,1000,100):
    # 검색 시작 위치를 위해 설정 
    url = f"https://openapi.naver.com/v1/search/{매체}?query={encText}&display=100&start={시작위치}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    json_rt = response.read().decode('utf-8-sig')

    py_rt = json.loads(json_rt)

    data= pd.DataFrame(py_rt['items'])
    # 데이터 프레임으로 만든 후 csv 로 저장할것

    def clean_html(x):
        x = re.sub("\&\w*\;","",x)
        x = re.sub("<.*?>","",x)
        return x

    # 정규식 이용하여 깔끔하게 정리
    for key in data.keys():
        data[key] = data[key].apply(lambda x: clean_html(x))
    # 람다 이용

    # csv로 저장
    data.to_csv('{}_{}_{}.csv'.format(제목,매체,시작위치),encoding='utf-8-sig')
    # 제목은 제목_매체_시작위치