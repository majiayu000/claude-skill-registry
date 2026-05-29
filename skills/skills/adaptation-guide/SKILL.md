---
name: ADAPTATION_GUIDE
description: Use when adapting Droidz framework or creating custom workflows. Guide for customizing droids, skills, and commands for specific project needs.
category: framework
---

# Superpowers Skills Adaptation Guide

## Overview

Adapting 21 workflow skills from obra/superpowers for Factory.ai Droid CLI.

## Key Differences: Superpowers vs Factory.ai

| Aspect | Superpowers (Claude Code) | Factory.ai Droid CLI |
|--------|---------------------------|----------------------|
| **Skill Reference** | `superpowers:skill-name` | Just `skill-name` (auto-loaded) |
| **User Reference** | "your human partner" | "the user" |
| **Slash Commands** | `/superpowers:command` | `/command` or native Droid commands |
| **Skill Location** | `~/.superpowers/skills/` | `.factory/skills/` |
| **Plan Location** | `docs/plans/` | `.droidz/specs/` or `docs/plans/` |
| **Worktree** | Git worktrees assumed | Optional, document if needed |
| **Subagents** | `superpowers:subagent-*` | Task tool with droidz-* droids |

## Adaptation Rules

### 1. Keep Core Methodology
- ✅ **KEEP**: The process/workflow (these are excellent!)
- ✅ **KEEP**: Red flags, rationalizations, checklists
- ✅ **KEEP**: Examples (Good/Bad patterns)
- ✅ **KEEP**: The "Iron Laws" and core principles

### 2. Update References
- ❌ **REMOVE**: "superpowers:" prefix from skill references
- ✅ **UPDATE**: "REQUIRED SUB-SKILL" → "RECOMMENDED SKILL" or "SEE ALSO"
- ✅ **UPDATE**: "your human partner" → "the user"
- ✅ **UPDATE**: Slash commands to Factory.ai equivalents

### 3. Simplify Frontmatter
```yaml
---
name: skill-name
description: When to use this skill
category: workflow  # Add this for workflow skills
---
```

### 4. Update File Paths
- Plans: `docs/plans/` → `.droidz/specs/` (or keep docs/plans)
- Skills: Reference other skills without prefix
- Tests: Keep language-agnostic examples

### 5. Update Subagent References
- `superpowers:subagent-driven-development` → Use Task tool with droidz-codegen
- `superpowers:executing-plans` → Use Task tool with droidz-orchestrator
- Document Factory.ai Task tool patterns

## Skills to Adapt (21 Total)

### Testing Skills (5)
1. **test-driven-development** - TDD process (RED-GREEN-REFACTOR)
2. **systematic-debugging** - 4-phase debugging framework
3. **verification-before-completion** - Pre-completion checklist
4. **defense-in-depth** - Multi-layer validation
5. **testing-anti-patterns** - What NOT to do

### Collaboration Skills (5)
6. **brainstorming** - Design through questions
7. **writing-plans** - Detailed implementation plans
8. **executing-plans** - Following plans step-by-step
9. **requesting-code-review** - How to ask for review
10. **receiving-code-review** - How to respond to feedback

### Development Skills (5)
11. **root-cause-tracing** - Backward tracing technique
12. **subagent-driven-development** - Task-by-task with fresh agents
13. **finishing-a-development-branch** - Completing work properly
14. **using-git-worktrees** - Parallel work branches
15. **condition-based-waiting** - Replace arbitrary timeouts

### Advanced/Meta Skills (6)
16. **dispatching-parallel-agents** - Spawning multiple agents
17. **writing-skills** - Creating new skills
18. **testing-skills-with-subagents** - Validating skill quality
19. **sharing-skills** - Publishing skills
20. **using-superpowers** → **using-droidz** - How to use this system
21. **commands** - Custom command reference

## Adaptation Workflow

For each skill:
1. **Fetch** original from obra/superpowers
2. **Keep** core methodology (process, principles, examples)
3. **Update** Factory.ai references (no "superpowers:" prefix)
4. **Simplify** frontmatter, update paths
5. **Test** that references work (skill → skill not superpowers:skill)
6. **Save** to `.factory/skills/[name].md`

## Quality Standards

Each adapted skill must:
- ✅ Preserve the original methodology and quality
- ✅ Remove superpowers-specific references
- ✅ Update to Factory.ai Droid CLI patterns
- ✅ Keep all examples, checklists, red flags
- ✅ Maintain 800+ lines (these are already comprehensive!)
- ✅ Add `category: workflow` to distinguish from framework skills

## Success Criteria

- ✅ All 21 skills adapted
- ✅ No broken references (superpowers: removed)
- ✅ Factory.ai Task tool patterns documented
- ✅ Skills work with Factory.ai auto-loading
- ✅ Total skill count: 42 (21 framework + 21 workflow)
