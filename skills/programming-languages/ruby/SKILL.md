---
name: ruby
description: Ruby development guidelines covering idiomatic code style, Ruby 3.x features, testing with RSpec, and best practices for building maintainable Ruby applications.
---

# Ruby Development

You are an expert in Ruby development, including Ruby 3.x features, testing frameworks, and modern Ruby best practices.

## Code Style and Structure

- Write concise, idiomatic Ruby code with accurate examples
- Adhere to Ruby community conventions and style guides
- Use snake_case for files, methods, and variables
- Use CamelCase for classes and modules
- Favor descriptive names like `user_signed_in?` and `calculate_total`

## Ruby Language Features

- Leverage Ruby 3.x capabilities including:
  - Pattern matching with `case/in`
  - Endless methods for simple one-liners
  - Keyword arguments for clarity
  - Safe navigation operator (`&.`)
- Use blocks, procs, and lambdas effectively
- Apply metaprogramming judiciously

## Syntax and Formatting

- Follow the Ruby Style Guide
- Employ expressive syntax features
- Prefer single quotes except when string interpolation is needed
- Use meaningful method and variable names
- Keep methods small and focused (Single Responsibility Principle)

## Error Handling

- Apply exceptions for genuine edge cases only
- Implement proper logging with user-friendly messages
- Use custom exception classes for domain-specific errors
- Handle errors gracefully with appropriate rescue blocks

## Object-Oriented Design

- Follow SOLID principles
- Favor composition over inheritance
- Use modules for shared behavior (mixins)
- Keep classes focused and cohesive

## Testing Best Practices

### RSpec Guidelines

- Write comprehensive coverage of typical cases, edge cases, and error conditions
- Use clear, descriptive naming conventions for test blocks
- Organize logically with `describe` for classes/methods and `context` for scenarios
- Use `let` and factories (FactoryBot) instead of fixtures
- Ensure test independence with minimal shared state
- Mock external services strategically while testing real behavior when possible

### Test Structure

```ruby
describe ClassName do
  describe '#method_name' do
    context 'when condition exists' do
      it 'does expected behavior' do
        expect(result).to eq(expected)
      end
    end
  end
end
```

## Performance Optimization

- Profile code before optimizing
- Use appropriate data structures
- Leverage lazy enumerators for large collections
- Cache expensive computations

## Security

- Sanitize user input
- Use parameterized queries
- Keep dependencies updated
- Follow security best practices for handling sensitive data
