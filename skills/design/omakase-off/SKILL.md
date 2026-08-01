---
name: omakase-off
description: 'ALWAYS invoke FIRST on ANY "build/create/implement/add feature" request.
  This skill WRAPS brainstorming - it decides the approach. Present choice BEFORE
  any brainstorming starts: (1) Brainstorm togeth'
---

---
name: omakase-off
description: ALWAYS invoke FIRST on ANY "build/create/implement/add feature" request. This skill WRAPS brainstorming - it decides the approach. Present choice BEFORE any brainstorming starts: (1) Brainstorm together step-by-step, OR (2) Omakase - I generate 3-5 best approaches, implement in parallel, tests pick winner. If user picks brainstorming, check if brainstorming skill exists - if yes use it, if no do brainstorming yourself (ask questions, propose options, validate). Also triggers DURING brainstorming on 2+ "not sure"/"don't know" responses. For same design competing implementations, use cookoff.
---

# Omakase-Off

Chef's choice exploration - when you're not sure WHAT to build, explore different approaches in parallel.

**Part of Test Kitchen Development:**
- `omakase-off` - Chef's choice exploration (different approaches/plans)
- `cookoff` - Same recipe, multiple cooks compete (same plan, multiple implementations)

**Core principle:** Let indecision emerge naturally during brainstorming, then implement multiple approaches in parallel to let real code + tests determine the best solution.

## Skill Dependencies

This skill orchestrates other skills. Check what's installed and use fallbacks if needed.

| Reference | Primary (if installed) | Fallback (if not) |
|-----------|------------------------|-------------------|
| `brainstorming` | `superpowers:brainstorming` | Ask questions one at a time, propose 2-3 approaches, validate incrementally |
| `writing-plans` | `superpowers:writing-plans` | Write detailed plan with file paths, code examples, verification steps |
| `git-worktrees` | `superpowers:using-git-worktrees` | `git worktree add .worktrees/<name> -b <branch>`, verify .gitignore |
| `parallel-agents` | `superpowers:dispatching-parallel-agents` | Dispatch multiple Task tools in single message, review when all return |
| `subagent-dev` | `superpowers:subagent-driven-development` | Fresh subagent per task, code review between tasks |
| `tdd` | `superpowers:test-driven-development` | Write test first, watch fail, write minimal code, refactor |
| `scenario-testing` | `scenario-testing:skills` (2389) | Create `.scratch/` E2E scripts, real dependencies, no mocks |
| `verification` | `superpowers:verification-before-completion` | Run verification command, read output, THEN claim status |
| `fresh-eyes` | `fresh-eyes-review:skills` (2389) | 2-5 min review for security, logic errors, edge cases |
| `code-review` | `superpowers:requesting-code-review` | Dispatch code-reviewer subagent with SHA range |
| `finish-branch` | `superpowers:finishing-a-development-branch` | Verify tests, present options (merge/PR/keep/discard) |

**At skill start:** Check which dependencies are available. Announce: "Using [X] for brainstorming, [Y] for scenario testing..." so user knows which tools are active.

**If primary not installed:** Use the fallback behavior described above. The fallback is the essential behavior - primary skills just formalize it.

## When to Use

Omakase-off has TWO trigger points:

### Trigger 1: BEFORE Brainstorming (Short-Circuit Option)

When user requests "build X", "create Y", "implement Z" - BEFORE diving into detailed brainstorming, offer the short-circuit:

```
Before we brainstorm the details, would you like to:

1. Brainstorm together - We'll explore requirements and design step by step
2. Omakase (chef's choice) - I'll generate 3-5 best approaches, implement them
   in parallel, and let tests pick the winner
   → Best when: you're flexible on approach, want to see options in code

Which approach?
```

**When to offer this:** On any substantial "build/create/implement" request before starting brainstorming.

### Trigger 2: DURING Brainstorming (Indecision Detection)

If user shows uncertainty during brainstorming:

**Detection signals:**
- 2+ uncertain responses in a row on architectural decisions
- Phrases: "not sure", "don't know", "either works", "you pick", "no preference", "hmm"
- User defers multiple decisions to you

**When detected, offer omakase:**
```
You seem flexible on the approach. Would you like to:
1. I'll pick what seems best and continue brainstorming
2. Explore multiple approaches in parallel (omakase-off)
   → I'll implement 2-3 variants and let tests decide
```

### Trigger 3: Explicitly Requested

User directly asks:
- "try both approaches", "explore both", "omakase"
- "implement both variants", "let's see which is better"
- "not sure which is better, try both"

## The Process

### Phase 0: Entry Point (Short-Circuit vs Brainstorm)

**When user requests "build/create/implement X":**

Present the choice BEFORE starting detailed brainstorming:
```
Before we dive into the details, how would you like to approach this?

1. Brainstorm together - We'll explore requirements and design step by step
2. Omakase (chef's choice) - I'll generate 3-5 best approaches, implement
   them in parallel, and let tests pick the winner
   → Best when: you're flexible, want to see options in working code

Which approach?
```

**If user picks Omakase (option 2):**
1. Quick context gathering (1-2 essential questions only)
2. Generate 3-5 distinct architectural approaches
3. Jump directly to Phase 2 (Plan Generation) with those variants
4. Skip detailed brainstorming entirely

**If user picks Brainstorm (option 1):**
Continue to Phase 1 below.

### Phase 1: Brainstorming with Passive Slot Detection

**First, check if a brainstorming skill is available:**
- Look for `superpowers:brainstorming` or similar skill in available skills
- If available → invoke it and passively detect indecision during the flow
- If NOT available → **do brainstorming yourself using fallback behavior:**
  - Ask questions one at a time
  - Propose 2-3 approaches for key decisions
  - Validate incrementally with user
  - Track architectural vs trivial decisions

**Fallback brainstorming flow (when no brainstorming skill):**
1. Read the codebase to understand context
2. Ask focused questions about the feature (what, where, how)
3. For each decision point, propose options and get user input
4. Track decisions and note any indecision (potential slots)
5. Build toward a design document

**During brainstorming (whether using skill or fallback), passively detect indecision:**

**Detect indecision signals** when user responds to options:
- Explicit: "slot", "try both", "explore both"
- Uncertain: "not sure", "hmm", "either could work", "both sound good", "no idea", "I don't know"
- Deferring: "you pick", "whatever you think", "I don't have a strong preference"

**When indecision detected:**
- Mark that decision as a potential slot
- Classify it: **architectural** (affects code structure) vs **trivial** (cosmetic/config)
- Continue brainstorming normally (pick a placeholder to continue)

**Slot classification:**
| Type | Examples | Worth exploring? |
|------|----------|------------------|
| **Architectural** | Storage engine, framework, auth method, API style | Yes - different code paths |
| **Trivial** | File location, naming conventions, config format | No - easy to change later |

Only architectural decisions become real slots.

**Fast path detection:**
After 2+ uncertain answers in a row, offer to shortcut:
```
You seem flexible on the details. Want me to:
1. Make sensible defaults and you flag anything wrong
2. Continue exploring each decision

Which works better?
```

If user picks defaults, make reasonable choices and note them. Continue brainstorming for only the big architectural decisions.

**Track throughout:**
```
Architectural slots:
1. Data storage: [JSON, SQLite] - meaningfully different code

Trivial (defaulted):
- File location: ~/.todos.json (easy to change)
- Config format: JSON (doesn't affect architecture)

Fixed decisions:
- Language: TypeScript (user chose)
```

### Phase 1.5: End-of-Brainstorm Decision

**If NO architectural slots were collected** (user was decisive):

Hand off to cookoff for implementation. Present options:
```
Design complete. How would you like to implement?

1. Cookoff (recommended) - N parallel agents, each creates own plan, pick best
   → Complexity: [assess from design]
   → Best for: medium-high complexity, want to compare implementations
2. Single subagent - One agent plans and implements
3. Local - Implement here in this session
```

If user picks cookoff, invoke cookoff skill and exit omakase-off.

---

**If slots WERE collected** (user showed indecision):

```
I noticed some open decisions during our brainstorm:
- Storage: JSON vs SQLite
- Auth: JWT vs session-based

Would you like to:
1. **Explore in parallel** - I'll implement both variants and let tests decide
2. **Best guess** - I'll pick what seems best and proceed with one plan

Which approach?
```

**If "Best guess":** Pick the most suitable option for each slot, proceed with single plan (hand off to cookoff with the options above).

**If "Explore in parallel":** Continue to Phase 2 (omakase-off's variant exploration).

**Combination limits (max 5-6 implementations):**

When multiple architectural slots exist, don't do full combinatorial explosion. Instead, pick **meaningfully different** variants:

1. **Identify the primary axis** - Which slot has the biggest architectural impact?
2. **Create variants along that axis** - Each variant explores a different primary choice
3. **Fill in secondary slots** with the most natural pairing for each primary

**Example:** 3 slots (storage: JSON/SQLite, framework: Express/Fastify, auth: JWT/session)
- Don't create 2x2x2 = 8 variants
- Primary axis: storage (biggest code difference)
- Create 2-3 variants:
  - `variant-json-simple`: JSON + Express + session (lightweight stack)
  - `variant-sqlite-robust`: SQLite + Fastify + JWT (production-ready stack)
  - Maybe: `variant-json-jwt`: JSON + Express + JWT (if JWT is important to test)

**Pruning rules:**
- Remove architecturally incompatible pairings (e.g., SQLite + serverless)
- Remove redundant variants (if two variants would have nearly identical code)
- Ask user if unsure which variants are most meaningful to compare

### Phase 2: Plan Generation

For each variant combination:

1. Generate full implementation plan using `superpowers:writing-plans`
2. Store in structured directory:

```
docs/plans/<feature>/
  design.md                  # Shared context from brainstorming
  omakase/
    variant-<slug-1>/
      plan.md                # Implementation plan for this variant
    variant-<slug-2>/
      plan.md
    result.md                # Final report (written at end)
```

### Phase 3: Implementation

**Setup worktrees** (separate from plans directory):
- Use `git-worktrees` dependency for each variant
- Worktree location: `.worktrees/` or per project convention
- Branch naming: `<feature>/omakase/<variant-name>` (e.g., `auth/omakase/jwt-redis`)
- All worktrees created before implementation starts

**CRITICAL: Dispatch ALL variants in a SINGLE message**

Use `parallel-agents` pattern. Send ONE message with multiple Task tool calls:

```
<single message>
  Task(variant-json, run_in_background: true)
  Task(variant-sqlite, run_in_background: true)
</single message>
```

Do NOT send separate messages for each variant.

**Subagent prompt template:**
```
Implement variant-<name> in .worktrees/variant-<name>
- Read plan from docs/plans/<feature>/omakase/variant-<name>/plan.md
- Use `subagent-dev` to execute plan
- Follow `tdd` for each task
- Use `verification` before claiming done
- Report: what was built, test results, any issues
```

**Each subagent workflow:**
1. Read their variant's plan from `docs/plans/<feature>/omakase/variant-<name>/plan.md`
2. Execute tasks using `subagent-dev` (fresh context per task, review between)
3. Follow `tdd` - write test first, watch fail, implement, pass
4. Use `verification` - run tests, read output, THEN claim complete
5. Report back: summary, test counts, files changed, issues

**Monitor progress:**
```
Implementation status:
- variant-json: 3/5 tasks complete
- variant-sqlite: 2/5 tasks complete (in progress)
```

User can manually kill slow/stuck implementations.

**When subagent reports complete:**
- Use `code-review` to review the variant's implementation
- Fix any Critical/Important issues before proceeding to Phase 4
- Note: each variant reviewed independently

### Phase 4: Evaluation

**Step 1: Scenario testing (REQUIRED - not ad-hoc)**
- **MUST use `scenario-testing`** - not manual ad-hoc verification
- Create scenarios in `.scratch/` that exercise real functionality
- Same scenarios run against ALL variants (apples-to-apples comparison)
- Scenarios must use real dependencies, no mocks
- Must pass all scenarios to be a "survivor"

**Step 2: Fresh-eyes review on survivors**

For each variant that passed scenarios, use `fresh-eyes`:
```
Starting fresh-eyes review of variant-json (N files). This will take 2-5 minutes.

Checking for:
- Security vulnerabilities (SQL injection, XSS, command injection)
- Logic errors (off-by-one, race conditions, null handling)
- Edge cases tests might have missed
- Code quality issues

Fresh-eyes complete for variant-json: [N] issues found.
```

**Fresh-eyes findings become judge input:**
- Track issues found per variant
- Security issues = major negative
- Logic errors = moderate negative
- Clean review = positive signal

**Step 3: Elimination**
| Situation | Action |
|-----------|--------|
| Fails tests | Eliminated |
| Fails scenarios | Eliminated |
| Critical security issue in fresh-eyes | Eliminated (or fix first) |
| Crashes/stalls | User can eliminate |
| All fail | Report failures, ask user how to proceed |
| One survives | Auto-select |

**Step 4: Judge (comparing survivors)**

If multiple survivors, compare using:

| Input | Source | Weight |
|-------|--------|--------|
| Scenario results | Step 1 | Pass/fail gate |
| Fresh-eyes findings | Step 2 | Quality signal |
| Code complexity | Line count, dependencies | Simplicity preference |
| Test coverage | Test count, coverage % | Confidence signal |

**Present comparison to user:**
```
Both variants passed scenarios. Fresh-eyes review:
- variant-json: 0 issues, 450 lines, 12 tests
- variant-sqlite: 1 minor issue (magic number), 520 lines, 15 tests

Recommendation: variant-json (simpler, cleaner review)

Pick winner: [1] json  [2] sqlite  [3] show me the code
```

**LLM Judge (future):** Automate the comparison above with structured scoring.

### Phase 5: Completion

**Before declaring winner, use `verification`:**
```
Running final verification on winner (variant-json):
- npm test: 12/12 passing
- npm run build: exit 0
- Scenarios: all passing

Verification complete. Winner confirmed.
```

**Winner:** Use `finish-branch` dependency
- Verify all tests pass (already done above)
- Present options: merge locally, create PR, keep as-is, discard
- Execute user's choice

**Losers:** Cleanup
```bash
git worktree remove <worktree-path>
git branch -D <feature>/omakase/<variant>
```

**Write result.md:**
```markdown
# Omakase-Off Results: <feature>

## Variants
| Variant | Tests | Scenarios | Fresh-Eyes | Result |
|---------|-------|-----------|------------|--------|
| variant-json | 12/12 | PASS | 0 issues | WINNER |
| variant-sqlite | 15/15 | PASS | 1 minor | eliminated |

## Winner Selection
Reason: Both passed, but variant-json was simpler (fewer lines, cleaner fresh-eyes)

## Judge Inputs
- Scenario results: Both passed
- Fresh-eyes: json=clean, sqlite=1 minor issue
- Complexity: json=450 lines, sqlite=520 lines

## Cleanup
Worktrees removed: 1
Branches deleted: todo/omakase/variant-sqlite
Plans preserved: docs/plans/<feature>/omakase/
```

Save to: `docs/plans/<feature>/omakase/result.md`

## Skills Orchestrated

Uses dependencies defined above. Primary skill if installed, fallback otherwise.

| Dependency | Phase | Usage |
|------------|-------|-------|
| `brainstorming` | 1 | Modified flow with passive slot detection |
| `writing-plans` | 2 | Generate implementation plan per variant |
| `git-worktrees` | 3 | Create isolated worktree per variant |
| `parallel-agents` | 3 | Dispatch all variant subagents in parallel |
| `subagent-dev` | 3 | Each subagent uses this for task execution |
| `tdd` | 3 | Subagents follow RED-GREEN-REFACTOR |
| `verification` | 3, 5 | Before claiming variant done; before declaring winner |
| `code-review` | 3 | Review each variant after implementation |
| `scenario-testing` | 4.1 | Run same scenarios against all variants |
| `fresh-eyes` | 4.2 | Quality review on survivors → input for judge |
| `finish-branch` | 5 | Handle winner (merge/PR), cleanup losers |

## Common Mistakes

**Too many slots**
- Problem: Combinatorial explosion (2x2x2x2 = 16 variants)
- Fix: Cap at 5-6, ask user to constrain if exceeded

**Not using existing skills**
- Problem: Ad-hoc implementation instead of established workflow
- Fix: Each subagent MUST use executing-plans skill

**Ad-hoc scenario testing**
- Problem: Manual "click through" verification instead of real scenario tests
- Fix: MUST use `scenario-testing` skill with `.scratch/` scenarios, no mocks

**Premature elimination**
- Problem: Killing implementation that's just slow
- Fix: No hard timeouts; user decides when to kill

**Forgetting cleanup**
- Problem: Orphaned worktrees and branches
- Fix: Always cleanup losers, write result.md

## Example Invocation

```
User: "I need to build a CLI todo app."

Claude: I'm using omakase-off.

Before we dive into the details, how would you like to approach this?

1. Brainstorm together - We'll explore requirements and design step by step
2. Omakase (chef's choice) - I'll generate 3-5 best approaches, implement
   them in parallel, and let tests pick the winner

User: "1"

Claude: Great, let's brainstorm. What language would you like to use?

User: "not sure"

Claude: [Marks language as potential slot - architectural]
No problem. For data storage?

User: "no idea"

Claude: [Marks storage as potential slot - architectural]
[Detects 2+ uncertain answers]

You seem flexible on the details. Want me to:
1. Make sensible defaults and you flag anything wrong
2. Continue exploring each decision

User: "1"

Claude: Got it. Here's my proposal:

**Defaults:**
- Language: TypeScript (great CLI ecosystem)
- CLI framework: Commander (standard choice)
- File location: ~/.todos.json (trivial - easy to change)

**Worth exploring (architecturally different):**
- Storage: JSON file vs SQLite

JSON is simpler, SQLite handles larger datasets. Both are valid.
Does this look right? Anything to change?

User: "looks good"

Claude: Great. One architectural slot: storage (JSON vs SQLite).

Would you like to:
1. Explore in parallel - I'll implement both and let tests decide
2. Best guess - I'll pick JSON (simpler) and proceed

User: "1"

[Phase 2: Generate plans for variant-json, variant-sqlite]
[Phase 3: Create worktrees, dispatch parallel subagents]
[Phase 4: Both pass scenarios, present comparison]
[Phase 5: User picks sqlite, cleanup json branch]

Winner: variant-sqlite
Cleanup complete. Ready to merge or create PR.
```
