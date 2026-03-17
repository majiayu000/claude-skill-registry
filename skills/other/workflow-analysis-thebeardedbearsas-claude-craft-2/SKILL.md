---
name: workflow-analysis
description: Workflow d'Analyse Obligatoire. Use when working with workflow analysis.
triggers:
  files: []
  keywords: ["analyze", "analysis", "impact", "change", "modify", "implement", "feature", "bugfix"]
auto_suggest: true
---

# Workflow d'Analyse Obligatoire

This skill enforces mandatory analysis before any code modification.

See @REFERENCE.md for detailed documentation.

## Quick Reference

### Before ANY Change

1. **Understand**: Clear objective + acceptance criteria
2. **Analyze**: Read affected files + dependencies
3. **Document**: Files, impacts, risks, approach
4. **Validate**: User approval if medium/high impact
5. **TDD**: Write tests FIRST

### Impact Levels

| Impact | Action |
|--------|--------|
| Low (1 file, < 1h) | Proceed |
| Medium (2-5 files, migration) | Validate with user |
| High (> 5 files, breaking changes) | Detailed plan required |
