---
name: observability-analyze-session-logs
description: |
  Analyzes Claude Code session transcripts (JSONL files) to reveal context window content, token usage patterns,
  and decision-making processes using view_session_context.py tool. Use when debugging Claude behavior,
  investigating token patterns, tracking agent delegation, or analyzing context exhaustion. Triggers on
  "why did Claude do X", "analyze session", "check session logs", "context window exhaustion", or
  "track agent delegation".
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Analyze Session Logs

> **IMPORTANT DISTINCTION**: This skill analyzes **Claude Code session transcripts** (what Claude saw and thought), NOT application/production logs (what code executed). For application logs, use the **analyze-logs** skill instead.

## Quick Start

**Most common usage (list all messages):**
```bash
python3 .claude/tools/utils/view_session_context.py <session-file.jsonl> --list
```

**View context at specific point (by message index):**
```bash
python3 .claude/tools/utils/view_session_context.py <session-file.jsonl> --message-index 10
```

**View context at specific message (by UUID from logs/errors):**
```bash
python3 .claude/tools/utils/view_session_context.py <session-file.jsonl> --uuid "3c8467d6-..."
```

## When to Use This Skill

Invoke this skill when users mention:
- "why did Claude do X?"
- "what was in the context window?"
- "analyze session" / "check session logs"
- "debug Claude behavior"
- "token usage investigation"
- "context window exhaustion"
- "track agent delegation"
- Any mention of `.jsonl` session files

**Use cases:**
1. **Debugging decisions** - "Why did Claude choose approach X?" → View context at decision point
2. **Token analysis** - "Where are tokens being used?" → Track cache creation vs cache read
3. **Agent tracking** - "How are agents being delegated?" → Follow sidechain messages
4. **Context exhaustion** - "Why did Claude lose context?" → See context window growth
5. **Performance issues** - "Why is Claude slow?" → Identify cache thrashing

## What This Skill Does

Analyzes Claude Code session transcripts to provide forensic visibility into Claude's internal state, decision-making process, context window content, and token usage patterns.

**What it reveals:**
- Context window content at any point in conversation
- Token usage breakdown (input, cache creation, cache read, output)
- Message chains (parent-child relationships)
- Agent delegation patterns (sidechain vs main thread)
- Context window growth over time
- Thinking blocks (Claude's internal reasoning)
- Tool calls with parameters and results

**Key Distinction:**
- **This skill**: Analyzes Claude's session transcripts → Shows "what Claude saw and thought"
- **analyze-logs skill**: Analyzes OpenTelemetry application logs → Shows "what code executed"
- **Use both together** for complete debugging

## Session File Locations

**User-level session files (Claude Code transcripts):**
```
~/.claude/projects/-Users-{username}-{project-path}/{session-uuid}.jsonl
```

**Find recent sessions:**
```bash
ls -lt ~/.claude/projects/-Users-$(whoami)-*/*.jsonl | head -5
```

## Instructions

Follow this workflow to analyze Claude Code session logs:

1. **Locate session file** - Find .jsonl file in ~/.claude/projects/
2. **Choose analysis mode** - List messages, view context at index, or view at UUID
3. **Execute analysis** - Run view_session_context.py with appropriate flags
4. **Interpret results** - Examine context window, token usage, and decision points
5. **Report findings** - Explain Claude's behavior with evidence from context

## Analysis Workflow

### Step 1: Locate Session File

```bash
# Find most recent session file
ls -lt ~/.claude/projects/-Users-$(whoami)-*/*.jsonl | head -5

# Or search by UUID from error messages
grep -r "uuid" ~/.claude/projects/*/
```

### Step 2: Choose Analysis Mode

**Mode 1: List All Messages (Overview)**
```bash
python3 .claude/tools/utils/view_session_context.py <session.jsonl> --list
```

Use when: Initial investigation, finding specific messages, tracking token usage

**Mode 2: Context Window at Specific Point**
```bash
python3 .claude/tools/utils/view_session_context.py <session.jsonl> --message-index 10
```

Use when: Debugging specific decision, understanding available context, seeing thinking blocks

**Mode 3: View Specific Message by UUID**
```bash
python3 .claude/tools/utils/view_session_context.py <session.jsonl> --uuid "3c8467d6-..."
```

Use when: Error logs reference specific message UUID

**Mode 4: View Raw JSON**
```bash
python3 .claude/tools/utils/view_session_context.py <session.jsonl> --message-index 10 --raw
```

Use when: Need exact JSON structure, programmatic analysis

### Step 3: Execute Analysis

Run the appropriate command using the Bash tool:
```bash
python3 .claude/tools/utils/view_session_context.py ~/.claude/projects/-Users-*/abc123.jsonl --list
```

### Step 4: Interpret Results

**For List Output:**
1. Check message count - How long was the session?
2. Identify MAIN vs SIDE - SIDE indicates agent delegation
3. Spot token patterns:
   - High Cache Create = New context being cached
   - High Cache Read = Good cache utilization
   - High Cache Create repeatedly = Cache thrashing
4. Find interesting points - Large output tokens, sudden cache creation, sidechains
5. Note message indices for deeper investigation

**For Context Window Output:**
1. Review message chain - Understand conversation flow
2. Read THINKING blocks - See Claude's internal reasoning
3. Check TOOL calls - What tools were invoked and why
4. Examine token breakdown (input, cache creation, cache read, output)
5. Check total context size - Is it approaching 200k limit?

**For Token Usage:**
- Cache creation spike = Context changed significantly
- High cache read = Good utilization (cost effective)
- Low cache read = Cache misses (investigate why)
- Growing total context = Approaching 200k limit

### Step 5: Report Findings

Always provide:
1. **Summary** - Session length, main vs sidechain messages, total tokens
2. **Key insights** - What explains the behavior?
3. **Specific examples** - Quote relevant thinking blocks, tool calls
4. **Context evidence** - Show what Claude had access to
5. **Suggested next steps** - Additional investigation or fixes

**Example response format:**
```
Analyzed session abc123.jsonl (42 messages):

Key Findings:
1. Agent delegation at message 15 (→ unit-tester)
   - Context window at that point: 24,059 tokens
   - Thinking: "Need comprehensive test coverage for new service"
   - Agent had access to service implementation but not architectural context

2. Cache thrashing at messages 28-35
   - Cache creation spiked to 18k tokens each message
   - Context kept changing due to repeated file edits
   - Suggestion: Batch edits to reduce cache invalidation

3. Context exhaustion at message 40
   - Total context: 189,234 tokens (approaching 200k limit)
   - Claude started summarizing instead of quoting full code

To investigate further:
- View agent delegation context: --message-index 15
- Examine cache thrashing: --message-index 30
```

## Best Practices

1. **Start with List Mode** - Always get the overview first to identify interesting points
2. **Identify Patterns** - Look for high cache creation (10k+ tokens), SIDE messages, large outputs
3. **Use Message Index for Deep Dives** - From list output, drill down to specific points
4. **Follow Agent Delegation Chains** - When you see [SIDE], trace back to parent in main thread
5. **Track Token Usage** - Good: high cache read (80%+), Bad: repeated cache creation (thrashing)
6. **Compare Before/After** - When debugging changes, analyze sessions before and after fix
7. **Correlate with Code Execution Logs** - Session logs show "what Claude thought", OpenTelemetry logs show "what code executed"
8. **Save Important Sessions** - Archive critical sessions to `.claude/artifacts/` for future reference

## Common Scenarios

### "Why did Claude do X?"
1. Find session file → List messages (`--list`)
2. Identify message where decision was made
3. View context at that point (`--message-index N`)
4. Read THINKING blocks to see reasoning
5. Explain: "Claude did X because context included Y but not Z"

### Token Usage Investigation
1. List messages to see token breakdown
2. Identify spikes in cache_creation_input_tokens
3. View context at spike points
4. Determine what caused cache invalidation
5. Suggest optimizations (batch edits, cache earlier)

### Agent Delegation Analysis
1. List messages to find sidechains ([SIDE])
2. View sidechain message context
3. Trace back to parent in main thread
4. Compare context available in main vs sidechain
5. Explain what agent could/couldn't see

### Context Window Exhaustion
1. List messages to track context growth
2. Identify where total context approaches 200k
3. View context at exhaustion point
4. Analyze what's consuming space
5. Suggest context optimization (new session, prune messages)

## Integration with Other Skills

- **analyze-logs** - Combine session logs (what Claude thought) with execution logs (what code did)
- **debug-test-failures** - See what context was available when tests were written
- **orchestrate-agents** - Track actual delegation patterns vs expected
- **check-progress-status** - Understand how tasks were completed (decision points, delegations)

## Supporting Files

- **[references/reference.md](references/reference.md)** - Technical depth:
  - Session file format specification (JSONL structure)
  - Data models and content block types
  - Parent-child chain reconstruction algorithm
  - Cache token types and pricing details
  - Performance characteristics and limits
  - Tool implementation details
  - Understanding output format (session structure, token breakdown, message chains)
  - Advanced usage patterns (session comparison, pattern detection, metrics)
  - Troubleshooting guide (common errors, solutions)
  - Complete command reference

- **[templates/response-template.md](templates/response-template.md)** - Response formatting:
  - 6 response templates for different contexts
  - List mode summary template
  - Context window analysis template
  - Agent delegation investigation template
  - Token usage spike template
  - Context exhaustion template

## Requirements

**Tools:**
- Python 3.12+ (already in project)
- Session viewer: `.claude/tools/utils/view_session_context.py` (bundled)
- jq (optional, for advanced analysis): `brew install jq`

**Session files:**
- User-level: `~/.claude/projects/-Users-{username}-{project-path}/{session-uuid}.jsonl`
- Generated automatically by Claude Code

**Verification:**
```bash
# Verify tool exists
ls .claude/tools/utils/view_session_context.py

# Verify session files exist
ls -l ~/.claude/projects/-Users-$(whoami)-*/

# Test the tool
python3 .claude/tools/utils/view_session_context.py \
  $(ls -t ~/.claude/projects/-Users-$(whoami)-*/*.jsonl | head -1) --list
```

## Quick Reference

| Goal | Command |
|------|---------|
| List all messages | `python3 .claude/tools/utils/view_session_context.py <session.jsonl> --list` |
| View context at point | `python3 .claude/tools/utils/view_session_context.py <session.jsonl> --message-index 10` |
| View by UUID | `python3 .claude/tools/utils/view_session_context.py <session.jsonl> --uuid "abc123..."` |
| View raw JSON | `python3 .claude/tools/utils/view_session_context.py <session.jsonl> --message-index 10 --raw` |
| Find recent sessions | `ls -lt ~/.claude/projects/-Users-$(whoami)-*/*.jsonl \| head -5` |

---

**Key Messages:**
- This skill provides **X-ray vision into Claude's decision-making**
- Use when behavior is unexpected or token usage is unclear
- Complements OpenTelemetry logs (code execution) with context window visibility (what Claude thought)
- Essential for debugging complex agent orchestration
- Start with `--list`, then drill down with `--message-index`

**Remember:** Session logs show what Claude had access to and how it reasoned. This is your forensic tool for understanding "why Claude did X."
