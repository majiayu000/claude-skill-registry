---
name: validate-idea
description: "Validate idea/project structure, documentation completeness, and readiness for next phase"
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob, Grep
---

# /validate-idea

Comprehensive validation of an idea's documentation structure and readiness.

## Usage

```bash
/validate-idea coordinatr       # Validate specific idea
/validate-idea yourbench        # Check another project
```

## Validation Checklist

### Required Files (Minimum Viable Idea)

| File | Required | Purpose |
|------|----------|---------|
| **README.md** | Yes | Status, overview, progress |
| **project-brief.md** | Yes | Vision, problem, audience, solution |

### Recommended Files (Phase-Dependent)

| File/Directory | When Needed | Purpose |
|----------------|-------------|---------|
| **critique.md** | Before planning | Risk assessment |
| **competitive-analysis.md** | Before MVP | Market positioning |
| **specs/** | Defining features | Technical specifications |
| **docs/adrs/** | Major tech decisions | Architecture Decision Records |
| **issues/** | In development | Work tracking |

## Phase-Aware Validation

**Concept Phase:**
- README + project-brief.md sufficient
- critique.md optional (recommend before planning)

**Planning Phase:**
- Should have critique.md
- Should have specs/ OR features/

**Development/Implementation Phase:**
- Must have specs/ (at least one)
- Must have issues/ with PLAN.md files
- Should have docs/adrs/ if major decisions made

## Execution Flow

### 1. Locate Project
```bash
ls ideas/[project-name]/
```

### 2. Check Required Files
- README.md: Has status, last updated date, progress
- project-brief.md: Vision, problem, audience, solution complete

### 3. Check Recommended Files (Phase-Aware)
Based on project phase in README.

### 4. Verify Consistency
- README status matches CLAUDE.md
- Brief aligns with README description
- Specs reference features
- Issues link to specs

### 5. Suggest Next Steps

| Current State | Suggested Next Step |
|---------------|---------------------|
| Just README | Run `/brief` |
| Has brief | Run `/critique` |
| Has critique | Run `/research` |
| Has research | Run `/spec` |
| Has specs | Run `/plan` + `/issue` |

## Validation Report

```markdown
# Validation Report: [Project Name]

## Status
- Current phase: [Concept / Planning / Development]
- Documentation completeness: X/Y files

## Required Files
✅ README.md - Complete
✅ project-brief.md - Complete

## Recommended Files
⚠️  critique.md - Missing (run /critique)
✅ specs/SPEC-001.md - Present

## Issues Found
1. README last updated is stale
2. Status mismatch with CLAUDE.md

## Recommendations
1. Update README last updated
2. Run /critique before specs

## Readiness Assessment
- Ready for specs: ⚠️ After fixing issues
- Ready for implementation: ❌ No specs yet
- Overall health: 7/10
```

## Readiness Criteria

### Ready for /spec
- project-brief.md complete
- critique.md present
- Key research done

### Ready for /plan + /implement
- At least one spec complete
- Acceptance criteria clear
- Technical decisions made

## When to Use

- Before starting spec work
- After long pause in project
- Monthly project health checks
- Before presenting to stakeholders
- When unsure what to do next

## Integration

```
/validate-idea → Fix issues → /validate-idea again → /spec or /plan
```
