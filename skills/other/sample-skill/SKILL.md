---
name: sample-skill
description: "Use when validating the SkillForge validator itself - exercises every supported frontmatter feature: boolean user-invocable, an allowed-tools block list, and nested metadata with an inline list."
license: MIT
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Bash
metadata:
  version: 1.2.3
  author: skillforge-tests
  domains: [testing, meta]
---

# Sample Skill

A fixture skill used by test_validate_skill.py. It uses every frontmatter
feature the vendored YAML parser must support, and satisfies every
structural check in validate_skill.py, so the full validator must report
zero errors for it.

## Process

1. Run the validator against this directory.
2. Assert that the error list is empty.
3. Assert that typed values survived parsing (booleans stay booleans).

| Step | Check | Expected |
|------|-------|----------|
| 1 | frontmatter parse | no error |
| 2 | user-invocable | bool True |
| 3 | allowed-tools | list of 3 tools |

## Verification

- [ ] validate_skill.py reports zero errors
- [ ] quick_validate.py reports the skill as valid
- [ ] user-invocable parsed as a boolean

## Anti-Patterns

- Do not pin a dated model ID in frontmatter.
- Do not duplicate reference content in collapsible details blocks.

## Extension Points

- Add hooks frontmatter once the vendored parser grows hook fixtures.
- Add a scripts/ directory to exercise script lint checks.
