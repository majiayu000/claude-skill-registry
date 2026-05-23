---
name: oop-encapsulation
description: Use when applying encapsulation and information hiding principles in object-oriented design. Use when controlling access to object state and behavior.
allowed-tools:
  - Bash
  - Read
---

# OOP Encapsulation

Master encapsulation and information hiding to create robust, maintainable object-oriented systems. This skill focuses on controlling access to object internals and exposing well-defined interfaces.

## Understanding Encapsulation

Encapsulation is the bundling of data and methods that operate on that data within a single unit, while restricting direct access to some of the object's components. This principle protects object integrity and reduces coupling.

### Java Encapsulation

```java
// Strong encapsulation with validation
public class BankAccount {
    private String accountNumber;
    private BigDecimal balance;
    private final List<Transaction> transactions;

    public BankAccount(String accountNumber, BigDecimal initialBalance) {
        if (accountNumber == null || accountNumber.isEmpty()) {
            throw new IllegalArgumentException("Account number required");
        }
        if (initialBalance.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative");
        }

        this.accountNumber = accountNumber;
        this.balance = initialBalance;
        this.transactions = new ArrayList<>();
    }

    // Read-only access to account number
    public String getAccountNumber() {
        return accountNumber;
    }

    // Read-only access to balance
    public BigDecimal getBalance() {
        return balance;
    }

    // Defensive copy for collection
    public List<Transaction> getTransactions() {
        return Collections.unmodifiableList(transactions);
    }

    // Controlled mutation with validation
    public void deposit(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive");
        }

        balance = balance.add(amount);
        transactions.add(new Transaction(TransactionType.DEPOSIT, amount));
    }

    // Controlled mutation with business logic
    public void withdraw(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive");
        }
        if (amount.compareTo(balance) > 0) {
            throw new InsufficientFundsException("Insufficient balance");
        }

        balance = balance.subtract(amount);
        transactions.add(new Transaction(TransactionType.WITHDRAWAL, amount));
    }
}
```

### Python Encapsulation

```python
class Employee:
    """Employee with encapsulated salary information."""

    def __init__(self, name: str, salary: float, department: str):
        if not name:
            raise ValueError("Name is required")
        if salary < 0:
            raise ValueError("Salary cannot be negative")

        self._name = name  # Protected attribute
        self.__salary = salary  # Private attribute (name mangling)
        self._department = department
        self.__performance_rating = 0.0

    @property
    def name(self) -> str:
        """Read-only access to name."""
        return self._name

    @property
    def department(self) -> str:
        """Read-only access to department."""
        return self._department

    @property
    def salary(self) -> float:
        """Controlled access to salary."""
        return self.__salary

    @salary.setter
    def salary(self, value: float) -> None:
        """Controlled mutation with validation."""
        if value < 0:
            raise ValueError("Salary cannot be negative")
        if value < self.__salary * 0.9:
            raise ValueError("Salary cannot decrease by more than 10%")

        self.__salary = value

    @property
    def performance_rating(self) -> float:
        """Read-only access to performance rating."""
        return self.__performance_rating

    def update_performance(self, rating: float) -> None:
        """Controlled update with validation and side effects."""
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5")

        self.__performance_rating = rating

        # Business logic: automatic raise for high performers
        if rating >= 4.5:
            self.__salary *= 1.10

    def give_raise(self, percentage: float) -> None:
        """Apply percentage raise with validation."""
        if percentage < 0:
            raise ValueError("Raise percentage cannot be negative")
        if percentage > 20:
            raise ValueError("Single raise cannot exceed 20%")

        self.__salary *= (1 + percentage / 100)

    def __repr__(self) -> str:
        return f"Employee(name={self._name}, department={self._department})"
```

### TypeScript Encapsulation

```typescript
// Class-based encapsulation with private fields
class UserAccount {
  readonly #id: string;
  #username: string;
  #email: string;
  #passwordHash: string;
  #lastLoginAt: Date | null = null;
  #failedLoginAttempts = 0;
  #isLocked = false;

  constructor(username: string, email: string, passwordHash: string) {
    if (!username || username.length < 3) {
      throw new Error("Username must be at least 3 characters");
    }
    if (!this.isValidEmail(email)) {
      throw new Error("Invalid email format");
    }

    this.#id = crypto.randomUUID();
    this.#username = username;
    this.#email = email;
    this.#passwordHash = passwordHash;
  }

  // Read-only access
  get id(): string {
    return this.#id;
  }

  get username(): string {
    return this.#username;
  }

  get email(): string {
    return this.#email;
  }

  get lastLoginAt(): Date | null {
    return this.#lastLoginAt;
  }

  get isLocked(): boolean {
    return this.#isLocked;
  }

  // Controlled mutation with validation
  updateEmail(newEmail: string): void {
    if (!this.isValidEmail(newEmail)) {
      throw new Error("Invalid email format");
    }
    this.#email = newEmail;
  }

  // Business logic encapsulated
  attemptLogin(password: string): boolean {
    if (this.#isLocked) {
      throw new Error("Account is locked");
    }

    if (this.verifyPassword(password)) {
      this.#lastLoginAt = new Date();
      this.#failedLoginAttempts = 0;
      return true;
    }

    this.#failedLoginAttempts++;
    if (this.#failedLoginAttempts >= 3) {
      this.#isLocked = true;
    }
    return false;
  }

  // Private helper methods
  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  private verifyPassword(password: string): boolean {
    // Hash comparison logic
    return true; // Simplified
  }

  unlock(): void {
    this.#isLocked = false;
    this.#failedLoginAttempts = 0;
  }
}
```

### C# Encapsulation

```csharp
// Strong encapsulation with properties and backing fields
public class Product
{
    private readonly Guid _id;
    private string _name;
    private decimal _price;
    private int _stockQuantity;
    private readonly List<PriceHistory> _priceHistory;

    public Product(string name, decimal price, int initialStock)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Product name is required", nameof(name));

        if (price <= 0)
            throw new ArgumentException("Price must be positive", nameof(price));

        if (initialStock < 0)
            throw new ArgumentException("Stock cannot be negative", nameof(initialStock));

        _id = Guid.NewGuid();
        _name = name;
        _price = price;
        _stockQuantity = initialStock;
        _priceHistory = new List<PriceHistory>
        {
            new PriceHistory(price, DateTime.UtcNow)
        };
    }

    // Read-only property
    public Guid Id => _id;

    // Property with validation
    public string Name
    {
        get => _name;
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Product name is required");
            _name = value;
        }
    }

    // Property with side effects
    public decimal Price
    {
        get => _price;
        set
        {
            if (value <= 0)
                throw new ArgumentException("Price must be positive");

            if (value != _price)
            {
                _price = value;
                _priceHistory.Add(new PriceHistory(value, DateTime.UtcNow));
            }
        }
    }

    public int StockQuantity => _stockQuantity;

    // Defensive copy for collection
    public IReadOnlyList<PriceHistory> PriceHistory => _priceHistory.AsReadOnly();

    // Encapsulated business logic
    public bool TryReserveStock(int quantity)
    {
        if (quantity <= 0)
            throw new ArgumentException("Quantity must be positive");

        if (_stockQuantity >= quantity)
        {
            _stockQuantity -= quantity;
            return true;
        }

        return false;
    }

    public void RestockItems(int quantity)
    {
        if (quantity <= 0)
            throw new ArgumentException("Quantity must be positive");

        _stockQuantity += quantity;
    }

    public decimal GetAveragePrice()
    {
        return _priceHistory.Average(h => h.Price);
    }
}

public record PriceHistory(decimal Price, DateTime ChangedAt);
```

## Data Hiding Patterns

### Information Hiding in Java

```java
// Module pattern with package-private implementation
public class OrderProcessor {
    private final OrderValidator validator;
    private final InventoryService inventory;
    private final PaymentGateway payment;

    public OrderProcessor(
        OrderValidator validator,
        InventoryService inventory,
        PaymentGateway payment
    ) {
        this.validator = validator;
        this.inventory = inventory;
        this.payment = payment;
    }

    // Public interface - what clients need to know
    public OrderResult processOrder(Order order) {
        try {
            validateOrder(order);
            reserveInventory(order);
            processPayment(order);
            return OrderResult.success(order.getId());
        } catch (ValidationException e) {
            return OrderResult.validationError(e.getMessage());
        } catch (InventoryException e) {
            return OrderResult.inventoryError(e.getMessage());
        } catch (PaymentException e) {
            releaseInventory(order);
            return OrderResult.paymentError(e.getMessage());
        }
    }

    // Private implementation - hidden from clients
    private void validateOrder(Order order) {
        if (!validator.isValid(order)) {
            throw new ValidationException("Order validation failed");
        }
    }

    private void reserveInventory(Order order) {
        for (OrderItem item : order.getItems()) {
            if (!inventory.reserve(item.getProductId(), item.getQuantity())) {
                throw new InventoryException("Insufficient inventory");
            }
        }
    }

    private void processPayment(Order order) {
        PaymentRequest request = createPaymentRequest(order);
        PaymentResponse response = payment.charge(request);

        if (!response.isSuccessful()) {
            throw new PaymentException("Payment processing failed");
        }
    }

    private void releaseInventory(Order order) {
        for (OrderItem item : order.getItems()) {
            inventory.release(item.getProductId(), item.getQuantity());
        }
    }

    private PaymentRequest createPaymentRequest(Order order) {
        return PaymentRequest.builder()
            .orderId(order.getId())
            .amount(order.getTotalAmount())
            .customerId(order.getCustomerId())
            .build();
    }
}
```

### Closure-Based Encapsulation in TypeScript

```typescript
// Factory function with closures for private state
function createCounter(initialValue = 0) {
  // Private state - not accessible outside
  let count = initialValue;
  const listeners: Array<(value: number) => void> = [];

  // Private functions
  function notifyListeners(): void {
    listeners.forEach(listener => listener(count));
  }

  // Public interface
  return {
    // Read-only access
    getValue(): number {
      return count;
    },

    // Controlled mutation
    increment(): void {
      count++;
      notifyListeners();
    },

    decrement(): void {
      count--;
      notifyListeners();
    },

    reset(): void {
      count = initialValue;
      notifyListeners();
    },

    // Observer pattern
    subscribe(listener: (value: number) => void): () => void {
      listeners.push(listener);
      // Return unsubscribe function
      return () => {
        const index = listeners.indexOf(listener);
        if (index > -1) {
          listeners.splice(index, 1);
        }
      };
    }
  };
}

// Usage
const counter = createCounter(10);
const unsubscribe = counter.subscribe(value => console.log(`Count: ${value}`));
counter.increment(); // Logs: Count: 11
counter.increment(); // Logs: Count: 12
unsubscribe();
counter.increment(); // No log
```

### Module Pattern in Python

```python
# Module with private implementation details
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CacheEntry:
    """Internal representation - not exported."""
    value: any
    expires_at: datetime
    access_count: int = 0

class Cache:
    """Public cache interface."""

    def __init__(self, max_size: int = 100):
        self.__entries: Dict[str, CacheEntry] = {}
        self.__max_size = max_size
        self.__hits = 0
        self.__misses = 0

    def get(self, key: str) -> Optional[any]:
        """Get value from cache."""
        entry = self.__entries.get(key)

        if entry is None:
            self.__misses += 1
            return None

        if self.__is_expired(entry):
            self.__remove(key)
            self.__misses += 1
            return None

        self.__hits += 1
        entry.access_count += 1
        return entry.value

    def set(self, key: str, value: any, ttl_seconds: int = 3600) -> None:
        """Set value in cache with TTL."""
        if len(self.__entries) >= self.__max_size:
            self.__evict_least_used()

        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        self.__entries[key] = CacheEntry(value, expires_at)

    def delete(self, key: str) -> bool:
        """Remove entry from cache."""
        return self.__remove(key)

    def clear(self) -> None:
        """Clear all cache entries."""
        self.__entries.clear()
        self.__hits = 0
        self.__misses = 0

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'size': len(self.__entries),
            'hits': self.__hits,
            'misses': self.__misses,
            'hit_rate': self.__calculate_hit_rate()
        }

    # Private methods - implementation details
    def __is_expired(self, entry: CacheEntry) -> bool:
        return datetime.now() > entry.expires_at

    def __remove(self, key: str) -> bool:
        if key in self.__entries:
            del self.__entries[key]
            return True
        return False

    def __evict_least_used(self) -> None:
        if not self.__entries:
            return

        least_used = min(
            self.__entries.items(),
            key=lambda item: item[1].access_count
        )
        self.__remove(least_used[0])

    def __calculate_hit_rate(self) -> float:
        total = self.__hits + self.__misses
        return self.__hits / total if total > 0 else 0.0
```

## Access Control Levels

### Java Access Modifiers

```java
// Demonstrating all access levels
public class AccessControlExample {

    // Private - only within this class
    private String secretKey;

    // Package-private (default) - within same package
    String packageData;

    // Protected - within package and subclasses
    protected String inheritableData;

    // Public - everywhere
    public String publicData;

    // Private constructor for factory pattern
    private AccessControlExample(String key) {
        this.secretKey = key;
    }

    // Public factory method
    public static AccessControlExample create(String key) {
        return new AccessControlExample(key);
    }

    // Private helper method
    private boolean validateKey(String key) {
        return key != null && key.length() >= 10;
    }

    // Protected method for subclasses
    protected void performSecureOperation() {
        if (validateKey(secretKey)) {
            // Operation logic
        }
    }

    // Public interface method
    public String getPublicInfo() {
        return "Public information";
    }
}

// Nested class for internal implementation
class InternalHelper {
    // Package-private - only used within package
    static void helperMethod() {
        // Implementation
    }
}
```

### C# Access Levels

```csharp
// Comprehensive access control
public class PaymentProcessor
{
    // Private field - only within class
    private readonly IPaymentGateway _gateway;

    // Protected field - class and derived classes
    protected readonly ILogger _logger;

    // Internal - within same assembly
    internal readonly string AssemblyId;

    // Protected internal - within assembly OR derived classes
    protected internal readonly DateTime CreatedAt;

    // Private protected - within class AND derived classes in same assembly
    private protected readonly string ProcessorId;

    // Public constructor
    public PaymentProcessor(IPaymentGateway gateway, ILogger logger)
    {
        _gateway = gateway ?? throw new ArgumentNullException(nameof(gateway));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        AssemblyId = Guid.NewGuid().ToString();
        CreatedAt = DateTime.UtcNow;
        ProcessorId = GenerateProcessorId();
    }

    // Public method - external interface
    public async Task<PaymentResult> ProcessPaymentAsync(PaymentRequest request)
    {
        ValidateRequest(request);
        return await ExecutePaymentAsync(request);
    }

    // Protected method - for derived classes
    protected virtual void ValidateRequest(PaymentRequest request)
    {
        if (request == null)
            throw new ArgumentNullException(nameof(request));

        if (request.Amount <= 0)
            throw new ArgumentException("Amount must be positive");
    }

    // Private method - internal implementation
    private async Task<PaymentResult> ExecutePaymentAsync(PaymentRequest request)
    {
        _logger.LogInformation($"Processing payment: {request.Id}");

        try
        {
            var response = await _gateway.ChargeAsync(request);
            return ConvertToResult(response);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Payment processing failed");
            return PaymentResult.Failed(ex.Message);
        }
    }

    // Internal method - used by assembly
    internal void ResetGateway()
    {
        // Reset logic
    }

    // Private helper
    private static string GenerateProcessorId()
    {
        return $"PROC-{Guid.NewGuid():N}";
    }

    // Private conversion
    private PaymentResult ConvertToResult(GatewayResponse response)
    {
        return response.Success
            ? PaymentResult.Succeeded(response.TransactionId)
            : PaymentResult.Failed(response.ErrorMessage);
    }
}
```

## Immutability and Encapsulation

### Immutable Objects in Java

```java
// Immutable class - encapsulation through immutability
public final class Money {
    private final BigDecimal amount;
    private final Currency currency;

    private Money(BigDecimal amount, Currency currency) {
        this.amount = amount;
        this.currency = currency;
    }

    public static Money of(BigDecimal amount, Currency currency) {
        Objects.requireNonNull(amount, "Amount required");
        Objects.requireNonNull(currency, "Currency required");
        return new Money(amount, currency);
    }

    public static Money zero(Currency currency) {
        return new Money(BigDecimal.ZERO, currency);
    }

    // All getters return copies or immutable values
    public BigDecimal getAmount() {
        return amount;
    }

    public Currency getCurrency() {
        return currency;
    }

    // Operations return new instances
    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(amount.add(other.amount), currency);
    }

    public Money subtract(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(amount.subtract(other.amount), currency);
    }

    public Money multiply(BigDecimal factor) {
        return new Money(amount.multiply(factor), currency);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Money)) return false;
        Money other = (Money) obj;
        return amount.equals(other.amount) && currency.equals(other.currency);
    }

    @Override
    public int hashCode() {
        return Objects.hash(amount, currency);
    }

    @Override
    public String toString() {
        return String.format("%s %s", currency.getSymbol(), amount);
    }
}
```

## When to Use This Skill

Apply encapsulation principles when:

1. Designing classes and modules with internal state
2. Creating domain objects with business rules
3. Building APIs and public interfaces
4. Protecting object invariants
5. Hiding implementation details
6. Preventing invalid state transitions
7. Managing complex internal structures
8. Implementing data validation
9. Creating defensive copies of mutable objects
10. Controlling access to sensitive data
11. Implementing access control policies
12. Building frameworks and libraries
13. Refactoring procedural code to OOP
14. Designing immutable value objects
15. Creating thread-safe classes

## Best Practices

1. Make fields private by default, expose through methods
2. Use the principle of least privilege for access levels
3. Validate all inputs in public methods
4. Return defensive copies of mutable internal objects
5. Make classes immutable when possible
6. Use final/readonly for fields that don't change
7. Encapsulate collections, never expose them directly
8. Keep implementation details private
9. Use properties/getters for controlled access
10. Implement validation in setters/mutators
11. Group related data and behavior together
12. Hide complexity behind simple interfaces
13. Use package-private/internal for implementation classes
14. Avoid getter/setter pairs for every field
15. Design for change by hiding what might vary

## Common Pitfalls

1. Creating getter/setter for every field (JavaBeans antipattern)
2. Exposing mutable internal collections directly
3. Making fields public "for convenience"
4. Returning references to mutable internal objects
5. Using protected fields instead of protected methods
6. Overusing inheritance to access protected members
7. Ignoring validation in constructors
8. Allowing objects to be created in invalid states
9. Mixing business logic in getters/setters
10. Using static mutable state
11. Forgetting to make defensive copies
12. Exposing implementation details through exceptions
13. Not considering thread safety for mutable state
14. Breaking encapsulation with friend classes
15. Using reflection to access private members

## Resources

- Effective Java by Joshua Bloch (Encapsulation chapters)
- Clean Code by Robert Martin (Objects and Data Structures)
- Design Patterns: Elements of Reusable Object-Oriented Software
- Python Data Model: <https://docs.python.org/3/reference/datamodel.html>
- C# Properties: <https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties>
- Java Access Control: <https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html>
- TypeScript Private Fields: <https://www.typescriptlang.org/docs/handbook/2/classes.html#private>
