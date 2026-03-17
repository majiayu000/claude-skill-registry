---
name: arch-microservices
cluster: se-architecture
description: "Microservices: decomposition, API gateway Kong/Traefik, service mesh Istio, circuit breakers, saga/outbox"
tags: ["microservices","api-gateway","service-mesh","architecture"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "microservices api gateway service mesh circuit breaker saga istio"
---

# arch-microservices

## Purpose
This skill enables the AI to design, decompose, and implement microservices architectures using specific tools like Kong/Traefik for API gateways, Istio for service meshes, and patterns like circuit breakers and sagas for resilience. Focus on breaking down monoliths into independent services while ensuring scalability and fault tolerance.

## When to Use
Apply this skill when scaling applications beyond a monolith, such as e-commerce platforms with high traffic, or distributed systems needing isolation (e.g., payment processing separate from user management). Use it for new projects requiring API management or when retrofitting legacy apps for microservices to improve resilience and deployment speed.

## Key Capabilities
- Decompose monoliths: Identify bounded contexts and split into services, e.g., using domain-driven design to separate user and order services.
- API Gateway: Configure Kong for routing and rate limiting, or Traefik for dynamic service discovery.
- Service Mesh: Deploy Istio to handle inter-service communication, including mTLS and traffic shifting.
- Circuit Breakers: Implement with Istio's Envoy proxies to prevent cascading failures by tripping breakers on high error rates.
- Distributed Transactions: Use saga patterns for long-running processes or outbox for event-driven consistency, ensuring atomicity across services.

## Usage Patterns
To decompose a monolith, analyze dependencies and create separate services: Start by mapping modules to microservices, then define APIs. For API gateways, route requests through Kong by defining services and routes. In service meshes, inject Istio sidecars into pods for automatic traffic management. For circuit breakers, configure Istio policies to detect failures and fallback. Use sagas by orchestrating transactions via a coordinator service. Example pattern: Wrap service calls in a saga for multi-step operations, committing or compensating based on outcomes.

## Common Commands/API
For Kong API Gateway:
- Create a service: `curl -X POST http://localhost:8001/services --data "name=my-service&url=http://myapp.com"`
- Add a route: `curl -X POST http://localhost:8001/services/my-service/routes --data "paths[]=/api" --data "methods[]=GET"`
- Config format: Use Kong's declarative config in YAML, e.g., `_format_version: "1.1" services: - name: my-service url: http://myapp.com`

For Istio Service Mesh:
- Install Istio: `istioctl install -y --set profile=demo`
- Apply a VirtualService for circuit breaking: `kubectl apply -f - <<EOF apiVersion: networking.istio.io/v1alpha3 kind: VirtualService metadata: name: my-service spec: hosts: - my-service retries: attempts: 3 EOF`
- API Endpoint: Use Istio's control plane via `istiod` pod, e.g., query metrics with `kubectl exec -it istiod-xyz -- curl localhost:15014/stats`

For Saga/Outbox:
- Implement saga: Use a library like Axon Framework; code snippet:
  ```java
  Saga mySaga = Saga.builder().step(() -> orderService.createOrder()).step(() -> paymentService.process()).build();
  mySaga.execute();
  ```
- Outbox pattern: In a service, log events to a database table and process via a separate worker; config: SQL table like `CREATE TABLE outbox (id UUID, payload JSONB);`

Auth requirements: Set environment variables like `$KONG_API_KEY` for authenticated API calls, e.g., `curl -H "apikey: $KONG_API_KEY" http://localhost:8001/services`.

## Integration Notes
Integrate Kong with Istio by running Kong as an Istio ingress gateway: Deploy Kong pod with Istio sidecar injection via Kubernetes annotation `sidecar.istio.io/inject: "true"`. For Traefik, configure as a Kubernetes ingress controller using a ConfigMap: `kubectl apply -f traefik-config.yaml` with content like `api: {} entryPoints: web: address: ":80"`. When combining with other skills (e.g., se-deployment), ensure services are deployed with compatible labels, such as `app: my-microservice`, and use `$ISTIO_NAMESPACE` env var for multi-namespace setups. For saga patterns, integrate with message queues like Kafka by publishing events: `kafka-producer.send("topic", eventPayload)`.

## Error Handling
Handle circuit breaker errors in Istio by configuring fallbacks in VirtualServices: Set `route: fault: abort: percentage: 100 httpStatus: 503` for simulated failures, then monitor with `kubectl logs istiod-xyz | grep error`. For sagas, implement compensating actions on failure, e.g., if an order fails, call a rollback method: Code snippet:
  ```java
  try { saga.execute(); } catch (Exception e) { saga.compensate(); log.error("Saga failed: " + e.getMessage()); }
  ```
For API gateways, use Kong's plugins for error responses: Add a plugin with `curl -X POST http://localhost:8001/services/my-service/plugins --data "name=request-termination" --data "config.status_code=503"`. Always check logs with `kong logs` or `istioctl analyze` for validation errors, and use env vars like `$ERROR_WEBHOOK_URL` to notify external systems.

## Concrete Usage Examples
1. Decomposing and deploying a microservices app: For a blog platform, split into "posts" and "comments" services. Decompose by creating separate Docker images, then set up Kong: Command: `docker run -d -p 8000:8000 kong:latest; curl -X POST http://localhost:8000/services -d 'name=posts-service&url=http://posts-app:8080'`. Integrate with Istio: `istioctl create -f posts-virtualservice.yaml` to add circuit breaking.
   
2. Implementing resilience in a payment system: Use Istio for service mesh and saga for transactions. Configure a circuit breaker: `kubectl apply -f circuitbreaker.yaml` with content `apiVersion: networking.istio.io/v1alpha3 kind: DestinationRule spec: trafficPolicy: connectionPool: tcp: maxConnections: 100 outlierDetection: consecutiveErrors: 5 interval: 10m`. For sagas, orchestrate payment flow: Code snippet:
  ```java
  Saga paymentSaga = Saga.builder().step(() -> reserveFunds()).step(() -> processPayment()).build();
  paymentSaga.executeWithCompensation();
  ```

## Graph Relationships
- Related to: se-deployment (for deploying and scaling microservices built with this skill)
- Connected to: se-scaling (for integrating auto-scaling with Istio's traffic management)
- Part of cluster: se-architecture (shares tags like "architecture" for broader system design)
- Links to: se-monitoring (for observing metrics from Kong and Istio setups)
