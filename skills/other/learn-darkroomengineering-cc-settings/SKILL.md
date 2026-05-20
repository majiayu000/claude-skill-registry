---
name: learn
description: |
  Persistent memory system for storing and recalling learnings across sessions.

  AUTO-INVOKE THIS SKILL when you:
  - Fix a non-obvious bug (store as "bug")
  - Discover a useful code pattern (store as "pattern")
  - Encounter a gotcha or edge case (store as "gotcha")
  - Find a useful tool/library feature (store as "tool")
  - Make a performance optimization (store as "perf")
  - Discover configuration that solved a problem (store as "config")
  - Make an architecture decision with rationale (store as "arch")
  - Find a useful testing insight (store as "test")

  Also invoke when user says: "remember this", "store learning", "recall learnings",
  "what did we learn", "lessons learned"
---

# Persistent Learning System

Store learnings that survive across Claude Code sessions. **Proactively store learnings when you discover something valuable** - don't wait for the user to ask.

## Auto-Store Triggers

Store a learning AUTOMATICALLY when:
- You fix a bug that wasn't immediately obvious
- You discover why something was breaking
- You find a workaround for a limitation
- You make a decision that future sessions should know about
- You encounter behavior that was unexpected
- You find a pattern that works well in this codebase

## Actions

### Store a learning
```bash
bash ~/.claude/scripts/learning.sh store "<category>" "<learning>" "[context]"
```

**Categories:** `bug`, `pattern`, `gotcha`, `tool`, `perf`, `config`, `arch`, `test`

**Examples:**
```bash
# After fixing a hydration error
bash ~/.claude/scripts/learning.sh store "bug" "useAuth hook causes hydration mismatch - wrap in dynamic import with ssr:false"

# After discovering a pattern
bash ~/.claude/scripts/learning.sh store "pattern" "Always use Image wrapper from @/components/image, not next/image directly"

# After hitting a gotcha
bash ~/.claude/scripts/learning.sh store "gotcha" "Biome ignores .mdx files by default - add to biome.json includes"

# After a tool discovery
bash ~/.claude/scripts/learning.sh store "tool" "Use 'bun --bun' flag to enable native Bun APIs in scripts"
```

### Recall learnings
```bash
bash ~/.claude/scripts/learning.sh recall [filter] [value]
```

**Filters:**
- `all` - All learnings for current project
- `all-projects` - List all projects with learnings
- `category <cat>` - Filter by category
- `search <keyword>` - Search in learning text
- `recent <n>` - Most recent n learnings

### Delete a learning
```bash
bash ~/.claude/scripts/learning.sh delete <id>
```

## Storage

Learnings are stored per-project at `~/.claude/learnings/<project>/learnings.json`

## Best Practices

1. **Be specific** - Include the actual fix, not just "fixed the bug"
2. **Include context** - What file, what component, what was the symptom
3. **Store immediately** - Don't wait until end of session
4. **Categorize correctly** - Helps with recall later
