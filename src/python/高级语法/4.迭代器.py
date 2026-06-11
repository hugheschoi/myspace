"""
惰性求值 - 非常节省内存
可迭代对象 vs 迭代器
可迭代对象：
  1. 定义： 内部实现了 __iter__() 方法的对象。可以被 for 循环遍历。
  2. 特点： 是一整坨数据，但不能自己记住读到哪了。

迭代器：
  1. 定义：内部同时实现了 __iter__() 和 __next__() 方法的对象。
  2. 特点：能够记住当前遍历的位置，每次调用返回下一个值。

对比起来迭代器的优势是可以分批处理数据(用next)，惰性求值不占用大量内存
"""


class MyIterator:
    """自定义迭代器示例"""

    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        """返回迭代器自身"""
        return self

    def __next__(self):
        """返回下一个元素"""
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value


# 使用自定义迭代器
my_iter = MyIterator([1, 2, 3])
for item in my_iter:
    print(item)  # 输出: 1, 2, 3

# 也可以手动调用 next()
my_iter2 = MyIterator(["a", "b", "c"])
print(next(my_iter2))  # 'a'
print(next(my_iter2))  # 'b'
print(next(my_iter2))  # 'c'
# print(next(my_iter2))  # 抛出 StopIteration 异常

"""
for 循环的幕后黑手
当你写 for x in [1, 2, 3]: 时，Python 在底层其实做了这三件事：

调用 iter([1, 2, 3]) 把列表变成一个迭代器。

不断调用迭代器的 __next__() 方法（或使用内置函数 next()）获取元素。

捕捉到 StopIteration 异常时，默默地结束循环。
"""


class Fibonacci:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.max_count:
            result = self.a
            self.a, self.b = self.b, self.a + self.b
            self.count += 1
            return result
        else:
            raise StopIteration


fib = Fibonacci(10)

# 方式 A：使用 next() 释放数据
print(next(fib))  # 0
print(next(fib))  # 1

print("--- 剩下的用 for 循环吃掉 ---")
# 方式 B：使用 for 循环（它会自动处理 StopIteration）
for num in fib:
    print(num)
