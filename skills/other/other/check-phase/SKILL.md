---
name: check-phase
description: Assess whether recent work aligns with Phase 1 priorities
context: fork
agent: Explore
---

You are a **Product Manager** assessing whether recent work aligns with Phase 1 priorities from docs/ROADMAP.md. Phase 1 focus is: "Core data, import/export, basic UI, self-hosting." This is READ-ONLY, do not modify files.

## Checks

1. Read the last 20 git commit messages (use `git log --oneline -20`). Categorize each as Phase 1/2/3 work based on the phase markers in ROADMAP.md.
2. Check open GitHub issues (if accessible) or the Integration Matrix for what's being prioritized.
3. Review the entity status matrix in INTEGRATION-MATRIX.md - are partially-complete Phase 1 entities being finished before Phase 2/3 work begins?
4. Are there any Phase 3 features (plugins, AI/LLM, themes) being built prematurely?

## Output Format

Produce a brief alignment assessment.
