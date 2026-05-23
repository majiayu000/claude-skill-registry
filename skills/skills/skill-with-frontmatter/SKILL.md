---
name: skill-with-frontmatter
description: A test skill with full YAML frontmatter for testing frontmatter parsing
triggers:
  - test-frontmatter
  - frontmatter-example
---

# Skill With Frontmatter

This skill tests YAML frontmatter parsing and name field updates during installation.

## Usage

Trigger this skill with "test-frontmatter" or "frontmatter-example" keywords.

## Instructions

When this skill is invoked:
1. Confirm that frontmatter was parsed correctly
2. Verify the name field matches the flattened skill name
3. Report the triggers that were extracted from frontmatter
