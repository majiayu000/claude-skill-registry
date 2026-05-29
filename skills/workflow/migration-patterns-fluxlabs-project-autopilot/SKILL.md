---
name: migration-patterns
description: Database, framework, and API migration strategies and safe patterns. Reference this skill when planning migrations.
---

# Migration Patterns Skill
# Project Autopilot - Safe migration strategies
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for safe, reliable migrations.

---

## Migration Principles

### The Migration Pyramid

```
           ┌─────────┐
          ╱           ╲
         ╱   VERIFY    ╲
        ╱               ╲
       ├─────────────────┤
      ╱                   ╲
     ╱      EXECUTE        ╲
    ╱                       ╲
   ├─────────────────────────┤
  ╱                           ╲
 ╱          PREPARE            ╲
╱                               ╲
└───────────────────────────────┘
```

1. **Prepare** (Foundation)
   - Full backups
   - Rollback procedures
   - Impact analysis

2. **Execute** (Implementation)
   - Incremental changes
   - Continuous testing
   - Monitoring

3. **Verify** (Validation)
   - Integrity checks
   - Performance benchmarks
   - Functionality testing

---

## Database Migration Patterns

### Expand-Contract Pattern

Safe schema evolution in production.

**Phase 1: Expand**
```sql
-- Add new column (nullable)
ALTER TABLE users ADD COLUMN email_verified BOOLEAN;

-- Add new index concurrently
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

**Phase 2: Migrate Data**
```sql
-- Backfill existing data
UPDATE users SET email_verified = false WHERE email_verified IS NULL;
```

**Phase 3: Contract**
```sql
-- Add constraint (after all code updated)
ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;

-- Drop old column (after deprecation period)
ALTER TABLE users DROP COLUMN legacy_field;
```

### Parallel Change Pattern

Run old and new simultaneously.

```typescript
// 1. Write to both
async function updateUser(id: string, data: UserData) {
  // Write to new schema
  await newSchema.update(id, data);
  // Write to old schema (for rollback)
  await oldSchema.update(id, data);
}

// 2. Compare results
async function getUser(id: string) {
  const [oldResult, newResult] = await Promise.all([
    oldSchema.get(id),
    newSchema.get(id),
  ]);

  if (!deepEqual(oldResult, newResult)) {
    logger.warn('Schema mismatch', { id, old: oldResult, new: newResult });
  }

  return newResult;
}

// 3. Switch reads to new
// 4. Stop writing to old
// 5. Remove old schema
```

### Zero-Downtime Migration

```sql
-- Create new table
CREATE TABLE users_v2 (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create trigger to sync writes
CREATE OR REPLACE FUNCTION sync_users_v2()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO users_v2 (id, email, created_at)
  VALUES (NEW.id, NEW.email, NEW.created_at)
  ON CONFLICT (id) DO UPDATE SET
    email = EXCLUDED.email;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_sync_trigger
AFTER INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION sync_users_v2();

-- Backfill historical data
INSERT INTO users_v2 (id, email, created_at)
SELECT id, email, created_at FROM users
ON CONFLICT DO NOTHING;

-- Switch application to new table
-- Remove trigger and old table
```

---

## Framework Migration Patterns

### Strangler Fig Pattern

Gradually replace legacy system.

```typescript
// Facade that routes to old or new
class AuthFacade {
  async authenticate(credentials: Credentials): Promise<User> {
    // Check if user should use new system
    if (this.shouldUseNew(credentials)) {
      return this.newAuth.authenticate(credentials);
    }
    return this.legacyAuth.authenticate(credentials);
  }

  private shouldUseNew(credentials: Credentials): boolean {
    // Gradual rollout based on email domain
    const domain = credentials.email.split('@')[1];
    return this.enabledDomains.includes(domain);
  }
}
```

### Branch by Abstraction

Create abstraction, implement new, switch.

```typescript
// 1. Create interface
interface PaymentProcessor {
  charge(amount: number, source: string): Promise<ChargeResult>;
  refund(chargeId: string): Promise<RefundResult>;
}

// 2. Implement for legacy
class LegacyPaymentProcessor implements PaymentProcessor {
  async charge(amount: number, source: string) {
    return this.legacySDK.processPayment(amount, source);
  }
}

// 3. Implement for new
class NewPaymentProcessor implements PaymentProcessor {
  async charge(amount: number, source: string) {
    return this.newSDK.createCharge({ amount, source });
  }
}

// 4. Use factory to switch
class PaymentProcessorFactory {
  create(): PaymentProcessor {
    if (config.useNewPayments) {
      return new NewPaymentProcessor();
    }
    return new LegacyPaymentProcessor();
  }
}
```

### Incremental TypeScript Migration

```typescript
// tsconfig.json - Start lenient
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false,
    "strict": false,
    "noImplicitAny": false
  }
}

// Phase 1: Rename .js to .ts (no changes)
// Phase 2: Add types to new files
// Phase 3: Enable noImplicitAny per-directory
// Phase 4: Enable strict per-directory
// Phase 5: Full strict mode
```

---

## API Migration Patterns

### Versioned API

```typescript
// Version in URL
app.get('/api/v1/users', v1UserController);
app.get('/api/v2/users', v2UserController);

// Version in header
app.get('/api/users', (req, res, next) => {
  const version = req.header('API-Version') || '1';
  if (version === '2') {
    return v2UserController(req, res, next);
  }
  return v1UserController(req, res, next);
});
```

### Deprecation Pattern

```typescript
// Add deprecation warnings
app.get('/api/v1/users', (req, res, next) => {
  res.setHeader('Deprecation', 'true');
  res.setHeader('Sunset', 'Sat, 31 Dec 2026 23:59:59 GMT');
  res.setHeader('Link', '</api/v2/users>; rel="successor-version"');

  // Log deprecation usage
  logger.info('Deprecated API called', {
    endpoint: '/api/v1/users',
    client: req.headers['user-agent'],
  });

  return v1UserController(req, res, next);
});
```

### Consumer-Driven Contract

```typescript
// Maintain contracts for consumers
const consumerContracts = {
  'mobile-app': {
    endpoints: ['/api/users', '/api/orders'],
    fields: ['id', 'name', 'email'],
  },
  'admin-dashboard': {
    endpoints: ['/api/users', '/api/analytics'],
    fields: ['id', 'name', 'email', 'role', 'lastLogin'],
  },
};

// Verify contracts before release
function verifyContracts(newApi: OpenAPISpec): ContractResult[] {
  return Object.entries(consumerContracts).map(([consumer, contract]) => ({
    consumer,
    result: validateContract(newApi, contract),
  }));
}
```

---

## Rollback Strategies

### Instant Rollback (Feature Flags)

```typescript
// Disable feature instantly
await featureFlags.set('new-checkout', false);
// All traffic immediately uses old implementation
```

### Blue-Green Rollback

```bash
# Switch traffic back to blue
kubectl patch service myapp -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Database Rollback

```sql
-- Point-in-time recovery
pg_restore -d mydb --target-time="2026-01-29 14:30:00" backup.dump

-- Or restore from backup
pg_restore -d mydb backup_before_migration.dump
```

### Git Rollback

```bash
# Revert specific commit
git revert abc123

# Revert merge commit
git revert -m 1 merge_commit_hash

# Reset to previous state (caution!)
git reset --hard HEAD~1
```

---

## Migration Checklist

### Before Migration

- [ ] Impact analysis complete
- [ ] All affected systems identified
- [ ] Rollback plan documented
- [ ] Rollback plan tested
- [ ] Full backup taken
- [ ] Backup verified
- [ ] Team notified
- [ ] Monitoring in place
- [ ] Maintenance window scheduled (if needed)

### During Migration

- [ ] Execute steps in order
- [ ] Verify each step before proceeding
- [ ] Monitor error rates
- [ ] Monitor performance
- [ ] Be ready to rollback

### After Migration

- [ ] Full functionality test
- [ ] Performance benchmarks
- [ ] Data integrity checks
- [ ] Remove deprecated code/data
- [ ] Update documentation
- [ ] Notify stakeholders
- [ ] Post-mortem if issues occurred
