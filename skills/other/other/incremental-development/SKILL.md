---
name: incremental-development
description: Guidelines for incremental development practices. Claude should use this skill when writing multiple similar files (tests, classes, configurations) to ensure each piece is verified before moving to the next.
---

# Incremental Development Guidelines

When creating multiple similar files or implementing multiple similar features, follow these guidelines:

## One at a Time

Complete and verify ONE item before starting the next:

1. Write the first file
2. Update any dependencies (build.gradle, package.json, etc.)
3. Verify it compiles
4. Verify it runs/passes
5. Only then start the second file

## Why This Matters

- Catches errors early before they're duplicated
- Avoids propagating the same mistake across multiple files
- Faster debugging - you know exactly which change caused a problem
- Each verified step builds confidence for the next

## Examples

### Writing Multiple Tests

BAD:
```
Write TestA.java
Write TestB.java
Write TestC.java
Update build.gradle
Try to compile - find errors in all three
```

GOOD:
```
Write TestA.java
Update build.gradle with test dependencies
Compile TestA
Run TestA - verify it passes
Write TestB.java
Compile and run TestB
Write TestC.java
Compile and run TestC
```

### Writing Multiple Configuration Classes

BAD:
```
Write ConfigA.java
Write ConfigB.java
Compile - both have the same import error
```

GOOD:
```
Write ConfigA.java
Compile - works
Write ConfigB.java
Compile - works
```

## When to Apply

Apply incremental development when:
- Writing multiple test classes
- Creating multiple similar configuration classes
- Implementing multiple similar features
- Any task where files follow a similar pattern

Do NOT batch similar work if each piece requires verification.