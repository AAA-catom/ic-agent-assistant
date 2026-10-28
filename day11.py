# day11.py：ReAct 循环 —— AI 连续调用多个工具，直到能回答
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


# 一个问题需要两个工具：先算加法，再查时间
messages = [{"role": "user", "content": "先算 3 加 5 等于几，然后告诉我现在是几点"}]
body = {"model": "deepseek-chat", "messages": messages, "tools": tools}


# 核心：while 循环 —— 一直转到 AI 不再喊工具为止
while True:
    # 发请求
    resp = requests.post(URL, json=body, headers=headers, timeout=60)
    data = resp.json()
    assistant_msg = data["choices"][0]["message"]
    messages.append(assistant_msg)

    # 关键判断：AI 这次还有没有喊工具？
    tool_calls = assistant_msg.get("tool_calls")
    if not tool_calls:
        # 没喊 = 它已经答完了，打印最终答案，结束循环
        print("AI 最终回答：", assistant_msg["content"])
        break

    # 喊了 = 执行它要的所有工具
    for call in tool_calls:
        name = call["function"]["name"]
        if name == "get_current_time":
            result = get_current_time()
        elif name == "add":
            args = json.loads(call["function"]["arguments"])
            result = str(add(args["a"], args["b"]))
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})

    # 回到 while 开头，带着工具结果再发一次
