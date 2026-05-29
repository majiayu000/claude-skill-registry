---
name: introspect
description: "Analyze Claude Code session logs - extract thinking blocks, tool usage stats, error patterns, debug trajectories. Triggers on: introspect, session logs, trajectory, analyze sessions, what went wrong, tool usage, thinking blocks, session history, my reasoning, past sessions, what did I do."
allowed-tools: "Bash Read Grep Glob"
---

# Introspect

Extract actionable intelligence from Claude Code session logs. Analyze tool usage, reasoning patterns, errors, and conversation flow to improve workflows and debug issues.

## Log File Structure

```
~/.claude/
├── history.jsonl                              # Global: all user inputs across projects
├── projects/
│   └── {project-path}/                        # e.g., X--Dev-claude-mods/
│       ├── sessions-index.json                # Session metadata index
│       ├── {session-uuid}.jsonl               # Full session transcript
│       └── agent-{short-id}.jsonl             # Subagent transcripts
```

### Project Path Encoding

Project paths use double-dash encoding: `X:\Dev\claude-mods` → `X--Dev-claude-mods`

```bash
# Find project directory for current path
project_dir=$(pwd | sed 's/[:\\\/]/-/g' | sed 's/--*/-/g')
ls ~/.claude/projects/ | grep -i "${project_dir##*-}"
```

## Entry Types in Session Files

| Type | Contains | Key Fields |
|------|----------|------------|
| `user` | User messages | `message.content`, `uuid`, `timestamp` |
| `assistant` | Claude responses | `message.content[]`, `cwd`, `gitBranch` |
| `thinking` | Reasoning blocks | `thinking`, `signature` (in content array) |
| `tool_use` | Tool invocations | `name`, `input`, `id` (in content array) |
| `tool_result` | Tool outputs | `tool_use_id`, `content` |
| `summary` | Conversation summaries | `summary`, `leafUuid` |
| `file-history-snapshot` | File state checkpoints | File contents at point in time |
| `system` | System context | Initial context, rules |

## Core Analysis Patterns

### List Sessions for Current Project

```bash
# Get sessions index
cat ~/.claude/projects/X--Dev-claude-mods/sessions-index.json | jq '.'

# List session files with sizes and dates
ls -lah ~/.claude/projects/X--Dev-claude-mods/*.jsonl | grep -v agent
```

### Session Overview

```bash
SESSION="417ce03a-6fc7-4906-b767-6428338f34c3"
PROJECT="X--Dev-claude-mods"

# Entry type distribution
jq -r '.type' ~/.claude/projects/$PROJECT/$SESSION.jsonl | sort | uniq -c

# Session duration (first to last timestamp)
jq -s '[.[].timestamp // .[].message.timestamp | select(.)] | [min, max] | map(. / 1000 | strftime("%Y-%m-%d %H:%M"))' \
  ~/.claude/projects/$PROJECT/$SESSION.jsonl

# Conversation summaries (quick overview)
jq -r 'select(.type == "summary") | .summary' ~/.claude/projects/$PROJECT/$SESSION.jsonl
```

### Tool Usage Statistics

```bash
PROJECT="X--Dev-claude-mods"

# Tool frequency across all sessions
cat ~/.claude/projects/$PROJECT/*.jsonl | \
  jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' | \
  sort | uniq -c | sort -rn

# Tool frequency for specific session
jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' \
  ~/.claude/projects/$PROJECT/$SESSION.jsonl | sort | uniq -c | sort -rn

# Tools with their inputs (sampled)
jq -c 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | {tool: .name, input: .input}' \
  ~/.claude/projects/$PROJECT/$SESSION.jsonl | head -20
```

### Extract Thinking Blocks

```bash
SESSION="417ce03a-6fc7-4906-b767-6428338f34c3"
PROJECT="X--Dev-claude-mods"

# All thinking blocks (reasoning trace)
jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "thinking") | .thinking' \
  ~/.claude/projects/$PROJECT/$SESSION.jsonl

# Thinking blocks with context (which turn)
jq -r 'select(.type == "assistant") |
  .message.content as $content |
  ($content | map(select(.type == "thinking")) | .[0].thinking) as $thinking |
  ($content | map(select(.type == "text")) | .[0].text | .[0:100]) as $response |
  select($thinking) | "---\nThinking: \($thinking[0:500])...\nResponse: \($response)..."' \
  ~/.claude/projects/$PROJECT/$SESSION.jsonl
```

### Error Analysis

```bash
PROJECT="X--Dev-claude-mods"

# Find tool errors across sessions
cat ~/.claude/projects/$PROJECT/*.jsonl | \
  jq -r 'select(.type == "user") | .message.content[]? | select(.type == "tool_result") |
    select(.content | test("error|Error|ERROR|failed|Failed|FAILED"; "i")) |
    {tool_id: .tool_use_id, error: .content[0:200]}' 2>/dev/null | head -50

# Count errors by pattern
cat ~/.claude/projects/$PROJECT/*.jsonl | \
  jq -r 'select(.type == "user") | .message.content[]? | select(.type == "tool_result") | .content' 2>/dev/null | \
  grep -i "error\|failed\|exception" | \
  sed 's/[0-9]\+//g' | sort | uniq -c | sort -rn | head -20
```

### Search Across Sessions

```bash
PROJECT="X--Dev-claude-mods"

# Search user messages
cat ~/.claude/projects/$PROJECT/*.jsonl | \
  jq -r 'select(.type == "user") | .message.content[]? | select(.type == "text") | .text' | \
  grep -i "pattern"

# Search assistant responses
cat ~/.claude/projects/$PROJECT/*.jsonl | \
  jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "text") | .text' | \
  grep -i "pattern"

# Find sessions mentioning a file
for f in ~/.claude/projects/$PROJECT/*.jsonl; do
  if grep -q "specific-file.ts" "$f"; then
    echo "Found in: $(basename $f)"
  fi
done
```

### Conversation Flow Reconstruction

```bash
SESSION="417ce03a-6fc7-4906-b767-6428338f34c3"
PROJECT="X--Dev-claude-mods"

# Reconstruct conversation (user/assistant turns)
jq -r '
  if .type == "user" then
    .message.content[]? | select(.type == "text") | "USER: \(.text[0:200])"
  elif .type == "assistant" then
    .message.content[]? | select(.type == "text") | "CLAUDE: \(.text[0:200])"
  else empty end
' ~/.claude/projects/$PROJECT/$SESSION.jsonl
```

### Subagent Analysis

```bash
PROJECT="X--Dev-claude-mods"

# List subagent sessions
ls ~/.claude/projects/$PROJECT/agent-*.jsonl 2>/dev/null

# Subagent tool usage
for f in ~/.claude/projects/$PROJECT/agent-*.jsonl; do
  echo "=== $(basename $f) ==="
  jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' "$f" | \
    sort | uniq -c | sort -rn | head -5
done
```

## Advanced Analysis

### Token/Cost Estimation

```bash
SESSION="417ce03a-6fc7-4906-b767-6428338f34c3"
PROJECT="X--Dev-claude-mods"

# Rough character count (tokens ≈ chars/4)
jq -r '[
  (select(.type == "user") | .message.content[]? | select(.type == "text") | .text | length),
  (select(.type == "assistant") | .message.content[]? | select(.type == "text") | .text | length)
] | add' ~/.claude/projects/$PROJECT/$SESSION.jsonl | \
  awk '{sum+=$1} END {print "Total chars:", sum, "Est tokens:", int(sum/4)}'
```

### File Modification Tracking

```bash
SESSION="417ce03a-6fc7-4906-b767-6428338f34c3"
PROJECT="X--Dev-claude-mods"

# Files edited (Edit tool usage)
jq -r 'select(.type == "assistant") | .message.content[]? |
  select(.type == "tool_use" and .name == "Edit") | .input.file_path' \
  ~/.claude/projects/$PROJECT/$SESSION.jsonl | sort | uniq -c | sort -rn

# Files written
jq -r 'select(.type == "assistant") | .message.content[]? |
  select(.type == "tool_use" and .name == "Write") | .input.file_path' \
  ~/.claude/projects/$PROJECT/$SESSION.jsonl | sort | uniq
```

### Session Comparison

```bash
PROJECT="X--Dev-claude-mods"
SESSION1="session-id-1"
SESSION2="session-id-2"

# Compare tool usage between sessions
echo "=== Session 1 ===" && \
jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' \
  ~/.claude/projects/$PROJECT/$SESSION1.jsonl | sort | uniq -c | sort -rn

echo "=== Session 2 ===" && \
jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' \
  ~/.claude/projects/$PROJECT/$SESSION2.jsonl | sort | uniq -c | sort -rn
```

## Quick Reference Commands

| Task | Command Pattern |
|------|-----------------|
| List sessions | `ls -lah ~/.claude/projects/$PROJECT/*.jsonl \| grep -v agent` |
| Entry types | `jq -r '.type' $SESSION.jsonl \| sort \| uniq -c` |
| Tool stats | `jq -r '... \| select(.type == "tool_use") \| .name' \| sort \| uniq -c` |
| Extract thinking | `jq -r '... \| select(.type == "thinking") \| .thinking'` |
| Find errors | `grep -i "error\|failed" $SESSION.jsonl` |
| Session summaries | `jq -r 'select(.type == "summary") \| .summary'` |
| User messages | `jq -r 'select(.type == "user") \| .message.content[]?.text'` |

## Usage Examples

### "What tools did I use most in yesterday's session?"

```bash
# Find yesterday's sessions by modification time
find ~/.claude/projects/X--Dev-claude-mods -name "*.jsonl" -mtime -1 ! -name "agent-*" | \
  xargs -I{} jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' {} | \
  sort | uniq -c | sort -rn
```

### "Show me my reasoning when debugging the auth issue"

```bash
# Search for sessions mentioning auth, then extract thinking
for f in ~/.claude/projects/$PROJECT/*.jsonl; do
  if grep -qi "auth" "$f"; then
    echo "=== $(basename $f) ==="
    jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "thinking") | .thinking' "$f" | \
      grep -i -A5 -B5 "auth"
  fi
done
```

### "What errors occurred most frequently this week?"

```bash
find ~/.claude/projects/ -name "*.jsonl" -mtime -7 | \
  xargs cat 2>/dev/null | \
  jq -r 'select(.type == "user") | .message.content[]? | select(.type == "tool_result") | .content' 2>/dev/null | \
  grep -i "error\|failed" | \
  sed 's/[0-9]\+//g' | sed 's/\/[^ ]*//g' | \
  sort | uniq -c | sort -rn | head -10
```

## Privacy Considerations

Session logs contain:
- Full conversation history including any sensitive data discussed
- File contents that were read or written
- Thinking/reasoning (internal deliberation)
- Tool inputs/outputs

**Before sharing session exports:**
1. Review for credentials, API keys, personal data
2. Consider redacting file paths if they reveal project structure
3. Thinking blocks may contain candid assessments

## Export Formats

### Markdown Report

```bash
SESSION="session-id"
PROJECT="X--Dev-claude-mods"

echo "# Session Report: $SESSION"
echo ""
echo "## Summary"
jq -r 'select(.type == "summary") | "- \(.summary)"' ~/.claude/projects/$PROJECT/$SESSION.jsonl
echo ""
echo "## Tool Usage"
jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' \
  ~/.claude/projects/$PROJECT/$SESSION.jsonl | sort | uniq -c | sort -rn | \
  awk '{print "| " $2 " | " $1 " |"}'
```

### JSON Export (for further processing)

```bash
jq -s '{
  session_id: "'$SESSION'",
  entries: length,
  tools: [.[] | select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name] | group_by(.) | map({tool: .[0], count: length}),
  summaries: [.[] | select(.type == "summary") | .summary]
}' ~/.claude/projects/$PROJECT/$SESSION.jsonl
```
