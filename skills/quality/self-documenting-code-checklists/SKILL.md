---
name: self-documenting-code-checklists
description: Use this skill when writing, reviewing, or refactoring code to ensure it is self-documenting. Apply these checklists to routines, data naming, data organization, and overall code layout to improve code clarity and maintainability without relying on comments.
---

# Self-Documenting Code Checklists

Self-documenting code communicates its purpose through clear naming, structure, and organization rather than through comments. Use these checklists to evaluate and improve code clarity.

## When to Use

- Writing new routines, functions, or methods
- Conducting code reviews
- Refactoring existing code for maintainability
- Evaluating code quality and readability

## Routine Design Checklist

Apply this checklist when designing or reviewing functions, methods, and subroutines:

- [ ] **Naming accuracy**: Does the routine name accurately describe what it does?
- [ ] **Single responsibility**: Does the routine perform one well-defined task?
- [ ] **Modularity**: Have all parts that could benefit from being independent been extracted into their own routines?
- [ ] **Interface clarity**: Is the routine's interface obvious and clear?

**Action**: If any item is "no," refactor the routine.

## Data Naming Checklist

Apply this checklist when declaring or naming variables, constants, and types:

- [ ] **Type descriptiveness**: Is the type name descriptive enough to help document data declarations?
- [ ] **Variable naming**: Are variables named well?
- [ ] **Purpose consistency**: Is each variable used only for the purpose its name indicates?
- [ ] **Loop counters**: Do loop counters use more informative names than i, j, k?
- [ ] **Enumerated types**: Are well-named enums used instead of ad-hoc flags or booleans?
- [ ] **Named constants**: Are named constants used instead of magic numbers or magic strings?
- [ ] **Naming conventions**: Do naming conventions distinguish between type names, enums, named constants, local variables, class variables, and global variables?

**Action**: Rename variables or introduce constants if magic numbers or ambiguous names are found.

## Data Organization Checklist

Apply this checklist when organizing data access and structures:

- [ ] **Helper variables**: Are additional variables used where needed to improve clarity?
- [ ] **Reference locality**: Are references to variables grouped together?
- [ ] **Type simplicity**: Are data types simple to minimize complexity?
- [ ] **Abstract access**: Is complex data accessed through abstract access routines (abstract data types)?

**Action**: Refactor data structures or introduce intermediate variables to simplify logic.

## Layout and Design Checklist

Apply this checklist when reviewing code layout or high-level design:

- [ ] **Logical layout**: Does the program's layout display its logical structure?
- [ ] **Directness**: Is the code straightforward, avoiding "clever" tricks?
- [ ] **Hidden details**: Are implementation details hidden as much as possible?
- [ ] **Domain terminology**: Is the program written using problem-domain terminology rather than computer science or programming language terminology?

**Action**: Format and simplify code if it is too "clever" or the layout is confusing.