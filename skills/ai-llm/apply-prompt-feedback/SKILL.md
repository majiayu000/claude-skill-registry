---
name: apply-prompt-feedback
description: 'Applies user feedback to prompts with precision - incorporates feedback intent without over-fitting, maintains information density, prevents regressions. Use when asked to apply feedback, incorporate suggestions, or update a prompt based on user input.'
---

# Apply Prompt Feedback

Apply user feedback to prompts with calibrated precision—addressing feedback intent fully while avoiding over-fitting, maintaining information density, and preventing regressions.

## Overview

This skill applies feedback through:
1. **Initial Application** - Apply feedback to prompt using Application Techniques
2. **Verification** - `prompt-feedback-verifier` checks for issues (over-fitting, regression, density loss)
3. **Refinement** - Fix issues based on verifier findings, iterate if needed (max 5 iterations)
4. **Output** - Atomic replacement only after verification passes

**Loop**: Gather inputs → Copy → Apply feedback → Verify → (Iterate if issues) → Output

**Key principles**:
- **Just-right application**: Address ALL of feedback, ONLY feedback, nothing more
- **Information density**: Use minimal text to achieve the change
- **Regression prevention**: Preserve everything feedback didn't mention
- **Verifier validates**: Verifier catches over-fitting, under-fitting, and regressions

**Required tools**: This skill requires Task tool to launch the verifier agent. If Task is unavailable, report error: "Task tool required for verification loop." This skill uses TodoWrite to track progress. If TodoWrite is unavailable, track progress internally.

## Workflow

### Phase 0: Create Todo List (TodoWrite immediately)

Create todos tracking workflow phases:

```
- [ ] Input validation; done when prompt + feedback files read successfully
- [ ] Initial application→verify; done when verifier returns VERIFIED or issues fixed
- [ ] (Expand: refinement iterations on ISSUES_FOUND)
- [ ] Output updated prompt; done when updated prompt displayed + optionally saved
```

### Phase 1: Input Validation

**Mark "Input validation" todo `in_progress`.**

**Step 1.1: Parse arguments**

Extract from `$ARGUMENTS`:
- Prompt (file path or inline)
- Feedback (may be in arguments or need to ask)

**Step 1.2: Determine prompt source**

| Input Type | Detection | Action |
|------------|-----------|--------|
| File path | Contains `/` or `\`, OR ends with `.md`, `.txt`, `.yaml`, `.yml` | Read file content |
| Inline prompt | Does not match file path criteria | Write to `/tmp/prompt-{timestamp}.md` |

**Priority**: If ambiguous, treat as file path first; if not found, treat as inline.

**Step 1.3: Gather feedback**

If feedback not in arguments, use AskUserQuestion:

```
questions: [
  {
    question: "What feedback do you want to apply to this prompt?",
    header: "Feedback",
    options: [
      { label: "I'll type it", description: "Enter feedback in the text field" }
    ],
    multiSelect: false
  }
]
```

**Step 1.4: Validate inputs**

- If prompt file exists and has content: Use file content
- If prompt file empty: Error: "Cannot apply feedback to empty prompt: {path}"
- If file not found: Re-classify as inline, write to temp file
- If no prompt: Error: "Usage: /apply-prompt-feedback <file-path-or-prompt> [feedback] OR provide feedback when prompted"
- If no feedback after asking: Error: "Feedback required to proceed"

**Step 1.5: Store metadata**

- `source_path`: Source file path (or temp path for inline)
- `is_inline`: Boolean
- `original_content`: Full prompt text
- `feedback`: User's feedback text
- `original_path`: `/tmp/feedback-original-{YYYYMMDDHHMMSS}-{4-lowercase-alphanumeric}.md` (copy of original for verifier comparison)
- `working_path`: `/tmp/feedback-modified-{YYYYMMDDHHMMSS}-{4-lowercase-alphanumeric}.md` (modified version)

**Mark "Input validation" todo `completed`.**

### Phase 2: Initial Application

**Mark "Initial application" todo `in_progress`.**

**Step 2.1: Create working copies**

Using Write tool:
1. Copy original content to `original_path` (untouched reference for verifier)
2. Copy original content to `working_path` (will be modified)

**Step 2.2: Apply feedback**

Apply the feedback to the prompt using Application Techniques (see below). Write the updated prompt to working_path.

**Key principle**: Apply feedback with just-right calibration—address the full intent without over-fitting or adding unrelated changes.

**Step 2.3: Verify application**

Launch prompt-feedback-verifier agent via Task tool:
- subagent_type: "prompt-engineering:prompt-feedback-verifier"
- prompt: "Verify feedback application. Original: {original_path}. Modified: {working_path}. Feedback: {feedback}. Check for: feedback not addressed, partial incorporation, over-fitting, over-specification, regression, information density loss. Report VERIFIED or ISSUES_FOUND with specific details."

**Step 2.4: Handle verifier response**

- If "VERIFIED": Mark todo completed, proceed to Phase 4
- If "ISSUES_FOUND": Mark todo completed, save issues, add "Refinement iteration 1" todo, proceed to Phase 3
- If verifier fails: Retry once. If retry fails, proceed to Phase 4 with warning: "Verification failed - manual review recommended."

**Step 2.5: Display findings**

If issues found:
```
Feedback Summary: {summary from verifier}
Verifier found {count} issues. Proceeding with refinement...
```

**Mark "Initial application" todo `completed`.**

### Phase 3: Refinement Loop (Verifier-Driven)

**Mark "Refinement iteration 1" todo `in_progress`.**

**Key principle**: All refinements driven by verifier feedback. Only fix issues the verifier reported.

For each iteration from 1 to 5:

1. **Apply fixes from verifier feedback**: For each issue, apply the Suggested Fix using Application Techniques. Write to working_path.
   - Only address issues the verifier identified
   - If Write tool fails: display error, proceed to Phase 4 with most recent version

2. **Re-verify**: Launch prompt-feedback-verifier agent via Task tool:
   - subagent_type: "prompt-engineering:prompt-feedback-verifier"
   - prompt: "Verify feedback application. Original: {original_path}. Modified: {working_path}. Feedback: {feedback}. Check for: feedback not addressed, partial incorporation, over-fitting, over-specification, regression, information density loss. Report VERIFIED or ISSUES_FOUND with specific details."

3. **Handle response**:
   - If "VERIFIED": mark todo completed, exit loop, proceed to Phase 4
   - If "ISSUES_FOUND" and iteration < 5: mark todo completed, save issues, add "Refinement iteration {next}" todo, continue
   - If "ISSUES_FOUND" and iteration = 5: mark todo completed with note, proceed to Phase 4 with warning
   - If verifier fails: display error, retry once. If retry fails, proceed to Phase 4 with warning: "Verification incomplete - manual review recommended."

## Application Techniques

Apply feedback using these calibrated techniques:

### Incorporation Techniques

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Feedback Not Addressed** | Add minimal instruction that addresses feedback intent | Feedback: "handle empty input" → Add: "If input is empty, return error message." |
| **Partial Incorporation** | Add missing aspects only, don't expand what's already there | Feedback: "handle A, B, C" (A done) → Add B and C handling only |

### Calibration Techniques

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Over-Fitting** | Remove unrelated additions, keep only feedback-relevant changes | Remove new sections that feedback didn't request |
| **Over-Specification** | Condense verbose implementation to minimal form | "When timeout occurs after 30 seconds of no response from the server, the system should log the error, notify the user, and retry up to 3 times" → "Timeout after 30s; retry up to 3x" |

### Preservation Techniques

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Regression** | Restore removed/changed behavior, integrate with new additions | Re-add removed instruction, resolve any conflict with new content |
| **Information Density Loss** | Consolidate redundant text, use concise phrasing | Merge repeated statements, remove verbose explanations |

### Information Density Rules

When applying feedback, maximize information density:

1. **Minimal additions**: Add only text necessary to address feedback
2. **Concise phrasing**: Use fewest words that convey meaning precisely
3. **No duplication**: Don't repeat what prompt already says
4. **Consolidate**: Merge related additions into existing sections when possible
5. **Delete redundancy**: If adding X makes existing text Y redundant, remove Y

**Density checklist before writing**:
- [ ] Can this be said in fewer words?
- [ ] Does existing text already partially cover this?
- [ ] Can this be merged with an existing section?
- [ ] Am I adding explanation where a rule suffices?

### Resolution Strategy

For each issue:

```
Issue from verifier
    │
    ▼
Is the fix text provided in Suggested Fix?
    │
    ├─ YES → Apply exact fix text
    │
    └─ NO → Use Application Techniques
             │
             ▼
         Apply minimal change that:
         1. Addresses the issue
         2. Uses fewest possible words
         3. Preserves existing content
         4. Doesn't introduce new issues
```

### Phase 4: Output

**Mark "Output updated prompt" todo `in_progress`.**

**Step 4.1: Apply changes**

After application complete:
- For file input: `mv {working_path} {source_path}` (atomic replacement)
- For inline input: Keep at working_path, report location

**Step 4.2: Display results**

If verification passed:
```
Updated: {path}
Iterations: {count}
Status: Feedback applied

Feedback: {original feedback}

Changes applied:
- {List each change as bullet, categorized: "Incorporation:", "Calibration:", or "Preservation:"}
```

If verification failed after 5 iterations:
```
Updated with warnings: {path}
Iterations: 5
Status: Some issues may remain

Feedback: {original feedback}

Unresolved issues:
- {list from last verification}

Review the changes manually.
```

**Mark "Output updated prompt" todo `completed`. Mark all todos complete.**

## Key Principles

| Principle | Rule |
|-----------|------|
| **Apply then verify** | Apply feedback first, verifier catches issues |
| **Verifier-driven refinement** | Refinements only fix issues verifier identifies |
| **Just-right application** | Address ALL feedback, ONLY feedback |
| **Information density** | Minimal text to achieve the change; no bloat |
| **Regression prevention** | Preserve everything feedback didn't mention |
| **Track progress** | TodoWrite for phases; expand on iteration |
| **Atomic output** | Original untouched until application complete |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No prompt provided | Error: "Usage: /apply-prompt-feedback <file-path-or-prompt> [feedback]" |
| No feedback provided | Use AskUserQuestion to gather feedback |
| File not found | Re-classify as inline prompt, write to temp file |
| Empty file | Error: "Cannot apply feedback to empty prompt: {path}" |
| Vague feedback | Apply reasonable interpretation; verifier will catch over/under-fitting |
| Conflicting feedback | Apply most recent/prominent request; note conflict in output |
| Verifier fails | Retry once; if fails, output with warning: "Verification failed - manual review recommended." |
| Task tool unavailable | Error: "Task tool required for verification loop." |

## Example Usage

```bash
# Apply feedback to a prompt file
/apply-prompt-feedback prompts/assistant.md "Make it handle empty input gracefully"

# Apply feedback to inline prompt (will be prompted for feedback)
/apply-prompt-feedback "You are a helpful assistant. Answer questions concisely."

# Apply multiple feedback points
/apply-prompt-feedback skills/reviewer/SKILL.md "Add timeout handling and clarify what 'significant' means"
```

## Example Output

```
Updated: prompts/assistant.md
Iterations: 2
Status: Feedback applied

Feedback: Make it handle empty input gracefully

Changes applied:
- Incorporation: Added "If input is empty, respond with 'Please provide a question or topic.'"
- Preservation: Existing response format unchanged
- Calibration: Kept addition minimal (single sentence vs. elaborate error handling)
```
