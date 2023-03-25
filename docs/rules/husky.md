## 前言

本文主要探索 git commit 时代码提交校验的实现，日常开发我们使用 git 来管理代码，而 git commit 校验的实现依赖于第三方插件 husky，commitlint，lint-staged等，他们各自都有特殊的功能，共同作用实现 git commit 提交校验。

注：要实现 git commit 校验应确保你已经安装并配置好了相关的代码格式校验工具，比如eslint，prettier等。如果你还不知道如何安装 eslint，推荐阅读我的另一篇文章：

## husky是什么

husky 是一个 Git Hook 工具。其实就是一个为 git 客户端增加 hook 的工具。将其安装到所在仓库（husky install）的过程中它会自动在 .git 目录下增加相应的钩子实现在 pre-commit 阶段就执行一系列流程保证每一个 commit 的正确性。可以理解为 husky 是 git 版本管理工具为开发者开放的一个开口，让我们可以在代码提交的前后阶段做自己的事情。

实现 git commit 提交校验其实是依赖于 githooks，即git 使用的挂钩（githooks ）。

Git Hooks 就是那些在 Git 执行特定事件（如commit、merge，push、receive等等）前后后触发运行的脚本，挂钩是可以放置在挂钩目录中的程序，可在git执行的某些点触发动作。如果你使用过 vue，那么可以将挂钩类比为 vue 的生命周期钩子函数。挂钩可以在 git 的不同阶段做不同的事情。

如果想了解 githooks 的相关内容，推荐你查看文章：

GitHook工具 - husky 介绍及使用，Husky 官方文档，Husky - GitHub

安装
```bash
npm install husky --save-dev
```

安装完成执行如下代码，初始化(生成) .husky 目录文件
```

npx husky install
```

.husky 文件用来存放需要被git 读取的钩子文件

commitlint是什么

commitlint 包含 @commitlint/cli 和 @commitlint/config-conventional 插件，

commitlint 用来校验 commit 提交内容的格式的正确性

安装
```
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

安装完成添加 commit-msg 钩子，执行如下代码添加：
```
npx husky add .husky/commit-msg
```

 将新增的 commit-msg 文件中的 undefined 替换为：

```
npx --no-install commitlint --edit "$1"
```

这个钩子的主要作用就是在执行 git commit 之前执行上面这条命令，判断 commit 提交信息格式的正确性，依赖于 commitlint.config.js 配置文件中配置的规则。

在项目根目录新建 commitlint.config.js 文件，内容如下：

```js
module.exports = {

  // 继承的规则

  extends: ['@commitlint/config-conventional'],

  // 定义规则类型

  rules: {

​    'body-leading-blank': [2, 'always'],

​    'footer-leading-blank': [1, 'always'],

​    'header-max-length': [2, 'always', 108],

​    'subject-empty': [2, 'never'],

​    'type-empty': [2, 'never'],

​    // type 类型定义，表示 git 提交的 type 必须在以下类型范围内

​    'type-enum': [

​      2,

​      'always',

​      [

​        'feat', // 新功能 feature

​        'fix', // 修复 bug

​        'docs', // 文档注释

​        'style', // 代码格式(不影响代码运行的变动)

​        'refactor', // 重构(既不增加新功能，也不是修复bug)

​        'perf', // 性能优化

​        'test', // 增加测试

​        'chore', // 构建过程或辅助工具的变动

​        'revert', // 回退

​        'build' // 打包

​      ]

​    ],

​    // subject 大小写不做校验

​    'subject-case': [0]

  }

}
```

现在你就可以按照配置的格式来提交你的代码了。


commit 时报错：

Please add rules to your commitlint.config.js - Getting started guide: https://commitlint.

那么现在当你 git commit 时必须严格安装规定的格式来提交你的 commit，但是如果代码有错误依然可以提交成功。所以下面就针对 git commit 时代码格式进行校验

pre-commit 钩子

创建命令
```

npx husky add .husky/pre-commit
```

因为代码正确性校验是依赖于其他插件的，比如我自己项目使用 eslint，而eslint 的命令行执行方式就是在 package.json 文件 script 对象中定义的命令，将 pre-commit 文件中的 undefined 替换为触发命令行执行的命令，如：npm run serve，serve即是你在 script 对象中配置的命令，如下：
```js
// package.json   script对象

"scripts": {

  "serve": "vue-cli-service serve",

  "build": "vue-cli-service build",

  "lint:eslint": "eslint --ext .js,.vue src --fix"

},

```
pre-commit 文件

```

\#!/usr/bin/env sh

. "$(dirname -- "$0")/_/husky.sh"

 
npm run lint:eslint
```

现在当你每次提交代码都会对代码的正确性进行校验

但是存在一个问题，就是每次修改一个文件就给所有文件执行一次 lint 检查，如果你觉得无所谓可以忽略下面的内容。

如果你不想每次都对所有文件执行检查，那么可以使用 lint-staged 来实现这个功能

安装 lint-staged

安装
```

npm install --save-dev lint-staged
```

添加配置文件，在 .husky 文件中新增 lintstagedrc.js 文件，内容如下：
```js

module.exports = {

  '*.{js,jsx,ts,tsx}': ['eslint --fix', 'prettier --write'],

  '{!(package)**.json,**.code-snippets,.!(browserslist)*rc}': ['prettier --write--parser json'],

  'package.json': ['prettier --write'],

  '*.vue': ['eslint --fix', 'prettier --write'],

  '*.{scss,less,styl,html}': ['eslint --fix', 'prettier --write'],

  '*.md': ['prettier --write']

}
```

添加 lint-staged 的命令行执行方式，在package.json 文件 script 对象中添加：

"lint:staged": "lint-staged -c ./.husky/lintstagedrc.js --allow-empty"

-c 表示配置文件的路径

--allow-empty 表示默认情况下，当 linter 任务撤消所有暂存更改时，lint-staged 将退出并出错并中止提交。使用此标志允许创建空的 git 提交。

命令行配置及lint-staged 的详细内容请看：

lint-staged 使用教程

lint-staged - npm

修改 pre-commit 钩子中的命令行，改为执行 lint-staged，如下：

npm run lint:staged

现在你可以正常提交代码了

存在问题

基于上述的提交方式可能会存在问题，具体问题及解决方案详见：

vue 项目集成 husky+commitlint+stylelint

完善后的 pre-commit 文件

\#!/bin/sh

. "$(dirname "$0")/_/husky.sh"

. "$(dirname "$0")/common.sh"

 

[ -n "$CI" ] && exit 0

 

**# Check the file name**

**# ! ls-lint cannot be used normally in mac pro of M1 system.**

**# npm run lint:ls-lint**

 

**# Format and submit code according to lintstagedrc.js configuration**

yarn run lint:lint-staged

 

**# npm run lint:prettier**

————————————————