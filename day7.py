# day7.py：Function Calling 第一步 —— 看 AI 怎么「喊」要调用函数
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


# 1. 真实的函数：返回当前时间
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 2. 告诉 AI「我有这个工具」（tools 描述）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# 3. 问 AI 一个它自己答不了、必须用工具的问题
messages = [{"role": "user", "content": "现在几点了？"}]
body = {"model": "deepseek-chat", "messages": messages, "tools": tools}

resp = requests.post(URL, json=body, headers=headers, timeout=60)
data = resp.json()

# 4. 打印 AI 返回的完整信息，看它有没有「喊」要调用工具
print(json.dumps(data["choices"][0]["message"], indent=2, ensure_ascii=False))
