---
name: review-agentmd
description: Review recent conversations to find improvements for AGENTS.md files.
---

# Review AGENTS.md from conversation history

Analyze recent conversations to improve both global (~/.codex/AGENTS.md) and local (project) AGENTS.md files.

## Step 1: Find conversation history

The conversation history is in `~/.codex/sessions/`.

```bash
# List recent sessions
ls -lt ~/.codex/sessions/ | head -20
```

## Step 2: Extract recent conversations

Extract the 15-20 most recent conversations (excluding the current one) to a temp directory:

```bash
SCRATCH=/tmp/agentmd-review-$(date +%s)
mkdir -p "$SCRATCH"

for f in $(ls -t ~/.codex/sessions/*.jsonl 2>/dev/null | head -20); do
  basename=$(basename "$f" .jsonl)
  cat "$f" | jq -r '
    if .type == "user" then
      "USER: " + (.message.content // "")
    elif .type == "assistant" then
      "ASSISTANT: " + ((.message.content // []) | map(select(.type == "text") | .text) | join("\n"))
    else
      empty
    end
  ' 2>/dev/null | grep -v "^ASSISTANT: $" > "$SCRATCH/${basename}.txt"
done

ls -lhS "$SCRATCH"
```

## Step 3: Analyze conversations

Review each conversation file and compare against both AGENTS.md files:
- Global: `~/.codex/AGENTS.md`
- Local: `./AGENTS.md` (if exists)

For each conversation, look for:
1. Instructions that exist but were violated (need reinforcement or rewording)
2. Patterns that should be added to LOCAL AGENTS.md (project-specific)
3. Patterns that should be added to GLOBAL AGENTS.md (applies everywhere)
4. Anything in either file that seems outdated or unnecessary

## Step 4: Aggregate findings

Combine results into a summary with these sections:

1. **Instructions violated** - existing rules that weren't followed (need stronger wording)
2. **Suggested additions - LOCAL** - project-specific patterns
3. **Suggested additions - GLOBAL** - patterns that apply everywhere
4. **Potentially outdated** - items that may no longer be relevant

Present as tables or bullet points. Ask user if they want edits drafted.
