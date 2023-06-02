import click, pyperclip
from pwn import log
from libs.openai_api import get_completion
import sys, select


def get_prompt(text):
    return f"""
        Actua como un experto profesor en ingles y corrige el siguiente texto encerrado en triple acento grave ```{text}```. este texto puede estar en ingles o español deberas corregir si existe algun error
        y tambien puedes dar sugeriencias para mejorarlo.
        Devolveras un resumen con los errores y sugerencias en formato markdown. finalmente devolveras el texto correjido en ingles encerrado en triple acento grave.
    """

def copy_response(text: str):
    try:
        text_to_copy = text.split('```')[1]
        pyperclip.copy(text_to_copy)
        log.info('Texto copiado al portapapeles.')
    except:
        log.error('Texto no pudo ser copiado al portapapeles.')

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
    log.info('Pensando...')
    prompt = get_prompt(text)
    answer = get_completion(prompt=prompt)['answer']
    copy_response(answer)
    print(f"\n{answer}\n")
       

if __name__ == "__main__":
    translate()
