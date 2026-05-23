---
name: career-fit-assessor
description: >
  Red team/blue team career fit assessment for job opportunities. Evaluates candidate 
  suitability using adversarial analysis against Critical Success Factors (CSFs). 
  Use when asked to: assess job fit, evaluate a job opportunity, analyze a job description 
  against my background, determine if I should apply for a role, red/blue team a job, 
  assess my candidacy, or evaluate career opportunities. Requires XML career history 
  files in project context. Supports two modes: "quick" (BLUF + argument table + prep 
  recommendations) and "detailed" (comprehensive weighted CSF analysis with passion 
  alignment). Triggers: "assess this job", "should I apply", "evaluate this role", 
  "career fit assessment", "job fit analysis", "red team this opportunity".
---

# Career Fit Assessor

Adversarial career fit analysis using red team/blue team methodology against job-specific Critical Success Factors.

## Prerequisites Check

**Before any assessment, verify career data exists:**

1. Check for XML files containing career history in project context or `/experience/`
2. If no career XML files found:
   - STOP assessment immediately
   - Inform user: "Career fit assessment requires XML files containing your work experience. Please add your career history files to the project or upload them to proceed."
   - Do not attempt to proceed with partial information
3. If career files exist, load and parse them before continuing

## Mode Selection

Determine assessment mode from user request:

**Quick Mode** (default if unspecified):
- Triggers: "quick", "brief", "summary", "fast", "overview", or no mode specified
- Output: BLUF → Red/Blue table → Interview prep recommendations

**Detailed Mode**:
- Triggers: "detailed", "comprehensive", "full", "deep dive", "complete analysis"
- Output: Full CSF analysis with weighted scoring, passion alignment, and strategic recommendations
- See `references/detailed-assessment-criteria.md` for complete methodology

## Quick Mode Workflow

### Step 1: Establish Critical Success Factors

Analyze the job description to identify 8-12 CSFs across these categories:
- **Explicit requirements**: Stated skills, qualifications, experience
- **Implicit requirements**: Read between the lines—what's emphasized, company context, role positioning
- **Industry standards**: Common success factors for this role type not explicitly listed
- **Cultural factors**: Soft skills, work style, values alignment

### Step 2: Red Team/Blue Team Analysis

For each CSF, develop adversarial arguments:

**Blue Team (Advocate)**: Build the strongest case FOR the candidate
- Direct experience matches
- Transferable skills from adjacent domains
- Demonstrated learning ability in similar areas
- Unique differentiators that exceed requirements

**Red Team (Challenger)**: Build the strongest case AGAINST the candidate
- Experience gaps or misalignments
- Missing explicit requirements
- Potential concerns a hiring manager would raise
- Competitive disadvantages vs. typical applicants

### Step 3: Synthesize Assessment

Weigh blue vs. red arguments to form overall assessment:
- **Strong Fit** (75%+): Blue team arguments clearly dominate
- **Moderate Fit** (50-74%): Mixed case with addressable gaps
- **Weak Fit** (<50%): Red team arguments dominate; significant gaps

### Step 4: Output Format (Quick Mode)

```markdown
## Career Fit Assessment: [Role Title] at [Company]

### Bottom Line Up Front

[1-2 sentence definitive recommendation: Apply/Consider with caveats/Pass]
[Overall fit percentage and confidence level]

### Red Team / Blue Team Analysis

| Blue Team (For) | Red Team (Against) |
|-----------------|-------------------|
| • [Argument 1] | • [Argument 1] |
| • [Argument 2] | • [Argument 2] |
| • [Argument 3] | • [Argument 3] |
| • [Argument 4] | • [Argument 4] |
| • [Argument 5] | • [Argument 5] |

### Interview Preparation Recommendations

**Strengths to Emphasize:**
1. [Specific talking point with evidence]
2. [Specific talking point with evidence]
3. [Specific talking point with evidence]

**Gaps to Address Proactively:**
1. [Gap + recommended framing/mitigation strategy]
2. [Gap + recommended framing/mitigation strategy]
3. [Gap + recommended framing/mitigation strategy]

**Key Questions to Prepare For:**
1. [Likely challenging question + approach]
2. [Likely challenging question + approach]
3. [Likely challenging question + approach]
```

## Detailed Mode Workflow

For comprehensive analysis, follow the methodology in `references/detailed-assessment-criteria.md`.

Output includes:
1. **BLUF**: Definitive recommendation with fit percentage
2. **CSF Table**: Each factor with weight (1-10), fit score (0-10), and reasoning
3. **Overall Fit Score**: Weighted average as percentage
4. **Confidence Level**: Low/Medium/High with reasoning
5. **Key Assumptions**: Assessment dependencies
6. **Strengths to Emphasize**: 3-5 strategic talking points
7. **Gaps to Address**: 3-5 mitigation strategies
8. **Passion Alignment**: Role fit with candidate's stated interests and career goals
9. **Final Recommendation**: Clear apply/pass decision with rationale

## Assessment Principles

- **Be brutally honest**: Surface uncomfortable truths the candidate needs to hear
- **Assume smart hiring managers**: They will identify gaps; better to prepare for them
- **Weight recent experience heavily**: Last 3-5 years matter most
- **Consider trajectory**: Demonstrated growth patterns indicate future potential
- **Factor in passion**: Misalignment with interests predicts dissatisfaction regardless of skills
