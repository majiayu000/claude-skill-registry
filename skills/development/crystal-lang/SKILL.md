---
name: crystal-lang
description: "Use this skill when working with the Crystal programming language. Crystal is a statically-typed, compiled language with Ruby-like syntax. It features type inference, null safety, macros, and compiles to efficient native code. Use for understanding Crystal's standard library, syntax, semantics, concurrency model, and FFI bindings."
---

# Crystal-Lang Skill

Use this skill when working with the Crystal programming language. a statically-typed, compiled language with Ruby-like syntax that combines Ruby's coding efficiency with C's runtime performance.

## When to Use This Skill

This skill should be triggered when:
- Writing Crystal code and need syntax, semantic, or API guidance
- Debugging Crystal compilation errors or runtime issues
- Understanding Crystal's type system, type inference, or union types
- Working with Crystal's concurrency model (fibers, channels, spawn)
- Using Crystal macros for metaprogramming and compile-time code generation
- Interfacing with C libraries via FFI bindings
- Implementing web services with the Crystal standard library (HTTP, HTTPS, WebSocket)
- Processing data formats (JSON, XML, YAML, CSV)
- Working with Crystal's standard library APIs

## Key Concepts

### Type System
- **Type Inference**: The compiler infers types without explicit annotations in most cases
- **Union Types**: Variables can have multiple possible types at compile time (e.g., `Int32 | String`)
- **Null Safety**: Nilable types (`String?`) must be checked before use
- **Generic Types**: Reusable code with type parameters (e.g., `Array(T)`, `Hash(K, V)`)

### Concurrency Model
- **Fibers**: Lightweight cooperative threads scheduled by the runtime
- **Channels**: Communication primitives for passing data between fibers
- **spawn**: Create a new fiber for concurrent execution

### Macros
- **Compile-time Execution**: Macros run during compilation, not at runtime
- **AST Manipulation**: Modify and generate code programmatically
- **Flag-based Compilation**: Conditional code based on compile-time flags

## Quick Reference

### Basic Syntax

**Hello World**
```crystal
# hello.cr
puts "Hello, World!"
```

**Variables and Types**
```crystal
name = "Crystal"       # : String
count = 42            # : Int32
pi = 3.14             # : Float64
enabled = true        # : Bool
nothing = nil         # : Nil

# Type annotations work too
x : Int32 = 10
```

**String Interpolation**
```crystal
name = "World"
puts "Hello, #{name}!"   # => Hello, World!
```

### Methods and Blocks

**Defining Methods**
```crystal
def greet(name : String) : String
  "Hello, #{name}!"
end

def add(x : Int32, y : Int32) : Int32
  x + y
end
```

**Default Arguments**
```crystal
def greet(name : String, enthusiastic : Bool = false)
  message = "Hello, #{name}"
  enthusiastic ? "#{message}!" : message
end
```

**Blocks and Procs**
```crystal
# Using a block
[1, 2, 3].map { |x| x * 2 }  # => [2, 4, 6]

# Short syntax
[1, 2, 3].map(&.to_s)        # => ["1", "2", "3"]

# Storing a block
double = ->(x : Int32) { x * 2 }
double.call(5)                # => 10
```

### Control Flow

**If/Else**
```crystal
if count > 0
  puts "Positive"
elsif count < 0
  puts "Negative"
else
  puts "Zero"
end

# Ternary
result = count > 0 ? "positive" : "non-positive"
```

**Case/When**
```crystal
case value
when 1, 2, 3
  puts "Small"
when 4..10
  puts "Medium"
else
  puts "Large"
end
```

**Unless**
```crystal
puts "Access denied" unless user.logged_in?
```

### Classes and Structs

**Class Definition**
```crystal
class Person
  property name : String
  property age : Int32

  def initialize(@name : String, @age : Int32)
  end

  def greet : String
    "Hi, I'm #{@name}, #{@age} years old"
  end
end

person = Person.new("Alice", 30)
person.greet  # => "Hi, I'm Alice, 30 years old"
```

**Inheritance**
```crystal
class Employee < Person
  def initialize(@name : String, @age : Int32, @title : String)
    super(@name, @age)
  end
end
```

**Structs for Value Types**
```crystal
struct Point
  property x : Float64
  property y : Float64

  def initialize(@x : Float64, @y : Float64)
  end
end
```

### Collections

**Arrays**
```crystal
# Literal
numbers = [1, 2, 3, 4, 5]

# Operations
numbers << 6              # append
numbers.first             # => 1
numbers.last              # => 5
numbers.size              # => 5
numbers.includes?(3)      # => true
numbers.map { |x| x * 2 } # => [2, 4, 6, 8, 10]
```

**Hashes**
```crystal
# Literal
scores = {"Alice" => 100, "Bob" => 95}

# Access
scores["Alice"]           # => 100
scores["Charlie"]?        # => nil (safe access)
scores.fetch("Dave", 0)   # => 0 (default)
```

**Ranges**
```crystal
1..10        # inclusive range
1...10       # exclusive range
('a'..'z').to_a.first(3)  # => ['a', 'b', 'c']
```

### Union Types and Nilable Types

**Union Types**
```crystal
def process(value : Int32 | String)
  # Methods must exist for ALL types in the union
  value.to_s
end
```

**Nilable Types**
```crystal
def find_user(id : Int32) : User?
  # Returns User or nil
  users.find { |u| u.id == id }
end

user = find_user(1)
if user
  puts user.name  # user is guaranteed non-nil here
end

# Safe navigation
name = user&.name || "Unknown"
```

**Type Narrowing**
```crystal
value = rand > 0.5 ? 42 : "hello"

if value.is_a?(Int32)
  value.abs  # Compiler knows value is Int32 here
else
  value.size  # Compiler knows value is String here
end
```

### Exception Handling

**Begin/Rescue/Ensure**
```crystal
begin
  File.read("nonexistent.txt")
rescue ex : FileNotFoundError
  puts "File not found: #{ex.message}"
rescue ex : Exception
  puts "Error: #{ex.message}"
ensure
  puts "Cleanup code runs here"
end
```

**Custom Exceptions**
```crystal
class MyError < Exception
end

raise MyError.new("Something went wrong")
```

### Concurrency

**Spawning Fibers**
```crystal
spawn do
  puts "Running in background"
  sleep 1
  puts "Done"
end

puts "Main continues"
Fiber.yield  # Let other fibers run
```

**Channels**
```crystal
channel = Channel(Int32).new

spawn do
  channel.send(42)
end

result = channel.receive  # Blocks until value is available
puts result  # => 42
```

**Async Operations**
```crystal
def fetch_data : String
  "data"
end

# Non-blocking with spawn
spawn { puts fetch_data }
Fiber.yield
```

### Macros

**Compile-time Execution**
```crystal
# Run shell command at compile time
{% `echo "compiled at build time"` %}

# Check compile-time flags
{% if flag?(:x86_64) %}
  puts "Running on 64-bit architecture"
{% end %}
```

**Macro Methods**
```crystal
macro define_method(name, content)
  def {{name}}
    {{content}}
  end
end

define_method(:greet, puts "Hello from macro!")
```

**Reading Files at Compile Time**
```crystal
# Embed file contents at compile time
VERSION = {{ read_file("VERSION.txt").strip }}
```

### File I/O

**Reading Files**
```crystal
# Read entire file
content = File.read("file.txt")

# Read line by line
File.each_line("file.txt") do |line|
  puts line
end

# Check file exists
if File.exists?("file.txt")
  puts "File exists"
end
```

**Writing Files**
```crystal
# Write string to file
File.write("output.txt", "Hello, File!")

# Append to file
File.open("log.txt", "a") do |file|
  file.puts "Log entry"
end
```

### JSON Processing

**Parsing JSON**
```crystal
require "json"

data = JSON.parse(%({"name": "Alice", "age": 30}))
data["name"].as_s  # => "Alice"
data["age"].as_i   # => 30
```

**Generating JSON**
```crystal
require "json"

hash = {"name" => "Bob", "age" => 25}
JSON.build do |json|
  json.object do
    json.field "name", hash["name"]
    json.field "age", hash["age"]
  end
end
```

**JSON Mapping**
```crystal
require "json"

class User
  include JSON::Serializable

  property name : String
  property age : Int32
end

user = User.from_json(%({"name": "Charlie", "age": 35}))
user.to_json  # => %({"name":"Charlie","age":35})
```

### HTTP Client

**Simple GET Request**
```crystal
require "http"

response = HTTP.get("https://api.example.com/data")
puts response.status_code  # => 200
puts response.body
```

**POST with JSON Body**
```crystal
require "http"

response = HTTP.post("https://api.example.com/users",
  headers: {"Content-Type" => "application/json"},
  body: %({"name": "Dave"}).to_json
)
```

**HTTP Client with Persistent Connection**
```crystal
require "http"

client = HTTP::Client.new("https://api.example.com")
response = client.get("/endpoint")
client.close
```

### XML Processing

**Parsing XML**
```crystal
require "xml"

xml = <<-XML
<person id="1">
  <firstname>Jane</firstname>
  <lastname>Doe</lastname>
</person>
XML

document = XML.parse(xml)
person = document.first_element_child
if person
  puts person["id"]         # => "1"
  puts person.content       # => "Jane"
end
```

**Building XML**
```crystal
require "xml"

string = XML.build(indent: "  ") do |xml|
  xml.element("person", id: 1) do
    xml.element("firstname") { xml.text "Jane" }
    xml.element("lastname") { xml.text "Doe" }
  end
end
```

### C Bindings (FFI)

**Declaring External Library**
```crystal
lib LibC
  fun strlen(s : UInt8*) : SizeT
end

# Call C function
LibC.strlen(pointer)
```

**C Linking**
```crystal
@[Link("pcre")]
lib LibPCRE
  fun pcre_compile(pattern : UInt8*) : Pointer(Void)
end
```

**Pointer Operations**
```crystal
x = 1
ptr = pointerof(x)
ptr.value = 2
puts x  # => 2

# Allocated memory
ptr = Pointer.malloc(2, 42)
ptr[0]  # => 42
ptr[1]  # => 42
```

### BitArray

```crystal
require "bit_array"

ba = BitArray.new(12)  # => "BitArray[000000000000]"
ba[2]                  # => false
0.upto(5) { |i| ba[i * 2] = true }
ba                     # => "BitArray[101010101010]"
ba[2]                  # => true
```

### Union Type Operations

```crystal
# Union simplification
Union(Int32 | String)      # => (Int32 | String)
Union(Int32)               # => Int32
Union(Int32, Int32, Int32) # => Int32
```

### Weak References

```crystal
require "weak_ref"

ref = WeakRef.new("oof".reverse)
p ref      # => #<WeakRef(String):...>
GC.collect
p ref      # => #<WeakRef(String):... @target=Pointer.null>
p ref.value  # => nil
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### Getting Started (`getting_started.md`)
- **Source**: Official Crystal documentation (medium confidence)
- **Pages**: 2 (Language Introduction, About this guide)
- **Content**: Beginner-friendly introduction to Crystal's core concepts

### Standard Library (`standard_library.md`)
- **Source**: Official Crystal API documentation (medium confidence)
- **Pages**: 265 (extensive API coverage)
- **Topics**:
  - Core types: Union, WeakRef, Pointer, BitArray
  - I/O operations: XML, JSON, compression, hexdump
  - Networking: HTTP, HTTPS, WebSocket, OpenSSL
  - System: GC stats, event loop, LLVM integration
  - Standard library utilities

### Syntax and Semantics (`syntax_and_semantics.md`)
- **Source**: Official Crystal language reference (medium confidence)
- **Pages**: 351 (comprehensive language specification)
- **Topics**:
  - Crystal::Macros module for compile-time metaprogramming
  - Event loop and concurrency primitives
  - Type system details (generics, unions, nilable types)
  - Inheritance and type relationships
  - C bindings and FFI
  - Language semantics and features

## Working with This Skill

### For Beginners
1. Start with the **Getting Started** reference for language introduction
2. Review the basic syntax examples in the Quick Reference above
3. Practice with simple programs before moving to advanced topics

### For Intermediate Users
1. Use **Syntax and Semantics** for understanding type system details
2. Reference the **Standard Library** for available APIs
3. Explore macros for compile-time code generation

### For Advanced Users
1. Dive into C bindings for performance-critical code
2. Study concurrency patterns with fibers and channels
3. Use advanced macro techniques for metaprogramming

### Navigation Tips
- Search reference files using the "URL:" markers to locate specific API docs
- Code examples include language tags for syntax highlighting
- Macro examples use `{% %}` for compile-time code
- Type annotations use `# : TypeName` comments

## Resources

### Official Documentation
- [Crystal Website](https://crystal-lang.org)
- [API Reference](https://crystal-lang.org/api)
- [Language Reference](https://crystal-lang.org/reference)
- [Playground](https://play.crystal-lang.org)

### Community
- Crystal Forum
- Gitter channel
- IRC: #crystal-lang at irc.libera.chat
- Stack Overflow: crystal-lang tag
- GitHub: crystal-lang/crystal

## Notes

- This skill synthesizes knowledge from official Crystal documentation
- Documentation version: 1.18
- Crystal prioritizes backward compatibility within major versions
- The language is statically-typed but with powerful type inference
- Compile-time macros enable zero-cost abstractions

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper
2. The skill will be rebuilt with the latest information from official sources
