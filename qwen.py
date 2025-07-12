from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from prompt.prompt import TOOLS
import os
import threading
import torch
from dotenv import load_dotenv

load_dotenv()
PATH = os.path.dirname(os.path.abspath(__file__))
from tools.tools import read_file


device = "cuda:0" if torch.cuda.is_available() else "cpu"


class QwenChatbot:
    def __init__(
        self,
        model_name=os.path.join(PATH, "models", os.getenv("MODEL_NAME")),
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, local_files_only=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, local_files_only=True, torch_dtype=torch.float32
        ).to(device)
        self.history = []

    def generate_response(self, user_input):
        SYSTEM_PROMPT = (
            read_file(PATH + "/prompt/system_prompt.md")
            + "\n\n"
            + read_file(PATH + "/prompt/memory.md")
        )
        messages = (
            [{"role": "system", "content": SYSTEM_PROMPT}]
            + self.history[:-4]  # change this if can handel
            + [{"role": "user", "content": user_input}]
        )

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=True,
            tools=TOOLS,
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
        ).to(device)
        streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, skip_special_token=True
        )

        generation_kwargs = dict(
            inputs,
            streamer=streamer,
            max_new_tokens=2048,
            top_k=50,
            top_p=20,
            min_p=0.1,
        )
        thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        response = ""
        print("\nAssistant:\n", end="", flush=True)
        for token in streamer:
            print(token, end="", flush=True)
            response += token
        print()

        self.history.append({"role": "assistant", "content": response})

        return response
