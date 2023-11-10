import click

def model_option(model='gpt3'):
    model_choices= [
        'gpt3',
        'gpt3-16k',
        'gpt4',
        'gpt4-32k'
    ]
    def decorator(wrapped_function):
        
        return click.option(
            '--model', '-m',
            type=click.Choice(model_choices, case_sensitive=False),
            default=model,
            help='Indica el modelo AI a usar'
        )(wrapped_function)

    return decorator