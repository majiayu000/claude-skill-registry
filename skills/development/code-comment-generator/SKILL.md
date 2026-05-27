---
name: code-comment-generator
description: Generates meaningful comments and documentation for code to improve maintenance and readability. Use when adding documentation to Python or Java code, including function/method docstrings, class documentation, inline explanations for complex logic, and code annotations (TODO, FIXME). Analyzes existing comment style in the codebase to match conventions. Produces clear, concise comments that explain the "why" not just the "what", following best practices for each language.
---

# Code Comment Generator

Generate meaningful, maintainable comments and documentation for your code.

## Core Capabilities

This skill helps you create effective code documentation by:

1. **Analyzing code context** - Understanding what the code does and why
2. **Matching existing style** - Following comment conventions in your codebase
3. **Writing clear documentation** - Creating function/method/class documentation
4. **Adding inline explanations** - Explaining complex logic and algorithms
5. **Inserting code annotations** - Adding TODO, FIXME, and optimization notes

## Comment Generation Workflow

### Step 1: Analyze Existing Comment Style

Before generating comments, examine the codebase to match style:

**Look for:**
- Documentation format (docstrings, Javadoc, etc.)
- Comment verbosity level (detailed vs. concise)
- Naming conventions and terminology
- Use of examples in documentation
- Type annotation style

**Python Example - Analyze Existing Style:**

```python
# If existing code uses this pattern:
def get_user(user_id: int) -> User:
    """
    Retrieve user by ID.

    Args:
        user_id: Unique identifier for the user

    Returns:
        User object if found

    Raises:
        UserNotFoundError: If user doesn't exist
    """
    return db.query(User).get(user_id)
```

**Style Identified:**
- Google-style docstrings
- Type hints in signature
- Concise summary line
- Args/Returns/Raises sections
- No examples included

**Java Example - Analyze Existing Style:**

```java
// If existing code uses this pattern:
/**
 * Retrieves a user by their unique identifier.
 *
 * @param userId the unique identifier for the user
 * @return the User object if found
 * @throws UserNotFoundException if no user exists with the given ID
 */
public User getUser(int userId) throws UserNotFoundException {
    return database.findUser(userId);
}
```

**Style Identified:**
- Standard Javadoc format
- Brief summary sentence
- @param, @return, @throws tags
- Formal tone
- No code examples

### Step 2: Understand the Code

Analyze the code to understand what to document:

**For Functions/Methods:**
- What does it do? (purpose)
- Why does it exist? (intent)
- What are the parameters?
- What does it return?
- What exceptions/errors can it raise?
- Are there side effects?
- Are there important preconditions or postconditions?

**For Classes:**
- What is the class responsible for?
- What design pattern does it implement?
- How should it be used?
- What are the key methods?
- Are there usage examples needed?

**For Complex Logic:**
- What algorithm is being used?
- Why this approach vs. alternatives?
- What are the edge cases?
- Are there performance considerations?

### Step 3: Write Function/Method Documentation

Generate documentation that explains purpose and usage.

**Python Example:**

```python
# Before (no comments)
def calculate_shipping_cost(items, destination, method):
    base = sum(item.weight * 0.5 for item in items)
    if destination.international:
        base *= 1.5
    if method == 'express':
        base *= 2
    return base + 5

# After (with documentation)
def calculate_shipping_cost(items: List[Item], destination: Address, method: str) -> float:
    """
    Calculate total shipping cost based on items, destination, and shipping method.

    The base cost is calculated from item weights ($0.50 per unit). International
    shipping adds a 50% surcharge, and express shipping doubles the cost. A flat
    $5 handling fee is added to all orders.

    Args:
        items: List of items to ship, each with a weight attribute
        destination: Shipping address with international flag
        method: Shipping method ('standard' or 'express')

    Returns:
        Total shipping cost in USD

    Example:
        >>> items = [Item(weight=2), Item(weight=3)]
        >>> addr = Address(country='USA', international=False)
        >>> calculate_shipping_cost(items, addr, 'standard')
        7.5
    """
    # Calculate base cost from item weights
    base = sum(item.weight * 0.5 for item in items)

    # Apply international surcharge if applicable
    if destination.international:
        base *= 1.5

    # Double cost for express shipping
    if method == 'express':
        base *= 2

    # Add handling fee
    return base + 5
```

**Java Example:**

```java
// Before (no comments)
public double calculateShippingCost(List<Item> items, Address destination, String method) {
    double base = items.stream()
        .mapToDouble(item -> item.getWeight() * 0.5)
        .sum();
    if (destination.isInternational()) {
        base *= 1.5;
    }
    if ("express".equals(method)) {
        base *= 2;
    }
    return base + 5;
}

// After (with documentation)
/**
 * Calculates the total shipping cost based on items, destination, and shipping method.
 *
 * <p>The base cost is calculated from item weights ($0.50 per unit). International
 * shipping adds a 50% surcharge, and express shipping doubles the cost. A flat
 * $5 handling fee is added to all orders.
 *
 * @param items the list of items to ship, each with a weight
 * @param destination the shipping address with international flag
 * @param method the shipping method ("standard" or "express")
 * @return the total shipping cost in USD
 * @throws IllegalArgumentException if method is not "standard" or "express"
 */
public double calculateShippingCost(List<Item> items, Address destination, String method) {
    // Calculate base cost from item weights ($0.50 per unit)
    double base = items.stream()
        .mapToDouble(item -> item.getWeight() * 0.5)
        .sum();

    // Apply 50% surcharge for international shipping
    if (destination.isInternational()) {
        base *= 1.5;
    }

    // Double the cost for express shipping
    if ("express".equals(method)) {
        base *= 2;
    }

    // Add $5 handling fee
    return base + 5;
}
```

### Step 4: Add Inline Explanations

Add comments for complex or non-obvious code sections.

**When to Add Inline Comments:**
- Complex algorithms or formulas
- Non-obvious business logic
- Workarounds or hacks
- Performance optimizations
- Edge case handling
- Regex patterns
- Bit manipulation
- Magic numbers

**When NOT to Add Inline Comments:**
- Obvious code (e.g., `// increment counter` for `i++`)
- Repeating what code already says
- Outdated comments that don't match code

**Python Example:**

```python
def find_median(numbers):
    """Find the median value in a list of numbers."""
    # Sort is required for median calculation - O(n log n)
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)

    # For even-length lists, median is average of two middle elements
    if n % 2 == 0:
        mid1 = sorted_nums[n // 2 - 1]
        mid2 = sorted_nums[n // 2]
        return (mid1 + mid2) / 2
    # For odd-length lists, median is the middle element
    else:
        return sorted_nums[n // 2]


def validate_email(email):
    """Validate email format using RFC 5322 simplified pattern."""
    # Regex breakdown:
    # ^[a-zA-Z0-9._%+-]+ - local part (before @)
    # @ - literal @ symbol
    # [a-zA-Z0-9.-]+ - domain name
    # \.[a-zA-Z]{2,}$ - top-level domain (at least 2 chars)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def calculate_discount(price, quantity):
    """Calculate bulk discount for quantity purchases."""
    # Bulk discount tiers (from business requirements doc v3.2)
    # 10+ items: 5% off
    # 50+ items: 10% off
    # 100+ items: 15% off
    if quantity >= 100:
        discount = 0.15
    elif quantity >= 50:
        discount = 0.10
    elif quantity >= 10:
        discount = 0.05
    else:
        discount = 0

    return price * quantity * (1 - discount)
```

**Java Example:**

```java
public int findMedian(int[] numbers) {
    // Sort array in-place - required for median calculation
    Arrays.sort(numbers);
    int n = numbers.length;

    // For even-length arrays, return average of two middle elements
    if (n % 2 == 0) {
        return (numbers[n/2 - 1] + numbers[n/2]) / 2;
    }
    // For odd-length arrays, return middle element
    return numbers[n/2];
}

public boolean validateEmail(String email) {
    // Use RFC 5322 simplified pattern for email validation
    // Pattern breakdown:
    // ^[\\w.%-]+ - local part (letters, digits, dots, %, -)
    // @ - literal @ symbol
    // [\\w.-]+ - domain name
    // \\.[a-zA-Z]{2,}$ - TLD (minimum 2 characters)
    String pattern = "^[\\w.%-]+@[\\w.-]+\\.[a-zA-Z]{2,}$";
    return email.matches(pattern);
}

public double calculateDiscount(double price, int quantity) {
    double discount;

    // Bulk discount tiers (from business requirements doc v3.2)
    // These thresholds were set by the sales team in Q4 2023
    if (quantity >= 100) {
        discount = 0.15;  // 15% off for 100+ items
    } else if (quantity >= 50) {
        discount = 0.10;  // 10% off for 50-99 items
    } else if (quantity >= 10) {
        discount = 0.05;  // 5% off for 10-49 items
    } else {
        discount = 0;     // No discount for less than 10
    }

    return price * quantity * (1 - discount);
}
```

### Step 5: Document Classes and Modules

Provide high-level documentation for classes and modules.

**Python Example:**

```python
class ShoppingCart:
    """
    Shopping cart for e-commerce checkout process.

    Manages items, quantities, and pricing calculations. Supports discount
    codes, tax calculation, and shipping cost estimation. Cart state is
    persisted to the session.

    Attributes:
        items: Dictionary mapping product IDs to CartItem objects
        discount_code: Optional discount code applied to cart
        user_id: ID of the user who owns this cart

    Example:
        >>> cart = ShoppingCart(user_id=123)
        >>> cart.add_item(product_id=456, quantity=2)
        >>> cart.apply_discount("SAVE10")
        >>> cart.get_total()
        89.99
    """

    def __init__(self, user_id: int):
        """
        Initialize a new shopping cart for a user.

        Args:
            user_id: The ID of the user who owns this cart
        """
        self.items = {}
        self.discount_code = None
        self.user_id = user_id
```

**Java Example:**

```java
/**
 * Shopping cart for e-commerce checkout process.
 *
 * <p>Manages items, quantities, and pricing calculations. Supports discount
 * codes, tax calculation, and shipping cost estimation. Cart state can be
 * persisted to the database.
 *
 * <p>This class is thread-safe for concurrent access by multiple requests
 * from the same user session.
 *
 * <h3>Usage Example:</h3>
 * <pre>{@code
 * ShoppingCart cart = new ShoppingCart(userId);
 * cart.addItem(productId, 2);
 * cart.applyDiscount("SAVE10");
 * double total = cart.getTotal();
 * }</pre>
 *
 * @author Engineering Team
 * @since 2.0
 * @see Order
 * @see CartItem
 */
public class ShoppingCart {
    private Map<Integer, CartItem> items;
    private String discountCode;
    private int userId;

    /**
     * Constructs a new shopping cart for the specified user.
     *
     * @param userId the ID of the user who owns this cart
     */
    public ShoppingCart(int userId) {
        this.items = new HashMap<>();
        this.userId = userId;
    }
}
```

### Step 6: Add Code Annotations

Insert markers for future work, issues, and optimizations.

**Common Annotations:**

```python
# TODO: Add validation for negative quantities
def add_item(self, product_id, quantity):
    self.items[product_id] = quantity

# FIXME: This breaks when user is None - needs null check
def get_user_email(self, user):
    return user.email

# HACK: Workaround for database connection pool bug (#1234)
# Remove when upgrading to DB driver v2.0
def get_connection():
    time.sleep(0.1)  # Give pool time to refresh
    return pool.get_connection()

# OPTIMIZE: Consider caching this result - called frequently
def calculate_complex_metric(self):
    return sum(expensive_operation(x) for x in self.data)

# NOTE: This threshold was determined through A/B testing (see doc/experiments/cart-threshold.md)
MIN_ORDER_VALUE = 25.00

# DEPRECATED: Use get_user_by_id() instead - will be removed in v3.0
def fetch_user(self, user_id):
    warnings.warn("fetch_user is deprecated", DeprecationWarning)
    return self.get_user_by_id(user_id)
```

**Java Example:**

```java
// TODO: Add validation for null products
public void addItem(Product product, int quantity) {
    items.put(product.getId(), new CartItem(product, quantity));
}

// FIXME: Throws NullPointerException when user has no email set
// See issue #456
public String getUserEmail(User user) {
    return user.getEmail();
}

// HACK: Workaround for connection pool bug in DB driver v1.5
// Remove this sleep when we upgrade to v2.0
private Connection getConnection() throws SQLException {
    Thread.sleep(100);  // Give pool time to refresh
    return pool.getConnection();
}

// OPTIMIZE: Cache this calculation - it's expensive and called frequently
// Consider memoization or storing result in database
private double calculateComplexMetric() {
    return data.stream()
        .map(this::expensiveOperation)
        .reduce(0.0, Double::sum);
}

/**
 * @deprecated Use {@link #getUserById(int)} instead. This method will be
 *             removed in version 3.0.
 */
@Deprecated
public User fetchUser(int userId) {
    return getUserById(userId);
}
```

## Comment Quality Guidelines

### Do: Explain WHY, not WHAT

```python
# Bad - states the obvious
# Loop through users
for user in users:
    send_email(user)

# Good - explains the reason
# Send reminder emails to users who haven't logged in within 30 days
for user in inactive_users:
    send_reminder_email(user)
```

### Do: Add Context and Intent

```python
# Bad - no context
MAX_RETRIES = 3

# Good - explains the reasoning
# Retry up to 3 times to handle transient network errors
# Based on 99.9% success rate observed in production logs
MAX_RETRIES = 3
```

### Do: Document Assumptions

```python
# Good - documents assumptions
def process_payment(amount):
    """
    Process payment transaction.

    Assumes:
    - Amount is in USD
    - User has already been authenticated
    - Payment method has been validated
    """
```

### Don't: State the Obvious

```python
# Bad - comment adds no value
# Increment counter
counter += 1

# Set name to "Alice"
name = "Alice"

# Return true
return True
```

### Don't: Write Outdated Comments

```python
# Bad - comment doesn't match code
# Return the user's age
return user.birth_date  # Oops, this returns birth_date not age!

# Good - keep comments in sync with code
# Return the user's birth date
return user.birth_date
```

### Don't: Comment Bad Code Instead of Fixing It

```python
# Bad - explaining messy code
# This is complicated because we need to handle edge cases
if (x > 0 and y < 10 and (z == 5 or z == 7) and not flag) or (x < 0 and special):
    do_something()

# Good - refactor and simplify
def should_do_something(x, y, z, flag, special):
    """Check if conditions are met to perform action."""
    normal_case = x > 0 and y < 10 and z in [5, 7] and not flag
    special_case = x < 0 and special
    return normal_case or special_case

if should_do_something(x, y, z, flag, special):
    do_something()
```

## Language-Specific Guidelines

### Python

**Docstring Format:** Use Google-style or NumPy-style docstrings

```python
def function(arg1: str, arg2: int) -> bool:
    """
    Brief one-line summary.

    More detailed explanation if needed. Can span multiple
    lines and paragraphs.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input provided

    Example:
        >>> function("test", 42)
        True
    """
```

**Use Type Hints:** Reduce need for comments

```python
# Less clear - needs comment
def get_users(active):
    """Get users. active parameter filters active users."""

# More clear - type hints make it obvious
def get_users(active: bool) -> List[User]:
    """Get all users, optionally filtered by active status."""
```

### Java

**Javadoc Format:** Standard tags

```java
/**
 * Brief one-line summary.
 *
 * <p>More detailed explanation if needed. Use paragraph tags
 * for multi-paragraph descriptions.
 *
 * @param arg1 description of arg1
 * @param arg2 description of arg2
 * @return description of return value
 * @throws IllegalArgumentException when invalid input provided
 * @see RelatedClass
 * @since 1.5
 */
```

**Use @see and @link:**

```java
/**
 * Processes the order and updates inventory.
 *
 * @param order the order to process
 * @return the processed order
 * @see Order
 * @see InventoryService#updateStock(int, int)
 */
```

## Resources

- **`references/comment_examples.md`** - Comprehensive examples of well-commented code for various scenarios (algorithms, API clients, data processing, etc.)
- **`references/style_guides.md`** - Language-specific comment style guides and conventions

## Best Practices Summary

1. **Explain WHY, not WHAT** - Focus on intent and reasoning
2. **Keep comments up-to-date** - Update comments when code changes
3. **Be concise** - Short, clear comments are better than verbose ones
4. **Use consistent style** - Match existing conventions in codebase
5. **Document public APIs** - All public functions/classes need documentation
6. **Add context** - Explain business rules, assumptions, edge cases
7. **Use meaningful names** - Good names reduce need for comments
8. **Annotate TODOs** - Mark future work and technical debt
9. **Avoid redundancy** - Don't repeat what code already says clearly
10. **Write for maintainers** - Help future developers (including yourself)
