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

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class filter_sale_aptTest(unittest.TestCase):

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

                # 2. 아파트 지도 화면 > 매매 필터 기능

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class='btn-change-unit']"))).click()
                # 평 단위 변환 버튼 클릭 (1회)
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn"))).click()
                # 필터 클릭
                time.sleep(2)

                # 3. 매매가 필터

                rndSale = random.randint(0,292)
                # 매매가 필터 범위 랜덤 선택

                saleMinslider = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class = 'rc-slider-handle rc-slider-handle-1']")))

                # 매매가 필터 옵션 값
                # 0~7 > / 전체, 전체
                # 8~23 > 16 / 5천, 18억
                # 24~38 > 15 / 1억, 16억
                # 39~54 > 16 / 1억5천, 14억
                # 55~69 > 15 / 2억, 12억
                # 70~85 > 16 / 2억5천, 10억
                # 86~100 > 15 / 3억, 9억
                # 101~116 > 16 / 3억5천, 8억
                # 117~131 > 15 / 4억, 7억
                # 132~147 > 16 / 4억5천, 6억
                # 148~162 > 15 / 5억, 5억
                # 163~178 > 16 / 6억, 4억5천
                # 179~193 > 15 / 7억, 4억
                # 194~209 > 16 / 8억, 3억5천
                # 210~224 > 15 / 9억, 3억
                # 225~240 > 16 / 10억, 2억5천
                # 241~255 > 15 / 12억, 2억
                # 256~271 > 16 / 14억, 1억5천
                # 272~286 > 15 / 16억, 1억
                # 287~302(287~292) > 16 / 18억, 5천

                dragMinslider = ActionChains(self.driver).drag_and_drop_by_offset(saleMinslider, rndSale, 0)
                dragMinslider.perform()

                tooltipMin = self.driver.find_elements_by_class_name("rc-slider-tooltip-inner")[0].text
                # 매매가 툴팁 최소 값

                if tooltipMin == '최소':
                    saleMin = int(0)

                elif tooltipMin == '5,000':
                    saleMin = int(tooltipMin.replace(',', ''))

                elif len(tooltipMin) <= 3:
                    saleMin = int(tooltipMin.replace('억', '0000'))

                else:
                    saleMin = int(tooltipMin.replace('억', '').replace(',', ''))

                saleMaxslider = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class = 'rc-slider-handle rc-slider-handle-2']")))
                # 매매가 최대 값 슬라이더 엘리먼트

                dragMaxslider = ActionChains(self.driver).drag_and_drop_by_offset(saleMaxslider, -rndSale, 0)
                dragMaxslider.perform()

                hoverMaxslider = ActionChains(self.driver).move_to_element(saleMaxslider)
                hoverMaxslider.perform()
                time.sleep(1)
                # '최대'의 경우 마우스 오버 필요

                tooltipMax = self.driver.find_elements_by_class_name("rc-slider-tooltip-inner")[1].text
                # 매매가 툴팁 최대 값

                if tooltipMax == '최대':
                    saleMax = int(1000000)

                elif len(tooltipMax) <= 3:
                    saleMax = int(tooltipMax.replace('억', '0000'))

                salePrice = []
                # 가공된 아파트 매매가 리스트

                try:
                    self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-msg")))
                    print("매매가 검색 결과가 존재하지 않습니다.")
                    # 검색 결과가 없는 경우 Pass 처리

                except:
                    salepriceValue = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.card_a-container h3')))
                    # 여러개의 아파트 매물 매매가 데이터 받아오기

                    for i in salepriceValue:
                        saleValue = (i.text).split(' ')
                        saleValue2 = saleValue[1].replace('억', '')

                        if len(saleValue2) < 3:
                            salePrice.append(int(saleValue2+'0000'))
                            # 천의 자리가 없는 경우

                        else:
                            saleReplace = saleValue2.replace(',', '')
                            salePrice.append(int(saleReplace))
                            # 천의 자리가 있는 경우

                    for i in range(len(salePrice)):
                        # 매물 검색 결과 개수 만큼 테스트
                        if not saleMin <= salePrice[i] <= saleMax:
                            raise Exception("매매가와 검색 결과 값이 상이함으로 자동화를 종료합니다.", saleMin, int(salePrice[i]), saleMax)

                # 4. 면적(공급면적) 10평 이하 필터

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

                # 4-1. 면적(공급면적) 10평 이하 ~ 10평대 필터

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

                # 4-2. 면적(공급면적) 20평대 필터

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

                # 4-3. 면적(공급면적) 20평대 ~ 30평대 필터

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

                # 4-4. 면적(공급면적) 40평대 필터

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

                # 4-5. 면적(공급면적) 40평대 ~ 50평대 필터

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

                # 4-6. 면적(공급면적) 60평 이상 필터

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