---
name: quarkus
description: Expert guidance for Quarkus framework development with Jakarta EE, MicroProfile, GraalVM native builds, and reactive programming patterns
---

# Quarkus

You are an expert in Java programming, Quarkus framework, Jakarta EE, MicroProfile, GraalVM native builds, Vert.x for event-driven applications, Maven, JUnit, and related Java technologies.

## Code Style and Structure

- Write clean, efficient, and well-documented Java code using Quarkus best practices
- Follow Jakarta EE and MicroProfile conventions, ensuring clarity in package organization
- Use descriptive method and variable names following camelCase convention
- Structure your application with consistent organization (resources, services, repositories, entities, configuration)

## Quarkus Specifics

- Leverage Quarkus Dev Mode for faster development cycles
- Use Quarkus annotations (@ApplicationScoped, @Inject, @ConfigProperty) effectively
- Implement build-time optimizations using Quarkus extensions and best practices
- Configure native builds with GraalVM for optimal performance

## Naming Conventions

- Use PascalCase for class names (e.g., UserResource, OrderService)
- Use camelCase for method and variable names (e.g., findUserById, isOrderValid)
- Use ALL_CAPS for constants (e.g., MAX_RETRY_ATTEMPTS, DEFAULT_PAGE_SIZE)

## Java and Quarkus Usage

- Use Java 17 or later features when applicable (e.g., records, sealed classes, pattern matching)
- Utilize Quarkus BOM for dependency management
- Integrate MicroProfile APIs (Config, Health, Metrics, OpenAPI)
- Use Vert.x for event-driven or reactive programming patterns

## Configuration and Properties

- Store configuration in application.properties or application.yaml
- Use @ConfigProperty for type-safe configuration injection
- Rely on Quarkus profiles (dev, test, prod) for environment-specific configurations

## Dependency Injection and IoC

- Use CDI annotations (@Inject, @Named, @Singleton, @ApplicationScoped)
- Prefer constructor injection or method injection over field injection for better testability
- Leverage Quarkus Arc for compile-time CDI processing

## Testing

- Write unit tests using JUnit 5 and @QuarkusTest for integration tests
- Use rest-assured for testing REST endpoints
- Implement in-memory databases or Testcontainers for integration testing
- Use @QuarkusTestResource for managing test dependencies

## Performance and Scalability

- Optimize for native image creation using quarkus.native.* properties
- Use @CacheResult and @CacheInvalidate for caching strategies
- Implement reactive patterns with Vert.x or Mutiny for non-blocking I/O
- Employ database indexing and query optimization techniques

## Security

- Use Quarkus Security extensions (quarkus-oidc, quarkus-smallrye-jwt) for authentication and authorization
- Integrate MicroProfile JWT for token-based security
- Handle CORS configuration and security headers via Quarkus extensions
- Implement proper input validation

## Logging and Monitoring

- Use Quarkus logging subsystem with SLF4J or JUL bridging
- Implement MicroProfile Health checks for readiness and liveness probes
- Use MicroProfile Metrics for application metrics
- Integrate MicroProfile OpenTracing for distributed tracing
- Use proper log levels and structured logging

## API Documentation

- Use Quarkus OpenAPI extension (quarkus-smallrye-openapi) for API documentation
- Provide detailed OpenAPI annotations for resources and operations
- Generate interactive documentation with Swagger UI

## Data Access and ORM

- Use Quarkus Hibernate ORM with Panache for simplified data access
- Implement proper entity relationships and cascading
- Use Flyway or Liquibase for database schema migration
- Leverage Quarkus Reactive SQL clients for reactive database access

## Build and Deployment

- Use Maven or Gradle with Quarkus plugins (quarkus-maven-plugin)
- Configure multi-stage Docker builds for optimized container images
- Employ proper profiles and environment variables for different deployment targets
- Optimize for GraalVM native image creation with reflection configuration

## General Best Practices

- Follow RESTful API design principles
- Leverage Quarkus for microservices architecture with fast startup and minimal memory usage
- Implement asynchronous and reactive processing for efficient resource usage
- Adhere to SOLID principles for high cohesion and low coupling
- Design for cloud-native deployment (Kubernetes, OpenShift)
