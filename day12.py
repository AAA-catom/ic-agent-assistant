# day12.py：给 Agent 装「真实」工具 —— read_file（读文件）
import requests
import os
import sys
import json
import datetime
from dotenv import load_dotenv
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


# 工具1：读文件（真实有用的工具）
def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


# 工具2：查时间（保留）
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取一个文件的内容，返回文件里的文字",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "要读取的文件名"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的时间",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]


messages = [{"role": "user", "content": "帮我看看 test.v 文件里写了什么"}]
body = {"model": "deepseek-chat", "messages": messages, "tools": tools}


while True:
    resp = requests.post(URL, json=body, headers=headers, timeout=60)
    data = resp.json()
    assistant_msg = data["choices"][0]["message"]
    messages.append(assistant_msg)

    tool_calls = assistant_msg.get("tool_calls")
    if not tool_calls:
        print("AI 最终回答：", assistant_msg["content"])
        break

    for call in tool_calls:
        name = call["function"]["name"]
        if name == "read_file":
            args = json.loads(call["function"]["arguments"])
            result = read_file(args["filename"])   # 真的打开 test.v 读内容
        elif name == "get_current_time":
            result = get_current_time()
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
