---
name: yaml-error-skill
description: A skill with malformed YAML to test error handling
metadata:
  key1: value1
  key2: [unclosed array
  key3: value3
---

This skill has intentionally malformed YAML frontmatter to test error handling.
