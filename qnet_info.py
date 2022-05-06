# 큐넷에 존재하는 모든 자격증 정보(자격명, 자격코드)를 얻어옵니다.
# 캘린더 입력에 필요한 jmCd(코드) 값을 얻어오기 위함입니다.

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver

import json

dic = {}
list = []

# 국가자격 종목별 상세정보가 존재하는 URL
URL = 'https://www.q-net.or.kr/crf005.do?id=crf00501&gSite=Q&gId='

# 크롬 드라이버 사용
driver = webdriver.Chrome('chromedriver.exe')

# 크롬 실행
driver.get(url=URL)

# 한국산업인력공단 시행종목 큰 카테고리가 총 26개이기 때문에 01~26을 검색 (해당 페이지 jmListInfo 자바스크립트 참조)
for idx in range(1, 27):
    response = urlopen('https://www.q-net.or.kr/crf005.do?id=crf00501s01&gSite=Q&gId=&div=1&obligFldCd=' + str(format(idx, '02')))
    soup = BeautifulSoup(response, 'html.parser')
    
    # 큰 카테고리 내부에 있는 a 태그를 갖고 있는 작은 카테고리 리스트 정보를 얻어옴
    for data in soup.select("a"):
        list.append(data['href'].split(":")[1])

# 작은 카테고리 내부에 있는 자격증 정보를 for문을 돌려서 자격증 별로 자격명과 자격코드를 추출
for scriptData in list:
    driver.execute_script(scriptData)

    ulList = driver.find_elements_by_css_selector("#searchJMlist_view li input")

    for index in range(1, len(ulList), 2):
        dic[ulList[index].get_attribute("value")] = ulList[index-1].get_attribute("value")

# 해당 폴더에 licenselist.json 라는 파일로 추출한 값들을 입력
json_val = json.dumps(dic, ensure_ascii=False)
with open('licenselist.json', 'w', encoding='utf-8') as license:
    license.write(json_val)

# 크롬 닫기
driver.close()
