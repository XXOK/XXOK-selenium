import os
import datetime
from selenium import webdriver

class helper:
    def __init__(self, testCase):
        self.testCase = testCase
        self.driver = testCase.driver

    def screen_capture(self):
        screenshotsPath = os.getcwd() +'/screenshots/'
        directoryName = str(datetime.date.today())

        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d%H:%M:%S')

        filePath = screenshotsPath+directoryName+'/'

        if not os.path.isdir(screenshotsPath + directoryName):
            os.mkdir(screenshotsPath + directoryName)
        self.driver.save_screenshot(filePath + nowDatetime +'.png')
