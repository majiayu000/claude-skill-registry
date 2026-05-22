---
name: docstring-format
description: Automatically applies when writing function docstrings. Uses Google-style format with Args, Returns, Raises, Examples, and Security Note sections for proper documentation.
---

# Docstring Format Enforcer

Use Google-style docstrings with proper sections for all functions and classes.

## ✅ Standard Function Docstring

```python
def calculate_total(items: List[Item], tax_rate: float, discount: Optional[float] = None) -> Decimal:
    """
    Calculate total price including tax and optional discount.

    Computes the subtotal from items, applies discount if provided,
    then adds tax to get final total.

    Args:
        items: List of items with price and quantity
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)
        discount: Optional discount as decimal (e.g., 0.10 for 10% off)

    Returns:
        Total price as Decimal with 2 decimal places

    Raises:
        ValueError: If tax_rate is negative or > 1
        ValueError: If discount is negative or > 1

    Example:
        >>> items = [Item(price=10.00, quantity=2)]
        >>> calculate_total(items, tax_rate=0.08)
        Decimal('21.60')
    """
    if tax_rate < 0 or tax_rate > 1:
        raise ValueError("tax_rate must be between 0 and 1")

    subtotal = sum(item.price * item.quantity for item in items)

    if discount:
        if discount < 0 or discount > 1:
            raise ValueError("discount must be between 0 and 1")
        subtotal = subtotal * (1 - discount)

    total = subtotal * (1 + tax_rate)
    return round(total, 2)
```

## ✅ Async Function with Security Note

```python
async def fetch_user_payment_methods(user_id: str, include_expired: bool = False) -> List[PaymentMethod]:
    """
    Fetch payment methods for a user.

    Retrieves all payment methods from database, optionally filtering
    out expired cards. Payment tokens are included for transaction use.

    Args:
        user_id: User's unique identifier (MongoDB ObjectId)
        include_expired: Whether to include expired payment methods

    Returns:
        List of PaymentMethod objects containing:
        - token: Payment token for transactions (handle securely)
        - last_four: Last 4 digits of card
        - expiry: Expiration date (MM/YY format)
        - brand: Card brand (visa, mastercard, etc.)

    Raises:
        UserNotFoundError: If user_id doesn't exist
        DatabaseError: If database connection fails

    Security Note:
        Returns payment tokens that can be used for transactions.
        - Never log tokens in full
        - Always use HTTPS for transmission
        - Tokens expire after 1 hour of inactivity

    Example:
        >>> methods = await fetch_user_payment_methods("user_123")
        >>> for method in methods:
        ...     print(f"Card ending in {method.last_four}")
    """
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")

    methods = await db.payment_methods.find({"user_id": user_id}).to_list()

    if not include_expired:
        methods = [m for m in methods if not m.is_expired()]

    return methods
```

## ✅ Class Docstring

```python
class UserRepository:
    """
    Repository for user data access.

    Provides CRUD operations for user entities with caching
    and automatic cache invalidation on updates.

    Attributes:
        db: Database connection
        cache: Redis cache instance
        cache_ttl: Cache time-to-live in seconds (default: 3600)

    Example:
        >>> repo = UserRepository(db_conn, redis_client)
        >>> user = await repo.get_by_id("user_123")
        >>> await repo.update(user_id, {"name": "New Name"})
    """

    def __init__(self, db: Database, cache: Redis, cache_ttl: int = 3600):
        """
        Initialize repository with database and cache.

        Args:
            db: Database connection instance
            cache: Redis cache instance
            cache_ttl: Cache time-to-live in seconds
        """
        self.db = db
        self.cache = cache
        self.cache_ttl = cache_ttl
```

## ✅ Property Docstring

```python
class User:
    """User model."""

    @property
    def full_name(self) -> str:
        """
        Get user's full name.

        Combines first and last name with a space. Returns empty
        string if both names are missing.

        Returns:
            Full name as string, or empty string if no names set
        """
        if not self.first_name and not self.last_name:
            return ""
        return f"{self.first_name} {self.last_name}".strip()

    @full_name.setter
    def full_name(self, value: str) -> None:
        """
        Set user's full name.

        Splits on first space to set first_name and last_name.
        If no space, sets only first_name.

        Args:
            value: Full name to parse and set

        Raises:
            ValueError: If value is empty or only whitespace
        """
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")

        parts = value.strip().split(" ", 1)
        self.first_name = parts[0]
        self.last_name = parts[1] if len(parts) > 1 else ""
```

## ✅ Tool/API Function Docstring

```python
@tool
async def search_products(
    query: str,
    category: Optional[str] = None,
    max_results: int = 10
) -> str:
    """
    Search for products in catalog.

    Performs full-text search across product names and descriptions.
    Results are ranked by relevance and limited to max_results.

    Use this when customers ask to:
    - Find products by name or description
    - Search within a specific category
    - Browse available products

    Args:
        query: Search query string (e.g., "wireless headphones")
        category: Optional category filter (e.g., "electronics")
        max_results: Maximum results to return (1-100, default: 10)

    Returns:
        JSON string containing:
        - products: List of matching products
        - total: Total number of matches
        - query: Original search query
        - request_id: Request identifier for debugging

    Example Response:
        {
            "products": [
                {
                    "id": "prod_123",
                    "name": "Wireless Headphones",
                    "price": 99.99,
                    "in_stock": true
                }
            ],
            "total": 1,
            "query": "wireless headphones",
            "request_id": "req_abc123"
        }

    Security Note:
        Logs are PII-redacted. User ID is logged but not included
        in response to maintain privacy.
    """
    # Implementation
```

## Required Sections

**Always include:**
- ✅ Brief description (one-line summary)
- ✅ Extended description (what it does, how it works)
- ✅ `Args:` section (if has parameters)
- ✅ `Returns:` section (if returns value)

**Include when applicable:**
- ✅ `Raises:` section (if raises exceptions)
- ✅ `Example:` or `Example Response:` section
- ✅ `Security Note:` (if handles PII, payment data, auth)
- ✅ `Note:` or `Warning:` for important caveats
- ✅ `Attributes:` (for classes)
- ✅ Use cases (for tools: "Use this when...")

## Args Section Format

```python
def function(
    required_param: str,
    optional_param: Optional[int] = None,
    flag: bool = False
) -> dict:
    """
    Function description.

    Args:
        required_param: Description of required parameter.
            Can span multiple lines with 4-space indent.
        optional_param: Description of optional parameter.
            Default: None
        flag: Whether to enable feature. Default: False

    Returns:
        Dictionary containing results
    """
```

## Returns Section Format

```python
def get_user_stats(user_id: str) -> dict:
    """
    Get user statistics.

    Returns:
        Dictionary containing:
        - total_orders: Total number of orders (int)
        - total_spent: Total amount spent (Decimal)
        - last_order_date: Date of last order (datetime)
        - loyalty_tier: Current loyalty tier (str)
    """

def process_payment(amount: Decimal) -> Tuple[bool, Optional[str]]:
    """
    Process payment transaction.

    Returns:
        Tuple of (success, error_message) where:
        - success: True if payment succeeded, False otherwise
        - error_message: Error description if failed, None if succeeded
    """
```

## Raises Section Format

```python
def divide(a: float, b: float) -> float:
    """
    Divide two numbers.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Result of division

    Raises:
        ValueError: If b is zero
        TypeError: If a or b are not numeric
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Security Note Guidelines

**Add Security Note when function:**
- Handles payment tokens/cards
- Logs or processes PII data
- Accesses customer data
- Performs financial transactions
- Requires authentication/authorization
- Handles secrets or API keys

**Security Note should mention:**
```python
"""
Security Note:
    Handles customer payment data (PCI-DSS Level 1).
    - All PII is redacted in logs
    - Payment tokens expire after 1 hour
    - Requires user authentication
    - Never log full card numbers
    - Always use HTTPS for transmission
"""
```

## ❌ Anti-Patterns

```python
# ❌ No docstring
def calculate_total(items, tax):
    return sum(items) * (1 + tax)

# ❌ Minimal/unhelpful docstring
def calculate_total(items, tax):
    """Calculate total."""
    return sum(items) * (1 + tax)

# ❌ Wrong format (not Google-style)
def calculate_total(items, tax):
    """
    Calculate total.
    :param items: The items
    :param tax: The tax
    :return: The total
    """

# ❌ No type information
def calculate_total(items, tax):
    """
    Calculate total.

    Args:
        items: List of items
        tax: Tax rate

    Returns:
        Total
    """
    # Types should be in signature AND described in docstring!

# ❌ Vague descriptions
def process(data):
    """
    Process data.

    Args:
        data: The data

    Returns:
        The result
    """
    # Not helpful! What kind of data? What processing? What result?
```

## Best Practices Checklist

- ✅ Start with brief one-line summary
- ✅ Add detailed description for complex functions
- ✅ Document all parameters with clear descriptions
- ✅ Specify parameter types (should match type hints)
- ✅ Document return value structure and type
- ✅ List all exceptions that can be raised
- ✅ Add examples for non-obvious usage
- ✅ Include Security Note for sensitive operations
- ✅ Use complete sentences with proper punctuation
- ✅ Be specific about formats (ISO dates, decimals, etc.)
- ✅ Mention side effects (logs, DB writes, API calls)
- ✅ Document default values for optional parameters

## Auto-Apply

When writing functions:
1. Start with brief one-line description
2. Add extended description if needed
3. Add `Args:` section with all parameters
4. Add `Returns:` section describing output
5. Add `Raises:` if throws exceptions
6. Add `Security Note:` if handling sensitive data
7. Add `Example:` for complex usage
8. Use complete sentences
9. Be specific about data types and formats

## Related Skills

- pydantic-models - Document model fields
- structured-errors - Document error responses
- tool-design-pattern - Document tool usage
- pytest-patterns - Write test docstrings
