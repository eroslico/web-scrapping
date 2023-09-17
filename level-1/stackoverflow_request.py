import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

url = 'https://stackoverflow.com/questions'

respuesta = requests.get(url, headers=headers)

# BS4 es otro parseador del arbol
# Concepto: Sopa de letras

# Por convencion se denomina siempre soup esta variable
soup = BeautifulSoup(respuesta.text)

# De todo el arbo, buscamos lo que tenga id questions
contenedor_preguntas = soup.find(id='questions')
lista_preguntas = contenedor_preguntas.find_all(
    'div', class_='s-post-summary--content')  # find_all encuentra todos. Encuentrame todos los div con clase

for pregunta in lista_preguntas:
    elemento_texto_pregunta = pregunta.find('h3')
    texto_pregunta = elemento_texto_pregunta.text

    elemento_texto_pregunta.find_next_sibling(
        'div').text  # encuentrame el siguiente primo

    descripcion_pregunta = pregunta.find(
        class_='s-post-summary--content-excerpt').text
    descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace(
        '\r', '').strip()  # \n, \r es un salto de linea, \t es una tabulacion # strip() elimina cualquier espacio al inicio o al final
    print(texto_pregunta)
    print(descripcion_pregunta)


# BS4 es mejor porque me puedo mover por etiquetas. ej de un h3 paso a al primo siguiente
