#필요한 모듈 다운
import pandas as pd #데이터프레임 사용하기 위함
import xmltodict #xml을 parsing하기 위함
from urllib.request import urlopen #url을 이용하여 웹상의 데이터 불러오기 위함
import json

review_dict = [] 

for j in range(1,11): 
  url = "https://itunes.apple.com/kr/rss/customerreviews/page=%i/id=433592412/sortby=mostrecent/xml?urlDesc=/customerreviews/id=433592412/sortBy=mostRecent/xml" % j 
  response = urlopen(url).read() 

  xml = xmltodict.parse(response) 
  XmlToJson = json.loads(json.dumps(xml)) 
  
  for i in range(len(XmlToJson['feed']['entry'])): 
    review_dict.append({ 
        'DATE' : XmlToJson['feed']['entry'][i]['updated'], 
        'STAR' : int(XmlToJson['feed']['entry'][i]['im:rating']), 
        'LIKE' : int(XmlToJson['feed']['entry'][i]['im:voteSum']), 
        'DISLIKE' : int(XmlToJson['feed']['entry'][i]['im:voteCount']) - int(XmlToJson['feed']['entry'][i]['im:voteSum']), 
        'TITLE' : XmlToJson['feed']['entry'][i]['title'], 
        'REVIEW' : XmlToJson['feed']['entry'][i]['content'][0]['#text'] 
    }) 
    
review_df = pd.DataFrame(review_dict) 
review_df['DATE'] = pd.to_datetime(review_df['DATE'], format="%Y-%m-%dT%H:%M:%S-07:00") 
review_df.to_csv('IOS_ReviewData.csv', encoding='utf-8')
