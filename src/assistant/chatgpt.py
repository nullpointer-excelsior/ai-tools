from dataclasses import dataclass
import os
import openai
from libs.openai_api import ChatGPTModel

openai.api_key = os.environ['OPENAI_API_KEY']

@dataclass
class ChatGPT:
    
    tokens: int
    model: ChatGPTModel
    
    def chat_completion(self ,messages, temperature=0):
        response = openai.ChatCompletion.create(
            model=self.model.value,
            messages=messages,
            temperature=temperature
        )
        self.tokens += response['usage']['total_tokens']
        return response['choices'][0]['message']['content']
    
    def get_completion(self, prompt, temperature=0): 
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages=messages, temperature=temperature)
    

    def update_model(self, model):
        self.model = model
    

