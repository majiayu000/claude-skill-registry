---
name: token-usage
description: Sprawdzenie zużycia tokenów/kontekstu w sesji. Triggers: token usage, ile tokenów, ile zostało
---

# token-usage

## Trigger
When user says **"@token-usage"**, **"token usage"**, **"context window"**, or **"token cost"**.

---

## Actions

1. When user asks about current AI token/context usage (e.g., "token usage", "context window", "how many tokens"), respond with ONLY this format:

**Tokens: [used]/[total] ([remaining] remaining, [percentage]% used)**

No explanations. No additional text. Just the numbers.

2. When asked about token cost of specific files/code/systems (e.g., "How expensive is CHANGELOG?", "Token cost of Log File Genius?"), analyze the component(s) and runtime dependencies. For each component, report in two paragraphs: (1) token breakdown, (2) dependencies that load when used.

**Note:**
- For systems (e.g., "Log File Genius"), analyze all related files and rules
- For multiple targets, analyze each separately
- Ignore non-AI token references (OAuth, JWT, API tokens)
