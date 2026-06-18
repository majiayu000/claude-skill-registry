---
name: forge-security-review
description: >
  Performs a white-box security review of Atlassian Forge apps using structured, Forge-specific
  security rules and evidence-driven reporting. Use when the user asks for a Forge security
  review, security audit, vuln assessment, pentest-style code review, authz review, tenant
  isolation analysis, web trigger hardening, or static analysis execution for a Forge app.
license: Apache-2.0
labels:
  - forge
  - security
  - review
  - audit
  - atlassian
maintainer: atlassian-developer
namespace: cloud
---

# Forge Security Review

Runs a Forge-focused white-box security review and reports validated findings with exploitability, impact, evidence, and remediation guidance.

## Token-Efficient Default

Use manifest-driven routing by default to reduce token usage. Do not load every rule file up front.

## Rule Assets

The review rules are packaged with this skill under `assets/security-rules/`:

- Global baseline: `assets/security-rules/_global-forge.mdc`
- Category indexes: `assets/security-rules/forge-*/_index-*.mdc`
- Category deep checks: `assets/security-rules/forge-*/*.mdc`

## Execution Mandate

When this skill is triggered:

1. Run static analysis first from this skill directory:
  - `scripts/run_static_analysis.sh <forge-project-root-directory>`
  - use `.ps1` script for windows
2. Read `manifest.yml` first before any deep code review.
3. Load `assets/security-rules/_global-forge.mdc` first.
4. Load only relevant category index rules based on manifest and code signals.
5. Load deep subrules only when the matching detection heuristics are triggered by real code patterns.
6. Perform an evidence-based security review across:
   - AuthN/AuthZ
   - Injection and input validation
   - Tenant isolation and cross-tenant leakage
   - Secrets and storage
   - Egress/remotes/CSP and manifest permissions
   - Public entry points (web triggers)
   - Agent and miscellaneous Forge security risks
7. Do not modify app code unless the user explicitly requests fixes.
8. Write all scan outputs and generated artifacts to `security-audit-artifacts/`.

## Rule Routing Workflow

### Phase 1: Reconnaissance (Mandatory)

Read `manifest.yml` first and extract:

- `permissions.scopes`
- `permissions.external.fetch`
- `permissions.content.scripts`
- `modules` (resolver/webtrigger/scheduledTrigger/rovo/etc.)
- `remotes`
- `app.runtime.name`

Build an execution map:

- UI modules -> bridge calls -> resolvers/functions
- External entry points (web triggers, events, schedules)
- `api.asUser()` vs `api.asApp()` paths
- Outbound fetch destinations

### Phase 2: Index Rule Selection (Two-Tier Loading)

Always load first:

- `assets/security-rules/_global-forge.mdc`

Then load only relevant category index rules:

| Signal                                                    | Load                                                                                   |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Any meaningful scope usage, mutations, or `asApp()` usage | `assets/security-rules/forge-authn-authz/_index-authn-authz.mdc`                       |
| `webtrigger` or `scheduledTrigger` modules                | `assets/security-rules/forge-webtrigger-entrypoints/_index-webtrigger-entrypoints.mdc` |
| `permissions.external.fetch` or `remotes`                 | `assets/security-rules/forge-egress-remotes/_index-egress-remotes.mdc`                 |
| SQL APIs or untrusted input reaching resolver sinks       | `assets/security-rules/forge-injection/_index-injection.mdc`                           |
| Multi-tenant patterns, module/global state, cache reuse   | `assets/security-rules/forge-tenant-isolation/_index-tenant-isolation.mdc`             |
| Credentials/tokens/secrets handling                       | `assets/security-rules/forge-secrets-storage/_index-secrets-storage.mdc`               |
| Unsafe CSP or likely scope/config misconfiguration        | `assets/security-rules/forge-manifest-config/_index-manifest-config.mdc`               |
| Rovo modules/actions                                      | `assets/security-rules/forge-rovo-agents/_index-rovo-agents.mdc`                       |
| Baseline logging/error/static analysis concerns           | `assets/security-rules/forge-auditing/_index-auditing.mdc`                             |
| Dependency/package risk review                            | `assets/security-rules/forge-misc/_index-misc.mdc`                                     |

Subrule policy:

- After reading an index, load only the subrules that match the detection heuristics observed in code.
- Do not pre-load every subrule in a category.

### Phase 3: Analysis and Verification

For each loaded category:

1. Enumerate reachable entry points.
2. Trace source -> validation/authz -> sink.
3. Confirm exploitability with evidence.
4. Score confirmed findings with CVSS v3.1.

## Focused Review Mode

If the user asks for a narrow review (for example, only authz), load:

- Global baseline
- Requested category index
- Only matching subrules in that category

Still mention any obvious critical findings observed outside scope.

## Review Workflow

1. Build an execution map:
   - UI Kit/Custom UI entry points
   - Bridge invocations and resolver handlers
   - `api.asUser()` / `api.asApp()` call paths
   - External egress/remotes and trigger entry points
2. For each finding, trace source -> validation/authz -> sink.
3. Validate exploitability before classifying as a confirmed vulnerability.
4. Keep non-exploitable hardening observations in a separate "needs validation" section.
5. Provide file-level evidence and practical test leads for each issue.

## Static Analysis Mode

If the user asks for a full scan, run the complete workflow from:

- `assets/security-rules/forge-auditing/static-analysis-forge.mdc`

Expected tools (when available): Semgrep, npm audit, Snyk, gitleaks.

## Output Requirements

- Provide a markdown security audit report.
- Order confirmed exploitable findings by CVSS v3.1 severity and impact.
- Include for each confirmed finding:
  - CVSS vector and base score
  - Severity band
  - Exploitability and impact
  - File evidence and source-to-sink trace
  - CWE mapping
  - Reproducible PoC/test steps with concrete commands
- Include assumptions and evidence gaps.
- Do not report scanner counts only when vulnerabilities exist.

## Example Trigger Phrases

- "Review this Forge app for security"
- "Do a white-box security audit of my Forge app"
- "Check this app for authz bypass and tenant isolation issues"
- "Run full static analysis for this Forge codebase"
