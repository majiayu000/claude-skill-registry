---
name: claude-md-development
description: "Manage CLAUDE.md documentation when updating the seed system documentation or project overview. Not for creating specific skills or commands."
---

# Claude.md Development

CLAUDE.md serves as the project's single source of truth for session behavior and component architecture. This skill ensures consistency between documentation and implementation.

**Core principle**: CLAUDE.md must remain concise, evergreen, and properly synchronized with .claude/rules/ and component meta-skills.

---

## What CLAUDE.md Contains

### Role 1: Health Maintenance (Session-Only)

- Project overview and architecture
- Core principles and philosophy
- Development workflow guidance
- Navigation to rules, skills, and docs

### Role 2: Component Factory Reference

- Key meta-skills reference table
- Component-specific guidance links
- Quality standards and Success Criteria
- Portability invariant enforcement

---

## Update Protocol

### When to Update CLAUDE.md

**Update required when:**

- Adding new meta-skills (invocable-development, etc.)
- Changing core architecture (Layer A/Layer B)
- Modifying project structure or navigation
- Adding new documentation directories
- Changing quality standards

**No update needed for:**

- Individual skill/command content changes
- Minor reference file updates
- Example additions
- Routine maintenance

---

## Content Synchronization

### Critical Synchronization Points

**CLAUDE.md ↔ .claude/rules/**

| CLAUDE.md Section | Rules File      | Sync Action                                |
| ----------------- | --------------- | ------------------------------------------ |
| Philosophy table  | principles.md   | Update table when principles change        |
| Key Meta-Skills   | All meta-skills | Add/remove entries when meta-skills change |
| Navigation        | patterns.md     | Ensure consistent terminology              |

**CLAUDE.md ↔ Meta-Skills**

| CLAUDE.md Reference | Meta-Skill                  | Sync Action                                    |
| ------------------- | --------------------------- | ---------------------------------------------- |
| Component Guidance  | invocable-development, etc. | Update links when meta-skill structure changes |
| Quality Standards   | quality-standards           | Align Success Criteria descriptions            |

---

## Best Practices

### Structure

- **Keep it concise**: CLAUDE.md should be ~300-500 lines max
- **Evergreen content**: Avoid transient information
- **Single source of truth**: Each concept documented once
- **Progressive disclosure**: High-level in CLAUDE.md, details in references/

### Navigation

- Use tables for structured references
- Include both file paths and descriptions
- Mark mandatory references clearly
- Cross-link to docs/ directory for extended content

### Quality

- Validate all links actually exist
- Ensure consistency with .claude/rules/
- Keep meta-skill table current
- Sync Success Criteria with quality-standards

---

## Common CLAUDE.md Patterns

### Philosophy Table Format

```markdown
| File          | Layer    | Content                                        |
| ------------- | -------- | ---------------------------------------------- |
| principles.md | **Both** | Dual-layer architecture, Portability Invariant |
| patterns.md   | **Both** | Implementation patterns, Degrees of Freedom    |
```

### Meta-Skill Table Format

```markdown
| Meta-Skill                | Purpose                  | Transformation                   |
| ------------------------- | ------------------------ | -------------------------------- |
| **invocable-development** | Creating portable skills | Tutorial → Architectural refiner |
```

### Component Guidance Format

```markdown
## Component-Specific Guidance

For detailed guidance on creating portable components, consult the appropriate meta-skill:

| Component | Meta-Skill            | Output Traits             |
| --------- | --------------------- | ------------------------- |
| Skills    | invocable-development | Portable, self-sufficient |
```

---

## Anti-Patterns

### DON'T: Include Generic Content

❌ "How to write Markdown"
❌ "What is YAML"
❌ "Introduction to Git"

### DON'T: Duplicate Content

❌ Repeating rules from .claude/rules/
❌ Copying meta-skill content into CLAUDE.md
❌ Duplicating philosophy explanations

### DON'T: Make It Transient

❌ Including session-specific notes
❌ Temporary workarounds
❌ "TODO" items for future work

---

## Navigation

For hybrid format standards (Markdown + XML), see the **hybrid-format rule**.

For architectural philosophy, see: `docs/philosophy/deep-dives.md`

For development workflows, see: `docs/workflows/development.md`

---

<critical_constraint>
MANDATORY: Keep CLAUDE.md under 500 lines (use progressive disclosure)
MANDATORY: Validate all links exist before committing changes
MANDATORY: Sync meta-skill table when adding/removing meta-skills
MANDATORY: Never include transient or TODO content
No exceptions. CLAUDE.md is evergreen documentation, not a scratchpad.
</critical_constraint>
