---
name: gemini-cli
description: Use Google's Gemini CLI for web-grounded research (Google Search), automation via one-shot prompts, and second-opinion review. Use when you need structured JSON output, fast scripting workflows, or cross-AI validation.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
---

# Gemini CLI Integration Skill

This skill enables Claude Code to orchestrate Google's **Gemini CLI** reliably using **one-shot prompts** (positional prompt) for scripting and automation.

## When to Use This Skill

### Ideal Use Cases

1. **Second Opinion / Cross-Validation**
   - Code review after writing code (different AI perspective)
   - Security audit with alternative analysis
   - Finding bugs Claude might have missed

2. **Google Search Grounding**
   - Questions requiring current internet information
   - Latest library versions, API changes, documentation updates
   - Current events or recent releases

3. **Automation (One-Shot)**
   - One-shot prompts in CI/scripts with `gemini "..."` (positional prompt)
   - Structured output via `--output-format json`
   - Streaming JSON events via `--output-format stream-json` (only when you explicitly need detailed event traces)

4. **Parallel Processing**
   - Offload tasks while continuing other work
   - Run multiple code generations simultaneously
   - Background documentation generation

5. **Specialized Generation**
   - Test suite generation
   - JSDoc/documentation generation
   - Code translation between languages

### When NOT to Use

- Simple, quick tasks (overhead not worth it)
- Tasks requiring immediate response (rate limits cause delays)
- When context is already loaded and understood
- Interactive refinement requiring conversation

## Core Instructions

### Model policy (pinned for consistency)

In this workspace, run Gemini CLI **with an explicit pinned model** for consistency and deeper reviews:

```bash
gemini --model gemini-3-pro-preview "..."
```

This is intentional: our tests show the pinned `gemini-3-pro-preview` run produces more careful, slower, code-grounded reviews.

### 1. Verify Installation & Auth (Gemini CLI itself)

```bash
command -v gemini && gemini --version
```

If missing, install:

```bash
npm install -g @google/gemini-cli
```

Authenticate (one of):
- **API key**: export `GEMINI_API_KEY=...`
- **OAuth (interactive)**: run `gemini` once and follow the prompts

### 2. Critical Concept: Gemini CLI Has NO Claude Context

Gemini CLI is a separate process. It **does not see this chat**.

Gemini one-shot calls are **not interactive** by default: you get one request and one answer.

To make Gemini effective in one-shot mode, always include:
- **Goal**: what you want and why
- **Inputs**: explicit file paths (or inject files/dirs via `@path`), plus any relevant snippets
- **Constraints**: languages, frameworks, versions, coding style, do/don't rules
- **Deliverable**: exact output shape (e.g. “return JSON”, “output diff”, “output a markdown table”)
- **Scope**: what to touch vs not touch (files/dirs, no network, no deps, etc.)
- **Working directory**: run from the project root so relative paths resolve

### 3. Basic One-Shot Pattern (Recommended)

Use one-shot prompts for predictable, scriptable behavior:

```bash
gemini --model gemini-3-pro-preview "Your prompt here" --output-format text
```

Key flags:
- `--output-format`: `text` (default), `json`, `stream-json`
- `--yolo`, `-y`: Auto-approve all actions
- `--approval-mode`: e.g. `auto_edit`
- `--include-directories`: add extra workspace dirs (comma-separated)
- `--debug`, `-d`: debug output

### 3.1 One-shot prompt checklist (must be exhaustive)

Use this checklist when writing the prompt you pass to `gemini "..."`:

- **Context injection**: include `@path/to/file` / `@src/` where needed (Gemini does not see your repo unless you provide it).
- **Exact task**: “Do X” + acceptance criteria (what counts as “done”).
- **Output contract**:
  - If you want a clean final answer only: say “Output ONLY the final answer. No reasoning.”
  - If you want machine parsing: request `--output-format json` and rely on `.response`.
- **Safety / approvals**:
  - If you want it to act without prompts: use `--yolo` or `--approval-mode auto_edit`.
  - If you want zero traces: avoid `--output-format stream-json` and avoid `--debug`.

### 3.2 Multi-line prompts (practical pattern)

For long instructions, build a multi-line prompt and pass it as one argument:

```bash
PROMPT=$(cat <<'EOF'
Output ONLY the final answer. No reasoning.

Task:
- ...

Inputs:
- @path/to/file
- @src/

Constraints:
- ...

Deliverable:
- ...
EOF
)

gemini --model gemini-3-pro-preview "$PROMPT" --output-format json > /tmp/gemini.json 2> /tmp/gemini.err \
  && jq -r '.response' /tmp/gemini.json > /tmp/gemini.out
```

### 4. Output Handling Best Practice (Low-Token, Reliable)

**Do not stream Gemini output directly into the tool output** for large responses. Instead, redirect to a file and read the file.

```bash
gemini --model gemini-3-pro-preview "Review @backend/src/app.module.ts for security issues" \
  --output-format text \
  --yolo \
  > /tmp/gemini.txt 2> /tmp/gemini.err && echo "Gemini completed"

# Then read with Read tool:
# - /tmp/gemini.txt
# - /tmp/gemini.err (only if needed)
```

### Output only the final answer (no logs / no event stream)

If you want **only the final output** (and to avoid extra CLI chatter), prefer JSON output and extract `.response` into a clean file.

```bash
gemini --model gemini-3-pro-preview "Answer with ONLY the final result. No reasoning. Task: ..." \
  --output-format json \
  --yolo \
  > /tmp/gemini.json 2> /tmp/gemini.err \
  && jq -r '.response' /tmp/gemini.json > /tmp/gemini.out \
  && echo "Gemini completed"

# Then read with Read tool:
# - /tmp/gemini.out   (clean final answer only)
# - /tmp/gemini.err   (only if something went wrong)
```

Avoid these when you want “final output only”:
- `--output-format stream-json` (it emits tool/event traces by design)
- `--debug` (adds verbose debug logs)

For structured automation:

```bash
gemini --model gemini-3-pro-preview "Summarize @README.md in 5 bullets" \
  --output-format json \
  > /tmp/gemini.json 2> /tmp/gemini.err && echo "Gemini completed"

# Extract just the response:
jq -r '.response' /tmp/gemini.json
```

### 5. Critical Behavioral Notes

**Approval behavior**:
- `--yolo` auto-approves all actions.
- `--approval-mode auto_edit` can be a safer middle ground (auto-edit without fully "yolo"-ing everything).

**Rate limits** (documented): CLI auto-retries with backoff; you may see messages like "quota will reset after Xs".

### 6. Injecting Files & Directories into Prompts (`@` commands)

Use `@<path>` in the prompt to inject file/directory contents (git-aware filtering by default):

```bash
gemini --model gemini-3-pro-preview "@src/ Summarize the code in this directory. Focus on architecture." --output-format text
gemini --model gemini-3-pro-preview "What does this file do? @README.md" --output-format text
```

Notes:
- For paths with spaces, escape spaces: `@My\ Documents/file.txt`
- By default, git-ignored paths (e.g. `node_modules/`, `.env`) are excluded (configurable in settings)

### 7. Output Processing (JSON)

For JSON output (`--output-format json`), parse:
```json
{
  "response": "actual content",
  "stats": {
    "models": { "tokens": {...} },
    "tools": { "byName": {...} }
  }
}
```

## Quick Reference Commands

### Code Generation
```bash
gemini --model gemini-3-pro-preview "Create [description] with [features]. Output complete file content." --yolo --output-format text
```

### Code Review
```bash
gemini --model gemini-3-pro-preview "Review @path/to/file for: 1) features, 2) bugs/security issues, 3) improvements" --output-format text
```

### Bug Fixing
```bash
gemini --model gemini-3-pro-preview "Fix these bugs in @path/to/file: [list]. Apply fixes now." --yolo --output-format text
```

### Test Generation
```bash
gemini --model gemini-3-pro-preview "Generate [Jest/pytest] tests for @path/to/file. Focus on [areas]." --yolo --output-format text
```

### Documentation
```bash
gemini --model gemini-3-pro-preview "Generate JSDoc for all functions in @path/to/file. Output as markdown." --yolo --output-format text
```

### Web Research
```bash
gemini --model gemini-3-pro-preview "What are the latest [topic]? Use Google Search." --output-format text
```

## Error Handling

### Rate Limit Exceeded
- CLI auto-retries with backoff
- Run in background for long operations

### Command Failures
- Prefer `--output-format json` and inspect `.error` (if present)
- Verify Gemini is authenticated and available: `gemini --version`
- Check settings: `~/.gemini/settings.json` and `.gemini/settings.json`

### Validation After Generation
Always verify Gemini's output:
- Check for security vulnerabilities (XSS, injection)
- Test functionality matches requirements
- Review code style consistency
- Verify dependencies are appropriate

## Integration Workflow

### Standard Generate-Review-Fix Cycle

```bash
# 1. Generate
gemini --model gemini-3-pro-preview "Create [code]" --yolo --output-format text

# 2. Review (Gemini reviews its own work)
gemini --model gemini-3-pro-preview "Review @path/to/file for bugs and security issues" --output-format text

# 3. Fix identified issues
gemini --model gemini-3-pro-preview "Fix [issues] in @path/to/file. Apply now." --yolo --output-format text
```

### Background Execution

For long tasks, run in background and monitor:
```bash
gemini --model gemini-3-pro-preview "[long task]" --yolo --output-format text > /tmp/gemini-long.txt 2>&1 &
# Monitor by reading /tmp/gemini-long.txt
```

## Gemini CLI Capabilities Worth Using

Notable built-in tools:
- **`google_web_search`**: real-time web search grounding
- **`web_fetch`**: fetch & summarize specific URLs
- **`run_shell_command`**: execute shell commands (be careful)

## Configuration

### Project Context (Optional)

Create `.gemini/GEMINI.md` in project root for persistent context that Gemini will automatically read.

## See Also

- `reference.md` - Complete command and flag reference
- `templates.md` - Prompt templates for common operations
- `patterns.md` - Advanced integration patterns
- `tools.md` - Gemini's built-in tools documentation
- `image-generation.md` - Practical notes for image generation (nanobanana)
