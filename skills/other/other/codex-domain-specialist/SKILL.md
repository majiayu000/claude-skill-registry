---
name: codex-domain-specialist
description: Apply layered domain routing for frontend, backend, mobile, debugging, security, and specialized engineering concerns. Use to select focused reference files with strict context boundaries before implementation or review.
load_priority: on-demand
---

## TL;DR
Detect primary domain from file signals -> load matching references from routing table -> enforce max 4 references first pass. Check `.codex/profile.yaml` for fast-path. Check feedback logs for supplemental loading. Never bulk-load all references.

# Domain Specialist

## Activation

1. Activate when the task edits domain-specific files.
2. Activate on explicit `$codex-domain-specialist`.

## Project Profile (Fast Path)

Before running detection, check for `.codex/profile.yaml` in the project root.
If the file exists:
1. Parse `primary_domain` and map to the routing decision table directly.
2. Use `stack` entries as supplemental signals for "Load On Signal" column.
3. Skip file-extension-based detection entirely.
If the file does not exist or fails to parse:
- Fall back to the standard Detection and Routing Order below.
See: `references/project-profile-spec.md` for schema and validation rules.

## Feedback-Aware Supplemental Loading

After determining the primary domain (via profile or detection), check for recurring feedback patterns:
1. Scan `.codex/feedback/*.md` files from the last 30 days.
2. Count feedback entries by `Category` field (e.g., "database", "security", "performance").
3. If any category has 3+ entries in 30 days AND that category maps to a domain reference:
   - Auto-load that domain's reference as supplemental context.
   - Declare: `Feedback-driven load: [reference file] (N issues in 30 days)`.
4. Maximum 1 supplemental reference from feedback (highest count wins).
5. If no feedback files exist or all counts < 3, skip this step silently.

### Category to Reference Mapping

| Feedback Category | Supplemental Reference |
| --- | --- |
| database | `references/database-rules.md` |
| security | `references/security-rules.md` |
| performance | `references/performance-rules.md` |
| accessibility | `references/accessibility-rules.md` |
| testing | `references/testing-rules.md` |
| frontend | `references/frontend-rules.md` |
| backend | `references/backend-rules.md` |
| api | `references/api-design-rules.md` |

## Detection and Routing Order

Route in this exact order:

1. Detect primary domain.
2. Load primary domain references from the decision table.
3. Add only signal-driven references.
4. Enforce context boundaries before implementation or review.

## Primary Domain Detection

| Signal | Primary Domain |
| --- | --- |
| `.tsx`, `.jsx`, hooks, component, styling, UI state | React/Frontend |
| Next.js app router, server components, ISR/SSR/SSG | Next.js |
| `routes/`, `controllers/`, `services/`, `api/`, middleware | Backend API |
| schema, migration, query plan, index, transaction | Database |
| React Native, Flutter, Expo, `.swift`, `.kt` | Mobile |
| auth, secrets, crypto, authz, attack surface, vulnerability | Security |
| unit/integration/e2e, flaky test, regression coverage | Testing |
| Docker, CI/CD, deploy, rollback, observability | DevOps |

## Context Boundary Enforcement

1. Max context load: load at most 4 reference files in the first pass. If more are needed, state clear reason and list additional files explicitly.
2. Domain isolation:
   - Frontend-only tasks (component, styling, hooks): do not load `backend-rules.md`, `database-rules.md`, or `devops-rules.md`.
   - Backend-only tasks (API, service, middleware): do not load `react-patterns.md`, `nextjs-patterns.md`, or `accessibility-rules.md`.
   - Database-only tasks (schema, migration, query): do not load `frontend-rules.md`, `mobile-rules.md`, or `seo-rules.md`.
3. Cross-domain trigger:
   - API contract change: load both `api-design-rules.md` and `backend-rules.md`.
   - Security concern detected: load `security-rules.md` regardless of primary domain.
   - Performance issue detected: load `performance-rules.md` as supplemental context.
4. Explicit declaration: whenever references are loaded, always declare:
   - `Loading: [file1], [file2]`
   - `Skipping: [reason]`

## Routing Decision Table

| Primary Domain | Always Load | Load On Signal | Never Load |
| --- | --- | --- | --- |
| React/Frontend | `frontend-rules.md`, `react-patterns.md` | `typescript-rules.md`, `performance-rules.md`, `accessibility-rules.md` | `database-rules.md`, `devops-rules.md` |
| Next.js | `frontend-rules.md`, `nextjs-patterns.md` | `react-patterns.md`, `seo-rules.md`, `performance-rules.md` | `database-rules.md`, `mobile-rules.md` |
| Backend API | `backend-rules.md`, `api-design-rules.md` | `database-rules.md`, `security-rules.md`, `testing-rules.md` | `react-patterns.md`, `nextjs-patterns.md`, `seo-rules.md` |
| Database | `database-rules.md` | `backend-rules.md`, `performance-rules.md`, `testing-rules.md` | `frontend-rules.md`, `react-patterns.md`, `mobile-rules.md`, `seo-rules.md` |
| Mobile | `mobile-rules.md` | `frontend-rules.md`, `performance-rules.md`, `accessibility-rules.md` | `nextjs-patterns.md`, `seo-rules.md`, `database-rules.md` |
| Security | `security-rules.md` | `backend-rules.md`, `api-design-rules.md`, `devops-rules.md` | `react-patterns.md`, `seo-rules.md`, `mobile-rules.md` |
| Testing | `testing-rules.md` | domain-specific rules matching code under test | unrelated domain rules |
| DevOps | `devops-rules.md` | `backend-rules.md`, `security-rules.md`, `performance-rules.md` | `react-patterns.md`, `mobile-rules.md`, `seo-rules.md` |

## Specialized Signal Routing

| Signal | Add Reference |
| --- | --- |
| generics, unions, strict typing, DTO mismatch | `references/typescript-rules.md` |
| pagination, versioning, idempotency, error envelope | `references/api-design-rules.md` |
| profiling, rerender storm, p95 latency, memory hotspot | `references/performance-rules.md` |
| keyboard/focus/screen reader/WCAG | `references/accessibility-rules.md` |
| canonical/sitemap/metadata/structured data | `references/seo-rules.md` |
| flaky tests, mock strategy, regression gaps | `references/testing-rules.md` |

## Operating Rules

1. Never bulk-load all references.
2. Keep first-pass load minimal and task-specific.
3. Re-check boundaries after each major step and prune irrelevant references.
4. If user task spans multiple domains, justify each added reference in the declaration.

## Script Invocation Discipline

1. When domain routing recommends helper scripts from other skills, run `--help` first.
2. Treat scripts as black-box helpers and execute by CLI contract before source inspection.
3. Read script source only when customization or bug fixing is required.

## Reference Files

- `references/project-profile-spec.md`: project profile schema and fast-path routing.
