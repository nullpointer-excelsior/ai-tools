import click, pyperclip
from pwn import log
from libs.openai_api import get_completion_stream
from libs.utils import print_stream
import sys, select


def get_prompt(text):
    return f"""
        Actua como un experto profesor en ingles y corrige el siguiente texto encerrado en triple acento grave ```{text}```. este texto puede estar en ingles o español deberas corregir si existe algun error
        y tambien puedes dar sugeriencias para mejorarlo.
        Devolveras un resumen con los errores y sugerencias en formato markdown. finalmente devolveras el texto correjido en ingles encerrado en triple acento grave.
    """

def copy_response(text: str, progress):
    try:
        text_to_copy = text.split('```')[1]
        pyperclip.copy(text_to_copy)
        progress.success('Texto copiado al portapapeles.')
    except:
        progress.error('Texto no pudo ser copiado al portapapeles.')

@click.command()
@click.argument('text', default=None, required=False)
@click.option('--explain', '-e', type=str, help='Explica la corrección y da sugerencias', default=None)
def translate(text, explain):
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
    progress = log.progress('Openai ChatGPT')
    progress.status('Conectando...')
    print()
    prompt = get_prompt(text)
    complete_response = ''
    stream_initialized = False
    for stream in get_completion_stream(prompt):
        if not stream_initialized:
            progress.status('Escribiendo...')
            stream_initialized = True
        print_stream(stream)
        complete_response += stream
    copy_response(complete_response, progress)
    print('\n')
       

if __name__ == "__main__":
    translate()
