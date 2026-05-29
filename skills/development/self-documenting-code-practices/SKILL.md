---
name: self-documenting-code-practices
description: Apply self-documenting code practices through good programming style and evaluate class design for abstraction quality. Use when writing code, conducting code reviews, designing class interfaces, or establishing documentation standards.
---

# Self-Documenting Code Practices

Apply these practices to create code that documents itself through quality design and style.

## Documentation Types

### External Documentation
- **Definition:** Information located outside source code listings, typically separate documents or Unit Development Folders (UDF)
- **Unit Development Folder (UDF) / Software Development Folder (SDF):**
  - Informal documentation containing developer notes during construction
  - Primary purpose: provide clues about design decisions not recorded elsewhere
  - Contents: copies of relevant requirements, top-level design sections, development standards, current code listings, design notes
- **Detailed Design Document:** Low-level design document describing class-level or routine-level design decisions

### Internal Documentation (Programming Style)
- **Definition:** Documentation located within the program listing itself
- **Characteristics:** Most detailed documentation type, at source statement level
- **Advantage:** Most closely tied to code, most likely to remain correct when code is modified

## Programming Style as Primary Documentation

**Core principle:** The primary contributor to code-level documentation is not comments, but good programming style.

**Components of good programming style:**
- Good program structure
- Straightforward, easy-to-understand methods
- Good variable naming
- Good routine naming
- Use of named constants instead of literals
- Clear layout
- Minimized control flow and data structure complexity

**Goal:** Achieve "self-documenting code" where the code itself carries most of the documentation burden.

**Effect:** Good programming style makes code meaning obvious without relying on extensive comments.

## Self-Documenting Code Checklist: Classes

**When to apply:** When designing or reviewing classes

Verify the following points:

1. **Abstraction consistency:** Does the class interface present a consistent abstraction?
2. **Naming accuracy:** Is the class well-named, describing its core purpose?
3. **Interface intuitiveness:** Does the class interface clearly indicate how to use it?
4. **Abstraction level:** Is the interface abstract enough that users don't need to consider implementation details?
5. **Black-box property:** Can the class be treated as a black box?

**Action:** If any answer is "no," refactor the class design.

## Result
- Code is self-explanatory and easy to understand
- Class interfaces present clean abstractions
- Documentation burden is reduced through quality design
- Code is easier to maintain and modify