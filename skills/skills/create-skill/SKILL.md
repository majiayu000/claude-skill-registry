---
name: create-skill
description: "Add a new skill to the LaunchDarkly agent-skills repo. Use when creating a new SKILL.md, updating the skills catalog, and aligning with repo conventions."
license: Apache-2.0
compatibility: Works in repositories following the Agent Skills open standard
metadata:
  author: launchdarkly
  version: "0.1.0"
---

# Create a LaunchDarkly Skill

This skill guides contributors through adding a new skill to the LaunchDarkly agent-skills repository, following the open standard and local repo conventions.

## Prerequisites

- Access to the LaunchDarkly agent-skills repo
- Familiarity with the workflow you want to encode

## Steps

1. **Pick a category and name**
   - Choose a category under `skills/` (for example, `feature-flags`, `ai-config`).
   - Create a directory `skills/<category>/<skill-name>/`.
   - Ensure `<skill-name>` is lowercase with hyphens, and matches the `name` field exactly.

2. **Create `SKILL.md`**
   - Copy `template/SKILL.md.template` into the new skill directory and rename it to `SKILL.md`.
   - Fill in required frontmatter: `name`, `description`.
   - Keep `SKILL.md` under 500 lines and move deep details to `references/`.

3. **Add supporting files**
   - If needed, add `references/` and optional `scripts/` or `assets/`.
   - Keep reference files small and focused for on-demand loading.

4. **Update repo docs**
   - Add the skill to the table in `README.md`.
   - If the skill requires specific tooling, document it clearly in the skill.

5. **Update the catalog**
   - Run `python3 scripts/generate_catalog.py` to update `skills.json`.

6. **Validate**
   - Run `python3 scripts/validate_skills.py`.
   - Run `python3 -m unittest discover -s tests`.

## Guidelines

- Follow the Agent Skills spec for naming and frontmatter.
- Make “when to use this” explicit in the description.
- Avoid internal-only links or tools unless the skill is internal-only.

## Examples

### Example: Add an AI config skill

**User**: "Add a skill to guide creating AI Configs"

**Expected behavior**:
1. Create `skills/ai-configs/create-ai-config/`.
2. Fill `SKILL.md` using the template.
3. Add references if needed.
4. Update `README.md` and `skills.json`.
5. Run validation scripts.

## Edge Cases

- **Name mismatch**: If `name` doesn’t match the folder name, fix the folder or frontmatter.
- **Overlong SKILL.md**: Move detailed content into `references/`.
- **Missing catalog update**: Regenerate `skills.json` before committing.

## References

- `README.md`
- `docs/skills.md`
- `docs/versioning.md`
