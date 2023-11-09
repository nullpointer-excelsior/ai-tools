import sys
import sys, select
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


def read_argument():
    return sys.argv[1] if len(sys.argv) > 1 else None


def read_stdin():
    if select.select([sys.stdin,],[],[],0.0)[0]:
        return sys.stdin.read().strip()
    return None


def read_file(filename):
    with open(filename, "r") as file:
        return file.read()
