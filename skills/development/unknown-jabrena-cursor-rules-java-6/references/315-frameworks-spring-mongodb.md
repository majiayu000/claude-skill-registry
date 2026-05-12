---
name: 315-frameworks-spring-mongodb
description: Use when you need MongoDB with Spring Data MongoDB — including Maven dependencies, document modeling with @Document and @CompoundIndex, MongoRepository, MongoTemplate for complex queries, @Version optimistic locking, and explicit error handling for DuplicateKeyException and OptimisticLockingFailureException. This should trigger for requests such as Add MongoDB in Spring Boot; Review Spring Data Mongo repositories; Improve error handling for Mongo writes.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Spring Boot — MongoDB

## Role

You are a Senior software engineer with extensive experience in Spring Boot and MongoDB

## Goal

Design clear document models, implement correct Spring Data MongoDB repositories and services, and handle MongoDB failures explicitly. Prefer immutable records for documents, explicit index declarations, and `@Version` for concurrency control. Never expose managed documents at API boundaries — map to DTOs. Guard against injection by using derived finders or `Criteria` — never string-concatenated query strings.

**What is covered in this Skill?**

- Maven `spring-boot-starter-data-mongodb` dependency aligned with the Spring Boot BOM
- Document design: `@Document`, `@Field`, `@CompoundIndex`, and `@Id` mapping
- Factory methods for new documents; `@Version` for optimistic locking
- `MongoRepository` with derived finders and explicit `@Query` methods
- `MongoTemplate` for complex aggregations and multi-condition queries
- `@Transactional` on service methods (MongoDB multi-document transactions where supported)
- Error handling: `DuplicateKeyException`, `OptimisticLockingFailureException`, `DataAccessException`
- DTO projections: returning view types instead of leaking internal documents
- Testing with `@DataMongoTest` slice and Testcontainers MongoDB

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any MongoDB changes, ensure the project compiles. Compilation failure is a BLOCKING condition.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **INJECTION**: Never build query strings by concatenating user input — always use Criteria API or derived finders
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files
- **EDGE CASE**: If required context, files, or tools are missing, report the blocker explicitly

## Examples

### Table of contents

- Example 1: Maven dependency
- Example 2: Document design
- Example 3: Repository pattern
- Example 4: Service layer
- Example 5: MongoTemplate for complex queries
- Example 6: Error handling
- Example 7: Testing

### Example 1: Maven dependency

Title: Add the Spring Data MongoDB starter; version is managed by the Spring Boot BOM
Description: Spring Boot's BOM manages the `spring-boot-starter-data-mongodb` version. Declaring an explicit version risks classpath conflicts with the auto-configured `MongoAutoConfiguration`. Add the embedded Flapdoodle MongoDB only in `test` scope for slice tests when not using Testcontainers.

**Good example:**

```xml
<!-- pom.xml — Spring Boot BOM manages the version -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb</artifactId>
</dependency>

<!-- Optional: embedded MongoDB for @DataMongoTest slices without Testcontainers -->
<dependency>
    <groupId>de.flapdoodle.embed</groupId>
    <artifactId>de.flapdoodle.embed.mongo.spring30x</artifactId>
    <scope>test</scope>
</dependency>
```

**Bad example:**

```xml
<!-- Bad: pinned version fights the BOM -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb</artifactId>
    <version>3.2.0</version>
</dependency>
```

### Example 2: Document design

Title: @Document with explicit collection, @Field, @CompoundIndex, and factory method
Description: Annotate with `@Document` and name the collection explicitly to avoid case-sensitivity surprises across environments. Map field names with `@Field` when the Java property name differs from the stored field. Declare indexes on the entity with `@CompoundIndex` to keep schema intent alongside the model. Use a static factory method (`of(...)`) that leaves `id` null for new inserts.

**Good example:**

```java
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Version;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import java.time.Instant;

@Document(collection = "orders")
@CompoundIndex(name = "uk_order_number", def = "{'order_number': 1}", unique = true)
public record OrderDocument(
    @Id String id,
    @Field("order_number") String orderNumber,
    @Field("customer_id") String customerId,
    @Field("created_at") Instant createdAt,
    @Version Long version
) {
    public static OrderDocument of(String orderNumber, String customerId) {
        return new OrderDocument(null, orderNumber, customerId, Instant.now(), null);
    }
}
```

**Bad example:**

```java
// Bad: implicit collection name derived from class name; no indexes; mutable class
@Document
class OrderDocument {
    @Id String id;
    String orderNumber;  // no unique index
    String customerId;
    // setters allow accidental mutation
    public void setId(String id) { this.id = id; }
}
```

### Example 3: Repository pattern

Title: MongoRepository with derived finders; avoid string-concatenated queries
Description: Extend `MongoRepository` (or `ListCrudRepository` for `List&lt;T&gt;` return types). Use Spring Data's query derivation for simple lookups and `@Query` with named parameters for complex ones. Never build MongoDB JSON query strings from user input — use the Criteria API or `@Query` with `:?0` / `:#{[0]}` placeholders.

**Good example:**

```java
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;
import java.time.Instant;
import java.util.List;
import java.util.Optional;

@Repository
public interface OrderRepository extends MongoRepository<OrderDocument, String> {

    Optional<OrderDocument> findByOrderNumber(String orderNumber);

    List<OrderDocument> findByCustomerId(String customerId);

    // Named @Query — binds the parameter safely
    @Query("{ 'created_at': { $gte: ?0 } }")
    List<OrderDocument> findCreatedAfter(Instant since);
}
```

**Bad example:**

```java
// Bad: raw string concatenation into a Mongo query — NoSQL injection risk
class OrderRepositoryBad {
    @Autowired MongoTemplate mongoTemplate;

    List<OrderDocument> findByCustomer(String customerId) {
        String json = "{ 'customer_id': '" + customerId + "' }"; // injection-prone
        return mongoTemplate.find(new BasicQuery(json), OrderDocument.class);
    }
}
```

### Example 4: Service layer

Title: Constructor injection, @Transactional for multi-document atomicity
Description: Keep the repository out of REST controllers — route everything through a service. Declare the class `@Transactional(readOnly = true)` and override write methods with `@Transactional`. MongoDB multi-document transactions require a replica set; Spring Data MongoDB supports them transparently when the driver is connected to one.

**Good example:**

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@Transactional(readOnly = true)
class OrderService {

    private final OrderRepository repository;

    OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    Optional<OrderDocument> findByOrderNumber(String orderNumber) {
        return repository.findByOrderNumber(orderNumber);
    }

    List<OrderDocument> findByCustomer(String customerId) {
        return repository.findByCustomerId(customerId);
    }

    @Transactional
    OrderDocument create(String orderNumber, String customerId) {
        return repository.save(OrderDocument.of(orderNumber, customerId));
    }

    @Transactional
    OrderDocument updateCustomer(String orderId, String newCustomerId) {
        return repository.findById(orderId)
            .map(o -> new OrderDocument(o.id(), o.orderNumber(), newCustomerId, o.createdAt(), o.version()))
            .map(repository::save)
            .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
    }
}
```

**Bad example:**

```java
// Bad: no transaction boundary; repository directly in REST controller leaks persistence
@RestController
class OrderController {
    @Autowired OrderRepository repository;

    @PostMapping("/orders")
    OrderDocument create(String orderNumber) {
        return repository.save(new OrderDocument(null, orderNumber, null, null, null));
    }
}
```

### Example 5: MongoTemplate for complex queries

Title: Criteria API — type-safe and injection-free
Description: Use `MongoTemplate` with the `Criteria` and `Query` builder API when query derivation is insufficient (e.g. dynamic optional filters, aggregation pipelines). This keeps query logic readable, testable, and free of string concatenation risks.

**Good example:**

```java
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Repository
class OrderCustomRepository {

    private final MongoTemplate mongoTemplate;

    OrderCustomRepository(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    List<OrderDocument> search(String customerId, Instant since) {
        var criteria = new ArrayList<Criteria>();
        if (customerId != null) {
            criteria.add(Criteria.where("customer_id").is(customerId));
        }
        if (since != null) {
            criteria.add(Criteria.where("created_at").gte(since));
        }
        var query = criteria.isEmpty()
            ? new Query()
            : new Query(new Criteria().andOperator(criteria.toArray(new Criteria[0])));
        return mongoTemplate.find(query, OrderDocument.class);
    }
}
```

**Bad example:**

```java
// Bad: building the JSON query document from user input
List<OrderDocument> search(String customerId) {
    String json = "{ customer_id: '" + customerId + "' }"; // injection risk
    return mongoTemplate.find(new BasicQuery(json), OrderDocument.class);
}
```

### Example 6: Error handling

Title: DuplicateKeyException, OptimisticLockingFailureException — translate at service boundary
Description: Catch MongoDB-specific Spring Data exceptions (`DuplicateKeyException`, `OptimisticLockingFailureException`) at the service layer and translate them into domain exceptions or meaningful HTTP status codes. Never let raw driver-level exceptions leak to the API. Avoid blanket `catch (Exception e)` which swallows the failure and loses context.

**Good example:**

```java
import org.springframework.dao.DuplicateKeyException;
import org.springframework.dao.OptimisticLockingFailureException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
class OrderService {

    private final OrderRepository repository;

    OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    @Transactional
    OrderDocument create(String orderNumber, String customerId) {
        try {
            return repository.save(OrderDocument.of(orderNumber, customerId));
        } catch (DuplicateKeyException ex) {
            throw new IllegalStateException("Order number already exists: " + orderNumber, ex);
        }
    }

    @Transactional
    OrderDocument updateCustomer(String orderId, String newCustomerId) {
        try {
            return repository.findById(orderId)
                .map(o -> new OrderDocument(o.id(), o.orderNumber(), newCustomerId, o.createdAt(), o.version()))
                .map(repository::save)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
        } catch (OptimisticLockingFailureException ex) {
            throw new IllegalStateException("Concurrent update on order: " + orderId, ex);
        }
    }
}
```

**Bad example:**

```java
OrderDocument create(String orderNumber, String customerId) {
    try {
        return repository.save(OrderDocument.of(orderNumber, customerId));
    } catch (Exception e) {
        // Bad: generic catch + silent return null hides duplicate-key and network errors
        return null;
    }
}
```


### Example 7: Testing

Title: @DataMongoTest slice with Testcontainers for repository behaviour
Description: Use `@DataMongoTest` to spin up only the MongoDB slice — repositories, `MongoTemplate`, and auto-configurations — without the full web layer. Pair it with a `MongoDBContainer` from Testcontainers to run tests against the real dialect. Never mock the repository inside this test — the entire purpose is exercising real MongoDB behaviour.

**Good example:**

```java
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.MongoDBContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataMongoTest
@Testcontainers
class OrderRepositoryIT {

    @Container
    static MongoDBContainer mongo = new MongoDBContainer("mongo:7.0");

    @DynamicPropertySource
    static void mongoProps(DynamicPropertyRegistry registry) {
        registry.add("spring.data.mongodb.uri", mongo::getReplicaSetUrl);
    }

    @Autowired
    OrderRepository repository;

    @AfterEach
    void cleanup() { repository.deleteAll(); }

    @Test
    void save_generatesId() {
        OrderDocument saved = repository.save(OrderDocument.of("ORD-001", "CUST-1"));
        assertThat(saved.id()).isNotNull();
    }

    @Test
    void findByOrderNumber_returnsDocument() {
        repository.save(OrderDocument.of("ORD-002", "CUST-2"));
        Optional<OrderDocument> found = repository.findByOrderNumber("ORD-002");
        assertThat(found).isPresent();
        assertThat(found.get().customerId()).isEqualTo("CUST-2");
    }
}
```

**Bad example:**

```java
// Bad: @SpringBootTest loads full context; mocking repository adds no value
@SpringBootTest
class OrderRepositoryTest {
    @MockBean OrderRepository repository;

    @Test
    void findByOrderNumber() {
        when(repository.findByOrderNumber("ORD-001"))
            .thenReturn(Optional.of(new OrderDocument("id", "ORD-001", "c", null, null)));
        // verifies Mockito wiring only — tests nothing about real MongoDB
    }
}
```

## Output Format

- **ANALYZE** MongoDB code: document mapping completeness, index declarations, repository query safety, service transaction placement, error handling specificity, and DTO vs document leakage
- **CATEGORIZE** issues by impact (SECURITY for injection risk, CORRECTNESS for missing @Version or transactions, PERFORMANCE for missing indexes or unbounded queries, MAINTAINABILITY for mutable documents or missing factory methods)
- **APPLY** Spring Data MongoDB–aligned fixes: explicit collection, @Field, @CompoundIndex, @Version, safe Criteria-based queries, service-layer transactions, exception translation
- **IMPLEMENT** changes so document model, indexes, repositories, and tests stay consistent
- **EXPLAIN** trade-offs (MongoRepository derived finders vs MongoTemplate Criteria, embedded Flapdoodle vs Testcontainers, multi-document transactions vs application-level idempotency)
- **TEST** repository behaviour with `@DataMongoTest` + Testcontainers; never mock repositories inside persistence slice tests
- **VALIDATE** with `./mvnw compile` before and `./mvnw clean verify` after changes

## Safeguards

- **BLOCKING SAFETY CHECK**: Run `./mvnw compile` before ANY MongoDB refactoring — compilation failure is a HARD STOP
- **CRITICAL VALIDATION**: Run `./mvnw clean verify` after changes; confirm repository tests pass before promoting
- **INJECTION SAFETY**: Never concatenate user input into MongoDB query strings or `BasicQuery` objects — use Criteria API or `@Query` with bound parameters
- **ERROR HANDLING**: Catch `DuplicateKeyException` and `OptimisticLockingFailureException` at the service boundary and translate to domain exceptions; never swallow with a generic catch
- **OPTIMISTIC LOCKING**: Adding `@Version` to an existing document requires a planned rollout for existing documents; test stale-update behavior before enabling it in production
- **INDEXES**: Deploy index changes as coordinated background operations on large collections; avoid blocking foreground index builds in production
- **API BOUNDARIES**: Never return managed `@Document` entities directly from REST controllers — map to DTOs to keep API contracts stable and prevent field leakage
- **INCREMENTAL SAFETY**: Change one repository surface or document mapping at a time; verify with `@DataMongoTest` between steps