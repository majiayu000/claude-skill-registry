---
name: quality
description: Code quality analysis through cleanup analysis and multi-perspective reviews.
---

# Quality

Analyze code quality through different lenses: cleanup analysis for technical debt and multi-perspective reviews for holistic assessment.

## Requirements

- None (both actions work independently)

## Actions

### cleanup - Code Quality Analysis

Analyze changed code for quality issues and technical debt.

**Scope:** $ARGUMENTS (or current branch vs main if not specified)

#### Steps

1. **Determine scope:**
   - If $ARGUMENTS specifies files/scope, use that
   - Otherwise: `git diff origin/main...HEAD` from current directory

2. **Analyze for issues:**
   - Dead code - exported but never used functions/classes/constants
   - Duplicate code - similar logic in multiple places
   - Unclear patterns - confusing imports, magic numbers, missing comments
   - Inconsistencies - same thing done differently in different files
   - Type safety - missing or incorrect type hints
   - Complexity - overly complex patterns that could be simplified
   - Documentation - missing docstrings, unclear parameter purposes
   - TODOs/FIXMEs - should they be tracked issues instead?

3. **Create cleanup report:**
   - File: `[TIMESTAMP_FILE]-cleanup.md` in current directory

   ```markdown
   # Cleanup Analysis
   Date: [TIMESTAMP_LOG]
   Scope: [what was analyzed]

   ## Issues Found

   ### 1. [Issue title]
   **Type:** [Dead code/Duplicate/Unclear/etc.]
   **Location:** [file:line]
   **Priority:** [High/Medium/Low]
   **Breaking:** [Yes/No]

   **Problem:**
   [Description]

   **Options:**
   1. [Option with pros/cons]
   2. [Option with pros/cons]

   **Recommendation:** [Which option and why]

   [Repeat for each issue]

   ## Summary

   | Issue | Recommendation | Priority | Breaking? |
   |-------|---------------|----------|-----------|
   | ...   | ...           | ...      | ...       |

   ## Implementation Phases

   ### Phase 1: High Priority
   - [ ] [Action item]

   ### Phase 2: Medium Priority
   - [ ] [Action item]

   ### Phase 3: Low Priority
   - [ ] [Action item]
   ```

4. **Report back:** Summary of issues found by priority

---

### multi-review - Multi-Perspective Review

Review changes using five specialized perspectives: Future Maintainer, System Architect, Product/User Advocate, one opposite-provider external reviewer (Security & Correctness), and Gemini (Performance & Testing).

**Target branch:** $ARGUMENTS (defaults to current branch if not specified)

#### Setup

Before spawning sub-agents, set up the review environment:

1. **If `$ARGUMENTS` is empty or not provided**:
   - Use current directory, no setup needed
   - Working directory for sub-agents: current directory

2. **If `$ARGUMENTS` is specified**:

   ```bash
   # Fetch to ensure remote branches are available
   git fetch origin

   # Clean up any existing worktree from previous reviews
   WORKTREE_PATH="../review-$ARGUMENTS"
   git worktree remove --force "$WORKTREE_PATH" 2>/dev/null || true

   # Try local branch first, then remote
   if git show-ref --verify --quiet "refs/heads/$ARGUMENTS"; then
     git worktree add "$WORKTREE_PATH" "$ARGUMENTS"
   elif git show-ref --verify --quiet "refs/remotes/origin/$ARGUMENTS"; then
     git worktree add "$WORKTREE_PATH" "origin/$ARGUMENTS"
   else
     echo "Error: Branch '$ARGUMENTS' not found locally or on origin"
     # Stop here - do not spawn sub-agents
   fi
   ```

   - Working directory for sub-agents: the worktree path

3. **Prepare change context:**
   Read the commit messages yourself: `cd <REVIEW_DIRECTORY> && git log origin/main..HEAD --oneline`

   **IMPORTANT: You MUST then spawn a haiku sub-agent** (via Task tool, model: haiku) to summarize the diff. Do NOT skip this step — reading the diff yourself wastes context you need for the final synthesis:

   ```
   Run `cd <REVIEW_DIRECTORY> && git diff origin/main...HEAD` and write a concise
   summary of the actual code changes -- what was added, modified, removed, and
   the key patterns/logic involved. Keep it to 3-5 sentences. Return ONLY the
   summary, nothing else.
   ```

   Combine the commit messages with the haiku agent's diff summary into a change context block. Include it in every reviewer agent's instructions so each understands the purpose and substance of the change. Do NOT read the diff yourself.

#### Shared Output Schema

All five agents MUST use this structured format for every finding. Define this once and include it in each agent's instructions:

```
For each finding, provide ALL of these fields:
- file: [exact file path from the diff]
- lines: [line range, e.g. "42-58"]
- category: [one of: naming, documentation, complexity, coupling, security,
             error-handling, performance, testing, logic, ux]
- severity: [blocking | important | suggestion]
- confidence: [high | medium | low]
- title: [one-line summary, max 80 chars]
- finding: [detailed description, 2-5 sentences]
- evidence: [specific code snippet or reference supporting this finding]
- recommendation: [concrete action -- what should be done instead]

After all findings, include a summary line:
"Total: X findings (Y blocking, Z important, W suggestions)"
```

#### Shared Reasoning Protocol

Prepend these instructions to every agent's review task, before their persona-specific instructions:

```
Before listing findings, follow this reasoning process:
1. Read the diff and understand what this change accomplishes
2. Identify the key operations, data flows, and integration points
3. Evaluate each against your review checklist below
4. For each potential concern, verify it is genuine by checking surrounding context
5. Only report findings you can support with specific evidence from the diff
```

#### Sub-Agent Instructions

Spawn three internal sub-agents **in parallel** (via Task tool), plus one opposite-provider external review and one Gemini review (via Bash tool). All five run concurrently. Give each agent:

- The **change context summary** from Setup step 3
- The **review directory path** (current directory or worktree path)
- The **shared reasoning protocol** above
- The **shared output schema** above
- Their **persona-specific instructions** below
- Instructions to run the git diff command **from that directory** using `cd <path> && git diff origin/main...HEAD`

**Critical**: When a worktree is used, agents MUST `cd` into the worktree directory before running git commands.

---

**Agent 1: Future Maintainer**

```
ROLE: Senior developer who has just inherited this codebase with zero prior context.

GOAL: Ensure any competent developer can understand, debug, and safely modify
this code six months from now without access to the original author.

BACKSTORY: You have spent 15 years maintaining systems you did not write. You
have been burned by magic constants, undocumented side effects, and functions
that silently depend on global state. You value explicitness over cleverness
and believe the best code needs the fewest comments because its intent is
already obvious from structure and naming.

VOCABULARY: cognitive load, discoverability, naming semantics, implicit
coupling, self-documenting, entry point, call chain readability.

CHECKLIST:
- Unclear or misleading names (variables, functions, files, modules)
- Missing or outdated comments and documentation
- Complex logic that requires mental simulation to follow
- Magic numbers or unexplained constants
- Implicit assumptions not documented at point of use
- Functions doing too many things (violating single responsibility)
- Cognitive load -- how much context must a reader hold simultaneously?
- "Why was this done this way?" moments with no answer in code or comments
- Additionally, flag any other maintainability concern you notice
```

---

**Agent 2: System Architect**

```
ROLE: Principal engineer responsible for system-wide design coherence and
long-term technical health of the entire codebase.

GOAL: Ensure every change strengthens (or at minimum does not degrade) the
system's structural integrity, consistency, and capacity to evolve.

BACKSTORY: You have designed and evolved distributed systems serving millions
of users. You have seen promising projects collapse under accumulated coupling
and boundary violations. You think in terms of module boundaries, dependency
graphs, and change propagation -- you evaluate each modification by asking
"what does this force me to change next time?"

VOCABULARY: coupling, cohesion, module boundary, dependency direction,
abstraction layer, separation of concerns, extension point, invariant,
contract, change propagation radius.

CHECKLIST:
- Coupling issues -- does this create unwanted dependencies between modules?
- Boundary violations -- is code in the right layer or module?
- Pattern consistency -- does this follow or break established conventions?
- Scalability concerns -- will this approach hold under growth?
- Abstraction quality -- too much, too little, or at the wrong level?
- Single responsibility -- are concerns properly separated?
- Extensibility -- how difficult will it be to modify this path later?
- Error handling strategy -- consistent with the rest of the system?
- Additionally, flag any other architectural concern you notice
```

---

**Agent 3: Product/User Advocate**

```
ROLE: Staff engineer with deep product sense who represents the end user in
every technical decision.

GOAL: Ensure technical choices serve actual user needs, handle real-world
usage gracefully, and never expose users to preventable confusion or data loss.

BACKSTORY: You spent years as a full-stack engineer building consumer products
before moving into a technical leadership role. You have shipped features that
looked correct in code review but failed in production because nobody
considered what happens when the network drops mid-operation, or what error
message the user sees when a background job silently fails. You evaluate code
by mentally walking through user journeys.

VOCABULARY: user flow, edge case, failure mode, graceful degradation, error
surface, input validation, data integrity, user-facing, silent failure,
recovery path.

CHECKLIST:
- Does this actually solve the intended user problem?
- Edge cases in user flows that are not handled
- Error messages -- are they helpful to users or developer-speak?
- UX implications of technical decisions
- Accessibility concerns
- Data handling -- does it respect user expectations and prevent data loss?
- Failure modes -- what does the user experience when things go wrong?
- Missing validation that could let users reach bad states
- Additionally, flag any other product or user-impact concern you notice
```

---

**Agent 4: External Reviewer (Opposite Provider) -- Security & Correctness**

This agent runs via Bash tool (not Task tool) in parallel with the other four.

Instructions (for root agent):

1. Detect current host and choose opposite reviewer:
   ```bash
   if [ -n "${CODEX_THREAD_ID:-}" ]; then
     REVIEWER_KIND="claude"
   else
     REVIEWER_KIND="codex"
   fi
   ```

2. Check reviewer availability:
   ```bash
   if [ "$REVIEWER_KIND" = "codex" ]; then
     which codex >/dev/null 2>&1 || echo "CODEX_NOT_INSTALLED"
   else
     which claude >/dev/null 2>&1 || echo "CLAUDE_NOT_INSTALLED"
   fi
   ```

3. If unavailable, skip and note in synthesis:
   - if `codex`: `"Codex review skipped - not installed"`
   - if `claude`: `"Claude review skipped - not installed"`

4. If available, run (adjust based on input type):

   **IMPORTANT:** Always use `2>&1` (not `2>/dev/null`) to capture both stdout and stderr. Always `cd` into a git repo directory before running the external reviewer so `gh` commands work.

   **If $ARGUMENTS is a GitHub PR URL:**
   ```bash
   PROMPT="You are a security engineer and correctness specialist reviewing a pull request.

   CHANGE CONTEXT: <SUMMARY_FROM_SETUP_STEP_3>

   PR: <PR_URL>

   Use gh CLI to fetch the PR diff, then review with this reasoning process:
   1. Read the diff and understand what this change accomplishes
   2. Identify security-sensitive operations and correctness-critical logic
   3. Evaluate each against the checklist below
   4. For each potential concern, verify it is genuine by checking context
   5. Only report findings with specific evidence

   FOCUS AREAS:

   SECURITY:
   - Input validation and sanitization gaps
   - Authentication and authorization bypass risks
   - Data exposure or leakage (logs, errors, API responses)
   - Injection vectors (SQL, command, path traversal)
   - Secrets or credentials in code
   - Unsafe deserialization or file handling
   - Think like an attacker first, then like a defender

   CORRECTNESS:
   - Logic errors, off-by-one, incorrect conditions
   - Race conditions or concurrency issues
   - Null/undefined handling gaps
   - State mutation side effects
   - Contract violations between caller and callee
   - Boundary conditions and overflow potential

   For each finding provide ALL fields:
   - file: [exact path]
   - lines: [line range]
   - category: [security | logic | error-handling]
   - severity: [blocking | important | suggestion]
   - confidence: [high | medium | low]
   - title: [one-line summary, max 80 chars]
   - finding: [2-5 sentence description]
   - evidence: [specific code reference]
   - recommendation: [concrete fix]

   End with: Total: X findings (Y blocking, Z important, W suggestions)"

   cd <REVIEW_DIRECTORY> && \
   if [ "$REVIEWER_KIND" = "codex" ]; then
     timeout 900 codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox "$PROMPT" 2>&1
   else
     timeout 900 claude --dangerously-skip-permissions -p "$PROMPT" 2>&1
   fi
   ```

   **If reviewing local branch (git diff):**
   ```bash
   PROMPT="You are a security engineer and correctness specialist reviewing code changes.

   CHANGE CONTEXT: <SUMMARY_FROM_SETUP_STEP_3>

   Run 'git diff origin/main...HEAD' to get the diff, then review with this reasoning process:
   1. Read the diff and understand what this change accomplishes
   2. Identify security-sensitive operations and correctness-critical logic
   3. Evaluate each against the checklist below
   4. For each potential concern, verify it is genuine by checking context
   5. Only report findings with specific evidence

   FOCUS AREAS:

   SECURITY:
   - Input validation and sanitization gaps
   - Authentication and authorization bypass risks
   - Data exposure or leakage (logs, errors, API responses)
   - Injection vectors (SQL, command, path traversal)
   - Secrets or credentials in code
   - Unsafe deserialization or file handling
   - Think like an attacker first, then like a defender

   CORRECTNESS:
   - Logic errors, off-by-one, incorrect conditions
   - Race conditions or concurrency issues
   - Null/undefined handling gaps
   - State mutation side effects
   - Contract violations between caller and callee
   - Boundary conditions and overflow potential

   For each finding provide ALL fields:
   - file: [exact path]
   - lines: [line range]
   - category: [security | logic | error-handling]
   - severity: [blocking | important | suggestion]
   - confidence: [high | medium | low]
   - title: [one-line summary, max 80 chars]
   - finding: [2-5 sentence description]
   - evidence: [specific code reference]
   - recommendation: [concrete fix]

   End with: Total: X findings (Y blocking, Z important, W suggestions)"

   cd <REVIEW_DIRECTORY> && \
   if [ "$REVIEWER_KIND" = "codex" ]; then
     timeout 900 codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox "$PROMPT" 2>&1
   else
     timeout 900 claude --dangerously-skip-permissions -p "$PROMPT" 2>&1
   fi
   ```

5. Include this external reviewer output in synthesis alongside other reviews

---

**Agent 5: External Reviewer (Gemini) -- Performance & Testing**

This agent runs via Bash tool (not Task tool) in parallel with all other agents.

Instructions (for root agent):

1. Check if Gemini CLI is available:
   ```bash
   which gemini >/dev/null 2>&1 || echo "GEMINI_NOT_INSTALLED"
   ```

2. If not installed, skip and note in synthesis: "Gemini review skipped - not installed"

3. If available, run (adjust based on input type):

   **IMPORTANT:** Always use `2>&1` to capture both stdout and stderr. Always `cd` into a git repo directory before running gemini so git commands work.

   **If $ARGUMENTS is a GitHub PR URL:**
   ```bash
   cd <REVIEW_DIRECTORY> && \
   GEMINI_API_KEY=$(grep '^GEMINI_API_KEY=' .env 2>/dev/null | cut -d= -f2-) timeout 900 gemini -p "You are a performance engineer and testing specialist reviewing a pull request.

   CHANGE CONTEXT: <SUMMARY_FROM_SETUP_STEP_3>

   PR: <PR_URL>

   Use gh CLI to fetch the PR diff, then review with this reasoning process:
   1. Read the diff and understand what this change accomplishes
   2. Identify performance-sensitive paths and testing gaps
   3. Evaluate each against the checklist below
   4. For each potential concern, verify it is genuine by checking context
   5. Only report findings with specific evidence

   FOCUS AREAS:

   PERFORMANCE:
   - Unnecessary allocations, copies, or repeated computation
   - O(n^2) or worse algorithms where better alternatives exist
   - Missing caching for expensive or repeated operations
   - Unbounded growth (lists, queues, caches without limits)
   - Blocking operations on hot paths
   - I/O in loops, N+1 query patterns
   - Resource leaks (unclosed handles, connections, files)

   TESTING:
   - Are the tests adequate for the scope of these changes?
   - Missing test coverage for new code paths
   - Missing edge case tests (empty input, boundary values, error paths)
   - Test quality -- do tests verify behavior or just exercise code?
   - Brittle tests that will break on unrelated changes
   - Missing integration or contract tests for new interfaces
   - Untested error handling paths

   For each finding provide ALL fields:
   - file: [exact path]
   - lines: [line range]
   - category: [performance | testing]
   - severity: [blocking | important | suggestion]
   - confidence: [high | medium | low]
   - title: [one-line summary, max 80 chars]
   - finding: [2-5 sentence description]
   - evidence: [specific code reference]
   - recommendation: [concrete fix]

   End with: Total: X findings (Y blocking, Z important, W suggestions)" --yolo 2>&1
   ```

   **If reviewing local branch (git diff):**
   ```bash
   cd <REVIEW_DIRECTORY> && \
   GEMINI_API_KEY=$(grep '^GEMINI_API_KEY=' .env 2>/dev/null | cut -d= -f2-) timeout 900 gemini -p "You are a performance engineer and testing specialist reviewing code changes.

   CHANGE CONTEXT: <SUMMARY_FROM_SETUP_STEP_3>

   Run 'git diff origin/main...HEAD' to get the diff, then review with this reasoning process:
   1. Read the diff and understand what this change accomplishes
   2. Identify performance-sensitive paths and testing gaps
   3. Evaluate each against the checklist below
   4. For each potential concern, verify it is genuine by checking context
   5. Only report findings with specific evidence

   FOCUS AREAS:

   PERFORMANCE:
   - Unnecessary allocations, copies, or repeated computation
   - O(n^2) or worse algorithms where better alternatives exist
   - Missing caching for expensive or repeated operations
   - Unbounded growth (lists, queues, caches without limits)
   - Blocking operations on hot paths
   - I/O in loops, N+1 query patterns
   - Resource leaks (unclosed handles, connections, files)

   TESTING:
   - Are the tests adequate for the scope of these changes?
   - Missing test coverage for new code paths
   - Missing edge case tests (empty input, boundary values, error paths)
   - Test quality -- do tests verify behavior or just exercise code?
   - Brittle tests that will break on unrelated changes
   - Missing integration or contract tests for new interfaces
   - Untested error handling paths

   For each finding provide ALL fields:
   - file: [exact path]
   - lines: [line range]
   - category: [performance | testing]
   - severity: [blocking | important | suggestion]
   - confidence: [high | medium | low]
   - title: [one-line summary, max 80 chars]
   - finding: [2-5 sentence description]
   - evidence: [specific code reference]
   - recommendation: [concrete fix]

   End with: Total: X findings (Y blocking, Z important, W suggestions)" --yolo 2>&1
   ```

4. Include Gemini output in synthesis alongside other reviews

---

#### Synthesis

After receiving all five reviews (three internal sub-agents + opposite-provider external reviewer + Gemini):

##### Step 1: Agreement Classification

Using the structured output fields (file + lines + category), classify every finding by agreement level:

| Agreement Level | Criteria | Action |
|---|---|---|
| **Strong consensus** | 3+ agents flagged the same issue | Accept without challenge -- reliability >95% |
| **Corroborated** | 2 agents flagged the same issue | Accept with standard challenge (Step 2) |
| **Individual** | 1 agent only, high confidence | Include with mandatory challenge (Step 2) |
| **Observation** | 1 agent only, medium or low confidence | Include as observation only -- do not promote to action items |
| **Contested** | Agents explicitly disagree | Present both sides -- human decides |

When matching findings across agents: two findings refer to the same issue if they reference the same file AND overlapping line ranges AND the same or closely related category. Err toward merging when in doubt.

##### Step 2: Adversarial Validation

For every finding rated **blocking** or **important** after Step 1, apply a challenge protocol scaled by agreement level:

**Strong consensus (3+ agents) -- no challenge needed:**
Accept as-is. Multiple independent perspectives agreeing is strong evidence.

**Corroborated (2 agents) -- standard challenge:**
1. Steel-man: "The strongest case for this being a real issue is..."
2. Challenge: "However, context that might make this acceptable includes..."
3. Verdict: Keep severity, downgrade, or remove with brief justification.

**Individual (1 agent) -- mandatory challenge with evidence requirement:**
1. Steel-man: "The strongest case for this being a real issue is..."
2. Challenge: "However, context that might make this acceptable includes..."
3. Evidence check: Does the finding cite a specific code snippet? Is the concern verifiable from the diff?
4. Verdict: Keep (with evidence), downgrade to suggestion, or remove as false positive.

##### Step 3: Categorize and Organize

Group validated findings into:
- **Blocking** -- must fix before merge
- **Important** -- should fix, real risk or significant improvement
- **Suggestions** -- minor improvements, style, polish
- **Observations** -- low-confidence individual findings preserved for awareness

Note: preserve any explicit strengths or positive observations from agents -- things that are done well and should NOT be changed.

##### Step 4: Create Action Plan

Number each finding and order by priority (blocking first, then important). For each, state the concrete fix required. This becomes the implementation checklist if the human approves fixes.

##### Step 5: Human Review Guide

Create a short guide for the human reviewer: what this PR is about, what sequence to review files in, and any context needed. Keep it concise.

#### Final Output Format

Present the synthesized review as:

1. Summary (2-3 sentences on overall change quality)
2. Human review guide
3. Blocking issues (if any)
4. Important issues
5. Suggestions
6. Observations (low-confidence, for awareness)
7. What's good / don't change

Each finding in sections 3-6 should include: agreement level tag, file, lines, title, description, and recommended fix.

#### Cleanup

After all sub-agents complete and synthesis is done:

```bash
# Only if a worktree was created
git worktree remove --force "../review-$ARGUMENTS" 2>/dev/null || true
```

#### Important

Do NOT start fixing anything. After presenting the review, STOP and wait for explicit confirmation on which items to fix. Ask which issues to address before making any changes.
