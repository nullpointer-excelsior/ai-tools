from colorama import Fore, Style

def green_color(text):
    return f'{Fore.GREEN}{text}{Style.RESET_ALL}'

def yellow_color(text):
    return f'{Fore.YELLOW}{text}{Style.RESET_ALL}'

def cyan_color(text):
    return f'{Fore.CYAN}{text}{Style.RESET_ALL}'

def red_color(text):
    return f'{Fore.RED}{text}{Style.RESET_ALL}'
