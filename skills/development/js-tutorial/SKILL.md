---
name: js-tutorial
description: typeof操作符返回一个字符串，表示未经计算的操作数的类型；该运算符数据类型（返回字符串，对应列表如图）
---

### 一、数据类型检测
##### 1.1

typeof操作符返回一个字符串，表示未经计算的操作数的类型；该运算符数据类型（返回字符串，对应列表如图）

![image](https://user-gold-cdn.xitu.io/2019/3/8/1695b063b387ac39?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

###### 1.2 instanceof
```
var str = "This is a simple string";
var num = 1111;
var boolean = true;
var und = undefined;
var nl = null;
var sb = Symbol('1111');
var obj = {}; // 非原始类型数据字面量定义

console.log(str instanceof String);         // false
console.log(num instanceof Number);         // false
console.log(boolean instanceof Boolean);    // false
console.log(nl instanceof Object);          // false
console.log(sb instanceof Symbol);          // false
console.log(obj instanceof Object);         // true

var strN = new String("This is a simple string");
var numN = new Number(1111);
var booleanN = new Boolean(true);
var objN = new Object();

console.log(strN instanceof String);            // true
console.log(numN instanceof Number);            // true
console.log(booleanN instanceof Boolean);       // true
console.log(objN instanceof Object);            // true

```

instanceof运算符用于测试构造函数的prototype属性是否出现在对象的原型链中的任何位置； 由上结果，**字面量产出的原始数据类型无法使用instanceof判断**。

##### 1.3 Object.propotype.toString

```
Object.prototype.toString.call('string');       //"[object String]"
Object.prototype.toString.call(1111);           //"[object Number]"
Object.prototype.toString.call(true);           //"[object Boolean]"
Object.prototype.toString.call(null);           //"[object Null]"
Object.prototype.toString.call(undefined);      //"[object Undefined]"
Object.prototype.toString.call(Symbol('111'));  //"[object Symbol]"
Object.prototype.toString.call({});             //"[object Object]"

Object.prototype.toString.call('string').slice(8, -1);
// "String"
```

##### 1.4 constructor

比较对象的构造函数与类的构造函数是否相等

```
var a = {}
a.constructor === Object     // true

var b = '111';
b.constructor === String    // true

var strN = new String('11111');
strN.constructor === String // true

var c = true;
c.constructor === Boolean   // true

var d = Symbol('symbol')
d.constructor === Symbol    // true

```

##### 1.5 propotype

比较对象的原型与构造函数的原型是否相等

```
var a = {}
a.__proto__ === Object.prototype     // true

var t = new Date();
t.__proto__ === Date.prototype      // true


var str = 'sting';
str.__proto__ === String.prototype  // true

var strN = new String('11111');
strN.__proto__ === String.prototype // true

```

### 二、数据特殊操作

#### 2.1 交换两个值
##### 2.1.1 利用一个数异或本身等于0和异或运算符合交换率
```
var a = 3;
var b = 4
a ^= b; // a = a ^ b
b ^= a;
a ^= b;

console.log(a, b);
```
##### 2.1.2 使用ES6解构赋值
```
let a = 1;
let b = 2;

[b, a] = [a, b];

console.log(a, b);
```

#### 2.2 小数取整

```
var num = 123.123

// 常用方法
console.log(parseInt(num)); // 123
// “双按位非”操作符
console.log(~~ num); // 123
// 按位或
console.log(num | 0); // 123
// 按位异或
console.log(num ^ 0); // 123
// 左移操作符
console.log(num << 0); // 123
```

#### 2.3 数字金额千分位格式化
##### 2.3.1 使用Number.prototype.toLocaleString()

```
var num = 123455678;
var num1 = 123455678.12345;

var formatNum = num.toLocaleString('en-US');
var formatNum1 = num1.toLocaleString('en-US');

console.log(formatNum); // 123,455,678
console.log(formatNum1); // 123,455,678.123
```

##### 2.3.2 使用正则表达式
```
var num = 123455678;
var num1 = 123455678.12345;

var formatNum = String(num).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
var formatNum1 = String(num1).replace(/\B(?=(\d{3})+(?!\d))/g, ',');

console.log(formatNum); // 123,455,678
console.log(formatNum1); // 123,455,678.12,345
```

### 三、对象数据常用操作

#### 3.1 深度克隆技巧

##### 3.1.1 JSON.stringify 转换成字符， JSON.parse重新生成JSON数据类型

```
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}
var obj = {
    number: 1,
    string: 'abc',
    bool: true,
    undefined: undefined,
    null: null,
    symbol: Symbol('s'),
    arr: [1, 2, 3],
    date: new Date(),
    userInfo: {
        name: 'Better',
        position: 'front-end engineer',
        skill: ['React', 'Vue', 'Angular', 'Nodejs', 'mini programs']
    },
    func: function () {
        console.log('hello better');
    }
}

console.log(deepClone(obj))
```

从打印结果可以得出以下结论：

1、undefined、symbol、function 类型直接被过滤掉了

2、date 类型被自动转成了字符串类型

##### 3.1.2 常用方式 简单递归

```
function deepClone(obj) {
    var newObj = obj instanceof Array ? [] : {};
    for (let i in obj) {
        newObj[i] = typeof obj[i] === 'object' ? deepClone(obj[i]) : obj[i]
    }
    return newObj;
}

var obj = {
    number: 1,
    string: 'abc',
    bool: true,
    undefined: undefined,
    null: null,
    symbol: Symbol('s'),
    arr: [1, 2, 3],
    date: new Date(),
    userInfo: {
        name: 'Better',
        position: 'front-end engineer',
        skill: ['React', 'Vue', 'Angular', 'Nodejs', 'mini programs']
    },
    func: function () {
        console.log('hello better');
    }
}

console.log(deepClone(obj))

```

从打印的结果来看，这种实现方式还存在很多问题：这种方式只能实现特定的object的深度复制（比如对象、数组和函数），不能实现null以及包装对象Number，String ，Boolean，以及Date对象，RegExp对象的复制。

#### 3.2 对象遍历方式

##### 3.2.1 for-in

```
function A() {
	this.a = 1
	this.b = 1
}

A.prototype = {
	c: 1,
	d: 2
}

var a = new A()

for(var i in a) {
    console.log(i)
}
// a b c d

```

由上打印结果可知，for-in 会遍历对象属性，包括原型链中的属性

##### 3.2.3 Object.keys()、 Object.values()

```
function A() {
	this.a = 1
	this.b = 1
}

A.prototype = {
	c: 1,
	d: 2
}

var a = new A()
var keys = Object.keys(a)
var values = Object.values(a)
console.log(keys, values)

```

由上结果可知，keys, values 返回一个给定对象自身可枚举属性数组,自身可枚举属性值的数组

### 四、数组常用操作
#### 4.1 数组去重

##### 4.1.1 Set 去重
```
var arr = [1,2,1,1,22,4,5,6];
arr1 = [...new Set(arr)];
```

##### 4.1.2 结合使用数组filter方法和indexOf()方法

```
var arr = [1, 2, 3, 2, 6, '2', 3, 1];
function uniqueArr (arr) {
    return arr.filter(function (ele, index, array) {
        // 利用数组indexOf()方法，返回找到的第一个值的索引
        // 如果数组元素的索引值与indexOf方法查找返回的值不相等，则说明该值重复了，直接过滤掉
        return array.indexOf(ele) === index;
    })
}
```

4.2 多维数组一行代码实现一维转换
```
var arr = [ [1, 2, 2], [3, 4, 5, 5], [6, 7, 8, 9, [11, 12, [12, 13, [14] ] ] ], 10];

var resultArr = arr.toString().split(',').map(Number);

console.log(resultArr); // [1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 9, 11, 12, 12, 13, 14, 10]
```

4.3 一行代码实现获取一个网页使用了多少种标签
```
[...new Set([...document.querySelectorAll('*')].map(node => node.tagName))].length;
```
#### 4.4 如何实现a == 1 && a == 2 && a == 3
##### 4.4.1  改写数组的toString方法
```
var a = [1, 2, 3];
// a.join = a.shift;
// a.valueOf = a.shift;
a.toString = a.shift;

console.log(a == 1 && a == 2 && a == 3); // true
```

原理：当复杂类型数据与基本类型数据作比较时会发生隐性转换，会调用toString()或者valueOf()方法

##### 4.4.2  改写对象的toString方法
```
var a = {
    value: 1,
    toString: function () {
        return a.value++;
    }
}
console.log(a == 1 && a == 2 && a == 3); // true
```

#### 4.5 统计字符串中相同字符出现的次数
```
var str = 'aaabbbccc66aabbc6';

var strInfo = str.split('').reduce((p, c) => (p[c]++ || (p[c] = 1), p), {});

console.log(strInfo); // {6: 3, a: 5, b: 5, c: 4}
```
#### 4.6 将类数组对象转成数组
##### 4.6.1 使用Array.prototype.slice
```
var likeArrObj = {
    0: 1,
    1: 2,
    2: 3,
    length: 3
}

var arr1 = Array.prototype.slice.call(likeArrObj); // 或者使用[].slice.call(likeArrObj);
console.log(arr1); // [1, 2, 3]
```
##### 4.6.2 使用Array.from
```
var likeArrObj = {
    0: 1,
    1: 2,
    2: 3,
    length: 3
}
var arr = Array.from(likeArrObj);
console.log(arr); // [1, 2, 3]
```

##### 4.6.3 使用Object.values
```
var likeArrObj = {
    0: 1,
    1: 2,
    2: 3,
    length: 3
}
likeArrObj = Object.values(likeArrObj)
// [1, 2, 3, 3]
Object.prototype.toString.call(likeArrObj).slice(8, -1) === "Array"
// true
```
