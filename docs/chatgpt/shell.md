#### **判断变量是不是等于"error"?**

在 `sh` 中，可以使用双等号 `==` 来判断一个变量是否等于另一个字符串。因此，要检查一个变量是否等于 `"error"`，可以使用以下代码：

```sh
if [ "$YOUR_VARIABLE" == "error" ]; then
  # Do something if variable equals "error"
fi
```

在上面的代码中，将您想要检查的变量名替换到 `$YOUR_VARIABLE` 的位置即可。如果变量确实等于 `"error"`，则条件成立，并且 `then` 后面的语句将被执行。如果不等于，则条件不成立，将跳过 `then` 后面的语句。



#### **sh if else 怎么写?**

在 `sh` 中，可以使用 `if-else` 语句来根据条件执行不同的代码块。以下是 `if-else` 语句的基本结构：

```sh
if [condition]; then
  # Execute this code if condition is true
else
  # Execute this code if condition is false
fi
```

其中 `[condition]` 是一个表达式，如果它的值为真，则执行 `then` 后面的代码块，否则执行 `else` 后面的代码块。

下面是一个示例，演示了如何使用 `if-else` 语句在 `sh` 中判断一个数是否小于等于 10：

```sh
#!/bin/sh

number=5

if [ "$number" -le 10 ]; then
  echo "The number is less than or equal to 10"
else
  echo "The number is greater than 10"
fi
```

在上面的示例中，我们定义了一个变量 `number` 并将其设置为 5。然后，我们使用 `if-else` 语句测试该变量是否小于或等于 10，并在控制台输出相应的文本。

注意，`if-else` 语句中的条件需要用方括号括起来，并且关键字 `then` 和 `else` 后面都需要有空格。



#### 执行 node 如何传递参数和使用参数

在执行 Node.js 脚本时，可以通过命令行传递参数并在脚本中使用这些参数。以下是如何在 Node.js 中传递和使用参数的方法：

**传递参数**

要传递参数，请在命令行上使用 `node` 命令，并在文件名后面添加要传递的参数。多个参数之间用空格分隔。例如：

```sh
node app.js arg1 arg2 arg3
```

在上面的例子中，我们向 `app.js` 脚本传递了三个参数：`arg1`、`arg2` 和 `arg3`。

你也可以将参数作为环境变量传递给 Node.js 脚本。例如：

```sh
MY_ARG=hello node app.js
```

在上面的例子中，我们将 `MY_ARG` 变量设置为 `hello` 并将其传递给 `app.js` 脚本中。

**使用参数**

在 Node.js 中，传递给脚本的参数可以通过 `process.argv` 数组来访问。该数组包含了以下元素：

- `process.argv[0]`：Node.js 的可执行文件路径。
- `process.argv[1]`：当前执行的 JavaScript 文件路径。
- `process.argv[2]` 到 `process.argv[n]`：传递给脚本的参数。

例如，如果我们将以下代码保存到 `app.js` 文件中：

```js
console.log(process.argv);
```

然后在命令行上执行以下命令：

```sh
node app.js arg1 arg2 arg3
```

我们将看到以下输出：

```
[ 'C:\\Program Files\\nodejs\\node.exe',
  'D:\\path\\to\\app.js',
  'arg1',
  'arg2',
  'arg3' ]
```

从上面的输出中，我们可以发现传递给脚本的参数是从 `process.argv[2]` 开始的。因此，我们可以根据需要访问这些参数并在脚本中使用它们。例如：

```js
console.log('First argument:', process.argv[2]);
console.log('Second argument:', process.argv[3]);
console.log('Third argument:', process.argv[4]);
```

这将分别输出：

```
First argument: arg1
Second argument: arg2
Third argument: arg3
```

请注意，`process.argv` 数组的前两个元素是 Node.js 和 JavaScript 文件的路径，并不是传递给脚本的参数。



#### 想再 sh 脚本上执行 nodejs 脚本，node.js 脚本执行异步的请求，得到结果后，在sh脚本上获取这个异步获取的值，并设置成环境变量

当在 sh 脚本中执行 nodejs 脚本时，可以使用以下命令：

```sh
result=$(node script.js)
```

这将执行 `script.js` 文件，并将脚本返回的数据存储在 `$result` 变量中。如果 `script.js` 包含异步请求，它可能不会立即返回结果。在这种情况下，您需要等待结果并将其设置为环境变量。以下是一个示例：

```sh
#!/bin/bash

# Execute script.js and store the result in a variable
result=$(node script.js)

# Wait until the result is available
while [ -z "$result" ]
do
  sleep 1
done

# Set the result as an environment variable
export MY_VAR=$result

echo "The value of MY_VAR is: $MY_VAR"
```

在上面的示例中，我们首先执行 `node script.js` 命令，并将其结果赋值给 `$result` 变量。接下来，我们等待 `$result` 变量的值不再为空。一旦结果可用，我们使用 `export` 命令将其设置为环境变量 `$MY_VAR`。最后，我们打印出变量的值以进行验证。

请注意，等待异步结果的方式可能有所不同，具体取决于您的代码实现方式。例如，您可以使用 `sleep` 来等待固定时间，或者使用类似 `jq` 的工具来解析 JSON 数据并提取特定字段。在任何情况下，只要您能够获取异步结果并将其设置为环境变量，就可以做到这一点。

**有详细的例子吗？**

当您在 shell 脚本中执行一个 Node.js 脚本，该脚本可能会执行异步请求。然后，您需要等待异步请求返回结果，并将其设置为环境变量。下面是一个例子：


**async.js**

```javascript
setTimeout(() => {
  console.log('Async result is ready')
  process.stdout.write(JSON.stringify({ message: 'Hello, World!' }))
}, 5000)
```

这个脚本只是执行 5 秒钟的 `setTimeout`，并在控制台上输出一条消息，然后返回一个 JSON 格式的数据。

正如我之前所解释的，使用 `$()` 运算符可以将 Node.js 脚本输出的值赋给 shell 变量。所以，我们可以使用以下的语句来执行 `async.js` 并将结果存储到 `$RESULT` 变量中：

```sh
RESULT=$(node async.js)
```

但是，由于 `setTimeout` 的存在，`RESULT` 变量将被设置为空字符串。实际上，5 秒的延迟意味着在执行上述语句时，Node.js 脚本并没有立即返回任何东西。

因此，我们需要等待 Node.js 脚本完成执行以获取完整的结果。在这种情况下，我们可以使用 `jq` 工具来解析 JSON 数据并提取我们需要的字段。如果尚未安装 `jq`，请参阅官方 [安装说明](https://stedolan.github.io/jq/download/)。

接下来，我们可以使用以下代码来等待异步请求返回结果：

```sh
RESULT=$(node async.js)
while [ -z "$RESULT" ] || [ "$RESULT" == 'null' ]
do
  sleep 1
  RESULT=$(node async.js)
done

MESSAGE=$(echo "$RESULT" | jq -r '.message')
```

注意，我们通过检查 `$RESULT` 变量及其是否为 `null` 来等待异步请求的结果。如果它是空的或是 `null`，我们就等待一秒钟并再次获取它的值。直到 Node.js 脚本输出 JSON 数据为止。

现在，我们可以使用 `jq` 工具提取消息字段，并将其设置为环境变量:

```sh
export MESSAGE=$MESSAGE
```

最终，整个脚本应该长成这样：

**get_async_message.sh**

```sh
#!/bin/sh

RESULT=$(node async.js)

while [ -z "$RESULT" ] || [ "$RESULT" == 'null' ]
do
  sleep 1
  RESULT=$(node async.js)
done

MESSAGE=$(echo "$RESULT" | jq -r '.message')

export MESSAGE=$MESSAGE

echo "Async message is: $MESSAGE"
```

当您运行此脚本时，它应该会等待 5 秒钟(由 `async.js` 的 `setTimeout` 函数控制) 并输出以下内容：

```
Async message is: Hello, World!
```

#### 我如何在 js 中获取从 sh 脚本中设置的环境变量

在 JavaScript 中，您可以使用 `process.env` 对象来访问从 shell 脚本中设置的环境变量。

例如，在 Shell 脚本中，您可以这样设置环境变量：

```sh
export MY_VAR="Hello World"
```

要在 JavaScript 中访问此环境变量，请使用以下代码：

```javascript
const myVar = process.env.MY_VAR;
console.log(myVar); // 输出 "Hello World"
```

请注意，您需要使用与 shell 脚本中设置变量名称相同的 `key` 来访问环境变量。在上面的示例中，我们使用 `MY_VAR` 作为变量的名称。然后，在 JavaScript 中，我们使用 `process.env.MY_VAR` 来检索变量的值。

