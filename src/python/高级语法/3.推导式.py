# [表达式 for 变量 in 可迭代对象 (可选的if条件)]
# 传统方式
squares = []
for x in range(5):
    squares.append(x**2)
print(squares)  # [0, 1, 4, 9, 16]

squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]

# 带条件的列表推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]

# 多个条件
numbers = [x for x in range(20) if x % 2 == 0 if x % 3 == 0]

# 条件表达式（三元运算符）
results = [x if x % 2 == 0 else "odd" for x in range(5)]
print(results)

# 字典推导式:  {键表达式: 值表达式 for 变量 in 可迭代对象 (可选的if条件)}

d = {x: x**2 for x in range(5)}
print(d)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 从分数字典中只保留及格的学生
scores = {"Alice": 85, "Bob": 58, "Charlie": 71, "David": 49}
passed = {name: score for name, score in scores.items() if score > 60}
print(passed)  # {'Alice': 85, 'Charlie': 71}

# 交换字典中的键和值
fruit_colors = {"apple": "red", "banana": "yellow", "grape": "purple"}
color_fruits = {color: fruits for fruits, color in fruit_colors.items()}
print(color_fruits)

# 将不及格成绩标记为"不及格"
scores = {"Alice": 85, "Bob": 58, "Charlie": 71, "David": 49}
result = {name: (score if score >= 60 else "不及格") for name, score in scores.items()}
print(result)

# 集合推导式（集合去重）
# 创建唯一平方数的集合
squares_set = {x**2 for x in range(-5, 6)}
print(squares_set)  # {0, 1, 4, 9, 16, 25}

# 从列表去重
words = ["hello", "world", "hello", "python", "world"]
unique_words = {word for word in words}
print(unique_words)  # {'hello', 'world', 'python'}

# 带条件的集合推导式
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0, 64, 4, 36, 16}


# 内存效率对比
import sys

n = 100000
# 列表推导式 - 立即创建所有元素
list_comp = [x**2 for x in range(n)]
# 生成器表达式 - 惰性计算
gen_expr = (x**2 for x in range(n))

print(f"列表推导式内存: {sys.getsizeof(list_comp)} 字节")  # 800984 字节
print(f"生成器表达式内存: {sys.getsizeof(gen_expr)} 字节")  # 200 字节

# 多层嵌套推导式
three_d = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
flattened_3d = [num for matrix in three_d for row in matrix for num in row]
print(flattened_3d)

nested_dict = {
    f"group_{i}": {f"item_{j}": i * j for j in range(1, 4)} for i in range(1, 4)
}
print(nested_dict)


# .文件处理
def process_file_data(filename):
    """处理文件数据"""
    with open(filename, "r", encoding="utf-8") as file:
        # 读取非空行并去除空白
        lines = [line.strip() for line in file if line.strip()]
        # 筛选包含关键词的行
        keyword_lines = [line for line in lines if "error" in line.lower()]
        # 创建行号字典
        line_dict = {i: line for i, line in enumerate(lines, 1)}
        return lines, keyword_lines, line_dict
