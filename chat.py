import collections
import argparse
from ollama import chat, Message
from rich import print
from rich.prompt import Prompt
from rich.columns import Columns
from rich.panel import Panel
from rich.console import Console


def parse_models():
    parser = argparse.ArgumentParser(description="Send message to multiple models")
    parser.add_argument(
        "--model",
        nargs="+",
        help="One or more model names to send the message to",
        required=True,
    )
    args = parser.parse_args()
    return args.model


def print_chats(chats):
    console = Console()
    responses = [
        Panel(messages[-1].content, title=model) for model, messages in chats.items()
    ]
    cols = Columns(
        responses, equal=True, width=(console.size.width // len(responses) - 2)
    )
    print(cols)


def interactive(models):
    messages = collections.defaultdict(list)

    while True:
        message = str(Prompt.ask(">> "))
        for model in models:
            user_message = Message(role="user", content=message)
            messages[model].append(user_message)
            model_message: dict = chat(model=model, messages=messages[model])
            messages[model].append(model_message.message)
        print_chats(messages)


if __name__ == "__main__":
    models = parse_models()
    interactive(models)
