---
name: spring-data-jpa
description: Implement persistence layers with Spring Data JPA. Use when creating repositories, configuring entity relationships, writing queries (derived and @Query), setting up pagination, database auditing, transactions, UUID primary keys, multiple databases, and database indexing. Covers repository interfaces, JPA entities, custom queries, relationships, and performance optimization patterns.
allowed-tools: Read, Write, Bash, Grep
category: backend
tags: [spring-data, jpa, database, hibernate, orm, persistence]
version: 1.2.0
---

# Spring Data JPA

## Overview

To implement persistence layers with Spring Data JPA, create repository interfaces that provide automatic CRUD operations, entity relationships, query methods, and advanced features like pagination, auditing, and performance optimization.

## When to Use

Use this Skill when:
- Implementing repository interfaces with automatic CRUD operations
- Creating entities with relationships (one-to-one, one-to-many, many-to-many)
- Writing queries using derived method names or custom @Query annotations
- Setting up pagination and sorting for large datasets
- Implementing database auditing with timestamps and user tracking
- Configuring transactions and exception handling
- Using UUID as primary keys for distributed systems
- Optimizing performance with database indexes
- Setting up multiple database configurations

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

3. **Implement custom queries with @Query:**
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

3. **Set up database auditing:**
   ```java
   @CreatedDate
   @Column(nullable = false, updatable = false)
   private LocalDateTime createdDate;
   ```

### Apply Query Patterns

1. **Use derived queries for simple conditions**
2. **Use @Query for complex queries**
3. **Return Optional<T> for single results**
4. **Use Pageable for pagination**
5. **Apply @Modifying for update/delete operations**

### Manage Transactions

1. **Mark read-only operations with @Transactional(readOnly = true)**
2. **Use explicit transaction boundaries for modifying operations**
3. **Specify rollback conditions when needed**

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

### Repository Queries
- Use derived queries for simple conditions
- Use `@Query` for complex queries to avoid long method names
- Always use `@Param` for query parameters
- Return `Optional<T>` for single results
- Apply `@Transactional` on modifying operations

### Performance Optimization
- Use appropriate fetch strategies (LAZY vs EAGER)
- Implement pagination for large datasets
- Use database indexes for frequently queried fields
- Consider using `@EntityGraph` to avoid N+1 query problems

### Transaction Management
- Mark read-only operations with `@Transactional(readOnly = true)`
- Use explicit transaction boundaries
- Avoid long-running transactions
- Specify rollback conditions when needed

## Reference Documentation

For comprehensive examples, detailed patterns, and advanced configurations, see:

- [Examples](references/examples.md) - Complete code examples for common scenarios
- [Reference](references/reference.md) - Detailed patterns and advanced configurations
