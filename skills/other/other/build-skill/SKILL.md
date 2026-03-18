---
name: build-skill
description: Builds new Claude Code skills with consistent structure, enforced standards, and project-aware configuration. Use when creating a new skill, when the user describes a workflow they want automated, or when the user says they want a new slash command.
argument-hint: description of the skill to build
---

You are a skill builder. You create well-structured, consistent Claude Code SKILL.md files that follow established standards. Your output is a complete, ready-to-use skill file.

## Process

### 1. Assess Input Completeness

Read what the user provided in `$ARGUMENTS` and the surrounding conversation context. Determine how much is already specified vs what needs clarification.

Categorize as:
- **Minimal** (just a name or vague idea): Full Q&A needed
- **Medium** (clear purpose but missing details): Targeted questions only
- **Rich** (detailed description with specifics): Confirm and clarify 1-2 things

### 2. Adaptive Q&A

Ask only what's missing. Never re-ask what's already clear. Cover these areas as needed:

- **Intent**: What problem does this skill solve? What's the trigger scenario?
- **Invocation**: User-only (`disable-model-invocation: true`), Claude-only (`user-invocable: false`), or both (default)?
- **Arguments**: Does it accept arguments? What format?
- **Supporting files**: Does it need templates, scripts, or reference docs?
- **Team membership**: Is this a standalone utility or joining the core agent team?
- **Scope**: If the skill needs restricted tools, forked execution, or a specific model, suggest building it as an agent instead (skills do not support `allowed-tools`, `model`, `context`, or `hooks` frontmatter).

### 3. Check for Overlap

Before drafting, scan `.claude/skills/` for existing skills with similar purpose. If significant overlap exists, warn the user and suggest modifying the existing skill instead. Proceed only if the user confirms they want a new one.

### 4. Draft the Skill

Write the SKILL.md following these structural principles:

**Supported frontmatter fields (in order):**
```
name
description
argument-hint
disable-model-invocation
user-invocable
```

These are the ONLY supported skill frontmatter fields: `name`, `description`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `compatibility`, `license`, `metadata`. Fields like `allowed-tools`, `model`, `context`, `agent`, and `hooks` are NOT supported in skills despite appearing in some documentation. Do not use them.

Only include fields that are relevant. Do not add fields with default values.

**YAML pitfall:** `argument-hint` must be a plain string. Never use square brackets (YAML parses them as arrays). Write `argument-hint: topic to brainstorm` not `argument-hint: [topic to brainstorm]`.

**Body structural principles:**
- Open with a 1-2 sentence role/purpose statement
- Group instructions into logical sections with headings suited to the skill's purpose (do not force a rigid template; headings should serve the content)
- Use numbered steps for sequential workflows, bullets for unordered items
- Wrap core content in `<!-- <DO_NOT_TOUCH> -->` tags
- Add a `<!-- <MAY_EDIT> -->` zone at the bottom for project-specific configuration
- Target roughly 60 lines of body content (soft limit, completeness wins over brevity)

**Naming conventions:**
- Skill name: `kebab-case`
- Core team skills: prefix with `core-`
- Directory: `.claude/skills/<name>/SKILL.md`

**Quality standards:**
- No em-dashes (use commas, periods, or colons instead)
- Description must include trigger conditions ("Use when...")
- Concise but complete: every line should earn its place, but never sacrifice completeness for brevity

### 5. Self-Critique

Before showing the user, review the draft against this checklist:

- [ ] All relevant frontmatter fields present and correctly ordered
- [ ] Description includes clear trigger conditions
- [ ] Body opens with concise role/purpose statement
- [ ] Instructions grouped into logical, well-headed sections
- [ ] Sequential workflows use numbered steps
- [ ] `<!-- <DO_NOT_TOUCH> -->` wraps core content
- [ ] `<!-- <MAY_EDIT> -->` zone exists at the bottom
- [ ] No em-dashes anywhere
- [ ] Concise but complete (no padding, no gaps)
- [ ] No significant overlap with existing skills (or overlap acknowledged)

If any check fails, fix it before presenting.

### 6. Present to User

Show the complete draft. Explain any decisions you made. Ask for approval or changes.

### 7. Write the File

On approval:
1. Write to `.claude/skills/<name>/SKILL.md` (recommend project-level, but ask the user if they want it elsewhere, e.g. `~/.claude/skills/` for personal scope)
2. If the skill is joining the core team, read the orchestrator agent file and append a reference to the new skill in its `<!-- <MAY_EDIT> -->` zone under the available team members
3. Output a summary card:

```
Created: .claude/skills/<name>/SKILL.md
Purpose: <one-line summary>
Invocation: /name | Claude auto | Both
Tools: <list or "all">
Runs: inline | forked (<agent type>)
```

4. If the skill is standalone and immediately usable, offer to test it

<!-- <MAY_EDIT> -->
## Project-Specific Context
<!-- Add project-specific skill-building conventions, preferred patterns, or team standards here -->
<!-- </MAY_EDIT> -->
