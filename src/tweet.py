from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.timer import Timer


class Tweet:

    def __init__(self, msg=None, timer=None):
        self.__url = 'https://twitter.com/login'
        self.logged = False
        self.__browser = None
        self.msg = msg
        self.timer = Timer(timer)

    def __create_driver(self):
        options = Options()
        options.headless = False
        self.__browser = webdriver.Chrome(options=options)

    def login(self, username, password):
        try:
            self.__create_driver()
            self.__browser.get(self.__url)
            user_element = WebDriverWait(self.__browser, timeout=15).until(
                lambda driver: driver.find_element(By.NAME, 'text')).send_keys(username)

            WebDriverWait(self.__browser, timeout=15).until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]'))).click()

            pass_element = WebDriverWait(self.__browser, timeout=15).until(
                lambda driver: driver.find_element(By.NAME, 'password')).send_keys(password)

            WebDriverWait(self.__browser, timeout=15).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"][role="button"]'))).click()

            # pass_element.send_keys(Keys.ENTER)
            self.__logged = True
            return 'Loged'

        except Exception as error:
            return f'There was an error while loading the page: {error}'

    def push_tweet(self):
        if self.__msg and self.logged:
            try:
                WebDriverWait(self.__browser, timeout=15).until(lambda driver: driver.find_element(
                    By.CSS_SELECTOR, 'br[data-text="true"]')).send_keys(self.__msg)

                WebDriverWait(self.__browser, timeout=15).until(lambda driver: driver.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]')).click()

                return 'Tweet success'

            except Exception as error:
                return f'There was an error while loading the page.\n{error}'
        elif self.msg:
            return 'You new to log in first'
        else:
            return 'You new to set a message'

    def stop(self):
        if (self.__browser):
            self.__browser.close()

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, msg):
        self.__msg = msg
