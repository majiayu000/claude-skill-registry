---
name: review-reviews
description: Meta-audit all review skills for stale references, drifted architecture claims, and cross-skill inconsistencies
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit every skill in `.claude/skills/` for mechanical inaccuracies that would mislead an agent running the skill. Use maximum parallelism — the skills are independent.

## Why This Matters

Skills reference specific file paths, tool names, tool flags, function names, architecture claims, and each other. All of these drift as the codebase evolves — files get renamed, tools gain or lose flags, architecture gets refactored. A skill that tells an agent to "read `gui_store.ahk`" when that file was renamed six months ago wastes tokens and produces confused findings. A "Known Safe" pattern copied from a rules file that was since updated gives stale safety guidance.

## Phase 1 — Identifier Cross-Reference (Mechanical, High Confidence)

For each skill in `.claude/skills/*/SKILL.md`, extract every concrete identifier and verify it against the current codebase.

### What to extract and verify

- **File paths** — any `.ahk`, `.ps1`, `.py`, `.md` path mentioned. Does the file exist at that path? Use glob to check.
- **Function names** — any `FunctionName()` or `_FunctionName()` referenced. Does it exist? Use `query_function_visibility.ps1` to check.
- **Global variable names** — any `gSomething` referenced. Does it exist? Use `query_global_ownership.ps1` to check.
- **Tool names** — any `query_*.ps1` or `check_*.ps1` referenced. Does the tool exist in `tools/` or `tests/`?
- **Config key names** — any config key referenced by name. Does it exist in the registry? Use `query_config.ps1` to check.
- **IPC message types** — any `IPC_MSG_*` referenced. Does it exist? Use `query_ipc.ps1` to check.
- **Skill cross-references** — any mention of another skill by name (e.g., "that's `review-race-conditions` territory"). Does that skill exist in `.claude/skills/`?

### Classification

- **Broken**: The identifier doesn't exist. Agent following this skill will hit a dead end.
- **Renamed**: The identifier was renamed — old name gone, similar new name exists. Skill needs updating.
- **Current**: The identifier exists and the reference makes sense.

## Phase 2 — Tool Flag Verification (Mechanical, High Confidence)

Skills reference tools with specific flags and usage patterns. Verify these still work.

For each tool referenced in a skill:

1. Read the tool's source (the `.ps1` or `.py` file) to extract its actual parameter definitions
2. Compare against what the skill claims — does `-Discover` still exist? Is the positional parameter still positional? Did the output format change?
3. Flag any mismatches

Common drift patterns:
- Flag renamed (`-Query` → positional parameter)
- Flag added (tool gained a new flag the skill doesn't mention — not a bug, but worth noting if it would improve the skill's methodology)
- Flag removed (skill references a flag that no longer exists)
- Tool moved (`tests/` → `tools/`)

## Phase 3 — Architecture and Rules Consistency (Medium Confidence)

### Architecture claims

Skills make claims about the project's architecture — process model, data flow, what lives where. Cross-reference against:
- `.claude/rules/architecture.md` — the canonical architecture description
- `.claude/rules/ahk-patterns.md` — language patterns and conventions
- `.claude/rules/keyboard-hooks.md` — hook and Critical section patterns
- Other rules files as relevant

Flag any contradictions between what a skill says and what the rules files say. The rules files are the source of truth.

### Known Safe pattern drift

Several skills contain "Known Safe — Do NOT Flag" sections that duplicate patterns from rules files. These are particularly dangerous when stale — they tell agents to *ignore* something that may no longer be safe.

For each Known Safe pattern in a skill:
1. Find the canonical source in `.claude/rules/`
2. Compare the skill's version against the rules file version
3. Flag any drift — additions, removals, or wording changes in the rules that aren't reflected in the skill

### Cross-skill scope claims

Skills reference each other's scope ("Critical section restructuring is `review-race-conditions` territory", "buffer loops are `review-mcode` territory"). Verify:
1. The referenced skill exists
2. The referenced skill actually covers the claimed scope
3. No two skills claim the same scope in contradictory ways

## Phase 4 — Structural Consistency (Low Priority)

Optional — only if the above phases don't fill the plan. Check whether skills follow consistent patterns:

- Do all skills have the same YAML frontmatter fields?
- Do all skills end with "Ignore any existing plans — create a fresh one"?
- Do all skills have a Validation section with the cite-evidence / counter-argument / observed-vs-inferred requirements?
- Are plan format tables consistent across skills that audit similar things?

These are style issues, not correctness — report them but don't prioritize over Phase 1–3 findings.

## Scope

All files in `.claude/skills/*/SKILL.md`. Also check `.claude/rules/*.md` as cross-reference targets (but don't audit the rules files themselves — they're the source of truth, not the skills).

Do NOT audit non-review skills (like `ship`, `worktree`, `clean-all`, `merge-all`, `issue-from-plan`, `profile`) unless they reference codebase identifiers that could drift.

## Explore Strategy

Split by skill batch (run in parallel). Each agent gets a group of skills and performs Phase 1 + Phase 2 for those skills:

- **Performance skills** — `review-latency`, `review-blocking`, `review-criticals`, `review-mcode`, `review-resource-leaks`, `review-paint`, `review-d3d`
- **Correctness skills** — `review-race-conditions`, `review-option-interaction`, `review-comments`, `review-ahk2`, `review-reentrancy`
- **Static analysis skills** — `review-static-coverage`, `review-static-history`, `review-static-lintignore`, `review-static-speed`
- **Test/tool skills** — `review-test-coverage`, `review-test-quality`, `review-test-speed`, `review-test-skips`, `review-test-reliability`, `review-tool-coverage`, `review-tool-speed`
- **Code structure skills** — `review-dead-code`, `review-code-quality`, `review-function-visibility`, `review-ownership-manifest`, `review-file-size`, `review-constants-to-configs`
- **Rendering skills** — `review-shaders`, `review-shaders-open`
- **UX/meta skills** — `review-professionalism`, `review-debug`, `review-outside-box`, `review-reviews`

Phase 3 (architecture/rules consistency) should run as a separate pass after Phase 1/2, since it requires cross-referencing findings across skills.

## Validation

After explore agents report back, **validate every finding yourself**.

For each candidate:

1. **Cite evidence**: Quote the skill text containing the stale reference AND show the verification (glob result, tool source, rules file quote).
2. **Confirm it's actually stale**: A file path like `gui_store.ahk` in an *example table* might be illustrative, not a real reference. Only flag references the agent would actually try to follow.
3. **Propose the fix**: Don't just say "stale" — provide the updated reference. "Change `gui_store.ahk` to `gui_data.ahk`" or "Change `-Query <name>` to positional `<name>`."
4. **Check if the skill's methodology is affected**: A stale file name in the explore strategy is worse than one in an example table. A broken tool flag makes a whole phase of the skill fail. Rank by impact on the skill's effectiveness.

## Plan Format

**Section 1 — Broken/renamed identifiers (Phase 1):**

| Skill | Reference | Type | Status | Fix |
|-------|-----------|------|--------|-----|
| `review-latency` | `gui_store.ahk` | File path | Renamed to `gui_data.ahk` | Update reference |
| `review-blocking` | `_OldFunc()` | Function | Deleted | Remove reference |

**Section 2 — Tool flag mismatches (Phase 2):**

| Skill | Tool | Claimed Usage | Actual Usage | Fix |
|-------|------|--------------|-------------|-----|
| `review-ownership-manifest` | `query_global_ownership.ps1` | `-Query <name>` | Positional `<name>` | Update flag syntax |

**Section 3 — Architecture/rules drift (Phase 3):**

| Skill | Claim | Source of Truth | Contradiction | Fix |
|-------|-------|----------------|--------------|-----|
| `review-criticals` | Known Safe: "Critical through `GUI_OnInterceptorEvent`" | `keyboard-hooks.md` line 42 | Rules file added new exception not in skill | Add exception to skill |

**Section 4 — Cross-skill scope conflicts (Phase 3):**

| Skill A | Skill B | Overlapping Scope | Resolution |
|---------|---------|------------------|------------|
| `review-blocking` | `review-latency` | Both audit Critical section duration | Intentional — different framing (per-function vs per-path) |

**Section 5 — Structural inconsistencies (Phase 4, if applicable):**

| Skill | Issue | Fix |
|-------|-------|-----|
| `review-foo` | Missing "Ignore any existing plans" closing line | Add closing line |

Order by impact: broken references that would cause skill failure first, cosmetic inconsistencies last.

Ignore any existing plans — create a fresh one.
