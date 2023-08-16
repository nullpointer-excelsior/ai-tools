import os
import openai
from libs.openai_api import ChatGPTModel

openai.api_key = os.environ['OPENAI_API_KEY']

class ChatGPT:
    
    tokens = 0
    
    def chat_completion(self ,messages, model: ChatGPTModel=ChatGPTModel.GPT_3_5_TURBO, temperature=0):
        response = openai.ChatCompletion.create(
            model=model.value,
            messages=messages,
            temperature=temperature
        )
        self.tokens += response['usage']['total_tokens']
        return response['choices'][0]['message']['content']
    
    def get_completion(self, prompt, model: ChatGPTModel=ChatGPTModel.GPT_3_5_TURBO, temperature=0): 
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages=messages, model=model.value, temperature=temperature)
    

