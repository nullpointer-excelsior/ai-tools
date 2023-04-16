import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']


def ask_to_chatgpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return {
        'total_token': response['usage']['total_tokens'],
        'answer': response['choices'][0]['message']['content']
    }

