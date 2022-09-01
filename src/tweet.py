from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.timer import Timer

class Tweet:

    def __init__(self, msg=None, timer=600):
        self.__url = 'https://twitter.com/login'
        self.__logged = False
        self.__browser = None
        self.msg = msg
        self.timer = Timer(timer)
        self.__create_driver()

    def __create_driver(self):
        options = Options()
        options.headless = False
        self.__browser = webdriver.Chrome(options=options)

    def login(self, username, password):
        try:
            self.__browser.get(self.__url)
            user_element = WebDriverWait(self.__browser, timeout=15).until(lambda driver: driver.find_element(By.NAME, 'text')).send_keys(username)

            WebDriverWait(self.__browser, timeout=15).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]'))).click()

            pass_element = WebDriverWait(self.__browser, timeout=15).until(lambda driver: driver.find_element(By.CLASS_NAME, 'password')).send_keys(password)

            pass_element.send_keys(Keys.ENTER)
            self.__logged = True
            return 'Loged'

        except Exception as error:
            return f'There was an error while loading the page: {error}'

    def push_tweet(self):
        if self.__msg and self.__logged:
            try:
                WebDriverWait(self.__browser, timeout=15).until(lambda driver: driver.find_element(By.CSS_SELECTOR, 'br[data-text="true"]')).send_keys(self.__msg)
                
                WebDriverWait(self.__browser, timeout=15).until(lambda driver: driver.find_element(By.CSS_SELECTOR,'div[data-testid="tweetButtonInline"]')).click()

                return 'Tweet success'            

            except Exception as error:
                return f'There was an error while loading the page.\n{error}'
        elif self.msg:
            return 'You new to log in first'
        else:
            return 'You new to set a message'

    def stop(self):
        if(self.__browser):
            self.__browser.close()

    @property
    def msg(self):
        return self.__msg
    
    @msg.setter
    def msg(self, msg):
        self.__msg = msg