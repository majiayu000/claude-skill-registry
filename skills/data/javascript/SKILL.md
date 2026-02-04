# JavaScript 小技巧 笔记

★★★★★★★★★★

1. 多次解构

    ```javascript
    let obj = {
      part1: {
        name: '01',
        age: 23
      }
    }

    // 解构
    const { part1: { name, age } } = obj
    // 使用
    console.log(name, age) // "01"  23
    console.log(part1) // Uncaught ReferenceError: part1 is not defined

    // 多次解构
    const { part1: { name, age }, part1 } = obj
    console.log(part1) // {name: "01", age: 23}
    ```

1. 数字分隔符

    ```javascript
    const myMoney = 1_000_000_000_000

    console.log(myMoney)  // 1000000000000
    ```

1. `try` | `catch` | `finally` 能使用 `return` 提前终止操作吗？

    ```javascript
    function demo() {
      try {
        return 1
      } catch (err) {
        console.log(err)
        return 2
      } finally {
        try {
          return 3
        } finally {
          return 4
        }
      }
    }

    console.log(demo())  // 4
    ```

1. 获取当前调用栈

    ```javascript
    function firstFunction() { secondFunction(); } 
    function secondFunction() { thridFunction(); } 
    function thridFunction() { console.log(new Error().stack); } 

    firstFunction();

    //=> Error 
    //  at thridFunction (<anonymous>:2:17) 
    //  at secondFunction (<anonymous>:5:5) 
    //  at firstFunction (<anonymous>:8:5) 
    //  at <anonymous>:10:1
    ```

    使用 `new Error().stack` 就能随时获取到当前代码执行的调用栈信息，也是一种调试代码的办法

1. 如何快速生成随机数字+字符串

    ```javascript
    const str = Math.random().toString(36).substr(2, 10);
    console.log(str);   // 'w5jetivt7e'
    ```

    先是 `Math.random()` 生成 `[0, 1)` 的数，然后调用 `number` 的 `toString` 方法将其转换成`36`进制的，按照 `MDN` 的说法，`36` 进制的转换应该是包含了字母 `a~z` 和 数字 `0~9` 的，因为这样生成的是 `0.89kjna21sa` 类似这样的，所以要截取一下小数部分，即从索引 `2` 开始截取 `10` 个字符就是我们想要的随机字符串了

1. 最快获取 `dom` 的方法

    ```javascript
    <div id="zero2one"></div>

    const el = document.getElementById('zero2one')  
    console.log(el) // <div id="zero2one"></div>
    
    // 等同于
    console.log(zero2one) // <div id="zero2one"></div>
    ```

1. `||` 和 `??` 的区别？

    `??`：空值合并操作符是一个逻辑操作符，当左侧的操作数为 `null` 或者 `undefined` 时，返回其右侧操作数，否则返回左侧操作数。

    `||`：与逻辑或操作符不同，逻辑或操作符会在左侧操作数为假值时返回右侧操作数。也就是说，如果使用 `||` 来为某些变量设置默认值，可能会遇到意料之外的行为。比如为假值（例如，`''` 或 `0`）时。见下面的例子

    ```javascript
    const foo = null ?? 'default string';
    console.log(foo);
    // expected output: "default string"

    const baz = 0 ?? 42;
    console.log(baz);
    // expected output: 0
    ```

1. `Array.prototype.sort()` 中排序顺序

    `arr.sort()`：默认从小到大
    `arr.sort((a, b) => a - b)`：从小到大
    `arr.sort((a, b) => b - a)`：从大到小

1. 在使用 `EventSource` 的过程中注意：
   - `eventSource.onmessage`：只能监听默认的 `type = message` 的事件
   - `eventSource.addEventListener("custom", (event) => {})`：可以监听其它 `custom` 事件

★★★★★★★★★★
