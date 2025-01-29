import argparse
from ollama import chat, ChatResponse


def parse_models():
    parser = argparse.ArgumentParser(description="Send message to multiple models")
    parser.add_argument(
        "--model",
        nargs="+",
        help="One or more model names to send the message to",
        required=True,
    )
    parser.add_argument("message", help="The message to send to the models")
    args = parser.parse_args()
    return args.model, args.message


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
    models, message = parse_models()
    print(send_parallel(models, message))
