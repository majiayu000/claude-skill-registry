---
name: refactoring
description: "Improve code quality and maintainability through systematic identification of code smells and application of proven refactoring patterns. Use when the user requests refactoring or provides relevant inputs for this workflow."
license: "MIT"
metadata:
  author: "awesome-ai-agent-skills contributors"
  version: "1.1.0"
---

# Code Refactoring

This skill guides an AI agent through the disciplined process of restructuring existing code without changing its external behavior. Refactoring improves readability, reduces complexity, and makes the codebase easier to extend and maintain. The agent identifies code smells, proposes targeted refactoring patterns, applies transformations safely, and verifies correctness through tests.

## Workflow

1. **Identify Code Smells**: Scan the target code for common quality issues — long functions, deeply nested conditionals, duplicated logic, overly broad variable scoping, magic numbers, dead code, and large parameter lists. Flag each smell with its location and a brief explanation of why it harms the codebase.

2. **Select Refactoring Patterns**: For every identified smell, choose the most appropriate refactoring pattern. Common patterns include Extract Method, Rename Symbol, Simplify Conditional, Inline Variable, Replace Magic Number with Named Constant, Remove Dead Code, and Introduce Parameter Object. Explain the trade-offs and expected improvement for each proposed change.

3. **Plan the Change Order**: Determine a safe sequence for applying refactorings. Prefer small, independent changes that can each be verified in isolation. Group related changes (e.g., extracting a helper then renaming it) and avoid interleaving unrelated transformations that make rollback difficult.

4. **Apply Refactorings**: Transform the code one pattern at a time. Preserve the original public API and behavior. Use language-idiomatic constructs — list comprehensions in Python, destructuring in JavaScript, pattern matching in Rust, etc.

5. **Run Tests and Verify**: Execute the existing test suite after each transformation. If no tests exist, generate lightweight unit tests covering the refactored paths before and after the change. Confirm that all tests pass and that no regressions have been introduced.

6. **Document Changes**: Summarize each refactoring applied, the smell it addressed, and any follow-up improvements that are now possible. This summary serves as a commit message or PR description.

## Supported Languages

- Python
- JavaScript / TypeScript
- Java
- Go
- Rust
- C / C++
- Ruby

## Usage

Provide the code you want refactored along with an optional goal such as "reduce complexity," "improve naming," or "break this into smaller functions." The agent will analyze the code, present a refactoring plan, and apply the changes upon approval. You can also point the agent at an entire file or module and ask it to perform a general quality pass.

## Examples

### Example 1 — Extract Method and Simplify Conditionals (Python)

**User Request**: "This function is too long and the nested ifs are hard to follow. Refactor it."

**Before**:
```python
def register_user(payload):
    if payload.get("email"):
        if "@" in payload["email"]:
            if payload.get("password") and len(payload["password"]) >= 8:
                user = {"email": payload["email"], "active": True}
                db.save(user)
                send_welcome_email(user["email"])
                log.info(f"User {user['email']} registered")
                return user
            else:
                raise ValueError("Password must be at least 8 characters")
        else:
            raise ValueError("Invalid email format")
    else:
        raise ValueError("Email is required")
```

**After**:
```python
def register_user(payload):
    _validate_payload(payload)
    user = _create_user(payload["email"])
    _notify_and_log(user)
    return user

def _validate_payload(payload):
    if not payload.get("email"):
        raise ValueError("Email is required")
    if "@" not in payload["email"]:
        raise ValueError("Invalid email format")
    if not payload.get("password") or len(payload["password"]) < 8:
        raise ValueError("Password must be at least 8 characters")

def _create_user(email):
    user = {"email": email, "active": True}
    db.save(user)
    return user

def _notify_and_log(user):
    send_welcome_email(user["email"])
    log.info(f"User {user['email']} registered")
```

**Patterns applied**: Extract Method, Flatten Nested Conditionals (guard clauses).

### Example 2 — Remove Duplication and Introduce Constants (TypeScript)

**User Request**: "Clean up this Express route handler. There's a lot of repetition."

**Before**:
```typescript
app.post("/orders", async (req, res) => {
  if (!req.body.items || req.body.items.length === 0) {
    return res.status(400).json({ error: "Items are required" });
  }
  if (req.body.items.length > 50) {
    return res.status(400).json({ error: "Too many items" });
  }
  let total = 0;
  for (const item of req.body.items) {
    total += item.price * item.quantity;
  }
  if (total > 10000) {
    return res.status(400).json({ error: "Order exceeds maximum total" });
  }
  const order = { items: req.body.items, total: total, status: "pending" };
  await db.orders.insert(order);
  return res.status(201).json(order);
});
```

**After**:
```typescript
const MAX_ITEMS = 50;
const MAX_ORDER_TOTAL = 10_000;

app.post("/orders", async (req, res) => {
  const { items } = req.body;
  const validationError = validateOrder(items);
  if (validationError) {
    return res.status(400).json({ error: validationError });
  }

  const total = calculateTotal(items);
  if (total > MAX_ORDER_TOTAL) {
    return res.status(400).json({ error: "Order exceeds maximum total" });
  }

  const order = await createOrder(items, total);
  return res.status(201).json(order);
});

function validateOrder(items?: OrderItem[]): string | null {
  if (!items || items.length === 0) return "Items are required";
  if (items.length > MAX_ITEMS) return "Too many items";
  return null;
}

function calculateTotal(items: OrderItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

async function createOrder(items: OrderItem[], total: number) {
  const order = { items, total, status: "pending" as const };
  await db.orders.insert(order);
  return order;
}
```

**Patterns applied**: Extract Method, Replace Magic Number with Named Constant, Destructuring.

## Best Practices

- **Keep refactorings small and atomic.** Each change should be independently verifiable and easy to revert if something breaks.
- **Never refactor and add features at the same time.** Mixing behavior changes with structural changes makes bugs nearly impossible to trace.
- **Preserve the public API.** Internal restructuring should not force callers to change unless the user explicitly requests an API redesign.
- **Lean on the test suite.** If test coverage is low, write characterization tests that capture current behavior before refactoring.
- **Use guard clauses to flatten deeply nested conditionals.** Early returns improve readability far more than adding comments to nested branches.
- **Rename aggressively.** Clear names eliminate the need for comments. A function called `validate_email` is better than `check` with a comment explaining what it checks.

## Edge Cases

- **No existing tests**: Generate minimal tests that capture current input/output behavior before applying any transformations. Warn the user that confidence in correctness depends on test coverage.
- **Tightly coupled modules**: When refactoring one module would break imports or contracts in another, map the dependency graph first and propose an interface boundary before extracting logic.
- **Generated or vendored code**: Do not refactor auto-generated files (e.g., protobuf stubs, ORM migrations). Flag them and skip.
- **Performance-critical hot paths**: Some "ugly" code is intentionally optimized. Verify with the user before replacing hand-tuned loops with higher-level abstractions that may regress performance.
- **Mixed formatting styles**: If the file has inconsistent style (tabs vs. spaces, quote styles), run the project's formatter after refactoring rather than manually fixing style during the refactoring pass.
