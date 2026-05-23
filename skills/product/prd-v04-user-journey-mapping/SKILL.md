---
name: prd-v04-user-journey-mapping
description: Map user missions from trigger to value moment, organizing features into coherent paths during PRD v0.4 User Journeys. Triggers on requests to map user journeys, define user flows, describe how users accomplish goals, or when user asks "map user journeys", "define user flows", "user missions", "how do users accomplish X?", "journey mapping", "what steps do users take?", "pain to value flow". Consumes PER- (Persona Definition), FEA- (Feature Value Planning), KPI- (Outcome Definition). Outputs UJ- entries with step flows, pain points, and value moments. Feeds v0.4 Screen Flow Definition.
---

# User Journey Mapping

Position in workflow: v0.4 Persona Definition → **v0.4 User Journey Mapping** → v0.4 Screen Flow Definition

User journeys transform features into paths. A journey answers: "How does [persona] go from [trigger] to [value moment] using [features]?"

## Journey Types

| Type | Purpose | Priority Signal | Example |
|------|---------|-----------------|---------|
| **Core** | Primary value delivery | Must complete for activation | First report generated |
| **Onboarding** | First-time user setup | Blocks all other journeys | Account creation → first action |
| **Recovery** | Error handling, support | Retention protection | Password reset, billing issue |
| **Power User** | Advanced workflows | Expansion/upsell | Bulk operations, integrations |

**Rule**: Define Onboarding first (it gates everything), then Core journeys (they deliver KPI-), then others.

## Journey Anatomy

Every journey has:

1. **Trigger** — What causes the user to start? (Event, not "opens app")
2. **Steps** — Actions linked to FEA- features
3. **Pain Points** — Where friction exists (design around these)
4. **Moment of Value** — When user achieves goal (this drives KPI-)

## Mapping Process

1. **Pull PER-** (personas) from Persona Definition
   - Each journey belongs to a specific persona

2. **Pull FEA-** (features) and KPI- (outcomes) from v0.3
   - Features are the building blocks of journey steps
   - KPIs tell you which journeys matter most

3. **Define trigger events**
   - What causes the user to start this journey?
   - Be specific: "Receives calendar invite" not "opens app"

4. **Map step flow using features**
   - Each step = an action the user takes
   - Link each step to the FEA- that enables it

5. **Identify pain points**
   - Where might the user get confused, frustrated, or blocked?
   - These inform UX design decisions

6. **Mark "moments of value"**
   - When does the user get the payoff?
   - This should tie to KPI- measurement

7. **Create UJ- entries** with full traceability

## UJ- Output Template

```
UJ-XXX: [Journey Title]
Persona: [PER-XXX]
Type: [Core | Onboarding | Recovery | Power User]
Trigger: [Event that initiates journey]
Goal: [What user wants to accomplish]

Steps:
  1. [Action] → FEA-XXX
  2. [Action] → FEA-XXX
  3. [Action] → FEA-XXX
  ...

Pain Points:
  - [Step X]: [Potential friction — e.g., "requires context switch"]
  - [Step Y]: [Potential friction]

Moment of Value: [When user achieves goal — be specific]
KPI Link: [KPI-XXX this journey drives]
Success Metric: [How we measure journey completion]
Dependencies: [BR-XXX constraints, API-XXX if known]
```

**Example UJ- entry:**
```
UJ-001: First Report Generation
Persona: PER-001 (Overwhelmed Ops Manager)
Type: Core
Trigger: User completes onboarding and sees empty dashboard
Goal: Generate first automated report to see time-saving value

Steps:
  1. Click "Create Report" → FEA-003 (one-click reports)
  2. Select data source → FEA-001 (auto-sync)
  3. Choose report template → FEA-008 (templates)
  4. Preview report → FEA-003
  5. Export/share report → FEA-009 (export)

Pain Points:
  - Step 2: User may not have connected data source yet (dependency on UJ-002)
  - Step 3: Template overload if too many choices

Moment of Value: Seeing the completed report with their actual data
KPI Link: KPI-002 (activation rate)
Success Metric: Time from "Create Report" click to export ≤ 5 minutes
Dependencies: BR-015 (data format rules), UJ-002 (data source connection)
```

## Feature-to-Journey Validation

After mapping journeys, validate:

- [ ] **No orphaned features**: Every FEA- appears in at least one UJ-
- [ ] **No journey gaps**: Every step has a FEA- that enables it
- [ ] **KPI coverage**: Core journeys tie to Tier 1/2 KPIs

If a FEA- isn't in any journey, either:
1. Add it to a journey (you missed a use case), or
2. Cut it from scope (it's not needed)

## Journey Sequencing

Map dependencies between journeys:

```
UJ-000: Onboarding (gates all)
    ↓
UJ-001: First Report (Core) ← KPI-002 (activation)
    ↓
UJ-002: Data Source Connection (Core) ← KPI-003 (depth)
    ↓
UJ-003: Team Invite (Power User) ← KPI-004 (expansion)
```

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Feature-first journeys** | Steps = feature list dumped in order | Start with user goal, then map features to it |
| **No trigger** | "User opens app" | Define specific event: "receives notification" |
| **No value moment** | Journey ends without payoff | Each journey needs clear outcome |
| **Orphaned features** | FEA- not in any journey | Add to journey or cut from scope |
| **Generic personas** | "User does X" | Specify PER-: "PER-001 does X" |
| **Happy path only** | No pain points identified | Anticipate where users struggle |
| **Mega-journeys** | 15+ steps | Split into sub-journeys |

## Quality Gates

Before proceeding to Screen Flow Definition:

- [ ] Onboarding journey defined first
- [ ] All Core journeys mapped to KPI-
- [ ] Every FEA- appears in at least one journey
- [ ] Every journey has a specific trigger (not "opens app")
- [ ] Pain points identified for friction design
- [ ] Journey dependencies documented

## Downstream Connections

UJ- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.4 Screen Flow Definition** | Steps become screens | UJ-001 Step 3 → SCR-005 |
| **v0.6 Technical Specification** | Journeys inform API sequences | UJ-001 → API-001, API-002 flow |
| **v0.7 Test Planning** | Journeys become E2E tests | TEST-020 validates UJ-001 |
| **v0.9 GTM** | Journey-based onboarding messaging | "Complete [UJ-001] in 5 minutes" |

## Detailed References

- **Journey mapping examples**: See `references/examples.md`
- **UJ- entry template**: See `assets/uj.md`
- **Journey sequencing guide**: See `references/sequencing.md`
