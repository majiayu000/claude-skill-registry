---
name: 415-frameworks-quarkus-mongodb
description: Use when you need MongoDB in Quarkus with MongoDB Panache — including Maven extension, entity/repository design with @MongoEntity, PanacheMongoEntity active record vs PanacheMongoRepository, parameterized queries, service-layer persistence boundaries, optional transaction support where infrastructure allows it, and explicit error handling for duplicate key and transient failures. This should trigger for requests such as Add MongoDB in Quarkus; Review Quarkus Mongo Panache entities; Improve Mongo error handling in Quarkus services.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Quarkus — MongoDB

## Role

You are a Senior software engineer with extensive experience in Quarkus and MongoDB

## Goal

Design and implement MongoDB persistence in Quarkus using MongoDB Panache. Choose the **repository pattern** (`PanacheMongoRepository`) for layered architectures and testability; use the **active record** pattern (`PanacheMongoEntity`) only for small, isolated entities. Keep business logic in `@ApplicationScoped` services, not in entities or REST resources. Prefer single-document atomic updates and explicit idempotency; only rely on multi-document MongoDB transactions when the infrastructure is configured for them. Guard all Panache query parameters — never concatenate user input into query strings.

**What is covered in this Skill?**

- Maven `quarkus-mongodb-panache` extension dependency
- `@MongoEntity` document design with `@BsonProperty` and index strategy
- Active record (`PanacheMongoEntity`) for simple CRUD
- Repository (`PanacheMongoRepository`) for separation of concerns
- Parameterized `find` using field shorthand, positional parameters, and `Document` filters
- `@ApplicationScoped` service boundaries with explicit single-document atomicity and optional transaction support where infrastructure allows it
- Error handling: `MongoWriteException` category checks (`DUPLICATE_KEY`), `MongoTimeoutException`, exception chaining
- DTO projections — never leak internal entities at API boundaries
- Dev Services for MongoDB (zero-config in dev/test)
- Testing with `@QuarkusTest`, Dev Services, and explicit cleanup between tests

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any MongoDB changes, ensure the project compiles. Compilation failure is a BLOCKING condition.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **INJECTION**: Never build Mongo query strings by concatenating user input — always use bound parameters or the Document filter API
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns
- **EDGE CASE**: If the user goal is ambiguous, stop and ask a clarifying question before editing files

## Examples

### Table of contents

- Example 1: Maven extension
- Example 2: Entity design
- Example 3: Repository pattern
- Example 4: Service layer
- Example 5: Error handling
- Example 6: Testing

### Example 1: Maven extension

Title: Add quarkus-mongodb-panache; Quarkus BOM manages the version
Description: Add `quarkus-mongodb-panache` to your `pom.xml`. The Quarkus BOM manages the version. Quarkus Dev Services automatically starts a MongoDB instance in dev and test modes when no `quarkus.mongodb.connection-string` is configured, so no manual setup is needed for local development.

**Good example:**

```xml
<!-- pom.xml — Quarkus BOM manages the version -->
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-mongodb-panache</artifactId>
</dependency>
```

**Bad example:**

```xml
<!-- Bad: pinned version fights the Quarkus BOM -->
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-mongodb-panache</artifactId>
    <version>3.8.1</version>
</dependency>
```

### Example 2: Entity design

Title: @MongoEntity with @BsonProperty for explicit field mapping
Description: Annotate the entity class with `@MongoEntity` and specify the collection name explicitly. Use `@BsonProperty` to map Java field names to MongoDB document field names when they differ. Keep domain-significant business identifiers (like `orderNumber`) separate from the MongoDB `id`. Use a `Instant createdAt` timestamp for auditability.

**Good example:**

```java
import io.quarkus.mongodb.panache.common.MongoEntity;
import org.bson.codecs.pojo.annotations.BsonProperty;
import org.bson.types.ObjectId;
import java.time.Instant;

@MongoEntity(collection = "orders")
public class OrderDocument {
    public ObjectId id;

    @BsonProperty("order_number")
    public String orderNumber;

    @BsonProperty("customer_id")
    public String customerId;

    @BsonProperty("created_at")
    public Instant createdAt;
}
```

**Bad example:**

```java
// Bad: no @MongoEntity → collection name derived from class name case-sensitively;
// no @BsonProperty → Java field names stored as-is in Mongo (camelCase vs snake_case mismatch)
public class OrderDocument extends io.quarkus.mongodb.panache.PanacheMongoEntity {
    public Object payload; // untyped — no schema
}
```

### Example 3: Repository pattern

Title: PanacheMongoRepository with typed, parameterized queries
Description: Implement `PanacheMongoRepository&lt;OrderDocument&gt;` in an `@ApplicationScoped` bean. Use Panache's shorthand field equality (`find("field", value)`) for simple lookups or `Document` filter objects for composite criteria. Never concatenate user input into a query string — always pass values as bound parameters.

**Good example:**

```java
import io.quarkus.mongodb.panache.PanacheMongoRepository;
import jakarta.enterprise.context.ApplicationScoped;
import org.bson.Document;
import java.time.Instant;
import java.util.List;
import java.util.Optional;

@ApplicationScoped
public class OrderRepository implements PanacheMongoRepository<OrderDocument> {

    // Safe: field shorthand — Panache builds the filter internally
    public Optional<OrderDocument> findByOrderNumber(String orderNumber) {
        return find("orderNumber", orderNumber).firstResultOptional();
    }

    // Safe: Document filter with bound parameters — no string concatenation
    public List<OrderDocument> findByCustomerSince(String customerId, Instant since) {
        return find(new Document("customer_id", customerId)
            .append("created_at", new Document("$gte", since)))
            .list();
    }
}
```

**Bad example:**

```java
@ApplicationScoped
public class OrderRepository implements PanacheMongoRepository<OrderDocument> {
    // Bad: concatenating user input into a query string — NoSQL injection risk
    public List<OrderDocument> findByCustomer(String customerId) {
        return find("{ customer_id: '" + customerId + "' }").list();
    }
}
```

### Example 4: Service layer

Title: @ApplicationScoped service with explicit persistence boundaries
Description: Wrap business use cases in `@ApplicationScoped` services. Keep REST resources or CDI event handlers thin — they delegate to the service, not to the repository directly. Constructor-inject the repository to maintain testability. Use single-document atomic updates by default; if a use case truly needs multi-document atomicity, verify MongoDB transaction support and configure it deliberately.

**Good example:**

```java
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import java.time.Instant;
import java.util.Optional;

@ApplicationScoped
public class OrderService {

    private final OrderRepository repository;

    @Inject
    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderDocument create(String orderNumber, String customerId) {
        var doc = new OrderDocument();
        doc.orderNumber = orderNumber;
        doc.customerId = customerId;
        doc.createdAt = Instant.now();
        repository.persist(doc);
        return doc;
    }

    public Optional<OrderDocument> findByOrderNumber(String orderNumber) {
        return repository.findByOrderNumber(orderNumber);
    }
}
```

**Bad example:**

```java
// Bad: business logic scattered inside a REST resource; no service layer
@Path("/orders")
class OrderResource {
    @Inject OrderRepository repository;

    @POST
    void create(String body) {
        var doc = new OrderDocument();
        doc.orderNumber = body; // no validation, no mapping
        repository.persist(doc);
    }
}
```

### Example 5: Error handling

Title: MongoWriteException category check; exception chaining; no generic catch
Description: Catch MongoDB driver-level exceptions by category rather than by message string. `MongoWriteException` carries an `ErrorCategory` — check for `DUPLICATE_KEY` to translate it into a domain constraint violation. Catch `MongoTimeoutException` separately for transient connectivity failures and consider retry logic there. Always chain the original exception to preserve the stack trace. Never swallow with a generic `catch (Exception e)` that returns `null` or logs and continues.

**Good example:**

```java
import com.mongodb.ErrorCategory;
import com.mongodb.MongoTimeoutException;
import com.mongodb.MongoWriteException;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class OrderService {

    @Inject OrderRepository repository;

    public OrderDocument create(String orderNumber, String customerId) {
        try {
            var doc = new OrderDocument();
            doc.orderNumber = orderNumber;
            doc.customerId = customerId;
            doc.createdAt = java.time.Instant.now();
            repository.persist(doc);
            return doc;
        } catch (MongoWriteException ex) {
            if (ex.getError().getCategory() == ErrorCategory.DUPLICATE_KEY) {
                throw new IllegalStateException("Order number already exists: " + orderNumber, ex);
            }
            throw ex;
        } catch (MongoTimeoutException ex) {
            throw new IllegalStateException("Transient MongoDB timeout — consider retry", ex);
        }
    }
}
```

**Bad example:**

```java
public OrderDocument create(String orderNumber, String customerId) {
    try {
        repository.persist(doc);
        return doc;
    } catch (Exception e) {
        // Bad: generic catch swallows duplicate-key, timeout, schema errors
        return null; // corrupts control flow for the caller
    }
}
```


### Example 6: Testing

Title: @QuarkusTest + Dev Services for repository integration; clean collections between tests
Description: Annotate the test class with `@QuarkusTest`. Quarkus Dev Services starts a MongoDB container automatically. Clean the repository before or after each test to keep test data isolated. Do not use JPA-style rollback assumptions for MongoDB persistence tests. Never mock `PanacheMongoRepository` inside a persistence test — the goal is exercising real MongoDB behaviour.

**Good example:**

```java
import io.quarkus.test.junit.QuarkusTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@QuarkusTest
class OrderRepositoryTest {

    @Inject
    OrderRepository repository;

    @AfterEach
    void cleanup() {
        repository.deleteAll();
    }

    @Test
    void persist_and_findByOrderNumber() {
        OrderDocument doc = new OrderDocument();
        doc.orderNumber = "ORD-001";
        doc.customerId = "CUST-1";
        doc.createdAt = java.time.Instant.now();
        repository.persist(doc);

        Optional<OrderDocument> found = repository.findByOrderNumber("ORD-001");
        assertThat(found).isPresent();
        assertThat(found.get().customerId).isEqualTo("CUST-1");
    }
}
```

**Bad example:**

```java
// Bad: mocking PanacheMongoRepository proves nothing about real Mongo behavior
@QuarkusTest
class OrderRepositoryTest {
    @InjectMock OrderRepository repository;

    @Test
    void find() {
        when(repository.findByOrderNumber("ORD-001")).thenReturn(Optional.empty());
        assertThat(repository.findByOrderNumber("ORD-001")).isEmpty();
        // only tests Mockito wiring
    }
}
```

## Output Format

- **ANALYZE** MongoDB code: entity mapping correctness, query parameter safety, service persistence boundaries, error handling specificity, and DTO vs entity leakage
- **CATEGORIZE** issues by impact (SECURITY for query injection, CORRECTNESS for non-atomic multi-document assumptions or generic exception handling, PERFORMANCE for missing indexes, MAINTAINABILITY for active-record overuse or entity leakage at API boundaries)
- **APPLY** Quarkus MongoDB–aligned fixes: explicit `@MongoEntity` collection, `@BsonProperty` mappings, parameterized `find()` calls, clear service-layer persistence boundaries, and typed exception translation
- **IMPLEMENT** changes so entity design, repositories, services, and tests stay consistent; create index creation scripts when adding `@CompoundIndex`-equivalent needs
- **EXPLAIN** trade-offs (active record vs repository, Dev Services vs Testcontainers, multi-document transactions vs single-document atomicity and application-level idempotency)
- **TEST** persistence behaviour with `@QuarkusTest` using Dev Services and explicit cleanup; never mock repositories inside persistence tests
- **VALIDATE** with `./mvnw compile` before and `./mvnw clean verify` after changes

## Safeguards

- **BLOCKING SAFETY CHECK**: Run `./mvnw compile` before ANY MongoDB refactoring — compilation failure is a HARD STOP
- **CRITICAL VALIDATION**: Run `./mvnw clean verify` after changes; confirm persistence tests pass with Dev Services before promoting
- **INJECTION SAFETY**: Never concatenate user input into Panache query strings or MongoDB JSON filters — use bound parameters or the `Document` builder API
- **ERROR HANDLING**: Catch `MongoWriteException` by `ErrorCategory`; never use a generic `catch (Exception e)` that swallows failures or returns `null`
- **API BOUNDARIES**: Do not return Panache entity instances directly from REST resources — map to DTOs to keep contracts stable and prevent internal field leakage
- **TRANSACTIONS**: Multi-document MongoDB transactions require replica set/session support — verify infrastructure compatibility before relying on them; prefer single-document atomic updates when possible
- **INCREMENTAL SAFETY**: Change one entity, repository, or service surface at a time; verify with `@QuarkusTest` and isolated test data between steps