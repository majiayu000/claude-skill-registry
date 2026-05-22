---
name: zero-trust
description: Identify and remediate Zero Trust security gaps in Cloudflare deployments. Use this skill when auditing Access policies, checking staging/dev environment protection, detecting unprotected admin routes, or implementing mTLS and service tokens for machine-to-machine auth.
---

# Cloudflare Zero Trust Skill

Audit and implement Zero Trust security policies using Cloudflare Access, service tokens, and mTLS. Ensure all environments (production, staging, dev) have appropriate access controls.

## Environment Protection Matrix

| Environment | Expected Protection | Common Gap | Risk Level |
|-------------|--------------------|-----------| -----------|
| Production | CF Access + WAF + Rate Limiting | Usually protected | LOW |
| Staging | CF Access (should mirror prod) | Often missing Access | HIGH |
| Development | CF Access or IP restrictions | Frequently exposed | CRITICAL |
| Preview (PR deploys) | CF Access or time-limited | Often public | HIGH |
| Admin/Internal APIs | Service Tokens + mTLS | Basic auth only | CRITICAL |

## Zero Trust Audit Workflow

### Step 1: Environment Discovery

```
1. List all Workers in account via MCP
2. Identify environment patterns:
   - *-staging, *-dev, *-preview
   - staging.*, dev.*, preview.*
   - Feature branch deployments
3. Check route configurations
```

### Step 2: Access Policy Verification

For each environment, verify:

```javascript
// Query Access applications
mcp__cloudflare-access__list_applications()

// For each route/hostname, check if Access policy exists:
// - Authentication requirement
// - Allow/Block rules
// - Session duration
// - Geographic restrictions
```

### Step 3: Audit Findings

| ID | Name | Severity | Check |
|----|------|----------|-------|
| ZT001 | Staging without Access | CRITICAL | staging.* routes without Access policy |
| ZT002 | Dev environment exposed | CRITICAL | dev.* publicly accessible |
| ZT003 | Preview deploys public | HIGH | *.pages.dev or preview.* without Access |
| ZT004 | Admin routes unprotected | CRITICAL | /admin/* without Access or auth middleware |
| ZT005 | Internal APIs no service token | HIGH | Internal service routes without mTLS/tokens |
| ZT006 | Weak session duration | MEDIUM | Access session > 24h for sensitive routes |
| ZT007 | No geographic restriction | LOW | Admin access from any country |
| ZT008 | Missing bypass audit | MEDIUM | Bypass rules without justification |
| ZT009 | Jobs route no service token | CRITICAL | /jobs/* without service token auth |
| ZT010 | Admin without MFA | HIGH | Admin uses password-only (no OTP/MFA) |
| ZT011 | Hardcoded credentials | CRITICAL | Service token credentials in source |
| ZT012 | Long admin sessions | MEDIUM | Admin session > 4h |

## Environment Detection Heuristics

### Staging/Dev Indicators

```
Hostname patterns:
- staging.*, stage.*, stg.*
- dev.*, development.*
- preview.*, pr-*.*, branch-*.*
- *.pages.dev (Cloudflare Pages previews)
- localhost:*, 127.0.0.1:*

Wrangler config indicators:
- env.staging, env.development
- name: "*-staging", "*-dev"
- vars.ENVIRONMENT: "staging" | "development"
```

### Admin Route Indicators

```
Path patterns requiring protection:
- /admin/*
- /api/admin/*
- /internal/*
- /dashboard/*
- /manage/*
- /config/*
- /_debug/*
- /metrics, /health (depends on sensitivity)
```

## Output Format

```markdown
# Zero Trust Audit Report

**Scope**: [Account/Zone]
**Environments Scanned**: X

## Critical Gaps (Immediate Action Required)

### [ZT001] Staging Environment Exposed
- **Route**: staging.example.com/*
- **Status**: No Access policy detected
- **Risk**: Staging data/functionality exposed to internet
- **Fix**: Create Access application with team email domain restriction
- **Provenance**: `[LIVE-VALIDATED]` via cloudflare-access MCP

## Recommendations

1. [ ] Create Access application for `staging.example.com`
2. [ ] Implement service token auth for CI/CD access
3. [ ] Add mTLS for internal service-to-service calls
4. [ ] Review and reduce session durations
```

## MCP Tools for Zero Trust

```javascript
// List Access applications
mcp__cloudflare-access__list_applications()

// Get application details
mcp__cloudflare-access__get_application({ app_id: "..." })

// List Access policies
mcp__cloudflare-access__list_policies({ app_id: "..." })

// Verify route protection
mcp__cloudflare-bindings__workers_list()
```

## Quick Reference

| Topic | Recommendation |
|-------|----------------|
| Preview deploys | Always protect with Access; use time-limited URLs |
| Service tokens | Rotate quarterly; scope to specific applications |
| mTLS | Required for PCI-DSS/HIPAA compliance scenarios |
| Session duration | Shorter for admin (1-4h), longer for general (24h) |
| Bypass rules | Document and audit regularly; set expiration |
| Geographic restrictions | Consider for admin access |
| Device posture | Enable for high-security environments (requires WARP) |

## Reference Files

For detailed implementation patterns, consult:

- **`references/access-policies.md`** - Access policy patterns, Terraform examples, policy generator
- **`references/tunnel-config.md`** - Cloudflare Tunnel setup, config.yml examples, deployment patterns
- **`references/service-tokens.md`** - Service token auth, admin protection checklist, extended validation rules

## Related Skills

- **architect**: Overall architecture including Access integration
- **guardian**: Security auditing across all Cloudflare services
- **loop-breaker**: Preventing service token abuse in loops
