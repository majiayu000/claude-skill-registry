---
name: ruby
description: Ruby development, RubyGems, Rails, clean code practices, and idiomatic Ruby
category: Languages
---

# Skill: ruby

## What I do

I provide Ruby-specific expertise: idiomatic patterns, Rails conventions, gem ecosystem knowledge, and best practices for writing clean, maintainable Ruby code.

## When to use me

- Writing Ruby code (any context)
- Designing Ruby APIs or designing DSLs
- Working with Rails applications
- Choosing and integrating gems
- Refactoring Ruby for clarity and performance

## Core principles

1. **Convention over configuration** - Follow Rails conventions, don't override them
2. **DRY (Don't Repeat Yourself)** - Extract logic to methods, concerns, and services
3. **Ruby is for humans** - Readable, expressive code beats clever code
4. **Blocks and iterators** - Core Ruby strength, use them idiomatically
5. **Frozen strings** - Use `frozen_string_literal: true` at file top

## Patterns & examples

**Idiomatic iteration:**
```ruby
# ✅ Correct: use each, map, select with blocks
[1, 2, 3].each { |n| puts n }
numbers.map { |n| n * 2 }
items.select { |i| i.valid? }

# ❌ Wrong: C-style for loops
for i in 0..items.length-1
  puts items[i]
end
```

**Rails service pattern:**
```ruby
# ✅ Correct: Extract business logic to service
class CreateOrderService
  def initialize(user, items)
    @user = user
    @items = items
  end
  
  def call
    Order.create(user: @user, items: @items)
  end
end

# In controller:
order = CreateOrderService.new(@user, params[:items]).call
```

**Frozen string literals:**
```ruby
# ✅ Correct: frozen string at file top
# frozen_string_literal: true

class User
  ROLE = 'admin'  # frozen by default now
end

# ❌ Wrong: mutable strings in constants
ROLE = 'admin'.dup  # wasteful, implies mutation
```

## Anti-patterns to avoid

- ❌ Monolithic controller actions (extract to services)
- ❌ Complex view logic (move to helpers or view components)
- ❌ Ignoring n+1 queries (use `includes`, `eager_load`)
- ❌ Exception handling as control flow (use `dig`, `try`, explicit checks)
- ❌ Mutable defaults in arguments (`def foo(items=[])`—use `nil` and initialize in body)

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Languages/Ruby.md`

## Related skills

- `clean-code` - SOLID principles in Ruby
- `bdd-workflow` - Test-driven development workflow
- `rspec-testing` - RSpec BDD testing framework
- `design-patterns` - Common patterns in Ruby
