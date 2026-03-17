---
name: pi-dcp
description: Dynamic Context Pruning extension for pi. Expert guidance on using intelligent message pruning to optimize token usage while preserving conversation coherence.
---

# Pi-DCP: Dynamic Context Pruning Expert

You are an expert on the Pi-DCP (Dynamic Context Pruning) extension for pi. You help users understand and optimize context pruning for token efficiency.

## Core Concepts

### What Pi-DCP Does

Pi-DCP automatically removes obsolete and redundant messages from conversation context before each LLM call. This:

- **Reduces token usage** - Fewer messages sent to the LLM
- **Lowers costs** - Smaller prompts = cheaper API calls
- **Preserves coherence** - Smart rules keep important context
- **Works transparently** - No user intervention needed

### Workflow: Prepare > Process > Filter

1. **Prepare Phase**: Rules annotate message metadata (hashes, file paths, error status, etc.)
2. **Process Phase**: Rules make pruning decisions based on metadata
3. **Filter Phase**: Messages marked for pruning are removed

### Built-in Rules

**Deduplication**
- Removes duplicate tool outputs based on content hash
- Keeps first occurrence, prunes later duplicates
- Never prunes user messages

**Superseded Writes**
- Removes older file write/edit operations when newer versions exist
- Tracks file paths and versions
- Only keeps the latest write to each file

**Error Purging**
- Removes resolved errors from context
- Identifies errors followed by successful retries
- Keeps unresolved errors for context

**Recency Protection**
- Always preserves recent messages (default: last 10)
- Overrides other pruning decisions
- Configurable threshold

## Usage Guidance

### Commands

Tell users about these commands:

- `/dcp-debug` - Toggle debug logging to see what's being pruned
- `/dcp-stats` - Show pruning statistics for current session
- `/dcp-toggle` - Enable/disable the extension
- `/dcp-recent <number>` - Adjust recency threshold (default: 10)

### When to Use Debug Mode

Recommend `/dcp-debug` when:
- User suspects important context is being pruned
- Investigating unexpected LLM behavior
- Understanding what the extension is doing
- Tuning configuration

### When to Adjust Recency Threshold

Recommend changing `keepRecentCount`:
- **Increase** (e.g., `/dcp-recent 20`) if:
  - LLM seems to forget recent context
  - Working on complex multi-step tasks
  - Need more working memory
  
- **Decrease** (e.g., `/dcp-recent 5`) if:
  - Token usage is still too high
  - Conversation is very repetitive
  - Most context is in recent messages anyway

### When to Disable

Recommend `/dcp-toggle` to disable when:
- Debugging issues and want to see full context
- Working on tasks where all history matters
- Testing if pruning is causing problems

## Custom Rules

### Creating Custom Rules

Guide users on implementing `PruneRule`:

```typescript
import type { PruneRule } from "~/.pi/agent/extensions/pi-dcp/src/types";

const myRule: PruneRule = {
  name: 'my-rule-name',
  description: 'What this rule does',
  
  // Optional: Annotate metadata
  prepare(msg, ctx) {
    // Access: msg.message (original message)
    //         msg.metadata (metadata object to annotate)
    //         ctx.messages (all messages)
    //         ctx.index (current message index)
    //         ctx.config (configuration)
    
    msg.metadata.myScore = calculateScore(msg.message);
  },
  
  // Optional: Make pruning decisions
  process(msg, ctx) {
    // Check if already pruned
    if (msg.metadata.shouldPrune) return;
    
    // Never prune user messages
    if (msg.message.role === 'user') return;
    
    // Make decision
    if (msg.metadata.myScore < threshold) {
      msg.metadata.shouldPrune = true;
      msg.metadata.pruneReason = 'low score';
    }
  },
};
```

### Rule Design Patterns

**Prepare-only rules**: Annotate metadata for other rules to use

**Process-only rules**: Make decisions based on metadata from prepare phase

**Two-phase rules**: Annotate in prepare, decide in process (most common)

**Protective rules**: Override pruning decisions (like recency)

### Metadata Fields

Standard metadata fields:
- `hash` - Content hash for deduplication
- `filePath` - File path for superseded writes
- `fileVersion` - Version hash for file tracking
- `isError` - Whether message is an error
- `errorResolved` - Whether error was resolved
- `protectedByRecency` - Protected by recency rule
- `shouldPrune` - Final pruning decision (boolean)
- `pruneReason` - Why it should be pruned (string)

Custom rules can add any fields.

## Troubleshooting

### "LLM forgot recent context"

1. Check recency threshold: `/dcp-recent 15` to increase
2. Enable debug: `/dcp-debug` to see what's being pruned
3. Check if important messages are within recency window

### "Still using too many tokens"

1. Check stats: `/dcp-stats` to see pruning rate
2. Consider adding custom rules for domain-specific pruning
3. Reduce recency threshold if safe: `/dcp-recent 5`

### "Extension not working"

1. Check if enabled: `/dcp-toggle` twice (off then on)
2. Look for initialization message in logs
3. Check for configuration errors in console

### "Rule not found error"

Rules must be registered before use. Built-in rules auto-register when extension loads.

For custom rules, ensure they're registered:
```typescript
import { registerRule } from "~/.pi/agent/extensions/pi-dcp/src/registry";
registerRule(myRule);
```

## Best Practices

### Configuration

- Start with defaults (4 built-in rules, keepRecentCount: 10)
- Enable debug mode initially to understand behavior
- Tune recency threshold based on use case
- Add custom rules for domain-specific patterns

### Rule Order

Rules are applied in the order configured. Standard order:
1. Deduplication
2. Superseded Writes
3. Error Purging
4. Recency (should be last to override)

Recency should typically be last since it protects messages.

### Performance

- Prepare phase should be fast (just annotation)
- Avoid expensive computation in prepare/process
- Process phase runs for every rule on every message
- Keep rule count reasonable (4-8 rules is typical)

## Example Scenarios

### Scenario: Long File Editing Session

User has edited `src/app.ts` 20 times. Without DCP, all 20 write operations are in context.

**Pi-DCP behavior**:
- Superseded Writes rule keeps only the latest write
- Saves 19 message slots
- LLM sees current file state, not full history

### Scenario: Debugging with Retries

User encountered an error, retried 5 times, finally succeeded.

**Pi-DCP behavior**:
- Error Purging rule removes the 5 failed attempts
- Keeps only the successful result
- LLM focuses on solution, not failure history

### Scenario: Repetitive Tool Calls

User ran `ls` 10 times in the same directory.

**Pi-DCP behavior**:
- Deduplication rule keeps only first `ls` result
- Prunes 9 duplicate outputs
- Saves tokens on redundant information

## Advanced Topics

### State Tracking

Rules can track state across prepare/process:

```typescript
const seenFiles = new Set<string>();

const rule: PruneRule = {
  name: 'track-files',
  prepare(msg, ctx) {
    const path = extractFilePath(msg.message);
    if (path) {
      msg.metadata.isFirstSeen = !seenFiles.has(path);
      seenFiles.add(path);
    }
  },
};
```

Note: State resets each time workflow runs (each LLM call).

### Multi-Rule Coordination

Rules can check metadata from other rules:

```typescript
process(msg, ctx) {
  // Check if another rule already marked it
  if (msg.metadata.shouldPrune) return;
  
  // Use metadata from deduplication rule
  if (msg.metadata.hash === targetHash) {
    // ...
  }
}
```

### Conditional Pruning

Rules can make context-aware decisions:

```typescript
process(msg, ctx) {
  // Only prune if many similar messages exist
  const similar = ctx.messages.filter(m => 
    m.metadata.category === msg.metadata.category
  );
  
  if (similar.length > 10) {
    msg.metadata.shouldPrune = true;
  }
}
```

## Integration with Pi

Pi-DCP hooks into the `context` event, which fires before every LLM call. This means:

- Pruning happens automatically
- No changes to pi's core behavior
- Works with all models and tools
- Transparent to the user (unless debug enabled)

The extension is fail-safe: if any error occurs, original messages are returned unchanged.

## Future Enhancements

Potential features to suggest:
- Per-rule statistics
- Interactive rule configuration UI
- Rule performance metrics
- Visualization of pruning decisions
- Export/import rule configurations
- LLM-assisted pruning (expensive but intelligent)

## Summary

Pi-DCP is a **transparent, configurable, extensible** context pruning system that:
- Reduces token usage through intelligent pruning
- Preserves conversation coherence with smart rules
- Requires no user intervention (but offers control when needed)
- Supports custom rules for domain-specific optimization

Guide users to start with defaults, enable debug mode to understand behavior, then tune configuration and add custom rules as needed.
