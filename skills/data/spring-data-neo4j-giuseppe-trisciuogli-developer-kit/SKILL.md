---
name: spring-data-neo4j
description: Expert in Spring Data Neo4j integration patterns for graph database development. Use when working with Neo4j graph databases, node entities, relationships, Cypher queries, reactive Neo4j operations, or Spring Data Neo4j repositories. Essential for graph data modeling, relationship mapping, custom queries, and Neo4j testing strategies.
version: 1.1.0
allowed-tools: Read, Write, Bash, Grep, Glob
category: backend
tags: [spring-data, neo4j, graph-database, database, java, spring-boot]
---

# Spring Data Neo4j Integration Patterns

## When to Use This Skill

To use this skill when you need to:
- Set up Spring Data Neo4j in a Spring Boot application
- Create and map graph node entities and relationships
- Implement Neo4j repositories with custom queries
- Write Cypher queries using @Query annotations
- Configure Neo4j connections and dialects
- Test Neo4j repositories with embedded databases
- Work with both imperative and reactive Neo4j operations
- Map complex graph relationships with bidirectional or unidirectional directions
- Use Neo4j's internal ID generation or custom business keys

## Overview

Spring Data Neo4j provides three levels of abstraction for Neo4j integration:
- **Neo4j Client**: Low-level abstraction for direct database access
- **Neo4j Template**: Medium-level template-based operations
- **Neo4j Repositories**: High-level repository pattern with query derivation

Key features include reactive and imperative operation modes, immutable entity mapping, custom query support via @Query annotation, Spring's Conversion Service integration, and full support for graph relationships and traversals.

## Quick Setup

### Dependencies

**Maven:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-neo4j</artifactId>
</dependency>
```

**Gradle:**
```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-data-neo4j'
}
```

### Configuration

**application.properties:**
```properties
spring.neo4j.uri=bolt://localhost:7687
spring.neo4j.authentication.username=neo4j
spring.neo4j.authentication.password=secret
```

**Configure Neo4j Cypher-DSL Dialect:**
```java
@Configuration
public class Neo4jConfig {

    @Bean
    Configuration cypherDslConfiguration() {
        return Configuration.newConfig()
            .withDialect(Dialect.NEO4J_5).build();
    }
}
```

## Basic Entity Mapping

### Node Entity with Business Key

```java
@Node("Movie")
public class MovieEntity {

    @Id
    private final String title;  // Business key as ID

    @Property("tagline")
    private final String description;

    private final Integer year;

    @Relationship(type = "ACTED_IN", direction = Direction.INCOMING)
    private List<Roles> actorsAndRoles = new ArrayList<>();

    @Relationship(type = "DIRECTED", direction = Direction.INCOMING)
    private List<PersonEntity> directors = new ArrayList<>();

    public MovieEntity(String title, String description, Integer year) {
        this.title = title;
        this.description = description;
        this.year = year;
    }
}
```

### Node Entity with Generated ID

```java
@Node("Movie")
public class MovieEntity {

    @Id @GeneratedValue
    private Long id;

    private final String title;

    @Property("tagline")
    private final String description;

    public MovieEntity(String title, String description) {
        this.id = null;  // Never set manually
        this.title = title;
        this.description = description;
    }

    // Wither method for immutability with generated IDs
    public MovieEntity withId(Long id) {
        if (this.id != null && this.id.equals(id)) {
            return this;
        } else {
            MovieEntity newObject = new MovieEntity(this.title, this.description);
            newObject.id = id;
            return newObject;
        }
    }
}
```

## Repository Patterns

### Basic Repository Interface

```java
@Repository
public interface MovieRepository extends Neo4jRepository<MovieEntity, String> {

    // Query derivation from method name
    MovieEntity findOneByTitle(String title);

    List<MovieEntity> findAllByYear(Integer year);

    List<MovieEntity> findByYearBetween(Integer startYear, Integer endYear);
}
```

### Reactive Repository

```java
@Repository
public interface MovieRepository extends ReactiveNeo4jRepository<MovieEntity, String> {

    Mono<MovieEntity> findOneByTitle(String title);

    Flux<MovieEntity> findAllByYear(Integer year);
}
```

**Imperative vs Reactive:**
- Use `Neo4jRepository` for blocking, imperative operations
- Use `ReactiveNeo4jRepository` for non-blocking, reactive operations
- **Do not mix imperative and reactive in the same application**
- Reactive requires Neo4j 4+ on the database side

## Custom Queries with @Query

```java
@Repository
public interface AuthorRepository extends Neo4jRepository<Author, Long> {

    @Query("MATCH (b:Book)-[:WRITTEN_BY]->(a:Author) " +
           "WHERE a.name = $name AND b.year > $year " +
           "RETURN b")
    List<Book> findBooksAfterYear(@Param("name") String name,
                                   @Param("year") Integer year);

    @Query("MATCH (b:Book)-[:WRITTEN_BY]->(a:Author) " +
           "WHERE a.name = $name " +
           "RETURN b ORDER BY b.year DESC")
    List<Book> findBooksByAuthorOrderByYearDesc(@Param("name") String name);
}
```

**Custom Query Best Practices:**
- Use `$parameterName` for parameter placeholders
- Use `@Param` annotation when parameter name differs from method parameter
- MATCH specifies node patterns and relationships
- WHERE filters results
- RETURN defines what to return

## Testing Strategies

### Neo4j Harness for Integration Testing

**Test Configuration:**
```java
@DataNeo4jTest
class BookRepositoryIntegrationTest {

    private static Neo4j embeddedServer;

    @BeforeAll
    static void initializeNeo4j() {
        embeddedServer = Neo4jBuilders.newInProcessBuilder()
            .withDisabledServer()  // No HTTP access needed
            .withFixture(
                "CREATE (b:Book {isbn: '978-0547928210', " +
                "name: 'The Fellowship of the Ring', year: 1954})" +
                "-[:WRITTEN_BY]->(a:Author {id: 1, name: 'J. R. R. Tolkien'}) " +
                "CREATE (b2:Book {isbn: '978-0547928203', " +
                "name: 'The Two Towers', year: 1956})" +
                "-[:WRITTEN_BY]->(a)"
            )
            .build();
    }

    @AfterAll
    static void stopNeo4j() {
        embeddedServer.close();
    }

    @DynamicPropertySource
    static void neo4jProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.neo4j.uri", embeddedServer::boltURI);
        registry.add("spring.neo4j.authentication.username", () -> "neo4j");
        registry.add("spring.neo4j.authentication.password", () -> "null");
    }

    @Autowired
    private BookRepository bookRepository;

    @Test
    void givenBookExists_whenFindOneByTitle_thenBookIsReturned() {
        Book book = bookRepository.findOneByTitle("The Fellowship of the Ring");
        assertThat(book.getIsbn()).isEqualTo("978-0547928210");
    }
}
```

## Examples

Progress from basic to advanced examples covering complete movie database, social network patterns, e-commerce product catalogs, custom queries, and reactive operations.

See [examples](./references/examples.md) for comprehensive code examples.

## Best Practices

### Entity Design
- Use immutable entities with final fields
- Choose between business keys (@Id) or generated IDs (@Id @GeneratedValue)
- Keep entities focused on graph structure, not business logic
- Use proper relationship directions (INCOMING, OUTGOING, UNDIRECTED)

### Repository Design
- Extend `Neo4jRepository` for imperative or `ReactiveNeo4jRepository` for reactive
- Use query derivation for simple queries
- Write custom @Query for complex graph patterns
- Don't mix imperative and reactive in same application

### Configuration
- Always configure Cypher-DSL dialect explicitly
- Use environment-specific properties for credentials
- Never hardcode credentials in source code
- Configure connection pooling based on load

### Testing
- Use Neo4j Harness for integration tests
- Provide test data via `withFixture()` Cypher queries
- Use `@DataNeo4jTest` for test slicing
- Test both successful and edge-case scenarios

### Architecture
- Use constructor injection exclusively
- Separate domain entities from DTOs
- Follow feature-based package structure
- Keep domain layer framework-agnostic

### Security
- Use Spring Boot property overrides for credentials
- Configure proper authentication and authorization
- Validate input parameters in service layer
- Use parameterized queries to prevent Cypher injection

## References

For detailed documentation including complete API reference, Cypher query patterns, and configuration options:

- [Annotations Reference](./references/reference.md#annotations-reference)
- [Cypher Query Language](./references/reference.md#cypher-query-language)
- [Configuration Properties](./references/reference.md#configuration-properties)
- [Repository Methods](./references/reference.md#repository-methods)
- [Projections and DTOs](./references/reference.md#projections-and-dtos)
- [Transaction Management](./references/reference.md#transaction-management)
- [Performance Tuning](./references/reference.md#performance-tuning)

### External Resources
- [Spring Data Neo4j Official Documentation](https://docs.spring.io/spring-data/neo4j/reference/)
- [Neo4j Developer Guide](https://neo4j.com/developer/)
- [Spring Data Commons Documentation](https://docs.spring.io/spring-data/commons/reference/)
