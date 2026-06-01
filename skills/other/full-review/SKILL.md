---
name: full-review
description: >
  · Run combined code-review, anti-slop, security-audit, and update-docs pass. Triggers: 'full review', 'review everything', 'audit this repo', 'full check', 'run all checks'. Not for single-dimension audits.
license: MIT
compatibility: "Requires code-review, anti-slop, security-audit, update-docs skills installed"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-22"
  effort: high
  argument_hint: "[scope]"
---

# Full Review: Quad Audit Orchestrator

Run four independent audits in parallel and present each report separately. One command that catches bugs, slop, security issues, and stale docs across the entire codebase without invoking each skill manually.

The four audits:

1. **Code Review** (`code-review` skill) - bugs, logic errors, edge cases, race conditions, resource leaks, convention violations. Uses confidence-based filtering (>= 80%), adversarial self-check, and evidence-based verification.
2. **Slop Check** (`anti-slop` skill) - machine-generated patterns, over-abstraction, verbose code, stale idioms
3. **Security Audit** (`security-audit` skill) - vulnerabilities, secrets, dependency risks, OWASP mapping
4. **Docs Sweep** (`update-docs` skill) - stale docs, bloated instruction files, missing gotchas, broken links, companion-file drift

Each audit runs in its own parallel agent/subprocess with a fresh context window, so they don't compete for tokens or bias each other's findings.

## When to use

- Running a repo-wide quality gate before merge, release, or handoff
- Auditing an unfamiliar codebase across correctness, security, slop, and docs in one pass
- Getting a broad review when the user explicitly wants multiple audit lenses at once

## When NOT to use

- A targeted correctness review on specific files - use **code-review**
- Style/slop cleanup without the other audit passes - use **anti-slop**
- A dedicated security review only - use **security-audit**
- A documentation-only maintenance sweep - use **update-docs**
- A comprehensive audit across all applicable lenses (up to 29 audit agents, including 20 conditional Wave 3 domain lenses) - use **deep-audit**
- Auditing the skill collection for consistency or quality - use **skill-creator**
- CI/CD pipeline design or pipeline-config review - use **ci-cd**

## AI Self-Check

Run this checklist after all agents return but before presenting the combined report to the user. Do not present results until every item passes.

Verify:

- [ ] All 4 agents dispatched as `general-purpose` type (NOT `feature-dev:*`, `code-simplifier:*`, or other restricted types)
- [ ] Each agent invoked its assigned custom skill (`code-review`, `anti-slop`, `security-audit`, `update-docs`) via the Skill tool
- [ ] Each report presented under its own header, unedited
- [ ] No cross-report merging or editorializing (findings from different audits stay separate)
- [ ] SECURITY-AUDIT.md gitignore reminder included
- [ ] Failed agents noted with reason (don't silently drop a missing audit)
- [ ] Preflight context block was passed to all agents
- [ ] When user specified a scope, the `Scope:` line in every agent's context block reflects that scope (not "full codebase review")
- [ ] Scope held in output: each agent's findings reference only files/modules within the requested scope. If any agent's output references out-of-scope paths, flag it in that report's header (see Step 3 scope verification)
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Routing explicit**: code-review, anti-slop, security-audit, and update-docs findings stay in their lanes
- [ ] **No false coverage**: unrun tests, skipped directories, and unavailable tools are reported

---

## Performance

- Run inventory and changed-file analysis before invoking every review mode.
- Escalate only confirmed high-risk areas to deeper sweeps.


---

## Best Practices

- Lead with actionable findings and severity; keep summaries secondary.
- Separate code bugs, security issues, slop, and docs drift so owners can act.
- Do not claim a full audit if the pass was sampled or tool-limited.


## Workflow

### Step 0: Preflight

Gather context before dispatching agents. Run these in parallel (guard each with `; true` so one failure doesn't cancel siblings):

1. **Repo state**: `git rev-parse --show-toplevel ; true` and `git rev-parse --short HEAD ; true`
2. **Branch**: `git branch --show-current ; true`
3. **Language detection**: check for manifest files (`package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `composer.json`, `Gemfile`, `*.tf`, `helmfile.yaml`)
4. **Repo size estimate**: `git ls-files | wc -l ; true`

**If not a git repo** (step 1 fails): stop and tell the user. The audits rely on git context (history, blame, diff). Running without it produces low-quality results.

Record preflight values - each subagent prompt uses them. Substitute `{placeholders}` in the agent prompts below with the actual values from preflight (e.g., replace `{repo_root}` with the output of `git rev-parse --show-toplevel`). Default `{scope}` to "full codebase review - scan everything"; override in Step 1 if the user specifies a narrower target.

### Step 1: Determine Scope

Default is **full codebase** since the user is running this as a quality gate. Adapt if context suggests otherwise:

- **Uncommitted changes present** -> mention this, but still audit the full repo.
- **Detached HEAD / bare repo** -> warn the user, proceed with what's available.
- **User specified a narrower scope** (specific files, directory, module) -> pass that scope constraint to all four agents. Each agent only audits within the specified scope. This is the key to scoped reviews: narrowing the target, not the audit dimensions. Set `{scope}` in the context block to the user's scope (e.g., "src/auth/ directory only") instead of the default "full codebase review - scan everything".

### Step 2: Dispatch Four Parallel Agents

Spawn all four agents concurrently. Each agent invokes one of the four custom skills and runs a full codebase audit.

**Agent type selection (critical):** Each agent MUST be dispatched as a `general-purpose` agent (or equivalent full-access agent type). Do NOT use specialized agent types like `feature-dev:code-reviewer`, `feature-dev:code-explorer`, `code-simplifier:*`, or any other restricted-toolset agent - these lack access to the Skill tool and cannot invoke custom skills. The agent type name should reflect its capabilities (full tool access), not the audit it performs.

**Skill invocation:** Each `general-purpose` agent MUST invoke the named custom skill via the Skill tool (or equivalent skill-loading mechanism) as its first action. Custom skills from the user's installed collection take priority over built-in reviewers or platform-provided audit modes. Specifically:
- Agent 1 invokes `code-review` via Skill tool, not a built-in code-review mode
- Agent 2 invokes `anti-slop` via Skill tool, not a built-in code simplifier
- Agent 3 invokes `security-audit` via Skill tool, not a built-in security scanner
- Agent 4 invokes `update-docs` via Skill tool, not a built-in documentation reviewer

**Fallback:** If a custom skill is not available (skill lookup/load returns "not found" or similar), THEN fall back to the best available alternative (manual review following the skill's principles) and note which skill was unavailable in the output header.

**If parallel execution is unavailable** (restricted sandbox, no subagent support): run
sequentially in this order: Security Audit, Code Review, Slop Check, Docs Sweep. Security
first because those findings are most time-sensitive. If any agent exceeds 5 minutes wall-clock, note the timeout in the output header and continue with the remaining agents.

**If agent dispatch is unavailable** (non-Claude harness, no subagent API): run each audit
sequentially in separate CLI sessions, invoking each skill manually in its own conversation.

Pass this context block to every agent, substituting the `{placeholders}` from preflight:

```
Context:
- Repo: {repo_root}
- Commit: {short_sha}
- Branch: {branch}
- Languages: {detected_languages}
- File count: {file_count}
- Scope: {scope}
```

Each agent receives the context block above plus a task prompt. Use these templates:

#### Agent 1: Code Review

```
{context_block}

Invoke the `code-review` skill via the Skill tool, then run a full code review on the codebase.
Scope: {scope}. ({scope} defaults to "full codebase" if the user did not specify a narrower target.)
Return the complete report.
```

#### Agent 2: Slop Check

```
{context_block}

Invoke the `anti-slop` skill via the Skill tool, then audit the codebase for machine-generated
patterns, over-abstraction, and code quality issues.
Scope: {scope}. ({scope} defaults to "full codebase" if the user did not specify a narrower target.)
Return the complete report.
```

#### Agent 3: Security Audit

```
{context_block}

Invoke the `security-audit` skill via the Skill tool, then run a security audit on the codebase.
Scope: {scope}. ({scope} defaults to "full codebase" if the user did not specify a narrower target.)
Return the complete report including SECURITY-AUDIT.md content.
```

#### Agent 4: Docs Sweep

```
{context_block}

Invoke the `update-docs` skill via the Skill tool as a read-only audit.
Scope: {scope}. ({scope} defaults to "full codebase" if the user did not specify a narrower target.)
Focus on: stale docs, instruction-file bloat (40,000 char limit), companion-file drift, broken
links, orphaned gotchas, missing docs on recent changes. Do NOT make changes or commit anything.
Return the complete report.
```

### Step 3: Present Results

After all four agents return, present each report under its own header. Do not merge, summarize, or editorialize across reports - each stands alone. The user reads the skill's native output, not a reinterpretation.

**Scoped reviews**: when the user specified a narrower scope, each report focuses on that scope. Use this routing table to emphasize domain-relevant checks:

| Scope | code-review focus | security-audit focus | anti-slop focus | update-docs focus |
|-------|-------------------|---------------------|-----------------|-------------------|
| Auth/session | Auth logic paths, token lifecycle | Session handling, token validation, credential storage | Auth middleware over-abstraction | Auth-related docs current |
| API endpoints | Request/response handling, error paths | Input validation, injection, rate limiting | Handler boilerplate, verbose error wrapping | API docs, OpenAPI spec |
| Data layer | Query correctness, race conditions | SQL injection, data exposure, access control | ORM abstraction, unnecessary wrappers | Schema docs, migration notes |
| Infrastructure | Config correctness, resource handling | Secrets exposure, misconfiguration | Over-engineered deploy scripts | Infra docs, runbook accuracy |

For scopes not in the table, apply each skill's standard checklist narrowed to the specified files/module. Do not skip an audit just because the scope seems domain-specific - every skill may surface relevant findings on arbitrary code.

**Scope verification before presenting**: when a scope was specified, confirm each agent's output before including it in the report. If an agent's findings reference files or modules outside the requested scope, that agent ignored the scope constraint - note the discrepancy in its report header and, if possible, filter out-of-scope findings. If an agent returned zero findings, confirm it actually ran against the scoped target (not an empty or wrong path) before reporting "no issues found."

**User requests synthesis**: if the user asks for a combined summary after seeing the reports, prioritize: security fixes > correctness bugs > slop cleanup > doc updates. Keep synthesis brief - the individual reports are the source of truth.

After presenting results, remind the user: "Check that `SECURITY-AUDIT.md` is in `.gitignore` - it contains vulnerability details that shouldn't be committed."

Use this structure:

```markdown
# Full Review: {repo_name} @ {short_sha}

Languages: {detected_languages} | Files: {file_count} | Branch: {branch}
Scope: {scope}

---

## 1. Code Review

{agent 1 output verbatim}

---

## 2. Slop Check

{agent 2 output verbatim}

---

## 3. Security Audit

{agent 3 output verbatim}

---

## 4. Docs Sweep

{agent 4 output verbatim}

---
```

### Step 4: Handle Failures

If an agent fails or times out:
- Note which audit failed and why (timeout, skill not found, tool permission denied)
- Present whatever completed successfully
- Do not re-run failed agents unless the user asks

If a skill is not available, perform a manual review in the same `general-purpose` agent. Note the substitution in the output header so the user knows a fallback was used. Partial results are still useful.

| Unavailable skill | Fallback approach |
|-------------------|-------------------|
| `code-review` | Manually review for bugs, logic errors, edge cases, and resource leaks. Focus on high-confidence findings only. |
| `anti-slop` | Scan for verbose code, redundant comments, over-abstraction, and dead code manually. No structured slop taxonomy - report what you find. |
| `security-audit` | Manually check for hardcoded secrets, injection points, missing auth checks, and dependency CVEs. Skip SECURITY-AUDIT.md generation. |
| `update-docs` | Review README, CLAUDE.md, AGENTS.md, and inline doc comments for staleness. Check that recent code changes have corresponding doc updates. |

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** FULL-REVIEW
- **Deliverable bucket:** `audits`
- **Mode:** always-on. Every invocation emits the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table.
- **Deliverable path:** `docs/local/audits/full-review/<YYYY-MM-DD>-<slug>.md`
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract).

## Related Skills

- **code-review** - one of the four parallel audits. Finds bugs, logic errors, correctness issues.
- **anti-slop** - one of the four parallel audits. Finds quality/style issues and AI-generated patterns.
- **security-audit** - one of the four parallel audits. Finds vulnerabilities, secrets, dependency risks.
- **update-docs** - one of the four parallel audits. Finds stale docs, bloated instruction files, and missing gotchas.
- **skill-creator** - audits the skill collection itself. Full-review audits application code.
- **ci-cd** - pipeline design and pipeline-config review. Full-review audits application code, not the pipelines that run it.

---

## Rules

- **General-purpose agents only.** Every subagent MUST be a `general-purpose` (full-access) agent type. Never use `feature-dev:*`, `code-simplifier:*`, or other restricted agent types - they cannot invoke custom skills. The agent type controls tool access, not the audit topic.
- **Custom skills first.** Each agent invokes its assigned custom skill (`code-review`, `anti-slop`, `security-audit`, `update-docs`) via the Skill tool as its first action. Fall back to manual review only if the skill is not installed.
- **Parallel dispatch is strongly preferred.** Run all four agents concurrently when the environment supports it. If parallel execution is unavailable, run sequentially (security first - see Step 2).
- **Don't editorialize.** Present each report as the skill produced it. No unsolicited synthesis across reports.
- **Respect each skill's output format.** The anti-slop skill has its own format. The security audit writes SECURITY-AUDIT.md. The code reviewer and docs sweep have their formats. Don't normalize them into a single style.
- **Don't duplicate work.** If a finding appears in multiple reports (e.g., dead code in both slop check and code review), that's fine - independent auditors catching the same thing is signal, not noise.
- **Preflight is fast.** The parallel git commands in Step 0 should take under 2 seconds. Don't skip them - the agent prompts are much better with context.
- **Large repos.** If file count exceeds 1000, mention to the user that this will take a while. Don't reduce scope unless asked.
- **SECURITY-AUDIT.md gitignore.** The security audit writes a report file containing vulnerability details to the repo root. After presenting results, remind the user to check that `SECURITY-AUDIT.md` is in `.gitignore` - the sub-skill warns too, but it's easy to miss buried in output.
- **Docs sweep is read-only.** The update-docs agent must not make changes or commit anything during a full review. It reports what needs updating; the user decides when to act on it.
