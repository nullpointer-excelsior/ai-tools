import click
from chatbots import summarize_text
import sys, json


@click.group()
def main():
    """Chatgpt CLI utilities"""

@main.command()
@click.argument('text', default=None, required=False)
def summarize(text):
    if not text:
        text = sys.stdin.read().strip()
    response = summarize_text(text)
    print(json.dumps(response))


@main.command()
def cmd2():
    print("cmd2")




if __name__ == "__main__":
    main()