from pwn import log
import pyperclip
from assistant.chatgpt import ChatGPT
from assistant.chat_context import ChatContext, Command
from libs.colored import green_color, yellow_color


class ResetAssistantCommand(Command):
    name = 'reset'
    description = 'Resetar el maldito asistente.'

    def action(self, user_input: str, context: ChatContext):
        context.status('Reseteando asistente...')
        context.messages = [{ 'role': 'system', 'content': context.prompt }]
        context.assistant_input = context.chat_completion(messages=context.messages)
        context.success('Asistente reseteado!')


class CopyCommand(Command):
    name = 'copy'
    description = 'Copiar la ultima respuesta al portapapeles.'

    def action(self, user_input: str, context: ChatContext):
        pyperclip.copy(context.assistant_input)
        context.assistant_input = 'Respuesta copiada al portapapeles!!'


class HelpCommand(Command):
    name = 'help'
    description = 'Muestra los comandos disponibles.'

    def action(self, user_input: str, context: ChatContext):
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
    

def command_line_assistant(prompt: str, custom_commands: list[Command] = []):
    
    commands = [
        ResetAssistantCommand(),
        CopyCommand(),
        HelpCommand()
    ]
    commands += custom_commands

    context = ChatContext(
        prompt=prompt,
        messages=[{ 'role': 'system', 'content': prompt }],
        chatgpt=ChatGPT(),
        commands=commands
    )

    try:
        print()
        assistant_progress = log.progress('AI Assistant')
        assistant_progress.status('Iniciando asistente...')
        assistant_input = context.chat_completion(messages=context.messages)
        assistant_progress.success('Asistente listo!')
        print(command_info(commands))
        while True:
            user_input = input(f"{green_color('[Assistant]')}{assistant_input}\n\n{green_color('[User]')}")
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
                    context.success(f'Comando {cmd.name} ejecutado.')
                    break
            if command_executed:
                continue

            context.status('Pensando...')
            assistant_input = context.asking(user_input)
            context.success("Listo!")

    except KeyboardInterrupt:
        log.info('Saliendo...')
    log.info(f'Total tokens: {context.used_tokens()}\n')

