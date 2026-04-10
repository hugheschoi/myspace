# 整型(int)表示整数，包括正整数、负整数和零。
# 基本整型定义
positive = 42
negative = -15
zero = 0

print(f"positive: {positive}, 类型: {type(positive)}")  # <class 'int'>
print(f"negative: {negative}, 类型: {type(negative)}")  # <class 'int'>
print(f"zero: {zero}, 类型: {type(zero)}")  # <class 'int'>

# 2.不同进制的整型表示
# 十进制 (默认)
decimal = 10
print(f"十进制 10: {decimal}")

# 二进制 (以 0b 或 0B 开头)
binary = 0b1010  # 二进制 1010 = 十进制 10
print(f"二进制 0b1010: {binary}")

# 八进制 (以 0o 或 0O 开头)
octal = 0o12  # 八进制 12 = 十进制 10
print(f"八进制 0o12: {octal}")

# 十六进制 (以 0x 或 0X 开头)
hexadecimal = 0xA  # 十六进制 A = 十进制 10
print(f"十六进制 0xA: {hexadecimal}")

# 使用下划线提高可读性 (Python 3.6+)
large_number = 1_000_000
print(f"大数字: {large_number}")

credit_card = 1234_5678_9012_3456
print(f"信用卡号: {credit_card}")

bytes_value = 0b1100_1010_1111_0101
print(f"字节值: {bytes_value}")

# 3.整型转换函数
# 其他类型转整型
print("类型转换:")
print(f"int(3.14) = {int(3.14)}")  # 浮点数转整型 (截断小数)
print(f"int(-2.99) = {int(-2.99)}")  # -2
print(f"int('100') = {int('100')}")  # 字符串转整型
print(f"int('1010', 2) = {int('1010', 2)}")  # 二进制字符串转十进制
print(f"int('FF', 16) = {int('FF', 16)}")  # 十六进制字符串转十进制
print(f"int(True) = {int(True)}")  # 布尔值转整型 (True=1)
print(f"int(False) = {int(False)}")  # 布尔值转整型 (False=0)
# 进制转换函数
number = 10
print(f"\n数字 {number} 的不同进制表示:")
print(f"二进制: {bin(number)}")  # 0b1010
print(f"八进制: {oct(number)}")  # 0o12
print(f"十六进制: {hex(number)}")  # 0xa

# 4.1 算术运算
a, b = 10, 3

print("基本算术运算:")
print(f"{a} + {b} = {a + b}")  # 加法: 13
print(f"{a} - {b} = {a - b}")  # 减法: 7
print(f"{a} * {b} = {a * b}")  # 乘法: 30
print(f"{a} / {b} = {a / b}")  # 除法: 3.333... (返回浮点数)
print(f"{a} // {b} = {a // b}")  # 整除: 3
print(f"{a} % {b} = {a % b}")  # 取余: 1
print(f"{a} ** {b} = {a ** b}")  # 幂运算: 1000
print(f"-{a} = {-a}")  # 取负: -10
print(f"+{a} = {+a}")  # 取正: 10

# 4.2 位运算
x, y = 5, 3  # 5 = 0b101, 3 = 0b011

print("位运算:")
print(
    f"{x} & {y} = {x & y}"
)  # 按位与（规则：全 1 才 1，有 0 则 0）: 0b101 & 0b011 = 0b001 = 1
print(
    f"{x} | {y} = {x | y}"
)  # 按位或（规则：有 1 就 1，全 0 才 0）: 0b101 | 0b011 = 0b111 = 7
print(
    f"{x} ^ {y} = {x ^ y}"
)  # 按位异或(规则：相同为 0，不同为 1): 0b101 ^ 0b011 = 0b110 = 6 异或是指两个位不同则返回1，相同则返回0
print(
    f"~{x} = {~x}"
)  # 按位取反(记公式：~x = -x - 1): ~0b101 = -6 (补码表示)  −x−1 00000101→11111010-1→11111001→ 00000110
print(f"{x} << 1 = {x << 1}")  # 左移: 0b101 << 1 = 0b1010 = 10 左移是乘以2
print(
    f"{x} >> 1 = {x >> 1}"
)  # 右移: 0b101 >> 1 = 0b10 = 2 右移是除以2. 5 << 3 =  5 × 2³ = 40

READ_PERMISSION = 0b001  # 1
# 定义写权限，二进制010，十进制2
WRITE_PERMISSION = 0b010  # 2
# 定义执行权限，二进制100，十进制4
EXECUTE_PERMISSION = 0b100  # 4

# 用户权限：拥有读和写权限，使用按位或运算
user_permissions = READ_PERMISSION | WRITE_PERMISSION  # 0b011

# 打印权限控制标题
print(f"\n权限控制:")
# 打印用户当前的权限（二进制表示）
print(f"用户权限: {bin(user_permissions)}")
# 判断用户是否有读权限
print(f"可读权限: {(user_permissions & READ_PERMISSION) != 0}")
# 判断用户是否有写权限
print(f"可写权限: {(user_permissions & WRITE_PERMISSION) != 0}")
# 判断用户是否有执行权限
print(f"可执行权限: {(user_permissions & EXECUTE_PERMISSION) != 0}")

# 给用户添加执行权限，使用按位或运算
user_permissions |= EXECUTE_PERMISSION
# 打印添加执行权限后的用户权限（二进制表示）
print(f"添加执行权限后: {bin(user_permissions)}")

# 4.3.比较运算
a, b = 10, 5

print("比较运算:")
print(f"{a} == {b}: {a == b}")  # 等于: False
print(f"{a} != {b}: {a != b}")  # 不等于: True
print(f"{a} > {b}: {a > b}")  # 大于: True
print(f"{a} < {b}: {a < b}")  # 小于: False
print(f"{a} >= {b}: {a >= b}")  # 大于等于: True
print(f"{a} <= {b}: {a <= b}")  # 小于等于: False

# 链式比较
c = 7
print(f"\n链式比较:")
print(f"{b} < {c} < {a}: {b < c < a}")  # True
print(f"{a} > {c} > {b}: {a > c > b}")  # True

# 5.整型的特性
# 5.1.无限精度
# Python的整型没有固定的位数限制，可以根据需要自动扩展。这意味着你可以处理非常大的整数，而不必担心溢出。
# Python整型没有大小限制 (仅受内存限制)
very_large = 10**100  # 10的100次方
very_small = -(10**100)

print(f"非常大的数: {very_large}")
print(f"非常小的数: {very_small}")
print(f"类型仍然是int: {type(very_large)}")


def factorial(n):
    """计算阶乘"""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


print(f"\n阶乘演示:")
print(f"10! = {factorial(10)}")
print(f"50! = {factorial(50)}")  # 可以计算非常大的阶乘

# 5.2.内存占用
import sys

"""显示整型的内存占用"""
numbers = [0, 1, 10, 100, 1000, 10**10, 10**100]

print("整型内存占用:")
for num in numbers:
    size = sys.getsizeof(num)
    print(f"数字 {num}: {size} 字节")

# 6.内置数学函数
import math

numbers = [-5, 0, 5, 10, 15]

print("内置数学函数:")
for num in numbers:
    print(f"abs({num}) = {abs(num)}")  # 绝对值

print(f"\n最大值: {max(1, 5, 2, 8, 3)}")  # 8
print(f"最小值: {min(1, 5, 2, 8, 3)}")  # 1
print(f"求和: {sum([1, 2, 3, 4, 5])}")  # 15

# 更多数学函数
print(f"\n高级数学函数:")
print(f"2的3次方: {pow(2, 3)}")  # 8
print(f"四舍五入: {round(3.14159, 2)}")  # 3.14
print(f"向上取整: {math.ceil(3.14)}")  # 4
print(f"向下取整: {math.floor(3.14)}")  # 3
