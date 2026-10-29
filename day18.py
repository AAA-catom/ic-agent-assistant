import sys
sys.stdout.reconfigure(encoding='utf-8')



def split_by_paragraph(text):
    """把一大段文字按段落切成小段，返回一个列表"""
    chunks = text.split("\n\n")  # 按两个换行符切分
    return chunks   



with open("manual.txt", "r", encoding="utf-8") as f:
    text = f.read()



chunks = split_by_paragraph(text)
print("手册一共", len(text), "个字，切成了", len(chunks), "段\n")



for i in range(len(chunks)):
    print("===== 第", i, "段 =====")
    print(chunks[i])
    print()















