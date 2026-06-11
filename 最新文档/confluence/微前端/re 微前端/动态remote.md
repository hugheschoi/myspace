Webpack Module Federation 的 **动态 remote**，核心就是：**remoteEntry.js 的地址不要在构建时写死，而是在运行时决定**。官方支持把 `remotes` 写成 `promise new Promise(...)`，这个 promise 最终 resolve 一个带 `get/init` 方法的 remote container。([webpack][1])

静态写法：

```js
remotes: {
  order: "order@https://cdn.xxx.com/order/remoteEntry.js",
}
```

动态写法：

```js
remotes: {
  order: `promise new Promise((resolve, reject) => {
    const url = window.__REMOTE_CONFIG__.order;

    const script = document.createElement("script");
    script.src = url;

    script.onload = () => {
      const proxy = {
        get: (request) => window.order.get(request),
        init: (arg) => {
          try {
            return window.order.init(arg);
          } catch (e) {
            console.log("remote already initialized");
          }
        },
      };

      resolve(proxy);
    };

    script.onerror = reject;
    document.head.appendChild(script);
  })`,
}
```

然后业务里还是这样用：

```js
const OrderApp = React.lazy(() => import("order/App"));
```

重点是：**import 路径还是固定的 `order/App`，但 `order` 对应的 remoteEntry 地址可以运行时变化。**

---

## 为什么要动态 remote？

真实项目里常见场景：

```text
dev  -> https://dev-cdn.xxx.com/order/remoteEntry.js
test -> https://test-cdn.xxx.com/order/remoteEntry.js
prod -> https://cdn.xxx.com/order/remoteEntry.js
```

或者灰度：

```text
用户 A -> order v1
用户 B -> order v2
```

或者多租户：

```text
sg -> https://sg-cdn.xxx.com/order/remoteEntry.js
id -> https://id-cdn.xxx.com/order/remoteEntry.js
```

---

## 面试里可以这样讲

> 静态 remote 的问题是 remoteEntry 地址在构建时确定，如果不同环境、灰度版本、租户域名不同，就需要重新构建 Host。
>
> 动态 remote 可以把 remoteEntry 的地址延迟到运行时决定。Webpack 支持基于 Promise 的 remote 配置，这个 Promise 最终返回一个符合 Module Federation container 协议的对象，也就是包含 `get` 和 `init` 方法。

---

## 更工程化的封装

通常不会直接把一大段代码写在 webpack config 里，而是封装成 loader：

```js
function loadRemote(scope, url) {
  return new Promise((resolve, reject) => {
    if (window[scope]) {
      resolve(window[scope]);
      return;
    }

    const script = document.createElement("script");
    script.src = url;
    script.type = "text/javascript";
    script.async = true;

    script.onload = () => {
      resolve(window[scope]);
    };

    script.onerror = () => {
      reject(new Error(`Failed to load remote: ${scope}`));
    };

    document.head.appendChild(script);
  });
}
```

然后：

```js
async function loadComponent(scope, module) {
  await __webpack_init_sharing__("default");

  const container = await loadRemote(
    scope,
    window.__REMOTE_CONFIG__[scope]
  );

  await container.init(__webpack_share_scopes__.default);

  const factory = await container.get(module);
  return factory();
}
```

使用：

```js
const RemoteButton = React.lazy(() =>
  loadComponent("order", "./Button")
);
```

这个方式更“彻底动态”：连 webpack config 里的 `remotes` 都可以不写。

---

## 两种动态 remote 对比

| 方式                              | 特点                           | 适合                  |
| ------------------------------- | ---------------------------- | ------------------- |
| `promise new Promise(...)`      | 仍然走 Webpack remote import 机制 | remote 名称固定，URL 动态  |
| 手写 `loadRemote + container.get` | 更灵活                          | remote 名称、URL、模块都动态 |

官方概念里 remote 是运行时加载的远程容器；remote module 的加载本身就是异步操作。([webpack][2])

---

## 真实项目要注意的坑

第一，`scope` 必须和 remote 的 `name` 一致：

```js
// remote
new ModuleFederationPlugin({
  name: "order",
  filename: "remoteEntry.js",
})
```

Host 里才能：

```js
window.order.get("./App")
```

第二，必须先初始化 shared：

```js
await __webpack_init_sharing__("default");
await container.init(__webpack_share_scopes__.default);
```

否则 React、ReactDOM 等共享依赖可能不按预期复用。

第三，`container.init()` 可能被调用多次，所以一般要 catch：

```js
try {
  await container.init(__webpack_share_scopes__.default);
} catch (e) {
  // already initialized
}
```

第四，要做失败降级：

```jsx
<ErrorBoundary fallback={<div>模块加载失败</div>}>
  <Suspense fallback={<div>加载中...</div>}>
    <RemoteApp />
  </Suspense>
</ErrorBoundary>
```

第五，多个 remote 时建议设置 `output.uniqueName`，避免多个 Webpack runtime 冲突；Webpack 中文文档也提到，加载多个 remote 时建议为 remote builds 设置 `output.uniqueName`。([webpack][3])

---

你面试里可以用一句话总结：

> 动态 remote 的本质不是动态 `import`，而是动态加载 remote container。只要运行时拿到符合 `get/init` 协议的 container，Webpack 就能继续通过 Module Federation 加载远程模块。

[1]: https://docs.webpack.js.org/guides/module-federation?utm_source=chatgpt.com "Module Federation - webpack"
[2]: https://webpack.js.org/concepts/module-federation/?utm_source=chatgpt.com "Module Federation - webpack"
[3]: https://webpack.docschina.org/concepts/module-federation/?utm_source=chatgpt.com "Module Federation | webpack 中文文档"
