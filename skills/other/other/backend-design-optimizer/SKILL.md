---
name: backend-design-optimizer
description: Find the best backend architecture, database design, and API patterns using deep research. Use when user asks "best database for...", "optimize API", "backend architecture for...", or "scale this service".
version: 1.0.0
agents: [codex-deep-research, gemini-research-analyst]
---

# Backend Design Optimizer

**Deep research-driven skill for finding optimal backend architectures and patterns.**

## When to Use

Invoke this skill when the user mentions:
- "What's the best database for..."
- "How should I architect the backend for..."
- "Best API design for..."
- "Optimize this service..."
- "Scalability patterns for..."
- "Microservices vs monolith for..."
- "Best caching strategy..."
- "Database schema design for..."

## Research-First Methodology

This skill uses multi-agent deep research to find proven, production-tested backend patterns.

### Step 1: Understand Context

```bash
# Analyze current architecture
- What's the tech stack? (Node.js, Python, Go, Java)
- What's the database? (PostgreSQL, MongoDB, Redis)
- What's the scale? (users/day, requests/sec, data volume)
- What are the constraints? (budget, team size, deadlines)
- What are the requirements? (real-time, analytics, compliance)
```

### Step 2: Launch Deep Research

**Use the codex-deep-research agent** to investigate:

```markdown
Invoke Task tool with subagent_type="codex-deep-research"

Prompt:
"Research the best backend architecture and design patterns for [specific use case].

Context:
- Current stack: [from Step 1]
- Scale requirements: [users, requests, data]
- Key requirements: [real-time, security, compliance, etc.]
- Constraints: [budget, timeline, team expertise]

Please provide:
1. Top 3-5 architectural patterns with trade-offs
2. Database design recommendations (schema, indexing, partitioning)
3. API design patterns (REST, GraphQL, gRPC)
4. Caching strategies (Redis, CDN, application-level)
5. Scalability approaches (horizontal, vertical, sharding)
6. Security best practices (auth, encryption, rate limiting)
7. Performance optimization techniques
8. Cost analysis (infrastructure, maintenance)
9. Real-world case studies (companies using these patterns at scale)
10. Migration path (if changing from current architecture)

Include code examples, database schemas, and architecture diagrams (in markdown)."
```

### Step 3: Check AI-Powered Solutions

**Use the gemini-research-analyst agent** for AI-enhanced backend tools:

```markdown
Invoke Task tool with subagent_type="gemini-research-analyst"

Prompt:
"Research if Google's Gemini AI provides any backend development tools, code generation, or architectural recommendations for [specific use case].

Specifically investigate:
1. Gemini-powered code generation for backend services
2. AI-assisted database schema design
3. Automated API generation or optimization
4. Performance profiling and optimization suggestions
5. Security vulnerability detection
6. Load testing and capacity planning tools
7. Integration with Google Cloud services (Cloud SQL, Firestore, etc.)

If Gemini has relevant capabilities, explain:
- How to integrate with our stack
- Performance benefits
- Cost implications
- Examples of production usage"
```

### Step 4: Synthesize Recommendations

After agents return results:

1. **Compare architectural patterns** from research
2. **Rank by criteria**:
   - Scalability (most important for growth)
   - Performance (response times, throughput)
   - Cost-efficiency (infrastructure + maintenance)
   - Developer productivity (time to market)
   - Reliability (uptime, fault tolerance)
   - Security (compliance, data protection)

3. **Provide decision matrix**:
```markdown
## Architecture Pattern Comparison

| Pattern | Scalability | Performance | Cost | Complexity | Best For |
|---------|-------------|-------------|------|------------|----------|
| Monolith + Cache | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰 | Low | Small teams, MVP |
| Microservices | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰💰 | High | Large scale, multiple teams |
| Serverless | ⭐⭐⭐⭐ | ⭐⭐⭐ | 💰💰 | Medium | Variable load, pay-per-use |
| Hybrid | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 | Medium | Migration, best of both |
```

4. **Database design recommendations**:
```markdown
## Database Design

### Recommended: [Database Type]

**Schema Design:**
```sql
-- Optimized schema based on access patterns
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  status VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  -- Indexes based on query patterns
  INDEX idx_status (status),
  INDEX idx_created (created_at DESC)
);

-- Partitioning strategy for large tables
CREATE TABLE audit_logs (
  id BIGSERIAL,
  event_type VARCHAR(100),
  created_at TIMESTAMP NOT NULL,
  data JSONB
) PARTITION BY RANGE (created_at);
```

**Indexing Strategy:**
- Primary queries: [list queries]
- Indexes needed: [list with justification]
- Composite indexes: [where beneficial]

**Partitioning/Sharding:**
- Shard key: [field choice with explanation]
- Partition strategy: [time-based, hash-based, etc.]
```

### Step 5: Provide Implementation Plan

```markdown
## Recommended: [Architecture Pattern]

### Why This Architecture?
- [Justification based on research]
- [Real-world examples at similar scale]
- [Performance benchmarks]
- [Cost projections]

### Implementation Phases

#### Phase 1: Foundation (Week 1-2)
1. Set up database with optimized schema
2. Implement core API layer
3. Add caching strategy
4. Set up monitoring and logging

```typescript
// Example: API layer with caching
import { Pool } from 'pg';
import Redis from 'redis';

const dbPool = new Pool({
  max: 20, // Connection pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

const redisClient = Redis.createClient({
  socket: {
    host: process.env.REDIS_HOST,
    port: 6379,
  },
});

// Cached API endpoint
export async function getProject(id: string) {
  const cacheKey = `project:${id}`;

  // Check cache first
  const cached = await redisClient.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Query database
  const result = await dbPool.query(
    'SELECT * FROM projects WHERE id = $1',
    [id]
  );

  // Cache for 5 minutes
  await redisClient.setEx(cacheKey, 300, JSON.stringify(result.rows[0]));

  return result.rows[0];
}
```

#### Phase 2: Optimization (Week 3-4)
1. Add rate limiting
2. Implement connection pooling
3. Set up CDN for static assets
4. Database query optimization

#### Phase 3: Scalability (Week 5-6)
1. Horizontal scaling setup
2. Load balancer configuration
3. Database read replicas
4. Caching layer expansion

### Performance Targets
- API response time: <100ms (p95)
- Database query time: <50ms (p95)
- Cache hit rate: >80%
- Uptime: 99.9%
- Concurrent users: [target based on requirements]

### Security Checklist
- [ ] Authentication (JWT, OAuth, API keys)
- [ ] Authorization (RBAC, permissions)
- [ ] Rate limiting (per-user, per-IP)
- [ ] Input validation (SQL injection, XSS prevention)
- [ ] Encryption at rest (database, backups)
- [ ] Encryption in transit (TLS 1.3)
- [ ] Secrets management (env vars, vault)
- [ ] Audit logging (all mutations)

### Monitoring Setup
```yaml
# Example: Prometheus metrics
metrics:
  - api_request_duration_seconds
  - api_requests_total
  - database_connection_pool_size
  - cache_hit_rate
  - error_rate_5xx

alerts:
  - high_error_rate: >1% for 5 minutes
  - slow_response: p95 >200ms for 10 minutes
  - database_connection_exhaustion: >80% pool usage
```

### Cost Estimation
```markdown
## Monthly Cost Breakdown

**Infrastructure:**
- Database (PostgreSQL): $[amount] ([tier/size])
- Cache (Redis): $[amount]
- Application servers: $[amount] ([count] x [size])
- Load balancer: $[amount]
- CDN: $[amount] (based on [GB] traffic)
- Monitoring: $[amount]

**Total: $[amount]/month**

**Scaling Cost:**
- At 2x traffic: $[amount]
- At 5x traffic: $[amount]
- At 10x traffic: $[amount]
```

### Migration Path (if applicable)
```markdown
## Migration from [Current] to [Recommended]

### Strategy: [Blue-Green / Canary / Phased]

**Phase 1: Preparation**
1. Set up new infrastructure in parallel
2. Data migration scripts
3. Dual-write to both systems

**Phase 2: Validation**
1. Shadow traffic to new system
2. Compare responses
3. Performance testing

**Phase 3: Cutover**
1. Route 10% traffic → monitor
2. Route 50% traffic → monitor
3. Route 100% traffic
4. Decommission old system

**Rollback Plan:**
- DNS cutover (instant)
- Database snapshots (before migration)
- Feature flags (gradual rollback)
```

## Validation Criteria

Before presenting recommendations, ensure:

- ✅ At least 3 architectural patterns evaluated
- ✅ Database schema optimized for access patterns
- ✅ Performance benchmarks from similar systems
- ✅ Cost projections included
- ✅ Security best practices addressed
- ✅ Scalability path defined
- ✅ Monitoring strategy included
- ✅ Migration path (if changing architecture)
- ✅ Real-world case studies cited

## Anti-Patterns to Avoid

**NEVER recommend without research:**
- Over-engineering for current scale
- Technologies without proven track record
- Architectures that don't match team expertise
- Solutions that ignore budget constraints

**ALWAYS consider:**
- Start simple, scale when needed
- Team's learning curve
- Operational complexity
- Total cost of ownership (not just infrastructure)
- Time to market vs perfect architecture

## Example Invocation

```markdown
User: "What's the best database and API design for a real-time collaboration platform with 10k concurrent users?"