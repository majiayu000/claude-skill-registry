---
name: traceability
activation_code: TRACEABILITY_V1
phase: any
command: /trace
aliases: ["/traceability", "/req"]
description: Manage requirement traceability - generate matrix, check coverage, find orphans, trace requirements
tier: focused
model: sonnet
invokes: traceability-auditor
---

# Traceability Skill

## Usage

```
/trace                      - Show traceability dashboard
/trace generate             - Scan artifacts and generate traceability matrix
/trace coverage             - Report traceability coverage metrics
/trace orphans              - Find artifacts without proper traces
/trace REQ-xxx-nnn          - Show full trace chain for a requirement
/trace impact REQ-xxx-nnn   - Show what would be affected if requirement changes
/trace validate             - Verify all trace links are valid
/trace suggest              - Auto-suggest traces for orphan artifacts
```

## Commands

### `/trace` (Dashboard)

Shows the current traceability health:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  TRACEABILITY DASHBOARD                                               ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Matrix Last Updated: 2024-01-15 10:30:00                             ║
║                                                                        ║
║  ARTIFACTS                                                             ║
║  ├── Requirements: 25                                                  ║
║  ├── User Stories: 23                                                  ║
║  ├── Tasks: 18                                                         ║
║  ├── Specifications: 15                                                ║
║  ├── Tests: 50                                                         ║
║  └── Implementations: 48                                               ║
║                                                                        ║
║  COVERAGE                                                              ║
║  ├── Forward (Req → Code): 92%  ✓                                     ║
║  ├── Backward (Code → Req): 73%  ⚠                                    ║
║  └── Test Coverage: 84%  ✓                                            ║
║                                                                        ║
║  ORPHANS: 8 artifacts need attention                                  ║
║                                                                        ║
║  HEALTH SCORE: 82/100                                                 ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [G] Generate  [C] Coverage  [O] Orphans  [V] Validate                ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### `/trace generate`

Scans all artifacts and generates the traceability matrix:

1. Scans PRD for REQ-IDs
2. Scans PRD/docs for User Stories (US-NNN)
3. Scans .taskmaster/tasks/tasks.json for tasks
4. Scans openspec/changes/*.md for specifications
5. Scans tests/**/*.{ts,js,py} for @traces annotations
6. Scans src/**/*.{ts,js,py} for @implements annotations
7. Generates `.claude/traceability/matrix.json`

### `/trace coverage`

Reports detailed coverage metrics with drill-down:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  TRACEABILITY COVERAGE REPORT                                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  FORWARD TRACEABILITY                                                  ║
║  ├── REQ → US:     23/25 (92%)  ███████████░ ✓                        ║
║  ├── US → TASK:    18/23 (78%)  ████████░░░░ ⚠                        ║
║  ├── TASK → SPEC:  15/18 (83%)  █████████░░░ ✓                        ║
║  └── SPEC → CODE:  14/15 (93%)  ███████████░ ✓                        ║
║                                                                        ║
║  BACKWARD TRACEABILITY                                                 ║
║  ├── TEST → REQ:   42/50 (84%)  █████████░░░ ✓                        ║
║  └── CODE → REQ:   35/48 (73%)  ████████░░░░ ⚠                        ║
║                                                                        ║
║  GAPS:                                                                 ║
║  ├── REQ-PERF-003: No user stories                                    ║
║  ├── REQ-SEC-007: No implementation                                   ║
║  └── US-015, US-018, US-021, US-022, US-023: No tasks                 ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### `/trace orphans`

Lists all artifacts without proper traces:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  ORPHAN ARTIFACTS                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  CRITICAL (Requirements with no path to implementation):              ║
║  ├── REQ-PERF-003: Response time < 100ms                              ║
║  └── REQ-SEC-007: Audit logging                                       ║
║                                                                        ║
║  WARNING (Code/tests without requirement link):                       ║
║  ├── tests/unit/utils/helpers.test.ts                                 ║
║  ├── tests/unit/api/legacy.test.ts                                    ║
║  ├── src/utils/deprecated.ts                                          ║
║  └── src/api/v1/compat.ts                                             ║
║                                                                        ║
║  MEDIUM (Tasks without requirement):                                  ║
║  └── TASK-042: Refactor database connection                          ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [S] Suggest traces  [M] Mark intentional  [I] Ignore                 ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### `/trace REQ-xxx-nnn`

Shows the complete trace chain for a single requirement:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  TRACE: REQ-AUTH-001                                                  ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  REQ-AUTH-001: User authentication via email/password                 ║
║  Priority: P0 | Source: docs/PRD.md:142                               ║
║                                                                        ║
║  ┌─► US-001: User can log in                                          ║
║  │   ├─► TASK-003: Implement login API                                ║
║  │   │   ├─► SPEC-003-01: Login endpoint spec                         ║
║  │   │   │   └─► src/api/auth/login.ts                                ║
║  │   │   └─► TEST-UNIT-015: tests/unit/auth/login.test.ts            ║
║  │   └─► TASK-004: Implement password validation                      ║
║  │       ├─► SPEC-004-01: Password rules spec                         ║
║  │       │   └─► src/services/auth.ts                                 ║
║  │       └─► TEST-UNIT-016: tests/unit/auth/password.test.ts         ║
║  │                                                                    ║
║  └─► US-002: User receives error on invalid credentials               ║
║      └─► TASK-003: (shared)                                           ║
║                                                                        ║
║  Coverage: FULL ✓ (all paths traced to code and tests)               ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### `/trace impact REQ-xxx-nnn`

Shows impact analysis for requirement changes:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  IMPACT ANALYSIS: REQ-AUTH-001                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  If this requirement changes:                                          ║
║                                                                        ║
║  ARTIFACTS AFFECTED:                                                   ║
║  ├── 2 User Stories                                                   ║
║  ├── 3 Tasks                                                          ║
║  ├── 2 Specifications                                                 ║
║  ├── 3 Code files                                                     ║
║  └── 4 Test files                                                     ║
║                                                                        ║
║  ESTIMATED REWORK:                                                     ║
║  ├── Complexity: HIGH                                                  ║
║  ├── Files to modify: 9                                               ║
║  └── Tests to update: 4                                               ║
║                                                                        ║
║  DOWNSTREAM DEPENDENCIES:                                              ║
║  └── REQ-SEC-002 (Session management) depends on this                 ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [F] Show full artifact list  [D] Show dependency graph               ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### `/trace validate`

Validates all trace links exist and are consistent:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  TRACE VALIDATION                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  BROKEN LINKS (referenced artifact doesn't exist):                    ║
║  ├── TASK-007 references REQ-DATA-099 (not found)                    ║
║  └── TEST-UNIT-042 references US-099 (not found)                     ║
║                                                                        ║
║  INCONSISTENT LINKS (bidirectional mismatch):                         ║
║  └── US-015 links to TASK-012, but TASK-012 doesn't link back        ║
║                                                                        ║
║  DUPLICATE IDS:                                                        ║
║  └── None found ✓                                                     ║
║                                                                        ║
║  VALIDATION: 3 issues found                                           ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### `/trace suggest`

Auto-suggests traces for orphan artifacts:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  TRACE SUGGESTIONS                                                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  tests/unit/auth/session.test.ts                                      ║
║  Currently orphan (no @traces annotation)                             ║
║                                                                        ║
║  Suggested traces (by content similarity):                            ║
║  ├── REQ-AUTH-002 (85%) - Session management                         ║
║  ├── US-004 (78%) - User session handling                            ║
║  └── TASK-008 (72%) - Implement session storage                       ║
║                                                                        ║
║  Recommended annotation:                                               ║
║  /**                                                                   ║
║   * @traces REQ-AUTH-002, US-004, TASK-008                            ║
║   */                                                                   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [A] Apply suggestion  [S] Skip  [M] Manual entry                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Integration

### With Audit Orchestrator

The traceability-auditor is invoked as part of audit dimension F01 (Requirements Coverage).

### With Phase Gates

- **Phase 5**: Verify all requirements have tasks
- **Phase 6**: Verify all tasks have specifications
- **Phase 8**: Verify all tests have traces
- **Phase 10**: Verify full forward/backward traceability

### With Plan Guardian

When Plan Guardian detects drift, it can use traceability to identify which requirements are affected.

## Files

| File | Purpose |
|------|---------|
| `.claude/traceability/matrix.json` | Generated traceability matrix |
| `templates/requirement-traceability.schema.yaml` | Schema reference |
