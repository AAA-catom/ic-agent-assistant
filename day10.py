# day10.py：多工具 —— AI 自己决定用哪个工具
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


# 工具1：查时间
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 工具2：算加法
def add(a, b):
    return a + b


# 说明书里放两个工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的时间",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个整数相加",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个数"},
                    "b": {"type": "integer", "description": "第二个数"}
                },
                "required": ["a", "b"]
            }
        }
    }
]


messages = [{"role": "user", "content": "现在几点了"}]
body = {"model": "deepseek-chat", "messages": messages, "tools": tools}

# 第一次请求：AI 喊工具
resp = requests.post(URL, json=body, headers=headers, timeout=60)
data = resp.json()
assistant_msg = data["choices"][0]["message"]
messages.append(assistant_msg)

# 分派：AI 要哪个工具，就执行哪个（if / elif）
for call in assistant_msg["tool_calls"]:
    name = call["function"]["name"]
    if name == "get_current_time":
        result = get_current_time()
    elif name == "add":
        args = json.loads(call["function"]["arguments"])
        result = str(add(args["a"], args["b"]))

    messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})

# 第二次请求：AI 拿到结果回答
resp = requests.post(URL, json=body, headers=headers, timeout=60)
data = resp.json()
print("AI 最终回答：", data["choices"][0]["message"]["content"])
