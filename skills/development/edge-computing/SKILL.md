---
name: edge-computing
description: Use when designing edge computing architectures, serverless at edge, or distributed compute strategies. Covers edge functions, compute placement decisions, Cloudflare Workers, Lambda@Edge, and edge-native patterns.
allowed-tools: Read, Glob, Grep
---

# Edge Computing

Comprehensive guide to edge computing architecture - running compute closer to users for lower latency and better performance.

## When to Use This Skill

- Designing edge function architectures
- Deciding where to place compute (edge vs origin)
- Implementing serverless at edge
- Understanding edge platform capabilities
- Optimizing latency-sensitive applications
- Building globally distributed applications

## Edge Computing Fundamentals

### What is Edge Computing?

```text
Compute Placement Spectrum:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  User Device    Edge     Regional    Central    Origin     │
│  (Client)       (CDN)    (Cloud)     (Cloud)    (Cloud)    │
│                                                             │
│     ◄──────────────────────────────────────────────────►   │
│                                                             │
│  Lowest         ┌─────────────────────────────┐  Highest   │
│  Latency        │      EDGE COMPUTING         │  Latency   │
│                 │  (This skill's focus)       │            │
│                 └─────────────────────────────┘            │
│                                                             │
│  Limited        ◄─────────────────────────────►  Full      │
│  Resources                                       Resources  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Edge = Running code on CDN/network edge servers (100s of locations)
vs Regional = Running in a few cloud regions (10-20 locations)
vs Origin = Running in one primary location (1-3 locations)
```

### Edge vs Serverless vs Traditional

```text
Comparison:

                    Edge Functions    Cloud Functions    Containers/VMs
────────────────────────────────────────────────────────────────────────
Locations           100-300+          10-20             1-10
Cold Start          <50ms             100ms-seconds     N/A (always warm)
Execution Limit     10-30 seconds     15 minutes        Unlimited
Memory              128MB-1GB         256MB-10GB        Unlimited
CPU                 Limited           Standard          Full control
State               Stateless         Stateless         Stateful OK
Cost Model          Per request       Per request       Per instance
Best For            Low-latency,      General compute   Complex apps,
                    simple logic                        long-running

Use Cases by Type:
Edge: Auth, routing, personalization, A/B tests, redirects
Cloud Functions: APIs, webhooks, background processing
Containers: Full applications, databases, ML inference
```

### Edge Platform Architecture

```text
Edge Platform Components:

┌─────────────────────────────────────────────────────────────┐
│                    Control Plane                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Deploy   │  │  Config  │  │ Secrets  │  │ Metrics  │   │
│  │ API      │  │  Store   │  │  Mgmt    │  │ & Logs   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┼─────────────┼─────────────┘
                      │             │
        ╔═════════════╧═════════════╧═════════════╗
        ║           Global Distribution            ║
        ╚═════════════════════════════════════════╝
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│ Edge  │        │ Edge  │        │ Edge  │
│ POP 1 │        │ POP 2 │        │ POP N │
│┌─────┐│        │┌─────┐│        │┌─────┐│
││ V8  ││        ││ V8  ││        ││ V8  ││
││Isol.││        ││Isol.││        ││Isol.││
│└─────┘│        │└─────┘│        │└─────┘│
└───────┘        └───────┘        └───────┘

Execution Model:
- V8 Isolates: Lightweight isolation (not containers)
- Instant cold start (sub-50ms)
- Per-request execution
- Auto-scaled per POP
```

## Edge Function Patterns

### Request Interception

```text
Request/Response Lifecycle:

User Request ──► Edge Function ──► Origin (optional)
                      │
              ┌───────┴───────┐
              │               │
         Modify Request   Short-circuit
         (continue to    (return response
          origin)         from edge)

Use Cases:

1. URL Rewriting
   /old-page → /new-page
   /api/v1/* → /api/v2/*

2. Header Manipulation
   Add security headers
   Add request ID
   Normalize Accept-Language

3. Authentication
   Validate JWT at edge
   Check API key
   Redirect to login

4. A/B Testing
   Assign cohort
   Rewrite to variant URL

5. Bot Protection
   Challenge bots
   Block known bad actors

6. Geolocation Routing
   Route to regional origin
   Apply regional rules
```

### Response Transformation

```text
Response Transformation Patterns:

1. HTML Injection
   ┌─────────────────────────────────────────┐
   │ Inject analytics, A/B test scripts     │
   │ Add personalized content               │
   │ Insert GDPR banners by region          │
   └─────────────────────────────────────────┘

2. Content Optimization
   ┌─────────────────────────────────────────┐
   │ Compress responses                      │
   │ Image optimization/resizing            │
   │ Minification                           │
   └─────────────────────────────────────────┘

3. Response Caching
   ┌─────────────────────────────────────────┐
   │ Cache API responses at edge            │
   │ Assemble from cache fragments          │
   │ Serve stale while revalidating         │
   └─────────────────────────────────────────┘

4. Error Handling
   ┌─────────────────────────────────────────┐
   │ Fallback pages on origin error         │
   │ Custom error pages per region          │
   │ Retry logic with backoff               │
   └─────────────────────────────────────────┘
```

### Edge Storage Patterns

```text
Edge Storage Options:

1. Key-Value Store (KV)
   ├── Read-heavy workloads
   ├── Eventually consistent
   ├── Low latency reads
   └── Limited write throughput

   Use: Feature flags, configuration, user sessions

2. Durable Objects (Cloudflare)
   ├── Strong consistency
   ├── Stateful edge compute
   ├── Single-instance per ID
   └── WebSocket support

   Use: Real-time collaboration, chat, gaming state

3. Edge Databases
   ├── Distributed SQL (PlanetScale, Turso)
   ├── Read replicas at edge
   ├── Low latency reads
   └── Write to primary region

   Use: User data, product catalogs, CMS

4. R2/S3-Compatible Storage
   ├── Object storage at edge
   ├── No egress fees (some providers)
   └── Large file storage

   Use: Static assets, user uploads, backups
```

## Compute Placement Decisions

### Decision Framework

```text
Where Should This Run?

Question 1: Latency Requirements
├── <50ms required? → Edge
├── <200ms acceptable? → Regional cloud
└── Latency not critical? → Central origin

Question 2: Compute Complexity
├── Simple transformations? → Edge
├── Moderate logic? → Edge or Regional
└── Complex processing? → Regional or Central

Question 3: Data Dependencies
├── No data needed? → Edge
├── Read-heavy, cacheable? → Edge with cache
├── Strong consistency needed? → Regional
└── Write-heavy? → Central

Question 4: State Requirements
├── Stateless? → Edge
├── Session state? → Edge with KV/Durable Objects
└── Complex state? → Regional or Central

Question 5: Cost Sensitivity
├── High request volume, simple? → Edge (efficient)
├── CPU-intensive? → Regional (cheaper)
└── Long-running? → Central
```

### Hybrid Architecture

```text
Hybrid Edge + Origin Architecture:

┌─────────────────────────────────────────────────────────────┐
│                        Edge Layer                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Authentication/Authorization                     │    │
│  │  • Rate limiting                                    │    │
│  │  • Request routing                                  │    │
│  │  • Static content                                   │    │
│  │  • Simple personalization                           │    │
│  │  • Caching logic                                    │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────┘
                             │
                  Only complex requests pass through
                             │
┌────────────────────────────▼────────────────────────────────┐
│                       Origin Layer                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Business logic                                   │    │
│  │  • Database operations                              │    │
│  │  • Third-party integrations                         │    │
│  │  • ML inference                                     │    │
│  │  • Complex computations                             │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

Benefits:
- Offload work from origin
- Faster responses for simple requests
- Origin protected from attack traffic
- Scale each layer independently
```

## Edge Platforms

### Cloudflare Workers

```text
Cloudflare Workers:

Execution:
- V8 isolates (not containers)
- <5ms cold start
- 200+ edge locations
- 10ms CPU time (free) / 30s (paid)

Features:
├── Workers KV (key-value store)
├── Durable Objects (stateful)
├── R2 (object storage)
├── D1 (SQLite at edge)
├── Queues (async processing)
└── Hyperdrive (database connection pooling)

Example:
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Simple routing
    if (url.pathname.startsWith('/api/')) {
      return handleAPI(request, env);
    }

    // Serve static
    return env.ASSETS.fetch(request);
  }
}
```

### AWS Lambda@Edge / CloudFront Functions

```text
AWS Edge Options:

CloudFront Functions:
├── JavaScript only
├── Sub-millisecond start
├── 2MB memory
├── Request/response manipulation only
├── Cannot make network calls
└── Very cheap at scale

Lambda@Edge:
├── Node.js, Python
├── 128-3008MB memory
├── Up to 30s execution (origin response)
├── Can make network calls
├── Access to AWS services
└── Higher latency than CF Functions

Use Case Mapping:
CloudFront Functions: Headers, redirects, URL rewrites
Lambda@Edge: Auth, A/B testing, dynamic responses
Lambda (Regional): Full API logic, database access
```

### Fastly Compute@Edge

```text
Fastly Compute@Edge:

Execution:
- WebAssembly-based (Wasm)
- Multi-language (Rust, JS, Go, etc.)
- No cold start (pre-compiled)
- 50ms-120s execution time

Features:
├── Geolocation data
├── Device detection
├── Real-time logging
├── Edge dictionaries
└── Origin fetch with caching

Strengths:
- Best for dynamic content
- Real-time purging
- Advanced caching control
- Strong VCL migration path

Example (Rust):
use fastly::{Request, Response};

#[fastly::main]
fn main(req: Request) -> Result<Response, Error> {
    match req.get_path() {
        "/api" => handle_api(req),
        _ => Ok(req.send("origin")?)
    }
}
```

## Best Practices

```text
Edge Computing Best Practices:

1. Keep It Simple
   □ Edge = simple, fast operations
   □ Complex logic → origin
   □ Minimize dependencies
   □ Fail fast and gracefully

2. Optimize Cold Start
   □ Minimize code size
   □ Lazy load where possible
   □ Use global scope for init
   □ Avoid heavy dependencies

3. Handle Failures
   □ Origin unavailable handling
   □ Timeout handling
   □ Fallback responses
   □ Error tracking

4. Monitor Everything
   □ Latency percentiles
   □ Error rates
   □ Cold start frequency
   □ Origin fallthrough rate

5. Security
   □ Validate input at edge
   □ Rate limit early
   □ Sanitize data
   □ Use secrets management

6. Cost Optimization
   □ Cache aggressively
   □ Right-size execution time
   □ Use appropriate tier
   □ Monitor usage patterns
```

## Anti-Patterns

```text
Edge Computing Anti-Patterns:

1. "Everything at Edge"
   ❌ Moving all logic to edge
   ✓ Strategic placement based on requirements

2. "Database at Edge"
   ❌ Complex database operations at edge
   ✓ Read replicas or cached data at edge

3. "Ignoring Cold Starts"
   ❌ Large bundles, heavy initialization
   ✓ Optimize bundle size, lazy loading

4. "Origin Coupling"
   ❌ Edge functions tightly coupled to origin
   ✓ Edge functions should work independently when possible

5. "No Fallbacks"
   ❌ Edge function fails = user sees error
   ✓ Graceful degradation, cached responses

6. "Synchronous Everything"
   ❌ Waiting for slow operations at edge
   ✓ Async processing, fire-and-forget logging
```

## Related Skills

- `cdn-architecture` - CDN and caching patterns
- `serverless-patterns` - Serverless architecture
- `latency-optimization` - End-to-end latency reduction
- `multi-region-deployment` - Global infrastructure
