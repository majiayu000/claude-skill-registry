---
name: code-translation
description: "Convert code between programming languages while preserving functionality and semantics. Use when: (1) Translating functions, classes, or modules between languages (Python, JavaScript/TypeScript, Java, Go, Rust, C/C++), (2) Migrating entire projects to a different language, (3) Need idiomatic translation that follows target language conventions, (4) Converting between different paradigms (OOP to functional, etc.), (5) Porting legacy code to modern languages. Provides language-specific patterns, idiomatic translation guides, and project migration strategies."
---

# Code Translation

Convert code between programming languages while preserving functionality, adapting to target language idioms and best practices.

## Translation Workflow

### 1. Analyze Source Code

Understand what the code does:
- Core functionality and algorithms
- Dependencies and external libraries
- Language-specific features used
- Performance characteristics

### 2. Choose Translation Strategy

**Direct Translation**: Literal conversion maintaining structure
- **Use for**: Simple algorithms, data transformations, utility functions
- **Pros**: Faster, easier to verify correctness
- **Cons**: May not be idiomatic in target language

**Idiomatic Translation**: Adapt to target language patterns
- **Use for**: Production code, public APIs, long-term maintenance
- **Pros**: Native-feeling code, better performance, maintainable
- **Cons**: Takes longer, requires deep language knowledge

**Recommended**: Start with direct translation, then refine to idiomatic.

### 3. Translate Code

Perform the translation following language patterns and conventions.

### 4. Verify Correctness

Ensure translated code behaves identically to source:
- Port existing tests
- Add behavioral tests
- Compare outputs on same inputs

## Quick Translation Examples

### Python → JavaScript

**Source (Python)**
```python
def calculate_total(items):
    """Calculate total price with tax."""
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    tax = subtotal * 0.08
    return subtotal + tax

# Usage
items = [
    {'name': 'Widget', 'price': 10.0, 'quantity': 2},
    {'name': 'Gadget', 'price': 15.0, 'quantity': 1}
]
total = calculate_total(items)
```

**Target (JavaScript)**
```javascript
function calculateTotal(items) {
    // Calculate total price with tax
    const subtotal = items.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
    );
    const tax = subtotal * 0.08;
    return subtotal + tax;
}

// Usage
const items = [
    { name: 'Widget', price: 10.0, quantity: 2 },
    { name: 'Gadget', price: 15.0, quantity: 1 }
];
const total = calculateTotal(items);
```

### JavaScript → Python

**Source (JavaScript)**
```javascript
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Failed to fetch user: ${error.message}`);
        return null;
    }
}
```

**Target (Python)**
```python
import aiohttp
import logging

async def fetch_user_data(user_id: int) -> dict | None:
    """Fetch user data from API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'/api/users/{user_id}') as response:
                if not response.ok:
                    raise ValueError(f'HTTP {response.status}')
                return await response.json()
    except Exception as e:
        logging.error(f'Failed to fetch user: {e}')
        return None
```

### Java → Go

**Source (Java)**
```java
public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    public Optional<User> findById(Long id) {
        return repository.findById(id);
    }

    public List<User> findAll() {
        return repository.findAll();
    }
}
```

**Target (Go)**
```go
type UserService struct {
    repository UserRepository
}

func NewUserService(repository UserRepository) *UserService {
    return &UserService{repository: repository}
}

func (s *UserService) FindById(id int64) (*User, error) {
    return s.repository.FindById(id)
}

func (s *UserService) FindAll() ([]User, error) {
    return s.repository.FindAll()
}
```

## Common Translation Patterns

### Data Structures

**Lists/Arrays**
```python
# Python
numbers = [1, 2, 3]
numbers.append(4)
```
```javascript
// JavaScript
const numbers = [1, 2, 3];
numbers.push(4);
```
```go
// Go
numbers := []int{1, 2, 3}
numbers = append(numbers, 4)
```

**Dictionaries/Maps**
```python
# Python
user = {"name": "Alice", "age": 30}
```
```javascript
// JavaScript
const user = { name: "Alice", age: 30 };
```
```go
// Go
user := map[string]interface{}{
    "name": "Alice",
    "age":  30,
}
```

### Error Handling

**Exceptions → Error Returns**
```python
# Python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```
```go
// Go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("cannot divide by zero")
    }
    return a / b, nil
}
```

**Error Returns → Exceptions**
```go
// Go
result, err := divide(10, 0)
if err != nil {
    return err
}
```
```python
# Python
try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")
```

### Async/Concurrency

**Python asyncio → JavaScript async/await**
```python
# Python
async def fetch_all(urls):
    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)
```
```javascript
// JavaScript
async function fetchAll(urls) {
    const promises = urls.map(url => fetch(url));
    return await Promise.all(promises);
}
```

**JavaScript Promises → Go Goroutines**
```javascript
// JavaScript
const results = await Promise.all([
    fetchUser(1),
    fetchUser(2),
    fetchUser(3)
]);
```
```go
// Go
var wg sync.WaitGroup
results := make([]*User, 3)

for i := 1; i <= 3; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        results[id-1] = fetchUser(id)
    }(i)
}
wg.Wait()
```

## Translation Decision Tree

```
Is this a complete project migration?
├─ Yes → See [project_migration.md](references/project_migration.md)
│         Follow 8-phase migration process
│
└─ No → Is this a function/class/module?
        │
        ├─ Single function
        │  ├─ Simple logic? → Direct translation
        │  └─ Complex logic? → Idiomatic translation
        │
        ├─ Class with methods
        │  ├─ Does target language have classes?
        │  │  ├─ Yes → Translate class structure
        │  │  └─ No → Convert to module/functions
        │
        └─ Full module
           └─ Translate file by file
              Consider dependencies first
```

## Language-Specific Guidance

### For Idiomatic Translation

See **[idiomatic_guide.md](references/idiomatic_guide.md)** for:
- Language-specific idioms and patterns
- Naming conventions (snake_case, camelCase, PascalCase)
- Standard library usage
- Anti-patterns to avoid
- Community style guides

### For Specific Language Pairs

See **[language_patterns.md](references/language_patterns.md)** for detailed patterns:
- Python ↔ JavaScript/TypeScript
- Java ↔ Python
- Python ↔ Go
- C++ ↔ Rust
- TypeScript ↔ Go
- Common patterns across all languages

### For Project Migration

See **[project_migration.md](references/project_migration.md)** for:
- 8-phase migration process
- Dependency mapping
- Build system translation
- Testing strategies
- Deployment configuration
- Incremental migration approaches

## Best Practices

### 1. Preserve Behavior, Not Structure

Focus on what the code does, not how it's written:
```python
# Python (imperative)
total = 0
for item in items:
    total += item.price
```
```javascript
// JavaScript (functional - different structure, same behavior)
const total = items.reduce((sum, item) => sum + item.price, 0);
```

### 2. Use Target Language Features

Don't fight the language - embrace its strengths:
```python
# Python - use list comprehensions
squares = [x**2 for x in range(10)]

# Not: Java-style loop
squares = []
for x in range(10):
    squares.append(x**2)
```

### 3. Maintain Type Safety When Possible

Add type hints/annotations in statically typed languages:
```python
# Python source (dynamic)
def greet(name):
    return f"Hello, {name}"
```
```typescript
// TypeScript (add types)
function greet(name: string): string {
    return `Hello, ${name}`;
}
```

### 4. Handle Library Differences

Map to equivalent libraries or implement abstractions:
```python
# Python using requests
import requests
response = requests.get(url)
data = response.json()
```
```javascript
// JavaScript using fetch
const response = await fetch(url);
const data = await response.json();
```

### 5. Test Rigorously

Verify translated code behaves identically:
```python
# Port tests alongside code
def test_calculate_total():
    items = [{"price": 10, "quantity": 2}]
    assert calculate_total(items) == 21.6  # 20 + 8% tax
```
```javascript
// Same test in target language
test('calculateTotal', () => {
    const items = [{ price: 10, quantity: 2 }];
    expect(calculateTotal(items)).toBe(21.6);
});
```

## Translation Checklist

### Before Translation
- [ ] Understand source code functionality
- [ ] Identify dependencies and library equivalents
- [ ] Choose translation strategy (direct vs idiomatic)
- [ ] Set up target project structure

### During Translation
- [ ] Translate core logic first
- [ ] Adapt to target language idioms
- [ ] Handle error handling differences
- [ ] Map data structures appropriately
- [ ] Convert async/concurrency patterns
- [ ] Translate comments and documentation

### After Translation
- [ ] Port or create tests
- [ ] Verify behavioral equivalence
- [ ] Code review for idioms
- [ ] Performance testing
- [ ] Update documentation
- [ ] Add type hints/annotations if applicable

## Common Pitfalls

### 1. Literal Translation
❌ Translating line-by-line without adapting
✅ Adapting to target language patterns

### 2. Ignoring Language Safety
❌ Using `any`/`interface{}`/`Object` everywhere
✅ Proper typing and error handling

### 3. Wrong Abstraction Level
❌ Translating implementation details
✅ Translating behavior and intent

### 4. Missing Edge Cases
❌ Assuming same behavior for edge cases
✅ Testing boundary conditions

### 5. Performance Blindness
❌ Ignoring performance characteristics
✅ Profiling and optimizing for target language

## Example: Complete Translation

**Python Source**
```python
class Calculator:
    """Simple calculator with memory."""

    def __init__(self):
        self.memory = 0

    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self.memory = result
        return result

    def recall(self) -> float:
        """Recall last result."""
        return self.memory

    def clear(self):
        """Clear memory."""
        self.memory = 0
```

**TypeScript Translation**
```typescript
/**
 * Simple calculator with memory.
 */
class Calculator {
    private memory: number = 0;

    /**
     * Add two numbers.
     */
    add(a: number, b: number): number {
        const result = a + b;
        this.memory = result;
        return result;
    }

    /**
     * Recall last result.
     */
    recall(): number {
        return this.memory;
    }

    /**
     * Clear memory.
     */
    clear(): void {
        this.memory = 0;
    }
}
```

**Go Translation (Idiomatic)**
```go
// Calculator is a simple calculator with memory.
type Calculator struct {
    memory float64
}

// NewCalculator creates a new calculator.
func NewCalculator() *Calculator {
    return &Calculator{memory: 0}
}

// Add two numbers and store result in memory.
func (c *Calculator) Add(a, b float64) float64 {
    result := a + b
    c.memory = result
    return result
}

// Recall returns the last result.
func (c *Calculator) Recall() float64 {
    return c.memory
}

// Clear resets the memory to zero.
func (c *Calculator) Clear() {
    c.memory = 0
}
```
