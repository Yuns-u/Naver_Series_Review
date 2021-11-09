# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
from datetime import datetime
import pandas as pd

#크롤링하고자 하는 페이지
url = 'https://play.google.com/store/apps/details?id=com.nhn.android.nbooks&hl=ko&gl=US&showAllReviews=true'

#웹상의 몇 페이지나 크롤링할 것인가.
scroll_cnt = 50

# chrome driver 다운로드: https://sites.google.com/a/chromium.org/chromedriver/home
driver = webdriver.Chrome('./chromedriver')
driver.get(url)

os.makedirs('result', exist_ok=True)

for i in range(scroll_cnt):
  # scroll to bottom
  driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  time.sleep(3)

  # click 'Load more' button, if exists
  try:
    load_more = driver.find_element_by_xpath('//*[contains(@class,"U26fgb O0WRkf oG5Srb C0oVfc n9lfJ")]').click()
  except:
    print('Cannot find load more button...')

# 리뷰 가져오기
reviews = driver.find_elements_by_xpath('//*[@jsname="fk8dgd"]//div[@class="d15Mdf bAhLNe"]')

print('There are %d reviews avaliable!' % len(reviews))
print('Writing the data...')

# 데이터프레임에 저장하기
df = pd.DataFrame(columns=['name', 'ratings', 'date', 'helpful', 'comment', 'developer_comment'])

# 리뷰를 가져와 뷰티풀스프로 파싱하기
for review in reviews:
  # parse string to html using bs4
  soup = BeautifulSoup(review.get_attribute('innerHTML'), 'html.parser')

  # reviewer
  name = soup.find(class_='X43Kjb').text

  # rating
  ratings = int(soup.find('div', role='img').get('aria-label').replace('별표 5개 만점에', '').replace('개를 받았습니다.', '').strip())

  # review date
  date = soup.find(class_='p2TkOb').text
  date = datetime.strptime(date, '%Y년 %m월 %d일')
  date = date.strftime('%Y-%m-%d')

  # helpful(좋아요 수)
  helpful = soup.find(class_='jUL89d y92BAb').text
  if not helpful:
    helpful = 0
  
  # review text
  comment = soup.find('span', jsname='fbQN7e').text
  if not comment:
    comment = soup.find('span', jsname='bN97Pc').text
  
  # developer comment
  developer_comment = None
  dc_div = soup.find('div', class_='LVQB0b')
  if dc_div:
    developer_comment = dc_div.text.replace('\n', ' ')
  
  # append to dataframe
  df = df.append({
    'name': name,
    'ratings': ratings,
    'date': date,
    'helpful': helpful,
    'comment': comment,
    'developer_comment': developer_comment
  }, ignore_index=True)

# finally save the dataframe into csv file
filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
df.to_csv('playstore_ReviewData_naverseries.csv', encoding='utf-8-sig', index=False)
driver.stop_client()
driver.close()

print('Done!')