---
name: simpson-you-dont-know-js
description: Write JavaScript code in the style of Kyle Simpson, author of "You Don't Know JS". Emphasizes deep understanding of JavaScript mechanics—scope, closures, this, prototypes, and async. Use when you need to truly understand JavaScript behavior.
---

# Kyle Simpson Style Guide

## Overview

Kyle Simpson is the author of the "You Don't Know JS" book series. His philosophy centers on truly understanding JavaScript's core mechanics rather than just memorizing patterns or avoiding features out of fear.

## Core Philosophy

> "The only way to understand JavaScript is to understand JavaScript."

> "Don't fear what you don't understand—learn it."

> "Coercion is not evil, it's just misunderstood."

Simpson believes that most JavaScript confusion comes from not understanding how the language actually works, not from the language being inherently broken.

## Design Principles

1. **Understand, Don't Memorize**: Know why code works, not just that it works.

2. **Embrace the Language**: Use JavaScript as JavaScript, not as Java-lite.

3. **Master the Core**: Scope, closures, `this`, prototypes are essential.

4. **Explicit Over Magic**: Prefer explicit code even if longer.

## When Writing Code

### Always

- Understand what `this` refers to in every function
- Know the difference between lexical and dynamic scope
- Use closures intentionally and understand their implications
- Understand coercion rules when using `==`
- Know prototype chain behavior
- Understand event loop and async mechanics

### Never

- Use `this` without understanding its binding rules
- Ignore type coercion—understand it instead
- Assume `class` hides JavaScript's prototype nature
- Use `async/await` without understanding Promises
- Copy-paste code you don't understand

### Prefer

- Understanding over avoidance
- Explicit type coercion (`Number()`, `String()`) over implicit
- Factory functions or OLOO over `class` (for clarity)
- Clear naming that reveals intent
- Comments explaining *why*, not *what*

## Code Patterns

### The Four Rules of `this`

```javascript
// Rule 1: Default Binding (standalone function call)
function sayHello() {
    console.log(this.name);  // undefined (strict) or global (sloppy)
}
sayHello();


// Rule 2: Implicit Binding (method call)
var person = {
    name: 'Alice',
    greet: function() {
        console.log(this.name);  // 'Alice'
    }
};
person.greet();

// CAUTION: Implicit binding can be lost!
var greet = person.greet;
greet();  // undefined - default binding now!


// Rule 3: Explicit Binding (call, apply, bind)
function introduce() {
    console.log('I am ' + this.name);
}
var bob = { name: 'Bob' };

introduce.call(bob);   // 'I am Bob'
introduce.apply(bob);  // 'I am Bob'

var boundIntroduce = introduce.bind(bob);
boundIntroduce();      // 'I am Bob'


// Rule 4: new Binding
function Person(name) {
    this.name = name;
}
var charlie = new Person('Charlie');
console.log(charlie.name);  // 'Charlie'


// Arrow functions: Lexical this (inherits from enclosing scope)
var team = {
    members: ['Alice', 'Bob'],
    name: 'Dev Team',
    introduce: function() {
        // Arrow function inherits 'this' from introduce()
        this.members.forEach(member => {
            console.log(member + ' is on ' + this.name);
        });
    }
};
```

### Closures Demystified

```javascript
// Closure: function retains access to its lexical scope
function createCounter() {
    var count = 0;  // This variable is "closed over"
    
    return function increment() {
        count += 1;
        return count;
    };
}

var counter = createCounter();
counter();  // 1
counter();  // 2
counter();  // 3 - count persists!


// Classic closure gotcha
for (var i = 0; i < 3; i++) {
    setTimeout(function() {
        console.log(i);  // 3, 3, 3 - all share same i!
    }, 100);
}

// Solution 1: IIFE creates new scope each iteration
for (var i = 0; i < 3; i++) {
    (function(j) {
        setTimeout(function() {
            console.log(j);  // 0, 1, 2
        }, 100);
    })(i);
}

// Solution 2: let creates block scope
for (let i = 0; i < 3; i++) {
    setTimeout(function() {
        console.log(i);  // 0, 1, 2
    }, 100);
}
```

### OLOO (Objects Linked to Other Objects)

```javascript
// Simpson's preferred pattern over class
// Explicit delegation instead of hidden inheritance

var PersonPrototype = {
    init: function(name) {
        this.name = name;
        return this;
    },
    greet: function() {
        return 'Hello, I am ' + this.name;
    }
};

var EmployeePrototype = Object.create(PersonPrototype);
EmployeePrototype.initEmployee = function(name, title) {
    this.init(name);
    this.title = title;
    return this;
};
EmployeePrototype.introduce = function() {
    return this.greet() + ', ' + this.title;
};

// Usage
var alice = Object.create(EmployeePrototype)
    .initEmployee('Alice', 'Engineer');
alice.introduce();  // 'Hello, I am Alice, Engineer'

// Clear delegation chain, no hidden magic
```

### Understanding Coercion

```javascript
// Explicit coercion (preferred - clear intent)
var num = Number('42');      // 42
var str = String(42);        // '42'
var bool = Boolean('hello'); // true

// Implicit coercion (understand it, use carefully)
var result = '5' - 2;    // 3 (string coerced to number)
var concat = '5' + 2;    // '52' (number coerced to string)

// The == algorithm (Abstract Equality Comparison)
// Know these rules:
null == undefined;    // true (special case)
42 == '42';          // true (string → number)
true == 1;           // true (boolean → number)
'0' == false;        // true (both → number: 0 == 0)

// Simpson's take: == is safe when types are known
// Use === when types are unknown or mixed
function isNullOrUndefined(val) {
    return val == null;  // Safely checks both null and undefined
}
```

### Async Patterns Deep Dive

```javascript
// Callbacks: Understand the problems
doA(function() {
    doB(function() {
        doC(function() {
            // "Callback hell" - but inversion of control is the real issue
        });
    });
});

// Promises: Understand the guarantees
// 1. Only resolved once
// 2. Either success or failure
// 3. Values are immutable once settled
// 4. Exceptions become rejections

function fetchData(url) {
    return new Promise(function(resolve, reject) {
        // Async operation
        if (success) {
            resolve(data);
        } else {
            reject(new Error('Failed'));
        }
    });
}

// Promise chaining - each .then returns a new Promise
fetchUser(id)
    .then(function(user) {
        return fetchPosts(user.id);  // Returns Promise
    })
    .then(function(posts) {
        return processPosts(posts);
    })
    .catch(function(err) {
        // Catches any error in the chain
        console.error(err);
    });


// async/await: Syntactic sugar over Promises
// MUST understand Promises first!
async function getUserPosts(id) {
    try {
        var user = await fetchUser(id);
        var posts = await fetchPosts(user.id);
        return processPosts(posts);
    } catch (err) {
        console.error(err);
        throw err;
    }
}
```

### Scope and Hoisting

```javascript
// var is function-scoped and hoisted
function example() {
    console.log(x);  // undefined (not ReferenceError!)
    var x = 5;
    console.log(x);  // 5
}

// How JavaScript sees it (hoisting):
function example() {
    var x;           // Declaration hoisted
    console.log(x);  // undefined
    x = 5;           // Assignment stays
    console.log(x);  // 5
}

// let/const are block-scoped with TDZ
function example() {
    console.log(x);  // ReferenceError: TDZ
    let x = 5;
}

// Functions are fully hoisted
sayHi();  // Works!
function sayHi() {
    console.log('Hi');
}

// Function expressions are not
sayBye();  // TypeError: sayBye is not a function
var sayBye = function() {
    console.log('Bye');
};
```

## Mental Model

Simpson approaches JavaScript by asking:

1. **What does `this` point to?** Apply the four rules
2. **What scope does this live in?** Lexical, not dynamic
3. **What's in the closure?** What variables are captured
4. **What's the prototype chain?** Follow the `[[Prototype]]` links
5. **What type coercion is happening?** Know the algorithm

## Signature Simpson Moves

- OLOO pattern instead of classes
- Understanding `this` binding rules explicitly
- Safe `==` usage when types are known
- Explicit coercion over implicit
- Deep async understanding before using `async/await`
