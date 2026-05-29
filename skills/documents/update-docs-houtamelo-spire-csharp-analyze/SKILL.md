---
name: update-docs
description: Propagate a change across all related docs, agents, skills, and rules using the cross-reference map. Use when adding/removing MCP tools, skills, or modifying conventions.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: [description of the change]
---

# Update Docs

Change description: `$ARGUMENTS`

## Step 1: Read the cross-reference map

Read `.claude/rules/cross-reference-check.md` to understand which files are grouped together.

## Step 2: Identify affected groups

Based on the change description, determine which cross-reference groups are affected.

## Step 3: Read all files in affected groups

Read every file in each affected group. Build a list of edits needed.

## Step 4: Handle specific change types

### MCP tool added

1. Grep `.claude/agents/` and `.claude/skills/` for the `tools:` frontmatter field.
2. For each agent/skill, read its description and role.
3. If the new MCP tool is relevant to the agent's role, add it to the `tools:` list.
4. If the agent/skill body references related tools or workflows, add a mention of the new tool where appropriate.
5. Ask the user for confirmation before adding the tool to any agent you're uncertain about.

### MCP tool removed

1. Grep `.claude/` for the tool name.
2. Remove the tool from every `tools:` frontmatter list where it appears.
3. Remove or rewrite any instructions that reference the tool.
4. Ask the user what should replace the tool's functionality (if anything).

### Skill added

1. Read the new skill's `SKILL.md` to understand what it does.
2. Read all agent definitions in `.claude/agents/`.
3. For agents whose role overlaps with the skill's purpose, add a reference (e.g., "Use `/skill-name` for X").
4. If the skill relates to a workflow step in `CLAUDE.md`, update that step.
5. Ask the user for confirmation before adding references to agents you're uncertain about.

### Skill removed

1. Grep `.claude/` and `CLAUDE.md` for the skill name.
2. Remove or rewrite all references.
3. If the skill was part of a workflow step in `CLAUDE.md`, update or remove that step.

### Convention or format changed

1. Identify the cross-reference group for the convention.
2. Read all files in the group.
3. Update each file to reflect the new convention.
4. Check for inline examples or templates that use the old convention.

### Other changes

1. Use the cross-reference map to find all related files.
2. Read each one and determine if it needs updating.
3. Apply edits, asking the user when unsure.

## Step 5: Apply edits

For each edit:
- If you're confident the edit is correct, apply it.
- If you're unsure whether a specific file should be changed, ask the user before editing.

## Step 6: Verify

After all edits, grep for any remaining references to old names, removed tools, or stale conventions. Report any you find.

## Constraints

- Always read before editing — never edit a file you haven't read in this session.
- Ask the user when unsure about a specific edit — don't guess.
- Do not delete files — only edit content within them (or report that a file should be deleted).
- Update the cross-reference map itself if the change adds or removes files from a group.
