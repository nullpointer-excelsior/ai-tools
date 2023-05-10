import click, pyperclip
from pwn import log
from libs.openai_api import get_completion
from colorama import Fore, Style
import sys, select


def get_instructions(words, sentences, tone, audience, style, markdown):
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
    return instructions


def get_prompt(text, instructions):
    if len(instructions) > 0:
        instructions_list = '\n'.join(instructions)
        instructions_text = f'El resumen debe seguir las siguientes instrucciones:\n{instructions_list}'
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
    print(f"Instrucciones:\n\n{Fore.CYAN}{instructions}{Style.RESET_ALL}\n\n")
    p1 = log.progress('Creando resumen')
    p1.status(f'{Fore.GREEN}ChatGPT esta pensando...{Style.RESET_ALL}')
    try:
        response = get_completion(prompt=prompt)
        p1.success(f'{Fore.GREEN}Listo{Style.RESET_ALL}')
    except Exception as err:
        p1.error(f'ChatGPT no pudo procesar el texto: {str(err)}')
    answer = response['answer']
    print(f"\nResumen:\n\n{Fore.YELLOW}{answer}{Style.RESET_ALL}\n")
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
def text_processor(text, words, sentences, tone, audience, style, markdown, verbose, no_clipboard):
    """
    Resume un texto con ChatGPT y diversas opciones.
    """
    if not text:
        if select.select([sys.stdin,],[],[],0.0)[0]:
            text = sys.stdin.read().strip()
        else:
            log.error('No se ha proporcionado ningún texto.')
            return
    
    instructions = get_instructions(words, sentences, tone, audience, style, markdown)
    prompt = get_prompt(text, instructions)
    
    if verbose:
        summary = get_summary_verbose(prompt)
        pyperclip.copy(summary)
        log.info('Resumen copiado al portapapeles!\n\n')
    else:
        response = get_completion(prompt=prompt)
        print(response['answer'])
       

if __name__ == "__main__":
    text_processor()
