---
name: prd-v04-persona-definition
description: Synthesize behavioral personas from prior stage evidence for journey mapping and marketing during PRD v0.4 User Journeys. Triggers on requests to define personas, create user profiles, identify target users, or when user asks "who are our users?", "define personas", "user profiles", "target users", "persona creation", "who uses this product?". Consumes CFD- (v0.1-v0.3), BR- (targeting from v0.3 Moat), FEA- (v0.3 Feature Value Planning). Outputs PER- entries with behavioral profiles and feature relationships. Feeds v0.4 User Journey Mapping.
---

# Persona Definition

Position in workflow: v0.3 Feature Value Planning → **v0.4 Persona Definition** → v0.4 User Journey Mapping

Personas are not demographic profiles—they are behavioral models synthesized from evidence. Every persona must trace back to CFD- research, BR- targeting rules, and FEA- features they care about.

## Core Constraint

**Maximum 5 personas. Most products need 1-2.**

If you have more than 3, you're likely over-segmenting by demographics instead of behavior. Consolidate ruthlessly.

## Persona Types

| Type | Definition | When to Create |
|------|------------|----------------|
| **Primary** | Core user, drives most revenue | Always (at least 1) |
| **Secondary** | Important but not primary buyer | If distinct needs exist |
| **Negative** | Who we explicitly exclude | If exclusion is strategic |
| **Aspirational** | Future target, not current focus | Only for roadmap planning |

**Rule**: Primary personas must link to primary revenue KPI-. If a persona doesn't influence revenue, question whether it's truly primary.

## Evidence Requirements

Every persona field must link to prior stage evidence:

| Persona Field | Must Link To | Source Stage |
|---------------|--------------|--------------|
| Goals | CFD- value hypothesis | v0.1 User Value Articulation |
| Frustrations | CFD- pain points | v0.1 Problem Framing |
| Decision Factors | CFD- competitive research | v0.2 Competitive Landscape |
| Key Features | FEA- entries | v0.3 Feature Value Planning |
| Pricing Sensitivity | BR- pricing rules | v0.3 Pricing Model |
| Acquisition Channel | BR- targeting rules | v0.3 Moat Definition |

**No link = No claim.** If you can't cite evidence, the attribute is assumption, not fact.

## Synthesis Process

1. **Pull USER TYPE** from v0.1 Problem Framing (CFD-)
   - These are your candidate personas

2. **Pull SEGMENTS** from v0.2 Market Definition (CFD-, BR-)
   - How is the market divided? Which segments are we targeting?

3. **Pull TARGETING RULES** from v0.3 Moat Definition (BR-)
   - New-to-category vs. Switchers? Trigger moments?

4. **Synthesize behavioral patterns** from all CFD- evidence
   - What goals unite this segment?
   - What frustrations are consistent?

5. **Map FEA- features** to each persona
   - Which features matter most to each?
   - This informs journey mapping

6. **Create PER- entries** with full traceability

## PER- Output Template

```
PER-XXX: [Persona Name]
Source IDs: [CFD-XXX, CFD-YYY, BR-ZZZ that inform this persona]
Type: [Primary | Secondary | Negative | Aspirational]
Segment: [From v0.2 market segment]

Demographics:
  Role: [Job title / function]
  Context: [Company size, industry, team structure]
  Technical Level: [Novice | Intermediate | Expert]

Behavioral Profile:
  Goals: [What they're trying to achieve — link to CFD- value]
  Frustrations: [Current pain points — link to CFD- pain]
  Decision Factors: [What influences their choices — link to CFD- research]
  Current Workflow: [How they solve this today]

Product Relationship:
  Primary Value: [CFD- value hypothesis they care about most]
  Key Features: [FEA-XXX, FEA-YYY most relevant to them]
  Pricing Sensitivity: [From BR- pricing rules]
  Acquisition Channel: [How they'll find us — from BR- targeting]

Marketing Hook: [One-sentence pitch for this persona]
```

**Example PER- entry:**
```
PER-001: The Overwhelmed Ops Manager
Source IDs: CFD-003 (pain: manual tracking), CFD-012 (value: automation), BR-041 (target: switchers at renewal)
Type: Primary
Segment: SMB SaaS companies (10-50 employees)

Demographics:
  Role: Operations Manager / Head of Ops
  Context: Growing startup, wearing multiple hats, no dedicated tools budget
  Technical Level: Intermediate (comfortable with SaaS, not a developer)

Behavioral Profile:
  Goals: Reduce time spent on manual reporting (CFD-012)
  Frustrations: Current tools require too much setup (CFD-003)
  Decision Factors: Ease of use > feature count, must show ROI to CEO (CFD-025)
  Current Workflow: Spreadsheets + manual data entry + weekly report compilation

Product Relationship:
  Primary Value: CFD-012 ("Save 5 hours/week on reporting")
  Key Features: FEA-001 (auto-sync), FEA-003 (one-click reports), FEA-007 (dashboard)
  Pricing Sensitivity: BR-030 (SMB tier ≤$50/mo)
  Acquisition Channel: BR-041 (target at contract renewal of competing tools)

Marketing Hook: "Stop building reports. Start using them."
```

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Persona explosion** | >5 personas | Consolidate by behavior, not demographics |
| **Fictional personas** | No CFD- links | Every attribute needs evidence |
| **Demographic-only** | "25-35 year old male" | Focus on behaviors and goals |
| **All personas are primary** | "Everyone is important" | Rank by revenue potential |
| **Copy-paste from competitors** | Generic descriptions | Ground in YOUR research |
| **Features without personas** | Personas created but no FEA- links | Map features to who cares |

## Quality Gates

Before proceeding to User Journey Mapping:

- [ ] Maximum 5 personas (ideally 1-3)
- [ ] At least one Primary persona defined
- [ ] Every persona has CFD- evidence links
- [ ] Key Features mapped from FEA- entries
- [ ] Acquisition Channel specified from BR- targeting
- [ ] Marketing Hook is specific and testable

## Downstream Connections

PER- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.4 User Journey Mapping** | Each UJ- references a PER- | UJ-001 is for PER-001 |
| **v0.4 Screen Flow Definition** | Persona context shapes UI | SCR-001 optimized for PER-001 tech level |
| **v0.9 GTM** | Marketing messaging per persona | Campaign targeting PER-002 segment |
| **Sales Enablement** | Persona-specific pitches | Discovery questions per PER- |

## Detailed References

- **Persona creation examples**: See `references/examples.md`
- **PER- entry template**: See `assets/per.md`
