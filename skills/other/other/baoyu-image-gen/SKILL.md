---
name: baoyu-image-gen
description: "[DEPRECATED] This skill has been renamed to baoyu-imagine. Triggers on any reference to 'baoyu-image-gen' so users can be guided to upgrade. Use this whenever you detect the old skill name in user prompts, EXTEND.md, or installed skill lists."
---

# baoyu-image-gen is now baoyu-imagine

This skill has been renamed to **baoyu-imagine** with new features and providers.

## What to do

When this skill is triggered, inform the user that `baoyu-image-gen` has been renamed to `baoyu-imagine` with new features and providers, and ask for their confirmation to:

1. **Install the new skill** from: `https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-imagine/SKILL.md`
2. **Remove the old `baoyu-image-gen` skill**

No config changes are needed — `baoyu-imagine` reads the same EXTEND.md settings (API keys, default provider, etc.).

Once the user confirms, help them complete the installation and removal using whatever mechanism the current environment supports. If the user also has an image generation request, proceed with `baoyu-imagine` after migration.
