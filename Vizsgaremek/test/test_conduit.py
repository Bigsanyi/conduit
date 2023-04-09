import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, date, time, timezone


class TestConduit(object):
    unique = datetime.now().strftime("%Y%m%d%H%M%S")

    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)

        '''options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')'''

        self.browser = webdriver.Chrome(service=service, options=options)
        URL = 'http://localhost:1667/'
        self.browser.get(URL)
        self.browser.maximize_window()
        sleep(2)
        # wait = WebDriverWait(self.browser, 5).until(self.browser.title == 'Conduit')

    def teardown_method(self):
        self.browser.quit()

    def test_statement(self):
        # TC1 Az adatkezelési nyilatkozat használata
        decline = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'cookie__bar__buttons__button--decline')))
        decline.click()
        assert self.browser.current_url == 'http://localhost:1667/#/'
        sleep(1)
        assert self.browser.find_elements(By.CLASS_NAME, 'cookie__bar__buttons__button--decline') == []
        sleep(2)

    def test_registry(self):
        # Regisztrációs felület használata
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
        email.send_keys(f"teszt@{self.unique}.hu")
        password.send_keys('Abcd1234')
        sign_up_btn.click()'''

        username.send_keys("TesztUser")
        email.send_keys("teszt@vizsga.hu")
        password.send_keys('Abcd1234')
        sign_up_btn.click()

        ok_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'swal-button--confirm')))
        assert self.browser.find_element(By.CLASS_NAME, 'swal-title').text == "Welcome!"
        ok_btn.click()

    def test_login(self):
        # TC3 A bejelentkezési felület használata, korábban regisztrált felhasználóval
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
        sleep(1)
        assert self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/@TesztUser/"]').text == "TesztUser"

    def test_new_post(self):
        # TC4 Új adat bevitele -Új poszt készítése-
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
        assert published == f'article{self.unique}'
        sleep(2)
        home = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/"]')
        home.click()
        sleep(1)
        tag_published = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href="#/tag/tag{self.unique}"]')))
        assert tag_published.is_displayed()

    def test_edit_post(self):
        # TC5 Meglévő adat módosítása -Korábbi poszt módosítása-
        self.test_login()
        user = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul li a[href="#/@TesztUser/"')))
        user.click()
        sleep(2)
        post = self.browser.find_element(By.CSS_SELECTOR, f'a[href="#/articles/article{self.unique}"]')
        post.click()
        edit_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ion-edit')))
        edit_article.click()

        article_title = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'form-control-lg')))
        about = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')
        write = self.browser.find_element(By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')
        tag = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')
        publish = self.browser.find_element(By.CLASS_NAME, 'btn-primary')
        for i in [article_title, about, write]:
            while i.get_attribute("value") != "":
                i.send_keys(Keys.BACKSPACE)
        article_title.send_keys("article edit")
        about.send_keys("about edit")
        write.send_keys("write edit")
        tag.send_keys("tag edit")
        sleep(2)
        assert article_title.get_attribute("value") == "article edit"

        publish.click()
        published = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))).text
        assert published == "article edit"
        sleep(2)
        home = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/"]')
        home.click()
        sleep(1)

    def test_delete_post(self):
        # TC6 Meglévő adat törlése -Korábbi poszt törlése-
        self.test_login()
        user = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul li a[href="#/@TesztUser/"')))
        user.click()
        sleep(2)
        post = self.browser.find_element(By.CSS_SELECTOR, f'a[href="#/articles/article{self.unique}"]')
        post.click()
        delete_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ion-trash-a')))
        delete_article.click()
        sleep(2)
        assert self.browser.find_elements(By.CSS_SELECTOR, f'a[href="#/tag/tag edit"]') == []

    def test_data_source(self):
        # TC7 Ismételt és sorozatos adatbevitel adatforrásból -Új posztok létrehozása-
        self.test_login()

        with open('/vizsgaremek/test/forras.csv', 'r', encoding='utf-8') as forras:
            forras_reader = csv.reader(forras, delimiter=',')

            for forras in forras_reader:
                new_article = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/editor"]')
                new_article.click()
                article_title = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'form-control-lg')))
                about = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')
                write = self.browser.find_element(By.CSS_SELECTOR,
                                                  'textarea[placeholder="Write your article (in markdown)"]')
                tag = self.browser.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')
                publish = self.browser.find_element(By.CLASS_NAME, 'btn-primary')
                new_article.click()
                sleep(1)
                article_title.send_keys(forras[0])
                about.send_keys(forras[1])
                write.send_keys(forras[2])
                tag.send_keys(forras[3])
                sleep(1)
                publish.click()
                sleep(2)
                published = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))).text
                assert published == forras[0]
                home = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/"]')
                home.click()
                sleep(1)
                article_published = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, f'a[href="#/articles/{"-".join(forras[0].split())}"]')))
                assert article_published.is_displayed()

    def test_pages_list(self):
        # TC8 Több oldalas lista bejárása -Létrehozott oldalak végigjárása-
        self.test_login()
        pages = self.browser.find_elements(By.CSS_SELECTOR, 'ul.pagination li a')
        for num, i in enumerate(pages):
            i.click()
            assert i.text == str(num + 1)
            sleep(2)
        assert str(len(pages)) == i.text

    def test_data_save_txt(self):
        # TC9 Adatok lementése felületről -TestUser által létrehozott címek txt-be mentve-
        self.test_login()
        user = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul li a[href="#/@TesztUser/"')))
        user.click()
        sleep(2)
        posztok = self.browser.find_elements(By.CSS_SELECTOR, 'a p')
        posztok = [i.text for i in posztok]

        with open('kerdesek.txt', 'w', encoding='UTF-8') as poszt_file:
            for i in posztok:
                poszt_file.write(i + '\n')

        with open('kerdesek.txt', 'r', encoding='UTF-8') as poszt_read:
            assert len(list(poszt_read)) == len(posztok)

    def test_data_list(self):
        # TC10 Adatok listázása -TestUser posztjaira szűrve nem jelenik meg másik felhasználó cikke-
        self.test_login()
        user = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul li a[href="#/@TesztUser/"')))
        user.click()
        sleep(2)
        writer = self.browser.find_elements(By.CSS_SELECTOR, 'div.info a[aria-current="page"]')
        writer = [i.text for i in writer]

        for i in writer:
            assert i == "TesztUser"

    def test_log_out(self):
        # TC11 Kijelentkezés -TestUser kilép-
        self.test_login()
        sleep(1)
        log_out = self.browser.find_element(By.CSS_SELECTOR, 'i.ion-android-exit')
        log_out.click()
        sleep(1)
        sign_in = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/login"]')
        assert sign_in.is_displayed()
