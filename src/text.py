import click, pyperclip
from pwn import log
from libs.openai_api import get_completion_stream
from libs.utils import print_stream
import sys, select

class InvalidOption(Exception):
    pass

def get_prompt(text, translate, grammar):
    if translate:
        return f"""
            Traduce el siguiente texto encerrado entre triple acento grave.
            - Si el texto esta en ingles traducelo al español
            - Si el texto esta en español traducelo al ingles
            ```{text}```.
        """
    if grammar:
        return f"""
        Corrije gramaticalmente el siguiente texto encerrado en triple acento grave. ```{text}```
        """
    raise InvalidOption('No arguments given')

def copy_response(text, progress):
    pyperclip.copy(text)
    progress.success('Texto copiado al portapapeles.')

@click.command()
@click.argument('text', default=None, required=False)
@click.option('--translate', '-t', is_flag=True,  help='Traduce el texto aingles o español')
@click.option('--grammar', '-g', is_flag=True,  help='Corrije el texto gramaticalmente')
def process_text(text, translate, grammar):
    """
    Operaciones básicas con textos con ChatGPT
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
    prompt = get_prompt(text, translate, grammar)
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
    process_text()
