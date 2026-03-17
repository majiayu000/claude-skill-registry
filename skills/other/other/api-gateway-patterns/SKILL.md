---
name: api-gateway-patterns
description: API Gateway patterns for routing, authentication, rate limiting, and service composition in microservices architectures. Use when implementing API gateways, building BFF layers, or managing service-to-service communication at scale.
---

# API Gateway Patterns

Expert guidance for implementing API gateways with routing, authentication, traffic management, and service composition patterns for microservices architectures at scale.

## When to Use This Skill

- Implementing API gateway infrastructure for microservices
- Designing Backend for Frontend (BFF) layers
- Adding authentication and authorization at the gateway level
- Implementing rate limiting, circuit breakers, and retry logic
- Setting up service discovery and dynamic routing
- Building API composition and aggregation layers
- Managing cross-cutting concerns (logging, monitoring, CORS)
- Evaluating gateway solutions (Kong, Nginx, Envoy, AWS API Gateway)

## Core Concepts

### Gateway Responsibilities
**Routing**: Direct requests to appropriate backend services based on path, headers, or host
**Security**: Centralized authentication, authorization, and API key validation
**Traffic Management**: Rate limiting, circuit breakers, retry logic
**Composition**: Aggregate multiple service calls into unified responses
**Transformation**: Modify requests/responses for client optimization or legacy adaptation

### Architecture Patterns
**Single Gateway**: One gateway for all clients (simple, potential bottleneck)
**BFF Pattern**: Separate gateway per client type (mobile, web, admin) - optimized for each
**GraphQL Gateway**: Schema stitching across services, client-driven data fetching
**Service Mesh**: Distributed gateway pattern with sidecar proxies (Istio, Linkerd)

## Quick Reference

| Task | Load reference |
| --- | --- |
| Routing strategies (path, header, host-based) | `skills/api-gateway-patterns/references/routing-patterns.md` |
| Request/response transformation | `skills/api-gateway-patterns/references/transformation.md` |
| API composition and aggregation | `skills/api-gateway-patterns/references/composition.md` |
| Authentication & authorization (JWT, OAuth, RBAC) | `skills/api-gateway-patterns/references/authentication.md` |
| Traffic management (rate limiting, circuit breakers) | `skills/api-gateway-patterns/references/traffic-management.md` |
| Backend for Frontend (BFF) pattern | `skills/api-gateway-patterns/references/bff-pattern.md` |
| Service discovery integration | `skills/api-gateway-patterns/references/service-discovery.md` |
| Gateway implementations (Kong, Nginx, Envoy, AWS) | `skills/api-gateway-patterns/references/implementations.md` |

## Implementation Workflow

### Phase 1: Requirements Analysis
1. **Identify client types**: Mobile, web, admin, partners
2. **Map service landscape**: Catalog backend services and endpoints
3. **Define cross-cutting concerns**: Auth, logging, monitoring, CORS
4. **Determine composition needs**: Which endpoints require aggregation?
5. **Establish SLAs**: Latency, throughput, availability targets

### Phase 2: Gateway Design
1. **Choose architecture**: Single gateway vs BFF vs GraphQL
2. **Select implementation**: Kong, Nginx, Envoy, AWS API Gateway
3. **Design routing rules**: Path-based, header-based, host-based
4. **Plan authentication**: JWT, OAuth 2.0, API keys, or hybrid
5. **Define traffic policies**: Rate limits, circuit breakers, timeouts

### Phase 3: Implementation
1. **Set up infrastructure**: Deploy gateway instances, configure load balancer
2. **Implement routing**: Configure service discovery and route definitions
3. **Add authentication**: JWT validation, OAuth integration, API key management
4. **Apply traffic management**: Rate limiting, circuit breakers, retry logic
5. **Enable observability**: Distributed tracing, metrics, structured logging

### Phase 4: Testing & Optimization
1. **Load testing**: Verify performance under expected and peak load
2. **Failure injection**: Test circuit breakers and retry logic
3. **Security testing**: Verify auth flows, token validation, RBAC policies
4. **Latency optimization**: Cache strategies, connection pooling
5. **Monitor and tune**: Adjust timeouts, limits based on real traffic

## Best Practices

1. **Centralize Cross-Cutting Concerns**: Authentication, logging, monitoring at gateway
2. **Keep Gateway Lightweight**: Avoid complex business logic, delegate to services
3. **Implement Health Checks**: Monitor upstream service health, remove unhealthy instances
4. **Use Circuit Breakers**: Prevent cascading failures, fail fast
5. **Apply Rate Limiting**: Protect services from overload, implement tiered limits
6. **Enable Observability**: Distributed tracing, metrics, structured logging
7. **Version APIs**: Support multiple API versions, plan deprecation
8. **Secure Communication**: TLS everywhere, mutual TLS for service-to-service
9. **Cache Strategically**: Response caching, but invalidate properly
10. **Test Resilience**: Chaos engineering, failure injection, load testing

## Common Mistakes

1. **Business Logic in Gateway**: Keep gateway focused on routing/security, not business rules
2. **Chatty Composition**: Too many upstream calls (use BFF, GraphQL, or caching)
3. **Single Point of Failure**: Deploy redundantly, use load balancers
4. **No Timeout Configuration**: Always set connection/read timeouts to prevent hanging requests
5. **Ignoring Backpressure**: Implement queue limits, graceful degradation
6. **Over-Aggregation**: Don't make gateway do too much work (compute-heavy transformations)
7. **Inadequate Monitoring**: Must track latency, errors, throughput at gateway level
8. **No Rate Limiting**: Services will be overwhelmed eventually without protection
9. **Synchronous Everything**: Use async patterns for non-critical operations
10. **No Version Strategy**: Breaking changes break all clients simultaneously

## Resources

- **Kong**: https://docs.konghq.com/gateway/latest/
- **Nginx**: https://nginx.org/en/docs/
- **Envoy**: https://www.envoyproxy.io/docs/envoy/latest/
- **AWS API Gateway**: https://docs.aws.amazon.com/apigateway/
- **Patterns**: "Microservices Patterns" by Chris Richardson
- **Service Mesh**: https://istio.io/latest/docs/
- **Circuit Breakers**: Martin Fowler's CircuitBreaker pattern
- **BFF Pattern**: Sam Newman's "Building Microservices"
