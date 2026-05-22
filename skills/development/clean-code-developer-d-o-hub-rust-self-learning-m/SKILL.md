---
name: clean-code-developer
description: Assist developers in writing clean, maintainable code following software engineering best practices. Use when conducting code reviews, refactoring code, enforcing coding standards, seeking guidance on clean code principles, or integrating automated quality checks into development workflows.
---

# Clean Code Development

Systematic approach to writing clean, maintainable code through software engineering best practices.

## Purpose

Apply SOLID principles, eliminate code duplication, maintain simplicity, and write code that reads like well-written prose.

## When to Use

Use this skill when:
- **Code Reviews**: Reviewing code for adherence to clean code principles
- **Refactoring**: Improving existing code structure and maintainability
- **Coding Standards**: Enforcing consistent coding practices and conventions
- **Clean Code Guidance**: Seeking advice on clean code principles and patterns
- **Quality Checks**: Integrating automated quality checks into workflows

## Core Principles

### SOLID Principles

#### Single Responsibility Principle
- Each function/module has one reason to change
- Clear, focused purpose
- Easy to test and maintain

#### Open-Closed Principle
- Open for extension, closed for modification
- Use interfaces/traits for abstraction
- New behavior through composition, not modification

#### Liskov Substitution Principle
- Subtypes must be substitutable for base types
- Derived classes should enhance functionality
- Don't break expected behavior

#### Interface Segregation Principle
- Clients shouldn't depend on interfaces they don't use
- Small, focused interfaces
- Prefer composition over large interfaces

#### Dependency Inversion Principle
- Depend on abstractions, not concretions
- High-level modules shouldn't depend on low-level modules
- Use dependency injection

### Other Key Principles

#### DRY (Don't Repeat Yourself)
- Extract common code into reusable functions/modules
- Avoid duplication through abstraction
- One source of truth for each piece of logic

#### KISS (Keep It Simple, Stupid)
- Simple solutions over complex ones
- Avoid over-engineering
- Clear, straightforward code

#### YAGNI (You Aren't Gonna Need It)
- Don't build for hypothetical future requirements
- Implement what's needed now
- Defer complexity until necessary

#### Boy Scout Rule
- Leave code better than you found it
- Small improvements add up
- Prevent technical debt accumulation

## Code Quality Assessment

### Readability
- Self-documenting code
- Clear, descriptive names
- Logical flow
- Appropriate comments

### Maintainability
- Easy to understand
- Easy to modify
- Easy to test
- Clear structure

### Testability
- Dependencies easily mocked
- Pure functions where possible
- Clear inputs and outputs
- Testable in isolation

### Extensibility
- Open for extension
- Closed for modification
- Plugin points where appropriate
- Flexible design

## Refactoring Techniques

### Extract Method/Function
- Replace duplicated code with method call
- Name methods by what they do
- Keep methods small and focused

### Extract Class/Module
- Group related functionality
- Create coherent abstractions
- Separate concerns

### Replace Conditional with Polymorphism
- Use strategy pattern for conditionals
- Eliminate type checking
- Improve extensibility

### Introduce Parameter Object
- Reduce parameter count
- Group related parameters
- Improve method signatures

### Decompose Conditional
- Simplify complex conditions
- Extract boolean expressions
- Improve readability

## Anti-Patterns to Avoid

### Code Smells
- **Long Method**: Break into smaller methods
- **Long Parameter List**: Use parameter objects
- **Duplicate Code**: Extract to reusable functions
- **Large Class**: Split into smaller classes
- **God Class**: Reduce responsibilities
- **Feature Envy**: Move methods to appropriate classes
- **Data Clumps**: Group related data
- **Primitive Obsession**: Use value objects
- **Switch Statements**: Use polymorphism/strategy pattern
- **Temporary Field**: Eliminate through parameter passing
- **Refused Bequest**: Pass parameters explicitly

### Rust-Specific Issues
- **Excessive Clone**: Use borrowing or Arc
- **Unnecessary Unwrap**: Use proper error handling with `?`
- **Deep Nesting**: Extract methods to flatten
- **Large Functions**: Split into smaller, focused functions (< 50 LOC)
- **Unsafe Code**: Only when necessary, well-documented
- **Memory Leaks**: Proper ownership and borrowing
- **Deadlocks**: Release locks before `.await`

## Integration with Development Workflows

### Pre-Commit Hooks
- Run formatting (rustfmt)
- Run linting (clippy)
- Run basic tests
- Check for common anti-patterns

### CI/CD Integration
- Automated formatting checks
- Linting with warnings as errors
- Test coverage requirements
- Code quality metrics

### Code Review Checklist
- [ ] Follows SOLID principles
- [ ] No code duplication
- [ ] Appropriate naming conventions
- [ ] Proper error handling
- [ ] Comprehensive tests
- [ ] Clear documentation

## Best Practices

### DO:
✓ Apply SOLID principles consistently
✓ Extract common code into reusable functions
✓ Keep functions small and focused (< 50 LOC)
✓ Use descriptive names that reveal intent
✓ Write tests before refactoring (TDD)
✓ Document complex business logic, not obvious code
✓ Use static analysis tools (clippy, SonarQube)
✓ Leave code better than you found it
✓ Prefer composition over inheritance
✓ Keep dependencies minimal and explicit

### DON'T:
✗ Violate SOLID principles
✗ Duplicate code "for now" - fix immediately
✗ Write functions longer than 50 lines without strong justification
✗ Use abbreviations or unclear names
✗ Refactor without adequate test coverage
✗ Over-document obvious code
✗ Skip static analysis warnings
✗ Over-engineer simple problems
✗ Create tight coupling between modules

## Metrics

Track these metrics to assess code quality:
- **Cyclomatic Complexity**: Average < 10 per function
- **Lines of Code**: < 500 per file (project standard)
- **Function Length**: < 50 lines average
- **Test Coverage**: > 90% line coverage
- **Code Duplication**: < 5%
- **Technical Debt Ratio**: Trend downward over time

## Examples

### Example 1: Extract Method
```rust
// BEFORE - Code smell: duplicate logic
fn process_data_a(data: &Data) -> Result<Output> {
    // Validation
    if data.id.is_empty() {
        return Err(anyhow!("ID is required"));
    }
    if data.value < 0 {
        return Err(anyhow!("Value must be positive"));
    }
    // Processing
    let result = calculate(data);
    Ok(result)
}

fn process_data_b(data: &Data) -> Result<Output> {
    // Same validation code duplicated
    if data.id.is_empty() {
        return Err(anyhow!("ID is required"));
    }
    if data.value < 0 {
        return Err(anyhow!("Value must be positive"));
    }
    // Processing
    let result = calculate(data);
    Ok(result)
}
```

```rust
// AFTER - Applied DRY principle
fn validate_data(data: &Data) -> Result<()> {
    if data.id.is_empty() {
        return Err(anyhow!("ID is required"));
    }
    if data.value < 0 {
        return Err(anyhow!("Value must be positive"));
    }
    Ok(())
}

fn process_data_a(data: &Data) -> Result<Output> {
    validate_data(data)?;
    let result = calculate(data);
    Ok(result)
}

fn process_data_b(data: &Data) -> Result<Output> {
    validate_data(data)?;
    let result = calculate(data);
    Ok(result)
}
```

### Example 2: Single Responsibility Principle
```rust
// BEFORE - Single function doing too much
pub fn handle_user_request(data: UserData) -> Result<UserResult> {
    // Validate
    validate_user(&data)?;
    // Store in database
    db::save_user(&data)?;
    // Send email
    email::send_welcome(&data.email)?;
    // Calculate recommendations
    let recs = calculate_recommendations(&data)?;
    Ok(UserResult {
        saved: true,
        recommendations: recs,
    })
}
```

```rust
// AFTER - Split responsibilities
pub struct UserHandler {
    db: Arc<Database>,
    email: Arc<EmailService>,
    recommender: Arc<RecommenderService>,
}

impl UserHandler {
    pub async fn handle_user_request(&self, data: UserData) -> Result<UserResult> {
        // Each function has single responsibility
        self.validate_user(&data)?;
        self.save_user(&data).await?;
        self.send_welcome_email(&data.email).await?;
        let recs = self.get_recommendations(&data).await?;

        Ok(UserResult {
            saved: true,
            recommendations: recs,
        })
    }

    fn validate_user(&self, data: &UserData) -> Result<()> {
        // Validation logic
        Ok(())
    }

    async fn save_user(&self, data: &UserData) -> Result<()> {
        self.db.save_user(data).await
    }

    async fn send_welcome_email(&self, email: &str) -> Result<()> {
        self.email.send_welcome(email).await
    }

    async fn get_recommendations(&self, data: &UserData) -> Result<Vec<Recommendation>> {
        self.recommender.calculate(data).await
    }
}
```

## Integration with Skills

Complements:
- **rust-code-quality**: For Rust-specific quality checks
- **code-reviewer**: For comprehensive code review workflows
- **test-runner**: For testing refactored code

Invokes:
- **quality-unit-testing**: For testing best practices

## Tools and Commands

### Static Analysis
```bash
# Clippy - Rust linter
cargo clippy --all-targets -- -D warnings

# Check for specific issues
cargo clippy -- -W clippy::too_many_arguments
cargo clippy -- -W clippy::unwrap_used
```

### Complexity Analysis
```bash
# Install complexity tool
cargo install cargo-complexity

# Analyze complexity
cargo complexity
```

### Duplication Detection
```bash
# Use tools like jscpd, SonarQube, or custom scripts
# Find duplicated code blocks
```

## Quality Gates

Ensure code passes these quality gates:
- **Formatting**: 100% rustfmt compliant
- **Linting**: Zero clippy warnings
- **Complexity**: Cyclomatic complexity < 10 per function
- **Test Coverage**: > 90% line coverage
- **Duplication**: < 5% duplicate code
- **Documentation**: All public APIs documented

## Continuous Improvement

### Weekly Reviews
- Review code quality metrics
- Identify trends and issues
- Update coding standards if needed
- Refactor technical debt

### Retrospectives
- Analyze what worked well
- Identify common issues
- Improve guidelines
- Share learnings with team

## Summary

Clean code development produces software that is:
- **Readable**: Easy to understand by others
- **Maintainable**: Easy to modify and extend
- **Testable**: Easy to write tests for
- **Efficient**: Minimal technical debt
- **Reliable**: Fewer bugs and issues

Apply these principles systematically to write code that stands the test of time.
