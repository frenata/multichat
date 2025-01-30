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
    parser.add_argument("--message", help="The message to send to the models")
    args = parser.parse_args()
    return args.model, args.message


def print_columns(responses):
    console = Console()
    responses = [Panel(res[1], title=res[0]) for res in responses]
    cols = Columns(
        responses, equal=True, width=(console.size.width // len(responses) - 2)
    )
    print(cols)


def print_chats(chats):
    console = Console()
    responses = [
        Panel(messages[-1].content, title=model) for model, messages in chats.items()
    ]
    cols = Columns(
        responses, equal=True, width=(console.size.width // len(responses) - 2)
    )
    print(cols)


def main(models, message):
    responses = []
    for model in models:
        try:
            response = chat(
                model=model, messages=[{"role": "user", "content": message}]
            )
            responses.append((model, response["message"]["content"]))
        except Exception as e:
            responses.append((model, str(e)))

    print_columns(responses)


def interactive(models):
    messages = collections.defaultdict(list)

    while True:
        responses = []
        message = str(Prompt.ask(">> "))
        for model in models:
            user_message = Message(role="user", content=message)
            messages[model].append(user_message)
            model_message: dict = chat(model=model, messages=messages[model])
            messages[model].append(model_message.message)
            responses.append((model, model_message.message.content))
        print_chats(messages)


if __name__ == "__main__":
    models, message = parse_models()
    if message is not None:
        main(models, message)
    else:
        interactive(models)
