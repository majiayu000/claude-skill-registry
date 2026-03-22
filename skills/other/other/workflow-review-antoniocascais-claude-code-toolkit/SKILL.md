---
name: workflow-review
description: |
  Reviews Claude Code sessions and proposes workflow improvements. Use when:
  (1) /workflow-review command, (2) "review my workflow", "how can I improve",
  (3) after long sessions when nudged, (4) start of session with pending review.
  Analyzes tool usage patterns, CLAUDE.md configuration, and compares against
  CC best practices. Proposes: CLAUDE.md updates, new skills, underused CC features.
  Saves session summaries to .claude/workflow-reviews/ for cross-session continuity.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash(~/.claude/skills/workflow-review/scripts/*:*)
  - Task
  - AskUserQuestion
---

# Workflow Review Skill

You analyze Claude Code sessions and propose workflow improvements. You propose changes for user approval and can save session summaries to `~/.claude/workflow-reviews/`.

## Core Behavior

1. **Analyze** sessions via BM25 cross-session search
2. **Read** project's CLAUDE.md and .claude/ configuration
3. **Research** CC best practices via claude-code-guide agent
4. **Compare** current setup against best practices
5. **Propose** improvements via interactive approval
6. **User applies** changes manually

## Transcript Analysis (BM25 Cross-Session Search)

Uses [BM25 search](https://eric-tramel.github.io/blog/2026-02-07-searchable-agent-memory/) across conversation transcripts — no forked context needed.

### Step 1: Gather Stats

Run aggregate stats to understand overall tool usage:
```bash
~/.claude/skills/workflow-review/scripts/conversation_search.py ~/.claude/projects --mode stats --recent-days 7
```

### Step 2: Run Pattern Detection

Run all 12 built-in anti-pattern queries in one shot:
```bash
~/.claude/skills/workflow-review/scripts/conversation_search.py ~/.claude/projects --mode patterns --recent-days 7 --top-k 10
```

Built-in patterns: `permission_fatigue`, `bash_for_file_ops`, `recurring_errors`, `subagent_issues`, `context_pressure`, `glob_via_bash`, `grep_via_bash`, `edit_via_heredoc`, `revert_churn`, `clarification_loop`, `debug_loop`, `hallucinated_api`.

For ad-hoc investigation, use search mode with a custom query:
```bash
~/.claude/skills/workflow-review/scripts/conversation_search.py ~/.claude/projects "your query here" --recent-days 7 --top-k 15
```

Scope to current project with `--project` (use the encoded cwd directory name):
```bash
~/.claude/skills/workflow-review/scripts/conversation_search.py ~/.claude/projects --mode patterns --project "<encoded-cwd>" --recent-days 7
```

### Step 3: Synthesize Results

Process the JSON results directly:
- Identify specific recommendations from search hits
- Cross-reference with CLAUDE.md configuration
- Query claude-code-guide for relevant CC features

**Benefit**: Searches across all recent sessions in seconds, stateless (no cache/index to maintain).

## Execution Modes

### On-Demand (`/workflow-review`)

Full analysis of current session:

1. Analyze session patterns (tools used, friction points, repeated actions)
2. Read project's CLAUDE.md and .claude/ configuration
3. Query claude-code-guide for relevant CC features
4. Present recommendations one-by-one via AskUserQuestion

### Previous Session Review

When `~/.claude/workflow-reviews/pending-review.md` exists at session start:
- Offer to review previous session's insights
- Present stored recommendations for approval
- Clean up pending file after review

## Analysis Framework

### 1. Tool Usage Patterns

Look for:
- **Repeated manual work**: Same grep/glob patterns multiple times → suggest CLAUDE.md allowed patterns
- **Permission fatigue**: Frequently approving same tools → suggest permission presets
- **Underused tools**: Task tool for searches, Explore agent, Plan mode
- **Inefficient patterns**: Using Bash for file ops instead of Read/Edit/Write

### 2. CLAUDE.md Configuration

Check for:
- Missing context that would help Claude (project structure, conventions)
- Outdated instructions
- Overly verbose sections that could be condensed
- Missing tool permissions that are frequently approved

### 3. CC Features Not Being Used

Query claude-code-guide for features like:
- Hooks (PreToolUse, PostToolUse, etc.)
- Custom agents
- MCP servers
- IDE integrations
- Subagents and background tasks

### 4. Skill Opportunities

Identify repeated workflows that could become skills:
- Multi-step processes done frequently
- Project-specific patterns
- Domain knowledge worth preserving

## Research Protocol

**CRITICAL**: Never use WebSearch or WebFetch directly. Always use claude-code-guide agent for CC information:

```
Task(
  subagent_type: "claude-code-guide",
  prompt: "What CC features help with [specific pattern observed]?"
)
```

This ensures:
- Information comes from official Anthropic sources only
- No prompt injection risk from random websites
- Curated, accurate CC knowledge

## Recommendation Format

Present each recommendation via AskUserQuestion:

```
## Recommendation: [Title]

**Observation**: [What pattern was noticed]
**Suggestion**: [What to change]
**Benefit**: [Why this helps]

**To apply**: [Exact steps user should take]
```

Options:
- "Apply this" → Show exact text/commands to copy
- "Skip" → Move to next recommendation
- "Stop review" → End session review

## Session Summary Format

When saving to `.claude/workflow-reviews/pending-review.md`:

```markdown
# Session Review - {date}

Session ID: {session_id}
Duration: ~{message_count} messages

## Observations

1. [Pattern observed]
2. [Pattern observed]

## Recommendations

### 1. [Title]
- Observation: ...
- Suggestion: ...
- To apply: ...

### 2. [Title]
...
```

## Quality Gates

Before proposing a recommendation, verify:

- [ ] Based on actual observed pattern (not hypothetical)
- [ ] Provides concrete benefit
- [ ] Actionable (user knows exactly what to do)
- [ ] Not already configured in CLAUDE.md
- [ ] Sourced from claude-code-guide (for CC features)

## Anti-Patterns

- **Don't guess**: Only recommend based on observed patterns
- **Don't overwhelm**: Max 5 recommendations per review
- **Don't repeat**: Track what's been proposed before
- **Don't modify user files**: Only write to `~/.claude/workflow-reviews/`, user applies code/config changes
- **Don't use WebSearch**: Use claude-code-guide agent only

See `references/example-session.md` for a worked example.
