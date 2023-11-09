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

def ask_to_chatgpt(prompt="Eres un util asistente. Responderas de forma directa y sin explicaciones"):
    @click.command(name="Commandline chatgpt question",)
    @click.argument('argument', default=None, required=False)
    @model_option
    @click.option('--temperature', '-t', type=int, help='Temperatura del modelo', default=0)
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
    
    return cli


