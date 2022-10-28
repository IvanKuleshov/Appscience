from bs4 import BeautifulSoup
from set_country import AgilentBrowser
from time import sleep


def verify_elem(obj, pattern: str = '-') -> str:
    return obj.text.strip() if obj is not None else pattern


def parcing_products_data(browser: AgilentBrowser, link: str):
    """
    Функция, реализующая всю логику парсинга продуктов со страниц. Парсинг происходит через браузер Silenium,
    поскольку сайт отдаёт информацию о ценах только для определённых стран-языков.

    Результат парсинга записывается в параметр data объекта browser.

    :browser: объект типа AgilentBrowser - браузер Selenium
    :link: ссылка на категорию с продуктами, берётся из sitemap.xml
    """
    parts = []
    # страница, содержащая список продуктов
    browser.driver.get(link)
    soup = BeautifulSoup(browser.driver.page_source, 'lxml')
    # категория
    category = verify_elem(soup.find(class_='meta-value pageSubTitle'))
    category_name = verify_elem(soup.find(class_='media-heading pageTitle reg-heading'))

    # Цикл парсинга продуктов
    # проходим все страницы и собираем ссылки на продукты
    part_number = []  # список всех номер продуктов во всех страницах
    desc = []  # описание если есть
    price = []  # стоимость в единицах, выбранной страны и языка

    while True:
        # Строка, которая пойдёт в *.csv
        row_ = {'CategoryLink': link,
                'Category': category,
                'CategoryName': category_name
                }
        # проверяем, есть ли следующая страница
        forward = soup.find(class_='page-forward disabled') is None

        # Part Number
        part_number += soup.findAll(class_='btn btn-link plusIcon browsePartPlus')

        # Description
        desc += soup.findAll(class_='sorting_1')
        # Price
        price += soup.findAll(class_='myprice')

        # условие выхода: если нет управляющего элемента "следующая страница", то выход
        if soup.find(class_='page-forward') is None:
            break
        # условие выхода: если мы не на последней странице - кликаем следующую страницу, иначе - выходим
        if forward:
            # удаляем мешающие на некоторых страницах нажатию элементы
            browser.delete_element('class name', "transparent-button")
            browser.delete_element('class name', "designstudio-animated")
            browser.delete_element('class name', "loading")

            try:
                browser.wait_to_be_clicable('xpath', "//li[@class='page-forward']/a")
                sleep(3)
            except Exception as er:
                break

            soup = BeautifulSoup(browser.driver.page_source, 'lxml')
        else:
            break

    # Перебираем все Part Number и собираем характеристики
    for i, _ in enumerate(part_number):
        row = row_.copy()
        row['Part Number'] = verify_elem(part_number[i])
        row['Description'] = verify_elem(desc[i])

        # Price
        try:
            row['Price'] = price[i].text.split(' ')[0]
            row['CurrencySymbol'] = price[i].text.split(' ')[1]
        except IndexError:
            row['CurrencySymbol'] = '-'

        # UnitKey
        unitkey = verify_elem(soup.find(class_='unitKey'))
        row['UnitKey'] = unitkey

        # Заходим на страничку i-го продукта
        browser.driver.get(f"https://www.agilent.com/store/productDetail.jsp?catalogId={row['Part Number']}")
        soup = BeautifulSoup(browser.driver.page_source, 'lxml')

        # browser.save_to_file(f"html/{row['Part Number']}.html")

        row['In stock'] = verify_elem(soup.find(class_='custom-instock'))  # Доступность

        # Т.к. каждый товар содержит свой набор характеристик, а по условию задания вернуть надо *.csv, а не json
        # то все характеристики собираю в одну строку через разделитель "|"
        table = soup.find('table', class_='specsNewTable')
        if table is not None:
            # Названия и значения характеристик
            specs_keys = [k.find('td') for k in table.findAll('tr')]
            specs_values = table.findAll('ul', class_='sameattr')

            row['Specifications'] = '|'.join([k.text.strip() + ':' + v.text.strip()
                                              for k, v in zip(specs_keys, specs_values)]
                                             )
        row['link'] = f"https://www.agilent.com/store/productDetail.jsp?catalogId={row['Part Number']}"
        parts.append(row)

    # Если для категории нет ни одного товара с тегом part_number - внести в *.csv об этом запись
    if not parts:
        row_['Part Number'] = 'no part numbers'
        parts.append(row_)

    browser.data += parts
    pass
