---
name: site-reliability-engineer
description: Docusaurus build health validation and deployment safety for Claude Skills showcase. Pre-commit MDX validation (Liquid syntax, angle brackets, prop mismatches), pre-build link checking, post-build health reports. Activate on 'build errors', 'commit hooks', 'deployment safety', 'site health', 'MDX validation'. NOT for general DevOps (use deployment-engineer), Kubernetes/cloud infrastructure (use kubernetes-architect), runtime monitoring (use observability-engineer), or non-Docusaurus projects.
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
category: DevOps & Site Reliability
tags:
  - docusaurus
  - build-health
  - mdx
  - validation
  - deployment
pairs-with:
  - skill: devops-automator
    reason: CI/CD for site deployments
  - skill: skill-documentarian
    reason: Maintain skill documentation quality
---

# Site Reliability Engineer

Expert in Docusaurus build health, MDX validation, and deployment safety for the Claude Skills showcase website. Prevents common build failures through pre-commit validation and automated health checks.

## When to Use

**Use for:**
- Pre-commit validation of markdown/MDX files
- Catching Liquid template syntax errors
- Validating SkillHeader component props
- Checking for missing hero images/ZIP files
- Pre-build link validation
- Post-build health reports
- Diagnosing Docusaurus build failures

**Do NOT use for:**
- General DevOps (use deployment-engineer)
- Kubernetes/cloud infrastructure (use kubernetes-architect)
- Runtime monitoring/alerting (use observability-engineer)
- Database migrations (use database-migrations agents)
- Security scanning (use security-auditor)

## Core Problem Domain

### The 5 Recurring Anti-Patterns

| # | Problem | Symptom | Fix |
|---|---------|---------|-----|
| 1 | Liquid syntax in examples | Liquid templates break MDX | Wrap in backtick expression |
| 2 | Unescaped angle brackets | `&lt;70` parsed as HTML | Use `&lt;70` |
| 3 | Wrong SkillHeader props | SSG build failure | Use `fileName` not `skillId` |
| 4 | Missing critical files | Skill invisible on site | Add to `skills.ts` |
| 5 | Cache corruption | Phantom errors | Clear `.docusaurus`, `build` |

## Quick Start

### Install Hooks (One-Time)
```bash
npm run install-hooks
```

### Manual Validation
```bash
npm run validate:liquid    # Liquid syntax
npm run validate:brackets  # Angle brackets
npm run validate:props     # SkillHeader props
npm run validate:all       # All checks
```

### Clear Cache (When Stuck)
```bash
rm -rf .docusaurus build node_modules/.cache
npm run build
```

## Pre-Commit Validation

The pre-commit hook automatically:
1. **Liquid syntax** - Scans for double-brace templates outside code blocks
2. **Angle brackets** - Finds `<digit` patterns
3. **SkillHeader props** - Validates component usage
4. **Required files** - Checks hero images, ZIPs exist

**Speed**: Under 5 seconds for typical commits

## Expert vs Novice Approach

| Novice | Expert |
|--------|--------|
| Runs full build to check | Pre-commit catches 90% in 5 seconds |
| Manual cache clearing | Auto-detect cache issues |
| Ignores warnings | Zero-tolerance for broken links |
| Simple regex validation | Context-aware (skips code blocks) |

## Anti-Patterns

### Anti-Pattern: Full Build for Validation
**What it looks like**: `npm run build` to check for errors
**Why wrong**: Minutes vs seconds, slow feedback
**Instead**: `npm run validate:all` (under 30 seconds)

### Anti-Pattern: Ignoring Build Warnings
**What it looks like**: "Build succeeded, ship it!" (ignoring warnings)
**Why wrong**: Broken links = poor UX, tech debt
**Instead**: Post-build validation fails on warnings

### Anti-Pattern: Naive Regex Validation
**What it looks like**: `/\{\{.*?\}\}/` (matches in code blocks too)
**Why wrong**: False positives in code examples
**Instead**: Track code block state, skip protected regions

## Scripts (in `scripts/` folder)

| Script | Purpose |
|--------|---------|
| `validate-liquid.js` | Detect unescaped Liquid syntax |
| `validate-brackets.js` | Detect unescaped angle brackets |
| `validate-skill-props.js` | Validate SkillHeader component |

## Troubleshooting Quick Reference

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Hook not running | `ls -la .git/hooks/pre-commit` | `chmod +x` or reinstall |
| False positives | Pattern in code block | Check ``` markers |
| Slow validation | `time npm run validate:all` | Optimize glob patterns |

## Success Metrics

After installing hooks:
- **Build failure rate**: 15% → under 2%
- **Time to diagnose errors**: 10 min → under 1 min
- **Validation speed**: Under 30 seconds

## Reference Files

- `references/validation-logic.md` - Context-aware detection patterns
- `references/ci-cd-integration.md` - GitHub Actions, health reports
- `scripts/` - Working validation scripts

---

**Prevents**: Liquid errors | Angle bracket failures | Prop mismatches | Missing assets | Broken links

**Use with**: skill-documentarian (sync) | docusaurus-expert (advanced config)
