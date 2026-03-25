---
name: spring-data-jpa
description: Provides patterns to implement persistence layers with Spring Data JPA. Use when creating repositories, configuring entity relationships, writing queries (derived and `@Query`), setting up pagination, database auditing, transactions, UUID primary keys, multiple databases, and database indexing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Spring Data JPA

## Overview

Provides patterns for Spring Data JPA repositories, entity relationships, queries, pagination, auditing, and transactions.

## When to Use

Creating repositories with CRUD operations, entity relationships, `@Query` annotations, pagination, auditing, or UUID primary keys.

## Instructions

### Create Repository Interfaces

To implement a repository interface:

1. **Extend the appropriate repository interface:**
   ```java
   @Repository
   public interface UserRepository extends JpaRepository<User, Long> {
       // Custom methods defined here
   }
   ```

2. **Use derived queries for simple conditions:**
   ```java
   Optional<User> findByEmail(String email);
   List<User> findByStatusOrderByCreatedDateDesc(String status);
   ```

3. **Implement custom queries with `@`Query:**
   ```java
   @Query("SELECT u FROM User u WHERE u.status = :status")
   List<User> findActiveUsers(@Param("status") String status);
   ```

### Configure Entities

1. **Define entities with proper annotations:**
   ```java
   @Entity
   @Table(name = "users")
   public class User {
       @Id
       @GeneratedValue(strategy = GenerationType.IDENTITY)
       private Long id;

       @Column(nullable = false, length = 100)
       private String email;
   }
   ```

2. **Configure relationships using appropriate cascade types:**
   ```java
   @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
   private List<Order> orders = new ArrayList<>();
   ```
   **Validation:** Test cascade behavior with a small dataset before applying to production data. Verify delete operations don't cascade unexpectedly.

3. **Set up database auditing:**
   ```java
   @CreatedDate
   @Column(nullable = false, updatable = false)
   private LocalDateTime createdDate;
   ```

### Apply Query Patterns

1. **Use derived queries for simple conditions**
2. **Use `@`Query for complex queries**
3. **Return Optional<T> for single results**
4. **Use Pageable for pagination**
5. **Apply `@`Modifying for update/delete operations**

### Manage Transactions

1. **Mark read-only operations with `@`Transactional(readOnly = true)**
2. **Use explicit transaction boundaries for modifying operations**
3. **Specify rollback conditions when needed**

### Validate and Optimize

**1. Verify entity configuration:**
- Test cascade behavior in a transaction before production deployment
- Validate bidirectional relationships sync correctly

**2. Optimize query performance:**
- Run `EXPLAIN ANALYZE` on queries against large tables
- If performance issues detected: add indexes → verify with EXPLAIN → repeat
- Use `@EntityGraph` to prevent N+1 queries

**3. Validate pagination:**
- Ensure indexed columns support pagination queries
- Test with large datasets to verify cursor stability

## Examples

### Basic CRUD Repository

```java
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    // Derived query
    List<Product> findByCategory(String category);

    // Custom query
    @Query("SELECT p FROM Product p WHERE p.price > :minPrice")
    List<Product> findExpensiveProducts(@Param("minPrice") BigDecimal minPrice);
}
```

### Pagination Implementation

```java
@Service
public class ProductService {
    private final ProductRepository repository;

    public Page<Product> getProducts(int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("name").ascending());
        return repository.findAll(pageable);
    }
}
```

### Entity with Auditing

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdDate;

    @LastModifiedDate
    private LocalDateTime lastModifiedDate;

    @CreatedBy
    @Column(nullable = false, updatable = false)
    private String createdBy;
}
```

## Best Practices

### Entity Design
- Use constructor injection exclusively (never field injection)
- Prefer immutable fields with `final` modifiers
- Use Java records (16+) or `@Value` for DTOs
- Always provide proper `@Id` and `@GeneratedValue` annotations
- Use explicit `@Table` and `@Column` annotations

### Performance Optimization
- Use appropriate fetch strategies (LAZY vs EAGER)
- Implement pagination for large datasets
- Use database indexes for frequently queried fields
- Consider using `@EntityGraph` to avoid N+1 query problems

### Reference Documentation

For comprehensive examples, detailed patterns, and advanced configurations, see:

- [Examples](references/examples.md) - Complete code examples for common scenarios
- [Reference](references/reference.md) - Detailed patterns and advanced configurations

## Constraints and Warnings

- Never expose JPA entities directly in REST APIs; always use DTOs to prevent lazy loading issues.
- Avoid N+1 query problems by using `@EntityGraph` or `JOIN FETCH` in queries.
- Be cautious with `CascadeType.REMOVE` on large collections as it can cause performance issues.
- Do not use `EAGER` fetch type for collections; it can cause excessive database queries.
- Avoid long-running transactions as they can cause database lock contention.
- Use `@Transactional(readOnly = true)` for read operations to enable optimizations.
- Be aware of the first-level cache; entities may not reflect database changes within the same transaction.
- UUID primary keys can cause index fragmentation; consider using sequential UUIDs or Long IDs.
- Pagination on large datasets requires proper indexing to avoid full table scans.
