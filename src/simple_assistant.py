import click
from assistant.command_line_assistant import command_line_assistant
from libs.cli import model_option
from libs.openai_api import get_model
    

@click.command()
@model_option
def create_assistant(model):
    command_line_assistant(prompt="Se un util asistente, responde mis consultas de forma clara, resumida y respuesta directa", model=get_model(model))


if __name__ == "__main__":
    create_assistant()
