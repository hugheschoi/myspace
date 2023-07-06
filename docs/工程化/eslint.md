请帮我实现一个对 Vue 文件进行代码解析的 eslint 规则插件，它的具体分析流程如下：

1. 第一步，对 template 部分的代码，收集这些属性的引用变量，收集规则如下

   - Html 属性： label、title，比如 <div :title="title"></div>，找到变量 title，并收集起来
   - <s-input> 标签下的 placeholder 属性
   - <s-form-item> 标签的 label 属性
   - {{ }} 引用的变量，比如 <span>{{ test }}</span>, 找到变量 test，并收集起来

   在 template 模板中找到上述规则引用变量收集起来
   收集规则是 eslint 外部配置传入的

2. 将第一步在 template 收集的引用变量，第二部是解析 Script 部分，可能是 composition-api 写法，也可能是 vue-property-decorator 的写法，在 script 代码找到第一步在 template 收集的引用变量的赋值情况，有以下情况：

   - 如果赋值是字符串，则报错提示 "Need use $i8n"
   - 如果是对象或对象组成的数组，则观察对象内部的 label、title 属性是否被赋值为字符串，如果是字符串，则报错提示 "Need use $i8n"
   - 如果引用变量来自于组件接收的 Props，则将他们收集起来，console.log 出来