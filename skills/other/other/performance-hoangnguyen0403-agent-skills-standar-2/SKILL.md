---
name: NestJS Performance
description: Fastify adapter, Scope management, and Compression.
metadata:
  labels: [nestjs, performance, fastify]
  triggers:
    files: ['main.ts']
    keywords: [FastifyAdapter, compression, SINGLETON, REQUEST scope]
---

# Performance Tuning

## **Priority: P1 (OPERATIONAL)**

High-performance patterns and optimization techniques for NestJS applications.

- **Adapter**: Use `FastifyAdapter` instead of Express (2x throughput).
- **Compression**: Enable Gzip/Brotli compression.

  ```typescript
  // main.ts
  app.use(compression());
  ```

- **Keep-Alive**: Configure `http.Agent` keep-alive settings to reuse TCP connections for upstream services.

## Scope & Dependency Injection

- **Default Scope**: Adhere to `SINGLETON` scope (default).
- **Request Scope**: AVOID `REQUEST` scope unless absolutely necessary.
  - **Pro Tip**: A single request-scoped service makes its entire injection chain request-scoped.
  - **Solution**: Use **Durable Providers** (`durable: true`) for multi-tenancy.
- **Lazy Loading**: Use `LazyModuleLoader` for heavyweight modules (e.g., Admin panels).

## Caching Strategy

- **Application Cache**: Use `@nestjs/cache-manager` for computation results.
  - **Deep Dive**: See **[Caching & Redis](../caching/SKILL.md)** for L1/L2 strategies and Invalidation patterns.
- **HTTP Cache**: Set `Cache-Control` headers for client-side caching (CDN/Browser).
- **Distributed**: In microservices, use Redis store, not memory store.

## Queues & Async Processing

- **Offloading**: Never block the HTTP request for long-running tasks (Emails, Reports, webhooks).
- **Tool**: Use `@nestjs/bull` (BullMQ) or RabbitMQ (`@nestjs/microservices`).
  - **Pattern**: Producer (Controller) -> Queue -> Consumer (Processor).

## Serialization

- **Warning**: `class-transformer` is CPU expensive.
- **Optimization**: For high-throughput READ endpoints, consider manual mapping or using `fast-json-stringify` (built-in fastify serialization) instead of interceptors.

## Database Tuning

- **Projections**: Always use `select: []` to fetch only needed columns.
- **N+1**: Prevent N+1 queries by using `relations` carefully or `DataLoader` for Graph/Field resolvers.
- **Connection Pooling**: Configure pool size (e.g., `pool: { min: 2, max: 10 }`) in config to match DB limits.

## Profiling & Scaling

- **Offloading**: Move CPU-heavy tasks (Image processing, Crypto) to `worker_threads`.
- **Clustering**: For non-containerized environments, use `ClusterModule` to utilize all CPU cores. In K8s, prefer ReplicaSets.
