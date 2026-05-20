---
name: codex-chat
description: Interactive REPL workflows with Codex CLI including session management, multimodal conversations, and automated execution. Use for extended development sessions, debugging, or collaborative problem-solving.
---

# Codex Interactive Chat

Advanced interactive workflows with Codex CLI REPL featuring full automation and session management.

**Last Updated**: December 2025 (GPT-5.2 Release)

## Quick Start

```bash
# Start interactive session
codex "Let's work on improving authentication"

# With full automation
codex --dangerously-bypass-approvals-and-sandbox "Auto-execute everything"

# With specific model (December 2025)
codex -m gpt-5.1-codex-max "Complex development task"  # Default, best for coding
codex -m gpt-5.2 "Tasks needing 400K context"
codex -m gpt-5.2-pro "Maximum accuracy tasks"

# With images
codex -i design.png "Implement this UI design"

# With web search
codex --search "Research and implement OAuth2"
```

## Automated Interactive Workflows

```bash
# Full auto development session (December 2025)
codex --dangerously-bypass-approvals-and-sandbox \
  -m gpt-5.1-codex-max \
  --search \
  "Build complete user authentication system"

# With GPT-5.2 for long-context tasks
codex --dangerously-bypass-approvals-and-sandbox \
  -m gpt-5.2 \
  --compact \
  "Analyze entire codebase and refactor"

# Sandboxed automation
codex --full-auto "Refactor safely with tests"
```

## Session Management

```bash
# Resume last session
codex exec resume --last

# Pick session to resume
codex resume

# Apply latest changes from session
codex apply
# or
codex a
```

## Multimodal Development

```bash
# With single image
codex -i mockup.png --dangerously-bypass-approvals-and-sandbox \
  "Implement this design perfectly"

# With multiple images
codex -i design1.png -i design2.png --full-auto \
  "Compare and implement best approach"
```

## Automation Patterns

### Continuous Development

```bash
#!/bin/bash
# Automated feature development session (December 2025)

dev_session() {
  local feature="$1"

  codex --dangerously-bypass-approvals-and-sandbox \
    --search \
    -m gpt-5.1-codex-max \
    "Feature: $feature

    Execute automatically:
    1. Research best practices
    2. Create implementation plan
    3. Generate all code
    4. Write comprehensive tests
    5. Run tests and fix failures
    6. Generate documentation
    7. Create git commits
    8. Summarize changes"
}

# For complex tasks requiring high accuracy
dev_session_pro() {
  local feature="$1"

  codex --dangerously-bypass-approvals-and-sandbox \
    -m gpt-5.2-pro \
    --reasoning-effort xhigh \
    "Feature: $feature - Implement with maximum accuracy"
}

# Usage
dev_session "user profile caching"
dev_session_pro "payment processing system"
```

## Related Skills

- `codex-cli`: Main integration
- `codex-auth`: Authentication
- `codex-tools`: Tool execution
- `codex-review`: Code review
- `codex-git`: Git workflows
