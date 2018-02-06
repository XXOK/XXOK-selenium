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
from selenium.webdriver import ActionChains

class my_roomsTest(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to_window(window_before)
        return time.sleep(2)

    def setUp(self):
        self.chromeDriver = os.path.abspath('../zigbang_web_monitoring/driver/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 5)

    def runTest(self):
        count = 0
        while True:
            try:
                zigbangUrl = "https://www.zigbang.com/"

                confirmAccount = "dustls456@naber.com"
                confirmpwAccount = "asd12345"
                wording = u"QA파트 자동화 테스트 (실제 매물이 아닙니다)"

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 중개사무소에 방 내놓기·관리 접속

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[0]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"중개사무소에 방 내놓기·관리"))).click()
                time.sleep(1)

                # 2. 인증 회원 로그인

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(confirmAccount)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".mb-20 > button"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(confirmpwAccount)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))).click()
                time.sleep(1)

                # 3. 등록 매물 개수 확인

                splitInfo = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".item-title > span")))
                splitInfo2 = (splitInfo.text).split(':')
                splitInfo3 = splitInfo2[1].split(' ')
                roomscountInfo = int(splitInfo3[1].replace('개', ''))

                roomscountList = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='i-tag']")))

                if not roomscountInfo == len(roomscountList):
                    raise Exception ("등록 매물 개수가 상이합니다.", "매물 리스트 : ", len(roomscountList), "매물 개수 표시: ", roomscountInfo)

                # 4. 중개사무소에 방 내놓기란?

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-banner"))).click()
                self.moveTab(1)
                self.driver.close()
                self.moveTab(0)

                # 5. 방 내놓기 이용가이드 (PDF)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-rooms"))).click()
                self.moveTab(1)
                self.driver.close()
                self.moveTab(0)

                # 6. 수정 후 방 내놓기

                try:
                    self.driver.find_element_by_css_selector("button[class='close_room']").click()
                    # 방 내리기 버튼 클릭 (예외 상황 처리)
                    time.sleep(1)

                    self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".layer-btn > button")))[0].click()
                    time.sleep(1)

                except:
                    pass

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".i-btn > button")))[1].click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".layer-btn > button")))[0].click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.NAME, "deposit"))).clear()
                self.wait.until(EC.visibility_of_element_located((By.NAME, "deposit"))).send_keys("9999")
                # 보증금 값 입력

                self.wait.until(EC.visibility_of_element_located((By.NAME, "rent"))).clear()
                self.wait.until(EC.visibility_of_element_located((By.NAME, "rent"))).send_keys("9999")
                # 월세 값 입력

                roomsType = self.wait.until(EC.visibility_of_element_located((By.NAME, "room_type")))
                # 방 구조 옶션 값 저장

                roomstypeValue = roomsType.find_elements_by_tag_name("option")[1]
                roomstypeValue.click()
                # 오픈형 원룸 (방1) 값 선택

                self.wait.until(EC.visibility_of_element_located((By.NAME, "fee"))).clear()
                self.wait.until(EC.visibility_of_element_located((By.NAME, "fee"))).send_keys("9999")
                # 관리비 값 입력

                roomsFloor = self.wait.until(EC.visibility_of_element_located((By.NAME, "room_floor")))
                # 해당 층 값 저장

                roomsfloorValue = roomsFloor.find_elements_by_tag_name("option")[3]
                roomsfloorValue.click()
                # 1층 값 선택

                self.driver.execute_script("arguments[0].scrollIntoView()", roomsFloor)
                # 해당 층 엘리먼트 영역으로 화면 스크롤
                time.sleep(1)

                roomsDirection = self.wait.until(EC.visibility_of_element_located((By.NAME, "room_direction")))
                # 방향 옵션 값 저장

                roomsdirectionValue = roomsDirection.find_elements_by_tag_name("option")
                roomsdirectionValue[1].click()
                # 동향 선택

                self.wait.until(EC.visibility_of_all_elements_located((By.NAME, "loan")))[0].click()
                # 전세 대출 가능 선택

                self.wait.until(EC.visibility_of_all_elements_located((By.NAME, "pets")))[0].click()
                # 반려동물 가능 선택

                self.wait.until(EC.visibility_of_all_elements_located((By.NAME, "parking")))[0].click()
                # 주차 가능 선택

                self.wait.until(EC.visibility_of_all_elements_located((By.NAME, "building_elevator")))[0].click()
                # 엘리베이터 있음 선택

                self.wait.until(EC.visibility_of_element_located((By.NAME, "movein_date"))).clear()
                self.wait.until(EC.visibility_of_element_located((By.NAME, "movein_date"))).send_keys(wording)
                # 입주가능일 작성

                self.wait.until(EC.visibility_of_element_located((By.NAME, "title"))).clear()
                self.wait.until(EC.visibility_of_element_located((By.NAME, "title"))).send_keys(wording)
                # 제목 작성

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "description"))).clear()
                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "description"))).send_keys(wording * 5)
                # 상세설명 작성

                self.wait.until(EC.visibility_of_element_located((By.NAME, "to_agent"))).clear()
                self.wait.until(EC.visibility_of_element_located((By.NAME, "to_agent"))).send_keys(wording)
                # 중개사에게 남기는 메세지 작성

                addRoom = self.wait.until(EC.visibility_of_element_located((By.ID, "add_room")))
                self.driver.execute_script("arguments[0].scrollIntoView()", addRoom)
                time.sleep(1)
                addRoom.click()
                # 방 내놓기 버튼 클릭
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".agent-box > button"))).click()
                # 중개사무소 방 내놓기 완료 페이지 > 확인 버튼 클릭
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".i-btn > button"))).click()
                # 방 내리기 버튼 클릭
                time.sleep(1)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".layer-btn > button")))[0].click()
                # 방 내리기 확인 팝업 > 확인 버튼 클릭
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