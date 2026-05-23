---
name: class-organization-and-layout
description: Organize class members in standard order, separate classes with blank lines, and maintain one-class-per-file structure. Use when designing class interfaces, implementing classes, organizing project files, or establishing OOP coding standards.
---

# Class Organization and Layout

Apply these principles to create consistent, maintainable class structures.

## Class Interface Member Order

**When to apply:** When defining class interfaces in header files

Present class members in this order:

1. Header comment: Describes the class and provides overall usage instructions
2. Constructors and destructors
3. Public routines
4. Protected routines
5. Private routines and member data

## Class Implementation Member Order

**When to apply:** When implementing classes in source files

Organize class implementation in this order:

1. Header comment: Describes the file contents
2. Class data
3. Public routines
4. Protected routines
5. Private routines

## File-to-Class Relationship

**When to apply:** When organizing project files (in languages that support multiple source files)

1. **Single responsibility:** Each file should contain routines supporting a single, unique purpose
2. **One-to-one relationship:** 
   - Place only one class per file when language permits (C++, Java, VB)
   - Exception: compelling reasons exist (e.g., several small classes forming a single pattern)
3. **File naming:** Relate filename to class name (e.g., `CustomerAccount` class → `CustomerAccount.cpp` and `CustomerAccount.h`)
4. **Concept reinforcement:** Files reinforce that grouped routines belong to the same class

## Class Visual Separation

**When to apply:** When separating different classes within a file

1. Use multiple blank lines to clearly identify and separate each class
2. **Avoid over-emphasis:**
   - Don't mark every routine and comment with asterisk lines
   - When everything is emphasized, nothing is truly emphasized
3. **Hierarchical separation** (if special characters must be used):
   - Establish character hierarchy (densest to sparsest)
   - Example: Asterisks for class separation, dashes for routine separation, blank lines for important comments
   - Never place two lines of asterisks or dashes together

**Principle:** In formatting, less is more.

## Result
- Class boundaries are clearly visible
- Visual noise is minimized
- File structure reinforces class organization
- Members follow consistent ordering conventions