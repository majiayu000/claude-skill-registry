---
description: Comprehensive guide for creating by-example tutorials - code-first learning path with 75-90 heavily annotated examples achieving 95% language coverage. Covers five-part example structure, annotation density standards (1-2.25 comments per code line PER EXAMPLE), self-containment rules, and multiple code blocks for comparisons. Essential for creating by-example tutorials for programming languages on educational platforms
---

# By-Example Tutorial Creation Skill

## Purpose

This Skill provides comprehensive guidance for creating **by-example tutorials** - a code-first learning path designed for experienced developers who want rapid language pickup through heavily annotated working code examples.

**When to use this Skill:**

- Creating by-example tutorials for programming languages
- Writing heavily annotated code examples for education
- Designing code-first learning paths
- Achieving 95% language coverage through examples
- Meeting annotation density standards (1-2.25 comments per code line)
- Targeting experienced developers who know at least one language well

## Core Concepts

### What is By-Example?

**By-example tutorials** are a code-first learning path that achieves 95% language coverage through 75-90 heavily annotated, self-contained code examples.

**NOT a replacement for**:

- Beginner tutorials (which provide deep explanations for complete beginners)
- Quick Start (which is 5-30% coverage touchpoints)
- Cookbook (which is problem-solving oriented, not learning-oriented)

**Target Audience**:

- **Experienced developers**: Seasonal programmers, software engineers
- **Already know at least one programming language well**
- **Want quick language pickup** without extensive narrative
- **Prefer learning through working code**
- **Need 90% coverage efficiently**

### Five-Part Example Structure

Each example follows a consistent five-part structure:

```markdown
### Example N: Concept Name

**Brief explanation** (1-3 sentences describing what this example demonstrates)

**Optional diagram** (Mermaid diagram if concept relationships complex)

**Heavily commented code** (self-contained, runnable example with educational annotations)

**Key takeaway** (1-2 sentences summarizing the lesson)
```

## Annotation Density Standards

### The 1-2.25 Rule

**CRITICAL**: Target 1.0-2.25 comment lines per code line **PER EXAMPLE**

**Measurement**: Each code block is measured independently

- **Minimum**: 1.0 (examples below this need enhancement)
- **Optimal**: 1-2.25 (target range for educational value)
- **Upper bound**: 2.5 (examples exceeding this need reduction)

### Annotation Pattern

Use `// =>` or `# =>` notation to document:

- **Values**: Show variable values after assignment
- **States**: Show object/data structure states after modification
- **Outputs**: Show console/print output
- **Side effects**: Show file changes, network calls, database updates
- **Intermediate steps**: Show values during complex operations

**Examples**:

```java
// Simple line (1 annotation)
int x = 10;                      // => x is 10 (type: int)

// Complex line (2 annotations)
String result = transform(x);    // => Calls transform with 10
                                 // => result is "10-transformed" (type: String)

// Output line (1 annotation)
System.out.println(result);      // => Output: 10-transformed
```

```python
# Simple operation (1 annotation)
numbers = [1, 2, 3, 4, 5]       # => numbers is [1, 2, 3, 4, 5] (type: list)

# Complex operation (2 annotations)
squared = [n**2 for n in numbers]  # => List comprehension squares each number
                                    # => squared is [1, 4, 9, 16, 25]

# Output (1 annotation)
print(squared)                  # => Output: [1, 4, 9, 16, 25]
```

### Quality Over Quantity

**Focus on**:

- Concise explanations that scale with code complexity
- Simple operations get brief annotations
- Complex operations get detailed breakdowns
- Avoid repetitive patterns across similar code

## Self-Containment Rules

### What is Self-Contained?

Each example MUST be:

- **Runnable without dependencies**: No external libraries, files, or setup
- **Complete**: All necessary code in the example
- **Independent**: Doesn't require previous examples to work
- **Verified**: Actually runs and produces shown output

### How to Achieve Self-Containment

**DO**:

- Use only standard library features
- Include all helper functions/classes in example
- Provide sample data inline
- Show complete working code

**DON'T**:

- Require external packages (unless demonstrating that package)
- Reference code from previous examples
- Assume reader has specific files/data
- Show partial code snippets that won't compile

**Example (Java)**:

```java
// Self-contained - includes helper class
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {  // => Constructor
        this.name = name;                  // => Sets name field
        this.age = age;                    // => Sets age field
    }

    public String getName() { return name; }  // => Getter for name
}

public class Example {
    public static void main(String[] args) {
        Person p = new Person("Alice", 30);  // => Creates Person object
                                               // => p.name is "Alice", p.age is 30
        System.out.println(p.getName());     // => Output: Alice
    }
}
```

## Multiple Code Blocks for Comparisons

**CRITICAL**: Use **multiple code blocks with text between** when showing comparisons, alternatives, or before/after patterns.

**DO NOT** combine different approaches in single code block. Separate them for clarity.

**Example Pattern**:

````markdown
### Example: Mutable vs Immutable Approach

**Comparison**: Java String (immutable) vs StringBuilder (mutable)

**Immutable approach (String)**:

```java
String str = "Hello";           // => str is "Hello"
str = str + " World";           // => Creates NEW string
                                 // => str is "Hello World" (original discarded)
System.out.println(str);        // => Output: Hello World
```

**Text explanation**: Strings are immutable. Each concatenation creates a new String object, making repeated concatenations inefficient.

**Mutable approach (StringBuilder)**:

```java
StringBuilder sb = new StringBuilder("Hello");  // => sb is "Hello"
sb.append(" World");                             // => Modifies EXISTING object
                                                 // => sb is "Hello World" (no new object)
System.out.println(sb.toString());               // => Output: Hello World
```

**Text explanation**: StringBuilder is mutable. Append operations modify the existing object, making repeated concatenations efficient.

**Key takeaway**: Use String for immutable, final values. Use StringBuilder for building strings incrementally.
````

## Coverage Progression

### Three Tutorial Levels

By-example tutorials are split into three difficulty levels:

**Beginner (Examples 1-15)**:

- **Coverage**: 0-40% of language features
- **Focus**: Basic syntax, control flow, functions, simple data structures
- **Annotation density**: 1.5-2.25 (higher for fundamentals)

**Intermediate (Examples 16-35)**:

- **Coverage**: 40-75% of language features
- **Focus**: OOP/functional programming, modules, error handling, common patterns
- **Annotation density**: 1.0-1.75 (moderate for standard features)

**Advanced (Examples 36-60+)**:

- **Coverage**: 75-95% of language features
- **Focus**: Concurrency, metaprogramming, internals, advanced patterns
- **Annotation density**: 1.0-1.5 (concise for experienced developers)

### Total Coverage Target

**Goal**: 75-90 examples achieving 95% language coverage

**Not covered** (remaining 5%):

- Extremely rare features
- Deprecated features
- Platform-specific edge cases
- Niche use cases

## Mermaid Diagram Usage

### When to Use Diagrams

**Use diagrams for**:

- Complex concept relationships
- Data flow in multi-step operations
- Object hierarchies
- State transitions
- Execution flow in async/concurrent code

**Skip diagrams for**:

- Simple syntax examples
- Single-operation code
- Linear execution flow
- When code is self-explanatory

### Accessible Color Requirements

**CRITICAL**: All Mermaid diagrams MUST use accessible color palette

Use the **docs\_\_creating-accessible-diagrams** Skill for complete color guidance.

**Verified Accessible Palette**:

- Blue: `#0173B2`
- Orange: `#DE8F05`
- Teal: `#029E73`
- Purple: `#CC78BC`
- Brown: `#CA9161`

## Common Patterns

### Pattern 1: Basic Syntax Example

````markdown
### Example 1: Variable Declaration and Type Inference

**Demonstrates**: Basic variable declaration with type inference

```java
var x = 10;                    // => x is 10 (type: int, inferred)
var name = "Alice";            // => name is "Alice" (type: String, inferred)
var pi = 3.14;                 // => pi is 3.14 (type: double, inferred)

System.out.println(x);         // => Output: 10
System.out.println(name);      // => Output: Alice
System.out.println(pi);        // => Output: 3.14
```
````

**Key takeaway**: Use `var` for local variables when type is obvious from initializer.

`````

### Pattern 2: Complex Operation with Diagram

````markdown
### Example 25: Stream Pipeline Transformation

**Demonstrates**: Multi-stage data transformation using streams

**Data flow diagram**:

```mermaid
graph LR
    A[Source List] -->|filter| B[Even Numbers]
    B -->|map| C[Squared Values]
    C -->|collect| D[Result List]

    style A fill:#0173B2,stroke:#000,color:#fff
    style B fill:#DE8F05,stroke:#000,color:#000
    style C fill:#029E73,stroke:#000,color:#fff
    style D fill:#CC78BC,stroke:#000,color:#000
`````

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6);  // => Source data

List<Integer> result = numbers.stream()              // => Creates stream
    .filter(n -> n % 2 == 0)                         // => Keeps only even: [2, 4, 6]
    .map(n -> n * n)                                 // => Squares each: [4, 16, 36]
    .collect(Collectors.toList());                   // => Collects to List

System.out.println(result);                          // => Output: [4, 16, 36]
```

**Key takeaway**: Stream pipelines enable declarative data transformations with filter, map, and collect operations.

`````

### Pattern 3: Comparison Example (Multiple Code Blocks)

````markdown
### Example 40: Exception Handling - Try-Catch vs Try-With-Resources

**Comparison**: Manual resource closing vs automatic resource management

**Manual approach (try-catch-finally)**:

```java
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("data.txt"));  // => Opens file
    String line = reader.readLine();                           // => Reads first line
    System.out.println(line);                                  // => Output: [file content]
} catch (IOException e) {
    e.printStackTrace();                                       // => Handles errors
} finally {
    if (reader != null) {
        try {
            reader.close();                                    // => Closes manually
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

**Problem**: Verbose, error-prone (might forget to close), nested try-catch in finally.

**Automatic approach (try-with-resources)**:

```java
try (BufferedReader reader = new BufferedReader(new FileReader("data.txt"))) {
    // => Opens file, reader auto-closes when block exits
    String line = reader.readLine();                  // => Reads first line
    System.out.println(line);                         // => Output: [file content]
    // => reader.close() called automatically here
} catch (IOException e) {
    e.printStackTrace();                              // => Handles errors
}
```

**Benefit**: Concise, safe (guaranteed closing), no nested try-catch.

**Key takeaway**: Use try-with-resources for automatic resource management. Implements AutoCloseable interface.
`````

## Best Practices

### Example Creation Workflow

1. **Identify concept**: What specific feature/pattern to demonstrate?
2. **Write working code**: Ensure it compiles and runs
3. **Make self-contained**: Remove external dependencies
4. **Add annotations**: 1-2.25 comments per code line
5. **Verify output**: Run code, document actual output
6. **Add diagram** (if complex): Use accessible colors
7. **Write takeaway**: 1-2 sentence lesson summary
8. **Measure density**: Count annotations per code line

### Annotation Guidelines

**DO**:

- Document WHAT happens at each step
- Show variable values after operations
- Indicate types when useful
- Explain side effects
- Use consistent `// =>` or `# =>` notation

**DON'T**:

- Repeat obvious information ("assigns 10 to x" when code shows `x = 10`)
- Write paragraphs (keep annotations concise)
- Skip intermediate values in complex operations
- Use inconsistent notation styles

### Quality Checklist

Before publishing by-example tutorial:

- [ ] 75-90 examples total
- [ ] 95% language coverage achieved
- [ ] Each example follows five-part structure
- [ ] Annotation density 1.0-2.25 per example
- [ ] All examples are self-contained and runnable
- [ ] Multiple code blocks used for comparisons
- [ ] Diagrams use accessible color palette
- [ ] Examples progress from beginner → intermediate → advanced
- [ ] Key takeaways summarize lessons clearly

## Common Mistakes

### ❌ Mistake 1: File-level annotation density instead of per-example

**Wrong**: Measuring annotations across entire file

**Right**: Measure each example independently. One example with 0.5 density and another with 2.0 density both fail (first too low, second acceptable). Target 1.0-2.25 for EACH example.

### ❌ Mistake 2: Combining different approaches in single code block

```java
// WRONG! Mixed mutable and immutable in one block
String str = "Hello";
str = str + " World";
StringBuilder sb = new StringBuilder("Hello");
sb.append(" World");
```

**Right**: Use multiple code blocks with text between explaining differences.

### ❌ Mistake 3: Examples requiring external setup

```java
// WRONG! Requires database setup
Connection conn = DriverManager.getConnection("jdbc:...");
// Users can't run this without database
```

**Right**: Use in-memory data structures or mock objects for self-containment.

### ❌ Mistake 4: Missing intermediate values

```java
// WRONG! Complex operation with no intermediate annotations
int result = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .reduce(0, Integer::sum);  // => result is 56
```

**Right**: Annotate each stage showing intermediate values.

### ❌ Mistake 5: Paragraph annotations

```java
// WRONG! Too verbose
int x = 10;  // This line declares a variable named x and assigns it the integer value 10. Variables in Java must have a type, and here the type is int which represents 32-bit signed integers ranging from -2,147,483,648 to 2,147,483,647.
```

**Right**: Concise annotations scaling with code complexity.

## References

**Primary Convention**: [By Example Tutorial Convention](../../../../governance/conventions/tutorial/by-example.md)

**Related Conventions**:

- [Programming Language Tutorial Structure](../../../../governance/conventions/tutorial/programming-language-structure.md) - Dual-path organization
- [Programming Language Content Standard](../../../../governance/conventions/tutorial/programming-language-content.md) - Universal content architecture
- [Hugo ayokoding Convention](../../../../governance/conventions/hugo/ayokoding.md) - Code annotation standards for ayokoding-web

**Related Skills**:

- `apps__ayokoding-web__developing-content` - ayokoding-web specific patterns for hosting tutorials
- `docs__creating-accessible-diagrams` - Accessible diagram creation for complex examples

---

This Skill packages critical by-example tutorial creation knowledge for rapid language pickup. For comprehensive details, consult the primary convention document.
