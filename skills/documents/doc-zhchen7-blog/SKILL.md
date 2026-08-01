---
name: doc
description: '> rem：利用它能实现强大的屏幕适配布局'
---

## 你一定要会的适配技巧和组件化思想

> rem：利用它能实现强大的屏幕适配布局
>
> less：Less 是一门 CSS 预处理语言，它扩展了 CSS 语言，增加了变量、Mixin、函数等特性，使 CSS 更易维护和扩展。(代表的有less，Sass，stylus)
>
> 模板引擎：art-template（实现组件化，代码不复用，提高开发效率）(当然还有很多其它好用的模板引擎，但原理上基本一样。)

## 说明

- 本文将介绍以rem（结合流式布局）+less（为代表）的适配方式
- 模板引擎上以将以art-template举例说明。（模板引擎 ==> 这里特指用于Web开发的模板引擎,是为了使[用户界面](https://baike.baidu.com/item/%E7%94%A8%E6%88%B7%E7%95%8C%E9%9D%A2)与业务数据（内容）分离而产生的，它可以生成特定格式的文档，用于网站的模板引擎就会生成一个标准的[HTML](https://baike.baidu.com/item/HTML)文档。）



## 需求分析

为什么 **rem+less** 会产生？

- **rem** ：<u>rem是相对长度单位，相对于根元素font-size计算值的倍数（通俗来讲，相对于html字体大小）</u>

  这种需求主要产生在移动端，因为随着科学水平的发展，手机产业发展非常迅速，作为一个前端工作者，大量的手机页面需要我们去书写，而现在市面上的手机大小不一（分辨率各不相同），一种适配所有手机的页面开发模式需求应由而生。（px为一种固定的像素单位，不太适合需求），之后**流式布局，响应式布局**等随之产生，rem的作用也逐渐凸显出来。

####   如何使用rem+less呢？

  ===>新建个less目录，在里面做如下操作：

1.新建 variable.less（名字随便都可以，反正这是一个表示变量的less文件）

```javascript
@charset "utf-8";
//适配主流设备
@adapterDeviceList:750px,720px,640px,540px,529px,480px,434px,414px,400px,384px,375px,360px,320px;
//设计稿尺寸
@psdwidth:529px;  //就是你参考的设计稿的尺寸
/*
    预设基准值
    我习惯设100px，这样感觉用起来比较方便。比如：32px可以写作32rem/@baseFontSize
*/
@baseFontSize:100px;

//设备种类数量
@len:length(@adapterDeviceList);
```



2.新建 mixins.less（这是一个表示函数的less文件）

~~~ javascript
/*
  这类似一个循环（定义一个函数），只是less没有跟js差不多的for循环啥滴，所以只能通过这种方式来实现一个循环。
*/
.adapterMixin(@index) when (@index > 0){
  @media (min-width: extract(@adapterDeviceList,@index)){
    html{
      font-size: @baseFontSize/@psdwidth* extract(@adapterDeviceList,@index);
    }
  }
  .adapterMixin(@index - 1);
}
~~~



3.新建 adapter.less（调用函数）

~~~javascript
.adapterMixin(@len);
~~~

4.新建 index.less (主入口)

~~~javascript
@charset "utf-8";
@import 'variable';
@import "mixins";
@import "adapter";
~~~

5.在网页中引用

~~~html
<link rel="stylesheet" type="text/less" href="/less/index.less">
<script src="//cdnjs.cloudflare.com/ajax/libs/less.js/3.9.0/less.min.js" ></script>
~~~

[less官网](http://lesscss.org/)

说明：在网页中直接引用less文件是不行的，一定要加一个less.min.js来解析less文件，这样浏览器才能认识。



在完成上述操作后，你已基本完成  **rem+less**的适配方式。接下来在less文件中 （像素单位px 将可以用  rem/@baseFontSize来代替），你的页面将适配所有大小的容器。



## 组件化思想

#### 需求分析：

> 随着要写大量的页面，页面的重复，冗杂等问题相应而出。为了解决这种重复的问题，组件化思想出来了。

#### 什么是组件化

  组件化并不是前端所特有的，一些其他的语言或者桌面程序等，都具有组件化的先例。确切的说，只要有UI层的展示，就必定有可以组件化的地方。简单来说，组件就是将一段UI样式和其对应的功能作为独立的整体去看待，无论这个整体放在哪里去使用，它都具有一样的功能和样式，从而实现复用，这种整体化的细想就是组件化。不难看出，组件化设计就是为了增加复用性，灵活性，提高系统设计，从而提高开发效率。





- css实现代码分离（组件化思想）：可以用 less，Sass，stylus。[less官网](http://lesscss.org/)
- html实现代码分离（组件化思想）：可以用模板引擎----如 [art-template](https://aui.github.io/art-template/docs/) 等...



> art-template 是一个简约、超快的模板引擎。它采用作用域预声明的技术来优化模板渲染速度，从而获得接近 JavaScript 极限的运行性能，并且同时支持 NodeJS 和浏览器。
>
> 1. 拥有接近 JavaScript 渲染极限的的性能
> 2. 调试友好：语法、运行时错误日志精确到模板所在行；支持在模板文件上打断点（Webpack Loader）
> 3. 支持 Express、Koa、Webpack
> 4. 支持模板继承与子模板
> 5. 浏览器版本仅 6KB 大小



详情介绍：   [art-template官网](https://aui.github.io/art-template/zh-cn/docs/index.html)





## 总结

1. 1.适配技巧和组件化思想是你必不可少的技能
2. 2.组件化思想将是未来主流方向（React、Vue、Angular三大前端主流框架）
3. 3.多做项目===>体会这种组件化开发思想和适配方案。

