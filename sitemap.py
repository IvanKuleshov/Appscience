import requests
from bs4 import BeautifulSoup

COMMON_SITEMAP = 'https://www.agilent.com/sitemap.xml'
PRODUCT_MASK = "products"


def get_html_text(page: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"}

        r = requests.get(page, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return r.text


def get_xml_links_from_tag(xml_source: str, tag: str) -> list:
    try:
        soup = BeautifulSoup(get_html_text(xml_source), 'xml')
        links = soup.findAll(tag)
    except:
        return []
    return links


class GetProductLinks:
    """
    Собирает и возвращает в виде параметра map список всех ссылок, содержащихся в sitemap.xml
    """
    def __init__(self):
        self.map = self.get_links()

    @staticmethod
    def get_links():
        #  Общий sitemap
        links = get_xml_links_from_tag(COMMON_SITEMAP, 'loc')

        #  Собираем дочерние sitemap, если удовлетворяет маске
        products_xml = [link.text
                        for link in links
                        if PRODUCT_MASK in link.text]

        #  Для каждого дочернего sitemap собираем ссылки на страницу, содержащей сведения о продукте
        products_link = []
        for product_xml in products_xml:
            links = get_xml_links_from_tag(product_xml, 'loc')
            products_link += [link.text for link in links]

        return products_link

    # def get_links_gen(self):
    #    for link in self.map:
    #        yield link
