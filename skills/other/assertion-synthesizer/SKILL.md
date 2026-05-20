---
name: assertion-synthesizer
description: Generate test assertions from existing code implementation. Use when the user has implementation code without tests or incomplete test coverage, and needs assertions synthesized by analyzing the code's behavior, inputs, outputs, and state changes. Supports Python (pytest/unittest), Java (JUnit/AssertJ), and JavaScript/TypeScript (Jest/Chai). Handles equality checks, collections, exceptions, and state verification.
---

# Assertion Synthesizer

Generate comprehensive test assertions by analyzing code implementation, behavior, and expected outputs.

## Workflow

### 1. Analyze Code

Read and understand the implementation to identify testable behavior:

- **Function signatures**: Parameters, return types, side effects
- **Logic paths**: Conditionals, loops, branching behavior
- **Edge cases**: Boundary conditions, null/empty inputs, error conditions
- **State changes**: Object mutations, attribute modifications
- **Dependencies**: External calls, database operations, I/O

### 2. Identify Test Scenarios

Extract scenarios that need assertions:

- **Happy path**: Normal inputs producing expected outputs
- **Edge cases**: Empty lists, zero values, boundary conditions
- **Error cases**: Invalid inputs, exceptions, error handling
- **State verification**: Object state before/after operations
- **Collection assertions**: List contents, ordering, membership

### 3. Generate Assertions

Create appropriate assertions for each scenario:

**Assertion Types:**
- **Equality**: `assert result == expected`, `assertEquals(expected, actual)`
- **Truthiness**: `assert is_valid`, `assertTrue(condition)`
- **Collections**: `assert item in list`, `assertContains(list, item)`
- **Exceptions**: `pytest.raises(Exception)`, `assertThrows(Exception)`
- **State**: `assert obj.status == "active"`, `assertEquals("active", obj.getStatus())`

### 4. Structure Tests

Organize assertions into well-structured test functions:

- Use descriptive test names
- Follow Arrange-Act-Assert pattern
- Group related assertions
- Add explanatory comments

### 5. Verify Coverage

Ensure all important behaviors have assertions:

- Check all return values are tested
- Verify edge cases are covered
- Confirm error conditions are tested
- Validate state changes are asserted

## Language-Specific Patterns

### Python (pytest)

```python
def test_basic_equality():
    # Arrange
    calculator = Calculator()

    # Act
    result = calculator.add(2, 3)

    # Assert
    assert result == 5

def test_collection_membership():
    items = get_active_items()
    assert "item1" in items
    assert len(items) == 3

def test_exception_handling():
    with pytest.raises(ValueError, match="Invalid input"):
        process_data(None)

def test_state_change():
    user = User("Alice")
    user.activate()
    assert user.is_active == True
    assert user.status == "active"
```

### Python (unittest)

```python
def test_basic_equality(self):
    calculator = Calculator()
    result = calculator.add(2, 3)
    self.assertEqual(result, 5)

def test_collection_membership(self):
    items = get_active_items()
    self.assertIn("item1", items)
    self.assertEqual(len(items), 3)

def test_exception_handling(self):
    with self.assertRaises(ValueError):
        process_data(None)

def test_state_change(self):
    user = User("Alice")
    user.activate()
    self.assertTrue(user.is_active)
    self.assertEqual(user.status, "active")
```

### Java (JUnit + AssertJ)

```java
@Test
void testBasicEquality() {
    Calculator calculator = new Calculator();
    int result = calculator.add(2, 3);
    assertThat(result).isEqualTo(5);
}

@Test
void testCollectionMembership() {
    List<String> items = getActiveItems();
    assertThat(items).contains("item1");
    assertThat(items).hasSize(3);
}

@Test
void testExceptionHandling() {
    assertThatThrownBy(() -> processData(null))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Invalid input");
}

@Test
void testStateChange() {
    User user = new User("Alice");
    user.activate();
    assertThat(user.isActive()).isTrue();
    assertThat(user.getStatus()).isEqualTo("active");
}
```

### JavaScript/TypeScript (Jest)

```javascript
test('basic equality', () => {
    const calculator = new Calculator();
    const result = calculator.add(2, 3);
    expect(result).toBe(5);
});

test('collection membership', () => {
    const items = getActiveItems();
    expect(items).toContain('item1');
    expect(items).toHaveLength(3);
});

test('exception handling', () => {
    expect(() => processData(null))
        .toThrow('Invalid input');
});

test('state change', () => {
    const user = new User('Alice');
    user.activate();
    expect(user.isActive).toBe(true);
    expect(user.status).toBe('active');
});
```

## Assertion Synthesis Strategies

### From Return Values

Analyze what the function returns and assert on it:

```python
# Code:
def get_full_name(first, last):
    return f"{first} {last}"

# Synthesized assertion:
def test_get_full_name():
    result = get_full_name("John", "Doe")
    assert result == "John Doe"
    assert isinstance(result, str)
```

### From Side Effects

Identify state changes and mutations:

```python
# Code:
def withdraw(account, amount):
    if account.balance >= amount:
        account.balance -= amount
        return True
    return False

# Synthesized assertions:
def test_withdraw_success():
    account = Account(balance=100)
    result = withdraw(account, 50)
    assert result == True
    assert account.balance == 50

def test_withdraw_insufficient_funds():
    account = Account(balance=30)
    result = withdraw(account, 50)
    assert result == False
    assert account.balance == 30  # Balance unchanged
```

### From Conditional Logic

Test each branch:

```python
# Code:
def classify_age(age):
    if age < 0:
        raise ValueError("Invalid age")
    elif age < 18:
        return "minor"
    elif age < 65:
        return "adult"
    else:
        return "senior"

# Synthesized assertions:
def test_classify_age_invalid():
    with pytest.raises(ValueError):
        classify_age(-1)

def test_classify_age_minor():
    assert classify_age(10) == "minor"
    assert classify_age(17) == "minor"

def test_classify_age_adult():
    assert classify_age(18) == "adult"
    assert classify_age(64) == "adult"

def test_classify_age_senior():
    assert classify_age(65) == "senior"
    assert classify_age(100) == "senior"
```

### From Collections

Assert on collection properties:

```python
# Code:
def filter_active_users(users):
    return [u for u in users if u.is_active]

# Synthesized assertions:
def test_filter_active_users():
    users = [
        User("Alice", is_active=True),
        User("Bob", is_active=False),
        User("Charlie", is_active=True)
    ]
    result = filter_active_users(users)

    assert len(result) == 2
    assert all(u.is_active for u in result)
    assert result[0].name == "Alice"
    assert result[1].name == "Charlie"
```

### From Object State

Verify object properties:

```python
# Code:
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item, price):
        self.items.append(item)
        self.total += price

# Synthesized assertions:
def test_shopping_cart_add_item():
    cart = ShoppingCart()

    # Initial state
    assert cart.items == []
    assert cart.total == 0

    # After first item
    cart.add_item("book", 20)
    assert len(cart.items) == 1
    assert "book" in cart.items
    assert cart.total == 20

    # After second item
    cart.add_item("pen", 5)
    assert len(cart.items) == 2
    assert cart.total == 25
```

## Best Practices

### Assertion Quality
- **Be specific**: Prefer `assert result == 5` over `assert result > 0`
- **Test one thing**: Each test should verify one specific behavior
- **Use meaningful values**: Avoid magic numbers, use named constants
- **Check types**: Verify return types when relevant

### Coverage Completeness
- **All branches**: Test every if/else path
- **Boundary values**: Test min, max, zero, empty, null
- **Error cases**: Assert on exceptions and error messages
- **State transitions**: Verify before/after states

### Test Organization
- **Descriptive names**: `test_withdraw_insufficient_funds` not `test_case_2`
- **Arrange-Act-Assert**: Clear separation of setup, execution, verification
- **Group related tests**: Use test classes or describe blocks
- **Comment complex assertions**: Explain what's being verified

### Common Patterns

**Multiple assertions for comprehensive verification:**
```python
def test_user_registration():
    user = register_user("alice@example.com", "password123")

    # Verify all important properties
    assert user.email == "alice@example.com"
    assert user.is_active == False  # Not activated yet
    assert user.created_at is not None
    assert user.id is not None
    assert len(user.roles) == 1
    assert "user" in user.roles
```

**Parametrized tests for multiple inputs:**
```python
@pytest.mark.parametrize("input,expected", [
    (0, "zero"),
    (1, "one"),
    (5, "many"),
    (100, "many"),
])
def test_number_to_word(input, expected):
    assert number_to_word(input) == expected
```

## Example Sessions

### Example 1: Untested Function

**User provides code:**
```python
def calculate_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

**Synthesized assertions:**
```python
def test_calculate_discount_normal():
    assert calculate_discount(100, 10) == 90.0
    assert calculate_discount(50, 20) == 40.0

def test_calculate_discount_zero():
    assert calculate_discount(100, 0) == 100.0

def test_calculate_discount_full():
    assert calculate_discount(100, 100) == 0.0

def test_calculate_discount_invalid_negative():
    with pytest.raises(ValueError, match="between 0 and 100"):
        calculate_discount(100, -10)

def test_calculate_discount_invalid_over_100():
    with pytest.raises(ValueError, match="between 0 and 100"):
        calculate_discount(100, 150)
```

### Example 2: Enhancing Existing Tests

**User provides weak test:**
```python
def test_sort_list():
    result = sort_list([3, 1, 2])
    assert result  # Only checks if result exists
```

**Enhanced assertions:**
```python
def test_sort_list():
    result = sort_list([3, 1, 2])

    # Verify actual sorting behavior
    assert result == [1, 2, 3]
    assert len(result) == 3
    assert isinstance(result, list)

def test_sort_list_empty():
    assert sort_list([]) == []

def test_sort_list_already_sorted():
    assert sort_list([1, 2, 3]) == [1, 2, 3]

def test_sort_list_duplicates():
    assert sort_list([3, 1, 2, 1]) == [1, 1, 2, 3]
```

## Tips

### Analyzing Complex Code
- Break down complex functions into testable units
- Identify all execution paths through code
- Look for implicit assumptions to test
- Consider edge cases the code may not handle

### Capturing Behavior
- Run code mentally or actually execute it
- Note all observable outputs and state changes
- Document expected behavior in assertions
- Test both success and failure scenarios

### Balancing Coverage
- Prioritize critical paths over trivial code
- Don't over-assert on implementation details
- Focus on public API behavior
- Test the contract, not the implementation
