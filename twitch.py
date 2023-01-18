from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
import undetected_chromedriver as uc

import time
import logging

# setup logging
logging.basicConfig(
    format="%(asctime)s : %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
    filename="log.txt",
)


class TwitchAPI:
    def __init__(self, token, streamer, headless=True, logs=True):
        self.logs = logs
        self.streamer = streamer
        self.driver = self._init_driver(token, headless)

    def log(self, message):
        if self.logs:
            logging.info(message)

    def _init_driver(self, token, headless=True):
        """
        will create webdriver that is fullscrened (for reason to appear chat and points)
        and add auth-token cookie (login)
        """
        self.log("creating driver")
        options = Options()
        if headless:
            self.log("driver will be headles")
            options.add_argument("--headless")
        else:
            self.log("driver will be displayed")
        driver = uc.Chrome(options=options)
        driver.set_window_size(1920, 1280)
        self.log(f"getting {self.streamer} twitch")
        driver.get(f"https://www.twitch.tv/{self.streamer}")
        self.log("adding auth cookies")
        driver.add_cookie({"name": "auth-token", "value": f"{token}"})
        driver.refresh()  # refresh to update cookie
        self.log("driver created succesfully")
        return driver

    def is_streamer_online(self):
        """
        will return True when stream is online if is not then return False
        """
        self.refresh_and_set_up_stream()
        self.log(f"checking if {self.streamer} is online")
        try:
            # Number of viewers
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "p[data-a-target='animated-channel-viewers-count']",
                    )
                )
            )
            self.log(f"streamer {self.streamer} is online")
            return True
        except TimeoutException:
            self.log(f"streamer {self.streamer} is offline")
            return False

    def get_points(self):
        """
        if are points to pickup, then pick them up and return True,
        else return False
        """
        self.log("looking for point")
        try:
            self.points_button = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[1]/aside/div/div/div/div/div/section/div/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button",
            )
            self.points_button.click()
            self.log("points are collected")
        except NoSuchElementException:
            self.log("no points found")

    def refresh_and_set_up_stream(self):
        """
        refresh stream, will click adults button and set quality for stream 160p
        """
        self.driver.refresh()
        # if streamer will have set stream only for adults, will click accept button
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'button[class="ScCoreButton-sc-ocjdkq-0 ScCoreButtonPrimary-sc-ocjdkq-1 ibtYyW eVWnXL"]',
                    )
                )
            ).click()
            self.log("age verificitaion clicked")
        except:
            pass
        """
        will set up video quality for 160p for consumption saving
        
        try 3x to set lower quality, if it will fail then will continue
        """
        time.sleep(3)  # let stream load

        loop_count = 0
        MAXIMUM_LOOP_NUMBER = 3
        while loop_count < MAXIMUM_LOOP_NUMBER:
            try:
                # will get button for setting and click it
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[1]/div[2]/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[6]/div/section/div/div[2]/div[1]/div[2]/div/button",
                        )
                    )
                ).click()

                # get quality option a nd click it
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div[1]/div[2]/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[4]/div/div/div/div/div/div/div/div/div[3]/button",
                        )
                    )
                ).click()

                # get 160p and click it
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div[1]/div[2]/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[4]/div/div/div/div/div/div/div/div/div[9]/div/div/div/div",
                        )
                    )
                ).click()
                self.log("low resolution was setted")
                break
            except:
                self.log("couldnt set lower resolutions, trying again")
                loop_count += 1
                if loop_count == MAXIMUM_LOOP_NUMBER:
                    self.log("cant set low resolution, skipping...")
