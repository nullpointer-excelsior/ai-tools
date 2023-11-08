import click


def model_option(wrapped_function):
    model_choices= [
        'gpt3',
        'gpt3-16k',
        'gpt4',
        'gpt4-32k'
    ]
    return click.option(
        '--model', '-m',
        type=click.Choice(model_choices, case_sensitive=False),
        default='gpt3',
        help='Indica el modelo AI a usar'
    )(wrapped_function)