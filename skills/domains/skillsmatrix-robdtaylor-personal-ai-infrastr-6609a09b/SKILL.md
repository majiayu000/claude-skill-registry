---
name: SkillsMatrix
description: |
  Operator training and competency tracking for MNMUK machine shop.
  Supports IATF 16949 competency requirements and workforce planning.
  USE WHEN user asks 'who can run', 'training matrix', 'competency', 'skills matrix',
  'operator certification', 'who is trained on', or workforce planning questions.
---

# SkillsMatrix - Operator Competency Tracking

**Purpose:** Track who can run what, plan training, ensure coverage, support IATF 16949 compliance.

## When to Activate

- "Who can run the NLX2500?"
- "Create training matrix"
- "What machines is Dave trained on?"
- "Do we have backup for Swiss?"
- "Training needs for new hire"
- "Competency gap analysis"

---

## IATF 16949 Requirements

### Clause 7.2 - Competence

> The organization shall determine necessary competence, ensure competence based on education/training/experience, take actions to acquire competence, and retain documented evidence.

### Required Documentation

1. **Competency definitions** - What skills needed per role
2. **Training records** - Evidence of training completed
3. **Competency assessment** - Verification of capability
4. **Ongoing effectiveness** - Periodic revalidation

---

## Competency Levels

| Level | Code | Description | Can Do |
|-------|------|-------------|--------|
| **Not Trained** | 0 | No exposure | Nothing |
| **Awareness** | 1 | Observed, understands basics | Assist only |
| **Under Training** | 2 | In training program | Supervised work |
| **Competent** | 3 | Can work independently | Standard work |
| **Proficient** | 4 | Handles complex jobs | All work + troubleshoot |
| **Expert** | 5 | Trains others, process owner | All + train + improve |

---

## Skills Matrix Template

### By Machine

```markdown
# MNMUK Skills Matrix - Machines

Last Updated: YYYY-MM-DD

| Employee | NMV3000 | DMU50 | NHX500 | VMC 4-Axis | NLX2500 Twin | NLX2500 Single | ALX2000 | HARDINGE | CITIZEN Laser | CITIZEN LFV | Wire EDM | Spark EDM | Haas Mill | Haas Lathe |
|----------|---------|-------|--------|------------|--------------|----------------|---------|----------|---------------|-------------|----------|-----------|-----------|------------|
| [Name 1] | | | | | | | | | | | | | | |
| [Name 2] | | | | | | | | | | | | | | |
| [Name 3] | | | | | | | | | | | | | | |

**Legend:** 0=Not Trained, 1=Awareness, 2=Under Training, 3=Competent, 4=Proficient, 5=Expert
```

### By Skill Category

```markdown
# MNMUK Skills Matrix - Categories

| Employee | 5-Axis Mill | 4-Axis Mill | CNC Turning | Swiss | EDM | Setup | Programming | Quality/Inspection | First-Off | Forklift | Crane |
|----------|-------------|-------------|-------------|-------|-----|-------|-------------|-------------------|-----------|----------|-------|
| [Name] | | | | | | | | | | | |
```

---

## Machine-Specific Requirements

### DMG MORI 5-Axis (NMV3000, DMU50, NHX500)

**Required Competencies:**
- [ ] CELOS interface operation
- [ ] 5-axis work coordinate setup
- [ ] Pallet system operation (NMV3000/DMU50)
- [ ] Tool length measurement
- [ ] Probe calibration and use
- [ ] Crash recovery procedures
- [ ] Program editing (basic)

**Training Hours:** 40-80 hours supervised
**Certification:** Internal practical assessment

### DMG MORI Turning (NLX2500, ALX2000)

**Required Competencies:**
- [ ] Chuck/collet setup
- [ ] Bar feeder operation
- [ ] Live tooling setup
- [ ] Sub-spindle transfer (NLX2500)
- [ ] Tool offset adjustment
- [ ] In-process gauging
- [ ] Chip management

**Training Hours:** 30-60 hours supervised
**Certification:** Internal practical assessment

### HARDINGE Precision Turning

**Required Competencies:**
- [ ] All standard turning competencies
- [ ] Precision setup techniques
- [ ] Temperature compensation understanding
- [ ] Micro-adjustment of offsets
- [ ] SPC/gauging for tight tolerances

**Training Hours:** 60-100 hours supervised (after CNC turning base)
**Certification:** Practical assessment on ±0.003mm parts

### CITIZEN Swiss (Laser Head, LFV)

**Required Competencies:**
- [ ] Guide bushing selection and setup
- [ ] Gang tooling setup
- [ ] Sub-spindle pickup programming
- [ ] Oil system management
- [ ] LFV parameter adjustment (LFV model)
- [ ] Laser operation (Laser model)
- [ ] Small part handling

**Training Hours:** 80-120 hours supervised
**Certification:** Manufacturer training recommended + internal

### MITSUBISHI EDM (Wire & Spark)

**Wire EDM Competencies:**
- [ ] Wire threading (auto and manual)
- [ ] Start hole location
- [ ] Multi-pass programming understanding
- [ ] Flushing optimization
- [ ] Wire break recovery

**Spark EDM Competencies:**
- [ ] Electrode design principles
- [ ] Electrode alignment
- [ ] Orbiting parameters
- [ ] Surface finish control

**Training Hours:** 40-80 hours per machine type
**Certification:** Internal assessment

### Haas Fast Response

**Required Competencies:**
- [ ] Basic Haas control operation
- [ ] Manual tool setting
- [ ] Vice setup and alignment
- [ ] G-code basics
- [ ] When to escalate to production machines

**Training Hours:** 16-24 hours (entry level machine)
**Certification:** Internal practical

---

## Training Record Template

```markdown
# Training Record

## Employee Information
| Field | Value |
|-------|-------|
| Name | |
| Employee ID | |
| Start Date | |
| Department | |
| Role | |

## Training History

| Date | Training | Machine/Skill | Trainer | Hours | Assessment | Result | Next Review |
|------|----------|---------------|---------|-------|------------|--------|-------------|
| | | | | | | | |

## Current Competencies

| Machine/Skill | Level | Date Achieved | Assessor | Evidence |
|---------------|-------|---------------|----------|----------|
| | | | | |

## Training Plan

| Skill Needed | Target Level | Target Date | Training Method | Progress |
|--------------|--------------|-------------|-----------------|----------|
| | | | | |

## Signatures

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Employee | | | |
| Supervisor | | | |
| Training Coordinator | | | |
```

---

## Coverage Analysis

### Minimum Coverage Requirements

| Machine Type | Min Operators | Current | Gap | Risk Level |
|--------------|---------------|---------|-----|------------|
| 5-Axis Mills | 3 | | | |
| 4-Axis VMC | 2 | | | |
| NLX2500 Turning | 3 | | | |
| HARDINGE | 2 | | | |
| CITIZEN Swiss | 2 | | | |
| Wire EDM | 2 | | | |
| Spark EDM | 1 | | | |
| Haas (any) | 2 | | | |

### Risk Assessment

| Risk Level | Coverage | Action |
|------------|----------|--------|
| Critical | 0-1 operators | Immediate training required |
| High | 2 operators | Cross-train within 3 months |
| Medium | 3 operators | Maintain, develop experts |
| Low | 4+ operators | Focus on specialization |

### Single Point of Failure Report

```markdown
# Single Points of Failure

Machines with only ONE competent operator:

| Machine | Only Operator | Risk | Mitigation Plan |
|---------|---------------|------|-----------------|
| | | | |

Action Required: Cross-train second operator within [X] weeks
```

---

## Training Needs Analysis

### New Hire Onboarding

**Week 1-2: Orientation**
- [ ] Safety training
- [ ] Quality system overview
- [ ] Shop floor familiarization
- [ ] Basic measurement tools

**Week 3-4: Foundation**
- [ ] Haas Mini Mill basics
- [ ] Blueprint reading
- [ ] GD&T fundamentals
- [ ] First-off inspection

**Month 2-3: Primary Machine**
- [ ] Assigned machine training
- [ ] Supervised operation
- [ ] Progressive independence

**Month 4-6: Competency**
- [ ] Independent operation
- [ ] Formal assessment
- [ ] Sign-off to Level 3

### Cross-Training Priority

```markdown
# Cross-Training Priority Matrix

Based on: Coverage gaps, business risk, employee development

| Priority | From Machine | To Machine | Candidate | Reason |
|----------|--------------|------------|-----------|--------|
| 1 | | | | Coverage gap |
| 2 | | | | Backup needed |
| 3 | | | | Development |
```

---

## Competency Assessment Checklist

### Practical Assessment Template

```markdown
# Competency Assessment

**Employee:**
**Machine:**
**Date:**
**Assessor:**

## Setup Assessment
| Task | Pass | Fail | Notes |
|------|------|------|-------|
| Interpret setup sheet | | | |
| Select correct tooling | | | |
| Install workholding | | | |
| Set work offsets | | | |
| Verify tool offsets | | | |
| Load program correctly | | | |

## Operation Assessment
| Task | Pass | Fail | Notes |
|------|------|------|-------|
| Start machine safely | | | |
| Run first part at reduced feed | | | |
| Monitor cutting conditions | | | |
| Respond to abnormal conditions | | | |
| Adjust offsets correctly | | | |
| Maintain quality during run | | | |

## Quality Assessment
| Task | Pass | Fail | Notes |
|------|------|------|-------|
| Perform first-off inspection | | | |
| Use measurement equipment correctly | | | |
| Record results properly | | | |
| Identify out-of-spec conditions | | | |
| Know when to stop and escalate | | | |

## Safety Assessment
| Task | Pass | Fail | Notes |
|------|------|------|-------|
| PPE compliance | | | |
| Guards in place before start | | | |
| Emergency stop knowledge | | | |
| Chip/coolant handling | | | |
| Housekeeping | | | |

## Result

| | |
|---|---|
| Total Pass: | /20 |
| Assessment Result: | PASS / FAIL |
| Competency Level Awarded: | |
| Retest Required: | Y / N |
| Retest Date: | |

**Assessor Signature:** _________________ **Date:** _________
**Employee Signature:** _________________ **Date:** _________
```

---

## Reports

### Monthly Skills Report

```markdown
# Skills Matrix Report - [Month YYYY]

## Coverage Summary
| Machine Category | Required | Available | Gap | Status |
|------------------|----------|-----------|-----|--------|
| 5-Axis | 3 | | | |
| Turning | 3 | | | |
| Swiss | 2 | | | |
| EDM | 2 | | | |

## Training Completed This Month
| Employee | Training | New Level |
|----------|----------|-----------|
| | | |

## Training In Progress
| Employee | Training | Target Date | % Complete |
|----------|----------|-------------|------------|
| | | | |

## Upcoming Training Needs
| Employee | Training | Start Date | Reason |
|----------|----------|------------|--------|
| | | | |

## Actions Required
1.
2.
3.
```

---

## Integration

- **CNCSetup:** Only generate setup sheets for machines operator is trained on
- **PlantCapability:** Consider operator availability in machine selection
- **TribalKnowledge:** Experts (Level 5) are primary knowledge sources
- **AutomotiveManufacturing:** Supports IATF 16949 Clause 7.2 compliance
