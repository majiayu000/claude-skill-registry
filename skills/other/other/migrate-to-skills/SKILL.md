---
name: migrate-to-skills
description: |
  Convert legacy subagents, slash commands, and rules to the unified Agent Skills format.
  Use when migrating agent resources, consolidating legacy directories, or standardizing 
  across Claude Code, Cursor, Copilot, Codex, and Open Code.
disable-model-invocation: true
argument-hint: <scope: all|subagents|commands|rules|path>
allowed-tools: Read Write Edit Glob Grep Bash
---

# Convert to Skills

Convert legacy agent resources to the unified [Agent Skills](https://agentskills.io) format.

## Workflow

Execute these phases in order. Always get user approval before making changes.

### Phase 1: Discovery

Search for legacy resources. Run these searches immediately:

```bash
# Subagents
find . -path "*/.claude/agents/*.md" -o -path "*/.cursor/agents/*.md" -o -path "*/.codex/agents/*.md" 2>/dev/null

# Commands  
find . -path "*/.claude/commands/*.md" -o -path "*/.cursor/commands/*.md" -o -path "*/.codex/commands/*.md" 2>/dev/null

# Rules
find . -path "*/.claude/rules/*.md" -o -path "*/.cursor/rules/*.mdc" -o -path "*/.cursor/rules/*.md" 2>/dev/null

# Custom Prompts (Codex)
find . -path "*/.codex/prompts/*.md" 2>/dev/null

# AGENTS.md files
find . -name "AGENTS.md" 2>/dev/null
```

If `$1` specifies a path, only scan that location.

### Phase 2: Classification

Read each discovered file and classify it. Present findings as:

```markdown
## Discovery Results

### Subagents (X found)
| File | Name | Recommended Action |
|------|------|-------------------|
| .claude/agents/reviewer.md | reviewer | Convert to skill |

### Commands (X found)
| File | Name | Recommended Action |
|------|------|-------------------|
| .claude/commands/test.md | test | Convert to skill |

### Rules (X found)
| File | Name | Type | Recommended Action |
|------|------|------|-------------------|
| .cursor/rules/style.mdc | style | always-apply | Import to CLAUDE.md |
| .cursor/rules/react.mdc | react | glob-scoped | Keep as rule |
| .claude/rules/security.md | security | knowledge | Convert to skill |

### Already Skills (No Action)
- .claude/skills/existing/ ✓

### Needs Manual Review
- [file]: [reason]
```

**Rule classification logic:**
- `alwaysApply: true` → Import to CLAUDE.md via `@import`
- Has `globs` pattern → Keep as rule (skills don't support glob activation)
- General knowledge → Convert to skill

### Phase 3: Approval

Ask user:
> "Found X resources to convert. Proceed with conversion? [Y/n/customize]"

If "customize": Let user select specific items or modify actions.

### Phase 4: Conversion

For each approved conversion, apply the appropriate mapping:

**Subagent → Skill:**
- Add `context: fork` (required for subagent behavior)
- Simplify model names (see field-mappings.md)
- Keep `allowed-tools`
- Enhance description with trigger keywords

**Command → Skill:**
- Add `disable-model-invocation: true`
- Keep `argument-hint`
- Document `$ARGUMENTS`, `$1`, `$2` usage

**Rule → Skill (knowledge type only):**
- Write description with auto-trigger keywords
- No `disable-model-invocation` (allow auto-activation)

**Rule → CLAUDE.md (always-apply):**
- Add `@import path/to/rule.md` to CLAUDE.md

Create skill structure:
```
.claude/skills/{name}/
├── SKILL.md
├── scripts/      # If original has executables
├── references/   # If original has docs
└── assets/       # If original has templates
```

### Phase 5: Verification

After conversion, run:
```bash
# List created skills
ls -la .claude/skills/

# Verify frontmatter
for skill in .claude/skills/*/SKILL.md; do
  echo "=== $skill ===" && head -20 "$skill"
done
```

Present summary:
```markdown
## Conversion Complete

### Created Skills
| Skill | Location | Source |
|-------|----------|--------|
| reviewer | .claude/skills/reviewer/ | .claude/agents/reviewer.md |

### Updated Files
- CLAUDE.md: Added 2 @import statements

### Verification
- [x] All skills have valid frontmatter
- [x] Names match directory names
- [x] No duplicate skills
```

### Phase 6: Cleanup (Optional)

Ask user:
> "Delete original files? [y/N/archive]"

- **y**: Delete originals
- **N**: Keep originals (default)
- **archive**: Move to `.claude/archive/`

## Quick Reference

### Key Conversion Rules

| Source Type | Target | Key Addition |
|-------------|--------|--------------|
| Subagent | Skill | `context: fork` |
| Command | Skill | `disable-model-invocation: true` |
| Rule (knowledge) | Skill | Trigger keywords in description |
| Rule (always-apply) | CLAUDE.md | `@import` statement |
| Rule (glob-scoped) | Keep as rule | No conversion needed |

### Model Mapping

| Legacy | Skills |
|--------|--------|
| `claude-opus-4-*` | `opus` |
| `claude-sonnet-4-*` | `sonnet` |
| `claude-3-5-haiku-*` | `haiku` |
| `inherit` / omitted | *(omit)* |

### Tool Mapping

| Variations | Standard |
|------------|----------|
| read, ReadFile, file_read | `Read` |
| write, WriteFile | `Write` |
| bash, Terminal, Shell | `Bash` |
| grep, Search | `Grep` |
| glob, Find, list_files | `Glob` |

## Reference Files

For detailed specifications, read these on-demand:
- `references/spec-reference.md` - Full Agent Skills specification
- `references/field-mappings.md` - Complete field conversion tables
- `references/examples.md` - Before/after conversion examples

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not discovered | Check: name matches directory, valid YAML frontmatter |
| Triggers too often | Add `disable-model-invocation: true` |
| Doesn't auto-trigger | Remove `disable-model-invocation`, add keywords to description |
| Subagent behavior changed | Ensure `context: fork` is present |
| Hooks not working | Requires Claude Code 2.1+ |
