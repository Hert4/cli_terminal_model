import requests
import json
import os
from dotenv import load_dotenv
from prompt.system_prompt_api import SYSTEM_PROMPT

load_dotenv()


class Models:
    def __init__(self):
        self.api = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = [
            os.getenv("OPENROUTER_API_KEY"),
            os.getenv("OPENROUTER_API_KEY_1"),
            os.getenv("OPENROUTER_API_KEY_2"),
            os.getenv("OPENROUTER_API_KEY_3"),
        ]
        self.history = []

    def generate_response(self, user_input):
        messages = (
            [{"role": "system", "content": SYSTEM_PROMPT}]
            + self.history[-4:]
            + [{"role": "user", "content": user_input}]
        )

        payload = {
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": messages,
            "stream": True,
            "reasoning": {
                "effort": "high",
                "max_tokens": 2048,
            },
        }

        for key in self.api_key:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
                "X-Title": "MyLocalApp",
            }

            try:
                with requests.post(
                    self.api, headers=headers, json=payload, stream=True
                ) as r:
                    r.encoding = "utf-8"
                    if r.status_code == 200:

                        print("Assistant: ", end="", flush=True)
                        full_response = ""
                        reasoning = ""
                        buffer = ""

                        for chunk in r.iter_content(
                            chunk_size=1024, decode_unicode=True
                        ):
                            buffer += chunk
                            while True:
                                line_end = buffer.find("\n")
                                if line_end == -1:
                                    break

                                line = buffer[:line_end].strip()
                                buffer = buffer[line_end + 1 :]

                                if line.startswith("data: "):
                                    data = line[6:]
                                    if data == "[DONE]":
                                        print()
                                        self.history.append(
                                            {"role": "user", "content": user_input}
                                        )
                                        self.history.append(
                                            {
                                                "role": "assistant",
                                                "content": full_response,
                                            }
                                        )
                                        return f"<think>\n{reasoning}\n</think>\n{full_response}"

                                    try:
                                        data_obj = json.loads(data)
                                        delta = data_obj["choices"][0]["delta"]

                                        # Capture reasoning safely
                                        if "reasoning" in delta:
                                            reasoning += delta["reasoning"] or ""

                                        # Capture content
                                        content = delta.get("content")
                                        if content:
                                            print(content, end="", flush=True)
                                            full_response += content

                                    except json.JSONDecodeError:
                                        pass

                    elif r.status_code == 429:
                        print("Opps! Some issues occus you might want to restart!")
                        print("If restart does not help? Please comeback tomorrow")
                        continue
                    else:
                        print(f"Error: {r.status_code}, {r.text}")
                        return None

            except Exception as e:
                print(f"Exception occurred: {e}")
                continue

        print("All API keys exhausted or failed.")
        return None
