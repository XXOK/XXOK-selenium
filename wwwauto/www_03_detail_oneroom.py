#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import unittest
import random
import datetime
import sys, traceback
import platform
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class detail_oneroomTest(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to_window(window_before)
        return time.sleep(2)

    def setUp(self):
        if platform.system() == 'Darwin' :
            self.chromeDriver = PATH('../drivers/mac/chromedriver')
        else :
            self.chromeDriver = PATH('../drivers/win/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 5)

    def runTest(self):
        count = 0
        while True:
            try:
                zigbangUrl = "https://www.zigbang.com/"

                confirmAccount = "인증 계정"
                confirmpwAccount = "인증 계정"

                stations = ["신림역", "수원역", "홍대입구역", "서울대입구역", "건대입구역"]
                rndstations = random.choice(stations)

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 원,투룸 접속

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'has_d2'))).click()
                time.sleep(1)

                # 2. 원룸 지도 화면 > 지하철역 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys(rndstations)
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(3)

                stationName = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".list-title > h3"))).text

                if not rndstations == stationName:
                    raise Exception(u"역이름이 일치하지 않습니다.", stationName)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-delete"))).click()
                time.sleep(1)

                # 3. 원룸 지도 화면 > 지역 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys(u"서울시 동작구 사당동")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-delete"))).click()
                time.sleep(1)

                # 4. 매물 상세 진입

                listItem = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item")))
                listItem[0].click()
                self.moveTab(1)
                time.sleep(1)

                # 5. 사진 개수 유효성 검사

                imgItem = self.driver.find_elements_by_css_selector('.item-pager > a')
                # imgItem = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.item-pager > a')))

                if not len(imgItem) >= 5:
                    raise Exception(u"등록된 사진 개수가 5개 미만입니다.", len(imgItem), self.driver.current_url)
                time.sleep(1)

                # 6. 인증 로그인 및 찜 하기

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "icon-question2")))[0].click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-close"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class='btn-zzim off']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "link1"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(confirmAccount)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".mb-20 > button"))).click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(confirmpwAccount)

                self.driver.find_element_by_css_selector("button[type='submit']").is_displayed()

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "button[type='submit']")))[0].click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class='btn-zzim off']"))).click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "button[type='submit']")))[0].click()
                time.sleep(1)

                self.driver.close()
                self.moveTab(0)

                # 7. 테스트 매물 상세 진입

                # self.driver.execute_script('''window.open("https://www.zigbang.com/items1/10171899","_blank");''')
                #
                # self.moveTab(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys(u"인천시 강화군 서도면")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(3)

                listItem = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item ")))
                listItem[0].click()
                self.moveTab(1)

                # 8. 연락처 보기 / 문자 보내기

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "call_btn"))).click()

                dt = datetime.datetime.now().hour

                self.wait.until(EC.visibility_of_element_located((By.ID, "phone"))).send_keys("테스트 휴대폰 번호")

                self.wait.until(EC.visibility_of_element_located((By.ID, "comment"))).send_keys(u"테스트 문자 내용")

                if (dt > 22 or dt < 8):

                    self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry4"))).click()

                    self.wait.until(EC.alert_is_present()).accept()

                    self.wait.until(EC.visibility_of_element_located((By.ID, "check_agree"))).click()
                    time.sleep(3)

                    self.driver.find_elements_by_css_selector(".layer-btn > button")[1].click()

                    self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry4"))).click()

                    self.wait.until(EC.alert_is_present()).accept()
                    time.sleep(1)

                else:

                    self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry"))).click()

                    self.wait.until(EC.alert_is_present()).accept()

                    self.wait.until(EC.visibility_of_element_located((By.ID, "check_agree"))).click()
                    time.sleep(3)

                    self.driver.find_elements_by_css_selector(".layer-btn > button")[1].click()

                    self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry"))).click()

                    self.wait.until(EC.alert_is_present()).accept()
                    time.sleep(1)

                # 9. 중개사무소 정보 보기 / 매물 개수 체크 / 이것 저것 버튼 클릭

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "info_btn"))).click()
                self.moveTab(2)

                agentzzimList = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".list-item")))

                if not len(agentzzimList) == 4:
                    raise Exception (u"안심중개사 즐겨찾기 매물 개수가 상이합니다.", len(agentzzimList))

                self.driver.find_elements_by_class_name("list-item")[0].click()
                self.moveTab(3)
                self.driver.close()
                self.moveTab(2)
                self.driver.close()
                self.moveTab(1)

                # 10. 추천 매물 더보기

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "view_agent_reco"))).click()
                self.moveTab(2)
                self.driver.close()
                self.moveTab(1)

                self.driver.execute_script("window.scrollTo(0, 0);")

                # 11. 간편하게 문의 요청하기

                dt2 = datetime.datetime.now().hour

                if (dt2 > 22 or dt2 < 8):

                    self.wait.until(EC.visibility_of_element_located((By.ID, "phone3"))).send_keys("테스트 휴대폰 번호")

                    self.wait.until(EC.visibility_of_element_located((By.ID, "comment3"))).send_keys(u"테스트 문자 내용")

                    self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry3"))).click()

                    self.wait.until(EC.alert_is_present()).accept()

                    self.wait.until(EC.visibility_of_element_located((By.ID, "check_agree3"))).click()
                    time.sleep(3)

                    self.driver.find_elements_by_css_selector(".layer-btn > button")[1].click()

                    self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry3"))).click()

                    self.wait.until(EC.alert_is_present()).accept()
                    time.sleep(1)

                else:

                    self.wait.until(EC.visibility_of_element_located((By.ID, "phone2"))).send_keys("테스트 휴대폰 번호")

                    self.wait.until(EC.visibility_of_element_located((By.ID, "comment2"))).send_keys(u"테스트 문자 내용")

                    self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry2"))).click()

                    self.wait.until(EC.alert_is_present()).accept()

                    self.wait.until(EC.visibility_of_element_located((By.ID, "check_agree2"))).click()
                    time.sleep(3)

                    self.driver.find_elements_by_css_selector(".layer-btn > button")[1].click()

                    self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry2"))).click()

                    self.wait.until(EC.alert_is_present()).accept()
                    time.sleep(1)

                break

            except Exception:

                if count == 2:
                    raise

                else:
                    traceback.print_exc(file=sys.stdout)
                    print("에러 발생 페이지 URL : ", self.driver.current_url)
                    self.driver.quit()
                    self.setUp()
                    count += 1

    def tearDown(self):
        self.driver.quit()