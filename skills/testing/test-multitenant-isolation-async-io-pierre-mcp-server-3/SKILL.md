---
name: test-multitenant-isolation
description: Validates complete data isolation between tenants, tests cross-tenant access, ensures proper query scoping
user-invocable: true
---

# Multi-Tenant Isolation Testing Skill

## Purpose
Validates complete data isolation between tenants to prevent catastrophic data leaks. Tests cross-tenant access attempts and ensures all database queries are properly scoped.

## CLAUDE.md Compliance
- ✅ Tests use synthetic data (no external dependencies)
- ✅ Deterministic test execution
- ✅ Tests both success and attack scenarios
- ✅ Validates security-critical functionality

## Usage
Run this skill:
- After authentication/authorization changes
- After database schema modifications
- Before production deployments
- After tenant-related code changes
- Weekly security audits

## Prerequisites
- SQLite or PostgreSQL database
- Test database cleanup (automatic via tempfile)

## Commands

### Comprehensive Multi-Tenant Test
```bash
# Run full multi-tenant isolation test suite
cargo test --test mcp_multitenant_complete_test --features testing -- --nocapture
```

### Quick Isolation Check
```bash
# Run specific isolation tests
cargo test multitenant -- --nocapture

# Test cross-tenant access attempts
cargo test test_cross_tenant -- --nocapture

# Test tenant context middleware
cargo test test_tenant_middleware -- --nocapture
```

### Database Query Scoping Validation
```bash
# Search for queries without tenant_id filtering
echo "🔍 Checking for unscoped queries..."
rg "SELECT.*FROM.*WHERE" src/ --type rust -A 3 | rg -v "tenant_id" | head -20

# Verify TenantContext usage in routes
echo "🔍 Checking route handler tenant context..."
rg "Extension.*TenantContext" src/routes/ --type rust -n | wc -l

# Check for hardcoded tenant IDs (security issue)
rg -i "tenant.*=.*\"[a-f0-9-]{36}\"" src/ --type rust -n || echo "✓ No hardcoded tenant IDs"
```

## Test Scenarios

### Scenario 1: Cross-Tenant Activity Access
```rust
// Tenant A creates activity
// Tenant B attempts to read it
// Expected: 403 Forbidden or empty result
```

### Scenario 2: Tenant Context Injection
```rust
// Middleware extracts tenant_id from JWT
// All subsequent queries filtered by tenant_id
// Expected: Only tenant's own data visible
```

### Scenario 3: API Key Isolation
```rust
// Tenant A's API key used
// Attempt to access Tenant B's data
// Expected: Empty results (not 403 - security through obscurity)
```

### Scenario 4: OAuth Token Isolation
```rust
// OAuth tokens stored per tenant
// Tenant A cannot access Tenant B's tokens
// Expected: Null/NotFound
```

## Security Checks

### Database Query Patterns
```bash
# All queries MUST include tenant_id filter
# Examples of CORRECT patterns:

# ✅ SELECT with tenant_id
SELECT * FROM activities WHERE tenant_id = $1 AND user_id = $2

# ✅ INSERT with tenant_id
INSERT INTO activities (tenant_id, user_id, ...) VALUES ($1, $2, ...)

# ✅ UPDATE with tenant_id
UPDATE activities SET ... WHERE tenant_id = $1 AND id = $2

# ✅ DELETE with tenant_id
DELETE FROM activities WHERE tenant_id = $1 AND id = $2
```

### TenantContext Pattern
```rust
// All route handlers must use TenantContext

// ✅ Correct
pub async fn get_activities(
    Extension(tenant): Extension<TenantContext>,
    Json(params): Json<GetActivitiesParams>,
) -> Result<Json<Activities>, AppError> {
    // tenant.tenant_id automatically scopes queries
}

// ❌ Incorrect (missing TenantContext)
pub async fn get_activities(
    Json(params): Json<GetActivitiesParams>,
) -> Result<Json<Activities>, AppError> {
    // No tenant scoping!
}
```

## Test Output Analysis

### Expected Output
```
test test_tenant_isolation ... ok
test test_cross_tenant_activity_access ... ok (should fail access)
test test_cross_tenant_user_access ... ok (should fail access)
test test_tenant_oauth_isolation ... ok
test test_tenant_api_key_isolation ... ok

test result: ok. 12 passed; 0 failed
```

### Failure Indicators
```
# ❌ BAD: Cross-tenant access succeeded
test test_cross_tenant_activity_access ... FAILED
  Expected: Forbidden or empty
  Actual: Returned data from other tenant

# ❌ BAD: Query without tenant_id
  SELECT * FROM activities WHERE user_id = $1
  (Missing tenant_id filter!)

# ❌ BAD: Tenant ID from request body instead of JWT
  let tenant_id = params.tenant_id;  // User can forge!
```

### OAuth Credential Isolation
```bash
# Verify OAuth tokens are stored per-tenant (not global)
echo "🔐 Checking OAuth credential isolation..."
rg "oauth_token|refresh_token|access_token" src/database/ --type rust -A 3 | \
  rg "tenant_id" | wc -l
echo "OAuth token queries with tenant_id scoping"

# Check that provider credentials are tenant-scoped
rg "provider.*credential|strava.*token|garmin.*token" src/ --type rust -A 5 | \
  rg -v "tenant_id" | rg "SELECT|INSERT|UPDATE" && \
  echo "⚠️  Provider credential query without tenant_id!" || \
  echo "✓ Provider credentials properly tenant-scoped"
```

### Config Write/Delete Tenant Scoping
```bash
# Verify config mutations check tenant membership
echo "🔐 Checking config write/delete tenant scoping..."
rg "fn.*config.*(create|update|delete|write|remove)" src/ --type rust -A 10 | \
  rg "tenant_id" | wc -l
echo "Config mutation functions with tenant_id check"

# Check admin tools verify target belongs to caller's tenant
rg "fn.*(assign|remove|update).*coach|fn.*(assign|remove|update).*user" src/ --type rust -A 10 | \
  rg "tenant_id" | wc -l
echo "Admin tool functions with tenant_id verification"
```

### LLM API Key Isolation
```bash
# Verify LLM/AI settings are per-tenant
echo "🔐 Checking LLM API key isolation..."
rg "llm.*key|ai.*key|gemini.*key|groq.*key|ollama.*url" src/ --type rust -A 5 | \
  rg "tenant_id" | wc -l
echo "LLM key storage/retrieval with tenant_id scoping"
```

## Success Criteria
- ✅ All multi-tenant tests pass
- ✅ Cross-tenant access attempts fail (403 or empty)
- ✅ All database queries include tenant_id filter
- ✅ TenantContext used in all route handlers
- ✅ No hardcoded tenant IDs in code
- ✅ OAuth tokens isolated per tenant
- ✅ API keys isolated per tenant
- ✅ Zero data leakage in logs (PII redaction active)
- ✅ Provider credentials (Strava, Garmin) tenant-scoped
- ✅ Config write/delete operations verify tenant membership
- ✅ LLM API keys stored and retrieved per-tenant
- ✅ Admin tools verify target belongs to caller's tenant

## Related Files
- `tests/mcp_multitenant_complete_test.rs` - Main test suite
- `src/tenant/mod.rs` - TenantContext definition
- `src/middleware/tenant_middleware.rs` - Tenant extraction
- `src/database/mod.rs` - Scoped database queries

## Related Skills
- `check-no-secrets` - Secret detection
- `validate-architecture` - Architectural validation
