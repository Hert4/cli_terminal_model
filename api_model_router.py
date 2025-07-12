import requests
import json
import os
from dotenv import load_dotenv
from tools.tools import read_file

load_dotenv()
from prompt.system_prompt_api import SYSTEM_PROMPT

PATH = os.path.dirname(os.path.abspath(__file__))


class Models:
    def __init__(self):
        self.api = "https://openrouter.ai/api/v1/chat/completions"

        self.api_key = [
            os.getenv("API_KEY"),
            os.getenv("API_KEY_1"),
            os.getenv("API_KEY_2"),
            os.getenv("API_KEY_3"),
        ]
        self.history = []

    def generate_response(self, user_input):
        messages = (
            [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                    + f"\n{read_file(PATH + '/prompt/memory.md')}",
                }
            ]
            + self.history[-4:]
            + [{"role": "user", "content": user_input}]
        )

        payload = {
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": messages,
        }

        for key in self.api_key:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
                "X-Title": "MyLocalApp",
            }

            try:
                response = requests.post(
                    self.api, headers=headers, data=json.dumps(payload)
                )

                if response.status_code == 200:
                    response_data = response.json()
                    message = response_data.get("choices", [{}])[0].get("message", {})

                    assistant_reply = message.get("content", "")
                    reasoning = f'<think>\n{message.get("reasoning", "")}\n</think>\n'

                    self.history.append({"role": "user", "content": user_input})
                    self.history.append(
                        {"role": "assistant", "content": assistant_reply}
                    )
                    return reasoning + assistant_reply

                elif response.status_code == 429:
                    print(f"Rate limit hit with key: {key}, trying next...")
                    continue  # thử key kế tiếp

                else:
                    print(f"Error: {response.status_code}, {response.text}")
                    return None

            except Exception as e:
                print(f"Exception occurred: {e}")
                return None

        print("All API keys exhausted or failed.")
        return None
