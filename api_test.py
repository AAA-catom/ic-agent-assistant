# 白纸测试：凭理解写一个「让 DeepSeek 回答 1+1 等于几」的脚本
import requests
import os
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
messages = [{"role":"system","content":"你是一个数学老师，回答要简短"}]
body = {"model":"deepseek-chat","messages":messages}
headers = {"Authorization":f"Bearer {API_KEY}", "Content-Type":"application/json"}
print("开始聊天，使用quit退出")
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
