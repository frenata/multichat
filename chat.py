import asyncio
import random
import os
import argparse
from ollama import chat, Message, AsyncClient
from rich import print
from rich.prompt import Prompt
from rich.live import Live
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


def prep_panels(chats):
    console = Console()
    panels = [
        Panel("...", title=model, style=f"color({hash(model) % 240})")
        for model in chats
    ]
    cols = Columns(panels, equal=True, width=((console.size.width - 10) // len(panels)))
    return Live(Panel(cols)), panels


client = AsyncClient()


async def chat_with_model(model, message, prior_messages, panel, barrier):
    user_message = Message(role="user", content=message)
    prior_messages.append(user_message)
    model_message: dict = await client.chat(model=model, messages=prior_messages)
    prior_messages.append(model_message.message)
    panel.renderable = model_message.message.content
    await barrier.wait()


async def interactive(models):
    chats = {model: [] for model in models}
    barrier = asyncio.Barrier(len(models) + 1)

    while True:
        message = str(Prompt.ask(">> "))
        if message in ["exit", "quit", "q", "x"]:
            exit(0)
        live, panels = prep_panels(chats)
        live.start()
        for i, model in enumerate(models):
            asyncio.create_task(
                chat_with_model(model, message, chats[model], panels[i], barrier)
            )
        await barrier.wait()
        live.stop()


if __name__ == "__main__":
    if os.getenv("OLLAMA_API_BASE", None) is None:
        print("Please set OLLAMA_API_BASE to connect to Ollama.")
        exit(1)

    models = parse_models()
    asyncio.run(interactive(models))
