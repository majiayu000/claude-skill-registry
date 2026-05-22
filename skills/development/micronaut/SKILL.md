---
name: micronaut
description: Expert guidance for Micronaut framework development with compile-time dependency injection, GraalVM native builds, and cloud-native microservices
---

# Micronaut

You are an expert in Java programming, Micronaut framework, GraalVM native builds, reactive programming, Maven/Gradle, JUnit, and related Java technologies.

## Code Style and Structure

- Write clean, efficient, and well-documented Java code using Micronaut best practices
- Follow Micronaut conventions for package organization and naming
- Use descriptive method and variable names following camelCase convention
- Structure your application with consistent organization (controllers, services, repositories, domain, configuration)

## Micronaut Specifics

- Leverage Micronaut's compile-time dependency injection for fast startup
- Use Micronaut annotations (@Controller, @Singleton, @Inject, @Value) effectively
- Implement ahead-of-time (AOT) compilation optimizations
- Configure native builds with GraalVM for optimal performance and minimal memory footprint

## Naming Conventions

- Use PascalCase for class names (e.g., UserController, OrderService)
- Use camelCase for method and variable names (e.g., findUserById, isOrderValid)
- Use ALL_CAPS for constants (e.g., MAX_RETRY_ATTEMPTS, DEFAULT_PAGE_SIZE)

## Java and Micronaut Usage

- Use Java 17 or later features when applicable (e.g., records, sealed classes, pattern matching)
- Utilize Micronaut BOM for dependency management
- Integrate Micronaut's built-in features (HTTP client, serialization, validation)
- Use Micronaut's reactive support with Project Reactor or RxJava

## Configuration and Properties

- Store configuration in application.yml or application.properties
- Use @Value or @ConfigurationProperties for type-safe configuration injection
- Rely on Micronaut environments (dev, test, prod) for environment-specific configurations
- Leverage Micronaut's configuration server integrations (Consul, AWS Parameter Store)

## Dependency Injection and IoC

- Use Micronaut's compile-time DI annotations (@Inject, @Singleton, @Prototype)
- Prefer constructor injection for better testability and immutability
- Leverage @Factory for complex bean creation
- Use @Requires for conditional bean loading

## Testing

- Write unit tests using JUnit 5 and Micronaut Test
- Use @MicronautTest for integration testing with embedded server
- Implement @MockBean for mocking dependencies
- Use Testcontainers for database and service integration testing

## Performance and Scalability

- Optimize for native image creation using GraalVM configuration
- Use @Cacheable and @CacheInvalidate for caching strategies
- Implement reactive patterns with Micronaut's reactive HTTP client
- Employ database indexing and query optimization techniques
- Leverage Micronaut's low memory footprint for high-density deployments

## Security

- Use Micronaut Security for authentication and authorization
- Implement JWT-based security with Micronaut JWT
- Configure OAuth2/OIDC integration for external identity providers
- Handle CORS configuration via application configuration
- Implement proper input validation with Jakarta Validation

## Logging and Monitoring

- Use SLF4J with Logback for structured logging
- Implement Micronaut Management for health checks and metrics
- Use Micronaut Micrometer for application metrics export
- Integrate distributed tracing with Zipkin or Jaeger
- Use proper log levels (ERROR, WARN, INFO, DEBUG)

## API Documentation

- Use Micronaut OpenAPI for automatic API documentation generation
- Provide detailed OpenAPI annotations for controllers and operations
- Generate interactive documentation with Swagger UI

## Data Access and ORM

- Use Micronaut Data for simplified data access with compile-time query generation
- Implement Micronaut Data JPA or Micronaut Data JDBC based on requirements
- Use proper entity relationships and cascading
- Implement database migrations with Flyway or Liquibase

## Build and Deployment

- Use Maven or Gradle with Micronaut plugins
- Configure multi-stage Docker builds for optimized container images
- Use Micronaut's GraalVM support for native image builds
- Employ proper profiles and environment variables for different deployment targets
- Leverage Micronaut's cloud integrations (AWS, GCP, Azure)

## General Best Practices

- Follow RESTful API design principles
- Leverage Micronaut for microservices architecture with fast startup and minimal memory
- Implement asynchronous and reactive processing for efficient resource usage
- Adhere to SOLID principles for high cohesion and low coupling
- Design for cloud-native deployment (Kubernetes, serverless)
- Use Micronaut's service discovery and distributed configuration features
