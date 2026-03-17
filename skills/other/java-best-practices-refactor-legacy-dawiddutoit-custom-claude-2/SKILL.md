---
name: java-best-practices-refactor-legacy
description: |
  Refactors legacy Java code to modern patterns and best practices. Use when modernizing old Java code, converting to Java 8+ features, refactoring legacy applications, applying design patterns, improving error handling, extracting methods/classes, converting to streams/Optional/records, or migrating from old Java versions. Works with pre-Java 8 code, procedural Java, legacy frameworks, and outdated patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Java Legacy Code Refactoring

## Quick Start

Point to any legacy Java file and receive a refactored version:

```bash
# Refactor a single legacy class
Refactor LegacyUserService.java to modern Java

# Refactor entire legacy package
Modernize all Java files in src/main/java/com/example/legacy/
```

## When to Use

Use this skill when you need to:
- Modernize pre-Java 8 code to use streams, lambdas, and Optional
- Refactor legacy applications to modern Java patterns
- Convert anonymous inner classes to lambda expressions
- Replace imperative loops with Stream API
- Apply SOLID principles to existing code
- Extract methods from long methods (>50 lines)
- Break up god classes into focused components
- Replace null returns with Optional
- Convert to try-with-resources for resource management
- Apply design patterns (Strategy, Builder, etc.)
- Migrate from old frameworks to modern alternatives
- Improve error handling with custom exceptions

## Instructions

### Step 1: Analyze Legacy Code

Read the target file and identify legacy patterns:

**Pre-Java 8 Patterns:**
- Anonymous inner classes instead of lambdas
- Manual iteration instead of Stream API
- Null checks instead of Optional
- Manual resource management instead of try-with-resources
- StringBuffer instead of StringBuilder
- Vector/Hashtable instead of modern collections

**Code Smells:**
- God classes (classes doing too much)
- Long methods (over 50 lines)
- Deep nesting (over 3 levels)
- Code duplication
- Poor naming
- Magic numbers and strings
- Tight coupling

**Anti-Patterns:**
- Singleton abuse
- Service locator pattern
- God objects
- Anemic domain models
- Transaction script pattern

### Step 2: Plan Refactoring Strategy

Prioritize refactorings by impact and risk:

**High Priority (High Impact, Low Risk):**
1. Extract constants for magic numbers/strings
2. Rename poorly named variables/methods
3. Convert to try-with-resources
4. Replace StringBuffer with StringBuilder

**Medium Priority (High Impact, Medium Risk):**
1. Convert loops to Stream API
2. Replace null returns with Optional
3. Extract methods from long methods
4. Apply design patterns

**Low Priority (Medium Impact, High Risk):**
1. Extract classes from god classes
2. Restructure architecture
3. Change public APIs

### Step 3: Apply Modern Java Features

**Lambda Expressions:**
```java
// Before: Anonymous inner class
Comparator<User> comparator = new Comparator<User>() {
    @Override
    public int compare(User u1, User u2) {
        return u1.getName().compareTo(u2.getName());
    }
};

// After: Lambda and method reference
Comparator<User> comparator = Comparator.comparing(User::getName);
```

**Stream API:**
```java
// Before: Imperative loops
List<String> names = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        names.add(user.getName().toUpperCase());
    }
}
Collections.sort(names);

// After: Functional streams
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .map(String::toUpperCase)
    .sorted()
    .toList();
```

**Optional:**
```java
// Before: Null returns
public User findUser(String id) {
    User user = repository.findById(id);
    return user != null ? user : DEFAULT_USER;
}

// After: Optional
public Optional<User> findUser(String id) {
    return repository.findById(id);
}

// Usage
User user = findUser(id).orElse(DEFAULT_USER);
```

**Records (Java 14+):**
```java
// Before: Boilerplate DTO
public class UserDTO {
    private final String name;
    private final String email;
    // constructor, getters, equals, hashCode...
}

// After: Record
public record UserDTO(String name, String email) {}
```

**Try-with-resources:**
```java
// Before: Manual resource management
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("file.txt"));
    // use reader
} finally {
    if (reader != null) {
        try { reader.close(); } catch (IOException e) {}
    }
}

// After: Try-with-resources
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    // use reader
} catch (IOException e) {
    log.error("Failed to read file", e);
}
```

### Step 4: Extract Methods and Classes

**Extract Method:**
```java
// Before: Long method
public void processOrder(Order order) {
    // Validation (20 lines)
    // Calculate total (15 lines)
    // Save order (10 lines)
}

// After: Extracted methods
public void processOrder(Order order) {
    validateOrder(order);
    double total = calculateTotal(order);
    saveOrder(order, total);
}
```

**Extract Class:**
```java
// Before: God class
public class OrderProcessor {
    public void processOrder(Order order) { /* ... */ }
    public void validateOrder(Order order) { /* ... */ }
    public double calculateTotal(Order order) { /* ... */ }
    public void sendEmail(Order order) { /* ... */ }
    public void updateInventory(Order order) { /* ... */ }
}

// After: Separated responsibilities
public class OrderProcessor {
    private final OrderValidator validator;
    private final OrderCalculator calculator;
    private final OrderNotifier notifier;
    private final InventoryManager inventory;

    public void processOrder(Order order) {
        validator.validate(order);
        double total = calculator.calculateTotal(order);
        order.setTotal(total);
        inventory.updateInventory(order);
        notifier.sendOrderConfirmation(order);
    }
}
```

### Step 5: Apply Design Patterns

See [references/design-patterns.md](./references/design-patterns.md) for:
- Strategy pattern for conditional logic
- Builder pattern for complex objects
- Factory pattern for object creation
- Repository pattern for data access

### Step 6: Improve Error Handling

**Replace printStackTrace with Logging:**
```java
// Before
try {
    processPayment(order);
} catch (Exception e) {
    e.printStackTrace();
}

// After
try {
    processPayment(order);
} catch (PaymentException e) {
    log.error("Payment processing failed for order {}", order.getId(), e);
    throw new OrderProcessingException("Failed to process order payment", e);
}
```

**Create Custom Exceptions:**
```java
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long id) {
        super("User not found with ID: " + id);
    }
}
```

## Supporting Files

- **[references/refactoring-examples.md](./references/refactoring-examples.md)** - Comprehensive before/after examples
- **[references/design-patterns.md](./references/design-patterns.md)** - Strategy, Builder, Factory patterns
- **[references/modernization-guide.md](./references/modernization-guide.md)** - Java 8+ feature migration guide

## Requirements

### Tools Needed
- Java 8+ (for lambdas, streams, Optional)
- Java 11+ (for var, improved String methods)
- Java 14+ (for records, switch expressions)
- Java 17+ (for sealed classes, pattern matching)
- Modern IDE with refactoring support

### Dependencies
```xml
<!-- Lombok (for reducing boilerplate) -->
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.30</version>
    <scope>provided</scope>
</dependency>

<!-- SLF4J for logging -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version>2.0.9</version>
</dependency>
```

## Refactoring Checklist

Before refactoring:
- [ ] Ensure tests exist (or create them first)
- [ ] Understand the current behavior completely
- [ ] Create a backup or commit current state

During refactoring:
- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Keep commits small and focused

After refactoring:
- [ ] Verify all tests pass
- [ ] Check for performance regressions
- [ ] Review code with team

## Output Format

When refactoring, provide:

1. **Analysis** of legacy code issues
2. **Refactoring plan** with prioritized changes
3. **Refactored code** with detailed explanations
4. **Before/After comparison** highlighting improvements
5. **Testing recommendations** for validation

## Red Flags to Avoid

- Never refactor code without understanding its purpose
- Never refactor without tests to validate behavior
- Avoid changing multiple patterns simultaneously
- Don't optimize prematurely
- Don't refactor code you can't test
- Never break public APIs without migration strategy

## Notes

- Focus on one refactoring pattern at a time
- Prioritize safety over cleverness
- Maintain backward compatibility when possible
- Document breaking changes clearly
- Run full test suite after each refactoring step
