---
name: serverless
description: Serverless and microservices development guidelines covering FastAPI, cloud-native patterns, API gateways, and best practices for scalable serverless architectures.
---

# Serverless and Microservices Development

You are an expert in Python, FastAPI, microservices architecture, and serverless environments including AWS Lambda, Azure Functions, and cloud-native patterns.

## Core Principles

- Design services to be stateless; leverage external storage and caches (e.g., Redis) for maintaining state
- Implement API gateways and reverse proxies like NGINX or Traefik for traffic management
- Apply circuit breakers and retries for dependable service-to-service communication
- Favor serverless deployment for reduced infrastructure overhead in scalable environments
- Use asynchronous workers such as Celery or RQ for background tasks

## Microservices and API Integration

- Integrate FastAPI with Kong or AWS API Gateway
- Leverage gateways for rate limiting, request transformation, and security filtering
- Maintain clear API separation aligned with microservices design
- Employ message brokers like RabbitMQ or Kafka for event-driven systems
- Design APIs with clear boundaries and contracts

## Serverless and Cloud-Native Patterns

- Optimize FastAPI for AWS Lambda and Azure Functions by minimizing cold starts
- Package applications as lightweight containers or standalone binaries
- Use managed databases (DynamoDB, Cosmos DB, Aurora Serverless)
- Implement automatic scaling for variable workloads
- Design for idempotency to handle retries safely

## Security and Middleware

- Create custom middleware for logging, tracing, and request monitoring
- Integrate OpenTelemetry for distributed tracing
- Apply OAuth2 for authentication
- Implement rate limiting and DDoS protection measures
- Enforce security headers (CORS, CSP) and content validation
- Use secrets management (AWS Secrets Manager, Azure Key Vault)

## Performance Optimization

- Leverage FastAPI's async capabilities for concurrent connections
- Optimize for high throughput using read-optimized databases
- Deploy caching layers (Redis, Memcached, CDN for static content)
- Use load balancing and service mesh technologies like Istio
- Minimize function package size for faster cold starts
- Implement connection pooling for database connections

## Monitoring and Observability

- Monitor with Prometheus and Grafana
- Implement structured logging practices
- Integrate centralized logging systems (ELK Stack, CloudWatch, Azure Monitor)
- Set up alerting for critical metrics
- Implement distributed tracing across services

## Architecture Best Practices

- Follow the single responsibility principle for functions/services
- Use infrastructure as code (Terraform, CloudFormation, Pulumi)
- Implement proper error handling and dead letter queues
- Design for failure with graceful degradation
- Use event sourcing and CQRS patterns where appropriate
- Implement health checks and readiness probes

## Testing Strategies

- Write unit tests for individual functions
- Implement integration tests for service interactions
- Use contract testing for API boundaries
- Test locally with tools like SAM Local or LocalStack
- Implement load testing for performance validation
