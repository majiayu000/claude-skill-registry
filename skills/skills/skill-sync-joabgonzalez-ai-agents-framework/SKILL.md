---
name: skill-sync
description: "Maintains synchronization across model directories after modifying skills, agents, or prompts. Ensures consistency between AGENTS.md, CLAUDE.md, GEMINI.md. Trigger: After creating or modifying any skill, agent, or prompt to synchronize changes across all model directories."
input: "modification type (skill/agent/prompt), affected files, validation queries | string"
output: "sync instructions, validation checklist, affected paths, manual steps | markdown"
---

# Skill Sync

## Overview

This skill guides the agent to maintain proper synchronization across all model directories after any modifications to skills, agents, or prompts. It ensures consistency between different model-specific files (AGENTS.md, CLAUDE.md, GEMINI.md) and provides comprehensive validation checklists to verify that all installations remain synchronized.

## Objective

Ensure that any modifications to skills, agents, or prompts are properly propagated to all relevant model directories (.github/, .claude/, .codex/, .gemini/). The agent must understand when synchronization is needed, what files require updates, and how to validate that synchronization is complete and correct.

This skill works in tandem with the automated `sync.sh` script: the agent uses this skill for manual, surgical updates during development, while users can run `make sync` for bulk automated synchronization.

---

## When Synchronization Is Needed

Synchronization is required after:

1. **Modifying a skill**: Updating SKILL.md content, frontmatter, conventions, examples, or dependencies
2. **Creating a new skill**: Adding a new skill directory and SKILL.md file
3. **Deleting a skill**: Removing a skill from the skills/ directory
4. **Modifying AGENTS.md**: Changing skills list, description, workflows, or any frontmatter
5. **Modifying prompts**: Updating or creating context prompts in prompts/ directory
6. **Changing meta-skills**: Modifications to skill-creation, agent-creation, prompt-creation, process-documentation, critical-partner, conventions, or a11y

---

## Synchronization Targets

### Model Directories to Update

When modifying skills, update these directories if they exist:

- `.github/skills/` (GitHub Copilot)
- `.claude/skills/` (Claude)
- `.codex/skills/` (Codex)
- `.gemini/skills/` (Gemini)

### Model-Specific Files to Update

When modifying AGENTS.md, update these files if they exist:

- `AGENTS.md` (root)
- `CLAUDE.md` (for Claude Desktop)
- `GEMINI.md` (for Google AI Studio)

**Note**: GitHub Copilot and Codex use only AGENTS.md and do not require separate files.

---

## Synchronization Workflows

### Workflow 1: After Modifying a Skill

1. Identify the modified skill (e.g., `skills/typescript/SKILL.md`)
2. Check which model directories exist (.github, .claude, .codex, .gemini)
3. For each existing model directory:
   - Remove the old skill directory
   - Copy the updated skill directory from `skills/`
4. Validate that all copies are identical
5. Suggest running `make sync` if multiple skills were modified

**Example**:

```bash
# Manual sync for single skill modification
rm -rf .github/skills/typescript
rm -rf .claude/skills/typescript
rm -rf .codex/skills/typescript
rm -rf .gemini/skills/typescript

cp -R skills/typescript .github/skills/
cp -R skills/typescript .claude/skills/
cp -R skills/typescript .codex/skills/
cp -R skills/typescript .gemini/skills/

# Or use automated sync
make sync
```

### Workflow 2: After Creating a New Skill

1. Verify the new skill follows skill-creation standards
2. Check which model directories exist
3. For each existing model directory:
   - Copy the new skill directory from `skills/`
4. If the skill is a meta-skill, update META_SKILLS in install.sh
5. Update README.md Skills Table with the new skill entry
6. Validate that all installations include the new skill

### Workflow 3: After Modifying AGENTS.md

1. Identify changes in frontmatter (name, description, skills list)
2. Update AGENTS.md (always exists)
3. If CLAUDE.md exists:
   - Update the source comment at the top
   - Update the content to match AGENTS.md
4. If GEMINI.md exists:
   - Update the source comment at the top
   - Update the content to match AGENTS.md
5. Validate consistency across all three files

**Example CLAUDE.md structure**:

```markdown
<!-- This file is generated from AGENTS.md -->
<!-- Do not edit manually. Update AGENTS.md and run sync -->

[Content identical to AGENTS.md]
```

### Workflow 4: After Modifying Prompts

1. Identify the modified prompt in `prompts/`
2. Prompts are typically not copied to model directories
3. Verify prompt follows prompt-creation standards
4. Update README.md if prompt structure or naming changed

### Workflow 5: Bulk Synchronization

When multiple skills or files are modified:

1. Inform the user about the automated sync option
2. Suggest running: `make sync`
3. The sync script will:
   - Detect all installed model directories
   - Remove old skills/ directories
   - Copy current skills/ to all models
   - Display colored status output

---

## Validation Checklist

After synchronization, verify:

### File Consistency

- [ ] All modified skills exist in every model directory (.github, .claude, .codex, .gemini)
- [ ] Skill content is identical across all model directories
- [ ] No outdated or orphaned skill directories remain
- [ ] AGENTS.md, CLAUDE.md, and GEMINI.md have matching content (except source comments)

### Frontmatter Compliance

- [ ] Modified skills use `dependencies` for external libraries (with version ranges)
- [ ] Modified skills use `skills` for internal skill references
- [ ] AGENTS.md uses `skills` for skill references (never `dependencies`)
- [ ] All referenced skills actually exist in skills/ directory

### Meta-Skills Verification

- [ ] If a new meta-skill was added, update META_SKILLS in install.sh
- [ ] Meta-skills list in install.sh: skill-creation, agent-creation, prompt-creation, process-documentation, critical-partner, conventions, a11y, skill-sync

### External Projects

- [ ] Consider if external projects using this framework need notification
- [ ] Update sync.sh if synchronization logic changed
- [ ] Update scripts/templates/uninstall.sh if new directories were added

---

## Edge Cases

### No Model Directories Installed

If no model directories exist (.github, .claude, .codex, .gemini):

- Skip synchronization steps
- Only validate skill/agent structure and compliance
- Inform user that sync will occur when models are installed

### Partial Installation

If only some model directories exist:

- Synchronize only to existing directories
- Document which models are installed
- Suggest running `make setup` to install additional models

### Sync Script vs Manual Sync

- **Use sync script** (`make sync`): After bulk changes, git pull, or multiple skill updates
- **Use manual sync**: For surgical updates during active development, when verifying specific skill propagation

### Conflicting Changes

If model directory content differs from skills/:

- Always prioritize skills/ as the source of truth
- Remove old content completely before copying
- Document discrepancies if they indicate configuration drift

---

## References

- [scripts/sync.sh](../../scripts/sync.sh): Automated synchronization script
- [scripts/install.sh](../../scripts/install.sh): META_SKILLS definition and installation logic
- [skill-creation](../skill-creation/SKILL.md): Standards for creating new skills
- [Makefile](../../Makefile): Available sync and clean commands
