from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


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

    """Using Scrapy"""
    def parse(self, response):
        sel = Selector(response)
        noticias = sel.xpath('//div[contains(@class, "content-feed")]/ul/li')
        # PARA INVESTIGAR: Para que sirve enumerate?
        for i, elem in enumerate(noticias):
            item = ItemLoader(Noticia(), elem)  # Cargo mi item

            # Llenando mi item a traves de expresiones XPATH
            item.add_xpath('titular', './/h2/a/text()')
            item.add_xpath('descripcion', './/p/text()')
            item.add_value('id', i)
            yield item.load_item()  # Retorno mi item lleno


process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'resultados.csv'
})
