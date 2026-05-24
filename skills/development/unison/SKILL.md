---
name: unison
description: Unison language - content-addressed functional programming with abilities for effects, distributed computing, and structural types. Use for pure functional code, effect management, distributed systems, and refactoring-safe codebases.
version: 1.0.0
---


# Unison

Content-addressed functional programming language with first-class effects.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Content-addressed** | Code identified by hash, not name - renames are free |
| **Abilities** | Algebraic effects for IO, Exception, Random, Remote |
| **Structural types** | Types with same structure are identical |
| **UCM** | Unison Codebase Manager - REPL + version control |

## UCM Commands

```bash
# Start UCM
ucm

# Start with specific project
ucm -p myproject/main

# Run compiled program
ucm run.compiled program.uc

# Create codebase at path
ucm -C ./my-codebase
```

### Inside UCM REPL

```
# Project management
project.create myproject
switch myproject/main

# Add code from scratch file
update
add

# Run a function
run helloWorld

# Compile to executable
compile helloWorld output

# Install library from Share
lib.install @unison/http

# Find definitions
find : Text -> Nat
find map

# View definition
view List.map

# Documentation
docs List.map

# Refactoring (rename is instant!)
move.term oldName newName
```

## Syntax Quick Reference

### Functions

```unison
-- Type signature
double : Nat -> Nat
double x = x * 2

-- Multi-argument
add : Nat -> Nat -> Nat
add x y = x + y

-- Lambda
List.map (x -> x * 2) [1, 2, 3]

-- Pipeline operator
[1, 2, 3] |> List.map (x -> x * 2) |> List.filter Nat.isEven
```

### Delayed Computations (Thunks)

```unison
-- Three equivalent ways to delay
main : '{IO, Exception} ()
main = do printLine "hello"

main : '{IO, Exception} ()
main _ = printLine "hello"

main : '{IO, Exception} ()
main = '(printLine "hello")

-- Force with ! or ()
!main
main()
```

### Pattern Matching

```unison
-- Match expression
isEven num = match num with
  n | mod n 2 === 0 -> "even"
  _ -> "odd"

-- Cases shorthand
isEven = cases
  0 -> "zero"
  n | Nat.isEven n -> "even"
  _ -> "odd"

-- As-patterns with @
match Some 12 with
  opt@(Some n) -> "opt binds whole value"
  None -> "none"
```

### Types

```unison
-- Sum type (unique by name)
type LivingThings = Animal | Plant | Fungi

-- Recursive type with parameter
structural type Tree a = Empty | Node a (Tree a) (Tree a)

-- Record type (generates accessors)
type Pet = { age: Nat, species: Text, foods: [Text] }

-- Use generated accessors
Pet.age : Pet -> Nat
Pet.age.set : Nat -> Pet -> Pet
Pet.age.modify : (Nat -> Nat) -> Pet -> Pet
```

### Lists

```unison
-- Literals
[1, 2, 3]

-- Concatenation
[1, 2] List.++ [3, 4]

-- Cons/snoc
use List +: :+
1 +: [2, 3]     -- [1, 2, 3]
[1, 2] :+ 3    -- [1, 2, 3]

-- Transformations
Nat.range 0 10
  |> List.map (x -> x * 100)
  |> List.filter Nat.isEven
  |> List.foldLeft (+) 0
```

### Text

```unison
-- Filter and split
Text.filter isDigit "abc_123_def" |> Text.split ?0
-- ["1", "2", "3"]

-- Pattern matching (regex-like)
Pattern.run (Pattern.capture (Pattern.many (chars "ab"))) "aabb123"
-- Some (["aabb"], "123")
```

## Abilities (Effects)

Abilities are Unison's approach to algebraic effects:

```unison
-- Function using abilities
getRandomElem : [a] ->{Abort, Random} a
getRandomElem list =
  index = natIn 0 (List.size list)
  List.at! index list

-- Handle with splitmix (Random) and toOptional (Abort)
toOptional! do splitmix 42 do getRandomElem [1, 2, 3]
```

### Common Abilities

| Ability | Purpose | Handler |
|---------|---------|---------|
| `IO` | File, network, console | Runtime |
| `Exception` | Raise/catch errors | `catch`, `toEither` |
| `Random` | Random number generation | `splitmix seed` |
| `Abort` | Early termination | `toOptional!` |
| `Remote` | Distributed computation | Cloud runtime |
| `STM` | Software transactional memory | `STM.atomically` |

### Exception Handling

```unison
nonZero : Nat ->{Exception} Nat
nonZero = cases
  0 -> Exception.raise (Generic.failure "Zero found" 0)
  n -> n

-- Catch returns Either
catch do nonZero 0
-- Left (Failure ...)

catch do nonZero 5
-- Right 5
```

### Distributed Computing

```unison
forkedTasks : '{Remote} Nat
forkedTasks = do
  task1 = Remote.fork here! do 1 + 1
  task2 = Remote.fork here! do 2 + 2
  Remote.await task1 + Remote.await task2
```

### Concurrency (STM)

```unison
type STM.TQueue a = TQueue (TVar [a]) (TVar Nat)

TQueue.enqueue : a -> TQueue a ->{STM} ()
TQueue.enqueue a = cases
  TQueue elems _ -> TVar.modify elems (es -> a +: es)

-- Atomic block
result = STM.atomically do
  queue = TQueue.fromList [1, 2, 3]
  TQueue.enqueue 4 queue
  TQueue.dequeue queue
```

## File Operations

```unison
-- Read file
content = readFileUtf8 (FilePath "data.txt")

-- Write file
FilePath.writeFile (FilePath "out.txt") (Text.toUtf8 "hello")

-- Rename
renameFile (FilePath "old.txt") (FilePath "new.txt")
```

## HTTP (with @unison/http)

```bash
myproject/main> lib.install @unison/http
```

```unison
exampleGet : '{IO, Exception, Threads} HttpResponse
exampleGet _ =
  uri = net.URI.parse "https://example.com/api"
  req = do Http.get uri
  Http.run req
```

## Hello World

```unison
-- In scratch.u file
helloWorld : '{IO, Exception} ()
helloWorld = do printLine "Hello World"
```

```
scratch/main> project.create hello-world
hello-world/main> update
hello-world/main> run helloWorld

-- Or compile to binary
hello-world/main> compile helloWorld hello
$ ucm run.compiled hello.uc
```

## Workflow

1. Write code in any `.u` file (scratch file)
2. UCM auto-watches and typechecks
3. Use `update` or `add` to add to codebase
4. Code stored by hash - refactoring is instant
5. Share via Unison Share (`push`, `pull`)

## GF(3) Integration

| Phase | Trit | Unison Pattern |
|-------|------|----------------|
| Validate | -1 | `Exception`, `Abort` abilities |
| Coordinate | 0 | `STM`, handlers, pipelines |
| Generate | +1 | `Remote.fork`, `IO` effects |

---

**Skill Name**: unison  
**Type**: Functional Programming Language  
**Trit**: 0 (ERGODIC - coordination via abilities)  
**Version**: 0.5.49  
**Platform**: Cross-platform (ucm binary)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 9. Generic Procedures

**Concepts**: dispatch, multimethod, predicate dispatch, generic

### GF(3) Balanced Triad

```
unison (+) + SDF.Ch9 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages
- Ch1: Flexibility through Abstraction
- Ch10: Adventure Game Example

### Connection Pattern

Generic procedures dispatch on predicates. This skill selects implementations dynamically.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.