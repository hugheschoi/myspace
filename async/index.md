# Async

## 异步编程的语法目标，就是怎样让它更像同步编程

- 回调函数实现
- 事件监听/发布订阅
- Promise/A+ 和生成器函数
- async/await
https://codesandbox.io/s/jslian-xi-6j3f79?file=/src/asyncawait.js

### **回调函数**
- 必须在异步任务结束调用回调函数
- 如果出错了要把错误传入回调函数供调用者判断

Node.js 的模块就是回调的方式，并且把错误放在第一个

**问题**：回调地狱

### 事件监听
