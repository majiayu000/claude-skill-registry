---
name: vigil-security-patterns
description: Security best practices and patterns for Vigil Guard v2.0.0 development. Use when implementing authentication, handling secrets, validating input, preventing injection attacks, managing CORS, ensuring secure coding practices, 3-branch detection security, or implementing security audit fixes.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Vigil Guard Security Patterns (v2.0.0)

## Overview

Comprehensive security best practices for developing and maintaining Vigil Guard's security-critical codebase with 3-branch parallel detection architecture.

## When to Use This Skill

- Implementing authentication flows
- Managing secrets and credentials
- Validating user input
- Preventing injection attacks
- Configuring CORS policies
- Handling password hashing
- Implementing RBAC permissions
- Secure session management
- Code review for security issues
- 3-branch service security (v2.0.0)

## v2.0.0 Architecture Security

### 3-Branch Detection Security

```yaml
11 Docker Services Security:
  Core Services:
    - clickhouse (data storage, port 8123)
    - grafana (monitoring, port 3001)
    - n8n (workflow engine, port 5678)

  3-Branch Detection (v2.0.0):
    - heuristics-service (Branch A, port 5005, 30% weight)
    - semantic-service (Branch B, port 5006, 35% weight)
    - prompt-guard-api (Branch C, port 8000, 35% weight)

  PII Detection:
    - presidio-pii-api (port 5001)
    - language-detector (port 5002)

  Web Interface:
    - web-ui-backend (port 8787)
    - web-ui-frontend (via proxy)
    - proxy (Caddy, port 80)
```

### Branch Service Security Considerations

```yaml
Branch A (Heuristics - port 5005):
  Risks:
    - Pattern injection via crafted input
    - DoS via complex regex (ReDoS)
    - Config file manipulation
  Mitigations:
    - Pattern timeout limits (1000ms)
    - unified_config.json validation
    - Read-only config mount in Docker

Branch B (Semantic - port 5006):
  Risks:
    - Model poisoning (if model updates allowed)
    - Embedding manipulation attacks
    - Resource exhaustion (GPU/CPU)
  Mitigations:
    - Fixed model (all-MiniLM-L6-v2)
    - Input length limits
    - Request timeout (2000ms)

Branch C (LLM Guard - port 8000):
  Risks:
    - Prompt injection to bypass detection
    - Model manipulation
    - Resource exhaustion
  Mitigations:
    - Separate container isolation
    - Request timeout (3000ms)
    - No external network access
```

### Arbiter v2 Security

```javascript
// Weighted fusion security (v2.0.0)
const WEIGHTS = {
  branch_a: 0.30,  // Heuristics
  branch_b: 0.35,  // Semantic
  branch_c: 0.35   // LLM Guard
};

// Arbiter decision thresholds (cannot be manipulated via input)
const THRESHOLDS = {
  block: 70,        // Score >= 70 → BLOCK
  sanitize: 30,     // Score 30-69 → SANITIZE
  allow: 0          // Score < 30 → ALLOW
};

// Branch degradation handling (fail-safe)
function arbiterDecision(scores) {
  const validBranches = Object.entries(scores)
    .filter(([_, score]) => score !== null);

  if (validBranches.length === 0) {
    // All branches failed → fail-safe to BLOCK
    return { decision: 'BLOCK', reason: 'all_branches_degraded' };
  }

  // Recalculate weights for available branches
  const totalWeight = validBranches
    .reduce((sum, [branch]) => sum + WEIGHTS[branch], 0);

  const normalizedScore = validBranches
    .reduce((sum, [branch, score]) =>
      sum + (score * WEIGHTS[branch] / totalWeight), 0);

  return applyThresholds(normalizedScore);
}
```

## Authentication Security

### JWT Token Management

```typescript
import jwt from 'jsonwebtoken';

const SECRET = process.env.JWT_SECRET;  // 32+ chars from .env
const EXPIRY = '24h';

// Token generation with claims
function generateToken(user: User): string {
  return jwt.sign(
    {
      id: user.id,
      username: user.username,
      permissions: user.permissions,
      iat: Math.floor(Date.now() / 1000)
    },
    SECRET,
    { expiresIn: EXPIRY }
  );
}

// Token verification with error handling
function verifyToken(token: string): JwtPayload | null {
  try {
    return jwt.verify(token, SECRET) as JwtPayload;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      console.warn('Token expired');
    } else if (error instanceof jwt.JsonWebTokenError) {
      console.warn('Invalid token');
    }
    return null;
  }
}
```

### Password Security

```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

async function hashPassword(password: string): Promise<string> {
  return await bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return await bcrypt.compare(password, hash);
}

// Password policy
function validatePasswordStrength(password: string): boolean {
  return password.length >= 8;  // Minimum 8 characters
}
```

### Permission Checks

```typescript
// Server-side RBAC middleware
function requirePermission(permission: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;

    if (!user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    if (!user.permissions.includes(permission)) {
      return res.status(403).json({ error: 'Permission denied' });
    }

    next();
  };
}

// Usage
app.post('/api/config/:filename',
  authMiddleware,
  requirePermission('can_view_configuration'),
  configHandler
);
```

## Input Validation

### Path Traversal Prevention

```typescript
// Whitelist allowed filenames
const ALLOWED_FILES = [
  'unified_config.json',
  'pii.conf',
  'sections.json',
  'variables.json'
];

function validateFilename(filename: string): boolean {
  // Reject path traversal attempts
  if (filename.includes('..') || filename.includes('/') || filename.includes('\\')) {
    return false;
  }

  // Whitelist check
  return ALLOWED_FILES.includes(filename);
}
```

### SQL Injection Prevention

```typescript
// ClickHouse parameterized queries
async function queryEvents(sessionId: string) {
  const client = getClickHouseClient();

  // ✅ CORRECT: Parameterized query
  const query = `
    SELECT
      timestamp,
      original_input,
      final_status,
      branch_a_score,
      branch_b_score,
      branch_c_score,
      arbiter_decision
    FROM n8n_logs.events_processed
    WHERE sessionId = {sessionId:String}
    ORDER BY timestamp DESC
    LIMIT 100
  `;

  return await client.query({
    query,
    query_params: { sessionId }
  });
}

// SQLite parameterized queries
const stmt = db.prepare('SELECT * FROM users WHERE username = ?');
const user = stmt.get(username);
```

### XSS Prevention

```typescript
// React auto-escapes JSX by default
// For HTML content, use DOMPurify
import DOMPurify from 'dompurify';

function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'target']
  });
}
```

## Secret Management

### Environment Variables

```bash
# .env (auto-generated by install.sh)
CLICKHOUSE_PASSWORD=$(openssl rand -base64 32)
GF_SECURITY_ADMIN_PASSWORD=$(openssl rand -base64 32)
SESSION_SECRET=$(openssl rand -base64 64)
JWT_SECRET=$(openssl rand -base64 32)
WEB_UI_ADMIN_PASSWORD=$(openssl rand -base64 24)
```

### Secret Masking in UI

```typescript
function maskSecret(value: string): string {
  if (value.length <= 2) return '***';
  return value[0] + '*'.repeat(value.length - 2) + value[value.length - 1];
}

// Example: "mysecret123" → "m*********3"
```

## Rate Limiting (v2.0.0)

### Authentication Endpoints

```typescript
import rateLimit from 'express-rate-limit';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,                     // 5 attempts per window
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false
});

app.post('/api/auth/login', authLimiter, loginHandler);
app.post('/api/auth/change-password', authLimiter, changePasswordHandler);
```

### General API Protection

```typescript
const apiLimiter = rateLimit({
  windowMs: 1 * 60 * 1000,  // 1 minute
  max: 100,                 // 100 requests per minute
  message: 'Too many requests, please slow down'
});

app.use('/api/', apiLimiter);
```

### Branch Service Proxy Protection

```typescript
const branchLimiter = rateLimit({
  windowMs: 60 * 1000,  // 1 minute
  max: 30               // 30 analysis requests per minute
});

app.use('/api/analyze/', branchLimiter);
```

## ReDoS Protection (v2.0.0)

### Pattern Timeout Limits

```javascript
// Heuristics service pattern matching
const PATTERN_TIMEOUT_MS = 1000; // 1 second max per pattern

async function matchPattern(text, pattern) {
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Pattern timeout')), PATTERN_TIMEOUT_MS)
  );

  const matchPromise = new Promise(resolve =>
    resolve(new RegExp(pattern).test(text))
  );

  return Promise.race([matchPromise, timeoutPromise]);
}
```

### Safe Regex Patterns

```javascript
// ❌ UNSAFE: Catastrophic backtracking
const unsafe = /^(a+)+$/;

// ✅ SAFE: Non-backtracking alternative
const safe = /^a+$/;

// ❌ UNSAFE: Nested quantifiers
const unsafe2 = /(x+x+)+y/;

// ✅ SAFE: Atomic grouping or simplified pattern
const safe2 = /x+y/;
```

### ReDoS Testing

```bash
# Use redos-detector tool
npm install -g redos-detector

# Test pattern
redos-detector '^(a+)+$'

# Scan unified_config.json patterns
cat services/workflow/config/unified_config.json | \
  jq -r '.categories[].patterns[]' | \
  xargs -I {} redos-detector '{}'
```

## CORS Configuration

### Development

```typescript
app.use(cors({
  origin: /^http:\/\/localhost(:\d+)?$/,  // Any localhost port
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### Production

```typescript
const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || [];
app.use(cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));
```

## Audit Logging

```typescript
function auditLog(action: string, username: string, details: object) {
  const entry = {
    timestamp: new Date().toISOString(),
    action,
    username,
    details: JSON.stringify(details),
    ip: req.ip
  };

  fs.appendFileSync('config/audit.log', JSON.stringify(entry) + '\n');
}

// Usage
auditLog('config_update', req.user.username, {
  file: 'unified_config.json',
  changes: diff(oldConfig, newConfig)
});
```

## Health Check Security (v2.0.0)

### Branch Service Health Checks

```typescript
// GET /api/health/branches
app.get('/api/health/branches',
  authMiddleware,
  async (req, res) => {
    try {
      const healthChecks = await Promise.allSettled([
        fetch('http://heuristics-service:5005/health', { signal: AbortSignal.timeout(2000) }),
        fetch('http://semantic-service:5006/health', { signal: AbortSignal.timeout(2000) }),
        fetch('http://prompt-guard-api:8000/health', { signal: AbortSignal.timeout(2000) })
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

### Docker Health Checks

```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "wget", "--spider", "-q", "http://localhost:8787/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

## Security Testing

### OWASP Top 10 Coverage

```yaml
Coverage (v2.0.0):
  - ✅ Broken Access Control (RBAC, last admin protection)
  - ✅ Cryptographic Failures (bcrypt, JWT, auto-generated secrets)
  - ✅ Injection Attacks (parameterized queries, input validation)
  - ✅ Insecure Design (defense in depth, fail-secure)
  - ✅ Security Misconfiguration (defaults secure, audit logging)
  - ✅ Vulnerable Components (pinned versions, SHA digests)
  - ✅ Identification & Authentication (JWT, session management)
  - ✅ Software & Data Integrity (ETag, audit trail, backups)
  - ✅ Security Logging (audit.log, ClickHouse, no sensitive data)
  - ✅ Server-Side Request Forgery (URL validation, allowlist)
```

### Security Tools

```bash
# TruffleHog secret scanning
trufflehog filesystem --directory . --only-verified

# npm audit
cd services/web-ui/backend && npm audit

# Vitest security tests
cd services/workflow && npm test -- security
```

## Code Review Checklist (v2.0.0)

```markdown
## Security Review

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL queries parameterized
- [ ] Permissions checked server-side
- [ ] Passwords hashed with bcrypt (12 rounds)
- [ ] CORS configured properly
- [ ] Audit logging implemented
- [ ] ETag used for concurrent edits

## 3-Branch Security (v2.0.0)

- [ ] Branch timeouts configured (A:1000ms, B:2000ms, C:3000ms)
- [ ] Degradation handled (fail-safe to BLOCK)
- [ ] Arbiter thresholds not exposed to input
- [ ] Branch services isolated (no external network)
- [ ] unified_config.json validated before loading
```

## Related Skills

- `react-tailwind-vigil-ui` - Frontend security patterns
- `n8n-vigil-workflow` - 3-branch workflow security
- `docker-vigil-orchestration` - 11 service security
- `express-api-developer` - API security patterns

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Security docs: `docs/SECURITY.md`
- Auth docs: `docs/AUTHENTICATION.md`
- unified_config.json: `services/workflow/config/unified_config.json` (303 lines, v5.0.0)

---

**Last Updated:** 2025-12-09
**Version:** v2.0.0
**Architecture:** 3-Branch Parallel Detection
**Services:** 11 Docker containers
