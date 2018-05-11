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
from selenium.webdriver.common.action_chains import ActionChains

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class item_detail_aptTest(unittest.TestCase):

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

                self.driver.add_cookie({'name': 'cookie_sms_apt_app_down', 'value': 'true'})  # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 아파트 상세화면 진입

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_apartments"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'테스트할 아파트 명')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(1)

                # 2. 아파트 매물 목록 진입

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-items-box "))).click()
                time.sleep(2)

                # 3. 아파트 매물 상세화면 진입

                aptitem = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "card_a-container")))[0]
                # 매물 리스트 최상단 위치 매물

                enterItem = ActionChains(self.driver).click(aptitem)
                enterItem.perform()

                self.moveTab(1)
                time.sleep(1)

                # 5. 신고하기 버튼 클릭

                # self.wait.until(EC.visibility_of_element_located((By.ID, "btn-report")))
                # time.sleep(3)
                #
                # self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "layer-close"))).click()
                # time.sleep(1)

                # 6. 문자 보내기

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn_contact_agent"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "phone"))).send_keys("테스트 휴대폰 번호")

                self.wait.until(EC.visibility_of_element_located((By.ID, "comment"))).send_keys(u"테스트 문자 내용")

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry"))).click()

                self.wait.until(EC.alert_is_present()).accept()

                self.wait.until(EC.visibility_of_element_located((By.ID, "check_agree"))).click()
                time.sleep(3)

                self.driver.find_elements_by_css_selector("button[class='btn btn-ok']")[1].click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry"))).click()

                self.wait.until(EC.alert_is_present()).accept()
                time.sleep(1)

                # 8. 중개사무소 정보 보기 버튼 클릭

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn_home_agent"))).click()
                self.moveTab(2)
                self.driver.close()
                self.moveTab(1)

                # 9. 문자 보내기 2

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "icon-question2")))[1].click()
                time.sleep(3)

                self.driver.find_elements_by_css_selector("button[class='btn-close icon-x2']")[1].click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "phone2"))).send_keys("테스트 휴대폰 번호")

                self.wait.until(EC.visibility_of_element_located((By.ID, "comment2"))).send_keys(u"테스트 문자 내용")

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry2"))).click()

                self.wait.until(EC.alert_is_present()).accept()

                self.wait.until(EC.visibility_of_element_located((By.ID, "check_agree2"))).click()
                time.sleep(3)

                self.driver.find_elements_by_css_selector("button[class='btn btn-ok']")[1].click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-inquiry2"))).click()

                self.wait.until(EC.alert_is_present()).accept()
                time.sleep(1)

                # 10. 실거래가 및 시세변동 버튼 클릭

                self.wait.until(EC.visibility_of_element_located((By.ID, "apt_area_info"))).click()
                time.sleep(3)

                self.driver.find_elements_by_css_selector("button[class='btn-close icon-x2']")[2].click()
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