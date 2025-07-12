import requests
import json
from tools.tools import read_file
import os
from prompt.system_prompt_api import SYSTEM_PROMPT

PATH = os.path.dirname(os.path.abspath(__file__))


class Models:
    def __init__(self, api="https://api.deepinfra.com/v1/openai/chat/completions"):
        self.api = api
        self.history = []

    def generate_response(self, user_input):

        messages = (
            [{"role": "system", "content": SYSTEM_PROMPT}]
            + self.history[-4:]
            + [{"role": "user", "content": user_input}]
        )

        payload = {"model": "deepseek-ai/DeepSeek-R1-0528-Turbo", "messages": messages}

        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(self.api, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            response_data = response.json()
            assistant_reply = (
                response_data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            self.history.append({"role": "user", "content": user_input})
            self.history.append({"role": "assistant", "content": assistant_reply})
            return assistant_reply
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None


# if __name__ == "__main__":
#     model = Models()
#     while True:

#         user_input = input("You:")
#         response = model.generate_response(user_input)
#         print(response)
