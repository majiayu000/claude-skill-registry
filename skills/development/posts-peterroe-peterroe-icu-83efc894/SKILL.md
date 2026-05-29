---
title: 思路不一样的高亮实现
date: 2022-07-06
duration: 2min
---

## 高亮的实现

我们知道，以`Vue`为例子，如果想要实现文字高亮效果，需要借助`v-html`进行模版渲染，例如：

在下面的代码中

```html
<script setup>
  const str = 'my name is peterroe'
  const keyWord = 'peterroe'
  const handleKeyWordHighlight = (s, k) => {     //希望高亮的文字
    const reg = new RegExp(k, 'g')
    return s.replace(reg, `<span class="highlight">${k}</span>`)
  }
</script>
<template>
  <div>
    <span v-html="handleKeyWordHighlight(str, keyWord)"></span>
  <div>
</template>
<style>
  .hight-light {
    background-color: yellow;
  }
</style>
```

效果：

<Split/>

***

### 其他实现方法

通常来说，不管是`vue`的`v-html`和`react`的`dangerouslySetInnerHTML`，还是原生的`innerHTML`的，操作是非常危险的。

> **假如现在不准用上面的这三个操作，你应该怎样实现高亮的效果呢？**

上面的这个问题实际上不是凭空捏造，而是本人碰到的真实场景，接下来我将使用`split`解决这个问题：

```html
<script setup>
  const str = 'my name is peterroe'
  const keyWord = 'peterroe'
  const handleKeyWordHighlight = (s, k) => {     //希望高亮的文字
    const reg = new RegExp(`(${k})`, 'g')
    return s.split(reg).map((item, index) => ({
      text: item,
      isKeyWord: item === k
    }))
  }
</script>
<template>
  <div>
    <span 
      v-for="item in handleKeyWordHighlight(str, keyWord)"
      :key="item.text"
      :class="{'highlight': item.isKeyWord}"
    >
      {{item.text}}
    </span>
  <div>
</template>
```

实现思路就是，将原始的文字分割成单词，然后每个单词都添加一个`class`，如果单词是高亮的，则添加`highlight`这个`class`，如果不是高亮的，则不添加这个`class`。

上面还用到了`split`一个不常用的技巧：

```ts
// 通常来说
'aabbcc'.split('bb') // ['aa', 'cc']
'aabbcc'.split(/bb/) // ['aa', 'cc']
// 用正则捕获
'aabbcc'.split(/(bb)/) // ['aa', 'bb', 'cc']
```

### 第三种方法

利用 Range Api

```html
<template>
  <div id="word">my name is peterroe</div>
</template>

<script setup lang="ts">
  const keyWord = 'name'
  const reg = new RegExp(keyWord)
  onMounted(() => {
    const textNode = document.querySelector('#word')?.childNodes[0]
    if(!textNode) return 

    const content = textNode?.textContent || ''

    const start = content.match(reg)?.index || 0
    const end = start + keyWord.length
    
    const range = document.createRange()
    range.setStart(textNode, start)
    range.setEnd(textNode, end)

    const highElm = document.createElement('span')
    highElm.setAttribute('class', 'high-light')
    range.surroundContents(highElm)
  })
</script>

<style>
.high-light {
  background-color: yellow;
}
</style>
```

---

<WebApiRange />

---