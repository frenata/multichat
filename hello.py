import sys
from ollama import chat
from ollama import ChatResponse


def send_parallel(models, message):
    responses = []
    for model in models:
        responses.append(
            chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
            )
        )

    return [response["message"]["content"] for response in responses]


if __name__ == "__main__":
    message = sys.argv[1]
    print(send_parallel(["llama3", "deepseek-r1:1.5b"], message))
