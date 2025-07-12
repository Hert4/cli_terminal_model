def parse_function_calls(response):
    import re
    import json
    import ast

    function_calls = []
    pattern = r"<tool_call>(.*?)</tool_call>"

    matches = re.findall(pattern, response, re.DOTALL)

    for raw_match in matches:
        cleaned_str = raw_match.strip()
        if not cleaned_str:
            continue

        try:
            call_data = json.loads(cleaned_str)
        except json.JSONDecodeError:
            try:

                fixed_keys = re.sub(r"([a-zA-Z_]\w*)\s*:", r'"\1":', cleaned_str)
                fixed_quotes = fixed_keys.replace("'", '"')
                call_data = json.loads(fixed_quotes)
            except:
                try:
                    call_data = ast.literal_eval(cleaned_str)
                except:
                    print(f"Failed to parse: {cleaned_str}")
                    continue

        req_keys = call_data.keys() if isinstance(call_data, dict) else []
        if "name" not in req_keys:
            continue

        func_call = {
            "name": call_data["name"],
            "arguments": call_data.get("arguments", {}),
        }
        function_calls.append(func_call)

    return function_calls


######## Search tools ########
from googlesearch import search


def get_search(query: str, num_results: int = 3):
    try:

        urls = list(search(query, num_results=num_results, lang="vi"))
        if not urls:
            return "Không tìm thấy kết quả"

        results = []
        for url in urls:
            results.append(scrape_webpage(url))

        return results
    except Exception as e:
        return str(e)


def scrape_webpage(url: str):
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(
            url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        soup = BeautifulSoup(response.text, "html.parser")

        # Loại bỏ các thẻ không cần thiết
        for tag in soup(["script", "style", "header", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:5000] + "..."
    except Exception as e:
        return f"Lỗi: {str(e)}"


def read_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        finally_content = file.read()
    return finally_content


##### File tools #####
import os


def search_file(file_name, search_path="."):
    found_files = []
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file_name in file:
                found_files.append(os.path.join(root, file))
    return found_files


def adjust_file(file_path, content):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)
    return "File updated successfully."


def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return "File write successfully."


##### Terminal and run python code ####
import subprocess


def run_terminal(command: str):

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Lỗi: {result.stderr.strip()}"
    except Exception as e:
        return f"Lỗi khi chạy lệnh: {str(e)}"


def run_python_code(code: str):

    try:
        local_vars = {}
        exec(code, {}, local_vars)

        return local_vars.get("output")
    except Exception as e:
        return f"Lỗi khi chạy mã: {str(e)}"
