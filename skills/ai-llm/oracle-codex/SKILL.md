---
name: oracle-codex
description: This skill should be used when the user asks to "use Codex", "ask Codex", "consult Codex", "Codex review", "use GPT for planning", "ask GPT to review", "get GPT's opinion", "what does GPT think", "second opinion on code", "consult the oracle", "ask the oracle", or mentions using an AI oracle for planning or code review. NOT for implementation tasks.
context: fork
agent: Plan
---

# Codex Oracle

Use OpenAI Codex CLI as a **planning oracle** and **code reviewer**. Codex provides analysis and recommendations; Claude synthesizes and presents to the user.

**Critical**: This skill is for planning and review ONLY. Never use Codex to implement changes.

## Prerequisites

Before invoking Codex, validate availability:

```bash
~/.claude/skills/oracle-codex/scripts/check-codex.sh
```

If the script exits non-zero, display the error message and stop. Do not proceed without Codex CLI.

## Configuration Defaults

| Setting   | Default                       | User Override                                   |
| --------- | ----------------------------- | ----------------------------------------------- |
| Model     | `gpt-5.2-codex`               | "use model X" or "with gpt-5.2-codex"           |
| Reasoning | Dynamic (based on complexity) | "use medium reasoning" or "with xhigh effort"   |
| Sandbox   | `read-only`                   | Not overridable (safety constraint)             |
| Timeout   | 5 minutes minimum             | Estimate based on task complexity               |
| Profile   | `quiet` (notify=[])           | User opts into another profile or notifications |

### Timeout Guidelines

When invoking `codex exec` via the Bash tool, always set an appropriate timeout:

- **Minimum**: 5 minutes (300000ms) for any Codex operation
- **Simple queries** (single file review, focused question): 5 minutes (300000ms)
- **Moderate complexity** (multi-file review, feature planning): 10 minutes (600000ms)
- **High complexity** (`high` reasoning): 15 minutes minimum (900000ms)
- **Maximum complexity** (`xhigh` reasoning): 20 minutes (1200000ms)

### Reasoning Effort Guidelines

Select reasoning effort based on task complexity:

| Complexity | Effort   | Examples                                                      |
| ---------- | -------- | ------------------------------------------------------------- |
| Simple     | `low`    | Single file review, syntax check, quick question              |
| Moderate   | `medium` | Multi-file review, focused feature planning, bug analysis     |
| Complex    | `high`   | Architecture analysis, cross-cutting concerns, security audit |
| Maximum    | `xhigh`  | Large codebase planning, comprehensive design, deep reasoning |

**Selection heuristics:**

- **`low`**: Task involves \<3 files, simple question, or quick validation
- **`medium`**: Task involves 3-10 files or requires moderate analysis
- **`high`**: Task spans multiple modules or requires architectural thinking
- **`xhigh`**: Task requires comprehensive codebase understanding or critical decisions

For available models and reasoning levels, consult `references/codex-flags.md`.

## Workflow

### 1. Validate Prerequisites

Run the check script. On failure, report the installation instructions and abort.

### 2. Determine Mode

- **Planning mode**: User wants architecture, implementation approach, or design decisions
- **Review mode**: User wants code analysis, bug detection, or improvement suggestions

### 3. Construct Prompt

Build a focused prompt for Codex based on mode:

**Planning prompt template:**

```
Analyze this codebase and provide a detailed implementation plan for: [user request]

Focus on:
- Architecture decisions and trade-offs
- Files to create or modify
- Implementation sequence
- Potential risks or blockers

Do NOT implement anything. Provide analysis and recommendations only.
```

**Review prompt template:**

```
Review the following code for:
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code quality and maintainability
- Adherence to best practices

[code or file paths]

Provide specific, actionable feedback with file locations and line references.
```

### 4. Assess Complexity and Execute Codex

Before executing, assess task complexity to select appropriate reasoning effort:

1. **Count files involved** in the query
2. **Evaluate scope** (single module vs cross-cutting)
3. **Consider depth** (surface review vs architectural analysis)

Use HEREDOC syntax for safe prompt handling. **Always use the Bash tool's timeout parameter** (minimum 300000ms / 5 minutes).

Redirect output to a temp file to avoid context bloat and race conditions.

**Step 1**: Generate a unique temp file path using `$RANDOM` for randomness:

```bash
CODEX_OUTPUT="/tmp/codex-${RANDOM}${RANDOM}.txt"
```

**Step 2**: Execute Codex and redirect output to the temp file:

```bash
# Select EFFORT based on complexity assessment (low/medium/high/xhigh)
# Bash tool timeout: 5-20 minutes based on complexity
codex exec \
  -m "${MODEL:-gpt-5.2-codex}" \
  -c "model_reasoning_effort=${EFFORT}" \
  --profile "${CODEX_PROFILE:-quiet}" \
  -s read-only \
  --skip-git-repo-check \
  2>/dev/null <<'EOF' > "$CODEX_OUTPUT"
[constructed prompt]
EOF
```

**Important flags:**

- `-m`: Model selection
- `-c model_reasoning_effort=`: Reasoning depth (low/medium/high/xhigh) — select based on Reasoning Effort Guidelines
- `--profile quiet`: Default for this skill (suppresses notify hooks); change only if the user explicitly wants another profile/notifications
- `-s read-only`: Prevents any file modifications (non-negotiable)
- `--skip-git-repo-check`: Works outside git repositories
- `2>/dev/null`: Suppresses thinking tokens from output

**Bash tool timeout**: Estimate based on task complexity (see Timeout Guidelines above). Never use the default 2-minute timeout for Codex operations.

### 5. Present Codex Output

**Step 3**: Read the analysis from the temp file and display to the user:

```bash
cat "$CODEX_OUTPUT"
```

Format the output with clear attribution:

```
## Codex Analysis

[Codex output from the temp file]

---
Model: gpt-5.2-codex | Reasoning: [selected effort level]
```

For very large outputs (>5000 lines), summarize key sections rather than displaying everything.

### 6. Synthesize and Plan

After presenting Codex output:

1. Synthesize key insights from Codex analysis
2. Identify actionable items and critical decisions
3. **If Codex's analysis presents multiple viable approaches or significant trade-offs**, consider using `AskUserQuestion` to clarify user preferences before finalizing the plan
4. Write a structured plan to `~/.claude/plans/[plan-name].md`
5. Call `ExitPlanMode` to present the plan for user approval

**When to use AskUserQuestion:**

- Codex proposes multiple architectures with different trade-offs
- Technology or library choices need user input
- Scope decisions (minimal vs comprehensive) are ambiguous

**Skip clarification when:**

- Codex's recommendations are clear and unambiguous
- User's original request already specified preferences
- Only one viable approach exists

## Error Handling

| Error               | Response                                              |
| ------------------- | ----------------------------------------------------- |
| Codex not installed | Show installation instructions from check script      |
| Codex timeout       | Inform user, suggest simpler query or lower reasoning |
| API rate limit      | Wait and retry, or inform user of limit               |
| Empty response      | Retry once, then report failure                       |

## Usage Examples

### Planning Request

User: "Ask Codex to plan how to add authentication to this app"

1. Validate Codex CLI available
2. Gather relevant codebase context
3. Assess complexity → auth spans multiple modules → `high` reasoning
4. Construct planning prompt with auth requirements
5. Execute Codex with `gpt-5.2-codex` and `high`
6. Present Codex's architecture recommendations
7. Synthesize into Claude plan format
8. Write to `~/.claude/plans/` and call `ExitPlanMode`

### Code Review Request

User: "Have Codex review the changes in src/auth/"

1. Validate Codex CLI available
2. Read files in `src/auth/` directory
3. Assess complexity → single directory, focused review → `medium` reasoning
4. Construct review prompt with file contents
5. Execute Codex review with `medium`
6. Present findings with file/line references
7. Summarize critical issues and recommendations

## Additional Resources

### Reference Files

- **`references/codex-flags.md`** - Complete model and flag documentation

### Scripts

- **`scripts/check-codex.sh`** - Prerequisite validation (run before any Codex command)
