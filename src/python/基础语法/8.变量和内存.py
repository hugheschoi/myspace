# 变量的命名规则
# 遵循 PEP 8 编码规范：
# 推荐：蛇形命名法（snake_case）
user_name = "Charlie"
total_count = 42
file_path = "/docs/report.pdf"

# 2.3.特殊命名约定
# 单下划线开头：内部使用，不建议外部访问
_internal_var = "private"

# 双下划线开头：类的私有成员
__private_var = "really private"

# 双下划线前后：魔术方法/特殊方法
# __init__, __str__, __len__

# 单下划线：临时变量或不重要的变量
for _ in range(5):
    print("Hello")
# __init__：构造方法，用于初始化对象。
# __str__：定义对象的字符串表示，通常用于print()输出。
# __len__：定义对象的长度，支持len()函数。
# 这些被称为“魔术方法”或“特殊方法”，在类中有特殊用途。

# 3.变量的赋值
# 3.1.基本赋值
# 基本类型赋值
message = "Hello, World!"
pi = 3.14159
is_active = True
count = 0
# 3.2.多重赋值
# 同时为多个变量赋同一个值
a = b = c = 100
print(a, b, c)  # 100 100 100

# 同时为多个变量赋不同的值（元组解包）
name, age, city = "Alice", 30, "Beijing"
print(name)  # Alice
print(age)  # 30
print(city)  # Beijing

# 3.3.变量交换
# Python 方式（推荐）
x, y = 10, 20
x, y = y, x
print(x, y)  # 20 10

# 传统方式（不推荐）
x, y = 10, 20
temp = x
x = y
y = temp
print(x, y)  # 20 10
# 3.4.链式赋值的陷阱
# 链式赋值会导致所有变量引用同一个对象
# 注意：共享同一个对象
a = b = [1, 2, 3]
a.append(4)
print(b)  # [1, 2, 3, 4] - b 也被修改了！

# 正确方式：分别赋值
a = [1, 2, 3]
b = [1, 2, 3]  # 创建新对象
a.append(4)
print(b)  # [1, 2, 3] - b 没有被修改

# 4.深入理解：变量与对象
# 4.1.一切皆对象
# 在 Python 中，一切都是对象，包括数字、字符串、函数、类等。
# 数字是对象
x = 42
print(type(x))  # <class 'int'>
print(isinstance(x, object))  # True


# 函数也是对象
def greet():
    return "Hello"


print(type(greet))  # <class 'function'>
print(isinstance(greet, object))  # True
# type(obj)：用于查看对象的类型。例如，type(123) 返回 <class 'int'>，type("abc") 返回 <class 'str'>。
# isinstance(obj, class_or_tuple)：判断一个对象是否是某个类型（或类型元组）的实例。例如，isinstance(123, int) 返回 True
# isinstance("abc", (int, str)) 返回 True。

# 4.2.动态类型
# 变量本身没有类型，类型属于对象。同一个变量可以指向不同类型的对象。
var = 100
print(var, type(var))  # 100 <class 'int'>

var = "Now I'm a string"
print(var, type(var))  # Now I'm a string <class 'str'>

var = [1, 2, 3]
print(var, type(var))  # [1, 2, 3] <class 'list'>

var = {"key": "value"}
print(var, type(var))  # {'key': 'value'} <class 'dict'>

# 4.3.对象的身份：id() 和 is
# id() 返回对象的唯一标识（内存地址）
a = [1, 2, 3]
print(id(a))  # 例如：140245678901234

# is 检查是否是同一个对象
b = a
c = [1, 2, 3]

print(a is b)  # True - 指向同一个对象
print(a is c)  # False - 指向不同的对象
print(a == c)  # True - 内容相同

# 查看 id
print(id(a))  # 140245678901234
print(id(b))  # 140245678901234 (相同)
print(id(c))  # 140245678905678 (不同)
# 重要区别：

# is：比较对象的身份（内存地址是否相同）
# ==：比较对象的值（内容是否相同）

# 5.内存指向关系
# 5.1.多个变量指向同一个对象
a = 100
b = a
# 变量 a ────┐
#           ↓
#       [整数对象 100]
#           ↑
# 变量 b ────┘
# (地址: 0x2000)

print(a is b)  # True - 指向同一个对象
print(id(a) == id(b))  # True - 内存地址相同

# 修改 a 会怎样？
a = 200
print(a)  # 200
print(b)  # 100 - b 仍然指向原来的对象

# 内存变化
print(a is b)  # False - 现在指向不同对象
# 关键理解：a = 200 不是修改了对象 100 的值，而是创建了新对象 200，然后让 a 指向这个新对象。

# 5.2.相同值的不同对象
# a = [1, 2, 3]
# b = [1, 2, 3]
# 变量 a ───→ [列表对象 [1,2,3]]
#             (地址: 0x3000)

# 变量 b ───→ [列表对象 [1,2,3]]
#             (地址: 0x4000)
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)  # True - 值相等
print(a is b)  # False - 不是同一个对象
print(id(a), id(b))  # 两个不同的地址

# 修改 a 不会影响 b
a.append(4)
print(a)  # [1, 2, 3, 4]
print(b)  # [1, 2, 3]

# 5.3.小整数缓存机制
# Python 对整数和短字符串进行了缓存优化（驻留机制）。
# 整数缓存
a = 100
b = 100
print(a is b)  # True - 指向同一个缓存对象
# 字符串驻留
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True - 指向同一个对象

# 包含特殊字符的字符串可能不驻留
s3 = "hello" * 10000
s4 = "hello" * 10000
print(s3 is s4)  # 可能是 False

# 6.可变对象 vs 不可变对象
# 这是理解 Python 内存管理的最关键部分！
# 6.1.不可变对象（Immutable）
# 不可变对象一旦创建，其值就不能被修改。

# 常见的不可变类型包括：

# int（整数）：一旦赋值，数值不可更改。
# float（浮点数）：数值不可更改。
# str（字符串）：内容不可更改，任何修改都会生成新字符串对象。
# tuple（元组）：元素不可更改。
# frozenset（冻结集合）：集合内容不可更改。
# bytes（字节串）：内容不可更改。
# 这些类型的对象在创建后，其内部数据不能被修改。如果对它们进行“修改”操作，实际上是创建了一个新的对象，原对象保持不变。
