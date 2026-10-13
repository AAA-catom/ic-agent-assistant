# -*- coding: utf-8 -*-
# 第一个正式 API 调用：让 DeepSeek 回话（密钥从 .env 读，不硬编码在代码里）
import requests
import sys
import os
from dotenv import load_dotenv

# 修中文 Windows 的 GBK 乱码问题
sys.stdout.reconfigure(encoding='utf-8')

# ① 从 .env 文件里读密钥（不写死在代码里，.env 已经被 .gitignore 忽略，不会上传）
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ② 打给谁：DeepSeek 的接口地址
URL = "https://api.deepseek.com/chat/completions"

# ③ 你要说的话（问题，可以自己改）
messages = [
    {"role": "user", "content": "你好，用一句话介绍你自己"}
]

# ④ 电话内容：告诉它用哪个模型、给什么参数
body = {
    "model": "deepseek-chat",   # 模型名
    "messages": messages,       # 上面的问题
    "temperature": 0.7,         # 回答随机程度（0=死板，1=放飞）
}

# ⑤ 证明你是谁：把 key 放进请求头
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# ⑥ 拨打电话，拿到回答
resp = requests.post(URL, json=body, headers=headers, timeout=60)

# ⑦ 把回答打印出来
data = resp.json()
print(data["choices"][0]["message"]["content"])
