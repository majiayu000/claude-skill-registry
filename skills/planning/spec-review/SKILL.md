---
name: spec-review
description: Multi-agent spec review with parallel Claude/OpenCode reviewers. Use after spec-create or standalone via /spec.review.
---

# Spec Review Skill

Multi-perspective spec review using parallel subagent dispatch for comprehensive validation.

> **Reference:** See [reference/roles/](reference/roles/) for reviewer personas, [reference/report-format.md](reference/report-format.md) for YAML schemas, [reference/playbook.md](reference/playbook.md) for edge case handling.

---

## When to Use

- After `spec-create` to validate before implementation
- When spec feels incomplete or ambiguous
- Before `task-dispatch` for Initiatives (catches gate issues early)
- Standalone review of existing specs

---

## Workflow

### Step 1: Identify Spec

1. Parse spec name from argument (e.g., `/spec.review auth-system`)
2. If no argument: find most recent in `./specs/draft/`
3. If no specs in draft: check `./specs/active/`
4. Read spec documents: `spec.md`, `context.md`, `tasks.yaml`, `validation.yaml`

### Step 2: Select Reviewers

Use **AskUserQuestion** with multiSelect to choose reviewers:

```
Header: Reviewers
Question: Which reviewers should analyze this spec?
multiSelect: true
Options:
- claude-opus: Claude Opus - native subagent, comprehensive, context-aware
- claude-sonnet: Claude Sonnet - faster native review
- openai-gpt5.2: OpenAI GPT-5.2 - base model
- openai-gpt5.2-codex: OpenAI GPT-5.2 Codex - code-specialized
- openai-gpt5.2-pro: OpenAI GPT-5.2 Pro - extended capabilities
- gemini-3-flash: Google Gemini 3 Flash - fast, efficient
- gemini-3-pro: Google Gemini 3 Pro - advanced reasoning
```

**Default selection:** claude-opus, openai-gpt5.2-pro, gemini-3-pro

**Model mapping to commands:**
- `claude-opus` → Task tool with `model: "opus"`
- `claude-sonnet` → Task tool with `model: "sonnet"`
- `openai-gpt5.2` → `opencode run --model "openai/gpt-5.2"`
- `openai-gpt5.2-codex` → `opencode run --model "openai/gpt-5.2-codex"`
- `openai-gpt5.2-pro` → `opencode run --model "openai/gpt-5.2-pro"`
- `gemini-3-flash` → `opencode run --model "google/gemini-3-flash-preview"`
- `gemini-3-pro` → `opencode run --model "google/gemini-3-pro-preview"`

### Step 3: Dispatch Reviewers in Parallel

**CRITICAL:** Dispatch all selected reviewers in the same message for true parallelism.

**Review Prompt Template:**

```
You are reviewing a spec for completeness and feasibility.

## Spec Documents
[Include spec.md, context.md, tasks.yaml content]

## Review Focus
Evaluate against these gates:

1. **Completeness** - Are all requirements specified? Missing behaviors?
2. **Consistency** - Do documents contradict each other? Ambiguous terms?
3. **Feasibility** - Can tasks be implemented as described? Missing dependencies?
4. **Clarity** - Would a fresh developer understand what to build?

## Output Format
Return a YAML report:

```yaml
reviewer_report:
  reviewer: {REVIEWER_ID}
  gates:
    completeness:
      status: pass | fail
      issues: []
    consistency:
      status: pass | fail
      issues: []
    feasibility:
      status: pass | fail
      issues: []
    clarity:
      status: pass | fail
      issues: []
  issues:
    - severity: critical | high | medium
      gate: completeness
      area: ${TAXONOMY_AREA}
      description: "Clear description"
      suggestion: "How to fix"
  clarifying_questions:
    - area: ${TAXONOMY_AREA}
      question: "What needs clarification?"
  strengths:
    - "Positive observation"
```
```

**Dispatch by Type:**

**Claude reviewers (Task tool):**
```python
Task(
  subagent_type="general-purpose",
  model="opus",  # or "sonnet"
  prompt=review_prompt
)
```

**OpenCode reviewers (Bash tool, background):**
```bash
timeout 300 opencode run --model "{MODEL_PATH}" "{review_prompt}"
```

**Examples:**
- `opencode run --model "openai/gpt-5.2-pro" "{prompt}"`
- `opencode run --model "google/gemini-3-pro-preview" "{prompt}"`
- `opencode run --model "openai/gpt-5.2-codex" "{prompt}"`

### Step 4: Synthesize Reviews

After all reviewers complete:

1. **Parse reports** - Extract YAML from all outputs
2. **Merge issues:**
   - Deduplicate by description similarity
   - Combine issues flagged by multiple reviewers (higher confidence)
   - Note which reviewer(s) found each issue
3. **Aggregate gates:**
   - Gate fails if ANY reviewer fails it
   - Record which reviewer(s) failed each gate
4. **Prioritize questions:**
   - Group by taxonomy area
   - Rank: Scope > Behavior > Data Model > Constraints > Edge Cases > Integration > Terminology

### Step 5: Present Review

**Gate Summary Table:**

```
| Gate         | Status | Claude | GPT-5.2 Pro | Gemini-3 Pro |
|--------------|--------|--------|-------------|--------------|
| Completeness | FAIL   | fail   | pass        | fail         |
| Consistency  | PASS   | pass   | pass        | pass         |
| Feasibility  | FAIL   | fail   | fail        | pass         |
| Clarity      | PASS   | pass   | pass        | pass         |
```

**Issues by Severity:**

```
## Critical (must fix before implementation)
- [C1] Missing error handling for auth timeout (Completeness)
  Found by: claude-opus, opencode-gemini3-pro
  Suggestion: Add error case to spec.md#edge-cases

## High (should fix)
- [H1] Task T003 depends on undefined API contract (Feasibility)
  Found by: claude-opus, opencode-gpt5.2-pro
  Suggestion: Define API in context.md or defer task

## Medium (consider)
- [M1] Term "session" used inconsistently (Consistency)
  Found by: opencode-gpt5.2-pro
  Suggestion: Add to terminology section
```

### Step 6: Clarifying Questions

Use **AskUserQuestion** with questions grouped by taxonomy area:

```
Header: Scope
Question: The spec mentions "user roles" but doesn't define them. What roles exist?
multiSelect: false
Options:
- Admin/User: Two-tier system
- Role-based: Granular permissions
- Defer: Address later
```

Record answers for validation.yaml update.

### Step 7: Update Validation

Add clarification session to `validation.yaml`:

```yaml
clarification_sessions:
  - id: S00${N}
    timestamp: ${ISO_TIMESTAMP}
    source: spec-review
    reviewers: [claude-opus, opencode-gpt5.2]
    questions:
      - id: Q001
        question: "${QUESTION}"
        answer: "${ANSWER}"
        area: ${TAXONOMY_AREA}
        doc_updates:
          - file: spec.md
            section: ${SECTION}
            action: modified
```

Update `markers` section:
- Close resolved markers (`status: resolved`)
- Add new markers for deferred questions (`status: open`)

### Step 8: Recommend Action

**All gates pass:**
```
Review complete. All gates passed.

Recommendation: Ready for /spec.promote or /implement
```

**Issues found:**
```
Review complete. 2 gates failed.

Recommendation:
1. Address critical/high issues
2. Re-run /spec.review
```

---

## Gates

| Gate | What It Checks |
|------|----------------|
| **Completeness** | All requirements specified, no missing behaviors |
| **Consistency** | Documents align, no contradictions, terms used consistently |
| **Feasibility** | Tasks implementable, dependencies available, no blockers |
| **Clarity** | Unambiguous, fresh developer can understand scope |

---

## Edge Cases

**OpenCode timeout (> 5 minutes):**
- Continue with completed reviews
- Note in output: "[Reviewer] timed out, partial results"
- Still usable but recommend re-running

**One reviewer fails:**
- Parse what you can
- Report partial results with clear indication
- "Claude review: complete, GPT-5.2 Pro: failed to parse, Gemini 3 Pro: complete"

**No reviewers selected:**
- Default to claude-opus only
- Warn: "Consider adding external reviewers for diverse perspectives"

**Spec not found:**
- List available specs in `./specs/draft/` and `./specs/active/`
- Ask user to specify

**OpenCode command syntax:**
- GPT-5.2 Pro: `opencode run --model "openai/gpt-5.2-pro" {query}`
- Gemini 3 Pro: `opencode run --model "google/gemini-3-pro-preview" {query}`

---

## Integration

**Command:** `/spec.review [spec-name]`

**Related skills:**
- `spec-create` - Creates specs to review
- `spec-clarify` - Resolves markers found during review
- `task-dispatch` - Next step after review passes

---

## Reference

- [reference/roles/claude-reviewer.md](reference/roles/claude-reviewer.md) - Claude reviewer persona
- [reference/roles/opencode-reviewer.md](reference/roles/opencode-reviewer.md) - OpenCode reviewer persona
- [reference/report-format.md](reference/report-format.md) - YAML report schemas
- [reference/playbook.md](reference/playbook.md) - Edge case handling
