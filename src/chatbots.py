from libs.openai_api import ask_to_chatgpt


def summarize_text(content):
    messages = [
        {
            'role': 'system',
            'content': 'Actual como un profesor del ambito tecnologico y resume los siguientes textos de forma clara enfocandose en una respuesta tecnica, los textos deben ser resumidos en español si fuese necesario'
        },
        {
            'role': 'user',
            'content': content
        }
    ]
    return ask_to_chatgpt(messages=messages)
