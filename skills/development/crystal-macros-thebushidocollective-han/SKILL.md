---
name: crystal-macros
description: Use when implementing compile-time metaprogramming in Crystal using macros for code generation, DSLs, compile-time computation, and abstract syntax tree manipulation.
allowed-tools: [Bash, Read]
---

# Crystal Macros

You are Claude Code, an expert in Crystal's macro system and compile-time
metaprogramming. You specialize in building powerful abstractions, DSLs, and
code generation systems using Crystal's compile-time execution capabilities.

Your core responsibilities:

- Write macros for code generation and boilerplate reduction
- Build domain-specific languages (DSLs) using macro methods
- Implement compile-time computations and validations
- Generate methods, classes, and modules dynamically
- Manipulate abstract syntax trees (AST) at compile time
- Create type-safe abstractions through macro expansion
- Build debugging and introspection tools
- Implement compile-time configuration and feature flags
- Generate serialization and deserialization code
- Design annotation-based programming patterns

## Macro Basics

Macros run at compile time and receive AST nodes as arguments. They can generate
and return code that gets inserted into the program.

### Simple Macro Definition

```crystal
# Basic macro that generates a method
macro define_getter(name)
  def {{name}}
    @{{name}}
  end
end

class Person
  def initialize(@name : String, @age : Int32)
  end

  define_getter name
  define_getter age
end

person = Person.new("Alice", 30)
puts person.name  # Generated method
puts person.age   # Generated method
```

### Macro with Multiple Arguments

```crystal
macro define_property(name, type)
  @{{name}} : {{type}}?

  def {{name}} : {{type}}?
    @{{name}}
  end

  def {{name}}=(value : {{type}})
    @{{name}} = value
  end
end

class Config
  define_property host, String
  define_property port, Int32
  define_property ssl, Bool

  def initialize
  end
end

config = Config.new
config.host = "localhost"
config.port = 8080
puts config.host
```

### Macro with Block

```crystal
macro measure_time(name, &block)
  start_time = Time.monotonic
  {{yield}}
  elapsed = Time.monotonic - start_time
  puts "{{name}} took #{elapsed.total_milliseconds}ms"
end

measure_time("database query") do
  sleep 0.5
  # Database operation here
end
```

## String Interpolation in Macros

Macros use `{{}}` for interpolation and can generate identifiers, literals, and code.

### Generating Method Names

```crystal
macro define_flag_methods(name)
  def {{name}}?
    @{{name}}
  end

  def {{name}}!
    @{{name}} = true
  end

  def clear_{{name}}
    @{{name}} = false
  end
end

class FeatureFlags
  def initialize
    @feature_a = false
    @feature_b = false
  end

  define_flag_methods feature_a
  define_flag_methods feature_b
end

flags = FeatureFlags.new
flags.feature_a!
puts flags.feature_a?  # true
flags.clear_feature_a
puts flags.feature_a?  # false
```

### Generating with String Manipulation

```crystal
macro define_enum_helpers(enum_type)
  {% for member in enum_type.resolve.constants %}
    def {{member.downcase.id}}?
      self == {{enum_type}}::{{member}}
    end
  {% end %}
end

enum Status
  Pending
  Running
  Completed
  Failed
end

class Job
  def initialize(@status : Status)
  end

  def status
    @status
  end

  # Generate pending?, running?, completed?, failed?
  define_enum_helpers Status
end

job = Job.new(Status::Pending)
puts job.pending?    # true
puts job.running?    # false
```

## Compile-Time Iteration

Macros can iterate over collections at compile time using `{% for %}`.

### Iterating Over Arrays

```crystal
macro define_constants(*names)
  {% for name, index in names %}
    {{name.upcase.id}} = {{index}}
  {% end %}
end

class ErrorCodes
  define_constants success, not_found, unauthorized, server_error
end

puts ErrorCodes::SUCCESS        # 0
puts ErrorCodes::NOT_FOUND      # 1
puts ErrorCodes::UNAUTHORIZED   # 2
puts ErrorCodes::SERVER_ERROR   # 3
```

### Iterating Over Hash Literals

```crystal
macro define_validators(**rules)
  {% for name, validator in rules %}
    def validate_{{name.id}}(value)
      {{validator}}
    end
  {% end %}
end

class Validator
  define_validators(
    email: /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i,
    phone: /\A\d{3}-\d{3}-\d{4}\z/,
    zip_code: /\A\d{5}(-\d{4})?\z/
  )
end

validator = Validator.new
puts validator.validate_email("test@example.com")
puts validator.validate_phone("555-123-4567")
```

### Iterating Over Type Methods

```crystal
macro log_all_methods(type)
  {% for method in type.resolve.methods %}
    puts "Method: {{method.name}}"
  {% end %}
end

class Calculator
  def add(a, b)
    a + b
  end

  def subtract(a, b)
    a - b
  end
end

# At compile time, this generates puts statements
macro list_calculator_methods
  log_all_methods Calculator
end
```

## Conditional Compilation

Use `{% if %}` for compile-time conditionals based on flags, types, or expressions.

### Platform-Specific Code

```crystal
macro platform_specific_path
  {% if flag?(:windows) %}
    "C:\\Program Files\\MyApp"
  {% elsif flag?(:darwin) %}
    "/Applications/MyApp.app"
  {% elsif flag?(:linux) %}
    "/usr/local/bin/myapp"
  {% else %}
    "/tmp/myapp"
  {% end %}
end

DEFAULT_PATH = {{platform_specific_path}}
puts DEFAULT_PATH
```

### Feature Flags

```crystal
macro with_feature(flag, &block)
  {% if flag?(flag) %}
    {{yield}}
  {% end %}
end

class Application
  with_feature(:debug) do
    def debug_info
      puts "Debug mode enabled"
    end
  end

  with_feature(:metrics) do
    def record_metric(name, value)
      puts "Recording #{name}: #{value}"
    end
  end
end

# Compile with: crystal build app.cr -Ddebug -Dmetrics
```

### Type-Based Conditionals

```crystal
macro generate_serializer(type)
  {% if type.resolve < Number %}
    def serialize_{{type.name.downcase.id}}(value : {{type}}) : String
      value.to_s
    end
  {% elsif type.resolve == String %}
    def serialize_{{type.name.downcase.id}}(value : {{type}}) : String
      value.inspect
    end
  {% elsif type.resolve < Array %}
    def serialize_{{type.name.downcase.id}}(value : {{type}}) : String
      "[" + value.map(&.to_s).join(", ") + "]"
    end
  {% end %}
end

class Serializer
  generate_serializer Int32
  generate_serializer String
  generate_serializer Array(Int32)
end

s = Serializer.new
puts s.serialize_int32(42)
puts s.serialize_string("hello")
puts s.serialize_array_int32([1, 2, 3])
```

## AST Node Types

Macros receive different types of AST nodes. Understanding these is crucial.

### Inspecting AST Nodes

```crystal
macro show_ast(expression)
  {{expression.class_name}}
end

# NumberLiteral
puts {{show_ast(42)}}

# StringLiteral
puts {{show_ast("hello")}}

# Call
puts {{show_ast(foo.bar)}}

# ArrayLiteral
puts {{show_ast([1, 2, 3])}}
```

### Working with Identifiers

```crystal
macro create_accessor(name)
  # name is a SymbolLiteral or StringLiteral
  # Convert to identifier with .id
  def {{name.id}}
    @{{name.id}}
  end

  def {{name.id}}=(value)
    @{{name.id}} = value
  end
end

class User
  def initialize
    @username = ""
  end

  create_accessor :username
end
```

### Manipulating String Literals

```crystal
macro define_constants_from_string(str)
  {% parts = str.split(",") %}
  {% for part in parts %}
    {{part.strip.upcase.id}} = {{part.strip.id.stringify}}
  {% end %}
end

module Colors
  define_constants_from_string("red, green, blue, yellow")
end

puts Colors::RED     # "red"
puts Colors::GREEN   # "green"
puts Colors::BLUE    # "blue"
puts Colors::YELLOW  # "yellow"
```

## Advanced Macro Patterns

### Building a DSL for Routes

```crystal
macro route(method, path, handler)
  {% ROUTES ||= [] of {String, String, String} %}
  {% ROUTES << {method.stringify, path, handler.stringify} %}
end

macro compile_routes
  ROUTES_MAP = {
    {% for route in ROUTES %}
      {{route[1]}} => {{route[2].id}},
    {% end %}
  }

  def handle_request(method : String, path : String)
    handler_name = ROUTES_MAP[path]?
    return not_found unless handler_name

    case handler_name
    {% for route in ROUTES %}
    when {{route[2]}}
      {{route[2].id}}
    {% end %}
    end
  end
end

class WebApp
  route :get, "/", :index
  route :get, "/about", :about
  route :post, "/users", :create_user

  def index
    "Home Page"
  end

  def about
    "About Page"
  end

  def create_user
    "Create User"
  end

  def not_found
    "404 Not Found"
  end

  compile_routes
end
```

### Automatic JSON Serialization

```crystal
macro json_serializable(*fields)
  def to_json(builder : JSON::Builder)
    builder.object do
      {% for field in fields %}
        builder.field {{field.stringify}} do
          @{{field.id}}.to_json(builder)
        end
      {% end %}
    end
  end

  def self.from_json(parser : JSON::PullParser)
    instance = allocate
    {% for field in fields %}
      {{field.id}} = nil
    {% end %}

    parser.read_object do |key|
      case key
      {% for field in fields %}
      when {{field.stringify}}
        {{field.id}} = typeof(instance.@{{field.id}}).from_json(parser)
      {% end %}
      end
    end

    {% for field in fields %}
      instance.@{{field.id}} = {{field.id}}.not_nil!
    {% end %}

    instance
  end
end

class User
  def initialize(@name : String, @age : Int32, @email : String)
  end

  json_serializable name, age, email
end

user = User.new("Alice", 30, "alice@example.com")
json = user.to_json
puts json
```

### Compile-Time Configuration

```crystal
macro configure(&block)
  {% begin %}
    {% config = {} of String => ASTNode %}
    {{yield}}
    {% for key, value in config %}
      {{key.upcase.id}} = {{value}}
    {% end %}
  {% end %}
end

macro set(key, value)
  {% config[key.stringify] = value %}
end

configure do
  set :app_name, "MyApp"
  set :version, "1.0.0"
  set :max_connections, 100
  set :debug, true
end

puts APP_NAME           # "MyApp"
puts VERSION            # "1.0.0"
puts MAX_CONNECTIONS    # 100
puts DEBUG              # true
```

## Macro Methods

Macro methods are called on types and can access compile-time type information.

### Generating Methods from Type Info

```crystal
class Model
  macro inherited
    # Called when a class inherits from Model
    def self.table_name : String
      {{@type.name.underscore.id.stringify}}
    end

    def self.column_names : Array(String)
      [
        {% for ivar in @type.instance_vars %}
          {{ivar.name.stringify}},
        {% end %}
      ]
    end
  end
end

class User < Model
  def initialize(@name : String, @email : String, @age : Int32)
  end
end

puts User.table_name       # "user"
puts User.column_names     # ["name", "email", "age"]
```

### Property Introspection

```crystal
class Base
  macro generate_initializer
    def initialize(
      {% for ivar in @type.instance_vars %}
        @{{ivar.name}} : {{ivar.type}},
      {% end %}
    )
    end

    def to_s(io : IO)
      io << "{{@type.name}}("
      {% for ivar, index in @type.instance_vars %}
        {% if index > 0 %}
          io << ", "
        {% end %}
        io << "{{ivar.name}}="
        @{{ivar.name}}.inspect(io)
      {% end %}
      io << ")"
    end
  end
end

class Person < Base
  @name : String
  @age : Int32
  @city : String

  generate_initializer
end

person = Person.new("Bob", 25, "NYC")
puts person  # Person(name="Bob", age=25, city="NYC")
```

### Method Delegation

```crystal
macro delegate(*methods, to target)
  {% for method in methods %}
    def {{method.id}}(*args, **kwargs)
      @{{target.id}}.{{method.id}}(*args, **kwargs)
    end

    def {{method.id}}(*args, **kwargs, &block)
      @{{target.id}}.{{method.id}}(*args, **kwargs) { |*yield_args| yield *yield_args }
    end
  {% end %}
end

class UserRepository
  def find(id : Int32)
    "User #{id}"
  end

  def all
    ["User 1", "User 2"]
  end

  def create(name : String)
    "Created #{name}"
  end
end

class UserService
  def initialize
    @repository = UserRepository.new
  end

  delegate find, all, create, to: repository
end

service = UserService.new
puts service.find(1)
puts service.all
```

## Debugging Macros

### Compile-Time Printing

```crystal
macro debug_print(value)
  {{puts value}}
  {{value}}
end

# This will print at compile time
result = {{debug_print(42 + 8)}}

# Print type information at compile time
macro show_type_info(type)
  {% puts "Type: #{type.resolve}" %}
  {% puts "Instance vars: #{type.resolve.instance_vars.map(&.name)}" %}
  {% puts "Methods: #{type.resolve.methods.map(&.name)}" %}
end

class Example
  @x : Int32 = 0
  @y : String = ""

  def foo
  end

  def bar
  end
end

{{show_type_info(Example)}}
```

### Macro Expansion Inspection

```crystal
# Use --no-codegen flag to see macro expansion
# crystal build --no-codegen app.cr

macro verbose_property(name, type)
  {{puts "Generating property #{name} of type #{type}"}}

  @{{name}} : {{type}}?

  def {{name}} : {{type}}?
    {{puts "Generating getter for #{name}"}}
    @{{name}}
  end

  def {{name}}=(value : {{type}})
    {{puts "Generating setter for #{name}"}}
    @{{name}} = value
  end
end

class Config
  verbose_property timeout, Int32
  verbose_property host, String
end
```

## When to Use This Skill

Use the crystal-macros skill when you need to:

- Reduce boilerplate code through code generation
- Build domain-specific languages (DSLs) for configuration or business logic
- Generate repetitive methods, classes, or modules
- Implement compile-time validation and type checking
- Create property definitions with custom behavior
- Generate serialization/deserialization code
- Build annotation-based programming patterns
- Implement automatic delegation or proxying
- Create compile-time configuration systems
- Generate database models from schema definitions
- Build testing frameworks with custom assertions
- Implement compile-time dependency injection
- Create type-safe builder patterns
- Generate API clients from specifications
- Implement aspect-oriented programming patterns

## Best Practices

1. **Keep Macros Simple**: Break complex macros into smaller, composable pieces
2. **Document Macro Behavior**: Explain what code the macro generates and why
3. **Use Meaningful Names**: Macro names should clearly indicate what they generate
4. **Validate Inputs**: Check macro arguments at compile time when possible
5. **Prefer Macro Methods**: Use macro methods over top-level macros for type-specific logic
6. **Use `{{yield}}`**: Pass blocks to macros for flexible code generation
7. **Debug with `{{puts}}`**: Print AST nodes and values during macro development
8. **Test Generated Code**: Verify that macro-generated code works as expected
9. **Avoid Overuse**: Only use macros when the benefit outweighs the complexity
10. **Use Type Information**: Leverage `@type` and reflection for powerful abstractions
11. **Handle Edge Cases**: Consider nil values, empty collections, and type variations
12. **Maintain Readability**: Generated code should be as readable as hand-written code
13. **Version Carefully**: Macro changes can break downstream code; version appropriately
14. **Use Conditional Compilation**: Leverage flags for platform-specific or feature-specific code
15. **Document Expansion**: Show example of expanded code in macro documentation

## Common Pitfalls

1. **Forgetting `.id` Conversion**: Literals must be converted to identifiers with `.id`
2. **String vs Symbol Confusion**: Know when to use stringify vs literal interpolation
3. **Infinite Macro Recursion**: Recursive macros must have proper termination conditions
4. **Scope Issues**: Variables in macro scope vs generated code scope can conflict
5. **Type Resolution Timing**: Some type information isn't available during early compilation
6. **Missing Nil Checks**: Generated code may not handle nil properly
7. **Hardcoded Assumptions**: Macros assuming specific type structures that may change
8. **Poor Error Messages**: Compilation errors in generated code are hard to debug
9. **Overusing Global State**: Class variables in macros can cause unexpected behavior
10. **Not Handling Empty Collections**: Iterating over empty arrays/hashes without checks
11. **Syntax Errors in Templates**: Invalid Crystal syntax in macro bodies causes confusing errors
12. **Type Mismatch**: Generated code doesn't match expected types
13. **Namespace Pollution**: Generating too many methods or constants in global scope
14. **Platform Dependencies**: Not handling platform differences in macro logic
15. **Circular Dependencies**: Macros that depend on types that depend on the same macros

## Resources

- [Crystal Macros Guide](https://crystal-lang.org/reference/syntax_and_semantics/macros.html)
- [Crystal API - Macros](https://crystal-lang.org/api/Crystal/Macros.html)
- [Crystal Metaprogramming](https://crystal-lang.org/reference/syntax_and_semantics/macros/macro_methods.html)
- [Crystal Macro Hooks](https://crystal-lang.org/reference/syntax_and_semantics/macros/hooks.html)
- [Crystal AST Nodes](https://crystal-lang.org/api/Crystal/Macros/ASTNode.html)
- [Crystal Book - Compile Time Flags](https://crystal-lang.org/reference/syntax_and_semantics/compile_time_flags.html)
- [Effective Crystal - Macro Patterns](https://crystal-lang.org/reference/)
