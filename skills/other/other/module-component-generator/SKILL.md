---
name: module-component-generator
description: Generates complete modules and components from interface contracts and specifications. Use when Claude needs to build larger software components, implement interfaces, create service layers, or generate complete modules with multiple related classes. Supports Python (with type hints and protocols) and Java (with interfaces and abstract classes). Trigger when users request "implement this interface", "generate a module for", "create a service layer", "build a component that implements", or provide interface definitions that need implementation.
---

# Module/Component Generator

Generate complete, production-ready modules and components from interface contracts and specifications.

## Quick Start

When a user provides an interface contract or requests a module:

1. **Understand the contract**: Analyze the interface, abstract class, or specification
2. **Determine scope**: Clarify if generating single implementation or full module
3. **Select patterns**: Choose appropriate design patterns and structure
4. **Generate code**: Create implementation with proper structure and documentation
5. **Add documentation**: Include comprehensive docstrings and usage examples

## What This Skill Generates

### Interface Implementations
Generate concrete implementations from:
- Python Protocols and Abstract Base Classes
- Java interfaces and abstract classes
- Complete with validation, error handling, and documentation

### Complete Modules
Generate multi-file modules with:
- Domain models
- Repository/data access layer
- Service/business logic layer
- Custom exceptions
- Comprehensive documentation

### Documentation
Generate for all code:
- Module-level documentation
- Class and method docstrings
- Usage examples
- API reference documentation

## Generation Scope

### Single Interface Implementation

**When to use:**
- User provides a single interface/protocol/abstract class
- Need one concrete implementation
- Simple, focused functionality

**What to generate:**
- Implementation class with all required methods
- Input validation
- Error handling
- Docstrings with examples
- Basic usage example

### Full Module Generation

**When to use:**
- Building a complete feature or service
- Need multiple related classes
- Require layered architecture (model, repository, service)

**What to generate:**
- Domain models with validation
- Repository layer for data access
- Service layer for business logic
- Custom exception hierarchy
- Module-level documentation
- Complete usage examples

## Language-Specific Guidance

### Python

**Patterns and conventions:**
- Use type hints for all parameters and returns
- Use `Protocol` for structural typing
- Use `ABC` for inheritance-based contracts
- Follow PEP 8 style guidelines
- Use dataclasses or Pydantic for models

**See:** [python-patterns.md](references/python-patterns.md) for detailed examples

**Common structures:**
- Protocol implementation
- ABC implementation
- Service layer module (model + repository + service)
- Adapter pattern module
- Factory pattern module

### Java

**Patterns and conventions:**
- Implement interfaces explicitly
- Use `Objects.requireNonNull()` for validation
- Use `Optional<T>` for nullable returns
- Follow Java naming conventions
- Use proper exception hierarchy

**See:** [java-patterns.md](references/java-patterns.md) for detailed examples

**Common structures:**
- Interface implementation
- Abstract class extension
- Service layer module (model + repository + service)
- Strategy pattern module
- Builder pattern module

## Workflow

### 1. Analyze the Contract

**For interfaces/protocols:**
- Identify all methods that need implementation
- Note parameter types and return types
- Check for any constraints or requirements
- Understand the intended behavior

**For module requests:**
- Identify core entities/models
- Determine required operations (CRUD, business logic)
- Understand relationships between components
- Clarify persistence requirements

### 2. Determine Structure

**Single implementation:**
- One class implementing the interface
- Helper methods if needed
- Validation and error handling

**Full module:**
- Domain models (data structures)
- Repository layer (data access)
- Service layer (business logic)
- Exception classes (error handling)
- Module initialization

### 3. Generate Implementation

**For each class:**
1. Write class declaration with proper inheritance
2. Implement constructor with dependency injection
3. Implement all required methods
4. Add validation and error handling
5. Add helper methods if needed
6. Write comprehensive docstrings

**Code quality standards:**
- Validate all inputs
- Handle edge cases
- Use meaningful variable names
- Follow language conventions
- Keep methods focused and small

### 4. Add Documentation

**Module level:**
- Overview of module purpose
- List of main classes
- Usage examples
- See [documentation-patterns.md](references/documentation-patterns.md)

**Class level:**
- Purpose and responsibility
- Constructor parameters
- Key methods overview
- Usage examples

**Method level:**
- What the method does
- Parameters and types
- Return value and type
- Exceptions that can be raised
- Usage example for complex methods

### 5. Provide Usage Examples

**Include:**
- Basic usage example
- Common use cases
- Error handling examples
- Integration examples for modules

## Design Patterns

### Repository Pattern
Separate data access from business logic.

**Structure:**
- Model: Domain entity
- Repository: Data access interface and implementation
- Service: Business logic using repository

**Use when:** Need to abstract data persistence

### Service Layer Pattern
Encapsulate business logic in service classes.

**Structure:**
- Models: Domain entities
- Services: Business operations
- Exceptions: Domain-specific errors

**Use when:** Building business logic layer

### Adapter Pattern
Provide unified interface to different implementations.

**Structure:**
- Interface: Common contract
- Adapters: Implementation for each variant
- Factory: Create appropriate adapter

**Use when:** Need to support multiple backends/providers

### Strategy Pattern
Encapsulate algorithms/behaviors as interchangeable strategies.

**Structure:**
- Strategy interface: Common contract
- Concrete strategies: Different implementations
- Context: Uses strategy

**Use when:** Need runtime algorithm selection

## Best Practices

### Code Quality

**Validation:**
- Validate all inputs at public API boundaries
- Use type hints/annotations
- Fail fast with clear error messages
- Check for null/None values

**Error Handling:**
- Create custom exception hierarchy
- Use specific exception types
- Provide meaningful error messages
- Document exceptions in docstrings

**Dependency Injection:**
- Accept dependencies through constructor
- Use interfaces/protocols for dependencies
- Make dependencies explicit
- Facilitate testing with mocks

### Documentation

**Completeness:**
- Document all public classes and methods
- Include parameter descriptions
- Document return values
- List possible exceptions

**Examples:**
- Provide usage examples in docstrings
- Show common use cases
- Include error handling examples
- Demonstrate integration patterns

**Clarity:**
- Use clear, concise language
- Explain the "why" not just the "what"
- Include type information
- Cross-reference related components

### Structure

**Organization:**
- Group related classes in modules/packages
- Separate concerns (model, repository, service)
- Use clear naming conventions
- Keep files focused and cohesive

**Modularity:**
- Keep classes focused on single responsibility
- Use composition over inheritance
- Minimize coupling between components
- Design for testability

## Example Usage Patterns

**User:** "Implement this DataRepository interface"
→ Generate single implementation class with all methods

**User:** "Create a user service module with CRUD operations"
→ Generate full module: User model, UserRepository, UserService, exceptions

**User:** "Build a notification system that supports email and SMS"
→ Generate adapter pattern: NotificationAdapter interface, EmailAdapter, SMSAdapter, factory

**User:** "Implement this PaymentProcessor abstract class for Stripe"
→ Generate StripePaymentProcessor extending abstract class

**User:** "Generate a complete order management module"
→ Generate full module: Order model, OrderRepository, OrderService, custom exceptions, documentation

**User:** "Create implementations for these three interfaces"
→ Generate three implementation classes, each with proper structure

## Quality Checklist

Before delivering generated code, verify:

- [ ] All interface methods implemented
- [ ] Input validation present
- [ ] Error handling included
- [ ] Type hints/annotations added
- [ ] Docstrings complete
- [ ] Usage examples provided
- [ ] Follows language conventions
- [ ] Dependencies properly injected
- [ ] Custom exceptions defined
- [ ] Module documentation included
