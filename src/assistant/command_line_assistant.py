from pwn import log
import pyperclip
from assistant.chatgpt import ChatGPT
from assistant.chat_context import ChatContext, Command
from libs.colored import cyan_color, green_color, yellow_color
from libs.openai_api import ChatGPTModel
from libs.utils import print_stream


class ResetAssistantCommand(Command):
    name = 'reset'
    description = 'Resetar el maldito asistente.'

    def action(self, context: ChatContext, user_input: str):
        context.status('Reseteando asistente...')
        context.messages = [{ 'role': 'system', 'content': context.prompt }]
        context.assistant_input = context.chat_completion(messages=context.messages)
        context.success('Asistente reseteado!')


class CopyCommand(Command):
    name = 'copy'
    description = 'Copiar la ultima respuesta al portapapeles.'

    def action(self, context: ChatContext, user_input: str):
        pyperclip.copy(context.assistant_input)
        context.assistant_input = 'Respuesta copiada al portapapeles!!'


class ChangeModelCommand(Command):
    name = 'model'
    description = 'Actualiza el modelo del chat actual '

    def action(self, context: ChatContext, user_input: str):
        context.status('Seleccionar modelo')
        model_input = int(input(f"""
        Selecciona uno de los siguientes opciones:
            {green_color('1')}) {yellow_color('gpt3')}
            {green_color('2')}) {yellow_color('gpt3-16k')}
            {green_color('3')}) {yellow_color('gpt4')}
            {green_color('4')}) {yellow_color('gpt4-32k')}
        """))
        try:
            if model_input == 1:
                model = ChatGPTModel.GPT_3_5_TURBO
            elif model_input == 2:
                model = ChatGPTModel.GPT_3_5_TURBO_16K
            elif model_input == 3:
                model = ChatGPTModel.GPT_4
            elif model_input == 4:
                model = ChatGPTModel.GPT_4_32K
            else:
                context.assistant_input = f'Opción {model_input} invalida'
                return 
            context.update_model(model)
            context.assistant_input = f'Modelo cambiado a {model_input}'
        except ValueError:
            context.assistant_input = f'Opción {model_input} invalida'


class HelpCommand(Command):
    name = 'help'
    description = 'Muestra los comandos disponibles.'

    def action(self, context: ChatContext, user_input: str):
        context.assistant_input = f"\n{command_info(context.commands)}"


def is_command(user_input: str, command: str):
    return user_input.lower().strip() == command


def command_info(commands):
    command_list = '\t'.join([ f"[{green_color('*')}] {yellow_color(c.name)}: {c.description}\n" for c in commands ])
    return f"""
    Comandos disponibles:

    [{green_color('*')}] {yellow_color('exit')}: Salir del asistente.
    {command_list}
    """
    

def command_line_assistant(prompt: str, model: ChatGPTModel = ChatGPTModel.GPT_3_5_TURBO, custom_commands: list[Command] = []):
    commands = [
        ResetAssistantCommand(),
        CopyCommand(),
        ChangeModelCommand(),
        HelpCommand()
    ]
    commands += custom_commands

    context = ChatContext(
        prompt=prompt,
        messages=[{ 'role': 'system', 'content': prompt }],
        chatgpt=ChatGPT(tokens=0, model=model),
        commands=commands
    )

    try:
        print()
        assistant_progress = log.progress('AI Assistant')
        assistant_progress.status('Iniciando asistente...')
        assistant_input = ''
        print(command_info(commands))
        print_stream(green_color('[Assistant] '))
        for stream in context.chat_completion_stream(messages=context.messages):
            print_stream(stream)

        assistant_progress.success('Asistente listo!')

        while True:
            user_input = input(f"{assistant_input}\n\n{green_color('[User] ')}")
            print()
            context.progress('Estado chat context')
            # exit command
            if is_command(user_input, 'exit'):
                break
            # custom commands
            command_executed = False
            for cmd in commands:
                if is_command(user_input, cmd.name):
                    context.assistant_input = assistant_input
                    cmd.action(user_input=user_input, context=context)
                    assistant_input = context.assistant_input
                    command_executed = True
                    context.success(f'Comando {cyan_color(cmd.name)} ejecutado.')
                    break
            if command_executed:
                continue

            context.status('Pensando...')
            print_stream(f"\n{green_color('[Assistant] ')}")
            context.asking_stream(user_input)
            context.success("Listo!")

    except KeyboardInterrupt:
        log.info('Saliendo...')
    # log.info(f'Total tokens: {context.used_tokens()}\n')
    log.info('Total tokens: No available in stream mode\n')

