---
name: rate-limit-recovery
description: >
  Collects recent transcripts and logging information from agent platforms that were rate-limited mid-task.
  Supports recovery from Codex, Claude Code, Pi, and Antigravity rate limits by gathering session data,
  logs, and partial results to resume interrupted work.
allowed-tools: Bash, Read, Glob, Grep, Write
triggers:
  - rate limit recovery
  - recover from rate limit
  - collect transcripts
  - gather logs
  - resume interrupted task
  - rate limited session
metadata:
  short-description: Recover from rate limits by collecting session data and logs
---

# Rate Limit Recovery Skill

Recovers from rate limiting interruptions across multiple agent platforms by collecting recent transcripts, logs, and session data to resume interrupted tasks.

## Supported Platforms

- **OpenAI Codex**: Collects from `codex` CLI sessions and sandbox logs
- **Claude Code**: Gathers from Claude Code workspace logs and session files
- **Pi**: Retrieves from Pi's episodic memory and session archives
- **Antigravity**: Collects from Antigravity sandbox logs and session data

## Features

1. **Automatic Platform Detection**: Identifies which agent platform was interrupted
2. **Session Data Collection**: Gathers recent transcripts, logs, and partial results
3. **Rate Limit Context**: Captures error details and retry timing information
4. **Recovery Summary**: Provides structured overview of what was collected
5. **Resume Guidance**: Suggests next steps for continuing interrupted work

## Usage

### Basic Recovery

```bash
./run.sh recover  # Auto-detect platform and collect recent data
```

### Platform-Specific Recovery

```bash
./run.sh recover --platform codex --session-id abc123
./run.sh recover --platform claude --workspace /path/to/project
./run.sh recover --platform pi --session-id recent
./run.sh recover --platform antigravity --task-id task456
```

### Advanced Options

```bash
# Export to specific format
./run.sh recover --format json --output recovery_report.json

# Custom output location
./run.sh recover --format markdown --output /path/to/custom/report.md
```

## Data Storage

Recovery data is stored in `~/.pi/rate-limit-recovery/` by default. This ensures:

- Consistent location across all projects
- Proper organization of recovery files
- Easy access for future reference

## Recovery Data Structure

The skill collects and organizes data into these categories:

### Session Context

- Recent conversation history and tool calls
- Partial results and intermediate outputs
- User inputs and agent responses

### Error Information

- Rate limit error details (429 responses, quota info)
- Retry timing and backoff information
- Platform-specific error codes and messages

### Log Files

- Platform-specific log locations and formats
- Recent activity timestamps and sequences
- Debug and verbose logging when available

### System State

- Workspace and file system state at interruption
- Environment variables and configuration
- Running processes and background tasks

## Integration with Other Skills

This skill works well with:

- **memory**: Store recovered session data for future reference
- **episodic-archiver**: Archive the recovery session for analysis
- **task-monitor**: Monitor recovery progress and retry attempts
- **agent-inbox**: Communicate recovery status to other agents

## Platform-Specific Details

### Codex Recovery

- Collects from `~/.codex/sessions/` and current workspace
- Gathers reasoning effort and model configuration
- Captures sandbox execution logs and tool outputs

### Claude Code Recovery

- Retrieves from Claude Code workspace `.claude/` directory
- Collects conversation history and context files
- Gathers Claude-specific configuration and settings

### Pi Recovery

- Accesses Pi's episodic memory and session archives
- Collects from `.pi/sessions/` and memory stores
- Gathers ArangoDB-backed conversation history

### Antigravity Recovery

- Collects from Antigravity sandbox logs and session data
- Grows Google Cloud Code Assist integration logs
- Captures multi-model conversation context

## Error Handling

The skill handles various failure scenarios:

- Missing or corrupted session files
- Inaccessible log directories
- Platform-specific authentication issues
- Network connectivity problems during recovery

## Output Formats

Recovery data can be exported in multiple formats:

- **JSON**: Structured data for programmatic access
- **Markdown**: Human-readable report with sections
- **Plain Text**: Simple chronological log format
- **HTML**: Rich formatted report with navigation
