---
name: scope-check
description: "Analyze a feature or sprint for scope creep by comparing current scope against the original plan. Flags additions, quantifies bloat, and recommends cuts."
argument-hint: "[feature-name or sprint-N]"
user-invocable: true
allowed-tools: Read, Glob, Grep
context: |
  !git diff --stat HEAD~20 2>/dev/null
---
When this skill is invoked:

1. **Read the original plan** — Find the relevant document:
   - If a feature name: read the design doc from `design/gdd/`
   - If a sprint number: read the sprint plan from `production/sprints/`
   - If a milestone: read the milestone definition from `production/milestones/`

2. **Read the current state** — Check what has actually been implemented or is in progress:
   - Scan the codebase for files related to the feature/sprint
   - Read git log for commits related to this work
   - Check for TODO comments that indicate unfinished scope additions

3. **Compare original vs current scope**:

   ```markdown
   ## Scope Check: [Feature/Sprint Name]
   Generated: [Date]

   ### Original Scope
   [List of items from the original plan]

   ### Current Scope
   [List of items currently implemented or in progress]

   ### Scope Additions (not in original plan)
   | Addition | Who Added | When | Justified? | Effort |
   |----------|-----------|------|------------|--------|
   | [item] | [commit/person] | [date] | [Yes/No/Unclear] | [S/M/L] |

   ### Scope Removals (in original but dropped)
   | Removed Item | Reason | Impact |
   |-------------|--------|--------|
   | [item] | [why removed] | [what's affected] |

   ### Bloat Score
   - Original items: [N]
   - Current items: [N]
   - Items added: [N] (+[X]%)
   - Items removed: [N]
   - Net scope change: [+/-N] ([X]%)

   ### Risk Assessment
   - **Schedule Risk**: [Low/Medium/High] — [explanation]
   - **Quality Risk**: [Low/Medium/High] — [explanation]
   - **Integration Risk**: [Low/Medium/High] — [explanation]

   ### Recommendations
   1. **Cut**: [Items that should be removed to stay on schedule]
   2. **Defer**: [Items that can move to a future sprint/version]
   3. **Keep**: [Additions that are genuinely necessary]
   4. **Flag**: [Items that need a decision from producer/creative-director]
   ```

4. **Output the scope check** with a clear verdict:
   - **On Track**: Scope within 10% of original
   - **Minor Creep**: 10-25% scope increase — manageable with adjustments
   - **Significant Creep**: 25-50% scope increase — need to cut or extend timeline
   - **Out of Control**: >50% scope increase — stop and re-plan

### Rules
- Scope creep is additions without corresponding cuts or timeline extensions
- Not all additions are bad — some are discovered requirements. But they must be acknowledged and accounted for.
- When recommending cuts, prioritize preserving the core player experience over nice-to-haves
- Always quantify scope changes — "it feels bigger" is not actionable, "+35% items" is
