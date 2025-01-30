import argparse
from ollama import chat
from rich import print
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
    parser.add_argument(
        "--message", required=True, help="The message to send to the models"
    )
    args = parser.parse_args()
    return args.model, args.message


def print_columns(responses):
    console = Console()
    responses = [Panel(res[1], title=res[0]) for res in responses]
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


if __name__ == "__main__":
    models, message = parse_models()
    main(models, message)
