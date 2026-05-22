---
name: eich-language-fundamentals
description: Write JavaScript code with deep understanding of the language fundamentals as envisioned by Brendan Eich, creator of JavaScript. Emphasizes first-class functions, prototypes, and the dynamic nature of the language. Use when leveraging JavaScript's unique characteristics.
---

# Brendan Eich Style Guide

## Overview

Brendan Eich created JavaScript in 10 days at Netscape in 1995. Despite time constraints, he embedded powerful concepts: first-class functions, prototypal inheritance, and dynamic typing. Understanding his design choices unlocks JavaScript's true power.

## Core Philosophy

> "Always bet on JavaScript."

> "JavaScript has first-class functions and closures. That's a big deal."

Eich designed JavaScript to be accessible yet powerful, borrowing from Scheme (functions), Self (prototypes), and Java (syntax).

## Design Principles

1. **First-Class Functions**: Functions are values—pass them, return them, store them.

2. **Prototypal Inheritance**: Objects inherit directly from objects, not classes.

3. **Dynamic Nature**: Types are fluid; embrace duck typing.

4. **Flexibility**: The language adapts to many paradigms.

## When Writing Code

### Always

- Leverage closures for encapsulation
- Use functions as first-class citizens
- Understand the prototype chain
- Embrace JavaScript's multi-paradigm nature
- Know that objects are just property bags

### Never

- Fight the language's dynamic nature
- Ignore `undefined` and `null` semantics
- Assume JavaScript is "Java-like"
- Overlook the power of functions

### Prefer

- Function expressions and closures
- Object literals for simple objects
- Prototype delegation over deep hierarchies
- Dynamic features when they simplify code

## Code Patterns

### First-Class Functions

```javascript
// Functions as values
const greet = function(name) {
    return 'Hello, ' + name;
};

// Functions as arguments
function map(array, transform) {
    const result = [];
    for (let i = 0; i < array.length; i++) {
        result.push(transform(array[i]));
    }
    return result;
}

const doubled = map([1, 2, 3], function(x) { return x * 2; });

// Functions returning functions
function multiplier(factor) {
    return function(number) {
        return number * factor;
    };
}

const double = multiplier(2);
const triple = multiplier(3);
double(5);  // 10
triple(5);  // 15
```

### Closures

```javascript
// Closures capture their lexical environment
function createCounter() {
    let count = 0;  // Private state
    
    return {
        increment: function() { return ++count; },
        decrement: function() { return --count; },
        value: function() { return count; }
    };
}

const counter = createCounter();
counter.increment();  // 1
counter.increment();  // 2
counter.value();      // 2
// count is not directly accessible
```

### Prototypal Inheritance

```javascript
// Objects inherit from objects
const animal = {
    speak: function() {
        return this.sound;
    }
};

const dog = Object.create(animal);
dog.sound = 'Woof!';
dog.speak();  // 'Woof!'

const cat = Object.create(animal);
cat.sound = 'Meow!';
cat.speak();  // 'Meow!'

// The prototype chain
dog.hasOwnProperty('sound');  // true
dog.hasOwnProperty('speak');  // false (inherited)
```

### Dynamic Objects

```javascript
// Objects are dynamic property bags
const obj = {};

// Add properties anytime
obj.name = 'Dynamic';
obj['computed-key'] = 'Works too';

// Delete properties
delete obj.name;

// Check existence
'computed-key' in obj;  // true

// Iterate properties
for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
        console.log(key, obj[key]);
    }
}
```

## Mental Model

Eich's JavaScript is built on:

1. **Functions are fundamental** — Not just procedures, but values
2. **Objects are flexible** — Dynamic bags of properties
3. **Prototypes link objects** — Delegation, not copying
4. **Closures preserve scope** — Functions remember their birth environment

## Signature Moves

- Closures for private state
- Higher-order functions for abstraction
- Prototype chain for shared behavior
- Object literals for quick structures
- Dynamic property access when needed
