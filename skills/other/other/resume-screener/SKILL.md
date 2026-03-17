---
name: resume-screener
description: Screen resumes efficiently against job requirements with structured scoring, red flag identification, and interview recommendations
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Resume Screener

> Systematically evaluate resumes against job requirements to identify qualified candidates, flag concerns, and prioritize for interviews.

## When to Use This Skill

- High-volume application screening
- Creating screening criteria
- Building evaluation rubrics
- Training hiring managers
- Audit of screening consistency

## Methodology Foundation

Based on **structured interviewing research** and **EEOC guidelines**, combining:
- Job-related criteria only
- Objective scoring rubrics
- Bias-aware evaluation
- Documentation requirements

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Creates screening rubrics | Hiring decisions |
| Scores against criteria | Culture fit assessment |
| Identifies red/green flags | Interview invitation |
| Summarizes qualifications | Final selection |
| Flags potential concerns | Exception handling |

## Instructions

### Step 1: Define Job Criteria

**Required vs. Preferred:**
| Category | Must Have | Nice to Have |
|----------|-----------|--------------|
| Education | Minimum degree | Advanced degree |
| Experience | X years in Y | Specific industry |
| Skills | Core technical | Adjacent skills |
| Certifications | Required licenses | Preferred certs |

**Scoring Weight:**
| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Required experience | 40% | Core capability |
| Required skills | 30% | Day-one impact |
| Education | 15% | Foundation |
| Preferred qualifications | 15% | Growth potential |

### Step 2: Create Screening Rubric

**Scoring Scale:**
| Score | Definition |
|-------|------------|
| 4 | Exceeds requirement significantly |
| 3 | Meets requirement fully |
| 2 | Partially meets requirement |
| 1 | Does not meet requirement |
| 0 | Cannot assess from resume |

### Step 3: Evaluate Resume

**Assessment Framework:**
1. Check must-have requirements (binary pass/fail)
2. Score each criterion (1-4 scale)
3. Calculate weighted total
4. Identify flags (red and green)
5. Make recommendation

### Step 4: Document Findings

**For Each Resume:**
- Overall score
- Must-have checklist
- Criterion-by-criterion scores
- Flags and concerns
- Recommendation with rationale

### Step 5: Prioritize Candidates

**Priority Matrix:**
| Score Range | Action |
|-------------|--------|
| 80-100% | Priority interview |
| 60-79% | Standard review |
| 40-59% | Conditional hold |
| <40% | Not qualified |

## Examples

### Example 1: Full Resume Screening

**Input:**
```
Job: Senior Product Manager

Requirements:
- 5+ years product management experience
- B2B SaaS background required
- Technical degree or equivalent experience
- Experience with Agile methodologies
- Preferred: MBA or similar

Resume:
Jane Smith
Product Manager at TechCorp (3 years)
- Led product roadmap for B2B analytics platform
- Managed team of 4 designers and engineers
- Increased user retention by 35%

Associate PM at StartupXYZ (2 years)
- B2C mobile app
- Launched 3 major features

Education: BS Computer Science, Stanford
Certifications: CSPO, SAFe Agilist
```

**Output:**
```
## Resume Screening: Jane Smith

### Quick Summary
**Position:** Senior Product Manager
**Candidate:** Jane Smith
**Score:** 78/100 - STANDARD REVIEW

---

### Must-Have Requirements

| Requirement | Status | Evidence |
|-------------|--------|----------|
| 5+ years PM experience | ✅ PASS | 3 + 2 = 5 years total |
| B2B SaaS background | ✅ PASS | TechCorp B2B analytics |
| Technical degree/equivalent | ✅ PASS | BS CS Stanford |
| Agile experience | ✅ PASS | CSPO, SAFe certifications |

**Must-Have Result:** PASS (4/4)

---

### Detailed Scoring

| Criterion | Weight | Score | Weighted | Notes |
|-----------|--------|-------|----------|-------|
| Years of Experience | 40% | 3/4 | 30/40 | Meets minimum exactly |
| B2B SaaS | 30% | 3/4 | 22.5/30 | 3 years, not full tenure |
| Technical Background | 15% | 4/4 | 15/15 | Stanford CS |
| Preferred (MBA) | 15% | 2/4 | 7.5/15 | Has certs, no MBA |

**Total Score: 75/100**

---

### Green Flags

| Flag | Evidence | Significance |
|------|----------|--------------|
| Quantified impact | "35% retention increase" | Results-oriented |
| Management experience | "Team of 4" | Leadership ready |
| Relevant certifications | CSPO, SAFe | Agile commitment |
| Top-tier education | Stanford CS | Technical foundation |

---

### Yellow Flags

| Flag | Concern | Mitigation |
|------|---------|------------|
| Experience exactly at minimum | Just hits 5 years | Probe depth in interview |
| Mixed B2B/B2C | 2 years in B2C | Understand B2B transition |
| No MBA | Preferred qualification | Certs may compensate |

---

### Red Flags

None identified.

---

### Interview Recommendation

**Decision:** RECOMMEND FOR INTERVIEW

**Rationale:**
- Meets all must-have requirements
- Strong B2B SaaS experience at TechCorp
- Technical background exceeds expectations
- Quantified achievements show impact

**Interview Focus Areas:**
1. Depth of B2B product strategy experience
2. Transition from B2C to B2B context
3. Scale of products managed (ARR, users)
4. Examples of cross-functional leadership

---

### Comparison Notes

Candidate is solid but not exceptional. Meets requirements without
significantly exceeding them. Consider alongside stronger candidates
if available.
```

### Example 2: Batch Screening Summary

**Input:**
```
Screen these 5 candidates for Marketing Manager:
Requirements: 3+ years marketing, B2B experience, analytics skills

1. Alice: 5 years B2B marketing, Google Analytics certified
2. Bob: 2 years marketing, B2C only, strong analytics
3. Carol: 4 years, mixed B2B/B2C, basic Excel
4. David: 6 years B2B, owns marketing analytics tool
5. Eve: 3 years B2B, HubSpot certified
```

**Output:**
```
## Batch Screening Summary: Marketing Manager

### Quick Rank

| Rank | Candidate | Score | Recommendation |
|------|-----------|-------|----------------|
| 1 | David | 95% | Priority Interview |
| 2 | Alice | 85% | Priority Interview |
| 3 | Eve | 75% | Standard Review |
| 4 | Carol | 55% | Conditional Hold |
| 5 | Bob | 40% | Not Qualified |

---

### Individual Summaries

#### 1. David (95%) - PRIORITY INTERVIEW

| Requirement | Status | Score |
|-------------|--------|-------|
| 3+ years | ✅ 6 years | 4/4 |
| B2B experience | ✅ Full tenure | 4/4 |
| Analytics skills | ✅ Tool owner | 4/4 |

**Standout:** Exceptional analytics depth - owns a marketing analytics tool
**Interview:** Immediately

---

#### 2. Alice (85%) - PRIORITY INTERVIEW

| Requirement | Status | Score |
|-------------|--------|-------|
| 3+ years | ✅ 5 years | 4/4 |
| B2B experience | ✅ Full tenure | 4/4 |
| Analytics skills | ✅ GA certified | 3/4 |

**Standout:** Solid all-around, Google Analytics certification
**Interview:** This week

---

#### 3. Eve (75%) - STANDARD REVIEW

| Requirement | Status | Score |
|-------------|--------|-------|
| 3+ years | ✅ Exactly 3 | 3/4 |
| B2B experience | ✅ Full tenure | 4/4 |
| Analytics skills | ⚠️ HubSpot only | 2/4 |

**Concern:** HubSpot is automation, not analytics
**Interview:** Probe analytics skills deeper

---

#### 4. Carol (55%) - CONDITIONAL HOLD

| Requirement | Status | Score |
|-------------|--------|-------|
| 3+ years | ✅ 4 years | 3/4 |
| B2B experience | ⚠️ Mixed | 2/4 |
| Analytics skills | ❌ Basic Excel | 1/4 |

**Concern:** Weak analytics foundation
**Hold:** Consider if top candidates decline

---

#### 5. Bob (40%) - NOT QUALIFIED

| Requirement | Status | Score |
|-------------|--------|-------|
| 3+ years | ❌ 2 years | 1/4 |
| B2B experience | ❌ B2C only | 1/4 |
| Analytics skills | ✅ Strong | 3/4 |

**Disqualified:** Does not meet experience or B2B requirements
**Action:** Reject with positive note on analytics skills

---

### Screening Actions

| Action | Candidates |
|--------|------------|
| Schedule interviews | David, Alice |
| Standard queue | Eve |
| Hold file | Carol |
| Rejection email | Bob |
```

## Skill Boundaries

### What This Skill Does Well
- Structuring evaluation criteria
- Consistent scoring application
- Identifying relevant flags
- Documenting decisions

### What This Skill Cannot Do
- Assess culture fit
- Verify claims accuracy
- Conduct background checks
- Replace human judgment

### Important Compliance Notes
- Focus only on job-related criteria
- Avoid protected class considerations
- Document all decisions
- Apply criteria consistently

## Iteration Guide

**Follow-up Prompts:**
- "Create interview questions based on this screening"
- "What should I probe further with [candidate]?"
- "Compare these top 3 candidates side by side"
- "Draft rejection email for [candidate]"

## References

- SHRM Structured Interviewing Guidelines
- EEOC Uniform Guidelines on Employee Selection
- Google re:Work Hiring Practices
- Lever Recruiting Best Practices

## Related Skills

- `interview-scheduler` - Coordinate interviews
- `onboarding-guide` - Post-hire integration
- `job-description-writer` - Create requirements

## Skill Metadata

- **Domain**: HR Operations
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 10-15 min per resume
- **Prerequisites**: Job requirements, resumes
