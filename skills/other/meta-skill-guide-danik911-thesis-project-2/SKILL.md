---
name: meta-skill-guide
description: Comprehensive guide for creating Claude Code custom skills. Use when asked to create, design, or improve custom skills for Claude Code. Provides templates, best practices, and patterns for simple, moderate, and advanced skills.
---

# Meta-Skill Guide: Creating Claude Code Custom Skills

## Quick Reference

| Aspect | Constraint | Recommendation |
|--------|-----------|----------------|
| **SKILL.md size** | No hard limit | Keep under 500 lines |
| **Skill name** | Max 64 chars | Lowercase, hyphens, gerund form (`processing-pdfs`) |
| **Description** | Max 1024 chars | WHAT it does + WHEN to use (third person) |
| **Reference depth** | One level deep | SKILL.md -> File.md only |
| **File paths** | Forward slashes | Always `scripts/helper.py` |
| **Subagent context** | Completely isolated | NO conversation history, NO memory |

---

## Architecture: Three-Level Progressive Loading

**Level 1: Metadata (~100 tokens/skill)**
```yaml
---
name: skill-name
description: Brief description with usage triggers
---
```
- Loaded at Claude Code startup
- Critical for skill discovery

**Level 2: Instructions (<5,000 tokens)**
- Main SKILL.md body content
- Loaded when user request matches description
- Optimal: Under 500 lines

**Level 3: Resources (Unlimited)**
- Additional markdown files, scripts, templates
- Loaded as needed via bash navigation
- Scripts execute without loading code into context

---

## File Structure

```
skill-name/
├── SKILL.md              # Main instructions (mandatory)
├── reference/            # Additional documentation
│   ├── advanced.md
│   └── api_reference.md
├── scripts/              # Executable code
│   └── validator.py
└── templates/            # Templates
    └── template.ext
```

---

## YAML Frontmatter

**Required:**
```yaml
---
name: skill-name
description: What skill does and when to use it. Include triggers and key terms.
---
```

**Optional (Claude Code):**
```yaml
allowed-tools: ["Bash", "Read", "Write", "Edit"]
model: claude-sonnet-4-5-20250929
```

**Naming Rules:**
- Max 64 chars, lowercase letters/numbers/hyphens
- Use gerund form: `processing-pdfs` (not `process-pdf`)
- Avoid vague names: `helper`, `utils`, `documents`

---

## Skill Levels

| Level | Lines | Characteristics | Template |
|-------|-------|-----------------|----------|
| **Simple** | 100-300 | Single task, no scripts | [reference/templates/simple.md](reference/templates/simple.md) |
| **Moderate** | 300-500 | Multiple ops, validation scripts | [reference/templates/moderate.md](reference/templates/moderate.md) |
| **Advanced** | 500+ distributed | Multi-phase, extensive refs | [reference/templates/advanced.md](reference/templates/advanced.md) |

---

## Best Practices Summary

### Top 10 DOs
1. Keep SKILL.md under 500 lines
2. Write descriptions in third person with triggers
3. Use consistent terminology throughout
4. Provide concrete examples with input/output pairs
5. Implement validation loops (Create -> Validate -> Fix)
6. Structure long files with table of contents
7. Use checklists for complex tasks
8. Solve problems in scripts, don't punt to Claude
9. Justify all constants and magic numbers
10. List required packages explicitly

### Top 10 DON'Ts
1. Reference time-sensitive information
2. Use Windows-style paths (`scripts\helper.py`)
3. Assume tools are pre-installed
4. Use vague MCP tool references
5. Provide too many equal options (decision paralysis)
6. Create deeply nested references (one level max)
7. Skip validation for quality tasks
8. Mix inconsistent terminology
9. Leave constants unexplained
10. Assume subagent context from conversation

**Full checklist:** [reference/best-practices.md](reference/best-practices.md)

---

## Subagent Integration Summary

### When to Delegate

| Task Type | Recommendation |
|-----------|----------------|
| Simple, <10 min | Direct in skill |
| Research-heavy | Delegate to `context-collector` |
| Multi-stage | Orchestrate specialists |
| Language-specific | Language expert subagents |
| Quality assurance | `code-reviewer`, `test-automator` |

### Key Constraints
- **NO conversation history access** - each invocation is fresh
- **NO nested delegation** - main agent orchestrates all
- **File artifacts for state transfer** - save results to files
- **Explicit output format** - prevent context overload

### Orchestration Patterns
1. **Parallel** - Independent tasks, single message, multiple Task calls
2. **Sequential** - Dependent tasks, file artifacts between steps
3. **Hub-and-Spoke** - Implementation + multiple reviewers
4. **Iterative** - Architect -> Reviewer cycles

**Full guide:** [reference/subagent-patterns.md](reference/subagent-patterns.md)

---

## Domain Patterns Summary

| Domain | Key Pattern | Example |
|--------|-------------|---------|
| **Creative** | Philosophy-first, reductive mastery | `algorithmic-art` |
| **Document** | Validation loops, zero-error mandate | `xlsx`, `pdf` |
| **Development** | Phase-based workflow, quality gates | `mcp-builder` |
| **Enterprise** | Template routing, clarification protocols | `internal-comms` |
| **Workflow** | Slash commands, automation | `worktree-manager` |

**Full patterns:** [reference/domain-patterns.md](reference/domain-patterns.md)

---

## Quality & Testing Summary

### Build Evaluations First
1. Run Claude WITHOUT skill on real tasks
2. Create 3+ test scenarios
3. Write minimal instructions to pass
4. Iterate based on real behavior

### Two-Claude Method
- **Claude A**: Skill author
- **Claude B**: Skill tester
- Iterate based on where B struggles

### Cross-Model Testing
- [ ] Haiku (cost optimization)
- [ ] Sonnet (standard)
- [ ] Opus (complex tasks)

**Full guide:** [reference/evaluation.md](reference/evaluation.md)

---

## Key Takeaways

### Architecture
- Three-level progressive loading: metadata -> instructions -> resources
- Filesystem-based: bash navigation, scripts execute without loading
- One level deep references only

### Structure
- SKILL.md under 500 lines
- YAML: name (64 chars) + description (1024 chars, third person)
- Forward slashes always, gerund naming

### Subagents
- Context isolation: NO history, NO memory
- Main agent orchestrates all delegation
- File artifacts for state transfer
- 90% improvement with parallel specialists

### Distribution
- Skills don't sync across surfaces
- Claude Code: `~/.claude/skills/` or `.claude/skills/`
- Share via git for teams

---

## External References

**Official Docs:**
- Skills Overview: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Best Practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Claude Code Skills: https://docs.claude.com/en/docs/claude-code/skills

**GitHub Examples:**
- Anthropic Skills: https://github.com/anthropics/skills
- Claude Cookbooks: https://github.com/anthropics/claude-cookbooks/tree/main/skills

**Full links:** [reference/links.md](reference/links.md)

---

## Version

**v1.2.0** (December 2025) - Refactored to progressive disclosure pattern
