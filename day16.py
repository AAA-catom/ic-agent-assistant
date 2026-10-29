# day16.py：RAG 第三步 —— 查（提问，从向量库里找出最相关的几段）
import sys
sys.stdout.reconfigure(encoding='utf-8')
import chromadb
from embedding import SiliconFlowEmbedding

# 和 day15 一样：用同一个 embedding 函数、打开同一个向量库
ef = SiliconFlowEmbedding()
client = chromadb.PersistentClient(path="./chip_db")
collection = client.get_or_create_collection(
    name="chip_manual",
    embedding_function=ef,
)

question = "芯片的复位引脚 RST 应该怎么用？"

# 查！chromadb 自动把问题算成指纹，然后找指纹最像的段
results = collection.query(
    query_texts=[question],   # 要查的问题
    n_results=2,              # 只要最像的 2 段
)

# results["documents"][0] 就是返回的 2 段原文
docs = results["documents"][0]
print("你问的是：", question)
print()
for i in range(len(docs)):
    print("===== 最相关的第", i+1, "段 =====")
    print(docs[i])
    print()
