---
description: Search raw session transcripts for technical details and reasoning traces
triggers:
  - archive search
  - search archive
  - search transcripts
  - find in session
  - check raw sessions
invocation_examples:
  - /archive-search "model fallback implementation"
  - /archive-search "context tracking approaches"
  - /archive-search "thinking about memory design"
---

# Archive Search

Search through raw Claude Code session transcripts to recover technical details, reasoning traces, and thinking blocks that were compressed during episode distillation.

## What You'll Get

**The archive contains:**
- ✅ Complete thinking blocks (raw reasoning process)
- ✅ User messages (original intent and questions)
- ✅ Assistant explanations (first 1000 chars)
- ❌ Tool results (filtered out - too noisy)
- ❌ System messages (no semantic value)

**Best for:**
- Technical archaeology: "How did we implement X?"
- Decision rationale: "Why did we choose Y over Z?"
- Reasoning evolution: "How has our approach to X changed?"
- Debugging context: "What was the exact error we saw?"

## How Archive Differs from Regular Memory

| Memory Type | Content | Use Case |
|-------------|---------|----------|
| **Episodes** (`/episode`) | Curated summaries (2-8 bullets per section) | What happened today |
| **Learnings** (`/memory`) | Distilled insights | General knowledge |
| **Archive** (`/archive-search`) | Raw transcripts with thinking blocks | Technical depth, exact discussions |

The archive captures ~5-10% of raw transcript bytes by selecting only high-value content (thinking blocks, user questions, assistant reasoning). It's indexed separately to prevent noise pollution of curated memory.

## When to Use This Skill

**Good use cases:**
```
/archive-search "model fallback implementation"
→ Find thinking blocks about ModelFallbackChain design

/archive-search "Swift vs Python for memory database"
→ Recover exact trade-off analysis

/archive-search "context tracking approaches"
→ See evolution of ContextTracker across sessions
```

**Not helpful:**
```
/archive-search "who is Lucy"
→ Use /person instead (person profiles)

/archive-search "what did we decide about X"
→ Use /memory or check decisions.md
```

## Search Tips

**Thinking blocks are highest value:**
- Archive preserves full reasoning traces
- Includes technical discussion and trade-offs
- Most detailed context for implementation decisions

**Be specific:**
- Good: "memory database indexing strategy"
- Too broad: "memory" (will match thousands of chunks)

**Look for technical terms:**
- Good: "ModelFallbackChain", "ContextTracker", "sanitizeResponse"
- Generic: "error handling" (use more specific context)

## Coverage

**Time range:** Last 90 days of sessions
**Project:** samara-main only (for now)
**Update frequency:** Incremental sync during dream cycles (3 AM)

**Current state:**
Run `/archive-search stats` to see:
- Total indexed chunks
- Session count
- Thinking block count

## Example Session

**User:** `/archive-search "sanitization logic"`

**Claude:**
```
Found 3 relevant sessions:

================================================================================
Result 1 | Distance: 0.18 | Role: thinking
Session: 5399ef7a-... | Time: 2026-01-05 15:42:33
--------------------------------------------------------------------------------
The user is asking about the sanitization issue. Let me think through what we
know:

1. Thinking blocks are leaking into messages
2. Session IDs appearing in user-visible text
3. This happens in multi-stream scenarios (webcam + web fetch + conversation)

The root cause is likely in ClaudeInvoker.swift where we parse JSON output.
If parseJsonOutput() falls back to raw text when JSON parsing fails, it would
include everything - thinking blocks, session IDs, etc.

We need a three-layer defense:
- parseJsonOutput() should never fall back to raw
- sanitizeResponse() should strip known patterns
- MessageBus should coordinate all sends through single channel

[...1247 more characters]

Session file: ~/.claude/projects/.../5399ef7a-...jsonl
```

This gives you the exact reasoning process, not just the summary that ended up in episode logs.

## Commands

Once you invoke this skill with `/archive-search <query>`, you can:

1. **Search by query:**
   - `archive-search "your query here"`
   - Returns top 5 most relevant chunks

2. **Filter by role:**
   - `--role thinking` - Only thinking blocks (highest signal)
   - `--role user` - Only user messages
   - `--role assistant` - Only assistant text

3. **Adjust result count:**
   - `--n 10` - Get more results

4. **Check index stats:**
   - `stats` - See what's indexed

5. **Quality check:**
   - `sample` - Random sample of 3 chunks
   - `sample --session-id abc123` - Sample from specific session

---

## Implementation Notes

**For Claude instances:**

When a user invokes `/archive-search <query>`, you should:

1. Run: `~/.claude-mind/bin/archive-index search "<query>"`
2. Parse and present results clearly
3. Include session IDs for reference
4. Explain what the user is seeing (thinking blocks vs user messages)

**First-time setup:**

If the archive hasn't been built yet:
```bash
# Build initial index (takes 5-10 minutes for 90 days)
~/.claude-mind/bin/archive-index rebuild

# Check stats
~/.claude-mind/bin/archive-index stats

# Test search
~/.claude-mind/bin/archive-index search "model fallback"
```

After initial build, dream cycles handle incremental sync automatically.
