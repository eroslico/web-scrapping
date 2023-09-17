import requests
from lxml import html

encabezados = {
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
    # 'user-agent' es una cadena de texto con la cual se puede identificar el navegador y el S.O del cliente. Por DEFAULT viene ROBOT
}

url = 'https://www.wikipedia.org/'  # La url que quiero scrapear

# Estoy haciendo el request de la url
respuesta = requests.get(url, headers=encabezados)

# Los encabezados son grupos de variables para saber quien o como hace el requerimiento

parser = html.fromstring(respuesta.text)  # La transoformamos a un parseador


# EXTRAYENDO TODOS LOS IDOMAS CON XPATH
# idiomas = parser.xpath(
#    "//div[contains(@class, 'central-featured-lang')]//strong/text()")
# for idioma in idiomas:
#    print(idioma)

# EXTRAYENDO 1 SOLO LENGUAJE CON LXML
# ingles = parser.get_element_by_id('js-link-box-en')  # Obtengo elemento por ID
# print(ingles.text_content())  # Con text_content obtengo el texto

# EXTRAYENDO TODOS LOS IDIOMAS CON LXML
idiomas = parser.find_class('central-featured-lang')
for idioma in idiomas:
    print(idioma.text_content())
