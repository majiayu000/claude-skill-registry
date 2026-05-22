---
name: maintainability
description: Maintainability assessment criteria for code review. Apply when evaluating code for readability, change tolerance, hidden assumptions, and debuggability.
user-invocable: false
---

# Maintainability Assessment

Evaluate whether code will be easy to understand, modify, extend, and debug over time.

## Quick Reference

| Factor | Key Question | Severity |
|--------|--------------|----------|
| Readability | Understandable in 6 months? | Critical if high cognitive load |
| Change tolerance | Changes localized? | Improvement |
| Extensibility | Add without modifying? | Improvement |
| Hidden assumptions | Constraints explicit? | Critical if causes bugs |
| Debuggability | Failures traceable? | Critical if silent |
| Intent documentation | "Why" captured? | Improvement |

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Clever one-liners | Requires mental parsing | Named intermediate steps |
| Scattered logic | Changes touch many files | Centralize related behavior |
| Hardcoded values | Configuration changes require code changes | Use config objects |
| Growing if/elif chains | Every new type modifies existing code | Registry or protocol pattern |
| Bare `except:` | Swallows all errors including KeyboardInterrupt | Catch specific exceptions |
| Silent failures | No trace when things go wrong | Log errors with context |
| Comments saying "what" | Restates code | Explain "why" |

---

## Readability

### Check: Can someone understand this in 6 months?

```python
# HIGH COGNITIVE LOAD: Too much at once
def process(data):
    return {k: sum(x['value'] for x in v if x.get('active', True))
            for k, v in groupby(sorted(filter(lambda x: x['status'] != 'deleted',
            data), key=lambda x: x['category']), key=lambda x: x['category'])}

# READABLE: Named intermediate steps
def process(data):
    active_items = [x for x in data if x['status'] != 'deleted']
    sorted_items = sorted(active_items, key=lambda x: x['category'])

    result = {}
    for category, items in groupby(sorted_items, key=lambda x: x['category']):
        result[category] = sum(x['value'] for x in items if x.get('active', True))
    return result
```

### Heuristics

- Can you explain what a function does in one sentence?
- Would a new team member understand this without asking questions?
- Are variable names descriptive enough to skip comments?

### Severity

- **Critical**: Understanding requires significant mental effort
- **Improvement**: Some parts require careful reading
- **Nitpick**: Minor clarity improvements possible

---

## Change Tolerance

### Check: How many places need modification for typical changes?

```python
# BRITTLE: User display logic scattered
# views.py
def user_profile(user):
    return f"{user.first_name} {user.last_name}"

# emails.py
def format_recipient(user):
    return f"{user.first_name} {user.last_name} <{user.email}>"

# Adding middle name requires 2+ file changes

# RESILIENT: Centralized
class User:
    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def email_display(self) -> str:
        return f"{self.display_name} <{self.email}>"
```

### Severity

- **Critical**: Typical changes require 5+ file modifications
- **Improvement**: 2-4 files need coordinated changes
- **Nitpick**: Changes generally localized but could be cleaner

---

## Extensibility

### Check: Can new behavior be added without modifying existing code?

```python
# CLOSED: Adding new type requires modifying existing code
def process_payment(payment):
    if payment.type == "credit_card":
        process_credit_card(payment)
    elif payment.type == "paypal":
        process_paypal(payment)
    elif payment.type == "crypto":  # had to add this
        process_crypto(payment)

# OPEN: New types don't touch existing code
class PaymentProcessor(Protocol):
    def process(self, payment: Payment) -> Result: ...

PROCESSORS: dict[str, PaymentProcessor] = {
    "credit_card": CreditCardProcessor(),
    "paypal": PayPalProcessor(),
}

def process_payment(payment):
    return PROCESSORS[payment.type].process(payment)
```

### Severity

- **Improvement**: Extending requires modifying existing functions/classes
- **Nitpick**: Extension points exist but could be cleaner

---

## Hidden Assumptions

### Check: Are constraints and expectations explicit?

```python
# HIDDEN: items is never empty
def get_average(items):
    return sum(items) / len(items)  # ZeroDivisionError

# EXPLICIT: Documented and enforced
def get_average(items: list[float]) -> float:
    """Calculate average. Raises ValueError if items is empty."""
    if not items:
        raise ValueError("Cannot calculate average of empty list")
    return sum(items) / len(items)
```

### Severity

- **Critical**: Hidden assumptions will cause production bugs
- **Improvement**: Assumptions reasonable but not documented
- **Nitpick**: Assumptions obvious from context

---

## Debuggability

### Check: When things fail, is it clear why?

```python
# BAD: Silent failure
def update_user(user_id, data):
    user = get_user(user_id)
    if user:
        user.update(data)
    # if user doesn't exist... nothing happens

# BAD: Exception swallowing
try:
    result = complex_operation()
except Exception:
    pass

# GOOD: Specific error with context
def update_user(user_id, data):
    user = get_user(user_id)
    if user is None:
        raise UserNotFoundError(f"No user with id {user_id}")
    user.update(data)

# GOOD: Logged with structured context
def process_batch(items):
    for item in items:
        try:
            process(item)
        except Exception as e:
            logger.error(f"Failed to process item {item.id}: {e}",
                        extra={"item_id": item.id, "item_type": item.type})
```

### Severity

- **Critical**: Failures are silent or swallowed
- **Improvement**: Errors lack context for debugging
- **Nitpick**: Errors could be slightly more informative

---

## Intent Documentation

### Check: Is the "why" captured, not just the "what"?

```python
# USELESS: Restates the code
x = x + 1  # increment x

# USEFUL: Explains why
x = x + 1  # account for 0-indexing in the API response

# WITHOUT CONTEXT: What is this magic?
if (n & (n - 1)) == 0 and n != 0:
    ...

# WITH CONTEXT: Clear purpose
# Check if n is a power of 2 (only one bit set)
if (n & (n - 1)) == 0 and n != 0:
    ...
```

### Severity

- **Improvement**: Complex logic lacks explanation
- **Nitpick**: Documentation could be clearer but code is understandable

---

## Quick Smell Test

Answer these for any significant code change:

1. **New developer test**: Could someone unfamiliar fix a bug in this?
2. **2am test**: Could you debug this at 2am with incomplete logs?
3. **Feature request test**: Could you add a related feature without rewriting?
4. **Handoff test**: Could you explain this to a colleague in 5 minutes?

If any answer is "no", the code likely has maintainability issues worth flagging.

## Convention Reference

When flagging maintainability issues in reviews, reference this skill:

```markdown
**Convention**: See `maintainability` skill: Debuggability
```
