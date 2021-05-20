from flask import Flask, render_template, request
import speech_recognition as sr #sst 모듈
import pyttsx3 #tts 모듈

engine = pyttsx3.init() #tts모듈 실행
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def voice_input():
    url = ""
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
                return "날씨"

            elif '시간표' in text:
                return "시간표"

            elif '식단' or '메뉴' in text:
                return "식단"
            
            
            elif '건물' or '위치' in text:
                return "건물"
        
        except:
            print("Sorry could not recognize what you said\n\n")


app = Flask("CBNU_for_blind")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def index():
    word = voice_input();
    url = ""
    if word is "날씨":
        url = "weather.html"
        
    return render_template("index.html", word = word, url = url)

@app.route("/menu.html")
def menu():
    return render_template("menu.html")

@app.route("/navigation.html")
def navigation():
    return render_template("navigation.html")

@app.route("/profile.html")
def profile():
    return render_template("profile.html")

@app.route("/schedule.html")
def schedule():
    return render_template("schedule.html")

@app.route("/weather.html")
def weather():
    return render_template("weather.html")

app.run(host="0.0.0.0")