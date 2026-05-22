---
name: generating-rbs-inline
description: Generates RBS-inline type annotations directly in Ruby source files as comments. Triggers when adding inline type signatures, annotating Ruby methods with rbs-inline syntax, or generating type comments without existing inline annotations.
---

# RBS-Inline Generation Skill

Generate RBS-inline type annotations as comments directly in Ruby source files. Unlike pure RBS which uses separate `.rbs` files, rbs-inline embeds type information as structured comments within Ruby code.

# Instructions

When generating RBS-inline annotations, always follow these steps.

Copy this checklist and track your progress:

```
RBS-Inline Generation Progress:
- [ ] Step 1: Analyze the Ruby source
- [ ] Step 2: Add RBS-inline annotations
- [ ] Step 3: Eliminate `untyped` types in annotations
- [ ] Step 4: Review and refine annotations
- [ ] Step 5: Validate annotations
- [ ] Step 6: Ensure type safety (only if steep is configured)
```

## Rules

- You MUST NOT run Ruby code of the project.
- You MUST NOT use `untyped`. Infer the proper type instead.
- You MUST ask the user to provide more details if something is not clear.
- You MUST prepend any command with `bundle exec` if the project has Gemfile.
- You MUST use `# @rbs` comment syntax for inline annotations.
- You MUST NOT use regular RBS signatures and `.rbs` files in the project.

## 1. Analyze the Ruby Source

Always perform this step.

Read and understand the Ruby source file:
- Identify all classes, modules, methods, constants and instance variables.
- Note inheritance, module inclusion and definitions based on metaprogramming.
- Note visibility modifiers - `public`, `private`, `protected`.
- Note type parameters for generic classes.

## 2. Add RBS-Inline Annotations

Always perform this step.

1. First, add the magic comment at the top of the Ruby file to enable rbs-inline processing:
    ```ruby
    # rbs_inline: enabled
    ```

2. Then add type annotations as comments directly in the Ruby source file using rbs-inline syntax:

**Example - Before:**
```ruby
class User
  attr_reader :name, :age

  def initialize(name, age)
    @name = name
    @age = age
  end

  def greet(greeting)
    "#{greeting}, #{@name}!"
  end
end
```

**Example - After:**
```ruby
# rbs_inline: enabled

class User
  attr_reader :name #: String
  attr_reader :age #: Integer

  # @rbs name: String
  # @rbs age: Integer
  # @rbs return: void
  def initialize(name, age)
    @name = name
    @age = age
  end

  #: (String) -> String
  def greet(greeting)
    "#{greeting}, #{@name}!"
  end
end
```

- Follow RBS-inline syntax conventions strictly
  - See [syntax.md](reference/syntax.md) for the full RBS-inline syntax guide
- Pay extra attention to `Data` and `Struct` types
  - See [data-struct-support.md](reference/data-struct-support.md) for Data and Struct handling

## 3. Eliminate `untyped` Types in Annotations

Always perform this step.

- Review all annotations and replace `untyped` with proper types.
- Use code context, method calls, and tests to infer types.
- Use `untyped` only as a last resort when type cannot be determined.

## 4. Review and Refine Annotations

Always perform this step.

- Verify annotations are correct, coherent, and complete.
- Remove unnecessary `untyped` types.
- Fix any errors and repeat until annotations are correct.

## 5. Validate Annotations

Always perform this step.

rbs-inline is a transpiler - it generates RBS files from inline annotations. Validation happens on the generated RBS output.

1. Generate RBS files from annotations:
   ```bash
   rbs-inline --output lib
   ```
   This generates `.rbs` files in `sig/generated/` directory.

2. Validate the generated RBS files:
   ```bash
   rbs validate
   ```
   This checks syntax, name resolution, inheritance, and type applications.

3. Fix any errors in your inline annotations and repeat until validation passes.

## 6. Ensure Type Safety

Perform this step ONLY if the project Gemfile includes `steep` gem AND the project has Steepfile.

Steep works on RBS files, not directly on inline annotations. The RBS files must be generated first (step 5).

1. Ensure RBS files are generated from annotations:
   ```bash
   rbs-inline --output lib
   ```

2. Run Steep type checker:
   ```bash
   steep check
   ```

3. Fix any errors reported by `steep check`.
   - Do not modify Steepfile to fix errors.
   - Fix the inline annotations in Ruby source files.
   - Regenerate RBS files and repeat until no errors.

# References

- [syntax.md](reference/syntax.md) - RBS-inline syntax guide
- [data-struct-support.md](reference/data-struct-support.md) - Data and Struct handling in rbs-inline
- [examples/](reference/rbs_inline_examples/STRUCTURE.md) - Real-world rbs-inline examples from production gems
- [rbs-inline repository](https://github.com/soutaro/rbs-inline) - Official rbs-inline gem