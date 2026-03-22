---
name: audit-full
description: Full audit — launches all 6 audit skills in parallel, produces unified report
context: fork
---

# Full Audit Orchestrator

You are an **Engineering Director** orchestrating a comprehensive audit of the my-family codebase by delegating to 6 specialized auditors in parallel, then aggregating their findings into a unified report.

## What to Do

### Step 1: Launch All 6 Audits in Parallel

Use the Task tool to launch these 6 subagents simultaneously. Each should use `subagent_type: Explore` and work from the repository root `/Users/chris/devel/home/my-family/`.

**Launch these 6 agents in a single message (parallel):**

1. **Architecture Audit** — Read `.claude/skills/audit-architect/SKILL.md` and execute its instructions. Return the full audit report.

2. **Domain/Genealogy Audit** — Read `.claude/skills/audit-domain/SKILL.md` and execute its instructions. Return the full audit report.

3. **Security Audit** — Read `.claude/skills/audit-security/SKILL.md` and execute its instructions. Return the full audit report.

4. **Go Idioms Audit** — Read `.claude/skills/audit-go/SKILL.md` and execute its instructions. Return the full audit report.

5. **Frontend Audit** — Read `.claude/skills/audit-frontend/SKILL.md` and execute its instructions. Return the full audit report.

6. **Test Quality Audit** — Read `.claude/skills/audit-tests/SKILL.md` and execute its instructions. Return the full audit report.

### Step 2: Aggregate Results

Once all 6 agents complete, produce a unified report.

## Output Format

### Full Audit Report

**Date**: [current date]
**Scope**: Architecture, Domain, Security, Go, Frontend, Tests

#### Executive Summary

2-3 sentences on overall codebase health.

#### Summary Dashboard

| Audit | Overall | Key Finding |
|-------|---------|-------------|
| Architecture | [avg score] | [one-liner] |
| Domain | [avg score] | [one-liner] |
| Security | [avg score] | [one-liner] |
| Go Idioms | [avg score] | [one-liner] |
| Frontend | [avg score] | [one-liner] |
| Tests | [avg score] | [one-liner] |

#### Critical & High Findings (Cross-Audit)

Deduplicate and merge findings from all 6 audits. List only Critical and High severity items, ordered by impact:

For each:
- **Source Audit**: Which audit(s) flagged this
- **Severity**: Critical / High
- **Finding**: One-sentence summary
- **Evidence**: File paths
- **Suggestion**: Concrete fix

#### Top 10 Issue-Ready Tickets

Deduplicated and prioritized across all 6 audits. Use the format:

```
**Title**: [imperative verb] [thing]
**Source**: [which audit(s)]
**Description**: [1-2 sentences]
**Acceptance Criteria**:
- [ ] [specific, testable criterion]
**Affected Files**: [list]
```

#### What's Going Well

List 3-5 strengths identified across the audits. Morale matters.

#### Detailed Audit Reports

Include the full report from each of the 6 audits below, separated by `---`.
