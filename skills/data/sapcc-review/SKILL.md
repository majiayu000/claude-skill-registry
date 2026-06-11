---
name: sapcc-review
description: "Gold-standard SAP CC Go code review: 10 parallel domain specialists."
user-invocable: false
argument-hint: "[--fix]"
command: /sapcc-review
agent: golang-general-engineer
allowed-tools:
  - Agent
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - TaskCreate
  - TaskUpdate
  - TaskList
  - EnterWorktree
routing:
  triggers:
    - sapcc review
    - sapcc lead review
    - sapcc compliance review
    - comprehensive sapcc audit
    - full sapcc check
    - review sapcc standards
  pairs_with:
    - golang-general-engineer
    - go-patterns
    - sapcc-audit
  force_route: false
  complexity: Complex
  category: language
---

# SAPCC Comprehensive Code Review v1

10-agent domain-specialist review. Each agent masters one rule domain and scans every package for violations against the comprehensive patterns reference.

**How this differs from /sapcc-audit**: sapcc-audit segments by *package* (generalist per package). sapcc-review segments by *rule domain* (specialist per concern, cross-package). Both are useful; this one catches more because specialists find issues generalists miss.

---

## Overview

This skill executes a gold-standard code review against SAP Converged Cloud Go repository standards through parallel domain specialists. Rather than one generalist reviewing one package, ten specialists review all packages for their specific domain (error handling, testing, types, HTTP APIs, etc.). This catches systemic patterns that package-level reviews miss.

Each specialist loads only its domain-specific reference file to keep context tight and focus deep. Findings are code-level (actual rejected/correct examples, never abstract suggestions) and cite specific sections from sapcc-code-patterns.md.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Phase 2 DISPATCH: the 10 domain-specialist prompts | `agent-dispatch-prompts.md` | Loads detailed guidance from `agent-dispatch-prompts.md`. |
| Phase 3 AGGREGATE: report structure and severity boosts | `report-template.md` | Loads detailed guidance from `report-template.md`. |

## Instructions

### Phase 1: DISCOVER

**Goal**: Map the repository, verify it's an sapcc project, plan the review.

**Step 1: Verify sapcc project**

```bash
cat go.mod | head -5
grep -c "sapcc" go.mod
```

If the module path doesn't contain "sapcc" AND go.mod doesn't import any sapcc packages, warn the user but continue (they may want to check a non-sapcc repo against the project's standards).

**Step 2: Map all Go packages and files**

```bash
# Count .go files (excluding vendor)
find . -name "*.go" -not -path "*/vendor/*" | wc -l

# List packages with file counts
find . -name "*.go" -not -path "*/vendor/*" | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn

# Check for test files separately
find . -name "*_test.go" -not -path "*/vendor/*" | wc -l
```

**Step 3: Check for key imports** (determines which rules are most relevant)

```bash
grep -r "go-bits" go.mod               # Uses go-bits?
grep -r "go-api-declarations" go.mod   # Uses API declarations?
grep -r "gophercloud" go.mod           # Uses OpenStack?
grep -r "gorilla/mux" go.mod           # HTTP routing?
grep -r "database/sql" go.mod          # Database?
```

**Step 4: Create task_plan.md**

```markdown
# Task Plan: SAPCC Review — [repo name]

## Goal
Comprehensive code review of [repo] against project standards, dispatching 10 domain-specialist agents.

## Phases
- [x] Phase 1: Discover repo structure
- [ ] Phase 2: Dispatch 10 specialist agents
- [ ] Phase 3: Aggregate findings
- [ ] Phase 4: Write report

## Repo Profile
- Module: [module path]
- Packages: [N]
- Go files: [M] (excluding vendor)
- Test files: [T]
- Key imports: [list]

## Status
**Currently in Phase 2** - Dispatching agents
```

**Gate**: Repo mapped, plan created. Proceed to Phase 2.

---

### Phase 2: DISPATCH

**Goal**: Launch 10 domain-specialist agents in a SINGLE message for true parallel execution.

**CRITICAL**: All 10 agents must be dispatched in ONE message using the Agent tool. Dispatch them in one message. Parallel domain specialists work independently on disjoint concerns, so a single dispatch keeps the review moving.

Each agent receives:
1. The path to sapcc-code-patterns.md to read
2. Their assigned sections to focus on
3. Their domain-specific reference file (loaded to avoid context dilution; each agent reads ONLY what it needs because loading all references into every agent wastes context and dilutes focus)
4. Instructions to scan ALL .go files in the repo
5. The exact output format for findings

See `references/agent-dispatch-prompts.md` for the shared preamble and all 10 agent specifications (Agents 1-10).

**Gate**: All 10 agents dispatched in single message. Wait for all to complete. Proceed to Phase 3.

---

### Phase 3: AGGREGATE

**Goal**: Compile all agent findings into a single prioritized report.

**Step 0: Full file inventory**

Run `git status --short` (not just `git diff --stat`) to capture both modified AND untracked (new) files. This ensures new files created during the review session are not missed in the report.

**Step 1: Collect all findings**

Read each agent's output. Extract all findings with their severity, file, rule, and code.

**Step 2: Deduplicate**

If two agents flagged the same file:line, keep the higher-severity finding with the more specific rule citation.

**Step 3: Prioritize**

Apply cross-repository reinforcement from §35. See `references/report-template.md` for the severity boost table.

**Step 4: Identify Quick Wins**

Mark findings that are:
- Single-line changes (regex replace, import reorder)
- No behavioral change (pure style/naming)
- Low risk of breaking tests

These go in a "Quick Wins" section at the top of the report.

**Step 5: Write report**

Create `sapcc-review-report.md` using the full template in `references/report-template.md`.

**Gate**: Report written. Display summary to user. Proceed to Phase 4 if `--fix` specified.

---

### Phase 4: FIX (Optional — only with `--fix` flag)

**Goal**: Apply fixes on an isolated branch.

**Step 1: Create worktree**

Use `EnterWorktree` to create an isolated copy. Name it `sapcc-review-fixes`.

**Step 2: Apply Quick Wins first**

Start with Quick Wins (lowest risk). After each group of fixes:

```bash
go build ./...    # Must still compile
go vet ./...      # Must pass vet
make check 2>/dev/null || go test ./...  # Must pass tests
```

**Step 3: Apply Critical and High fixes**

Apply in order. Run tests between each fix. If a fix breaks tests, revert it and note in the report.

**Step 4: Create commit**

```bash
git add -A
git commit -m "fix: apply sapcc-review findings (N fixes across M files)"
```

**Step 5: Report results**

Update `sapcc-review-report.md` with:
- Which findings were fixed
- Which findings were skipped (and why)
- Test results after fixes

---

## Error Handling

**When an agent fails or produces empty findings**:
1. Verify the repo has Go files (some repos may be non-Go or already pass review completely)
2. Check agent logs for permission errors or gopls MCP connection failures
3. If agent timed out, increase timeout or split the 10 agents into two waves of 5
4. If agent reports "no findings", it has completed successfully — that domain is clean

**When a finding looks wrong** (e.g., false positive):
- Cross-check with sapcc-code-patterns.md section cited in the finding
- If it contradicts the reference, note the discrepancy and file in toolkit issue
- If it applies to pre-existing code older than the rule's introduction, mark as LOW and note in systemic recommendations

**When `--fix` breaks tests**:
1. Revert the failed fix
2. Note in report that this finding needs manual review
3. Document the test failure reason so the maintainer understands the blocker
4. Continue with next fix rather than stopping the whole process

---

## References

- **sapcc-code-patterns.md** — Comprehensive 36-section reference (single source of truth for all review rules)
- **Per-agent reference files** (loaded during dispatch):
  - Agent 1: `review-standards-lead.md`
  - Agent 2: `architecture-patterns.md`
  - Agent 3: `api-design-detailed.md`
  - Agent 4: `error-handling-detailed.md`
  - Agent 5: (none — rules inline in §7 + §27)
  - Agent 6: `testing-patterns-detailed.md`
  - Agent 7: `architecture-patterns.md`
  - Agent 8: (none — rules inline in §14, §15, §29)
  - Agent 9: (none — rules inline in §16-18, §20)
  - Agent 10: `preferred-patterns.md`
- **Optional deep-dive references** (load only when findings need calibration):
  - `pr-mining-insights.md` — Review severity calibration across projects
  - `library-reference.md` — Approved/forbidden dependency table
- **Progressive disclosure references** (loaded on demand):
  - `references/agent-dispatch-prompts.md` — Shared preamble + all 10 agent specifications
  - `references/report-template.md` — Full report template + severity boost table

**Integration notes**:
- Complements `/sapcc-audit` (package-level generalist) — use both for maximum coverage
- Prerequisite: go-patterns skill must be installed at `~/.claude/skills/engineering/go-patterns/`
- Sync: After creating, run `cp -r skills/engineering/sapcc-review ~/.claude/skills/sapcc-review` for global access
- Router: `/do` routes via "sapcc review", "sapcc lead review", "comprehensive sapcc audit"
