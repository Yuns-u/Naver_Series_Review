# Naver_Series_Review
![image](https://user-images.githubusercontent.com/76740971/140657546-d710878b-2048-4bee-b956-fb4ef5601e85.png)

네이버의 웹소설 플랫폼인 네이버 시리즈의 iOS 리뷰들을 분석해보면서 웹소설 플랫폼의 개선방향 등에 대해 생각해보고자 한 프로젝트입니다.
2020년 9월 22일부터 2021년 11월 5일까지 iOS 리뷰 500개와 40여개의 google playstore의 리뷰를 크롤링하여 자연어처리를 해보고자 했습니다.

# 리뷰 크롤링 및 스크랩핑(2021.11.08)
## 의의
- UI/UX 개선안을 찾을 때 앞으로 일일히 리뷰창에 들어가지 않아도 어느 정도의 리뷰를 확보하여 가공할 수 있을 것이다.
- 자동으로 리뷰를 수집한다면 최근의 리뷰를 추출하기 효율적일 것이다.

##  한계점 및 보완해야할 점
**App store**
- 스크랩한 날로부터 최대 500를 API를 통해 가져올 수 있었으나 그 외의 리뷰를 가져오기 어려움.
- API가 제공하는 것 외의 데이터를 가져오려면 selenium 등을 더 잘 활용하는 방법을 더 잘 숙지해야 함.

**Google Playstore**
- API를 사용하거나 python의 google-play-scraper PyPI 등을 사용해서 더 많은 리뷰를 다양한 방식으로 효율적으로 가져올 수 있을 것임.
- 프로젝트 기한의 한계로 위의 다양한 효율적인 방법을 사용해보지 못함.
- 웹 페이지에 나타난 리뷰들을 크롤링한 것으로 리뷰의 수와 질이 다소 떨어지는 것 같음.

# Reference
- playstore_naverseries_reviews.py : https://www.youtube.com/watch?v=QGKLVzG0Jd8 를 참조함.
- new_playstore_naver_series.py : https://heytech.tistory.com/148 참고함.
