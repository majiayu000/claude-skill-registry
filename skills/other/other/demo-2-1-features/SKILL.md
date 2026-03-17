---
name: demo-2-1-features
description: Demo skill showing all Claude Code 2.1 features. Use when asked to "demo 2.1" or "show new skill features".

# NEW IN 2.1: Isolated execution context (keeps main conversation clean)
context: fork

# Use general-purpose for Task tool access (enables parallel agents)
agent: general-purpose

# NEW IN 2.1: Cost optimization with model selection
model: haiku

# YAML-style tool list (cleaner than comma-separated)
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - TaskOutput
  - AskUserQuestion

user-invocable: true

# NEW IN 2.1: Lifecycle hooks scoped to this skill
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "echo '🚀 Launching parallel agent...'"
  PostToolUse:
    - matcher: "TaskOutput"
      hooks:
        - type: command
          command: "echo '✅ Agent results received'"
  Stop:
    - hooks:
        - type: command
          command: "echo '📊 Demo complete! All 2.1 features demonstrated.'"
---

# Knowledge Graph Quick Scan

This skill demonstrates Claude Code 2.1's parallel agent capabilities by analyzing your Second Brain knowledge base.

## Phase 1: Parallel Analysis

Launch exactly 3 Explore agents **IN A SINGLE MESSAGE** (this is critical - all 3 Task calls must be in one response to demonstrate parallelism):

**Agent 1 - Content Stats:**
Prompt: "Count markdown files in content/ directory by their frontmatter 'type' field. Read 10-15 sample files to identify the types used (book, podcast, article, til, moc, etc.), then use Glob to count files. Report a breakdown table of type → count."

**Agent 2 - Orphan Detection:**
Prompt: "Find markdown files in content/ that contain NO wiki-links (no [[...]] patterns). These are 'orphan' notes that could benefit from connections. Use Grep to find files WITHOUT the [[ pattern. Report the top 5 candidates with their titles."

**Agent 3 - Recent Activity:**
Prompt: "Find the 5 most recently modified markdown files in content/. Use Glob with sorting by modification time. Report their titles and relative dates (e.g., '2 days ago')."

## Phase 2: Collect & Present

Use TaskOutput (with block=true) to wait for all 3 agents.

Present findings in a summary:

```markdown
## 📊 Knowledge Graph Quick Scan Results

### Content Breakdown
[Agent 1 results as table]

### Orphan Notes (Need Links)
[Agent 2 results as list]

### Recently Modified
[Agent 3 results as list]
```

## Phase 3: Interactive Follow-up

Use AskUserQuestion with these options:
- Question: "What would you like to explore next?"
- Options:
  1. "Deep dive into orphan notes" - Show more orphans with suggestions
  2. "Analyze link patterns" - Find most-linked notes
  3. "Show more content stats" - Detailed type breakdown
  4. "Done - show feature summary" - End with 2.1 features list

If user selects options 1-3, spawn another targeted Explore agent.
If user selects option 4 or after completing a follow-up, proceed to Phase 4.

## Phase 4: Feature Summary

End by displaying:

```markdown
## 2.1 Features Demonstrated

✓ context: fork - Isolated execution (main conversation unchanged)
✓ agent: general-purpose - Enabled Task tool for parallelism
✓ model: haiku - Cost-optimized execution
✓ Parallel Task agents - 3 agents launched simultaneously
✓ hooks.PreToolUse - "🚀 Launching..." on each Task call
✓ hooks.PostToolUse - "✅ Results received" on each TaskOutput
✓ hooks.Stop - Completion message at end
✓ AskUserQuestion - Interactive follow-up options
✓ YAML allowed-tools - Cleaner list syntax
```

---

## Important Notes

- This is a READ-ONLY demo - no files are modified
- All agents use subagent_type: "Explore" for fast, safe analysis
- The demo works best with a populated content/ directory
