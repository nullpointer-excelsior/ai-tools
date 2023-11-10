import click, pyperclip
from pwn import log
from libs.cli import model_option
from libs.colored import cyan_color
from libs.openai_api import get_completion_stream, get_model
from libs.utils import print_stream
import sys, select


def get_assistant_prompt(text):
    return f"""
        Actua como un experto profesor en ingles y corrige el siguiente texto encerrado en triple acento grave ```{text}```. este texto puede estar en ingles o español deberas corregir si existe algun error
        y tambien puedes dar sugeriencias para mejorarlo.
        Devolveras un resumen con los errores y sugerencias en formato markdown. finalmente devolveras el texto correjido en ingles encerrado en triple acento grave.
    """

def get_translate_prompt(text):
    return f"""
        Traduce el siguiente texto al inglés ```{text}``` y dame la respuesta en triple acento grave.
    """

def copy_response(text: str, progress):
    try:
        text_to_copy = text.split('```')[1]
        pyperclip.copy(text_to_copy)
        progress.success('Texto copiado al portapapeles.')
    except:
        print('\nTexto no pudo ser copiado al portapapeles.')

@click.command()
@click.argument('text', default=None, required=False)
@click.option('--translate', '-t', is_flag=True, help='Traduce al ingles el texto', default=False)
@model_option()
def translate(text, translate, model):
    """
    Resume un texto con ChatGPT y diversas opciones.
    """
    if not text:
        if select.select([sys.stdin,],[],[],0.0)[0]:
            text = sys.stdin.read().strip()
        else:
            log.error('No se ha proporcionado ningún texto.')
            return
    print()
    progress = log.progress(f'OpenAI {cyan_color(model)}')
    progress.status('Conectando...')
    print()
    prompt = get_assistant_prompt(text) if not translate else get_translate_prompt(text)
    complete_response = ''
    stream_initialized = False
    for stream in get_completion_stream(prompt=prompt, model=get_model(model)):
        if not stream_initialized:
            progress.status('Escribiendo...')
            stream_initialized = True
        print_stream(stream)
        complete_response += stream
    copy_response(complete_response, progress)
    print('\n')
       

if __name__ == "__main__":
    translate()
