### React DOM Diff

React DOM Diff（差异算法）是 React 库中的核心算法之一，也被称为 Virtual DOM Diff 算法。它用于比较两棵虚拟 DOM 树的差异，找到最小的更新集合，并将这些更新应用到实际的 DOM 上，以实现高效的页面渲染。

React 的 Virtual DOM 是一个轻量级的 JavaScript 对象树，它是对实际 DOM 的抽象表示。当 React 应用中的数据发生变化时，React 会重新渲染整个虚拟 DOM 树，并生成一个新的虚拟 DOM 树。

在重新渲染后，React 会使用 Diff 算法比较新旧两棵虚拟 DOM 树，找到它们之间的差异。Diff 算法的目标是找到最小的差异，以便尽可能减少对实际 DOM 的操作，从而提高页面渲染性能。

Diff 算法的基本原理如下：

1. 深度优先遍历：首先，React 会从虚拟 DOM 树的根节点开始进行深度优先遍历，比较新旧节点的类型和属性。

2. 判断节点类型：当比较新旧节点时，React 会判断它们的类型是否相同。如果节点类型不同，React 将直接替换整个子树。如果节点类型相同，继续比较节点的属性。

3. 更新节点属性：对于相同类型的节点，React 会比较它们的属性。如果属性有变化，React 将更新实际 DOM 上的对应节点的属性。

4. 列表节点优化：当处理列表节点（例如数组映射为组件列表）时，React 会使用一种称为 "key" 的特殊属性来跟踪列表项的身份，以避免重新创建整个列表。

5. 递归遍历：React Diff 算法是递归的，它会继续比较子节点的差异，直到找到所有需要更新的节点。

通过使用 Diff 算法，React 能够高效地确定实际 DOM 的更新范围，并最小化对 DOM 的操作，从而提供快速的页面渲染和响应。

值得注意的是，虽然 React 的 Diff 算法在大多数情况下表现良好，但也有一些特殊情况下可能会引发性能问题。对于一些复杂的场景，可能需要手动优化渲染逻辑或使用 React 提供的一些优化措施，如 shouldComponentUpdate 方法或 React.memo()。

### 新生命周期

![react16_1626532331619](https://upload-markdown-images.oss-cn-beijing.aliyuncs.com/react16_1626532331619.jpg)

#### getDerivedStateFromProps

这个生命周期的功能实际上就是将传入的props映射到state上面

`getDerivedStateFromProps` 是 React 组件生命周期方法之一，在 React 16.3 版本中引入。它是一个静态方法（static method），用于在组件实例化或接收新的属性（props）时，根据新的属性计算和返回新的状态（state）。

在 React 16.3 版本之前，有一个旧的生命周期方法 `componentWillReceiveProps` 用于类似的目的，但由于它可能导致一些不可预料的行为，React 团队推荐使用更加明确和安全的 `getDerivedStateFromProps` 来代替。

`getDerivedStateFromProps` 方法在以下情况下会被调用：

1. 组件实例化时（初始化阶段）。
2. 组件接收新的属性（props）时。

它接收两个参数：

1. `props`：组件接收到的新属性。
2. `state`：组件当前的状态。

该方法应该返回一个对象，用于更新组件的状态（state）。返回的对象将会与现有的状态合并。

使用 `getDerivedStateFromProps` 需要谨慎，因为它可能导致一些副作用，例如可能在每次渲染时都触发新的状态更新，从而导致额外的渲染。在大多数情况下，组件的状态应该由用户交互、异步请求或其他生命周期方法来管理。

示例代码：

```javascript
class MyComponent extends React.Component {
  static getDerivedStateFromProps(nextProps, prevState) {
    // 根据新的属性计算并返回新的状态
    if (nextProps.value !== prevState.value) {
      return {
        value: nextProps.value
      };
    }
    return null; // 返回 null 表示不更新状态
  }

  constructor(props) {
    super(props);
    this.state = {
      value: props.value
    };
  }

  render() {
    return <div>{this.state.value}</div>;
  }
}
```

在上面的例子中，当组件接收到新的属性 `value` 时，会根据新的属性计算并更新状态 `value`。

总之，`getDerivedStateFromProps` 是一个用于根据新的属性计算和更新状态的 React 组件生命周期方法，它的使用需要慎重考虑。在大多数情况下，应该优先考虑使用组件内部的状态和其他生命周期方法来管理状态和副作用。

#### getSnapshotBeforeUpdate

`getSnapshotBeforeUpdate` 是 React 组件生命周期方法之一，在 React 16.3 版本中引入。它在组件更新前被调用，用于在实际 DOM 更新之前捕获组件更新前的信息（快照），并返回一个值，这个值将作为第三个参数传递给 `componentDidUpdate` 方法。

`getSnapshotBeforeUpdate` 方法在以下情况下会被调用：

1. 组件接收新的属性（props）和/或状态（state）并重新渲染之前。

它接收两个参数：

1. `prevProps`：组件更新前的属性。
2. `prevState`：组件更新前的状态。

该方法应该返回一个值，作为 `componentDidUpdate` 方法的第三个参数传递。返回的值可以是任意类型的数据，通常用于记录组件更新前的一些状态或信息。

`getSnapshotBeforeUpdate` 和 `componentDidUpdate` 通常一起使用，用于在组件更新前后进行一些额外的操作，例如保存滚动位置、获取 DOM 元素的信息等。

示例代码：

```javascript
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: props.value
    };
  }

  getSnapshotBeforeUpdate(prevProps, prevState) {
    // 在更新前捕获滚动位置
    if (prevProps.value !== this.props.value) {
      const container = document.getElementById('container');
      return container.scrollTop;
    }
    return null;
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    // 在更新后恢复滚动位置
    if (snapshot !== null) {
      const container = document.getElementById('container');
      container.scrollTop = snapshot;
    }
  }

  render() {
    return <div id="container">{this.props.value}</div>;
  }
}
```

在上面的例子中，当组件接收到新的属性 `value` 并更新之前，`getSnapshotBeforeUpdate` 方法被调用，捕获滚动位置并返回。在 `componentDidUpdate` 方法中，我们检查快照并在组件更新后恢复滚动位置。

总之，`getSnapshotBeforeUpdate` 是一个用于在组件更新前捕获信息并返回值的 React 组件生命周期方法。它通常和 `componentDidUpdate` 一起使用，用于在组件更新前后执行一些操作。使用时需要考虑副作用和状态管理的问题。

### Context

Context 是 React 中一种用于在组件树中共享数据的机制。它能够让数据在组件之间传递，而无需手动通过 props 层层传递。Context 在一些特定情况下非常有用，例如当多个组件需要访问相同的全局数据时。

Context 包含两个主要部分：Provider 和 Consumer。

1. Provider：Context Provider 是一个组件，负责将数据传递给其子组件。它通过 `value` 属性将数据提供给子组件，子组件可以通过 `Consumer` 组件来访问这些数据。

2. Consumer：Context Consumer 是一个组件，用于接收来自 `Provider` 的数据。它需要一个函数作为子元素，这个函数接收 `value` 属性作为参数，然后使用这些数据渲染子组件。

使用 Context 的基本步骤如下：

1. 创建 Context：使用 `React.createContext()` 方法创建一个 Context 对象。

```javascript
const MyContext = React.createContext(defaultValue);
```

2. 创建 Provider：创建一个 Context Provider 组件，并使用 `value` 属性将数据传递给其子组件。

```javascript
function MyProvider(props) {
  const someData = "Hello from Context!";
  return (
    <MyContext.Provider value={someData}>
      {props.children}
    </MyContext.Provider>
  );
}
```

3. 使用 Consumer：在需要访问 Context 数据的组件中，使用 `Consumer` 组件。

```javascript
function MyComponent() {
  return (
    <MyContext.Consumer>
      {value => <div>{value}</div>}
    </MyContext.Consumer>
  );
}
```

4. 将 Provider 包裹在组件树中：将创建的 Provider 组件包裹在应用的根组件下，以便所有子组件都可以访问 Context 数据。

```javascript
function App() {
  return (
    <MyProvider>
      <MyComponent />
    </MyProvider>
  );
}
```

在上面的示例中，`MyComponent` 组件通过 `Consumer` 组件访问了 `MyContext` 提供的数据。

需要注意的是，如果在应用中没有找到匹配的 `Provider`，`Consumer` 组件会使用 `createContext` 方法的 `defaultValue` 参数提供的默认值。而且，`Consumer` 组件必须位于 `Provider` 组件的子组件树中，否则将无法访问到 Context 的数据。

Context 的使用可以避免在组件之间传递大量的 props，但也应谨慎使用。在某些情况下，过度使用 Context 可能会导致组件之间的耦合性增加，不利于代码的维护和重构。因此，建议在真正需要在多个组件之间共享数据时再使用 Context。

### 高阶组件

高阶组件（Higher-Order Component，HOC）是一种在 React 中用于复用组件逻辑的模式。它是一个函数，接收一个组件作为参数，并返回一个新的组件。通过高阶组件，我们可以将共用的逻辑从组件中提取出来，从而实现代码的复用和简化。

高阶组件的主要用途包括：

1. 代码复用：高阶组件可以将共用的逻辑封装在一个函数中，然后通过传入不同的组件来复用该逻辑，避免代码重复。

2. 功能增强：通过高阶组件，可以增强组件的功能，例如添加状态管理、添加生命周期钩子、添加错误处理等。

3. 条件渲染：高阶组件可以根据特定的条件来决定是否渲染原始组件，从而实现条件渲染的效果。

使用高阶组件的一般步骤如下：

1. 定义高阶组件函数：创建一个函数，接收一个组件作为参数，并返回一个新的组件。

2. 在高阶组件中添加逻辑：在高阶组件函数内部，可以添加任何共用的逻辑或增强组件的功能。

3. 返回新的组件：在高阶组件函数中，返回一个新的组件，这个组件包裹了传入的原始组件，并应用了定义的逻辑。

4. 使用高阶组件：将高阶组件作为包裹组件，传递给原始组件，从而使用高阶组件提供的逻辑。

示例代码：

```javascript
// 定义高阶组件函数
const withLogger = (WrappedComponent) => {
  return class extends React.Component {
    componentDidMount() {
      console.log(`Component ${WrappedComponent.name} mounted.`);
    }

    componentWillUnmount() {
      console.log(`Component ${WrappedComponent.name} will unmount.`);
    }

    render() {
      return <WrappedComponent {...this.props} />;
    }
  };
};

// 使用高阶组件
class MyComponent extends React.Component {
  render() {
    return <div>My Component</div>;
  }
}

const MyComponentWithLogger = withLogger(MyComponent);

// 渲染包裹了高阶组件的组件
ReactDOM.render(<MyComponentWithLogger />, document.getElementById('root'));
```

在上面的示例中，我们定义了一个名为 `withLogger` 的高阶组件，它将在组件挂载和卸载时打印日志。然后，我们将 `MyComponent` 组件通过 `withLogger` 高阶组件包裹起来，从而实现了对 `MyComponent` 组件的功能增强。

通过高阶组件，我们可以实现许多复用性强、功能强大的组件逻辑，将共用的代码从组件中提取出来，提高了代码的可维护性和可读性。

#### 感觉和 Vue 的插槽挺像的

对的！React 的高阶组件（HOC）和 Vue 的插槽（Slot）有一些相似之处，它们都是用于在组件中复用逻辑或在组件之间共享内容的机制。虽然在细节和实现上有些差异，但它们都是实现组件复用和抽象的常见模式。

以下是一些相似和不同之处：

相似之处：

1. 复用逻辑：高阶组件和插槽都允许将逻辑从一个组件抽离出来，并在多个组件中复用该逻辑，以避免代码的重复。

2. 组件增强：通过高阶组件和插槽，我们都可以增强组件的功能，为组件提供一些共同的行为或特性。

3. 灵活性：高阶组件和插槽都提供了一种灵活的机制，使得我们可以在不同组件之间共享内容或逻辑，而不需要直接修改组件的结构或逻辑。

不同之处：

1. 实现方式：高阶组件是一个接收组件作为参数并返回新组件的函数，因此它是在 React 组件层级上操作的。而插槽是在 Vue 组件模板中使用 `<slot>` 元素来插入内容，因此它是在 Vue 组件模板层级上操作的。

2. 数据传递：在高阶组件中，数据传递是通过 props 进行的，高阶组件通过 props 将逻辑注入到子组件中。而在 Vue 的插槽中，数据传递是通过父组件将内容插入到插槽中，在子组件中可以通过插槽的名称来获取内容。

3. 嵌套：Vue 的插槽支持嵌套，可以在父组件中定义多个插槽，并在子组件中使用不同的插槽名来接收内容。而 React 的高阶组件并不直接支持嵌套，虽然可以使用组合来实现类似的效果，但实现方式略有不同。

虽然高阶组件和插槽有相似的用途，但在实际使用中，选择使用哪种模式取决于您的开发环境、项目需求和个人偏好。在 React 中，高阶组件是一种强大的模式，而在 Vue 中，插槽是 Vue 提供的特有机制。无论哪种方式，它们都有助于提高组件的复用性和可维护性。

#### 支持装饰器

是的，高阶组件（HOC）在 React 中支持装饰器语法，这使得使用 HOC 更加简洁和优雅。装饰器是 ECMAScript 提案中的一项功能，允许开发者通过注释的方式来扩展或修改类或类的方法。装饰器语法在 React 社区中广泛应用于高阶组件的定义。

在 React 中，可以使用 `@` 符号来定义装饰器。装饰器应用在组件类之前，并作为函数包裹组件类，通常返回一个新的组件类或修改原始组件类。

使用装饰器语法定义高阶组件的一般步骤如下：

1. 定义高阶组件函数。

2. 在高阶组件函数前添加装饰器。

3. 在装饰器中传入被包装的组件类。

示例代码：

```javascript
// 定义高阶组件函数
const withLogger = WrappedComponent => {
  return class extends React.Component {
    componentDidMount() {
      console.log(`Component ${WrappedComponent.name} mounted.`);
    }

    componentWillUnmount() {
      console.log(`Component ${WrappedComponent.name} will unmount.`);
    }

    render() {
      return <WrappedComponent {...this.props} />;
    }
  };
};

// 使用装饰器定义高阶组件
@withLogger
class MyComponent extends React.Component {
  render() {
    return <div>My Component</div>;
  }
}

// 渲染组件
ReactDOM.render(<MyComponent />, document.getElementById('root'));
```

在上面的示例中，我们使用装饰器语法 `@withLogger` 来定义了一个名为 `MyComponent` 的高阶组件，它在组件挂载和卸载时打印日志。这样，我们可以在不修改原始组件代码的情况下，为组件增加功能。

需要注意的是，使用装饰器需要在 Babel 的配置中启用装饰器插件。在 Create React App 等脚手架中，通常已经默认启用了该插件。

装饰器语法使得高阶组件的定义更加简洁和可读，但有些开发者也认为装饰器的语法在一些场景下会导致代码可读性下降，因此在实际使用时需要根据团队的编码规范和个人偏好来决定是否使用装饰器。

##### 安装

```
npm i react-app-rewired customize-cra @babel/plugin-proposal-decorators -D
```

##### 修改package.json

```js
  "scripts": {
    "start": "react-app-rewired start",
    "build": "react-app-rewired build",
    "test": "react-app-rewired test",
    "eject": "react-app-rewired eject"
  }
```

##### config-overrides.js 

```js
const { override, disableEsLint, addDecoratorsLegacy } = require('customize-cra');

module.exports = override(
  disableEsLint(),
  addDecoratorsLegacy()
)
```

##### jsconfig.json

```js
{
  "compilerOptions": {
     "experimentalDecorators": true
  }
}
```

```js
import React from 'react';
import ReactDOM from 'react-dom';
const loading = message =>OldComponent =>{
    return class extends React.Component{
        render(){
            const state = {
                show:()=>{
                   console.log('show', message);
                },
                hide:()=>{
                     console.log('hide', message);
                }
            }
            return  (
                <OldComponent {...this.props} {...state} {...{...this.props,...state}}/>
            )
        }
    }
}
@loading('消息')
class Hello extends React.Component{
  render(){
     return <div>hello<button onClick={this.props.show}>show</button><button onClick={this.props.hide}>hide</button></div>;
  }
}
let LoadingHello  = loading('消息')(Hello);

ReactDOM.render(
    <LoadingHello/>, document.getElementById('root'));
```



#### 什么是 override

"Override" 是一个英语词汇，它表示在特定上下文中，用一个更具优先级或更具权威性的事物取代另一个事物。在计算机编程和软件开发领域中，"override" 通常指的是覆盖（或重写）已有的方法、属性或行为，以改变其默认行为或实现更特定的功能。

在面向对象编程中，"override" 通常用于描述子类（派生类）重新定义了继承自父类（基类）的方法或属性。子类的重写方法将覆盖父类的同名方法，从而在调用该方法时执行子类的实现而不是父类的实现。

例如，在 Java 中，可以通过在子类中声明与父类相同签名的方法来重写父类的方法：

```java
class Animal {
    void makeSound() {
        System.out.println("Animal makes a sound");
    }
}

class Dog extends Animal {
    @Override
    void makeSound() {
        System.out.println("Dog barks");
    }
}
```

在上面的例子中，`Dog` 类重写了 `Animal` 类的 `makeSound()` 方法，当调用 `makeSound()` 方法时，会执行 `Dog` 类的实现而不是 `Animal` 类的实现。

类似地，在其他编程语言中，如 C++, C#，Python 等，也有类似的机制，用于重写继承的方法。

除了面向对象编程中的方法覆盖外，"override" 在其他上下文中也可能有不同的含义。在不同的领域中，这个词可能有一些微妙的差异，具体含义需要根据具体情境来确定。在软件开发中，通常 "override" 指的是子类重写父类的方法或属性。

#### 反向继承

- 基于反向继承：拦截生命周期、state、渲染过程

```js
import React from 'react';
import ReactDOM from 'react-dom';
class Button extends React.Component{
    state = {name:'张三'}
    componentWillMount(){
        console.log('Button componentWillMount');
    }
    componentDidMount(){
        console.log('Button componentDidMount');
    }
    render(){
        console.log('Button render');
        return <button name={this.state.name} title={this.props.title}/>
    }
}
const wrapper = OldComponent =>{
    return class NewComponent extends OldComponent{
        state = {number:0}
        componentWillMount(){
            console.log('WrapperButton componentWillMount');
             super.componentWillMount();
        }
        componentDidMount(){
            console.log('WrapperButton componentDidMount');
             super.componentDidMount();
        }
        handleClick = ()=>{
            this.setState({number:this.state.number+1});
        }
        render(){
            console.log('WrapperButton render');
            let renderElement = super.render();
            let newProps = {
                ...renderElement.props,
                ...this.state,
                onClick:this.handleClick
            }
            return  React.cloneElement(
                renderElement,
                newProps,
                this.state.number
            );
        }
    }
}
let WrappedButton = wrapper(Button);
ReactDOM.render(
    <WrappedButton title="标题"/>, document.getElementById('root'));
```

### Render Props

Render Props 是一种在 React 中实现组件复用的模式，通过在组件中传递一个函数作为 prop，使得组件可以共享该函数的功能和数据。Render Props 模式使得组件之间的代码复用更加灵活，类似于高阶组件（HOC）的功能，但使用起来更直观和简单。

Render Props 的基本思想是将一个函数作为组件的 children prop（也可以是其他的 prop 名称）传递，然后在组件的 render 方法中调用该函数并返回其返回值。这样，子组件可以在调用函数时获取一些数据或功能，从而实现组件的复用和逻辑的共享。

示例代码：

```javascript
// 使用 Render Props 的父组件
class ParentComponent extends React.Component {
  render() {
    return (
      <div>
        <h1>Parent Component</h1>
        {/* 将 render 函数作为 children prop 传递给 ChildComponent */}
        <ChildComponent render={(count) => <p>Count: {count}</p>} />
      </div>
    );
  }
}

// 使用 Render Props 的子组件
class ChildComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      count: 0,
    };
  }

  handleIncrement = () => {
    this.setState((prevState) => ({
      count: prevState.count + 1,
    }));
  };

  render() {
    // 在 render 方法中调用传递的 render 函数，并传递子组件的状态 count
    return (
      <div>
        <button onClick={this.handleIncrement}>Increment</button>
        {this.props.render(this.state.count)}
      </div>
    );
  }
}

// 渲染父组件
ReactDOM.render(<ParentComponent />, document.getElementById('root'));
```

在上面的例子中，`ParentComponent` 是使用 Render Props 的父组件，`ChildComponent` 是使用 Render Props 的子组件。`ParentComponent` 将一个名为 `render` 的函数作为 `ChildComponent` 的 children prop 传递，该函数在 `ChildComponent` 的 render 方法中调用并传递子组件的状态 `count`。

通过 Render Props 模式，我们可以在 `ParentComponent` 中自由定义要渲染的内容，并在 `ChildComponent` 中共享 `count` 状态。这样，我们可以轻松地实现在不同场景下复用 `ChildComponent` 的功能，同时也使得 `ChildComponent` 更加可组合和灵活。

Render Props 是 React 中一种强大的模式，但也需要谨慎使用，避免过度使用和嵌套，以保持代码的可读性和维护性。

#### Render Props 为 children

上述例子用 render 作为 props 传递，还有一种方式是 children，也必须是函数

```jsx
import React from './react';
import ReactDOM from './react-dom';

class MouseTracker extends React.Component {
    constructor(props) {
        super(props);
        this.state = { x: 0, y: 0 };
    }

    handleMouseMove = (event) => {
        this.setState({
            x: event.clientX,
            y: event.clientY
        });
    }

    render() {
        return (
            <div onMouseMove={this.handleMouseMove}>
                {this.props.children(this.state)}
            </div>
        );
    }
}
ReactDOM.render(<MouseTracker >
    {
        (props) => (
            <div>
                <h1>移动鼠标!</h1>
                <p>当前的鼠标位置是 ({props.x}, {props.y})</p>
            </div>
        )
    }
</MouseTracker >, document.getElementById('root'));
```

### 也可以是 HOC

```jsx
import React from 'react';
import ReactDOM from 'react-dom';
function withTracker(OldComponent){
  return class MouseTracker extends React.Component{
    constructor(props){
        super(props);
        this.state = {x:0,y:0};
    }
    handleMouseMove = (event)=>{
        this.setState({
            x:event.clientX,
            y:event.clientY
        });
    }
    render(){
        return (
            <div onMouseMove = {this.handleMouseMove}>
               <OldComponent {...this.state}/>
            </div>
        )
    }
 }
}
//render
function Show(props){
    return (
        <React.Fragment>
          <h1>请移动鼠标</h1>
          <p>当前鼠标的位置是: x:{props.x} y:{props.y}</p>
        </React.Fragment>
    )
}
let HighShow = withTracker(Show);
ReactDOM.render(
    <HighShow/>, document.getElementById('root'));
```

### React memo 、PureComponent 避免不必要的渲染

```jsx
import React from './react';
import ReactDOM from './react-dom';
class ClassCounter extends React.PureComponent {
    render() {
        console.log('ClassCounter render');
        return <div>ClassCounter:{this.props.count}</div>
    }
}
function FunctionCounter(props) {
    console.log('FunctionCounter render'); debugger
    return <div>FunctionCounter:{props.count}</div>
}
const MemoFunctionCounter = React.memo(FunctionCounter);
class App extends React.Component {
    state = { number: 0 }
    amountRef = React.createRef()
    handleClick = () => {
        let nextNumber = this.state.number + parseInt(this.amountRef.current.value);
        this.setState({ number: nextNumber });
    }
    render() {
        return (
            <div>
                <ClassCounter count={this.state.number} />
                <MemoFunctionCounter count={this.state.number} />
                <input ref={this.amountRef} />
                <button onClick={this.handleClick}>+</button>
            </div>
        )
    }
}
ReactDOM.render(
    <App />, document.getElementById('root'));
```

#### memo

`React.memo` 是 React 中用于性能优化的一个高阶组件（Higher-Order Component，HOC）。它的作用类似于 `PureComponent` 或 `shouldComponentUpdate` 生命周期钩子，用于防止不必要的组件渲染，从而提高组件的性能。

当组件的 props 或 state 变化时，React 会重新渲染该组件，但在某些情况下，组件的 props 或 state 并不会影响组件的渲染结果，这时候就可以使用 `React.memo` 来避免不必要的重新渲染。

使用 `React.memo` 的步骤：

1. 导入 `React` 和 `React.memo`。

2. 将组件通过 `React.memo` 包裹，并返回一个新的优化后的组件。

3. 可选地传入第二个参数，该参数是一个比较函数，用于自定义对 props 的比较逻辑。

示例代码：

```jsx
import React from 'react';

// 需要优化的组件
const ExpensiveComponent = ({ data }) => {
  // 假设这里有复杂的计算或数据处理
  return <div>{data}</div>;
};

// 使用 React.memo 对组件进行优化
const MemoizedExpensiveComponent = React.memo(ExpensiveComponent);

// 父组件
const ParentComponent = () => {
  const [count, setCount] = React.useState(0);

  const handleIncrement = () => {
    setCount((prevCount) => prevCount + 1);
  };

  return (
    <div>
      <button onClick={handleIncrement}>Increment</button>
      {/* 使用优化后的组件 */}
      <MemoizedExpensiveComponent data={count} />
    </div>
  );
};
```

在上面的例子中，我们使用 `React.memo` 对 `ExpensiveComponent` 进行了优化，使得组件在 `data` 的值不变时不会重新渲染，从而避免了不必要的计算和渲染开销。

需要注意的是，`React.memo` 仅对 props 进行浅比较（shallow comparison），也就是说它只会对 props 的引用进行比较。如果传入组件的 props 是复杂对象或数组，需要确保在更新 props 时始终返回一个新的引用，否则可能导致 `React.memo` 失效。

`React.memo` 是一种简单且有效的性能优化方式，但并不是适用于所有情况的银弹。在使用时，需要根据具体的组件和应用场景来评估是否需要进行优化，以及是否需要自定义比较函数来满足特定的需求。在大型应用中，综合考虑多种优化方式可以帮助提高应用的性能和用户体验。

#### PureComponent

`PureComponent` 是 React 中用于性能优化的一个类组件，它是 `Component` 类的一个变体。与普通的 `Component` 不同，`PureComponent` 实现了自身的 `shouldComponentUpdate` 方法，并对组件的 props 和 state 进行了浅比较（shallow comparison）。当组件的 props 或 state 变化时，`PureComponent` 会在渲染之前自动进行比较，如果发现新的 props 或 state 和前一次的值相同，就会阻止不必要的重新渲染，从而提高组件的性能。

使用 `PureComponent` 的步骤：

1. 导入 `React`。

2. 继承 `PureComponent` 类，创建一个新的组件。

3. 在组件中实现 `render` 方法，并在其中定义组件的渲染逻辑。

示例代码：

```jsx
import React from 'react';

// 需要优化的组件
class ExpensiveComponent extends React.PureComponent {
  render() {
    const { data } = this.props;
    // 假设这里有复杂的计算或数据处理
    return <div>{data}</div>;
  }
}

// 父组件
const ParentComponent = () => {
  const [count, setCount] = React.useState(0);

  const handleIncrement = () => {
    setCount((prevCount) => prevCount + 1);
  };

  return (
    <div>
      <button onClick={handleIncrement}>Increment</button>
      {/* 使用优化后的组件 */}
      <ExpensiveComponent data={count} />
    </div>
  );
};
```

在上面的例子中，我们使用 `PureComponent` 对 `ExpensiveComponent` 进行了优化，使得组件在 `data` 的值不变时不会重新渲染，从而避免了不必要的计算和渲染开销。

与 `React.memo` 类似，`PureComponent` 也仅对 props 进行浅比较。如果传入组件的 props 是复杂对象或数组，需要确保在更新 props 时始终返回一个新的引用，否则可能导致 `PureComponent` 失效。

需要注意的是，虽然 `PureComponent` 可以帮助我们简化优化过程，但并不是适用于所有情况的最佳方案。在使用 `PureComponent` 时，需要仔细考虑组件的 props 和 state 是否适合进行浅比较，并根据具体情况选择是否使用 `PureComponent` 进行性能优化。在大型应用中，综合考虑多种优化方式可以帮助提高应用的性能和用户体验。

### React Portal

React Portal 是 React 中的一种特性，它允许将子组件渲染到父组件的 DOM 层次结构之外。通常，React 组件的渲染结果都会插入到其最近的父元素中，但在某些情况下，我们可能需要将组件渲染到 DOM 树中的其他位置，而不是组件本身的直接父元素。

React Portal 的主要用途是在组件的层级结构之外创建某些 UI 组件，以解决一些特定的布局或层叠问题。例如，可以使用 Portal 在 React 应用的根元素之外创建一个模态对话框、弹出提示或菜单等。

使用 React Portal 的步骤如下：

1. 导入 `ReactDOM` 模块，因为 Portal 需要使用 `ReactDOM.createPortal` 方法。

2. 在组件中使用 `ReactDOM.createPortal` 方法，将要渲染的子组件传递给它。

示例代码：

```javascript
import React from 'react';
import ReactDOM from 'react-dom';

// 定义子组件
const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="modal-overlay">
      <div className="modal">
        <button onClick={onClose} className="modal-close-button">
          X
        </button>
        {children}
      </div>
    </div>,
    document.getElementById('modal-root')
  );
};

// 在应用根组件中使用 Portal
class App extends React.Component {
  state = {
    isModalOpen: false,
  };

  handleToggleModal = () => {
    this.setState((prevState) => ({
      isModalOpen: !prevState.isModalOpen,
    }));
  };

  render() {
    return (
      <div>
        <button onClick={this.handleToggleModal}>Toggle Modal</button>
        <Modal isOpen={this.state.isModalOpen} onClose={this.handleToggleModal}>
          <h2>Modal Content</h2>
          <p>This is a modal dialog.</p>
        </Modal>
      </div>
    );
  }
}

// 渲染根组件
ReactDOM.render(<App />, document.getElementById('root'));
```

在上面的例子中，我们创建了一个 `Modal` 组件，并使用 `ReactDOM.createPortal` 将 `Modal` 渲染到根元素之外的 `modal-root` DOM 元素中。这样，`Modal` 组件就脱离了组件树的层级结构，可以在应用根元素之外渲染，从而实现模态对话框的效果。

需要注意的是，`ReactDOM.createPortal` 第一个参数是要渲染的子组件，第二个参数是目标 DOM 节点，这个目标节点必须是已经存在于 DOM 中的节点，通常是在应用的根节点之外的某个节点。在上面的例子中，我们将 `Modal` 渲染到一个具有 `id="modal-root"` 的 DOM 节点中。

使用 React Portal 可以解决一些特定场景下的布局问题，但需要注意使用时的上下文和目标节点，以避免可能导致的问题和错误。

#### 有点像 Vue 的插槽

React 的 Portal 和 Vue 的插槽（Slot）功能有相似之处，并且都是用于在组件层级结构之外渲染内容的机制。虽然在实现细节和语法上有些差异，但它们都实现了在组件之间共享内容的能力。

相似之处：

1. 组件内容渲染：React 的 Portal 和 Vue 的插槽都允许将组件的内容渲染到指定的位置或 DOM 节点中，而不受组件层级结构的影响。

2. 灵活性：两者都提供了一种灵活的机制，使得开发者可以在父组件中定义内容，并在子组件中插入这些内容，从而实现不同的布局和交互效果。

3. 复用性：React 的 Portal 和 Vue 的插槽都有助于组件内容的复用，可以将通用的内容定义在父组件中，并在多个子组件中共享。

差异之处：

1. 使用方式：React 的 Portal 是通过 `ReactDOM.createPortal` API 来实现的，需要在 JavaScript 中创建 Portal，并且需要显式地指定目标 DOM 节点。而 Vue 的插槽是在模板中使用 `<slot>` 元素，并且由 Vue 的编译器负责将内容插入到插槽中。

2. 目标节点：React 的 Portal 需要显式指定目标 DOM 节点，可以将组件的内容渲染到应用的根元素之外。而 Vue 的插槽将内容插入到父组件中预先定义的插槽位置，需要在父组件中声明插槽，并在子组件中使用。

综上所述，虽然 React 的 Portal 和 Vue 的插槽在实现和语法上有一些差异，但它们都是用于在组件之间共享内容或在指定位置渲染内容的功能，从而提高了代码的可维护性和可读性。选择使用哪种机制取决于开发者的项目需求和个人偏好。

```jsx
import React from './react';
import ReactDOM from './react-dom';
class Dialog extends React.Component {
    constructor(props) {
        super(props);
        this.node = document.createElement('div');
        document.body.appendChild(this.node);
    }
    render() {
        return ReactDOM.createPortal(
            <div className="dialog">
                {this.props.children}
            </div>,
            this.node
        );
    }
    componentWillUnmount() {
        window.document.body.removeChild(this.node);
    }
}
class App extends React.Component {
    render() {
        return (
            <div>
                <Dialog>模态窗</Dialog>
            </div>
        )
    }
}
ReactDOM.render(
    <App />, document.getElementById('root'));
```

