import sys

def print_stream(value):
    sys.stdout.write(value)
    sys.stdout.flush()


def truncate_text(text, max_length):
    return f"{text[:max_length]}..." if len(text) > max_length else text
