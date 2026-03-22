---
name: test-version-207
description: |
  Test skill to verify version fields are properly included in YAML frontmatter.

  TRIGGER when: User wants to test version field generation.

  DO NOT TRIGGER when: In production use.
version: "1.0.0"
last-updated: "2026-03-15"
---

# Test Version 207

This is a test skill created to verify that skill-creator properly generates:
1. `version: "1.0.0"` in YAML frontmatter
2. `last-updated: "YYYY-MM-DD"` in YAML frontmatter
3. Version metadata in Markdown footer

## Usage

Simply invoke this skill to test version field generation.

---

**Version:** 1.0.0
**Pattern:** Test skill
**Compliance:** ADR-001 ✅
**Last Updated:** 2026-03-15
**Changelog:**
- v1.0.0: Initial test release
