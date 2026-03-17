---
name: compound
description: "This skill should be used when the user has solved a non-trivial problem and wants to document the solution for future reference. Triggers on phrases like 'that worked', 'fixed it', 'problem solved', 'figured it out', or when explicitly invoked with /compound."
allowed-tools: Read, Bash, Glob, Grep, Write, AskUserQuestion, Task
---

# Compound: Capture Learnings

Coordinate multiple subagents working in parallel to document a recently solved problem.

## Purpose

Captures problem solutions while context is fresh, creating structured documentation in `docs/solutions/` with YAML frontmatter for searchability and future reference. Uses parallel subagents for maximum efficiency.

**Why "compound"?** Each documented solution compounds your team's knowledge. The first time you solve a problem takes research. Document it, and the next occurrence takes minutes. Knowledge compounds.

## Auto-Invoke

This skill activates when:
- User explicitly runs `/compound`
- User says: "that worked", "it's fixed", "working now", "problem solved", "figured it out"
- A debugging session concludes successfully

Use `/compound [context]` to document immediately without waiting for auto-detection.

## Preconditions

Before proceeding, verify:
- Problem has been solved (not in-progress)
- Solution has been verified working
- Non-trivial problem (not a simple typo or obvious error)

If the problem is trivial, suggest skipping documentation.

## Step 1: Determine Scope (BLOCKING - Ask User)

Use `AskUserQuestion` to determine where this learning belongs:

```
I'd like to document this solution. First, is this learning:

1. **Project-specific** — Applies only to this codebase
2. **Global/reusable** — Applies across projects
```

**Routing:**
- **Project-specific** → `./docs/solutions/` (current project)
- **Global** → `~/.claude/docs/solutions/` (claude-corps, shared across all projects)

## Step 2: Launch Parallel Subagents

Launch ALL of these subagents **in parallel** using the Task tool:

### Agent 1: Context Analyzer
```
Task general-purpose: "Analyze the conversation history to identify:
- Problem type and affected component/module
- Observable symptoms and error messages
- Investigation steps taken
- Technologies and frameworks involved
- Whether this is a bug fix (is_bug_fix: true/false)
- Whether a regression test was added (has_regression_test: true/false)
- List of test files modified (test_files_modified: [])

Return a YAML frontmatter skeleton with:
scope, module, date, problem_type, symptoms, root_cause, severity, tags, is_bug_fix, has_regression_test, test_files_modified

Use this schema:
  problem_type: one of [build-error, test-failure, runtime-error, performance, database, security, integration, logic-error, workflow]
  root_cause: one of [missing-dependency, config-error, race-condition, incorrect-assumption, api-change, missing-validation, resource-exhaustion, logic-flaw, documentation-gap, other]
  severity: one of [critical, high, medium, low]
  is_bug_fix: boolean
  has_regression_test: boolean
  test_files_modified: list of file paths"
```

### Agent 2: Solution Extractor
```
Task general-purpose: "Analyze the conversation to extract:
- All investigation steps tried (what didn't work and why)
- The root cause (technical explanation)
- The working solution with specific code/config changes
- Code examples that demonstrate the fix

Return structured content for the Solution, Investigation, and Root Cause sections of a solution document."
```

### Agent 3: Related Docs Finder
```
Task general-purpose: "Search for related documentation:
1. Search docs/solutions/ for related files: grep -ri '<keywords>' docs/solutions/ --include='*.md' -l
2. Search ~/.claude/docs/solutions/ for global solutions: grep -ri '<keywords>' ~/.claude/docs/solutions/ --include='*.md' -l
3. Check for related GitHub issues if in a git repo

Return: list of related documents with brief relevance notes, and any cross-reference links."
```

### Agent 4: Prevention Strategist
```
Task general-purpose: "Based on the problem and solution discussed in this session:
- Develop prevention strategies (how to avoid this in the future)
- Suggest test cases that would catch this problem
- Identify patterns that could indicate similar issues elsewhere
- Recommend any CLAUDE.md additions if this is a project-wide gotcha

Return structured prevention content."
```

### Agent 5: Category Classifier
```
Task general-purpose: "Based on the problem type, determine:
1. The optimal docs/solutions/ category directory
2. A filename following the format: [symptom-slug]-[module]-YYYYMMDD.md

Categories:
  build-error → build-errors/
  test-failure → test-failures/
  runtime-error → runtime-errors/
  performance → performance/
  database → database/
  security → security/
  integration → integration/
  logic-error → logic-errors/
  workflow → workflow/

Rules for filename:
- Lowercase with hyphens
- Symptom first (what you'd search for)
- Module second (where it happened)
- Date last (for versioning)

Return: category directory and filename."
```

## Step 3: Assemble and Write Document

After all agents complete, assemble the document:

1. **Check for duplicates** — If Related Docs Finder found an existing similar solution, ask user:
   - Update the existing document
   - Create a new document (different enough to warrant separation)
   - Skip documentation (already covered)

2. **Create directory if needed:**
```bash
mkdir -p [target-dir]/[category]
```

3. **Write the document** using outputs from all agents:

```markdown
---
[frontmatter from Context Analyzer]
---

# [Descriptive Title]

## Symptom

[From Context Analyzer — observable symptoms, error messages]

## Investigation

[From Solution Extractor — steps tried, what didn't work]

## Root Cause

[From Solution Extractor — what was actually wrong]

## Solution

[From Solution Extractor — specific code/config changes]

## Prevention

[From Prevention Strategist — how to avoid in future]

## Related

[From Related Docs Finder — links to related docs, issues, solutions]
```

## Step 3.5: Regression Test Prompt (Bug Fixes Only)

**Only triggers when `is_bug_fix: true` from Context Analyzer output.**

Check recent commits for test file changes:

```bash
git diff --name-only HEAD~5 | grep -E '(test_|_test\.|\.test\.|spec\.)'
```

If no regression test is detected (`has_regression_test: false` AND no test files in git diff), use `AskUserQuestion`:

```
This was a bug fix. A regression test helps prevent this bug from recurring.

1. **Yes — draft regression test** (I'll generate test code targeting your project's test framework)
2. **Already added** (I'll note the test files from your recent changes)
3. **No — skip** (I'll note this was skipped)
```

**If "Yes — draft regression test":**
- Launch a subagent (Task tool, general-purpose, model: sonnet) to write a regression test:
  - Target the project's test framework (detect from existing test files: pytest, jest, vitest, etc.)
  - Test the specific scenario that triggered the bug
  - Include a comment explaining what bug this prevents
- Add a "Regression Test" section to the solution document with the generated test code and recommended file path

**If "Already added":**
- Note the test files from `git diff` in the document under a "Regression Test" section

**If "No — skip":**
- Note as skipped with the user's reason in the document

Add to YAML frontmatter: `regression_test_status: recommended|added|skipped`

## Step 4: Optional Specialized Agent Review

Based on the problem type detected by Context Analyzer, optionally run a domain expert for validation:

| Problem Type | Agent | What It Checks |
|-------------|-------|----------------|
| performance | `performance-oracle` | Validates optimization approach |
| security | `security-sentinel` | Reviews for remaining vulnerabilities |
| database | `data-integrity-guardian` | Reviews migration/query safety |
| Any code-heavy fix | `code-simplicity-reviewer` | Ensures solution is minimal |

Use `AskUserQuestion`: "Want me to run a specialized review on this solution?"

If yes, launch the appropriate agent against the solution document content.

## Step 5: Decision Menu

After creating the document, present:

```
Solution documented at: [path]/[category]/[filename].md

What would you like to do next?
1. Continue working (done documenting)
2. Add a reminder to CLAUDE.md (if this is a project-wide gotcha)
3. Create a follow-up task (if there's related work to do)
4. Link related documentation
```

## The Compounding Philosophy

This creates a compounding knowledge system:

1. First time you solve "N+1 query in brief generation" → Research (30 min)
2. Document the solution → `docs/solutions/performance/n-plus-one-briefs.md` (5 min)
3. Next time similar issue occurs → Quick lookup (2 min)
4. Knowledge compounds → Team gets smarter

```
Build → Test → Find Issue → Research → Improve → Document → Validate → Deploy
    ↑                                                                      ↓
    └──────────────────────────────────────────────────────────────────────┘
```

**Each unit of engineering work should make subsequent units of work easier—not harder.**

## Directory Setup

If directories don't exist, create them:

```bash
# Project-specific
mkdir -p docs/solutions/{build-errors,test-failures,runtime-errors,performance,database,security,integration,logic-errors,workflow}

# Global (should already exist via claude-corps)
mkdir -p ~/.claude/docs/solutions/{build-errors,test-failures,runtime-errors,performance,database,security,integration,logic-errors,workflow}
```

## Important Notes

- **Always ask about scope first** — Route to the right location before gathering details
- Keep solutions focused — one problem per document
- Use searchable terms in symptoms and tags
- Link to related solutions when patterns repeat
- Global learnings compound across ALL projects — high value for reusable knowledge
- Project-specific learnings stay with the project — don't pollute global with project details
