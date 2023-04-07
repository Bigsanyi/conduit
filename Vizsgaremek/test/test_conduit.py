'''Sziasztok, a GIT-en való futáskor az Allure-ban ezt találom hibaként:
"selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally.
  (unknown error: DevToolsActivePort file doesn't exist)
  (The process started from chrome location /usr/bin/google-chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.)"
'''
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
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)

        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(service=service, options=options)
        URL = 'http://localhost:1667/'
        self.browser.get(URL)
        self.browser.maximize_window()
        self.unique = datetime.now().strftime("%Y%m%d%H%M%S")

    # wait = WebDriverWait(self.browser, 10).until(self.browser.title == 'Conduit')
    def teardown_method(self):
        self.browser.quit()

    def test_statement(self):
        decline = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cookie__bar__buttons__button--decline')))
        decline.click()
        assert self.browser.current_url == 'http://localhost:1667/#/'
        sleep(1)
        assert self.browser.find_elements(By.CLASS_NAME, 'cookie__bar__buttons__button--decline') == []
        sleep(2)

    def test_registry(self):
        sign_up = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/register"]')))
        assert self.browser.title == 'Conduit'

        assert 'http://localhost:1667/#/' in self.browser.current_url
        sign_up.click()
        username = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        email = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]')
        password = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]')
        sign_up_btn = self.browser.find_element(By.CSS_SELECTOR, 'button')

        '''username.send_keys(f"TesztUser{self.unique}")
        email.send_keys(f"aateszt@{self.unique}.hu")
        password.send_keys('Abcd1234')
        sign_up_btn.click()'''

        username.send_keys("TesztUser")
        email.send_keys("teszt@vizsga.hu")
        password.send_keys('Abcd1234')
        sign_up_btn.click()

        ok_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'swal-button--confirm')))
        assert self.browser.find_element(By.CLASS_NAME, 'swal-button--confirm').text == "OK"
        ok_btn.click()

    # weboldal menyitása és bejelentkezés, korábban regisztrált felhasználóval
    def test_login(self):
        sign_in = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/login"]')
        assert self.browser.title == 'Conduit'

        sign_in.click()
        sign_in_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button')))
        assert sign_in_button.is_displayed()

        email = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]')
        password = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]')

        email.send_keys("teszt@vizsga.hu")
        password.send_keys('Abcd1234')
        sign_in_button.click()
        sleep(2)
        assert self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/@TesztUser/"]').text == "TesztUser"

    # ezt át kell írni

    def test_newpost(self):
        self.test_login()

        new_article = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/editor"]')
        new_article.click()
        article_title = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'form-control-lg')))
        about = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')
        write = self.browser.find_element(By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')
        tag = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')
        publish = self.browser.find_element(By.CLASS_NAME, 'btn-primary')
        article_title.send_keys(f'article{self.unique}')
        about.send_keys(f'about{self.unique}')
        write.send_keys(f'write{self.unique}')
        tag.send_keys(f'tag{self.unique}')
        sleep(2)
        assert article_title.get_attribute("value") == f'article{self.unique}'
        assert about.get_attribute("value") == f'about{self.unique}'
        assert write.get_attribute("value") == f'write{self.unique}'
        assert tag.get_attribute("value") == f'tag{self.unique}'
        publish.click()
        published = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))).text
        assert self.browser.find_element(By.CSS_SELECTOR, 'h1').text == f'article{self.unique}'
        sleep(2)
        home = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/"]')
        home.click()
        sleep(1)
        tag_published = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href="#/tag/tag{self.unique}"]')))
        assert tag_published.is_displayed()

        '''
                with open("deltee.txt", "w", encoding='utf-8') as file:
            file.write(str(tag_published))
        sleep(.5)
        TC1
        adatkezelési
        nyilatkozat
        használata
        adatok
        listázása
        több
        oldalas
        lista
        bejárása
        TC3
        új
        adat
        bevitele
        ismételt
        és
        sorozatos
        adatbevitel
        adatforrásból
        TC4
        meglévő
        adat
        módosítása
        adat
        vagy
        adatok
        törlése
        adatok
        lementése
        felületről
        kijelentkezés
        '''
