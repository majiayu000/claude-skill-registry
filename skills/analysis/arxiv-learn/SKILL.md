---
name: arxiv-learn
description: >
  INTERNAL MODULE - Use `arxiv learn` instead.
  This module provides the learn pipeline implementation for the arxiv skill.
internal: true
triggers: []
metadata:
  short-description: Internal module for arxiv learn command
---

# Arxiv-Learn (Internal Module)

**Do not use this skill directly.** Use `arxiv learn` instead:

```bash
.pi/skills/arxiv/run.sh learn 2601.08058 --scope memory --context "agent systems"
```

This module provides the implementation for the `arxiv learn` command pipeline:
1. Find/download paper
2. Distill Q&A pairs
3. Human review (interview)
4. Store to memory
5. Schedule edge verification

See the main [arxiv skill](../arxiv/SKILL.md) for documentation.
