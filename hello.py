import sys
import argparse
from ollama import chat, ChatResponse


def parse_models():
    parser = argparse.ArgumentParser(description='Send message to multiple models')
    parser.add_argument('--model', nargs='+',
                       help='One or more model names to send the message to',
                       required=True)
    args = parser.parse_args()
    return args.model


def send_parallel(models, message):
    responses = []
    for model in models:
        response = chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )
        responses.append((model, response["message"]["content"]))

    formatted_responses = "\n\n=========\n\n".join(
        [f"{model}: \n{response}" for model, response in responses]
    )
    return formatted_responses


if __name__ == "__main__":
    models = parse_models()
    message = sys.argv[2] if len(sys.argv) > 2 else "Hello"
    print(send_parallel(models, message))
