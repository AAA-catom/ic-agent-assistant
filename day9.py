# day9.py：带参数的工具 —— 让 AI 当计算器
import requests
import os
import sys
import json
from dotenv import load_dotenv
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


# 函数：两个数相加
def add(a, b):
    return a + b


# 告诉 AI 这个工具（注意 parameters 里把参数写清楚）
tools = [
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


messages = [{"role": "user", "content": "帮我算一下 3 加 5 等于几"}]
body = {"model": "deepseek-chat", "messages": messages, "tools": tools}

# ① 第一次请求：AI 喊要调 add，并给出参数
resp = requests.post(URL, json=body, headers=headers, timeout=60)
data = resp.json()
assistant_msg = data["choices"][0]["message"]
messages.append(assistant_msg)

# ② 你做饭：解析参数，调用函数
for call in assistant_msg["tool_calls"]:
    if call["function"]["name"] == "add":
        args = json.loads(call["function"]["arguments"])  # 参数字符串 → 字典
        result = add(args["a"], args["b"])                # 用真实参数调用函数
        result = str(result)                              # 转成字符串再端回去

    messages.append({
        "role": "tool",
        "tool_call_id": call["id"],
        "content": result
    })

# ③ 第二次请求：AI 拿到结果回答
resp = requests.post(URL, json=body, headers=headers, timeout=60)
data = resp.json()
print("AI 最终回答：", data["choices"][0]["message"]["content"])
