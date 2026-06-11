def function_name(params):
    """文档字符串（可选）"""
    return params


# 返回平方
def square(x):
    return x * x


# 不带参数和返回值的函数
def say_hello():
    print("Hello from function!")


say_hello()  # Hello from function!


# 可以在函数内部定义文档字符串（docstring），用于描述函数的作用：
def greet(name):
    """向指定的人打招呼"""
    print(f"Hello, {name}!")


# 查看文档字符串
print(greet.__doc__)  # 向指定的人打招呼
help(greet)


def student_info(name, age, city):
    print(f"姓名: {name}, 年龄: {age}, 城市: {city}")


# 使用关键字参数，参数顺序可以不按定义顺序
student_info(age=20, name="Lucy", city="Beijing")
# 输出：姓名: Lucy, 年龄: 20, 城市: Beijing


# 4.4.可变参数 (*args)
# 可变参数用于当函数需要接受不定数量的位置参数时，通过在参数前加*来实现。
def show_args(*args):
    print(f"参数类型: {type(args)}")
    print(f"参数内容: {args}")


show_args(1, 2, 3)


def make_pizza(*toppings):
    print("制作一个披萨，添加以下配料：")
    for topping in toppings:
        print(f"- {topping}")


make_pizza("意大利香肠")
make_pizza("蘑菇", "青椒", "芝士")


# 4.5.关键字可变参数 (**kwargs)
# 关键字可变参数允许函数接收任意数量的"关键字参数"。这些参数会被自动收集到一个字典中。
def show_keyargs(**kwargs):
    print(f"参数类型: {type(kwargs)}")
    print(f"参数内容: {kwargs}")


show_keyargs(a=1, b=2, c=3)


def demo(a, *args, b=1, **kwargs):
    print(f"a: {a}")
    print(f"args: {args}")
    print(f"b: {b}")
    print(f"kwargs: {kwargs}")


demo(100, 2, 3, x=4, y=5)
# 输出：
# a: 100
# args: (2, 3)
# b: 1
# kwargs: {'x': 4, 'y': 5}


# 4.6.参数解包
# 在Python中，*和**不仅可以用于函数定义时接收可变参数，还可以用于参数解包。
def greet(name, age, city):
    print(f"姓名: {name}, 年龄: {age}, 城市: {city}")


# 使用 * 解包列表
person_info = ["Alice", 25, "北京"]

greet(*person_info)

# 使用 * 解包元组
data = ("Bob", 30, "上海")
greet(*data)  # 等同于 greet("Bob", 30, "上海")


# ** 用于解包字典类型
def create_profile(name, age, city, occupation):
    print(f"姓名: {name}, 年龄: {age}, 城市: {city}, 职业: {occupation}")


# 使用 ** 解包字典
profile_data = {"name": "Charlie", "age": 28, "city": "广州", "occupation": "工程师"}
create_profile(**profile_data)


# 混合使用 * 和 **
def complex_function(a, b, c, d, e):
    print(f"a={a}, b={b}, c={c}, d={d}, e={e}")


# 位置参数列表
positional_args = [1, 2]
# 关键字参数字典
keyword_args = {"d": 4, "e": 5}

complex_function(*positional_args, 3, **keyword_args)

# Python采用LEGB原则查找变量：
name = "全局变量"


def outer():
    name = "外部函数变量"

    def inner():
        name = "内部函数变量"
        print(name)  # 输出"内部函数变量"

    inner()
    print(name)  # 输出"外部函数变量"


outer()
print(name)  # 输出"全局变量"

# global关键字
# global关键字允许我们在函数内部声明某个变量为全局变量，从而可以在函数内部修改它。
counter = 0


def increment():
    global counter
    counter += 1


increment()
increment()
print(counter)  # 2


# nonlocal关键字
# nonlocal关键字用于在嵌套函数中声明变量来自最近的一层非全局作用域（外层函数）。
def outer():
    x = "local"

    def inner():
        nonlocal x  # 声明 x 来自外层作用域
        x = "nonlocal"
        print("inner:", x)

    inner()
    print("outer:", x)


outer()
# inner: nonlocal
# outer: nonlocal


# 高级函数特性
# 函数作为参数
def apply_operation(numbers, operation):
    """对数字列表应用操作"""
    return [operation(x) for x in numbers]


def square(x):
    return x**2


def double(x):
    return x * 2


numbers = [1, 2, 3, 4, 5]
squared = apply_operation(numbers, square)
doubled = apply_operation(numbers, double)

print(squared)  # [1, 4, 9, 16, 25]
print(doubled)  # [2, 4, 6, 8, 10]


# 嵌套函数
"""
用途：
实现闭包（closure）
将某些逻辑封装到本地作用域
作为工厂函数创建带记忆的数据
"""


def greet(name):
    def format_message():
        return f"Hello, {name}!"

    return format_message()


"""
闭包是指一个函数可以"记住"它被创建时的环境，即使在其外部函数已经执行完毕后，内部函数依然能够访问其外部作用域的变量。
"""


def make_multiplier(factor):
    """创建乘法器函数"""

    def multiplier(x):
        return x * factor

    return multiplier


double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
"""
特点：

内部函数引用了外部函数的局部变量
外部函数返回内部函数
内部函数可以访问外部函数的变量，即使外部函数已经执行完毕
"""

# 装饰器
"""
装饰器本质上是一个函数，它接受一个函数作为参数，并返回一个新的函数。装饰器常用于在不修改原函数代码的情况下，动态地为其添加新功能。
"""


def my_decorator(func):
    def wrapper():
        print("执行前")
        func()
        print("执行后")

    return wrapper


@my_decorator
def say_hello():
    print("Hello!")


say_hello()

# 9.匿名函数 (Lambda)
# 匿名函数（lambda表达式）是一种快速定义简单函数的方法，通常用于一些无需命名、只用一次的小函数场景。
"""
语法: lambda 参数1, 参数2, ... : 表达式
"""
# 基本 lambda 函数
square = lambda x: x**2
print(square(5))  # 25
# 在排序中使用
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78},
]

# 按成绩排序
sorted_students = sorted(students, key=lambda x: x["grade"], reverse=True)
print(sorted_students)
# 在 map 中使用
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]


def factorial(n):
    """计算阶乘的递归函数"""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))  # 120


def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


for i in range(10):
    print(fibonacci(i), end=" ")  # 0 1 1 2 3 5 8 13 21 34

"""
错误处理
在函数中进行错误处理可以提升程序的健壮性和用户体验。
def 函数名(参数):
    try:
        # 可能抛出异常的操作
    except 异常类型1:
        # 异常类型1的处理代码
    except 异常类型2:
        # 异常类型2的处理代码
    else:
        # 没有发生异常时的代码
    finally:
        # 无论是否发生异常都执行
"""


def safe_divide(a, b):
    """安全的除法函数"""
    try:
        result = a / b
    except ZeroDivisionError:
        return "错误：除数不能为零"
    except TypeError:
        return "错误：参数类型不正确"
    else:
        return result


print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # 错误：除数不能为零
print(safe_divide(10, "a"))  # 错误：参数类型不正确


# 文件处理函数
def read_file_safely(filename):
    """安全读取文件内容"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"错误：文件{filename} 不存在"
    except Exception as e:
        return f"读取文件时出错：{str(e)}"


def process_csv_data(file_path, delimiter=","):
    """处理 csv数据"""
    import csv

    data = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=delimiter)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"处理csv文件时出错：{e}")
        return None


# 学生管理系统
def create_student_management_system():
    """创建学生管理系统"""
    students = []

    def add_student(name, age, grade):
        """添加学生"""
        student = {"name": name, "age": age, "grade": grade}
        students.append(student)
        print(f"学生 {name} 添加成功")

    def find_student(name):
        """查找学生"""
        for student in students:
            if student["name"].lower() == name.lower():
                return student
        return None

    def get_student_statistics():
        """获取学生信息"""
        if not students:
            return None
        total_students = len(students)
        average_grade = sum(s["grade"] for s in students) / total_students
        best_student = max(students, key=lambda x: x["grade"])
        return {
            "total_students": total_students,
            "average_grade": round(average_grade, 2),
            "best_student": best_student,
        }

    def display_all_students():
        """显示所有学生"""
        if not students:
            print("没有学生记录")
            return

        print("\n所有学生信息:")
        for i, student in enumerate(students, 1):
            print(
                f"{i}. 姓名: {student['name']}, "
                f"年龄: {student['age']}, 成绩: {student['grade']}"
            )

    return {
        "add_student": add_student,
        "find_student": find_student,
        "get_statistics": get_student_statistics,
        "display_all": display_all_students,
    }


# 使用示例
sms = create_student_management_system()
sms["add_student"]("Alice", 20, 95)
sms["add_student"]("Bob", 21, 87)
sms["display_all"]()
