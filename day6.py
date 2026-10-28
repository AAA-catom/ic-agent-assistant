# day6.py：把「发给 AI 检查」打包成函数 check_code()
import requests
import os
from dotenv import load_dotenv
import sys
import glob
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


# 函数：输入一段代码，返回 AI 的检查结果
def check_code(code):
    messages = [
        {"role": "system", "content": "你是一个 Verilog 语法检查器，检查语法错误并给出修改建议"},
        {"role": "user", "content": code}
    ]
    body = {"model": "deepseek-chat", "messages": messages}
    resp = requests.post(URL, json=body, headers=headers, timeout=60)
    data = resp.json()
    reply = data["choices"][0]["message"]["content"]
    return reply   # 关键：把 AI 的回答「交出来」


# 主流程：for 循环批量调用 check_code()
files = glob.glob("*.v")  # 批量找出当前目录下所有 .v 文件  

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        code = f.read()

    result = check_code(code)   # 调用函数，接住返回结果

    print("=" * 20)
    print(file, "的检查结果：")
    print(result)
