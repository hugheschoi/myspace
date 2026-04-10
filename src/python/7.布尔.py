# 1.布尔类型的基本概念
# 定义一个表示晴天的布尔变量
is_sunny = True
# 定义一个表示下雨的布尔变量
is_raining = False

# 输出is_sunny的值和类型
print(f"is_sunny: {is_sunny}, 类型: {type(is_sunny)}")  # <class 'bool'>
# 输出is_raining的值和类型
print(f"is_raining: {is_raining}, 类型: {type(is_raining)}")  # <class 'bool'>

# 输出True与1是否相等
print(f"True == 1: {True == 1}")  # True
# 输出False与0是否相等
print(f"False == 0: {False == 0}")  # True
# 输出True加True的结果
print(f"True + True: {True + True}")  # 2
# 输出True乘以10的结果
print(f"True * 10: {True * 10}")  # 10
# 输出False乘以10的结果
print(f"False * 10: {False * 10}")  # 0

# 2.2. 布尔运算
# 2.1.逻辑运算符
# 逻辑运算
a, b = True, False

print("逻辑运算:")
print(f"{a} and {b} = {a and b}")  # False
print(f"{a} or {b} = {a or b}")  # True
print(f"not {a} = {not a}")  # False
print(f"not {b} = {not b}")  # True

# 真值表
print("\n真值表:")
print("AND运算:")
print(f"True and True = {True and True}")  # True
print(f"True and False = {True and False}")  # False
print(f"False and True = {False and True}")  # False
print(f"False and False = {False and False}")  # False

print("\nOR运算:")
print(f"True or True = {True or True}")  # True
print(f"True or False = {True or False}")  # True
print(f"False or True = {False or True}")  # True
print(f"False or False = {False or False}")  # False

print("\nNOT运算:")
print(f"not True = {not True}")  # False
print(f"not False = {not False}")  # True


# 2.2.逻辑运算的短路特性
def expensive_operation():
    print("执行了耗时操作!")
    return True


print("短路特性:")
# and 短路：第一个为False时，不计算第二个
result1 = False and expensive_operation()  # 不会打印
print(f"False and 耗时操作: {result1}")

# or 短路：第一个为True时，不计算第二个
result2 = True or expensive_operation()  # 不会打印
print(f"True or 耗时操作: {result2}")

# 会执行的情况
print("会执行耗时操作的情况:")
result3 = True and expensive_operation()  # 会打印
print(f"True and 耗时操作: {result3}")
result4 = False or expensive_operation()  # 会打印
print(f"False or 耗时操作: {result4}")

# 3.3. 比较运算
print("\n比较运算:")
x, y = 10, 20
print(f"{x} == {y}: {x == y}")  # False
print(f"{x} != {y}: {x != y}")  # True
print(f"{x} > {y}: {x > y}")  # False
print(f"{x} < {y}: {x < y}")  # True
print(f"{x} >= {y}: {x >= y}")  # False
print(f"{x} <= {y}: {x <= y}")  # True
# 字符串比较
str1, str2 = "apple", "banana"
print(f"'apple' == 'apple': {'apple' == 'apple'}")  # True
print(f"'apple' == 'banana': {'apple' == 'banana'}")  # False
print(f"'apple' < 'banana': {'apple' < 'banana'}")  # True (按字典序)
# 链式比较
num = 15
print(f"10 < {num} < 20: {10 < num < 20}")  # True
print(f"10 < {num} < 15: {10 < num < 15}")  # False
print(f"15 < {num} < 20: {15 < num < 20}")  # False

# 4.4. 真值(Truthy)和假值(Falsy)
# 在Python中，很多非布尔值在布尔上下文中会被当作True或False。

# Python中的假值
falsy_values = [
    False,  # 布尔假
    None,  # 空值
    0,  # 整数零
    0.0,  # 浮点数零
    0j,  # 复数零
    "",  # 空字符串
    [],  # 空列表
    (),  # 空元组
    {},  # 空字典
    set(),  # 空集合
]
for value in falsy_values:
    if value:
        print(f"{value!r:10}  -> True")
    else:
        print(f"{value!r:10} -> False")
# 4.2.真值(Truthy)示例
# 真值示例
truthy_values = [
    True,  # 布尔真
    1,  # 非零数字
    0.1,  # 非零浮点数
    "hello",  # 非空字符串
    [1, 2, 3],  # 非空列表
    (1, 2),  # 非空元组
    {"key": "value"},  # 非空字典
    {1, 2, 3},  # 非空集合
]
for value in truthy_values:
    if value:
        print(f"{value!r:20} -> True")
    else:
        print(f"{value!r:20} -> False")

# 5.5. 布尔上下文中的应用
# 5.1.条件语句
age = 20
has_license = True
has_car = False

# if 语句
if age >= 18:
    print("已成年")

# if-else 语句
if has_license and has_car:
    print("可以开车")
else:
    print("不能开车")

# if-elif-else 语句
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"
print(f"分数 {score} -> 等级 {grade}")

# 5.2.循环控制
# while 循环
count = 0
while count < 5:
    print(f"while循环: count = {count}")
    count += 1

# break 和 continue
print("\nbreak和continue演示:")
for i in range(10):
    if i == 2:
        continue  # 跳过本次循环
    if i == 7:
        break  # 终止循环
    print(f"i = {i}")

# 6.6. 布尔函数和操作
# 6.1.bool() 函数
# bool() 函数用于将一个值转换为布尔类型（True 或 False）。在 Python 中，以下情况会被视为 False：


# 数值类型的 0（如 0, 0.0, 0j）
# 空序列或空集合（如 "", [], (), {}）
# None
# 自定义对象的 bool 或 len 返回 False 或 0
# 其他情况都被视为 True。
# 定义一个函数用于演示bool()函数的用法
def bool_function():
    # 定义一个包含多种类型测试值的列表
    test_values = [0, 1, -1, 0.0, 0.1, "", "hello", [], [1], None]

    # 打印测试标题
    print("bool()函数测试:")
    # 遍历每个测试值
    for value in test_values:
        # 打印每个值及其对应的bool()结果
        print(f"bool({value!r:10}) = {bool(value)}")


# 调用上面定义的函数
bool_function()


# 定义一个银行账户类，用于演示自定义对象的布尔值
class BankAccount:
    # 初始化方法，设置账户余额
    def __init__(self, balance):
        self.balance = balance

    # 定义__bool__方法，余额大于0时对象为True，否则为False
    def __bool__(self):
        return self.balance > 0

    # 定义__str__方法，返回账户余额的字符串表示
    def __str__(self):
        return f"BankAccount(余额: ${self.balance})"


# 打印自定义对象布尔值的测试标题
print("\n自定义对象布尔值:")
# 创建一个余额为100的账户对象
account1 = BankAccount(100)
# 创建一个余额为0的账户对象
account2 = BankAccount(0)

# 打印第一个账户对象及其bool()结果
print(f"{account1}: bool() = {bool(account1)}")
# 打印第二个账户对象及其bool()结果
print(f"{account2}: bool() = {bool(account2)}")
# 格式说明：{value!r:10}

# value：要格式化的变量或表达式
# !r：转换标志，表示使用 repr() 函数而不是 str()
# :10：格式规范，表示最小字段宽度为 10 个字符

# 6.2.any() 和 all() 函数
# any() 和 all() 是 Python 内置的两个常用函数，用于判断可迭代对象中的元素布尔值。

# any(iterable): 只要 iterable 中有一个元素为 True（即"真值"），就返回 True；如果所有元素都为 False，则返回 False。
# all(iterable): 只要 iterable 中有一个元素为 False（即"假值"），就返回 False；只有所有元素都为 True 时才返回 True。
# 这两个函数常用于列表、元组、集合等的批量条件判断。
# any(): 任意一个为True则返回True
print("any()函数:")
print(f"any([False, False, False]): {any([False, False, False])}")  # False
print(f"any([False, True, False]): {any([False, True, False])}")  # True
print(f"any([1, 0, 0]): {any([1, 0, 0])}")  # True

# all(): 所有都为True才返回True
print("\nall()函数:")
print(f"all([True, True, True]): {all([True, True, True])}")  # True
print(f"all([True, False, True]): {all([True, False, True])}")  # False
print(f"all([1, 1, 0]): {all([1, 1, 0])}")  # False

# 实际应用
numbers = [2, 4, 6, 8, 10]
all_even = all(n % 2 == 0 for n in numbers)
any_odd = any(n % 2 == 1 for n in numbers)

print(f"\n数字列表: {numbers}")
print(f"是否全是偶数: {all_even}")  #  True
print(f"是否有奇数: {any_odd}")  #  False
