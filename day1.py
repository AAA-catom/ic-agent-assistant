# Day1 练习代码写在这里（下面开始手写你的练习）
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