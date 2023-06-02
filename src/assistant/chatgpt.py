import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

class ChatGPT:
    
    tokens = 0
    
    def chat_completion(self ,messages, model="gpt-3.5-turbo", temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        self.tokens += response['usage']['total_tokens']
        return response['choices'][0]['message']['content']
    
    def get_completion(self, prompt, model="gpt-3.5-turbo", temperature=0): 
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages=messages, model=model, temperature=temperature)
    

