---
name: update-skill
model: standard
description: Update an existing skill with improvements
usage: /update-skill <path>
---

# /update-skill

Load an existing skill, make improvements, and validate.

## Usage

```
/update-skill <path>
```

**Arguments:**
- `path` — Path to skill directory (relative or absolute)

## Examples

```
/update-skill ai/skills/realtime/websocket-hub-patterns
/update-skill ai/skills/design-systems/distinctive-design-systems
/update-skill ai/skills/my-custom-skill
```

## When to Use

- After using a skill and finding gaps or issues
- When a better approach is discovered
- To add missing sections (NEVER Do, Related, examples)
- When patterns or best practices change
- During periodic skill maintenance

## What It Does

1. **Reads** the current SKILL.md content
2. **Validates** current structure (checks for required sections)
3. **Identifies** gaps (missing When to Use, NEVER Do, Related, examples)
4. **Prompts** for specific updates:
   - What needs to change?
   - New patterns to add?
   - Anti-patterns discovered?
5. **Updates** the skill with changes
6. **Re-validates** against quality criteria
7. **Reports** what was changed

## Required Sections Check

The command verifies these sections exist:

- [ ] Frontmatter with name and description
- [ ] When to Use section
- [ ] Code examples
- [ ] NEVER Do section
- [ ] Related section (if applicable)

## Quality Re-validation

After updates:

- [ ] Description still has WHAT, WHEN, KEYWORDS
- [ ] Still <300 lines (max 500)
- [ ] Still project-agnostic
- [ ] New content follows existing style

## Output Locations

- Updated skill → `[path]/SKILL.md`
- No new files created

## Related

- **Create new:** `/create-skill` (for new skills)
- **Validate:** `/validate-skill` (check without updating)
- **Archive old:** `/archive-skill` (deprecate skills)
