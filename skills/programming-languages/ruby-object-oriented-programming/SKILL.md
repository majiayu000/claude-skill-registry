---
name: ruby-oop
description: Use when working with Ruby's object-oriented programming features including classes, modules, inheritance, mixins, and method visibility.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Ruby Object-Oriented Programming

Master Ruby's elegant object-oriented programming features. Ruby is a pure object-oriented language where everything is an object.

## Class Definition

### Basic Class Structure

```ruby
class Person
  # Class variable (shared across all instances)
  @@count = 0

  # Constant
  MAX_AGE = 150

  # Class method
  def self.count
    @@count
  end

  # Constructor
  def initialize(name, age)
    @name = name  # Instance variable
    @age = age
    @@count += 1
  end

  # Instance method
  def introduce
    "Hi, I'm #{@name} and I'm #{@age} years old"
  end

  # Attribute accessors (getter and setter)
  attr_accessor :name
  attr_reader :age      # Read-only
  attr_writer :email    # Write-only
end

person = Person.new("Alice", 30)
puts person.introduce
person.name = "Alicia"
```

### Method Visibility

```ruby
class BankAccount
  def initialize(balance)
    @balance = balance
  end

  # Public methods (default)
  def deposit(amount)
    @balance += amount
    log_transaction(:deposit, amount)
  end

  def balance
    format_currency(@balance)
  end

  # Protected methods - callable by instances of same class/subclass
  protected

  def log_transaction(type, amount)
    puts "[#{type}] #{amount}"
  end

  # Private methods - only callable within this instance
  private

  def format_currency(amount)
    "$#{amount}"
  end
end
```

## Inheritance

### Single Inheritance

```ruby
class Animal
  def initialize(name)
    @name = name
  end

  def speak
    "Some sound"
  end
end

class Dog < Animal
  def speak
    "Woof! My name is #{@name}"
  end

  # Call parent method with super
  def introduce
    super  # Calls parent's speak method
    puts "I'm a dog"
  end
end

dog = Dog.new("Buddy")
puts dog.speak
```

### Method Override and Super

```ruby
class Vehicle
  def initialize(brand)
    @brand = brand
  end

  def start_engine
    puts "Engine starting..."
  end
end

class Car < Vehicle
  def initialize(brand, model)
    super(brand)  # Call parent constructor
    @model = model
  end

  def start_engine
    super  # Call parent method
    puts "#{@brand} #{@model} is ready to drive"
  end
end
```

## Modules and Mixins

### Module as Namespace

```ruby
module MyApp
  module Utils
    def self.format_date(date)
      date.strftime("%Y-%m-%d")
    end
  end
end

MyApp::Utils.format_date(Time.now)
```

### Module as Mixin

```ruby
module Swimmable
  def swim
    "I'm swimming!"
  end
end

module Flyable
  def fly
    "I'm flying!"
  end
end

class Duck
  include Swimmable  # Instance methods
  include Flyable

  def quack
    "Quack!"
  end
end

duck = Duck.new
puts duck.swim
puts duck.fly
```

### Extend vs Include

```ruby
module Greetable
  def greet
    "Hello!"
  end
end

class Person
  include Greetable  # Adds as instance method
end

class Company
  extend Greetable   # Adds as class method
end

Person.new.greet    # Works
Company.greet       # Works
```

## Advanced OOP Patterns

### Singleton Pattern

```ruby
class Database
  @instance = nil

  private_class_method :new

  def self.instance
    @instance ||= new
  end

  def connect
    puts "Connected to database"
  end
end

db1 = Database.instance
db2 = Database.instance
db1.object_id == db2.object_id  # true
```

### Method Missing (Dynamic Methods)

```ruby
class DynamicAttributes
  def method_missing(method_name, *args)
    attribute = method_name.to_s

    if attribute.end_with?("=")
      # Setter
      instance_variable_set("@#{attribute.chop}", args.first)
    else
      # Getter
      instance_variable_get("@#{attribute}")
    end
  end

  def respond_to_missing?(method_name, include_private = false)
    true
  end
end

obj = DynamicAttributes.new
obj.name = "Ruby"
puts obj.name  # "Ruby"
```

### Class Instance Variables

```ruby
class Product
  @inventory = []

  class << self
    attr_accessor :inventory

    def add(product)
      @inventory << product
    end
  end
end

Product.add("Laptop")
```

## Struct and OpenStruct

### Struct (Immutable-ish)

```ruby
Person = Struct.new(:name, :age) do
  def introduce
    "I'm #{name}, #{age} years old"
  end
end

person = Person.new("Bob", 25)
puts person.name
person.age = 26
```

### OpenStruct (Dynamic Attributes)

```ruby
require 'ostruct'

person = OpenStruct.new
person.name = "Charlie"
person.age = 30
person.email = "charlie@example.com"

puts person.name
```

## Composition Over Inheritance

```ruby
class Engine
  def start
    "Engine started"
  end
end

class Wheels
  def rotate
    "Wheels rotating"
  end
end

class Car
  def initialize
    @engine = Engine.new
    @wheels = Wheels.new
  end

  def start
    @engine.start
  end

  def drive
    @wheels.rotate
  end
end
```

## Comparable and Enumerable

### Making Classes Comparable

```ruby
class Person
  include Comparable

  attr_reader :age

  def initialize(name, age)
    @name = name
    @age = age
  end

  def <=>(other)
    age <=> other.age
  end
end

people = [Person.new("Alice", 30), Person.new("Bob", 25)]
puts people.sort.map(&:age)  # [25, 30]
```

## Class Variables vs Instance Variables

```ruby
class Counter
  @@count = 0      # Class variable (shared)
  @instances = []  # Class instance variable (not shared with subclasses)

  def initialize
    @@count += 1
  end

  def self.count
    @@count
  end
end
```

## Best Practices

1. **Prefer composition over inheritance** for complex relationships
2. **Use modules for mixins** to share behavior across unrelated classes
3. **Keep classes small and focused** (Single Responsibility Principle)
4. **Use attr_accessor/reader/writer** instead of manual getters/setters
5. **Make use of private/protected** to encapsulate implementation details
6. **Prefer instance variables** over class variables to avoid unexpected sharing
7. **Use Struct for simple data objects** instead of full classes
8. **Override to_s for debugging** to provide meaningful string representations

## Anti-Patterns

❌ **Don't use class variables unnecessarily** - they're shared across inheritance hierarchy
❌ **Don't create god objects** - keep classes focused and small
❌ **Don't expose internal state** - use methods instead of direct instance variable access
❌ **Don't overuse inheritance** - prefer composition or modules
❌ **Don't ignore visibility modifiers** - they exist for encapsulation

## Related Skills

- ruby-metaprogramming - For dynamic class/method generation
- ruby-blocks-procs-lambdas - For functional programming patterns
- ruby-modules - For advanced module usage
