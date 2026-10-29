# day17.py：RAG 最后一步 —— 生成（查资料 + 喂给 AI 回答）
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import requests
from dotenv import load_dotenv
import chromadb
from embedding import SiliconFlowEmbedding


# ===== 第 1 部分：查（就是 day16 的逻辑）=====
ef = SiliconFlowEmbedding()
client = chromadb.PersistentClient(path="./chip_db")
collection = client.get_or_create_collection(
    name="chip_manual",
    embedding_function=ef,
)

question = "XC100 支持哪些通信协议？"

results = collection.query(
    query_texts=[question],
    n_results=4,
)
docs = results["documents"][0]      # 找到的 4 段原文

# 把 4 段原文用空行粘成一大段"资料"
context = "\n\n".join(docs)


# ===== 第 2 部分：生成（就是 day7-13 的调 API）=====
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# 关键：把资料和问题一起塞进 prompt，并命令 AI 只能照资料回答
messages = [
    {"role": "system", "content": "你是芯片手册问答助手。只能根据下面提供的资料回答，资料里没有的就说不知道，不要瞎编。回 答时要注明信息来源（资料里每段开头的小节名）。"},
    {"role": "user", "content": f"资料：\n{context}\n\n问题：{question}"},
]

resp = requests.post(URL, json={"model": "deepseek-chat", "messages": messages}, headers=headers, timeout=60)
data = resp.json()
answer = data["choices"][0]["message"]["content"]

print("问题：", question)
print()
print("AI 回答：")
print(answer)
