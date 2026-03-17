---
name: skill-evolution-tracker
description: Track skill changes, improvements, and evolution over time. Task-based operations for version tracking, change documentation, impact measurement, and evolution analysis. Use when tracking skill versions, documenting changes over time, measuring improvement impact, or analyzing how skills evolved.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Skill Evolution Tracker

## Overview

skill-evolution-tracker documents and analyzes how skills change and improve over time, providing visibility into evolution patterns and improvement effectiveness.

**Purpose**: Track and understand skill evolution for continuous improvement insights

**The 4 Tracking Operations**:
1. **Version Tracking** - Document skill versions and changes
2. **Change Documentation** - Record what changed and why
3. **Impact Measurement** - Quantify improvement effects
4. **Evolution Analysis** - Identify patterns in how skills evolve

## When to Use

- After skill updates (document changes)
- Version releases (track versions)
- Analyzing improvement effectiveness
- Understanding skill maturity
- Identifying evolution patterns

## Operations

### Operation 1: Version Tracking

**Purpose**: Maintain version history for skills

**Process**:
1. Assign version numbers (semver: v1.0, v1.1, v2.0)
2. Document version in YAML frontmatter
3. Track major changes per version
4. Maintain changelog

**Format**:
```markdown
## Version History

### v1.1 (2025-11-07)
- Added Quick Reference section
- Enhanced examples in Operations
- Fixed validation criteria

### v1.0 (2025-10-15)
- Initial release
```

---

### Operation 2: Change Documentation

**Purpose**: Record what changed, why, and impact

**Process**:
1. List all changes made
2. Explain rationale for each
3. Note expected impact
4. Document validation results

**Format**:
```markdown
### Change: Added Quick Reference

**Rationale**: User experience improvement, easier memory refresh
**Changes**: Added Quick Reference section (96 lines)
**Impact**: Improved usability, 100% Quick Ref coverage
**Validation**: Passed structure validation, Quick Ref detected
```

---

### Operation 3: Impact Measurement

**Purpose**: Quantify effectiveness of improvements

**Metrics**:
- Quality score changes (before/after review-multi scores)
- Usage frequency changes
- User satisfaction changes
- Efficiency improvements

**Example**:
```
Impact Measurement: Quick Reference Addition

Before:
- Quick Reference: 4 of 7 skills (57%)
- User feedback: "Hard to refresh memory"

After:
- Quick Reference: 7 of 7 skills (100%)
- Validation: All pass Quick Ref check
- Impact: Improved UX, consistency

Quantified:
- Coverage: 57% → 100% (+43%)
- Time to refresh: ~30min → ~5min (-83%)
```

---

### Operation 4: Evolution Analysis

**Purpose**: Identify patterns in skill evolution

**Process**:
1. Review version histories
2. Identify common evolution patterns
3. Understand what drives changes
4. Extract meta-learnings

**Example Patterns**:
- Skills often add Quick Reference in v1.1
- Examples get refined/made concrete
- Validation criteria become more specific over time

---

## Quick Reference

| Operation | Focus | Output |
|-----------|-------|--------|
| Version Tracking | Version numbers, changelog | Version history |
| Change Documentation | What/why/impact of changes | Change log |
| Impact Measurement | Quantify improvements | Metrics, evidence |
| Evolution Analysis | Patterns across skills | Meta-learnings |

**Integration**: best-practices-learner (uses evolution insights for learnings)

---

**skill-evolution-tracker provides visibility into how skills improve over time, enabling data-driven understanding of what makes skills better.**
