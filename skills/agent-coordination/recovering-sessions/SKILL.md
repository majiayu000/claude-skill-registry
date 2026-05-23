---
name: recovering-sessions
description: "Recover from crashed, failed, or interrupted Claude Code sessions. Use this skill when: session crashed during multi-agent parallel execution, need to determine what work was completed vs incomplete, want to generate resumption commands for interrupted tasks, recovering from context window exhaustion, or handling session handoffs. Analyzes agent logs, verifies on-disk state, and creates resumption plans with ready-to-execute Task() commands."
---

# Session Recovery Skill

Recover from crashed, failed, or interrupted Claude Code sessions with automated analysis and resumption planning.

## Why This Skill

Claude Code sessions can crash during complex multi-agent operations. Recovery without this skill is:
- **Manual**: Requires parsing agent logs by hand
- **Error-prone**: Easy to miss completed or incomplete work
- **Time-consuming**: Ad-hoc investigation for each crash
- **Undocumented**: Knowledge lost between sessions

This skill provides **standardized recovery workflows** that:
- Discover and analyze agent conversation logs
- Verify on-disk state matches expected deliverables
- Generate recovery reports with clear status per task
- Create ready-to-execute Task() resumption commands
- Document prevention patterns to avoid future crashes

## When to Use

| Scenario | Action |
|----------|--------|
| Session crashed during parallel execution | Full recovery workflow |
| User reports interrupted work | Analyze recent agent logs |
| Need to determine completed vs incomplete | Status assessment |
| Generate resumption commands | Resumption plan |
| Session handoff to continue later | Handoff summary |
| Proactive health check | Scan for incomplete work |

## Quick Start

### Post-Crash Recovery

```
User: "Claude crashed while I had multiple agents running. Help me recover."

1. Identify project log directory
2. Discover recent agent logs (last 3 hours)
3. Analyze each log in parallel (haiku subagents)
4. Cross-reference with git status
5. Generate recovery report
6. Offer to commit completed work
7. Provide resumption commands for incomplete tasks
```

### Session Handoff

```
User: "I need to hand off this session to continue later."

1. Identify active/recent work
2. Capture current git state
3. Document in-progress tasks
4. Update progress tracking with session notes
5. Generate handoff summary with resumption instructions
```

### Proactive Health Check

```
User: "Check if any recent agent work was incomplete."

1. Scan recent agent logs (last 24 hours)
2. Identify logs without clear completion markers
3. Check if corresponding files exist
4. Report any gaps or incomplete work
5. Suggest remediation if needed
```

## Core Workflow

### Phase 1: Gather Context

1. **Get project path and derive log directory**:
   ```bash
   # Project path: /Users/name/dev/project
   # Log directory: ~/.claude/projects/-Users-name-dev-project/
   LOG_DIR="$HOME/.claude/projects/$(pwd | sed 's/\//-/g' | sed 's/^-//')"
   ```

2. **Check git status for uncommitted changes**:
   ```bash
   git status --short
   ```

3. **Read implementation plan/PRD** (if available) for expected deliverables

See `./techniques/discovering-agent-logs.md` for detailed discovery patterns.

### Phase 2: Discover Agent Logs

Find recent agent logs using multiple techniques:

| Technique | Command | Use Case |
|-----------|---------|----------|
| By recency | `find $LOG_DIR -name "agent-*.jsonl" -mmin -180` | Find agents active in last 3 hours |
| By ID pattern | `ls $LOG_DIR \| grep -E "(id1\|id2)"` | Match known agent IDs |
| By size | `find $LOG_DIR -name "*.jsonl" -size +10k -mtime -1` | Find substantial logs |
| All recent | `ls -lt $LOG_DIR/agent-*.jsonl \| head -20` | List by modification time |

See `./techniques/discovering-agent-logs.md` for complete reference.

### Phase 3: Analyze Each Log

For each discovered log, extract:
- Files created/modified (Write/Edit tool uses)
- Test results (passed/failed counts)
- Completion status (success markers, errors)
- Last activity timestamp

**Delegation Strategy** (token-efficient):
```
# Launch parallel analyzers with haiku model
Task("codebase-explorer", {
  model: "haiku",
  prompt: "Analyze agent log at {path}. Report: task ID, status, files created, test results, errors"
})
```

See `./techniques/parsing-jsonl-logs.md` for extraction patterns.

### Phase 4: Verify On-Disk State

Cross-reference agent deliverables against filesystem:

```bash
# For each file_path extracted from logs:
if [ -f "$file_path" ]; then
    echo "VERIFIED: $file_path exists"
    stat -f "%Sm" "$file_path"  # Check modification time
else
    echo "MISSING: $file_path not found"
fi
```

**Verification Checklist**:
- [ ] All expected files exist
- [ ] Files have content (not empty)
- [ ] Modification time aligns with session
- [ ] Tests pass (if test files created)
- [ ] No syntax errors (quick lint check)

See `./techniques/verifying-on-disk-state.md` for complete verification workflow.

### Phase 5: Generate Recovery Report

Produce structured report with:
- Agent status summary (COMPLETE/IN_PROGRESS/FAILED/UNKNOWN)
- Completed work inventory
- Interrupted tasks with resumption commands
- Recommended next actions

See `./techniques/generating-resumption-plans.md` and `./templates/recovery-report.md`.

### Phase 6: Execute Recovery

With user approval:
1. **Commit completed work** with comprehensive message
2. **Update progress tracking** (via artifact-tracking skill)
3. **Resume interrupted tasks** using generated Task() commands

## Status Determination Logic

```
IF log contains "COMPLETE" or "successfully" in final messages → COMPLETE
ELIF log contains uncaught errors in final 10 lines → FAILED
ELIF log size > threshold AND recent modification → IN_PROGRESS (likely crashed)
ELIF log is small with no file writes → NOT_STARTED
ELSE → UNKNOWN (requires manual review)
```

## Agent Delegation Strategy

Use haiku subagents for parallel log analysis (cheap, fast):

```javascript
// Standard parallel execution (2-4 logs)
Task("codebase-explorer", { model: "haiku", prompt: "Analyze log 1..." })
Task("codebase-explorer", { model: "haiku", prompt: "Analyze log 2..." })

// Background execution (5+ logs)
const tasks = logs.map(log =>
  Task("codebase-explorer", {
    model: "haiku",
    run_in_background: true,
    prompt: `Analyze ${log.path}...`
  })
);
const results = await Promise.all(
  tasks.map(t => TaskOutput(t.id, { block: true }))
);
```

## Recovery Report Format

```markdown
# Session Recovery Report
Generated: {timestamp}
Project: {project_path}

## Agent Status Summary

| Agent ID | Task | Status | Files Created | Tests |
|----------|------|--------|---------------|-------|
| a91845a | P2-T1: MatchAnalyzer | COMPLETE | 2 | 33/33 |
| xyz1234 | P4-T3: RatingDialog | IN_PROGRESS | 1 | - |

## Completed Work
- MatchAnalyzer with 97.67% coverage
- SemanticScorer with embedding provider abstraction

## Interrupted Tasks
### P4-T3: RatingDialog
- Last known state: Component scaffolding created
- Missing: Tests, accessibility, documentation
- Resumption command:
  ```
  Task("ui-engineer-enhanced", "Complete P4-T3: RatingDialog...")
  ```

## Recommended Actions
1. Commit completed work (files: {...})
2. Resume interrupted tasks with provided commands
3. Update progress tracking
```

See `./templates/recovery-report.md` for full template.

## Scripts

Node.js utilities in `./scripts/`:

| Script | Purpose | Usage |
|--------|---------|-------|
| `find-recent-agents.js` | Discover agent logs | `node find-recent-agents.js --minutes 180` |
| `analyze-agent-log.js` | Parse single log | `node analyze-agent-log.js <log-path>` |
| `generate-recovery-report.js` | Create full report | `node generate-recovery-report.js` |

All scripts use ESM imports and modern JavaScript (Node.js 20+).

## Prevention Recommendations

To prevent future crashes, see `./references/prevention-patterns.md`:

1. **Batch Size Limits**: Max 3-4 parallel agents per batch
2. **Checkpointing**: Update progress after each task completion
3. **Session Tracking**: Record agent IDs in progress files
4. **Heartbeat Pattern**: Emit periodic status updates
5. **Sequential Critical Paths**: Don't parallelize dependent tasks

## Integration Points

### With artifact-tracking Skill

Recovery updates progress tracking:
```
Task("artifact-tracker", "Update {PRD} phase {N}:
- Mark TASK-1.1 as complete (recovered)
- Mark TASK-1.2 as in_progress (interrupted)
- Add note: Recovered from session crash")
```

### With execute-phase Command

Recovery can resume interrupted phase execution:
```
/dev:execute-phase {N} --resume
```

### With Git Workflow

Recovery creates comprehensive commit:
```bash
git add {recovered_files}
git commit -m "feat: recover work from interrupted session

Completed:
- TASK-1.1: MatchAnalyzer
- TASK-1.2: SemanticScorer

Interrupted (to resume):
- TASK-1.3: RatingDialog

Recovered via session-recovery skill"
```

## Reference Files

| File | Purpose |
|------|---------|
| `./techniques/discovering-agent-logs.md` | Log location and discovery patterns |
| `./techniques/parsing-jsonl-logs.md` | JSONL extraction techniques |
| `./techniques/verifying-on-disk-state.md` | Filesystem verification workflow |
| `./techniques/generating-resumption-plans.md` | Recovery report generation |
| `./templates/recovery-report.md` | Report template |
| `./references/prevention-patterns.md` | Crash prevention guidance |
| `./scripts/` | Node.js automation utilities |

## Best Practices

### During Recovery

1. **Don't rush** - Verify state before committing
2. **Use haiku** - Cheap parallel log analysis
3. **Verify on disk** - Don't trust logs alone
4. **Commit incrementally** - One commit per verified task
5. **Update tracking** - Keep progress files current

### Prevention

1. **Smaller batches** - 3-4 agents max per batch
2. **Checkpoint often** - After each task completion
3. **Track agent IDs** - In progress file YAML
4. **Sequential dependencies** - Don't parallelize dependent work
5. **Background execution** - Use for large batches with timeouts

## Practical Lessons (2025-12-31)

Key insights from real recovery sessions:

### 1. File-First Verification is Faster

**Problem**: Complex jq/grep parsing of JSONL logs is fragile and slow.

**Solution**: Check if expected files exist BEFORE parsing logs in detail.

```bash
# FAST: Check file exists and has content
if [ -f "$expected_file" ] && [ -s "$expected_file" ]; then
  echo "✓ COMPLETE: $expected_file ($(wc -l < "$expected_file") lines)"
fi
```

### 2. Count Both Write AND Edit Operations

**Problem**: Only checking for `Write` misses agents that modify existing files.

**Solution**: Always check for both:

```bash
# Count file operations (both types)
echo "Write ops: $(grep -c '"Write"' "$LOG" 2>/dev/null || echo 0)"
echo "Edit ops: $(grep -c '"Edit"' "$LOG" 2>/dev/null || echo 0)"
```

Agents completing via Edit only are common (3 of 6 in one session).

### 3. Simple Grep Beats Complex jq

**Problem**: jq pipelines fail on macOS or with nested content blocks.

**Solution**: Use simple grep patterns that work everywhere:

```bash
# Reliable cross-platform pattern
grep -c 'Write' "$LOG"      # Count Write operations
tail -1 "$LOG" | grep -o '"type":"[^"]*"'  # Last message type
```

### 4. Log Structure Has Metadata

The JSONL format includes useful top-level fields:

```json
{
  "agentId": "a610b3c",
  "sessionId": "758467e4-...",
  "type": "user|assistant",
  "message": { ... }
}
```

Use `agentId` for correlation with progress tracking.

### 5. git status is the Source of Truth

**Best workflow**:
1. Run `git status --short` first
2. New files (`??`) = likely agent output
3. Modified files (`M`) = likely edits applied
4. Cross-reference with expected deliverables
5. Only parse logs for ambiguous cases

### 6. macOS Command Differences

Some commands behave differently on macOS (BSD) vs Linux (GNU):

| Command | macOS Issue | Workaround |
|---------|-------------|------------|
| `stat` | Different flags | Use `stat -f "%Sm"` on macOS |
| `uniq -c` | May need `sort` first | Always `sort \| uniq -c` |
| `sed -i` | Requires backup arg | Use `sed -i ''` or avoid |

## Example Recovery Session

```
> My session crashed with 6 agents running. Help me recover.

1. Finding project log directory...
   LOG_DIR: ~/.claude/projects/-Users-miethe-dev-skillmeat/

2. Discovering recent agent logs (last 3 hours)...
   Found 6 agent logs

3. Analyzing logs in parallel (haiku subagents)...
   a91845a: COMPLETE - MatchAnalyzer (2 files, 33 tests)
   abec615: COMPLETE - SemanticScorer (4 files, 17 tests)
   adad508: COMPLETE - DiffViewer (3 files, 25 tests)
   xyz1234: IN_PROGRESS - RatingDialog (1 file, no tests)
   abc5678: FAILED - FormValidator (error in final lines)
   def9012: NOT_STARTED - empty log

4. Verifying on-disk state...
   All files from COMPLETE agents verified
   RatingDialog component exists but incomplete

5. Generating recovery report...
   [See ./templates/recovery-report.md]

6. Ready to commit completed work?
   Files: [list of 9 files]

7. Resumption commands for interrupted work:
   Task("ui-engineer-enhanced", "Complete P4-T3: RatingDialog...")
   Task("python-backend-engineer", "Fix FormValidator...")
```

## Summary

This skill provides **standardized session recovery** with:
- Automated agent log discovery and analysis
- On-disk state verification
- Clear status reporting per task
- Ready-to-execute resumption commands
- Prevention recommendations

**Key Files**:
- Discovery: `./techniques/discovering-agent-logs.md`
- Parsing: `./techniques/parsing-jsonl-logs.md`
- Verification: `./techniques/verifying-on-disk-state.md`
- Planning: `./techniques/generating-resumption-plans.md`
- Prevention: `./references/prevention-patterns.md`
