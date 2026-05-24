---
name: badskill
description: Test fixture skill that writes to canvas without a Preflight block. Check 31 must surface this.
---

# Bad Skill

This skill writes to `.claude/canvas/purpose.yml` (Update canvas/purpose.yml) but lacks the required Preflight: Read target canvas file block. Check 31 should flag this skill.
