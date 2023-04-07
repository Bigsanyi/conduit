from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, date, time, timezone

class TestConduit(object):

    def setup_method(self):
        s = Service(executable_path=ChromeDriverManager().install())
        o = Options()
        o.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(service=s, options=o)
        URL = 'http://localhost:1667/'
        self.browser.get(URL)
        self.browser.maximize_window()
        self.unique = datetime.now().strftime("%Y%m%d%H%M%S")

    def teardown_method(self):
        self.browser.quit()

    def test_all(self):
        self.t_registry()
        self.t_login()

    def t_registry(self):
        sign_up = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/register"]')))
        assert self.browser.title == 'Conduit'
        assert self.browser.current_url == 'http://localhost:1667/#/'
        assert 'http://localhost:1667/#/' in self.browser.current_url
        sign_up.click()
        username = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        email = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]')
        password = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]')
        sign_up_btn = self.browser.find_element(By.CSS_SELECTOR, 'button')

        username.send_keys(f'Teszt{self.unique}')
        email.send_keys(f'{self.unique}@szerver.hu')
        password.send_keys('Abcd1234')
        sign_up_btn.click()

        ok_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'swal-button--confirm')))

        assert self.browser.find_element(By.CLASS_NAME, 'swal-button--confirm').text == "OK"
        ok_btn.click()

    def t_login(self):
        sign_in = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/login"]')
        assert self.browser.title == 'Conduit'
        assert self.browser.current_url == 'http://localhost:1667/#/'
        assert 'http://localhost:1667/#/' in self.browser.current_url
        sign_in.click()
        sign_in_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button')))
        assert sign_in_button.is_displayed()

        email = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]')
        password = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]')

        email.send_keys(f'{self.unique}@szerver.hu')
        password.send_keys('Abcd1234')
        sign_in_button.click()

    # weboldal menyitása és bejelentkezés, korábban regisztrált felhasználóval
    '''def page_open(self):

    def test_stuff(self):
        self.page_open()
        sign_in = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/login"]')
        sign_up = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/register"]')
        assert self.browser.title == 'Conduit'
        assert self.browser.current_url == 'http://localhost:1667/#/'
        assert 'http://localhost:1667/#/' in self.browser.current_url


'''
