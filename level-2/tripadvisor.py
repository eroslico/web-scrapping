from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()


# Cuando queremos hacer HORIZONTAL y VERTICAL se hereda CRAWLSPIDER
class TripAdvisor(CrawlSpider):
    name = "Hoteles"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    # Semilla
    start_urls = [
        'https://www.tripadvisor.com.ar/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    # Delay para que no me baneen
    download_delay = 2

    # Solo se van a extraer links que tengan esa regla
    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ), follow=True, callback="parse_hotel"
        ),
    )

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', '//div[@class="JPNOn"]/text()')
        item.add_xpath(
            'descripcion', '//div[contains(@class, "_T FKffI IGtbc Ci oYqEM")]/div/p/text()')
        item.add_xpath(
            'amenities', '//div[contains(@class, "yplav f ME H3 _c")]/text()')

        yield item.load_item()
