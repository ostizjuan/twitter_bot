from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Tweet:

    def __init__(self, msg=None):
        self.__url = 'https://twitter.com/login'
        self.logged = False
        self.__browser = None
        self.msg = msg

    def __create_driver(self):
        options = Options()
        options.headless = False
        self.__browser = webdriver.Chrome(options=options)

    def login(self, username, password):
        try:
            self.__create_driver()
            self.__browser.get(self.__url)
            WebDriverWait(self.__browser, timeout=15).until(
                lambda driver: driver.find_element(By.NAME, 'text')).send_keys(username)

            WebDriverWait(self.__browser, timeout=15).until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]'))).click()

            WebDriverWait(self.__browser, timeout=15).until(
                lambda driver: driver.find_element(By.NAME, 'password')).send_keys(password)

            WebDriverWait(self.__browser, timeout=15).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"][role="button"]'))).click()

            self.logged = True
            return 'Loged'

        except Exception as error:
            return f'There was an error while loading the page: {error}'

    def push_tweet(self):
        if self.__msg and self.logged:
            try:
                WebDriverWait(self.__browser, timeout=15).until(lambda driver: driver.find_element(
                    By.CSS_SELECTOR, 'br[data-text="true"]')).send_keys(self.msg)

                WebDriverWait(self.__browser, timeout=15).until(lambda driver: driver.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"][role="button"]')).click()

                return 'Tweet success'

            except Exception as error:
                return f'There was an error while loading the page.\n{error}'
        elif self.msg:
            raise Exception('You new to log in first')
        else:
            raise Exception('You new to set a message')

    def stop(self):
        if self.__browser is not None:
            self.__browser.close()

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, msg):
        self.__msg = msg
