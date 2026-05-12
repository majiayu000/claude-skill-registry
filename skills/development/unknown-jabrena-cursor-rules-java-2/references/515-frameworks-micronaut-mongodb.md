---
name: 515-frameworks-micronaut-mongodb
description: Use when you need MongoDB persistence in Micronaut — including Maven dependency, @MappedEntity document design, @MongoRepository with typed finders and @MongoFindQuery, @Singleton service boundaries, optional @Transactional use where MongoDB transaction support is configured, and explicit error handling for MongoWriteException and DataAccessException. This should trigger for requests such as Add MongoDB in Micronaut; Review Micronaut Data Mongo entities; Improve error handling for Micronaut Mongo operations.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Micronaut — MongoDB

## Role

You are a Senior software engineer with extensive experience in Micronaut and MongoDB

## Goal

Design and implement MongoDB persistence in Micronaut using Micronaut Data MongoDB. Prefer `@MappedEntity` records for immutable, compile-time-verified persistence types. Declare repositories as `@MongoRepository` interfaces so Micronaut generates implementations at compile time. Keep business logic in `@Singleton` services — never in repositories or controllers. Guard all queries with bound parameters — never concatenate user input into filter strings.

**What is covered in this Skill?**

- Maven `micronaut-data-mongodb` and `mongodb-driver-sync` dependencies
- `@MappedEntity` document design with `@Id`, `@MappedProperty`, and `@GeneratedValue`
- `@MongoRepository` extending `CrudRepository` with derived finders
- `@MongoFindQuery` for complex filter expressions with bound parameters
- `@Singleton` service with `io.micronaut.transaction.annotation.Transactional`
- Pagination with `Pageable` and `Page<T>`
- DTO projections with interface projections
- Error handling: `MongoWriteException` / duplicate-key category checks, `DataAccessException`, exception chaining
- Testing with `@MicronautTest` + `TestPropertyProvider` + Testcontainers MongoDB

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any MongoDB changes, ensure the project compiles. Compilation failure is a BLOCKING condition.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **INJECTION**: Never concatenate user input into MongoDB filter strings or raw JSON queries — always use derived finders or `@MongoFindQuery` with bound parameters
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files

## Examples

### Table of contents

- Example 1: Maven dependency
- Example 2: Entity design
- Example 3: Repository interface
- Example 4: Service layer
- Example 5: Pagination
- Example 6: Error handling
- Example 7: Integration testing

### Example 1: Maven dependency

Title: Add micronaut-data-mongodb and mongodb-driver-sync; BOM manages versions
Description: Add `micronaut-data-mongodb` for the repository abstraction and `mongodb-driver-sync` for the synchronous driver. The Micronaut BOM manages both versions — do not pin them explicitly. Add the Testcontainers MongoDB artifact in `test` scope for real-database integration tests.

**Good example:**

```xml
<!-- pom.xml — Micronaut BOM manages versions -->
<dependency>
    <groupId>io.micronaut.data</groupId>
    <artifactId>micronaut-data-mongodb</artifactId>
</dependency>
<dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongodb-driver-sync</artifactId>
    <scope>runtime</scope>
</dependency>

<!-- Testcontainers MongoDB for integration tests -->
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>mongodb</artifactId>
    <scope>test</scope>
</dependency>
```

**Bad example:**

```xml
<!-- Bad: pinned versions fight the BOM and risk classpath conflicts -->
<dependency>
    <groupId>io.micronaut.data</groupId>
    <artifactId>micronaut-data-mongodb</artifactId>
    <version>4.7.0</version>
</dependency>
```

### Example 2: Entity design

Title: @MappedEntity record with @Id, @MappedProperty, and factory method
Description: Annotate persistence types with `@MappedEntity("collection-name")` to bind them to an explicit MongoDB collection. Use `@MappedProperty` to map Java record components to MongoDB document field names when they differ (e.g. snake_case storage vs camelCase Java). Leave `@Id` null for new documents — Micronaut Data sets it after insert. Expose a static factory method so callers never construct a raw entity with a non-null `id`.

**Good example:**

```java
import io.micronaut.data.annotation.GeneratedValue;
import io.micronaut.data.annotation.Id;
import io.micronaut.data.annotation.MappedEntity;
import io.micronaut.data.annotation.MappedProperty;
import org.bson.types.ObjectId;
import java.time.Instant;

@MappedEntity("orders")
public record OrderDocument(
    @Id @GeneratedValue ObjectId id,
    @MappedProperty("order_number") String orderNumber,
    @MappedProperty("customer_id") String customerId,
    @MappedProperty("created_at") Instant createdAt
) {
    public static OrderDocument of(String orderNumber, String customerId) {
        return new OrderDocument(null, orderNumber, customerId, Instant.now());
    }
}
```

**Bad example:**

```java
// Bad: missing @MappedEntity — Micronaut Data cannot derive collection name reliably;
// no @MappedProperty — field names stored as Java camelCase, breaking schema conventions;
// mutable class with setters allows accidental mutation after load
public class OrderDocument {
    @Id private ObjectId id;
    private String orderNumber;
    public void setId(ObjectId id) { this.id = id; }
}
```

### Example 3: Repository interface

Title: @MongoRepository with typed derived finders and @MongoFindQuery
Description: Extend `CrudRepository` and annotate with `@MongoRepository`. Micronaut Data generates the implementation at compile time, validating method names and query correctness. Use query derivation (`findByOrderNumber`) for simple equality lookups. Use `@MongoFindQuery` with a bound filter document for composite or range queries — never concatenate user input into the filter string.

**Good example:**

```java
import io.micronaut.data.mongodb.annotation.MongoFindQuery;
import io.micronaut.data.mongodb.annotation.MongoRepository;
import io.micronaut.data.repository.CrudRepository;
import org.bson.types.ObjectId;
import java.time.Instant;
import java.util.List;
import java.util.Optional;

@MongoRepository
public interface OrderRepository extends CrudRepository<OrderDocument, ObjectId> {

    // Derived finder — safe, generated at compile time
    Optional<OrderDocument> findByOrderNumber(String orderNumber);

    List<OrderDocument> findByCustomerId(String customerId);

    // @MongoFindQuery: bound parameter :createdAt — no string concatenation
    @MongoFindQuery("{ 'created_at': { $gte: :createdAt } }")
    List<OrderDocument> findCreatedAfter(Instant createdAt);
}
```

**Bad example:**

```java
// Bad: missing @MongoRepository — not a Micronaut Data bean
public interface OrderRepository extends CrudRepository<OrderDocument, ObjectId> {}

// Bad: raw string concatenation into a Mongo filter — NoSQL injection risk
class OrderCustomQuery {
    @Inject MongoClient client;
    List<OrderDocument> findByCustomer(String customerId) {
        String filter = "{ customer_id: '" + customerId + "' }"; // injection-prone
        return ...; // unsafe
    }
}
```

### Example 4: Service layer

Title: @Singleton service with @Transactional for multi-step writes
Description: Wrap business use cases in `@Singleton` services. Use `io.micronaut.transaction.annotation.Transactional` for methods that coordinate multiple repository writes. MongoDB multi-document transactions require a replica set — verify infrastructure support before enabling. Constructor-inject the repository to maintain testability and keep the API layer out of persistence concerns.

**Good example:**

```java
import io.micronaut.context.annotation.Singleton;
import io.micronaut.transaction.annotation.Transactional;
import jakarta.inject.Inject;
import org.bson.types.ObjectId;
import java.util.Optional;

@Singleton
public class OrderService {

    private final OrderRepository repository;

    @Inject
    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    @Transactional
    public OrderDocument create(String orderNumber, String customerId) {
        return repository.save(OrderDocument.of(orderNumber, customerId));
    }

    public Optional<OrderDocument> findByOrderNumber(String orderNumber) {
        return repository.findByOrderNumber(orderNumber);
    }

    @Transactional
    public void delete(ObjectId id) {
        repository.deleteById(id);
    }
}
```

**Bad example:**

```java
// Bad: controller calling repository directly — no service layer, untestable
@Controller("/orders")
class OrderController {
    @Inject OrderRepository repository;

    @Post
    OrderDocument create(String body) {
        return repository.save(OrderDocument.of(body, "unknown")); // no validation or mapping
    }
}
```

### Example 5: Pagination

Title: Pageable and Page<T> for bounded list queries
Description: Never expose unbounded `findAll()` on large collections. Use `PageableRepository` or accept a `Pageable` parameter and return `Page&lt;T&gt;`. This keeps memory consumption bounded and lets callers navigate results page by page.

**Good example:**

```java
import io.micronaut.data.model.Page;
import io.micronaut.data.model.Pageable;
import io.micronaut.data.mongodb.annotation.MongoRepository;
import io.micronaut.data.repository.PageableRepository;
import org.bson.types.ObjectId;

@MongoRepository
public interface OrderRepository extends PageableRepository<OrderDocument, ObjectId> {

    Page<OrderDocument> findByCustomerId(String customerId, Pageable pageable);
}
```

**Bad example:**

```java
@MongoRepository
interface OrderRepository extends CrudRepository<OrderDocument, ObjectId> {

    // Bad: loads every document in the collection — OOM risk on large datasets
    List<OrderDocument> findAll();
}
```

### Example 6: Error handling

Title: MongoWriteException and DataAccessException — translate at service boundary
Description: Catch MongoDB driver write failures (for example duplicate-key violations via `MongoWriteException` and `ErrorCategory.DUPLICATE_KEY`) and `DataAccessException` at the service boundary, then translate them into meaningful domain exceptions. Always chain the original exception to preserve the stack trace. Never return `null` from a catch block — it corrupts the caller's control flow.

**Good example:**

```java
import com.mongodb.ErrorCategory;
import com.mongodb.MongoWriteException;
import io.micronaut.context.annotation.Singleton;
import io.micronaut.data.exceptions.DataAccessException;
import io.micronaut.transaction.annotation.Transactional;
import jakarta.inject.Inject;

@Singleton
public class OrderService {

    @Inject
    OrderRepository repository;

    @Transactional
    public OrderDocument create(String orderNumber, String customerId) {
        try {
            return repository.save(OrderDocument.of(orderNumber, customerId));
        } catch (MongoWriteException ex) {
            if (ex.getError().getCategory() == ErrorCategory.DUPLICATE_KEY) {
                throw new IllegalStateException("Order number already exists: " + orderNumber, ex);
            }
            throw ex;
        } catch (DataAccessException ex) {
            throw new IllegalStateException("MongoDB data access failure saving order: " + orderNumber, ex);
        }
    }
}
```

**Bad example:**

```java
public OrderDocument create(String orderNumber, String customerId) {
    try {
        return repository.save(OrderDocument.of(orderNumber, customerId));
    } catch (Exception e) {
        // Bad: generic catch + null return hides duplicate-key, network errors, schema drift
        return null;
    }
}
```


### Example 7: Integration testing

Title: @MicronautTest + TestPropertyProvider + Testcontainers MongoDB
Description: Use `@MicronautTest` with `TestPropertyProvider` to supply the real MongoDB connection string from a Testcontainers `MongoDBContainer`. This runs tests against a real MongoDB instance with the actual driver, schema, and index behaviour. Never mock `@MongoRepository` inside a persistence test — the goal is exercising real MongoDB behaviour.

**Good example:**

```java
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import io.micronaut.test.support.TestPropertyProvider;
import jakarta.inject.Inject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.testcontainers.containers.MongoDBContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import java.util.Map;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@Testcontainers
class OrderRepositoryIT implements TestPropertyProvider {

    @Container
    static MongoDBContainer mongo = new MongoDBContainer("mongo:7.0");

    @Inject
    OrderRepository repository;

    @Override
    public Map<String, String> getProperties() {
        if (!mongo.isRunning()) mongo.start();
        return Map.of("mongodb.uri", mongo.getReplicaSetUrl());
    }

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
// Bad: mocking @MongoRepository proves nothing about real MongoDB behavior
@MicronautTest
class OrderRepositoryTest {
    @MockBean(OrderRepository.class)
    OrderRepository mockRepository;

    @Test
    void findByOrderNumber() {
        when(mockRepository.findByOrderNumber("ORD-001")).thenReturn(Optional.empty());
        // verifies Mockito wiring only — no actual MongoDB interaction
    }
}
```

## Output Format

- **ANALYZE** MongoDB code: `@MappedEntity` mapping completeness, `@MongoRepository` query safety, service transaction boundaries, error handling specificity, pagination strategy, and DTO vs entity leakage
- **CATEGORIZE** issues by impact (SECURITY for filter injection, CORRECTNESS for missing transactions or generic exception handling, PERFORMANCE for unbounded queries or missing indexes, MAINTAINABILITY for mutable entities or entity leakage at API boundaries)
- **APPLY** Micronaut Data MongoDB–aligned fixes: explicit `@MappedEntity` collection, `@MappedProperty` field mappings, `@MongoRepository` with bound-parameter queries, service-layer `@Transactional`, and typed exception translation
- **IMPLEMENT** changes so document model, repository interfaces, services, and tests stay consistent
- **EXPLAIN** trade-offs (derived finder vs `@MongoFindQuery`, sync driver vs reactive, multi-document transactions vs application idempotency, `Page` vs full list returns)
- **TEST** repository behaviour with `@MicronautTest` + `TestPropertyProvider` + Testcontainers; never mock repositories inside persistence tests meant to verify MongoDB behaviour
- **VALIDATE** with `./mvnw compile` before and `./mvnw clean verify` after changes

## Safeguards

- **BLOCKING SAFETY CHECK**: Run `./mvnw compile` before ANY MongoDB refactoring — compilation failure is a HARD STOP
- **CRITICAL VALIDATION**: Run `./mvnw clean verify` after changes; confirm repository integration tests pass against a real MongoDB instance before promoting
- **INJECTION SAFETY**: Never concatenate user input into `@MongoFindQuery` filter strings or raw MongoDB JSON — use derived finders or bound parameters exclusively
- **ERROR HANDLING**: Catch duplicate-key write failures and `DataAccessException` at the service boundary; never use a generic `catch (Exception e)` that swallows failures or returns `null`
- **PAGINATION**: Never expose unbounded `findAll()` on large collections — always use `PageableRepository` or `Pageable`-accepting methods with `Page<T>`
- **TRANSACTIONS**: Multi-document `@Transactional` requires a MongoDB replica set — verify infrastructure compatibility before relying on it
- **AOP SELF-INVOCATION**: Never call a `@Transactional` method via `this.method()` inside the same Micronaut bean — the AOP interceptor is bypassed; extract to a separate injected bean
- **API BOUNDARIES**: Avoid returning `@MappedEntity` instances directly from HTTP controllers — map to DTOs to keep API contracts stable and prevent internal field leakage
- **INCREMENTAL SAFETY**: Change one entity, repository, or service surface at a time; verify with integration tests between steps