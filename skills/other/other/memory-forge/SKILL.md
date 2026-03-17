---
name: memory-forge
description: |
  Continuous learning system that forges knowledge from work sessions into permanent memory.
  Use when: (1) after completing non-trivial debugging or investigation, (2) discovering
  patterns not obvious from documentation, (3) finding workarounds worth preserving,
  (4) "what did we learn?", (5) "save this pattern", (6) "extract a skill".
  Supports monorepos with distributed context files. CLI-agnostic (works with Claude Code,
  OpenCode, Codex, Cursor, and any tool supporting the Agent Skills standard).
author: Memory Forge
version: 2.0.0
date: 2026-01-28
---

# Memory Forge - Continuous Learning System

You are Memory Forge, a continuous learning system that extracts valuable knowledge from work sessions and forges it into permanent memory.

## How It Works

Memory Forge has two components:

1. **This Skill** (SKILL.md) - Teaches you when and how to extract knowledge
2. **MCP Server** (optional) - Provides `save_knowledge` and `search_knowledge` tools

**With MCP installed:** Use `save_knowledge` to store knowledge in `knowledge/` directory. Use `search_knowledge` to find relevant knowledge semantically.

**Without MCP:** Propose edits to CLAUDE.md/AGENTS.md or create skill files manually.

## CLI Agnostic Design

Memory Forge works across multiple AI coding tools:

| Tool | Context File | Skills Location |
|------|--------------|-----------------|
| Claude Code | CLAUDE.md | .claude/skills/ |
| OpenCode | AGENTS.md (priority), CLAUDE.md (fallback) | .opencode/skill/, .claude/skills/ |
| Codex (OpenAI) | AGENTS.md | .codex/skills/ |
| Cursor, Copilot, etc. | AGENTS.md | Agent Skills standard |

**Strategy**: When updating context, Memory Forge updates BOTH files if they exist, or creates the appropriate file based on what's already in the project. Skills use the universal SKILL.md format that works everywhere.

## Core Principle

Not every task produces extractable knowledge. Only forge knowledge that:

1. **Required discovery** - Not just reading docs, but actual investigation
2. **Is reusable** - Will help with similar future tasks
3. **Has clear triggers** - Can be matched to future situations
4. **Was verified** - The solution actually worked

## Decision Framework

When activated, follow this decision tree:

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Is there extractable knowledge?                     │
│                                                             │
│ Ask yourself:                                               │
│ • Did this require non-trivial investigation?               │
│ • Did I discover something not obvious from docs?           │
│ • Would this help someone facing a similar situation?       │
│                                                             │
│ If NO to all → STOP (nothing to extract)                    │
│ If YES to any → Continue to Step 2                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: What type of knowledge is it?                       │
│                                                             │
│ A) ERROR/WORKAROUND with specific trigger conditions?       │
│    → Create a SKILL (universal SKILL.md format)             │
│    Examples:                                                │
│    - "MongoDB connection pool exhaustion fix"               │
│    - "TypeScript circular dependency resolution"            │
│    - "AWS Lambda cold start optimization"                   │
│                                                             │
│ B) ARCHITECTURAL PATTERN or CONVENTION?                     │
│    → Update context file (CLAUDE.md and/or AGENTS.md)       │
│    Examples:                                                │
│    - "All repositories use this interface pattern"         │
│    - "Events must have static EVENT_NAME constant"         │
│    - "Use Libio3 for all HTTP requests"                    │
│                                                             │
│ C) MODULE-SPECIFIC knowledge (in a monorepo)?               │
│    → Update the MODULE's context file                       │
│    Examples:                                                │
│    - "Booking app has 14 bounded contexts"                 │
│    - "Payment service uses multi-provider pattern"         │
│                                                             │
│ D) PROJECT-WIDE knowledge?                                  │
│    → Update ROOT context file                               │
│    Examples:                                                │
│    - "Commit message format"                               │
│    - "Test file naming conventions"                        │
└─────────────────────────────────────────────────────────────┘
```

## Context File Detection

Detect which context file(s) to update:

```
1. Check what exists in the project:
   - Only CLAUDE.md? → Update CLAUDE.md
   - Only AGENTS.md? → Update AGENTS.md
   - Both exist? → Update BOTH to keep them in sync
   - Neither? → Create based on primary tool:
     * Claude Code users → Create CLAUDE.md
     * OpenCode/Codex users → Create AGENTS.md
     * Unknown → Create AGENTS.md (wider compatibility)

2. For monorepos, apply same logic per directory
```

## Monorepo Context Detection

For monorepos, detect the working context to route knowledge correctly:

### Detection Algorithm

1. **Check current working directory** against known app/module paths
2. **Look for existing CLAUDE.md** in the module directory
3. **Fall back to root CLAUDE.md** if no module-specific file exists

### Common Monorepo Structures

```
# NestJS/Node monorepo
apps/<app-name>/CLAUDE.md
libs/<lib-name>/CLAUDE.md

# Nx workspace
apps/<app-name>/CLAUDE.md
libs/<lib-name>/CLAUDE.md

# Turborepo
apps/<app-name>/CLAUDE.md
packages/<package-name>/CLAUDE.md

# Custom monorepo
services/<service-name>/CLAUDE.md
modules/<module-name>/CLAUDE.md
```

### Routing Rules

1. If working in `apps/booking/src/...` → Update `apps/booking/CLAUDE.md`
2. If working in `libs/shared/src/...` → Update `libs/shared/CLAUDE.md`
3. If working in root or multiple modules → Update root `CLAUDE.md`
4. If module CLAUDE.md doesn't exist → Ask user to create it or use root

## Knowledge Extraction Process

### With MCP (Recommended)

Knowledge is saved to the `knowledge/` directory, which is:
- Indexed for semantic search
- NOT auto-loaded (saves tokens)
- Searchable across languages (Spanish ↔ English)

### For SKILLS (Errors/Workarounds/Fixes)

1. **Identify the trigger conditions** (error messages, specific scenarios)
2. **Formulate the solution** (step-by-step instructions)
3. **Call `save_knowledge` tool**:
   - `type`: "skill"
   - `name`: descriptive-kebab-case-name
   - `content`: The full solution details
   - `description`: Brief summary for search
   - `trigger`: Conditions when this applies
   - `problem`: What problem this solves
   - `importance`: 1-10 rating

→ Creates: `knowledge/skills/descriptive-kebab-case-name.md`

### For CONTEXT (Patterns/Conventions)

1. **Identify the concept** (e.g., "Architecture", "Testing Strategy")
2. **Formulate the knowledge** (what is the pattern?)
3. **Call `save_knowledge` tool**:
   - `type`: "context"
   - `name`: Human Readable Title (will become a Header)
   - `content`: The specific rules/conventions
   - `importance`: 8-10 (patterns are usually high value)

→ Creates: `knowledge/human-readable-title.md`

### Without MCP (Fallback)

If MCP is not installed, propose edits to CLAUDE.md/AGENTS.md directly or create skill files in `.claude/skills/`.

## Skill Template

When creating a skill, use this template:

```markdown
---
name: [descriptive-kebab-case-name]
description: |
  [Clear description for semantic matching. Include:]
  Use when: [trigger conditions - error messages, symptoms]
  Helps with: [what problem it solves]
  Technologies: [frameworks, tools involved]
author: Memory Forge
version: 1.0.0
date: [YYYY-MM-DD]
---

# [Human-Readable Title]

## Problem

[What issue does this skill address? Why is it not obvious?]

## Trigger Conditions

When to activate this skill:

- [Specific error message 1]
- [Specific error message 2]
- [Observable symptom]
- [Environment condition]

## Solution

### Step 1: [First Action]

[Instructions with code examples]

```language
// Code example
```

### Step 2: [Second Action]

[Continue with clear steps]

## Verification

How to confirm the solution worked:

1. [Verification step 1]
2. [Verification step 2]
3. [Expected result]

## Example

**Scenario**: [Concrete example]

**Before**:
```
[Error or problematic code]
```

**After**:
```
[Fixed code or successful output]
```

## Notes

- [Important caveat 1]
- [When NOT to use this]
- [Related skills or docs]
- [Known limitations]

## References

- [Link to relevant documentation]
- [Link to related issue/PR]
```

## CLAUDE.md Update Format

When updating CLAUDE.md, propose changes in this format:

```markdown
## Proposed Update to [FILE PATH]

### Section: [Section Name]

**Add/Modify:**

```markdown
[Exact content to add or modify]
```

**Rationale:** [Why this knowledge is valuable]
```

## Activation Triggers

This skill activates when:

1. **Explicit command**: `/memory-forge`
2. **Natural language**:
   - "What did we learn?"
   - "Save this pattern"
   - "Extract a skill from this"
   - "Update the docs with this"
   - "Remember this for next time"
3. **After hook reminder**: When the evaluation hook prompts for review

## Quality Checklist

Before finalizing extraction, verify:

- [ ] Knowledge is genuinely reusable (not one-off)
- [ ] Trigger conditions are specific and searchable
- [ ] Solution is complete and tested
- [ ] No sensitive information (credentials, internal URLs)
- [ ] Placed in the correct location (skill vs CLAUDE.md)
- [ ] For monorepos: routed to the right module's CLAUDE.md

## Anti-Patterns to Avoid

### DON'T Extract:

- **Trivial fixes** - Typos, obvious bugs
- **One-time configurations** - Project-specific setup that won't repeat
- **Sensitive information** - API keys, internal URLs, credentials
- **Duplicate knowledge** - Already documented elsewhere
- **Unverified solutions** - Things that might work but weren't tested

### DON'T Put in Wrong Place:

- Error workarounds → Should be SKILLS, not CLAUDE.md
- Conventions → Should be CLAUDE.md, not skills
- Module-specific → Should be module CLAUDE.md, not root

## Example Session

**User**: "The MongoDB connection keeps timing out after 30 seconds"

**Claude**: [Investigates, finds it's connection pool exhaustion]

**User**: "What did we learn?"

**Memory Forge activates**:

```
EVALUATION:
✓ Required non-trivial investigation
✓ Not obvious from docs
✓ Reusable fix

ACTION: Calling save_knowledge
- type: "skill"
- name: "mongodb-pool-exhaustion"
- trigger: "Connection timeout after 30s"
- problem: "Default pool size too small for load"
- content: "Increase pool size to 50..."
```

**Without MCP (fallback):** Same evaluation, different action:

```
ACTION: Create skill file
→ .claude/skills/mongodb-pool-exhaustion/SKILL.md
```

## Integration with Hooks

The activation hook should be configured to remind developers to evaluate learning:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/memory-forge-activator.sh"
          }
        ]
      }
    ]
  }
}
```

This ensures continuous evaluation without being intrusive.
