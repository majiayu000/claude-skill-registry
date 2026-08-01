---
name: basis
description: '> 来源：https://annatarhe.github.io/2016/04/19/hack-js-code.html'
---

# JavaScript小技巧

> 来源：https://annatarhe.github.io/2016/04/19/hack-js-code.html

## 类型转换

**1. 转为boolean**

```javascript
!!'foo' // true
!!0 //false
```

**2. 转为number**

```javascript
+'45'
+new Date //转为数字
```


***3. ~~*

~是一个按位取非的操作，返回数值的反码，是二进制操作，JavaScript中的number都是double类型的，在位操作的时候会转化为int，两次就还是原来的数

```javascript
~~3.1415 // 3 等同于parseInt()
~~5.678 //5
```

## IIFE

创建一个函数作用域，防止全局污染，

```javascript
(function (arg) {
    //作用域
});
```

## Closure

闭包：有权访问外部函数作用域的函数，作用是封装，保存变量的状态

```javascript
var counter = function() {
    counter = 0 ;
    return function() {
        return count++;
    }
}
```


