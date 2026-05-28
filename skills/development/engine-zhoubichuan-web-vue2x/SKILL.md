---
lang: zh-CN
sidebarDepth: 2
meta:
  - name: description
    content: 个人总结的vuepress学习技术文档-语法
  - name: keywords
    content: vuepress,最新技术文档,vuepress语法,markdown语法
---

# 静态页面（编码技巧）

::: tip 前言
总结一些开发中常见的问题，优化改善编码技巧，提高代码质量

:::

## 1.条件判断

```js
// 1.if/else 判断
// let name = "case1"
// if (name === "case1") {
// // 执行逻辑1
// } else if (name === "case2") {
// // 执行逻辑2
// } else if (name === "case3") {
// // 执行逻辑3
// }

// 2.switch/case 判断
// switch (name) {
// case "case1":
//     // 执行逻辑1
//     break
// case "case2":
//     // 执行逻辑2
//     break
// case "case3":
//     // 执行逻辑3
//     break
// }

let name = "case2"
let obj = {
  case1: function () {
    // 执行逻辑1
  },
  case2: function () {
    // 执行逻辑2
  },
  case3: function () {
    // 执行逻辑3
  },
}
let age = obj[name]()
```

::: warning 注意
以上这种技巧适用于循环判断一次赋值的情况，如果判断过后有较多处理逻辑的还需要使用 if 或 switch 等方法。
:::

## 2.生成数组

- Array.from

  ```js
  // let hours = []
  // for (let i = 0; i < 24; i++) {
  //   hours.push(i + "时")
  // }
  // ["0时", "1时", "2时", "3时", "4时", "5时", "6时", "7时", "8时", "9时", …]

  let hours = Array.from({ length: 24 }, (value, index) => index + "时")
  // ["0时", "1时", "2时", "3时", "4时", "5时", "6时", "7时", "8时", "9时", …]
  ```

## 3.按需加载

### 3.1 路由按需加载

- 常见加载页面方式

  ```js {6}
  // import home from'@/page/index/index'
  ...
  {
    path: '/index',
    // component: home,
    component: () => import('@/page/index/index'), // 推荐使用异步方式按需加载
    name: '首页'
  }
  ...
  ```

### 3.2 页面组件按需加载

页面中按需加载组件（可结合`component`）

## 4.按需渲染

在 Vue 页面中，一些模块可能需要用户主动触发才会显示，比如弹框组件等这样的子组件，那么我们可以使用 `v-if` 来进行按需渲染，没必要一进页面就渲染所有模块

## 5.路由跳转

::: danger 不推荐

- 直接调用原生 js API，会导致跳转到加载过的页面每次都是重新加载

  ```js
  location.href = "/home"
  location.hash = "/home"
  ```

  :::

- vue 中可以使用`path`：优于以上方式，当路径不变，路由方式修改不会影响跳转结果

  ```js
  this.$router.push({ path: "home" })
  this.$router.replace({ query: { path: "home" } })
  ```

::: tip 推荐

- 使用`name`: 对于 path，name 使用起来就方便多了，因为其具有唯一性，即使我们修改了 path，还可以使用原来的 `name` 值进行跳转

  ```js
  this.$router.push({ name: "home" })
  ```

:::

## 6.全局混入

```js
app.mixin({
  beforeCreate() {
    console.log("我是全局mixin")
  },
})
```

## 7.computed

尽量使用 computed 代替 watch，computed 可以理解为懒加载版的 watch,使用 computed 可以提高性能

## 8.枚举字段

- 常见项目一些变量像全局变量一样散落在项目的各个地方，难以管理

  ```js
  localStorage.token = "xxx" // a.page
  localStorage.token = "xxx" // b.page
  localStorage.token = "xxx" // c.page
  ```

  ::: tip 推荐

  - 定义枚举字段

    ```js
    // types.js
    export const USER_NAME = "userName"
    export const TOKEN = "token" // 当需要修改变量名（token）时，直接修改文件中的值即可，无需修改使用它的页面，同时这也可以避免命名冲突等问题的出现
    ```

  - 引用枚举字段

    ```js
    import { USER_NAME, TOKEN } from "../types.js"
    sessionStorage[USER_NAME] = "张三"
    localStorage[TOKEN] = "xxx"
    ```

  :::

::: details 枚举用法的扩展-位运算

- 定义

```js
const SKILLS = {
  CSS: 1,
  JS: 1 << 1,
  HTML: 1 << 2,
  WEB_GL: 1 << 3,
}
let skills = 0
function addSkill(skill) {
  skills = skills | skill
}
addSkill(SKILLS.CSS)
addSkill(SKILLS.HTML)
addSkill(SKILLS.WEB_GL)
```

- 使用

```js
SKILLS.CSS & skills // 判断是否有css
```

:::

## 9.setInterval 问题

一般情况下我们在项目里不建议使用 `setInterval`，因为其会存在代码的执行间隔比预期小以及 “丢帧” 的现象，原因在于其本身的实现逻辑。很多人会认为 setInterval 中第二个时间参数的作用是经过该毫秒数执行回调方法，其实不然，其真正的作用是**经过该毫秒数将回调方法放置到队列中去**，但是如果队列中存在正在执行的方法，其会等待之前的方法完毕再执行，如果存在还未执行的代码实例，其不会插入到队列中去，也就产生了 “丢帧”。

而 setTimeout 并不会出现这样的现象，因为每一次调用都会产生了一个新定时器，同时在前一个定时器代码执行完之前，不会向队列插入新的定时器代码。

```js
setInterval(() => {
  // 该定时器实际会在 3s 后立即触发下一次回调
  // 执行完这里的代码需要 2s
}, 1000)
let doSometing = () => {
  // 使用 setTimeout 改写，4秒后触发下一次回调
  // 执行完这里的代码需要 2s
  setTimeout(doSometing, 1000)
}
doSometing()
```

## 10.for in 问题

- 常规操作没有问题

  ```js
  let arr = [1, 2]
  for (let key in arr) {
    console.log(arr[key]) // 会正常打印 1, 2
  }
  ```

  ::: warning 注意

  - 添加自定义属性，会有问题

  ```js
  Array.prototype.test = function () {} // 在 Array 原型链上添加一个方法
  for (let key in arr) {
    console.log(arr[key]) // 此时会打印 1, 2, ƒ () {}
  }
  ```

  因为我们不能保证项目代码中不会对数组原型链进行操作，也不能保证引入的第三方库不对其进行操作，所以不要使用 for in 循环来遍历数组。
  :::

## 11.清除定时器

```vue
<template>
  <span>秒：{{ time }}</span>
</template>
<script>
export default {
  data() {
    return {
      time: new Date().getSeconds(),
    }
  },
  methods: {
    getTime() {
      let timer = setInterval(() => {
        this.time = new Date().getSeconds()
      }, 1000)
      // 方式一
      this.$on("hooks:beforeDestory", () => {
        clearInterval(timer)
        timer = null
      })
      // 方式二
      // this.$on("hooks:destoryed", () => {
      //   clearInterval(timer);
      //   timer = null;
      // });
    },
  },
  mounted() {
    this.getTime()
  },
}
</script>
```

## 12.复用代码

在 Vue 中，页面都可以看作是由大大小小的模块构成的，即便是一行代码、一个函数、一个组件都可以看作是一个个自由的模块。那么提高代码的复用性的关键便在于编写可复用的模块，也就是编写可复用的代码、函数和组件等。

- 使用变量的赋值缓存使用来解决数据的重复

  > ```js {4}
  > let person = []
  > for (let i = 0; i < data.obj.items.length; i++) {
  >   person.push({
  >     name: data.obj.items[i].name, // 出现了重复性的代码片段 data.obj.items
  >     age: data.obj.items[i].age,
  >   })
  > }
  > ```
  >
  > 上述代码一旦需要修改变量 `items` 为 `lists`，那么我们就得修改 3 处地方，不知不觉就增加了维护成本
  >
  > ```js {2}
  > let person = []
  > let values = data.obj.items // 通过变量 values 实现了复用，不管是维护成本还是代码可读性上，复用的优势都显而易见
  > for (let i = 0; i < values.length; i++) {
  >   person.push({
  >     name: values[i].name,
  >     age: values[i].age,
  >   })
  > }
  > ```

- 使用公共方法来解决功能的重复

  > ```js {5,6}
  > <tempalte>
  >    <div>
  >        <input type="text" v-model="str1">
  >        <input type="text" v-model="str2">
  >        <div>{{ str1.slice(1).toUpperCase() }}</div>
  >        <div>{{ str2.slice(1).toUpperCase() }}</div> // toUpperCase，大写字母转化功能点的重复
  >    </div>
  > </template>
  > ```
  >
  > 重复书写相同功能的代码是一种不经过大脑思考的行为，我们需要对其进行优化，这里我们可以把功能点封装成一个函数,在用到该方法的地方调用即可
  >
  > ```js
  > export default {
  >   methods: {
  >     sliceUpperCase(val) {
  >       return val.slice(1).toUpperCase()
  >     },
  >   },
  > }
  > ```

  像在双花括号插值和 v-bind 表达式中重复的功能点，我们可以封装成过滤器使用更加合适

  > ```js
  > // 单文件组件注册过滤器
  > filters: {
  >    sliceUpperCase(val) {
  >        return val.slice(1).toUpperCase()
  >    }
  > }
  > // 全局注册过滤器
  > Vue.filter('sliceUpperCase', function (val) {
  >    return val.slice(1).toUpperCase()
  > })
  > ```
  >
  > 然后在 模板 中使用“管道”符进行过滤：
  >
  > ```js
  > <div>{{ str1 | toUpperCase }}</div>
  > <div>{{ str2 | toUpperCase }}</div>
  > ```

  这样我们就把重复的功能性代码封装成了函数，而不管是过滤器还是正常的方法封装，其本质都是函数的封装。

- 组件封装

  相比较于函数的封装，规模更大一点的便是组件的封装，组件包含了模板、脚本以及样式的代码，在实际开发中组件的使用频率也是非常大的，我们项目中的每一个页面其实都可以看作是一个父组件，其可以包含很多子组件，子组件通过接收父组件的值来渲染页面，父组件通过响应子组件的回调来触发事件。

  封装一个组件主要包含两种方式，一种是最常见的整体封装，用户通过改变数据源来呈现不同的页面状态，代码结构不可定制化。例如：

  ```js
  <div>
    <my-component data="我是父组件传入子组件的数据"></my-component>
  </div>
  ```

  另一种便是自定义封装，也就是插槽(slot)，我们可以开放一部分槽位给父组件，使其能够进行一定程度的定制化，例如：

  ```js
  <div>
    <my-component data="我是父组件传入子组件的数据">
      <template slot="customize">
        <span>这是定制化的数据</span>
      </template>
    </my-component>
  </div>
  ```

  在 myComponent 组件中我们便可以接收对应的 slot：

  ```js
  <div class="container">
      <span>{{ data }}</span>
      <slot name="customize"></slot>
  <div>
  ```

  这里我们通过定义 slot 标签的 name 值为 customize 来接收父组件在使用该组件时在 template 标签上定义的 slot="customize" 中的代码，不同父组件可以定制不同的 slot 代码来实现差异化的插槽。最终渲染出来的代码如下：

  ```js
  <div>
    <div class="container">
      <span>我是父组件传入子组件的数据</span>
      <span>这是定制化的数据</span>
    </div>
  </div>
  ```

  这样我们就完成了一个小型组件的封装，将共用代码封装到组件中去，页面需要引入的时候直接使用 import 并进行相应注册即可，当然你也可以进行全局的引入：

  ```js
  import myComponent from "../myComponent.vue"
  // 全局
  Vue.component("my-component", myComponent)
  ```

- 插件封装

  在某些情况下，我们封装的内容可能不需要使用者对其内部代码结构进行了解，其只需要熟悉我们提供出来的相应方法和 api 即可，这需要我们更系统性的将公用部分逻辑封装成插件，来为项目添加全局功能，比如常见的 loading 功能、弹框功能等。

  > 编写插件
  >
  > ```js
  > /* toast.js */
  > import ToastComponent from "./toast.vue" // 引入组件
  > let $vm
  > export default {
  >   install(Vue, options) {
  >     if (!$vm) {
  >       const ToastPlugin = Vue.extend(ToastComponent) // 创建一个“扩展实例构造器”
  >       $vm = new ToastPlugin({
  >         el: document.createElement("div"), // 声明挂载元素
  >       })
  >       document.body.appendChild($vm.$el) // 把 toast 组件的 DOM 添加到 body 里
  >     }
  >     let toast = (text, duration) => {
  >       // 给 toast 设置自定义文案和时间
  >       $vm.text = text
  >       $vm.duration = duration
  >       setTimeout(() => {
  >         // 在指定 duration 之后让 toast 消失
  >         $vm.isShow = false
  >       }, $vm.duration)
  >     }
  >     if (!Vue.$toast) {
  >       // 判断 Vue.$toast 是否存在
  >       Vue.$toast = toast
  >     }
  >     Vue.prototype.$toast = Vue.$toast // 全局添加 $toast 事件
  >   },
  > }
  > ```
  >
  > 注册插件
  >
  > ```js
  > import Toast from "@/widgets/toast/toast.js"
  > Vue.use(Toast) // 注册 Toast
  > ```
  >
  > 使用插件
  >
  > ```js
  > this.$toast("Hello World", 2000)
  > ```

  当然你也可以不使用 install 方法来编写插件，直接采用导出一个封装好的实例方法并将其挂载到 Vue 的原型链上来实现相同的功能。

## 11.require.context

- 批量导入组件

```js
const path = require("path")
const files = require.context("@/components", false, /\.vue$/)
const modules = {}
files.keys().forEach((key) => {
  const name = path.basename(key, ".vue")
  modules[name] = files(key).default || files(key)
})
components: modules
```

- require.context(directory,useSubdirectories,regExp)
- 接收三个参数:
  - directory：说明需要检索的目录
  - useSubdirectories：是否检索子目录
  - regExp: 匹配文件的正则表达式,一般是文件名

## 12.将对象转换为HTTP参数

```js
url + '?' + new URLSearchParams(params).toString()
```

::: tip 总结
掌握一些常见的 vue 开发技巧，写出更规范的代码
:::
