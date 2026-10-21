# Verilog 语法检查器：读 .v 文件，让 AI 检查语法错误
import requests
import os
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
with open("test.v", "r", encoding="utf-8") as f:
    verilog_code = f.read()
messages = [{"role":"system","content":"你是一个 Verilog 语法检查器，检查代码语法错误并给出修改建议"}, {"role":"user","content":verilog_code}]
body = {"model":"deepseek-chat","messages":messages}
headers = {"Authorization":f"Bearer {API_KEY}", "Content-Type":"application/json"}
print("Verilog 语法检查器，输入 quit 退出")
while True:
    user_input = input("用户：")
    if user_input.lower() == "quit":
        break
    messages.append({"role":"user","content":user_input})
    body["messages"] = messages
    try:
        resp = requests.post(URL,json=body,headers=headers)
        if resp.status_code ==200:
            data = resp.json()
            reply=data["choices"][0]["message"]["content"]
        else:
            reply=f"请求失败，状态码：{resp.status_code}"
    except Exception as e:
        reply=f"请求异常：{e}"
    messages.append({"role":"assistant","content":reply})
    print("AI：",reply)