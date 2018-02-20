#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import pytest
import unittest
import sys, traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class item_zzim_aptTest(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to_window(window_before)
        return time.sleep(2)

    def setUp(self):
        self.chromeDriver = PATH('../driver/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 5)

    def runTest(self):
        count = 0
        while True:
            try:
                zigbangUrl = "http://zigbang-www2.ecqnug3usp.ap-northeast-1.elasticbeanstalk.com/"

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_apt_app_down', 'value': 'true'})  # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 아파트 상세화면 진입

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_apartments"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'직방테스트5')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(1)

                # 2. 아파트 상세화면 > 찜 하기

                self.driver.find_element_by_css_selector("button[class='btn-zzim']").click()
                time.sleep(1)

                # 3. 찜한 아파트 진입

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[1]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"찜한 아파트"))).click()
                time.sleep(1)

                # 4. 찜한 아파트 매물 개수 유효성 검사

                zzimCnt = int(self.wait.until(EC.visibility_of_element_located((By.ID, "zzim-cnt"))).text)
                time.sleep(1)

                zzimItems = len(self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "zzim-item"))))
                time.sleep(1)

                if not zzimCnt == zzimItems:
                    raise Exception(u"찜한 아파트 매물 개수가 상이합니다.", zzimCnt, zzimItems)

                # 5. 지도에서 보기 버튼 클릭

                self.driver.find_element_by_class_name("btn_bx").click()
                self.moveTab(1)

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