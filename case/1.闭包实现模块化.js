
// 闭包实现模块化
// 定义一个模块
const myModule = (function() {
  // 私有变量
  let privateVar = '私有变量';

  // 私有函数
  function privateFunction() {
    console.log('私有函数');
  }

  // 公共接口（通过返回一个对象将需要暴露的变量和函数公开）
  return {
    privateVar,
    privateFunction,
  };
})();

console.log(myModule.privateVar); // 1
console.log(privateVar); // publicVar is not defined

// 使用闭包创建模块
// (function() {
//     // 在这里编写你的代码
// })();

(function() {
    // 在这里编写你的代码
    var module = {};

    // 定义一个函数，用于在控制台输出 "Hello, World!"
    module.sayHello = function() {
        console.log("Hello, World!");
    };

    // 导出模块
    window.module = module;
})();

// 使用模块
module.sayHello(); // 输出 "Hello, World!"

// 闭包可以用来创建私有变量和函数，从而实现模块化编程。在上面的例子中，我们使用闭包创建了一个名为 module 的对象，并在其中定义了一个 sayHello 函数。最后，我们将 module 对象导出，使其可以在其他地方使用。
// 在其他地方使用模块
