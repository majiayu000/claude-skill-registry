---
name: documentation-sync
description: Use when creating or modifying skills - enforces documentation consistency across 6 system files to maintain alignment between Cursor and Claude Code agents
---

# Documentation Sync

## Purpose

Ensure all system documentation remains consistent when skills, workflows, quality gates, or context assembly patterns are created or modified. This quality gate enforces updates across 6 critical documentation files that support both Cursor (rules-based) and Claude Code (skills-based) agents.

## The Iron Law

**NO SKILL COMPLETE WITHOUT DOCUMENTATION SYNC**

This applies to:
- New skills ✓
- Modified skills ✓
- New workflows ✓
- Modified workflows ✓
- New quality gates ✓
- New context assembly patterns ✓
- Any change affecting system capabilities ✓

No exceptions. No rationalizations. Documentation sync is mandatory.

## When to Use This Skill

Activate when:
- Creating any new skill (meta, quality-gate, context-assembly, workflow)
- Modifying existing skill that changes capabilities or interfaces
- Adding new slash commands that invoke skills
- Changing skill categories or organizational structure
- The `create-skill` meta-skill is being executed
- The `refine-workflow` meta-skill extracts new skills

**When NOT to use:**
- Minor typo fixes that don't affect functionality
- Internal comment updates
- Refactoring that doesn't change external interface

## The 6 Documentation Files

### 1. `.claude/CLAUDE.md` (Cursor-specific, primary)
**Purpose**: Instructions for Cursor AI agents
**Update when**: Any skill/workflow change
**Key sections**:
- Skills System (line ~65-136)
- Commands Index (line ~138-202)

### 2. `CLAUDE.md` (Root-level, Claude Code-specific)
**Purpose**: Instructions for Claude Code agents
**Update when**: Any skill/workflow change
**Key sections**:
- Skills System (line ~9-46)
- Core Commands (line ~48-133)

### 3. `CURSOR-PM-SYSTEM.md` (Architecture)
**Purpose**: System architecture documentation
**Update when**: New workflow categories, major capability additions
**Key sections**:
- Rules/Workflow descriptions (line ~27-38)
- Key Workflows (line ~40-104)

### 4. `AGENTS.md` (Agent capabilities)
**Purpose**: Agent/mode capability reference
**Update when**: New user-facing capabilities
**Key sections**:
- Agent Capabilities (line ~13-20)
- Example Prompts (line ~30-54)
- Task Routing (line ~187-206)
- Quality Standards (line ~210-234)

### 5. `README.md` (Main entry)
**Purpose**: User-facing documentation and getting started guide
**Update when**: New workflows, capabilities, or major features
**Key sections**:
- Agent descriptions (line ~14-37)
- Key Workflows (line ~56-94)
- Example Prompts (line ~147-168)
- Documentation links (line ~170-177)

### 6. `.cursor/rules/*.mdc` (Cursor rules)
**Purpose**: Cursor-specific workflow definitions
**Update when**: Creating/modifying workflows in specific domains
**Files**:
- `core-system.mdc` — System-wide behavior
- `product-workflows.mdc` — Product management workflows
- `metrics-workflows.mdc` — Metrics analysis workflows
- `strategy-workflows.mdc` — Strategy session workflows
- `research-workflows.mdc` — Research processing workflows
- `quality-gates.mdc` — Quality gate definitions
- `context-assembly.mdc` — Context assembly patterns

## Documentation Update Matrix

### For Meta Skills
- ✓ `.claude/CLAUDE.md` — Add to Meta Skills list
- ✓ `CLAUDE.md` — Add to Meta Skills category
- ✓ `.cursor/rules/quality-gates.mdc` — If it's a quality gate
- ⚬ `CURSOR-PM-SYSTEM.md` — Only if architecture-significant
- ⚬ `AGENTS.md` — Only if user-facing
- ⚬ `README.md` — Only if user needs to know

### For Quality Gates
- ✓ `.claude/CLAUDE.md` — Add to Quality Gates list
- ✓ `CLAUDE.md` — Add to Quality Gates category
- ✓ `.cursor/rules/quality-gates.mdc` — Add full description
- ✓ `AGENTS.md` — Add to Quality Standards section
- ⚬ `CURSOR-PM-SYSTEM.md` — Only if architecture-significant
- ⚬ `README.md` — Brief mention in quality standards

### For Context Assembly Skills
- ✓ `.claude/CLAUDE.md` — Add to Context Assembly list
- ✓ `CLAUDE.md` — Add to Context Assembly category
- ✓ `.cursor/rules/context-assembly.mdc` — Add full description
- ⚬ `CURSOR-PM-SYSTEM.md` — Only if architecture-significant
- ⚬ `AGENTS.md` — Only if user-facing
- ⚬ `README.md` — Only if user needs to know

### For Workflow Skills
- ✓ `.claude/CLAUDE.md` — Add to Workflows list and Commands Index
- ✓ `CLAUDE.md` — Add to Workflows category and Core Commands
- ✓ `.cursor/rules/{domain}-workflows.mdc` — Add full workflow description
- ✓ `CURSOR-PM-SYSTEM.md` — Add to Key Workflows section
- ✓ `AGENTS.md` — Add to relevant agent's Capabilities and Example Prompts
- ✓ `README.md` — Add to agent description, workflow diagram, example prompts

### For Metrics Analysis Skills
- ✓ All workflow documentation (as above)
- ✓ `.cursor/rules/metrics-workflows.mdc` — Complete workflow documentation
- ✓ Special attention to integration with existing metrics workflows

## Validation Procedure

### Step 1: Identify Skill Type
Determine which category applies: meta, quality-gate, context-assembly, or workflow.

### Step 2: Apply Documentation Matrix
Use the matrix above to determine which files require updates.

### Step 3: Update Each Required File
For each file marked with ✓:
1. Read the file to understand current structure
2. Identify the correct section for the update
3. Add skill name, description, and relevant details
4. Maintain consistent formatting with existing entries
5. Verify line numbers match plan expectations

### Step 4: Cross-Reference Validation
After updating all files, verify:
- [ ] Skill name appears consistently across all files
- [ ] Description is consistent (or appropriately adapted per context)
- [ ] All files reference the same skill location
- [ ] Slash command mappings are consistent (if applicable)
- [ ] Example prompts are aligned (for workflows)
- [ ] No broken cross-references

### Step 5: Completeness Check
Ask these questions:
- If a user reads only `.claude/CLAUDE.md`, would they know this skill exists?
- If a user reads only `CLAUDE.md`, would they know how to use it?
- If a user reads only `README.md`, would they discover the capability?
- If a user reads `AGENTS.md`, would they know which agent to use?
- If a Cursor agent loads the relevant `.mdc` file, would it have complete instructions?
- Is `CURSOR-PM-SYSTEM.md` accurately describing the system architecture?

All must be "yes" to pass.

## Common Rationalizations (ALL REJECTED)

| Rationalization | Reality |
|-----------------|---------|
| "This skill is too minor to document" | All skills must be documented for discoverability |
| "I'll update docs later" | Documentation sync happens NOW, not later |
| "Only one file needs updating" | Matrix determines requirements, not convenience |
| "Users won't use this directly" | System documentation serves multiple purposes |
| "The description is obvious" | Consistency matters more than obviousness |
| "I'm just fixing a bug" | If behavior changes, documentation updates |

## Anti-Rationalization Blocks

**Time Pressure:**
"I know you're in a hurry, but documentation sync is not optional. The system depends on consistency between Cursor and Claude Code agents. Taking 10 extra minutes now prevents hours of confusion later."

**Sunk Cost:**
"I know you've already written the skill, but documentation is part of skill completion. An undocumented skill is an incomplete skill."

**Authority:**
"Even if this seems like bureaucratic overhead, the Iron Law applies to everyone: NO SKILL COMPLETE WITHOUT DOCUMENTATION SYNC."

**Scope Creep:**
"Documenting feels like extra work beyond the original task, but it's actually a core requirement of the create-skill workflow. Not optional."

## Success Criteria

Documentation sync passes when:
- All required files identified via matrix have been updated
- Skill name appears consistently across all files
- Descriptions are contextually appropriate for each file
- Cross-references are valid and non-broken
- Example prompts align (for user-facing workflows)
- Completeness check questions all answered "yes"
- No rationalization attempted or accepted

## Related Skills

- **create-skill**: Must invoke documentation-sync before completion
- **refine-workflow**: Must invoke documentation-sync when extracting skills
- **skill-discovery**: Benefits from accurate documentation

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Updating only 1-2 files | Apply full documentation matrix |
| Inconsistent skill names | Use exact same name across all files |
| Skipping `.mdc` files | Cursor agents need these files updated |
| Forgetting example prompts | User-facing workflows need examples |
| Not checking line numbers | Verify updates in correct sections |
| Skipping completeness check | Run all 6 validation questions |

