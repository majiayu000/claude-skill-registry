---
name: engineering-fundamentals
description: |
  TRIGGERS: "review my code", "is this clean?", "code review", "refactor this", "code quality",
  "refactoring", "cleaning up", "organizing", "structuring code", "naming this",
  "splitting function", "extract method", "too long", "messy code", "better way",
  naming conventions, DRY, SOLID, clean code, refactoring, code organization, best practices.
  USE WHEN: Junior is refactoring, organizing code, or asking about code quality and naming.
  PROVIDES: Naming standards, function size limits, DRY enforcement, SOLID principles, organization.
  PROACTIVE: Triggers when junior mentions refactoring or improving code structure.
---

# Engineering Fundamentals Review

> "Code is read more than it is written. Write for the reader, not the machine."

## When to Apply

Activate this skill when reviewing:
- Any code changes
- Function and variable naming
- Code organization and structure
- General refactoring decisions

---

## Review Checklist

### Naming

- [ ] **Descriptive**: Can you understand the variable without context?
- [ ] **No abbreviations**: Are names spelled out? (`user` not `usr`)
- [ ] **No generic names**: No `data`, `temp`, `info`, `stuff`?
- [ ] **Boolean prefix**: Do booleans start with `is`, `has`, `can`, `should`?
- [ ] **Function verbs**: Do functions start with action verbs?

### Function Design

- [ ] **Single responsibility**: Does each function do ONE thing?
- [ ] **Size limit**: Are functions under 20-30 lines?
- [ ] **Parameter count**: Are there fewer than 4 parameters?
- [ ] **No side effects**: Are pure functions actually pure?
- [ ] **Early returns**: Are guard clauses used instead of deep nesting?

### Code Organization

- [ ] **DRY**: Is duplicated code extracted into functions?
- [ ] **But not too DRY**: Are abstractions justified (rule of three)?
- [ ] **Cohesion**: Are related things grouped together?
- [ ] **Separation**: Are unrelated things separated?

### Comments & Documentation

- [ ] **Why, not what**: Do comments explain reasoning, not obvious code?
- [ ] **No commented-out code**: Is dead code deleted, not commented?
- [ ] **JSDoc on public APIs**: Are exported functions documented?

---

## Common Mistakes (Anti-Patterns)

### 1. Magic Numbers
```
❌ if (status === 2) { ... }
   setTimeout(callback, 86400000);

✅ const STATUS = { ACTIVE: 2, INACTIVE: 1 };
   if (status === STATUS.ACTIVE) { ... }

   const ONE_DAY_MS = 24 * 60 * 60 * 1000;
   setTimeout(callback, ONE_DAY_MS);
```

### 2. Unclear Naming
```
❌ const d = new Date();
   const temp = getUser();
   const flag = true;

✅ const createdAt = new Date();
   const currentUser = getUser();
   const isAuthenticated = true;
```

### 3. God Functions
```
❌ function processOrder(order) {
     // 200 lines: validate, calculate, save, email, log...
   }

✅ function processOrder(order) {
     validateOrder(order);
     const total = calculateTotal(order);
     await saveOrder(order, total);
     await sendConfirmationEmail(order);
     logOrderProcessed(order);
   }
```

### 4. Deep Nesting
```
❌ function check(user) {
     if (user) {
       if (user.active) {
         if (user.role === 'admin') {
           return true;
         }
       }
     }
     return false;
   }

✅ function check(user) {
     if (!user) return false;
     if (!user.active) return false;
     if (user.role !== 'admin') return false;
     return true;
   }
```

### 5. Premature Abstraction
```
❌ // Used once, but has 10 configuration options
   createFlexibleReusableButton({ ... });

✅ // Just make the button
   <button className="primary">Submit</button>

   // Abstract when you need it 3+ times
```

---

## SOLID Principles Quick Check

| Principle | Question | Red Flag |
|-----------|----------|----------|
| **S**ingle Responsibility | "Does this class/function do one thing?" | Class with 10+ methods |
| **O**pen/Closed | "Can I extend without modifying?" | Switch statements for types |
| **L**iskov Substitution | "Can I swap implementations?" | Overriding methods that break contracts |
| **I**nterface Segregation | "Are interfaces focused?" | Clients forced to depend on unused methods |
| **D**ependency Inversion | "Do high-level modules depend on abstractions?" | Direct instantiation of dependencies |

---

## Socratic Questions

Ask the junior these questions instead of giving answers:

1. **Naming**: "Would a new developer understand this name without context?"
2. **Function Size**: "Can you describe what this function does in one sentence?"
3. **Duplication**: "I see this pattern in three places. What happens if it needs to change?"
4. **Abstraction**: "How many times is this abstraction actually used?"
5. **Readability**: "If you came back to this code in 6 months, would you understand it?"

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | camelCase | `userName`, `isActive` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES`, `API_URL` |
| Functions | camelCase + verb | `getUser()`, `handleSubmit()` |
| Classes | PascalCase | `UserService`, `AuthProvider` |
| Files (components) | PascalCase | `UserProfile.tsx` |
| Files (utilities) | camelCase | `formatDate.ts` |

---

## Standards Reference

See detailed patterns in:
- `/standards/global/naming-conventions.md`

---

## Red Flags to Call Out

| Flag | Question to Ask |
|------|-----------------|
| Single letter variables | "What does `d` represent?" |
| Functions > 30 lines | "Can we break this into smaller functions?" |
| > 3 levels of nesting | "Can we use early returns?" |
| Copy-pasted code | "If this logic changes, how many places need updating?" |
| Commented-out code | "Is this needed? Can we delete it?" |
| TODO without tracking | "Is there a ticket for this?" |
| Magic strings/numbers | "Should this be a named constant?" |
