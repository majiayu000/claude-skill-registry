---
name: context-security-resolver
description: Authentication, authorization, Clerk integration, RLS policies, and security
  patterns. Use when working with security-resolver code, files, or integration. Invoke
  when navigating security-resolver cod
---

---
name: context-security-resolver
description: |
  Authentication, authorization, Clerk integration, RLS policies, and security patterns. Use when working with security-resolver code, files, or integration. Invoke when navigating security-resolver codebase, searching for security-resolver files, debugging security-resolver errors, or discussing security-resolver patterns. Keywords: security-resolver, {{KEYWORDS}}
tags: {{TAGS}}
---

# security-resolver Context

**Files:** 32 files, 4118 LOC

Quick navigation for security-resolver area. Indexed 2025-11-22.

## Quick Navigation

### Database (Active)
- supabase/migrations/20250926220000_fix_rls_policies_for_service_role.sql ✅ CURRENT
- supabase/migrations/20250922160400_optimize_clerk_rls.sql ✅ CURRENT
- supabase/migrations/20250922131600_update_all_rls_for_clerk.sql ✅ CURRENT
- supabase/migrations/20250922124709_fix_rls_policies_v4.sql ✅ CURRENT
- supabase/migrations/20251003_fix_eodhd_constituents_rls.sql ✅ CURRENT
- supabase/migrations/20250922131700_fix_accounts_rls_jwt_claims.sql ✅ CURRENT
- supabase/migrations/20250913140001_rls_policies.sql ✅ CURRENT
- supabase/migrations/20250922125230_fix_rls_policies_v6.sql ✅ CURRENT
- supabase/migrations/20250922125100_fix_rls_policies_v5.sql ✅ CURRENT
- supabase/migrations/20250926213000_correct_security_master_rls_policies.sql ✅ CURRENT
- supabase/migrations/20250922131500_fix_clerk_rls_jwt_claims.sql ✅ CURRENT
- supabase/migrations/20250922130300_fix_rls_policies_v7.sql ✅ CURRENT
- supabase/migrations/20250914054145_supabase_auth_rls_policies.sql ✅ CURRENT
- supabase/migrations/20250922172000_clerk_auth_fixed.sql ✅ CURRENT
- supabase/migrations/20250921172500_clerk_auth_integration_v3.sql ✅ CURRENT
- supabase/migrations/20250921170000_clerk_auth_integration.sql ✅ CURRENT
- supabase/migrations/20250922160500_support_multiple_auth_methods.sql ✅ CURRENT
- supabase/migrations/20250922130400_fix_all_auth_references_v8.sql ✅ CURRENT
- supabase/migrations/20250922171500_clerk_auth_migration.sql ✅ CURRENT
- supabase/migrations/20250922130500_remove_supabase_auth_refs.sql ✅ CURRENT
- supabase/migrations/20250922161200_fix_clerk_auth_constraints.sql ✅ CURRENT
- supabase/migrations/20250921171000_clerk_auth_integration_v2.sql ✅ CURRENT
- supabase/migrations/20250914054145_supabase_auth_rls_policies.sql ✅ CURRENT
- supabase/migrations/20250925120000_add_security_id_to_fundamentals.sql ✅ CURRENT
- supabase/migrations/20250930180000_enhanced_security_resolver_schema.sql ✅ CURRENT
- supabase/migrations/20250928120000_create_auditable_security_master_v2.sql ✅ CURRENT
- supabase/migrations/20250926213000_correct_security_master_rls_policies.sql ✅ CURRENT
- supabase/migrations/20250926152616_create_auditable_security_master_schema.sql ✅ CURRENT
- supabase/migrations/20250925120001_backfill_fundamentals_security_id.sql ✅ CURRENT

### Backend (Active)
- backend/auth/clerk.py ✅ CURRENT
- backend/auth/__init__.py ✅ CURRENT

### Backend (Deprecated)
- backend/main_backup_pre_clerk_openapi.py ❌ DO NOT EDIT



## How to Use This Skill

**When navigating security-resolver code:**
- Use file paths with line numbers for precise navigation
- Check "CURRENT" markers for actively maintained files
- Avoid "DO NOT EDIT" files (backups, deprecated)
- Look for entry points (classes, main functions)

**Common tasks:**
- Find API endpoints: Look for `*_api.py:*` files
- Find business logic: Look for `*_service*.py` or engine classes
- Find data models: Look for `*_models.py` or schema definitions
- Find tests: Check "Tests" section

## Serena Quick Commands

```python
# Get symbol overview for a file
mcp__serena__get_symbols_overview(
  relative_path="<file_path_from_above>"
)

# Find specific symbol
mcp__serena__find_symbol(
  name_path="ClassName.method_name",
  relative_path="<file_path>",
  include_body=True
)

# Search for pattern
mcp__serena__search_for_pattern(
  substring_pattern="search_term",
  relative_path="<directory>"
)
```

## Maintenance

**Regenerate this skill:**
```bash
scripts/area-context-update security-resolver
```

**Edit area definition:**
```bash
# Edit .context/area-config.yml
# Then regenerate
scripts/area-context-update security-resolver
```

---

**Area:** security-resolver
**Last Updated:** 2025-11-22
**Maintenance:** Manual (regenerate as needed)
**Auto-activation:** Triggers on "security-resolver", "navigate security-resolver", "security-resolver files"
