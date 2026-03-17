---
name: dev_invoke_codex-cli
description: |
  Delegate code tasks to OpenAI Codex CLI using markdown file handoff pattern.
  Write instructions to TASK.md, Codex reads and executes, outputs to OUTPUT.md.
  Use for implementation, refactoring, code generation requiring extended thinking.

  Triggers: codex, codex cli, delegate to codex, codex subagent, implementation task,
  refactoring task, code generation, gpt-5.2-codex, openai codex, extended thinking,
  multi-file changes, complex implementation

  Prerequisites: Codex CLI authenticated (codex login or OPENAI_API_KEY)
  Model: gpt-5.2-codex (default, supports xhigh reasoning effort)
---

# Invoking Codex CLI

Delegate tasks to Codex CLI using markdown files for instruction input and deliverable output.

## Pattern: Markdown File Handoff

```
Claude Code                         Codex CLI
    |                                   |
    +-- Write TASK.md ------------------+
    |   (instructions + context)        |
    |                                   |
    +-- Execute: codex e "Read TASK.md, |
    |   follow instructions, write      |
    |   deliverables to OUTPUT.md"      |
    |                                   |
    |                                   +-- Reads TASK.md
    |                                   +-- Executes task
    |                                   +-- Writes OUTPUT.md
    |                                   |
    +-- Read OUTPUT.md <----------------+
    |   (deliverables + results)        |
    v                                   v
```

**Benefits**:
- No shell escaping issues (quotes, special characters, code blocks)
- Structured context in reviewable files
- Explicit deliverable format
- Session resume via thread ID

## When to Use

- Complex implementation requiring multi-file changes
- Refactoring with dependency tracking
- Code generation with detailed specifications
- Tasks requiring extended thinking (20-30 minutes)

## Model Selection

**Model**: Always use `gpt-5.2-codex` (latest model)

**Reasoning Effort**: Adjust based on task complexity

| Reasoning Effort | Use Case | Speed |
|------------------|----------|-------|
| `xhigh` | **Default.** Complex tasks, deep analysis | Slowest, best quality |
| `high` | Medium complexity, good reasoning | Balanced |
| `medium` | Lighter tasks, adequate reasoning | Faster |
| `low` | Simple tasks, quick response | Fastest |

**Recommendation**: Use default `xhigh` reasoning for most tasks. Lower reasoning effort for simpler tasks, not older models.

## Invocation

### Standard Pattern (Recommended)

```bash
codex e "Read TASK.md in the current directory. Follow the instructions exactly. Write all deliverables to OUTPUT.md." \
  -C "/path/to/project" \
  --full-auto \
  --skip-git-repo-check
```

### With Lower Reasoning Effort

```bash
# For simpler tasks, reduce reasoning effort (not model)
codex e "Read TASK.md, follow instructions, write results to OUTPUT.md" \
  -C "/path/to/project" \
  -c model_reasoning_effort=medium \
  --full-auto \
  --skip-git-repo-check
```

### Resume Session

```bash
codex e resume <thread_id> "Read TASK.md for updated instructions, append results to OUTPUT.md"
```

## Core Flags Reference

| Flag | Purpose |
|------|---------|
| `-C /path` | Working directory (where TASK.md lives) |
| `--full-auto` | Sandboxed auto-execution (workspace-write + no approvals) |
| `--skip-git-repo-check` | Work in any directory |
| `-c model_reasoning_effort=<level>` | Reasoning: xhigh (default), high, medium, low |

**Model**: Always `gpt-5.2-codex` (latest). Adjust reasoning effort instead of changing models.

## Task File Template (TASK.md)

```markdown
# Task: [Brief Title]

## Objective
[Clear statement of what needs to be accomplished]

## Context
[Relevant background, constraints, requirements]

## Input Files
- `src/api/users.ts` - User service to modify
- `src/types/user.ts` - Type definitions

## Instructions
1. [First step]
2. [Second step]
3. [Third step]

## Deliverables
Write to OUTPUT.md:
- Summary of changes made
- List of files modified
- Any issues encountered
- Recommendations for follow-up
- Thread ID for session resume

## Constraints
- Do not modify files outside src/api/
- Maintain backward compatibility
- Follow existing code style
```

## Output File Template (OUTPUT.md)

Codex should produce:

```markdown
# Deliverables: [Task Title]

## Summary
[Brief description of what was done]

## Changes Made

### Files Modified
| File | Change |
|------|--------|
| `src/api/users.ts` | Added validation logic |

### Code Changes
[Key code snippets if relevant]

## Issues Encountered
- [Any problems and how resolved]

## Recommendations
- [Suggested follow-up actions]

## Session
Thread ID: `<thread_id>` (for resume)
```

## Workflow Example (ras-commander)

### 1. Write TASK.md

```markdown
# Task: Add Validation to Precipitation API

## Objective
Add depth conservation validation to precipitation methods.

## Context
The precipitation methods in ras_commander/precip/ need validation
to ensure depth conservation at 10^-6 precision.

## Input Files
- `ras_commander/precip/Atlas14Storm.py`
- `ras_commander/precip/StormGenerator.py`

## Instructions
1. Add depth conservation check after hyetograph generation
2. Raise ValidationError if conservation fails
3. Log successful validation with actual precision achieved

## Deliverables
Write to OUTPUT.md:
- Summary of validation logic added
- Files modified with line references
- Test cases to validate

## Constraints
- Use existing ValidationSeverity pattern
- Maintain backward compatibility
```

### 2. Execute Codex

```bash
codex e "Read TASK.md, follow the instructions, write deliverables to OUTPUT.md" \
  -C "C:/GH/ras-commander" \
  --full-auto \
  --skip-git-repo-check
```

### 3. Read OUTPUT.md

Parse results, verify changes, continue workflow.

## Environment Variables

```bash
CODEX_API_KEY=sk-xxx      # Required (or use codex login)
OPENAI_API_KEY=sk-xxx     # Alternative
```

## Session Management

- Thread ID appears in Codex console output at session start
- Request thread ID in OUTPUT.md deliverables section
- Resume with: `codex e resume <thread_id> "follow-up instruction"`

## Tips

1. **Be explicit in TASK.md** - Include all context, don't assume
2. **Specify output structure** - Tell Codex exactly what OUTPUT.md should contain
3. **List input files** - Explicitly name files Codex should read
4. **Define constraints** - Prevent unwanted modifications
5. **Request thread ID** - Include in deliverables for session resume
6. **Use default model** - `gpt-5.2-codex` is best for complex reasoning tasks

## When to Escalate

**Use Codex for**:
- Implementation requiring extended thinking
- Multi-file refactoring
- Complex code generation
- Architecture planning

**Use specialized ras-commander agents for**:
- HDF analysis -> `hdf-analyst`
- Geometry parsing -> `geometry-parser`
- USGS integration -> `usgs-integrator`

---

**See Also**:
- `code-oracle-codex` agent - Full orchestration capabilities
- `.claude/rules/subagent-output-pattern.md` - Output format standards
