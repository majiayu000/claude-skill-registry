---
name: code-documentation-generator
description: Эксперт по документации кода. Используй для JSDoc, docstrings, комментариев и автогенерации документации.
---

# Code Documentation Generator

Эксперт по созданию качественной документации кода.

## Основные принципы

- **Clarity > Sophistication** — ясность важнее сложности
- **Progressive disclosure** — от общего к деталям
- **Consistency** — единообразие форматирования
- **Accuracy** — синхронизация с кодом
- **Accessibility** — для разных уровней разработчиков

## JSDoc (JavaScript/TypeScript)

```javascript
/**
 * Calculates the total price including tax and discounts.
 *
 * @param {number} basePrice - The original price before modifications
 * @param {number} taxRate - Tax rate as decimal (e.g., 0.21 for 21%)
 * @param {number} [discount=0] - Optional discount as decimal
 * @returns {number} The final calculated price
 * @throws {Error} If basePrice or taxRate is negative
 *
 * @example
 * // Calculate price with 21% tax and 10% discount
 * const total = calculateTotalPrice(100, 0.21, 0.10);
 * // Returns: 108.90
 */
function calculateTotalPrice(basePrice, taxRate, discount = 0) {
  if (basePrice < 0 || taxRate < 0) {
    throw new Error('Price and tax rate must be non-negative');
  }
  const discountedPrice = basePrice * (1 - discount);
  return discountedPrice * (1 + taxRate);
}
```

## TypeScript с JSDoc

```typescript
/**
 * User service for managing user operations.
 */
export class UserService {
  /**
   * Creates a new user in the system.
   *
   * @param userData - The user data for registration
   * @returns Promise resolving to the created user
   * @throws {ValidationError} When user data is invalid
   * @throws {DuplicateError} When email already exists
   *
   * @example
   * const user = await userService.createUser({
   *   email: 'user@example.com',
   *   name: 'John Doe'
   * });
   */
  async createUser(userData: CreateUserDTO): Promise<User> {
    // Implementation
  }

  /**
   * Retrieves a user by their unique identifier.
   *
   * @param id - The user's UUID
   * @returns The user if found, null otherwise
   */
  async getUserById(id: string): Promise<User | null> {
    // Implementation
  }
}
```

## Python Docstrings (Google Style)

```python
def process_transaction(
    amount: float,
    currency: str,
    metadata: dict | None = None
) -> TransactionResult:
    """Process a financial transaction with validation and logging.

    This function handles the complete transaction lifecycle including
    validation, processing, and audit logging. It supports multiple
    currencies and optional metadata attachment.

    Args:
        amount: The transaction amount in the specified currency.
            Must be positive and not exceed the daily limit.
        currency: ISO 4217 currency code (e.g., 'USD', 'EUR').
        metadata: Optional dictionary with additional transaction
            details. Keys 'reference' and 'notes' are recommended.

    Returns:
        TransactionResult containing:
            - transaction_id: Unique identifier for the transaction
            - status: 'completed', 'pending', or 'failed'
            - timestamp: UTC datetime of processing
            - fee: Applied transaction fee

    Raises:
        ValidationError: If amount is negative or exceeds limits.
        CurrencyNotSupportedError: If currency code is invalid.
        InsufficientFundsError: If account balance is too low.

    Example:
        >>> result = process_transaction(
        ...     amount=100.50,
        ...     currency='USD',
        ...     metadata={'reference': 'INV-001'}
        ... )
        >>> print(result.transaction_id)
        'txn_abc123xyz'

    Note:
        Transactions over $10,000 require additional verification
        and may be held for compliance review.
    """
    pass
```

## Python Docstrings (NumPy Style)

```python
def calculate_statistics(
    data: np.ndarray,
    weights: np.ndarray | None = None,
    axis: int = 0
) -> dict:
    """
    Calculate weighted statistics for the input data.

    Parameters
    ----------
    data : np.ndarray
        Input data array of shape (n_samples, n_features).
    weights : np.ndarray, optional
        Weight array of shape (n_samples,). If None, uniform
        weights are used.
    axis : int, default=0
        Axis along which to compute statistics.

    Returns
    -------
    dict
        Dictionary containing:
        - 'mean' : np.ndarray
            Weighted mean values.
        - 'std' : np.ndarray
            Weighted standard deviation.
        - 'median' : np.ndarray
            Weighted median values.

    Raises
    ------
    ValueError
        If data and weights have incompatible shapes.
    TypeError
        If data is not a numpy array.

    See Also
    --------
    numpy.average : Compute weighted average.
    scipy.stats.describe : Compute descriptive statistics.

    Examples
    --------
    >>> data = np.array([[1, 2], [3, 4], [5, 6]])
    >>> stats = calculate_statistics(data)
    >>> stats['mean']
    array([3., 4.])
    """
    pass
```

## REST API Documentation

```yaml
# OpenAPI/Swagger style
paths:
  /api/users:
    post:
      summary: Create a new user
      description: |
        Creates a new user account with the provided information.
        Email must be unique across the system.
      tags:
        - Users
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            example:
              email: "user@example.com"
              name: "John Doe"
              role: "member"
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Invalid request data
        '409':
          description: Email already exists
```

## Markdown API Documentation

```markdown
## Create User

Creates a new user account.

**Endpoint:** `POST /api/users`

**Authentication:** Bearer token required

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email address |
| name | string | Yes | Full name (2-100 chars) |
| role | string | No | Role: "admin", "member" (default) |

### Example Request

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member"
}
```

### Response

**201 Created**
```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Error Responses

| Code | Description |
|------|-------------|
| 400 | Invalid request data |
| 401 | Unauthorized |
| 409 | Email already exists |
```

## README Template

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

```bash
npm install project-name
```

```javascript
import { Client } from 'project-name';

const client = new Client({ apiKey: 'your-key' });
const result = await client.doSomething();
```

## Prerequisites

- Node.js 18+
- npm 8+

## Installation

```bash
# Using npm
npm install project-name

# Using yarn
yarn add project-name
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| API_KEY | - | Your API key (required) |
| TIMEOUT | 30000 | Request timeout in ms |
| DEBUG | false | Enable debug logging |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

## Inline Comments

```javascript
// GOOD: Explain WHY, not WHAT
// Skip validation for internal requests to improve performance
// External requests are validated at the API gateway
if (request.isInternal) {
  return processDirectly(data);
}

// BAD: States the obvious
// Check if user is null
if (user === null) {
  return null;
}

// GOOD: Document complex logic
// Using binary search for O(log n) lookup in sorted array
// Linear search would be O(n) for 10k+ items
const index = binarySearch(sortedItems, targetId);

// GOOD: Explain business rules
// Orders over $1000 require manager approval per policy DOC-123
// This threshold was set by finance team in Q3 2023
if (order.total > 1000 && !order.hasManagerApproval) {
  throw new ApprovalRequiredError();
}
```

## Автоматизация документации

### TypeDoc

```json
{
  "typedocOptions": {
    "entryPoints": ["src/index.ts"],
    "out": "docs",
    "plugin": ["typedoc-plugin-markdown"],
    "readme": "README.md",
    "excludePrivate": true,
    "excludeInternal": true
  }
}
```

### Sphinx (Python)

```python
# conf.py
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints'
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True
}
```

## Лучшие практики

1. **Документируйте публичный API** — всё, что экспортируется
2. **Примеры кода** — реальные use cases
3. **Обновляйте синхронно** — документация = часть PR
4. **Используйте линтеры** — eslint-plugin-jsdoc, pydocstyle
5. **Версионируйте** — документация должна соответствовать версии кода
