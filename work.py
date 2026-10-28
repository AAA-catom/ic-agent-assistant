# 文件读写练习
# 写文件：w = write
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("hello agent")

# 读文件：r = read
with open("test.txt", "r", encoding="utf-8") as f:
    print(f.read())
