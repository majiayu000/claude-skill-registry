---
name: code-smell-detector
description: Identify and report code smells indicating poor design or maintainability issues in Python code, including duplicate code, magic numbers, hardcoded values, God classes, feature envy, inappropriate intimacy, data clumps, primitive obsession, and long parameter lists. Use when conducting code quality audits, preparing for refactoring, improving codebase maintainability, or performing design reviews. Produces markdown reports with severity ratings, locations, descriptions, and specific refactoring recommendations with before/after examples. Triggers when users ask to find code smells, identify design issues, suggest refactorings, improve code quality, or detect maintainability problems.
---

# Code Smell Detector

## Overview

Identify code quality and design smells in Python codebases, then provide specific refactoring recommendations to improve maintainability and design.

## Workflow

### 1. Understand the Analysis Scope

Define what to analyze:

**Questions to ask:**
- What directory or files should be analyzed?
- Focus on quality smells, design smells, or both?
- Are there specific concerns (e.g., "this class is too complex")?
- Should test files be included?

**Determine scope:**
```bash
# Check project structure
ls -la

# Count Python files
find . -name "*.py" | wc -l

# Identify large files (potential smells)
find . -name "*.py" -exec wc -l {} + | sort -rn | head -10
```

### 2. Detect Code Smells

Use multiple detection strategies.

#### Strategy 1: Automated Detection

Use the bundled script for AST-based analysis:

```bash
# Scan entire project
python scripts/detect_smells.py /path/to/project

# Exclude specific directories
python scripts/detect_smells.py /path/to/project venv,tests,docs
```

**What it detects:**
- Long methods (>50 lines)
- Too many parameters (>5)
- Large classes (>15 methods)
- God classes (>20 methods)
- Magic numbers

#### Strategy 2: Manual Code Review

Read the code to identify design smells. See [smell-patterns.md](references/smell-patterns.md) for comprehensive catalog.

**Look for:**

**Code Quality Smells:**
- Duplicate code blocks
- Magic numbers (unexplained numeric literals)
- Hardcoded values (paths, URLs, config)
- Commented-out code
- Inconsistent naming

**Design Smells:**
- God classes (too many responsibilities)
- Feature envy (method uses more from another class)
- Inappropriate intimacy (classes too coupled)
- Data clumps (same parameters repeated)
- Primitive obsession (using primitives instead of objects)
- Long parameter lists (>5 parameters)

**Search patterns:**
```bash
# Find long files (potential large classes)
find . -name "*.py" -exec wc -l {} + | awk '$1 > 300'

# Find magic numbers (basic pattern)
grep -r "[^0-9]\d\{3,\}" --include="*.py" .

# Find hardcoded paths
grep -r '"/.*/"' --include="*.py" .

# Find commented code
grep -r "^[ ]*#.*def \|^[ ]*#.*class " --include="*.py" .
```

#### Strategy 3: Use External Tools

**radon** - Complexity metrics:
```bash
# Install
pip install radon

# Check cyclomatic complexity
radon cc /path/to/project -a

# Maintainability index
radon mi /path/to/project

# Show only complex functions
radon cc /path/to/project -nc
```

**pylint** - Code quality:
```bash
pip install pylint

# Check for code smells
pylint /path/to/project --disable=C0111  # Disable docstring warnings
```

### 3. Categorize Smells

Organize findings by severity and type.

See [smell-patterns.md](references/smell-patterns.md) for detailed patterns.

#### High Severity

**Immediate attention needed:**
- God classes (>20 methods, multiple responsibilities)
- Shotgun surgery (changes ripple across many files)
- Feature envy (method belongs in different class)
- Long parameter lists (>7 parameters)

#### Medium Severity

**Should refactor soon:**
- Large classes (>15 methods)
- Duplicate code
- Data clumps
- Primitive obsession
- Inappropriate intimacy

#### Low Severity

**Nice to improve:**
- Magic numbers
- Hardcoded values
- Inconsistent naming
- Lazy classes
- Commented-out code

### 4. Identify Refactorings

For each smell, determine appropriate refactoring.

See [refactoring-patterns.md](references/refactoring-patterns.md) for detailed examples.

**Common mappings:**

| Smell | Refactoring |
|-------|-------------|
| God class | Extract Class, Extract Service |
| Feature envy | Move Method |
| Duplicate code | Extract Method, Pull Up Method |
| Data clumps | Introduce Parameter Object |
| Magic numbers | Replace with Symbolic Constant |
| Long parameter list | Introduce Parameter Object |
| Primitive obsession | Replace Data Value with Object |
| Inappropriate intimacy | Move Method, Hide Delegate |
| Shotgun surgery | Move Method, Inline Class |
| Lazy class | Inline Class, Collapse Hierarchy |

### 5. Generate Report

Create a structured markdown report with specific refactoring recommendations.

## Code Smell Analysis Report

**Project:** [Project Name]
**Analyzed:** [Date]
**Scope:** [Directories analyzed]
**Excluded:** [Excluded directories]

---

## Summary

- **High severity smells:** X issues
- **Medium severity smells:** Y issues
- **Low severity smells:** Z issues

**Total:** N code smells detected

---

## 🔴 High Severity Smells

### Smell 1: God Class

**Location:** `src/services/user_manager.py:15`

**Class:** `UserManager`

**Description:** Class has 28 methods handling multiple unrelated responsibilities (user CRUD, authentication, email, logging, analytics).

**Impact:**
- Violates Single Responsibility Principle
- Hard to test and maintain
- Changes ripple across unrelated features

**Refactoring:** Extract Class

**Recommendation:**

Split into focused classes by responsibility:

```python
# Before: God class with 28 methods
class UserManager:
    def create_user(self, data): pass
    def update_user(self, user_id, data): pass
    def delete_user(self, user_id): pass
    def authenticate(self, username, password): pass
    def hash_password(self, password): pass
    def send_welcome_email(self, user): pass
    def send_password_reset(self, user): pass
    def log_activity(self, user, action): pass
    def get_statistics(self, user): pass
    # ... 19 more methods

# After: Split by responsibility
class UserRepository:
    """Handles user persistence."""
    def create(self, data): pass
    def update(self, user_id, data): pass
    def delete(self, user_id): pass
    def find_by_id(self, user_id): pass

class UserAuthService:
    """Handles authentication."""
    def authenticate(self, username, password): pass
    def hash_password(self, password): pass
    def validate_password_strength(self, password): pass

class UserNotificationService:
    """Handles user notifications."""
    def send_welcome_email(self, user): pass
    def send_password_reset(self, user): pass

class UserAnalyticsService:
    """Handles user analytics."""
    def log_activity(self, user, action): pass
    def get_statistics(self, user): pass
```

**Priority:** High - Refactor within 1-2 sprints

---

### Smell 2: Feature Envy

**Location:** `src/models/order.py:45`

**Method:** `Order.calculate_total()`

**Description:** Method uses customer features heavily (discount_rate, is_premium, shipping_address) rather than its own class features.

**Impact:**
- Poor cohesion - method is in wrong class
- Changes to Customer affect Order
- Violates "tell, don't ask" principle

**Refactoring:** Move Method

**Recommendation:**

Move calculation logic to Customer class:

```python
# Before: Feature envy
class Order:
    def calculate_total(self):
        discount = self.customer.get_discount_rate()
        is_premium = self.customer.is_premium_member()
        address = self.customer.get_shipping_address()

        total = sum(item.price for item in self.items)
        if is_premium:
            total *= (1 - discount)
        if address.country != 'US':
            total += 50
        return total

# After: Move to appropriate class
class Customer:
    def calculate_order_total(self, items):
        total = sum(item.price for item in items)
        if self.is_premium_member():
            total *= (1 - self.get_discount_rate())
        if self.shipping_address.country != 'US':
            total += 50
        return total

class Order:
    def calculate_total(self):
        return self.customer.calculate_order_total(self.items)
```

**Priority:** High - Refactor within 2 weeks

---

## 🟡 Medium Severity Smells

### Smell 3: Duplicate Code

**Locations:**
- `src/validators/user_validator.py:23-35`
- `src/validators/profile_validator.py:45-57`

**Description:** Identical email and name validation logic appears in two validators.

**Impact:**
- Changes must be made in multiple places
- Risk of inconsistent validation
- Maintenance burden

**Refactoring:** Extract Method

**Recommendation:**

Extract common validation into shared utility:

```python
# Before: Duplicate code
class UserValidator:
    def validate(self, data):
        if not data.get('email') or '@' not in data['email']:
            raise ValueError("Invalid email")
        if not data.get('name') or len(data['name']) < 2:
            raise ValueError("Invalid name")
        # ... more validation

class ProfileValidator:
    def validate(self, data):
        if not data.get('email') or '@' not in data['email']:
            raise ValueError("Invalid email")
        if not data.get('name') or len(data['name']) < 2:
            raise ValueError("Invalid name")
        # ... more validation

# After: Extract common validation
class ValidationHelpers:
    @staticmethod
    def validate_email(email):
        if not email or '@' not in email:
            raise ValueError("Invalid email")

    @staticmethod
    def validate_name(name):
        if not name or len(name) < 2:
            raise ValueError("Invalid name")

class UserValidator:
    def validate(self, data):
        ValidationHelpers.validate_email(data.get('email'))
        ValidationHelpers.validate_name(data.get('name'))
        # ... more validation

class ProfileValidator:
    def validate(self, data):
        ValidationHelpers.validate_email(data.get('email'))
        ValidationHelpers.validate_name(data.get('name'))
        # ... more validation
```

**Priority:** Medium - Refactor within month

---

### Smell 4: Data Clumps

**Locations:**
- `src/services/email_service.py:12` (6 parameters)
- `src/services/sms_service.py:23` (6 parameters)
- `src/services/notification_service.py:34` (6 parameters)

**Description:** Same parameter group (name, email, phone, address_street, address_city, address_zip) appears in multiple methods.

**Impact:**
- Suggests missing abstraction
- Hard to maintain - changes affect many signatures
- Easy to pass wrong parameters

**Refactoring:** Introduce Parameter Object

**Recommendation:**

Create ContactInfo value object:

```python
# Before: Data clumps
def send_email(name, email, phone, street, city, zip_code):
    pass

def send_sms(name, email, phone, street, city, zip_code):
    pass

def send_notification(name, email, phone, street, city, zip_code):
    pass

# After: Parameter object
from dataclasses import dataclass

@dataclass
class Address:
    street: str
    city: str
    zip_code: str

@dataclass
class ContactInfo:
    name: str
    email: str
    phone: str
    address: Address

def send_email(contact: ContactInfo):
    pass

def send_sms(contact: ContactInfo):
    pass

def send_notification(contact: ContactInfo):
    pass
```

**Priority:** Medium - Refactor within month

---

## 🔵 Low Severity Smells

### Smell 5: Magic Numbers

**Location:** `src/billing/calculator.py:67-78`

**Description:** Multiple unexplained numeric literals (1000, 0.15, 500, 0.10, 0.05).

**Impact:**
- Unclear business rules
- Hard to change discount thresholds
- Risk of typos

**Refactoring:** Replace Magic Number with Symbolic Constant

**Recommendation:**

Use named constants:

```python
# Before: Magic numbers
def calculate_discount(price):
    if price > 1000:
        return price * 0.15
    elif price > 500:
        return price * 0.10
    else:
        return price * 0.05

# After: Named constants
BULK_ORDER_THRESHOLD = 1000
LARGE_ORDER_THRESHOLD = 500
BULK_DISCOUNT_RATE = 0.15
LARGE_DISCOUNT_RATE = 0.10
STANDARD_DISCOUNT_RATE = 0.05

def calculate_discount(price):
    if price > BULK_ORDER_THRESHOLD:
        return price * BULK_DISCOUNT_RATE
    elif price > LARGE_ORDER_THRESHOLD:
        return price * LARGE_DISCOUNT_RATE
    else:
        return price * STANDARD_DISCOUNT_RATE
```

**Priority:** Low - Refactor when touching this code

---

## Recommendations

### Immediate Actions (High Priority)

1. Refactor UserManager god class into separate services
2. Move Order.calculate_total() to Customer class
3. Address feature envy in payment processing

### Short-term Actions (Medium Priority)

4. Extract duplicate validation logic
5. Introduce ContactInfo parameter object
6. Refactor large classes (>15 methods)

### Long-term Actions (Low Priority)

7. Replace magic numbers with named constants
8. Standardize naming conventions
9. Remove commented-out code

### Prevention Strategies

**Add to CI/CD:**
```bash
# Complexity checks
radon cc src/ -nc  # Fail on complex functions

# Code quality
pylint src/ --fail-under=8.0
```

**Code review checklist:**
- [ ] No methods >50 lines
- [ ] No classes >15 methods
- [ ] No parameter lists >5 parameters
- [ ] No duplicate code blocks
- [ ] No magic numbers
- [ ] No hardcoded config

**Regular audits:**
- Weekly: Review new code for smells
- Monthly: Full codebase smell detection
- Quarterly: Major refactoring sprints

---

### 6. Present Findings

Share report with team and discuss refactoring priorities.

**Presentation tips:**
- Start with summary statistics
- Focus on high-severity smells first
- Show before/after code examples
- Discuss business impact
- Prioritize based on team capacity

**Get team input:**
- "Does this class actually have too many responsibilities?"
- "Is this refactoring worth the effort?"
- "Should we tackle this now or later?"

## Tips for Effective Smell Detection

**Start with obvious smells:**
- Focus on metrics first (long methods, large classes)
- Look for duplicate code
- Check for magic numbers and hardcoded values

**Consider context:**
- Some "smells" may be justified
- Legacy code may have historical reasons
- Performance-critical code may break rules

**Prioritize by impact:**
- **High impact:** God classes, shotgun surgery
- **Medium impact:** Duplicate code, data clumps
- **Low impact:** Magic numbers, naming issues

**Refactor incrementally:**
- Don't refactor everything at once
- Focus on areas changing frequently
- Test after each refactoring step

**Use tools as guides:**
- Tools find potential issues
- Human judgment determines if it's truly a smell
- Team decides refactoring priorities

## Common False Positives

**Not every pattern is a smell:**

**Long methods may be acceptable:**
- Sequential data processing pipelines
- Complex algorithms better kept together
- Generated code

**Large classes may be justified:**
- Façade pattern intentionally centralizes
- DTO/Entity classes with many fields
- Framework base classes

**Magic numbers may be OK:**
- Well-known constants (0, 1, 100, 1024)
- Index operations
- Test data

**Consider trade-offs:**
- Refactoring has costs (time, risk, testing)
- Some smells aren't worth fixing
- Balance purity with pragmatism

## Reference

For comprehensive smell patterns and refactoring techniques:
- [smell-patterns.md](references/smell-patterns.md) - Detailed catalog of code smells
- [refactoring-patterns.md](references/refactoring-patterns.md) - Refactoring techniques with examples
