import sys
from ollama import chat
from ollama import ChatResponse


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

    formatted_responses = "\n".join([f"{model}: {response}" for model, response in responses])
    return formatted_responses


if __name__ == "__main__":
    message = sys.argv[1]
    print(send_parallel(["llama3", "deepseek-r1:1.5b"], message))
