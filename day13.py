# day13.py：合体！Agent = ReAct 引擎 + 扫文件夹 + 读文件 + 检查 Verilog
import requests
import os
import sys
import json
import glob
from dotenv import load_dotenv
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


# 工具1：列出所有 .v 文件
def list_files():
    files = glob.glob("*.v")
    return "\n".join(files)   # 把文件名列表拼成多行字符串返回


# 工具2：读文件
def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "列出当前目录下所有 .v 文件",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取一个文件的内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "要读取的文件名"}
                },
                "required": ["filename"]
            }
        }
    }
]


# system 角色：把 AI 设定成 Verilog 语法检查器
messages = [
    {"role": "system", "content": "你是一个 Verilog 语法检查器，检查代码语法错误并给出修改建议"},
    {"role": "user", "content": "帮我检查项目里所有 .v 文件的语法错误"}
]
body = {"model": "deepseek-chat", "messages": messages, "tools": tools}


while True:
    resp = requests.post(URL, json=body, headers=headers, timeout=60)
    data = resp.json()
    assistant_msg = data["choices"][0]["message"]
    messages.append(assistant_msg)

    tool_calls = assistant_msg.get("tool_calls")
    if not tool_calls:
        print("AI 最终回答：\n", assistant_msg["content"])
        break

    for call in tool_calls:
        name = call["function"]["name"]
        if name == "list_files":
            result = list_files()
        elif name == "read_file":
            args = json.loads(call["function"]["arguments"])
            result = read_file(args["filename"])
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
