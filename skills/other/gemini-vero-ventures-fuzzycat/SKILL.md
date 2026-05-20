---
name: gemini
description: >
  Offload tasks to Google Gemini CLI to preserve Claude credits. Gemini has internet access
  and strong code analysis. Use for code reviews, summaries, test generation, diff analysis,
  and general questions. Prefer Gemini over Ollama when internet/API knowledge is needed.
allowed-tools: Bash, Read, Grep, Glob
---

# Google Gemini CLI Offloading

You have access to the **Gemini CLI** (`gemini`) for offloading tasks. Gemini runs Google's
latest model with sandbox mode (no file system access) and provides fast, high-quality responses
for code analysis tasks. It's already authenticated.

## When to Use Gemini vs Ollama vs Claude

| Task | First choice | Why |
|------|-------------|-----|
| Quick syntax/API questions | Ollama | Fastest (~0.5s warm), offline |
| File summarization | Ollama | Fast, no network needed |
| Code review | Gemini | Better reasoning, current API knowledge |
| Diff analysis | Gemini | Catches more subtle issues |
| Test generation | Gemini | Better at idiomatic test patterns |
| Questions needing current docs | Gemini | Has internet access |
| Multi-file architecture | Claude | Needs conversation context + tools |
| Running tests / debugging | Claude | Needs tool access |
| Financial/security logic | Claude | Highest accuracy required |

**Decision flow:**
1. Can Ollama handle it? (simple, offline-capable) → Use Ollama
2. Needs better reasoning or current knowledge? → Use Gemini
3. Needs tools, context, or highest accuracy? → Use Claude

## How to Use

```bash
# Check availability
.claude/skills/gemini/gemini.sh status

# Quick question
.claude/skills/gemini/gemini.sh query "How do Stripe destination charges work with application fees?"

# Summarize a file
.claude/skills/gemini/gemini.sh summarize server/services/payout.ts

# Review code
.claude/skills/gemini/gemini.sh review components/shared/captcha.tsx

# Analyze a diff
git diff --staged | .claude/skills/gemini/gemini.sh diff

# Generate test stubs
.claude/skills/gemini/gemini.sh test-gen server/services/founding-clinic.ts
```

## Important Notes

- **Sandbox mode (`-s`)**: Gemini runs sandboxed — it cannot read/write local files. All file
  content must be passed via the prompt. This is intentional for security.
- **Auth may expire.** If Gemini fails with auth errors, the user needs to run `gemini`
  interactively to re-authenticate. If unavailable, fall back to Ollama or Claude silently.
- **Rate limits apply.** Google has API rate limits. Don't send rapid-fire batch requests.
  Space requests or use Ollama for batch file summarization.
- **Gemini sees project context** by default (reads GEMINI.md / local files). Sandbox mode
  prevents tool execution but the CLI may still provide context from the project.
- **Response time**: ~3-8s per request (network latency). Slower than warm Ollama but faster
  than cold Ollama.
