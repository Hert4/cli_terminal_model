from llama_cpp import Llama
import os
import threading


import sys
import os
import contextlib


@contextlib.contextmanager
def suppress_stderr():
    """Context manager that redirects stderr to devnull (suppresses llama.cpp logs)."""
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr


PATH = os.path.dirname(os.path.abspath(__file__))
from tools.tools import read_file


class QwenChatbot:
    def __init__(
        self,
        model_path=os.path.join(PATH, "models", "Qwen3-0.6B-GGUF/Qwen3-0.6B-Q8_0.gguf"),
    ):
        self.model = Llama(model_path=model_path)
        self.history = []

    def generate_response(self, user_input):
        SYSTEM_PROMPT = (
            read_file(PATH + "/prompt/system_prompt.md")
            + "\n\n"
            + read_file(PATH + "/prompt/memory.md")
        )
        messages = (
            [{"role": "system", "content": SYSTEM_PROMPT}]
            + self.history[-4:]
            + [{"role": "user", "content": user_input}]
        )

        # Simple prompt formatting for llama.cpp
        prompt = ""
        for msg in messages:
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        prompt += "Assistant:"

        def run_llama():
            response = ""
            print("\nAssistant:\n", end="", flush=True)

            with suppress_stderr():
                output = self.model(
                    prompt,
                    max_tokens=2048,
                    stop=["User:", "Assistant:"],
                    stream=True,
                )

                for chunk in output:
                    token = chunk["choices"][0]["text"]
                    print(token, end="", flush=True)
                    response += token

            print()
            self.history.append({"role": "assistant", "content": response})
            return response

        thread = threading.Thread(target=run_llama)
        thread.start()
