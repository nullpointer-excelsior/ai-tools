
from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from typing import Any
from assistant.chatgpt import ChatGPT
from pwn import log

from libs.utils import print_stream

@dataclass
class ChatContext():
    
    prompt: str
    messages: list
    chatgpt: ChatGPT
    commands: list
    chat_status: Any = None
    assistant_input = ''

    def progress(self, msg):
        self.chat_status = log.progress(msg)

    def status(self, msg):
        self.chat_status.status(msg)

    def success(self, msg):
        self.chat_status.success(msg)

    def chat_completion(self, messages):
        return self.chatgpt.chat_completion(messages)
    
    def chat_completion_stream(self, messages):
        return self.chatgpt.chat_completion_stream(messages)
    
    def asking(self, message):
        self.add_message({ 'role': 'user', 'content': message })
        answer = self.chat_completion(messages=self.messages)
        self.add_message({ 'role': 'assistant', 'content': answer})
        return answer
    
    def asking_stream(self, message):
        self.add_message({ 'role': 'user', 'content': message })
        return self.chat_completion_stream(messages=self.messages)
    
    def add_message(self, message):
        self.messages.append(message)
    
    def used_tokens(self):
        return self.chatgpt.tokens
    
    def update_model(self, model):
        self.chatgpt.update_model(model)


    


@dataclass
class Command(ABC):
    
    @property
    def name(self) -> str:
        ...
    @property
    def description(self) -> str:
        ...
    
    @abstractclassmethod
    def action(self, context: ChatContext, user_input: str):
        ...


