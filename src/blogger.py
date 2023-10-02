
from datetime import datetime
import sys

def read_post_content():
    
    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_al_archivo>")
        return
    
    filename = sys.argv[1]
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        return "El archivo no existe."
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"
    
    return {
        'title': content[0].replace("#", ""),
        'content': content
    }




def generate_filename(title: str, path: str = None):
    path_file=f"{path + '/' if path is not None else ''}"
    return f"{path_file}{datetime.now().strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"


def create_post_file(title, categories, content: str, path=None):
    categories_text = str(categories).replace("'", "")
    tags = categories_text.lower()

    template=f"""
---
title: {title}
author: Benjamin
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -0500
categories: {categories_text}
tags: {tags}
---

{content}

    """
    filename = generate_filename(title, path)
    with open(filename, "w") as file:
        file.write(template)



post = read_post_content()
title=post['title'] #"Como integrar Rxjs en React para aplicaciones asincronas complejas"
categories=["Frontend", "React", "Rxjs", "Arquitectura Frontend", "Javascript", "Typescript"]
create_post_file(title=title, categories=categories, content=post['content'],)



hashtags="#developer #fullstackdeveloper #fullstack #typescript #javascript #code #microservicios #backend #programacion #programadores #programación #programador #developments #devs #codigo"