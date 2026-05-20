---
name: case-analyzer
description: Analyzes legal case facts and identifies viable legal theories, causes of action, and evidentiary requirements. Use when conducting case intake, strategy development, or initial legal analysis.
version: 1.0.0
category: legal-analysis
complexity: complex
author: MISJustice Alliance Development Team
---

# Case Analyzer Skill

## Purpose

Conduct comprehensive legal case analysis to identify viable claims, evaluate strengths and weaknesses, map evidence requirements, and develop litigation strategy for civil rights and legal advocacy cases.

## When to Use This Skill

- When user says "analyze this case" or "help me with a new case"
- During initial case intake and assessment
- When evaluating potential causes of action
- When mapping legal theories to case facts
- When assessing case viability for litigation
- When identifying discovery needs
- When strategizing affirmative defenses to counter

## When NOT to Use This Skill

- For legal research (use legal-research-assistant skill instead)
- For drafting legal documents (use legal-document-drafter skill instead)
- For case archival (use arweave-case-archiver skill instead)
- For calculating damages (use damages-calculator skill if available)
- For trial preparation (use trial-prep skill if available)

## Prerequisites

- Basic case facts available (who, what, when, where)
- Jurisdiction identified (federal, state, which court)
- General understanding of harm/violation alleged
- Access to reference files in references/ directory
- Python 3.9+ for automation scripts (statute of limitations calculator)

---

## Workflow

### Step 1: Case Intake and Fact Gathering

**Purpose**: Collect essential case information systematically

**Process**:

Ask the user these intake questions in order:

1. **What happened?** (Chronological narrative of events)
   - Request dates, times, locations
   - Identify all parties involved
   - Note sequence of events

2. **Who is involved?**
   - Plaintiff(s) - individual or organization
   - Defendant(s) - individual, organization, government entity
   - Witnesses - who observed what
   - Other parties - employers, supervisors, third parties

3. **When did events occur?**
   - Specific dates of incidents
   - Ongoing conduct vs. discrete events
   - **CRITICAL**: Calculate statute of limitations immediately

4. **Where did events take place?**
   - Geographic location (determines jurisdiction)
   - Federal property vs. state property
   - Public vs. private property

5. **What harm resulted?**
   - Physical injuries
   - Economic damages (lost wages, medical costs)
   - Emotional distress
   - Civil rights violations
   - Property damage

6. **What evidence exists?**
   - Documents (emails, contracts, policies)
   - Video/audio recordings
   - Photographs
   - Witness statements
   - Medical records
   - Police reports

**Output**: Structured case facts document

```markdown
## Case Facts Summary

**Incident Date**: [YYYY-MM-DD]
**Location**: [City, State] - [Specific location]
**Jurisdiction**: [Court]

### Parties
- **Plaintiff**: [Name] - [Description]
- **Defendant**: [Name/Entity] - [Role]
- **Witnesses**: [List]

### Narrative
[Chronological description of events]

### Harm Alleged
- [Injury type 1]
- [Injury type 2]

### Evidence Available
- [Document 1]
- [Recording 1]
- [Witness testimony]
```

**Statute of Limitations Check**:

Use `scripts/statute_of_limitations.py` immediately:

```bash
python3 scripts/statute_of_limitations.py \
  --incident-date="2025-06-15" \
  --claim-type="1983" \
  --jurisdiction="california"
```

**CRITICAL**: If statute of limitations is approaching (<90 days), flag as URGENT

---

### Step 2: Identify Applicable Legal Theories

**Purpose**: Match case facts to potential causes of action

**Process**:

Review case facts against legal frameworks in `references/causes-of-action.md`:

#### Federal Civil Rights Claims

**42 U.S.C. § 1983** (Civil Rights Act):
- Elements:
  1. Defendant acted under color of state law
  2. Defendant's conduct violated constitutional rights

**When to Consider**:
- Police misconduct (excessive force, false arrest, malicious prosecution)
- Jail/prison conditions (deliberate indifference to harm)
- First Amendment violations (retaliation for protected speech)
- Due process violations

**Check for**:
- State actor involvement (police, sheriff, correctional officers, public officials)
- Constitutional rights implicated (4th, 8th, 14th Amendments)

**Americans with Disabilities Act** (ADA):
- **Title I**: Employment discrimination
- **Title II**: State/local government services discrimination
- **Title III**: Public accommodations discrimination

**When to Consider**:
- Disability discrimination by government entity
- Failure to provide reasonable accommodation
- Denial of access to services

#### State Law Claims

Review `references/state-tort-law.md` for:

- **Assault and Battery**: Intentional harmful or offensive contact
- **False Imprisonment**: Unlawful restraint of liberty
- **Intentional Infliction of Emotional Distress**: Extreme and outrageous conduct
- **Negligence**: Breach of duty causing harm

**Analysis Framework**:

For each potential claim, create preliminary assessment:

```markdown
### Legal Theory: [Claim Name]

**Legal Basis**: [Statute, constitutional provision]

**Elements**:
1. [Element 1]
2. [Element 2]
3. [Element 3]

**Fact Mapping**:
- Element 1: [How facts support this element]
- Element 2: [How facts support this element]
- Element 3: [How facts support this element]

**Preliminary Viability**: [Strong | Moderate | Weak]

**Challenges**:
- [Potential defense 1]
- [Evidentiary gap]
```

**Output**: List of 2-5 viable legal theories ranked by strength

---

### Step 3: Elements-Based Analysis

**Purpose**: Rigorously analyze whether facts satisfy each required legal element

**Process**:

For each identified claim (from Step 2), perform detailed elements analysis using `references/elements-checklists/`.

**Example: § 1983 Excessive Force Claim**

Load reference: `references/federal-civil-rights.md` → § 1983 Elements

**Required Elements**:
1. Defendant acted under color of state law
2. Force used was objectively unreasonable (Graham v. Connor standard)
3. Plaintiff suffered injury

**Elements Analysis Table**:

```markdown
| Element | Facts Supporting | Evidence Available | Strength | Notes |
|---------|------------------|-------------------|----------|-------|
| Color of law | Officer on duty, badge #1234 | Body camera, uniform | ★★★★★ | Clear state actor |
| Objectively unreasonable | No resistance shown, compliant | Video, 3 witnesses | ★★★★☆ | Strong but need expert |
| Injury | Broken arm, bruising | Medical records, photos | ★★★★★ | Well documented |

**Overall Element Support**: 14/15 stars - STRONG CASE
```

**Graham v. Connor Factors** (for excessive force):
1. Severity of crime at issue
2. Whether suspect poses immediate threat
3. Whether suspect actively resisting or fleeing

**Analysis**:
```markdown
1. **Severity of Crime**: Misdemeanor jaywalking - LOW
2. **Immediate Threat**: No weapon, hands visible, compliant - NONE
3. **Resistance/Flight**: Video shows no resistance - NONE

**Conclusion**: Force objectively unreasonable under Graham
```

**For Each Claim, Assess**:
- ✅ **Strong** (4-5 stars): All elements clearly supported by facts and evidence
- ⚠️ **Moderate** (2-3 stars): Most elements supported but gaps exist
- ❌ **Weak** (0-1 stars): Critical elements missing or unsupported

**Output**: Elements analysis for top 2-3 claims

---

### Step 4: Discovery Planning

**Purpose**: Identify what additional evidence is needed to prove elements

**Process**:

Based on elements analysis, create comprehensive discovery plan:

#### Documents to Request

**Initial Disclosures** (FRCP 26):
- [ ] Witness list with contact information
- [ ] Document list (descriptions)
- [ ] Damages computation
- [ ] Insurance agreements

**Interrogatories** (Questions to opposing party):
```markdown
1. Identify all officers present at scene on [date]
2. Describe all use-of-force policies in effect on [date]
3. Detail training received by Officer [Name] on [topic]
4. Identify all internal affairs investigations of Officer [Name]
5. [Additional interrogatories - maximum 25 under FRCP]
```

**Document Requests**:
```markdown
### Request 1: Incident Reports
All police reports, incident reports, and supplemental reports related to incident on [date]

### Request 2: Video Evidence
All body camera, dashboard camera, and surveillance footage from [time range]

### Request 3: Personnel Files
Complete personnel file for Officer [Name] including:
- Training records (use of force, de-escalation)
- Disciplinary history
- Prior complaints
- Performance evaluations

### Request 4: Policies and Procedures
All use-of-force policies in effect on [date]

### Request 5: Internal Investigations
All internal affairs investigations related to Officer [Name]
```

**Depositions** (Oral testimony under oath):
```markdown
Priority Order:
1. **Defendant Officer(s)** - 7 hour deposition
   - Training and experience
   - Incident reconstruction
   - Force decision-making process

2. **Supervisor(s)** - 4 hour deposition
   - Oversight and training
   - Policy enforcement

3. **Eyewitnesses** - 2-3 hours each
   - What they observed
   - Credibility assessment

4. **Plaintiff** - 6 hours (prepare thoroughly)
   - Incident narrative
   - Injuries and damages
   - Medical treatment
```

**Expert Witnesses Needed**:
```markdown
1. **Use of Force Expert**
   - Credentials: Former police chief, trainer
   - Purpose: Opine on reasonableness of force
   - Cost: $10,000 - $25,000

2. **Medical Expert**
   - Credentials: Orthopedic surgeon
   - Purpose: Causation of injuries, permanence
   - Cost: $5,000 - $15,000

3. **Economic Expert** (if wage loss)
   - Credentials: Economist, CPA
   - Purpose: Calculate economic damages
   - Cost: $5,000 - $10,000
```

**Output**: Comprehensive discovery plan organized by category

---

### Step 5: Assess Affirmative Defenses and Weaknesses

**Purpose**: Anticipate opposing arguments and develop counter-strategies

**Process**:

Review `references/defenses.md` for common defenses:

#### Qualified Immunity (§ 1983 cases)

**Defense Argument**:
"The constitutional right was not clearly established at the time of the incident"

**Two-Prong Test**:
1. Did defendant violate constitutional right?
2. Was the right clearly established?

**Our Response Strategy**:
```markdown
### Defeating Qualified Immunity

**Prong 1: Constitutional Violation**
- Video evidence shows clear excessive force
- No resistance, no threat = constitutional violation

**Prong 2: Clearly Established Law**
- **Case 1**: [Circuit Case Name] (20XX)
  - Holding: Force against compliant suspect unreasonable
  - Similarity: [Explain how facts parallel our case]

- **Case 2**: [Supreme Court Case]
  - Holding: Graham factors analysis
  - Application: All factors support plaintiff

**Conclusion**: Right was clearly established. QI should be denied.
```

**Risk Assessment**: [Low | Medium | High]
**Mitigation**: Conduct thorough legal research on circuit precedents

#### Governmental Immunity (State Tort Claims)

**Defense Argument**:
"Municipality has governmental immunity for discretionary acts"

**Analysis**:
```markdown
**Immunity Type**: [Sovereign | Qualified | Discretionary]

**Exceptions Available**:
- Ministerial act exception
- Dangerous condition of public property
- [Jurisdiction-specific exceptions]

**Our Strategy**:
- Focus on federal § 1983 claim (no immunity)
- State claims as alternative/backup
- Identify applicable immunity exceptions
```

#### Contributory Negligence

**Defense Argument**:
"Plaintiff's own actions contributed to injury"

**Analysis**:
```markdown
**Defendant's Likely Arguments**:
- Plaintiff was jaywalking (crime)
- Plaintiff didn't immediately comply

**Our Counters**:
- Jaywalking is minor infraction, doesn't justify force
- Video shows compliance
- Contributory negligence not applicable to § 1983 excessive force

**Risk**: Low - Strong video evidence of compliance
```

#### Case Weaknesses to Address

**Identify Honestly**:

```markdown
### Weakness 1: [Description]
**Issue**: Only plaintiff's testimony for initial contact
**Impact**: Credibility battle
**Mitigation**:
- Obtain body camera footage
- Depose witnesses
- Medical records corroborate injuries

### Weakness 2: [Description]
**Issue**: Minor physical injuries (no hospitalization)
**Impact**: Lower damages
**Mitigation**:
- Emphasize constitutional violation (nominal + punitive damages available)
- Emotional distress damages
- Focus on deterrence value of verdict

### Weakness 3: [Description]
**Issue**: [Specific weakness]
**Impact**: [How it affects case]
**Mitigation**: [Strategy to address]
```

**Output**: Comprehensive defense analysis with counter-strategies

---

### Step 6: Generate Case Analysis Report

**Purpose**: Create comprehensive documented analysis for case file

**Process**:

Synthesize all prior steps into structured CASE_ANALYSIS.md:

```markdown
# Case Analysis: [Case Name]

**Generated**: [ISO Timestamp]
**Analyst**: case-analyzer skill v1.0.0
**Jurisdiction**: [Court]

---

## Executive Summary

[2-3 paragraph summary of case viability and recommended strategy]

**Recommended Primary Strategy**: [e.g., Federal § 1983 claim in U.S. District Court]

**Estimated Likelihood of Success**: [Percentage or qualitative assessment]

**Estimated Settlement Range**: $[Low] - $[High]

**Statute of Limitations**: [Date] ([X] days remaining)

**Urgency**: [CRITICAL <30 days | URGENT <90 days | MODERATE <180 days | ROUTINE]

---

## Case Facts

### Incident Summary
[Chronological narrative - 3-5 paragraphs]

### Parties
- **Plaintiff**: [Name], [Age], [Occupation]
- **Defendant**: [Name/Entity], [Role]
- **Witnesses**: [List with brief descriptions]

### Evidence Inventory
| Evidence Type | Description | Status | Location |
|---------------|-------------|--------|----------|
| Body camera | Officer #1234 footage | Requested | City PD |
| Medical records | ER visit 12/15/25 | ✓ Obtained | Case file |
| Witness statements | 3 civilian witnesses | Pending | To be deposed |

---

## Legal Analysis

### Identified Claims

#### Primary Claim: 42 U.S.C. § 1983 - Excessive Force

**Legal Basis**: Fourth Amendment via § 1983

**Elements Analysis**:

| Element | Support | Strength | Evidence |
|---------|---------|----------|----------|
| Color of state law | Officer on duty | ★★★★★ | Badge, uniform |
| Constitutional violation | Force unreasonable | ★★★★☆ | Video, witnesses |
| Injury | Physical harm | ★★★★★ | Medical records |

**Overall Viability**: ★★★★☆ (STRONG)

**Estimated Damages**: $75,000 - $200,000
- Compensatory: $25,000 - $75,000
- Punitive: $50,000 - $125,000 (if malice/recklessness shown)
- Attorney's fees: Recoverable under 42 U.S.C. § 1988

#### Alternative Claim: State Assault and Battery

**Legal Basis**: [State] Common Law Tort

**Elements Analysis**:
[Similar format as above]

**Overall Viability**: ★★★☆☆ (MODERATE)

**Challenges**:
- Governmental immunity may apply
- Lower damages than § 1983
- Purpose: Backup if federal claim fails

---

## Discovery Plan

### Phase 1: Initial Disclosures (Due: [Date])
- [ ] Witness list
- [ ] Document list
- [ ] Damages computation
- [ ] Insurance disclosure

### Phase 2: Written Discovery (Serve by: [Date])

**Interrogatories** (25 maximum):
1. [Question 1]
2. [Question 2]
...

**Document Requests** (50 recommended):
1. All police reports re: incident
2. All body/dashboard camera footage
3. Personnel files for Officer [Name]
...

### Phase 3: Depositions (Complete by: [Date])

| Deponent | Role | Priority | Duration | Topics |
|----------|------|----------|----------|--------|
| Officer Smith | Defendant | HIGH | 7 hours | Force decision, training |
| Witness Jones | Eyewitness | MEDIUM | 2 hours | Observations |
| Plaintiff | Party | HIGH | 6 hours | Incident, injuries, damages |

### Phase 4: Expert Witnesses

| Expert Type | Name | Purpose | Cost Est | Deadline |
|-------------|------|---------|----------|----------|
| Use of force | [TBD] | Opine on reasonableness | $15K | Discovery close |
| Medical | [TBD] | Injury causation | $10K | Discovery close |

---

## Affirmative Defenses & Counter-Strategies

### Defense 1: Qualified Immunity

**Defendant's Argument**:
"Right not clearly established; officer entitled to immunity"

**Our Counter-Strategy**:
1. Identify circuit precedents with similar facts
2. Emphasize obviousness of constitutional violation
3. Cite: [Case 1], [Case 2], [Case 3]

**Risk Level**: MEDIUM
**Likelihood of Success in Defeating**: 70%

### Defense 2: [Additional Defense]
[Similar format]

---

## Case Strengths and Weaknesses

### Strengths ✓
1. **Video Evidence**: Body camera shows clear lack of resistance
2. **Injury Documentation**: Medical records well-documented
3. **Precedent**: Strong circuit law on excessive force
4. **Credible Plaintiff**: No criminal history, steady employment

### Weaknesses ⚠️
1. **Minor Crime**: Jaywalking is low-level infraction
   - **Mitigation**: Emphasize this strengthens our case (force disproportionate)

2. **Limited Physical Injury**: No hospitalization
   - **Mitigation**: Focus on constitutional violation + emotional distress

3. **Witness Credibility**: Only 1 witness to initial contact
   - **Mitigation**: Obtain body camera, depose all witnesses early

---

## Recommended Strategy

### Forum Selection
**Primary**: U.S. District Court, [District]
- **Rationale**: Federal jurisdiction via § 1983, federal judges experienced in civil rights

**Alternative**: State Superior Court
- **Use if**: Federal court dismisses on qualified immunity (unlikely)

### Claim Prioritization
1. **Primary**: § 1983 excessive force (strongest claim)
2. **Alternative**: State assault/battery (backup)
3. **Omit**: [Weaker claims with high risk]

### Settlement Posture
**Pre-Suit Demand**: $150,000
**Post-Suit Settlement Range**: $100,000 - $175,000
**Trial Verdict Estimate**: $150,000 - $250,000

**Timing**:
- Demand letter: Immediate (preserve SOL)
- Mediation: Post-discovery (6-9 months)
- Trial: 12-18 months if no settlement

---

## Next Steps

### Immediate (Week 1)
- [ ] Calculate exact SOL deadline (scripts/statute_of_limitations.py)
- [ ] Draft and send demand letter to defendant
- [ ] Preserve evidence (send preservation letter)

### Short-term (Weeks 2-4)
- [ ] Conduct legal research on qualified immunity
- [ ] Draft federal complaint (use legal-document-drafter skill)
- [ ] Identify and retain expert witnesses

### Medium-term (Months 1-3)
- [ ] File complaint
- [ ] Serve defendants
- [ ] Initiate discovery process

### Long-term (Months 4-12)
- [ ] Complete discovery
- [ ] Prepare for trial or mediation
- [ ] Archive case documents to Arweave (arweave-case-archiver skill)

---

## Statute of Limitations Tracker

**Incident Date**: 2025-06-15
**Claim Type**: § 1983 (uses state personal injury SOL)
**Jurisdiction**: California (2-year SOL)
**Filing Deadline**: 2027-06-15
**Days Remaining**: 547 days
**Urgency**: ROUTINE (adequate time)

**Calculated by**: scripts/statute_of_limitations.py
**Last Checked**: [ISO Timestamp]

---

## Archive Information

**Case ID**: [UUID]
**Arweave TX IDs**: [To be populated after archival]
**Last Updated**: [ISO Timestamp]
**Next Review**: [Date + 30 days]

---

**END OF CASE ANALYSIS**
```

**Quality Check**:
- [ ] All sections complete
- [ ] Legal citations accurate
- [ ] Evidence mapped to elements
- [ ] Discovery plan comprehensive
- [ ] Defense analysis thorough
- [ ] Next steps actionable
- [ ] SOL calculated and verified

---

## Error Handling

### Scenario: Insufficient Facts Provided

**Symptom**: User provides vague description like "police mistreated me"

**Response**:
```
I notice we need more detailed facts to conduct thorough analysis. Let me ask some targeted questions:

1. What specifically did the officer(s) do? (describe physical actions)
2. When did this occur? (exact date and time if possible)
3. Where did this take place? (city, state, specific location)
4. What injuries did you sustain? (physical, emotional, economic)
5. Do you have any documentation? (reports, medical records, video)

Once we have these details, I can identify viable legal claims and assess case strength.
```

**Escalation**: If user cannot provide basic facts, suggest:
- Obtain police report
- Gather medical records
- Interview witnesses
- Return when facts are better documented

---

### Scenario: Novel Legal Issue

**Symptom**: Facts don't clearly fit known causes of action

**Response**:
```markdown
## Novel Legal Issue Identified

**Issue**: [Description of novel issue]

**Why Novel**: [Explanation - e.g., "No binding precedent in this circuit"]

**Recommended Approach**:
1. Flag for legal research (use legal-research-assistant skill)
2. Research analogous cases in other circuits
3. Consult with senior attorney specializing in [area]
4. Consider test case strategy if issue important

**Risk**: [HIGH - outcome uncertain]
**Recommendation**: Proceed with caution; may require expert consultation
```

---

### Scenario: Statute of Limitations Expired

**Symptom**: SOL calculator returns negative days remaining

**Response**:
```markdown
⚠️ **CRITICAL ISSUE: STATUTE OF LIMITATIONS EXPIRED**

**Incident Date**: [Date]
**SOL Deadline**: [Date - in past]
**Days Overdue**: [X] days

**Implications**:
- Case likely barred from filing
- Exceptions are rare and narrow

**Possible Exceptions to Explore**:
1. **Tolling**: Was plaintiff minor, incapacitated, or fraudulently concealed?
2. **Discovery Rule**: Did plaintiff reasonably discover injury later?
3. **Continuing Violation**: Is conduct ongoing?
4. **Equitable Tolling**: Extraordinary circumstances?

**URGENT ACTION REQUIRED**:
Consult experienced attorney immediately to assess exception applicability.
Do NOT proceed with case analysis until SOL issue resolved.
```

---

### Scenario: Jurisdictional Complexity

**Symptom**: Multiple potential forums (federal, multiple states, tribal, etc.)

**Response**:
```markdown
## Jurisdictional Analysis Required

**Complexity Detected**: [e.g., "Incident spans multiple states"]

**Potential Forums**:
1. **U.S. District Court - [District]**
   - Pros: [Federal question jurisdiction, experienced judges]
   - Cons: [Qualified immunity more common]

2. **[State] Superior Court**
   - Pros: [Jury pool favorable, state law claims easier]
   - Cons: [Slower docket, less civil rights experience]

3. **[Other Forum]**
   - Pros: [...]
   - Cons: [...]

**Recommendation**: Analyze forum selection as separate task
**Tools**: Use jurisdiction_analyzer.py script (if available)
**Consult**: Attorney licensed in all relevant jurisdictions
```

---

## Quality Standards

### Output Quality Checklist

Before marking case analysis complete, verify:

- [ ] **Completeness**: All 6 workflow steps executed
- [ ] **Accuracy**: Legal citations correct (case names, statutes)
- [ ] **Element Mapping**: Every element analyzed with evidence
- [ ] **Risk Assessment**: Strengths and weaknesses candidly assessed
- [ ] **Actionability**: Next steps are specific and time-bound
- [ ] **SOL Verified**: Deadline calculated and flagged if urgent
- [ ] **Professional Tone**: Objective, analytical, non-judgmental
- [ ] **Organized**: Clear structure with headers and tables
- [ ] **Archived**: Ready for Arweave permanent storage

### Red Flags (Do Not Proceed)

- ❌ Statute of limitations < 30 days without immediate action plan
- ❌ Critical facts missing (who, what, when, where)
- ❌ Jurisdictional issues unresolved
- ❌ Legal issues beyond analyzer's expertise (complex constitutional law, novel theories)
- ❌ Conflicts of interest detected

**If Red Flag Detected**: Escalate to supervising attorney

---

## Resources

### Reference Files

Load these as needed during analysis:

- `references/causes-of-action.md` - Comprehensive list of federal/state claims
- `references/federal-civil-rights.md` - § 1983, ADA, Fair Housing detailed
- `references/state-tort-law.md` - State-specific tort claims by jurisdiction
- `references/elements-checklists/` - Element-by-element analysis templates
- `references/defenses.md` - Common affirmative defenses and counters
- `references/qualified-immunity.md` - QI doctrine and defeat strategies

### Automation Scripts

- `scripts/statute_of_limitations.py` - Calculate filing deadlines
  ```bash
  python3 scripts/statute_of_limitations.py \
    --incident-date="2025-06-15" \
    --claim-type="1983" \
    --jurisdiction="california"
  ```

- `scripts/jurisdiction_analyzer.py` - Determine proper venue (optional)
- `scripts/damages_estimator.py` - Estimate settlement range (optional)

### Templates

- `assets/intake-questionnaire.md` - Client intake form
- `assets/case-analysis-template.md` - Blank analysis template

---

## Integration with MISJustice Platform

### Related Skills

- **legal-research-assistant**: Use after Step 2 to research identified claims
- **legal-document-drafter**: Use after Step 6 to draft complaint
- **arweave-case-archiver**: Use after Step 6 to permanently archive analysis

### Related Commands

- `/case-plan`: Orchestrates this skill + research + drafting
- `/legal-session-start`: Loads legal context before case analysis

### MCP Dependencies

None currently. Future: Legal database MCPs (Westlaw, LexisNexis)

### Orchestration

Can be chained with other skills:
```
case-analyzer → legal-research-assistant → legal-document-drafter → arweave-case-archiver
```

---

## Examples

### Example 1: § 1983 Excessive Force Case

**Input (User)**:
```
I was arrested for jaywalking on December 15, 2025. The officer tackled me to the ground even though I wasn't resisting. I suffered a broken arm and needed surgery. I have body camera footage showing I had my hands up. This happened in Oakland, California.
```

**Output (case-analyzer)**:
```markdown
# Case Analysis: [Plaintiff] v. Oakland Police Department

## Executive Summary

Strong § 1983 excessive force claim against arresting officer. Video evidence shows plaintiff compliant with hands up when tackled, resulting in significant physical injury (broken arm requiring surgery). Incident occurred 17 days ago, SOL deadline is December 15, 2027 (729 days remaining).

**Recommended Strategy**: File federal § 1983 claim in U.S. District Court, Northern District of California. Estimated settlement value: $100,000 - $250,000.

**Urgency**: MODERATE (adequate time but act promptly to preserve evidence)

## Identified Claims

### Primary: 42 U.S.C. § 1983 - Fourth Amendment Excessive Force

**Elements Analysis**:
| Element | Support | Strength | Evidence |
|---------|---------|----------|----------|
| Color of law | Oakland PD officer on duty | ★★★★★ | Body camera, badge |
| Objectively unreasonable force | Tackling compliant suspect for jaywalking | ★★★★★ | Body camera, medical records |
| Injury | Broken arm requiring surgery | ★★★★★ | Medical records, X-rays, surgical notes |

**Graham v. Connor Analysis**:
1. Severity of crime: Jaywalking (infraction) - MINIMAL
2. Immediate threat: Hands up, compliant - NONE
3. Active resistance/flight: No resistance shown on video - NONE

**Conclusion**: All Graham factors favor plaintiff. Force objectively unreasonable.

**Viability**: ★★★★★ (VERY STRONG)

[... continues with full analysis ...]
```

---

### Example 2: ADA Disability Discrimination

**Input (User)**:
```
I use a wheelchair. Last month, the county courthouse had no elevator working and staff refused to help me access the courtroom on the second floor. I missed my hearing because of this. This was in Tampa, Florida on January 5, 2026.
```

**Output (case-analyzer)**:
```markdown
# Case Analysis: [Plaintiff] v. [County] Courthouse

## Executive Summary

Strong ADA Title II claim against county for failure to provide access to government services. Plaintiff, wheelchair user, denied access to second-floor courtroom due to broken elevator and staff refusal to assist, causing missed court hearing.

**Recommended Strategy**: Federal ADA Title II claim + potential § 1983 claim (deprivation of court access). Settlement range: $25,000 - $75,000 + injunctive relief.

## Identified Claims

### Primary: ADA Title II - Denial of Access to Government Services

**Elements Analysis**:
| Element | Support | Strength | Evidence |
|---------|---------|----------|----------|
| Plaintiff has disability | Wheelchair user (physical impairment) | ★★★★★ | Medical documentation needed |
| Otherwise qualified | Had court hearing scheduled | ★★★★★ | Court docket |
| Excluded from services | Denied courtroom access | ★★★★★ | Witness testimony, court records |
| Because of disability | Inaccessible second floor | ★★★★★ | Physical inspection, photos |

**Viability**: ★★★★★ (VERY STRONG)

**Estimated Damages**:
- Compensatory: $25,000 - $50,000 (emotional distress, legal consequences of missed hearing)
- Injunctive relief: Elevator repair, accessibility plan
- Attorney's fees: Recoverable under ADA

### Alternative: 42 U.S.C. § 1983 - Access to Courts

[... continues with full analysis ...]
```

---

### Example 3: Weak Case (Honest Assessment)

**Input (User)**:
```
I got a speeding ticket last week and the cop was really rude to me. Can I sue for civil rights violations?
```

**Output (case-analyzer)**:
```markdown
# Case Analysis: Speeding Stop

## Executive Summary

**Case Viability**: ★☆☆☆☆ (VERY WEAK - NOT RECOMMENDED)

After analyzing the facts, this case does not present a viable civil rights claim. While the officer's rudeness was unprofessional, it does not rise to the level of a constitutional violation.

## Analysis

### Potential Claim: § 1983 Violation

**Why This Fails**:
1. **No Constitutional Right Violated**: Rudeness alone does not violate the Constitution
2. **No Physical Force**: Traffic stop without excessive force is lawful
3. **No Unlawful Detention**: Speeding provides probable cause for stop
4. **No Actionable Harm**: Emotional distress from rudeness insufficient

**Supreme Court Precedent**:
"The Fourth Amendment does not forbid officers from being rude" - controlling case law

### Alternative Options

1. **Traffic Court**: Challenge the ticket on its merits
2. **Police Complaint**: File internal affairs complaint about officer conduct
3. **Not Recommended**: Federal civil rights lawsuit (likely dismissed, waste of resources)

## Recommendation

**Do NOT pursue civil rights litigation**. This case does not meet the threshold for federal constitutional claims.

**Alternative Actions**:
- Contest ticket in traffic court if factual disputes
- File police complaint if officer conduct warrants discipline
- Accept outcome and move forward

**Consultation**: If you believe there are additional facts not disclosed (physical force, discriminatory statements, unlawful search), please provide those details for re-analysis.
```

---

## Version History

- **1.0.0** (2026-01-01): Initial release
  - Comprehensive 6-step workflow
  - Federal civil rights focus (§ 1983, ADA)
  - State tort law integration
  - Discovery planning module
  - Defense analysis framework
  - SOL automation integration

---

## Troubleshooting

**Issue**: Skill produces overly optimistic case assessment

**Solution**:
- Re-review Step 5 (affirmative defenses)
- Ensure weaknesses are honestly identified
- Apply "red team" thinking - argue against your own case
- Consult qualified-immunity.md for realistic QI assessment

---

**Issue**: Legal citations are outdated or incorrect

**Solution**:
- Verify citations in `references/` files are current
- Update reference files annually
- Flag for legal research if citation uncertain
- Use legal-research-assistant skill for verification

---

**Issue**: Jurisdiction-specific rules not addressed

**Solution**:
- Ensure `references/state-tort-law.md` includes your jurisdiction
- Add jurisdiction-specific reference files as needed
- Consult local counsel for unique state rules
- Note jurisdiction limitations in analysis

---

**END OF SKILL DOCUMENTATION**
