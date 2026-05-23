---
name: Pfmea
description: Generate AIAG-VDA compliant Process FMEAs with proper Severity/Occurrence/Detection ratings, RPN calculations, and countermeasure recommendations. Covers MNMUK departments (Machine Shop, Damper, LVA, FML). USE WHEN user says 'PFMEA', 'FMEA', 'failure mode', 'risk analysis', 'RPN', 'severity occurrence detection', or 'process risk assessment'. Integrates with AutomotiveManufacturing, ControlPlan, and A3criticalthinking skills.
---

# Process FMEA (PFMEA)

## When to Activate This Skill
- "Create a PFMEA for [process]"
- "What are the failure modes for [operation]?"
- "Calculate RPN for [risk scenario]"
- "Rate severity/occurrence/detection for [failure]"
- "Identify process risks"
- "FMEA analysis for [part/process]"

## AIAG-VDA 7-Step Methodology

### Step 1: Planning and Preparation
- Define scope and boundaries
- Identify team members (cross-functional)
- Gather documentation (process flow, control plan, drawings)
- Review lessons learned from similar processes

### Step 2: Structure Analysis
- Define process steps from process flow diagram
- Create process tree (System > Sub-system > Process Element)
- Identify interfaces between steps
- Link to product characteristics

### Step 3: Function Analysis
- Define function of each process step
- Identify product/process requirements
- Link to customer/engineering specifications
- Document special characteristics (CC/SC)

### Step 4: Failure Analysis
- Identify failure modes (how can step fail to perform function?)
- Determine failure effects (consequences to customer/next operation)
- Identify failure causes (why would failure mode occur?)
- Chain: Cause → Failure Mode → Effect

### Step 5: Risk Analysis
- Rate Severity (S) of effects: 1-10
- Rate Occurrence (O) of causes: 1-10
- Rate Detection (D) of controls: 1-10
- Calculate Action Priority (AP) or RPN

### Step 6: Optimization
- Prioritize high-risk items
- Develop countermeasures (hierarchy: Eliminate > Substitute > Engineer > Admin > Detect)
- Assign responsibility and target dates
- Re-rate after countermeasures

### Step 7: Results Documentation
- Document all analysis
- Track countermeasure completion
- Update Control Plan linkage
- Archive for lessons learned

## Rating Scales (MNMUK Standard)

### Severity (S) - Effect on Customer/Process

| Rating | Criteria | MNMUK Examples |
|--------|----------|----------------|
| 10 | Affects safety without warning | Brake component failure, no containment possible |
| 9 | Affects safety with warning | Safety critical dimension OOS, detectable at assembly |
| 8 | Product inoperable, 100% scrap | Part cannot be reworked, total loss |
| 7 | Product operable but degraded, customer dissatisfied | Performance below spec, customer complaint |
| 6 | Product operable, comfort/convenience affected | Cosmetic defect, minor fit issue |
| 5 | 50% of product may need rework | Significant rework required |
| 4 | Product requires sorting/rework | Sorting operation needed |
| 3 | Minor rework at station | In-station repair possible |
| 2 | Slight inconvenience | Minor adjustment |
| 1 | No effect | No discernible impact |

### Occurrence (O) - Likelihood of Cause

| Rating | Failure Rate | Cpk Equivalent | MNMUK Examples |
|--------|--------------|----------------|----------------|
| 10 | Very high: ≥100/1000 | <0.33 | New process, no controls |
| 9 | High: 50/1000 | ≥0.33 | Known problem process |
| 8 | High: 20/1000 | ≥0.51 | Similar process had failures |
| 7 | Moderately high: 10/1000 | ≥0.67 | Occasional failures observed |
| 6 | Moderate: 2/1000 | ≥0.83 | Infrequent failures |
| 5 | Moderately low: 0.5/1000 | ≥1.00 | Controlled process, some failures |
| 4 | Low: 0.1/1000 | ≥1.17 | Well-controlled process |
| 3 | Very low: 0.01/1000 | ≥1.33 | Capable and controlled |
| 2 | Remote: 0.001/1000 | ≥1.50 | Proven design and controls |
| 1 | Nearly impossible: ≤0.001/1000 | ≥1.67 | Failure eliminated by design |

### Detection (D) - Ability to Detect Before Customer

| Rating | Detection Capability | MNMUK Examples |
|--------|---------------------|----------------|
| 10 | No detection possible | No inspection, no opportunity to detect |
| 9 | Unlikely to detect | Random sampling only, infrequent |
| 8 | Low: Visual inspection by operator | 100% visual check, variable attention |
| 7 | Very low: Double visual inspection | Two operators check |
| 6 | Low: Charting/SPC | Control charts, trend monitoring |
| 5 | Moderate: Attribute gaging | Go/No-go gaging |
| 4 | Moderately high: Variable gaging | Measurement with limit checking |
| 3 | High: Automated in-process test | Automatic measurement, alarm |
| 2 | Very high: Error-proofing | Poka-yoke prevents defect production |
| 1 | Almost certain: Error-proofing prevents cause | Design makes failure impossible |

## Action Priority (AIAG-VDA Approach)

Instead of or in addition to RPN, use Action Priority:

| Priority | Criteria | Action Required |
|----------|----------|-----------------|
| **HIGH** | S=9-10 (any O, D) OR S=7-8 with O≥4 AND D≥4 | Immediate action required |
| **MEDIUM** | S=5-8 with O≥4 OR D≥4 | Action recommended |
| **LOW** | All others | Monitor and document |

## RPN Thresholds (MNMUK Standard)

| RPN Range | Priority | Required Action |
|-----------|----------|-----------------|
| ≥120 | Critical | Immediate countermeasure, cannot ship without action |
| 80-119 | High | Countermeasure required before PPAP |
| 40-79 | Medium | Countermeasure recommended |
| <40 | Low | Monitor, no immediate action |

**Note:** Any Severity ≥8 requires action regardless of RPN.

## Countermeasure Hierarchy

When addressing failure modes, apply controls in this priority order:

1. **Eliminate** - Design out the failure mode entirely
2. **Substitute** - Replace with less hazardous process/material
3. **Engineer** - Install physical safeguards, poka-yoke
4. **Admin** - Procedures, training, work instructions
5. **Detect** - Inspection, testing, monitoring

## Special Characteristics

### Critical Characteristics (CC)
- Safety or regulatory impact
- Marked with shield symbol or (CC)
- Requires enhanced controls
- Mandatory documentation

### Significant Characteristics (SC)
- Fit, function, or durability impact
- Marked with diamond or (SC)
- Requires appropriate controls
- SPC typically required

## Output Format

When generating PFMEA content:

```markdown
# PFMEA: [Part/Process Name]
**Part Number**: [P/N]
**Process**: [Description]
**FMEA Number**: PFMEA-[DEPT]-[SEQ]
**Revision**: [Rev] | **Date**: [YYYY-MM-DD]
**Team**: [Names/Roles]

## Process Step: [Step Name]

### Failure Mode 1: [Description]
**Function**: [What the step should do]
**Effect**: [What happens if it fails]
**Cause**: [Why it would fail]

| S | O | D | RPN | AP |
|---|---|---|-----|-----|
| X | X | X | XXX | H/M/L |

**Current Controls**:
- Prevention: [Current prevention measures]
- Detection: [Current detection measures]

**Recommended Actions**:
- [ ] [Action description] - Owner: [Name] - Due: [Date]

**After Action**:
| S | O | D | RPN | AP |
|---|---|---|-----|-----|
| X | X | X | XXX | H/M/L |
```

## Department-Specific Guidance

### Machine Shop
- Common failure modes: Dimensional OOS, surface finish, tool wear
- Focus on: Fixturing, program parameters, tool life management
- Key controls: First piece inspection, SPC, gage R&R

### Damper Assembly
- Common failure modes: Leak, incorrect torque, missing component
- Focus on: Seal integrity, fastener torque, component presence
- Key controls: Leak test, torque verification, poka-yoke

### LVA (Low Volume Assembly)
- Common failure modes: Wrong component, incorrect orientation, damage
- Focus on: Part identification, assembly sequence, handling
- Key controls: Visual verification, traveler documentation

### FML (Final Manufacturing Line)
- Common failure modes: Test failure, labeling error, packaging damage
- Focus on: Final test parameters, traceability, packaging
- Key controls: Automated test, barcode verification, packaging audit

## Integration with Related Skills

### ControlPlan
PFMEA feeds directly into Control Plan:
- High S/O items require enhanced inspection
- Detection controls become Control Plan methods
- Special characteristics flow to Control Plan

**Load:** `read ~/.claude/skills/Controlplan/SKILL.md`

### AutomotiveManufacturing
Work instructions should reflect PFMEA findings:
- High-risk steps highlighted
- Operator controls documented
- Quality checkpoints specified

**Load:** `read ~/.claude/skills/Automotivemanufacturing/SKILL.md`

### A3criticalthinking
When PFMEA reveals issues:
- Use 5 Whys for root cause analysis
- Fishbone diagram for cause identification
- A3 format for countermeasure planning

**Load:** `read ~/.claude/skills/A3criticalthinking/SKILL.md`

## Supplementary Resources

For detailed guidance:
`read ~/.claude/skills/Pfmea/CLAUDE.md`

For templates:
`ls ~/.claude/skills/Pfmea/templates/`

For rating scales:
`read ~/.claude/skills/Pfmea/reference/rating-scales.md`

For common failure modes:
`read ~/.claude/skills/Pfmea/reference/common-failure-modes.md`
