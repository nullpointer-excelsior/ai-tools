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

### Ejemplo
```bash
#!/bin/bash

# define your openai apikey
export OPENAI_API_KEY=""

# run your summary
python src/simple_assistant.py 

```