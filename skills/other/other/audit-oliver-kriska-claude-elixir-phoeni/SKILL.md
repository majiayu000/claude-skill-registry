---
name: phx:audit
description: Project health audit across 5 areas (architecture, performance, security, tests, dependencies) using parallel specialist agents. Use quarterly, before major releases, after large refactors, or when onboarding. Also use when the user mentions "project health", "code quality overview", "how healthy is this codebase", or any request for holistic assessment.
effort: high
argument-hint: [--quick|--full|--focus=area|--since=commit]
---

# Project Health Audit

Comprehensive project-wide health assessment using 5 parallel specialist subagents.

## Usage

```
/phx:audit              # Full audit (default)
/phx:audit --quick      # 2-3 minute pulse check
/phx:audit --focus=security   # Deep dive single area
/phx:audit --focus=performance
/phx:audit --since abc123   # Incremental audit since commit
/phx:audit --since HEAD~10  # Audit last 10 commits
```

## When to Use

- **Quarterly** health checks
- **Before major releases**
- **After large refactors**
- **New team member onboarding** (understand codebase health)

## Iron Laws

1. **Wait for ALL agents before synthesizing** — Partial results create misleading health scores because cross-category correlations get missed
2. **Scope agent prompts to specific directories** — Vague prompts like "analyze the codebase" produce generic findings that waste tokens and miss real issues
3. **Never compare scores across projects** — Scoring methodology depends on project size and maturity; only track trends within the same project
4. **Quick mode before full mode** — Run `--quick` first to catch compile/test failures before spending tokens on 5 parallel agents

## Subagent Architecture

Spawn 5 specialists in parallel using Agent tool:

| Subagent | Focus | Output File |
|----------|-------|-------------|
| Architecture Reviewer | Structure quality, coupling, cohesion | `arch-review.md` |
| Performance Auditor | N+1, indexes, bottlenecks, scalability | `perf-audit.md` |
| Security Auditor | OWASP scan, auth patterns, secrets | `security-audit.md` |
| Test Health Auditor | Coverage, quality, flaky tests | `test-audit.md` |
| Dependency Auditor | Vulnerabilities, outdated, unused | `deps-audit.md` |

## Workflow

### Step 1: Create Task List and Spawn All 5 Auditors (Parallel)

**Create Claude Code tasks** for real-time progress visibility:

```
For each auditor:
  TaskCreate({subject: "{Area} audit", activeForm: "Auditing {area}..."})
  TaskUpdate({taskId, status: "in_progress"})
```

Then spawn all 5 agents with Agent tool (parallel):

```
Agent(subagent_type: "general-purpose", prompt: "Architecture audit...", run_in_background: true)
Agent(subagent_type: "general-purpose", prompt: "Performance audit...", run_in_background: true)
Agent(subagent_type: "general-purpose", prompt: "Security audit...", run_in_background: true)
Agent(subagent_type: "general-purpose", prompt: "Test health audit...", run_in_background: true)
Agent(subagent_type: "general-purpose", prompt: "Dependency audit...", run_in_background: true)
```

**Agent prompts must be FOCUSED.** Scope each prompt to the
relevant directories and patterns. Do NOT give vague prompts
like "analyze the codebase."

**Output efficiency**: Tell each agent: "Report ONLY issues found.
Do NOT list clean checks, passing categories, or 'What's Good'.
One summary line per clean area suffices."

### Step 2: Collect Results

Wait for ALL auditors to complete. Mark each auditor's task as
`completed` via `TaskUpdate` as it finishes. NEVER proceed while
any auditor is still running.

Read reports from `.claude/audit/reports/`.

### Step 3: Compress Findings

After all 5 auditors complete, spawn context-supervisor:

```
Agent(subagent_type: "context-supervisor", prompt: """
Compress audit findings.
Input: .claude/audit/reports/
Output: .claude/audit/summaries/
Priority: Health scores per category, critical findings
only, cross-category correlations, deduplicate findings
found by 2+ agents.
""")
```

Read `.claude/audit/summaries/consolidated.md` for synthesis.

### Step 4: Calculate Health Score

Each category scores 0-100. See `${CLAUDE_SKILL_DIR}/references/scoring-methodology.md`.

### Step 5: Generate Report

Write to `.claude/audit/summaries/project-health-{date}.md`.

## Output Format

Report includes: Executive summary with health score (A-F, numeric/100),
per-category score table (Architecture, Performance, Security, Tests, Dependencies),
critical issues, top recommendations, and action plan (Immediate/Short-term/Long-term).

## Quick Mode (`--quick`)

Only run essential checks (~2-3 minutes):

```bash
mix compile --warnings-as-errors
mix hex.audit && mix deps.audit
mix xref graph --format stats
mix test --trace 2>&1 | tail -20
```

Skip: Full security scan, N+1 analysis, test quality metrics, architecture deep dive.

## Focus Mode (`--focus=area`)

Deep dive single area with full specialist resources:

| Focus | Subagent | Extra Checks |
|-------|----------|--------------|
| `security` | security-analyzer | Full OWASP, sobelow, manual patterns |
| `performance` | (performance subagent) | Profile-level analysis, query explain |
| `architecture` | (arch subagent) | Full xref, coupling matrix, cohesion |
| `tests` | testing-reviewer | Coverage by context, quality metrics |
| `deps` | (deps subagent) | License audit, maintenance status |

## Incremental Mode (`--since <commit>`)

Analyze only changes since a specific commit. Useful for pre-merge checks:

```bash
# Identify changed files
git diff --name-only <commit>...HEAD

# Run targeted audits on changed files only
# Skips full project scan, focuses on modified code
```

Combines with other flags: `/phx:audit --since HEAD~5 --focus=security`

## Relationship to Other Commands

| Command | Scope | Frequency |
|---------|-------|-----------|
| `/phx:review` | Changed files (diff) | Every PR |
| `/phx:audit` | Entire project | Quarterly |
| `/phx:boundaries` | Context structure | On-demand |
| `/phx:verify` | Compile/test pass | Anytime |

## References

- `${CLAUDE_SKILL_DIR}/references/scoring-methodology.md` - How scores are calculated
- `${CLAUDE_SKILL_DIR}/references/architecture-checks.md` - Detailed architecture criteria
