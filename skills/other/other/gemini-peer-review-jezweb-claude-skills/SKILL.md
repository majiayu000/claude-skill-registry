---
name: gemini-peer-review
description: "Get a second opinion from Gemini on code, architecture, debugging, or security. Uses direct Gemini API calls — no CLI dependencies. Trigger with 'ask gemini', 'gemini review', 'second opinion', 'peer review', or 'consult gemini'."
compatibility: claude-code-only
---

# Gemini Peer Review

Consult Gemini as a coding peer for a second opinion on code quality, architecture decisions, debugging, or security reviews.

## Setup

**API Key**: Set `GEMINI_API_KEY` as an environment variable. Get a key from https://aistudio.google.com/apikey if you don't have one.

```bash
export GEMINI_API_KEY="your-key-here"
```

## Workflow

1. **Determine mode** from user request (review, architect, debug, security, quick)
2. **Read target files** into context
3. **Build prompt** using the AI-to-AI template from [references/prompt-templates.md](references/prompt-templates.md)
4. **Write prompt to file** at `.claude/artifacts/gemini-prompt.txt` (avoids shell escaping issues)
5. **Call the API** — generate a Python script that:
   - Reads `GEMINI_API_KEY` from environment
   - Reads the prompt from `.claude/artifacts/gemini-prompt.txt`
   - POSTs to `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
   - Payload: `{"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3, "maxOutputTokens": 8192}}`
   - Extracts text from `candidates[0].content.parts[0].text`
   - Prints result to stdout

   Write the script to `.claude/scripts/gemini-review.py` and run it.

6. **Synthesize** — present Gemini's findings, add your own perspective (agree/disagree), let the user decide what to implement

## Modes

### Code Review

Review specific files for bugs, logic errors, security vulnerabilities, performance issues, and best practice violations.

Read the target files, build a prompt using the Code Review template, call with `gemini-2.5-flash`.

### Architecture Advice

Get feedback on design decisions with trade-off analysis. Include project context (CLAUDE.md, relevant source files).

Read project context, build a prompt using the Architecture template, call with `gemini-2.5-pro`.

### Debugging Help

Analyse errors when stuck after 2+ failed fix attempts. Gemini sees the code fresh without your debugging context bias.

Read the problematic files, build a prompt using the Debug template (include error message and previous attempts), call with `gemini-2.5-flash`.

### Security Scan

Scan code for security vulnerabilities (injection, auth bypass, data exposure).

Read the target directory's source files, build a prompt using the Security template, call with `gemini-2.5-pro`.

### Quick Question

Fast question without file context. Build prompt inline, write to file, call with `gemini-2.5-flash`.

## Model Selection

| Mode | Model | Why |
|------|-------|-----|
| review, debug, quick | `gemini-2.5-flash` | Fast, good for straightforward analysis |
| architect, security-scan | `gemini-2.5-pro` | Better reasoning for complex trade-offs |

Check current model IDs if errors occur — they change frequently:

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY" | python3 -c "import sys,json; [print(m['name']) for m in json.load(sys.stdin)['models'] if 'gemini' in m['name']]"
```

## When to Use

**Good use cases**:
- Before committing major changes (final review)
- When stuck debugging after multiple attempts
- Architecture decisions with multiple valid options
- Security-sensitive code review

**Avoid using for**:
- Simple syntax checks (Claude handles these faster)
- Every single edit (too slow, unnecessary)
- Questions with obvious answers

## Prompt Construction

**Critical**: Always use the AI-to-AI prompting format. Write the full prompt to a file — never pass code inline via bash arguments (shell escaping will break it).

When building the prompt:
1. Start with the AI-to-AI header from [references/prompt-templates.md](references/prompt-templates.md)
2. Append the mode-specific template
3. Append the file contents with clear `--- filename ---` separators
4. Write to `.claude/artifacts/gemini-prompt.txt`
5. Generate and run the API call script

## Reference Files

| When | Read |
|------|------|
| Building prompts for any mode | [references/prompt-templates.md](references/prompt-templates.md) |
