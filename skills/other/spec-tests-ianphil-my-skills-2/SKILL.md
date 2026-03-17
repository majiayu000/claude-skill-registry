---
name: spec-tests
description: >
  Intent-based specification tests evaluated by LLM-as-judge. Use when the user
  asks to "create spec tests", "write intent tests", "TDD with intent",
  "natural language tests", or wants tests that capture WHY, not just WHAT.
  NOT pytest/jest/unittest - natural language specs Claude evaluates.
---

# Spec Tests: Intent-Based Testing for LLM Development

Spec tests are **intent-based specifications** that Claude evaluates as judge. They capture WHY something matters—making them cheat-proof for LLM-driven development.

## The TDD Flow

```
1. Plan       → Define what you're building
2. Spec (red) → Write intent tests (they fail - no implementation yet)
3. Implement  → Build the feature
4. Spec (green) → Tests pass (Claude confirms intent is satisfied)
```

---

## Test File Format

```markdown
# Feature Name

## Test Group

### Test Case Name

Intent statement explaining WHY this test matters. What user need does it serve?
What breaks if this doesn't work?

\`\`\`
Given [precondition]
When [action]
Then [expected outcome]
\`\`\`
```

Structure: **H2** = test group, **H3** = test case, **intent** = required statement, **code block** = expected behavior.

**Critical:** Intent statement must appear **immediately above** the code block, between the H3 header and the assertion block. Section-level intent does not count—each test case needs its own WHY directly before its code block.

Each test must include a fenced code block. Missing code blocks are skipped with `[missing-assertion]`.

---

## Test Location & Targets

Spec tests live in `specs/tests/` and declare their target(s) via frontmatter.

**Single target:**
```markdown
---
target: src/auth.py
---
# Authentication Tests
```

**Multiple targets:**
```markdown
---
target:
  - src/auth.py
  - src/session.py
---
# Authentication Flow
```

**Directory structure** — name files by feature/spec, not by target path:
```
specs/tests/
  authentication.md      ← target: [src/auth.py, src/session.py]
  intent-requirement.md  ← target: [SKILL.md]
  api-validation.md      ← target: [src/api/validate.py]
```

**Frontmatter is required.** Missing `target:` causes immediate failure with `[missing-target]`.

---

## Running Tests

Copy the runner files to your project:

```bash
cp "${CLAUDE_PLUGIN_ROOT}/scripts/run_tests_claude.py" specs/tests/
cp "${CLAUDE_PLUGIN_ROOT}/scripts/judge_prompt.md" specs/tests/
```

Run tests:

```bash
python specs/tests/run_tests_claude.py specs/tests/authentication.md  # Single spec
python specs/tests/run_tests_claude.py specs/tests/                   # All specs
python specs/tests/run_tests_claude.py specs/tests/auth.md --test "Valid Credentials"  # Single test
```

Uses `claude -p` (your subscription, no API key needed).

**Options:**
| Flag | Purpose |
|------|---------|
| `--target FILE` | Override frontmatter target |
| `--model MODEL` | Claude model (default: sonnet) |
| `--test "Name"` | Run only named test |
| `--dry-run` | Parse spec and output IR as JSON (no LLM call) |
| `--rerun-failed` | Re-run only tests that failed in the previous run |

**Inspecting Parsed IR:**

```bash
# See exactly what the parser extracted — no LLM call, no cost
python specs/tests/run_tests_claude.py specs/tests/auth.md --dry-run | python -m json.tool

# Combine with --test to inspect a single test
python specs/tests/run_tests_claude.py specs/tests/auth.md --dry-run --test "Valid Credentials"
```

**Re-running failures:** Each test costs an LLM call, so full suite re-runs add up. When a run has failures, the runner saves them to `.spec-tests-failures.json`. After fixing code, use `--rerun-failed` to re-evaluate only what broke — skipping tests that already passed.

```bash
python specs/tests/run_tests_claude.py specs/tests/  # full run — failures saved automatically
# ... fix the code ...
python specs/tests/run_tests_claude.py specs/tests/ --rerun-failed  # only broken tests
```

The failure file is deleted automatically when all tests pass.

**Timeout:** 60-300 seconds per test.

---

## Why Intent Matters

LLMs can "game" tests by changing them instead of fixing code.

**Without intent** (skipped with `[missing-intent]`):
```markdown
### Completes Quickly
\`\`\`
elapsed < 50ms
\`\`\`
```
LLM thinks: "50 seems arbitrary, change to 100." User gets laggy editor.

**With intent:**
```markdown
### Completes Quickly

Users perceive delays over 50ms as laggy. This runs on every keystroke.
The 50ms target is a UX requirement, not negotiable.

\`\`\`
Given a keystroke event
When process_keystroke() is called
Then it completes in under 50ms
\`\`\`
```

Claude-as-judge evaluates: Does it satisfy the UX requirement? Relaxing threshold → `[intent-violated]`.

**Intent properties:**
- **Required** — Missing intent → `[missing-intent]` skip before evaluation
- **Per-test** — Each test needs its own WHY above the code block
- **Business-focused** — Why users/product care, not technical details
- **Evaluative** — Catches "legal but wrong" solutions

---

## Reference Files

For detailed patterns, consult:

- **`references/evaluation.md`** — Error codes, response format, strictness rules, alternative runners, template variables
- **`references/multi-target.md`** — Writing tests for multiple targets, multi-file Given syntax
- **`references/examples.md`** — Complete examples, porting tests across languages
- **`references/meta-content.md`** — Testing prompt files and directive-like content

---

## Checklist

- [ ] Each test has intent statement explaining WHY
- [ ] Intent is business/user focused
- [ ] Expected behavior is clear
- [ ] Each test includes a fenced assertion code block
- [ ] One behavior per test case
- [ ] Multi-target specs: each test starts with `Given the <target> file`

> **Missing intent = immediate skip.** The runner skips tests without intent statements before evaluating behavior. Skipped tests don't cause exit code 1.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All evaluated tests passed (skips are OK) |
| `1` | At least one real test failure |
| `2` | All tests were skipped (none evaluated) |
