---
name: report-phase
description: Final reporting and sign-off workflow. Spawns business-analyst for PRD completion verification, project-manager to consolidate results into executive report with metrics and recommendations. Use when finalizing and summarizing workflow results.
---

# Report Phase - Sign-off & Consolidation

> **ROOT AGENT ONLY** - Called by commands only, never by subagents.

**Purpose:** Validate PRD completion and generate final report
**Trigger:** After validation-phase completes
**Input:** PRD path, architecture, worker results, validation results, complexity, scope
**Output:** Executive report with sign-off status

---

## Workflow Steps

1. **Spawn business-analyst agent (sign-off mode):**
   - Compare PRD requirements vs delivered results
   - Verify success criteria met
   - Check for gaps or incomplete items
   - Return: completion %, success criteria status, gaps, recommendation

2. **Spawn project-manager agent (consolidation mode):**
   - Aggregate all worker results
   - Calculate metrics (tasks, files, compliance %)
   - Generate executive summary (1-2 sentences)
   - Compile prioritized recommendations
   - Return: markdown-formatted report

3. **If files were modified:** Spawn agent to execute `repomix-cache-refresh` skill:

   ```
   subagent_type="general-purpose"
   Prompt: "Execute /skill repomix-cache-refresh"
   ```

4. **Output:** Executive report formatted for /audit or /build

---

## BA Sign-off Assessment

```
{
  requirementsMet: "95%",
  successCriteria: "all met",
  gaps: ["Optional item not implemented"],
  recommendation: "Sign-off approved"
}
```

---

## Report Output by Command

**For /audit:**

- Compliance %, status by domain, critical/warning recommendations

**For /build:**

- Implementation summary table, files modified, validation results, next steps

Both include:

- Executive summary
- Sign-off status
- Metrics
- Prioritized recommendations

---

## Configuration

| Setting | Value    | Rationale              |
| ------- | -------- | ---------------------- |
| Format  | Markdown | Standard documentation |

---

## Integration

**Called by:** /audit, /build, /ms (complexity ≥15)
**Calls:** business-analyst (sign-off mode), project-manager (consolidation mode), repomix-cache-refresh skill
**Next phase:** None (final phase)

---

## Example

```
/build JWT Authentication API

Previous Phases Complete:
  PRD: /docs/epics/in-progress/msm-jwt-auth-api/prd.md
  Architecture: AuthController, AuthService, TokenService
  Worker Results: 4 tasks, 6 files modified
  Validation: All checks passed

Report Phase (this skill):
  → BA (sign-off): 100% requirements met, no gaps, approve
  → PM (consolidation): Generate executive report
  → Repomix cache refresh (6 files modified)

Output:
  # JWT Authentication API Build Report

  Successfully implemented with login, logout, token refresh.
  Requirements Met: 100%, Deliverables: Complete
  Files Modified: 6

  Recommendations: Add rate limiting, improve docs
  Next Steps: Code review, deploy to staging
```
