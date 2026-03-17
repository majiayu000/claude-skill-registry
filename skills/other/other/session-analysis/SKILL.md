---
name: session-analysis
agent: explore
context: fork
description: "Analyze session transcripts for patterns, mistakes, and improvements. Use when reviewing past work, identifying recurring issues, or summarizing completed sessions. Includes transcript parsing, pattern detection, improvement suggestions, and metrics extraction. Not for live session work."
---

<mission_control>
<objective>Extract insights from session transcripts to identify patterns, mistakes, and improvement opportunities</objective>
<success_criteria>Complete analysis with pattern summary, mistake categorization, improvement suggestions, and key metrics</success_criteria>
</mission_control>

## Quick Start

**If you need to analyze a session:** Read the transcript, extract metrics, identify patterns, and summarize findings.

**If you need to compare sessions:** Load multiple transcripts, identify trends, and track improvement over time.

**If you need to generate a report:** Output structured markdown with findings, metrics, and action items.

## Session Data Structure

### Files to Read

| File | Path | Purpose |
| :--- | :--- | :--- |
| Transcript | `.claude/workspace/sessions/{id}/raw-transcript.jsonl` | Full session messages |
| Start | `.claude/workspace/sessions/{id}/start.jsonl` | Session metadata |
| End | `.claude/workspace/sessions/{id}/end.jsonl` | Session duration, stats |
| Previous | `.claude/workspace/sessions/previous-session.jsonl` | Most recent session |

### Transcript Format

Each line is a JSON message:

```json
{"message":{"content":[{"type":"text","text":"User request"},{"type":"tool_use","name":"Read","input":{"file_path":"..."}}],"role":"user"},"timestamp":"..."}
```

Extract:
- `message.content[].type` - message type (text, tool_use, tool_result)
- `message.content[].text` - actual content
- `message.role` - user or assistant

## Analysis Framework

### Phase 1: Load & Basic Metrics

```
1. Read transcript JSONL
2. Count messages by type
3. Calculate session duration (start → end timestamps)
4. Extract tool usage frequency
5. Identify session branch/context
```

### Phase 2: Pattern Detection

| Pattern | Indicator | Significance |
| :--- | :--- | :--- |
| Skill invocation | `Skill(...)` calls | Skill adoption rate |
| Tool chaining | Multiple related tools in sequence | Workflow efficiency |
| Context switching | Frequent file switching | Focus quality |
| Error loops | Same error repeated | Training opportunity |
| Iteration | Multiple attempts at same goal | Task complexity |
| Quick wins | Single-pass task completion | Skill fit |

### Phase 3: Mistake Identification

Common categories:

1. **Skill gap** - Task done manually when skill exists
2. **Context miss** - Acting without reading relevant files
3. **Over-engineering** - Complex solution for simple problem
4. **Under-engineering** - Simple solution for complex problem
5. **Tool misuse** - Wrong tool for the job
6. **Validation skip** - No verification after action

### Phase 4: Improvement Extraction

For each mistake pattern:

```
- What happened
- Why it happened (root cause)
- How to prevent it
- Skill or rule that could help
```

## Output Format

```markdown
# Session Analysis: {session_id}

## Summary
- Duration: {start} → {end}
- Total messages: {n}
- Tool invocations: {n}
- Skills invoked: {n}

## Key Patterns

### Positive Patterns
- [Pattern description with evidence]

### Improvement Areas
- [Pattern description with evidence]
- [Root cause]
- [Suggested fix]

## Mistakes Analysis

| Mistake | Count | Severity | Root Cause |
| :--- | :--- | :--- | :--- |
| [Type] | n | high/med/low | [Cause] |

## Recommendations

1. [Actionable improvement]
2. [Skill to invoke]
3. [Rule to add]
```

## Practical Examples

### Example 1: Analyze Previous Session

```bash
# Read previous session transcript
Read .claude/workspace/sessions/previous-session.jsonl

# Parse and analyze
# Extract messages, tools, timestamps
# Generate report
```

### Example 2: Compare Two Sessions

```bash
# Load both transcripts
Read .claude/workspace/sessions/{id1}/raw-transcript.jsonl
Read .claude/workspace/sessions/{id2}/raw-transcript.jsonl

# Compare metrics
# Identify trends
# Output comparison
```

### Example 3: Extract Training Data

```bash
# Find recurring mistakes
# Categorize by type
# Generate improvement suggestions
# Output as actionable items
```

## Common Analysis Tasks

### Task: Post-Session Review

1. Read `previous-session.jsonl`
2. Extract all tool calls and their outcomes
3. Identify any user corrections ("No", "Wrong", "Wait")
4. Count skill invocations vs direct tool use
5. Generate improvement suggestions

### Task: Trend Analysis

1. Load last 3 session transcripts
2. Calculate metrics for each
3. Track improvement/decline
4. Identify persistent issues
5. Recommend focused improvement

### Task: Skill Gap Analysis

1. Count `Skill(...)` invocations
2. Identify tasks that could use skills but didn't
3. Cross-reference with available skills
4. Suggest missing skills or skill adoption

## Command Aliases

For quick analysis, use these patterns:

| Alias | Command |
| :--- | :--- |
| `/session:analyze` | Analyze previous session |
| `/session:compare id1 id2` | Compare two sessions |
| `/session:patterns` | Extract recurring patterns |
| `/session:summary` | Quick session overview |

## Output Best Practices

1. **Lead with summary** - Top-level findings first
2. **Include evidence** - Quote from transcript
3. **Be specific** - File paths, line numbers
4. **Actionable** - Each finding has a next step
5. **Quantified** - Use metrics when possible
