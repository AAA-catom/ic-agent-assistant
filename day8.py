# day8.py：Function Calling 完整流程（AI 点菜 → 你做饭 → 端回去 → AI 回答）
import requests
import os
import sys
import datetime
from dotenv import load_dotenv
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


# 真实的函数：返回当前时间
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 告诉 AI 有哪些工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的时间",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]


messages = [{"role": "user", "content": "现在几点了？"}]
body = {"model": "deepseek-chat", "messages": messages, "tools": tools}

# ① 第一次请求：AI 会「喊」要调用工具
resp = requests.post(URL, json=body, headers=headers, timeout=60)
data = resp.json()
assistant_msg = data["choices"][0]["message"]
messages.append(assistant_msg)   # 把 AI 的 tool_calls 记进历史

# ② 你做饭：AI 要哪个工具，就真的执行哪个
for call in assistant_msg["tool_calls"]:
    name = call["function"]["name"]
    if name == "get_current_time":
        result = get_current_time()   # 真正运行函数，拿到真实时间

    # ③ 端回去：把结果以 role="tool" 塞回历史
    messages.append({
        "role": "tool",
        "tool_call_id": call["id"],
        "content": result
    })

# ④ 第二次请求：AI 拿到结果，给出最终回答
resp = requests.post(URL, json=body, headers=headers, timeout=60)
data = resp.json()
print("AI 最终回答：", data["choices"][0]["message"]["content"])
