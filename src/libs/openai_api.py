import os
import openai
from pwn import log
from colorama import Fore, Style


openai.api_key = os.environ['OPENAI_API_KEY']


def ask_to_chatgpt(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=200
    )
    return {
        'total_token': response['usage']['total_tokens'],
        'answer': response['choices'][0]['message']['content']
    }


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0): 
    messages = [{"role": "user", "content": prompt}]
    return ask_to_chatgpt(messages=messages, model=model, temperature=temperature)


def chatgpt_cli(prompt: str):
    tokens = 0
    try:
        assistant_progress = log.progress('AI Assistant')
        assistant_progress.status('Iniciando asistente...')
        messages = [{ 'role': 'system', 'content': prompt }]
        response = ask_to_chatgpt(messages)
        input_message = response['answer']
        tokens += response['total_token']
        assistant_progress.success('Asistente listo!')
        while True:
            user_input = input(f'{Fore.GREEN}\n[Assistant]: {Style.RESET_ALL}{input_message}\n\n{Fore.GREEN}[User]: {Style.RESET_ALL}')
            if user_input.lower().strip() == 'salir':
                break
            print()
            chat_status = log.progress('Estado chat')
            chat_status.status('Escribiendo...')
            messages.append({ 'role': 'user', 'content': user_input })
            response = ask_to_chatgpt(messages)
            tokens += response['total_token']
            chat_status.success("Listo!")
            messages.append({ 'role': 'assistant', 'content': response['answer']})
            input_message = response['answer']
    except KeyboardInterrupt:
        log.info('Saliendo...')
    log.info(f'Total tokens: {tokens}\n')


def completion_cli(prompt: str):
    tokens = 0
    try:
        assistant_progress = log.progress('AI Task')
        assistant_progress.status('Iniciando tarea basada en AI...')
        messages = [{ 'role': 'system', 'content': prompt }]
        response = ask_to_chatgpt(messages)
        input_message = response['answer']
        tokens += response['total_token']
        assistant_progress.success('AI Task listo!')
        user_input = input(f'{Fore.GREEN}\n[Task]: {Style.RESET_ALL}{input_message}\n\n{Fore.GREEN}[User]:{Style.RESET_ALL} ')
        print()
        chat_status = log.progress('Estado tarea')
        chat_status.status('Procesando...')
        messages.append({ 'role': 'user', 'content': user_input })
        response = ask_to_chatgpt(messages)
        tokens += response['total_token']
        chat_status.success("Listo!")
        messages.append({ 'role': 'assistant', 'content': response['answer']})
        print(f"{Fore.GREEN}\n[Task]:{Style.RESET_ALL} {response['answer']}\n")
    except KeyboardInterrupt:
        log.info('Terminando tarea...')
    log.info(f'Total tokens: {tokens}\n\n')