---
name: security-review
description: Comprehensive security review checklist for auth, OAuth, admin, and multi-tenant code changes
user-invocable: true
---

# Security Review Skill

## Purpose
Comprehensive security review checklist triggered when modifying authentication, authorization, OAuth, admin, or multi-tenant code. Covers the categories identified in the Feb 2026 post-mortem audit.

## CLAUDE.md Compliance
- ✅ Enforces Security Engineering Rules from CLAUDE.md
- ✅ Validates authorization boundaries (authn != authz)
- ✅ Checks multi-tenant isolation patterns
- ✅ Verifies input validation and logging hygiene

## Usage
Run this skill:
- After modifying auth/OAuth/admin code
- After adding new API endpoints
- After database schema changes affecting tenant data
- Before committing security-sensitive changes
- During code review of security-related PRs

## Commands

### Full Security Review
```bash
echo "========================================="
echo "  SECURITY REVIEW CHECKLIST"
echo "========================================="

# 1. Authorization Boundaries
echo ""
echo "--- 1. Authorization Boundaries ---"

# Check for endpoints with auth but no role/permission check
echo "🔍 Checking auth endpoints for authorization..."
rg "async fn.*(admin|coach|manage|assign|remove|revoke|create_token|delete)" src/routes/ --type rust -A 15 | \
  rg -v "is_admin|is_super_admin|role|permission|tenant_membership" | \
  rg "async fn" && \
  echo "⚠️  Admin endpoints may lack authorization checks" || \
  echo "✓ Admin endpoints have authorization checks"

# Check super-admin operations require super-admin
echo "🔍 Checking super-admin gating..."
rg "super.?admin|SuperAdmin" src/routes/ --type rust -B 3 -A 10 | \
  rg "is_super_admin" | wc -l
echo "Super-admin check count (should be >0 for admin routes)"

# 2. Multi-Tenant Isolation
echo ""
echo "--- 2. Multi-Tenant Isolation ---"

# Check all SQL queries for tenant_id
echo "🔍 Checking SQL queries for tenant scoping..."
rg "sqlx::query" src/ --type rust -A 5 | \
  rg "SELECT|INSERT|UPDATE|DELETE" | \
  rg -v "tenant_id|migration|schema_version|system_config" | head -10
echo "(Above should be empty — all queries need tenant_id)"

# Check cache keys include tenant_id
echo "🔍 Checking cache key construction..."
rg "cache.*key|cache.*get|cache.*set|cache.*insert" src/ --type rust -A 3 | \
  rg -v "tenant" | rg "fn\|let" | head -5
echo "(Above should be empty — cache keys need tenant_id)"

# 3. Input Domain Validation
echo ""
echo "--- 3. Input Domain Validation ---"

# Check for division operations
echo "🔍 Checking division safety..."
rg "/ [a-z_]+" src/ --type rust -n | \
  rg -v "test|//|as f64|as f32|\.len\(\)|\.count\(\)" | \
  head -10
echo "(Review above for potential divide-by-zero)"

# Check pagination bounds
echo "🔍 Checking pagination bounds..."
rg "limit|offset|page_size|per_page" src/routes/ --type rust -A 3 | \
  rg "clamp|min|max|\.max\(1\)" | wc -l
echo "Pagination bound checks found"

# 4. OAuth & Protocol
echo ""
echo "--- 4. OAuth & Protocol Compliance ---"

# Check state parameter validation
echo "🔍 Checking OAuth state validation..."
rg "state.*param|validate.*state|verify.*state" src/ --type rust -n | wc -l
echo "State validation checks (should be >0)"

# Check PKCE enforcement
echo "🔍 Checking PKCE enforcement..."
rg "code_challenge|code_verifier" src/ --type rust -n | wc -l
echo "PKCE references (should be >0)"

# 5. Logging Hygiene
echo ""
echo "--- 5. Logging Hygiene ---"

# Check for sensitive data in logs
echo "🔍 Checking for secrets in log statements..."
rg "(info!|warn!|error!)\(.*\{.*(token|key|secret|password)" src/ --type rust -n | \
  rg -v "redact|REDACT|mask|\*\*\*|token_type|key_id|key_count" | head -5
echo "(Above should be empty — no secrets in logs)"

# 6. Template & Query Safety
echo ""
echo "--- 6. Template & Query Safety ---"

# Check for format! SQL
echo "🔍 Checking for format! SQL injection..."
rg "format!\(.*(?:SELECT|INSERT|UPDATE|DELETE)" src/ --type rust -n && \
  echo "❌ CRITICAL: format! used in SQL!" || \
  echo "✓ No format! SQL injection"

# Check HTML escaping
echo "🔍 Checking HTML escaping..."
rg "text/html|Content-Type.*html" src/ --type rust -B 5 -A 10 | \
  rg "format!" | rg -v "html_escape" | head -5
echo "(Above should be empty — HTML must use escaping)"

echo ""
echo "========================================="
echo "  SECURITY REVIEW COMPLETE"
echo "========================================="
```

## When to Trigger

This skill should be invoked when files in these paths are modified:
- `src/routes/auth.rs` — authentication/session management
- `src/routes/admin.rs` — admin panel operations
- `src/oauth2_server/` — OAuth authorization server
- `src/oauth2_client/` — OAuth client (Strava, etc.)
- `src/mcp/multitenant.rs` — multi-tenant MCP handling
- `src/database/` — database queries (tenant scoping)
- `src/middleware/` — auth/tenant middleware

## Success Criteria
- ✅ All admin endpoints verify role/permission (not just auth)
- ✅ All SQL queries include tenant_id scoping
- ✅ All cache keys include tenant_id
- ✅ No divide-by-zero risks in user-facing code
- ✅ Pagination has min/max bounds
- ✅ OAuth state is validated on callback
- ✅ No secrets/PII in INFO+ log levels
- ✅ No format!() SQL construction
- ✅ HTML output uses escaping functions

## Standalone Script
The CI-runnable version of this skill lives at `scripts/ci/security-review.sh`.
It runs automatically in CI via `./scripts/ci/architectural-validation.sh --apply-skills`.

## Related Skills
- `validate-architecture` — Architectural patterns
- `check-no-secrets` — Secret detection
- `test-multitenant-isolation` — Tenant isolation tests
- `check-input-validation` — Input validation checks
