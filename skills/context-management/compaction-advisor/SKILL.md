---
name: compaction-advisor
description: Provides context-aware compaction guidance with intelligent checkpointing. Monitors context during long tasks and suggests checkpoints before compaction interrupts your work.
license: MIT
compatibility: Claude Code CLI with hooks enabled
---

# Compaction Advisor

You receive automatic context status via XML tags when context is concerning.

## Message Types

### 1. Context Status (on user prompts)

When you see these tags at the start of a conversation turn:

```
<context-status>CRITICAL: Only 12k tokens free. Run /compact before any task.</context-status>
<context-status>WARNING: 25k tokens free. Only small tasks safe.</context-status>
<context-status>CAUTION: 40k tokens free. Medium tasks OK, compact before large.</context-status>
```

When context is healthy (50k+ free), you won't see any tag.

### 2. Checkpoint Suggestions (during long tasks)

During multi-step work, you may see:

```
<context-checkpoint>
CHECKPOINT RECOMMENDED: Context critically low (18k free) after 12 operations.
Good time to pause and /compact. Summarize progress so far and key context to preserve.
</context-checkpoint>
```

This means you've been working for a while and context is running low.

### 3. PreCompact Warning (emergency)

Just before auto-compaction triggers:

```
<precompact-warning>
AUTO-COMPACTION IMMINENT
Context window is full. Compaction will happen after this message.
</precompact-warning>
```

## How to Respond

### When you see `<context-status>` CRITICAL

Immediately advise:
```
Context is critically low (12k free). Before we proceed, run:
/compact Focus on [relevant context to preserve]
```

### When you see `<context-status>` WARNING

For small tasks: proceed with caution
For medium+ tasks: recommend compaction first

```
Context is at 25k free. For a refactor like this (~50k needed),
run /compact first to avoid mid-task interruption.
```

### When you see `<context-checkpoint>`

This is mid-task. Pause and offer a checkpoint:

```
Good checkpoint - I've completed:
• [List what you've done so far]
• [Key decisions made]
• [Files modified]

Context is at 18k. To continue safely, run:
/compact Focus on [key context for remaining work]

After compacting, I'll continue with [next steps].
```

### When you see `<precompact-warning>`

This is urgent. Quickly summarize:

```
Compaction is about to happen. Quick summary of our progress:
• [What we were working on]
• [What's been completed]
• [What remains to do]

After compaction, remind me to [specific next step].
```

### When you see nothing

Context is healthy. Proceed normally without mentioning it.

## Task Size Reference

| Task | ~Tokens Needed |
|------|----------------|
| Typo fix | 5k |
| Bug fix | 15k |
| New feature | 30k |
| Refactor | 50k |
| Architecture | 80k+ |

## Compact Commands

```
/compact                              # General
/compact Focus on [specific context]  # Preserve specific context
```

Examples:
- `/compact Focus on the auth changes and test failures`
- `/compact Keep the refactoring progress and file structure decisions`

## Key Points

- You automatically receive context state - no need to ask user
- During long tasks, checkpoint suggestions appear after 8+ operations
- Match urgency to the tag level (CRITICAL > WARNING > CAUTION)
- For checkpoints, summarize progress and suggest what to preserve
- For precompact, quickly capture essential context
- For healthy context, work normally without mentioning it
