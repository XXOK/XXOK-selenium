#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import pdb
import unittest
import sys, traceback
import platform
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class mainTest(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to_window(window_before)
        return time.sleep(2)

    def setUp(self):
        self.chromeDriver = PATH('../drivers/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 5)

    def runTest(self):
        count = 0
        while True:
            try:
                zigbangUrl = "https://www.zigbang.com/"

                illbanidAccount = "미인증 계정"
                confirmAccount = "인증 계정"
                confirmpwAccount = "인증 계정"
                agentAccount = "중개사 계정"
                agentpwAccount = "중개사 계정"

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 미인증 계정 로그인

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(illbanidAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                userName = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='i_user']"))).text

                if not u"강연신" == userName:
                    raise Exception(u"사용자 이름이 일치하지 않습니다.", userName)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_user"))).click()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"로그아웃"))).click()

                # 2. 인증 계정 로그인

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(confirmAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[type='password']"))).send_keys(confirmpwAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                userName = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='i_user']"))).text

                if not u"사용자 계정" == userName:
                    raise Exception(u"사용자 이름이 일치하지 않습니다.", userName)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_user"))).click()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"로그아웃"))).click()

                # 3. 중개사 계정 로그인

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(agentAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(agentpwAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_link"))).click()
                self.moveTab(1)
                self.driver.close()
                self.moveTab(0)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_user"))).click()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"로그아웃"))).click()

                # 4. 원,투룸 지역 검색
                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u"경상북도 울릉군 울릉읍")

                locationSearch = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ui-menu-item")))
                locationSearch[0].click()

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 5. 원,투룸 지하철 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'강남역')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(1)

                stationName = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='list-title']")))[0].text[0:3]

                if not u"강남역" == stationName:
                    raise Exception(u"역이름이 일치하지 않습니다.", stationName)

                self.driver.execute_script("window.history.go(-1)")

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 6. 원,투룸 오피스텔 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'테스트할 오피스텔명')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(1)

                offiName = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='list-title']")))[0].text[0:9]

                if not u"테스트할 오피스텔명" == offiName:
                    raise Exception(u"오피스텔명이 일치하지 않습니다.", offiName)

                self.driver.execute_script("window.history.go(-1)")

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 7. 아파트 지역 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_apartments"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'경상북도 울릉군 울릉읍')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(1)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 8. 아파트 지하철 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'강남역')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(1)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 9. 아파트 명 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'테스트할 아파트명')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(1)

                aptName = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='i-tit']"))).text[0:6]

                if not u'테스트할 아파트명' == aptName:
                    raise Exception(u"아파트명이 일치하지 않습니다.", aptName)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 10. 중개사 가입 배너 클릭

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "m-tv"))).click()

                if not "https://www.zigbang.com/home/RegisterInfo" == self.driver.current_url :
                    raise Exception(u"CEO 페이지 링크가 잘못되었습니다")
                    # 이동 된 페이지 링크 검사

                self.driver.execute_script("window.history.go(-1)", self.driver.current_url)

                # 11. 뉴스 및 공지사항 더 보기 버튼 클릭
                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "item_more")))[0].click()

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(1)

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "item_more")))[1].click()

                self.driver.execute_script("window.history.go(-1)")
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