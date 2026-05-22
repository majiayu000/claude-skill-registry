---
name: java-best-practices-refactor-legacy
description: |
  Refactor legacy Java code to modern patterns and best practices.
  Use when modernizing old Java code, converting to Java 8+ features, refactoring legacy applications,
  applying design patterns, improving error handling, extracting methods/classes,
  converting to streams/Optional/records, or migrating from old Java versions.
  Works with pre-Java 8 code, procedural Java, legacy frameworks, and outdated patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Java Legacy Code Refactoring

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Requirements](#requirements)
- [Refactoring Checklist](#refactoring-checklist)
- [Output Format](#output-format)
- [Error Handling](#error-handling)

## Purpose

Systematically refactors legacy Java code to modern patterns, converting outdated idioms to Java 8+ features (streams, Optional, lambda expressions), applying SOLID principles, extracting cohesive classes and methods, and improving overall code maintainability.

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

## Quick Start
Point to any legacy Java file and receive a refactored version:

```bash
# Refactor a single legacy class
Refactor LegacyUserService.java to modern Java

# Refactor entire legacy package
Modernize all Java files in src/main/java/com/example/legacy/
```

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
// Before
Comparator<User> comparator = new Comparator<User>() {
    @Override
    public int compare(User u1, User u2) {
        return u1.getName().compareTo(u2.getName());
    }
};

// After
Comparator<User> comparator = (u1, u2) ->
    u1.getName().compareTo(u2.getName());
// Or even better
Comparator<User> comparator = Comparator.comparing(User::getName);
```

**Stream API:**
```java
// Before
List<String> names = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        names.add(user.getName().toUpperCase());
    }
}
Collections.sort(names);

// After
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .map(String::toUpperCase)
    .sorted()
    .toList();
```

**Optional:**
```java
// Before
public User findUser(String id) {
    User user = repository.findById(id);
    if (user == null) {
        return DEFAULT_USER;
    }
    return user;
}

// After
public Optional<User> findUser(String id) {
    return repository.findById(id);
}

// Usage
User user = findUser(id).orElse(DEFAULT_USER);
```

**Records (Java 14+):**
```java
// Before
public class UserDTO {
    private final String name;
    private final String email;

    public UserDTO(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public String getName() { return name; }
    public String getEmail() { return email; }

    @Override
    public boolean equals(Object o) { /* ... */ }
    @Override
    public int hashCode() { /* ... */ }
}

// After
public record UserDTO(String name, String email) {}
```

**Try-with-resources:**
```java
// Before
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("file.txt"));
    String line = reader.readLine();
} catch (IOException e) {
    e.printStackTrace();
} finally {
    if (reader != null) {
        try {
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

// After
try (BufferedReader reader = new BufferedReader(
        new FileReader("file.txt"))) {
    String line = reader.readLine();
} catch (IOException e) {
    log.error("Failed to read file", e);
    throw new FileReadException("Could not read file.txt", e);
}
```

### Step 4: Extract Methods and Classes

**Extract Method:**
```java
// Before
public void processOrder(Order order) {
    // Validate order (20 lines)
    if (order == null) { /* ... */ }
    if (order.getItems().isEmpty()) { /* ... */ }
    // ... more validation

    // Calculate total (15 lines)
    double total = 0;
    for (OrderItem item : order.getItems()) {
        // ... calculation logic
    }

    // Save order (10 lines)
    // ... saving logic
}

// After
public void processOrder(Order order) {
    validateOrder(order);
    double total = calculateTotal(order);
    saveOrder(order, total);
}

private void validateOrder(Order order) {
    if (order == null) {
        throw new IllegalArgumentException("Order cannot be null");
    }
    if (order.getItems().isEmpty()) {
        throw new IllegalArgumentException("Order must have items");
    }
}

private double calculateTotal(Order order) {
    return order.getItems().stream()
        .mapToDouble(item -> item.getPrice() * item.getQuantity())
        .sum();
}

private void saveOrder(Order order, double total) {
    order.setTotal(total);
    orderRepository.save(order);
}
```

**Extract Class:**
```java
// Before - God class
public class OrderProcessor {
    public void processOrder(Order order) { /* ... */ }
    public void validateOrder(Order order) { /* ... */ }
    public double calculateTotal(Order order) { /* ... */ }
    public void sendEmail(Order order) { /* ... */ }
    public void generateInvoice(Order order) { /* ... */ }
    public void updateInventory(Order order) { /* ... */ }
}

// After - Separated responsibilities
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

**Replace Conditional with Polymorphism:**
```java
// Before
public double calculateShipping(Order order) {
    if (order.getType().equals("STANDARD")) {
        return order.getWeight() * 0.5;
    } else if (order.getType().equals("EXPRESS")) {
        return order.getWeight() * 1.5;
    } else if (order.getType().equals("OVERNIGHT")) {
        return order.getWeight() * 3.0;
    }
    return 0;
}

// After
public interface ShippingStrategy {
    double calculateCost(double weight);
}

public class StandardShipping implements ShippingStrategy {
    public double calculateCost(double weight) {
        return weight * 0.5;
    }
}

public class ExpressShipping implements ShippingStrategy {
    public double calculateCost(double weight) {
        return weight * 1.5;
    }
}

// Usage with enum and strategy
public enum ShippingType {
    STANDARD(new StandardShipping()),
    EXPRESS(new ExpressShipping()),
    OVERNIGHT(new OvernightShipping());

    private final ShippingStrategy strategy;

    ShippingType(ShippingStrategy strategy) {
        this.strategy = strategy;
    }

    public double calculateCost(double weight) {
        return strategy.calculateCost(weight);
    }
}
```

**Builder Pattern for Complex Objects:**
```java
// Before
public class User {
    private String name;
    private String email;
    private String phone;
    private Address address;
    private List<Role> roles;

    public User(String name, String email, String phone,
                Address address, List<Role> roles) {
        // Messy constructor with many parameters
    }
}

// After
public class User {
    private final String name;
    private final String email;
    private final String phone;
    private final Address address;
    private final List<Role> roles;

    private User(Builder builder) {
        this.name = builder.name;
        this.email = builder.email;
        this.phone = builder.phone;
        this.address = builder.address;
        this.roles = builder.roles;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private String name;
        private String email;
        private String phone;
        private Address address;
        private List<Role> roles = new ArrayList<>();

        public Builder name(String name) {
            this.name = name;
            return this;
        }

        public Builder email(String email) {
            this.email = email;
            return this;
        }

        // ... other setters

        public User build() {
            return new User(this);
        }
    }
}
```

### Step 6: Improve Error Handling

**Replace printStackTrace with Proper Logging:**
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
    log.error("Payment processing failed for order {}",
        order.getId(), e);
    throw new OrderProcessingException(
        "Failed to process order payment", e);
}
```

**Create Custom Exceptions:**
```java
// Before
if (user == null) {
    throw new RuntimeException("User not found");
}

// After
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String userId) {
        super("User not found with ID: " + userId);
    }
}

if (user == null) {
    throw new UserNotFoundException(userId);
}
```

### Step 7: Add Proper Logging

```java
// Before
public void processOrder(Order order) {
    System.out.println("Processing order: " + order.getId());
    // ... processing
    System.out.println("Order processed");
}

// After
@Slf4j
public class OrderService {
    public void processOrder(Order order) {
        log.info("Processing order: orderId={}", order.getId());
        try {
            // ... processing
            log.info("Order processed successfully: orderId={}",
                order.getId());
        } catch (Exception e) {
            log.error("Failed to process order: orderId={}",
                order.getId(), e);
            throw e;
        }
    }
}
```

## Examples

### Example 1: Refactor Legacy Data Access Code

**Before:**
```java
public class UserDAO {
    public User getUserById(int id) {
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;
        User user = null;

        try {
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
            stmt.setInt(1, id);
            rs = stmt.executeQuery();

            if (rs.next()) {
                user = new User();
                user.setId(rs.getInt("id"));
                user.setName(rs.getString("name"));
                user.setEmail(rs.getString("email"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

        return user;
    }

    public List<User> getAllUsers() {
        List<User> users = new ArrayList<User>();
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            stmt = conn.createStatement();
            rs = stmt.executeQuery("SELECT * FROM users");

            while (rs.next()) {
                User user = new User();
                user.setId(rs.getInt("id"));
                user.setName(rs.getString("name"));
                user.setEmail(rs.getString("email"));
                users.add(user);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

        return users;
    }
}
```

**After:**
```java
@Repository
@RequiredArgsConstructor
@Slf4j
public class UserRepository {
    private final JdbcTemplate jdbcTemplate;

    private static final RowMapper<User> USER_ROW_MAPPER = (rs, rowNum) ->
        User.builder()
            .id(rs.getInt("id"))
            .name(rs.getString("name"))
            .email(rs.getString("email"))
            .build();

    public Optional<User> findById(int id) {
        log.debug("Finding user by id: {}", id);
        try {
            User user = jdbcTemplate.queryForObject(
                "SELECT * FROM users WHERE id = ?",
                USER_ROW_MAPPER,
                id
            );
            return Optional.ofNullable(user);
        } catch (EmptyResultDataAccessException e) {
            log.debug("User not found with id: {}", id);
            return Optional.empty();
        } catch (DataAccessException e) {
            log.error("Database error while fetching user: id={}", id, e);
            throw new UserRepositoryException(
                "Failed to fetch user with id: " + id, e);
        }
    }

    public List<User> findAll() {
        log.debug("Finding all users");
        try {
            return jdbcTemplate.query(
                "SELECT * FROM users",
                USER_ROW_MAPPER
            );
        } catch (DataAccessException e) {
            log.error("Database error while fetching all users", e);
            throw new UserRepositoryException(
                "Failed to fetch users", e);
        }
    }
}
```

**Improvements:**
- Replaced manual JDBC with Spring JdbcTemplate
- Added Optional for nullable returns
- Proper exception handling with logging
- Extracted RowMapper for reusability
- Used builder pattern for User construction
- Added SLF4J logging
- No resource leaks (JdbcTemplate handles it)

### Example 2: Refactor Procedural Service Logic

**Before:**
```java
public class OrderService {
    private OrderDAO orderDAO = new OrderDAO();
    private InventoryDAO inventoryDAO = new InventoryDAO();

    public boolean processOrder(int orderId) {
        Order order = orderDAO.getOrderById(orderId);
        if (order == null) {
            System.out.println("Order not found: " + orderId);
            return false;
        }

        // Check inventory
        List<OrderItem> items = order.getItems();
        for (int i = 0; i < items.size(); i++) {
            OrderItem item = items.get(i);
            int available = inventoryDAO.getAvailableQuantity(
                item.getProductId());
            if (available < item.getQuantity()) {
                System.out.println("Insufficient inventory for product: "
                    + item.getProductId());
                return false;
            }
        }

        // Calculate total
        double total = 0.0;
        for (int i = 0; i < items.size(); i++) {
            OrderItem item = items.get(i);
            total += item.getPrice() * item.getQuantity();
        }

        // Apply discount
        if (total > 100) {
            total = total * 0.9;
        }

        order.setTotal(total);
        order.setStatus("CONFIRMED");

        // Update inventory
        for (int i = 0; i < items.size(); i++) {
            OrderItem item = items.get(i);
            inventoryDAO.reduceQuantity(item.getProductId(),
                item.getQuantity());
        }

        orderDAO.updateOrder(order);

        System.out.println("Order processed: " + orderId);
        return true;
    }
}
```

**After:**
```java
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {
    private final OrderRepository orderRepository;
    private final InventoryService inventoryService;
    private final DiscountCalculator discountCalculator;

    private static final double DISCOUNT_THRESHOLD = 100.0;

    @Transactional
    public Order processOrder(int orderId) {
        log.info("Processing order: orderId={}", orderId);

        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        validateInventory(order);
        applyPricingAndDiscounts(order);
        updateInventory(order);
        confirmOrder(order);

        log.info("Order processed successfully: orderId={}", orderId);
        return order;
    }

    private void validateInventory(Order order) {
        List<OrderItem> unavailableItems = order.getItems().stream()
            .filter(item -> !inventoryService.isAvailable(
                item.getProductId(), item.getQuantity()))
            .toList();

        if (!unavailableItems.isEmpty()) {
            log.warn("Insufficient inventory for order: orderId={}, items={}",
                order.getId(), unavailableItems);
            throw new InsufficientInventoryException(unavailableItems);
        }
    }

    private void applyPricingAndDiscounts(Order order) {
        double subtotal = order.getItems().stream()
            .mapToDouble(item -> item.getPrice() * item.getQuantity())
            .sum();

        double discount = discountCalculator.calculateDiscount(
            subtotal, order.getCustomer());
        double total = subtotal - discount;

        order.setSubtotal(subtotal);
        order.setDiscount(discount);
        order.setTotal(total);
    }

    private void updateInventory(Order order) {
        order.getItems().forEach(item ->
            inventoryService.reduceQuantity(
                item.getProductId(),
                item.getQuantity()
            )
        );
    }

    private void confirmOrder(Order order) {
        order.setStatus(OrderStatus.CONFIRMED);
        order.setConfirmedAt(LocalDateTime.now());
        orderRepository.save(order);
    }
}

@Component
public class DiscountCalculator {
    private static final double VOLUME_DISCOUNT_RATE = 0.1;
    private static final double VOLUME_THRESHOLD = 100.0;

    public double calculateDiscount(double subtotal, Customer customer) {
        double discount = 0.0;

        // Volume discount
        if (subtotal > VOLUME_THRESHOLD) {
            discount += subtotal * VOLUME_DISCOUNT_RATE;
        }

        // Customer loyalty discount
        if (customer.isVIP()) {
            discount += subtotal * customer.getLoyaltyRate();
        }

        return discount;
    }
}
```

**Improvements:**
- Dependency injection instead of direct instantiation
- Stream API for collection processing
- Extracted methods for single responsibilities
- Extracted DiscountCalculator class
- Proper exception handling with custom exceptions
- SLF4J logging instead of System.out
- Optional for null handling
- Constants for magic numbers
- @Transactional for data consistency
- Modern Java features (lambdas, method references)

### Example 3: Refactor Complex Conditionals

**Before:**
```java
public String getUserStatus(User user) {
    if (user != null) {
        if (user.isActive()) {
            if (user.getLastLoginDate() != null) {
                long daysSinceLogin = ChronoUnit.DAYS.between(
                    user.getLastLoginDate(), LocalDate.now());
                if (daysSinceLogin < 30) {
                    return "ACTIVE_RECENT";
                } else if (daysSinceLogin < 90) {
                    return "ACTIVE_DORMANT";
                } else {
                    return "ACTIVE_INACTIVE";
                }
            } else {
                return "ACTIVE_NEVER_LOGGED_IN";
            }
        } else {
            if (user.getDeactivatedDate() != null) {
                return "DEACTIVATED";
            } else {
                return "SUSPENDED";
            }
        }
    } else {
        return "UNKNOWN";
    }
}
```

**After:**
```java
public enum UserStatus {
    ACTIVE_RECENT("Active and recently used"),
    ACTIVE_DORMANT("Active but rarely used"),
    ACTIVE_INACTIVE("Active but not used recently"),
    ACTIVE_NEVER_LOGGED_IN("Active but never logged in"),
    DEACTIVATED("Account deactivated"),
    SUSPENDED("Account suspended"),
    UNKNOWN("Status unknown");

    private final String description;

    UserStatus(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}

public class UserStatusCalculator {
    private static final long RECENT_LOGIN_DAYS = 30;
    private static final long DORMANT_LOGIN_DAYS = 90;

    public UserStatus calculateStatus(User user) {
        if (user == null) {
            return UserStatus.UNKNOWN;
        }

        if (user.isActive()) {
            return calculateActiveStatus(user);
        } else {
            return calculateInactiveStatus(user);
        }
    }

    private UserStatus calculateActiveStatus(User user) {
        return Optional.ofNullable(user.getLastLoginDate())
            .map(this::getStatusByLastLogin)
            .orElse(UserStatus.ACTIVE_NEVER_LOGGED_IN);
    }

    private UserStatus getStatusByLastLogin(LocalDate lastLogin) {
        long daysSinceLogin = ChronoUnit.DAYS.between(
            lastLogin, LocalDate.now());

        if (daysSinceLogin < RECENT_LOGIN_DAYS) {
            return UserStatus.ACTIVE_RECENT;
        } else if (daysSinceLogin < DORMANT_LOGIN_DAYS) {
            return UserStatus.ACTIVE_DORMANT;
        } else {
            return UserStatus.ACTIVE_INACTIVE;
        }
    }

    private UserStatus calculateInactiveStatus(User user) {
        return Optional.ofNullable(user.getDeactivatedDate())
            .map(date -> UserStatus.DEACTIVATED)
            .orElse(UserStatus.SUSPENDED);
    }
}
```

**Improvements:**
- Reduced nesting from 4 levels to 1-2 levels
- Extracted enum for user statuses
- Extracted class for status calculation logic
- Used Optional to handle null dates
- Named constants for magic numbers
- Extracted methods for each status category
- More testable and maintainable

## Requirements

### Tools Needed
- Java 8+ (for lambdas, streams, Optional)
- Java 11+ (for var, improved String methods)
- Java 14+ (for records, switch expressions)
- Java 17+ (for sealed classes, pattern matching)
- Modern IDE with refactoring support (IntelliJ IDEA, Eclipse, VS Code)

### Dependencies (if applicable)
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
- [ ] Identify all dependencies and usages
- [ ] Create a backup or commit current state

During refactoring:
- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Keep commits small and focused
- [ ] Update documentation as needed

After refactoring:
- [ ] Verify all tests pass
- [ ] Check for performance regressions
- [ ] Review code with team
- [ ] Update API documentation if public API changed

## Output Format

When refactoring, provide:

1. **Analysis** of legacy code issues
2. **Refactoring plan** with prioritized changes
3. **Refactored code** with detailed explanations
4. **Before/After comparison** highlighting improvements
5. **Testing recommendations** for validation

Example output structure:
```markdown
## Refactoring Analysis: [ClassName]

**Legacy Issues Identified:**
- Issue 1: Manual iteration instead of streams
- Issue 2: Null returns instead of Optional
- Issue 3: God class with 15 responsibilities

**Refactoring Plan:**
1. Extract 3 classes from god class
2. Convert loops to streams
3. Replace null with Optional
4. Add proper logging
5. Apply builder pattern

**Refactored Code:**
[Show refactored code with comments]

**Improvements:**
- 40% reduction in lines of code
- Better testability with dependency injection
- Improved readability with modern Java features
- SOLID principles applied
```

## Error Handling

If refactoring cannot be completed safely:

1. **No tests exist:** Recommend creating characterization tests first
2. **Breaking change required:** Explain implications and migration path
3. **Complex dependencies:** Request additional context or files
4. **Unclear behavior:** Ask for clarification on expected behavior

Never refactor code without understanding its purpose and having tests to validate behavior.
