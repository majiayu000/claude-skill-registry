---
name: Claude Code X - Autonomous Execution Subagent
description: Execute Claude Code autonomously in the background for well-defined tasks, enabling parallel execution of up to 5 concurrent sessions while the user continues other work.
allowed-tools: Bash, Task, Edit, Read, Write, Grep, Glob
---

# Claude Code X - Autonomous Execution Subagent

**Type**: Task Execution Agent
**Mode**: Background Autonomous
**Version**: 1.0.0

---

## 🎯 Purpose

Execute Claude Code autonomously in the background for well-defined tasks, enabling parallel execution of up to 5 concurrent sessions while the user continues other work.

---

## 🚀 When to Use This Skill

**✅ Use When**:
- You have 3+ independent, well-defined tasks
- Tasks don't require user interaction during execution
- You want to maximize throughput with parallel execution
- User can benefit from multitasking during execution
- Tasks follow clear patterns (e.g., similar Issues)

**❌ Don't Use When**:
- Task requires user decisions during execution
- Requirements are unclear or exploratory
- Task has complex dependencies on other running tasks
- Immediate interactive feedback is needed

---

## 📋 Capabilities

### Core Features
- **Parallel Execution**: Run up to 5 Claude Code sessions concurrently
- **Session Management**: JSON-based persistence and lifecycle tracking
- **Background Operation**: Non-blocking, allows user to continue other work
- **Timeout Control**: Configurable timeout (default 10 minutes)
- **Result Retrieval**: Access full output logs after completion
- **Session Monitoring**: Check status and progress in real-time

### Session Lifecycle
1. **Spawn**: Create new background Claude Code session
2. **Execute**: Run task autonomously with specified tools
3. **Monitor**: Check status and output
4. **Complete**: Retrieve results and clean up

---

## 🛠️ Usage

### Basic Execution

```
Please use the Claude Code X skill to execute the following task in the background:

"Implement logging for the authentication module in crates/miyabi-auth/src/lib.rs"
```

### Parallel Batch Execution

```
Use Claude Code X to execute these 5 tasks in parallel:

1. Add logging to crates/miyabi-auth/src/lib.rs
2. Add logging to crates/miyabi-database/src/lib.rs
3. Add logging to crates/miyabi-api/src/lib.rs
4. Add logging to crates/miyabi-cache/src/lib.rs
5. Add logging to crates/miyabi-worker/src/lib.rs

Monitor their progress and report when all are complete.
```

### With Custom Configuration

```
Use Claude Code X with:
- Timeout: 15 minutes
- Tools: Bash, Read, Write, Edit, Grep
- Task: "Refactor error handling in crates/miyabi-core/src/errors.rs"
```

---

## 🎬 Implementation Instructions

When this skill is invoked, execute the following steps:

### Step 1: Validate Task

Check that the task is:
- Well-defined with clear success criteria
- Independent (no dependencies on user input)
- Suitable for autonomous execution

If unclear, ask user for clarification before proceeding.

### Step 2: Execute with Shell Script

Use the claude-code-x.sh shell script:

```bash
# Execute task
./.claude/commands/claude-code-x.sh exec "Task description here"

# Optional: Custom configuration
./.claude/commands/claude-code-x.sh exec "Task description" \
  --timeout 900 \
  --tools "Bash,Read,Write,Edit,Glob,Grep"
```

### Step 3: Capture Session ID

The script will output:
```
✅ Session started successfully
🔗 Session ID: claude-code-x-20251027-123456-abc123
🔗 PID: 12345
```

Store this session ID for monitoring.

### Step 4: Monitor Progress (Optional)

During execution, you can check status:

```bash
# Check status
./.claude/commands/claude-code-x.sh status claude-code-x-20251027-123456-abc123

# List all sessions
./.claude/commands/claude-code-x.sh sessions
```

### Step 5: Retrieve Results

After completion, get full output:

```bash
./.claude/commands/claude-code-x.sh result claude-code-x-20251027-123456-abc123
```

### Step 6: Report to User

Provide summary:
- Session ID
- Execution time
- Exit code (0 = success)
- Files modified
- Any issues encountered

---

## 📊 Best Practices

### Task Breakdown
```
Good Task:
"Add comprehensive logging to crates/miyabi-auth/src/lib.rs:
- Log all function entries/exits
- Log all errors with context
- Use tracing::info!, tracing::error!
- Include test coverage"

Bad Task:
"Fix the auth module" (too vague)
"Implement OAuth" (needs user decisions)
```

### Parallel Execution Strategy

**Pattern 1: Similar Tasks** (Ideal)
```
Task 1: Add logging to module A
Task 2: Add logging to module B  
Task 3: Add logging to module C
Task 4: Add logging to module D
Task 5: Add logging to module E

→ All 5 tasks in parallel (max efficiency)
```

**Pattern 2: Phased Execution** (Good)
```
Phase 1 (parallel): Infrastructure setup tasks
  - Task 1: Create config struct
  - Task 2: Add database schema
  - Task 3: Implement Redis cache

Phase 2 (interactive): Critical logic (use regular Claude Code)

Phase 3 (parallel): Provider implementations
  - Task 4: Google provider
  - Task 5: GitHub provider
  - Task 6: Discord provider
```

### Error Handling

If a session fails:
1. Check the log file for error details
2. Determine if it's retryable
3. Fix any issues (e.g., missing files)
4. Re-execute with corrected task description

---

## 🔍 Session Management Commands

### List Active Sessions
```bash
./.claude/commands/claude-code-x.sh sessions
```

### Check Session Status
```bash
./.claude/commands/claude-code-x.sh status <session-id>
```

### Get Full Results
```bash
./.claude/commands/claude-code-x.sh result <session-id>
```

### Kill Running Session
```bash
./.claude/commands/claude-code-x.sh kill <session-id>
```

### Cleanup Old Sessions
```bash
./.claude/commands/claude-code-x.sh cleanup
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Session directory (default: .ai/sessions/claude-code-x)
export CLAUDE_CODE_X_SESSION_DIR=".ai/sessions/claude-code-x"

# Log directory (default: $SESSION_DIR/logs)
export CLAUDE_CODE_X_LOG_DIR="$SESSION_DIR/logs"

# Max concurrent sessions (default: 5)
export CLAUDE_CODE_X_MAX_SESSIONS=5

# Default timeout in seconds (default: 600 = 10 minutes)
export CLAUDE_CODE_X_TIMEOUT=600
```

### Default Tools

The following tools are enabled by default:
- Bash (command execution)
- Read (file reading)
- Write (file writing)
- Edit (file editing)
- Glob (file pattern matching)
- Grep (content search)

### Permission Mode

- Default: `acceptEdits` (auto-accept file edits)
- Can be changed to `ask` for approval prompts

---

## 📈 Performance Characteristics

### Speed
- **Overhead**: ~2-3 seconds per session spawn
- **Execution**: Similar to interactive Claude Code
- **Parallel**: Up to 5x throughput with 5 concurrent sessions

### Resource Usage
- **Memory**: ~200MB per session
- **Disk**: ~1MB per session log
- **CPU**: Minimal (most time spent in AI inference)

### Limits
- **Max Sessions**: 5 concurrent (configurable)
- **Max Timeout**: 10 minutes default (configurable up to 30 min)
- **Log Retention**: Logs persist until manual cleanup

---

## 🎓 Examples

### Example 1: Single Task

**User Request**: "Add logging to the auth module"

**Agent Action**:
```bash
./.claude/commands/claude-code-x.sh exec \
  "Add comprehensive logging to crates/miyabi-auth/src/lib.rs:
  - Log all function entries/exits with tracing::info!
  - Log all errors with tracing::error!
  - Include request IDs in log context
  - Add tests for logging behavior"
```

**Agent Response**:
```
✅ Started Claude Code X session: claude-code-x-20251027-100000-abc123
📝 Executing task in background (timeout: 10 minutes)
💡 Monitor with: /claude-code-x status claude-code-x-20251027-100000-abc123

I'll check back in 2 minutes to see progress.
```

### Example 2: Parallel Batch

**User Request**: "Add logging to all 5 core modules"

**Agent Action**:
```bash
# Launch 5 parallel sessions
./.claude/commands/claude-code-x.sh exec "Add logging to crates/miyabi-auth/src/lib.rs"
./.claude/commands/claude-code-x.sh exec "Add logging to crates/miyabi-database/src/lib.rs"
./.claude/commands/claude-code-x.sh exec "Add logging to crates/miyabi-api/src/lib.rs"
./.claude/commands/claude-code-x.sh exec "Add logging to crates/miyabi-cache/src/lib.rs"
./.claude/commands/claude-code-x.sh exec "Add logging to crates/miyabi-worker/src/lib.rs"
```

**Agent Response**:
```
✅ Started 5 parallel Claude Code X sessions:
1. claude-code-x-20251027-100000-abc123 (auth)
2. claude-code-x-20251027-100015-def456 (database)
3. claude-code-x-20251027-100030-ghi789 (api)
4. claude-code-x-20251027-100045-jkl012 (cache)
5. claude-code-x-20251027-100100-mno345 (worker)

Estimated completion: ~5 minutes
I'll monitor progress and report when all complete.
```

### Example 3: Phased Hybrid

**User Request**: "Implement OAuth 2.0 authentication"

**Agent Action** (Pattern 3: Hybrid Orchestration):
```
Phase 1: Planning (Interactive)
- Breaking down OAuth into discrete tasks...

Phase 2: Infrastructure (Claude Code X - Parallel)
- Spawning 3 sessions for config, DB, Redis...

Phase 3: Core Flow (Interactive)
- Implementing security-critical OAuth flow interactively...

Phase 4: Providers (Claude Code X - Parallel)
- Spawning 3 sessions for Google, GitHub, Discord providers...

Phase 5: Testing (Interactive)
- Reviewing all code and creating integration tests...

Result: 42 minutes (30% faster than all-interactive)
```

---

## 🔗 Related Documentation

- **Implementation**: [CLAUDE_CODE_X_IMPLEMENTATION_GUIDE.md](../../../docs/CLAUDE_CODE_X_IMPLEMENTATION_GUIDE.md)
- **Workflow**: [OPTIMAL_MIYABI_WORKFLOW_WITH_CODEX_CLAUDE.md](../../../docs/OPTIMAL_MIYABI_WORKFLOW_WITH_CODEX_CLAUDE.md)
- **Pattern 3 Example**: [PATTERN3_HYBRID_EXAMPLE.md](../../../docs/PATTERN3_HYBRID_EXAMPLE.md)
- **Command Reference**: [.claude/commands/claude-code-x.md](../../commands/claude-code-x.md)

---

## 🐛 Troubleshooting

### Session Won't Start

**Error**: `Maximum concurrent sessions (5) reached`

**Solution**:
```bash
# List active sessions
./.claude/commands/claude-code-x.sh sessions

# Kill inactive sessions or wait for completion
./.claude/commands/claude-code-x.sh kill <session-id>

# Or cleanup old sessions
./.claude/commands/claude-code-x.sh cleanup
```

### Session Timeout

**Error**: Session times out before completion

**Solution**:
```bash
# Increase timeout for complex tasks
./.claude/commands/claude-code-x.sh exec "Complex task" --timeout 1200
```

### Session Fails

**Check logs**:
```bash
./.claude/commands/claude-code-x.sh result <session-id>
```

**Common issues**:
- Missing files → Add file creation to task description
- Dependency errors → Ensure dependencies are available
- Unclear task → Make task description more specific

---

## 📊 Success Metrics

Track these metrics to evaluate Claude Code X effectiveness:

- **Time Savings**: Compare total execution time vs sequential
- **Success Rate**: Percentage of sessions completing successfully
- **Parallelization Factor**: Average concurrent sessions used
- **Task Clarity**: Percentage requiring clarification before execution

**Target Metrics**:
- Time Savings: >25%
- Success Rate: >90%
- Parallelization: 3-5 concurrent sessions
- Task Clarity: <10% requiring clarification

---

**Version**: 1.0.0
**Created**: 2025-10-27
**Author**: Claude Code (Sonnet 4.5)
**Status**: ✅ Production Ready
