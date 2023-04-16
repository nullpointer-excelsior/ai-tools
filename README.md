# AI Tools 

Aplicaciones de utilidad basados en Chatgpt y otras herramientas


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

## Ejecutar 

```bash
#!/bin/bash

## summarize texts
# with pipes
pbpaste | python src/main.py summarize | jq
# with args
python src/main.py summarize "My text to summarize"

```
