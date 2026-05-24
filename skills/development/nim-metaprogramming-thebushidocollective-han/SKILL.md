---
name: Nim Metaprogramming
description: Use when nim's metaprogramming including macros, templates, compile-time evaluation, AST manipulation, code generation, DSL creation, and leveraging compile-time computation for performance and abstraction in systems programming.
allowed-tools: []
---

# Nim Metaprogramming

## Introduction

Nim's metaprogramming system provides powerful compile-time code generation and
manipulation through templates, macros, and compile-time evaluation. This enables
zero-overhead abstractions, domain-specific languages, and optimizations performed
at compile time rather than runtime.

The system operates on Nim's abstract syntax tree (AST), allowing inspection and
transformation of code structure. Templates provide hygienic macro-like substitution,
while macros enable full AST manipulation. Compile-time evaluation executes Nim
code during compilation for constant folding and validation.

This skill covers templates for code substitution, macros for AST transformation,
compile-time evaluation with static blocks, AST inspection and manipulation, code
generation patterns, DSL creation, and metaprogramming best practices.

## Templates

Templates provide hygienic code substitution with type safety and inline expansion.

```nim
# Basic template
template max(a, b: untyped): untyped =
  if a > b: a else: b

echo max(5, 10)  # Expands inline

# Template with multiple statements
template withFile(filename: string, body: untyped): untyped =
  let file = open(filename, fmRead)
  try:
    body
  finally:
    file.close()

withFile("data.txt"):
  for line in file.lines:
    echo line

# Template with inject
template defineProperty(name: untyped, typ: typedesc): untyped =
  var `name Value`: typ

  proc `get name`(): typ {.inject.} =
    `name Value`

  proc `set name`(value: typ) {.inject.} =
    `name Value` = value

defineProperty(age, int)
setAge(30)
echo getAge()  # 30

# Template accepting block
template benchmark(name: string, code: untyped): untyped =
  let start = cpuTime()
  code
  let elapsed = cpuTime() - start
  echo name, ": ", elapsed, " seconds"

benchmark "computation":
  var sum = 0
  for i in 1..1000000:
    sum += i

# Template with typed parameters
template swap(a, b: typed): untyped =
  let tmp = a
  a = b
  b = tmp

var x = 5
var y = 10
swap(x, y)
echo x, " ", y  # 10 5

# Template for DSL
template html(body: untyped): string =
  var result = ""
  template tag(name: string, content: untyped): untyped =
    result.add "<" & name & ">"
    content
    result.add "</" & name & ">"

  body
  result

let page = html:
  tag "html":
    tag "body":
      tag "h1":
        result.add "Hello World"

# Template with generic constraints
template findMax[T: Ordinal](items: openArray[T]): T =
  var maxVal = items[0]
  for item in items:
    if item > maxVal:
      maxVal = item
  maxVal

echo findMax([1, 5, 3, 9, 2])

# Template forwarding
template forward(call: untyped): untyped =
  echo "Before call"
  call
  echo "After call"

proc myProc() =
  echo "Inside proc"

forward myProc()

# Template for custom operators
template `~=`(a, b: float): bool =
  abs(a - b) < 0.0001

echo 1.0 ~= 1.00001  # true

# Template with immediate parameter
template log(msg: string): untyped =
  when defined(debug):
    echo "[LOG] ", msg

log "Debug message"  # Only in debug builds
```

Templates provide compile-time code substitution with hygiene and type safety.

## Macros and AST Manipulation

Macros transform AST at compile time, enabling powerful code generation and
domain-specific languages.

```nim
import macros

# Basic macro
macro debug(n: varargs[typed]): untyped =
  result = newStmtList()
  for arg in n:
    result.add quote do:
      echo astToStr(`arg`), " = ", `arg`

let x = 5
let y = 10
debug x, y, x + y

# Macro examining AST
macro inspect(node: untyped): untyped =
  echo node.treeRepr
  result = node

inspect:
  let x = 5 + 3

# Building AST manually
macro makeProc(name: untyped, body: untyped): untyped =
  result = newProc(
    name = name,
    params = [newEmptyNode()],
    body = body
  )

makeProc greet:
  echo "Hello!"

greet()

# Macro for property generation
macro property(name: untyped, typ: typedesc): untyped =
  let
    fieldName = ident($name & "Field")
    getName = ident("get" & $name)
    setName = ident("set" & $name)

  result = quote do:
    var `fieldName`: `typ`

    proc `getName`(): `typ` =
      `fieldName`

    proc `setName`(value: `typ`) =
      `fieldName` = value

property(count, int)
setCount(42)
echo getCount()

# Case statement macro
macro switch(value: typed, branches: varargs[untyped]): untyped =
  result = nnkCaseStmt.newTree(value)

  for branch in branches:
    expectKind(branch, nnkCall)
    let pattern = branch[0]
    let body = branch[1]
    result.add nnkOfBranch.newTree(pattern, body)

switch(5):
  1: echo "one"
  2: echo "two"
  5: echo "five"

# Builder pattern macro
macro build(typ: typedesc, fields: varargs[untyped]): untyped =
  result = nnkObjConstr.newTree(typ)

  for field in fields:
    expectKind(field, nnkExprEqExpr)
    result.add field

type Person = object
  name: string
  age: int

let p = build(Person, name = "Alice", age = 30)

# Compile-time assertion macro
macro staticAssert(condition: bool, message: string): untyped =
  if not condition.boolVal:
    error(message.strVal)
  result = newEmptyNode()

staticAssert sizeof(int) >= 4, "int must be at least 4 bytes"

# Unrolling loop macro
macro unroll(count: static[int], body: untyped): untyped =
  result = newStmtList()
  for i in 0..<count:
    let iNode = newLit(i)
    result.add body.replace(ident("it"), iNode)

unroll 5:
  echo "Iteration: ", it

# Pattern matching macro
macro match(value: typed, patterns: varargs[untyped]): untyped =
  result = nnkIfStmt.newTree()

  for pattern in patterns:
    expectMinLen(pattern, 2)
    let condition = pattern[0]
    let body = pattern[1]

    let check = quote do:
      `value` == `condition`

    result.add nnkElifBranch.newTree(check, body)
```

Macros enable compile-time code transformation and generation through AST
manipulation.

## Compile-Time Evaluation

Nim executes code at compile time for constants, optimizations, and validations.

```nim
# Compile-time constants
const maxSize = 100
const computed = maxSize * 2 + 10  # Evaluated at compile time

# Compile-time function evaluation
proc factorial(n: int): int =
  if n <= 1: 1 else: n * factorial(n - 1)

const fact10 = factorial(10)  # Computed at compile time

# Static block
static:
  echo "This runs at compile time"
  echo "Factorial of 10 is: ", factorial(10)

# Compile-time type information
proc sizeInfo[T](x: T): string =
  static:
    "Size of " & $T & " is " & $sizeof(T) & " bytes"

echo sizeInfo(5)
echo sizeInfo(5.0)

# Compile-time conditional compilation
when sizeof(int) == 8:
  proc printSize() = echo "64-bit platform"
else:
  proc printSize() = echo "32-bit platform"

# Compile-time string operations
const
  version = "1.0.0"
  parts = version.split('.')
  major = parts[0].parseInt

when major >= 1:
  echo "Version 1.0 or later"

# Compile-time file reading
const configData = staticRead("config.txt")

proc getConfig(): string =
  configData

# Compile-time HTTP requests (with stdlib)
const apiResponse = staticExec("curl -s https://api.example.com/data")

# Compile-time code generation
proc generateAccessors(fields: seq[string]): string =
  result = ""
  for field in fields:
    result.add &"""
      proc get{field.capitalizeAscii}(): int = {field}
      proc set{field.capitalizeAscii}(val: int) = {field} = val
    """

const accessors = generateAccessors(@["x", "y", "z"])

# Static parameter constraints
proc processArray[T; N: static[int]](arr: array[N, T]) =
  static:
    echo "Array size: ", N
  for item in arr:
    echo item

processArray([1, 2, 3, 4, 5])

# Compile-time assertions
static:
  doAssert sizeof(int) >= 4, "int too small"
  doAssert sizeof(ptr) == sizeof(int), "pointer size mismatch"

# Compile-time regex compilation
import re

const emailPattern = re"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

proc validateEmail(email: string): bool =
  email.match(emailPattern)

# Compile-time validation
proc validateConfig() =
  static:
    when not fileExists("config.txt"):
      {.fatal: "config.txt not found".}

# Compile-time optimization
proc optimizedPower(base: float, exp: static[int]): float =
  when exp == 0:
    1.0
  elif exp == 1:
    base
  elif exp mod 2 == 0:
    let half = optimizedPower(base, exp div 2)
    half * half
  else:
    base * optimizedPower(base, exp - 1)

echo optimizedPower(2.0, 10)
```

Compile-time evaluation enables zero-runtime-cost abstractions and build-time
validations.

## DSL Creation

Nim's metaprogramming enables creating domain-specific languages with natural
syntax.

```nim
# HTML DSL
macro html(body: untyped): string =
  proc processNode(node: NimNode): NimNode =
    case node.kind
    of nnkCall, nnkCommand:
      let tag = node[0]
      let attrs = newSeq[NimNode]()
      var content = newStmtList()

      for i in 1..<node.len:
        if node[i].kind == nnkExprEqExpr:
          attrs.add node[i]
        else:
          content.add processNode(node[i])

      result = quote do:
        result.add "<" & `tag`.astToStr & ">"
        `content`
        result.add "</" & `tag`.astToStr & ">"
    of nnkStrLit:
      result = quote do:
        result.add `node`
    else:
      result = newStmtList()

  result = quote do:
    var result = ""
    `processNode(body)`
    result

let page = html:
  html:
    head:
      title: "My Page"
    body:
      h1: "Welcome"
      p: "Hello World"

# SQL DSL
macro select(fields: varargs[untyped]): string =
  var fieldList = ""
  for i, field in fields:
    if i > 0: fieldList.add ", "
    fieldList.add $field

  result = newLit("SELECT " & fieldList)

macro fromTable(table: untyped): string =
  newLit(" FROM " & $table)

let query = select(name, age) & fromTable(users)

# Test DSL
macro describe(name: string, tests: untyped): untyped =
  result = newStmtList()

  for test in tests:
    if test.kind == nnkCall and $test[0] == "it":
      let testName = test[1]
      let testBody = test[2]

      result.add quote do:
        echo "Testing: ", `testName`
        try:
          `testBody`
          echo "  ✓ Passed"
        except:
          echo "  ✗ Failed"

describe "Math operations":
  it "adds numbers":
    doAssert 1 + 1 == 2

  it "multiplies numbers":
    doAssert 2 * 3 == 6

# Configuration DSL
macro config(body: untyped): untyped =
  result = nnkObjConstr.newTree(ident("Config"))

  for stmt in body:
    if stmt.kind == nnkCall:
      let key = stmt[0]
      let value = stmt[1]
      result.add nnkExprColonExpr.newTree(key, value)

type Config = object
  host: string
  port: int
  debug: bool

let cfg = config:
  host("localhost")
  port(8080)
  debug(true)

# Builder DSL
macro builder(typ: typedesc, body: untyped): untyped =
  var assignments = newStmtList()

  for stmt in body:
    if stmt.kind == nnkCall:
      let field = stmt[0]
      let value = stmt[1]
      assignments.add quote do:
        result.`field` = `value`

  result = quote do:
    var result: `typ`
    `assignments`
    result

type Request = object
  url: string
  method: string
  headers: seq[string]

let req = builder(Request):
  url("https://api.example.com")
  method("GET")
```

DSLs enable domain-specific notation within Nim while maintaining type safety.

## Code Generation Patterns

Metaprogramming enables automated code generation from specifications or runtime
data.

```nim
# Generate enum from compile-time list
macro generateEnum(name: untyped, values: static[seq[string]]): untyped =
  result = nnkTypeSection.newTree(
    nnkTypeDef.newTree(
      name,
      newEmptyNode(),
      nnkEnumTy.newTree(newEmptyNode())
    )
  )

  for value in values:
    result[0][2].add ident(value)

generateEnum(Color, @["Red", "Green", "Blue"])

# Generate getters/setters
macro generateAccessors(typ: typedesc): untyped =
  let impl = typ.getImpl
  result = newStmtList()

  for field in impl[2][2]:
    let fieldName = field[0]
    let fieldType = field[1]

    let getter = ident("get" & ($fieldName).capitalizeAscii)
    let setter = ident("set" & ($fieldName).capitalizeAscii)

    result.add quote do:
      proc `getter`(obj: `typ`): `fieldType` =
        obj.`fieldName`

      proc `setter`(obj: var `typ`, value: `fieldType`) =
        obj.`fieldName` = value

type Person = object
  name: string
  age: int

generateAccessors(Person)

# Generate pattern matching
macro matchGen(value: typed, patterns: varargs[untyped]): untyped =
  result = nnkCaseStmt.newTree(value)

  for pattern in patterns:
    let condition = pattern[0]
    let body = pattern[1]
    result.add nnkOfBranch.newTree(condition, body)

# Generate state machine
macro stateMachine(states: varargs[untyped]): untyped =
  var stateEnum = nnkEnumTy.newTree(newEmptyNode())

  for state in states:
    stateEnum.add ident($state)

  result = nnkTypeSection.newTree(
    nnkTypeDef.newTree(
      ident("State"),
      newEmptyNode(),
      stateEnum
    )
  )

stateMachine Idle, Running, Stopped

# Generate serialization
macro deriveJson(typ: typedesc): untyped =
  result = newStmtList()

  # Generate toJson proc
  result.add quote do:
    proc toJson(obj: `typ`): JsonNode =
      result = newJObject()
      # Add fields...

# Generate validators
macro validate(typ: typedesc, rules: untyped): untyped =
  result = quote do:
    proc validate(obj: `typ`): bool =
      # Generated validation logic
      true
```

Code generation reduces boilerplate and ensures consistency across similar
implementations.

## Best Practices

1. **Use templates for simple substitutions** to avoid macro complexity when AST
   manipulation isn't needed

2. **Prefer typed macro parameters** over untyped when possible for better type
   checking

3. **Test macros thoroughly** as compile-time errors are harder to debug than
   runtime errors

4. **Document macro usage** with examples since expanded code isn't visible to
   users

5. **Use quote do for AST generation** to write natural Nim code instead of
   manual AST construction

6. **Leverage compile-time evaluation** for validations and optimizations without
   runtime cost

7. **Keep macros focused** on single responsibilities for maintainability

8. **Use static blocks for compile-time** side effects like logging or validation

9. **Provide error messages in macros** using error() for clear compile-time
   failures

10. **Test macro expansions** by examining generated code with dumpTree or
    expandMacros

## Common Pitfalls

1. **Overusing macros** for problems solvable with templates adds unnecessary
   complexity

2. **Not handling AST node kinds** properly causes compilation failures on
   unexpected input

3. **Forgetting hygiene in templates** can capture unintended identifiers from
   calling scope

4. **Creating overly complex macros** makes code hard to understand and maintain

5. **Not validating macro inputs** leads to confusing error messages at macro
   expansion

6. **Mixing runtime and compile-time** code without static blocks causes errors

7. **Assuming AST structure** without checking node kinds breaks on different
   inputs

8. **Not using result variable** in templates returns last statement
   unexpectedly

9. **Creating DSLs that are too magical** reduces code readability and
   maintainability

10. **Forgetting to return nodes** from macros causes empty code generation

## When to Use This Skill

Apply templates for zero-overhead abstractions replacing repetitive patterns.

Use macros when transforming or generating code based on compile-time information.

Leverage compile-time evaluation for constants, validations, and build-time
optimizations.

Create DSLs for domain-specific problems requiring specialized notation.

Generate code for boilerplate like serialization, getters, or pattern matching.

Use metaprogramming for performance-critical abstractions with zero runtime cost.

## Resources

- [Nim Macros Tutorial](<https://nim-lang.org/docs/tut3.html>)
- [Nim Macros Module](<https://nim-lang.org/docs/macros.html>)
- [Nim Manual - Macros](<https://nim-lang.org/docs/manual.html#macros>)
- [Nim by Example - Metaprogramming](<https://nim-by-example.github.io/macros/>)
- [Nim AST Pattern Matching](<https://nim-lang.org/docs/ast_pattern_matching.html>)
