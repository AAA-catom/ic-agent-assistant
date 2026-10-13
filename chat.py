# -*- coding: utf-8 -*-
# 交互式聊天：在终端里和 AI 连续对话，输入 quit 退出（带错误处理）
import requests
import sys
import os
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"

messages = [
    {"role": "system", "content": "你是一个芯片设计助手，回答要简短"}
]

print("和 AI 聊天中，输入 quit 退出")
while True:
    user_input = input("你：")
    if user_input == "quit":
        break

    messages.append({"role": "user", "content": user_input})

    body = {"model": "deepseek-chat", "messages": messages, "temperature": 0.7}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    # 关键：用 try-except 包住 API 调用，出错不崩，打印原因继续聊
    try:
        resp = requests.post(URL, json=body, headers=headers, timeout=60)
        if resp.status_code == 200:                     # 200 = 成功
            data = resp.json()
            reply = data["choices"][0]["message"]["content"]
        else:                                            # 非 200 = 失败（如限流 429）
            reply = f"[出错：状态码 {resp.status_code}]"
    except Exception as e:                               # 网络断、超时等异常
        reply = f"[请求失败：{e}]"

    messages.append({"role": "assistant", "content": reply})
    print("AI：", reply)
