---
name: best-practices
description: >-
  Transforms vague prompts into optimized Claude Code prompts. Adds verification,
  specific context, constraints, and proper phasing. Invoke with /best-practices.
---

# Best Practices — Prompt Transformer

> Transform prompts by adding what Claude needs to succeed.

## Start Here

Based on user's request:

**User provides a prompt to transform:**
→ Ask using AskUserQuestion:
  - **Question:** "How should I improve this prompt?"
  - **Header:** "Mode"
  - **Options:**
    1. **Transform directly** — "I'll apply best practices and output an improved version"
    2. **Build context first** — "I'll gather codebase context and intent analysis first"

**User asks to learn/understand:**
→ Show the 5 Transformation Principles section

**User asks for examples:**
→ Link to references/before-after-examples.md

**User asks to evaluate a prompt:**
→ Use the Success Criteria eval rubric at the end of this document

---

## If "Transform directly"

Apply the 5 principles below and output the improved prompt immediately.

## If "Build context first"

Launch 3 parallel agents to gather context:

```
Run these agents IN PARALLEL using the Task tool:

- Task task-intent-analyzer("[user's prompt]")
- Task best-practices-referencer("[user's prompt]")
- Task codebase-context-builder("[user's prompt]")
```

### What Each Agent Returns

| Agent | Mission | Returns |
|-------|---------|---------|
| **task-intent-analyzer** | Understand what user is trying to do | Task type, gaps, edge cases, transformation guidance |
| **best-practices-referencer** | Find relevant patterns from references/ | Matching examples, anti-patterns to avoid, transformation rules |
| **codebase-context-builder** | Explore THIS codebase | Specific file paths, similar implementations, conventions |

### After Agents Return

1. **Synthesize findings** — Combine intent + best practices + codebase context
2. **Apply matching patterns** — Use examples from best-practices-referencer as templates
3. **Ground in codebase** — Add specific file paths from codebase-context-builder
4. **Transform the prompt** — Apply the 5 principles with all gathered context
5. **Output** — Show improved prompt with before/after comparison

### Agent Definitions

The agents are defined in `agents/`:
- `agents/task-intent-analyzer.md` — Analyzes intent, gaps, and edge cases
- `agents/best-practices-referencer.md` — Finds relevant examples and patterns from references/
- `agents/codebase-context-builder.md` — Explores codebase for files and conventions

---

## Transformation Workflow

When transforming (after mode selection):

1. **Identify what's missing** — Check against the 5 principles below
2. **Add missing elements** — Verification, context, constraints, phases, rich content
3. **Output the improved prompt** — In a code block, ready to copy-paste
4. **Show what changed** — Brief comparison of before/after

---

## The 5 Transformation Principles

Apply these in order of priority:

### 1. Add Verification (Highest Priority)

**The single highest-leverage improvement.** Claude performs dramatically better when it can verify its own work.

| Missing | Add |
|---------|-----|
| No success criteria | Test cases with expected inputs/outputs |
| UI changes | "take screenshot and compare to design" |
| Bug fixes | "write a failing test, then fix it" |
| Build issues | "verify the build succeeds after fixing" |
| Refactoring | "run the test suite after each change" |
| No root cause enforcement | "address root cause, don't suppress error" |
| No verification report | "summarize what you ran and what passed" |

```
BEFORE: "implement email validation"
AFTER:  "write a validateEmail function. test cases: user@example.com → true,
         invalid → false, user@.com → false. run the tests after implementing"
```

```
BEFORE: "fix the API error"
AFTER:  "the /api/orders endpoint returns 500 for large orders. check
         OrderService.ts for the error. address the root cause, don't suppress
         the error. after fixing, run the test suite and summarize what passed
         and what you verified."
```

### 2. Provide Specific Context

Replace vague references with precise locations and details.

| Vague | Specific |
|-------|----------|
| "the code" | `src/auth/login.ts` |
| "the bug" | "users report X happens when Y" |
| "the API" | "the /api/users endpoint in routes.ts" |
| "that function" | `processPayment()` on line 142 |

**Four ways to add context:**

| Strategy | Example |
|----------|---------|
| **Scope the task** | "write a test for foo.py covering the edge case where user is logged out. avoid mocks." |
| **Point to sources** | "look through ExecutionFactory's git history and summarize how its API evolved" |
| **Reference patterns** | "look at HotDogWidget.php and follow that pattern for the calendar widget" |
| **Describe symptoms** | "users report login fails after session timeout. check src/auth/, especially token refresh" |

**Respect Project CLAUDE.md:**

If the project has a CLAUDE.md, the transformed prompt should:
- Not contradict project conventions
- Reference project-specific patterns when relevant
- Note any project constraints that apply

```
BEFORE: "add a new API endpoint"
AFTER:  "add a GET /api/products endpoint. check CLAUDE.md for API conventions
         in this project. follow the pattern in routes/users.ts. run the API
         tests after implementing."
```

```
BEFORE: "fix the login bug"
AFTER:  "users report login fails after session timeout. check the auth flow
         in src/auth/, especially token refresh. write a failing test that
         reproduces the issue, then fix it"
```

### 3. Add Constraints

Tell Claude what NOT to do. Prevents over-engineering and unwanted changes.

| Constraint Type | Examples |
|-----------------|----------|
| **Dependencies** | "no new libraries", "only use existing deps" |
| **Testing** | "avoid mocks", "use real database in tests" |
| **Scope** | "don't refactor unrelated code", "only touch auth module" |
| **Approach** | "address root cause, don't suppress error", "keep backward compat" |
| **Patterns** | "follow existing codebase conventions", "match the style in utils.ts" |

```
BEFORE: "add a calendar widget"
AFTER:  "implement a calendar widget with month selection and year pagination.
         follow the pattern in HotDogWidget.php. build from scratch without
         libraries other than the ones already used in the codebase"
```

### 4. Structure Complex Tasks in Phases

For larger tasks, separate exploration from implementation.

**The 4-Phase Pattern:**

```
Phase 1: EXPLORE
"read src/auth/ and understand how we handle sessions and login.
 also look at how we manage environment variables for secrets."

Phase 2: PLAN
"I want to add Google OAuth. What files need to change?
 What's the session flow? Create a plan."

Phase 3: IMPLEMENT
"implement the OAuth flow from your plan. write tests for the
 callback handler, run the test suite and fix any failures."

Phase 4: COMMIT
"commit with a descriptive message and open a PR"
```

**When to use phases:**
- Uncertain about the approach
- Change modifies multiple files
- Unfamiliar with the code being modified

**Skip phases when:**
- Could describe the diff in one sentence
- Fixing a typo, adding a log line, renaming a variable

```
BEFORE: "add OAuth"
AFTER:  "read src/auth/ and understand current session handling. create a plan
         for adding OAuth. then implement following the plan. write tests and
         verify they pass"
```

### 5. Include Rich Content

Provide supporting materials that Claude can use directly.

| Content Type | How to Provide |
|--------------|----------------|
| **Files** | Use `@filename` to reference files |
| **Images** | Paste screenshots directly |
| **Errors** | Paste actual error messages, not descriptions |
| **Logs** | Pipe with `cat error.log \| claude` |
| **URLs** | Link to relevant documentation |

```
BEFORE: "make the dashboard look better"
AFTER:  "[paste screenshot] implement this design for the dashboard.
         take a screenshot of the result and compare it to the original.
         list any differences and fix them. ensure responsive behavior
         at 768px and 1024px breakpoints"
```

```
BEFORE: "the build is failing"
AFTER:  "the build fails with this error: [paste actual error]. fix it
         and verify the build succeeds. address the root cause, don't
         suppress the error"
```

---

## Output Format

When transforming a prompt, output:

```markdown
**Original:** [their prompt]

**Improved:**
```
[transformed prompt in code block]
```

**Added:**
- [what was missing and added]
- [another improvement]
- [etc.]
```

---

## Quick Transformation Examples

### Bug Fix
```
BEFORE: "fix the login bug"

AFTER: "users report login fails after session timeout. check the auth flow
in src/auth/, especially token refresh. write a failing test that reproduces
the issue, then fix it. verify by running the auth test suite."

ADDED: symptom, location, verification (failing test), success criteria
```

### Feature Implementation
```
BEFORE: "add a search feature"

AFTER: "implement search for the products page. look at how filtering works
in ProductList.tsx for the pattern. search should filter by name and category.
add tests for: empty query returns all, partial match works, no results shows
message. no external search libraries."

ADDED: location, reference pattern, specific behavior, test cases, constraint
```

### Refactoring
```
BEFORE: "make the code better"

AFTER: "refactor utils.js to use ES2024 features while maintaining the same
behavior. specifically: convert callbacks to async/await, use optional
chaining, add proper TypeScript types. run the existing test suite after
each change to ensure nothing breaks."

ADDED: specific changes, constraint (same behavior), verification after each step
```

### Testing
```
BEFORE: "add tests for foo.py"

AFTER: "write tests for foo.py covering the edge case where the user is
logged out. avoid mocks. use the existing test patterns in tests/. test
cases: logged_out_user returns 401, expired_session redirects to login,
invalid_token raises AuthError."

ADDED: specific edge case, constraint (no mocks), pattern reference, test cases
```

### Debugging
```
BEFORE: "the API is slow"

AFTER: "the /api/orders endpoint takes 3+ seconds. profile the database
queries in OrderService.ts. look for N+1 queries or missing indexes.
fix the performance issue and verify response time is under 500ms."

ADDED: specific endpoint, location, what to look for, measurable success criteria
```

### UI Changes
```
BEFORE: "fix the button styling"

AFTER: "[paste screenshot of design] update the primary button to match this
design. check Button.tsx and the theme in tailwind.config.js. take a
screenshot after changes and compare to the design. list any differences."

ADDED: design reference, file locations, visual verification
```

### Exploration
```
BEFORE: "how does auth work?"

AFTER: "read src/auth/ and explain how authentication works in this codebase.
cover: how sessions are created, how tokens are refreshed, where secrets
are stored. summarize in a markdown doc."

ADDED: specific files, specific questions to answer, output format
```

### Migration
```
BEFORE: "upgrade to React 18"

AFTER: "migrate from React 17 to React 18. first, read the migration guide
at [URL]. then identify all components using deprecated APIs. update one
component at a time, running tests after each. don't change unrelated code."

ADDED: phased approach, reference docs, incremental verification, scope constraint
```

### With Verification Report
```
BEFORE: "fix the API error"

AFTER: "the /api/orders endpoint returns 500 for large orders. check
OrderService.ts for the error. address the root cause, don't suppress
the error. after fixing, run the test suite and summarize what passed
and what you verified."

ADDED: symptom, location, root cause enforcement, verification report
```

---

## Transformation Checklist

Before outputting, verify the improved prompt has:

- [ ] **Verification** — How to know it worked (tests, screenshot, output)
- [ ] **Location** — Specific files, functions, or areas
- [ ] **Constraints** — What NOT to do
- [ ] **Single task** — Not compound (split if needed)
- [ ] **Phases** — If complex, structured as explore → plan → implement
- [ ] **Root cause** — For bugs: "address root cause, don't suppress"
- [ ] **CLAUDE.md** — Respect project conventions if they exist

---

## Quick Prompt Quality Check

Rate the prompt against these dimensions:

| Dimension | 0 (Missing) | 1 (Partial) | 2 (Complete) |
|-----------|-------------|-------------|--------------|
| **Verification** | None | "test it" | Specific test cases + report |
| **Location** | "the code" | "auth module" | `src/auth/login.ts:42` |
| **Constraints** | None | Implied | "avoid X, no Y, root cause only" |
| **Scope** | Vague | Partial | Single clear task |

**Quick assessment:**
- 0-3: Needs significant work
- 4-5: Needs some improvements
- 6-8: Good, minor tweaks

---

## Fallback: If Still Too Vague

If user chose "Transform directly" but the prompt lacks enough context, ask one natural question:

> "What would Claude need to know to do this well?"

Don't interrogate — one question is enough. Transform with what you learn.

---

## Common Anti-Patterns to Fix

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "fix the bug" | No symptom, no location | Add what users report + where to look |
| "add tests" | No scope, no cases | Specify edge cases + test patterns |
| "make it better" | No criteria for "better" | Define specific improvements |
| "implement X" | No verification | Add test cases or success criteria |
| "update the code" | No constraints | Add what to preserve, what to avoid |

---

## Success Criteria — Prompt Quality Eval

A well-transformed prompt passes these checks:

### Principle 1: Verification ✅
| Check | Pass | Fail |
|-------|------|------|
| Has success criteria | "run tests", "screenshot matches" | Nothing |
| Measurable outcome | "response < 500ms" | "make it faster" |
| Self-verifiable | Claude can check its own work | Requires human judgment |
| Root cause enforced | "don't suppress error" | Silent about approach |

### Principle 2: Specificity ✅
| Check | Pass | Fail |
|-------|------|------|
| File locations | `src/auth/login.ts` | "the auth code" |
| Function/class names | `processPayment()` | "that function" |
| Line numbers (if relevant) | `:42` | "somewhere in there" |
| CLAUDE.md respected | "check project conventions" | Ignores project rules |

### Principle 3: Constraints ✅
| Check | Pass | Fail |
|-------|------|------|
| What NOT to do | "avoid mocks", "no new deps" | Open-ended |
| Scope boundaries | "only touch auth module" | Unlimited scope |
| Pattern to follow | "match UserService.ts style" | No reference |

### Principle 4: Structure ✅
| Check | Pass | Fail |
|-------|------|------|
| Single task | One clear objective | Multiple goals |
| Phased (if complex) | "explore → plan → implement" | Jump straight to code |
| Appropriate depth | Matches task complexity | Over/under-specified |

### Principle 5: Rich Content ✅
| Check | Pass | Fail |
|-------|------|------|
| Actual errors | Pasted error message | "it's broken" |
| Screenshots (UI) | Image attached | "the button looks wrong" |
| File references | `@filename` or path | "that file" |

### Overall Quality Score

| Score | Meaning | Principles Passed |
|-------|---------|-------------------|
| ⭐⭐⭐⭐⭐ | Excellent | All 5 |
| ⭐⭐⭐⭐ | Good | 4 of 5 |
| ⭐⭐⭐ | Acceptable | 3 of 5 |
| ⭐⭐ | Needs work | 2 of 5 |
| ⭐ | Poor | 1 or 0 |

**Target:** Every transformed prompt should score ⭐⭐⭐⭐ or ⭐⭐⭐⭐⭐

---

## Reference Files

For more examples and patterns:

- **50+ Examples**: See [references/before-after-examples.md](references/before-after-examples.md)
- **Prompt Templates**: See [references/prompt-patterns.md](references/prompt-patterns.md)
- **Task Workflows**: See [references/common-workflows.md](references/common-workflows.md)
- **What to Avoid**: See [references/anti-patterns.md](references/anti-patterns.md)
- **Official Guide**: See [references/best-practices-guide.md](references/best-practices-guide.md)

---

## Sources

- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — Official documentation
- [Claude Code Skills](https://code.claude.com/docs/en/skills) — Skill authoring guide
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) — General prompting patterns
- [Dicklesworthstone meta_skill](https://github.com/Dicklesworthstone/meta_skill) — "THE EXACT PROMPT" pattern
