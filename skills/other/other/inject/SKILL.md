---
name: inject
description: 'Inject relevant knowledge into session context from .agents/ artifacts. Triggers: "inject knowledge", "recall context", SessionStart hook.'
user-invocable: false
metadata:
  tier: background
  dependencies: []
  internal: true
---

# Inject Skill

**Typically runs automatically via SessionStart hook.**

Inject relevant prior knowledge into the current session.

## How It Works

The SessionStart hook runs:
```bash
ao inject --apply-decay --format markdown --max-tokens 1000
```

This searches for relevant knowledge and injects it into context.

## Manual Execution

Given `/inject [topic]`:

### Step 1: Search for Relevant Knowledge

**With ao CLI:**
```bash
ao inject --context "<topic>" --format markdown --max-tokens 1000
```

**Without ao CLI, search manually:**
```bash
# Recent learnings
ls -lt .agents/learnings/ | head -5

# Recent patterns
ls -lt .agents/patterns/ | head -5

# Recent research
ls -lt .agents/research/ | head -5

# Global patterns (cross-repo knowledge)
ls -lt ~/.claude/patterns/ 2>/dev/null | head -5
```

### Step 2: Read Relevant Files

Use the Read tool to load the most relevant artifacts based on topic.

### Step 3: Summarize for Context

Present the injected knowledge:
- Key learnings relevant to current work
- Patterns that may apply
- Recent research on related topics

### Step 4: Record Citations (Feedback Loop)

After presenting injected knowledge, record which files were injected for the feedback loop:

```bash
mkdir -p .agents/ao
# Record each injected learning file as a citation
for injected_file in <list of files that were read and presented>; do
  echo "{\"learning_file\": \"$injected_file\", \"timestamp\": \"$(date -Iseconds)\", \"session\": \"$(date +%Y-%m-%d)\"}" >> .agents/ao/citations.jsonl
done
```

Citation tracking enables the feedback loop: learnings that are frequently cited get confidence boosts during `/post-mortem`, while uncited learnings decay faster.

## Knowledge Sources

| Source | Location | Priority |
|--------|----------|----------|
| Learnings | `.agents/learnings/` | High |
| Patterns | `.agents/patterns/` | High |
| Research | `.agents/research/` | Medium |
| Retros | `.agents/retros/` | Medium |
| Global Patterns | `~/.claude/patterns/` | High |

## Decay Model

Knowledge relevance decays over time (~17%/week). More recent learnings are weighted higher.

## Key Rules

- **Runs automatically** - usually via hook
- **Context-aware** - filters by current directory/topic
- **Token-budgeted** - respects max-tokens limit
- **Recency-weighted** - newer knowledge prioritized

## Examples

### SessionStart Hook Invocation

**Hook triggers:** `session-start.sh` runs at session start

**What happens:**
1. Hook calls `ao inject --apply-decay --format markdown --max-tokens 1000`
2. CLI searches `.agents/learnings/`, `.agents/patterns/`, `.agents/research/` for relevant artifacts
3. CLI applies recency-weighted decay (~17%/week) to rank results
4. CLI outputs top-ranked knowledge as markdown within token budget
5. Agent presents injected knowledge in session context

**Result:** Prior learnings, patterns, research automatically available at session start without manual lookup.

### Manual Context Injection

**User says:** `/inject authentication` or "recall knowledge about auth"

**What happens:**
1. Agent calls `ao inject --context "authentication" --format markdown --max-tokens 1000`
2. CLI filters artifacts by topic relevance
3. Agent reads top-ranked learnings and patterns
4. Agent summarizes injected knowledge for current work
5. Agent references artifact paths for deeper exploration

**Result:** Topic-specific knowledge retrieved and summarized, enabling faster context loading than full artifact reads.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No knowledge injected | Empty knowledge pools or ao CLI unavailable | Run `/post-mortem` to seed pools; verify ao CLI installed |
| Irrelevant knowledge | Topic mismatch or stale artifacts dominate | Use `--context "<topic>"` to filter; prune stale artifacts |
| Token budget exceeded | Too many high-relevance artifacts | Reduce `--max-tokens` or increase topic specificity |
| Decay too aggressive | Recent learnings not prioritized | Check artifact modification times; verify `--apply-decay` flag |
