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
# 进制转换
num = 255
print(f"十进制: {num}, 十六进制: {num:x}, 二进制: {num:b}")

# 格式化输出 2: format() 方法
name = "Bob"
age = 30
score = 95.5

# 按顺序填充
print("姓名: {}, 年龄: {}".format(name, age))

# 指定索引
print("{1}的年龄是{0}".format(age, name))  # Bob的年龄是30

# 使用关键字参数
print("姓名: {n}, 年龄: {a}".format(n=name, a=age))

# 数字格式化
print("分数: {:.2f}".format(score))  # 保留2位小数

# 对齐和填充
print("{:<10} {:>10}".format(name, age))  # 左对齐和右对齐
