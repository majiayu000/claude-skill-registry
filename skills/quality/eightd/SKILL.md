---
name: Eightd
description: Structured 8D problem solving for customer complaints and quality issues. D0-D8 phases with containment, root cause analysis, and escape point identification. USE WHEN user says '8D', 'eight disciplines', 'customer complaint', 'corrective action', 'root cause analysis', 'containment', 'escape point', or 'problem solving report'.
---

# 8D Problem Solving Skill

## Overview

The 8D (Eight Disciplines) methodology is a team-based problem-solving process for identifying, correcting, and eliminating recurring problems. Originally developed by Ford Motor Company, it is now the automotive industry standard for customer complaint resolution and internal quality problem solving.

## Skill Integration

| Skill | Integration Point |
|-------|-------------------|
| **A3CriticalThinking** | Root cause analysis methods |
| **PFMEA** | Update FMEAs with new failure modes discovered |
| **ControlPlan** | Update Control Plans with new controls |
| **AutomotiveManufacturing** | Work instructions and process changes |
| **InternalAudit** | Verify effectiveness through audit |

## 8D Phase Overview

| Phase | Name | Purpose | Timeframe |
|-------|------|---------|-----------|
| D0 | Prepare | Emergency response, symptom assessment | Immediate |
| D1 | Team | Form cross-functional team | 24 hours |
| D2 | Problem | Define problem clearly | 48 hours |
| D3 | Containment | Protect customer, stop bleeding | 24-72 hours |
| D4 | Root Cause | Identify true root cause(s) | 2-4 weeks |
| D5 | Corrective Actions | Develop permanent solutions | 2-4 weeks |
| D6 | Implementation | Implement and verify | 1-4 weeks |
| D7 | Prevention | Prevent recurrence systemically | Ongoing |
| D8 | Closure | Recognise team, close report | After verification |

---

## D0: Prepare for the 8D Process

### Emergency Response Actions (ERA)

Before formal 8D begins, immediate actions to protect:

1. **Customer Protection**
   - Identify all potentially affected product
   - Stop shipment of suspect product
   - Notify customer of situation
   - Provide replacement/rework timeline

2. **Symptom Assessment**
   - What is the symptom?
   - When was it first detected?
   - How much product is affected?
   - Is this a safety/regulatory issue?

3. **8D Trigger Criteria

| Trigger | 8D Required? |
|---------|--------------|
| Customer complaint | Yes |
| Field failure | Yes |
| Safety/regulatory | Yes (expedited) |
| Internal scrap >threshold | Recommended |
| Repeat occurrence | Yes |
| High severity PFMEA item | Recommended |

### D0 Outputs

- Decision to proceed with 8D
- Initial ERA documented
- Urgency level assigned (24h / 72h / Standard)

---

## D1: Establish the Team

### Team Composition

| Role | Responsibility | Required? |
|------|---------------|-----------|
| Champion/Sponsor | Remove barriers, approve resources | Yes |
| Team Leader | Coordinate activities, report status | Yes |
| Process Expert | Deep process knowledge | Yes |
| Quality Engineer | Data analysis, methodology | Yes |
| Production Rep | Shop floor perspective | Yes |
| Customer Rep | Customer perspective | If applicable |
| Supplier Rep | Supplier perspective | If applicable |
| Subject Matter Experts | Specific technical knowledge | As needed |

### Team Size

- **Ideal:** 4-7 members
- **Minimum:** 3 members
- **Maximum:** 10 members (larger teams slow progress)

### D1 Outputs

- Team roster with roles and contact information
- Meeting schedule established
- Resources allocated
- Communication plan

---

## D2: Describe the Problem

### Problem Description Techniques

**5W2H Analysis:**

| Question | Answer |
|----------|--------|
| **What** is the problem? | Specific defect/symptom |
| **Where** was it found? | Location (customer, inspection, operation) |
| **When** was it found? | Date, time, shift, production lot |
| **Who** found it? | Person, inspection method |
| **Why** is it a problem? | Impact to customer/function |
| **How many** are affected? | Quantity, frequency, trend |
| **How** was it detected? | Detection method used |

**IS / IS NOT Analysis:**

| Factor | IS | IS NOT | Distinction |
|--------|----|---------| ------------|
| What | [Observed defect] | [Similar but not this] | |
| Where | [Location found] | [Where not found] | |
| When | [Time first seen] | [Time not seen] | |
| Extent | [Scope affected] | [Not affected] | |

### Problem Statement Format

**Good problem statement:**
> "Outer diameter of part #12345 measures 25.08-25.12mm (spec: 25.00 ±0.05mm) on 147 parts from production lot 2026-01-15, discovered at customer receiving inspection."

**Bad problem statement:**
> "Parts are out of spec" (too vague)

### D2 Outputs

- Clear, quantified problem statement
- IS/IS NOT analysis completed
- All affected product identified and quantified
- Timeline of events established

---

## D3: Interim Containment Actions (ICA)

### Containment Scope

| Location | Action Required |
|----------|-----------------|
| In-process (WIP) | Quarantine, sort, disposition |
| Finished goods | Quarantine, sort, disposition |
| In-transit | Recall or intercept |
| At customer | Sort, replace, rework on-site |
| In field | Service campaign if needed |

### Containment Actions

1. **Sort** - 100% inspection to separate good/bad
2. **Hold** - Quarantine suspect product
3. **Replace** - Provide conforming product
4. **Enhanced inspection** - Temporary additional checks
5. **Process change** - Temporary parameter adjustment

### Containment Verification

Before releasing containment:
- Verify containment is effective
- Track containment metrics (PPM before/after)
- Document all contained material
- Customer acceptance of containment

### Escape Point Analysis

**Critical Question:** Where should this have been caught?

| Stage | Did we have detection? | Why did it escape? |
|-------|----------------------|-------------------|
| Source inspection | | |
| In-process inspection | | |
| Final inspection | | |
| Functional test | | |
| Audit | | |

### D3 Outputs

- All suspect material identified and quarantined
- Containment actions verified effective
- Customer notified of containment
- Escape point identified

---

## D4: Root Cause Analysis

### Root Cause Categories

**Occurrence Root Cause:** Why did the defect occur?
- Process, machine, material, method, environment

**Detection Root Cause (Escape Point):** Why wasn't it caught?
- Inspection method, frequency, capability, training

### Root Cause Analysis Tools

| Tool | Best For | Reference |
|------|----------|-----------|
| 5-Why | Simple cause chains | `reference/root-cause-tools.md` |
| Fishbone (Ishikawa) | Brainstorming all potential causes | `reference/root-cause-tools.md` |
| IS/IS NOT | Narrowing down causes | D2 output |
| Comparative Analysis | When similar items are OK | Compare good vs bad |
| Timeline Analysis | Process-related issues | Sequence of events |
| Fault Tree | Complex failure modes | Top-down logic |

### 5-Why Guidelines

| Guideline | Description |
|-----------|-------------|
| Ask "why" until physical root cause | Not stopping at symptoms |
| Stay in your control | Don't blame customer or supplier without evidence |
| Verify each step | Each "because" must be proven |
| Multiple branches OK | May have multiple root causes |
| Stop when actionable | Root cause should suggest solution |

### Root Cause Verification

**Verification Methods:**

| Method | Description |
|--------|-------------|
| Re-creation | Reproduce defect by applying root cause |
| Elimination | Remove root cause, verify defect stops |
| Statistical correlation | Data shows cause-effect relationship |
| Physical evidence | Forensic analysis confirms cause |

**Root cause is verified when:**
- Can reproduce defect by introducing cause
- Can eliminate defect by removing cause
- Explains all data (IS/IS NOT)
- Team consensus on verification

### D4 Outputs

- Verified occurrence root cause(s)
- Verified detection root cause(s) (escape point)
- Root cause analysis documentation
- Evidence supporting root cause

---

## D5: Develop Corrective Actions

### Corrective Action Types

| Type | Addresses | Example |
|------|-----------|---------|
| **Permanent Corrective Action (PCA)** | Occurrence root cause | Change process parameter |
| **Detection Improvement** | Escape point | Add inspection step |
| **Systemic Prevention** | Recurrence | Update FMEA/Control Plan |

### Corrective Action Hierarchy

**Prefer higher-order controls:**

| Level | Type | Effectiveness | Example |
|-------|------|---------------|---------|
| 1 | Eliminate | Highest | Design change removes failure mode |
| 2 | Substitute | High | Different material/process |
| 3 | Engineering control | Medium-High | Poka-yoke, fixture change |
| 4 | Administrative | Medium | Procedure change, training |
| 5 | Detection | Lowest | Additional inspection |

### Corrective Action Criteria

Each corrective action must be:
- **Specific** - Clear what will be done
- **Measurable** - Can verify implementation
- **Assignable** - Single owner responsible
- **Realistic** - Can be implemented
- **Time-bound** - Due date defined

### Risk Assessment

Before implementing corrective actions:
- Will action introduce new risks?
- Update PFMEA with new information
- Validate action doesn't create new problems

### D5 Outputs

- List of corrective actions with owners and dates
- Risk assessment of each action
- PFMEA updates identified
- Control Plan updates identified

---

## D6: Implement and Verify Corrective Actions

### Implementation Steps

1. **Plan** - Detailed implementation plan
2. **Communicate** - Notify all affected parties
3. **Train** - Train operators on changes
4. **Execute** - Implement changes
5. **Verify** - Confirm actions completed
6. **Validate** - Confirm actions are effective

### Verification vs Validation

| Verification | Validation |
|--------------|------------|
| Did we implement the action correctly? | Did the action solve the problem? |
| Check implementation | Check effectiveness |
| Immediate | Over time |

### Effectiveness Verification

| Method | Description | Duration |
|--------|-------------|----------|
| Before/After comparison | Metric improvement | 1-3 months data |
| Control chart | Process stability | 25+ subgroups |
| Capability study | Cpk improvement | Per standard |
| Audit | Process compliance | Scheduled |
| Zero defects | No recurrence | 3-6 months |

### D6 Outputs

- All corrective actions implemented
- Implementation verification completed
- Effectiveness validation initiated
- Updated documentation (WI, Control Plan, FMEA)

---

## D7: Prevent Recurrence

### Systemic Prevention Actions

| System | Update Required |
|--------|-----------------|
| **PFMEA** | Add failure mode, update S/O/D, add controls |
| **Control Plan** | Add/modify inspection, update reaction plan |
| **Work Instructions** | Incorporate process changes |
| **Training** | Update training materials, retrain |
| **Lessons Learned** | Document for future reference |
| **Similar Products** | Apply to similar parts/processes |

### Horizontal Deployment

Apply learning across:
- Similar parts on same equipment
- Similar processes in other areas
- Similar failure modes in PFMEA
- Supplier processes if applicable

### D7 Outputs

- FMEA updated with new failure mode
- Control Plan updated
- Work instructions revised
- Training completed
- Lessons learned documented
- Horizontal deployment completed

---

## D8: Recognise Team and Close

### Closure Criteria

- [ ] Root cause verified
- [ ] All corrective actions implemented
- [ ] Effectiveness verified (no recurrence period)
- [ ] FMEA/Control Plan updated
- [ ] Work instructions updated
- [ ] Training completed
- [ ] Customer accepts closure (if customer complaint)
- [ ] Lessons learned documented

### Team Recognition

- Acknowledge team contribution
- Share success with organisation
- Consider formal recognition programme

### 8D Archive

Retain 8D reports for:
- Customer-required retention period
- Minimum 3 years per IATF 16949
- Accessible for reference and audits

### D8 Outputs

- 8D report complete and approved
- Customer acceptance (if applicable)
- Archive in quality records
- Team recognised

---

## Templates

- `templates/8d-report.md` - Full 8D report template

## Reference Materials

- `reference/root-cause-tools.md` - 5-Why, Fishbone, IS/IS NOT
- `reference/verification-methods.md` - How to verify root cause and effectiveness

## MNMUK-Specific Guidelines

### Response Timeframes

| Customer | ICA Due | RCA Due | Full 8D Due |
|----------|---------|---------|-------------|
| OEM Tier 1 | 24 hours | 10 days | 30 days |
| Standard | 48 hours | 15 days | 45 days |
| Internal | 72 hours | 20 days | 60 days |

### 8D Numbering

Format: `8D-[YYYY]-[SEQ]`
Example: `8D-2026-001`

### Approval Authority

| Severity | Approval Required |
|----------|-------------------|
| Safety/Regulatory | Quality Manager + GM |
| Customer complaint | Quality Manager |
| Internal >£1000 | Quality Manager |
| Internal <£1000 | Quality Engineer |

---

## Quick Reference

```
# Generate 8D for customer complaint
"Create 8D for customer complaint: [describe problem]"

# Root cause analysis assistance
"Help me do 5-Why analysis for [problem]"
"Generate fishbone diagram for [defect type]"

# Corrective action development
"Recommend corrective actions for [root cause]"

# 8D review
"Review this 8D for completeness"
```
