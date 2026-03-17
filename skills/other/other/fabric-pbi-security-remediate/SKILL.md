---
name: fabric-pbi-security-remediate
description: Diagnose and resolve Microsoft Fabric Power BI security issues including row-level security (RLS), object-level security (OLS), column-level security (CLS), workspace permissions, sensitivity labels, service principal authentication, XMLA endpoint access, DirectLake security fallback, Entra ID app registration, and data loss prevention (DLP) policy restrictions. Use when remediate access denied errors, missing data in reports, broken visuals from OLS, RLS not filtering, sensitivity label problems, permission model conflicts, or capacity-related security issues.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric Power BI Security remediate

Systematic diagnostic toolkit for resolving security and access control issues across the Microsoft Fabric Power BI stack. Covers workspace permissions, data-level security (RLS/OLS/CLS), sensitivity labels, service principal access, and governance policy restrictions.

## When to Use This Skill

- User reports "access denied" or "unauthorized" errors in Power BI reports or workspaces
- Report visuals show blank data or "field cannot be found" errors
- RLS filters are not applying correctly or returning unexpected data
- Sensitivity labels are greyed out, blocking exports, or preventing publishing
- Service principal cannot access workspaces or semantic models
- DirectLake reports fall back to DirectQuery unexpectedly due to security
- DLP or Purview protection policies are blocking item access
- Workspace role assignments are not behaving as expected
- XMLA endpoint connections fail with permission errors
- Users lose access to items after policy or label changes

## Prerequisites

- **PowerShell 7+** with `MicrosoftPowerBIMgmt` module
- **Fabric Admin** or **Workspace Admin** role for diagnostic scripts
- **Power BI REST API** access (interactive or service principal)
- Optional: Tabular Editor for OLS/RLS inspection

Install required modules:

```powershell
Install-Module -Name MicrosoftPowerBIMgmt -Scope CurrentUser -Force
Install-Module -Name Az.Accounts -Scope CurrentUser -Force
```

## Quick Diagnostic Flowchart

```
User reports access issue
    │
    ├─ Can they see the workspace? ─── NO ──► Check workspace role assignment
    │                                          See: Workspace Permissions
    │
    ├─ Can they see the item? ──────── NO ──► Check item-level sharing or
    │                                          Purview/DLP policies
    │                                          See: Governance Policy Restrictions
    │
    ├─ Can they see data in visuals? ─ NO ──► Check RLS role membership
    │                                          and DAX filter expressions
    │                                          See: RLS remediate
    │
    ├─ Do visuals show "field not      YES ─► Check OLS/CLS configuration
    │   found" errors?                         See: OLS/CLS remediate
    │
    ├─ Can they export/download? ───── NO ──► Check sensitivity label encryption
    │                                          and export settings
    │                                          See: Sensitivity Labels
    │
    └─ XMLA or API errors? ────────────────► Check endpoint settings, service
                                               principal permissions, and capacity
                                               See: XMLA & API Access
```

## Step-by-Step Workflows

### 1. Workspace Permission Issues

**Symptoms**: User cannot see workspace or items within it.

1. Verify the user's workspace role:

```powershell
# Run the diagnostic script
./scripts/Get-PBISecurityDiagnostic.ps1 -WorkspaceName "Sales Analytics" -UserEmail "user@contoso.com"
```

2. Understand the permission hierarchy:

| Role | See Items | Use Items | OneLake Access | RLS Enforced? |
|------|-----------|-----------|----------------|---------------|
| Admin | ✅ | ✅ | ✅ | ❌ (bypassed) |
| Member | ✅ | ✅ | ✅ | ❌ (bypassed) |
| Contributor | ✅ | ✅ | ✅ | ❌ (bypassed) |
| Viewer | ✅ | Read-only | ❌ | ✅ (enforced) |

3. Key rule: **RLS only applies to Viewers**. If a user has Admin, Member, or Contributor role, RLS is bypassed entirely.

4. To enforce RLS, ensure content consumers have **only Viewer** workspace role and **only Read** permission on the semantic model.

### 2. Row-Level Security (RLS) Not Filtering

**Symptoms**: Users see all data instead of their filtered subset.

See [RLS remediate Guide](./references/rls-remediate.md) for the full diagnostic workflow.

Quick checks:

1. Confirm user is mapped to the correct RLS role
2. Verify the user has only **Viewer** permissions (Admin/Member/Contributor bypass RLS)
3. Test using "Test as role" in the Power BI service
4. Add a `USERNAME()` DAX measure to a card visual to verify identity
5. Check relationship filter directions — RLS filters only propagate through **active** relationships

### 3. Object-Level Security (OLS) / Column-Level Security (CLS)

**Symptoms**: Visuals display "The field cannot be found" or "may not be used in this expression."

See [OLS/CLS remediate Guide](./references/ols-cls-remediate.md) for the full workflow.

Quick checks:

1. OLS only applies to **Viewers** — same bypass rules as RLS
2. OLS must be configured using Tabular Editor (not natively in Power BI Desktop)
3. OLS and RLS cannot be combined from **different roles** — this causes query-time errors
4. Measures referencing secured columns are automatically restricted
5. Q&A, Quick Insights, and Smart Narrative visuals do not support OLS

### 4. Sensitivity Label Issues

**Symptoms**: Labels greyed out, exports blocked, PBIX files inaccessible.

See [Sensitivity Labels Guide](./references/sensitivity-labels-guide.md) for the full workflow.

Quick checks:

1. Ensure the tenant setting "Allow users to apply sensitivity labels" is enabled
2. User needs Pro or PPU license AND create/edit permissions on the item
3. Protected PBIX files require Full Control or Export usage rights
4. Service principals **cannot** publish protected PBIX files — remove label first
5. B2B and multi-tenant scenarios are not supported with sensitivity labels

### 5. DirectLake Security Fallback

**Symptoms**: DirectLake reports unexpectedly run in DirectQuery mode.

- If RLS is defined in the **SQL analytics endpoint**, DirectLake falls back to DirectQuery for those tables
- To avoid fallback: define RLS in the semantic model only, not in SQL
- For app-based distribution without fallback, switch from SSO to a **fixed identity** credential
- Create a new Lakehouse with shortcuts to avoid inheriting SQL-level security

### 6. Service Principal & XMLA Access

**Symptoms**: API calls return 401/403, XMLA connections fail.

See [XMLA & API Access Guide](./references/xmla-api-access.md) for the full workflow.

Quick checks:

1. Verify tenant setting: "Allow service principals to use Fabric APIs" is enabled
2. Add the service principal to a security group referenced in the tenant setting
3. Add the service principal to the workspace with the correct role
4. For XMLA: verify "Allow XMLA endpoints" is enabled in tenant Integration settings
5. Impersonation via `EffectiveUserName` requires both Read and Build permissions

### 7. Governance Policy Restrictions

**Symptoms**: User suddenly loses access to items they previously could see.

- Check for Purview **protection policies** that restrict access based on sensitivity labels
- Check for Purview **DLP policies** with "restrict access" actions on sensitive content
- In the item's Manage Permissions page, look for "No access" — indicates policy-level restriction
- Label issuers and item creators retain access even when policies restrict others
- Contact your Microsoft 365 compliance admin to review active policies

## remediate Decision Matrix

| Symptom | Likely Cause | First Action |
|---------|-------------|--------------|
| Can't see workspace | Missing workspace role | Check `Get-PowerBIWorkspace` |
| Blank visuals | RLS misconfiguration | Test as role, check USERNAME() |
| "Field not found" | OLS restriction | Inspect roles in Tabular Editor |
| Can't export PBIX | Sensitivity label encryption | Check usage rights |
| Label greyed out | Missing license or permissions | Verify Pro/PPU + security group |
| API 401/403 | Service principal not authorized | Check tenant settings + workspace role |
| DirectQuery fallback | SQL-level RLS on endpoint | Move RLS to semantic model |
| Sudden access loss | Purview/DLP policy change | Check Manage Permissions for "No access" |

## Available Scripts

Run the [security diagnostic script](./scripts/Get-PBISecurityDiagnostic.ps1) for automated workspace and permission analysis.

Run the [RLS validation script](./scripts/Test-PBIRowLevelSecurity.ps1) to test RLS role membership and filter expressions.

Use the [incident report template](./templates/security-incident-template.md) to document and track security remediate cases.

## References

- [RLS remediate Guide](./references/rls-remediate.md) — Full RLS diagnostic workflow
- [OLS/CLS remediate Guide](./references/ols-cls-remediate.md) — Object and column security
- [Sensitivity Labels Guide](./references/sensitivity-labels-guide.md) — Label configuration and issues
- [XMLA & API Access Guide](./references/xmla-api-access.md) — Service principal and endpoint access
- [Microsoft Learn: Security in Fabric](https://learn.microsoft.com/en-us/fabric/security/security-overview)
- [Microsoft Learn: Permission Model](https://learn.microsoft.com/en-us/fabric/security/permission-model)
- [Microsoft Learn: RLS with Power BI](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security)
- [Microsoft Learn: OLS](https://learn.microsoft.com/en-us/fabric/security/service-admin-object-level-security)
- [Microsoft Learn: Troubleshoot Access Restrictions](https://learn.microsoft.com/en-us/fabric/governance/troubleshoot-restricted-access)
