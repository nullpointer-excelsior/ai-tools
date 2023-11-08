# AI Tools 

Aplicaciones de utilidad basados en Chatgpt y otras herramientas

### Requisitos

Python 3.10 o superior
Paquete Click
Paquete OpenAI

## Instalacion

```bash
#!/bin/bash

# create virtual env
virtualenv -p python3.10 venv
# activate env
source venv/bin/activate
# install dependencies
pip install -r requirements.txt
```

## Asistentes disponibles:

* waitress: recomendar cervezas desde una API
* summarize: resume textos y los traduce siu es necesario
* simple_assistant: ChatGPT por CLI

## `summarize:`

Este script de Python permite resumir un texto utilizando ChatGPT y varias opciones.

## Uso
`summarize` admite los siguientes argumentos y opciones:

### Argumentos
* `text`: El texto que se desea resumir.

### Opciones

* `--words`, `-w`: El número aproximado de palabras que se desea que tenga el resumen.
* `--sentences`, `-s`: El número aproximado de oraciones que se desea que tenga el resumen.
* `--tone`, `-t`: El tono que se desea que tenga el resumen.
* `--audience`, `-a`: El público objetivo para el que se está escribiendo el resumen.
* `--style`, `-s`t: El estilo que se desea que tenga el resumen.
* `--markdown`, `-md`: Si se desea que el formato de salida sea en Markdown.
* `--verbose`, `-v`: Si se desea que el resumen detallado sea mostrado.
* `--no-clipboard`, `-nc`: Si se desea que el resumen no se copie al portapapeles.
* `--model`, `-m`: Escoje el modelo GPT a usar las opciones son: `gpt3`, `gpt3-16k`, `gpt4` y `gpt4-32k`

### Ejemplo
```bash
#!/bin/bash

# define your openai apikey
export OPENAI_API_KEY=""

# run your summary
python src/summarize.py "Este es un ejemplo de texto que se desea resumir" -w 10 -s 2 -t neutral -a estudiantes -st informativo -md

```

## `simple_assistant:`

Simple asitente sin ningun prompt especial, util para usar chatGPT en la terminal

### Opciones

* `--model`, `-m`: Escoje el modelo GPT a usar las opciones son: `gpt3`, `gpt3-16k`, `gpt4` y `gpt4-32k`

### Ejemplo
```bash
#!/bin/bash

# define your openai apikey
export OPENAI_API_KEY=""

# run your summary
python src/simple_assistant.py 

```

## `Blogger de tecnología AI`

Crea un articulo de internet para la herramienta de sitios estaticos `Jekill`. solo debemos proporcionar la ruta de un archivo .md con el contenido del articulo

### Uso

```bash
python src/blogger.py $PATH_TO_MD_FILE
```

Esto creara un archivo .md con correcciones gramaticales y metadata para `Jekill`.

## `Corrector de inglés AI`

Corrije y entrega los errores gramaticales de un texto en ingles. el texto correjido lo copiara al portapapeles

### Opciones

* `--model`, `-m`: Escoje el modelo GPT a usar las opciones son: `gpt3`, `gpt3-16k`, `gpt4` y `gpt4-32k`
* `--traslate`, `-t`: Traduce al inglés el texto

### Uso

```bash
#!/bin/bash

# no options 
python src/english.py "My text to correct"
# with specific model
python src/english.py -m gpt4 "My text to correct"
# Translate the given text. The assistant will resolve the language.
python src/english.py -t "My text to correct"

```

## TODO
- [x] Add english and blogger ai documentation
- [x] Change model option in cli options
- [x] blogger assistant 
- [ ] refactorize chatgpt call functions and chatgpt without call functions
- [x] command_line_assistant function with stream feature 
- [ ] add token usage feature to strem mode



### Autor: **Benjamín**