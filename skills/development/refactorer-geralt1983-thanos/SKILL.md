---
name: Refactorer
description: Code refactoring, cleanup, and improvement. USE WHEN user mentions refactor, cleanup, improve, simplify, extract, rename, deduplicate, DRY, rewrite, modernize, technical debt, code smell, or asks to make code better without changing behavior.
---

# Refactorer Skill

AI-powered refactoring guidance for improving code structure, readability, and maintainability while preserving behavior with focus on systematic transformations, safe changes, and measurable improvements.

## What This Skill Does

This skill provides expert-level refactoring guidance including identifying improvement opportunities, planning safe transformations, executing changes systematically, and verifying behavior preservation. It combines refactoring best practices with practical, behavior-preserving changes.

**Key Capabilities:**
- **Code Smell Detection**: Identifying patterns that indicate deeper problems
- **Refactoring Patterns**: Extract, rename, move, inline transformations
- **Safe Transformations**: Step-by-step changes that preserve behavior
- **Complexity Reduction**: Simplifying nested logic, long methods
- **Deduplication**: Finding and consolidating repeated code
- **Modernization**: Updating to current language idioms and APIs

## Core Principles

### The Refactoring Mindset
- **Behavior First**: Never change what code does, only how it does it
- **Small Steps**: One transformation at a time, test between
- **Test Before**: Have tests in place before refactoring
- **Know When to Stop**: Perfect is the enemy of good enough
- **Leave Camp Clean**: Code you touch should be better

### Refactoring Quality Metrics
1. **Readability** - Is the code easier to understand?
2. **Maintainability** - Is the code easier to modify?
3. **Testability** - Is the code easier to test?
4. **Simplicity** - Is the code simpler?
5. **Consistency** - Does the code follow patterns?

## Refactoring Workflow

### 1. Assessment
```
Analyze current state:
├── Test Coverage (do tests exist? what coverage?)
├── Code Smells (what patterns indicate problems?)
├── Complexity Metrics (cyclomatic, cognitive)
├── Dependencies (what else does this touch?)
└── Risk Level (critical path? frequently changed?)
```

### 2. Planning
```
Create refactoring plan:
├── Goals (what improvement are we targeting?)
├── Scope (what files/functions are involved?)
├── Order (what sequence of changes?)
├── Safety (how do we verify behavior?)
└── Rollback (how do we undo if needed?)
```

### 3. Execution
```
For each transformation:
├── Run Tests (ensure baseline passes)
├── Make Change (single, focused transformation)
├── Run Tests (ensure tests still pass)
├── Commit (small, atomic commit)
└── Review (did we improve? continue?)
```

### 4. Verification
```
Confirm success:
├── Tests Pass (same behavior)
├── Metrics Improved (complexity reduced)
├── Code Review (team agrees it's better)
└── Performance (no regression)
```

## Code Smell Catalog

### Bloaters
| Smell | Symptoms | Refactoring |
|-------|----------|-------------|
| **Long Method** | > 20 lines, multiple concerns | Extract Method |
| **Long Parameter List** | > 3-4 parameters | Parameter Object, Builder |
| **Large Class** | > 300 lines, many responsibilities | Extract Class |
| **Primitive Obsession** | Raw types for domain concepts | Value Objects |
| **Data Clumps** | Same fields appear together | Extract Class |

### Object-Orientation Abusers
| Smell | Symptoms | Refactoring |
|-------|----------|-------------|
| **Switch Statements** | Repeated switch/case on type | Polymorphism, Strategy |
| **Refused Bequest** | Subclass doesn't use inherited | Composition over Inheritance |
| **Alternative Classes** | Similar classes, different interfaces | Extract Interface |
| **Feature Envy** | Method uses other class's data | Move Method |
| **Inappropriate Intimacy** | Classes know too much about each other | Move Method/Field |

### Change Preventers
| Smell | Symptoms | Refactoring |
|-------|----------|-------------|
| **Divergent Change** | One class changed for different reasons | Extract Class |
| **Shotgun Surgery** | One change touches many classes | Move Method/Field |
| **Parallel Inheritance** | Create subclass in two hierarchies | Consolidate |

### Dispensables
| Smell | Symptoms | Refactoring |
|-------|----------|-------------|
| **Dead Code** | Unreachable or unused | Delete |
| **Speculative Generality** | Unused abstraction "for future" | Inline, Delete |
| **Duplicate Code** | Same logic in multiple places | Extract Method/Class |
| **Lazy Class** | Class does too little | Inline Class |

## Core Refactoring Patterns

### Extract Method
```python
# Before: Long method with multiple concerns
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Empty order")
    if not order.customer:
        raise ValueError("No customer")
    
    # Calculate totals
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * 0.1
    shipping = 5.99 if subtotal < 50 else 0
    total = subtotal + tax + shipping
    
    # Send notification
    email_body = f"Order total: ${total:.2f}"
    send_email(order.customer.email, "Order Confirmation", email_body)
    
    return total

# After: Small, focused methods
def process_order(order):
    validate_order(order)
    total = calculate_order_total(order)
    send_order_confirmation(order.customer, total)
    return total

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if not order.customer:
        raise ValueError("No customer")

def calculate_order_total(order):
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * 0.1
    shipping = 5.99 if subtotal < 50 else 0
    return subtotal + tax + shipping

def send_order_confirmation(customer, total):
    email_body = f"Order total: ${total:.2f}"
    send_email(customer.email, "Order Confirmation", email_body)
```

### Replace Conditional with Polymorphism
```python
# Before: Switch on type
def calculate_shipping(order):
    if order.shipping_type == "standard":
        return 5.99
    elif order.shipping_type == "express":
        return 15.99
    elif order.shipping_type == "overnight":
        return 29.99
    else:
        raise ValueError(f"Unknown shipping type: {order.shipping_type}")

# After: Polymorphism
from abc import ABC, abstractmethod

class ShippingMethod(ABC):
    @abstractmethod
    def calculate_cost(self, order) -> float:
        pass

class StandardShipping(ShippingMethod):
    def calculate_cost(self, order) -> float:
        return 5.99

class ExpressShipping(ShippingMethod):
    def calculate_cost(self, order) -> float:
        return 15.99

class OvernightShipping(ShippingMethod):
    def calculate_cost(self, order) -> float:
        return 29.99

# Usage
SHIPPING_METHODS = {
    "standard": StandardShipping(),
    "express": ExpressShipping(),
    "overnight": OvernightShipping(),
}

def calculate_shipping(order):
    method = SHIPPING_METHODS.get(order.shipping_type)
    if not method:
        raise ValueError(f"Unknown shipping type: {order.shipping_type}")
    return method.calculate_cost(order)
```

### Introduce Parameter Object
```python
# Before: Many related parameters
def create_user(first_name, last_name, email, phone, 
                street, city, state, zip_code, country):
    # ... create user with all these fields

# After: Group into objects
@dataclass
class PersonalInfo:
    first_name: str
    last_name: str
    email: str
    phone: str

@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str

def create_user(personal_info: PersonalInfo, address: Address):
    # ... cleaner, more cohesive
```

### Replace Magic Numbers
```python
# Before: Magic numbers
def calculate_price(quantity, price):
    if quantity > 10:
        return quantity * price * 0.9  # What is 0.9?
    elif quantity > 5:
        return quantity * price * 0.95  # What about 0.95?
    return quantity * price

# After: Named constants
BULK_DISCOUNT_THRESHOLD = 10
BULK_DISCOUNT_RATE = 0.10  # 10% off

VOLUME_DISCOUNT_THRESHOLD = 5
VOLUME_DISCOUNT_RATE = 0.05  # 5% off

def calculate_price(quantity, price):
    if quantity > BULK_DISCOUNT_THRESHOLD:
        return quantity * price * (1 - BULK_DISCOUNT_RATE)
    elif quantity > VOLUME_DISCOUNT_THRESHOLD:
        return quantity * price * (1 - VOLUME_DISCOUNT_RATE)
    return quantity * price
```

### Simplify Conditional Logic
```python
# Before: Nested conditionals (arrow code)
def get_user_discount(user):
    if user is not None:
        if user.is_active:
            if user.membership:
                if user.membership.level == "gold":
                    return 0.20
                elif user.membership.level == "silver":
                    return 0.10
                else:
                    return 0.05
            else:
                return 0
        else:
            return 0
    else:
        return 0

# After: Guard clauses + early returns
def get_user_discount(user):
    if user is None:
        return 0
    if not user.is_active:
        return 0
    if not user.membership:
        return 0
    
    discount_rates = {
        "gold": 0.20,
        "silver": 0.10,
    }
    return discount_rates.get(user.membership.level, 0.05)
```

## Deduplication Strategies

### Extract Common Method
```python
# Before: Duplicate validation in two places
class UserController:
    def create_user(self, data):
        if not data.get("email"):
            raise ValueError("Email required")
        if "@" not in data.get("email", ""):
            raise ValueError("Invalid email")
        # ... create user

    def update_user(self, user_id, data):
        if not data.get("email"):
            raise ValueError("Email required")
        if "@" not in data.get("email", ""):
            raise ValueError("Invalid email")
        # ... update user

# After: Extract to shared helper
class UserController:
    def _validate_email(self, data):
        email = data.get("email", "")
        if not email:
            raise ValueError("Email required")
        if "@" not in email:
            raise ValueError("Invalid email")
    
    def create_user(self, data):
        self._validate_email(data)
        # ... create user

    def update_user(self, user_id, data):
        self._validate_email(data)
        # ... update user
```

### Template Method Pattern
```python
# Before: Similar methods with slight variations
def export_csv(data):
    lines = ["name,email,phone"]  # Header
    for row in data:
        lines.append(f"{row.name},{row.email},{row.phone}")
    return "\n".join(lines)

def export_tsv(data):
    lines = ["name\temail\tphone"]  # Header
    for row in data:
        lines.append(f"{row.name}\t{row.email}\t{row.phone}")
    return "\n".join(lines)

# After: Template with customization point
def export_delimited(data, delimiter=","):
    lines = [delimiter.join(["name", "email", "phone"])]
    for row in data:
        lines.append(delimiter.join([row.name, row.email, row.phone]))
    return "\n".join(lines)

def export_csv(data):
    return export_delimited(data, delimiter=",")

def export_tsv(data):
    return export_delimited(data, delimiter="\t")
```

## Modernization Patterns

### Python Modernization
```python
# Old: Manual string formatting
message = "Hello, %s. You have %d messages." % (name, count)
message = "Hello, {}. You have {} messages.".format(name, count)

# Modern: f-strings (3.6+)
message = f"Hello, {name}. You have {count} messages."

# Old: Dictionary access with default
value = d.get("key", None)
if value is None:
    value = default_value

# Modern: Walrus operator (3.8+) or defaultdict
value = default_value if (v := d.get("key")) is None else v

# Old: Type checking in comments
def greet(name):  # type: (str) -> str
    return f"Hello, {name}"

# Modern: Type hints
def greet(name: str) -> str:
    return f"Hello, {name}"
```

### JavaScript Modernization
```javascript
// Old: var and function declarations
var self = this;
var items = [];
for (var i = 0; i < data.length; i++) {
    items.push(data[i].name);
}

// Modern: const/let, arrow functions, methods
const items = data.map(item => item.name);

// Old: Callbacks
function fetchData(callback) {
    ajax.get('/api/data', function(err, data) {
        if (err) callback(err);
        else callback(null, data);
    });
}

// Modern: async/await
async function fetchData() {
    const response = await fetch('/api/data');
    return response.json();
}

// Old: Object property shorthand
const obj = { name: name, age: age };

// Modern: Shorthand
const obj = { name, age };
```

## When to Use This Skill

**Trigger Phrases:**
- "This code is messy..."
- "How can I clean up..."
- "This function is too long..."
- "There's duplicate code in..."
- "Help me refactor..."
- "Make this more readable..."
- "This is hard to understand..."
- "Can we simplify..."

**Example Requests:**
1. "This function is 200 lines, help me break it up"
2. "I have the same code in three places"
3. "How do I remove these nested if statements?"
4. "This class does too many things"
5. "Help me modernize this old code"
6. "The tests are hard to write for this function"

## Refactoring Readiness Checklist

Before starting a refactoring:

- [ ] **Tests exist?** Behavior-preserving needs tests to verify
- [ ] **Tests pass?** Start from a known-good state
- [ ] **Scope defined?** Know what you're changing and what you're not
- [ ] **Time boxed?** Set a limit to avoid rabbit holes
- [ ] **Commit point?** Know where you can stop if interrupted
- [ ] **Team aligned?** Others know you're refactoring this area

## Safe Refactoring Steps

### IDE-Assisted Refactoring (Recommended)
```
Most modern IDEs can automatically:
├── Rename (variables, functions, classes, files)
├── Extract (method, variable, constant, interface)
├── Inline (method, variable)
├── Move (function, class to different file)
├── Change Signature (add/remove/reorder parameters)
└── Generate (constructors, getters/setters, delegating methods)

Use IDE refactoring tools when available - they update all references.
```

### Manual Refactoring Safely
```
1. Run tests - confirm they pass
2. Make smallest possible change
3. Run tests - confirm they still pass
4. Commit with descriptive message
5. Repeat until done

If tests fail after a change:
→ Undo immediately (git checkout)
→ Try a smaller step
```

## Integration with Other Skills

- **Architect**: Major restructuring follows architectural guidance
- **Tester**: Ensure test coverage before refactoring
- **Reviewer**: Post-refactor review confirms improvement
- **Troubleshooter**: Sometimes refactoring reveals or fixes bugs

---

*Skill designed for Thanos + Antigravity integration*
