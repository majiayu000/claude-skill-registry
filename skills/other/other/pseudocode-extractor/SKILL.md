---
name: pseudocode-extractor
description: Extract programming-language-agnostic pseudocode from source code in any language, preserving control flow and logical structure while filtering out implementation details. Use when the user asks to convert code to pseudocode, abstract code logic, understand code structure without syntax, create language-independent documentation, or analyze algorithmic flow without language-specific details.
---

# Pseudocode Extractor

## Overview

Transform source code from any programming language into clear, language-agnostic pseudocode that captures the essential logic and control flow while removing syntax-specific details.

## Extraction Process

### 1. Analyze Input Code

First, identify the programming language and understand the code structure:
- Recognize functions, classes, methods, and modules
- Identify control flow structures (loops, conditionals, error handling)
- Note data structures and their relationships
- Understand the overall algorithmic approach

### 2. Extract Core Logic

Focus on WHAT the code does, not HOW it's implemented:

**Preserve:**
- Function/method names and their purpose
- Control flow (if/else, loops, switch/case logic)
- Logical operations and conditions
- Data transformations and assignments
- Function calls and their relationships
- Class structures and inheritance relationships
- Key variable names that convey meaning

**Filter out:**
- Language-specific syntax (semicolons, braces, keywords)
- Type declarations and annotations
- Import/include statements (unless critical to understanding)
- Error handling boilerplate (try/catch unless the logic is important)
- Memory management details
- Language-specific idioms
- Verbose getter/setter methods
- Standard library implementation details

### 3. Format Pseudocode

Use clear, readable pseudocode conventions:

**Structure:**
```
FUNCTION function_name(parameters)
    // High-level description of what function does

    IF condition THEN
        action
    ELSE IF another_condition THEN
        another_action
    ELSE
        default_action
    END IF

    FOR EACH item IN collection DO
        process item
    END FOR

    WHILE condition DO
        action
    END WHILE

    RETURN result
END FUNCTION
```

**Conventions:**
- Use UPPERCASE for keywords (FUNCTION, IF, FOR, WHILE, RETURN, etc.)
- Use descriptive names in lowercase or camelCase
- Indent to show nesting and structure
- Use comments to explain complex logic
- Keep operations at a high level of abstraction
- Use mathematical notation where appropriate (←, ≠, ≤, etc.)

### 4. Organize Output

Structure the pseudocode to match the original code organization:

**For single functions:**
- Start with function signature
- Add brief description
- Show main logic flow
- Note return value

**For classes:**
- Show class name and inheritance
- List key attributes
- Show method signatures with brief descriptions
- Detail only the most important methods

**For modules/files:**
- Group related functions
- Show high-level module structure
- Indicate dependencies between components
- Use section headers for clarity

## Examples

### Example 1: Simple Function

**Input (Python):**
```python
def calculate_discount(price, customer_type):
    if customer_type == "premium":
        discount = 0.20
    elif customer_type == "regular":
        discount = 0.10
    else:
        discount = 0.05

    final_price = price * (1 - discount)
    return round(final_price, 2)
```

**Output (Pseudocode):**
```
FUNCTION calculate_discount(price, customer_type)
    // Calculate final price after applying customer-specific discount

    IF customer_type is "premium" THEN
        discount ← 20%
    ELSE IF customer_type is "regular" THEN
        discount ← 10%
    ELSE
        discount ← 5%
    END IF

    final_price ← price × (1 - discount)

    RETURN final_price rounded to 2 decimals
END FUNCTION
```

### Example 2: Loop with Data Processing

**Input (JavaScript):**
```javascript
function filterActiveUsers(users) {
    const activeUsers = [];
    for (let i = 0; i < users.length; i++) {
        if (users[i].lastLogin !== null &&
            users[i].status === 'active') {
            activeUsers.push({
                id: users[i].id,
                name: users[i].name
            });
        }
    }
    return activeUsers;
}
```

**Output (Pseudocode):**
```
FUNCTION filter_active_users(users)
    // Extract active users who have logged in at least once

    active_users ← empty list

    FOR EACH user IN users DO
        IF user has logged in AND user status is "active" THEN
            ADD user.id and user.name to active_users
        END IF
    END FOR

    RETURN active_users
END FUNCTION
```

### Example 3: Class Structure

**Input (Java):**
```java
public class ShoppingCart {
    private List<Item> items;
    private double totalPrice;

    public ShoppingCart() {
        this.items = new ArrayList<>();
        this.totalPrice = 0.0;
    }

    public void addItem(Item item) {
        items.add(item);
        totalPrice += item.getPrice();
    }

    public void removeItem(String itemId) {
        for (int i = 0; i < items.size(); i++) {
            if (items.get(i).getId().equals(itemId)) {
                totalPrice -= items.get(i).getPrice();
                items.remove(i);
                break;
            }
        }
    }

    public double getTotalPrice() {
        return totalPrice;
    }
}
```

**Output (Pseudocode):**
```
CLASS ShoppingCart
    ATTRIBUTES:
        items: list of Item objects
        total_price: numeric value

    CONSTRUCTOR
        Initialize empty items list
        Set total_price to 0
    END CONSTRUCTOR

    METHOD add_item(item)
        Add item to items list
        Increase total_price by item price
    END METHOD

    METHOD remove_item(item_id)
        FOR EACH item IN items DO
            IF item.id equals item_id THEN
                Decrease total_price by item price
                Remove item from items list
                EXIT loop
            END IF
        END FOR
    END METHOD

    METHOD get_total_price()
        RETURN total_price
    END METHOD
END CLASS
```

## Best Practices

1. **Maintain Clarity**: Pseudocode should be easier to understand than the original code
2. **Be Consistent**: Use the same conventions throughout the extraction
3. **Preserve Intent**: Focus on the algorithm's purpose, not implementation details
4. **Use Natural Language**: Write operations in plain English where possible
5. **Show Structure**: Use indentation and keywords to make control flow obvious
6. **Add Context**: Include brief comments for complex logic
7. **Stay Abstract**: Avoid language-specific constructs unless they're conceptually important
8. **Group Related Logic**: Keep related operations together for readability

## Common Patterns

### Conditional Logic
```
IF condition THEN
    action
ELSE IF another_condition THEN
    another_action
ELSE
    default_action
END IF
```

### Loops
```
FOR i FROM 1 TO n DO
    action
END FOR

FOR EACH element IN collection DO
    process element
END FOR

WHILE condition DO
    action
END WHILE

REPEAT
    action
UNTIL condition
```

### Data Operations
```
// Assignment
variable ← value

// Comparison
IF x > y THEN ...
IF x ≠ y THEN ...

// Collections
ADD item TO list
REMOVE item FROM list
FIND item IN list WHERE condition
```

### Function Calls
```
result ← function_name(arguments)
CALL procedure_name(arguments)
```
