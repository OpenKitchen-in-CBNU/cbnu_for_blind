import re    #정규 표현식 모듈
import datetime as dt    #현재 시간 정보 가져오기 위해 호출 / download complete
import speech_recognition as sr #sst 모듈
import pyttsx3 #tts 모듈
import requests
from bs4 import BeautifulSoup
from flask import Flask

now_info = dt.datetime.now()         #현재 시간 객체
weekday_info = now_info.weekday()    #요일 (월:0 / 화:1 / 수:2 / 목:3 / 금:4 / 토:5 / 일:6)     

engine = pyttsx3.init() #tts모듈 실행
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#현재기온 최저기온 최고기온 미세먼지 초미세먼지 스크롤링
temp_url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%B2%AD%EC%A3%BC+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=h49mQlp0Jy0ssSNKjLGssssss2C-422644"
temp_res = requests.get(temp_url)    
temp_res.raise_for_status()
dust_url = "https://weather.naver.com/today/16113114"          #미세먼지 가져오기 위한 url 
dust_res = requests.get(dust_url)
dust_res.raise_for_status()

soup2 = BeautifulSoup(temp_res.text, "lxml")
soup3 = BeautifulSoup(dust_res.text, "lxml")
#모든 변수 type str
curr_temperature = soup2.find("span", attrs={"class" : "todaytemp"}).text        #현재기온
min_temperature = soup2.find_all("span", attrs={"class" : "num"})[0].text        #최저기온
max_temperature = soup2.find_all("span", attrs={"class" : "num"})[1].text        #최고기온
fine_dust = soup3.find_all("em", attrs={"class" : "level_text"})[0].text            #미세먼지
ultra_fine_dust = soup3.find_all("em", attrs={"class" : "level_text"})[1].text      #초미세먼지


def no_space(text):     #공백,개행 제거 함수 정의
    text1=re.sub('&nbsp; | &nbsp;| \n|\t|\r| \ufeff |\xa0', '', text)
    text2=re.sub('\n\n', '',text1)
    return text2




def get_weather(): #입력받은 키워드에 '날씨'가 있으면 청주 개신동의 날씨를 출력한다.
    print("기상청과 웨더아이에서 제공하는 오늘의 개신동 날씨입니다.")
    engine.say("기상청과 웨더아이에서 제공하는 오늘의 개신동 날씨입니다.")
    engine.runAndWait()
    print("현재 기온은" + curr_temperature + "도 이며,")
    engine.say("현재 기온은" + curr_temperature + "도 이며,")    
    engine.runAndWait()
    print("금일 최저 기온은" + min_temperature + "도")      
    engine.say("금일 최저 기온은" + min_temperature + "도")
    engine.runAndWait()
    print("금일 최고 기온은 " + max_temperature + "도 입니다.")
    engine.say("금일 최고 기온은 " + max_temperature + "도 입니다.")
    engine.runAndWait()
    print("오늘의 미세먼지 농도는 " + fine_dust  + "이며")
    engine.say("오늘의 미세먼지 농도는 " + fine_dust  + "이며")
    engine.runAndWait()
    print("초미세먼지 농도는 " + ultra_fine_dust + "입니다.")
    engine.say("초미세먼지 농도는 " + ultra_fine_dust + "입니다.")
    engine.runAndWait()

def scp_res():
    #url ->_b:별빛 / _e:은하수 / h:한빛
    url_b="http://coop.cbnu.ac.kr/index.php?mid=m0302"    
    url_e="http://coop.cbnu.ac.kr/index.php?mid=m0304"
    res1=requests.get(url_b)
    res2=requests.get(url_e)      
    res1.raise_for_status()      #오류 발생시 예외 발생
    res2.raise_for_status()
    soup1=BeautifulSoup(res1.text,"lxml")
    soup2=BeautifulSoup(res2.text,"lxml")
    #필요한 데이터 검색
    diet_b = soup1.find_all("td",{"bgcolor":"#ffffff"})
    diet_e = soup2.find_all("td",{"bgcolor":"#ffffff"})

    return diet_b, diet_e



    
def get_eat(): #입력받은 키워드에 '식단'이 있으면 실행되는 함수.
    #식당이름 받아옴 ex)은하수 식당 -> 요일별 출력

     diet_b, diet_e = scp_res()

     engine.say("메뉴를 검색할 식당과 검색할 이번주의 요일을 말씀해주세요. 검색 날짜의 기본값은 오늘입니다.")
     engine.runAndWait()
     print("Speak Anything :")
     audio = r.listen(source)
     res = r.recognize_google(audio, language="ko-KR")
     engine.say(res + "이라고 말씀하셨습니다.")
     engine.runAndWait()
     print("You said : {} \n\n".format(res))
     
     temp_weekday_info = weekday_info
     days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
     weekday = days[weekday_info]

     if '월요일' in res:
         temp_weekday_info = 0
         weekday = '월요일'
     elif '화요일' in res:
         temp_weekday_info = 1
         weekday = '화요일'
     elif '수요일' in res:
         temp_weekday_info = 2
         weekday = '수요일' 
     elif '목요일' in res:
         temp_weekday_info = 3   
         weekday = '목요일' 
     elif '금요일' in res:
         temp_weekday_info = 4   
         weekday = '금요일' 

     if '은하' in res:
        engine.say('은하수 식당의 ' + weekday + '식단정보입니다.')
        engine.runAndWait()
        if temp_weekday_info==0:
            print(no_space(diet_e[0].get_text()))
            engine.say(no_space(diet_e[0].get_text()))
            engine.runAndWait()
        elif temp_weekday_info==1:
            print(no_space(diet_e[1].get_text()))
            engine.say(no_space(diet_e[1].get_text()))
            engine.runAndWait()
        elif temp_weekday_info==3:
            print(no_space(diet_e[3].get_text()))
            engine.say(no_space(diet_e[3].get_text()))
            engine.runAndWait()
        elif temp_weekday_info==3:
            print(no_space(diet_e[3].get_text()))
            engine.say(no_space(diet_e[3].get_text()))
            engine.runAndWait()
        elif temp_weekday_info==4:
            print(no_space(diet_e[4].get_text()))
            engine.say(no_space(diet_e[4].get_text()))
            engine.runAndWait()
        else:
            print("오늘은 식당 영업을 하지 않습니다.")
            engine.say("오늘은 식당 영업을 하지 않습니다.")
            engine.runAndWait()
            
     elif '별빛' in res:
        engine.say('별빛식당의 ' + weekday + '식단정보입니다.')
        engine.runAndWait()
        if temp_weekday_info==0:
            print(no_space(diet_b[0].get_text()))
            engine.say(no_space(diet_b[0].get_text()))
            engine.runAndWait()
        elif temp_weekday_info==1:
            print(no_space(diet_b[1].get_text()))
            engine.say(no_space(diet_b[1].get_text()))
            engine.runAndWait()
        elif temp_weekday_info==3:
            print(no_space(diet_b[3].get_text()))
            engine.say(no_space(diet_b[3].get_text()))
            engine.runAndWait()
        elif temp_weekday_info==3:
            print(no_space(diet_b[3].get_text()))
            engine.say(no_space(diet_b[3].get_text()))
            engine.runAndWait()
        elif temp_weekday_info==4:
            print(no_space(diet_b[4].get_text()))
            engine.say(no_space(diet_b[4].get_text()))
            engine.runAndWait()
        else:
            print("오늘은 식당 영업을 하지 않습니다.")
            engine.say("오늘은 식당 영업을 하지 않습니다.")
            engine.runAndWait()
            
     elif '한빛' in res:
         print("한빛식당은 영업을 하지 않습니다.")
         engine.say("한빛식당은 영업을 하지 않습니다.")
         engine.runAndWait()
     else:
         
         print("식당 이름을 잘못 말씀하셨습니다. 다시 말씀해주세요")
         get_eat()

    
def get_timetable(): #입력받은 내용에 시간표 가 있으면 호출되는 함수 , 요일별 시간표를 말해주는 함수다
     if int(weekday_info) == 0:
         subjects = "오늘은 09시 선형대수학 13시 자료구조 16시 컴퓨터구조 수업이 있습니다"
         print(subjects)
         engine.say(subjects)
         engine.runAndWait()
     elif int(weekday_info) == 1:
         subjects = "오늘은 10시 기초통계학 12시 영상으로 보는 한국사 16시 자료구조 수업이 있습니다"
         print(subjects)
         engine.say(subjects)
         engine.runAndWait()
     elif int(weekday_info) == 2:
         subjects = "오늘은 09시 객체지향 프로그래밍 11시 컴퓨터 구조 16시 미래설계구현 수업이 있습니다."
         print(subjects)
         engine.say(subjects)
         engine.runAndWait()
     elif int(weekday_info) == 3:
         subjects = "오늘은 09시 선형대수학 11시 기초통계학 13시 오픈소스 기초프로젝트 수업이 있습니다"
         print(subjects)
         engine.say(subjects)
         engine.runAndWait()
     elif int(weekday_info) == 4:
         subjects = "오늘은 13시 객체지향 프로그래밍 수업이 있습니다"
         print(subjects)
         engine.say(subjects)
         engine.runAndWait()
     elif int(weekday_info) == 5:
         subjects = "오늘은 토요일입니다. 수업이 없어요"
         print(subjects)
         engine.say(subjects)
         engine.runAndWait()
     else:
         subjects = "오늘은 일요일입니다. 수업이 없어요"
         print(subjects)
         engine.say(subjects)
         engine.runAndWait()
        
    
    
def nevigation():  #건물 위치를 알려주는 함수
    {
     }
    
    
r = sr.Recognizer()
with sr.Microphone() as source:
    #입력 받을 내용 = 시간표, 건물 위치, 식단표, 날씨
    print("시간표, 날씨, 식단, 건물위치중 필요한 정보를 말씀하세요. ")
    engine.say(("시간표, 날씨, 식단, 건물위치중 필요한 정보를 말씀하세요. "))
    engine.runAndWait()
    print("Speak Anything :")
    audio = r.listen(source)#오디오 변수에 저장
    try:
        text = r.recognize_google(audio, language="ko-KR")#한국어로 언어 받는다
        print("You said : {} \n\n".format(text))
        
        if '날씨' in text:
            get_weather()

        elif '시간표' in text:
            get_timetable()

        elif '식단' or '메뉴' in text:
            print("식단 정보를 불러오고 있습니다. 잠시만 기다려주세요.")
            engine.say(("식단 정보를 불러오고 있습니다. 잠시만 기다려주세요."))
            engine.runAndWait()
            get_eat()
           
        
            
        elif '건물' or '위치' in text:
            pass
    
    except:
        print("Sorry could not recognize what you said\n\n")
