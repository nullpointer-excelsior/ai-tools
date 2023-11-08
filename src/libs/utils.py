import sys
from pwn import log

def print_stream(value):
    sys.stdout.write(value)
    sys.stdout.flush()


def truncate_text(text, max_length):
    return f"{text[:max_length]}..." if len(text) > max_length else text


def suppress_keyboard_interrupt(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            log.info('Saliendo...')
    return wrapper