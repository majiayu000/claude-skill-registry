---
name: distill-pending
description: Process pending transcript distillation
execution: inline
---

# Distill Pending Sessions

Trigger distillation of pending transcripts and check distillation status.

## How Distillation Works

1. **Automatic**: The daemon distills transcripts every 5 minutes (configurable)
2. **On Compaction**: PreCompact hook triggers immediate distillation before context is lost
3. **On Session Start**: SessionStart hook triggers distillation of any pending work

## Manual Trigger

If you need to manually trigger distillation for the current session:

```bash
# Add to queue for daemon processing
echo '{"tool":"distill_trigger","args":{"session_id":"CURRENT_SESSION_ID"},"ts":'$(date +%s)'}' >> /tmp/chitta-queue.jsonl
```

## Check Distillation Status

View registered transcripts and their distillation state:

```bash
chitta transcript_list
```

This shows:
- `session_id`: Transcript identifier
- `last_processed_line`: How many lines have been distilled
- `distilled`: Whether any distillation has occurred
- `realm`: Project context

## Distillation Output

Distilled learnings are stored as memories with:
- `[learn]` prefix for extracted insights
- SSL format for efficient storage
- Connected via triplets for graph navigation

## Configuration

Daemon distillation settings (in `chittad --help`):
- `--distill-interval MINS`: Check interval (default: 5)
- `--distill-min-turns N`: Min turns before distilling (default: 4)
- `--distill-model MODEL`: LLM model for extraction
- `--no-distill`: Disable automatic distillation

## Troubleshooting

If distillation isn't running:
1. Check daemon is running: `chitta health_check`
2. Check opencode is available: `which opencode`
3. Check transcript is registered: `chitta transcript_list`
4. Check queue is being processed: `ls -la /tmp/chitta-queue.jsonl*`
