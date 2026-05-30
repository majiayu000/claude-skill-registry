---
name: goodskill
description: Test fixture skill that writes to canvas AND carries the Preflight block. Check 31 must pass.
---

# Good Skill

This skill writes to `.claude/canvas/purpose.yml` (Update canvas/purpose.yml).

## Preflight: Read target canvas file

Before any canvas write, this skill reads the target file first per the Read-before-Write hard rule (anti-pattern #7 instance #5 prevention).

```
Read .claude/canvas/purpose.yml (limit: 1 for Edit, full Read for Write)
```

Then proceeds with the write.
