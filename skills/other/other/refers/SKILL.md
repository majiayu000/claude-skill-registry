---
name: refers
description: |
  Reference collection of official Anthropic skills for learning and best practices study.

  TRIGGER when: Never - this is a reference collection, not an invocable skill.

  DO NOT TRIGGER when: Always - this directory contains sample skills from anthropic-skills repository for reference purposes only.
version: "1.0.0"
user-invocable: false
---

# Official Anthropic Skills Reference Collection

> Reference collection of 5 representative skills from [anthropic-skills](https://github.com/anthropics/anthropic-skills) repository

## Purpose

This is **NOT** an invocable skill. It's a reference collection of official Anthropic skills used for:

1. **Learning best practices** - Study how official skills are structured
2. **Pattern reference** - See examples of different skill types
3. **API examples** - Multi-language Claude API integration samples
4. **Design inspiration** - Canvas and PDF processing examples

## Contents

| Skill | Size | Type | Description |
|-------|------|------|-------------|
| **skill-creator** | 260KB | Meta-tool | Tool for creating and managing other skills |
| **mcp-builder** | 144KB | Tool | MCP (Model Context Protocol) server builder |
| **pdf** | 80KB | Document | PDF generation and processing |
| **claude-api** | 236KB | API | Claude API integration examples (multi-language) |
| **canvas-design** | 5.5MB | Design | Canvas design tool with font resources |

## Usage

**DO NOT invoke this skill.** Instead:

1. Browse subdirectories to study official skill patterns
2. Read individual SKILL.md files for structure examples
3. Examine scripts/ and references/ to understand skill organization
4. Learn from multi-language API examples in claude-api/

**See**: [README.md](README.md) for detailed descriptions

## Source

- **Official Repository**: https://github.com/anthropics/anthropic-skills
- **Downloaded**: 2026-03-05
- **Purpose**: Reference and learning resource
- **License**: Each skill contains its own LICENSE.txt

---

**Version:** 1.0.0
**Last Updated:** 2026-03-11
**Changelog:**
- v1.0.0 (2026-03-11): Initial release - reference collection (non-invocable)

**Type:** Reference Collection (Non-invocable)
**Maintained By:** AI Dev Framework Team
