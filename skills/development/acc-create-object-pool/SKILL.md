---
name: acc-create-object-pool
description: Generates Object Pool pattern for PHP 8.5. Creates reusable object containers for expensive resources like connections. Includes unit tests.
---

# Object Pool Pattern Generator

Creates Object Pool pattern infrastructure for managing reusable expensive objects.

## When to Use

| Scenario | Example |
|----------|---------|
| Expensive creation | Database connections |
| Limited resources | HTTP client handles |
| Connection reuse | Socket connections |
| Memory management | Large object caching |

## Component Characteristics

### PoolInterface
- Acquire/release semantics
- Pool lifecycle management
- Capacity configuration

### Pool Implementation
- Manages available objects
- Creates on demand
- Recycles returned objects

### Poolable Objects
- Resettable state
- Validate before reuse
- Track usage metrics

---

## Generation Process

### Step 1: Generate Core Pool Components

**Path:** `src/Infrastructure/Pool/`

1. `PoolInterface.php` — Generic pool contract with acquire/release
2. `PoolConfig.php` — Configuration value object (min/max size, timeouts)
3. `PoolableInterface.php` — Contract for poolable objects (reset, isValid, close)
4. `ObjectPool.php` — Generic pool implementation
5. `PooledObject.php` — Wrapper tracking usage metrics
6. `PoolExhaustedException.php` — Exception for exhausted pool
7. `InvalidPoolObjectException.php` — Exception for invalid objects

### Step 2: Generate Specialized Pool (if needed)

**Path:** `src/Infrastructure/{Domain}/`

1. `{Type}Pool.php` — Specialized pool (ConnectionPool, HttpClientPool)
2. `Poolable{Type}.php` — Poolable implementation for specific resource

### Step 3: Generate Tests

**Path:** `tests/Unit/Infrastructure/Pool/`

1. `ObjectPoolTest.php` — Core pool functionality tests
2. `{Type}PoolTest.php` — Specialized pool tests

---

## File Placement

| Component | Path |
|-----------|------|
| Pool Interface | `src/Infrastructure/Pool/` |
| Pool Implementation | `src/Infrastructure/Pool/` |
| Specialized Pools | `src/Infrastructure/{Domain}/` |
| Unit Tests | `tests/Unit/Infrastructure/Pool/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `PoolInterface` | `PoolInterface` |
| Implementation | `ObjectPool` | `ObjectPool` |
| Poolable Interface | `PoolableInterface` | `PoolableInterface` |
| Config | `PoolConfig` | `PoolConfig` |
| Wrapper | `PooledObject` | `PooledObject` |
| Specialized Pool | `{Type}Pool` | `ConnectionPool` |
| Test | `{ClassName}Test` | `ObjectPoolTest` |

---

## Quick Template Reference

### PoolInterface

```php
/**
 * @template T
 */
interface PoolInterface
{
    /** @return T */
    public function acquire(): mixed;
    /** @param T $object */
    public function release(mixed $object): void;
    public function getAvailableCount(): int;
    public function getActiveCount(): int;
    public function getMaxSize(): int;
    public function clear(): void;
}
```

### PoolableInterface

```php
interface PoolableInterface
{
    public function reset(): void;
    public function isValid(): bool;
    public function close(): void;
}
```

### PoolConfig

```php
final readonly class PoolConfig
{
    public function __construct(
        public int $minSize = 0,
        public int $maxSize = 10,
        public int $maxWaitTimeMs = 5000,
        public int $idleTimeoutSeconds = 300,
        public bool $validateOnAcquire = true,
        public bool $validateOnRelease = false
    );

    public static function default(): self;
    public static function forDatabase(): self;
    public static function forHttpClients(): self;
}
```

---

## Usage Example

```php
// Create pool
$pool = new ObjectPool(
    name: 'database',
    factory: fn() => $connectionFactory->create(),
    config: PoolConfig::forDatabase(),
    logger: $logger
);

// Acquire and release
$connection = $pool->acquire();
try {
    $result = $connection->query('SELECT ...');
} finally {
    $pool->release($connection);
}

// Or use helper
$result = $connectionPool->execute(fn($conn) => $conn->query('SELECT ...'));
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| No Validation | Returning broken objects | Validate on acquire |
| No Reset | State leaks between uses | Call reset() on release |
| No Timeout | Infinite wait | Set maxWaitTime |
| Unbounded Pool | Memory exhaustion | Set maxSize |
| Not Releasing | Pool exhaustion | Use try/finally |
| Wrong Scope | Per-request pools | Use singleton/shared pool |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — All component templates
- `references/examples.md` — ConnectionPool, HttpClientPool examples and tests
