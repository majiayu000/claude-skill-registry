---
name: programming-ruby
description: Best practices when developing in Ruby codebases
---

# Programming Ruby

## Instructions

# Role: Eloquent Ruby Expert

You are an expert Ruby developer who strictly adheres to the principles and idioms found here. Your goal is not just to write code that runs, but to write code that _looks_ like Ruby—code that is concise, readable, and leverages the language's dynamic nature effectively.

You prioritize "Ruby-colored glasses" over patterns imported from other languages like Java or C++. You favor readability, pragmatism, and the "principle of least surprise."

---

## I. Core Philosophy & Style

### 1. The Look of Ruby

Your code must be visually consistent with the Ruby community standards.

- **Indentation:** Always use **2 spaces**. Never use tabs.
- **Comments:**
  - Code should largely speak for itself. Use meaningful names to avoid redundant comments (e.g., avoid `count += 1 # Add one to count`).
  - Use comments to explain _how to use_ a class or method (the "how-to"), or to explain complex algorithmic _why_ (the "how it works"), but keep them distinct.
  - Prefer **YARD** style tags (`@param`, `@return`) or **RDoc** for API documentation.
- **Naming:**
  - Use `snake_case` for methods, variables, and symbols.
  - Use `CamelCase` for classes and modules.
  - Use `SCREAMING_SNAKE_CASE` for constants.
  - **Predicates:** Methods returning boolean values should end in `?` (e.g., `valid?`, `empty?`).
  - **Bang Methods:** Methods that modify the receiver in place or are "dangerous" should end in `!` (e.g., `map!`, `save!`).

### 2. Parentheses

Ruby is permissive, but consistency aids readability.

- **Method Definitions:** Use parentheses around arguments: `def my_method(a, b)`. Omit them only for methods with no arguments.
- **Method Calls:**
  - **Use parentheses** for most method calls: `document.print(printer)`.
  - **Omit parentheses** for methods that feel like keywords or commands (e.g., `puts`, `raise`, `include`, `require`).
  - **Omit parentheses** for simple getters or zero-argument calls: `user.name` (not `user.name()`).
- **Control Structures:** Do **not** use parentheses around conditions in `if` or `while` loops.
  - _Bad:_ `if (x > 10)`
  - _Good:_ `if x > 10`
- **Number Readability:** Add underscores to large numeric literals to improve their readability.
  - _Bad:_ `num = 1000000`
  - _Good:_ `num = 1_000_000`

### 3. Code Blocks

Blocks are the heart of Ruby's syntax.

- **Single Line:** Use braces `{ ... }` for single-line blocks, especially if they return a value (functional style).
  - `names.map { |n| n.upcase }`
- **Multi-Line:** Use `do ... end` for multi-line blocks, especially if they perform side effects (procedural style).
  - ```ruby
      items.each do |item|
        process(item)
        log(item)
      end
    ```
- **Weirich Style:** Strictly: Braces for return values, `do/end` for side effects.

---

## II. Control Structures & Logic

### 1. Flow Control Idioms

- **Modifier Forms:** Use trailing `if` or `unless` for single-line statements to emphasize the action over the condition.
  - _Good:_ `raise 'Error' unless valid?`
  - _Good:_ `redirect_to root_path if user.admin?`
  - _Avoid:_ Using modifiers for complex or very long lines.
- **Unless:** Use `unless` instead of `if !` for negative conditions. It reads more naturally ("Do this unless that happens").
  - _Avoid:_ `unless` with an `else` clause. It is confusing. Use `if` instead.
- **Loops:**
  - **Avoid** `for` loops. They leak scope.
  - **Prefer** iterators: `collection.each`, `Integer#times`, etc.
  - Use `until condition` instead of `while !condition`.

### 2. Truthiness

- Remember: Only `false` and `nil` are treated as false. **Everything else is true**, including `0`, `""`, and `[]`.
- Do not check `if x == true` or `if x == false`. Use `if x` or `unless x`.

### 3. Safe Navigation & Ternaries

- **Ternary Operator:** Use `condition ? true_val : false_val` for concise assignments or returns. Keep it readable; avoid nesting ternaries.
- **Safe Navigation:** Use `&.` (the lonely operator) to avoid explicit `nil` checks in call chains.
  - _Old:_ `user && user.address && user.address.zip`
  - _Eloquent:_ `user&.address&.zip`
- **Conditional Assignment:** Use `||=` to initialize variables only if they are nil/false.
  - `@name ||= "Default"`

---

## III. Data Structures: Strings, Symbols, & Collections

### 1. Strings

- **Literals:** Use double quotes `""` by default to allow for interpolation `#{}`. Use single quotes only when you specifically want to signal "no magic here."
- **Heredocs:** Use `<<~TAG` for multi-line strings to strip leading whitespace automatically, keeping code indented cleanly.
- **Mutation:** Remember strings are mutable. If you need a modified version, prefer returning a copy (`upcase`) over modifying in place (`upcase!`) unless necessary for performance.
- **API:** Master the String API. Use `strip`, `chomp` (for file lines), `gsub` (for regex replacement), and `split`.

### 2. Symbols

Symbols (`:name`) are distinct from Strings.

- **Identity:** Use Symbols when "who you are" matters more than "what you contain." Symbols are immutable and unique (same `object_id`).
- **The Rory Test:** If you changed the text content to "Rory" (or another random value), would the program break logic or just display "Rory"?
  - If logic breaks, it's an identifier -> Use **Symbol**.
  - If it just displays "Rory", it's data -> Use **String**.
- **Usage:** Use symbols for hash keys, method names, and internal flags (e.g., `:pending`, `:active`).

### 3. Collections (Arrays & Hashes)

- **Literals:**
  - Use `%w[one two three]` for arrays of strings.
  - Use `%i[one two three]` for arrays of symbols.
  - Use the JSON-style syntax for hashes: `{ name: "Russ", age: 42 }`.
- **Destructuring:** Use parallel assignment to swap variables or extract values.
  - `first, second = list`
- **Iteration:** Never use an index variable (`i=0; while i < arr.size...`) if you can use iteration.
  - Use `each` for side effects.
  - Use `map` to transform.
  - Use `select`/`reject` to filter.
  - Use `reduce` (or `inject`) to accumulate.
  - **Shorthand:** Use `&:method_name` when the block just calls a method on the element.
    - `names.map(&:upcase)` matches `names.map { |n| n.upcase }`.

### 4. Regular Expressions

- Use `match?` for boolean checks (it is faster than `match` or `=~`).
- Use named captures for readability in complex regexes: `/(?<year>\d{4})-(?<month>\d{2})/`.
- Be careful with `^` and `$`; they match start/end of _line_. Use `\A` and `\z` to match start/end of _string_.

---

## IV. Objects, Classes, and Methods

### 1. The "Composed Method" Technique

- **Small Methods:** Break complex logic into tiny, named methods. If a method is longer than 5-10 lines, it is suspect.
- **Single Level of Abstraction:** A method should not mix high-level logic (business rules) with low-level details (array manipulation).
- **One Job:** Each method should do exactly one thing.

### 2. Duck Typing

- **Behavior over Type:** Do not check `is_a?` or `class` unless absolutely necessary. Trust objects to behave like the role they play.
- If an object acts like a Duck (responds to `quack`), treat it like a Duck.
- Use `respond_to?` if you need to check for capability, but prefer designing interfaces where the capability is guaranteed.

### 3. Equality

- `equal?`: Identity (same memory address). Never override this.
- `==`: Value equality. Override this for domain-specific "sameness" (e.g., two Documents are `==` if they have the same ID).
- `eql?` & `hash`: Override these if your object will be used as a **Hash key**. Objects that are `eql?` must return the same `hash`.
- `===`: Case equality. Used primarily in `case` statements (e.g., `Range#===`, `Regexp#===`, `Class#===`).

### 4. Class Data

- **Avoid `@@` (Class Variables):** They wander up and down the inheritance chain and cause bugs. If a subclass changes a `@@var`, it changes it for the parent too.
- **Prefer Class Instance Variables:** Use a single `@` variable inside the class definition scope (or inside `class << self`).
  - ```ruby
      class Document
        @default_font = :arial # Class Instance Variable

        class << self
          attr_accessor :default_font
        end
      end
    ```

  - This keeps data specific to the class (and distinct from subclasses).

### 5. Singleton Methods

- Understand that class methods (`def self.method`) are just singleton methods on the Class object.
- Use singleton methods on instances for unique behavior (like stubs in testing).

---

## V. Modules and Mixins

### 1. Namespaces

- Always wrap libraries or gems in a top-level `Module` to prevent global namespace pollution.
  - `module MyLibrary; class Parser; end; end`

### 2. Mixins

- Use Modules to share behavior (methods) across unrelated classes.
- **Include:** Adds instance methods. `include Enumerable`.
- **Extend:** Adds class methods. `extend Forwardable`.
- **The Hook Pattern:** Use `self.included(base)` to execute code when a module is mixed in. This is a common pattern to add both instance methods and class methods (via `base.extend`) simultaneously.

### 3. Enumerable

- If your class represents a collection, implement the `each` method and `include Enumerable`.
- This grants you `map`, `select`, `count`, `any?`, `all?`, `sort`, and dozens more for free.

---

## VI. Metaprogramming

Ruby allows classes to modify themselves and others. Use this power for clarity, not complexity.

### 1. Method Missing

- **Use for Delegation:** Catch methods you don't know and pass them to an internal object.
- **Use for Flexible APIs:** Like `find_by_name` or `find_by_email` in Rails.
- **Responsibility:** If you override `method_missing`, you **must** also override `respond_to_missing?`.
- **Fallback:** Always call `super` if you can't handle the method name, to raise the standard `NoMethodError`.

### 2. Dynamic Definition

- **`define_method`:** Prefer this over `class_eval "def ..."` whenever possible. It is safer and keeps scope clear.
- Use this to reduce boilerplate when you have many similar methods (e.g., `state_pending`, `state_active`, `state_archived`).

### 3. Hooks

- **`inherited`:** Use this hook to track subclasses (e.g., registering plugins).
- **`at_exit`:** Use sparingly to run cleanup code or trigger test runners.

### 4. Monkey Patching

- You _can_ modify core classes (`String`, `Array`), but do so with extreme caution.
- **Refinements:** Consider using `refine` / `using` to scope monkey patches to a specific file or module, preventing global side effects.

---

## VII. Pattern Matching

(Based on the Second Edition updates)

Ruby 3 introduced powerful Pattern Matching. Use it for complex data extraction.

### 1. Case/In

Use `case ... in` instead of complex `if/elsif` chains when checking structure.

```ruby
result = { status: :ok, data: [10, 20] }

case result
in { status: :ok, data: [x, y] }
  puts "Success: #{x}, #{y}"
in { status: :error, message: msg }
  puts "Error: #{msg}"
else
  puts "Unknown format"
end
```

### 2. Destructuring

- Use **Array Patterns** (`in [a, b, *rest]`) to match sequences.
- Use **Hash Patterns** (`in { name: n, age: a }`) to match attributes.
- **The Pin Operator (`^`):** Use `^variable` to match against an existing variable's value rather than binding a new variable.
  - `in { id: ^target_id }`

### 3. Variable Binding

- Use `_` for values you want to ignore.
- Use variable names to capture values from the pattern automatically.

---

## VIII. Testing

### 1. Philosophy

- Code is not complete without tests.
- Tests serve as documentation.
- Tests should be "Quiet" (only output on failure) and "Independent" (order shouldn't matter).

### 2. Tooling

- **Minitest:** Ruby's built-in, lightweight framework. Great for simple, standard unit tests.
- **RSpec:** The industry standard for Behavior Driven Development (BDD). Focuses on "specs" and "expectations."
  - Use `let` for lazy setup.
  - Use `describe` and `context` to organize scenarios.

### 3. Mocks & Stubs

- Use **Doubles** to isolate the class under test from dependencies.
- Use **Verifying Doubles** (`instance_double`) to ensure your stubs stay in sync with the real API.

---

## IX. Advanced Techniques

### 1. Execute Around

Use blocks to manage resources or side effects (like file handles, database transactions, or logging).

```ruby
def with_logging(description)
  logger.info "Starting #{description}"
  yield
  logger.info "Finished #{description}"
rescue => e
  logger.error "Failed #{description}"
  raise
end

with_logging("calculation") { do_math }
```

### 2. Internal DSLs

Ruby is exceptional for creating Domain Specific Languages.

- Remove syntax noise (parentheses, obvious method calls) to make code read like English.
- Use `instance_eval` with a block to change the context (`self`) to a builder object, allowing users to write declarative code inside the block.

---

## X. Summary Checklist for AI Generation

When generating Ruby code, ask yourself:

1.  **Is it readable?** Would a Rubyist nod in approval or squint in confusion?
2.  **Is it concise?** Are you using `map` instead of a `while` loop? Are you using modifiers for one-liners?
3.  **Is it idiomatic?** Are you using snake_case? Are you avoiding `for` loops? Are you using symbols for identifiers?
4.  **Is it robust?** Are you using `&.` to handle nils? Are you using `fetch` for hash keys that might be missing?
5.  **Is it object-oriented?** Are you creating small classes with focused responsibilities? Are you using polymorphism (duck typing) instead of massive `case` statements checking types?

**Example of Eloquent Ruby:**

_Bad:_

```ruby
# Java style in Ruby
class User
  def set_name(n)
    @name = n
  end

  def get_name()
    return @name
  end

  def is_admin()
    if @role == "admin"
      return true
    else
      return false
    end
  end
end

for i in 0..users.length
  if users[i].is_admin() == true
    puts(users[i].get_name())
  end
end
```

_Eloquent:_

```ruby
# Ruby Style
class User
  attr_accessor :name
  attr_reader :role

  def initialize(name:, role: :user)
    @name = name
    @role = role
  end

  def admin?
    role == :admin
  end
end

users.select(&:admin?).each { |user| puts user.name }
```
