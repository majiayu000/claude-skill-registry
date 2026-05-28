---
name: routine-parameter-design
description: Design and optimize function/method parameter lists when defining or refactoring API interfaces, method signatures, or function parameters. Apply best practices for parameter count, ordering, pass mechanisms, and documentation to create clear, efficient, and maintainable interfaces.
---

# Routine Parameter Design

Use this skill when defining new functions, refactoring existing method signatures, or designing API interfaces to ensure proper parameter design.

## When to Use

- Defining or refactoring a function's parameter list
- Designing API interfaces or method signatures
- Reviewing code for parameter-related issues
- Optimizing function interfaces for clarity and maintainability

## Core Design Principles

### 1. Limit Parameter Count

- Minimize the number of parameters to improve readability and usability
- Consider using parameter objects or structs when parameters exceed 3-5 items
- Each parameter should serve a distinct, necessary purpose

### 2. Order Parameters (Input-Modify-Output)

Arrange parameters in this specific sequence:

1. **Input parameters**: Data the routine reads but does not modify
2. **Modify parameters**: Data the routine both reads and modifies
3. **Output parameters**: Data the routine writes but does not read

### 3. Choose Appropriate Pass Mechanisms

- **Pass by value**: For primitive types and small objects that won't be modified
- **Pass by reference**: For objects that need modification or to avoid copying overhead
- **Objects**: Typically passed as object references (not individual fields)
- **Pointers**: Follow the asterisk rule (use `*` consistently for pointer parameters)

### 4. Ensure Interface Consistency

- Match actual parameters with formal parameter types
- Follow language-specific conventions (e.g., C library ordering when applicable)
- Maintain consistent ordering across related functions
- Use similar parameter names for similar purposes across the codebase

### 5. Apply Modifiers Appropriately

- Use `const` prefix to prevent modification of input parameters
- Use `in` keyword to explicitly mark input-only parameters
- Use `out` keyword to explicitly mark output-only parameters
- Consider `inout` or equivalent for parameters that are both read and modified

### 6. Document and Name Clearly

- Use descriptive, self-documenting parameter names
- Write clear comments explaining parameter purpose and constraints
- Document expected ranges, valid values, and edge cases
- Include units of measurement when applicable

### 7. Validate Parameter Usage

- Ensure the routine uses all passed parameters
- Remove unused parameters to avoid confusion
- If a parameter is temporarily unused, document why and when it will be used

### 8. Avoid Global Variables

- Never use global variables as substitutes for parameters
- Pass all required data explicitly through the parameter list
- Global variables make code harder to test, understand, and maintain

## Language-Specific Considerations

- **C/C++**: Pay attention to pointer vs reference semantics, const correctness
- **Java**: All objects are passed by reference; primitives by value
- **Visual Basic**: Use `ByVal` and `ByRef` keywords explicitly
- Always check language-specific syntax limitations and conventions

## Review Checklist

- [ ] Parameter count is minimized and reasonable
- [ ] Parameters follow input-modify-output ordering
- [ ] Pass mechanism is appropriate for each parameter
- [ ] Modifiers (const, in, out) are used correctly
- [ ] All parameters have clear names and documentation
- [ ] All parameters are actually used by the routine
- [ ] No global variables are used as parameter substitutes
- [ ] Interface is consistent with related functions