## Multichat

This is a simple interactive program that allows you to simultaneously chat with multiple Ollama models at once.

Each user message is sent to all models simultaneously along with the model-specific history.

### Requirements

  * `uv`
  * `ollama`

### Usage

Install the deps and initiate the environment via `uv sync`.

Run the program with `uv chat.py --models <list> <of> <ollama> <models>`

Exit the program with (q)uit or e(x)it.
