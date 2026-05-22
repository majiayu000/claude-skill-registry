---
name: edge-computing-patterns
description: Use when deploying to Cloudflare Workers, Vercel Edge, or Deno Deploy. Covers edge middleware, streaming, runtime constraints, and globally distributed low-latency patterns.
context: fork
agent: frontend-ui-developer
version: 1.1.0
author: AI Agent Hub
tags: [edge, cloudflare, vercel, deno, serverless, 2025]
user-invocable: false
---

# Edge Computing Patterns

## Overview

Edge computing runs code closer to users worldwide, reducing latency from seconds to milliseconds. This skill covers Cloudflare Workers, Vercel Edge Functions, and Deno Deploy patterns for building globally distributed applications.

**When to use this skill:**
- Global applications requiring <50ms latency
- Authentication/authorization at the edge
- A/B testing and feature flags
- Geo-routing and localization
- API rate limiting and DDoS protection
- Transforming responses (image optimization, HTML rewriting)

## Platform Comparison

| Feature | Cloudflare Workers | Vercel Edge | Deno Deploy |
|---------|-------------------|-------------|-------------|
| Cold Start | <1ms | <10ms | <10ms |
| Locations | 300+ | 100+ | 35+ |
| Runtime | V8 Isolates | V8 Isolates | Deno |
| Max Duration | 30s (paid: unlimited) | 25s | 50ms-5min |
| Free Tier | 100k req/day | 100k req/month | 100k req/month |

## Platform-Specific Implementation

For detailed code examples and patterns, load the appropriate reference file:

### Cloudflare Workers
**Reference:** `references/cloudflare-workers.md`
- Worker fetch handlers and routing
- KV storage patterns (eventually consistent)
- Durable Objects for stateful edge
- Wrangler CLI and wrangler.toml configuration
- Caching strategies with Cache API

### Vercel Edge Functions
**Reference:** `references/vercel-edge.md`
- Edge Middleware for Next.js (auth, A/B testing, geo-routing)
- Edge API routes with streaming
- Edge Config for feature flags
- Geolocation-based routing patterns

### Runtime Differences
**Reference:** `references/runtime-differences.md`
- Node.js APIs NOT available at edge
- Web API compatibility matrix
- Polyfill strategies for crypto, Buffer, streams

## Edge Runtime Constraints

**Available APIs:**
- fetch, Request, Response, Headers
- URL, URLSearchParams
- TextEncoder, TextDecoder
- ReadableStream, WritableStream
- crypto, SubtleCrypto (Web Crypto API)
- Web APIs (atob, btoa, setTimeout, etc.)

**NOT Available:**
- Node.js APIs (fs, path, child_process)
- Native modules and binary dependencies
- File system access
- Some npm packages with Node.js dependencies

## Common Patterns Summary

### Authentication at Edge
Verify JWT tokens at edge for sub-millisecond auth checks. See `references/cloudflare-workers.md` for implementation.

### Rate Limiting
Use KV (Cloudflare) or Edge Config (Vercel) for distributed rate limiting. Pattern: IP-based key with TTL expiration.

### Edge Caching
Cache API with cache-aside pattern. Check cache first, fetch origin on miss, store with TTL.

### A/B Testing
Assign users to buckets via cookie, rewrite URLs to variant pages. See `references/vercel-edge.md` for middleware pattern.

### Geo-Routing
Access request.cf.country (Cloudflare) or request.geo (Vercel) for location-based routing.

## Best Practices

- Keep bundles small (<1MB compressed)
- Use streaming for large responses to avoid timeouts
- Leverage platform caching (KV, Durable Objects, Edge Config)
- Handle errors gracefully (edge errors cannot be recovered)
- Test cold starts and warm starts separately
- Monitor edge function performance and error rates
- Use environment variables for secrets (never hardcode)
- Implement proper CORS headers for cross-origin requests

## Decision Guide

| Use Case | Recommended Platform |
|----------|---------------------|
| Global CDN + compute | Cloudflare Workers |
| Next.js middleware | Vercel Edge |
| TypeScript-first | Deno Deploy |
| Stateful edge | Cloudflare Durable Objects |
| Feature flags | Vercel Edge Config |
| Real-time collaboration | Cloudflare Durable Objects + WebSockets |

## Resources

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions)
- [Deno Deploy](https://deno.com/deploy/docs)

## Related Skills

- `caching-strategies` - Redis caching patterns that complement edge KV storage and CDN caching
- `react-server-components-framework` - Next.js App Router patterns for edge-rendered React components
- `streaming-api-patterns` - SSE and streaming responses for edge function output
- `api-design-framework` - REST API patterns for edge-deployed endpoints

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary Runtime | V8 Isolates | Sub-millisecond cold starts, security isolation |
| State Management | KV / Edge Config | Eventually consistent, globally replicated |
| Stateful Workloads | Durable Objects | Strong consistency when needed |
| Auth Strategy | JWT at Edge | No origin roundtrip, sub-ms verification |
| Cache Pattern | Cache-Aside | Simple, effective, CDN-compatible |

## Capability Details

### cloudflare-workers
**Keywords:** cloudflare, workers, kv, durable objects, r2, wrangler
**Reference:** references/cloudflare-workers.md
**Solves:**
- How do I deploy to Cloudflare Workers?
- Cloudflare KV storage patterns
- Durable Objects for stateful edge
- Wrangler CLI usage and configuration

### vercel-edge
**Keywords:** vercel edge, edge functions, edge middleware, geolocation, next.js
**Reference:** references/vercel-edge.md
**Solves:**
- How do I use Vercel Edge Functions?
- Edge middleware patterns (auth, A/B testing)
- Geo-based routing and localization
- Edge streaming responses

### runtime-differences
**Keywords:** edge runtime, web apis, node.js compatibility, polyfills
**Reference:** references/runtime-differences.md
**Solves:**
- What Node.js APIs are NOT available at edge?
- Edge-compatible alternatives to Node APIs
- How to polyfill crypto, base64, buffers
- Package compatibility for edge runtimes

### edge-caching
**Keywords:** edge cache, cdn, cache-control, stale-while-revalidate, invalidation
**Solves:**
- How do I cache at the edge?
- CDN caching strategies and headers
- Stale-while-revalidate patterns
- Cache invalidation strategies
- Personalization at edge

### edge-function-template
**Keywords:** edge function, template, boilerplate, production-ready
**Solves:**
- How do I structure an edge function?
- Production-ready edge function template
- Error handling and validation patterns
- CORS, rate limiting, caching setup

### edge-middleware-template
**Keywords:** middleware, next.js, authentication, a/b testing
**Solves:**
- How do I write Next.js edge middleware?
- Authentication middleware patterns
- A/B testing and feature flags
- Geolocation routing middleware

### deployment-checklist
**Keywords:** deployment, checklist, production, monitoring
**Reference:** checklists/edge-deployment-checklist.md
**Solves:**
- What should I check before deploying to edge?
- Edge deployment best practices
- Production readiness checklist
- Monitoring and debugging setup

## Quick Example

```typescript
// Cloudflare Worker - Basic fetch handler
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    // Geo-based routing
    const country = request.cf?.country || 'US';

    // Edge caching
    const cacheKey = url.pathname + "-" + country;
    const cached = await caches.default.match(cacheKey);
    if (cached) return cached;

    const response = await fetch(request);
    return response;
  }
}
```