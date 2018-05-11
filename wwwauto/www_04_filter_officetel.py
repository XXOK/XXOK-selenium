#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import unittest
import random
import sys, traceback
import platform
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class filter_officetelTest(unittest.TestCase):

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

                # 1. 오피스텔 접속

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[0]
                ActionChains(self.driver).move_to_element(element_to_hover_over).perform()

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "gnb-item-officetel"))).click()
                time.sleep(1)

                # 2. 방 구조 '오픈형 원룸' 선택 및 유효성 검사

                checkOption = self.wait.until(EC.visibility_of_any_elements_located((By.XPATH, "//input[@type='checkbox']")))

                for i in range(1, 5, 1):
                    checkOption[i].click()
                    time.sleep(4)
                time.sleep(2)

                openType = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, ".i-info > em")))
                time.sleep(1)

                for i in openType:
                    if not (i.text == u"오픈형 원룸"):
                        raise Exception(u"방구조가 오픈형 원룸 이 아닌 매물이 존재합니다.", i.text)

                # 2-1. 방 구조 '분리형 원룸' 선택 및 유효성 검사

                for i in reversed(range(0, 2, 1)):
                    checkOption[i].click()
                    time.sleep(4)
                time.sleep(2)

                partroomType = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".i-info > em")))
                time.sleep(1)

                for i in partroomType:
                    if not (i.text == u"분리형 원룸"):
                        raise Exception(u"방구조가 분리형 원룸 이 아닌 매물이 존재합니다.", i.text)

                # 2-2. 방 구조 '복층형 원룸' 선택 및 유효성 검사

                for i in reversed(range(1, 3, 1)):
                    checkOption[i].click()
                    time.sleep(4)
                time.sleep(2)

                upType = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, ".i-info > em")))
                time.sleep(1)

                for i in upType:
                    if not (i.text == u"복층형 원룸"):
                        raise Exception(u"방구조가 복층형 원룸 이 아닌 매물이 존재합니다.", i.text)

                # 2-3. 방 구조 '투룸' 선택 및 유효성 검사

                for i in reversed(range(2, 4, 1)):
                    checkOption[i].click()
                    time.sleep(4)
                time.sleep(2)

                tworoomType = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, ".i-info > em")))
                time.sleep(1)

                for i in tworoomType:
                    if not (i.text == u"투룸"):
                        raise Exception(u"방구조가 투룸 이 아닌 매물이 존재합니다.", i.text)

                # 2-4. 방 구조 '쓰리룸+' 선택 및 유효성 검사

                for i in reversed(range(3, 5, 1)):
                    checkOption[i].click()
                    time.sleep(4)
                time.sleep(2)

                threeroomType = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, ".i-info > em")))
                time.sleep(1)

                for i in threeroomType:
                    if not (i.text == u"쓰리룸" + u"+"):
                        raise Exception(u"방구조가 쓰리룸+ 이 아닌 매물이 존재합니다.", i.text)

                for i in range(0, 4):
                    checkOption[i].click()  # 원상 복구
                    time.sleep(1)
                time.sleep(3)

                # 3. 보증금 검색 조건 랜덤 선택

                emptyDeposit = []

                depositStart = Select(self.wait.until(EC.visibility_of_element_located((By.ID, 'deposit_s'))))
                depositEnd = Select(self.wait.until(EC.visibility_of_element_located((By.ID, 'deposit_e'))))
                # 샐랙트 박스의 값

                depositOption = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@name='deposit_s']")))
                depositoptValue = depositOption.find_elements_by_tag_name("option")

                for i in depositoptValue:
                    emptyDeposit.append(i.get_attribute("value"))

                depositstartValue = [i.text for i in depositStart.options]
                depositendValue = [i.text for i in depositEnd.options]
                # 샐랙트 박스에 대한 옵션 값들

                minDeposit = random.randint(1, len(depositstartValue) - 1)
                maxDeposit = random.randint(minDeposit,len(depositendValue) - 1)

                depositStart.select_by_visible_text(depositstartValue[minDeposit])
                time.sleep(3)
                depositEnd.select_by_visible_text(depositendValue[maxDeposit])
                time.sleep(3)

                # 4. 선택된 보증금 필터 값, 실제 매물과 비교

                depositCompmin = int(emptyDeposit[minDeposit])
                depositCompmax = int(emptyDeposit[maxDeposit])

                itemValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".i-tit")))
                # 매물의 금액 값

                for i in itemValue:
                    depositValue = (i.text).split('/')
                    depositEog = depositValue[0].split('억')

                    if len(depositEog[0]) == 1:
                        depositChun = depositEog[1].replace(',', '')
                        depositEmpty = int(depositEog[0] + ("0" * (4 - len(depositChun))) + depositChun)

                    else:
                        depositChun_Only = depositEog[0].replace(',', '')
                        depositEmpty = int("0" * (4 - len(depositChun_Only)) + depositChun_Only)

                    if not depositCompmin <= depositEmpty <= depositCompmax:
                        raise Exception("보증금 필터 값과 검색 결과 값이 상이함으로 자동화를 종료합니다.", depositCompmin, depositEmpty, depositCompmax)

                depositStart.select_by_visible_text(depositstartValue[0])
                time.sleep(3)
                depositEnd.select_by_visible_text(depositendValue[0])
                time.sleep(3)

                # 5. 월세 검색 조건 랜덤 선택

                emptyRent = []

                rentStart = Select(self.wait.until(EC.visibility_of_element_located((By.ID, 'rent_s'))))
                rentEnd = Select(self.wait.until(EC.visibility_of_element_located((By.ID, 'rent_e'))))
                # 샐랙트 박스의 값

                rentOption = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@name='rent_s']")))
                rentoptValue = rentOption.find_elements_by_tag_name("option")

                for i in rentoptValue:
                    emptyRent.append(i.get_attribute("value"))

                rentstartValue = [i.text for i in rentStart.options]
                rentendValue = [i.text for i in rentEnd.options]
                # 샐랙트 박스에 대한 옵션 값들

                minRent = random.randint(2, len(rentstartValue) - 1)
                maxRent = random.randint(minRent, len(rentendValue) - 1)

                rentStart.select_by_visible_text(rentstartValue[minRent])
                time.sleep(3)
                rentEnd.select_by_visible_text(rentendValue[maxRent])
                time.sleep(3)
                # 실제로 셀렉트 박스 선택하는 부분

                # 6. 선택된 월세 필터 값, 실제 매물과 비교

                rentCompmin = int(emptyRent[minRent])
                rentCompmax = int(emptyRent[maxRent])

                itemValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".i-tit")))
                # 매물의 금액

                for i in itemValue:
                    rentValue = (i.text).split('/')
                    rentSpace = rentValue[1].split(' ')

                    rentEmpty = 0

                    if len(rentSpace[0]) <= 3:
                        rentEmpty = int(rentSpace[0])

                    if not rentCompmin <= rentEmpty <= rentCompmax:
                        raise Exception("월세 필터 값과 검색 결과 값이 상이함으로 자동화를 종료합니다.", rentCompmin, rentEmpty, rentCompmax)

                rentStart.select_by_visible_text(rentstartValue[0])
                rentEnd.select_by_visible_text(rentendValue[0])

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