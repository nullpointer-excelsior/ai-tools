import click

def model_option(model='gpt4om'):
    model_choices= [
        'gpt3',
        'gpt4',
        'gpt4t',
        'gpt4o',
        'gpt4om'
    ]
    def decorator(wrapped_function):
        
        return click.option(
            '--model', '-m',
            type=click.Choice(model_choices, case_sensitive=False),
            default=model,
            help='Indica el modelo AI a usar'
        )(wrapped_function)

    return decorator


def temperature_option(temperature=0):

    def decorator(wrapped_function):
        
        return click.option(
            '--temperature', '-t',
            type=float, 
            help='Temperatura del modelo. Entre 0 y 2. Los valores más altos como 0.8 harán que la salida sea más aleatoria, mientras que los valores más bajos como 0.2 la harán más enfocada y determinista.', 
            default=temperature
        )(wrapped_function)
    
    return decorator