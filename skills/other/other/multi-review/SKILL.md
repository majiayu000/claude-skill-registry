---
name: multi-review
description: "This skill should be used when the user wants a comprehensive code review using multiple specialized reviewers in parallel. Invoked with /multi-review or when user asks for 'thorough review', 'full code review', or 'review from multiple perspectives'."
allowed-tools: Read, Bash, Glob, Grep, Write, AskUserQuestion, Task, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_click, mcp__playwright__browser_fill_form, mcp__playwright__browser_type, mcp__playwright__browser_press_key, mcp__playwright__browser_take_screenshot, mcp__playwright__browser_resize, mcp__playwright__browser_console_messages, mcp__playwright__browser_close, mcp__playwright__browser_run_code, mcp__playwright__browser_navigate_back, mcp__playwright__browser_evaluate
---

# Multi-Review: Parallel Specialized Code Review

You are orchestrating a comprehensive code review using multiple specialized review agents in parallel.

## Workflow

### Step 1: Identify Changes

Determine what code to review:

```bash
# If in a PR/branch context
git diff main...HEAD --name-only

# Or for staged changes
git diff --cached --name-only

# Or recent changes
git diff HEAD~5 --name-only
```

List the changed files and their types (e.g., `.py`, `.ts`, `.go`).

### Step 1.5: Load Review Configuration

Check for a project-level review configuration:

```bash
# Prefer review.json, fall back to risk-tiers.json for backward compatibility
cat .claude/review.json 2>/dev/null || cat .claude/risk-tiers.json 2>/dev/null || echo "No review config found"
```

If found, parse the configuration:
- `tiers`: Maps risk levels (critical, high, medium, low) to file glob patterns
- `reviewers` (v2): Optional object with `exclude` and `include` arrays for reviewer control

**Backward compatibility:** If the config contains a v1 `frameworks` key, honor it as a gate for framework reviewers and log a deprecation note: "Deprecation: `frameworks` array in risk-tiers.json is deprecated. Framework reviewers now auto-detect. Migrate to review.json v2 schema."

**Risk tier resolution:** For each changed file, match against tier patterns (most specific match wins). If a file matches multiple tiers, use the highest tier. If no match, default to `medium`.

Determine the **overall PR risk tier** = the highest tier among all changed files.

If no review config exists, fall back to the keyword-based behavior in Step 2.

### Step 2: Analyze Change Types

Categorize the changes to select appropriate reviewers:

| Change Type | Indicators | Relevant Reviewers |
|------------|------------|-------------------|
| Auth/Security | login, auth, password, token, jwt, permission | security-sentinel |
| Performance | query, cache, loop, batch, async, database | performance-oracle |
| Architecture | new files, interface, refactor, module | architecture-strategist |
| Patterns | any code change | pattern-recognition-specialist |
| Complexity | any code change | code-simplicity-reviewer |
| Agent/Tool systems | agent definitions, skills, prompts, tool configs, UI actions, API endpoints, forms, routes | agent-native-reviewer |
| Database migrations | db/migrate/*, schema changes, data backfills | data-integrity-guardian, data-migration-expert |
| UX/Interaction | components, forms, modals, flows, navigation | ux-reviewer |
| Frontend Perf  | images, imports, dependencies, animations     | frontend-performance-reviewer |
| Frontend/UI | .tsx, .jsx, .vue, .svelte, .html, .css, templates | (browser testing — see Step 9) |

### Step 2.5: Framework Auto-Detection

Map changed files to framework reviewers. A framework reviewer is activated when at least one changed file matches its patterns. No config required.

| File Patterns | Framework | Agent |
|--------------|-----------|-------|
| `*.tsx`, `*.jsx`, `next.config.*`, `middleware.ts` | `nextjs` | `nextjs-reviewer` |
| `*.css`, `tailwind.*`, `components/ui/**` | `tailwind` | `tailwind-reviewer` |
| `*.py`, `alembic/**` | `python-backend` | `python-backend-reviewer` |
| `routes/**`, `api/**`, `endpoints/**`, `controllers/**` | `api` | `api-security-reviewer` |
| `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `components/**`, `pages/**` | `ux` | `ux-reviewer` |
| `*.tsx`, `*.jsx`, `*.css`, `next.config.*`, `package.json` | `frontend-perf` | `frontend-performance-reviewer` |

**Reviewer overrides (v2 config):**
- `reviewers.exclude`: Suppress auto-detected reviewers (e.g., `["tailwind-reviewer"]` to prevent false positives)
- `reviewers.include`: Force always-on reviewers regardless of changed files (e.g., `["security-sentinel"]`)

**Backward compatibility:** If a v1 config with a `frameworks` key is loaded, use it as a gate — only activate framework reviewers that are both listed in `frameworks` AND matched by changed files (preserves old behavior).

### Step 3: Select Reviewers

**Always include:**
- `code-simplicity-reviewer` (YAGNI, complexity)
- `pattern-recognition-specialist` (anti-patterns, conventions)

**Conditionally include (keyword-based):**
- `security-sentinel` — if auth, input handling, secrets, or user data
- `performance-oracle` — if database queries, loops, caching, or data operations
- `architecture-strategist` — if structural changes, new modules, or interface changes
- `agent-native-reviewer` — if agent definitions, skill files, system prompts, tool configurations, new UI actions/views, API endpoints, forms, or routes (any user-facing capability that should have agent parity)
- `data-integrity-guardian` — if database migrations, schema changes, or data model modifications
- `data-migration-expert` — if data backfills, ID mappings, enum conversions, or column renames

**Tier-based reviewer selection (when review config exists):**

Use the overall PR risk tier from Step 1.5 to adjust reviewer selection:

| Tier | Reviewers |
|------|-----------|
| **critical** | All conditional reviewers that match + ALL matched framework agents |
| **high** | `security-sentinel` + `performance-oracle` + matched framework agents |
| **medium** | `code-simplicity-reviewer` + `pattern-recognition-specialist` + matched framework agents |
| **low** | `code-simplicity-reviewer` + up to 1 matched framework agent |

Always include `code-simplicity-reviewer` and `pattern-recognition-specialist` regardless of tier.

**Select 3-7 reviewers** based on the change types identified.

### Step 3b: Conditional Migration Reviewers

**Run migration-specific agents when the PR matches ANY of these criteria:**

- Files matching `db/migrate/*`, `migrations/*`, or `alembic/versions/*`
- Modifications to columns that store IDs, enums, or mappings
- Data backfill scripts or management commands
- Changes to how data is read/written (e.g., FK to string column)
- PR title/body mentions: migration, backfill, data transformation, ID mapping

**What these agents check:**
- `data-integrity-guardian`: Transaction boundaries, reversibility, constraint safety, ACID compliance, regulatory considerations (GDPR/CCPA)
- `data-migration-expert`: Verifies hard-coded mappings match production reality (prevents swapped IDs), checks for orphaned associations, validates dual-write patterns, provides SQL verification queries

### Step 4: Read Agent Definitions

For each selected reviewer, read the agent definition:

```bash
cat ~/.claude/agents/review/<agent-name>.md
```

### Step 4.5: SAST Artifact Consumption (Hybrid Verification)

Before launching reviewers, check if CI/CD SAST results are available:

```bash
# Check for SARIF artifacts from the security-checks workflow
gh run download --name semgrep-sarif --dir /tmp/sarif 2>/dev/null
```

If SARIF results are found, parse them and include in the `security-sentinel` prompt:

> "The following SAST findings were reported by Semgrep. For each finding, verify it in context: **confirm** as a real vulnerability, **dismiss** as a false positive with explanation, or **escalate** with additional context that amplifies the severity. Do not simply repeat SAST output — add the reasoning that automated tools cannot."

Append the SARIF finding summaries (file, rule ID, message) to the security-sentinel agent's prompt. This creates the hybrid approach: deterministic tools catch patterns, the AI agent reasons about whether they are real vulnerabilities in this specific codebase.

If no SARIF artifacts exist (CI hasn't run, or the project doesn't use the security-checks workflow), skip this step silently.

### Step 5: Launch Parallel Reviews

Use the Task tool to spawn parallel review agents.

**Model selection:** Default to Sonnet for efficiency. When review config exists and the PR risk tier is **critical**, use Opus for `security-sentinel` and `architecture-strategist` (these benefit most from deeper reasoning on critical code). All other reviewers use Sonnet regardless of tier.

```
Launch these agents in parallel:

1. Task: code-simplicity-reviewer
   - Subagent type: general-purpose
   - Model: sonnet
   - Prompt: [agent definition] + [files to review]

2. Task: pattern-recognition-specialist
   - Subagent type: general-purpose
   - Model: sonnet
   - Prompt: [agent definition] + [files to review]

3. Task: security-sentinel (if critical tier)
   - Subagent type: general-purpose
   - Model: opus (critical tier) or sonnet (other tiers)
   - Prompt: [agent definition] + [files to review]

4. Task: [additional selected reviewer]
   ...
```

Each agent should return findings in this format:
```markdown
## [Agent Name] Findings

### Critical Issues
- [Issue with file:line] - Confidence: X%

### Important Issues
- [Issue with file:line] - Confidence: X%

### Suggestions
- [Issue with file:line] - Confidence: X%
```

### Step 5.5: Checklist Augmentation

When constructing prompts for review agents in Step 5, append the following checklist categories as additional review guidance. These supplement each agent's core focus area.

**For all agents — check these universal categories:**

*LLM-specific (high priority if PR touches prompts, tools, or AI integrations):*
- 0-indexed lists in prompts (LLMs reliably return 1-indexed)
- Prompt text listing available tools/capabilities that don't match what's actually wired up
- LLM trust boundary: hallucinated values (emails, URLs, names) persisted without format validation
- Structured tool output accepted without type/shape checks before DB writes
- Word/token limits stated in multiple places that could drift

*Race conditions (include for security-sentinel and performance-oracle):*
- TOCTOU: check-then-set without atomic operation
- find-or-create without unique constraint (concurrent duplicates)
- Non-atomic status transitions (concurrent updates skip/double-apply)

*Niche categories (include for pattern-recognition-specialist):*
- Conditional side effects: branch that forgets a side effect on one path
- Type coercion at language boundaries (cross-language type changes, hash input normalization)
- Time window safety: mismatched windows between related features
- Crypto entropy: truncation vs hashing, rand() for security values, non-constant-time comparisons

### Step 6: Aggregate Findings

Combine results from all reviewers, sorted by severity:

```markdown
## Multi-Review Summary

### Reviewers
- [x] reviewer-name
...

### CRITICAL Findings (blocking — require action)
Security, data safety, race conditions, correctness bugs.
| File:Line | Issue | Reviewer | Confidence | Gate |
|-----------|-------|----------|------------|------|
| ... | ... | ... | ...% | CRITICAL |

### IMPORTANT Findings (should fix — non-blocking but significant)
Performance issues, error handling gaps, non-trivial anti-patterns, meaningful code quality issues.
| File:Line | Issue | Reviewer | Confidence | Gate |
|-----------|-------|----------|------------|------|
| ... | ... | ... | ...% | IMPORTANT |

### INFORMATIONAL Findings (surface, don't block)
Style, suggestions, minor improvements, nice-to-haves.
| File:Line | Issue | Reviewer | Confidence | Gate |
|-----------|-------|----------|------------|------|
| ... | ... | ... | ...% | INFO |
```

**Gate classification rules:**
- **CRITICAL**: Security vulnerabilities, data loss risks, race conditions, correctness bugs, missing error handling on critical paths, broken functionality
- **IMPORTANT**: Performance issues, error handling gaps on non-critical paths, non-trivial anti-patterns, meaningful code quality issues
- **INFORMATIONAL**: Code style, naming, minor refactoring opportunities, test coverage suggestions, documentation gaps, performance micro-optimizations

Note: Reviewer agents already output in `Critical Issues / Important Issues / Suggestions` format (Step 5 output template). Map these directly: Critical → CRITICAL, Important → IMPORTANT, Suggestions → INFORMATIONAL.

**Resolution Ledger**: Every finding that enters aggregation (post-suppression) must end the review in one of: `fixed[]`, `dropped[]` (with reason), or `deferred[]` (with reason meeting strict criteria). No finding may remain unresolved when the review concludes.

### Step 6.5: Suppressions

When aggregating findings in Step 6, suppress (do not surface) these categories of findings:

- **"X is redundant with Y"** when the redundancy is harmless and aids readability
- **"Add a comment explaining why this threshold/constant was chosen"** — thresholds change during tuning, comments rot
- **"This assertion could be tighter"** when the assertion already covers the behavior
- **Consistency-only changes** (wrapping a value to match how another is guarded)
- **"Regex doesn't handle edge case X"** when the input is constrained and X never occurs in practice
- **Anything already addressed in the diff being reviewed** — agents must read the FULL diff before commenting

These suppressions reduce noise from low-value suggestions that waste review cycles.

### Step 7: Filter Results

Only surface findings with **confidence >= 80%**. Findings below 80% confidence are entered into the resolution ledger as `dropped[reason: "below confidence threshold (N%)"]` — they do not silently vanish.

**Security exception:** All `security-sentinel` and `api-security-reviewer` findings appear in the main severity tables regardless of confidence level — never collapse them into "Low-Confidence Findings." Tag each with a `[SEC]` prefix in the Issue column to distinguish them from other reviewer findings. Security issues at any confidence level warrant human review.

### Step 8: Resolve Findings

> **Verification discipline** (from `/verify`): Before proposing any fix, read the actual code at the file:line the reviewer flagged. Reviewers hallucinate. Confirm the issue exists, then fix. If it doesn't exist, drop it — don't implement phantom fixes.

This step resolves ALL findings through a 5-phase process. No finding may remain unresolved.

#### Phase 1: Verify and Classify (agent acts alone)

For each CRITICAL and IMPORTANT finding, before presenting anything:

1. Read actual code at file:line (verification discipline — keeps this)
2. False positive or speculative → `dropped[]` with reason
3. Clear fix exists → `auto-fixable` (agent will apply)
4. Genuinely requires human decision → `deferred`

**Strict defer criteria:**

> The bar for `deferred` is HIGH. These are NOT valid reasons to defer:
> - "This is complex" — complexity isn't a reason to punt
> - "This might have side effects" — verify whether it does, then fix or drop
> - "This could be done multiple ways" — pick the approach matching existing codebase patterns
> - "I'm not sure about the intent" — read surrounding code and git blame
> - "This is a style/taste issue" — match existing patterns, or drop
>
> These ARE valid reasons to defer:
> - Fix requires choosing between two valid architectural approaches with real tradeoffs
> - Fix involves a product/business decision (e.g., "should this error be user-visible or silent?")
> - Fix requires production knowledge the agent cannot verify (e.g., "is this table too large for this migration?")

#### Phase 2: Auto-fix with preview (agent acts, does NOT ask permission)

Present the resolution plan, then apply fixes:

```
## Resolution Plan

### Auto-fixing (N findings):
1. [file:line] - [issue] - [fix description]
2. ...

### Dropped (M findings):
3. [file:line] - [issue] - DROPPED: [reason]
4. ...

### Deferred — requires your decision (P findings):
5. [file:line] - [issue] - DEFERRED: [specific decision needed]
6. ...

Applying auto-fixes...
```

The agent applies all auto-fixable changes to the working tree without asking. It does NOT commit — that's the caller's job (finish-task commits, or the user commits manually). The user can review the diff afterward.

#### Phase 3: Mandatory adjudication of deferred items

After auto-fixes are applied, present ALL deferred findings in a SINGLE `AskUserQuestion` (not one question per finding):

```
## N Deferred Findings Require Your Decision

1. **[file:line]** - [issue] — [reviewer]
   Decision needed: [specific question, e.g., "extract to service vs inline guard?"]
   Options: (a) approach A, (b) approach B, (c) dismiss, (d) create task

2. **[file:line]** - [issue] — [reviewer]
   Decision needed: [specific question]
   Options: (a) approach A, (b) approach B, (c) dismiss, (d) create task

Reply with your choices (e.g., "1a, 2c"):
```

Each response moves the finding to `fixed[]` (agent implements chosen approach), `dropped[]` (dismissed), or `deferred[task: <id>]` (beads task created). The review does NOT proceed to re-review until all deferred items are resolved.

**Autonomous context** (when multi-review runs inside `/finish-task` as an Agent Teams worker with no human available): skip `AskUserQuestion`. Instead, auto-create beads tasks for all deferred items and log them as `deferred[task: <id>]`. Report the deferred count in the session summary for the orchestrator to see. Detection: if the session is a dispatched teammate, treat as autonomous.

#### Phase 4: INFORMATIONAL batch resolution

Present INFORMATIONAL findings as a batch:

```
## Informational Findings (N items)

1. [file:line] - [issue]
2. [file:line] - [issue]
...

Options:
1. Fix all informational items
2. Fix specific items (provide numbers)
3. Acknowledge all (mark as reviewed, no action)
```

User must pick one. "Acknowledge all" is fine — the point is explicit accounting, not forced action. All items move to `fixed[]` or `dropped[acknowledged]`.

**Autonomous context**: auto-fix INFORMATIONAL items that have clear fixes, drop the rest as `dropped[informational — auto-acknowledged]`.

#### Phase 5: Re-review cycles (refined)

After fixes are applied, re-review modified files with escalating thresholds:

- Previous-cycle ledger entries are DONE — never re-evaluated
- Escalating thresholds apply only to NET-NEW findings from re-review of modified files:
  - **Cycle 2**: Re-run only affected reviewers on fix-modified files. Net-new findings >= 85% confidence only.
  - **Cycle 3**: Only Critical findings >= 90% confidence on fix-modified files.
- New findings from Cycle 2/3 enter the ledger and go through the same Verify → Classify → Fix → Adjudicate flow
- The ledger accumulates across cycles

**Exit conditions** (stop the loop when ANY is met):
- **Clean**: Zero findings this iteration → EXIT
- **Diminishing returns**: <3 net-new findings AND zero Critical → EXIT
- **Plateau**: Net-new count >= previous iteration (not converging) → EXIT
- **Limit**: 3 iterations → EXIT

Log exit reason so the final report explains why the loop stopped.

#### Final Report

After all phases complete, output the resolution ledger summary:

```
═══════════════════════════════════════════
MULTI-REVIEW COMPLETE
═══════════════════════════════════════════
Reviewers: [list]
Cycles: N (exit reason: [reason])
Findings: X | Fixed: Y | Dropped: Z | Deferred: W

FIXED:
- [file:line] issue — fix applied

DROPPED:
- [file:line] issue — [reason]

DEFERRED (tasks created):
- [file:line] issue — task <id>

INFORMATIONAL (acknowledged):
- [file:line] issue
═══════════════════════════════════════════
```

### Step 9: Browser Workflow Testing

**When the PR includes frontend/UI changes**, run workflow-based browser testing.

Detect frontend changes by checking for files matching:
- `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.html`
- `*.css`, `*.scss`, `*.less`
- `templates/**`, `views/**`, `components/**`, `pages/**`

If no frontend changes detected, skip this step.

**Read `docs/browser-testing-protocol.md` and follow Phases 1-6:**

1. Pre-flight checks — verify Playwright MCP available, dev server running (Phase 1)
2. Infer workflows from diff — classify changed files, propose to user via `AskUserQuestion` for confirmation (Phase 2)
3. Navigate → clear cache/storage → reload — ensures fresh state, not stale cache (Phase 3)
4. Handle auth if page redirects to login (Phase 4)
5. Execute workflow-type checklists — interact, verify outcomes, verify persistence via reload (Phase 5)
6. Responsive check at desktop (1280x800) + mobile (375x812) and report findings (Phase 6)

**Multi-review specific:** Browser findings enter the same aggregation pipeline as code review findings (Step 6). Classify as Critical/Important/Minor per the protocol's Phase 6 severity table.

## Agent Reference

### Always Included

#### code-simplicity-reviewer
**Focus**: YAGNI, complexity reduction, unnecessary code
**Path**: `agents/review/code-simplicity-reviewer.md`

#### pattern-recognition-specialist
**Focus**: Anti-patterns, code conventions, consistency
**Path**: `agents/review/pattern-recognition-specialist.md`

### Conditionally Included

#### security-sentinel
**Focus**: CWE-enriched OWASP review, business logic vulnerabilities (IDOR, auth bypass), absence detection, self-verification loop
**Include when**: Auth code, user input, API endpoints, secrets handling, new routes/handlers
**Path**: `agents/review/security-sentinel.md`

#### performance-oracle
**Focus**: N+1 queries, memory leaks, caching, async patterns
**Include when**: Database operations, loops over data, caching changes
**Path**: `agents/review/performance-oracle.md`

#### architecture-strategist
**Focus**: SOLID principles, design patterns, module structure
**Include when**: New files, interface changes, structural refactoring
**Path**: `agents/review/architecture-strategist.md`

#### agent-native-reviewer
**Focus**: Action/context parity, tool design, agent capability gaps
**Include when**: Agent definitions, skill files, system prompts, MCP configs, new UI actions/views, API endpoints, forms, routes — any change that adds user-facing capabilities
**Path**: `agents/review/agent-native-reviewer.md`

#### data-integrity-guardian
**Focus**: Migration safety, ACID compliance, transaction boundaries, GDPR/CCPA
**Include when**: Database migrations, schema changes, data model modifications
**Path**: `agents/review/data-integrity-guardian.md`

#### data-migration-expert
**Focus**: Mapping validation, rollback safety, production data verification
**Include when**: Data backfills, ID mappings, enum conversions, column renames
**Path**: `agents/review/data-migration-expert.md`

### Framework-Specific Reviewers (Auto-detected from changed files)

#### nextjs-reviewer
**Focus**: App Router conventions, Server vs Client Components, Server Actions security, metadata, routing
**Auto-detected when**: Changed files match `*.tsx`, `*.jsx`, `next.config.*`, `middleware.ts`
**Path**: `agents/review/nextjs-reviewer.md`

#### tailwind-reviewer
**Focus**: Tailwind/shadcn patterns, accessibility, responsive design, dark mode, WCAG 2.1 AA
**Auto-detected when**: Changed files match `*.css`, `tailwind.*`, `components/ui/**`
**Path**: `agents/review/tailwind-reviewer.md`

#### python-backend-reviewer
**Focus**: FastAPI, SQLAlchemy 2.0, Alembic, async Python, Pydantic v2, pytest
**Auto-detected when**: Changed files match `*.py`, `alembic/**`
**Path**: `agents/review/python-backend-reviewer.md`

#### api-security-reviewer
**Focus**: Rate limiting, pagination bounds, response data filtering, CORS, request size limits, security logging
**Auto-detected when**: Changed files match `routes/**`, `api/**`, `endpoints/**`, `controllers/**`
**Path**: `agents/review/api-security-reviewer.md`

#### ux-reviewer
**Focus**: Interaction flows, state completeness, form UX patterns, component API consistency, screen reader narrative, cognitive load
**Auto-detected when**: Changed files match `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `components/**`, `pages/**`
**Path**: `agents/review/ux-reviewer.md`

#### frontend-performance-reviewer
**Focus**: Core Web Vitals (LCP, CLS, INP), bundle size, request waterfalls, rendering efficiency, image optimization
**Auto-detected when**: Changed files match `*.tsx`, `*.jsx`, `*.css`, `next.config.*`, `package.json`
**Path**: `agents/review/frontend-performance-reviewer.md`

## Important Notes

- Parallel execution is key — don't run reviewers sequentially
- Filter to >= 80% confidence to reduce noise
- Security findings should always be surfaced even at lower confidence
- Maximum 3 review cycles for auto-fix iterations
- Migration reviewers should always run together (integrity + migration expert)
- Browser testing uses workflow-based verification (not just screenshots) and requires user consent
- Framework reviewers auto-detect from changed files. Use `reviewers.exclude` in `review.json` to suppress false positives.
