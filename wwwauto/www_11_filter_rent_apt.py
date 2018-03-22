#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import pdb
import unittest
import sys, traceback
import platform
import re
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from wwwauto.helper import helper

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class filter_rent_aptTest(unittest.TestCase):

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

                # 1. 매물 접속

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[1]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"매물"))).click()
                time.sleep(2)

                # 2. 아파트 지도 화면 > 전월세 필터 기능

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class='btn-change-unit']"))).click()
                # 평 단위 변환 버튼 클릭 (1회)
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "price-btn-wrap"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".sale-type-holder > div:last-child"))).click()
                # 전월세 클릭
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn"))).click()
                # 필터 클릭
                time.sleep(2)

                # 3. 면적(공급면적) 10평 이하 필터

                salearea = []
                # 가공된 아파트 면적(공급면적) 리스트

                areaOption = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, " item")))
                # 면적(공급면적) 필터 버튼

                areaOption[1].click()
                # 10평 이하 클릭

                try:
                    self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-msg")))
                    print("10평 이하 검색 결과가 존재하지 않습니다.")
                    # 검색 결과가 없는 경우 Pass 처리

                except:
                    saleareaValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "p[class='p1']")))
                    # 여러개의 아파트 매물 평 데이터 받아오기

                    for i in saleareaValue:
                        areaSplit = (i.text).split('/')
                        salearea.append(int(re.findall('\d+', areaSplit[0])[0]))
                        # 면적 값의 문자 제거 정규식

                    for i in range(len(salearea)):
                        # 매물 검색 결과 개수 만큼 테스트
                        if not salearea[i] <= 10:
                            raise Exception("10평 이하 면적 검색 결과 값이 상이함으로 자동화를 종료합니다.", str(salearea[i]))

                # 3-1. 면적(공급면적) 10평 이하 ~ 10평대 필터

                salearea1 = []
                # 가공된 아파트 면적(공급면적) 리스트

                areaOption[2].click()
                # 10평대 클릭

                try:
                    self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-msg")))
                    print("10평 이하 ~ 10평대 필터 검색 결과가 존재하지 않습니다.")
                    # 검색 결과가 없는 경우 Pass 처리

                except:
                    saleareaValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "p[class='p1']")))
                    # 여러개의 아파트 매물 평 데이터 받아오기

                    for i in saleareaValue:
                        areaSplit = (i.text).split('/')
                        salearea1.append(int(re.findall('\d+', areaSplit[0])[0]))
                        # 면적 값의 문자 제거 정규식

                    for i in range(len(salearea1)):
                        # 매물 검색 결과 개수 만큼 테스트
                        if not 0 < salearea1[i] <= 19:
                            raise Exception("10평 이하 ~ 10평대 면적 검색 결과 값이 상이함으로 자동화를 종료합니다.", str(salearea1[i]))

                # 3-2. 면적(공급면적) 20평대 필터

                salearea2 = []
                # 가공된 아파트 면적(공급면적) 리스트

                areaOption[3].click()
                # 20평대 클릭

                try:
                    self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-msg")))
                    print("20평대 필터 검색 결과가 존재하지 않습니다.")
                    # 검색 결과가 없는 경우 Pass 처리

                except:
                    saleareaValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "p[class='p1']")))
                    # 여러개의 아파트 매물 평 데이터 받아오기

                    for i in saleareaValue:
                        areaSplit = (i.text).split('/')
                        salearea2.append(int(re.findall('\d+', areaSplit[0])[0]))
                        # 면적 값의 문자 제거 정규식

                    for i in range(len(salearea2)):
                        # 매물 검색 결과 개수 만큼 테스트
                        if not 20 <= salearea2[i] <= 29:
                            raise Exception("20평대 면적 검색 결과 값이 상이함으로 자동화를 종료합니다.", str(salearea2[i]))

                # 3-3. 면적(공급면적) 20평대 ~ 30평대 필터

                salearea3 = []
                # 가공된 아파트 면적(공급면적) 리스트

                areaOption[4].click()
                # 30평대 클릭

                try:
                    self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-msg")))
                    print("20평대 ~ 30평대 필터 검색 결과가 존재하지 않습니다.")
                    # 검색 결과가 없는 경우 Pass 처리

                except:
                    saleareaValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "p[class='p1']")))
                    # 여러개의 아파트 매물 평 데이터 받아오기

                    for i in saleareaValue:
                        areaSplit = (i.text).split('/')
                        salearea3.append(int(re.findall('\d+', areaSplit[0])[0]))
                        # 면적 값의 문자 제거 정규식

                    for i in range(len(salearea3)):
                        # 매물 검색 결과 개수 만큼 테스트
                        if not 20 <= salearea3[i] <= 39:
                            raise Exception("20평대 ~ 30평대 면적 검색 결과 값이 상이함으로 자동화를 종료합니다.", str(salearea3[i]))

                # 3-4. 면적(공급면적) 40평대 필터

                salearea4 = []
                # 가공된 아파트 면적(공급면적) 리스트

                areaOption[5].click()
                # 40평대 클릭

                try:
                    self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-msg")))
                    print("40평대 필터 검색 결과가 존재하지 않습니다.")
                    # 검색 결과가 없는 경우 Pass 처리

                except:
                    saleareaValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "p[class='p1']")))
                    # 여러개의 아파트 매물 평 데이터 받아오기

                    for i in saleareaValue:
                        areaSplit = (i.text).split('/')
                        salearea4.append(int(re.findall('\d+', areaSplit[0])[0]))
                        # 면적 값의 문자 제거 정규식

                    for i in range(len(salearea4)):
                        # 매물 검색 결과 개수 만큼 테스트
                        if not 40 <= salearea4[i] <= 49:
                            raise Exception("40평대 면적 검색 결과 값이 상이함으로 자동화를 종료합니다.", str(salearea4[i]))

                # 3-5. 면적(공급면적) 40평대 ~ 50평대 필터

                salearea5 = []
                # 가공된 아파트 면적(공급면적) 리스트

                areaOption[6].click()
                # 50평대 클릭

                try:
                    self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-msg")))
                    print("40평대 ~ 50평대 필터 검색 결과가 존재하지 않습니다.")
                    # 검색 결과가 없는 경우 Pass 처리

                except:
                    saleareaValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "p[class='p1']")))
                    # 여러개의 아파트 매물 평 데이터 받아오기

                    for i in saleareaValue:
                        areaSplit = (i.text).split('/')
                        salearea5.append(int(re.findall('\d+', areaSplit[0])[0]))
                        # 면적 값의 문자 제거 정규식

                    for i in range(len(salearea5)):
                        # 매물 검색 결과 개수 만큼 테스트
                        if not 40 <= salearea5[i] <= 59:
                            raise Exception("40평대 ~ 50평대 면적 검색 결과 값이 상이함으로 자동화를 종료합니다.", str(salearea5[i]))

                # 3-6. 면적(공급면적) 60평 이상 필터

                salearea6 = []
                # 가공된 아파트 면적(공급면적) 리스트

                areaOption[7].click()
                # 60평 이상 클릭

                try:
                    self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-msg")))
                    print("60평 이상 필터 검색 결과가 존재하지 않습니다.")
                    # 검색 결과가 없는 경우 Pass 처리

                except:
                    saleareaValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "p[class='p1']")))
                    # 여러개의 아파트 매물 평 데이터 받아오기

                    for i in saleareaValue:
                        areaSplit = (i.text).split('/')
                        salearea6.append(int(re.findall('\d+', areaSplit[0])[0]))
                        # 면적 값의 문자 제거 정규식

                    for i in range(len(salearea6)):
                        # 매물 검색 결과 개수 만큼 테스트
                        if not 60 <= salearea6[i]:
                            raise Exception("60평 이상 면적 검색 결과 값이 상이함으로 자동화를 종료합니다.", str(salearea6[i]))

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class='btn-reset-filter']"))).click()
                time.sleep(1)
                # 필터 초기화

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class='btn-close-filter']"))).click()
                # 필터 창 닫기

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