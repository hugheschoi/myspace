"""
1.什么是 while 循环？
while 循环会重复执行一段代码，直到条件不再满足为止。
"""

# 示例1：基础用法
count = 1
while count <= 5:
    print(f"这是第 {count} 次循环")
    count += 1  # 重要：更新计数器，避免无限循环

# 输出：
# 这是第 1 次循环
# 这是第 2 次循环
# 这是第 3 次循环
# 这是第 4 次循环
# 这是第 5 次循环

"""
4.while 循环的关键要素
4.1.条件表达式
4.2.循环体
4.3.条件更新
"""

# 示例2：使用 while 循环计算1到10的和
total = 0
count = 1
while count <= 10:
    total += count
    count += 1
print(f"1到10的和是: {total}")

"""
5.常见应用场景
"""
# 5.1.计数器循环
count = 0
while count < 5:
    print(f"这是第 {count} 次循环")
    count += 1

# 5.2.用户输入验证
password = "123456"
while True:
    input_password = input("请输入密码: ")
    if input_password == password:
        print("密码正确")
        break
    else:
        print("密码错误")

# 5.3.处理列表数据
items = ["apple", "banana", "cherry"]
index = 0
while index < len(items):
    print(f"这是第 {index} 个水果: {items[index]}")
    index += 1

# 6. 控制循环的特殊语句
# 6.1.break 语句
# 找到第一个能被7整除的数
num = 1
while num <= 20:
    if num % 7 == 0:
        print(f"找到第一个能被7整除的数：{num}")
        break
    num += 1
# 6.2.continue 语句
# 跳过能被3整除的数
# 打印1-10中的奇数
num = 0
while num < 10:
    num += 1
    if num % 2 == 0:
        continue  # 如果是偶数，跳过本次循环的剩余部分
    print(num)
# 6.3.pass 语句
# 6.4.else 语句
# 当循环正常结束时，执行else语句
num = 1
while num <= 5:
    print(num)
    num += 1
else:
    print("循环结束")
# 6.5.finally 语句
# 6.6.with 语句
# 6.7.yield 语句
# 6.8.async for 语句
# 6.9.async with 语句
# 6.10.async for 语句
# 6.11.async with 语句

# 猜数字游戏
import random

secret_number = random.randint(1, 100)
attempts = 0
max_attempts = 7

print("猜数字游戏！我想了一个1-100之间的数字")

while attempts < max_attempts:
    guess = int(input("请输入你的猜测："))
    attempts += 1
    
    if guess < secret_number:
        print("太小了！")
    elif guess > secret_number:
        print("太大了！")
    else:
        print(f"恭喜！你在第 {attempts} 次猜对了！")
        break
else:
    print(f"游戏结束！正确答案是 {secret_number}")

# 7.2.示例2：菜单系统
def show_menu():
    print("\n=== 菜单系统 ===")
    print("1. 查看信息")
    print("2. 修改信息")
    print("3. 退出系统")

while True:
    show_menu()
    choice = input("请选择操作（1-3）：")
    
    if choice == "1":
        print("显示信息...")
    elif choice == "2":
        print("修改信息...")
    elif choice == "3":
        print("感谢使用，再见！")
        break
    else:
        print("无效选择，请重新输入！")

"""
8.注意事项
避免无限循环：确保循环条件最终会变为 False正确缩进：循环体内的所有代码必须正确缩进
更新条件变量：在循环体内更新影响条件的变量
使用break谨慎：过多的break语句可能使代码难以理解
"""

"""
9.while vs for 循环
while循环：当不确定循环次数时使用
for循环：当知道要遍历序列或明确循环次数时使用
"""
# while循环 - 不确定次数
import random
target = random.randint(1, 5)
guess = 0
while guess != target:
    guess = int(input("猜数字："))
else:
    print("猜对了")
# for循环 - 确定次数
for i in range(5):
    print(f"第 {i+1} 次循环")