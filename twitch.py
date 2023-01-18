from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
import undetected_chromedriver as uc

import time
import logging

#setup logging
logging.basicConfig(format='%(asctime)s : %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO, filename='log.txt')

class TwitchAPI():
    def __init__(self, token, streamer, headless=True, logs=True):
        self.logs = logs
        self.streamer = streamer
        self.driver = self._initDriver(token, headless)


    def log(self, message):
        if self.logs:
            logging.info(message)


    def _initDriver(self, token, headless=True):
        self.log('creating driver')
        options = Options()
        if headless:
            self.log("driver will be headles")
            options.add_argument('--headless')
        else:
            self.log("driver will be displayed")
        driver = uc.Chrome(
            options=options
        )
        driver.set_window_size(1920, 1280)
        self.log(f"getting {self.streamer} twitch")
        driver.get(f"https://www.twitch.tv/{self.streamer}")
        self.log("adding auth cookies")
        driver.add_cookie({"name": "auth-token", "value":f"{token}"})
        driver.refresh()
        self.log("driver created succesfully")
        return driver


    def isStreamerOnline(self):
        '''
        will return True when stream is online if is not then return False
        '''
        self.refreshAndAgeVer()
        self.log(f"checking if {self.streamer} is online")
        try:
            # Number of viewers
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p[data-a-target='animated-channel-viewers-count']"))
            )
            self.log(f"streamer {self.streamer} is online")
            return True
        except TimeoutException:
            self.log(f"streamer {self.streamer} is offline")
            return False


    def getPoints(self):
        '''
        if are points to pickup, then pick them up and return True,
        else return False
        '''
        self.log("looking for point")
        time.sleep(10)
        try:
            self.points_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[1]/aside/div/div/div/div/div/section/div/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button")
            self.points_button.click()
            self.log("points are collected")
        except NoSuchElementException:
            self.log("no points found")

    def refreshAndAgeVer(self, r=0):
        self.driver.refresh()
        try:
            # Number of viewers
            AgeButton = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="ScCoreButton-sc-ocjdkq-0 ScCoreButtonPrimary-sc-ocjdkq-1 ibtYyW eVWnXL"]'))
            )
            AgeButton.click()
            self.log('age verificitaion clicked')
        except:
            pass
        x = 0
        time.sleep(3)
        while x < 3:
            try:
                #setting up 180p
                settingButton = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[6]/div/section/div/div[2]/div[1]/div[2]/div/button'))
                )
                settingButton.click()

                qualityButton = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[4]/div/div/div/div/div/div/div/div/div[3]/button'))
                )
                qualityButton.click()

                finalButton = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[4]/div/div/div/div/div/div/div/div/div[9]/div/div/div/div'))
                )
                finalButton.click()
                self.log('low resolution was setted')
                x = 4
            except:
                self.log('couldnt set lower resolutions, trying again')
                x += 1
                if x == 3:
                    self.log('cant set low resolution, skipping...')






# if __name__ == '__main__':
#     wrap = TwitchAPI(TOKEN, STREAMER, False)
#     wrap.getPoints()
#     time.sleep(3600)
#     wrap.driver.close()
