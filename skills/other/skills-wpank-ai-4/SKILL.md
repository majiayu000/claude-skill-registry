---
name: validate-skill
model: fast
description: Check a skill against quality criteria
usage: /validate-skill <path>
---

# /validate-skill

Validate a skill against quality criteria.

## Usage

```
/validate-skill <path>
```

**Arguments:**
- `path` — Path to skill (can be relative or absolute)

## Examples

```
/validate-skill ai/skills/realtime/websocket-hub-patterns
/validate-skill ai/staging/skills/new-pattern
/validate-skill ai/skills/my-skill
```

## What It Does

1. **Reads** the SKILL.md file at the given path
2. **Checks** for required sections (When to Use, NEVER Do)
3. **Validates** description format (WHAT, WHEN, KEYWORDS)
4. **Measures** line count (<300 preferred, 500 max)
5. **Scans** for project-specific references
6. **Checks** for code examples
7. **Reports** pass/fail for each criterion
8. **Suggests** improvements for failures

## Sample Output

```
Validating: ai/skills/realtime/websocket-hub-patterns

Quality Criteria:
  ✓ Has description with WHAT, WHEN, KEYWORDS
  ✓ Has "When to Use" section
  ✓ Has code examples
  ✓ Has NEVER Do section
  ✓ Line count: 187 (< 300 ✓)
  ✓ Project-agnostic (no hardcoded names)

Expert Knowledge Check:
  ✓ Contains patterns not in base model

Result: PASS (7/7 criteria met)
```

## Quality Criteria Checked

| Criterion | Requirement |
|-----------|-------------|
| Description | Contains WHAT, WHEN, KEYWORDS |
| When to Use | Section exists with trigger conditions |
| Code Examples | At least one code block |
| NEVER Do | Section exists with anti-patterns |
| Line Count | <300 preferred, 500 max |
| Project-Agnostic | No hardcoded project names/paths |
| Expert Knowledge | >70% not in base Claude model |

## Output Locations

- No files created — displays to terminal only

## Automation

- **Optional automation:** Run `python3 scripts/validate_links.py` to validate all markdown links in the skill with fix suggestions.

## Related

- **Create skill:** `/create-skill` (guided creation)
- **Check overlaps:** `/check-overlaps` (find redundant skills)
- **Quality criteria:** [`ai/skills/extraction/references/skill-quality-criteria.md`](ai/skills/extraction/references/skill-quality-criteria.md)
