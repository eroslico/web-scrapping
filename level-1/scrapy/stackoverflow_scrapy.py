from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


# 1. Defino la abstaccion
class Pregunta(Item):
    # 2. Definicion de cada cosa que voy a extraer
    id = Field()
    pregunta = Field()
    # descripcion = Field()


# 3. Defino la clase CORE de Scrapy. Que va a hacer los request y parseos
# Hereda solo de Spider porque es unicamente una pagina
class StackOverflowSpider(Spider):
    name = 'SpiderWithFlow'

    # 4. Ahora defino el user_agent
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    # 5. Defino la URL semilla
    start_urls = ['https://stackoverflow.com/questions']

    # 6. Defino la funcion donde sucede el parseo
    def parse(self, response):
        # 7. Defino Selector para hacer consultar a la pagina
        sel = Selector(response)
        # 8. Defino preguntas con ruta XPATH para encontrar lo que quiero
        preguntas = sel.xpath(
            '//div[@id="questions"]//div[@class="s-post-summary--content"]')

        for pregunta in preguntas:  # La variable PREGUNTA tiene todos los titulos
            # 9. Defino ITEMLOADER para cargar la info dentro de scrapy
            item = ItemLoader(Pregunta(), pregunta)
            # 10. Llenar item. Pregunta se va a llenar con lo que este a continuacion
            item.add_xpath('pregunta', './/h3/a/text()')
            # item.add_xpath(
            #    'descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value('id', 1)

            # 11. Hago un return que devuelve la info a un archivo
            yield item.load_item()
