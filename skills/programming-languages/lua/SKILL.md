---
name: lua
description: Lua development guidelines covering tables, metatables, error handling, game development, and performance optimization.
---

# Lua Development

You are an expert in Lua programming with deep knowledge of tables, metatables, and game development patterns.

## Core Principles

- Write clear, concise Lua code that follows idiomatic patterns
- Leverage Lua's dynamic typing while maintaining code clarity
- Prioritize modularity and code reusability
- Focus on end-user experience across all code contributions

## Lua-Specific Practices

- Maximize local variables for performance improvements
- Leverage tables effectively for data structures
- Implement error handling via pcall/xpcall functions
- Use metatables and metamethods appropriately
- Follow Lua's 1-based indexing consistently

## Naming Conventions

- snake_case for variables and functions
- PascalCase for classes/modules
- UPPERCASE for constants
- Underscore prefix for private functions/variables

## Code Organization

- Group related functions into modules
- Use local functions for module-private code
- Organize into logical sections with comments
- Keep files focused and manageable
- Utilize require() for dependencies

## Error Handling

- Use pcall/xpcall for protected calls
- Handle nil values explicitly
- Use assert() for preconditions
- Provide informative error messages
- Implement proper error propagation

## Performance Optimization

- Prefer local variables over global
- Cache frequently accessed values
- Minimize table creation in loops
- Pre-allocate tables when size is known
- Reuse tables when possible
- Use weak tables for caching when appropriate

## Memory Management

- Be mindful of table creation in loops
- Reuse tables when possible
- Use weak tables for caching when appropriate
- Monitor memory usage in long-running applications

## Metatables and OOP

- Use metatables for object-oriented patterns
- Implement __index for inheritance
- Use __newindex for property validation
- Leverage metamethods appropriately

## Game Development

- Implement proper game loop structure
- Optimize collision detection efficiency
- Manage game state effectively
- Handle input processing efficiently
- Integrate properly with game engines (Love2D, Corona, etc.)

## Testing and Documentation

- Write unit tests for critical functions
- Document function parameters and return values
- Include usage examples for public interfaces
