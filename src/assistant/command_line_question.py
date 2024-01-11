import click
import os
import pyperclip
from libs.cli import model_option
from libs.openai_api import ask_to_chatgpt_stream, get_model
from libs.utils import print_stream, read_stdin


def read_file_or_get_content(value):
    if os.path.exists(value):
        with open(value, 'r') as file:
            return file.read()
    return value


def ask_to_chatgpt(model='gpt3', prompt="Eres un util asistente. Responderas de forma directa y sin explicaciones", help="Pregunta rápida y configurable a ChatGPT"):
    @click.command(help=help)
    @click.argument('argument', default=None, required=False)
    @model_option(model)
    @click.option('--temperature', '-t', type=float, help='Temperatura del modelo. Entre 0 y 2. Los valores más altos como 0.8 harán que la salida sea más aleatoria, mientras que los valores más bajos como 0.2 la harán más enfocada y determinista.', default=0)
    def cli(argument, model, temperature):
        content = argument if argument is not None else read_stdin()
        content = read_file_or_get_content(content)
        complete_response = ''
        messages = [
            {"role": "assistant", "content": prompt},
            {"role": "user", "content": content}
        ]
        for stream in ask_to_chatgpt_stream(messages=messages, model=get_model(model), temperature=temperature):
            print_stream(stream)
            complete_response += stream
        print()
        pyperclip.copy(complete_response)
        return complete_response
    
    return cli


