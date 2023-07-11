## tsconfig.json



### typeRoots

在TypeScript中，可以通过typeRoots选项为项目定义类型文件的搜索位置。该选项用于指定包含类型声明文件（.d.ts）的根目录。如果你使用了第三方库，并且这些库没有自己的类型声明文件，你就需要手动创建声明文件（或者从其他地方获取）并将它们放在typeRoots目录中。

typeRoots选项通常在tsconfig.json文件中进行配置。例如：

```
{
  "compilerOptions": {
    "typeRoots": ["./typings"]
  }
}
```

上面的例子中，将`"./typings"`目录作为默认的类型文件搜索路径。如果你想要添加多个位置，你可以简单地将它们添加到数组中：

```
{
  "compilerOptions": {
    "typeRoots": ["./typings", "./node_modules/@types"]
  }
}
```

上面的例子中，`"./typings"`和`"./node_modules/@types"`两个目录都会被搜索以寻找类型文件。

请注意，如果typeRoots选项未指定，则TypeScript只会在当前包含源代码的目录中搜索类型易声明文件。因此，如果使用了第三方库且未提供类型声明文件，则无法编译您的项目并会出现错误提示。使用typeRoots选项可以帮助您管理您的类型声明文件，使得您的项目更加容易维护和扩展。

### declaration

可以将其设置为 `true` 来让 tsc 自动生成相应的 `.d.ts` 文件：

```js
"compilerOptions": {
  "declaration": true,
}
```

