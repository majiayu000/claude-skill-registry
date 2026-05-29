[1 String技巧](#1-String技巧)

[2 Number技巧](#2-Number技巧)

[3 Boolean技巧](#3-Boolean技巧)

[4 Array技巧](#4-Array技巧)

[5 Object技巧](#5-Object技巧)

[6 Function技巧](#6-Function技巧)

[7 DOM技巧](#7-DOM技巧)

# 1 String技巧

> 把值转换成String的5个方法

你最了解你的程序，因此你应该选择最适合你的方式。

```js
const value = 12345;

// Concat Empty String
value + '';

// Template Strings
`${value}`;

// JSON.stringify
JSON.stringify(value);

// toString()
value.toString();

// String()
String(value);

// RESULT
// '12345'

```

> 字符串插值

在用例中，如果正在构建一个基于模板的helper组件，那么这一点就会非常突出，它使动态模板连接容易得多。

```js
const user = {
  name: 'John',
  surname: 'Doe',
  details: {
    email: 'john@doe.com',
    displayName: 'SuperCoolJohn',
    joined: '2016-05-05',
    image: 'path-to-the-image',
    followers: 45
  }
}

const printUserInfo = (user) => { 
  const text = `The user is ${user.name} ${user.surname}. Email: ${user.details.email}. Display Name: ${user.details.displayName}. ${user.name} has ${user.details.followers} followers.`
  console.log(text);
}

printUserInfo(user);
// outputs 'The user is John Doe. Email: john@doe.com. Display Name: SuperCoolJohn. John has 45 followers.'

```

> 格式化金额

```js
const thousandNum = num => num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
const money = thousandNum(20190214);
```

> 生成随机ID

```js
const randomId = len => Math.random().toString(36).substr(3, len);
const id = randomId(10);

console.log(id) // jg7zpgiqva
```

> 生成随机HEX色值

```js
const randomColor = () => "#" + Math.floor(Math.random() * 0xffffff).toString(16).padEnd(6, "0");
const color = randomColor();
// color => "#f03665"
```

> 操作URL查询参数

```js
const params = new URLSearchParams(location.search.replace(/\?/ig, '')); // location.search = "?name=young&sex=male"
params.has("young"); // true
params.get("sex"); // "male"
```

> 生成星级评分

```js
const startScore = rate => "★★★★★☆☆☆☆☆".slice(5 - rate, 10 - rate);
const start = startScore(3);
// start => "★★★"
```

# 2 Number技巧

> 取整：代替正数的Math.floor()，代替负数的Math.ceil()

```js
const num1 = ~~ 1.69;
const num2 = 1.69 | 0;
const num3 = 1.69 >> 0;

// num1 num2 num3 => 1 1 1
```

> 补零

```js
const fillZero = (num, len) => num.toString().padStart(len, '0');
const num = fillZero(169, 5);

// num => "00169"
```

> 转数值：只对null、''、false、数值字符串有效

```js
const num1 = +null;
const num2 = +'';
const num3 = +false;
const num4 = +'169';
// num1 num2 num3 num4 => 0 0 0 169
```

> 时间戳

```js
const timestamp = +new Date('2019-02-14');
// timestamp => 1550102400000
```

> 精确小数

```js
const roundNum = (num, decimal) => Math.round(num * 10 ** decimal) / 10 ** decimal;
const num = roundNum(1.69, 1);
// num => 1.7
```

> 判断奇偶

```js
const oddEven = num => !!(num & 1) ? 'odd' : 'even';
const num = oddEven(2);
// num => 'even'

// 或
const isOdd = num => {num % 2}

// 或
const isOdd = num => num & 1
```

> 取最小最大值

```js
const arr = [0, 1, 2];
const min = Math.min(...arr);
const max = Math.max(...arr);
// min max => 0 2
```

> 生成范围随机数

```js
const randomNum = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const num = randomNum(1, 10);
```

# 3 Boolean技巧

> 短路运算符

```js
const a = d && 1; // 满足条件赋值：取假运算，从左到右依次判断，遇到假值返回假值，后面不再执行，否则返回最后一个真值
const b = d || 1; // 默认赋值：取真运算，从左到右依次判断，遇到真值返回真值，后面不再执行，否则返回最后一个假值
const c = !d; // 取假赋值：单个表达式转换为true则返回false，否则返回true

```

> 判断数据类型：undefined、null、string、number、boolean、array、object、symbol、date、regexp、function、asyncfunction、arguments、set、map、weakset、weakmap

```js
function dataType(tgt, type) {
  const dataType = Object.prototype.toString.call(tgt).replace(/\[object /g, '').replace(/\]/g, '').toLowerCase();
  return type ? dataType === type : dataType;
}
dataType('young'); // "string"
dataType(20190214); // "number"
dataType(true); // "boolean"
dataType([], 'array'); // true
dataType({}, 'array'); // false
```

> 是否为空数组

```js
const arr = [];
const flag = Array.isArray(arr) && !arr.length;
// flag => true
```

> 是否为空对象

```js
function dataType(tgt, type) {
  const dataType = Object.prototype.toString.call(tgt).replace(/\[object /g, "").replace(/\]/g, "").toLowerCase();
  return type ? dataType === type : dataType;
}

const obj = {};
const flag = dataType(obj, 'object') && !Object.keys(obj).length;
// flag => true
```

> 满足条件时执行

```js
function Func () {
  // doing...
}

const flagA = true; // 条件A
const flagB = false; // 条件B
(flagA || flagB) && Func(); // 满足A或B时执行
(flagA || !flagB) && Func(); // 满足A或不满足B时执行
flagA && flagB && Func(); // 同时满足A和B时执行
flagA && !flagB && Func(); // 满足A且不满足B时执行

```

> 为非假值时执行

```js
function Func () {
  // doing...
}

const flag = false; // undefined、null、''、0、false、NaN
!flag && Func();

```

> 数组不为空时执行

```js
function Func () {
  // doing...
}

const arr = [0, 1, 2];
arr.length && Func();
```

> 对象不为空时执行

```js
function Func () {
  // doing...
}

const obj = {a: 0, b: 1, c: 2};
Object.keys(obj).length && Func();
```

> 函数退出代替条件分支退出

```js
function Func () {
  // doing...
}

const flag = true;

if (flag) {
  Func();
  return false;
}

// 换成
if (flag) {
  return Func();
}

```

> switch/case使用区间

```js
const age = 26;
switch (true) {
  case isNaN(age):
    console.log("not a number");
    break;
  case (age < 18):
    console.log("under age");
    break;
  case (age >= 18):
    console.log("adult");
    break;
  default:
    console.log("please set your age");
    break;
}
```

# 4 Array技巧

> 获取数组唯一值

ES6 提供了从数组中提取唯一值的两种非常简洁的方法。不幸的是，它们不能很好地处理非基本类型的数组。在本文中，主要关注基本数据类型。

```js
const cars = ['Mazda', 'Ford', 'Renault', 'Opel', 'Mazda'];
const uniqueWithArrayFrom = Array.from(new Set(cars));
console.log(uniqueWithArrayFrom); // outputs ['Mazda', 'Ford', 'Renault', 'Opel']

const uniqueWithSpreadOperator = [...new Set(cars)];
console.log(uniqueWithSpreadOperator); // outputs ['Mazda', 'Ford', 'Renault', 'Opel']
```
> 使用展开运算符合并对象和对象数组

对象合并是很常见的事情，我们可以使用新的ES6特性来更好，更简洁的处理合并的过程。

```js
// merging objects
const product = { name: 'Milk', packaging: 'Plastic', price: '5$' }
const manufacturer = { name: 'Company Name', address: 'The Company Address' }

const productManufacturer = { ...product, ...manufacturer };
console.log(productManufacturer); 
// outputs { name: "Company Name", packaging: "Plastic", price: "5$", address: "The Company Address" }

// merging an array of objects into one
const cities = [
    { name: 'Paris', visited: 'no' },
    { name: 'Lyon', visited: 'no' },
    { name: 'Marseille', visited: 'yes' },
    { name: 'Rome', visited: 'yes' },
    { name: 'Milan', visited: 'no' },
    { name: 'Palermo', visited: 'yes' },
    { name: 'Genoa', visited: 'yes' },
    { name: 'Berlin', visited: 'no' },
    { name: 'Hamburg', visited: 'yes' },
    { name: 'New York', visited: 'yes' }
];

const result = cities.reduce((accumulator, item) => {
  return {
    ...accumulator,
    [item.name]: item.visited
  }
}, {});

console.log(result);
/* outputs
Berlin: "no"
Genoa: "yes"
Hamburg: "yes"
Lyon: "no"
Marseille: "yes"
Milan: "no"
New York: "yes"
Palermo: "yes"
Paris: "no"
Rome: "yes"
*/

```

> 数组 map 的方法 (不使用Array.Map)

另一种数组 map 的实现的方式，不用 Array.map。

Array.from 还可以接受第二个参数，作用类似于数组的map方法，用来对每个元素进行处理，将处理后的值放入返回的数组。如下：

```js
const cities = [
    { name: 'Paris', visited: 'no' },
    { name: 'Lyon', visited: 'no' },
    { name: 'Marseille', visited: 'yes' },
    { name: 'Rome', visited: 'yes' },
    { name: 'Milan', visited: 'no' },
    { name: 'Palermo', visited: 'yes' },
    { name: 'Genoa', visited: 'yes' },
    { name: 'Berlin', visited: 'no' },
    { name: 'Hamburg', visited: 'yes' },
    { name: 'New York', visited: 'yes' }
];

const cityNames = Array.from(cities, ({ name}) => name);
console.log(cityNames);
// outputs ["Paris", "Lyon", "Marseille", "Rome", "Milan", "Palermo", "Genoa", "Berlin", "Hamburg", "New York"]

```

> 克隆数组

```js
const arr1 = [0, 1, 2];
const arr2 = [...arr1];
// arr2 => [0, 1, 2]

```

> 合并数组

```js
const arr1 = [0, 1, 2];
const arr2 = [3, 4, 5];
const arr = [...arr1, ...arr2];
// arr => [0, 1, 2, 3, 4, 5];

```

> 去重数组

```js
const arr = [...new Set([0, 1, 1, null, null])];
// arr => [0, 1, null]

```

> 混淆数组

```js
const arr = [0, 1, 2, 3, 4, 5].slice().sort(() => Math.random() - .5);
// arr => [3, 4, 0, 5, 1, 2]

```

> 截断数组

```js
const arr = [0, 1, 2];
arr.length = 2;
// arr => [0, 1]

```

> 交换赋值

```js
let a = 0;
let b = 1;
[a, b] = [b, a];
// a b => 1 0

// 或 只能是整数才能使用该方法
let a = 0;
let b = 1;
a ^= b;
b ^= a;
a ^= b;

```

> 过滤空值：undefined、null、''、0、false、NaN

```js
const arr = [undefined, null, '', 0, false, NaN, 1, 2].filter(Boolean);
// arr => [1, 2]

```

> 数组首部插入成员

```js
let arr = [1, 2]; // 以下方法任选一种
arr.unshift(0);
// 或
arr = [0].concat(arr);
// 或
arr = [0, ...arr];
// arr => [0, 1, 2]

```

> 数组尾部插入成员

```js
let arr = [0, 1]; // 以下方法任选一种
arr.push(2);
// 或
arr.concat(2);
// 或
arr[arr.length] = 2;
// 或
arr = [...arr, 2];
// arr => [0, 1, 2]

```

> 统计数组成员个数

```js
const arr = [0, 1, 1, 2, 2, 2];
const count = arr.reduce((t, c) => {
    t[c] = t[c] ? ++ t[c] : 1;
    return t;
}, {});
// count => { 0: 1, 1: 2, 2: 3 }

```

> 解构数组成员嵌套

```js
const arr = [0, 1, [2, 3, [4, 5]]];
const [a, b, [c, d, [e, f]]] = arr;
// a b c d e f => 0 1 2 3 4 5

```

> 解构数组成员别名

```js
const arr = [0, 1, 2];
const { 0: a, 1: b, 2: c } = arr;
// a b c => 0 1 2

```

> 解构数组成员默认值

```js
const arr = [0, 1, 2];
const [a, b, c = 3, d = 4] = arr;
// a b c d => 0 1 2 4

```

> 获取随机数组成员

```js
const arr = [0, 1, 2, 3, 4, 5];
const randomItem = arr[Math.floor(Math.random() * arr.length)];
// randomItem => 1

```

> 创建指定长度数组

```js
const arr = [...new Array(3).keys()];
// arr => [0, 1, 2]

```

> 创建指定长度且值相等的数组

```js
const arr = new Array(3).fill(0);
// arr => [0, 0, 0]

```

> reduce代替map和filter

```js
const _arr = [0, 1, 2];

// map
const arr = _arr.map(v => v * 2);
const arr = _arr.reduce((t, c) => {
    t.push(c * 2);
    return t;
}, []);
// arr => [0, 2, 4]

// filter
const arr = _arr.filter(v => v > 0);
const arr = _arr.reduce((t, c) => {
    c > 0 && t.push(c);
    return t;
}, []);
// arr => [1, 2]

// map和filter
const arr = _arr.map(v => v * 2).filter(v => v > 2);
const arr = _arr.reduce((t, c) => {
    c = c * 2;
    c > 2 && t.push(c);
    return t;
}, []);
// arr => [4]

```

# 5 Object技巧

> 克隆对象

```js
const obj1 = {a: 0, b: 1, c: 2}; // 以下方法任选一种
const obj2 = {...obj1};
const obj2 = JSON.parse(JSON.stringify(obj1));
// obj2 => { a: 0, b: 1, c: 2 }

```

> 合并对象

```js
const obj1 = {a: 0, b: 1, c: 2};
const obj2 = {c: 3, d: 4, e: 5};
const obj = { ...obj1, ...obj2 };
// obj => { a: 0, b: 1, c: 3, d: 4, e: 5 }

```

> 对象字面量：获取环境变量时必用此方法，用它一直爽，一直用它一直爽

```js
const env = 'prod';
const link = {
    dev: 'Development Address',
    test: 'Testing Address',
    prod: 'Production Address'
}[env];
// link => "Production Address"

```

> 对象变量属性

```js
const flag = false;
const obj = {
    a: 0,
    b: 1,
    [flag ? 'c' : 'd']: 2
};
// obj => { a: 0, b: 1, d: 2 }

```

> 删除对象无用属性

```js
const obj = {a: 0, b: 1, c: 2}; // 只想拿b和c
const {a, ...rest} = obj;
// rest => { b: 1, c: 2 }

```

> 解构对象属性嵌套

```js
const obj = {a: 0, b: 1, c: {d: 2, e: 3}};
const {c: {d, e}} = obj;
// d e => 2 3

```

> 解构对象属性别名

```js
const obj = {a: 0, b: 1, c: 2};
const {a, b: d, c: e} = obj;
// a d e => 0 1 2

```

> 解构对象属性默认值

```js
const obj = {a: 0, b: 1, c: 2};
const {a, b = 2, d = 3} = obj;
// a b d => 0 1 3

```

> 有条件的对象属性

不再需要根据一个条件创建两个不同的对象，可以使用展开运算符号来处理。

```js
let getUser = (emailIncluded) => {
  return {
    name: 'John',
    surname: 'Doe',
    ...emailIncluded && {email : 'john@doe.com'}
  }
}

const user = getUser(true);
console.log(user); // outputs {name: 'John', surname: 'Doe', email: 'john@doe.com'}

const userWithoutEmail = getUser(false);
console.log(userWithoutEmail); // outputs {name: 'John', surname: 'Doe'}

```

> 解构原始数据

有时候一个对象包含很多属性，而我们只需要其中的几个，这里可以使用解构方式来提取我们需要的属性。如一个用户对象内容如下：

```js
const rawUser = {
   name: 'John',
   surname: 'Doe',
   email: 'john@doe.com',
   displayName: 'SuperCoolJohn',
   joined: '2016-05-05',
   image: 'path-to-the-image',
   followers: 45,
   ...
}
```

我们需要提取出两个部分，分别是用户及用户信息，这时可以这样做:

```js
let user = {}, userDetails = {};
({ name: user.name, surname: user.surname, ...userDetails } = rawUser);

console.log(user); // outputs { name: "John", surname: "Doe" }
console.log(userDetails); // outputs { email: "john@doe.com", displayName: "SuperCoolJohn", joined: "2016-05-05", image: "path-to-the-image", followers: 45 }

```
> 动态属性名

早期，如果属性名需要是动态的，我们首先必须声明一个对象，然后分配一个属性。这些日子已经过去了，有了ES6特性，我们可以做到这一点。

```js
const dynamic = 'email';
let user = {
    name: 'John',
    [dynamic]: 'john@doe.com'
}
console.log(user); // outputs { name: "John", email: "john@doe.com" }

```

# 6 Function技巧

> 函数自执行

```js
const Func = function() {}(); // 常用

(function() {})(); // 常用
(function() {}()); // 常用
[function() {}()];

+ function() {}();
- function() {}();
~ function() {}();
! function() {}();

new function() {};
new function() {}();
void function() {}();
typeof function() {}();
delete function() {}();

1, function() {}();
1 ^ function() {}();
1 > function() {}();

```

> 隐式返回值：只能用于单语句返回值箭头函数，如果返回值是对象必须使用()包住

```js
const Func = function(name) {
    return 'I Love ' + name;
};
// 换成
const Func = name => 'I Love ' + name;

```

> 一次性函数：适用于运行一些只需执行一次的初始化代码

```js
function Func() {
    console.log('x');
    Func = function() {
        console.log('y');
    }
}

Func();
```

> 惰性载入函数：函数内判断分支较多较复杂时可大大节约资源开销

```js
function Func() {
    if (a === b) {
        console.log('x');
    } else {
        console.log('y');
    }
}

// 换成
function Func() {
    if (a === b) {
        Func = function() {
            console.log('x');
        }
    } else {
        Func = function() {
            console.log('y');
        }
    }
    return Func();
}
```

> 检测非空参数

```js
function IsRequired() {
    throw new Error('param is required');
}
function Func(name = IsRequired()) {
    console.log('I Love ' + name);
}
Func(); // "param is required"
Func('You'); // "I Love You"
```

> 字符串创建函数

```js
const Func = new Function('name', `console.log("I Love " + ${name})`);
```

> 优雅处理错误信息

```js
try {
    Func();
} catch (e) {
    location.href = `https://stackoverflow.com/search?q=[js]+${e.message}`;
}
```

> 优雅处理Async/Await参数

```js
async function AsyncTo(promise) {
    return promise.then(data => [null, data]).catch(err => [err]);
}
const [err, res] = await AsyncTo(Func());
```

> 优雅处理多个函数返回值

```js
async function Func() {
    return Promise.all([
        fetch('/user'),
        fetch('/comment')
    ]);
}
const [user, comment] = await Func(); // 需在async包围下使用
```

# 7 DOM技巧

> 显示全部DOM边框：调试页面元素边界时使用

```js
[].forEach.call($$('*'), dom => {
    dom.style.outline = '1px solid #' + (~~(Math.random() * (1 << 24))).toString(16);
});

```

> 自适应页面：页面基于一张设计图但需做多款机型自适应，元素尺寸使用rem进行设置

```js
function AutoResponse(width = 750) {
    const target = document.documentElement;
    target.clientWidth >= 600
        ? (target.style.fontSize = '80px')
        : (target.style.fontSize = target.clientWidth / width * 100 + 'px');
}

```

> 过滤XSS

```js
function FilterXss(content) {
    let elem = document.createElement('div');
    elem.innerText = content;
    const result = elem.innerHTML;
    elem = null;
    return result;
}

```

> 存取LocalStorage：反序列化取，序列化存

```js
const love = JSON.parse(localStorage.getItem('love'));
localStorage.setItem('love', JSON.stringify('I Love You'));

```

> 银行卡号分割
```js
bank_filter = val =>{
  val += '';
  val = val.replace(/(\s)/g,'').replace(/(\d{4})/g,'$1 ').replace(/\s*$/,'');
  return val;
}
```

> 数字超过99显示99+
```js
nineNumFilter = val =>{
  val = val?val-0:0;
  if (val > 99 ) {
    return '99+'
  }else{
    return val;
  }
}
```

> 防抖与节流
```js
/**
 * 函数防抖 (只执行最后一次点击)
 */
Debounce = (fn, t) => {
    let delay = t || 500;
    let timer;
    return function () {
        let args = arguments;
        if(timer){
            clearTimeout(timer);
        }
        timer = setTimeout(() => {
            timer = null;
            fn.apply(this, args);
        }, delay);
    }
};
/*
 * 函数节流
 */
Throttle = (fn, t) => {
    let last;
    let timer;
    let interval = t || 500;
    return function () {
        let args = arguments;
        let now = +new Date();
        if (last && now - last < interval) {
            clearTimeout(timer);
            timer = setTimeout(() => {
                last = now;
                fn.apply(this, args);
            }, interval);
        } else {
            last = now;
            fn.apply(this, args);
        }
    }
};

```
