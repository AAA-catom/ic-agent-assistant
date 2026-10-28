# Day3：for 循环
# 列表：装几个文件名
files = ["work.py", "test.py", "main.py"]

# for 循环：每次从列表拿一个，放进变量 file，然后打印
for file in files:
    print(file)

files=["test.v", "test2.v"]
for file in files:
    with open(file,"r",encoding="utf-8") as f:
        print("=====",file,"=====")
        print(f.read())