---
name: refactor-elegant-teaching
description: "Refactor code to be cleaner, more modular, and self-documenting when making code more teachable and maintainable. Not for quick fixes, non-educational changes, or style-only changes."
---

# Refactor: Elegant Teaching

Refactor code toward elegance—where structure teaches intent. Clean code reads like well-written prose: self-documenting, modular, and obvious to the next reader.

---

<absolute_constraints>

- NEVER refactor without first reading and understanding the existing code
- NEVER apply refactoring patterns dogmatically—context matters more than rules
- ALWAYS preserve existing behavior—refactoring changes structure, not function
- ALWAYS verify after refactoring with tests or manual validation
  </absolute_constraints>

---

## When to Use This Skill

**Apply this skill when:**

- Code is difficult to understand at first glance
- Functions do too many things (violating single responsibility)
- Variable names require comments to explain
- Nesting makes control flow hard to follow
- Duplication creates maintenance burden

**Do NOT use when:**

- Only formatting changes are needed (use a formatter)
- Adding new features (that's feature development)
- Fixing bugs (that's debugging)
- Code is already clear and maintainable

**Recognition question**: "Would this change make the code's intent more obvious to someone seeing it for the first time?"

---

## Core Philosophy

<router>
```mermaid
flowchart TD
    Start[Read code] --> Understand{Understand intent?}
    Understand -->|No| Investigate[Read more context]
    Investigate --> Understand
    Understand -->|Yes| Identify{What obscures intent?}

    Identify -->|Bad names| Rename[Rename variables/functions]
    Identify -->|Too long| Extract[Extract functions]
    Identify -->|Nested| Flatten[Flatten nesting]
    Identify -->|Duplicated| Deduplicate[Remove duplication]

    Rename --> Preserve[Preserve behavior]
    Extract --> Preserve
    Flatten --> Preserve
    Deduplicate --> Preserve

    Preserve --> Verify[Verify tests pass]
    Verify --> Done[Done]

</router>

**Remember**: Elegant code teaches. A reader should understand WHAT the code does, WHY it exists, and HOW it works—without needing additional explanation.

**Think of it this way**: Every line of code is a lesson plan for the next developer. Are you teaching clearly or obscuring the lesson?

---

## Refactoring Patterns

Apply these patterns based on what obscures intent in the specific code you're working with.

### Pattern 1: Rename for Clarity

**Problem**: Names require comments or mental translation.

**Solution**: Rename variables and functions to describe their purpose.

**Before**:

```typescript
const d = data.filter((x) => x.active);
const h = handleUser(u);
```

**After**:

```typescript
const activeUsers = data.filter((user) => user.isActive);
const handleAuthenticatedUser = (user: User) => {};
```

**Recognition**: "Does this name explain WHAT it is, not just its data type?"

### Pattern 2: Extract to Comprehend

**Problem**: Functions do multiple things or are too long to understand.

**Solution**: Extract logical chunks into named functions.

**Before**:

```typescript
function processOrder(order) {
  // Validate
  if (!order.id || !order.items) return null;

  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }

  // Apply discount
  if (order.couponCode === "SAVE10") {
    total *= 0.9;
  }

  // Save
  const saved = db.save({ ...order, total });
  return saved;
}
```

**After**:

```typescript
function processOrder(order: Order): ProcessedOrder | null {
  if (!isValidOrder(order)) return null;

  const total = calculateOrderTotal(order.items);
  const discountedTotal = applyCouponDiscount(total, order.couponCode);

  return saveOrder({ ...order, total: discountedTotal });
}

function isValidOrder(order: Order): boolean {
  return !!(order.id && order.items?.length);
}

function calculateOrderTotal(items: OrderItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyCouponDiscount(total: number, couponCode?: string): number {
  return couponCode === "SAVE10" ? total * 0.9 : total;
}
```

**Recognition**: "Can I describe what this code block does in a simple function name?"

### Pattern 3: Flatten Nesting

**Problem**: Deep nesting makes control flow hard to follow.

**Solution**: Use early returns and guard clauses.

**Before**:

```typescript
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        // Do the thing
      }
    }
  }
}
```

**After**:

```typescript
function processUser(user: User | null) {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission) return;

  // Do the thing
}
```

**Recognition**: "Am I indenting more than 3 levels? Time to flatten."

### Pattern 4: Remove Duplication

**Problem**: Same logic appears in multiple places.

**Solution**: Extract to a named function.

**Before**:

```typescript
// In three different files:
const formattedDate = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
```

**After**:

```typescript
// In utils/date.ts:
export function formatDateISO(date: Date): string {
  return date.toISOString().split("T")[0];
}
```

**Recognition**: "Have I seen this logic before? Extract it."

### Pattern 5: Replace Magic with Constants

**Problem**: Numbers or strings appear without explanation.

**Solution**: Name the values.

**Before**:

```typescript
if (retryCount > 3 && elapsed > 5000) {
}
```

**After**:

```typescript
const MAX_RETRIES = 3;
const REQUEST_TIMEOUT_MS = 5000;

if (retryCount > MAX_RETRIES && elapsed > REQUEST_TIMEOUT_MS) {
}
```

**Recognition**: "Would I understand this value in 6 months without context?"

---

## Degrees of Freedom

**High freedom**: These patterns are guidelines, not rules. Adapt them based on:

- Language idioms (Python differs from Rust)
- Codebase conventions (consistency with surrounding code matters)
- Performance constraints (sometimes clarity must yield to efficiency)
- Team preferences

**Low freedom**: NEVER violate these:

- Behavior preservation (refactoring must not change output)
- Test coverage (if tests exist, they must still pass)

**Recognition**: "What breaks if I don't follow this pattern?" If nothing breaks, consider skipping it.

---

## Workflow

Follow this sequence when refactoring:

1. **Read first**: Understand what the code does before changing anything
2. **Identify the smell**: What specifically makes this code hard to understand?
3. **Choose the pattern**: Select the refactoring that addresses the smell
4. **Make the change**: Apply the refactoring in small, verifiable steps
5. **Verify behavior**: Run tests or manually verify that nothing changed
6. **Commit separately**: Refactoring commits should be isolated from feature changes

**Recognition**: "Did I understand the code before I changed it?"

---

## Anti-Patterns to Avoid

### Anti-Pattern: Shotgun Refactoring

**❌ BAD**: Changing everything at once without understanding

```
"I'll just clean up this whole file while I'm here"
```

**✅ GOOD**: Focused, targeted changes

```
"This function is hard to understand—I'll extract the validation logic"
```

### Anti-Pattern: Refactoring Without Tests

**❌ BAD**: Hoping nothing breaks

**✅ GOOD**: Verify behavior is preserved

```
- Run tests first (they should pass)
- Make the refactoring change
- Run tests again (they should still pass)
```

### Anti-Pattern: Premature Abstraction

**❌ BAD**: Extracting things "just in case"

```typescript
// Don't create abstractions for code that's only used once
const getUserByIdFromDatabaseWithCache = abstractUserGetter("user");
```

**✅ GOOD**: Abstract when duplication actually exists

```typescript
// Wait until you see the pattern twice
const getUser = getById("users");
const getProduct = getById("products");
```

---

## Verification Checklist

Before considering refactoring complete:

- [ ] Tests pass (if tests exist)
- [ ] Behavior is unchanged (verified manually if no tests)
- [ ] Code is more readable than before
- [ ] No new abstractions were created "just in case"
- [ ] Names describe WHAT and WHY, not just data type
- [ ] Nesting is minimized (early returns used)
- [ ] Duplication was removed where it existed

---

## Integration

This skill works alongside:

- **engineering-lifecycle**: Refactor during the GREEN phase, never during RED
- **code-review**: Identify refactoring opportunities in PRs
- **quality-standards**: Verify refactoring preserved behavior

**Recognition**: "Am I in the RED phase? STOP—do not refactor yet."

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---

<critical_constraint>
MANDATORY: Read and understand code before refactoring
MANDATORY: Preserve existing behavior (refactor structure, not function)
MANDATORY: Run tests to verify behavior is unchanged
MANDATORY: Never refactor during RED phase (TDD workflow)
No exceptions. Refactoring without understanding breaks things.
</critical_constraint>```
