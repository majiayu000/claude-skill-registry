---
name: security-hygiene
description: >
  Security hygiene for GSD's self-modifying skill and agent system.
  Use this skill whenever: creating, editing, or deleting skill files
  (.claude/skills/, .claude/commands/), modifying agent definitions
  (.claude/agents/), working with YAML configuration or chipset files,
  handling JSONL observation data (.planning/patterns/), processing
  community-contributed skills or chipsets, any file path operations
  that could involve user input, or when installing/updating
  project-claude configuration. Also activates for discussions about
  skill-creator security, trust models, or content hygiene.
user-invocable: true
---

# Security Hygiene

## Security Philosophy

This is a self-modifying system. Security should work like a helpful companion, not an adversarial checkpoint — zen and the art of programming. Tools protect by default, guide by suggestion, block only when there is a real reason.

## Threat Surface

| Vector | Risk | Check |
|---|---|---|
| **Path traversal** | Skill names used in file paths could escape directory | Sanitize all skill names: alphanumeric, hyphens, underscores only. Reject `..`, `/`, `\`. |
| **YAML deserialization** | Unsafe YAML loading executes arbitrary code | Use safe parsing only (`yaml.safe_load` or equivalent). Never `yaml.load` with untrusted input. |
| **Data poisoning** | Append-only JSONL could contain injected entries | Validate entries on read: check schema, reject oversized entries, verify timestamps are monotonic. |
| **Permission bypass** | Automated workflows might skip user confirmation | **Never bypass user confirmation for skill application**, even in YOLO mode. YOLO applies to GSD workflow commands, not skill modifications. |
| **Cross-project leakage** | User-level skills might expose project-specific patterns | User-level skills must be generic. Project-specific patterns stay in project-level skills. |
| **Observation privacy** | Pattern data could leak into shared repos | `.planning/patterns/` must be in `.gitignore`. Verify on any git operation. |

## Content Hygiene Rules

When processing community-contributed content (skills, chipsets, LoRA adapters):
- Check for embedded commands or script execution
- Verify YAML does not contain unsafe tags (`!!python/object`, etc.)
- Validate that skill descriptions match their actual content
- Quarantine new community content for review before activation

## The Staging Layer Principle

"The user's ability to work should be reasonable. Security should also be reasonable. We strive for the clean intersection." Do not over-alert. Do not create friction for normal operations. Surface findings only when something genuinely warrants attention.
