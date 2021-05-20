import speech_recognition as sr #sst 모듈
import pyttsx3 #tts 모듈
import time

engine = pyttsx3.init() #tts모듈 실행
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def voice_input():
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

a = voice_input()

print(a)