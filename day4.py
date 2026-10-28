# day4.py：批量 Verilog 语法检查器（for 循环 + 读文件 + API 调用）
import requests
import os
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

files = ["test.v", "test2.v"]

for file in files:
    # 零件1：读文件内容
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()

    # 零件2：发给 AI 检查
    messages = [
        {"role": "system", "content": "你是一个 Verilog 语法检查器，检查语法错误并给出修改建议"},
        {"role": "user", "content": code}
    ]
    body = {"model": "deepseek-chat", "messages": messages}
    resp = requests.post(URL, json=body, headers=headers, timeout=60)
    data = resp.json()
    reply = data["choices"][0]["message"]["content"]

    # 零件3：打印结果
    print("=" * 20)
    print(file, "的检查结果：")
    print(reply)
