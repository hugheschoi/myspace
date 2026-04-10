with 是什么用法
with 是 Python 的上下文管理器语法：进入代码块时做“准备”，离开代码块时做“收尾”。
在这里的“收尾”就是：无论代码块里是否报错，都会自动 f.close() 关闭文件，避免文件句柄泄漏、内容未刷盘等问题。
等价写法（不推荐，但便于理解）：
```python
f = open("output.txt", "w", encoding="utf-8")
try:
    # 在这里写 f.write(...)
    pass
finally:
    f.close()
```
常见写法示例：
```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")
```
其实就是语法糖