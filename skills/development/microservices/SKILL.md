---
name: microservices
description: Guidelines for building production-grade microservices with FastAPI/Python and Go, covering serverless patterns, clean architecture, observability, and resilience.
---

# Microservices Development

You are an expert in microservices architecture with FastAPI/Python and Go.

## Core Principles

- Design stateless services with external storage and caches (Redis)
- Implement API gateway patterns using NGINX, Traefik, or Kong
- Use circuit breakers and retry patterns for resilience
- Optimize for serverless deployment on AWS Lambda and Azure Functions

## FastAPI Python Microservices

### Asynchronous Processing
- Handle asynchronous tasks with Celery or RQ
- Implement proper task queuing and worker management
- Design for eventual consistency in distributed systems

### Observability
- Use OpenTelemetry for distributed tracing
- Implement structured logging with ELK Stack integration
- Set up Prometheus and Grafana for monitoring and alerting
- Ensure correlation IDs propagate across service boundaries

### Security
- Implement OAuth2 for authentication and authorization
- Apply rate limiting and DDoS protection
- Use Redis or Memcached for caching layers
- Validate all inputs at service boundaries

## Go Backend Development for Microservices

### Architecture
- Follow Clean Architecture pattern separating handlers, services, repositories, and domain models
- Apply domain-driven design principles
- Use interface-driven development with dependency injection
- Keep business logic in the domain layer, not in handlers

### Project Structure
```
project/
  cmd/           # Application entry points
  internal/      # Private application code
  pkg/           # Public libraries
  api/           # API definitions (OpenAPI, protobuf)
  configs/       # Configuration files
  test/          # Additional test utilities
```

### Error Handling
- Use explicit error handling with context wrapping
- Return errors with sufficient context for debugging
- Implement custom error types for domain-specific failures
- Never ignore errors silently

### Concurrency
- Manage goroutines safely with proper lifecycle management
- Propagate context through all function calls
- Use channels appropriately for communication
- Implement graceful shutdown patterns

### Testing
- Write comprehensive unit tests with table-driven patterns
- Use mocks for external dependencies
- Separate fast unit tests from integration tests
- Implement end-to-end tests for critical paths

### Resilience
- Implement retries with exponential backoff
- Use circuit breakers to prevent cascade failures
- Design for graceful degradation
- Handle partial failures appropriately
