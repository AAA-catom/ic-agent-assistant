# -*- coding: utf-8 -*-
# 多轮对话演示：让 AI "记住"之前说的话
import requests
import sys
import os
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"

# 关键：messages 是「历史记录列表」，按时间顺序排。
# 我们把前几轮的对话全塞进去，AI 就能"看到"历史 = 记住了。
messages = [
    {"role": "system", "content": "你是一个芯片设计助手，回答要简短"},
    {"role": "user", "content": "记住，我最喜欢的芯片是 FPGA"},
    {"role": "assistant", "content": "好的，我记住了，你最喜欢 FPGA。"},
    {"role": "user", "content": "那我最喜欢的芯片是什么？"},
]

body = {
    "model": "deepseek-chat",
    "messages": messages,
    "temperature": 0.7,
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

resp = requests.post(URL, json=body, headers=headers, timeout=60)
data = resp.json()
print(data["choices"][0]["message"]["content"])
