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
from selenium.webdriver import ActionChains
from wwwauto.helper import helper

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class item_zzimTest(unittest.TestCase):

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

                confirmAccount = "인증 계정"
                confirmpwAccount = "인증 계정"

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 찜한 방 접속

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[0]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "찜한 방"))).click()
                time.sleep(1)

                # 2. 로그인 버튼 클릭

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(confirmAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(confirmpwAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                # 3. 찜 매물 개수 확인

                zzimList = len(self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item"))))

                zzimCount = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-title > span"))).text
                zzimReplace = zzimCount.replace("(", "").replace(")", "")

                if not int(zzimList) == int(zzimReplace):
                    raise Exception("찜 개수가 상이함으로 자동화를 종료합니다.", "찜 리스트 : ", int(zzimList), "찜 개수 표시 : ", int(zzimReplace))

                # 5. 전체 선택 및 전체 해제 (삭제)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "allcheck_btn1"))).click()

                # self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "allclear_btn1"))).click()

                # # 6. 매물 선택 후 찜 삭제
                #
                # self.wait.until(EC.visibility_of_all_elements_located((By.NAME, "check")))[0].click()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"삭제"))).click()

                self.wait.until(EC.alert_is_present()).accept()

                # zzimList = len(self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item"))))
                #
                # zzimCount = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-title > span"))).text
                # zzimReplace = zzimCount.replace("(", "").replace(")", "")
                #
                # if not int(zzimList) == int(zzimReplace):
                #     raise Exception("찜 개수가 상이함으로 자동화를 종료합니다.", "찜 리스트 : ", int(zzimList), "찜 개수 표시 : ", int(zzimReplace))

                break

            except Exception:

                if count == 2:
                    raise

                else:
                    helper.screen_capture(self.helper)
                    traceback.print_exc(file=sys.stdout)
                    print("에러 발생 페이지 URL : ", self.driver.current_url)
                    self.driver.quit()
                    self.setUp()
                    count += 1

    def tearDown(self):
        self.driver.quit()