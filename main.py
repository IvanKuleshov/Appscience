# -*- coding: utf-8 -*-
# python 3.7.9
# pip install beautifulsoup4
# pip install lxml

import pandas as pd
from tqdm import tqdm
from set_country import AgilentBrowser  # класс для установки страны и языка просмотра сайта ,с помощью Selenium
from sitemap import GetProductLinks  # класс, возвращающий генератор ссылок на продукты
from parcing import parcing_products_data
from multiprocessing.pool import ThreadPool
from typing import List

# Путь к драйверу Firefox
PATH_DRIVER = 'D:/python_work/chromedriver/geckodriver.exe'
# Константы для страны и языка, под которыми запускается парсинг
COUNTRY = 'United States'
LANGUAGE = 'English'


def get_parcing_data_by_pool(list_url: List[str]):
    global data  # данные о парсинге со всех браузеров

    browser = AgilentBrowser(path_driver=PATH_DRIVER)
    if browser.set_country(country=COUNTRY, language=LANGUAGE):
        for url in tqdm(list_url):
            parcing_products_data(browser=browser, link=url)

    data += browser.data
    browser.close()
    pass


data = []

# Получаем ссылки на продукты
links = GetProductLinks()

# Запускаем парсинг в несколько потоков
pool = ThreadPool(processes=5)

try:
    pool.map(get_parcing_data_by_pool, [links.map[:200],
                                        links.map[200:400],
                                        links.map[400:600],
                                        links.map[600:800],
                                        links.map[800:1000]
                                        ])
finally:
    pool.close()

    # Результат
    pd.DataFrame(data).to_csv('Appscience_parcing.csv', index=False)
