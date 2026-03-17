---
name: clean-abap
description: Check ABAP code for compliance with Clean ABAP principles. Use this skill when users ask to check, validate, review, or analyze ABAP code for clean code compliance, code quality, best practices, or adherence to Clean ABAP guidelines. Triggers include requests like "check this ABAP code", "is this clean ABAP", "review my ABAP for clean code", "validate ABAP against clean code principles", or "analyze ABAP code quality".
---

# Clean ABAP

This skill provides comprehensive checking of ABAP code against Clean ABAP principles, based on the Clean ABAP style guide which adapts Robert C. Martin's Clean Code for ABAP.

## How to Use This Skill

When checking ABAP code for Clean ABAP compliance:

1. **Read the code** provided by the user
2. **Categorize issues** by Clean ABAP sections (Names, Language, Constants, Variables, Tables, Strings, Booleans, Conditions, Ifs, Classes, Methods, Error Handling, Comments, Formatting, Testing)
3. **Identify violations** with specific line references when available
4. **Provide actionable recommendations** with code examples showing both the problem and the clean solution
5. **Prioritize issues** by impact (critical, major, minor)

## Check Categories

### 1. Names

**Key Principles:**
- Use descriptive names that convey content and meaning
- Prefer solution domain and problem domain terms
- Use pronounceable names
- Use snake_case consistently
- Avoid abbreviations unless necessary
- Use nouns for classes, verbs for methods
- Avoid noise words like "data", "info", "object"
- Pick one word per concept
- Avoid encodings (Hungarian notation, prefixes like iv_, rv_, lt_)
- Avoid obscuring built-in functions

**Check for:**
- Non-descriptive variable/method/class names (e.g., `data1`, `temp`, `x`)
- Inconsistent abbreviations across the code
- Mixed naming conventions (not snake_case)
- Noise words in names
- Hungarian notation or unnecessary prefixes (iv_, ev_, rv_, lt_, ls_)
- Method names that obscure ABAP built-in functions

### 2. Language

**Key Principles:**
- Prefer object orientation to procedural programming
- Prefer functional to procedural language constructs
- Avoid obsolete language elements
- Use design patterns wisely

**Check for:**
- Use of obsolete statements (unescaped host variables in SELECT, etc.)
- Procedural code that should be object-oriented
- Use of old-style MOVE instead of assignment
- TRANSLATE instead of to_upper()/to_lower()
- CREATE OBJECT instead of NEW
- Old-style READ TABLE instead of table expressions

### 3. Constants

**Key Principles:**
- Use constants instead of magic numbers
- Constants need descriptive names
- Prefer ENUM to constants interfaces
- Group related constants

**Check for:**
- Magic numbers or string literals in code
- Constants with non-descriptive names (c_01, c_x, etc.)
- Ungrouped constants that should be in BEGIN OF/END OF blocks

### 4. Variables

**Key Principles:**
- Prefer inline to up-front declarations
- Don't use variables outside their declaration block
- Don't chain up-front declarations
- Don't use field symbols for dynamic data access (modern ABAP)
- Choose the right loop targets (field symbols vs references vs values)

**Check for:**
- Up-front DATA declarations when inline would be clearer
- Variables used outside their declaration block scope
- Chained DATA declarations
- Unnecessary field symbols with ASSIGN

### 5. Tables

**Key Principles:**
- Use the right table type (STANDARD, SORTED, HASHED)
- Avoid DEFAULT KEY
- Prefer INSERT INTO TABLE to APPEND TO
- Prefer LINE_EXISTS to READ TABLE or LOOP AT
- Prefer READ TABLE to LOOP AT
- Prefer LOOP AT WHERE to nested IF
- Avoid unnecessary table reads

**Check for:**
- Tables with DEFAULT KEY
- APPEND TO when INSERT INTO TABLE is more appropriate
- READ TABLE ... TRANSPORTING NO FIELDS when LINE_EXISTS would be clearer
- LOOP AT ... EXIT when READ TABLE is intended
- Nested IF inside LOOP AT when WHERE clause would work
- Double reads (checking existence then reading again)

### 6. Strings

**Key Principles:**
- Use ` (backticks) to define string literals
- Use | (pipes) to assemble text

**Check for:**
- Single quotes for string literals
- String concatenation with && instead of string templates

### 7. Booleans

**Key Principles:**
- Use ABAP_BOOL for boolean types
- Use ABAP_TRUE and ABAP_FALSE for comparisons
- Use XSDBOOL to set boolean variables
- Consider if booleans are the right choice (vs enumerations)

**Check for:**
- Use of CHAR1 or other types instead of ABAP_BOOL
- Comparisons with 'X' and ' ' instead of ABAP_TRUE/ABAP_FALSE
- IF-THEN-ELSE to set boolean instead of XSDBOOL
- Boolean parameters that should be split methods

### 8. Conditions

**Key Principles:**
- Try to make conditions positive
- Prefer IS NOT to NOT IS
- Consider predicative method calls for boolean methods
- Consider decomposing/extracting complex conditions

**Check for:**
- Negative conditions that could be positive
- NOT IS instead of IS NOT
- Complex nested conditions that should be decomposed
- Long conditions that should be extracted to methods

### 9. Ifs

**Key Principles:**
- No empty IF branches
- Prefer CASE to ELSE IF for multiple alternatives
- Keep nesting depth low

**Check for:**
- Empty IF with logic only in ELSE
- Multiple ELSE IF that should be CASE
- Deeply nested IF statements (>3 levels)

### 10. Classes

**Key Principles:**
- Prefer objects to static classes
- Prefer composition to inheritance
- Don't mix stateful and stateless in same class
- Global by default, local only where appropriate
- FINAL if not designed for inheritance
- Members PRIVATE by default, PROTECTED only if needed
- Consider immutable instead of getter

**Check for:**
- Static classes that should be instance-based
- Deep inheritance hierarchies
- Mixed stateful/stateless methods
- Non-FINAL classes not designed for inheritance
- PUBLIC members that should be PRIVATE/PROTECTED
- Unnecessary getter methods for immutable data

### 11. Methods

**Key Principles:**
- Prefer instance to static methods
- Public instance methods should implement interfaces
- Aim for few IMPORTING parameters (<3)
- Split methods instead of OPTIONAL parameters
- RETURN, EXPORT, or CHANGE exactly one parameter
- Prefer RETURNING to EXPORTING
- Do one thing, do it well, do it only
- Keep methods small (3-5 statements ideal)
- Fail fast
- Omit RECEIVING, EXPORTING keywords when possible
- Omit self-reference ME when calling instance members

**Check for:**
- Static methods that should be instance methods
- Public methods not part of an interface
- Methods with >3 IMPORTING parameters
- Multiple OPTIONAL parameters (should be split methods)
- Multiple output parameters
- EXPORTING instead of RETURNING
- Long methods (>20 lines)
- Methods doing multiple things
- Unnecessary RECEIVING, EXPORTING keywords
- Explicit ME-> calls

### 12. Error Handling

**Key Principles:**
- Prefer exceptions to return codes
- Use class-based exceptions
- Throw CX_STATIC_CHECK for manageable exceptions
- Throw CX_NO_CHECK for unrecoverable situations
- Prefer RAISE EXCEPTION NEW to RAISE EXCEPTION TYPE
- Wrap foreign exceptions

**Check for:**
- Return codes instead of exceptions
- Use of message classes for error handling
- Old-style RAISE EXCEPTION TYPE
- Unwrapped foreign exceptions
- Catching generic CX_ROOT

### 13. Comments

**Key Principles:**
- Express yourself in code, not comments
- Comments are no excuse for bad names
- Write comments to explain why, not what
- Comment with ", not *
- Delete code instead of commenting it
- Use FIXME, TODO, XXX with your ID
- ABAP Doc only for public APIs

**Check for:**
- Obvious comments explaining what code does
- Comments compensating for bad names
- Commented-out code
- * comments instead of "
- Comments without TODO/FIXME tags
- Manual versioning in comments
- Duplicate message texts in comments

### 14. Formatting

**Key Principles:**
- Use ABAP Formatter before activating
- No more than one statement per line
- Reasonable line length (120 chars)
- Single blank lines to separate (not more)
- Close brackets at line end
- Keep single parameter calls on one line
- Indent and snap to tab

**Check for:**
- Multiple statements per line
- Lines exceeding 120 characters
- Multiple consecutive blank lines
- Inconsistent indentation
- Chained assignments

### 15. Testing

**Key Principles:**
- Write testable code
- Test publics, not private internals
- Use given-when-then structure
- Few, focused assertions
- Use the right assert type

**Check for:**
- Untestable code (tight coupling, no dependency injection)
- Tests without clear given-when-then structure
- Multiple unrelated assertions
- Missing test classes for public methods

## Output Format

Structure your analysis as follows:

```
# Clean ABAP Check Results

## Summary
- Total Issues: [count]
- Critical: [count]
- Major: [count]
- Minor: [count]

## Critical Issues

### [Category] - [Issue Title]
**Location:** Line [X] / Method [name]
**Problem:** [Description of what violates Clean ABAP]
**Recommendation:** [How to fix it]

**Anti-pattern:**
```abap
[problematic code]
```

**Clean code:**
```abap
[improved code]
```

## Major Issues
[Same format as Critical]

## Minor Issues
[Same format as Critical]

## Positive Observations
- [Things done well according to Clean ABAP]

## Overall Assessment
[Brief summary of code quality and main areas for improvement]
```

## Priority Levels

**Critical:** Issues that significantly impact maintainability, testability, or could cause bugs
- Magic numbers without constants
- Deep nesting (>3 levels)
- Methods with >5 parameters
- Empty IF branches
- Static classes without interfaces
- Return codes instead of exceptions

**Major:** Issues that reduce code clarity and violate Clean ABAP principles
- Non-descriptive names
- Hungarian notation/prefixes
- Long methods (>20 lines)
- DEFAULT KEY usage
- Commented-out code
- Multiple output parameters

**Minor:** Issues that are stylistic improvements
- Missing inline declarations
- String quotes instead of backticks
- Unnecessary ME-> references
- Formatting inconsistencies

## References

When you need detailed explanations or examples for specific Clean ABAP rules, consult these reference files:

1. **Complete Guidelines**: Read `@skills/clean-abap/references/CleanABAP.md` - the full Clean ABAP style guide with in-depth explanations, rationale, and code examples for all principles
2. **Quick Patterns**: Read `@skills/clean-abap/references/quick-reference.md` - condensed good/bad code examples for common patterns
3. **Review Checklist**: Read `@skills/clean-abap/references/checklist.md` - a checklist format for systematic code reviews

**When to consult references:**
- To provide accurate citations when explaining violations
- To show users the official reasoning behind recommendations
- To find specific code examples to illustrate points
- To answer follow-up questions about Clean ABAP principles
- When encountering edge cases not covered in the summary above

## Examples

### Example 1: Checking a Simple Method

**Input:**
```abap
METHOD calculate.
  DATA: lv_result TYPE i,
        lv_temp TYPE i.
  
  lv_temp = iv_value1 + iv_value2.
  IF lv_temp > 100.
    lv_result = lv_temp * 2.
  ELSE.
    lv_result = lv_temp.
  ENDIF.
  
  ev_result = lv_result.
ENDMETHOD.
```

**Output:**
```
# Clean ABAP Check Results

## Summary
- Total Issues: 4
- Critical: 0
- Major: 2
- Minor: 2

## Major Issues

### Names - Hungarian Notation Used
**Location:** Method calculate
**Problem:** Variables use Hungarian notation prefixes (lv_, iv_, ev_) which adds no value and violates Clean ABAP naming guidelines.
**Recommendation:** Remove prefixes and use descriptive names.

**Anti-pattern:**
```abap
DATA: lv_result TYPE i,
      lv_temp TYPE i.
```

**Clean code:**
```abap
DATA(result) = value1 + value2.
IF result > 100.
  result = result * 2.
ENDIF.
```

### Methods - EXPORTING Instead of RETURNING
**Location:** Method signature
**Problem:** Method uses EXPORTING parameter instead of RETURNING, preventing functional call style.
**Recommendation:** Use RETURNING parameter for single output value.

**Anti-pattern:**
```abap
METHOD calculate
  IMPORTING iv_value1 TYPE i
            iv_value2 TYPE i
  EXPORTING ev_result TYPE i.
```

**Clean code:**
```abap
METHOD calculate
  IMPORTING value1 TYPE i
            value2 TYPE i
  RETURNING VALUE(result) TYPE i.
```

## Minor Issues

### Variables - Up-front Declarations
**Location:** Lines 2-3
**Problem:** Variables declared up-front instead of inline, increasing distance between declaration and usage.
**Recommendation:** Use inline declarations with DATA( ).

### Language - Procedural Style
**Location:** Lines 5-9
**Problem:** Could use COND for conditional assignment instead of IF-ELSE.
**Recommendation:** Use functional constructs.

**Clean code:**
```abap
METHOD calculate
  IMPORTING value1 TYPE i
            value2 TYPE i
  RETURNING VALUE(result) TYPE i.
  
  DATA(sum) = value1 + value2.
  result = COND #( WHEN sum > 100 THEN sum * 2 ELSE sum ).
ENDMETHOD.
```

## Overall Assessment
The code is functional but uses outdated ABAP patterns. Main improvements needed: remove Hungarian notation, use RETURNING instead of EXPORTING, prefer inline declarations, and use functional language constructs. After these changes, the code will be significantly cleaner and more maintainable.
```
