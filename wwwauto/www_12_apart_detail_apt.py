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
from wwwauto.helper import helper

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class apart_detail_aptTest(unittest.TestCase):

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
        self.helper = helper(self)

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

                # 1. 아파트 상세화면 진입

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_apartments"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'테스트할 아파트 명')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(1)

                # 2. 상세 세부 기능

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='collapsible-box close']"))).click()
                # 단지 기본정보 펼치기
                time.sleep(1)

                # ratecount = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".i-arrow em span"))).text
                # 거주민 평가 개수 (현재 미사용)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='title-box type-link type-txt']")))[0].click()
                # 거주민 평가 페이지 진입
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".item-header > button"))).click()
                # 닫기 버튼 클릭

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='title-box type-link type-txt']")))[1].click()
                # 현장 투어 페이지 진입
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".item-header > button"))).click()
                # 닫기 버튼 클릭

                danjiZzim = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class='btn-zzim']")))
                # 아파트 찜 버튼 엘리먼트

                danjiZzim.click()
                # 찜 하기
                time.sleep(1)

                danjiZzim.click()
                # 찜 해제
                time.sleep(1)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='title-box type-link ']")))[0].click()
                # 우리집 내놓기 버튼 클릭
                self.moveTab(1)
                self.driver.close()
                self.moveTab(0)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='title-box type-link ']")))[1].click()
                # 아파트정보 제공하기 버튼 클릭
                self.moveTab(1)
                self.driver.close()
                self.moveTab(0)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".content-header > button"))).click()
                # 아파트 상세 닫기
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