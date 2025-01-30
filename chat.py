import asyncio
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


class Session:
    def __init__(self, models):
        self.models = models
        self.client = AsyncClient()

    def prep_panels(self):
        console = Console()
        panels = [
            Panel("...", title=model, style=f"color({hash(model) % 240})")
            for model in self.models
        ]
        cols = Columns(
            panels, equal=True, width=((console.size.width - 10) // len(panels))
        )
        return Live(Panel(cols)), panels

    async def chat_with_model(self, model, message, panel, barrier):
        user_message = Message(role="user", content=message)
        self.chats[model].append(user_message)
        model_message: dict = await self.client.chat(
            model=model, messages=self.chats[model]
        )
        self.chats[model].append(model_message.message)
        panel.renderable = model_message.message.content
        await barrier.wait()

    async def interactive(self):
        self.chats = {model: [] for model in self.models}
        barrier = asyncio.Barrier(len(self.models) + 1)

        while True:
            message = str(Prompt.ask(">> "))
            if message in ["exit", "quit", "q", "x"]:
                exit(0)
            live, panels = self.prep_panels()
            live.start()
            for i, model in enumerate(self.models):
                asyncio.create_task(
                    self.chat_with_model(model, message, panels[i], barrier)
                )
            await barrier.wait()
            live.stop()


if __name__ == "__main__":
    if os.getenv("OLLAMA_API_BASE", None) is None:
        print("Please set OLLAMA_API_BASE to connect to Ollama.")
        exit(1)

    asyncio.run(Session(parse_models()).interactive())
