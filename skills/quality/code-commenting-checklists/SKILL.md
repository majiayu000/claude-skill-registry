---
name: code-commenting-checklists
description: Use specific checklists to ensure comprehensive and high-quality code commenting for general code, data declarations, and program structures. Apply when writing new code, reviewing existing code, or conducting code reviews to ensure completeness and quality of documentation.
---

# Code Commenting Checklists

## When to Use This Skill
- Writing or reviewing code comments
- Conducting code reviews
- Establishing code quality standards
- Onboarding new developers to commenting practices
- Preparing code for maintenance or handoff

## General Comment Techniques Checklist

Apply this checklist to ensure overall comment quality:

- [ ] **Understandability**: Can others immediately pick up the code and understand it?
- [ ] **Intent explanation**: Does the comment explain the intent or summarize functionality, rather than repeating the code?
- [ ] **PPP usage**: Was Pseudocode Programming Process used to reduce commenting time?
- [ ] **Refactoring first**: Was tricky code rewritten instead of just adding comments?
- [ ] **Currency**: Are comments up-to-date with the current code?
- [ ] **Clarity**: Are comments clear and correct?
- [ ] **Maintainability**: Does the comment style allow easy modification?

## Data Declaration Comment Rules

Apply this checklist when declaring variables, constants, and data structures:

- [ ] **Units**: Are units of measurement commented? (e.g., `// milliseconds`, `// kilograms`)
- [ ] **Value ranges**: Are valid ranges for numeric data commented?
- [ ] **Encoding meanings**: Are coded values explained? (e.g., status codes, enum values)
- [ ] **Input constraints**: Are restrictions on input data documented?
- [ ] **Flag documentation**: Are flags documented to the bit level?
- [ ] **Global variables (declaration)**: Is each global variable commented at its declaration?
- [ ] **Global variables (usage)**: Is each global variable identified at every use via naming convention, comment, or both?
- [ ] **Magic numbers**: Are magic numbers replaced with named constants rather than just documented?

## Program Structure and File Comment Rules

Apply this checklist for subprograms, functions, classes, and files:

- [ ] **Subprogram purpose**: Is the purpose of each subprogram commented?
- [ ] **Subprogram details**: Are additional facts included when appropriate?
  - Input and output data
  - Interface assumptions
  - Limitations and constraints
  - Error correction behavior
  - Global effects
  - Algorithm sources
- [ ] **Control structures**: Is each control statement commented?
- [ ] **Complex structure endings**: Are long/complex control structure endings commented, or simplified to eliminate the need?
- [ ] **Program overview**: Is there a short document providing an overall view of program organization?
- [ ] **File purpose**: Is the purpose of each file described?
- [ ] **Author information**: Does the file include author name, email, and phone number?

## Usage Guidelines

### During Code Writing
1. Write comments as you write code
2. Apply relevant checklist items before committing
3. Review against all applicable checklists during self-review

### During Code Review
1. Use checklists as review criteria
2. Flag missing items for correction
3. Track common violations for team improvement

### For Legacy Code
1. Prioritize critical sections first
2. Focus on data declarations and public interfaces
3. Document complex logic before simple code

## Common Violations to Watch

### Data Declarations
```javascript
// BAD: No units or range
let timeout = 5000;

// GOOD: Complete documentation
// Timeout in milliseconds for API calls (range: 1000-30000)
let timeout = 5000;
```

### Magic Numbers
```python
# BAD: Magic number documented but not replaced
# Days in a year (365)
days = 365

# GOOD: Named constant
DAYS_IN_YEAR = 365
days = DAYS_IN_YEAR
```

### Global Variables
```java
// BAD: Global used without identification
public static int count;
// ... later ...
count++;

// GOOD: Clearly identified at usage
public static int g_userCount;  // Global: total active users
// ... later ...
g_userCount++;  // Global: increment active user count
```

### Control Structures
```javascript
// BAD: Complex structure without comment
for (let i = 0; i < items.length; i++) {
  for (let j = i + 1; j < items.length; j++) {
    if (items[i] > items[j]) {
      // swap
    }
  }
}

// GOOD: Commented or simplified
// Bubble sort: compare each pair and swap if out of order
for (let i = 0; i < items.length; i++) {
  for (let j = i + 1; j < items.length; j++) {
    if (items[i] > items[j]) {
      swap(items, i, j);
    }
  }
}
```