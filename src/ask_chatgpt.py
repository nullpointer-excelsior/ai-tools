import click
import os
import pyperclip
from libs.cli import model_option
from libs.openai_api import get_completion_stream, get_model
from libs.utils import print_stream, read_stdin


def read_file_or_get_content(value):
    if os.path.exists(value):
        with open(value, 'r') as file:
            return file.read()
    return value


@click.command()
@click.argument('argument', default=None, required=False)
@model_option
@click.option('--temperature', '-t', type=int, help='Temperatura del modelo', default=0)
def ask_to_chatgpt(argument, model, temperature):
    content = argument if argument is not None else read_stdin()
    content = read_file_or_get_content(content)
    complete_response = ''
    for stream in get_completion_stream(prompt=content, model=get_model(model), temperature=temperature):
        print_stream(stream)
        complete_response += stream
    print()
    pyperclip.copy(complete_response)


if __name__ == "__main__":
    ask_to_chatgpt()