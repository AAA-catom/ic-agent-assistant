import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import requests
from dotenv import load_dotenv
import chromadb
from embedding import SiliconFlowEmbedding
import json
import glob
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


ef = SiliconFlowEmbedding()
client = chromadb.PersistentClient(path="./chip_db")
collection = client.get_or_create_collection(
    name="chip_manual",
    embedding_function=ef,
)


def list_files():
    files = glob.glob("*.v")
    return "\n".join(files)

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def search_manual(question):
    results = collection.query(query_texts=[question], n_results=2)
    docs = results["documents"][0]
    return "\n\n".join(docs)

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "列出当前目录下所有 .v 文件",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取一个文件的内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "要读取的文件名"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_manual",
            "description": "在芯片手册里查资料，输入一个问题，返回相关的段落",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "要搜索的问题"}
                },
                "required": ["question"]
            }
        }
    }
]

messages = [
    {"role": "system", "content": "你是电赛助手，能查芯片手册、能读代码文件"},
    {"role": "user", "content": "帮我检查项目里的 .v 文件语法错误，再查一下手册里复位引脚 RST 怎么用  "},
]
body = {"model": "deepseek-chat", "messages": messages, "tools": tools}


while True:
    resp = requests.post(URL, json=body, headers=headers, timeout=60)
    data = resp.json()
    assistant_msg = data["choices"][0]["message"]
    messages.append(assistant_msg)

    tool_calls = assistant_msg.get("tool_calls")
    if not tool_calls:
        print("AI 最终回答：\n", assistant_msg["content"])
        break

    for call in tool_calls:
        name = call["function"]["name"]
        if name == "list_files":
            result = list_files()
        elif name == "read_file":
            args = json.loads(call["function"]["arguments"])
            result = read_file(args["filename"])
        elif name == "search_manual":
            args = json.loads(call["function"]["arguments"])
            result = search_manual(args["question"])    
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
