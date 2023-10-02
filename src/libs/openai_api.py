import os
import openai
from enum import Enum
from pwn import log
from colorama import Fore, Style


openai.api_key = os.environ['OPENAI_API_KEY']


class ChatGPTModel(Enum):
    GPT_3_5_TURBO = 'gpt-3.5-turbo'
    GPT_3_5_TURBO_16K = 'gpt-3.5-turbo-16k'
    GPT_4 = 'gpt-4'
    GPT_4_32K = 'gpt-4-32k'


def get_model(model: str):
    model_mapper = {
        'gpt3': ChatGPTModel.GPT_3_5_TURBO,
        'gpt3-16k': ChatGPTModel.GPT_3_5_TURBO_16K,
        'gpt4': ChatGPTModel.GPT_4,
        'gpt4-32k': ChatGPTModel.GPT_4_32K 
    } 
    return model_mapper[model]


def ask_to_chatgpt(messages, model=ChatGPTModel.GPT_3_5_TURBO, temperature=0):
    response = openai.ChatCompletion.create(
        model=model.value,
        messages=messages,
        temperature=temperature
    )
    return {
        'total_token': response['usage']['total_tokens'],
        'answer': response['choices'][0]['message']['content']
    }


def get_completion(prompt, model=ChatGPTModel.GPT_3_5_TURBO, temperature=0): 
    messages = [{"role": "user", "content": prompt}]
    return ask_to_chatgpt(messages=messages, model=model, temperature=temperature)


def ask_to_chatgpt_stream(messages, model=ChatGPTModel.GPT_3_5_TURBO, temperature=0):
    response = openai.ChatCompletion.create(
        model=model.value,
        messages=messages,
        temperature=temperature,
        stream=True
    )
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        answer = delta.get('content', '')
        yield answer


def get_completion_stream(prompt, model=ChatGPTModel.GPT_3_5_TURBO, temperature=0):
    messages = [{"role": "user", "content": prompt}]
    return ask_to_chatgpt_stream(messages=messages, model=model, temperature=temperature)


def completion_task(prompt: str):
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
