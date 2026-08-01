---
name: fe-rule
description: const timer = setInterval(() => {}, 1000);
---

#1 @hook那些事儿

```vue
<script >
  export default {
    mounted () {
      const timer = setInterval(() => {}, 1000);
      this.$once('hook:beforeDestroy', () => clearInterval(timer));
    }
  }
</script>
```

> 组件生命周期hook，通常，您可以向中央监听子组件的生命周期（例如 `mounted`）

```html
<!-- 子组件 -->
<script>
export default {
  mounted () {
    this.$emit('on-mounted')
  }
}
</script>

<!-- 父组件 -->
<template>
  <child @on-mounted="handleMounted"/>
</template>

<!-- 或者 -->
<template>
  <child @hook:mounted="handleMounted"/>
</template>
```



#2 .sync语法糖

> sync 就是为了实现prop进行“双向绑定”仅此而已（父对子，子对父，来回传）

```vue
<template>
  <!--父组件-->
  <div>
    <child :num.sync="num"/>

    <!--等同于-->
    <child :num="num" @update:num="e => num = e"/>
  </div>
</template>

<script>
  import Child from './Child'

  export default {
    components: {
      Child
    },

    data () {
      return {
        num: 1
      }
    }
  }
</script>
```


```vue
<template>
  <!--子组件-->
  <div>
    <div>{{num}}</div>
    <button class="submit-btn" @click="onAdd">添加</button>
  </div>
</template>

<script>
  export default {
    name: 'Child',

    props: ['num'],

    methods: {
      onAdd() {
        this.$emit('update:num', 10)
      }
    }
  }
</script>
```

#3 路由按需加载

> 随着项目功能模块的增加，引入的文件数量剧增。如果不做任何处理，那么首屏加载会相当缓慢，这个时候，路由按需加载就闪亮登场了。

```js
const routes = [
  // webpack < 2.4
  {
    path: '/',
    name: 'home',
    components: resolve => require(['@/views/home'], resolve)
  },
  // webpack > 2.4
  {
    path: '/',
    name: 'home',
    components: () => import('@/views/home')
  }
]
```

#4 卸载watch观察

> 通常定义数据观察，会使用选项的方式 `watch` 中配置：

```js
    export default {
        data() {
            return {
                count: 1
            }
        },
        watch: {
            count(newVal) {
                console.log('count 新值：' + newVal)
            }
        }
    }
```

> 除此之外，数据观察还有另一种函数式定义的方式：

```js
    export default {
        data() {
            return {
                count: 1
            }
        },
        created() {
            this.$watch('count', function (newVal) {
                console.log('count 新值：' + newVal)
            })
        }
    }
```

> 它和前者的作用一样，但这种方式使定义数据观察更灵活，而且 `$watch` 会返回一个取消观察函数，用来停止触发回调：

```js
let unwatchFn = this.$watch('count', function(){
    console.log('count 新值：'+newVal)
})
this.count = 2 // log: count 新值：2
unwatchFn()
this.count = 3 // 什么都没有发生...
```

> `$watch` 第三个参数接收一个配置选项

```js
this.$watch('count', function(newVal){
    console.log('count 新值：'+ newVal)
}, {
    immediate: true // 立即执行watch
})
```

#5 巧用template

> 相信 v-if 在开发中是用得最多的指令，那么你一定遇到过这样的场景，多个元素需要切换，而且切换条件都一样，一般都会使用一个元素包裹起来，在这个元素上做切换。

```html
<div v-if="status === 'ok'">
    <h1>Title</h1>
    <p>Paragraph 1</p>
    <p>Paragraph 2</p>
</div>
```

> 如果像上面的div只是为了切换条件而存在，还导致元素层级嵌套多一层，那么它没有存在的意义。我们都知道在声明页面模板时，所有元素需要放在 `<template>` 元素内，除此之外，它还能在模板内使用， `<template>` 元素作为不可见的包裹元素，只是在运行时做处理，最终的渲染结果并不包含它。

```html
<template>
    <div>
        <template v-if="status==='ok'">
          <h1>Title</h1>
          <p>Paragraph 1</p>
          <p>Paragraph 2</p>
        </template>
    </div>
</template>
```

> 同样的，我们也可以在 `<template>` 上使用 `v-for` 指令，这种当时还能解决 `v-for` 和 `v-if` 同时使用报出的警告问题。

```html
<template v-for="item in 10">
    <div v-if="item % 2 == 0" :key="item">{{item}}</div>
</template>
```

#6 深层选择器

> 有时，你需要修改第三方组件的CSS，这些都是`scoped`样式，移除`scoped`或打开一个新的样式是不可能的。现在，深层选择器`>>>` `/deep/` `::v-deep`可以帮助你。

```html
<style scoped>
>>> .scoped-third-party-class {
  color: gray;
}
</style>

<style scoped>
/deep/ .scoped-third-party-class {
  color: gray;
}
</style>

<style scoped>
::v-deep .scoped-third-party-class {
  color: gray;
}
</style>
```

#7 高级watcher

> 立即执行。当被监控的prop发生突变时，watch handler就会触发。但有时，它是在组件被创建后才出现的。是的，有一个简单的解决办法：在 `created` 的钩子中调用处理程序，但这看起来并不优雅，同时也增加了复杂性。或者，你可以向观察者添加 `immediate` 属性：

```js
export default {
  watch: {
    value: {
      handler: 'printValue',
      immediate: true
    }
  },

  methods: {
    printValue () {
      console.log(this.value)
    }
  }
}
```

> 深度监听。有时，watch是属性是一个对象，但是其属性突变无法触发watcher处理程序。在这种情况下，为观察者添加 `deep:true` 可以使用属性的突变可检测到。请注意，当对象具有多个层时，深层可能会导致一些严重的性能问题。最好考虑使用更扁平的数据解构。

```js
export default {
  data () {
    return {
      value: {
        one: {
          two: {
            three: 3
          }
        }
      }
    }
  },

  watch: {
    value: {
      handler: 'printValue',
      deep: true
    }
  },

  methods : {
    printValue () {
      console.log(this.value)
    }
  }
}
```

> 多个handlers。实际上，watch可设置为数组，支持的类型为 String、Function、Object。触发后，注册的watch处理程序将被一一调用。

```js
export default {
    watch: {
      value: [
        'printValue',
        function (val, oldVal) {
          console.log(val)
        },
        {
          handler: 'printValue',
          deep: true
        }
      ]
    },
    methods : {
      printValue () {
        console.log(this.value)
      }
    }
}
```

> 订阅多个变量突变。`watcher`不能监听多个变量，但我们可以将目标组合在一起作为一个新的 `computed`，并监视这个新的“变量”。

```js
export default {
  computed: {
    multipleValues () {
      return {
        value1: this.value1,
        value2: this.value2,
      }
    }
  },

  watch: {
    multipleValues (val, oldVal) {
      console.log(val)
    }
  }
}
```

#8 路由器参数解耦

> 我相信这是大多数人处理组件中路由器参数的方式：

```js
export default {
  methods: {
    getRouteParamsId() {
      return this.$route.params.id
    }
  }
}
```

> 在组件内部使用 `$route` 会对某个URL产生耦合，这限制了组件的灵活性。正确的解决方案是路由器添加props。

```js
const Component = import('@/views/hello.vue');
const router = new VueRouter({
  routes: [{
    path: '/:id',
    component: Component,
    props: true
  }]
})
```

> 这样，组件可以直接从props获取 `params` 。

```js
export default {
  props: ['id'],
  methods: {
    getParamsId() {
      return this.id
    }
  }
}
```

> 此外，你还可以传入函数以返回自定义 `props`。

```js
const router = new VueRouter({
  routes: [{
    path: '/:id',
    component: Component,
    props: router => ({ id: route.params.id })
  }]
})
```
