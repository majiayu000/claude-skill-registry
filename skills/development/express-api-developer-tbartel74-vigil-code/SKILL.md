---
name: express-api-developer
description: Express.js backend API development for Vigil Guard v2.0.0. Use for endpoint creation, JWT authentication, RBAC, ClickHouse queries with 3-branch columns, rate limiting, CORS management, branch service proxy endpoints, and audit logging.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Express API Developer (v2.0.0)

## Overview

Backend API development for Vigil Guard's Express.js server including JWT authentication, RBAC, ClickHouse integration with 3-branch detection columns, branch service proxy endpoints, and configuration management.

## When to Use This Skill

- Developing new API endpoints
- Implementing authentication flows
- Managing database queries (SQLite + ClickHouse)
- Proxying requests to 3-branch detection services
- Rate limiting configuration
- CORS policy management
- Audit logging implementation

## Tech Stack

- Express 4.18.2
- TypeScript 5.6.3
- JWT (jsonwebtoken ^9.0.2)
- bcrypt ^5.1.1 (12 rounds)
- SQLite (better-sqlite3)
- ClickHouse client
- express-rate-limit ^8.1.0

## Project Structure

```
services/web-ui/backend/src/
├── server.ts              # Main Express app
├── auth.ts                # JWT + bcrypt
├── retention.ts           # ClickHouse retention API
├── clickhouse.ts          # CH connection
├── piiAnalyzer.ts         # Dual-language PII detection
├── fileOps.ts             # Config file operations
└── db/
    └── users.db           # SQLite for users/sessions
```

## v2.0.0 Architecture Integration

### 3-Branch Service Endpoints

The backend can proxy requests to the 3-branch detection services:

```typescript
// Branch Service URLs (v2.0.0)
const BRANCH_SERVICES = {
  A: 'http://heuristics-service:5005',   // Heuristics (30% weight)
  B: 'http://semantic-service:5006',      // Semantic (35% weight)
  C: 'http://prompt-guard-api:8000'       // LLM Guard (35% weight)
};
```

### Service Health Check Endpoint

```typescript
// GET /api/health/branches
app.get('/api/health/branches',
  authMiddleware,
  async (req, res) => {
    try {
      const healthChecks = await Promise.allSettled([
        fetch(`${BRANCH_SERVICES.A}/health`, { signal: AbortSignal.timeout(2000) }),
        fetch(`${BRANCH_SERVICES.B}/health`, { signal: AbortSignal.timeout(2000) }),
        fetch(`${BRANCH_SERVICES.C}/health`, { signal: AbortSignal.timeout(2000) })
      ]);

      const results = {
        branch_a: {
          name: 'Heuristics',
          port: 5005,
          healthy: healthChecks[0].status === 'fulfilled' && healthChecks[0].value.ok
        },
        branch_b: {
          name: 'Semantic',
          port: 5006,
          healthy: healthChecks[1].status === 'fulfilled' && healthChecks[1].value.ok
        },
        branch_c: {
          name: 'LLM Guard',
          port: 8000,
          healthy: healthChecks[2].status === 'fulfilled' && healthChecks[2].value.ok
        }
      };

      const allHealthy = Object.values(results).every(b => b.healthy);
      res.status(allHealthy ? 200 : 503).json(results);
    } catch (error) {
      res.status(500).json({ error: 'Health check failed' });
    }
  }
);
```

## Common Tasks

### Task 1: Add New Endpoint

```typescript
// server.ts
import { authMiddleware, requirePermission } from './auth';

app.post('/api/my-endpoint',
  authMiddleware,                           // JWT validation
  requirePermission('can_view_configuration'), // RBAC check
  async (req, res) => {
    try {
      const { param } = req.body;

      // Input validation
      if (!param || typeof param !== 'string') {
        return res.status(400).json({ error: 'Invalid parameter' });
      }

      // Business logic
      const result = await doSomething(param);

      // Audit log
      auditLog('my-endpoint', req.user.username, { param, result });

      res.json({ success: true, data: result });
    } catch (error) {
      console.error('my-endpoint error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
);
```

### Task 2: ClickHouse Query (v2.0.0 Schema)

```typescript
import { getClickHouseClient } from './clickhouse';

// Query with 3-branch columns (v2.0.0)
async function queryEvents(sessionId: string) {
  const client = getClickHouseClient();

  const query = `
    SELECT
      timestamp,
      original_input,
      final_status,
      threat_score,
      -- v2.0.0: 3-Branch Detection Scores
      branch_a_score,
      branch_b_score,
      branch_c_score,
      arbiter_decision,
      -- v2.0.0: Branch Timing
      branch_a_timing_ms,
      branch_b_timing_ms,
      branch_c_timing_ms,
      total_timing_ms,
      -- v2.0.0: Branch Degradation
      branch_a_degraded,
      branch_b_degraded,
      branch_c_degraded
    FROM n8n_logs.events_processed
    WHERE sessionId = {sessionId:String}
    ORDER BY timestamp DESC
    LIMIT 100
  `;

  const result = await client.query({
    query,
    query_params: { sessionId }
  });

  return await result.json();
}

// Branch performance query (v2.0.0)
async function getBranchMetrics(hours: number = 24) {
  const client = getClickHouseClient();

  const query = `
    SELECT
      arbiter_decision,
      count() as total,
      round(avg(branch_a_score), 2) as avg_heuristics,
      round(avg(branch_b_score), 2) as avg_semantic,
      round(avg(branch_c_score), 2) as avg_llm_guard,
      round(avg(branch_a_timing_ms), 0) as avg_heuristics_ms,
      round(avg(branch_b_timing_ms), 0) as avg_semantic_ms,
      round(avg(branch_c_timing_ms), 0) as avg_llm_guard_ms,
      sum(branch_a_degraded) as heuristics_errors,
      sum(branch_b_degraded) as semantic_errors,
      sum(branch_c_degraded) as llm_guard_errors
    FROM n8n_logs.events_processed
    WHERE timestamp > now() - INTERVAL {hours:UInt32} HOUR
    GROUP BY arbiter_decision
    ORDER BY total DESC
  `;

  const result = await client.query({
    query,
    query_params: { hours }
  });

  return await result.json();
}
```

### Task 3: Branch Service Proxy

```typescript
// Proxy endpoint for heuristics analysis (v2.0.0)
app.post('/api/analyze/heuristics',
  authMiddleware,
  requirePermission('can_view_configuration'),
  async (req, res) => {
    try {
      const { text, request_id } = req.body;

      if (!text || typeof text !== 'string') {
        return res.status(400).json({ error: 'Text is required' });
      }

      const response = await fetch(`${BRANCH_SERVICES.A}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, request_id: request_id || 'api-test' }),
        signal: AbortSignal.timeout(5000)
      });

      if (!response.ok) {
        throw new Error(`Heuristics service error: ${response.status}`);
      }

      const result = await response.json();
      res.json(result);
    } catch (error) {
      console.error('Heuristics proxy error:', error);
      res.status(503).json({ error: 'Heuristics service unavailable' });
    }
  }
);

// Proxy endpoint for semantic analysis (v2.0.0)
app.post('/api/analyze/semantic',
  authMiddleware,
  requirePermission('can_view_configuration'),
  async (req, res) => {
    try {
      const { text, request_id } = req.body;

      if (!text || typeof text !== 'string') {
        return res.status(400).json({ error: 'Text is required' });
      }

      const response = await fetch(`${BRANCH_SERVICES.B}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, request_id: request_id || 'api-test' }),
        signal: AbortSignal.timeout(5000)
      });

      if (!response.ok) {
        throw new Error(`Semantic service error: ${response.status}`);
      }

      const result = await response.json();
      res.json(result);
    } catch (error) {
      console.error('Semantic proxy error:', error);
      res.status(503).json({ error: 'Semantic service unavailable' });
    }
  }
);
```

### Task 4: Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// Authentication endpoints (brute force protection)
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,                     // 5 attempts
  message: 'Too many login attempts',
  standardHeaders: true
});

app.post('/api/auth/login', authLimiter, loginHandler);

// General API (DoS protection)
const apiLimiter = rateLimit({
  windowMs: 60 * 1000,  // 1 minute
  max: 100              // 100 requests
});

app.use('/api/', apiLimiter);

// Branch proxy (separate limit)
const branchLimiter = rateLimit({
  windowMs: 60 * 1000,  // 1 minute
  max: 30               // 30 analysis requests
});

app.use('/api/analyze/', branchLimiter);
```

### Task 5: CORS Configuration

```typescript
import cors from 'cors';

app.use(cors({
  origin: process.env.NODE_ENV === 'production' ?
    process.env.ALLOWED_ORIGINS.split(',') :
    /^http:\/\/localhost(:\d+)?$/,  // Any localhost port in dev
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

## Security Best Practices

### Password Hashing

```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

async function hashPassword(password: string): Promise<string> {
  return await bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return await bcrypt.compare(password, hash);
}
```

### JWT Token Management

```typescript
import jwt from 'jsonwebtoken';

const SECRET = process.env.JWT_SECRET;  // 32+ chars from .env
const EXPIRY = '24h';

function generateToken(user: User): string {
  return jwt.sign(
    {
      id: user.id,
      username: user.username,
      permissions: user.permissions
    },
    SECRET,
    { expiresIn: EXPIRY }
  );
}

function verifyToken(token: string): any {
  return jwt.verify(token, SECRET);
}
```

### SQL Injection Prevention

```typescript
// ❌ WRONG: String concatenation
const query = `SELECT * FROM users WHERE username = '${username}'`;

// ✅ CORRECT: Parameterized query
const query = db.prepare('SELECT * FROM users WHERE username = ?');
const user = query.get(username);
```

## API Endpoints Reference (v2.0.0)

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/change-password` | Change password |

### Configuration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/files` | List config files |
| GET | `/api/files/:filename` | Get file content |
| PUT | `/api/files/:filename` | Update file (ETag) |

### Branch Services (v2.0.0)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/branches` | Check all branch health |
| POST | `/api/analyze/heuristics` | Test heuristics (Branch A) |
| POST | `/api/analyze/semantic` | Test semantic (Branch B) |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/events` | Query events |
| GET | `/api/metrics/branches` | Branch performance (v2.0.0) |
| GET | `/api/retention` | Get retention config |
| PUT | `/api/retention` | Update retention config |

### PII Detection

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/pii-detection/status` | Service health |
| GET | `/api/pii-detection/entity-types` | Available entities |
| POST | `/api/pii-detection/analyze` | Dual-language detection |

## Integration with Other Skills

### With `clickhouse-grafana-monitoring`:

```yaml
when: New ClickHouse column needed
action:
  1. Add migration SQL (branch columns already in v2.0.0)
  2. Update TypeScript interfaces
  3. Modify query functions
  4. Test with curl
```

### With `react-tailwind-vigil-ui`:

```yaml
when: Frontend needs new API
action:
  1. Design endpoint (REST conventions)
  2. Implement with proper auth/validation
  3. Update api.ts in frontend
  4. Test CORS and token handling
```

### With `docker-vigil-orchestration`:

```yaml
when: Backend needs branch service access
action:
  1. Verify services on vigil-net network
  2. Use internal hostnames (heuristics-service, semantic-service)
  3. Handle timeout/degradation gracefully
```

## Quick Reference

```bash
# Start dev server
cd services/web-ui/backend && npm run dev

# Test endpoint
curl -X POST http://localhost:8787/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Test branch health (v2.0.0)
curl http://localhost:8787/api/health/branches \
  -H "Authorization: Bearer $TOKEN"

# Test heuristics proxy (v2.0.0)
curl -X POST http://localhost:8787/api/analyze/heuristics \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"test input","request_id":"test-123"}'

# Check TypeScript
npx tsc --noEmit

# View logs
docker logs vigil-web-ui-backend -f
```

## Related Skills

- `react-tailwind-vigil-ui` - Frontend integration
- `clickhouse-grafana-monitoring` - Analytics queries
- `docker-vigil-orchestration` - Service networking
- `vigil-security-patterns` - Security best practices

## References

- Backend source: `services/web-ui/backend/src/`
- Express docs: https://expressjs.com/
- ClickHouse docs: https://clickhouse.com/docs

---

**Last Updated:** 2025-12-09
**Backend Version:** v2.0.0
**API Endpoints:** 25+ routes (including branch services)

## Version History

- **v2.0.0** (Current): 3-branch proxy endpoints, branch health checks, ClickHouse branch columns
- **v1.6.11**: Initial Express setup, JWT auth, basic endpoints
