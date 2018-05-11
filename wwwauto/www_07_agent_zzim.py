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

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class agent_zzimTest(unittest.TestCase):

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

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 원,투룸 접속

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[0].click()
                time.sleep(1)

                # 2. 테스트 매물 상세 진입

                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys(u"강남역")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-delete"))).click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys(u"인천시 강화군 서도면")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-delete"))).click()
                time.sleep(1)

                listItem = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item ")))
                listItem[0].click()
                self.moveTab(1)

                # 3. 중개사무소 정보 진입 / 중개사 즐겨찾기 클릭

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "info_btn"))).click()
                self.moveTab(2)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn_zzim"))).click()
                time.sleep(1)
                self.driver.close()
                self.moveTab(1)
                self.driver.close()
                self.moveTab(0)

                # 4. 안심중개사 즐겨찾기 접속

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[0]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"안심중개사 즐겨찾기"))).click()

                # 5. 안심중개사 즐겨찾기 개수 확인

                agentzzimList = self.wait.until(EC.visibility_of_all_elements_located((By.ID, "zzim_list")))
                time.sleep(1)
                agentzzimInfo = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.item-title h3 span'))).text[1]
                time.sleep(1)

                if not len(agentzzimList) == int(agentzzimInfo):
                    raise Exception ("안심중개사 즐겨찾기 개수가 상이합니다.", "중개사 리스트 : ", len(agentzzimList), "중개사 명수 표시 : ", int(agentzzimInfo))

                # 6. 안심중개사 정보 영역 버튼 클릭

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"위치보기"))).click()
                self.moveTab(1)
                self.driver.close()
                self.moveTab(0)

                # 7. 안심중개사 즐겨찾기 해제

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn_zzim'))).click()

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