---
name: Controlplan
description: Generate AIAG-format Control Plans linked to PFMEAs with proper inspection methods, frequencies, and reaction plans. Supports Prototype/Pre-launch/Production phases. USE WHEN user says 'control plan', 'CP', 'inspection plan', 'process control', 'sampling frequency', 'reaction plan', or 'special characteristics'. Integrates with PFMEA, AutomotiveManufacturing, and MSA skills.
---

# Control Plan

## When to Activate This Skill
- "Create a control plan for [part/process]"
- "What inspection frequency for [characteristic]?"
- "Define control methods for [operation]"
- "Link PFMEA to control plan"
- "What's the reaction plan for [out-of-spec condition]?"
- "Develop prototype/pre-launch/production control plan"

## Control Plan Phases

### Prototype Control Plan
- **Purpose**: Control during prototype build
- **Focus**: Dimensional measurements, material tests, performance
- **Frequency**: Often 100% on critical dimensions
- **Duration**: Until prototype approval

### Pre-Launch Control Plan
- **Purpose**: Control during PPAP/validation runs
- **Focus**: Enhanced inspection, process validation
- **Frequency**: Increased sampling, SPC establishment
- **Duration**: Until production approval (PSW)

### Production Control Plan
- **Purpose**: Ongoing production control
- **Focus**: Standardized controls, sustained quality
- **Frequency**: Based on process capability
- **Duration**: Life of production

## AIAG Control Plan Format

### Required Columns

| Column | Description | Source |
|--------|-------------|--------|
| Part/Process Number | Operation step number | Process Flow |
| Process Name/Description | Operation description | Process Flow |
| Machine/Device/Jig/Tool | Equipment used | Process documentation |
| Characteristic Number | Unique ID for characteristic | Sequential |
| Product Characteristic | Part feature being controlled | Drawing, spec |
| Process Characteristic | Process parameter affecting product | PFMEA |
| Special Char Class | CC, SC, or blank | PFMEA/Drawing |
| Product/Process Spec | Tolerance or requirement | Drawing, spec |
| Evaluation/Measurement | Gage/method used | MSA |
| Sample Size | Quantity inspected | Based on risk |
| Sample Frequency | How often inspection occurs | Based on risk |
| Control Method | How results are recorded/used | SPC, checklist, etc. |
| Reaction Plan | Action when out of spec | Defined response |

## Special Characteristics

### Critical Characteristics (CC)
- **Symbol**: Shield, (CC), or inverted delta
- **Criteria**: Safety or regulatory compliance
- **Requirements**:
  - Documented in Control Plan
  - Enhanced inspection (often 100%)
  - SPC required (Cpk ≥1.67)
  - Traceable records
  - Identified on drawing

### Significant Characteristics (SC)
- **Symbol**: Diamond, (SC)
- **Criteria**: Fit, function, appearance significant to customer
- **Requirements**:
  - Documented in Control Plan
  - Appropriate inspection frequency
  - SPC recommended (Cpk ≥1.33)
  - Records maintained

### Standard Characteristics
- **Symbol**: None
- **Criteria**: All other characteristics
- **Requirements**:
  - Documented in Control Plan
  - Sampling based on risk
  - Records as required

## Sample Size and Frequency Guidelines

### Based on Severity (from PFMEA)

| Severity | Sample Size | Frequency | Rationale |
|----------|-------------|-----------|-----------|
| 9-10 (Safety) | 100% | Every piece | Safety critical - no escape |
| 7-8 (High) | 100% or n≥5 | Per hour or per lot | High customer impact |
| 5-6 (Moderate) | n≥3 | Per shift or per setup | Moderate risk |
| 1-4 (Low) | n≥1 | Per lot or periodic | Low risk |

### Based on Process Capability

| Cpk Range | Typical Frequency | Notes |
|-----------|-------------------|-------|
| <1.00 | 100% or very frequent | Process not capable |
| 1.00-1.33 | Every hour or more | Marginal capability |
| 1.33-1.67 | Per shift or setup | Capable |
| >1.67 | Per setup, daily, or lot | Highly capable |

### Standard Frequency Terms

| Term | Meaning | When to Use |
|------|---------|-------------|
| Continuous | 100% inspection | Safety, high risk |
| Per piece | Every part | Critical characteristics |
| Per hour | n pieces every hour | SPC, high-risk |
| Per shift | Start and end of shift | Setup-sensitive |
| Per setup | At setup only | Stable characteristics |
| Per lot | One sample per production lot | Low-risk, stable |
| Daily | Once per day | Periodic verification |
| Weekly | Once per week | Very stable |

## Control Methods

### Inspection Methods

| Method | Description | Typical Use |
|--------|-------------|-------------|
| Visual | Operator observation | Surface defects, presence |
| Go/No-Go Gage | Attribute check | Hole size, thread, profile |
| Caliper/Micrometer | Variable measurement | Dimensions |
| CMM | Coordinate measurement | Complex features |
| Height Gage | Surface plate measurement | Flatness, position |
| Profilometer | Surface finish | Ra, Rz |
| Hardness Tester | Material property | HRC, HRB |
| Torque Wrench | Fastener torque | Assembly |
| Leak Test | Seal integrity | Fluid systems |
| Functional Test | Performance verification | End-of-line |

### Recording Methods

| Method | Description | When to Use |
|--------|-------------|-------------|
| Check Sheet | Attribute recording | Visual checks, presence |
| Data Log | Variable data recording | Measurements |
| SPC Chart | Statistical control chart | Critical/significant |
| Traveler | Part-specific record | Traceability |
| Electronic | MES/database entry | High volume |
| None (process control) | Poka-yoke, automated | Error-proofed |

## Reaction Plans

### Standard Reaction Plan Format

```
IF [out-of-spec condition] THEN:
1. STOP - Halt production/segregate suspect
2. CONTAIN - Quarantine affected parts
3. NOTIFY - Alert supervisor/quality
4. EVALUATE - Determine root cause and extent
5. CORRECT - Implement fix before restart
6. VERIFY - Confirm correction effective
```

### Reaction Plan Examples

**Dimension Out of Spec:**
1. Stop production
2. Segregate last good part to current
3. Notify Quality/Supervisor
4. Check tool condition, offset, fixture
5. Adjust/replace as needed
6. Run first piece, verify to spec
7. Inspect segregated parts 100%

**Visual Defect:**
1. Reject defective part
2. Assess severity (isolated vs trend)
3. If trend: notify supervisor, review process
4. Identify root cause (tool, material, handling)
5. Implement correction
6. Resume with enhanced attention

**SPC Out of Control:**
1. Mark control chart
2. Continue production if within spec
3. Investigate pattern (rule violated)
4. Identify assignable cause
5. Implement correction
6. Document on chart

## PFMEA to Control Plan Linkage

### Required Flow

```
PFMEA Item            →    Control Plan Entry
─────────────────          ───────────────────
Process Step          →    Part/Process Number
Function              →    Characteristic
Failure Mode          →    What we're preventing
Detection Control     →    Control Method
S/O/D Ratings         →    Sample Size/Frequency
Special Char          →    Special Char Class
```

### Linkage Verification

For each Control Plan line, verify:
- [ ] PFMEA has corresponding failure mode
- [ ] Special characteristics match
- [ ] Control method addresses PFMEA detection
- [ ] Frequency appropriate for risk level
- [ ] Reaction plan defined

## Output Format

When generating Control Plan content:

```markdown
# Control Plan
**Part Number**: [P/N]
**Part Name**: [Description]
**Customer**: [Customer Name]
**Control Plan Number**: CP-[DEPT]-[SEQ]
**Phase**: [ ] Prototype  [ ] Pre-Launch  [X] Production
**Revision**: [Rev] | **Date**: [YYYY-MM-DD]
**PFMEA Reference**: PFMEA-[XXX]

## Operation: [Number] - [Name]

### Characteristic 1: [Description]

| Field | Value |
|-------|-------|
| **Char No.** | [Unique ID] |
| **Product/Process** | Product / Process |
| **Class** | CC / SC / - |
| **Specification** | [Nominal ± Tolerance] |
| **Evaluation Method** | [Gage/Equipment] |
| **Sample Size** | [n] |
| **Sample Frequency** | [When] |
| **Control Method** | [Recording method] |
| **Reaction Plan** | [Reference or inline] |
```

## Integration with Related Skills

### PFMEA
Control Plan is direct output of PFMEA:
- Every PFMEA detection control → Control Plan method
- PFMEA severity drives inspection frequency
- PFMEA updates trigger Control Plan review

**Load:** `read ~/.claude/skills/Pfmea/SKILL.md`

### MSA
All gages in Control Plan require MSA:
- Gage R&R for variable gages
- Attribute agreement for attribute gages
- MSA acceptance before production approval

**Load:** `read ~/.claude/skills/Msa/SKILL.md`

### AutomotiveManufacturing
Work instructions must reflect Control Plan:
- Inspection steps in work instructions
- Operator-level control methods
- Quality checkpoints documented

**Load:** `read ~/.claude/skills/Automotivemanufacturing/SKILL.md`

## Supplementary Resources

For detailed guidance:
`read ~/.claude/skills/Controlplan/CLAUDE.md`

For templates:
`read ~/.claude/skills/Controlplan/templates/control-plan-template.md`

For control method selection:
`read ~/.claude/skills/Controlplan/reference/control-methods.md`

For sampling guidelines:
`read ~/.claude/skills/Controlplan/reference/sample-frequencies.md`
