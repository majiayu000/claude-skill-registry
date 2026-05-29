---
name: task-memory-consolidation
description: Parse memory.yaml and consolidate recurring patterns into skills. Use when memory.yaml grows large, when patterns recur 3+ times, or during RSID Ideate stage. Automates the memory-to-skill pipeline.
---

# Memory Consolidation

**Turn accumulated learnings into durable skill improvements.**

## When to Invoke

- During **RSID Ideate** stage
- When `memory.yaml` exceeds ~10 tasks
- When you notice repeated learnings across tasks
- Periodically after several merge cycles

## The Consolidation Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. PARSE: Read memory.yaml, extract all learnings                   │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 2. GROUP: Cluster similar learnings by topic/domain                 │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 3. THRESHOLD: Identify clusters with 3+ learnings                   │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 4. MAP: Determine which skill each cluster should update            │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 5. GENERATE: Create skill updates (new sections, anti-patterns)     │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 6. ARCHIVE: Move consolidated memories to memory-archive.yaml       │
└─────────────────────────────────────────────────────────────────────┘
```

## Step 1: Parse memory.yaml

Read `instructions/improvements/memory.yaml` and extract structured data:

```yaml
# Expected structure
memories:
  - task: string          # Task identifier
    date: string          # YYYY-MM-DD
    context: string       # Background
    learnings:
      - type: string      # command-correction|q-and-a|misconception|pattern|insight
        summary: string   # One-line
        detail: string    # Full explanation
```

**Extract into flat list:**

```typescript
interface Learning {
  task: string;
  date: string;
  type: 'command-correction' | 'q-and-a' | 'misconception' | 'pattern' | 'insight';
  summary: string;
  detail: string;
  context: string;  // From parent task
}
```

## Step 2: Group by Similarity

Cluster learnings using these heuristics:

### Keyword Matching

Look for shared keywords in summaries:

| Keywords | Likely Domain |
|----------|---------------|
| `sandbox`, `permission`, `operation not permitted` | Environment/Sandbox |
| `contract`, `port`, `deps`, `interface` | Architecture/Coding-patterns |
| `PR`, `merge`, `commit`, `branch` | Git/Workflow |
| `skill`, `SKILL.md`, `description` | Skill-writing |
| `RSID`, `loop`, `memory`, `reflection` | Meta/RSID |

### Type-Based Grouping

| Type | Typical Destination |
|------|---------------------|
| `command-correction` | coding-loop (commands section) or specific skill |
| `q-and-a` | Relevant skill's FAQ or quick reference |
| `misconception` | Anti-patterns section of relevant skill |
| `pattern` | Core patterns of relevant skill |
| `insight` | Context or principles section |

## Step 3: Apply Threshold

**The Rule**: 3+ similar learnings → consolidation candidate.

```
For each cluster:
  If learnings.length >= 3:
    → Ready for consolidation
  Else if learnings.length == 2:
    → Watch list (note but don't consolidate yet)
  Else:
    → Keep in memory.yaml, not yet a pattern
```

## Step 4: Map to Skills

### Skill Mapping Table

| Topic/Keywords | Target Skill | Section to Update |
|----------------|--------------|-------------------|
| Sandbox, permissions, heredocs | `devcontainer-sandboxing` | Workarounds |
| Contracts, ports, deps, architecture | `coding-patterns` | Core Principles or Anti-Patterns |
| Plans, alternatives, experts | `plan-writing` | Self-Check or Anti-Patterns |
| Commits, branches, git | `effective-git` | Phase guidance |
| PRs, merging, review workflow | `pull-request` | PR workflow |
| RSID, loops, reflection | `rsid` | Loop guidance |
| Skills, descriptions, triggers | `writing-claude-skills` | Best Practices |
| Memory, consolidation | `memory-consolidation` | This skill |

### Decision Tree

```
Is it about how code should be structured?
├── YES → coding-patterns
└── NO → Is it about git/commits/PRs?
    ├── YES → Is it about commit messages?
    │   ├── YES → effective-git
    │   └── NO → pull-request or coding-loop
    └── NO → Is it about environment/sandbox?
        ├── YES → devcontainer-sandboxing
        └── NO → Is it about planning?
            ├── YES → plan-writing
            └── NO → Is it about skills themselves?
                ├── YES → writing-claude-skills
                └── NO → rsid (meta-level)
```

## Step 5: Generate Skill Updates

### For Patterns → Add to Core Principles

```markdown
### [Pattern Number]. [Pattern Name]

**The Problem**: [What goes wrong without this pattern]

**The Pattern**:
[Extracted and generalized from the learnings]

**Examples**:
[Concrete examples from the memory entries]
```

### For Misconceptions → Add to Anti-Patterns

```markdown
### The "[Misconception Name]" Anti-Pattern

**Wrong:**
> [The incorrect belief, quoted from memories]

**Right:**
> [The correction, synthesized from learnings]

**Why it matters:**
[Consequences of the misconception]
```

### For Command-Corrections → Add to Commands/Workarounds

```markdown
### [Command/Approach]

**Fails with:** `[error message]`

**Use instead:**
```bash
[corrected command]
```

**Why:** [Root cause explanation]
```

### For Q&A → Add to Quick Reference

```markdown
| Question | Answer |
|----------|--------|
| [Q from memory] | [A from memory] |
```

### For Insights → Add to Context/Principles

```markdown
**Key Insight:** [Insight summary]

[Detailed explanation from memory, generalized]
```

## Step 6: Archive Consolidated Memories

After updating skills, move consolidated memories to `memory-archive.yaml`:

```yaml
# instructions/improvements/memory-archive.yaml
archived:
  - consolidated_date: "2024-12-15"
    consolidated_into: "coding-patterns"
    pattern_name: "No Fake Defaults"
    memories:
      - task: "add-rsid-skill"
        date: "2024-12-15"
        type: "pattern"
        summary: "No fake defaults for required dependencies"
        # ... full original entry

  - consolidated_date: "2024-12-15"
    consolidated_into: "devcontainer-sandboxing"
    pattern_name: "Heredoc Sandbox Restriction"
    memories:
      - task: "add-plan-writing-skill"
        # ... full original entry
```

**Archive Entry Structure:**

```yaml
archived:
  - consolidated_date: string    # When consolidation happened
    consolidated_into: string    # Which skill was updated
    pattern_name: string         # Name given to the pattern
    memories: Learning[]         # Original memory entries
```

## Consolidation Checklist

Before consolidating, verify:

- [ ] At least 3 similar learnings identified
- [ ] Target skill clearly identified
- [ ] Section for update determined (new or existing)
- [ ] Pattern generalized (not just copied verbatim)
- [ ] Examples included from original learnings
- [ ] Archive entry prepared with full original data

## Example Consolidation

### Input: 3 Related Learnings

```yaml
# From memory.yaml
- task: "add-plan-writing-skill"
  learnings:
    - type: "command-correction"
      summary: "Heredocs fail in sandbox"
      detail: "git commit with heredoc fails..."

- task: "feature-x"
  learnings:
    - type: "command-correction"
      summary: "Temp files blocked in sandbox"
      detail: "mktemp fails with operation not permitted..."

- task: "feature-y"
  learnings:
    - type: "insight"
      summary: "Sandbox restricts /tmp writes"
      detail: "Only /tmp/claude/ is writable..."
```

### Output: Skill Update

**Target**: `devcontainer-sandboxing` or `coding-loop`

```markdown
### Sandbox File System Restrictions

The Claude Code sandbox restricts file system writes:

| Location | Writable | Notes |
|----------|----------|-------|
| `/tmp/` | NO | Use `/tmp/claude/` instead |
| `/tmp/claude/` | YES | TMPDIR is set here |
| Heredocs | NO | Can't create temp files for here-documents |

**Workarounds:**

1. **Heredocs**: Use inline multiline strings instead
   ```bash
   # Instead of: git commit -m "$(cat <<'EOF' ... EOF)"
   git commit -m "message line 1

   line 2"
   ```

2. **Temp files**: Use `/tmp/claude/` or set TMPDIR explicitly
   ```bash
   export TMPDIR=/tmp/claude
   mktemp  # Now works
   ```
```

### Output: Archive Entry

```yaml
archived:
  - consolidated_date: "2024-12-15"
    consolidated_into: "coding-loop"
    pattern_name: "Sandbox File System Restrictions"
    section_added: "## Sandbox File System Restrictions"
    memories:
      - task: "add-plan-writing-skill"
        type: "command-correction"
        summary: "Heredocs fail in sandbox"
        # ... full entry
      - task: "feature-x"
        type: "command-correction"
        summary: "Temp files blocked in sandbox"
        # ... full entry
      - task: "feature-y"
        type: "insight"
        summary: "Sandbox restricts /tmp writes"
        # ... full entry
```

## Integration with RSID

This skill is invoked during the **Ideate** stage of RSID:

```
USER-DRIVEN:    Listen → Execute → Reflect
                                      ↓ (memories recorded)
AUTONOMOUS:     Ideate ← INVOKE memory-consolidation HERE → Execute → Reflect
                (patterns consolidated, skills updated)
```

**When Ideate finds consolidation candidates:**

1. Invoke this skill
2. Follow the consolidation pipeline
3. Create PR with skill updates + archive updates
4. Merge PR
5. Continue to Execute with next task

## Quick Reference

```
Parse → Group → Threshold (3+) → Map → Generate → Archive
```

| Step | Action |
|------|--------|
| Parse | Read memory.yaml, extract flat learning list |
| Group | Cluster by keywords and type |
| Threshold | 3+ similar → consolidate |
| Map | Determine target skill and section |
| Generate | Create update following templates |
| Archive | Move to memory-archive.yaml |
