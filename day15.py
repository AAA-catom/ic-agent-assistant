# day15.py：RAG 第二步 —— 存（把切好的段算指纹，存进向量库）
import sys
sys.stdout.reconfigure(encoding='utf-8')
import chromadb
from embedding import SiliconFlowEmbedding


# 1. 准备 embedding 函数：负责"把文字变成 384 个数字的指纹"
ef = SiliconFlowEmbedding()

# 2. 建一个向量库（存到本地 chip_db 文件夹，下次打开还在）
client = chromadb.PersistentClient(path="./chip_db")
collection = client.get_or_create_collection(
    name="chip_manual",
    embedding_function=ef,   # 告诉它：用这个函数算指纹
)


# 3. 切手册（和第 1 步一样，这里再放一遍）
def split_by_paragraph(text):
    """把一大段文字按段落切成小段，返回一个列表"""
    chunks = text.split("\n\n")  # 按两个换行符切分
    return chunks


with open("manual.txt", "r", encoding="utf-8") as f:
    text = f.read()
chunks = split_by_paragraph(text)


# 4. 入库：chromadb 会自动给每段算指纹，再存起来
ids = []
for i in range(len(chunks)):
    ids.append(f"chunk_{i}")   # 给每段一个编号：chunk_0、chunk_1、chunk_2…

collection.upsert(
    ids=ids,           # 每段的编号
    documents=chunks,  # 每段的原文
)

print("入库完成！向量库里现在有", collection.count(), "段")
