# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from time import sleep
import random
from tqdm.auto import tqdm, trange
import pandas as pd

#크롤링할 페이지
url = 'https://play.google.com/store/apps/details?id=com.nhn.android.nbooks&hl=ko&gl=US&showAllReviews=true'

#셀레니움을 사용하기 위한 드라이버
driver = webdriver.Chrome('./chromedriver')

def scrolling():
    try:        
        # 스크롤 높이 받아오기
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            pause_time = random.uniform(0.5, 0.8)
            # 최하단까지 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 페이지 로딩 대기
            time.sleep(pause_time)
            # 무한 스크롤 동작을 위해 살짝 위로 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
            time.sleep(pause_time)
            # 스크롤 높이 새롭게 받아오기
            new_height = driver.execute_script("return document.body.scrollHeight")
            try:
                # '더보기' 버튼 있을 경우 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div/span/span').click()
            except:
                # 스크롤 완료 경우
                if new_height == last_height:
                    print("Scrolling is completed!")
                    break
                last_height = new_height
                
    except Exception as e:
        print("error occurred: ", e)

# 페이지열기
driver.get(url)

# 페이지 로딩 대기
wait = WebDriverWait(driver, 10)

#####
#allreview_btn = '/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[3]/section/div/div/div[5]/div/div/button/span'
#chk_loading = wait.until(EC.element_to_be_clickable((By.XPATH, allreview_btn)))
#driver.find_element_by_xpath(allreview_btn).click()
######

chk_xpath = '/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/h3'
chk_loading = wait.until(EC.element_to_be_clickable((By.XPATH, chk_xpath)))

# 페이지 무한 스크롤 다운
scrolling()

# html parsing하기
html_src = driver.page_source
soup_src = BeautifulSoup(html_src, 'html.parser')

# html 데이터 저장
with open("./html_data.html", "w", encoding = 'utf-8') as file:
    file.write(str(soup_src))

# 리뷰 데이터 클래스 접근
review_all= soup_src.find_all(class_ = 'd15Mdf bAhLNe')

#데이터 프레임으로 변형
start = time.time() # 코드 실행 시간 측정을 위한 변수
date_ymd = [] # 리뷰등록일을 yyyymmdd 형태로 저장할 리스트 생성
date_y = [] # 리뷰등록일 중 연도 정보를 yyyy 형태로 저장할 리스트 생성
date_m = [] # 리뷰등록일 중 월 정보를 mm 형태 저장할 리스트 생성
date_d = [] # 리뷰등록일 중 일 정보를 dd 형태로 저장할 리스트 생성
username_list = [] # 사용자 닉네임 저장용 리스트
rating_list = [] # 평점 데이터 저장용 리스트
content_list = [] # 텍스트 리뷰 저장용 리스트

# 리뷰 1개씩 접근해 정보 추출
for rv in tqdm(review_all):
    
    date_ymd_v = rv.find_all(class_ = 'p2TkOb')[0].text
    date_y_v = date_ymd_v[0:4] # 연도 정보만 추출
    # 해당 단어가 등장한 인덱스 추출
    idx_y = date_ymd_v.find('년')
    idx_m = date_ymd_v.find('월')
    idx_d = date_ymd_v.find('일')
    date_m_v = str(int(date_ymd_v[idx_y+1:idx_m])) # 월 정보만 추출
    date_d_v = str(int(date_ymd_v[idx_m+1:idx_d])) # 일 정보만 추출
    
    # 월 정보가 1자리의 경우 앞에 0 붙여줌(e.g., 1월 -> 01월)
    if len(date_m_v) == 1:
        date_m_v = '0' + date_m_v
    # 일 정보가 1자리의 경우 앞에 0 붙여줌(e.g., 7일 -> 07일)
    if len(date_d_v) == 1:
        date_d_v = '0' + date_d_v
    
    # 리뷰등록일 full version은 최종적으로 yyyymmdd 형태로 저장
    date_full = date_y_v + date_m_v + date_d_v
    date_ymd.append(date_full)
    date_y.append(date_y_v)
    date_m.append(date_m_v)
    date_d.append(date_d_v)
    username_list.append(rv.find_all(class_ = 'X43Kjb')[0].text) # 닉네임 정보 추출 및 저장
    rating_list.append(rv.select('span.nt2C1d > .pf5lIe > div')[0]['aria-label'][10]) # 평점 정보 추출 및 저장
    content = rv.find_all('span', attrs={'jsname':"fbQN7e"})[0].text # 장문 리뷰 내용 추출 및 저장
    # 장문 리뷰 존재하는 경우 그대로 리스트에 저장
    if content:
        content_list.append(content)
    # 단문 리뷰만 존재하는 경우, 단문 리뷰 추출 및 저장
    else:
        content_list.append(rv.find_all('span', attrs={'jsname':"bN97Pc"})[0].text)
# 코드 실행 소요시간 출력
print(time.time() - start)

#데이터 프레임 저장
start = time.time() # 코드 실행 시간 측정을 위한 변수
rv_df = pd.DataFrame({'id': range(len(date_ymd)), # userID 임의부여
                      'date': date_ymd, # 리뷰등록일 전체(yyyymmdd)
                      'date_y': date_y, # 리뷰등록일 중 연도(yyyy)
                      'date_m': date_m, # 리뷰등록일 중 월(mm)
                      'date_d': date_d, # 리뷰등록일 중 일(dd)
                     'username': username_list, # 사용자 닉네임
                     'rating': rating_list, # 평점
                     'content': content_list}) # 리뷰 내용
rv_df.to_csv('./review_dataset.csv', encoding = 'utf-8-sig') # csv 파일로 저장

print(time.time() - start) # 코드 실행 소요시간 출력