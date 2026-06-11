# 计算平均分数
scores = [85, 92, 78, 96, 88]
total = 0

for score in scores:
    total += score

average = total / len(scores)
print(f"平均分: {average:.2f}")  # 平均分: 87.80

# 统计句子中的单词长度
sentence = "Python is a powerful programming language"
words = sentence.split()

word_lengths = {}
for word in words:
    word_lengths[word] = len(word)
print(word_lengths)

# 读取文件中的每一行（假设文件存在）
try:
    with open("example.txt", "r") as file:
        for line_num, line in enumerate(file, 1):
            print(f"第{line_num}行: {line.strip()}")
except FileNotFoundError:
    print("文件不存在")

# 不要在循环中修改正在遍历的列表
# 错误示范
numbers = [2, 4, 6, 8]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # 危险！会跳过元素
print(numbers)  # 实际输出 [4, 8]，并非全部删除，6被跳过了

# 正确做法：创建副本或使用列表推导式
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
numbers = [num for num in numbers if num % 2 != 0]
print(numbers)  # [1, 3, 5, 7]

# 使用 zip() 同时遍历多个列表
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f"{name}的分数是: {score}")
