# Day2 白纸测试：凭记忆写下面 7 段代码（不要看 day1.py）
print("Hello,Agent!")

num = 10
c = "gugugaga"
print(num, c)

a = 10
b = 3
print(a+b, a%b)

input_str = input("请输入一个内容：")
print("你输入的内容是：", input_str)

import json
info = {"module_name": "uart", "port_num": 8, "is_valid": True}
print(json.dumps(info, indent=2))

with open("test.txt", "w", encoding="utf-8") as f:
    f.write("module test;\nendmodule")
with open("test.txt", "r", encoding="utf-8") as f:
    print(f.read())

try:
    num = int("abc")
except Exception as e:
    print("捕获错误：", e)  

score=90
if score>=90:
    print("优秀")
else:
    print("继续努力")

s="hello,agent"
print(s[0])
print(s[0:5])
print(s[-5:])