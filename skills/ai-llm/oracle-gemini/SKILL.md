---
name: oracle-gemini
description: This skill should be used when the user asks to "use Gemini", "ask Gemini", "consult Gemini", "Gemini review", "use Gemini for planning", "ask Gemini to review", "get Gemini's opinion", "what does Gemini think", "second opinion from Gemini", mentions using Gemini as an oracle for planning or code review. NOT for implementation tasks.
context: fork
agent: Plan
---

# Gemini Oracle

Use Google Gemini CLI as a **planning oracle** and **code reviewer**. Gemini provides analysis and recommendations; Claude synthesizes and presents to the user.

**Critical**: This skill is for planning and review ONLY. Never use Gemini to implement changes.

## Prerequisites

Before invoking Gemini, validate availability:

```bash
~/.claude/skills/oracle-gemini/scripts/check-gemini.sh
```

If the script exits non-zero, display the error message and stop. Do not proceed without Gemini CLI.

## Configuration Defaults

| Setting | Default           | User Override            |
| ------- | ----------------- | ------------------------ |
| Model   | `gemini-2.5-pro`  | "use flash"              |
| Sandbox | `--sandbox`       | Not overridable (safety) |
| Timeout | 5 minutes minimum | Based on complexity      |
| Output  | `text`            | "use json output"        |

### Timeout Guidelines

When invoking `gemini` via the Bash tool, always set an appropriate timeout:

- **Minimum**: 5 minutes (300000ms) for any Gemini operation
- **Simple queries** (single file review, focused question): 5 minutes (300000ms)
- **Moderate complexity** (multi-file review, feature planning): 10 minutes (600000ms)
- **High complexity** (architecture analysis, large codebase planning): 15 minutes (900000ms)

### Model Selection

Choose model based on task requirements:

| Model              | Best For                                             | Speed   |
| ------------------ | ---------------------------------------------------- | ------- |
| `gemini-2.5-pro`   | Complex analysis, architecture, comprehensive review | Slower  |
| `gemini-2.5-flash` | Quick feedback, single-file review, rapid iteration  | Fastest |

**Selection heuristics:**

- **`gemini-2.5-pro`**: Task involves multiple files, requires deep analysis, or architectural thinking
- **`gemini-2.5-flash`**: Simple queries, single file review, or when speed is prioritized

For detailed model capabilities, consult `references/gemini-flags.md`.

## Workflow

### 1. Validate Prerequisites

Run the check script. On failure, report the installation instructions and abort.

### 2. Determine Mode

- **Planning mode**: User wants architecture, implementation approach, or design decisions
- **Review mode**: User wants code analysis, bug detection, or improvement suggestions

### 3. Construct Prompt

Build a focused prompt for Gemini based on mode:

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

### 4. Select Model and Execute Gemini

Before executing, assess task complexity to select appropriate model:

1. **Count files involved** in the query
2. **Evaluate scope** (single module vs cross-cutting)
3. **Consider depth** (surface review vs architectural analysis)

Use **positional prompt syntax** (Gemini CLI does NOT support HEREDOC/stdin). **Always use the Bash tool's timeout parameter** (minimum 300000ms / 5 minutes).

For short prompts, pass directly as a positional argument:

```bash
# Short prompt - direct positional argument
gemini -m gemini-2.5-pro --sandbox -o text "Your prompt here" 2>/dev/null
```

For long prompts, write to a temp file first, then use command substitution:

```bash
# Step 1: Generate unique temp file paths and write prompt
GEMINI_PROMPT="/tmp/gemini-${RANDOM}${RANDOM}.txt"
GEMINI_OUTPUT="/tmp/gemini-${RANDOM}${RANDOM}.txt"
cat > "$GEMINI_PROMPT" <<'EOF'
[constructed prompt with code context]
EOF

# Step 2: Execute Gemini with prompt from file
# Bash tool timeout: 300000-900000ms based on complexity
gemini \
  -m "${MODEL:-gemini-2.5-pro}" \
  --sandbox \
  -o text \
  "$(cat "$GEMINI_PROMPT")" \
  2>/dev/null > "$GEMINI_OUTPUT"
```

**Important flags:**

- `-m`: Model selection (gemini-2.5-pro or gemini-2.5-flash)
- `--sandbox`: Prevents any file modifications (non-negotiable)
- `-o text`: Plain text output (use `json` if user requests structured output)
- `2>/dev/null`: Suppresses error messages and stderr noise

**Bash tool timeout**: Estimate based on task complexity (see Timeout Guidelines above). Never use the default 2-minute timeout for Gemini operations.

### 5. Present Gemini Output

Read the analysis from the temp file and display to the user with clear attribution:

```bash
cat "$GEMINI_OUTPUT"
```

Format the output with clear attribution:

```
## Gemini Analysis

[Gemini output from /tmp/gemini-analysis.txt]

---
Model: gemini-2.5-pro
```

For very large outputs (>5000 lines), summarize key sections rather than displaying everything.

### 6. Synthesize and Plan

After presenting Gemini output:

1. Synthesize key insights from Gemini analysis
2. Identify actionable items and critical decisions
3. **If Gemini's analysis presents multiple viable approaches or significant trade-offs**, consider using `AskUserQuestion` to clarify user preferences before finalizing the plan
4. Write a structured plan to `~/.claude/plans/[plan-name].md`
5. Call `ExitPlanMode` to present the plan for user approval

**When to use AskUserQuestion:**

- Gemini proposes multiple architectures with different trade-offs
- Technology or library choices need user input
- Scope decisions (minimal vs comprehensive) are ambiguous

**Skip clarification when:**

- Gemini's recommendations are clear and unambiguous
- User's original request already specified preferences
- Only one viable approach exists

## Error Handling

| Error                | Response                                              |
| -------------------- | ----------------------------------------------------- |
| Gemini not installed | Show installation instructions from check script      |
| Gemini timeout       | Inform user, suggest simpler query or use flash model |
| API rate limit       | Wait and retry, or inform user of limit               |
| Empty response       | Retry once, then report failure                       |

## Usage Examples

### Planning Request

User: "Ask Gemini to plan how to add authentication to this app"

1. Validate Gemini CLI available
2. Gather relevant codebase context
3. Assess complexity → auth spans multiple modules → use `gemini-2.5-pro`
4. Construct planning prompt with auth requirements
5. Execute Gemini with `gemini-2.5-pro` model
6. Present Gemini's architecture recommendations
7. Synthesize into Claude plan format
8. Write to `~/.claude/plans/` and call `ExitPlanMode`

### Code Review Request

User: "Have Gemini review the changes in src/auth/"

1. Validate Gemini CLI available
2. Read files in `src/auth/` directory
3. Assess complexity → single directory, focused review → use `gemini-2.5-flash` for speed
4. Construct review prompt with file contents
5. Execute Gemini review
6. Present findings with file/line references
7. Summarize critical issues and recommendations

### Model Override Request

User: "Ask Gemini with flash model to review this function"

1. Validate Gemini CLI available
2. Read the target function
3. User explicitly requested flash model → use `gemini-2.5-flash`
4. Construct focused review prompt
5. Execute Gemini with flash model
6. Present quick feedback

## Additional Resources

### Reference Files

- **`references/gemini-flags.md`** - Complete model and flag documentation

### Scripts

- **`scripts/check-gemini.sh`** - Prerequisite validation (run before any Gemini command)
