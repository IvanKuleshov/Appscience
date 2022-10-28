from time import sleep
import selenium.common.exceptions as sl_exception
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service

USERAGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"


class AgilentBrowser:
    """
    Класс, реализующий навигацию по сайту www.agilent.com с помощью браузера Silenium
    """
    def __init__(self, path_driver):
        options = webdriver.FirefoxOptions()
        options.set_preference("general.useragent.override", USERAGENT)
        options.set_preference("dom.webdriver.enabled", False)
        options.headless = True
        self.driver = webdriver.Firefox(service=Service(path_driver), options=options)
        self.driver.set_window_size(300, 500)

        # list для хранения результатов парсинга
        self.data = []

    # Выбор указанной страны-языка
    def set_country(self, country: str = 'United States', language: str = 'English') -> bool:
        try:
            #  список стран и языков
            self.driver.get('https://www.agilent.com/home/more-countries')
            sleep(2)

            #  щелкаем на страну, чтобы появились языки
            country_mask = f"//li/a[text()='{country}']"
            elem = self.driver.find_element('xpath', country_mask)
            elem.click()
            sleep(2)

            #  выбираем язык
            elem = self.driver.find_element('xpath', country_mask + f"/following::a[text()='{language}']")
            elem.click()
            sleep(2)
        except self.driver.error_handler:
            return False

        return True

    def save_to_file(self, filename: str):
        with open(filename, 'wb') as file:
            file.write(self.driver.page_source.encode('utf-8'))
        pass

    def wait_to_be_clicable(self, by: str, elem: str):
        WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((by, elem))).click()
        pass

    def delete_element(self, by: str, elem: str):
        try:
            elem_remove = self.driver.find_element(by, elem)
            self.driver.execute_script("arguments[0].remove();", elem_remove)
        except sl_exception.NoSuchElementException:
            pass

        pass

    def close(self):
        self.driver.close()
        self.driver.quit()
