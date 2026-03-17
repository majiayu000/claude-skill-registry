---
name: code-refactoring-assistant
description: Suggest and apply code refactorings to improve readability, maintainability, and code quality. Use this skill when improving existing code structure, eliminating code smells, applying design patterns, simplifying complex logic, extracting duplicated code, renaming for clarity, or preparing code for new features. Provides specific before/after examples, explains benefits, identifies risks, and ensures behavior preservation through tests.
---

# Code Refactoring Assistant

Systematically improve code structure and quality through targeted refactorings. Identifies opportunities, suggests improvements, and applies changes while preserving behavior.

## Core Capabilities

### 1. Code Smell Detection

Identify refactoring opportunities:
- **Long methods/functions** - Functions doing too much
- **Large classes** - Classes with too many responsibilities
- **Duplicate code** - Repeated logic across codebase
- **Long parameter lists** - Functions with many parameters
- **Primitive obsession** - Using primitives instead of objects
- **Feature envy** - Methods using other classes more than their own
- **Data clumps** - Same group of data appearing together
- **Switch statements** - Complex conditionals that could be polymorphic

### 2. Structural Refactorings

Improve code organization:
- **Extract Method** - Pull out code into new function
- **Extract Class** - Split class responsibilities
- **Inline Method/Variable** - Remove unnecessary indirection
- **Move Method/Field** - Relocate to appropriate class
- **Rename** - Improve naming clarity
- **Change Function Signature** - Update parameters
- **Introduce Parameter Object** - Group parameters into object
- **Replace Conditional with Polymorphism** - Use inheritance/interfaces

### 3. Simplification Refactorings

Reduce complexity:
- **Decompose Conditional** - Simplify complex if/else
- **Consolidate Conditional** - Combine related conditions
- **Remove Dead Code** - Delete unused code
- **Simplify Boolean Expression** - Make logic clearer
- **Replace Magic Number with Constant** - Named constants
- **Replace Nested Conditional with Guard Clauses** - Early returns
- **Replace Loop with Pipeline** - Use functional operations

### 4. Generalization Refactorings

Improve abstraction:
- **Extract Interface** - Define contracts
- **Extract Superclass** - Pull up common behavior
- **Replace Type Code with Class** - Use objects not constants
- **Replace Conditional with Strategy** - Pluggable behavior
- **Form Template Method** - Define algorithm skeleton
- **Replace Constructor with Factory** - Flexible object creation

## Refactoring Workflow

### Step 1: Identify Refactoring Opportunity

Recognize code that needs improvement:

**Questions to ask:**
- Is this function/method too long? (>20-30 lines)
- Does this class have too many responsibilities?
- Is this code duplicated elsewhere?
- Are these names clear and descriptive?
- Is this logic overly complex?
- Would a design pattern help here?

**Example identification:**
```python
# Long method doing multiple things
def process_user_order(user_id, items, payment_info, shipping_address):  # 150 lines!
    # Validate user
    # Validate items
    # Calculate prices
    # Apply discounts
    # Process payment
    # Update inventory
    # Create shipment
    # Send emails
    # Update analytics
    # ...

# Opportunity: Extract Method refactoring
# This should be broken into focused functions
```

### Step 2: Choose Appropriate Refactoring

Select the right transformation:

**Refactoring catalog:**

| Code Smell | Refactoring Solution |
|------------|---------------------|
| Long Method | Extract Method, Replace Temp with Query |
| Large Class | Extract Class, Extract Subclass |
| Long Parameter List | Introduce Parameter Object, Preserve Whole Object |
| Duplicate Code | Extract Method, Pull Up Method, Form Template Method |
| Complex Conditional | Decompose Conditional, Replace Conditional with Polymorphism |
| Primitive Obsession | Replace Type Code with Class, Introduce Value Object |
| Feature Envy | Move Method, Extract Method |
| Data Clumps | Extract Class, Introduce Parameter Object |

**Example selection:**
```python
# Problem: Long Parameter List
def create_user(first_name, last_name, email, phone, street, city, state, zip_code, country):
    pass

# Solution: Introduce Parameter Object
# Create Address and User classes to group related data
```

### Step 3: Plan the Refactoring

Ensure safe transformation:

**Pre-refactoring checklist:**
- [ ] Code is under version control
- [ ] Tests exist and pass
- [ ] Understand current behavior completely
- [ ] Identify all callers/dependencies
- [ ] Plan small, incremental steps
- [ ] Know how to verify correctness

**Refactoring plan example:**
```markdown
Refactoring: Extract Class for Address information

Current state:
- User class has 8 address-related fields
- Address logic scattered across User methods

Steps:
1. Create new Address class
2. Add address fields to Address
3. Add Address field to User
4. Update User constructor to accept Address
5. Update all address-related methods
6. Run tests after each step
7. Remove old address fields from User

Risk: Medium (many callers to update)
Estimated time: 1-2 hours
```

### Step 4: Apply Refactoring Incrementally

Make changes in small, safe steps:

**Guidelines:**
- Make one change at a time
- Run tests after each step
- Commit after each successful refactoring
- If tests fail, revert and try smaller steps
- Keep working code compiling/running

**Example incremental approach:**
```python
# Step 1: Extract method (just one piece)
def process_order(order):
    # Before: All inline
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    # ... rest of function

# Step 1a: Extract just the calculation
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total

def process_order(order):
    total = calculate_total(order.items)
    # ... rest of function

# Run tests → Pass → Commit

# Step 2: Extract next piece (validation)
# Step 3: Extract next piece (payment)
# etc.
```

### Step 5: Verify and Document

Confirm behavior preservation:

**Verification steps:**
1. All existing tests pass
2. No new warnings or errors
3. Code review for correctness
4. Manual testing of critical paths
5. Performance not degraded

**Documentation:**
```python
# Document the refactoring in commit message
"""
Refactor: Extract Address class from User

- Created Address value object with street, city, state, zip
- Moved address validation to Address class
- Updated User to use Address instead of separate fields
- All tests passing, behavior unchanged

Benefits:
- Address logic now centralized
- Easier to add address validation
- Can reuse Address in Order, Shipping, etc.
"""
```

## Common Refactoring Patterns

### Pattern 1: Extract Method

**Before:**
```python
def print_owing(invoice):
    print_banner()

    # Print details
    print(f"name: {invoice.customer}")
    print(f"amount: {invoice.amount}")

    # Calculate outstanding
    outstanding = 0
    for order in invoice.orders:
        outstanding += order.amount
    print(f"outstanding: {outstanding}")
```

**After:**
```python
def print_owing(invoice):
    print_banner()
    print_details(invoice)
    print_outstanding(invoice)

def print_details(invoice):
    print(f"name: {invoice.customer}")
    print(f"amount: {invoice.amount}")

def print_outstanding(invoice):
    outstanding = calculate_outstanding(invoice)
    print(f"outstanding: {outstanding}")

def calculate_outstanding(invoice):
    return sum(order.amount for order in invoice.orders)
```

**Benefits:**
- Each function has single purpose
- Easier to understand and test
- More reusable components
- Better naming reveals intent

**When to use:**
- Function is too long (>20-30 lines)
- Code needs commenting to explain what it does
- Difficult to understand at a glance
- Want to reuse part of function elsewhere

### Pattern 2: Introduce Parameter Object

**Before:**
```python
def calculate_shipping(street, city, state, zip_code, country, weight, dimensions):
    # Too many parameters!
    pass

def validate_address(street, city, state, zip_code, country):
    # Same address params repeated
    pass

def format_label(name, street, city, state, zip_code, country):
    # Same address params again
    pass
```

**After:**
```python
class Address:
    def __init__(self, street, city, state, zip_code, country):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def validate(self):
        # Validation logic here
        pass

    def format_label(self, name):
        return f"{name}\n{self.street}\n{self.city}, {self.state} {self.zip_code}"

class Package:
    def __init__(self, weight, dimensions):
        self.weight = weight
        self.dimensions = dimensions

def calculate_shipping(address, package):
    address.validate()
    # Cleaner signature
    pass
```

**Benefits:**
- Fewer parameters (easier to call)
- Related data grouped together
- Can add behavior to parameter objects
- Easier to extend (add new address fields)

**When to use:**
- Functions have 3+ parameters that belong together
- Same group of parameters appears in multiple functions
- Parameters represent a concept (Address, Date Range, etc.)

### Pattern 3: Replace Conditional with Polymorphism

**Before:**
```python
class Employee:
    def __init__(self, name, employee_type):
        self.name = name
        self.type = employee_type  # "engineer", "manager", "salesperson"

    def calculate_pay(self):
        if self.type == "engineer":
            return self.base_salary + self.bonus
        elif self.type == "manager":
            return self.base_salary + (self.num_reports * 1000)
        elif self.type == "salesperson":
            return self.base_salary + (self.sales * 0.1)
        else:
            return self.base_salary

    def get_benefits(self):
        if self.type == "engineer":
            return ["health", "dental", "vision", "401k"]
        elif self.type == "manager":
            return ["health", "dental", "vision", "401k", "stock_options"]
        elif self.type == "salesperson":
            return ["health", "dental", "commission"]
        else:
            return ["health"]
```

**After:**
```python
class Employee:
    def __init__(self, name):
        self.name = name
        self.base_salary = 50000

    def calculate_pay(self):
        return self.base_salary

    def get_benefits(self):
        return ["health"]

class Engineer(Employee):
    def __init__(self, name, bonus=0):
        super().__init__(name)
        self.bonus = bonus

    def calculate_pay(self):
        return self.base_salary + self.bonus

    def get_benefits(self):
        return ["health", "dental", "vision", "401k"]

class Manager(Employee):
    def __init__(self, name, num_reports=0):
        super().__init__(name)
        self.num_reports = num_reports

    def calculate_pay(self):
        return self.base_salary + (self.num_reports * 1000)

    def get_benefits(self):
        return ["health", "dental", "vision", "401k", "stock_options"]

class Salesperson(Employee):
    def __init__(self, name, sales=0):
        super().__init__(name)
        self.sales = sales

    def calculate_pay(self):
        return self.base_salary + (self.sales * 0.1)

    def get_benefits(self):
        return ["health", "dental", "commission"]
```

**Benefits:**
- No complex conditionals
- Easy to add new employee types (just create new class)
- Each type's logic is isolated
- Follows Open/Closed Principle

**When to use:**
- Complex conditionals based on type code
- Same conditional pattern repeated multiple places
- Need to add new types frequently
- Different behavior for different types

### Pattern 4: Decompose Conditional

**Before:**
```python
def calculate_charge(customer, usage, date):
    if date.month < 6 or date.month > 8:
        # Winter rate
        if usage > 100:
            charge = usage * 0.15 + 10
        else:
            charge = usage * 0.12 + 5
    else:
        # Summer rate
        if usage > 150:
            charge = usage * 0.20 + 15
        else:
            charge = usage * 0.18 + 8

    if customer.is_premium:
        charge = charge * 0.9

    return charge
```

**After:**
```python
def calculate_charge(customer, usage, date):
    base_charge = get_base_charge(usage, date)
    return apply_customer_discount(base_charge, customer)

def get_base_charge(usage, date):
    if is_winter(date):
        return calculate_winter_charge(usage)
    else:
        return calculate_summer_charge(usage)

def is_winter(date):
    return date.month < 6 or date.month > 8

def calculate_winter_charge(usage):
    if usage > 100:
        return usage * 0.15 + 10
    else:
        return usage * 0.12 + 5

def calculate_summer_charge(usage):
    if usage > 150:
        return usage * 0.20 + 15
    else:
        return usage * 0.18 + 8

def apply_customer_discount(charge, customer):
    if customer.is_premium:
        return charge * 0.9
    return charge
```

**Benefits:**
- Each condition has descriptive name
- Logic broken into understandable pieces
- Easier to test each part
- Can reuse components

**When to use:**
- Complex nested conditionals
- Hard to understand what condition checks
- Multiple unrelated concerns in one conditional

### Pattern 5: Replace Magic Number with Named Constant

**Before:**
```python
def calculate_potential_energy(mass, height):
    return mass * 9.81 * height

def calculate_circumference(radius):
    return 2 * 3.14159 * radius

def is_valid_age(age):
    return 0 <= age <= 120

def apply_discount(price):
    if price > 100:
        return price * 0.9  # What discount is this?
    return price
```

**After:**
```python
# Constants at module level
GRAVITY = 9.81  # m/s²
PI = 3.14159
MIN_AGE = 0
MAX_AGE = 120
BULK_ORDER_THRESHOLD = 100
BULK_DISCOUNT_RATE = 0.10

def calculate_potential_energy(mass, height):
    return mass * GRAVITY * height

def calculate_circumference(radius):
    return 2 * PI * radius

def is_valid_age(age):
    return MIN_AGE <= age <= MAX_AGE

def apply_discount(price):
    if price > BULK_ORDER_THRESHOLD:
        return price * (1 - BULK_DISCOUNT_RATE)
    return price
```

**Benefits:**
- Clear meaning of numbers
- Easy to update (change in one place)
- Self-documenting code
- No more "what does 0.9 mean?" questions

**When to use:**
- Numbers with specific meaning (not 0, 1, -1)
- Same number used in multiple places
- Number represents business rule or constant
- Number's meaning not immediately obvious

### Pattern 6: Replace Nested Conditional with Guard Clauses

**Before:**
```python
def calculate_pay(employee):
    result = 0
    if employee.is_active:
        if employee.hours_worked > 0:
            if employee.hourly_rate > 0:
                result = employee.hours_worked * employee.hourly_rate
                if employee.is_overtime:
                    result = result * 1.5
            else:
                result = 0
        else:
            result = 0
    else:
        result = 0
    return result
```

**After:**
```python
def calculate_pay(employee):
    if not employee.is_active:
        return 0
    if employee.hours_worked <= 0:
        return 0
    if employee.hourly_rate <= 0:
        return 0

    base_pay = employee.hours_worked * employee.hourly_rate

    if employee.is_overtime:
        return base_pay * 1.5

    return base_pay
```

**Benefits:**
- Linear flow (easier to read)
- Exceptional cases handled early
- Main logic not buried in nesting
- Reduced cognitive load

**When to use:**
- Deep nesting (>2-3 levels)
- Checking preconditions before main logic
- Multiple failure conditions
- "Arrow" code (keeps indenting right)

### Pattern 7: Extract Class

**Before:**
```python
class Order:
    def __init__(self):
        self.items = []
        self.customer_name = ""
        self.customer_email = ""
        self.customer_phone = ""
        self.shipping_street = ""
        self.shipping_city = ""
        self.shipping_state = ""
        self.shipping_zip = ""
        self.billing_street = ""
        self.billing_city = ""
        self.billing_state = ""
        self.billing_zip = ""

    def validate_shipping_address(self):
        # Validation logic
        pass

    def validate_billing_address(self):
        # Validation logic
        pass

    def format_shipping_label(self):
        # Formatting logic
        pass

    def send_confirmation_email(self):
        # Email logic
        pass
```

**After:**
```python
class Address:
    def __init__(self, street, city, state, zip_code):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def validate(self):
        # Validation logic
        pass

    def format_label(self):
        return f"{self.street}\n{self.city}, {self.state} {self.zip_code}"

class Customer:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def send_email(self, subject, body):
        # Email logic
        pass

class Order:
    def __init__(self, customer, shipping_address, billing_address):
        self.items = []
        self.customer = customer
        self.shipping_address = shipping_address
        self.billing_address = billing_address

    def validate_addresses(self):
        self.shipping_address.validate()
        self.billing_address.validate()

    def send_confirmation(self):
        self.customer.send_email(
            "Order Confirmation",
            f"Your order will ship to:\n{self.shipping_address.format_label()}"
        )
```

**Benefits:**
- Clear separation of concerns
- Address and Customer are reusable
- Each class has focused responsibility
- Easier to test independently

**When to use:**
- Class has too many fields (>7-8)
- Subset of fields used together frequently
- Class has multiple responsibilities
- Want to reuse part of class functionality

### Pattern 8: Inline Method

**Before:**
```python
def get_rating(driver):
    return more_than_five_late_deliveries(driver) ? 2 : 1

def more_than_five_late_deliveries(driver):
    return driver.number_of_late_deliveries > 5
```

**After:**
```python
def get_rating(driver):
    return 2 if driver.number_of_late_deliveries > 5 else 1
```

**Benefits:**
- Less indirection
- Simpler code when method body is obvious
- Fewer functions to navigate

**When to use:**
- Method body is as clear as method name
- Method is only called from one place
- Method is too simple to justify extraction
- Removing unnecessary abstraction

### Pattern 9: Replace Loop with Pipeline

**Before:**
```python
def get_high_value_active_customers(customers):
    result = []
    for customer in customers:
        if customer.is_active:
            if customer.total_purchases > 1000:
                result.append(customer.name)
    result.sort()
    return result
```

**After:**
```python
def get_high_value_active_customers(customers):
    return sorted(
        customer.name
        for customer in customers
        if customer.is_active and customer.total_purchases > 1000
    )
```

**Benefits:**
- More declarative (what, not how)
- Concise and readable
- Easier to parallelize
- Functional style (no mutation)

**When to use:**
- Simple transformations/filtering
- No complex loop logic
- Language has good collection operations
- Team comfortable with functional style

### Pattern 10: Introduce Explaining Variable

**Before:**
```python
def calculate_price(order):
    return order.quantity * order.item_price - \
           max(0, order.quantity - 500) * order.item_price * 0.05 + \
           min(order.quantity * order.item_price * 0.1, 100)
```

**After:**
```python
def calculate_price(order):
    base_price = order.quantity * order.item_price
    quantity_discount = max(0, order.quantity - 500) * order.item_price * 0.05
    shipping = min(base_price * 0.1, 100)
    return base_price - quantity_discount + shipping
```

**Benefits:**
- Complex expressions broken down
- Named intermediate values
- Self-documenting
- Easier to debug

**When to use:**
- Long complex expressions
- Same subexpression used multiple times
- Expression meaning not immediately clear
- Debugging complex calculations

## Refactoring Safety Guidelines

### 1. Always Have Tests

```python
# Before refactoring, ensure tests exist
def test_calculate_total():
    order = Order(items=[
        Item(price=10, quantity=2),
        Item(price=5, quantity=3)
    ])
    assert calculate_total(order) == 35

# If tests don't exist, write them BEFORE refactoring
# This is your safety net
```

### 2. Make Small Steps

```python
# Bad: Trying to do too much at once
# - Extract 10 methods
# - Rename 20 variables
# - Move 5 classes
# - Change architecture
# All in one commit!

# Good: One refactoring at a time
# Commit 1: Extract calculate_total method
# Commit 2: Extract validate_order method
# Commit 3: Rename 'x' to 'total_price'
# Each commit: tests pass, code works
```

### 3. Preserve Behavior

```python
# Refactoring should NOT change behavior
# Only change structure, not functionality

# If you need to change behavior:
# 1. Refactor first (structure improvement)
# 2. THEN add new feature (behavior change)
# Don't mix them!
```

### 4. Use IDE Refactoring Tools

```python
# Many IDEs have safe, automated refactorings:
# - Rename (updates all references)
# - Extract Method (handles scope correctly)
# - Move Class/Method (updates imports)
# - Change Signature (updates callers)

# Use these instead of manual find-replace!
# They're safer and handle edge cases
```

### 5. Review Diff Before Committing

```bash
# Always review what changed
git diff

# Ask yourself:
# - Did I change only what I intended?
# - Are there unexpected changes?
# - Did I accidentally change behavior?
# - Are all tests still passing?
```

## Refactoring Anti-Patterns

### Anti-Pattern 1: Refactoring Without Tests

**Problem:**
```python
# No tests exist
def complex_business_logic():
    # 200 lines of critical code
    pass

# Start refactoring anyway
# Break something
# Don't notice until production
```

**Solution:**
```python
# First: Write characterization tests
def test_complex_business_logic_scenario_1():
    result = complex_business_logic(input1)
    assert result == expected1

def test_complex_business_logic_scenario_2():
    result = complex_business_logic(input2)
    assert result == expected2

# Now refactor safely with test coverage
```

### Anti-Pattern 2: Big Bang Refactoring

**Problem:**
```python
# Rewrite entire module at once
# Change everything
# Break everything
# Take weeks
# Can't merge back to main
```

**Solution:**
```python
# Incremental refactoring
# Week 1: Extract 3 methods, commit, deploy
# Week 2: Extract 3 more, commit, deploy
# Week 3: Introduce parameter object, commit, deploy
# Always working, always deployable
```

### Anti-Pattern 3: Premature Generalization

**Problem:**
```python
# Code is used in one place
# "But we MIGHT need it elsewhere!"
# Create abstract factory builder strategy pattern
# Never actually reused
# Just complex for no reason
```

**Solution:**
```python
# Rule of Three: Wait for 3rd use case
# 1st time: Write inline
# 2nd time: Note the duplication
# 3rd time: Now extract/generalize
# Don't abstract before you need it
```

### Anti-Pattern 4: Refactoring While Adding Features

**Problem:**
```python
# Pull request:
# - Adds new feature
# - Renames 50 variables
# - Extracts 10 methods
# - Moves 5 classes
# - Changes architecture
# Impossible to review what's actually new
```

**Solution:**
```python
# Separate commits:
# Commit 1: Refactor (structure only)
# Commit 2: Add feature (behavior change)
# Each commit easy to review and understand
```

## Best Practices

1. **Red-Green-Refactor** - Make tests pass first, then refactor
2. **Commit after each refactoring** - Small, reversible changes
3. **Keep it working** - Code should compile/run after each step
4. **Refactor regularly** - Don't wait for "refactoring sprint"
5. **Use IDE tools** - Automated refactorings are safer
6. **Boy Scout rule** - Leave code better than you found it
7. **Pair program** - Second set of eyes catches issues
8. **Code review** - Review refactorings like any other change
9. **Measure, don't guess** - Profile before optimizing
10. **Know when to stop** - Perfect is enemy of good

## Language-Specific Patterns

Different languages have different refactoring idioms:

**Python:**
- List comprehensions instead of loops
- Context managers for resource handling
- Decorators for cross-cutting concerns
- Duck typing over type checking

**JavaScript/TypeScript:**
- Arrow functions for callbacks
- Destructuring for parameter objects
- Async/await over callbacks
- Optional chaining for null safety

**Java:**
- Streams API for collections
- Optional for null handling
- Functional interfaces for strategies
- Records for value objects

**Go:**
- Table-driven tests
- Interfaces for abstractions
- Error handling patterns
- Goroutines for concurrency
