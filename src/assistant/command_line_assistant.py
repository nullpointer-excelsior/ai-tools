from pwn import log
import pyperclip, os, sys
from assistant.chatgpt import ChatGPT
from assistant.chat_context import ChatContext, Command
from libs.colored import cyan_color, green_color, red_color, yellow_color
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
            {green_color('5')}) {yellow_color('salir')}
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
            elif model_input == 5:
                return
            else:
                print(f'Opción {model_input} invalida')
                return 
            context.update_model(model)
            print(f'Modelo cambiado a {cyan_color(model)}')
        except ValueError:
            print(f'Opción {model_input} invalida')


class HelpCommand(Command):
    name = 'help'
    description = 'Muestra los comandos disponibles.'

    def action(self, context: ChatContext, user_input: str):
        print(f"\n{command_info(context.commands)}")


class DebugCommand(Command):
    name = 'debug'
    description = 'Muestra la configuracion del agente de ChatGPT'

    def action(self, context: ChatContext, user_input: str):
        messages = "\n\t".join([f"{m['role']}: {m['content']}" for m in context.messages])
        print(f"""
            {yellow_color('model')}: {context.chatgpt.model.value}
            {yellow_color('messages')}: {messages}
        """)


class PromptCommand(Command):
    name = 'prompt'
    description = 'Prompts disponibles para ajustar el asistente'

    def action(self, context: ChatContext, user_input: str):
        # get current path
        script_path = os.path.abspath(sys.argv[0])
        application_path = os.path.dirname(os.path.dirname(script_path))
        # get prompt files
        prompt_dir = f'{application_path}/src/prompts'
        prompt_files = [file for file in os.listdir(prompt_dir) if os.path.isfile(os.path.join(prompt_dir, file))]
        options = "\t".join([f"{green_color(i)}) {yellow_color(p)}\n" for i, p in enumerate(prompt_files, 1)])
        print(f"""\n\tPrompt disponibles:\n\n\t{options}""")
        # select prompt
        select = input("Selecione el prompt para actualizar el asistente: ")
        try:
            filename = f"{prompt_dir}/{select.strip()}"
            with open(filename, 'r') as file_selected:
                prompt = file_selected.read().strip()
                context.messages = [{ 'role': 'system', 'content': prompt }]
                for stream in context.chat_completion_stream(messages=context.messages):
                    print_stream(stream)
        except FileNotFoundError:
            print(f'\n[{red_color("*")}] Archivo prompt invalido!')


def parse_input_to_params(input: str):
    return input.lower().strip().split(' ')


def is_command(user_input: str, command: str):
    params = parse_input_to_params(user_input)
    return params[0] == command


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
        HelpCommand(),
        DebugCommand(),
        PromptCommand()
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
            user_input = input(f"\n\n{green_color('[User] ')}")
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
            for st in context.asking_stream(user_input):
                print_stream(f"{cyan_color(st)}")
            context.success("Listo!")


    except KeyboardInterrupt:
        log.info('Saliendo...')
    # log.info(f'Total tokens: {context.used_tokens()}\n')
    log.info('Total tokens: No available in stream mode\n')

