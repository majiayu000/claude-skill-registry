---
name: concatenative
description: "Forth/Factor/Joy: stack-based concatenative programming where composition replaces application."
trit: -1
bundle: strange-loops
---

# Concatenative Programming Skill

> *"Programs are composed by concatenation. The stack is the only state."*

## Core Concept

In concatenative languages:
1. **Stack** is the implicit data structure
2. **Words** (functions) transform the stack
3. **Composition = Concatenation** — `f g` means "do f, then g"
4. **No variables** (mostly) — data flows through stack

```forth
3 4 +        \ Push 3, push 4, add → 7 on stack
dup *        \ Duplicate top, multiply → 49
```

## Why It's Strange

1. **No application** — `f(x)` becomes `x f`
2. **No variables** — use stack manipulation
3. **Point-free by default** — everything is tacit
4. **Quotations** — code as data `[ ... ]`
5. **Extreme composability** — every word combines freely

## Forth Basics

```forth
\ Comments start with backslash
3 4 +           \ → 7
10 3 /          \ → 3 (integer division)
1 2 3 + *       \ 1 * (2 + 3) = 5

\ Stack manipulation
DUP             \ a → a a
DROP            \ a b → a
SWAP            \ a b → b a
OVER            \ a b → a b a
ROT             \ a b c → b c a

\ Defining words
: SQUARE  DUP * ;
5 SQUARE        \ → 25

: CUBE  DUP DUP * * ;
3 CUBE          \ → 27
```

## Factor (Modern Forth)

```factor
! Stack effect declarations
: square ( n -- n^2 ) dup * ;
: cube ( n -- n^3 ) dup dup * * ;

! Quotations (anonymous functions)
{ 1 2 3 } [ 2 * ] map   ! → { 2 4 6 }
{ 1 2 3 4 } [ even? ] filter  ! → { 2 4 }

! Cleave combinator (apply multiple quotations)
5 [ 1 + ] [ 2 * ] bi    ! → 6 10

! Spread combinator
1 2 [ 1 + ] [ 2 * ] bi* ! → 2 4
```

## Joy (Functional Concatenative)

```joy
# No mutable state, pure functional
# Quotations are first-class
[dup *] square define
5 square                  # → 25

# Combinators
[1 2 3] [2 *] map         # → [2 4 6]
[1 2 3 4 5] 0 [+] fold    # → 15

# Recursion via Y combinator
[dup 0 = [pop 1] [dup 1 - factorial *] ifte] factorial define
5 factorial               # → 120
```

## Stack Effect Notation

```
( before -- after )

dup   ( a -- a a )
drop  ( a -- )
swap  ( a b -- b a )
over  ( a b -- a b a )
rot   ( a b c -- b c a )
+     ( a b -- a+b )
```

## Quotations and Combinators

| Combinator | Stack Effect | Meaning |
|------------|--------------|---------|
| `call` | `( quot -- ... )` | Execute quotation |
| `dip` | `( x quot -- ... x )` | Run quot, restore x |
| `keep` | `( x quot -- ... x )` | Run quot, keep x |
| `bi` | `( x p q -- ... )` | `p(x) q(x)` |
| `tri` | `( x p q r -- ... )` | `p(x) q(x) r(x)` |
| `cleave` | `( x [p q ...] -- ... )` | Apply all to x |

## Point-Free Style

```factor
! Instead of:
: sum-of-squares-bad ( seq -- n )
    0 swap [ sq + ] each ;

! Point-free:
: sum-of-squares ( seq -- n )
    [ sq ] map sum ;

! Even more point-free:
: sum-of-squares ( seq -- n )
    [ sq ] [ + ] map-reduce ;
```

## Implementation

```python
class ConcatVM:
    def __init__(self):
        self.stack = []
        self.words = {
            '+': self.add,
            '*': self.mul,
            'dup': self.dup,
            'drop': self.drop,
            'swap': self.swap,
        }
    
    def push(self, val):
        self.stack.append(val)
    
    def pop(self):
        return self.stack.pop()
    
    def add(self):
        b, a = self.pop(), self.pop()
        self.push(a + b)
    
    def mul(self):
        b, a = self.pop(), self.pop()
        self.push(a * b)
    
    def dup(self):
        self.push(self.stack[-1])
    
    def drop(self):
        self.pop()
    
    def swap(self):
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
    
    def define(self, name, body):
        """Define new word as sequence of words."""
        def new_word():
            for word in body:
                self.run(word)
        self.words[name] = new_word
    
    def run(self, program):
        if isinstance(program, (int, float)):
            self.push(program)
        elif program in self.words:
            self.words[program]()
        else:
            raise ValueError(f"Unknown: {program}")

# Usage
vm = ConcatVM()
vm.define('square', ['dup', '*'])
for token in [5, 'square']:
    vm.run(token)
print(vm.stack)  # [25]
```

## GF(3) Integration

```python
# Trit stack with GF(3) operations
class TritStack:
    def __init__(self):
        self.stack = []  # Stack of trits: -1, 0, +1
    
    def push(self, trit):
        assert trit in (-1, 0, 1)
        self.stack.append(trit)
    
    def gf3_add(self):
        """( a b -- (a+b) mod 3 )"""
        b, a = self.stack.pop(), self.stack.pop()
        result = (a + b) % 3
        result = result if result != 2 else -1
        self.stack.append(result)
    
    def trit_sum(self):
        """Conservation check."""
        return sum(self.stack) % 3
```

## Categorical Semantics

Concatenative languages are **Cartesian closed categories** where:
- Objects = stack types
- Morphisms = stack transformations
- Composition = concatenation
- Identity = empty program

```
f : A → B
g : B → C
g ∘ f = "f g" : A → C
```

## Languages

| Language | Era | Features |
|----------|-----|----------|
| **Forth** | 1970 | Original, minimal |
| **PostScript** | 1982 | Graphics, stacks |
| **Joy** | 2001 | Pure functional |
| **Factor** | 2003 | Modern, typed |
| **Cat** | 2006 | Statically typed |
| **Kitten** | 2016 | Effect system |

## When to Use

- **Embedded systems** — Forth is tiny
- **DSLs** — Easy to extend
- **Calculators** — RPN style
- **Compilers** — Stack machines as target

## Literature

1. **Moore (1970)** - Forth invention
2. **von Thun (2001)** - "Joy: Forth's Functional Cousin"
3. **Pestov (2010)** - Factor language
4. **Diggins (2008)** - "Cat: A Typed Concatenative Language"

## Related Skills

- `stack-machines` - Implementation target
- `tacit-programming` - Point-free style
- `rank-polymorphism` - Also combinator-based
- `postfix-notation` - RPN
