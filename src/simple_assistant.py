import click
from assistant.command_line_assistant import command_line_assistant
from libs.openai_api import ChatGPTModel

model_choices= [
    'gpt3',
    'gpt3-16k',
    'gpt4',
    'gpt4-32k'
]

model_mapper = {
   'gpt3': ChatGPTModel.GPT_3_5_TURBO,
    'gpt3-16k': ChatGPTModel.GPT_3_5_TURBO_16K,
    'gpt4': ChatGPTModel.GPT_4,
    'gpt4-32k': ChatGPTModel.GPT_4_32K 
}
    

@click.command()
@click.option('--model', '-m', 
              type=click.Choice(model_choices, 
              case_sensitive=False),
              default='gpt3',
              help='Indica el modelo AI a usar')
def create_assistant(model):
    command_line_assistant(prompt="Se un util asistente", model=model_mapper[model])


if __name__ == "__main__":
    create_assistant()
