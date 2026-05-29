---
name: innovate-phase
description: Analyze PRD for innovation opportunities, present each with HITL selection loop (Implement/Skip/More Details), update PRD with selections. Use when /architect workflow reaches innovation phase after vibe-check. Always runs for /architect (unlike /build where innovation is optional).
---

# Innovate Phase - PRD Enhancement with HITL Selection

> **ROOT AGENT ONLY** - Called by /architect command exclusively.

**Purpose:** Analyze PRD for enhancements, walk through each innovation with HITL, update PRD with selections
**Trigger:** After vibe-check passes (/architect workflow only)
**Input:** PRD path, complexity, scope
**Output:** PRD updated with user-selected innovations

---

## Key Differences: /architect vs /build

| Aspect         | /architect (this skill)   | /build                      |
| -------------- | ------------------------- | --------------------------- |
| **Innovation** | ALWAYS runs               | OPTIONAL (user asked first) |
| **PRD State**  | Already exists (from req) | Written during innovate     |
| **HITL Stop**  | Always proceeds (no ask)  | Asks user before starting   |
| **Purpose**    | Planning & exploration    | Execution optimization      |
| **Depth**      | Deep analysis required    | Standard analysis           |

---

## Workflow Steps

### Phase 1: Spawn Innovation Advisor

1. **Read existing PRD** (already exists from requirements-phase, passed vibe-check)
2. **Spawn innovation-advisor agent** with PRD content, path, complexity, scope
3. **Agent returns structured innovations** (JSON, max 5-7) - see innovation-advisor agent for output format

---

### Phase 2: Interactive Innovation Review

**For EACH innovation (one at a time):**

4. **Display 1-page summary** (see templates/innovation-summary.md):
   - Title with [RECOMMENDED] or [OPTIONAL] tag
   - Impact/Effort/Category/Industry Standard
   - One-pager description
   - Key benefits (3 bullets)
   - Recommendation reason

5. **Use AskUserQuestion for HITL selection:**

   If `recommended: true`:
   - "Implement (Recommended)" - {recommendationReason}
   - "Skip"
   - "More Details"

   If `recommended: false`:
   - "Implement"
   - "Skip (Recommended)" - {recommendationReason}
   - "More Details"

6. **Handle response:**
   - **Implement** → Add to selectedInnovations, continue to next
   - **Skip** → Continue to next
   - **More Details** → Show detailed explanation (see templates/innovation-details.md), then ask again (Implement/Skip only)

7. **Repeat for all innovations**

---

### Phase 3: Apply Selections

8. **Update PRD** with selected innovations (if any):
   - Add as new section in PRD
   - Include: title, rationale, implementation notes

9. **Summary to user:**
   - Innovations reviewed: {total}
   - ✅ Implemented: {list}
   - ⏭️ Skipped: {list}
   - PRD updated with {count} innovations

10. **Return control** to /architect command → Continue to design-phase

---

## Output Format

```json
{
  "status": "complete",
  "prdPath": "docs/epics/in-progress/msm-feature/prd.md",
  "totalInnovations": 4,
  "innovationsImplemented": [
    { "id": 1, "title": "Add OpenAPI Documentation" },
    { "id": 3, "title": "Implement Rate Limiting" }
  ],
  "innovationsSkipped": [
    { "id": 2, "title": "Add MFA" },
    { "id": 4, "title": "Audit Logging" }
  ]
}
```

---

## Example Interaction

```
[Vibe check passes → Innovate phase starts]
[innovation-advisor returns 4 innovations]

Innovation 1 of 4: Add OpenAPI Documentation [RECOMMENDED]
Impact: High | Effort: Low
[User: Implement]

Innovation 2 of 4: Rate Limiting [RECOMMENDED]
[User: Implement]

Innovation 3 of 4: MFA [OPTIONAL]
[User: Skip]

Innovation 4 of 4: Audit Logging [OPTIONAL]
[User: More Details → detailed view → Skip]

Innovation Phase Complete
✅ Implemented: OpenAPI, Rate Limiting
⏭️ Skipped: MFA, Audit Logging
```

---

## Integration

**Called by:** /architect command exclusively
**Calls:** innovation-advisor agent, AskUserQuestion
**Separate from:** /build (different logic), /audit (different focus)
**Previous phase:** vibe-check
**Next phase:** design-phase (architect-phase)

---

## Notes

- ALWAYS runs for /architect (no "want to innovate?" HITL stop)
- PRD already exists (from requirements-phase, validated by vibe-check)
- HITL per innovation (user decides individually)
- More Details loop available (full explanation before deciding)
- Updates PRD in place (selected innovations added to existing file)
- Deep analysis mode (higher reasoning required)
