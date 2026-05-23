---
name: memory-sync
description: Memory Sync Skill
---

# Memory Sync Skill

How to manually sync learnings to memory systems after tasks.

## Dual Memory Architecture

Ariff uses two complementary memory systems:
- **mem0-memory-mcp** - AI-native semantic memory for quick recall
- **obsidian-memory** - Structured vault for long-term knowledge

## Manual Sync Commands

### Quick Save to mem0
```
Use mcp__mem0-memory-mcp__add_memory to store:
- Task context and solution
- Key learnings and gotchas
- Useful commands discovered
```

### Save to Obsidian
```
Use mcp__obsidian-memory__create_note with:
- path: "tasks/YYYY-MM-DD-task-slug.md"
- content: Structured task notes
```

## Memory Entry Template

```markdown
## Task: [Brief Title]
Date: [YYYY-MM-DD]
Device: [hostname]

### Problem
[What was the issue/request]

### Solution
[How it was resolved]

### Key Learnings
- [Learning 1]
- [Learning 2]

### Related
- Previous tasks: [links]
- Documentation: [links]
```

## Creating Agent Instructions

When a mistake or pattern should be avoided in future:

1. Create instruction file at:
   ```
   Ariff-code-config/instructions/[category]-[topic].instructions.md
   ```

2. Use format:
   ```markdown
   ---
   description: [What this instruction prevents/ensures]
   applyTo: [glob pattern like **/*.py or **/canvas/**]
   ---

   # [Rule Title]

   ## Context
   [When this applies]

   ## Rule
   [What to do/not do]

   ## Example
   [Good vs bad example]
   ```

3. Add to 00_INSTRUCTIONS_INDEX.md if significant

## Reconciliation

If memories seem out of sync:
1. Query both systems for topic
2. Compare entries
3. Update older system with newer info
4. Remove duplicates with less detail

## When to Save

Save memory when:
- ✅ Task completed successfully
- ✅ Discovered non-obvious solution
- ✅ Made mistake worth remembering
- ✅ Found useful tool/command
- ✅ Clarified user preference

Skip saving when:
- ❌ Trivial task (simple file edit)
- ❌ Already documented elsewhere
- ❌ One-off unique situation
