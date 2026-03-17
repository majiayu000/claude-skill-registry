---
version: 4.1.0-fractal
name: skill-developer
description: Create and manage Claude Code skills following Anthropic best practices. Use when creating new skills, modifying skill-rules.json, understanding trigger patterns, working with hooks, debugging skill activation, or implementing progressive disclosure. Covers skill structure, YAML frontmatter, trigger types (keywords, intent patterns, file paths, content patterns), enforcement levels (block, suggest, warn), hook mechanisms (UserPromptSubmit, PreToolUse), session tracking, and the 500-line rule.
---

# Skill Developer Guide

## Purpose

Comprehensive guide for creating and managing skills in Claude Code with auto-activation system, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern.

## When to Use This Skill

Automatically activates when you mention:
- Creating or adding skills
- Modifying skill triggers or rules
- Understanding how skill activation works
- Debugging skill activation issues
- Working with skill-rules.json
- Hook system mechanics
- Claude Code best practices
- Progressive disclosure
- YAML frontmatter
- 500-line rule

---

## System Overview

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Two-Hook Architecture](./sub-skills/two-hook-architecture.md)
### 2. [Configuration File](./sub-skills/configuration-file.md)
### 3. [1. Guardrail Skills](./sub-skills/1-guardrail-skills.md)
### 4. [2. Domain Skills](./sub-skills/2-domain-skills.md)
### 5. [Step 1: Create Skill File](./sub-skills/step-1-create-skill-file.md)
### 6. [Step 2: Add to skill-rules.json](./sub-skills/step-2-add-to-skill-rulesjson.md)
### 7. [Step 3: Test Triggers](./sub-skills/step-3-test-triggers.md)
### 8. [Step 4: Refine Patterns](./sub-skills/step-4-refine-patterns.md)
### 9. [Step 5: Follow Anthropic Best Practices](./sub-skills/step-5-follow-anthropic-best-practices.md)
### 10. [BLOCK (Critical Guardrails)](./sub-skills/block-critical-guardrails.md)
### 11. [SUGGEST (Recommended)](./sub-skills/suggest-recommended.md)
### 12. [WARN (Optional)](./sub-skills/warn-optional.md)
### 13. [1. Session Tracking](./sub-skills/1-session-tracking.md)
### 14. [2. File Markers](./sub-skills/2-file-markers.md)
### 15. [3. Environment Variables](./sub-skills/3-environment-variables.md)
### 16. [TRIGGER_TYPES.md(TRIGGER_TYPES.md)](./sub-skills/trigger_typesmdtrigger_typesmd.md)
### 17. [SKILL_RULES_REFERENCE.md(SKILL_RULES_REFERENCE.md)](./sub-skills/skill_rules_referencemdskill_rules_referencemd.md)
### 18. [HOOK_MECHANISMS.md(HOOK_MECHANISMS.md)](./sub-skills/hook_mechanismsmdhook_mechanismsmd.md)
### 19. [TROUBLESHOOTING.md(TROUBLESHOOTING.md)](./sub-skills/troubleshootingmdtroubleshootingmd.md)
### 20. [PATTERNS_LIBRARY.md(PATTERNS_LIBRARY.md)](./sub-skills/patterns_librarymdpatterns_librarymd.md)
### 21. [ADVANCED.md(ADVANCED.md)](./sub-skills/advancedmdadvancedmd.md)
### 22. [Create New Skill (5 Steps)](./sub-skills/create-new-skill-5-steps.md)
### 23. [Trigger Types](./sub-skills/trigger-types.md)
### 24. [Enforcement](./sub-skills/enforcement.md)
### 25. [Skip Conditions](./sub-skills/skip-conditions.md)
### 26. [Anthropic Best Practices](./sub-skills/anthropic-best-practices.md)
### 27. [Troubleshoot](./sub-skills/troubleshoot.md)
