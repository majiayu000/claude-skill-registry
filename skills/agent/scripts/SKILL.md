---
name: platxa-skill-generator
description: Autonomous skill creator for Claude Code CLI. Uses multi-phase orchestrated workflow with Task tool subagents to research domains, design architecture, generate content, and validate quality. Creates production-ready skills following Anthropic's Agent Skills specification.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - Task
  - AskUserQuestion
  - TodoWrite
metadata:
  version: "1.0.0"
  author: "DJ Patel — Founder & CEO, Platxa | https://platxa.com"
  tags:
    - skill-creation
    - automation
    - builder
    - claude-code
---

# Platxa Skill Generator

Create Claude Code skills autonomously using a multi-phase orchestrated workflow.

## Overview

This skill guides you through creating production-ready Claude Code skills by:

1. **Discovering** domain knowledge through web research and existing skill analysis
2. **Architecting** the skill structure based on type (Builder/Guide/Automation/Analyzer/Validator)
3. **Generating** SKILL.md content, scripts, and reference documentation
4. **Validating** against Anthropic's Agent Skills spec with quality scoring

The workflow uses Task tool subagents for each phase, ensuring deep expertise at every step.

## Workflow

### Phase 1: Initialize

```
User: /skill-generator
```

Ask the user for:
- Skill description (what should the skill do?)
- Target users (who will use this skill?)

### Phase 2: Discovery (Automatic)

Use Task tool with `subagent_type="Explore"` to:
1. Search web for domain best practices
2. Fetch relevant documentation
3. Analyze existing skills in `~/.claude/skills/` for patterns
4. Identify procedural knowledge (HOW) vs domain expertise (WHAT)
5. Determine what varies by project vs what's constant

**Sufficiency Check**: Evaluate if research is complete. Only ask user for clarification if gaps exist.

### Phase 3: Architecture

Based on discovery, determine:
- **Skill Type**: Builder, Guide, Automation, Analyzer, or Validator
- **Structure**: Which directories needed (scripts/, references/, assets/)
- **Token Budget**: SKILL.md < 500 lines, metadata ~100 tokens

Generate architecture blueprint JSON:
```json
{
  "skill_type": "Builder",
  "directories": ["scripts", "references"],
  "skill_md_sections": ["Overview", "Workflow", "Examples", "Output Checklist"],
  "scripts": [{"name": "validate.sh", "purpose": "Validate output"}],
  "references": [{"name": "best-practices.md", "purpose": "Domain expertise"}]
}
```

### Phase 4: Generation

Create all skill files:
1. **SKILL.md** with valid YAML frontmatter
2. **scripts/** with executable helpers
3. **references/** with domain documentation

Use templates from `references/templates/` based on skill type.

### Phase 5: Validation

Run quality checks:
- [ ] SKILL.md exists with valid frontmatter
- [ ] Name is hyphen-case, ≤64 characters
- [ ] Description is ≤1024 characters
- [ ] Token budget within limits
- [ ] Scripts are executable and secure
- [ ] References provide real domain expertise

**Quality Score**: Must be ≥7.0/10 to pass.

### Phase 6: Installation

Ask user for installation location:
- **User skill**: `~/.claude/skills/{skill-name}/`
- **Project skill**: `.claude/skills/{skill-name}/`

Copy files and verify installation.

## Examples

### Example 1: Creating a Code Documenter Skill

```
User: /skill-generator
Assistant: What skill would you like to create?
User: A skill that generates documentation for Python code
Assistant: [Runs Discovery subagent to research Python docstring standards...]
Assistant: [Creates architecture for "Automation" type skill...]
Assistant: [Generates py-documenter skill with SKILL.md, scripts/generate-docs.sh]
Assistant: Quality score: 8.2/10. Install to ~/.claude/skills/py-documenter? (y/n)
```

### Example 2: Creating a Security Analyzer Skill

```
User: /skill-generator
Assistant: What skill would you like to create?
User: A skill that scans code for security vulnerabilities
Assistant: [Discovers OWASP Top 10, SAST patterns, CVE databases...]
Assistant: [Creates "Analyzer" type skill with references/owasp-checklist.md]
Assistant: Quality score: 7.8/10. Ready to install.
```

## Output Checklist

When generating a skill, verify:

- [ ] SKILL.md has valid YAML frontmatter
- [ ] Name follows hyphen-case (e.g., `my-skill-name`)
- [ ] Name is ≤64 characters
- [ ] Description is ≤1024 characters
- [ ] `allowed-tools` lists only tools the skill needs
- [ ] Workflow section has clear steps
- [ ] Examples show realistic usage
- [ ] References contain actual domain expertise (not placeholders)
- [ ] Scripts are executable and tested
- [ ] Quality score ≥7.0/10

## Skill Types Reference

| Type | Purpose | Key Sections |
|------|---------|--------------|
| Builder | Create new things | Workflow, Templates, Output Checklist |
| Guide | Teach/explain | Steps, Examples, Best Practices |
| Automation | Automate tasks | Triggers, Scripts, Verification |
| Analyzer | Inspect/audit | Checklist, Metrics, Reports |
| Validator | Verify quality | Rules, Thresholds, Pass/Fail Criteria |