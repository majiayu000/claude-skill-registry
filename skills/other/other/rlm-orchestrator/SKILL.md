---
name: rlm-orchestrator
description: >-
  Implement RLM-style (Recursive Language Model) orchestration for complex tasks.
  This skill should be used when facing large context requirements, multi-part tasks
  that would benefit from parallel execution, or when context rot is a concern.
  Automatically decomposes tasks, spawns parallel subagents, aggregates results,
  and iterates until completion. Inspired by the RLM research paper (arXiv:2512.24601).
trigger: >-
  When user mentions "RLM", "recursive", "parallel agents", "context rot prevention",
  "large context task", or when facing tasks that would exceed comfortable context limits
version: 1.0.0
tags:
  - orchestration
  - subagents
  - context-management
  - parallel-execution
  - rlm
  - claude-code-only
---

# RLM-Style Recursive Orchestrator

Implement the orchestrator pattern from RLM research to handle arbitrarily large contexts
and complex multi-part tasks. The main conversation acts as the recursive coordinator,
spawning depth-1 subagents and aggregating results.

## Core Principle

> "No single language model call should require handling a huge context."
> — RLM Research (arXiv:2512.24601)

Since Claude Code subagents cannot spawn children (architectural limit), the main
conversation becomes the "recursion stack," enabling functional depth >1.

## When to Use This Skill

**Ideal for:**
- Tasks requiring >100K tokens of context
- Multi-file analysis or refactoring
- Research tasks with many sources
- Batch processing with independent partitions
- Any task showing signs of context rot (degraded recall, repeated mistakes)

**Not ideal for:**
- Simple single-file changes
- Tasks requiring tight sequential dependencies
- Quick exploratory questions

## The RLM Orchestration Pattern

```
Main Session (orchestrator/recursion stack)
    │
    ├─[DECOMPOSE]─ Analyze task, identify independent partitions
    │
    ├─[SPAWN BATCH 1]──┬── Subagent A (fresh 200K context) → summary
    │                  ├── Subagent B (fresh 200K context) → summary
    │                  └── Subagent C (fresh 200K context) → summary
    │
    ├─[AGGREGATE]─ Combine results, identify gaps
    │
    ├─[SPAWN BATCH 2]──┬── Subagent D (uses batch 1 results) → summary
    │                  └── Subagent E (uses batch 1 results) → summary
    │
    ├─[AGGREGATE]─ Final combination
    │
    └─[COMPLETE]─ Return unified result
```

## Orchestration Protocol

### Phase 1: Task Analysis and Decomposition

Before spawning any subagents, analyze the task:

1. **Estimate context requirements**
   - Count files/sources to process
   - Estimate tokens (~4 bytes per token)
   - If <50K tokens total, consider direct execution

2. **Identify partition boundaries**
   - Find natural divisions (files, sections, topics)
   - Ensure partitions are independent (no cross-dependencies)
   - Aim for 3-7 partitions per batch (Claude Code limit: ~10 concurrent)

3. **Define aggregation strategy**
   - How will partition results combine?
   - What format should subagent outputs use?
   - What information must propagate between batches?

### Phase 2: Subagent Dispatch

For each batch of partitions:

1. **Prepare subagent prompts** using the template in `references/subagent-prompt-template.md`

2. **Spawn subagents in parallel** using the Task tool:
   ```
   Task(subagent_type="general-purpose", description="[partition description]", prompt="...")
   Task(subagent_type="Explore", description="[research partition]", prompt="...")
   ```

3. **Use appropriate subagent types:**
   - `Explore` - For read-only research, file discovery
   - `general-purpose` - For tasks requiring code changes
   - `Plan` - For architecture/design work

4. **Run in background when appropriate:**
   - Set `run_in_background=true` for long-running tasks
   - Check results via `TaskOutput` or `Read` on output file

### Phase 3: Result Aggregation

When subagents complete:

1. **Collect all results** - Read summaries from each subagent

2. **Validate completeness** - Check for error indicators:
   - "could not find", "unable to", "failed to"
   - Missing expected outputs
   - Incomplete coverage of partition

3. **Merge results** using appropriate strategy:
   - **Union**: Combine all findings (research tasks)
   - **Synthesis**: Create unified narrative (analysis tasks)
   - **Reduce**: Aggregate metrics (measurement tasks)

4. **Identify gaps** - What wasn't covered? What needs follow-up?

### Phase 4: Iteration (if needed)

If gaps exist:

1. **Create follow-up partitions** for uncovered areas
2. **Include previous batch context** in new subagent prompts
3. **Spawn next batch** with refined focus
4. **Repeat until complete** or max iterations reached

## Emerged Strategies (from RLM Research)

Encode these strategies in subagent prompts:

### Peeking
> Sample the beginning of context to understand structure before deep processing.

```markdown
Before analyzing fully, first peek at the structure:
1. Read first 50 lines of each file
2. Identify file types and organization
3. Then proceed with targeted analysis
```

### Grepping
> Use pattern-based filtering to narrow context before semantic processing.

```markdown
Use Grep to filter before reading:
1. Search for relevant patterns: `Grep(pattern="error|exception|fail")`
2. Read only matching files fully
3. This reduces context consumption by 80%+
```

### Partition + Map
> Break context into chunks, process in parallel, then aggregate.

```markdown
This task uses partition+map strategy:
1. You handle partition [X] of [N]
2. Your partition covers: [specific scope]
3. Return findings in this format: [format spec]
4. Orchestrator will aggregate all partition results
```

### Summarization
> Extract condensed information for parent decision-making.

```markdown
Return a structured summary, not raw data:
- Key findings (3-5 bullet points)
- Specific file:line references
- Confidence level (high/medium/low)
- Gaps or uncertainties
```

## Token Budget Management

Track token consumption across the orchestration:

| Component | Estimated Tokens | Notes |
|-----------|------------------|-------|
| Main conversation | 200K max | Reserve 50K for orchestration |
| Per subagent | 200K max | Fresh context each |
| Subagent overhead | ~20K | System prompt + tools |
| Summary return | ~2-5K | Per subagent result |

**Budget formula:**
```
Effective capacity = (Main 150K usable) + (N subagents × 180K usable each)
For 5 subagents: 150K + 900K = ~1M effective tokens
```

## Integration with Existing Skills

This skill works with:

- **superpowers:brainstorming** - Use first to decompose complex problems
- **superpowers:writing-plans** - Create task partition structure
- **superpowers:dispatching-parallel-agents** - Detailed parallel dispatch patterns
- **superpowers:subagent-driven-development** - For implementation tasks
- **ralph-loop** - For autonomous iteration within partitions

## Example: Large Codebase Analysis

```markdown
# Task: Analyze security vulnerabilities across 500 files

## Phase 1: Decomposition
- Partition by directory: src/, lib/, tests/, config/
- Each partition: ~125 files, ~50K tokens
- Aggregation: Union of findings with deduplication

## Phase 2: Dispatch (Batch 1)
- Subagent A: src/ directory - authentication code
- Subagent B: lib/ directory - utility functions
- Subagent C: config/ directory - configuration files
- Subagent D: tests/ directory - test coverage gaps

## Phase 3: Aggregate
- Combine all vulnerability findings
- Cross-reference duplicates
- Prioritize by severity

## Phase 4: Follow-up (if needed)
- Deep dive on critical findings
- Verify false positives
```

## Troubleshooting

**Subagent returns incomplete results:**
- Check if partition was too large (reduce scope)
- Verify subagent had appropriate tools
- Retry with more specific instructions

**Aggregation produces conflicts:**
- Subagents may find contradictory information
- Spawn a "resolver" subagent to investigate conflicts
- Or present both findings with uncertainty markers

**Context still rotting in main session:**
- You're keeping too much in the main context
- Delegate more aggressively to subagents
- Trust summaries instead of raw data

**Hitting concurrent subagent limit:**
- Queue batches: 10 concurrent max
- Wait for batch completion before spawning next
- Consider if fewer, larger partitions would work

## Quick Start Template

For any large task, start with:

```markdown
I'll use RLM orchestration for this task.

**Task Analysis:**
- Total scope: [X files / Y sources / Z components]
- Estimated tokens: [rough estimate]
- Natural partitions: [list 3-7 independent parts]

**Orchestration Plan:**
1. Batch 1: [partitions A, B, C] - parallel Explore subagents
2. Aggregate: [strategy]
3. Batch 2 (if needed): [follow-up partitions]

**Subagent assignments:**
- Subagent A: [specific scope and instructions]
- Subagent B: [specific scope and instructions]
...

Proceeding with Phase 1...
```
