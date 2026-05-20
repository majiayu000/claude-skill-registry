---
name: ollama
description: >
  Offload simple tasks to local Ollama LLM to preserve Claude credits. Use for code summaries,
  file analysis, diff reviews, quick questions about syntax/APIs, and pre-screening code before
  deeper Claude analysis. Invoke automatically when exploring files or reviewing code.
allowed-tools: Bash, Read, Grep, Glob
---

# Local Ollama LLM Offloading

You have access to a **local Ollama instance** at `http://localhost:11434/` for offloading tasks
that don't need Claude's full capabilities. This saves token credits for complex reasoning,
multi-step planning, and tool-heavy workflows.

## When to Use Ollama

**ALWAYS prefer Ollama for these tasks (saves ~90% of credits for routine work):**
- Summarizing individual files (purpose, exports, structure)
- Reviewing code for bugs, style issues, or security problems
- Analyzing git diffs before committing
- Quick syntax/API questions ("What does X do in TypeScript?")
- Generating boilerplate (simple CRUD, test stubs, type definitions)
- Explaining grep/search results in context
- Pre-screening large codebases before deep Claude analysis
- Drafting commit messages, PR descriptions, or documentation
- Generating Zod schemas, Drizzle table definitions from descriptions
- Writing test cases from function signatures

**Use Claude (not Ollama) for:**
- Multi-file architectural decisions requiring conversation context
- Complex debugging requiring tool access (running tests, reading errors)
- Tasks requiring web search, browser interaction, or external APIs
- Security-sensitive financial logic (payment calculations, Stripe integration)
- Anything requiring previous conversation context

## How to Use

The helper script is at `.claude/skills/ollama/ollama.sh`. Run via Bash:

```bash
# Check availability and which model is loaded
.claude/skills/ollama/ollama.sh status

# Quick question (fast, no reasoning ~0.5-2s warm)
.claude/skills/ollama/ollama.sh query "What does pgEnum do in Drizzle?"

# Deep question (with reasoning, slower ~10-30s)
.claude/skills/ollama/ollama.sh think "Should I use a db transaction for this?"

# Summarize a file
.claude/skills/ollama/ollama.sh summarize server/services/payout.ts

# Review code for issues
.claude/skills/ollama/ollama.sh review components/shared/captcha.tsx

# Analyze a diff
git diff --staged | .claude/skills/ollama/ollama.sh diff

# Explain grep matches
.claude/skills/ollama/ollama.sh grep-explain "calculateApplicationFee" server/services/payout.ts
```

## Graceful Degradation

- **Server may not be running.** If Ollama is unavailable, fall back to Claude silently — never
  error out to the user or ask them about it. Just do the work yourself.
- **The model changes over time.** The script auto-discovers whatever model is available. Don't
  hardcode model names. Current models use a thinking mode that the script handles automatically.
- **Cold start: ~5-10s.** First request after idle loads the model to GPU. Run `status` early
  in a session to warm up. Subsequent requests are fast (~0.5-2s).
- **Not a replacement for Claude.** Ollama handles routine read/analyze tasks but lacks tool
  access, conversation context, and Claude's reasoning depth. Use it as a first pass.

## Batch Workflow Patterns

### Explore a directory (instead of reading every file yourself)
```bash
for f in server/services/*.ts; do
  echo "=== $f ==="; .claude/skills/ollama/ollama.sh summarize "$f"; echo
done
```

### Pre-review before committing
```bash
git diff --staged | .claude/skills/ollama/ollama.sh diff
```

### Generate test stubs
```bash
.claude/skills/ollama/ollama.sh query "Write bun:test stubs for: export function getEffectiveShareRate(clinic: { revenueShareBps: number; foundingClinic: boolean; foundingExpiresAt: Date | null }): number"
```
