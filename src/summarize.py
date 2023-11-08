import click, pyperclip
from pwn import log
from libs.cli import model_option
from libs.colored import cyan_color
from libs.openai_api import get_completion_stream, get_model
from libs.utils import print_stream
from colorama import Fore, Style
import sys, select


def get_instructions(words, sentences, tone, audience, style, markdown, translate):
    instructions = []
    if words:
        instructions.append(f' - El resumen no debe tener más de {words} palabras.')
    elif sentences:
        instructions.append(f' - El resumen no debe tener más de {sentences} oraciones.')
    if style:
        instructions.append(f' - El resumen debe tener un estilo {style}.')
    if audience:
        instructions.append(f' - El resumen debe apuntar a una audiencia {audience}.')
    if tone:
        instructions.append(f' - El resumen debe tener un tono {tone}.')
    if markdown:
        instructions.append(' - El resumen debe estar formato markdown.')
    if translate:
        instructions.append(' - El resumen debe ser traducido al español si es necesario.')
    return instructions


def get_prompt(text, instructions):
    if len(instructions) > 0:
        instructions_list = '\n'.join(instructions)
        instructions_text = f'El resumen debe seguir las siguientes instrucciones:\n{instructions_list}'
    else:
        instructions_text = ''
    return f"""Tu tarea sera resumir el texto encerrado en triple acento grave.\n{instructions_text}\n```{text}```."""


def get_summary_verbose(prompt):
    print()
    text_parts = prompt.split('```')
    initial_prompt = text_parts[0] 
    text_2_summarize = text_parts[1]
    text = f"{text_2_summarize[:300]}{'...' if len(text_2_summarize) > 300 else ''}"
    instructions = '\n'.join([l for l in initial_prompt.split('\n') if l.strip().startswith('-')])
    log.info('Summarize text with ChatGPT')
    print(f'\nTexto:\n\n{Fore.CYAN}{text}{Style.RESET_ALL}\n\n')
    if instructions != '':
        print(f"Instrucciones:\n\n{cyan_color(instructions)}\n\n")
    p1 = log.progress('Resumen')
    p1.status(f'{Fore.GREEN}Conectando con ChatGPT...{Style.RESET_ALL}')
    answer = ''
    try:
        print()
        streaming = False
        for stream in get_completion_stream(prompt=prompt):
            if not streaming:
                p1.status(f'{Fore.GREEN}ChatGPT Escribiendo...{Style.RESET_ALL}')
                streaming = True
            print_stream(f'{Fore.YELLOW}{stream}')
            answer += stream  
        print('\n')
        p1.success(f'{Fore.GREEN}Listo{Style.RESET_ALL}')
    except Exception as err:
        print(f"{Style.RESET_ALL}\n")
        p1.error(f'ChatGPT no pudo procesar el texto: {str(err)}')
    return answer


@click.command()
@click.argument('text', default=None, required=False)
@click.option('--words', '-w', type=int, help='Número de palabras aproximadas', default=None)
@click.option('--sentences', '-s', type=int, help='Número de oraciones aproximadas', default=None)
@click.option('--tone', '-t', type=str, help='Tono del resumen', default=None)
@click.option('--audience', '-a', type=str, help='Público objetivo del resumen', default=None)
@click.option('--style', '-st', type=str, help='Estilo del resumen', default=None)
@click.option('--markdown', '-md', type=str, is_flag=True, help='Formato de salida mardown')
@click.option('--verbose','-v', is_flag=True, help='Muestra el resumen detallado')
@click.option('--no-clipboard', '-nc', is_flag=True, help='No copia al clipboard')
@click.option('--translate', '-tr', is_flag=True, help='Traduce si es necesario')
@model_option
def text_processor(text, words, sentences, tone, audience, style, markdown, verbose, no_clipboard, translate, model):
    """
    Resume un texto con ChatGPT y diversas opciones.
    """
    if not text:
        if select.select([sys.stdin,],[],[],0.0)[0]:
            text = sys.stdin.read().strip()
        else:
            log.error('No se ha proporcionado ningún texto.')
            return
    
    instructions = get_instructions(words, sentences, tone, audience, style, markdown, translate)
    prompt = get_prompt(text, instructions)
    
    if verbose:
        summary = get_summary_verbose(prompt)
        if not no_clipboard:
            pyperclip.copy(summary)
            log.info('Resumen copiado al portapapeles!\n\n')
    else:
        stream = get_completion_stream(prompt=prompt,model=get_model(model))
        for s in stream:
            print_stream(s)
        print()
       

if __name__ == "__main__":
    text_processor()
