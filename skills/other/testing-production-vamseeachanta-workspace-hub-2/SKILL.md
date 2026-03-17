---
name: testing-production
description: Production validation specialist ensuring applications are fully implemented and deployment-ready. Use to verify no mock/stub/fake implementations remain, validate against real databases and APIs, perform end-to-end testing with actual systems, and confirm production readiness.
version: 1.0.0
category: development
type: hybrid
capabilities:
  - production_validation
  - implementation_verification
  - end_to_end_testing
  - deployment_readiness
  - real_world_simulation
  - security_validation
  - performance_under_load
tools:
  - Read
  - Write
  - Bash
  - Grep
  - Task
related_skills:
  - testing-tdd-london
  - webapp-testing
  - planning-code-goal
hooks:
  pre: |
    echo "Production Validator starting..."
    echo "Scanning for mock/fake implementations..."
    grep -r "mock\|fake\|stub\|TODO\|FIXME" src/ || echo "No mock implementations found"
  post: |
    echo "Production validation complete"
    if [ -f "package.json" ]; then
      npm run test:production --if-present
      npm run test:e2e --if-present
    fi
---

# Production Validation

> Ensuring applications are fully implemented, tested against real systems, and deployment-ready

## Quick Start

```bash
# Scan for incomplete implementations
grep -r "mock\|fake\|stub\|TODO\|FIXME" src/ --exclude-dir=__tests__

# Run production validation tests
npm run test:production
npm run test:e2e

# Validate against real services
npm run test:integration -- --env=staging
```

## When to Use

- Before deploying to production
- After completing TDD implementation phase
- To verify no mock implementations remain in production code
- To test against real databases, APIs, and infrastructure
- To validate performance under realistic load
- To confirm security measures are properly implemented

## Prerequisites

- Completed unit/integration test suite
- Access to staging environment with real services
- Environment variables for real service connections
- Load testing tools (if validating performance)

## Core Concepts

### Production Validation vs Unit Testing

| Aspect | Unit Tests (TDD) | Production Validation |
|--------|------------------|----------------------|
| Dependencies | Mocked | Real |
| Database | In-memory/fake | Actual PostgreSQL/etc |
| APIs | Stubbed responses | Live service calls |
| Purpose | Design/logic | Deployment readiness |
| Speed | Fast (ms) | Slower (seconds) |

### Validation Categories

1. **Implementation Completeness**: No mock/stub/fake code in production
2. **Database Integration**: CRUD operations on real database
3. **External APIs**: Actual service integrations work
4. **Infrastructure**: Cache, email, queues function correctly
5. **Performance**: Meets latency and throughput requirements
6. **Security**: Authentication, authorization, input validation

## Implementation Pattern

### 1. Implementation Completeness Check

```typescript
const validateImplementation = async (codebase: string[]): Promise<Violation[]> => {
  const violations: Violation[] = [];

  // Patterns indicating incomplete implementation
  const mockPatterns = [
    /mock[A-Z]\w+/g,           // mockService, mockRepository
    /fake[A-Z]\w+/g,           // fakeDatabase, fakeAPI
    /stub[A-Z]\w+/g,           // stubMethod, stubService
    /TODO.*implementation/gi,   // TODO: implement this
    /FIXME.*mock/gi,           // FIXME: replace mock
    /throw new Error\(['"]not implemented/gi
  ];

  for (const file of codebase) {
    for (const pattern of mockPatterns) {
      if (pattern.test(file.content)) {
        violations.push({
          file: file.path,
          issue: 'Mock/fake implementation found',
          pattern: pattern.source
        });
      }
    }
  }

  return violations;
};
```

### 2. Real Database Validation

```typescript
describe('Database Integration Validation', () => {
  let realDatabase: Database;

  beforeAll(async () => {
    // Connect to actual test database (NOT in-memory)
    realDatabase = await DatabaseConnection.connect({
      host: process.env.TEST_DB_HOST,
      database: process.env.TEST_DB_NAME,
      port: parseInt(process.env.TEST_DB_PORT || '5432'),
      ssl: true
    });
  });

  afterAll(async () => {
    await realDatabase.disconnect();
  });

  it('should perform complete CRUD operations', async () => {
    const repository = new UserRepository(realDatabase);

    // CREATE
    const user = await repository.create({
      email: 'validation-test@example.com',
      name: 'Validation Test'
    });
    expect(user.id).toBeDefined();
    expect(user.createdAt).toBeInstanceOf(Date);

    // READ
    const retrieved = await repository.findById(user.id);
    expect(retrieved).toEqual(user);

    // UPDATE
    const updated = await repository.update(user.id, { name: 'Updated Name' });
    expect(updated.name).toBe('Updated Name');

    // DELETE
    await repository.delete(user.id);
    const deleted = await repository.findById(user.id);
    expect(deleted).toBeNull();
  });
});
```

### 3. External API Validation

```typescript
describe('External API Validation', () => {
  it('should integrate with real payment service', async () => {
    const paymentService = new PaymentService({
      apiKey: process.env.STRIPE_TEST_KEY,
      baseUrl: 'https://api.stripe.com/v1'
    });

    // Test actual API call
    const paymentIntent = await paymentService.createPaymentIntent({
      amount: 1000,
      currency: 'usd',
      customer: 'cus_test_customer'
    });

    expect(paymentIntent.id).toMatch(/^pi_/);
    expect(paymentIntent.status).toBe('requires_payment_method');
    expect(paymentIntent.amount).toBe(1000);
  });

  it('should handle real API errors gracefully', async () => {
    const paymentService = new PaymentService({
      apiKey: 'invalid_key',
      baseUrl: 'https://api.stripe.com/v1'
    });

    await expect(
      paymentService.createPaymentIntent({ amount: 1000, currency: 'usd' })
    ).rejects.toThrow('Invalid API key');
  });
});
```

## Configuration

```yaml
production_validation:
  scan:
    patterns:
      - "mock"
      - "fake"
      - "stub"
      - "TODO"
      - "FIXME"
      - "not implemented"
    exclude_dirs:
      - "__tests__"
      - "tests"
      - "spec"
      - "node_modules"
    exclude_files:
      - "*.test.*"
      - "*.spec.*"

  database:
    use_real: true
    host: ${TEST_DB_HOST}
    cleanup_after: true

  external_apis:
    use_test_mode: true
    timeout_ms: 30000
    retry_count: 3

  performance:
    concurrent_requests: 100
    max_latency_ms: 200
    min_throughput_rps: 1000
    sustained_duration_s: 60
```

## Usage Examples

### Example 1: Complete Validation Suite

```typescript
describe('Production Readiness Validation', () => {
  describe('Implementation Completeness', () => {
    it('should have no mock implementations in production code', async () => {
      const result = await exec(
        'grep -r "mock\\|fake\\|stub" src/ --exclude-dir=__tests__ --exclude="*.test.*"'
      );
      expect(result.stdout).toBe('');
    });

    it('should have no TODO/FIXME in critical paths', async () => {
      const result = await exec('grep -r "TODO\\|FIXME" src/');
      expect(result.stdout).toBe('');
    });

    it('should have no hardcoded test data', async () => {
      const result = await exec(
        'grep -r "test@\\|example\\|localhost" src/ --exclude-dir=__tests__'
      );
      expect(result.stdout).toBe('');
    });
  });

  describe('Environment Configuration', () => {
    it('should have all required environment variables', () => {
      const required = [
        'DATABASE_URL',
        'REDIS_URL',
        'API_KEY',
        'SMTP_HOST',
        'JWT_SECRET'
      ];

      const missing = required.filter(key => !process.env[key]);
      expect(missing).toEqual([]);
    });
  });
});
```

### Example 2: Infrastructure Validation

```typescript
describe('Infrastructure Validation', () => {
  it('should connect to real Redis cache', async () => {
    const cache = new RedisCache({
      host: process.env.REDIS_HOST,
      port: parseInt(process.env.REDIS_PORT || '6379'),
      password: process.env.REDIS_PASSWORD
    });

    await cache.connect();

    // Test cache operations
    await cache.set('validation-key', 'test-value', 300);
    const value = await cache.get('validation-key');
    expect(value).toBe('test-value');

    await cache.delete('validation-key');
    const deleted = await cache.get('validation-key');
    expect(deleted).toBeNull();

    await cache.disconnect();
  });

  it('should send real emails via SMTP', async () => {
    const emailService = new EmailService({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587'),
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    });

    const result = await emailService.send({
      to: 'validation-test@example.com',
      subject: 'Production Validation Test',
      body: 'This is a real email sent during validation'
    });

    expect(result.messageId).toBeDefined();
    expect(result.accepted).toContain('validation-test@example.com');
  });
});
```

### Example 3: Performance Validation

```typescript
describe('Performance Validation', () => {
  it('should handle concurrent requests within latency requirements', async () => {
    const apiClient = new APIClient(process.env.API_BASE_URL);
    const concurrentRequests = 100;
    const startTime = Date.now();

    const promises = Array.from({ length: concurrentRequests }, () =>
      apiClient.get('/health')
    );

    const results = await Promise.all(promises);
    const duration = Date.now() - startTime;

    // All requests succeeded
    expect(results.every(r => r.status === 200)).toBe(true);

    // Within 5 seconds for 100 requests
    expect(duration).toBeLessThan(5000);

    // Average response time under 50ms
    const avgResponseTime = duration / concurrentRequests;
    expect(avgResponseTime).toBeLessThan(50);
  });

  it('should maintain performance under sustained load', async () => {
    const apiClient = new APIClient(process.env.API_BASE_URL);
    const duration = 60000; // 1 minute
    const requestsPerSecond = 10;
    const startTime = Date.now();

    let totalRequests = 0;
    let successfulRequests = 0;

    while (Date.now() - startTime < duration) {
      const batchStart = Date.now();
      const batch = Array.from({ length: requestsPerSecond }, () =>
        apiClient.get('/api/users').catch(() => null)
      );

      const results = await Promise.all(batch);
      totalRequests += requestsPerSecond;
      successfulRequests += results.filter(r => r?.status === 200).length;

      // Throttle to maintain rate
      const elapsed = Date.now() - batchStart;
      if (elapsed < 1000) {
        await new Promise(resolve => setTimeout(resolve, 1000 - elapsed));
      }
    }

    const successRate = successfulRequests / totalRequests;
    expect(successRate).toBeGreaterThan(0.95); // 95% success rate
  });
});
```

### Example 4: Security Validation

```typescript
describe('Security Validation', () => {
  it('should enforce authentication on protected routes', async () => {
    const response = await request(app)
      .get('/api/protected')
      .expect(401);

    expect(response.body.error).toBe('Authentication required');
  });

  it('should validate and sanitize input', async () => {
    const maliciousInput = '<script>alert("xss")</script>';

    const response = await request(app)
      .post('/api/users')
      .send({ name: maliciousInput })
      .set('Authorization', `Bearer ${validToken}`)
      .expect(400);

    expect(response.body.error).toContain('Invalid input');
  });

  it('should use HTTPS in production', () => {
    if (process.env.NODE_ENV === 'production') {
      expect(process.env.FORCE_HTTPS).toBe('true');
    }
  });

  it('should have proper health check endpoint', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);

    expect(response.body).toMatchObject({
      status: 'healthy',
      timestamp: expect.any(String),
      uptime: expect.any(Number),
      dependencies: {
        database: 'connected',
        cache: 'connected',
        external_api: 'reachable'
      }
    });
  });
});
```

## Execution Checklist

- [ ] Scan for mock/fake/stub implementations
- [ ] Scan for TODO/FIXME comments
- [ ] Verify all environment variables configured
- [ ] Test database CRUD with real database
- [ ] Test external APIs with real (test mode) services
- [ ] Test infrastructure (cache, email, queues)
- [ ] Validate performance under load
- [ ] Verify security measures (auth, input validation)
- [ ] Test health check endpoint
- [ ] Verify graceful shutdown handling

## Best Practices

### Real Data Usage
- Use production-like test data, not placeholder values
- Test with actual file uploads, not mock files
- Validate with real user scenarios and edge cases

### Infrastructure Testing
- Test against actual databases, not in-memory alternatives
- Validate network connectivity and timeouts
- Test failure scenarios with real service outages

### Performance Validation
- Measure actual response times under load
- Test memory usage with real data volumes
- Validate scaling behavior with production-sized datasets

### Security Testing
- Test authentication with real identity providers
- Validate encryption with actual certificates
- Test authorization with real user roles and permissions

## Error Handling

### Mock Found in Production Code

```bash
# Identify and report violations
grep -rn "mock\|fake\|stub" src/ --exclude-dir=__tests__ | while read line; do
  echo "VIOLATION: $line"
  echo "ACTION: Replace with real implementation"
done
```

### External Service Unavailable

```typescript
// Graceful handling of service outages during validation
try {
  await validateExternalService(service);
} catch (error) {
  if (error.code === 'ECONNREFUSED') {
    console.warn(`Service ${service.name} unavailable - skipping validation`);
    skippedValidations.push(service.name);
  } else {
    throw error;
  }
}

// Report skipped validations
if (skippedValidations.length > 0) {
  console.warn(`Skipped validations: ${skippedValidations.join(', ')}`);
  console.warn('These MUST be validated before production deploy');
}
```

## Metrics & Success Criteria

| Validation | Pass Criteria |
|------------|---------------|
| Mock-Free Code | 0 mock/fake/stub in production code |
| Database Integration | All CRUD operations work |
| API Integration | All external APIs respond correctly |
| Performance | p99 < 200ms, > 1000 req/s |
| Security | All auth/authz tests pass |
| Health Check | Returns healthy status |
| Error Rate | < 0.1% under load |

## Integration Points

### MCP Tools

```javascript
// Store validation results
  action: "store",
  namespace: "production-validation",
  key: "validation_report_" + Date.now(),
  value: JSON.stringify({
    timestamp: new Date().toISOString(),
    violations: violations,
    passed: validations.passed,
    failed: validations.failed
  })
});
```

### Hooks

```bash
# Pre-deploy: Run production validation

# Post-validation: Report results
```

### Related Skills

- [testing-tdd-london](../testing-tdd-london/SKILL.md) - Unit testing with mocks
- [webapp-testing](../../webapp-testing/SKILL.md) - Web application testing
- [planning-code-goal](../../planning/planning-code-goal/SKILL.md) - Testing strategy planning

## References

- [Continuous Delivery](https://continuousdelivery.com/)
- [Testing in Production](https://launchdarkly.com/blog/testing-in-production/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from production-validator agent
