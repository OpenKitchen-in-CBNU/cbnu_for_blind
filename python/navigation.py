from selenium import webdriver #셀레니움 웹 드라이버(모듈)(+크롬 드라이버 깔야야 함 -> 내 버전이랑 맞는 정보 도움말->크롬 정보 / exe파일 실행파일 있는곳에 넣기)
import time
from selenium.webdriver.common.keys import Keys#
import re #

browser = webdriver.Chrome("./chromedriver.exe")
browser.get("https://map.kakao.com")#브라우저 정보


start_location = "충북대학교 학연산공동기술연구원"            #샘플
end_location = "충북대학교 우편취급국"#말하면 입력 받음

browser.find_element_by_xpath("//*[@id='search.keyword.query']").send_keys(end_location)            #도착지 입력
browser.find_element_by_xpath("//*[@id='search.keyword.query']").send_keys(Keys.ENTER)              #엔터
time.sleep(1)       #화면 넘어가는 동안 1초 대기 - 화면 찾는동안

place_btn = browser.find_element_by_xpath("//*[@id='info.search.place.list']/li[1]/div[3]/strong/a[2]")           #장소 여러개중에 A장소 클릭
browser.execute_script("arguments[0].click();", place_btn)                                                      
time.sleep(0.5)      #화면 넘어가는 동안 0.5초 대기

dest_btn_elem = browser.find_element_by_class_name("destination")           #도착지로 설정 버튼    
browser.execute_script("arguments[0].click();", dest_btn_elem)              #도착지로 설정 버튼 클릭
browser.find_element_by_xpath("//*[@id='info.route.waypointSuggest.input0']").send_keys(start_location)         #츨발지 입력
browser.find_element_by_xpath("//*[@id='info.route.waypointSuggest.input0']").send_keys(Keys.ENTER)           #엔터
time.sleep(0.5)       #화면 넘어가는 동안 0.5초 대기

walk_btn_elem = browser.find_element_by_id("walktab")               #도보 버튼 엘리먼트
browser.execute_script("arguments[0].click();", walk_btn_elem)      #도보 버튼 클릭
time.sleep(0.5)       #화면 넘어가는 동안 0.5초 대기

path_btn_elem = browser.find_element_by_xpath("//*[@id='info.walkRoute']/div[1]/ul/li[1]/div[1]/a")         #큰길우선 버튼 엘리먼트
browser.execute_script("arguments[0].click();", path_btn_elem)      #큰길우선 버튼 클릭

#웹 엘리먼트로부터 정보를 받아 리스트로 저장
route_list = []                         #경로 리스트 생성
numbers = []                            #경로 숫자만 뽑아서 만드는 리스트(2차원인것 생각하기.)
for i in range(30):
    route_elem = browser.find_elements_by_class_name("desc")[i].text     #모든 경로 엘리먼트
    if("도착" in route_elem):           #엘리먼트 텍스트 안에 도착 이라는 단어 나오면 탈출 
        break
    route_list.append(route_elem)       #경로 리스트에 추가 
    numbers.append(re.findall("\d+", route_list[i]))            #정규식 이용하여 숫자만 뽑아 numbers 리스트에 추가
    
#보폭 계산    
foot_step = 0.7                         #한 걸음당 보폭 <- 이거 입력받을 수 있으면 이거 입력 받고..
step_list = []                          #걸음 수 저장하는 리스트 type은 int
for i in range(len(numbers)):
    step_num = float(numbers[i][0]) / foot_step
    step_list.append(int(step_num))

#최종 출력할 문자열 만들기
print_str = []                          #최종 출력할 문자열 리스트
for i in range(len(numbers)):
    if "왼쪽" in route_list[i]:
        print_str.append("왼쪽으로 " + str(numbers[i]) + "미터" + str(step_list[i]) + "걸음 이동")
    elif "오른쪽" in route_list[i]:
        print_str.append("오른쪽으로 " + str(numbers[i]) + "미터" + str(step_list[i]) + "걸음 이동")
    else:
        print_str.append(str(numbers[i]) + "미터" + str(step_list[i]) + "걸음 직진 이동")

print(print_str)

time.sleep(1)
#browser.close()   #현재 탭만 종료
browser.quit()   #전체 브라우저 종료