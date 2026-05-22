# Enhancing Prompts

<objective>
Analyze prompt quality, classify task type, and enhance with optimized templates while preserving original intent. Provides transparent feedback showing what was enhanced and why.
</objective>

<inputs>
- `prompt`: The user's original prompt to analyze and enhance
- `--analyze-only`: (optional) Show analysis without enhancement
- `--task-type <type>`: (optional) Force a specific task type
</inputs>

<workflow>

## Phase 1: Analysis

Analyze the prompt for components using the PTCF framework (Persona + Task + Context + Format).

### Component Detection

| Component | Patterns | Weight |
|-----------|----------|--------|
| **Persona** | `^(act as\|you are\|as a\|pretend\|imagine you're)` | 2 |
| **Task** | Action verbs: `(create\|review\|analyze\|fix\|summarize\|write\|debug\|refactor\|optimize\|draft\|investigate\|compare)` | 3 (required) |
| **Context** | `@\w+`, file paths (`\.ts\|\.js\|\.py\|\.md`), "given that", "based on", "from the", "in the" | 3 |
| **Format** | `(as bullets\|in JSON\|formatted as\|limit to\|with examples\|step by step\|list\|table)` | 2 |

### Quality Score Calculation

```
score = 0
if has_task_verb: score += 3
if has_context: score += 3
if has_format: score += 2
if has_persona: score += 2
return score  # 0-10
```

### Gap Identification

For each missing component, generate specific suggestions:
- Missing Persona → "Consider specifying who the AI should act as"
- Missing Context → "Add relevant files, constraints, or background"
- Missing Format → "Specify desired output structure"

## Phase 2: Classification

Classify the prompt into a task type for template selection.

### Classification Rules (priority order)

| Task Type | Trigger Patterns | Confidence Boost |
|-----------|------------------|------------------|
| `debugging` | "fix", "debug", "error", "broken", "not working", "fails" | +0.3 if has error message |
| `code_review` | "review", "check", "audit" + code file refs | +0.2 if has file paths |
| `refactoring` | "refactor", "improve", "optimize", "clean up" | +0.2 if mentions patterns |
| `summarization` | "summarize", "tldr", "brief", "key points", "overview" | +0.2 if has source |
| `research` | "analyze", "investigate", "compare", "research", "explore" | +0.2 if multiple subjects |
| `generation` | "create", "write", "draft", "generate", "make" | default |
| `general` | (fallback) | 0.5 |

### Classification Algorithm

```
classify_prompt(prompt):
  scores = {}
  for task_type, patterns in CLASSIFICATION_RULES:
    base_score = count_pattern_matches(prompt, patterns) / len(patterns)
    boost = calculate_boost(prompt, task_type)
    scores[task_type] = min(1.0, base_score + boost)

  best = max(scores, key=scores.get)
  confidence = scores[best]

  if confidence < 0.3:
    return ("general", 0.5)
  return (best, confidence)
```

## Phase 3: Enhancement

Load the task-specific template and merge with original prompt.

### Template Loading

Templates are located at: `resources/templates/{task_type}.yaml`

### Merge Algorithm

```
enhance_prompt(original, template, analysis):
  enhanced = original

  # Add persona if missing (prepend)
  if not analysis.components.persona:
    enhanced = template.persona.default + "\n\n" + enhanced

  # Add format if missing (append)
  if not analysis.components.format:
    enhanced = enhanced + "\n\n" + template.format.default

  # Add constraints (append as list)
  for constraint in template.constraints:
    if constraint not in enhanced:
      enhanced = enhanced + "\n- " + constraint

  # Preserve original intent - original text always wins
  return enhanced
```

## Phase 4: Output

Present the enhancement results transparently.

### Output Structure

```markdown
## Prompt Enhancement Analysis

### Quality Score: {before}/10 → {after}/10

### Original Prompt
> {original text}

### Detected Components
| Component | Status | Details |
|-----------|--------|---------|
| Persona | ❌/✅/⚠️ | {details} |
| Task | ❌/✅/⚠️ | {details} |
| Context | ❌/✅/⚠️ | {details} |
| Format | ❌/✅/⚠️ | {details} |

### Task Type
`{task_type}` (confidence: {confidence})

### Enhanced Prompt
> {enhanced text}

### Suggestions for Next Time
1. {suggestion 1}
2. {suggestion 2}
3. {suggestion 3}
```

### Status Icons

- ✅ Present - Component detected
- ⚠️ Partial - Component weak or incomplete
- ❌ Missing - Component not found, will be added

</workflow>

<analyze-only-mode>
When `--analyze-only` is specified:
1. Perform Phase 1 (Analysis) and Phase 2 (Classification)
2. Skip Phase 3 (Enhancement)
3. Output analysis only:
   - Quality score
   - Component detection table
   - Task type with confidence
   - Suggestions for improvement
   - No enhanced prompt shown
</analyze-only-mode>

<templates>
Load templates from: `resources/templates/{task_type}.yaml`

Available task types:
- code_review
- summarization
- research
- generation
- refactoring
- debugging
- general (fallback)
</templates>

<configuration>
Check `.loa.config.yaml` for settings:
```yaml
prompt_enhancement:
  enabled: true
  auto_enhance_threshold: 4
  show_analysis: true
  max_refinement_iterations: 3
```

If `enabled: false`, return original prompt unchanged.
If score >= `auto_enhance_threshold`, skip enhancement (prompt is good enough).
</configuration>

<feedback-integration>
When output fails (detected via error patterns or user rejection):
1. Log feedback type (runtime_error, verification_failure, user_rejection, partial_success)
2. Map to refinement action per `resources/feedback.md`
3. Re-analyze with feedback context
4. Apply refinement up to `max_refinement_iterations`
</feedback-integration>

<refinement-loop>
## Feedback-Driven Refinement Loop

When a prompt produces unsatisfactory output, the refinement loop improves the prompt iteratively.

### Trigger Detection

Detect failure signals from:
- **runtime_error**: Exception patterns, exit codes, stack traces
- **verification_failure**: Test failures, validation errors
- **user_rejection**: "no", "wrong", "try again", negative feedback
- **partial_success**: "almost", "close but", "except for"

### Refinement Process

```
1. Detect feedback type from user response or tool output
2. Load refinement actions for that feedback type:
   - runtime_error → add error context, specify constraints
   - verification_failure → add test requirements, specify behavior
   - user_rejection → request clarification, narrow scope
   - partial_success → focus on gap, add targeted constraint
3. Apply actions in priority order
4. Re-analyze refined prompt
5. If quality >= 7: return refined prompt
6. Else if iterations < max: repeat from step 1
7. Else: return best attempt with suggestions
```

### Iteration Limits

- Default maximum: 3 iterations
- Configurable via `prompt_enhancement.max_refinement_iterations`
- Hard stop prevents infinite loops
- Each iteration logged to trajectory

### Refinement History

When showing output, include refinement history if applicable:

```markdown
### Refinement History
| Iteration | Feedback | Action | Score |
|-----------|----------|--------|-------|
| 1 | user_rejection | Added persona | 4→6 |
| 2 | partial_success | Added format | 6→8 |
```

### Success Criteria

Refinement succeeds when:
- Quality score reaches 7+ (good prompt)
- User accepts the output
- Task completes without errors

Refinement fails when:
- Maximum iterations reached
- Same feedback type repeats 3 times (stuck)
- User requests to stop refining
</refinement-loop>
