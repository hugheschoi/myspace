### **从输入 URL 到页面渲染呈现，中间发生了什么**

1. DNS 解析
   在浏览器发起请求之前，需要将域名解析为服务器的 IP 地址。此时浏览器会查找本地 DNS 缓存是否有该域名对应的 IP 地址，如果没有则进行递归查询直到获取到 IP 地址。
2. 发起 TCP 连接
   浏览器与服务器通过 TCP/IP 协议建立连接。TCP 协议保证了数据传输的可靠性，即通过对数据进行分割、顺序控制、重传技术等手段来保证数据传输的可靠性。
3. 发起 HTTP 请求
   TCP 连接建立后，浏览器向服务器发送 HTTP 请求报文，包括请求方法、URL、HTTP 版本、请求头部和请求主体信息等。
4. 服务器处理请求并返回 HTTP 响应
   服务器收到客户端请求后进行处理，并将处理结果封装成响应报文发送给浏览器。响应报文包括协议版本、状态码、响应头部和响应正文等信息。
5. 浏览器解析渲染页面
   浏览器收到服务器返回的 HTML 文件后，首先将其解析成 DOM 树。接着，根据 CSS 文件及样式标记将样式信息添加至 DOM 树上形成渲染树。最后，根据渲染树渲染页面并呈现给用户。
6. 断开 TCP 连接
   当浏览器接收到完整的响应后，可选择断开 TCP 连接，也可以复用该连接再次请求其他资源，直到用户关闭浏览器。



### **http 主要用了什么算法提高了传输的可靠性和速度**

HTTP主要使用以下算法来提高传输的可靠性和速度：

1. TCP协议：TCP是一种面向连接的协议，用于确保数据的完整性和可靠性。它建立在IP协议之上，并通过三次握手来建立连接和四次握手来终止连接。
2. HTTP缓存：web缓存技术是通过保存以前请求和响应的副本来优化web性能的技术。当用户再次请求相同内容时，web缓存服务器可直接返回已经缓存的内容，从而大大减少了页面加载时间。
3. 压缩：HTTP可以通过压缩请求和响应数据来提高传输速度。目前常用的压缩算法是gzip和Deflate。
4. Keep-Alive：HTTP keep-alive 是一个常见的优化方法，它允许客户端与服务器之间暂时保持打开的TCP连接，从而避免了频繁地关闭和重新连接TCP连接所带来的开销。
5. CDN加速：Content Delivery Network（CDN），即内容分发网络，是一组被设计为更快地交付互联网内容的服务器。这些服务器通常位于于全球范围内各地，使得用户可以从最近的位置获取所需的内容，提高传输速度和可靠性。

总之， HTTP 中采用了多种技术和算法来提高传输的可靠性和速度，从而提高 web 性能。



### **http2 做了哪些优化**

HTTP/2 是 HTTP 协议的最新版本，并由 IETF 标准化。以下是 HTTP/2 所做的主要优化：

**1. 二进制分帧**
HTTP/2 改为在客户端和服务器之间传输二进制格式的数据。二进制格式的帧使得 HTTP/2 更容易解析和更加健壮，因为即使一个帧已经损坏了，它也不会影响到其他帧。

**2. 头部压缩**
HTTP/2 使用一种称为 HPACK 的算法对请求和响应头部进行压缩，以减少协议开销。这将显著减少需要在每个请求和响应中发送的字节数，并且只需发送更新或变化的头信息。

**3. 多路复用**
HTTP/2 允许在同一连接上同时发送多个请求和响应，这被称为 "多路复用"。相比于 HTTP/1.x，HTTP/2 可以更好地利用单个连接的资源，从而显著提高性能和并发度。

**4. 流量控制**
HTTP/2 支持流量控制机制，允许资源有序上传和下载。这可以避免单一的资源耗尽服务器/客户端的资源，提高整体性能。

**5. 服务端推送**
HTTP/2 提供了"服务端推送"功能，服务器可以在客户端请求资源时，推送与该资源相关的多个资源，以提高性能并减少客户端请求。

以上就是 HTTP/2 的优化点。其中多路复用、头部压缩和二进制协议是 HTTP/2 最重要的优化点。



### **二进制分帧**

二进制分帧是HTTP/2最大的改进之一，它将所有数据划分为更小的帧并对它们进行二进制编码。这样，TCP连接中的多个流就可以同时发送和接收，而不会阻塞。这种方式比HTTP / 1.1 基于文本的格式有更低的延迟，并且可以更好地执行流量控制，因为每个数据帧都包含标识符，表明哪个流它属于，并能够更好地精细地控制每个流的速度。

二进制分帧还支持服务器推送、处理头部压缩等多项功能，让HTTP/2速度更快、效率更高。



### js 实现 二进制分帧

要在 JavaScript 中实现二进制分帧，您可以使用 `ArrayBuffer` 对象来存储和操作数据。具体地说，您需要将消息拆分成事件，每个事件都是一个二进制帧，然后使用 WebSocket API 或类似于此的协议将它们发送到另一个端点。以下是一个简单的示例：

```js
// 创建 ArrayBuffer 缓冲区，参数为缓冲区大小（字节数）
let buffer = new ArrayBuffer(16);

// 从 ArrayBuffer 创建视图以读取和写入数据
let view = new DataView(buffer);

// 在视图偏移量 0 处写入第一个帧
view.setUint32(0, 123456);
view.setUint8(4, 1);

// 在视图偏移量 5 处写入第二个帧
view.setInt16(5, -32768);
view.setInt16(7, 32767);
view.setUint8(9, 2);

// 创建 WebSocket 连接并将两个帧发送到服务器
let ws = new WebSocket('ws://example.com');
ws.binaryType = 'arraybuffer';
ws.send(buffer);

```

上面的代码创建了一个 16 字节的 `ArrayBuffer` 缓冲区，并使用 `DataView` 视图在前 5 个字节中写入了第一个帧，在后 11 个字节中写入了第二个帧。最后，使用 `WebSocket` 对象将整个缓冲区发送到指定的服务器。

您可以根据自己的需要更改预定义数据的类型和大小，以及创建不同类型和数量的帧。重要的是要确保正确设置每个帧的标头和其他元数据，以便正常解析和处理它们。



### 什么是ALB转发规则

ALB (Application Load Balancer) 转发规则指定了 ALB 如何将传入的 HTTP/HTTPS 流量路由到与之对应的目标主机。使用ALB转发规则，可以将流量按路径、主机名或其他自定义条件进行分配，从而更好地控制流量流向以及如何处理特定类型的请求。

ALB转发规则是根据特定的匹配条件（例如，请求的 URL 路径）来匹配传入的流量并执行一组预定义的操作。通过使用条件和动作，转发规则可让您实现高度精细的负载均衡和流量分流策略。

下面是一个简单的 ALB 转发规则示例：

```
IF request path starts with /api
THEN forward to backend servers listening on port 8080
ELSE forward to backend servers listening on port 9090
```

在这个例子中，如果请求的 URL 包含“/api”路径，则该请求将被发送到监听端口8080的后端服务。否则，请求将被发送到监听端口9090的后端服务。

需要注意的是，ALB转发规则运行在 L7 协议层上，可以检查和操作 HTTP/HTTPS 请求。它们通常用于灵活的路由和流程控制，不仅帮助您保护应用程序免受恶意攻击，还可以提高性能和可用性。



### 写一个正则表达式，要以L或则R开头，拼接k，和大于0数字，拼接+号，拼接三位数字

正则表达式如下：

```
^[LR]k[1-9]\d{0,2}\+?\d{3}$
```

该正则表达式解释：

- `^`：匹配字符串的开始。
- `[LR]`：方括号内的任何一个字符都可以匹配，即以 L 或 R 开头。
- `k`：匹配 k 字符。
- `[1-9]`：1 ~ 9 中的任意一位数字。
- `\d{0,2}`：0 到 2 个数字。
- `\+?`：匹配一个加号或不匹配加号。
- `\d{3}`：匹配 3 位数字。
- `$`：匹配字符串结束。

综上所述，该正则表达式匹配以 L 或 R 开头，接着是字母 k，然后是大于 0 的整数（精度为 1 到 3 位）加一个可选的加号，最后是三位数字。



### 每次同个字符经过 md5后是不是同样的

不论多少次，相同的输入经过 MD5 哈希后会产生相同的输出结果。这也是哈希函数的基本特性之一，即给定相同的输入，输出结果总是相同的。这是因为 MD5 哈希函数是一种确定性函数，它将任意长度的输入转换成固定长度的输出（通常是 128 位），且输出结果是固定的、唯一的、不可逆的。因此，相同的输入每次经过 MD5 哈希后得到的结果都会是相同的，这也是哈希函数的一种重要应用，如在密码存储和校验等领域中广泛应用



