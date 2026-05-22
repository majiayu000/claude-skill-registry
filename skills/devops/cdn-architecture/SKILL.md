---
name: cdn-architecture
description: Use when designing content delivery networks, caching strategies, or global content distribution. Covers CDN architecture, cache hierarchies, origin shielding, cache invalidation, and edge optimization.
allowed-tools: Read, Glob, Grep
---

# CDN Architecture

Comprehensive guide to Content Delivery Network architecture - caching, distribution, and edge optimization patterns.

## When to Use This Skill

- Designing CDN strategies for web applications
- Implementing cache hierarchies
- Optimizing origin load and performance
- Understanding cache invalidation patterns
- Selecting CDN providers and features
- Configuring edge caching rules

## CDN Fundamentals

### How CDNs Work

```text
Without CDN:
User (Tokyo) ───────────────────► Origin (New York)
              2000km, ~200ms RTT

With CDN:
User (Tokyo) ──► Edge (Tokyo) ──► Origin (New York)
              <10km, ~10ms RTT    (only on cache miss)

CDN Benefits:
├── Reduced latency (content served from nearby)
├── Origin offload (fewer requests hit origin)
├── DDoS protection (distributed, absorbs attacks)
├── Scalability (handles traffic spikes)
└── Reliability (multiple POPs for redundancy)
```

### CDN Architecture

```text
CDN Components:

┌─────────────────────────────────────────────────────────┐
│                     Internet                             │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │  Edge   │    │  Edge   │    │  Edge   │
    │ POP 1   │    │ POP 2   │    │ POP 3   │
    │(Tokyo)  │    │(London) │    │(NY)     │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
              ┌──────────▼──────────┐
              │    Origin Shield    │
              │    (Mid-tier)       │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │       Origin        │
              │    (Your servers)   │
              └─────────────────────┘

Terminology:
- POP: Point of Presence (edge location)
- Edge: Servers closest to users
- Origin Shield: Optional intermediate cache
- Origin: Your actual servers
```

### Cache Hit/Miss Flow

```text
Request Flow:

1. User requests asset.js

2. Edge Cache Check
   ┌─────────────────────────────┐
   │ Is asset.js in edge cache? │
   └─────────────┬───────────────┘
                 │
        ┌────────┴────────┐
        │                 │
   HIT: Return        MISS: Forward
   immediately        to origin shield
   (~10ms)

3. Origin Shield Check (if configured)
   ┌─────────────────────────────┐
   │ Is asset.js in shield?     │
   └─────────────┬───────────────┘
                 │
        ┌────────┴────────┐
        │                 │
   HIT: Return        MISS: Forward
   to edge            to origin
   (~50ms)

4. Origin Fetch
   ┌─────────────────────────────┐
   │ Fetch from origin server   │
   │ Cache in shield and edge   │
   └─────────────────────────────┘
   (~200ms)

Key Metrics:
- Cache Hit Ratio (CHR): % of requests served from cache
- Time To First Byte (TTFB): Latency to receive first byte
- Origin Requests: Number of requests reaching origin
```

## Caching Strategies

### Cache-Control Headers

```text
Cache-Control Directives:

Browser + CDN:
Cache-Control: public, max-age=31536000
└── Cacheable by anyone for 1 year

CDN Only:
Cache-Control: private, no-store
└── Don't cache (sensitive data)

Short-term Cache:
Cache-Control: public, max-age=300, s-maxage=3600
└── Browser: 5 min, CDN: 1 hour

Stale-While-Revalidate:
Cache-Control: public, max-age=3600, stale-while-revalidate=86400
└── Serve stale for 24h while revalidating in background

CDN-Specific Headers:
CDN-Cache-Control: max-age=3600
Surrogate-Control: max-age=3600
Cloudflare-CDN-Cache-Control: max-age=3600
```

### Caching Decision Matrix

```text
Content Type → Caching Strategy:

Static Assets (JS, CSS, images):
├── Long TTL (1 year)
├── Content-based filename (hash)
├── Immutable flag
└── Cache-Control: public, max-age=31536000, immutable

HTML Pages:
├── Short TTL or no-cache
├── Revalidation-based
├── ETag/Last-Modified
└── Cache-Control: no-cache (revalidate every time)

API Responses (public data):
├── Short to medium TTL
├── Vary by appropriate headers
├── Consider stale-while-revalidate
└── Cache-Control: public, max-age=60, stale-while-revalidate=300

API Responses (personalized):
├── Don't cache at CDN
├── May cache at browser with auth
└── Cache-Control: private, no-store

User-Generated Content:
├── Medium TTL
├── Consider purge on update
└── Cache-Control: public, max-age=3600
```

### Vary Header

```text
Vary Header Usage:

Purpose: Cache different versions based on request headers

Vary: Accept-Encoding
└── Cache separate gzip vs brotli vs plain versions

Vary: Accept-Language
└── Cache separate versions per language
└── WARNING: Can explode cache variations

Vary: Cookie
└── Usually means "don't cache at CDN"
└── Every unique cookie = different cache entry

Best Practices:
✓ Vary: Accept-Encoding (always for compressible content)
✓ Vary: Origin (for CORS)
✗ Avoid Vary: Cookie (fragments cache badly)
✗ Avoid Vary: User-Agent (thousands of variants)

Alternative to Vary:
- Normalize headers at edge
- Use query parameters instead
- Separate URLs for different variants
```

## Origin Shielding

### Shield Architecture

```text
Without Origin Shield:

Edge POPs: 200+ locations
    │ │ │ │ │ │ │ │ │ │
    └─┴─┴─┴─┴─┴─┴─┴─┴─┘
              │
    All 200 POPs can request from origin
              ▼
         ┌────────┐
         │ Origin │  (200 potential requesters on cache miss)
         └────────┘

With Origin Shield:

Edge POPs: 200+ locations
    │ │ │ │ │ │ │ │ │ │
    └─┴─┴─┴─┴─┴─┴─┴─┴─┘
              │
    All edge misses go to shield
              ▼
    ┌─────────────────┐
    │  Origin Shield  │  (1 shield per region)
    │   (Collapsed)   │
    └────────┬────────┘
             │
    Only shield requests from origin
             ▼
         ┌────────┐
         │ Origin │  (1-3 potential requesters)
         └────────┘

Benefits:
- Collapses cache misses
- Reduces origin load
- Better cache efficiency
- Improved origin availability
```

### Request Collapsing

```text
Request Collapsing (Coalescing):

Scenario: 100 users request same uncached asset simultaneously

Without Collapsing:
100 requests ──► Edge ──► 100 requests ──► Origin
                         (thundering herd)

With Collapsing:
100 requests ──► Edge ──► 1 request ──► Origin
                  │
            99 requests wait
                  │
            Response cached, all 100 served

Implementation:
- First request triggers origin fetch
- Subsequent requests for same URL wait
- All requests served from single origin response
- Critical for protecting origin on cache miss spikes
```

## Cache Invalidation

### Invalidation Strategies

```text
Strategy 1: TTL-Based Expiration
└── Let content expire naturally
└── Simple, predictable
└── Delay in propagating changes

Strategy 2: Purge (Immediate Invalidation)
└── Remove specific URLs from cache
└── Fast update propagation
└── Can be expensive at scale

Strategy 3: Soft Purge (Stale-While-Revalidate)
└── Mark content as stale
└── Serve stale while fetching fresh
└── Best user experience

Strategy 4: Versioned URLs
└── Change URL when content changes
└── No purging needed
└── Best cache efficiency
└── asset.js?v=abc123 or asset.abc123.js

Strategy 5: Cache Tags (Surrogate Keys)
└── Tag content with identifiers
└── Purge by tag instead of URL
└── Powerful for related content
└── Purge all "product-123" tagged content
```

### Versioning Patterns

```text
URL Versioning:

Pattern 1: Query Parameter
/styles.css?v=1.2.3
/styles.css?v=a1b2c3d4 (hash)
+ Simple to implement
- Some CDNs don't cache query strings by default

Pattern 2: Filename Hash
/styles.a1b2c3d4.css
+ Best cache efficiency
+ CDNs cache by default
- Requires build process

Pattern 3: Path Versioning
/v1.2.3/styles.css
+ Clear version organization
- May have many versions to purge

Recommendation:
- Static assets: Filename hash (best cache efficiency)
- APIs: Path versioning (/v1/api/...)
- HTML: Short TTL + revalidation
```

### Cache Tags / Surrogate Keys

```text
Cache Tags Example:

Response from origin:
HTTP/1.1 200 OK
Surrogate-Key: product-123 category-electronics homepage
Cache-Control: public, max-age=86400

Content tagged with:
- product-123 (specific product)
- category-electronics (product category)
- homepage (appears on homepage)

Purge Scenarios:
- Product updated: Purge "product-123"
- Category reorganized: Purge "category-electronics"
- Homepage changed: Purge "homepage"

Single purge affects all URLs with that tag.
```

## Edge Computing

### Edge Functions

```text
Edge Function Use Cases:

1. Request Manipulation
   - URL rewriting
   - Header modification
   - Authentication
   - Geolocation-based routing

2. Response Manipulation
   - HTML injection (A/B testing)
   - Content transformation
   - Personalization at edge
   - Response compression

3. Security
   - Bot detection
   - Rate limiting
   - WAF rules
   - Token validation

4. Caching Logic
   - Custom cache keys
   - Vary normalization
   - Cache bypass rules
   - Selective purging

Platforms:
- Cloudflare Workers
- AWS Lambda@Edge / CloudFront Functions
- Fastly Compute@Edge
- Akamai EdgeWorkers
```

### A/B Testing at Edge

```text
Edge A/B Testing:

Traditional (Origin-Based):
User ──► CDN ──► Origin ──► Determine variant ──► Response
         │                  (uncacheable due to personalization)
      Cache miss every time

Edge-Based:
User ──► Edge Worker ──► Assign variant (cookie/header)
              │
              ├── Variant A: Serve /page-a (cacheable)
              └── Variant B: Serve /page-b (cacheable)

Benefits:
- Each variant is separately cacheable
- No origin computation per request
- Consistent variant assignment
- Analytics at edge
```

## CDN Selection

### Provider Comparison

```text
CDN Provider Considerations:

Performance:
├── Global POP coverage
├── Network quality (peering)
├── Cache hit ratio
└── TTFB benchmarks

Features:
├── Edge computing support
├── Real-time analytics
├── Custom caching rules
├── Image optimization
├── Video streaming
└── Security features (WAF, DDoS)

Pricing Models:
├── Bandwidth-based
├── Request-based
├── Flat-rate
└── Commit discounts

Integration:
├── API quality
├── Terraform/IaC support
├── CI/CD integration
└── Monitoring integration

Major Providers:
- Cloudflare: Great developer experience, generous free tier
- Fastly: Excellent for dynamic/personalized content
- AWS CloudFront: Best with AWS ecosystem
- Akamai: Enterprise, most POPs globally
- Azure CDN: Best with Azure ecosystem
```

## Best Practices

```text
CDN Best Practices:

1. Cache Efficiency
   □ Use content hashing for static assets
   □ Set appropriate TTLs for content type
   □ Implement origin shielding
   □ Monitor cache hit ratios

2. Performance
   □ Enable compression (Brotli/Gzip)
   □ Use HTTP/2 or HTTP/3
   □ Implement preconnect hints
   □ Optimize for Core Web Vitals

3. Cache Invalidation
   □ Prefer versioned URLs over purging
   □ Use cache tags for related content
   □ Implement soft purge when possible
   □ Have purge automation ready

4. Security
   □ Enable HTTPS everywhere
   □ Configure proper CORS
   □ Implement security headers
   □ Use signed URLs for sensitive content

5. Monitoring
   □ Track cache hit ratio
   □ Monitor origin load
   □ Set up latency alerts
   □ Analyze error rates
```

## Troubleshooting

```text
Common Issues:

1. Low Cache Hit Ratio
   - Check Vary header proliferation
   - Verify cache-control headers
   - Look for query string variations
   - Check for cookie-based variation

2. Stale Content
   - Verify cache-control max-age
   - Check purge propagation delay
   - Confirm versioning strategy
   - Review origin response headers

3. High Origin Load
   - Implement origin shield
   - Enable request collapsing
   - Extend TTLs where appropriate
   - Add caching for API responses

4. Slow Performance
   - Check POP distribution
   - Verify compression enabled
   - Review TLS configuration
   - Analyze origin response time

Debug Headers:
X-Cache: HIT/MISS
X-Cache-Hits: 123
Age: 3600
CF-Cache-Status: DYNAMIC/HIT/MISS
```

## Related Skills

- `edge-computing` - Compute at CDN edge
- `latency-optimization` - End-to-end latency reduction
- `multi-region-deployment` - Global infrastructure patterns
- `caching-strategies` - Application-level caching
