---
name: skill-validator
description: Validate skills against Anthropic best practices for frontmatter, structure, content, file organization, hooks, MCP, and security (62 rules in 8 categories). Use when creating new skills, updating existing skills, before publishing skills, reviewing skill quality, or when user mentions "validate skill", "check skill", "skill best practices", "skill review", or "lint skill".
argument-hint: [skill-path]
---

# Skill Validator

Run automated checks against 62 rules covering frontmatter, structure, content, files, references, security, hooks, and MCP.

## Quick Start

```bash
scripts/validate_skill.py /path/to/skill-directory
```

With severity filter:

```bash
scripts/validate_skill.py /path/to/skill --min-severity warning
```

## Validation Categories

| Category | Rules | Checks |
|----------|-------|--------|
| **Frontmatter** | FM001-FM018 | Required fields, naming, description, context/agent, maxTurns, memory, disable-model-invocation |
| **Structure** | SS001-SS006 | Line limits, progressive disclosure |
| **Content** | CW001-CW009 | Writing style, terminology, string substitution, dynamic context injection, ultrathink |
| **Files** | FO001-FO007 | Naming conventions, forbidden files |
| **References** | RI001-RI003 | Broken links, orphan files |
| **Security** | SC001-SC005 | eval/exec, undocumented constants |
| **Hooks** | HK001-HK003 | Hook structure, handler format, matcher format |
| **MCP** | MC001 | MCP server configuration format |

## Severity Levels

| Level | Action |
|-------|--------|
| CRITICAL | Must fix before publishing |
| ERROR | Should fix |
| WARNING | Consider fixing |
| SUGGESTION | Optional improvement |

## Output Example

```
=== Skill Validation Report: my-skill ===

Summary: 0 critical, 1 error, 2 warnings, 1 suggestion

[ERROR] SS002: SKILL.md exceeds 500 lines (523 lines)
  Location: SKILL.md
  Fix: Split content into WORKFLOW.md, EXAMPLES.md, TROUBLESHOOTING.md

[WARNING] CW001: Second-person language detected
  Location: SKILL.md:45
  Found: "You should create..."
  Fix: Use imperative: "Create..."
```

## Command Options

```bash
--min-severity {critical,error,warning,suggestion}  # Filter output
--format {text,json}                                # Output format
--ignore RULE1,RULE2                                # Skip specific rules
```

## Common Issues

**"False positive on second-person"**
- Context-appropriate "you" may be acceptable
- Use `--ignore CW001` to suppress

**"Script security warning"**
- Add inline comment: `# skill-validator: ignore SC001`

**"Hook/MCP validation incomplete"**
- Install PyYAML for full nested structure validation: `pip install pyyaml`

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for complete issue handling.

## References

- [EXAMPLES.md](EXAMPLES.md) - Real validation outputs
- [references/RULES_REFERENCE.md](references/RULES_REFERENCE.md) - Complete rules documentation
