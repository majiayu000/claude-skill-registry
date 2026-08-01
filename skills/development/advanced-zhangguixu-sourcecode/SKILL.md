---
name: advanced-zhangguixu-sourcecode
description: JavaScript内置的类型检测并非完全可靠
---

# JavaScript 高级技巧

## 一、高级函数

### 1-1 安全的类型检测

**JavaScript内置的类型检测并非完全可靠**

在<a href='../best practice/compare'>best practice/compare</a>中有详细说明。

### 1-2 作用域安全的构造函数

在全局作用域内调用函数构造函数，由于没有使用new，导致在全局作用域添加冗余的属性

```javascript
//Global
function Person(name,age,job){
    this.name = name;
    this.age = age;
    this.job = job;
}
//没有使用new
var person = Person('zhang',26,'font-end');

console.log(window.name);//'zhang'
console.log(window.age);//26
```

*这个问题是由this对象的晚绑定造成的*

因此，需要在函数里面`确认this对象是正确类型的实例`：

```javascript
function Person(name){
    if(this instanceof Person){
    this.name = 'zhang';
    } else {
        return new Person(name)
    }
}
```

### 1-3 惰性载入函数

惰性载入表示函数执行的分支只会在函数第一次调用的时候执行，在第一次调用过程中，该函数会被覆盖为另一个按照合适方式执行的函数，这样任何对原函数的调用就不用再经过执行的分支。

**应用场景**

实现事件注册函数，由于各浏览器之间的差异，不得不在用的时候做能力检测，单从功能上讲，已经做到了兼容浏览器，但美中不足的是，每次绑定监听，都会再进行一次检测，这在真实的环境中，显然是多余的，同一个应用环境中，其实只需要检测一次即可。

**注意点**

1. 应用越频繁，越能体现这种模式的优势所在

2. 固定不变，一次判定，在固定的应用环境中不会改变

3. 复杂的分支判断，没有差异性，不需要应用这种模式

<a href="../developing javascript web applications/model/ajax.js">代码示例</a>

### 1-4 函数绑定

这个技巧常常和回调函数与事件处理一起使用，以便在将函数作为变量传递的同时保留代码执行环境。

很多JavaScript库实现了一个可以将函数绑定到指定环境的函数，这个函数一般都叫做bind()。一个简单的bind()函数接受一个函数和一个环境，并返回一个给的环境中调用给定函数的函数，并且将所有参数原封不动传递过去。这个函数返回的是一个`闭包`。

```javascript
function bind(fn,context){
    return function(){
        fn.apply(context,arguments);
    };
}
```

ECMAScript5为所有函数定义了一个原生的bind()方法，进一步简单了操作。

### 1-5 函数柯里化

函数柯里化（function currying），它用于创建已经设置好了一个或多个参数的函数。它是与函数绑定紧密相关的主题。

**创建柯里化函数**

调用另一个函数，并为它传入要柯里化的函数和必要参数。

```javascript
function curry(fn){
    var args = Array.prototype.slice.call(arguments,1);
    return function(){
        var innerArgs = Array.prototype.slice.call(arguments);
        var finalArgs= args.concat(innerArgs);
        return fn.apply(null,finalArgs);
    }
};
```

示例：创建一个第一个参数绑定为3的add()的柯里化的版本

```javascript
function add(n1,n2){return n1 + n2;}
var curriedAdd = curry(add,3);
console.log(curriedAdd(5));//8
```

**柯里化与函数绑定的结合**

函数柯里化常常作为函数绑定的一部分包含在其中，构造出更为复杂的bind()函数。

```javascript
function bind(fn,context){
    var args = Array.prototype.slice.call(arguments,1);
    return function(){
        var innerArgs = Array.prototype.slice.call(arguments);
        var finalArgs = args.concat(innerArgs);
        return fn.apply(context,finalArgs);
    }
}
```

这样的bind()函数不仅可以返回绑定给定环境的函数，并且可能绑定其中的某些函数参数

*ECMAScript5的bind()方法实现了函数柯里化。*

**注意**

无论是柯里化函数或是绑定函数，都会带来额外的开销，所以不应滥用。

## 二、防篡改对象

JavaScript共享的本质一直是开发人员心头的痛，因为任何对象都可以被在同一个环境中运行的代码修改。

ECMAScript5致力于解决这个问题，可以让开发人员定义防篡改对象（tamper-proof object）。它的原理就是通过设置每个属性的

* [\[Configurable\]]

* [\[Writable\]]

* [\[Enumerable\]]

* [\[Value\]]

* [\[Get\]]

* [\[Set\]]

### 2-1 不可扩展对象

**Object.preventExtensions(o)**

可以使得不能在给对象添加属性和方法

**Object.isExtensible(o)**

确定对象是否可以扩展

```javascript
var person = {name:'zhang'};
Object.isExtensible(person); //true
Object.preventExtensions(person);
Object.isExtensible(person);//false
```

### 2-1 密封的对象

**Object.seal(o)**

密封对象不可扩展，而且已有成员的`[[Configurable]]`特性被设置为false，意味着不能删除属性和方法。

**Object.isSealed(o)**

检测是否被密封了

```javascript
var person = {name:'zhang'};
Object.isSealed(person);//false
Object.seal(person);
Object.isSealed(person);//true
Object.isExtensible(person);//false
```

### 2-3 冻结的对象

**Object.freeze(o)**

最严格的防篡改级别就是冻结对象（frozen object）。冻结的对象不能扩展，又是密封的，而且对象属性的`[[Writable]]`特性会被设置为false。

如果定义了`[[Set]]`函数，访问器属性仍然是可写的。

**Object.isFrozen(o)**

```javascript
var person = {name:'zhang'};
Object.freeze(person);
Object.isFrozen(person);//true
Object.isSealed(person);//true
Object.isExtensible(person);//false
```

## 三、高级定时器

要理解setTimeout()和setInterval()，必须结合<a href="./event-loop.md">Event Loop</a>

### 3-1 重复的定时器

setInterval有两个问题：

1. 某些间隔会被跳过
2. 多个定时器的代码执行之间的间隔可能会比预期的小

为了避免setInterval()的重复定时器的2个缺点，可以使用链式的setTimeout()调用

```javascript
setTimout(function(){
    //处理中

    setTimeout(arguments.callee,interval);

},interval);
```

这种写法可以保证在下一次定时器代码执行之前，至少要等到指定的间隔，避免了连续的运行。

### 3-2 Yielding Processes

浏览器在JavaScript运行时间上采取了限制,此类限制有两个

1. 调用栈尺寸限制
2. 长时间脚本限制（50ms以上）

在任何一种情况下，创建一个定时器造成UI线程暂停，如同它从一个任务切换到下一个任务。因此，`定时器代码复位所有相关的浏览器限制`，包括长运行脚本时间。此外，调用栈也在定时器代码中复位为零。这一特性使得定时器成为长运行JavaScript代码理想的跨浏览器解决方案。

例如在处理大规模的数组的时候，可以采用下列的方式来进行处理。

```javascript
function timedProcessArray(items,process,callback){
    var todo=items.concat();
    setTimeout(function(){
        var start=+new Date(); //小技巧，new Date()和+new Date()是不一样的
        do{
            process(todo.shift())  //进行批处理
        }while(todo.length>0&&(+new Date()-start)<50);

        if(todo.length>0){
            setTimeout(arguments.callee,25);
        }else{
            callback(items);
        }
    },25);
}
```

### 3-3 函数节流

函数节流是保证函数不要过于频繁并且在不超过规定时间内执行。

<a href="../blog/skill/throttle.md">详细解释</a>

## 四、自定义事件

基于`观察者模式`的一种创建松散耦合代码的技术。使用自定义事件有助于`解耦`相关对象，保持功能的隔绝。

```javascript
function EventTarget(){
    this.handlers = {};
}

EventTarget.prototype = {
    constructor : EventTraget,
    addHandler : function(type,handler){
        if(typeof this.handlers[type] === 'undefined'){
            this.handlers[type] = [];
        }
        this.handlers[type].push(handler);
    },
    fire : function(event){
        if(!event.target){
            event.target = this;
        }
        if(this.handlers[type] instanceof Array){
            var handlers = this.handlers[event.type];
            for(var i = 0,len = handlers.length; i < len; i++){
                handlers[i](event);//执行回调函数
            }
        }
    },
    removeHandler : function(type,handler){
        if(this.handlers[type] instanceof Array){
            var handlers = this.handlers[type];
            for(var i = 0,len = handlers.length; i < len; i++){
                if(handlers[i] === handler){
                    break;
                }
            }
            handlers.splice(i,1);//删除
        }
    }
}
```