---
name: function-class-generator
description: Generate complete, production-ready functions and classes from formal specifications, design descriptions, type signatures, or natural language requirements. Use this skill when implementing APIs from specifications, creating data structures from schemas, building classes from UML diagrams, generating code from contracts, or translating design documents into code. Supports multiple programming languages and follows language-specific best practices.
---

# Function/Class Generator

Transform formal specifications, design descriptions, and requirements into complete, well-structured, production-ready code. Generates functions, classes, interfaces, and data structures with proper error handling, documentation, and tests.

## Core Capabilities

### 1. Specification Parsing

Understand specifications from multiple sources:
- **Type signatures** - Function signatures with input/output types
- **Formal specifications** - Pre/postconditions, invariants, contracts
- **API documentation** - OpenAPI, Swagger, JSON Schema
- **UML diagrams** - Class diagrams, sequence diagrams
- **Natural language** - Requirements and design descriptions
- **Interface definitions** - Protocol buffers, GraphQL schemas

### 2. Code Generation

Create complete implementations:
- **Functions** - Standalone functions with logic and validation
- **Classes** - Full class definitions with methods and properties
- **Interfaces/Protocols** - Abstract definitions and contracts
- **Data structures** - Custom types, enums, unions
- **Error handling** - Exceptions, error types, validation
- **Documentation** - Docstrings, comments, type hints

### 3. Best Practices Integration

Apply language-specific patterns:
- **Naming conventions** - Follow language standards
- **Type safety** - Use static typing where available
- **Error handling** - Appropriate exception handling
- **Documentation** - Clear docstrings and comments
- **Testing** - Generate unit tests alongside code
- **SOLID principles** - Single responsibility, open/closed, etc.

### 4. Validation and Testing

Ensure correctness:
- **Type checking** - Verify type correctness
- **Contract validation** - Check pre/postconditions
- **Unit tests** - Generate test cases
- **Edge cases** - Handle boundaries and exceptions
- **Examples** - Provide usage examples

## Code Generation Workflow

### Step 1: Parse Specification

Extract key information:

**From type signature:**
```python
# Specification
def calculate_discount(price: float, percentage: float) -> float:
    """Calculate discounted price."""
    pass
```

**Extract:**
- Function name: `calculate_discount`
- Parameters: `price` (float), `percentage` (float)
- Return type: `float`
- Purpose: Calculate discounted price

**From formal specification:**
```
Function: binary_search
Inputs: sorted_array: List[int], target: int
Output: int (index of target, or -1 if not found)
Preconditions:
  - sorted_array is sorted in ascending order
  - sorted_array is not empty
Postconditions:
  - If result >= 0: sorted_array[result] == target
  - If result == -1: target not in sorted_array
```

### Step 2: Design Implementation

Plan the structure:

**Identify:**
- Main logic flow
- Edge cases to handle
- Validation needed
- Error conditions
- Helper functions required

**For binary_search example:**
- Main logic: Binary search algorithm
- Edge cases: Empty array, single element, target at boundaries
- Validation: Array must be sorted, index bounds
- Errors: Invalid input types, empty array
- Helpers: None needed (self-contained)

### Step 3: Generate Code

Create complete implementation:

**Generated code:**
```python
def binary_search(sorted_array: list[int], target: int) -> int:
    """
    Search for target in sorted array using binary search.

    Args:
        sorted_array: List of integers sorted in ascending order
        target: Integer value to search for

    Returns:
        Index of target if found, -1 otherwise

    Raises:
        ValueError: If sorted_array is empty
        TypeError: If inputs are not of correct type

    Examples:
        >>> binary_search([1, 2, 3, 4, 5], 3)
        2
        >>> binary_search([1, 2, 3, 4, 5], 6)
        -1

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    if not isinstance(sorted_array, list):
        raise TypeError("sorted_array must be a list")
    if not isinstance(target, int):
        raise TypeError("target must be an integer")
    if not sorted_array:
        raise ValueError("sorted_array cannot be empty")

    left, right = 0, len(sorted_array) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow

        if sorted_array[mid] == target:
            return mid
        elif sorted_array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

### Step 4: Add Documentation

Include comprehensive documentation:

**Elements:**
- Docstring with description
- Parameter descriptions
- Return value description
- Exceptions raised
- Usage examples
- Complexity analysis
- Precondition/postcondition notes

### Step 5: Generate Tests

Create validation tests:

```python
import pytest

def test_binary_search_found():
    """Test finding an element in the middle."""
    assert binary_search([1, 2, 3, 4, 5], 3) == 2

def test_binary_search_not_found():
    """Test element not in array."""
    assert binary_search([1, 2, 3, 4, 5], 6) == -1

def test_binary_search_first_element():
    """Test finding first element."""
    assert binary_search([1, 2, 3, 4, 5], 1) == 0

def test_binary_search_last_element():
    """Test finding last element."""
    assert binary_search([1, 2, 3, 4, 5], 5) == 4

def test_binary_search_single_element_found():
    """Test single-element array with target present."""
    assert binary_search([1], 1) == 0

def test_binary_search_single_element_not_found():
    """Test single-element array with target absent."""
    assert binary_search([1], 2) == -1

def test_binary_search_empty_array():
    """Test that empty array raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        binary_search([], 1)

def test_binary_search_invalid_array_type():
    """Test that invalid array type raises TypeError."""
    with pytest.raises(TypeError, match="must be a list"):
        binary_search("not a list", 1)

def test_binary_search_invalid_target_type():
    """Test that invalid target type raises TypeError."""
    with pytest.raises(TypeError, match="must be an integer"):
        binary_search([1, 2, 3], "not an int")
```

## Generation Patterns

### Pattern 1: Function from Type Signature

**Specification:**
```typescript
function calculateArea(width: number, height: number): number
```

**Generated implementation:**
```typescript
/**
 * Calculate the area of a rectangle.
 *
 * @param width - Width of the rectangle (must be positive)
 * @param height - Height of the rectangle (must be positive)
 * @returns The calculated area (width * height)
 * @throws {Error} If width or height is not positive
 *
 * @example
 * ```typescript
 * calculateArea(5, 10) // returns 50
 * calculateArea(2.5, 4) // returns 10
 * ```
 */
function calculateArea(width: number, height: number): number {
  if (width <= 0) {
    throw new Error('Width must be positive');
  }
  if (height <= 0) {
    throw new Error('Height must be positive');
  }

  return width * height;
}
```

**Generated tests:**
```typescript
import { describe, it, expect } from '@jest/globals';

describe('calculateArea', () => {
  it('should calculate area correctly', () => {
    expect(calculateArea(5, 10)).toBe(50);
    expect(calculateArea(2.5, 4)).toBe(10);
  });

  it('should handle decimal values', () => {
    expect(calculateArea(3.5, 2.5)).toBeCloseTo(8.75);
  });

  it('should throw error for zero width', () => {
    expect(() => calculateArea(0, 10)).toThrow('Width must be positive');
  });

  it('should throw error for negative width', () => {
    expect(() => calculateArea(-5, 10)).toThrow('Width must be positive');
  });

  it('should throw error for zero height', () => {
    expect(() => calculateArea(10, 0)).toThrow('Height must be positive');
  });

  it('should throw error for negative height', () => {
    expect(() => calculateArea(10, -5)).toThrow('Height must be positive');
  });
});
```

### Pattern 2: Class from Specification

**Specification:**
```
Class: BankAccount
Purpose: Manage a bank account with deposits and withdrawals

Attributes:
  - account_number: string (unique identifier)
  - balance: decimal (current balance, must be >= 0)
  - owner_name: string

Methods:
  - deposit(amount): Add money to account
    Precondition: amount > 0
    Postcondition: balance increased by amount

  - withdraw(amount): Remove money from account
    Precondition: amount > 0 and amount <= balance
    Postcondition: balance decreased by amount

  - get_balance(): Return current balance
    Postcondition: returns balance >= 0

Invariants:
  - balance must always be >= 0
  - account_number is immutable
```

**Generated implementation:**
```python
from decimal import Decimal
from typing import Final

class InsufficientFundsError(Exception):
    """Raised when withdrawal amount exceeds account balance."""
    pass

class InvalidAmountError(Exception):
    """Raised when transaction amount is invalid."""
    pass

class BankAccount:
    """
    Manage a bank account with deposits and withdrawals.

    Invariants:
        - Balance is always >= 0
        - Account number is immutable once set

    Attributes:
        account_number: Unique account identifier (immutable)
        balance: Current account balance (non-negative)
        owner_name: Name of account owner
    """

    def __init__(self, account_number: str, owner_name: str, initial_balance: Decimal = Decimal('0')):
        """
        Initialize a new bank account.

        Args:
            account_number: Unique account identifier
            owner_name: Name of account owner
            initial_balance: Starting balance (default: 0)

        Raises:
            ValueError: If account_number or owner_name is empty
            InvalidAmountError: If initial_balance is negative
        """
        if not account_number:
            raise ValueError("Account number cannot be empty")
        if not owner_name:
            raise ValueError("Owner name cannot be empty")
        if initial_balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative")

        self._account_number: Final[str] = account_number
        self._balance: Decimal = initial_balance
        self.owner_name: str = owner_name

    @property
    def account_number(self) -> str:
        """Get account number (immutable)."""
        return self._account_number

    @property
    def balance(self) -> Decimal:
        """Get current account balance."""
        return self._balance

    def deposit(self, amount: Decimal) -> None:
        """
        Add money to the account.

        Args:
            amount: Amount to deposit (must be positive)

        Raises:
            InvalidAmountError: If amount is not positive

        Postcondition:
            Balance increases by amount
        """
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")

        self._balance += amount

    def withdraw(self, amount: Decimal) -> None:
        """
        Remove money from the account.

        Args:
            amount: Amount to withdraw (must be positive and <= balance)

        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If amount exceeds current balance

        Postcondition:
            Balance decreases by amount
        """
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Insufficient funds: balance={self._balance}, requested={amount}"
            )

        self._balance -= amount

    def get_balance(self) -> Decimal:
        """
        Return current account balance.

        Returns:
            Current balance (always >= 0)
        """
        return self._balance

    def __repr__(self) -> str:
        """Return string representation of account."""
        return f"BankAccount(account_number={self._account_number!r}, balance={self._balance}, owner={self.owner_name!r})"
```

**Generated tests:**
```python
import pytest
from decimal import Decimal

class TestBankAccount:
    """Test suite for BankAccount class."""

    def test_init_valid(self):
        """Test creating account with valid parameters."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        assert account.account_number == "12345"
        assert account.balance == Decimal('100')
        assert account.owner_name == "John Doe"

    def test_init_default_balance(self):
        """Test creating account with default zero balance."""
        account = BankAccount("12345", "John Doe")
        assert account.balance == Decimal('0')

    def test_init_invalid_account_number(self):
        """Test that empty account number raises ValueError."""
        with pytest.raises(ValueError, match="Account number cannot be empty"):
            BankAccount("", "John Doe")

    def test_init_invalid_owner_name(self):
        """Test that empty owner name raises ValueError."""
        with pytest.raises(ValueError, match="Owner name cannot be empty"):
            BankAccount("12345", "")

    def test_init_negative_balance(self):
        """Test that negative initial balance raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="cannot be negative"):
            BankAccount("12345", "John Doe", Decimal('-10'))

    def test_account_number_immutable(self):
        """Test that account number cannot be changed."""
        account = BankAccount("12345", "John Doe")
        with pytest.raises(AttributeError):
            account.account_number = "67890"

    def test_deposit_valid(self):
        """Test depositing positive amount."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        account.deposit(Decimal('50'))
        assert account.balance == Decimal('150')

    def test_deposit_zero(self):
        """Test that depositing zero raises InvalidAmountError."""
        account = BankAccount("12345", "John Doe")
        with pytest.raises(InvalidAmountError, match="must be positive"):
            account.deposit(Decimal('0'))

    def test_deposit_negative(self):
        """Test that depositing negative amount raises InvalidAmountError."""
        account = BankAccount("12345", "John Doe")
        with pytest.raises(InvalidAmountError, match="must be positive"):
            account.deposit(Decimal('-10'))

    def test_withdraw_valid(self):
        """Test withdrawing valid amount."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        account.withdraw(Decimal('30'))
        assert account.balance == Decimal('70')

    def test_withdraw_entire_balance(self):
        """Test withdrawing entire balance."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        account.withdraw(Decimal('100'))
        assert account.balance == Decimal('0')

    def test_withdraw_insufficient_funds(self):
        """Test that withdrawing more than balance raises InsufficientFundsError."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        with pytest.raises(InsufficientFundsError, match="Insufficient funds"):
            account.withdraw(Decimal('150'))

    def test_withdraw_zero(self):
        """Test that withdrawing zero raises InvalidAmountError."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        with pytest.raises(InvalidAmountError, match="must be positive"):
            account.withdraw(Decimal('0'))

    def test_withdraw_negative(self):
        """Test that withdrawing negative amount raises InvalidAmountError."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        with pytest.raises(InvalidAmountError, match="must be positive"):
            account.withdraw(Decimal('-10'))

    def test_get_balance(self):
        """Test getting account balance."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        assert account.get_balance() == Decimal('100')
        assert account.get_balance() >= 0  # Invariant check

    def test_multiple_transactions(self):
        """Test sequence of deposits and withdrawals."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        account.deposit(Decimal('50'))  # 150
        account.withdraw(Decimal('30'))  # 120
        account.deposit(Decimal('10'))  # 130
        account.withdraw(Decimal('80'))  # 50
        assert account.balance == Decimal('50')

    def test_repr(self):
        """Test string representation."""
        account = BankAccount("12345", "John Doe", Decimal('100'))
        repr_str = repr(account)
        assert "12345" in repr_str
        assert "John Doe" in repr_str
        assert "100" in repr_str
```

### Pattern 3: Interface from API Specification

**Specification (OpenAPI):**
```yaml
paths:
  /users/{userId}:
    get:
      summary: Get user by ID
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
```

**Generated implementation (Python with FastAPI):**
```python
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    """User model."""
    id: int
    name: str
    email: str
    created_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": "2024-01-01T00:00:00Z"
            }
        }

# Mock database
users_db: dict[int, User] = {
    1: User(id=1, name="John Doe", email="john@example.com", created_at="2024-01-01T00:00:00Z")
}

@app.get(
    "/users/{userId}",
    response_model=User,
    summary="Get user by ID",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    }
)
async def get_user(
    userId: int = Path(..., description="User ID", ge=1)
) -> User:
    """
    Retrieve a user by their ID.

    Args:
        userId: Unique user identifier (must be >= 1)

    Returns:
        User object with id, name, email, and created_at

    Raises:
        HTTPException: 404 if user not found
    """
    user = users_db.get(userId)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {userId} not found")
    return user
```

**Generated tests:**
```python
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_get_user_success():
    """Test retrieving existing user."""
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

def test_get_user_not_found():
    """Test retrieving non-existent user."""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_get_user_invalid_id():
    """Test with invalid user ID."""
    response = client.get("/users/0")
    assert response.status_code == 422  # Validation error

def test_get_user_negative_id():
    """Test with negative user ID."""
    response = client.get("/users/-1")
    assert response.status_code == 422  # Validation error
```

### Pattern 4: Data Structure from Schema

**Specification (JSON Schema):**
```json
{
  "type": "object",
  "title": "Product",
  "required": ["id", "name", "price"],
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "price": {
      "type": "number",
      "minimum": 0
    },
    "category": {
      "type": "string",
      "enum": ["electronics", "clothing", "food", "other"]
    },
    "inStock": {
      "type": "boolean",
      "default": true
    }
  }
}
```

**Generated implementation (TypeScript):**
```typescript
/**
 * Product category enumeration.
 */
export enum ProductCategory {
  Electronics = 'electronics',
  Clothing = 'clothing',
  Food = 'food',
  Other = 'other'
}

/**
 * Product data structure.
 */
export interface Product {
  /** Unique product identifier (must be >= 1) */
  id: number;

  /** Product name (1-100 characters) */
  name: string;

  /** Product price (must be >= 0) */
  price: number;

  /** Product category (optional) */
  category?: ProductCategory;

  /** Whether product is in stock (default: true) */
  inStock?: boolean;
}

/**
 * Validate a product object.
 *
 * @param product - Product object to validate
 * @throws {Error} If validation fails
 */
export function validateProduct(product: Product): void {
  if (product.id < 1) {
    throw new Error('Product ID must be at least 1');
  }

  if (product.name.length < 1 || product.name.length > 100) {
    throw new Error('Product name must be 1-100 characters');
  }

  if (product.price < 0) {
    throw new Error('Product price must be non-negative');
  }

  if (product.category !== undefined &&
      !Object.values(ProductCategory).includes(product.category)) {
    throw new Error(`Invalid category: ${product.category}`);
  }
}

/**
 * Create a product with validation.
 *
 * @param data - Product data
 * @returns Validated product object
 * @throws {Error} If validation fails
 */
export function createProduct(data: Product): Product {
  const product: Product = {
    id: data.id,
    name: data.name,
    price: data.price,
    category: data.category,
    inStock: data.inStock ?? true
  };

  validateProduct(product);
  return product;
}
```

**Generated tests:**
```typescript
import { describe, it, expect } from '@jest/globals';
import { Product, ProductCategory, validateProduct, createProduct } from './product';

describe('Product validation', () => {
  const validProduct: Product = {
    id: 1,
    name: 'Test Product',
    price: 10.99,
    category: ProductCategory.Electronics,
    inStock: true
  };

  describe('validateProduct', () => {
    it('should accept valid product', () => {
      expect(() => validateProduct(validProduct)).not.toThrow();
    });

    it('should reject product with invalid ID', () => {
      const invalid = { ...validProduct, id: 0 };
      expect(() => validateProduct(invalid)).toThrow('ID must be at least 1');
    });

    it('should reject product with empty name', () => {
      const invalid = { ...validProduct, name: '' };
      expect(() => validateProduct(invalid)).toThrow('name must be 1-100 characters');
    });

    it('should reject product with too long name', () => {
      const invalid = { ...validProduct, name: 'a'.repeat(101) };
      expect(() => validateProduct(invalid)).toThrow('name must be 1-100 characters');
    });

    it('should reject product with negative price', () => {
      const invalid = { ...validProduct, price: -1 };
      expect(() => validateProduct(invalid)).toThrow('price must be non-negative');
    });

    it('should accept product with zero price', () => {
      const valid = { ...validProduct, price: 0 };
      expect(() => validateProduct(valid)).not.toThrow();
    });

    it('should accept product without category', () => {
      const valid = { ...validProduct, category: undefined };
      expect(() => validateProduct(valid)).not.toThrow();
    });
  });

  describe('createProduct', () => {
    it('should create product with all fields', () => {
      const product = createProduct(validProduct);
      expect(product).toEqual(validProduct);
    });

    it('should set default inStock to true', () => {
      const data = { ...validProduct, inStock: undefined };
      const product = createProduct(data);
      expect(product.inStock).toBe(true);
    });

    it('should respect explicit inStock value', () => {
      const data = { ...validProduct, inStock: false };
      const product = createProduct(data);
      expect(product.inStock).toBe(false);
    });

    it('should throw on invalid data', () => {
      const invalid = { ...validProduct, id: -1 };
      expect(() => createProduct(invalid)).toThrow();
    });
  });
});
```

## Language-Specific Templates

### Python
- Use type hints (PEP 484)
- Docstrings (Google or NumPy style)
- Property decorators for getters
- Raise appropriate exceptions
- Follow PEP 8 naming

### TypeScript/JavaScript
- Use interfaces for contracts
- JSDoc comments
- Readonly for immutability
- Async/await for promises
- camelCase naming

### Java
- Use interfaces and abstract classes
- Javadoc comments
- Getters/setters
- Checked exceptions
- camelCase naming

### Rust
- Use traits for interfaces
- Rustdoc comments
- Result type for errors
- Ownership patterns
- snake_case naming

## Best Practices

1. **Start with specifications** - Fully understand requirements before coding
2. **Include validation** - Check preconditions and invariants
3. **Handle errors explicitly** - Don't ignore edge cases
4. **Document thoroughly** - Explain what, why, and how
5. **Generate tests** - Tests validate the implementation
6. **Follow conventions** - Use language idioms and patterns
7. **Keep it simple** - Don't over-engineer
8. **Make it immutable** - When appropriate, prevent mutation
9. **Use types** - Leverage type systems for safety
10. **Provide examples** - Show how to use the code

## Common Patterns

- **Factory pattern** - For complex object creation
- **Builder pattern** - For objects with many parameters
- **Strategy pattern** - For interchangeable algorithms
- **Template method** - For invariant algorithms with variant steps
- **Dependency injection** - For testability and flexibility
