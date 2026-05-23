---
name: skill-builder
description: Generate new Claude Code skills from requirements through guided questions and pattern selection
argument-hint: "[skill-name] [--type research|automation|tool|simple]"
allowed-tools: Read, Write, Glob, AskUserQuestion
user-invocable: true
---

# Skill Builder

Generate complete Claude Code skills through requirements gathering, pattern selection, and template-based generation.

**Principle:** Most skills should be pure SKILL.md. Python only when it adds clear value.

---

## Arguments

Parse from `$ARGUMENTS`:

- **skill-name:** Required — Name for the new skill (kebab-case)
- **--type:** Optional — Hint skill type (research, automation, tool, simple)

---

## Workflow

### Phase 1: Parse Request

Extract:
- Skill name from arguments
- Type hint if provided
- Any description in user message

If no skill name provided, ask user.

### Phase 2: Detect Skill Type

Analyze user's description to determine type:

| Indicator | Type | Characteristics |
|-----------|------|-----------------|
| search, aggregate, synthesize, news, digest | **research** | Web searches, multiple sources, synthesis |
| scheduled, incremental, track, monitor, state | **automation** | State files, recurring runs, incremental |
| compute, transform, parse, API, external | **tool** | May need Python, external integrations |
| single purpose, straightforward | **simple** | Minimal phases, focused task |

**Default:** simple (avoid over-engineering)

### Phase 3: Gather Requirements

Load questions from `questions/`:
- `base-questions.md` — Always ask (3-4 questions)
- `{type}-questions.md` — Type-specific (2-3 questions)

Ask 5-7 total questions via AskUserQuestion tool.

**Question categories:**
1. Purpose and trigger ("When would you use this?")
2. Inputs ("What information do you provide?")
3. Outputs ("What should it produce?")
4. Sources/data ("Where does data come from?")
5. Quality criteria ("How do you know it's good?")

Store answers for template customization.

### Phase 4: Assess Python Need

**Python warranted ONLY if:**
- External API calls (not web search)
- Complex computation Claude can't do
- Binary/structured format parsing
- Rate limiting or pagination logic

**Ask explicitly if unclear:**
> "This skill involves [X]. Would you benefit from a Python script for [specific task], or should Claude handle it directly?"

**Default:** No Python. Simpler is better.

### Phase 5: Select Patterns

Based on answers, select from `patterns/`:

| User Need | Pattern |
|-----------|---------|
| Multiple phases, complex flow | phase-workflow.md |
| Runs repeatedly, tracks history | state-management.md |
| Needs Python scripts | python-integration.md |

Load selected patterns for template generation.

### Phase 6: Generate Skill

**6a. Create directory:**
```
.claude/skills/[skill-name]/
```

**6b. Generate SKILL.md:**

Load `templates/skill-base.md`, customize with:
- User's answers
- Detected type
- Selected patterns
- Concrete examples from answers

**6c. Generate supporting files (if needed):**

- `output-template.md` — If structured output required
- `sources.md` — If multiple data sources
- `checklist.md` — If complex quality requirements

**6d. If Python needed:**

- Create `scripts/` directory
- Generate `pyproject.toml` from `templates/pyproject-template.toml`
- Generate script skeleton (user completes implementation)

### Phase 7: Verify

Load `checklist.md` and verify:

- [ ] SKILL.md has valid YAML frontmatter
- [ ] All phases have concrete steps
- [ ] No placeholder text ("TODO", "fill in", etc.)
- [ ] Arguments documented
- [ ] Error handling defined
- [ ] Output format specified
- [ ] Python only if justified

### Phase 8: Output Summary

Write all files, then show:

```markdown
# Generated Skill: [name]

**Location:** .claude/skills/[name]/
**Type:** [detected-type]
**Python:** [Yes/No]

## Files Created
- SKILL.md — Main skill definition
- [other files if any]

## How to Use
```
/[skill-name] [example-args]
```

## Next Steps
- Review SKILL.md for accuracy
- [If Python] Implement script logic
- Test with example invocation
```

---

## Type-Specific Generation

### Research Skills

Include:
- Phase for multi-source search (WebSearch patterns)
- Phase for synthesis/deduplication
- State management for incremental runs
- Source attribution in output

### Automation Skills

Include:
- State file patterns (.last-run, .processed)
- Conditional skip logic
- Incremental processing
- Cleanup/rotation for state files

### Tool Skills

Include:
- Clear input/output contract
- Validation of inputs
- Structured output format
- Error handling with actionable messages

### Simple Skills

Include:
- Minimal phases (2-3)
- Focused scope
- Direct execution
- No state management unless needed

---

## Error Handling

- **No skill name:** Ask user for name
- **Ambiguous type:** Default to simple, note in output
- **Unclear Python need:** Ask user explicitly, default to no
- **Missing questions file:** Use base questions only

---

## Quality Principles

**From SKILL-GUIDELINES.md:**

1. **Concrete over generic** — Actual commands, real examples
2. **Self-contained** — Complete instructions in SKILL.md
3. **Minimal complexity** — Simplest solution that works
4. **Python only when valuable** — Most skills are pure markdown
