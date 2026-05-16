---
name: implement
description: Implement one tracked issue.
practices:
- tdd
- refactoring
- code-complete
hexagonal_role: driving-adapter
consumes:
- domain
produces:
- git-changes
context_rel:
- kind: customer-of
  with: domain
skill_api_version: 1
metadata:
  tier: execution
  dependencies:
  - beads
  - standards
context:
  window: isolated
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
output_contract: code changes, test results, bead status update, behavioral spec (optional)
---
# Implement Skill

> **Quick Ref:** Execute single issue end-to-end. Output: code changes + commit + closed issue.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Loop position

Move **4 (TDD per slice)** of the [operating loop](../../docs/architecture/operating-loop.md). Consumes one vertical slice from the [slice validation plan](../../docs/templates/slice-validation.md); produces failing test → passing implementation → refactor-under-green. Discipline: (1) first failing test must fail for the right reason (missing behavior, not syntax); (2) smallest change to flip green; (3) refactor as its own commit. Slices that mix refactor + feature are two slices, not one. Code without a failing test has no contract; the slice is not done.

Execute a single issue from start to finish.

**CLI dependencies:** bd (issue tracking), ao (ratchet gates). Both optional — see `skills/shared/SKILL.md` for fallback table. If bd is unavailable, use the issue description directly and track progress via TaskList instead of beads.

## When to use

- Use `/implement <issue-id>` to implement a specific tracked issue.
- Use `/implement` (no argument) to pick up next ready work via `bd ready`.
- Use `/implement <description>` to implement an ad-hoc task without a tracked issue.

## Examples

### Implement Specific Issue

**User says:** `/implement ag-5k2`

**What happens:**
1. Agent reads issue from beads: "Add JWT token validation middleware"
2. Explore agent finds relevant auth code and middleware patterns
3. Agent edits `middleware/auth.go` to add token validation
4. Runs `go test ./middleware/...` — all tests pass
5. Commits with message "Add JWT token validation middleware\n\nImplements: ag-5k2"
6. Closes issue via `bd close ag-5k2 --reason "commit:<sha> files:[middleware/auth.go]"`

**Result:** Issue implemented, verified, committed, and closed. Ratchet recorded.

### Pick Up Next Available Work

**User says:** `/implement`

**What happens:**
1. Agent runs `bd ready` — finds `ag-3b7` (first unblocked issue)
2. Claims issue via `bd update ag-3b7 --status in_progress`
3. Implements and verifies
4. Closes issue

**Result:** Autonomous work pickup and completion from ready queue.

### GREEN Mode (Test-First)

**User says:** `/implement ag-8h3` (invoked by `/crank --test-first`)

**What happens:**
1. Agent receives failing tests (immutable) and contract
2. Reads tests to understand expected behavior
3. Implements ONLY enough to make tests pass
4. Does NOT modify test files
5. Verification: all tests pass with fresh output

**Result:** Minimal implementation driven by tests, no over-engineering.

## Lifecycle Integration Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--no-lifecycle` | off | Skip ALL lifecycle skill auto-invocations (test gen, review, refactor) |
| `--lifecycle=<tier>` | matches complexity | Controls which lifecycle skills fire: `minimal` (test only), `standard` (+review), `full` (+refactor dry-run) |

Lifecycle tier defaults to matching the current complexity level. Explicit `--lifecycle=<tier>` overrides.

## Execution

Read [references/workflow.md](references/workflow.md) when you need the full step-by-step procedure (Steps 0 through 8, including pre-flight gates, TDD discipline, build/security verification, the binary-deployment gate, the verification iron law, commit, close, and ratchet record).

GREEN mode rules live in [references/green-mode.md](references/green-mode.md). The pre-commit autonomous quality loop lives in [references/quality-loop.md](references/quality-loop.md). The behavioral spec format lives in [references/behavioral-spec.md](references/behavioral-spec.md).

## Key Rules

- **TDD by default** - write failing tests before implementing (skip with `--no-tdd`)
- **Lifecycle skills fire automatically** - /test, /review, /refactor run at appropriate steps (disable with `--no-lifecycle`)
- **Explore first** - understand before changing
- **Edit, don't rewrite** - prefer Edit tool over Write tool
- **Follow patterns** - match existing code style
- **Verify changes** - run tests or sanity checks
- **Commit with context** - reference the issue ID
- **Close the issue** - update status when done

## Without Beads

If bd CLI not available:
1. Skip the claim/close status updates
2. Use the description as the task
3. Still commit with descriptive message
4. Report completion to user

## Output Specification

Per the `output_contract` in frontmatter: code changes, test results, bead status update, and behavioral spec (optional).

## Completion Markers

```
<promise>DONE</promise>
```

If blocked or incomplete:
```
<promise>BLOCKED</promise>
Reason: <why blocked>
```

```
<promise>PARTIAL</promise>
Remaining: <what's left>
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Issue not found | Issue ID doesn't exist or local state looks stale | Run `bd show <id>` to verify; use `bd vc status` only if you need Dolt state |
| GREEN mode violation | Edited a file not related to the issue scope | Revert unrelated changes. GREEN mode restricts edits to files relevant to the issue |
| Verification gate fails | Tests fail or build breaks after implementation | Read the verification output, fix the specific failures, re-run verification |
| "BLOCKED" status | Contract contradicts tests or is incomplete in GREEN mode | Write BLOCKED with specific reason, do NOT modify tests |
| Fresh verification missing | Agent claims success without running verification command | MUST run verification command fresh with full output before claiming completion |
| Ratchet record failed | ao CLI unavailable or chain.jsonl corrupted | Implementation still closes via bd, but ratchet chain needs manual repair |

## Reference Documents

- [references/behavioral-spec.md](references/behavioral-spec.md) — Behavioral spec format for Stage 4 validation
- [references/binary-deployment-gate.md](references/binary-deployment-gate.md) — CLI/hook binary-deployment gate spec
- [references/gate-checks.md](references/gate-checks.md) — Ratchet and pre-mortem gate checks
- [references/green-mode.md](references/green-mode.md) — GREEN mode test-first implementation rules
- [references/quality-loop.md](references/quality-loop.md) — Pre-commit autonomous quality loop
- [references/resume-protocol.md](references/resume-protocol.md) — Resume protocol for interrupted sessions
- [references/workflow.md](references/workflow.md) — Full execution workflow (Steps 0 through 8)

## See also

- [test](../test/SKILL.md) — Test generation, coverage analysis, and TDD workflow
