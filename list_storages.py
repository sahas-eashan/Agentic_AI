import os

assistant_path = r"venv_py310\lib\site-packages\phi\storage\assistant"

print("📦 Available storage backends in phi.storage.assistant:\n")

for file in os.listdir(assistant_path):
    if file.endswith(".py") and not file.startswith("__"):
        print(" -", file[:-3])  # remove .py extension
