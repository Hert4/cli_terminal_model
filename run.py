from qwen import QwenChatbot
from tools.tools import *
from api_model_router import Models

chatbot = QwenChatbot()
models = Models()
print("SUCCESSFULLY init!!")

# define function
function_map = {
    "get_search": get_search,
    "read_file": read_file,
    "search_file": search_file,
    "update_file": update_file,
    "run_python_code": run_python_code,
    "run_terminal": run_terminal,
}


def handle_function_call(func_name: str, args: dict) -> str:
    try:
        func = function_map.get(func_name)
        if func:
            return func(**args)
        else:
            return f"Hàm {func_name} không được hỗ trợ"
    except Exception as e:
        return f"ERROR: {str(e)}"


def chat():
    while True:
        user_prompt = input("You: ")
        response = chatbot.generate_response(user_prompt)

        while True:
            try:
                function_calls = parse_function_calls(response)
                if not function_calls:
                    break

                tool_results = []
                for call in function_calls:
                    result = handle_function_call(call["name"], call["arguments"])
                    response_str = f"<tool_response>\n{result}\n</tool_response>"
                    tool_results.append(response_str)
                    print("Get the results...")

                combined_responses = "\n".join(tool_results)
                response = chatbot.generate_response(combined_responses)

            except Exception as e:
                print(f"LỖI HỆ THỐNG: {str(e)}")
                break

        print(f"\033[31mAssistant: {response}\033[0m\n")


def chat_api():
    while True:
        user_prompt = input("You: ")
        response = models.generate_response(user_prompt)

        while True:
            try:
                function_calls = parse_function_calls(response)
                if not function_calls:
                    break

                tool_results = []
                for call in function_calls:
                    result = handle_function_call(call["name"], call["arguments"])
                    response_str = f"<tool_response>\n{result}\n</tool_response>"
                    tool_results.append(response_str)
                    print("Get the results...")

                combined_responses = "\n".join(tool_results)
                response = models.generate_response(combined_responses)

            except Exception as e:
                print(f"LỖI HỆ THỐNG: {str(e)}")
                break

        print(f"\033[31mAssistant: {response}\033[0m\n")


if __name__ == "__main__":
    # select_model = input("SELECT model (choose 'qwen' or 'deepseek'):")
    # if select_model.strip() == "qwen":
    #     chat()
    # elif select_model.strip() == "deepseek":
    #     chat_api()
    # else:
    #     print("Good byes")
    chat_api()
