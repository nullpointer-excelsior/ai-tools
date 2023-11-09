import re
from datetime import datetime
from pwn import log
from libs.openai_api import ChatGPTModel, get_completion
from libs.utils import read_argument, read_file, read_stdin, truncate_text

CORRECT_TEXT_PROMPT = """
Corrige gramaticalmente el siguiente artículo encerrado en triple acento grave, el cual está en formato markdown. Ignora los bloques de código, pero deben estar incluidos en el artículo final.
```{content}```
"""

CATEGORIES_PROMPT = """
De la siguiente lista de titulos encerradas en triple acento grave, elige de la siguiente lista:

AI
Angular
Arquitectura
Arquitectura Software
CTF
ChatGPT
Cyberseguridad
DDD
Domain Driven Design
ETL
Events architecture
Frontend
GraphQL
Java
Javascript
Microservicios
NestJs
Patrones
Programacion
Python
React
Reactive
Rxjs
Serverless
Spring
Springboot
Typescript
Backend
Fullstack
Hackcode
ORM
Software
Software Engineer

las categorias mas adecuadas para un articulo de blog de ingeniera de software separados por coma y capitalizadas. 
response de forma directa, sin explicaciones y en el siguiente formato: ```category1,categor2,...categoryN```.
```{titles}```
"""

MARKDOWN_PAGE_TEMPLATE = """---
title: {title}
author: Benjamin
date: {date} -0500
categories: {categories}
tags: {tags}
---

{content}

"""


def read_content():
    filename_input = read_argument()
    if filename_input is None:
        return read_stdin()
    return read_file(filename_input)


def correct_grammar_by_ai(content):
    prompt = CORRECT_TEXT_PROMPT.format(content=content)
    return get_completion(prompt=prompt,model=ChatGPTModel.GPT_3_5_TURBO_16K)
    

def find_first_title(text):
    pattern = r'^\s*#.*'  # Expresión regular que busca líneas que comiencen con '#'
    match = re.search(pattern, text, re.MULTILINE)
    if match:
        return match.group().replace('#', '').strip()
    return None


def find_all_titles(markdown_text):
    header_pattern = r'^(#+)\s+(.*?)\n'  # Patrón para encontrar títulos (##, ###, etc.)
    headers = re.findall(header_pattern, markdown_text, re.MULTILINE)
    headers = [header[1] for header in headers]
    return headers


def create_categories_by_ai(titles):
    prompt = CATEGORIES_PROMPT.format(titles=titles)
    return get_completion(prompt=prompt)


def generate_post_file(title: str):
    sanitized_title = title.lower().replace(' ', '-').replace(':', '')
    return f"{datetime.now().strftime('%Y-%m-%d')}-{sanitized_title}.md"


def create_post(title, categories, content: str):
    lines = content.split('\n')
    for index, line in enumerate(lines):
        if line.strip().startswith("# "):
            lines.pop(index)
            break
    content_text = '\n'.join(lines)
    categories_text = str(categories).replace("'", "")
    tags = categories_text.lower()
    title_text = title.replace(':', '')
    date = datetime.now().strftime('%Y-%m-%d 00:00:00')
    template = MARKDOWN_PAGE_TEMPLATE.format(
        content=content_text, 
        categories=categories_text, 
        tags=tags, 
        title=title_text,
        date=date
    )
    filename = generate_post_file(title)
    with open(filename, "w") as file:
        file.write(template)


bar = log.progress("Creating post")
bar.status("Reading content")

content = read_content()

log.info(f"Improving the following text: \"{truncate_text(content, 100)}\"")
bar.status("Thinking")

response = correct_grammar_by_ai(content)

log.info(f"tokens usado: {response['total_token']}")

post = dict()
post["content"] = response['answer']
post['title'] = find_first_title(post['content'])
post['headers'] = find_all_titles(content)
post['categories'] = create_categories_by_ai(post['headers'])['answer']

create_post(
    title=post['title'], 
    categories=post['categories'], 
    content=post['content']
)

bar.success("Task terminated successfuly")

