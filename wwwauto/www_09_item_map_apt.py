#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import unittest
import sys, traceback
import platform
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class item_map_aptTest(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to_window(window_before)
        return time.sleep(2)

    def setUp(self):
        self.chromeDriver = PATH('../drivers/mac/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 5)

    def runTest(self):
        count = 0
        while True:
            try:
                zigbangUrl = "https://www.zigbang.com/"

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_apt_app_down', 'value': 'true'})  # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 교통정보 상세화면 진입

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_apartments"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys('강남역')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(2)

                # 2. 교통정보 상세화면 > 역 이름 확인

                stationName = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title"))).text

                if not stationName == "강남역":
                    raise Exception("역 이름이 상이함으로 자동화를 종료합니다.", stationName)

                # 3. 인기아파트 상세 진입

                popApart = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".i-tit > strong"))).text
                # 인기아파트 최상단 매물 이름 엘리먼트

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='listItem listItemA  type-img type-click desc2-blue']")))[0].click()
                # 인기아파트 최상단 매물 클릭
                time.sleep(2)

                apartName = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title"))).text
                # 아파트 상세화면 이름 엘리먼트

                if not stationName == popApart:
                    raise Exception("역 이름이 상이함으로 자동화를 종료합니다.", popApart, apartName)

                # 4. 학교 상세 진입

                schooldInfo = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i-tit"))).text
                # 학군 정보 최상단 학교 이름 엘리먼트

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='listItem listItemB type-blue type-click']")))[0].click()
                # 학군 정보 최상단 학교 클릭
                time.sleep(2)

                schoolName = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title"))).text
                # 학교 상세화면 이름 엘리먼트

                if not schooldInfo == schooldInfo:
                    raise Exception("역 이름이 상이함으로 자동화를 종료합니다.", schooldInfo, schoolName)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".content-header > button")))[1].click()
                # 닫기 버튼 클릭

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