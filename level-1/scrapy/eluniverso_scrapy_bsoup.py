from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup


class Noticia(Item):
    id = Field()
    titular = Field()
    descripcion = Field()


class ElUniversoSpider(Spider):
    name = "MiSegundoSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    start_urls = ["https://www.eluniverso.com/deportes/"]

    """Using Beautiful Soup"""

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        contenedor_noticias = soup.find_all(class_="feed | divide-y relative")
        id = 0
        for contenedor in contenedor_noticias:
            noticias = contenedor.find_all(class_='relative', recursive=False)
            for noticia in noticias:
                item = ItemLoader(Noticia(), response.body)
                titular = noticia.find('h2').text.replace(
                    '\n', '').replace('\r', '')
                descripcion = noticia.find('p')
                if (descripcion):
                    item.add_value('descripcion', descripcion.text.replace(
                        '\n', '').replace('\r', ''))
                else:
                    item.add_value('descripcion', 'N/A')
                item.add_value('titular', titular)
                item.add_value('id', id)
                id += 1
                yield item.load_item()

process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'resultados.csv'
})
