---
name: job-application-optimizer
description: Strategic job application planning and Resume SEO optimization. Approaches applications like marketing campaigns with market research, opportunity qualification, and content optimization. Activate on 'optimize resume', 'tailor resume', 'ATS optimization', 'job fit score', 'should I apply'. NOT for initial career narratives (career-biographer), portfolio design (cv-creator), or market positioning (competitive-cartographer).
allowed-tools: Read,Write,Edit,WebSearch,WebFetch
category: Business & Monetization
tags:
  - job-search
  - ats
  - resume-seo
  - application
  - optimization
pairs-with:
  - skill: cv-creator
    reason: Generate optimized CVs
  - skill: competitive-cartographer
    reason: Understand job market positioning
---

# Job Application Optimizer

Strategic job application planning and "Resume SEO" optimization. This skill teaches Claude to approach job applications like a marketing campaign - researching the market, qualifying opportunities, and optimizing content for maximum conversion.

## When to Activate

Activate on:
- "optimize my resume for this job"
- "should I apply to this job"
- "tailor my resume"
- "ATS optimization"
- "keyword optimization"
- "job search strategy"
- "application strategy"
- "resume SEO"
- "job fit score"

NOT for:
- Initial career narrative creation (use career-biographer)
- Portfolio website design (use cv-creator directly)
- Market positioning analysis (use competitive-cartographer)
- General resume formatting (use cv-creator directly)

## Core Philosophy: Resume SEO

Treat job applications like search engine optimization:

| SEO Concept | Resume Equivalent |
|-------------|-------------------|
| Search query | Job description |
| Web page | Resume |
| Keywords | Skills & requirements |
| Meta description | Professional summary |
| H1 heading | Job title/headline |
| Content quality | Achievement metrics |
| Keyword density | Skills frequency (2-4% optimal) |
| Backlinks | Referrals & endorsements |
| Page speed | Scan time (&lt;6 seconds) |

## Strategic Framework

### 1. Opportunity Qualification

Before optimizing, determine if the job is worth applying to:

**APPLY signals:**
- Match score &gt;65% on core requirements
- &lt;3 years experience gap
- Transferable skills cover &gt;50% of gaps
- Company culture aligns (green flags)
- Compensation in range

**SKIP signals:**
- Match score &lt;50% with hard blockers
- &gt;5 years experience gap
- Required certifications you don't have
- Multiple red flags (rockstar, wear many hats)
- Major relocation required (if not willing)

### 2. Keyword Research

Like SEO keyword research, extract and prioritize:

**Primary Keywords (must include):**
- Job title (exact match)
- Top 5 required skills
- Required certifications
- Industry/domain terms

**Secondary Keywords (should include):**
- Preferred skills
- Technology stack specifics
- Methodology terms (Agile, Scrum)

**Long-tail Keywords (nice to have):**
- Specific tools mentioned
- Soft skills emphasized
- Cultural values expressed

### 3. Tailoring Levels

**LIGHT Tailoring** (match &gt;80%)
- Time: 15 minutes
- Reorder skills to match job priority
- Add 2-3 missing keywords to summary
- Ensure job title alignment
- Risk: None

**MEDIUM Tailoring** (match 60-80%)
- Time: 30 minutes
- Rewrite summary with top keywords
- Add skills section entries
- Emphasize relevant experience bullets
- Add 1-2 relevant projects
- Risk: Low

**AGGRESSIVE Tailoring** (match 50-65%)
- Time: 1 hour
- Complete summary rewrite
- Restructure skills by relevance
- Modify experience bullets with keywords
- Add quantifiable metrics
- Create variant resume
- Risk: Medium (over-optimization possible)

### 4. ATS Optimization Checklist

Before submitting, verify:

**Format:**
- [ ] Single-column layout
- [ ] Standard fonts (Arial, Calibri, Georgia)
- [ ] No tables, columns, text boxes
- [ ] No headers/footers (info gets lost)
- [ ] PDF or DOCX (DOCX preferred for ATS)
- [ ] No images or graphics

**Structure:**
- [ ] Contact info at top (not in header)
- [ ] Standard section headers
- [ ] Reverse chronological order
- [ ] Consistent date format (Month YYYY)
- [ ] 1-2 pages maximum

**Content:**
- [ ] Word count 400-800
- [ ] 5+ quantifiable achievements
- [ ] Action verbs at bullet start
- [ ] No buzzwords/clichés
- [ ] Keywords in first 1/3 of resume

**Keywords:**
- [ ] Keyword density 2-4%
- [ ] Both acronyms and full forms (AWS/Amazon Web Services)
- [ ] Skills in dedicated section
- [ ] Keywords in summary
- [ ] Exact match for proper nouns

### 5. Application Batch Strategy

For job search campaigns:

**Daily:**
- Apply to 5-10 jobs (quality over quantity)
- Track applications in spreadsheet
- Follow up on week-old applications

**Weekly:**
- Review which resumes got responses
- A/B test resume variants
- Adjust keyword strategy based on results

**Monthly:**
- Analyze conversion rates
- Update master resume with new achievements
- Refresh networking outreach

## Tool Integration

This skill works with:

**cv-creator-mcp:**
```
analyze_job → score_match → suggest_tailoring → score_ats
```

**career-biographer:**
Provides the structured CareerProfile that cv-creator-mcp uses.

**competitive-cartographer:**
Provides positioning strategy and differentiators.

## Example Workflow: Alex Chen

```markdown
## Job: Senior Backend Engineer at TechCorp

### Step 1: Analyze Job
- Required: Go, Kubernetes, PostgreSQL, 5+ years
- Preferred: Kafka, gRPC, AWS
- Signals: Remote-friendly ✓, Equity ✓

### Step 2: Score Match
- Overall: 78/100 (GOOD_MATCH)
- Matched: Go, Kubernetes, PostgreSQL, Kafka, gRPC
- Missing: None critical
- Gap: 0 years (8 > 5 required)

### Step 3: Recommendation
- Apply: YES
- Tailoring Level: LIGHT
- Estimated Time: 15 minutes

### Step 4: Tailoring Actions
1. Reorder skills: Go first, then K8s, PostgreSQL
2. Add to summary: "Specialized in event-driven microservices"
3. Ensure "Senior Backend Engineer" exact match in headline

### Step 5: ATS Check
- Score: 85/100 ✓
- Quick wins: Add AWS certification date

### Step 6: Apply
- Resume: alex-chen-techcorp-v1.pdf
- Cover letter: Generated with connection hook
- Tracking: Added to spreadsheet
```

## Common Mistakes to Avoid

1. **Keyword Stuffing** - &gt;4% density triggers spam filters
2. **Generic Resume** - Same resume for every application
3. **Ignoring ATS** - Pretty resumes that machines can't read
4. **Over-tailoring** - Claims that can't be backed up
5. **Skipping Cover Letter** - Many ATS weight it heavily
6. **Wrong File Format** - PNG/JPG images of resumes
7. **Missing Contact** - Email in header that ATS loses

## Metrics to Track

| Metric | Target | Alex Chen Example |
|--------|--------|-------------------|
| Applications/week | 20-30 | 25 |
| Response rate | &gt;10% | 16% |
| Interview rate | &gt;5% | 8% |
| Offer rate | &gt;2% | 4% |
| ATS pass rate | &gt;80% | 92% |
| Avg match score | &gt;70% | 78% |

## Output Artifacts

When optimizing, produce:

1. **Match Analysis Report**
   - Score breakdown
   - Matched/missing keywords
   - Gaps and recommendations

2. **Tailored Resume**
   - Modified summary
   - Reordered skills
   - Keyword-optimized bullets

3. **Cover Letter**
   - Job-specific opening
   - Achievement highlights
   - Keywords integrated

4. **Application Tracker Entry**
   - Date applied
   - Version used
   - ATS score
   - Follow-up date
