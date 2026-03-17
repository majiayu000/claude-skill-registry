---
name: design-smell-detector
description: "Identify design quality issues in code including high coupling, low cohesion, God classes, long methods, and other code smells. Use when: (1) Reviewing code architecture and design quality, (2) Identifying refactoring opportunities, (3) Detecting God classes or classes with too many responsibilities, (4) Finding high coupling or low cohesion issues, (5) Analyzing code maintainability and technical debt. Detects coupling smells, cohesion problems, complexity issues, size violations, and encapsulation problems with actionable refactoring suggestions."
---

# Design Smell Detector

Identify and address design quality issues in code through automated smell detection and refactoring guidance.

## Quick Start

### Detect Design Smells

```bash
# Analyze a single file
python scripts/detect_smells.py src/app.py

# Analyze entire directory
python scripts/detect_smells.py src/

# Output as JSON
python scripts/detect_smells.py src/ --format json
```

### Example Output

```
Found 5 design smell(s): 1 critical, 3 major, 1 minor

CRITICAL ISSUES:
  🔴 src/services.py:45 - God Class
     Class 'UserManager' has 25 methods (threshold: 20)
     💡 Split into multiple smaller, focused classes

MAJOR ISSUES:
  🟠 src/models.py:120 - Low Cohesion
     Class 'Order' has low cohesion (score: 0.25)
     💡 Group related methods/attributes or split class

  🟠 src/utils.py:89 - Long Method
     Method 'process_order' has 67 lines (threshold: 50)
     💡 Extract smaller methods or refactor
```

## Design Smells Detected

### Coupling Smells

**High Coupling**: Too many dependencies
- Module imports > 20
- Constructor dependencies > 10
- Changes cascade across classes

**Feature Envy**: Method uses other class more than own
- External access > internal access
- Method should move to envied class

**Inappropriate Intimacy**: Classes too tightly coupled
- Accessing private fields of other classes
- Excessive use of getters/setters

### Cohesion Smells

**Low Cohesion**: Class members unrelated
- LCOM (Lack of Cohesion) > 0.7
- Methods don't share instance variables
- Class has multiple responsibilities

**God Class**: Class knows/does too much
- Methods > 20
- Attributes > 15
- Lines of code > 500

### Complexity Smells

**High Cyclomatic Complexity**: Too many decision points
- Complexity > 10
- Deeply nested conditionals
- Many if/else, loops

**Long Method**: Method too long
- Lines of code > 50
- Multiple responsibilities
- Hard to understand

### Size Smells

**Long Parameter List**: Too many parameters
- Parameters > 5
- Related parameters not grouped
- Method signature hard to understand

**Large Module**: Module too large
- Classes > 20
- Lines of code > 1000
- Multiple responsibilities

### Encapsulation Smells

**Data Class**: Only data, no behavior
- Only getters/setters
- No business logic
- Missing encapsulation

**Exposed Internal State**: Implementation details exposed
- Public mutable fields
- Returns references to internal collections
- Breaks encapsulation

## Detection Workflow

### 1. Run Detection

Analyze codebase for design smells:

```bash
python scripts/detect_smells.py src/
```

### 2. Review Results

Examine detected smells by severity:
- **Critical**: God classes, severe coupling issues
- **Major**: Low cohesion, long methods, high complexity
- **Minor**: Long parameter lists, feature envy

### 3. Prioritize Refactoring

Focus on:
- Critical issues first
- Frequently changed code
- High-impact, low-effort improvements

### 4. Apply Refactoring

Use refactoring strategies based on smell type.

See **[refactoring_strategies.md](references/refactoring_strategies.md)** for detailed solutions.

### 5. Verify Improvements

Re-run detection to measure progress:

```bash
python scripts/detect_smells.py src/
```

Compare metrics before/after.

## Common Design Smells

### God Class

**Symptoms**:
- Too many methods (>20)
- Too many attributes (>15)
- Low cohesion
- Multiple responsibilities

**Example**:
```python
# ❌ God Class
class Application:
    # 30+ methods handling:
    # - User management
    # - Order processing
    # - Payment handling
    # - Reporting
    # - Email notifications
    # - File operations
    pass
```

**Refactoring**:
```python
# ✅ Split by responsibility
class UserManager:
    pass

class OrderProcessor:
    pass

class PaymentHandler:
    pass

class ReportGenerator:
    pass
```

### High Coupling

**Symptoms**:
- Too many imports (>20)
- Too many constructor dependencies
- Changes cascade across classes

**Example**:
```python
# ❌ High coupling
class UserService:
    def __init__(self):
        self.db = Database()
        self.cache = Cache()
        self.logger = Logger()
        self.validator = Validator()
        self.email = EmailService()
        self.sms = SMSService()
        # ... many more
```

**Refactoring**:
```python
# ✅ Dependency injection
class UserService:
    def __init__(self, db, logger, notifier):
        self.db = db
        self.logger = logger
        self.notifier = notifier  # Abstraction
```

### Low Cohesion

**Symptoms**:
- Methods don't share attributes
- Class does unrelated things
- LCOM score > 0.7

**Example**:
```python
# ❌ Low cohesion
class UserManager:
    def create_user(self):
        pass

    def send_email(self):
        pass

    def log_activity(self):
        pass

    def calculate_discount(self):
        pass
```

**Refactoring**:
```python
# ✅ High cohesion - focused classes
class UserRepository:
    def create_user(self):
        pass

class EmailService:
    def send_email(self):
        pass

class ActivityLogger:
    def log_activity(self):
        pass
```

### Long Method

**Symptoms**:
- Method > 50 lines
- Multiple responsibilities
- Hard to understand

**Example**:
```python
# ❌ Long method (100+ lines)
def process_order(order):
    # Validate (20 lines)
    # Calculate price (15 lines)
    # Save to DB (10 lines)
    # Send email (20 lines)
    # Update stats (10 lines)
    # Log activity (15 lines)
    pass
```

**Refactoring**:
```python
# ✅ Extract methods
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    save_order(order, total)
    send_confirmation(order)
    update_statistics()
    log_activity(order)
```

## Refactoring Strategies

### Reduce Coupling

**Dependency Injection**:
```python
# Inject dependencies instead of creating them
class OrderService:
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
```

**Interface Abstraction**:
```python
# Depend on abstractions, not implementations
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount):
        pass

class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
```

### Improve Cohesion

**Extract Class**:
```python
# Split into focused classes
class User:
    # User data and behavior

class UserRepository:
    # Database operations

class EmailService:
    # Email operations
```

**Move Method**:
```python
# Move method to appropriate class
class Account:
    def get_formatted_balance(self):  # Moved from reporter
        return f"${self.balance:.2f}"
```

### Reduce Complexity

**Extract Method**:
```python
# Break complex method into smaller ones
def process_order(order):
    validate_order(order)
    calculate_total(order)
    save_order(order)
```

**Replace Conditional with Polymorphism**:
```python
# Use inheritance instead of conditionals
class Customer:
    def calculate_price(self, base_price):
        return base_price

class PremiumCustomer(Customer):
    def calculate_price(self, base_price):
        return base_price * 0.9
```

For comprehensive refactoring strategies, see **[refactoring_strategies.md](references/refactoring_strategies.md)**.

## Metrics and Thresholds

### Detection Thresholds

| Smell | Metric | Threshold |
|-------|--------|-----------|
| God Class | Methods | > 20 |
| God Class | Attributes | > 15 |
| God Class | LOC | > 500 |
| High Coupling | Imports | > 20 |
| Low Cohesion | LCOM | > 0.7 |
| Long Method | LOC | > 50 |
| High Complexity | Cyclomatic | > 10 |
| Long Parameter List | Parameters | > 5 |

### Key Metrics

**LCOM (Lack of Cohesion of Methods)**:
- Measures how methods share instance variables
- Range: 0.0 (high cohesion) to 1.0 (low cohesion)
- Lower is better

**Cyclomatic Complexity**:
- Number of linearly independent paths
- Each if/while/for adds 1
- Lower is better (< 10)

**Fan-out (Coupling)**:
- Number of dependencies
- Lower is better (< 10)

## Design Smell Catalog

For complete descriptions, examples, and solutions for all design smells, see **[smell_catalog.md](references/smell_catalog.md)**.

Includes:
- **Coupling Smells**: High coupling, Feature Envy, Inappropriate Intimacy
- **Cohesion Smells**: Low cohesion, God Class
- **Complexity Smells**: High complexity, Long Method
- **Size Smells**: Long Parameter List, Large Module
- **Encapsulation Smells**: Data Class, Exposed Internal State

## Best Practices

### 1. Detect Regularly

Integrate into workflow:
```bash
# Pre-commit hook
python scripts/detect_smells.py src/

# CI/CD pipeline
make check-design-smells
```

### 2. Track Metrics Over Time

Monitor trends:
```
Sprint 1: 15 God classes, 45 long methods
Sprint 2: 12 God classes, 38 long methods
Sprint 3: 8 God classes, 25 long methods
```

### 3. Prioritize Strategically

Focus on:
- Code changed frequently
- Critical business logic
- High-impact areas

### 4. Refactor Incrementally

- Small, safe changes
- Run tests after each change
- Commit frequently

### 5. Measure Improvements

Before/after metrics:
```
Before: LCOM = 0.85 (low cohesion)
After:  LCOM = 0.25 (high cohesion)
```

## Common Scenarios

### Scenario 1: Legacy Codebase Modernization

**Goal**: Identify technical debt in legacy system

**Approach**:
1. Run smell detection on entire codebase
2. Generate metrics report
3. Identify top 10 worst files
4. Create refactoring backlog
5. Tackle incrementally

### Scenario 2: Code Review Enhancement

**Goal**: Automated design quality checks in PR reviews

**Approach**:
1. Add smell detection to CI pipeline
2. Fail build if critical smells introduced
3. Report metrics in PR comments
4. Require fixes before merge

### Scenario 3: Architecture Assessment

**Goal**: Evaluate system architecture quality

**Approach**:
1. Detect coupling and cohesion issues
2. Identify God classes and large modules
3. Analyze dependency structure
4. Recommend architectural improvements

## Integration with Development Workflow

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

python scripts/detect_smells.py src/
if [ $? -ne 0 ]; then
    echo "Critical design smells detected. Commit aborted."
    exit 1
fi
```

### CI/CD Pipeline

```yaml
# .github/workflows/quality.yml
name: Design Quality Check

on: [push, pull_request]

jobs:
  check-smells:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Detect design smells
        run: python scripts/detect_smells.py src/

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: smell-report
          path: smell-report.json
```

### IDE Integration

Most IDEs support similar analysis through plugins:
- **PyCharm**: Built-in inspections for coupling/cohesion
- **VS Code**: Python linting extensions
- **SonarLint**: Real-time smell detection

## Troubleshooting

### False Positives

**Problem**: Legitimate design flagged as smell

**Solution**:
- Understand context and constraints
- Consider if threshold should be adjusted
- Document reasons for exception

### Overwhelming Results

**Problem**: Too many smells to address

**Solution**:
- Filter by severity (critical first)
- Focus on frequently changed code
- Set incremental goals

### Refactoring Breaks Tests

**Problem**: Tests fail after refactoring

**Solution**:
- Ensure comprehensive test coverage first
- Refactor incrementally
- Run tests after each small change

## Reference Documentation

### Design Smell Catalog
See **[smell_catalog.md](references/smell_catalog.md)** for:
- Complete smell definitions
- Detection criteria and thresholds
- Code examples (before/after)
- Metrics explanations (LCOM, cyclomatic complexity, fan-out)
- All coupling, cohesion, complexity, size, and encapsulation smells

### Refactoring Strategies
See **[refactoring_strategies.md](references/refactoring_strategies.md)** for:
- Coupling reduction strategies (DI, interfaces, facades)
- Cohesion improvement (extract class, move method)
- Complexity reduction (extract method, polymorphism)
- Size reduction (split classes, parameter objects)
- Encapsulation improvement
- Refactoring workflow and best practices
- Anti-patterns to avoid
- Success metrics
