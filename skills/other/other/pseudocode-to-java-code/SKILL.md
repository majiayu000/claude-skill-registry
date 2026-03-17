---
name: pseudocode-to-java-code
description: Converts pseudocode descriptions and algorithm specifications into complete, executable Java code. Use this skill when you need to implement algorithms from pseudocode, translate algorithm descriptions to Java, generate Java code from specifications, convert textbook algorithms to working code, or create executable implementations from high-level descriptions. Preserves logic and control flow while handling Java idioms, data structures, and includes test cases for verification.
---

# Pseudocode to Java Code

## Overview

This skill converts pseudocode descriptions and algorithm specifications into complete, executable Java programs. It preserves the original logic and control flow, applies appropriate Java idioms and data structures, and generates test cases to verify correctness.

## Workflow

### 1. Provide Pseudocode Input

Give the pseudocode or algorithm specification. Formats accepted:
- Structured pseudocode with keywords (IF, FOR, WHILE, etc.)
- Algorithm descriptions in plain text
- Textbook-style algorithm specifications
- Flowchart-like descriptions

**Example:**
```
FUNCTION findMax(array)
    max ← array[0]
    FOR i FROM 1 TO LENGTH(array) - 1 DO
        IF array[i] > max THEN
            max ← array[i]
        END IF
    END FOR
    RETURN max
END FUNCTION
```

### 2. Specify Requirements (Optional)

Provide additional context:
- Expected input/output types
- Performance requirements
- Specific Java version or features to use
- Edge cases to handle
- Naming preferences

### 3. Generate Java Code

The skill will produce:
- Complete Java class with proper structure
- Converted algorithm as Java method(s)
- Appropriate data structures and types
- Necessary imports
- Main method with test cases

**Output Example:**
```java
import java.util.*;

public class ArrayMaxFinder {

    public static void main(String[] args) {
        ArrayMaxFinder solution = new ArrayMaxFinder();

        // Test case 1: Normal array
        int[] arr1 = {3, 7, 2, 9, 1};
        System.out.println("Max: " + solution.findMax(arr1)); // Expected: 9

        // Test case 2: Single element
        int[] arr2 = {5};
        System.out.println("Max: " + solution.findMax(arr2)); // Expected: 5
    }

    /**
     * Finds the maximum value in an array
     * @param array the input array
     * @return the maximum value
     */
    public int findMax(int[] array) {
        int max = array[0];
        for (int i = 1; i < array.length; i++) {
            if (array[i] > max) {
                max = array[i];
            }
        }
        return max;
    }
}
```

### 4. Review Mapping Summary

The skill provides a summary explaining:
- How pseudocode constructs map to Java
- Data structure choices
- Type decisions
- Any assumptions made

**Example Summary:**
```
Mapping Summary:
- FUNCTION → public method
- array parameter → int[] array
- LENGTH(array) → array.length
- FOR loop → standard Java for loop
- IF condition → if statement
- RETURN → return statement
- Added null/empty array handling
- Included test cases for verification
```

### 5. Test and Verify

Run the generated code:
```bash
javac ArrayMaxFinder.java
java ArrayMaxFinder
```

Verify output matches expected results.

## Common Conversions

### Control Structures

**IF-ELSE:**
```
Pseudocode: IF condition THEN ... ELSE ... END IF
Java: if (condition) { ... } else { ... }
```

**FOR Loop:**
```
Pseudocode: FOR i FROM 1 TO n DO ... END FOR
Java: for (int i = 1; i <= n; i++) { ... }
```

**WHILE Loop:**
```
Pseudocode: WHILE condition DO ... END WHILE
Java: while (condition) { ... }
```

### Data Structures

**Array:**
```
Pseudocode: DECLARE array[n] OF INTEGER
Java: int[] array = new int[n];
```

**List:**
```
Pseudocode: DECLARE list AS LIST OF INTEGER
Java: List<Integer> list = new ArrayList<>();
```

**Map:**
```
Pseudocode: DECLARE map AS MAP FROM STRING TO INTEGER
Java: Map<String, Integer> map = new HashMap<>();
```

**Set:**
```
Pseudocode: DECLARE set AS SET OF INTEGER
Java: Set<Integer> set = new HashSet<>();
```

### Operations

**String Operations:**
- `LENGTH(string)` → `string.length()`
- `SUBSTRING(string, start, end)` → `string.substring(start, end)`
- `CONCATENATE(str1, str2)` → `str1 + str2`

**Math Operations:**
- `POWER(base, exp)` → `Math.pow(base, exp)`
- `SQRT(value)` → `Math.sqrt(value)`
- `MAX(a, b)` → `Math.max(a, b)`

## Use Cases

### Use Case 1: Implement Textbook Algorithm
```
User: "Convert this binary search pseudocode to Java"
→ Provide pseudocode
→ Generate complete Java implementation
→ Include test cases with sorted arrays
→ Verify correctness
```

### Use Case 2: Algorithm Assignment
```
User: "I have this sorting algorithm in pseudocode, need Java code"
→ Analyze pseudocode structure
→ Generate Java with proper array handling
→ Add test cases with various inputs
→ Provide complexity analysis
```

### Use Case 3: Interview Preparation
```
User: "Convert this graph traversal algorithm to Java"
→ Map pseudocode to Java collections
→ Use appropriate data structures (Queue, Set)
→ Generate clean, interview-ready code
→ Include edge case handling
```

### Use Case 4: Learning Java
```
User: "I understand the algorithm in pseudocode, how does it look in Java?"
→ Generate side-by-side comparison
→ Explain Java-specific idioms
→ Show best practices
→ Provide runnable examples
```

## Best Practices

1. **Type Safety**: Choose appropriate Java types based on pseudocode context

2. **Null Handling**: Add null checks for reference types

3. **Edge Cases**: Include handling for empty inputs, boundary conditions

4. **Naming Conventions**: Use camelCase for variables, PascalCase for classes

5. **Comments**: Preserve pseudocode as comments for clarity

6. **Test Coverage**: Generate tests for normal cases, edge cases, and error conditions

7. **Imports**: Include all necessary import statements

8. **Documentation**: Add Javadoc comments for public methods

## Advanced Features

### Generic Types

When pseudocode uses generic collections:
```
Pseudocode: DECLARE list AS LIST OF TYPE
Java: List<T> list = new ArrayList<>();
```

### Exception Handling

Add appropriate exception handling:
```java
try {
    // algorithm implementation
} catch (ArrayIndexOutOfBoundsException e) {
    // handle error
}
```

### Optimization

Apply Java-specific optimizations:
- Use StringBuilder for string concatenation
- Use enhanced for loops where appropriate
- Apply stream operations for functional style

## Limitations

1. **Ambiguous Types**: May need clarification for ambiguous pseudocode types

2. **Complex Data Structures**: Custom data structures may need additional specification

3. **Concurrency**: Pseudocode doesn't usually specify thread safety

4. **I/O Operations**: File/network operations need additional context

5. **Language Features**: Some pseudocode constructs may not have direct Java equivalents

## Resources

### references/mapping_patterns.md
Comprehensive guide to pseudocode-to-Java mappings:
- Control structure conversions
- Data structure mappings
- Common operations
- Algorithm patterns
- Type conversions
- Best practices

Read this reference when you need detailed mapping rules, want to understand conversion patterns, or need examples of specific constructs.

### assets/java_template.java
Basic Java class template:
- Standard class structure
- Main method with test cases
- Placeholder for methods
- Proper formatting

Use this template as a starting point for generated code.
