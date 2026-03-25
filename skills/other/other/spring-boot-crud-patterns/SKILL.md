---
name: spring-boot-crud-patterns
description: Provides and generates complete CRUD workflows for Spring Boot 3 services. Creates feature-focused architecture with Spring Data JPA aggregates, repositories, DTOs, controllers, and REST APIs. Validates domain invariants and transaction boundaries. Use when modeling Java backend services, REST API endpoints, database operations, web service patterns, or JPA entities for Spring Boot applications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Spring Boot CRUD Patterns

## Overview

Provides complete CRUD workflows for Spring Boot 3.5+ services using feature-focused architecture. Creates and validates domain aggregates, JPA repositories, application services, and REST controllers with proper separation of concerns. Defer detailed code listings to reference files for progressive disclosure.

## When to Use

- Create REST endpoints for create/read/update/delete workflows backed by Spring Data JPA.
- Implement feature packages following DDD-inspired architecture with aggregates, repositories, and application services.
- Define DTO records, request validation, and controller mappings for external clients.
- Diagnose CRUD regressions, repository contracts, or transaction boundaries in existing Spring Boot services.
- Trigger phrases: **"implement Spring CRUD controller"**, **"create an endpoint"**, **"add database entity"**, **"refine feature-based repository"**, **"map DTOs for JPA aggregate"**, **"add pagination to REST list endpoint"**.

## Instructions

Follow this streamlined workflow to deliver feature-aligned CRUD services with explicit validation gates:

### 1. Establish Feature Structure
Create `feature/<name>/` directories with `domain`, `application`, `presentation`, and `infrastructure` subpackages.
**Validate**: Verify directory structure matches the feature boundary before proceeding.

### 2. Define Domain Model
Create entity classes with invariants enforced through factory methods (`create`, `update`). Keep domain logic framework-free.
**Validate**: Assert all invariants are covered by unit tests before advancing.

### 3. Expose Domain Ports
Declare repository interfaces in `domain/repository` describing persistence contracts without implementation details.
**Validate**: Confirm interface signatures match domain operations.

### 4. Provide Infrastructure Adapter
Create JPA entities in `infrastructure/persistence` that map to domain models. Implement Spring Data repositories.
**Validate**: Run `@DataJpaTest` to verify entity mapping and repository integration.

### 5. Implement Application Services
Create `@Transactional` service classes that orchestrate domain operations and DTO mapping.
**Validate**: Ensure transaction boundaries are correct and optimistic locking is applied where needed.

### 6. Define DTOs and Controllers
Use Java records for API contracts with `jakarta.validation` annotations. Map REST endpoints with proper status codes.
**Validate**: Test validation constraints and verify HTTP status codes (201 POST, 200 GET, 204 DELETE).

### 7. Validate and Deploy
Run integration tests with Testcontainers. Verify migrations (Liquibase/Flyway) mirror the aggregate schema.
**Validate**: Execute full test suite before deployment; confirm schema migration scripts are applied.

See `references/examples-product-feature.md` for complete code aligned with each step.

## Examples

### Java Code Example: Product Feature

```java
// feature/product/domain/Product.java
package com.example.product.domain;

import java.math.BigDecimal;
import java.time.Instant;

public record Product(
    String id,
    String name,
    String description,
    BigDecimal price,
    int stock,
    Instant createdAt,
    Instant updatedAt
) {
    public static Product create(String name, String desc, BigDecimal price, int stock) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Name required");
        if (price == null || price.compareTo(BigDecimal.ZERO) < 0) throw new IllegalArgumentException("Invalid price");
        return new Product(null, name.trim(), desc, price, stock, Instant.now(), null);
    }

    public Product withPrice(BigDecimal newPrice) {
        return new Product(id, name, description, newPrice, stock, createdAt, Instant.now());
    }
}
```

```java
// feature/product/domain/repository/ProductRepository.java
package com.example.product.domain.repository;

import com.example.product.domain.Product;
import java.util.Optional;

public interface ProductRepository {
    Product save(Product product);
    Optional<Product> findById(String id);
    void deleteById(String id);
}
```

```java
// feature/product/infrastructure/persistence/ProductJpaEntity.java
package com.example.product.infrastructure.persistence;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.Instant;

@Entity @Table(name = "products")
public class ProductJpaEntity {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    private String name;
    private String description;
    private BigDecimal price;
    private int stock;
    private Instant createdAt;
    private Instant updatedAt;

    // getters, setters, constructor from domain (omitted for brevity)
}
```

```java
// feature/product/infrastructure/persistence/JpaProductRepository.java
package com.example.product.infrastructure.persistence;

import com.example.product.domain.Product;
import com.example.product.domain.repository.ProductRepository;
import org.springframework.stereotype.Repository;

@Repository
public class JpaProductRepository implements ProductRepository {
    private final SpringDataProductRepository springData;

    public JpaProductRepository(SpringDataProductRepository springData) {
        this.springData = springData;
    }

    @Override
    public Product save(Product product) {
        ProductJpaEntity entity = toEntity(product);
        ProductJpaEntity saved = springData.save(entity);
        return toDomain(saved);
    }

    // findById, deleteById implementations...
}
```

```java
// feature/product/presentation/rest/ProductController.java
package com.example.product.presentation.rest;

import com.example.product.domain.Product;
import com.example.product.domain.repository.ProductRepository;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController @RequestMapping("/api/products")
public class ProductController {
    private final ProductService service;

    public ProductController(ProductService service) { this.service = service; }

    @PostMapping
    public ResponseEntity<ProductResponse> create(@Valid @RequestBody CreateProductRequest req) {
        Product product = service.create(req.toDomain());
        return ResponseEntity.status(201).body(ProductResponse.from(product));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProductResponse> getById(@PathVariable String id) {
        return service.findById(id)
            .map(p -> ResponseEntity.ok(ProductResponse.from(p)))
            .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable String id) {
        service.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    // record DTOs
    public record CreateProductRequest(
        @NotBlank String name,
        String description,
        @NotNull @DecimalMin("0.01") java.math.BigDecimal price,
        @Min(0) int stock
    ) {
        Product toDomain() { return Product.create(name, description, price, stock); }
    }

    public record ProductResponse(String id, String name, java.math.BigDecimal price) {
        static ProductResponse from(Product p) { return new ProductResponse(p.id(), p.name(), p.price()); }
    }
}
```

### JSON Input/Output Examples

**Create Request:**
```json
{
  "name": "Wireless Keyboard",
  "description": "Ergonomic keyboard",
  "price": 79.99,
  "stock": 50
}
```

**Created Response (201):**
```json
{
  "id": "prod-123",
  "name": "Wireless Keyboard",
  "price": 79.99,
  "_links": { "self": "/api/products/prod-123" }
}
```

**Paginated List Request:**
```bash
curl "http://localhost:8080/api/products?page=0&size=10&sort=name,asc"
```

## Best Practices

- Co-locate domain, application, and presentation code per aggregate within feature packages.
- Use Java records for immutable DTOs; convert domain types at the service boundary.
- Apply transactions and optimistic locking for write operations.
- Normalize pagination defaults (page, size, sort) and document query parameters.
- Log CRUD lifecycle events (create, update, delete) at info level with structured audit trails.
- Surface health and metrics through Spring Boot Actuator; monitor throughput and error rates.

## Constraints and Warnings

- **Never** expose JPA entities directly in controllers to prevent lazy-loading leaks and serialization issues.
- **Never** mix field injection with constructor injection; maintain immutability for testability.
- **Never** embed business logic in controllers or repository adapters; keep it in domain/application layers.
- **Always** validate input aggressively to prevent constraint violations and produce consistent error payloads.
- **Always** ensure migrations (Liquibase/Flyway) mirror aggregate evolution before deploying schema changes.
- **Always** run integration tests with Testcontainers before merging to prevent persistence regressions.

## References

- [HTTP methods, annotations, DTO patterns](references/crud-reference.md)
- [Progressive examples from starter to advanced](references/examples-product-feature.md)
- [Spring Boot official documentation](references/spring-official-docs.md)
- [CRUD generator script](scripts/generate_crud_boilerplate.py) - `python scripts/generate_crud_boilerplate.py --spec entity.json --package com.example.product --output ./generated`
