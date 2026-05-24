---
name: ai-orchestration
description: Multi-model AI collaboration via orchestrator MCP. Use when seeking second opinions, debugging complex issues, building consensus on architectural decisions, conducting code reviews, or needing external validation on analysis.
triggers: second opinion, multi-model, consensus, external AI, codex, gemini, model comparison, AI collaboration, expert validation, parallel AI, ai_spawn, ai_fetch
---

# AI CLI Orchestration

Query external AI models (claude, codex, gemini) for second opinions, debugging, consensus building, and expert validation.

## Tools Overview

| Tool        | Mode        | Description                                  |
| ----------- | ----------- | -------------------------------------------- |
| `ai_call`   | Synchronous | Call AI and wait for result                  |
| `ai_spawn`  | Async       | Start AI in background, get job ID           |
| `ai_fetch`  | Async       | Get result from spawned AI (with timeout)    |
| `ai_list`   | Utility     | List all running/completed AI jobs           |
| `ai_review` | Convenience | Spawn all 3 AIs in parallel with same prompt |

## Role Hierarchy

| CLI    | Role        | Mode      | Capabilities                       |
| ------ | ----------- | --------- | ---------------------------------- |
| claude | Worker/Peer | Full      | Can execute any tool/command       |
| codex  | Reviewer    | Read-only | Code review, analysis, suggestions |
| gemini | Researcher  | Read-only | Web search, documentation lookup   |

## Parallel Execution (Recommended)

```python
# Spawn all 3 models in parallel
claude_job = ai_spawn(cli="claude", prompt="Analyze this code for bugs...")
codex_job = ai_spawn(cli="codex", prompt="Review this code for patterns...")
gemini_job = ai_spawn(cli="gemini", prompt="Research best practices for...")

# All running simultaneously! Fetch results:
claude_result = ai_fetch(job_id=claude_job.job_id, timeout=120)
codex_result = ai_fetch(job_id=codex_job.job_id, timeout=120)
gemini_result = ai_fetch(job_id=gemini_job.job_id, timeout=120)

# Total time = slowest model (~60s) instead of sum (~180s)
```

Or use `ai_review` for convenience:

```python
review = ai_review(prompt="Analyze this architecture decision...", files=["src/"])
claude_result = ai_fetch(job_id=review.jobs["claude"].job_id, timeout=120)
```

## When to Use External Models

**Do use when:** Stuck on complex bugs, architectural decisions with tradeoffs, need validation before major refactoring, security-sensitive code, want diverse perspectives

**Don't use when:** Simple work, already confident, just executing known solution

## References

- **Tool parameters**: See [references/tools.md](references/tools.md)
- **Usage patterns**: See [references/patterns.md](references/patterns.md)
- **Sub-agents**: See [references/sub-agents.md](references/sub-agents.md)

## Tips

- **Use parallel for multi-model**: `ai_spawn` + `ai_fetch` is 3x faster than sequential
- **Be specific**: Include file paths, error messages, and context
- **Use appropriate CLI**: codex for code review, gemini for web search
- **Delegate complex work**: Use sub-agents for structured analysis
- **Remember read-only**: Codex and Gemini cannot execute commands or modify files
- **Include files**: Use the `files` parameter to provide code context
- **Monitor jobs**: Use `ai_list()` to check status of all running jobs
