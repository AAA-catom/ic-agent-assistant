# day14.py：RAG 第一步 —— 切片（把手册撕成一小段一小段）
import sys
sys.stdout.reconfigure(encoding='utf-8')


def split_manual(text, size=150):
    """把一大段文字按 size 个字切成小段，返回一个列表"""
    chunks = []
    for i in range(0, len(text), size):   # 从 0 开始，每次跳 150 步
        chunks.append(text[i:i+size])     # 取 i 到 i+150 这一段
    return chunks


# 读手册（这步你已经会了，day13 的 read_file 就是干这个的）
with open("manual.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 切！
chunks = split_manual(text)
print("手册一共", len(text), "个字，切成了", len(chunks), "段\n")

for i in range(len(chunks)):
    print("===== 第", i, "段 =====")
    print(chunks[i])
    print()
