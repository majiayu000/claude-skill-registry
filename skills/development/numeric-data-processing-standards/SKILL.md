---
name: numeric-data-processing-standards
description: Provides comprehensive guidelines for handling numeric data in code, including data type selection, magic number avoidance, type conversions, and boundary checks. Use this skill when writing or reviewing code that involves numeric variables, constants, calculations, or comparisons to prevent type errors, overflow, and runtime exceptions.
---

# Numeric Data Processing Standards

## When to Use
Apply this skill when:
- Defining numeric variables or constants
- Performing numeric calculations or operations
- Comparing numeric values
- Converting between data types
- Reviewing code for potential numeric-related defects

## Core Procedures

### 1. Data Type Selection and Declaration
- Choose appropriate data type based on requirements (BCD, floating-point, integer)
- Review compiler warnings related to data types
- Add explanatory comments when declaring variables
- Define portable data types for cross-platform compatibility

### 2. Literals and Magic Number Handling
- Replace literal numbers with named constants
- Avoid hardcoded 0 and 1 except when semantically appropriate
- Eliminate "magic numbers" by using descriptive constant names

### 3. Numeric Operations and Conversions
- Handle numeric type conversions explicitly
- Avoid comparisons between mixed types
- Prevent operations on numbers with vastly different magnitudes
- Consider computational cost of common operations

### 4. Error Prevention and Boundary Checks
- Implement integer overflow protection
- Validate integer ranges before operations
- Prevent division by zero errors
- Apply boundary analysis to avoid off-by-one errors

## Key Considerations

- **Type Safety**: Always verify type compatibility before operations
- **Precision**: Be aware of floating-point precision limitations
- **Portability**: Use type definitions that work across platforms
- **Performance**: Balance safety with computational efficiency
- **Readability**: Named constants improve code maintainability

## Common Pitfalls to Avoid

- Implicit type conversions that lose precision
- Comparing floating-point numbers for exact equality
- Assuming integer overflow behavior across compilers
- Using magic numbers without documentation
- Ignoring compiler warnings about type mismatches