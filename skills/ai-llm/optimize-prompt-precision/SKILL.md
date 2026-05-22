---
name: optimize-prompt-precision
description: 'Iteratively optimizes prompts for precision - eliminates ambiguities, resolves conflicts, adds missing definitions. Use when asked to optimize precision, clarify, disambiguate, or make a prompt unambiguous.'
---

# Optimize Prompt Precision

Iteratively optimize prompt precision through verification loops. Primary goal: ensure prompt cannot be interpreted in ways the author doesn't expect.

## Overview

This skill transforms ambiguous prompts into precise ones through:
1. **Verification First** - `prompt-precision-verifier` checks for issues before any changes
2. **Optimization** - Apply targeted fixes based on verifier feedback (infer from context when possible, ask user when not)
3. **Re-verification** - Verify fixes, iterate if issues remain (max 5 iterations)
4. **Output** - Atomic replacement only after verification passes

**Loop**: Read → Verify → (Exit if precise) → Optimize based on feedback → Re-verify → (Iterate if issues) → Output

**Key principle**: Don't try to optimize in one pass. The verifier drives all changes - if it finds no issues, the prompt is already precise.

## Workflow

### Phase 0: Create Todo List (TodoWrite immediately)

Create todos tracking workflow phases. List reflects areas of work, not fixed steps.

**Starter todos**:
```
- [ ] Input validation
- [ ] Initial verification
- [ ] (Expand: optimization iterations on ISSUES_FOUND)
- [ ] Output optimized prompt
```

### Phase 1: Input Validation

**Mark "Input validation" todo `in_progress`.**

**Step 1.1: Parse arguments**

Extract input from `$ARGUMENTS`. Determine if file path or inline prompt.

**Step 1.2: Handle input type**

| Input Type | Detection | Action |
|------------|-----------|--------|
| File path | Starts with `/`, `./`, `~`, or ends with `.md`, `.txt`, `.yaml` | Read file content |
| Inline prompt | Everything else | Write to `/tmp/prompt-{timestamp}.md` |

**Step 1.3: Validate content**

- If file path: Check file exists using Read tool
- If inline: Write to temp file, note original was inline
- Error if no input provided: "Usage: /optimize-prompt-precision <file-path> OR /optimize-prompt-precision <inline prompt text>"

**Step 1.4: Store metadata**

- `source_path`: Source file path (or temp path for inline)
- `is_inline`: Boolean (affects output messaging)
- `original_content`: Full prompt text
- `original_path`: `/tmp/precision-original-{YYYYMMDDHHMMSS}-{4-lowercase-alphanumeric}.md` (copy of original for verifier comparison)
- `working_path`: `/tmp/precision-optimized-{YYYYMMDDHHMMSS}-{4-lowercase-alphanumeric}.md` (modified version)

**Mark "Input validation" todo `completed`.**

### Phase 2: Initial Verification

**Mark "Initial verification" todo `in_progress`.**

**Step 2.1: Create working copies**

Using Write tool:
1. Copy original content to `original_path` (untouched reference for verifier comparison)
2. Copy original content to `working_path` (will be modified)

**Step 2.2: Run verifier first (single file mode)**

Launch prompt-precision-verifier agent via Task tool BEFORE any optimization:
- subagent_type: "prompt-engineering:prompt-precision-verifier"
- prompt: "Verify prompt precision. File: {working_path}. Check for ambiguities, conflicts, undefined terms, underspecified rules, vague thresholds, priority confusion, edge case gaps, and implicit expectations. Report VERIFIED or ISSUES_FOUND with specific details."

**Step 2.3: Handle verifier response**

- If "VERIFIED": Mark todo completed, proceed directly to Phase 4 (Output) with message: "Prompt is already precise. No changes needed."
- If "ISSUES_FOUND": Mark todo completed, save the issues list, add "Optimization iteration 1" todo and proceed to Phase 3
- If verifier fails or returns unexpected format: Retry once with identical parameters. If retry fails, report error: "Verification failed - cannot proceed without verifier."

**Step 2.4: Display verifier findings**

If issues found, show user summary and proceed:

```
Verifier found {count} precision issues. Proceeding with optimization...
```

**Mark "Initial verification" todo `completed`.**

### Phase 3: Optimization Loop (Verifier-Driven)

**Mark "Optimization iteration 1" todo `in_progress`.**

**Key principle**: All fixes are driven by verifier feedback. Do NOT analyze the prompt independently - only fix the specific issues the verifier reported.

For each iteration from 1 to 5:

1. **Apply fixes from verifier feedback**: For each issue in the verifier's report, apply the Suggested Fix or use Resolution Strategy (see below) to address it. Write optimized version to working_path.
   - Only fix issues the verifier identified - do not add your own improvements

2. **Re-verify (comparison mode)**: Launch prompt-precision-verifier agent via Task tool:
   - subagent_type: "prompt-engineering:prompt-precision-verifier"
   - prompt: "Verify optimization. Original: {original_path}. Modified: {working_path}. Check for ambiguities, conflicts, undefined terms, underspecified rules, vague thresholds, priority confusion, edge case gaps, implicit expectations, optimization regressions, and over-optimization. Report VERIFIED or ISSUES_FOUND with specific details."

3. **Handle response**:
   - If "VERIFIED": mark todo completed, exit loop, proceed to Phase 4
   - If "ISSUES_FOUND" and iteration < 5: mark todo completed, save new issues list, add "Optimization iteration {next}" todo, continue to next iteration
   - If "ISSUES_FOUND" and iteration = 5: mark todo completed with note about unresolved issues, proceed to Phase 4 with warning
   - If verifier fails or returns unexpected format: display error to user, retry once with identical parameters. If retry fails, proceed to Phase 4 with warning: "Verification incomplete - manual review recommended."

### Resolution Strategy

For each issue found, follow this decision tree:

```
Issue detected
    │
    ▼
Can resolution be INFERRED from prompt context?
(purpose, goals, existing patterns, domain conventions)
    │
    ├─ YES → Apply inferred fix directly
    │        Examples:
    │        - "Be concise" in a CLI tool prompt → infer "under 100 words"
    │        - Conflict between "brief" and "thorough" → infer based on prompt's stated purpose
    │        - Undefined "standard format" → infer from examples in prompt or domain norms
    │
    └─ NO → Ask user via AskUserQuestion
             (truly ambiguous, multiple valid interpretations, author intent unclear)
```

**Inference sources** (check in order):
1. **Prompt purpose/mission** - What is this prompt trying to accomplish?
2. **Existing patterns** - How does the prompt handle similar cases?
3. **Domain conventions** - What's standard practice in this domain?
4. **Sensible defaults** - What would a reasonable author likely intend?

**When to ask the user**:

| Ask When | Example |
|----------|---------|
| Multiple equally valid interpretations | "Be helpful" - could mean many things |
| Conflict with no clear winner | Two rules that contradict, no priority hints |
| Missing context only author knows | "Use the standard format" with no examples |
| Business/preference decision | Opt-in vs opt-out default |

**AskUserQuestion format**:

```
questions: [
  {
    question: "The prompt says '{ambiguous text}'. What did you intend?",
    header: "Clarify: {brief topic}",
    options: [
      { label: "{interpretation A}", description: "{what this means}" },
      { label: "{interpretation B}", description: "{what this means}" },
      { label: "{interpretation C}", description: "{what this means}" }
    ],
    multiSelect: false
  }
]
```

**Batch related questions** - If multiple issues need user input, ask up to 4 related questions in one AskUserQuestion call.

**After user answers**: Apply their clarification to the prompt, then continue optimization loop.

### Phase 4: Output

**Mark "Output optimized prompt" todo `in_progress`.**

**Step 4.1: Apply changes**

After optimization complete (verification passed or max iterations reached):
- For file input: `mv {working_path} {source_path}` (atomic replacement)
- For inline input: Keep at working_path, report location

**Step 4.2: Display results**

If verification passed:
```
Optimized: {path}
Iterations: {count}
Status: Precise and unambiguous

Changes applied:
- {summary of fixes}
```

If verification failed after 5 iterations:
```
Optimized with warnings: {path}
Iterations: 5
Status: Some issues may remain

Unresolved issues:
- {list from last verification}

Review the changes manually.
```

**Mark "Output optimized prompt" todo `completed`. Mark all todos complete.**

## Optimization Techniques

Apply these techniques to fix precision issues:

| Technique | Description | Before → After |
|-----------|-------------|----------------|
| **Define terms** | Add explicit definition for vague terms | "Be concise" → "Keep responses under 150 words" |
| **Resolve conflict** | Add priority or rephrase to eliminate contradiction | "Be brief" + "Be thorough" → "Be thorough for complex queries, brief for simple ones" |
| **Add threshold** | Replace subjective judgment with objective criteria | "When appropriate" → "When the user explicitly asks" |
| **Handle edge case** | Add explicit behavior for corner cases | Add "If both X and Y, prioritize X" |
| **Make explicit** | Surface implicit assumptions | Add "Assumes user has basic familiarity with..." |
| **Add priority** | Clarify which rules take precedence | Add "Rule A takes precedence over Rule B when..." |
| **Remove ambiguity** | Rephrase so only one interpretation possible | "Use the tool" → "Use the Read tool" |

## Key Principles

| Principle | Rule |
|-----------|------|
| **Verify first** | Always run verifier before any optimization; maybe prompt is already precise |
| **Verifier-driven** | Only fix issues the verifier identifies - no independent analysis or improvements |
| **Track progress** | TodoWrite to track phases; expand todos on iteration |
| **Infer first, ask second** | Try to resolve verifier-flagged issues from context before asking user |
| **Preserve intent** | Don't change what prompt is trying to do; only fix issues the verifier flagged |
| **Minimal questions** | Only ask user when inference is truly impossible |
| **Verification required** | Never output without verifier checking |
| **Atomic output** | Original untouched until verification passes |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No input provided | Error: "Usage: /optimize-prompt-precision <file-path> OR /optimize-prompt-precision <inline prompt text>" |
| File not found | Error: "File not found: {path}" |
| Already precise | Verifier returns VERIFIED on first check → Report: "Prompt is already precise. No changes needed." |
| Initial verifier fails | Retry once; if still fails, Error: "Verification failed - cannot proceed without verifier." |
| Re-verification fails | Display error, retry once; if retry fails, output with warning: "Verification incomplete - manual review recommended." |
| Severely ambiguous | Make best effort over 5 iterations; output with warnings |
| Very large prompt (>50KB) | Process as single unit |
| Task tool unavailable | Error: "Task tool required for verification loop." |

## Example Usage

```bash
# Optimize a prompt file for precision
/optimize-prompt-precision prompts/code-reviewer.md

# Optimize inline prompt for precision
/optimize-prompt-precision You are a helpful assistant. Be concise but thorough. Use good judgment.

# Optimize a skill file for precision
/optimize-prompt-precision claude-plugins/my-plugin/skills/my-skill/SKILL.md
```

## Example Output

```
Optimized: prompts/code-reviewer.md
Iterations: 2
Status: Precise and unambiguous

Changes applied:
- Defined "significant issues" as errors, security vulnerabilities, or logic bugs (inferred from code review context)
- Resolved conflict between "be thorough" and "keep it brief" by specifying contexts (inferred from prompt purpose)
- Added explicit behavior for empty input case (sensible default)
- Clarified priority when multiple rules apply (asked user - chose "security over style")
```
