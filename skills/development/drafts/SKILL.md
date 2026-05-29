---
title: JavaScript code小技巧
date: 2017-09-19 22:37:31
categories: ["Javascript"]
---

### 使用 === 取代 ==

== 和!= 操作符会自动转换数据类型。=== 和 !== 不会，它们会同时比较值和数据类型，所以 === 和 !== 要比 == 和 != 快。

```javascript
[10] === 10 // is false
[10] == 10 // is true
'10' == 10 // is true
'10' === 10 // is false
[] == 0 // is true
[] === 0 // is false
'' == false // is true but true == "a" is false
'' === false // is false
```
### underfined、null、0、false、NaN、空字符串的逻辑结果均为false
### 小心使用typeof、instanceof和contructor
####typeof：JavaScript一元操作符，用于以字符串的形式返回变量的原始类型，注意，`typeof null`也会返回`object`，
大多数的对象类型（数组Array、时间Date等）也会返回`object`
####`contructor`：内部原型属性，可以通过代码重写
####instanceof：JavaScript操作符，会在原型链中的构造器中搜索，找到则返回true，否则返回false
### 立即执行函数
函数在创建之后直接自动执行，通常称之为立即执行函数, 自调用匿名函数（Self-Invoked Anonymous Function）或直接调用函数表达式（Immediately Invoked Function Expression ）。
```javascript
(function(a,b){
return a+b;
})(10,20)
```
### 不要直接从数组中delete或remove元素
如果对数组元素直接使用delete，其实并没有删除，只是将元素置为了undefined。数组元素删除应使用splice。
```javascript
var items = [12, 548 ,'a' , 2 , 5478 , 'foo' , 8852, , 'Doe' ,2154 , 119 ];
items.length; // return 11
items.splice(3,1) ;
items.length; // return 10
items 结果为 [12, 548, "a", 5478, "foo", 8852, undefined × 1, "Doe", 2154, 119]
```
### 使用length属性截断或清空数组
```javascript
var arr = [1 , 2 , 3 , 4 , 5 , 6 ];
arr.length = 3 //[1 , 2 , 3]
arr.length = 0 //[]
```
### toFixed() 保留指定小数位数, 返回的是字符串，不是数字。
```javascript
var num =2.22222222;
num = num.toFixed(4);  // num will be equal to 2.2222
```

### 不要使用eval() with() 或者函数构造器
eval()和函数构造器（Function consturctor）的开销较大，每次调用，JavaScript引擎都要将源代码转换为可执行的代码。
使用with()可以把变量加入到全局作用域中，因此，如果有其它的同名变量，容易混淆，值也会被覆盖。
### 不要对数组使用for-in
```javascript
var sum = 0;
for (var i = 0, len = nums.length; i < len; i++) {
 sum += nums[i];
}
```
i和len两个变量是在for循环的第一个声明中，二者只会初始化一次，这要比下面这种写法快
```javascript
for (var i = 0; i < nums.length; i++)
```
### 不要在循环内部使用try-catch-finally
try-catch-finally中catch部分在执行时会将异常赋给一个变量，这个变量会被构建成一个运行时作用域内的新的变量。

### undefined与null的区别
null表示"没有对象"，即该处不应该有值。
* 作为函数的参数，表示该函数的参数不是对象。
* 作为对象原型链的终点。
undefined表示"缺少值"，就是此处应该有一个值，但是还没有定义。
* 变量被声明了，但没有赋值时，就等于undefined。
* 调用函数时，应该提供的参数没有提供，该参数等于undefined。
* 对象没有赋值的属性，该属性的值为undefined。
> 函数没有返回值时，默认返回undefined。

### 判断是否是数组
1. instanceof
```javascript
var arr = [];
console.log(arr instanceof Array) //返回true
```
2. constructor
js 中 `constructor` 属性返回对象相对应的构造函数
```javascript
a.constructor == Array
```
3. 特性判断
```javascript
function isArray(object){
    return object && typeof object==='object' &&
    typeof object.length==='number' &&
    typeof object.splice==='function' &&
    //判断length属性是否是可枚举的 对于数组 将得到false
    !(object.propertyIsEnumerable('length'));
}
```
不能枚举length属性，才是最重要的判断因子。
JavaScript中，对象的属性分为可枚举和不可枚举之分，它们是由属性的enumerable值决定的。可枚举性决定了这个属性能否被for…in查找遍历到。
for…in
Object.keys()
JSON.stringify
object. propertyIsEnumerable(proName)

判断指定的属性是否可列举
备注：如果 proName 存在于 object 中且可以使用一个 For…In 循环穷举出来，那么 propertyIsEnumerable 属性返回 true。如果 object 不具有所指定的属性或者所指定的属性不是可列举的，那么 propertyIsEnumerable 属性返回 false。
propertyIsEnumerable 属性不考虑原型链中的对象。

4. isArray
```javascript
Array.isArray([])
```

### && 的用法
```javascript
var add_step = 10;
//var add_level = (add_step==5 && 1) || (add_step==10 && 2) || (add_step==12 && 3) || (add_step==15 && 4) || 0;
var add_level={'5':1,'10':2,'12':3,'15':4}[add_step] || 0;
console.log(add_level);
if(a >=5){
  alert("你好");
}
//可以写成：
a >= 5 && alert("你好");
```

### 构造函数
构造函数和其他函数唯一的区别，在于调用的方式不同。
任何函数，只要通过new来调用，就可以作为构造函数

### NaN
NaN这个特殊的Number与所有其他值都不相等，包括它自己：
NaN === NaN; // false
唯一能判断NaN的方法是通过isNaN()函数：
isNaN(NaN); // true

### 数组的排序方法`sort`

```javascript
[10, 20, 1, 2].sort(); // [1, 10, 2, 20]
```
为什么排序结果不是`[1, 2, 10, 20]`，因为`Array`的`sort()`方法默认把所有元素先转换为`String`再排序，结果'10'排在了'2'的前面，因为字符'1'比字符'2'的`ASCII`码小。

### 分组选择符
```js
var a = (1,2,3);
console.log(a);  //3, 会以最后一个为准

// 所以下面的 typeof f 输出是 "number"
var f = (function f(){ return "1"; }, function g(){ return 2; })();
typeof f;//"number"
```

### 单引号和双引号的区别
双引号会搜索引号内的内容是不是有变量，有则输出其值，没有则输出原有内容。所以输出纯字符串的时候用单引号比双引号效率高，因为省去检索的过程。






