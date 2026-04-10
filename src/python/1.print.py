print("Hello World")  # Hello World
print(100)  # 100
print(3.14)  # 3.14
print(True)  # True

name = "Alice"
age = 25
score = 95.567
print("姓名:", name, "年龄:", age)  # 姓名: Alice 年龄: 25

# 可以混合不同类型
print("数字:", 42, "布尔:", True, "浮点:", 3.14)

# 分隔符
# 使用逗号分隔
print("A", "B", "C", sep=",")

# end - 结束符
print("Hello", end="!")  # Hello

# sep 和 end 可以同时使用
print("姓名", "年龄", "城市", sep=" | ", end="\n---\n")

# 输出到文件,
with open("output.txt", "w", encoding="utf-8") as f:
    print("这是写入文件的内容", file=f)
    print("第二行内容", file=f)
# with open(...) as f 是安全管理文件开关的语法糖，等价于：
# 运行
# f = open("output.txt", "w", encoding="utf-8")
# try:
#     # 你的代码
# finally:
#     f.close()  # 无论如何都会关闭文件

# 格式化输出 1: f-string
# : - 格式说明符开始
# .2 - 精度（保留2位小数）
# f - 格式类型（浮点数）
# < - 左对齐，> - 右对齐，^ - 居中
# x - 十六进制，b - 二进制，o - 八进制

print(f"name: {name}, age: {age}")  # name: Alice, age: 25
# 精度
print(f"score: {score:.2f}")  # score: 95.57
print(f"score: {score:.1f}")  # score: 95.6
# 对齐
print(f"name: {name:<10} age: {age:>5}")  # name: Alice      age:    25
print(f"name: {name:^10} age: {age:^5}")  # name:   Alice    age:  25
# 进制
print(f"score in hex: {score:x}")  # score in hex: 5f
print(f"score in binary: {score:b}")  # score in binary: 1011111
print(f"score in octal: {score:o}")  # score in octal: 137

# 格式化输出 2: format() 方法
print("name: {}, age: {}".format(name, age))  # name: Alice, age: 25
print("score: {:.2f}".format(score))  # score: 95.57
print("name: {:<10} age: {:>5}".format(name, age))  # name: Alice      age:    25
print("score in hex: {:x}".format(score))  # score in hex: 5f
print("score in binary: {:b}".format(score))  # score in binary: 1011111
print("score in octal: {:o}".format(score))  # score in octal: 137
