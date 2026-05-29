---
name: resolve-conflict
tags:
  technology: [git]
  feature: [workflow]
  priority: medium
summary: Resolve git conflicts and disagreements between agents
version: 1
---

# Resolve Conflict

## When to use

- Git merge conflicts occur
- Agents have conflicting recommendations
- Multiple approaches need reconciliation

## Instructions

### Git Conflicts

1. Identify the conflict type:
   - Content conflict (same lines modified)
   - Structural conflict (file moved/deleted)
   - Dependency conflict (version mismatch)

2. Analyze both sides:
   - Understand intent of each change
   - Check which is more recent
   - Verify which aligns with requirements

3. Resolve appropriately:
   - Keep the correct version
   - Merge changes if both needed
   - Document the resolution

### Agent Disagreements

1. Compare assessments:
   - List points of agreement
   - Identify specific disagreements
   - Check confidence levels

2. Apply resolution rules:
   - Security issues: Cursor preferred (0.8 weight)
   - Architecture issues: Gemini preferred (0.7 weight)
   - Equal weight: Escalate to human

3. Document decision:
   - Record which assessment won
   - Note the reason
   - Save for future learning

## Resolution Commands

```bash
# See conflicts
git status

# View conflict markers
git diff

# Accept current (ours)
git checkout --ours <file>

# Accept incoming (theirs)
git checkout --theirs <file>

# Manual resolution then:
git add <file>
git commit
```
