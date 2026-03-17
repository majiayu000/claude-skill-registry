---
name: fabric-lakehouse-access-control
description: Troubleshoot Microsoft Fabric Lakehouse access control issues including OneLake security roles, SQL analytics endpoint permissions, workspace roles, data access roles, row-level security (RLS), column-level security (CLS), object-level security (OLS), dynamic data masking, shortcut permissions, Direct Lake security integration, DefaultReader role, ReadAll permission, and OneLake data access role conflicts. Use when users report permission denied, unauthorized access, missing data, empty query results, or cannot see tables in Fabric Lakehouse.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric Lakehouse Access Control remediate

Diagnose and resolve access control issues across all security layers of Microsoft Fabric Lakehouse, including workspace roles, item permissions, OneLake security data access roles, SQL analytics endpoint granular permissions, and Direct Lake semantic model security integration.

## When to Use This Skill

- User cannot access lakehouse data or sees "permission denied" errors
- Queries return empty results or missing rows/columns unexpectedly
- OneLake security roles not applying or taking too long to propagate
- SQL analytics endpoint permissions not restricting access as expected
- Direct Lake semantic model returns errors after enabling OneLake security
- Shortcut data is inaccessible or returns 404 errors
- DefaultReader role conflicts with custom data access roles
- Deployment pipeline or git integration issues with data access roles
- Users see data they should not have access to (over-provisioned)
- Row-level or column-level security not filtering correctly

## Prerequisites

- Microsoft Fabric workspace with capacity or trial license
- Admin, Member, or Contributor workspace role for managing security
- Familiarity with T-SQL for SQL analytics endpoint security
- PowerShell 7+ for running diagnostic scripts

## Fabric Lakehouse Security Layers

Fabric Lakehouse enforces security through multiple overlapping layers. Understanding the evaluation order is critical for remediate.

**Layer 1 - Workspace Roles** control coarse access to all items in a workspace.

| Role | Workspace Access | OneLake Read/Write | Manage Security |
|------|-----------------|-------------------|-----------------|
| Admin | Full | Yes | Yes |
| Member | Full | Yes | Yes |
| Contributor | Full | Yes | No |
| Viewer | See items only | No (unless granted) | No |

**Layer 2 - Item Permissions** grant access to a single lakehouse without a workspace role. Key permissions: Read (see item), ReadAll (read all OneLake data), Reshare, Write.

**Layer 3 - OneLake Security (Preview)** provides granular role-based access at the table, folder, row, and column level. Enforced across all compute engines. Disabled by default; once enabled, cannot be turned off.

**Layer 4 - SQL Analytics Endpoint Security** uses T-SQL GRANT/DENY/REVOKE for object-level, row-level, and column-level security. Only applies to queries via the SQL analytics endpoint.

**Layer 5 - Semantic Model Security** applies RLS/OLS within Direct Lake or DirectQuery models only.

## Quick Diagnostic Workflow

Follow this sequence to isolate the root cause. See [workflow-diagnostics.md](./references/workflow-diagnostics.md) for full details.

### TODO
- [ ] Step 1: Identify the access path — see [workflow-diagnostics.md](./references/workflow-diagnostics.md#step-1-identify-access-path)
- [ ] Step 2: Verify workspace role and item permissions — see [workflow-diagnostics.md](./references/workflow-diagnostics.md#step-2-verify-workspace-and-item-permissions)
- [ ] Step 3: Check OneLake security role membership — see [workflow-diagnostics.md](./references/workflow-diagnostics.md#step-3-check-onelake-security)
- [ ] Step 4: Audit SQL analytics endpoint permissions — see [workflow-diagnostics.md](./references/workflow-diagnostics.md#step-4-audit-sql-endpoint-permissions)
- [ ] Step 5: Validate Direct Lake security integration — see [workflow-diagnostics.md](./references/workflow-diagnostics.md#step-5-validate-direct-lake-integration)
- [ ] Step 6: Check shortcut and cross-region access — see [workflow-diagnostics.md](./references/workflow-diagnostics.md#step-6-check-shortcuts)

## Common Issues and Resolutions

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| User sees all data despite OneLake security roles | DefaultReader role still active | Delete or edit DefaultReader role to remove ReadAll grant |
| Empty results from queries | RLS filtering all rows for user | Check RLS predicates; verify user is member of correct role |
| "Can't find table" or "Column can't be found" in Direct Lake | OLS/CLS hiding objects after OneLake security applied | Add user to role with table/column access |
| Shortcut returns 404 | Cross-region shortcut with OneLake security enabled | OneLake security does not support cross-region shortcuts |
| Permission changes not taking effect | Propagation latency | Role definition changes: ~5 min. Group membership changes: ~1 hour. Some engines add another hour of caching |
| SQL endpoint shows data OneLake security should restrict | SQL security and OneLake security are separate layers | Apply security at both layers or restrict access to only the secured endpoint |
| B2B guest user cannot access data via OneLake security role | Entra External ID settings | Set Guest user access to "same access as members" in Entra External Collaboration settings |
| Distribution list members can't access SQL endpoint | SQL endpoint can't resolve DL membership | Use security groups instead of distribution lists for OneLake security roles |
| Deployment pipeline fails for data access roles | Target workspace DAR tracking not enabled | Manually enable DAR tracking on target workspace before deploying |

## OneLake Security Limitations

See [onelake-security-reference.md](./references/onelake-security-reference.md) for complete details.

Key limits to remember: maximum 250 roles per lakehouse, 500 members per role, 500 permissions per role. Mixed-mode queries accessing both OneLake-security-enabled and non-enabled data will fail. OneLake security does not work with private link protection or Azure/Purview Data Share.

## Available Scripts

Run the [SQL permissions audit](./scripts/Audit-SqlEndpointPermissions.ps1) to enumerate explicit grants on a SQL analytics endpoint.

Run the [access control checklist](./scripts/Test-LakehouseAccessControl.ps1) to validate a user's effective permissions across all security layers.

Use the [RLS validation template](./templates/Validate-RowLevelSecurity.sql) as a starting point for testing row-level security predicates.

## References

- [Diagnostic Workflow](./references/workflow-diagnostics.md) — Step-by-step remediate procedure
- [OneLake Security Reference](./references/onelake-security-reference.md) — Data access roles, limitations, propagation latency, and best practices
- [SQL Endpoint Security Reference](./references/sql-endpoint-security-reference.md) — T-SQL granular permissions, RLS, CLS, OLS, dynamic data masking
- [Direct Lake Security Integration](./references/direct-lake-security-reference.md) — Permission models, OLS/RLS interaction, remediate matrix
- [Microsoft Learn: OneLake Security Overview](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security)
- [Microsoft Learn: SQL Granular Permissions](https://learn.microsoft.com/en-us/fabric/data-warehouse/sql-granular-permissions)
- [Microsoft Learn: Best Practices for OneLake Security](https://learn.microsoft.com/en-us/fabric/onelake/security/best-practices-secure-data-in-onelake)
