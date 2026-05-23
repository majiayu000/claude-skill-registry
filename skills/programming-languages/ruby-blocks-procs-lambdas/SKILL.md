---
name: ruby-blocks-procs-lambdas
description: Use when working with Ruby blocks, procs, lambdas, and functional programming patterns including closures and higher-order functions.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Ruby Blocks, Procs, and Lambdas

Master Ruby's functional programming features with blocks, procs, and lambdas. These are fundamental to Ruby's expressive and elegant style.

## Blocks

### Basic Block Syntax

```ruby
# Block with do...end (multi-line)
[1, 2, 3].each do |num|
  puts num * 2
end

# Block with {...} (single line)
[1, 2, 3].each { |num| puts num * 2 }
```

### Yielding to Blocks

```ruby
def repeat(times)
  times.times do
    yield  # Execute the block
  end
end

repeat(3) { puts "Hello" }

# With block parameters
def greet
  yield("World")
end

greet { |name| puts "Hello, #{name}!" }
```

### Block Arguments

```ruby
def process_data(data)
  result = yield(data)
  puts "Result: #{result}"
end

process_data(10) { |x| x * 2 }  # Result: 20
```

### Checking for Blocks

```ruby
def optional_block
  if block_given?
    yield
  else
    puts "No block provided"
  end
end

optional_block { puts "Block executed" }
optional_block
```

### Block Local Variables

```ruby
x = 10

[1, 2, 3].each do |num; local_var|
  local_var = num * 2  # local_var only exists in block
  puts local_var
end

puts x  # 10 (unchanged)
```

## Procs

### Creating Procs

```ruby
# Using Proc.new
my_proc = Proc.new { |x| x * 2 }
puts my_proc.call(5)  # 10

# Using proc method (deprecated in some versions)
my_proc = proc { |x| x * 2 }

# Using -> (stabby lambda syntax for Proc)
my_proc = ->(x) { x * 2 }
```

### Proc Characteristics

```ruby
# Procs don't care about argument count
flexible_proc = Proc.new { |x, y| "x: #{x}, y: #{y}" }
puts flexible_proc.call(1)     # x: 1, y:
puts flexible_proc.call(1, 2, 3)  # x: 1, y: 2 (ignores extra)

# Procs return from the enclosing method
def proc_return
  my_proc = Proc.new { return "from proc" }
  my_proc.call
  "after proc"  # Never reached
end

puts proc_return  # "from proc"
```

### Passing Procs as Arguments

```ruby
def execute_proc(my_proc)
  my_proc.call
end

greeting = Proc.new { puts "Hello from proc!" }
execute_proc(greeting)
```

### Converting Blocks to Procs

```ruby
def method_with_proc(&block)
  block.call
end

method_with_proc { puts "Block converted to proc" }
```

## Lambdas

### Creating Lambdas

```ruby
# Using lambda keyword
my_lambda = lambda { |x| x * 2 }

# Using -> (stabby lambda)
my_lambda = ->(x) { x * 2 }

# Multi-line stabby lambda
my_lambda = ->(x) do
  result = x * 2
  result + 1
end

puts my_lambda.call(5)  # 11
```

### Lambda Characteristics

```ruby
# Lambdas enforce argument count
strict_lambda = ->(x, y) { x + y }
# strict_lambda.call(1)     # ArgumentError
strict_lambda.call(1, 2)    # Works

# Lambdas return to the caller
def lambda_return
  my_lambda = -> { return "from lambda" }
  my_lambda.call
  "after lambda"  # This IS reached
end

puts lambda_return  # "after lambda"
```

### Lambda with Multiple Arguments

```ruby
add = ->(x, y) { x + y }
multiply = ->(x, y, z) { x * y * z }

puts add.call(3, 4)         # 7
puts multiply.call(2, 3, 4) # 24

# Default arguments
greet = ->(name = "World") { "Hello, #{name}!" }
puts greet.call           # "Hello, World!"
puts greet.call("Ruby")   # "Hello, Ruby!"
```

## Proc vs Lambda

```ruby
# Argument handling
my_proc = Proc.new { |x, y| puts "x: #{x}, y: #{y}" }
my_lambda = ->(x, y) { puts "x: #{x}, y: #{y}" }

my_proc.call(1)     # Works: x: 1, y:
# my_lambda.call(1) # ArgumentError

# Return behavior
def test_return
  proc_test = Proc.new { return "proc return" }
  lambda_test = -> { return "lambda return" }

  proc_test.call   # Returns from method
  "end"            # Never reached
end

def test_lambda
  lambda_test = -> { return "lambda return" }
  lambda_test.call # Returns from lambda
  "end"            # This IS reached
end

# Check if it's a lambda
my_proc = Proc.new { }
my_lambda = -> { }

puts my_proc.lambda?   # false
puts my_lambda.lambda? # true
```

## Closures

```ruby
def multiplier(factor)
  ->(x) { x * factor }
end

times_two = multiplier(2)
times_three = multiplier(3)

puts times_two.call(5)    # 10
puts times_three.call(5)  # 15

# Closures capture variables
def counter
  count = 0

  increment = -> { count += 1 }
  decrement = -> { count -= 1 }
  value = -> { count }

  [increment, decrement, value]
end

inc, dec, val = counter
inc.call
inc.call
puts val.call  # 2
dec.call
puts val.call  # 1
```

## Method Objects

```ruby
class Calculator
  def add(x, y)
    x + y
  end
end

calc = Calculator.new
add_method = calc.method(:add)
puts add_method.call(3, 4)  # 7

# Converting methods to procs
add_proc = calc.method(:add).to_proc
puts add_proc.call(5, 6)  # 11
```

## Symbol to Proc

```ruby
# & converts symbol to proc
numbers = [1, 2, 3, 4, 5]

# These are equivalent:
numbers.map { |n| n.to_s }
numbers.map(&:to_s)

# Works with any method
["hello", "world"].map(&:upcase)  # ["HELLO", "WORLD"]
[1, 2, 3].select(&:even?)         # [2]
```

## Higher-Order Functions

```ruby
def compose(f, g)
  ->(x) { f.call(g.call(x)) }
end

double = ->(x) { x * 2 }
square = ->(x) { x * x }

double_then_square = compose(square, double)
puts double_then_square.call(3)  # 36 (3 * 2 = 6, 6 * 6 = 36)
```

## Currying

```ruby
# Manual currying
add = ->(x) { ->(y) { x + y } }
add_five = add.call(5)
puts add_five.call(3)  # 8

# Built-in currying
multiply = ->(x, y, z) { x * y * z }
curried = multiply.curry
times_two = curried.call(2)
times_two_three = times_two.call(3)
puts times_two_three.call(4)  # 24

# Partial application
puts curried.call(2, 3).call(4)  # 24
```

## Practical Patterns

### Lazy Evaluation

```ruby
def lazy_value
  puts "Computing expensive value..."
  42
end

# Wrap in lambda for lazy evaluation
lazy = -> { lazy_value }

puts "Before call"
result = lazy.call  # Only computed here
puts result
```

### Callback Pattern

```ruby
class Button
  def initialize
    @on_click = []
  end

  def on_click(&block)
    @on_click << block
  end

  def click
    @on_click.each(&:call)
  end
end

button = Button.new
button.on_click { puts "Button clicked!" }
button.on_click { puts "Another handler" }
button.click
```

### Strategy Pattern

```ruby
class Sorter
  def initialize(strategy)
    @strategy = strategy
  end

  def sort(array)
    @strategy.call(array)
  end
end

ascending = ->(arr) { arr.sort }
descending = ->(arr) { arr.sort.reverse }

sorter = Sorter.new(ascending)
puts sorter.sort([3, 1, 2])  # [1, 2, 3]

sorter = Sorter.new(descending)
puts sorter.sort([3, 1, 2])  # [3, 2, 1]
```

### Memoization

```ruby
def memoize(&block)
  cache = {}
  ->(arg) do
    cache[arg] ||= block.call(arg)
  end
end

expensive_operation = memoize do |n|
  puts "Computing for #{n}..."
  n * n
end

puts expensive_operation.call(5)  # Computing for 5... 25
puts expensive_operation.call(5)  # 25 (cached)
```

## Best Practices

1. **Use blocks for simple iteration** and single-use closures
2. **Use lambdas for strict argument checking** and returnable closures
3. **Use procs for flexible argument handling** (rare cases)
4. **Prefer -> syntax** for lambdas (more concise)
5. **Use &:symbol** for simple method calls on collections
6. **Leverage closures** for encapsulation and data privacy
7. **Use block_given?** before yielding to optional blocks

## Anti-Patterns

❌ **Don't use Proc.new for strict behavior** - use lambda instead
❌ **Don't ignore return behavior** - understand proc vs lambda differences
❌ **Don't overuse closures** - can lead to memory leaks if not careful
❌ **Don't create deeply nested lambdas** - hard to read and debug
❌ **Don't forget to handle missing blocks** - check with block_given?

## Related Skills

- ruby-oop - For understanding method context
- ruby-metaprogramming - For dynamic block/proc usage
- ruby-standard-library - For Enumerable methods using blocks
