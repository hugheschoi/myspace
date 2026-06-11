"""
3.1.缩进
Python 使用缩进来区分代码块，这是语法强制要求的。

通常使用 4 个空格 作为一个缩进级别。
同一个代码块内的语句必须有相同的缩进。
缩进错误会导致 IndentationError。
"""
if True:
    print("Hello,") # 缩进4个空格
    print("World!") # 缩进4个空格
print("This is outside the if block.") # 没有缩进，不属于if代码块

"""
3.2.条件表达式
if 后面的“条件”可以是很广泛的表达式，其结果会被判断为 True 或 False。

比较运算符: == (等于), != (不等于), > (大于), < (小于), >= (大于等于), <= (小于等于)
逻辑运算符: and (与), or (或), not (非)
成员运算符: in (在...内), not in (不在...内)
其他可以产生布尔值的表达式或函数。
"""
age = 25
is_student = True

# 使用 and
if age >= 18 and is_student:
    print("您是成年学生。")

# 使用 or
if age < 12 or age >= 65:
    print("您可以享受优惠票价。")

# 使用 not
if not is_student:
    print("您不是学生。")

# 使用 in
name = "Alice"
if name in ["Alice", "Bob", "Charlie"]:
    print(f"你好，{name}！")

