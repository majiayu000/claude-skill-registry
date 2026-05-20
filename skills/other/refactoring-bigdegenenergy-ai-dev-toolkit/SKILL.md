---
name: refactoring
description: Safe refactoring patterns and code improvement strategies. Auto-triggers when cleaning up code, reducing complexity, or improving maintainability.
---

# Refactoring Skill

## Golden Rules

1. **Never refactor without tests** - Tests are your safety net
2. **Small steps** - One change at a time, test after each
3. **Keep it working** - Code should pass tests at every step
4. **Commit often** - Easy to revert if something breaks

## Code Smells to Address

### Bloaters
| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Long Method | >20 lines | Extract Method |
| Large Class | >200 lines | Extract Class |
| Long Parameter List | >3 params | Introduce Parameter Object |
| Data Clumps | Same fields appear together | Extract Class |

### Object-Orientation Abusers
| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Switch Statements | Multiple type checks | Replace with Polymorphism |
| Parallel Inheritance | Every subclass needs partner | Merge Hierarchies |
| Refused Bequest | Subclass doesn't use parent | Replace Inheritance with Delegation |

### Change Preventers
| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Divergent Change | One class changed for multiple reasons | Extract Class |
| Shotgun Surgery | One change affects many classes | Move Method/Field |
| Feature Envy | Method uses other class's data | Move Method |

### Dispensables
| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Dead Code | Unused code | Delete |
| Duplicate Code | Same logic repeated | Extract Method |
| Speculative Generality | Unused abstraction | Collapse Hierarchy |
| Comments | Explaining bad code | Refactor until self-explanatory |

## Common Refactorings

### Extract Method
```python
# Before
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")
    # ... more validation ...

    # Calculate shipping
    shipping = 0
    if order.total > 100:
        shipping = 0
    elif order.weight < 1:
        shipping = 5
    else:
        shipping = 10
    # ... continue

# After
def process_order(order):
    validate_order(order)
    shipping = calculate_shipping(order)
    # ... continue

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def calculate_shipping(order):
    if order.total > 100:
        return 0
    elif order.weight < 1:
        return 5
    return 10
```

### Replace Conditional with Polymorphism
```python
# Before
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    elif shape.type == "triangle":
        return 0.5 * shape.base * shape.height

# After
class Shape:
    def area(self) -> float:
        raise NotImplementedError

class Circle(Shape):
    def area(self) -> float:
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def area(self) -> float:
        return self.width * self.height
```

### Introduce Parameter Object
```python
# Before
def create_user(name, email, phone, address, city, zip_code):
    ...

# After
@dataclass
class UserInfo:
    name: str
    email: str
    phone: str
    address: str
    city: str
    zip_code: str

def create_user(info: UserInfo):
    ...
```

## Refactoring Workflow

1. **Identify** the smell or improvement opportunity
2. **Write tests** if they don't exist
3. **Run tests** - ensure green baseline
4. **Make ONE change**
5. **Run tests** - must still be green
6. **Commit** with descriptive message
7. **Repeat** until complete

## Anti-Patterns in Refactoring

- Big bang rewrites (do incremental changes instead)
- Refactoring and adding features simultaneously
- Skipping the test run between changes
- Refactoring without understanding the code
- Over-abstracting before patterns emerge
