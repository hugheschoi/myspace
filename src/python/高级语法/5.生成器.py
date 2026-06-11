"""
1. 所有的生成器都是迭代器（因为 Python 自动帮生成器实现了 __iter__() 和 __next__() 协议）。

2. 但迭代器不一定是生成器（比如你自己手写的迭代器类，或者 iter([1,2,3]) 得到的对象）。

3. 核心优势：比普通迭代器写法更简单、代码更少、可读性极高，同时完美继承了迭代器“省内存、惰性求值、分批处理”的所有优点。
"""


# 写法一： yield
def fib(max_count):
    a, b = 0, 1
    for _ in range(max_count):
        yield a
        a, b = b, a + b


# 直接用 for 循环消费（for 会自动调用 next()）
for num in fib(5):
    print(num)


# 写法二： 生成器表达式， 直接把列表推导式的方括号 [] 换成圆括号 () 即可：
# 这是一个列表推导式，直接在内存中生成包含 100 万个元素的列表（占内存）
squares_list = [x**2 for x in range(1000000)]

# 这是一个生成器表达式，内存占用几乎为 0！它现在什么都没算，只是记住了公式
squares_gen = (x**2 for x in range(1000000))

print(next(squares_gen))  # 0
print(next(squares_gen))  # 1

"""
列表推导式 vs 生成器表达式

列表推导式 - 立即计算所有结果
生成器表达式 - 惰性计算
"""


def example_gen():
    print("step 1")
    yield "A"
    print("step 2")
    yield "B"
    print("End")


gen = example_gen()
print(next(gen))
print(next(gen))
# print(next(gen))

"""
close() 方法 - 关闭生成器
close() 方法用于主动终止生成器，触发资源清理。

使用场景：

读取大文件时提前终止
数据库连接管理
网络连接清理
资源释放
"""
gen.close()
