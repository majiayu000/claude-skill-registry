---
name: code-documentation
description: Write comprehensive code documentation including JSDoc, Python docstrings, inline comments, function documentation, and API comments. Use when documenting code, writing docstrings, or creating inline documentation.
---

# Code Documentation

## Overview

Create clear, comprehensive code documentation using language-specific standards like JSDoc, Python docstrings, JavaDoc, and inline comments.

## When to Use

- Function and class documentation
- JSDoc for JavaScript/TypeScript
- Python docstrings
- JavaDoc for Java
- Inline code comments
- API documentation from code
- Type definitions
- Usage examples in code

## JavaScript/TypeScript (JSDoc)

### Function Documentation

```javascript
/**
 * Calculates the total price including tax and discount.
 *
 * @param {number} basePrice - The base price before tax and discount
 * @param {number} taxRate - Tax rate as a decimal (e.g., 0.08 for 8%)
 * @param {number} [discount=0] - Optional discount amount
 * @returns {number} The final price after tax and discount
 * @throws {Error} If basePrice or taxRate is negative
 *
 * @example
 * const price = calculateTotalPrice(100, 0.08, 10);
 * console.log(price); // 98
 *
 * @example
 * // Without discount
 * const price = calculateTotalPrice(100, 0.08);
 * console.log(price); // 108
 */
function calculateTotalPrice(basePrice, taxRate, discount = 0) {
  if (basePrice < 0 || taxRate < 0) {
    throw new Error('Price and tax rate must be non-negative');
  }
  return basePrice * (1 + taxRate) - discount;
}

/**
 * Fetches user data from the API with retry logic.
 *
 * @async
 * @param {string} userId - The unique identifier for the user
 * @param {Object} [options={}] - Additional options
 * @param {number} [options.maxRetries=3] - Maximum number of retry attempts
 * @param {number} [options.timeout=5000] - Request timeout in milliseconds
 * @returns {Promise<User>} Promise resolving to user object
 * @throws {Error} If user not found after all retries
 *
 * @typedef {Object} User
 * @property {string} id - User ID
 * @property {string} name - User's full name
 * @property {string} email - User's email address
 * @property {string[]} roles - Array of user roles
 *
 * @example
 * try {
 *   const user = await fetchUser('user123', { maxRetries: 5 });
 *   console.log(user.name);
 * } catch (error) {
 *   console.error('Failed to fetch user:', error);
 * }
 */
async function fetchUser(userId, options = {}) {
  const { maxRetries = 3, timeout = 5000 } = options;
  // Implementation...
}
```

### Class Documentation

```javascript
/**
 * Represents a shopping cart in an e-commerce application.
 * Manages items, calculates totals, and handles checkout operations.
 *
 * @class
 * @example
 * const cart = new ShoppingCart('user123');
 * cart.addItem({ id: 'prod1', name: 'Laptop', price: 999.99 }, 1);
 * console.log(cart.getTotal()); // 999.99
 */
class ShoppingCart {
  /**
   * Creates a new shopping cart instance.
   *
   * @constructor
   * @param {string} userId - The ID of the user who owns this cart
   * @param {Object} [options={}] - Configuration options
   * @param {string} [options.currency='USD'] - Currency code
   * @param {number} [options.taxRate=0] - Tax rate as decimal
   */
  constructor(userId, options = {}) {
    this.userId = userId;
    this.items = [];
    this.currency = options.currency || 'USD';
    this.taxRate = options.taxRate || 0;
  }

  /**
   * Adds an item to the cart or increases quantity if already present.
   *
   * @param {Product} product - The product to add
   * @param {number} quantity - Quantity to add (must be positive integer)
   * @returns {CartItem} The added or updated cart item
   * @throws {Error} If quantity is not a positive integer
   *
   * @typedef {Object} Product
   * @property {string} id - Product ID
   * @property {string} name - Product name
   * @property {number} price - Product price
   *
   * @typedef {Object} CartItem
   * @property {Product} product - Product details
   * @property {number} quantity - Item quantity
   * @property {number} subtotal - Item subtotal (price * quantity)
   */
  addItem(product, quantity) {
    if (!Number.isInteger(quantity) || quantity <= 0) {
      throw new Error('Quantity must be a positive integer');
    }

    const existingItem = this.items.find(
      item => item.product.id === product.id
    );

    if (existingItem) {
      existingItem.quantity += quantity;
      existingItem.subtotal = existingItem.product.price * existingItem.quantity;
      return existingItem;
    }

    const newItem = {
      product,
      quantity,
      subtotal: product.price * quantity
    };
    this.items.push(newItem);
    return newItem;
  }

  /**
   * Calculates the total price including tax.
   *
   * @returns {number} Total price with tax
   */
  getTotal() {
    const subtotal = this.items.reduce(
      (sum, item) => sum + item.subtotal,
      0
    );
    return subtotal * (1 + this.taxRate);
  }

  /**
   * Removes all items from the cart.
   *
   * @returns {void}
   */
  clear() {
    this.items = [];
  }
}
```

### Type Definitions

```typescript
/**
 * API response wrapper for all endpoints
 *
 * @template T - The type of data in the response
 * @typedef {Object} ApiResponse
 * @property {boolean} success - Whether the request succeeded
 * @property {T} [data] - Response data (present on success)
 * @property {string} [error] - Error message (present on failure)
 * @property {Object} [metadata] - Additional response metadata
 * @property {number} metadata.timestamp - Response timestamp
 * @property {string} metadata.requestId - Unique request ID
 */

/**
 * User authentication credentials
 *
 * @typedef {Object} Credentials
 * @property {string} email - User email address
 * @property {string} password - User password (min 8 characters)
 */

/**
 * Pagination parameters for list endpoints
 *
 * @typedef {Object} PaginationParams
 * @property {number} [page=1] - Page number (1-indexed)
 * @property {number} [limit=20] - Items per page (max 100)
 * @property {string} [sortBy='createdAt'] - Field to sort by
 * @property {'asc'|'desc'} [order='desc'] - Sort order
 */
```

## Python (Docstrings)

### Function Documentation

```python
def calculate_statistics(data: list[float], include_median: bool = True) -> dict:
    """
    Calculate statistical measures for a dataset.

    Computes mean, standard deviation, min, max, and optionally median
    for a list of numerical values.

    Args:
        data: List of numerical values to analyze. Must contain at least
            one value.
        include_median: Whether to calculate median (default: True).
            Set to False for better performance with large datasets.

    Returns:
        Dictionary containing the following keys:
        - 'mean' (float): Arithmetic mean of the data
        - 'std' (float): Standard deviation
        - 'min' (float): Minimum value
        - 'max' (float): Maximum value
        - 'median' (float): Median value (if include_median is True)
        - 'count' (int): Number of data points

    Raises:
        ValueError: If data is empty or contains non-numeric values.
        TypeError: If data is not a list.

    Examples:
        >>> data = [1, 2, 3, 4, 5]
        >>> stats = calculate_statistics(data)
        >>> print(stats['mean'])
        3.0

        >>> # Without median for performance
        >>> large_data = list(range(1000000))
        >>> stats = calculate_statistics(large_data, include_median=False)

    Note:
        For very large datasets, consider setting include_median=False
        as median calculation requires sorting which is O(n log n).

    See Also:
        numpy.mean, numpy.std, statistics.median
    """
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    if not data:
        raise ValueError("Data cannot be empty")

    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = variance ** 0.5

    result = {
        'mean': mean,
        'std': std,
        'min': min(data),
        'max': max(data),
        'count': len(data)
    }

    if include_median:
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            result['median'] = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            result['median'] = sorted_data[n//2]

    return result
```

### Class Documentation

```python
class DatabaseConnection:
    """
    Manages database connections with automatic retry and connection pooling.

    This class provides a context manager interface for database operations,
    handling connection establishment, query execution, and cleanup.

    Attributes:
        host (str): Database host address
        port (int): Database port number
        database (str): Database name
        max_retries (int): Maximum number of connection retry attempts
        timeout (int): Connection timeout in seconds
        pool_size (int): Maximum number of connections in the pool

    Example:
        Basic usage with context manager:

        >>> with DatabaseConnection('localhost', 5432, 'mydb') as db:
        ...     results = db.execute('SELECT * FROM users')
        ...     for row in results:
        ...         print(row)

        Custom configuration:

        >>> config = {
        ...     'max_retries': 5,
        ...     'timeout': 30,
        ...     'pool_size': 10
        ... }
        >>> db = DatabaseConnection('localhost', 5432, 'mydb', **config)

    Note:
        Always use this class with a context manager to ensure proper
        connection cleanup. Manual connection management is not recommended.

    Warning:
        Connections are not thread-safe. Create separate instances for
        concurrent operations.
    """

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str = None,
        password: str = None,
        max_retries: int = 3,
        timeout: int = 10,
        pool_size: int = 5
    ):
        """
        Initialize a new database connection manager.

        Args:
            host: Database server hostname or IP address
            port: Database server port (typically 5432 for PostgreSQL)
            database: Name of the database to connect to
            username: Database username (default: from environment)
            password: Database password (default: from environment)
            max_retries: Maximum retry attempts for failed connections
            timeout: Connection timeout in seconds
            pool_size: Maximum number of pooled connections

        Raises:
            ValueError: If host, port, or database is invalid
            ConnectionError: If unable to establish initial connection
        """
        self.host = host
        self.port = port
        self.database = database
        self.max_retries = max_retries
        self.timeout = timeout
        self.pool_size = pool_size
        self._connection = None
        self._pool = []

    def execute(self, query: str, params: tuple = None) -> list:
        """
        Execute a SQL query and return results.

        Args:
            query: SQL query string with optional parameter placeholders
            params: Tuple of parameter values for parameterized queries

        Returns:
            List of rows as dictionaries with column names as keys

        Raises:
            QueryError: If query execution fails
            ConnectionError: If database connection is lost

        Example:
            >>> db = DatabaseConnection('localhost', 5432, 'mydb')
            >>> results = db.execute(
            ...     'SELECT * FROM users WHERE age > %s',
            ...     (18,)
            ... )
        """
        pass

    def __enter__(self):
        """Enter context manager, establishing database connection."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager, closing database connection."""
        self.close()
```

### Module Documentation

```python
"""
User authentication and authorization module.

This module provides functions for user authentication, password hashing,
token generation, and permission checking. It supports multiple authentication
methods including JWT tokens, API keys, and OAuth2.

Features:
    - Secure password hashing with bcrypt
    - JWT token generation and validation
    - Role-based access control (RBAC)
    - OAuth2 integration (Google, GitHub)
    - Two-factor authentication (2FA)

Example:
    Basic authentication:

    >>> from auth import authenticate, generate_token
    >>> user = authenticate('user@example.com', 'password123')
    >>> token = generate_token(user)

    Password hashing:

    >>> from auth import hash_password, verify_password
    >>> hashed = hash_password('password123')
    >>> is_valid = verify_password('password123', hashed)

Attributes:
    TOKEN_EXPIRY (int): Default token expiration time in seconds
    HASH_ROUNDS (int): Number of bcrypt hashing rounds
    MAX_LOGIN_ATTEMPTS (int): Maximum failed login attempts before lockout

Todo:
    * Add support for SAML authentication
    * Implement refresh token rotation
    * Add rate limiting for login attempts

Note:
    This module requires bcrypt and PyJWT packages to be installed.
"""

TOKEN_EXPIRY = 3600  # 1 hour
HASH_ROUNDS = 12
MAX_LOGIN_ATTEMPTS = 5
```

## Java (JavaDoc)

```java
/**
 * Manages user accounts and authentication in the system.
 * <p>
 * This class provides methods for creating, updating, and deleting user
 * accounts, as well as authenticating users and managing sessions.
 * </p>
 *
 * <h2>Usage Example:</h2>
 * <pre>{@code
 * UserManager manager = new UserManager();
 * User user = manager.createUser("john@example.com", "password123");
 * boolean authenticated = manager.authenticate(user.getId(), "password123");
 * }</pre>
 *
 * @author John Doe
 * @version 2.0
 * @since 1.0
 * @see User
 * @see Session
 */
public class UserManager {
    /**
     * Creates a new user account with the specified credentials.
     *
     * @param email    the user's email address (must be valid and unique)
     * @param password the user's password (minimum 8 characters)
     * @return the newly created User object
     * @throws IllegalArgumentException if email is invalid or already exists
     * @throws PasswordTooWeakException if password doesn't meet requirements
     * @see #updateUser(String, User)
     * @see #deleteUser(String)
     */
    public User createUser(String email, String password)
            throws IllegalArgumentException, PasswordTooWeakException {
        // Implementation
    }

    /**
     * Authenticates a user with their credentials.
     *
     * @param userId   the unique user identifier
     * @param password the user's password
     * @return {@code true} if authentication succeeded, {@code false} otherwise
     * @throws UserNotFoundException if the user doesn't exist
     * @deprecated Use {@link #authenticateWithToken(String, String)} instead
     */
    @Deprecated
    public boolean authenticate(String userId, String password)
            throws UserNotFoundException {
        // Implementation
    }
}
```

## Inline Comments Best Practices

```javascript
// ❌ BAD: Obvious comment
// Increment counter by 1
counter++;

// ✅ GOOD: Explain why, not what
// Account for 1-based indexing in the API response
counter++;

// ❌ BAD: Outdated comment
// TODO: Fix this bug (written 2 years ago)
function processData() {}

// ✅ GOOD: Actionable comment with context
// TODO(john, 2025-01-15): Refactor to use async/await
// See GitHub issue #1234 for performance benchmarks
function processData() {}

// ❌ BAD: Commented-out code
// const oldCalculation = (a, b) => a + b;
// const anotherOldThing = 42;

// ✅ GOOD: Remove dead code, use version control instead

// ❌ BAD: Redundant comment
/**
 * Gets the user name
 */
function getUserName() {
  return this.name;
}

// ✅ GOOD: Add value with context
/**
 * Returns display name formatted according to user's locale preferences.
 * Falls back to username if display name is not set.
 */
function getUserName() {
  return this.displayName || this.username;
}
```

## Best Practices

### ✅ DO
- Document public APIs thoroughly
- Include usage examples
- Document parameters and return values
- Specify thrown exceptions/errors
- Use language-specific standards (JSDoc, docstrings, etc.)
- Keep comments up-to-date
- Document "why" not "what"
- Include edge cases and gotchas
- Add links to related functions
- Document type definitions
- Use consistent formatting

### ❌ DON'T
- State the obvious in comments
- Leave commented-out code
- Write misleading comments
- Skip examples for complex functions
- Use vague parameter descriptions
- Forget to update docs when code changes
- Over-comment simple code

## Resources

- [JSDoc Documentation](https://jsdoc.app/)
- [Python Docstring Conventions (PEP 257)](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [JavaDoc Guide](https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html)
- [TypeDoc](https://typedoc.org/)
