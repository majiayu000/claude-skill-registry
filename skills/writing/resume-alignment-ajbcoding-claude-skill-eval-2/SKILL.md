---
name: resume-alignment
description: Tailor resumes to job descriptions using verified achievements from your lexicon - never fabricates, always traceable to source
---

# Resume Alignment

## Overview

Tailor your resume to specific job descriptions by matching verified achievements from your career lexicon to job requirements. Every statement is traceable to source—no fabrication, no exaggeration.

**Core principle:** Authentic alignment through verified evidence. All content must trace to lexicon sources or user-provided documents.

**Announce at start:** "I'm tailoring your resume using your achievement library to ensure authentic, verified alignment with this job."

## When to Use

- "Tailor my resume for this job"
- "Align my resume with this position"
- "Update my resume for [job title]"

## Lexicon Dependencies

**Required files:**
- ✅ `~/career-applications/[job-slug]/01-job-analysis.md` (what they need)
- ✅ `~/lexicons_llm/02_achievement_library.md` (what you have)
- ✅ `~/lexicons_llm/04_language_bank.md` (how to phrase it)

**Missing prerequisites:**
- If no job analysis: "I need a job analysis first. Should I analyze the job description now?"
- If no lexicons: "I need your career lexicons. Run: python run_llm_analysis.py"

## Configuration

**Default paths:**
```python
LEXICONS_DIR = "~/lexicons_llm/"
APPLICATIONS_DIR = "~/career-applications/"
OUTPUT_FILE_PATTERN = "{job-slug}/02-resume-tailored.md"
```

## Workflow

### Phase 0: Lexicon Loading

**Startup sequence:**

1. Check for job analysis file
```
ls ~/career-applications/*/01-job-analysis.md | sort -r | head -1
```

If found: "I found your analysis of [job title]. Use this?"
If not found: "No job analysis found. Options:
1. Analyze job description now
2. Specify path to existing analysis
3. Cancel"

2. Load lexicons
```
Read: ~/lexicons_llm/02_achievement_library.md → store in context
Read: ~/lexicons_llm/04_language_bank.md → store in context
```

If files not found: Error with instructions to run lexicon generator

3. Verify all files loaded successfully

**Confirmation:**
"Loaded successfully:
- Job analysis: [job title]
- Achievement library: [count] achievements across [categories]
- Language bank: [count] action verbs

Ready to match your achievements to job requirements."

### Phase 1: Job + Lexicon Review

**Display job analysis summary:**
```markdown
Job: [Title] at [Company]

Top Requirements (from analysis):
1. [Requirement 1] - Priority: HIGH
2. [Requirement 2] - Priority: HIGH
3. [Requirement 3] - Priority: MEDIUM

Relevant sections of your achievement library:
- Section II.A: Capital Projects (3 achievements)
- Section III.A: Revenue Generation (2 achievements)
- Section IV: Academic Leadership (4 achievements)
```

**Ask:** "Ready to select specific achievements for each requirement?"

### Phase 2: Match & Select

**For each high-priority job requirement:**

Use **AskUserQuestion tool** to present side-by-side comparison:

```markdown
## Requirement: "Project management experience with $5M+ budgets"

From your Achievement Library (Section II.A: Capital Projects):

**Option A: Kirk Douglas Theater - $12.1M Project**

Variation 1 (Project Management Focus):
"Stewarded $12.1M adaptive reuse project from conceptual sketch through
on-time, on-budget delivery, managing all phases including budgeting,
architect selection, regulatory approvals, construction oversight, and
operational launch"

Source: achievement_library.md:338-342
Best for: PM roles, operations positions, executive leadership
Highlights: Process management, timeline adherence, comprehensive scope

Variation 2 (Financial Stewardship Focus):
"Delivered on-time, on-budget completion of $12.1M capital project,
negotiating Disposition and Development Agreement with municipality and
managing complex public-private partnership financing"

Source: achievement_library.md:348-352
Best for: CFO/finance roles, budget-conscious positions, fiscal leadership
Highlights: Fiscal responsibility, budget management, financial structuring

**Option B: Outdoor Amphitheater - 600-seat venue**

Variation 1 (Scope Focus):
"Conceived and delivered 600-seat outdoor amphitheater from design through
completion, managing vendor relationships and regulatory compliance"

Source: achievement_library.md:405-408
Best for: Smaller-scale but comprehensive project examples
Highlights: End-to-end ownership, stakeholder coordination

Which achievement and variation best demonstrates your qualifications
for this requirement?

Options:
- Kirk Douglas (Variation 1 - Project Management)
- Kirk Douglas (Variation 2 - Financial Stewardship)
- Outdoor Amphitheater (Variation 1)
- None - I'll describe a different project
```

**Selection tracking:**
```python
selections = {
    "requirement_1": {
        "achievement": "Kirk Douglas Theater",
        "variation": "Project Management Focus",
        "source": "achievement_library.md:338-342",
        "text": "[full text]"
    }
}
```

**Language selection from language bank:**

```markdown
The job posting uses "stewarded" 3 times. Your language bank categorizes
this under:
- Section I.A.1: Vision & Planning (Strategic Leadership)
- Usage context: Opening statements, executive-level positioning
- Frequency in your materials: Used in 60% of executive role applications

Use "stewarded" for your capital project bullets? [Yes/No]

Alternative verbs from your language bank:
- "Led" (more common, less distinctive)
- "Oversaw" (similar authority level)
- "Directed" (slightly more authoritative)
```

**Build selection list for all requirements**

### Phase 3: Draft Creation

**Generate resume section by section**

For each section (Summary, Experience, Education, Skills):

**Present before/after comparison:**

```markdown
## Professional Experience

### Associate Producer | Center Theatre Group | 1997-2004

**Original (from your 2023 resume):**
"Led theater renovation project with team of contractors"

**Proposed (tailored for this role):**
"Stewarded $12.1M adaptive reuse project from conception through on-time,
on-budget delivery, managing cross-functional team of 50 full- and part-time
staff across design, construction, and operational launch phases"

**Source:** achievement_library.md:338 (Kirk Douglas Theater, Variation A: Project Management Focus)

**Keywords matched:**
- "stewarded" (job posting priority keyword)
- "$12.1M" (exceeds $5M+ requirement)
- "cross-functional team" (collaboration emphasis from posting)
- "on-time, on-budget" (fiscal responsibility signal)

**Does this accurately represent your experience?**
- Yes → Include as written
- No → Tell me what's inaccurate
- Adjust → What changes would make this authentic?
```

**Rules:**
- ONLY include after user confirms "Yes"
- If "No" → Ask "What's inaccurate?" → Revise → Re-present
- If "Adjust" → Socratic questioning → Refine → Re-present
- Track every confirmation with timestamp

**Evidence tracking:**

```python
evidence_trail = {
    "line_5": {
        "content": "Stewarded $12.1M adaptive reuse project...",
        "sources": [
            "achievement_library.md:338 (Kirk Douglas, Variation A)",
            "language_bank.md:192 (Strategic Leadership verbs)"
        ],
        "keywords_matched": ["stewarded", "$12.1M", "cross-functional"],
        "user_confirmed": "2025-10-31",
        "accurate": True
    }
}
```

**Continue for all resume sections**

### Phase 4: Authenticity Validation

**Present complete draft:**

```markdown
# [Your Name]

[Complete tailored resume with all sections]

---

## Evidence & Source Trail

**Line 5:** "Stewarded $12.1M adaptive reuse project..."
← achievement_library.md:338 (Kirk Douglas Theater, Variation A)
← language_bank.md:192 (Strategic Leadership: Vision & Planning)

**Line 8:** "Negotiated multi-party agreement..."
← achievement_library.md:358 (Kirk Douglas Theater, Variation C)
← language_bank.md:215 (Stakeholder Engagement: Collaborative)

[... continue for all bullets ...]

---

## Verification Checklist

☐ All achievements verified from lexicon
☐ All language from language bank or user's existing materials
☐ No fabrication or exaggeration
☐ User confirms authenticity
☐ ATS keywords from job analysis incorporated
```

**Final authenticity check:**

Ask: "Does this resume feel authentic to how you describe your work?"

**Wait for explicit confirmation before saving**

**If user has concerns:**
- "What feels inauthentic?" → Address specific concern
- Review that section against lexicon sources
- Revise or remove questionable content
- Re-confirm

**Only save after:** "Yes, this feels authentic"

### Phase 5: Output Generation

**Write to:** `~/career-applications/[job-slug]/02-resume-tailored.md`

**File template:**

```markdown
---
job_title: [from job analysis]
company: [from job analysis]
date_created: YYYY-MM-DD
lexicons_referenced:
  - file: 02_achievement_library.md
    sections: [II.A, III.A, IV]
  - file: 04_language_bank.md
    sections: [Strategic Leadership, Stakeholder Engagement]
verified: true
authenticity_confirmed: YYYY-MM-DD
fabrication_check: passed
---

# [Your Name]
[Contact Information]

## Professional Summary
[Tailored summary incorporating job keywords and philosophy]

## Professional Experience

### [Position Title] | [Organization] | [Dates]

• [Achievement 1 - fully sourced]
  → Source: achievement_library.md:[lines]
  → Keywords: [matched keywords]

• [Achievement 2 - fully sourced]
  → Source: achievement_library.md:[lines]
  → Keywords: [matched keywords]

[Continue for all positions...]

---

## Evidence Trail

**All content verified and sourced:**

Line 5: "Stewarded $12.1M project..."
  ← achievement_library.md:338 (Kirk Douglas Theater, Variation A)
  ← language_bank.md:192 (Strategic Leadership: Vision & Planning)
  ← Keywords: stewarded (JD priority), $12.1M (exceeds requirement)

[... full trail for every bullet ...]

---

## Verification Status

✅ No fabricated content
✅ All achievements traced to lexicon or user-provided documents
✅ User confirmed authenticity: YYYY-MM-DD
✅ ATS keywords from job analysis incorporated
✅ Every statement includes source citation
✅ Before/after comparison approved for all changes

---
Generated: YYYY-MM-DD via resume-alignment skill
Version: 1.0
```

**Present to user:**

```
Resume tailored and saved to:
~/career-applications/[job-slug]/02-resume-tailored.md

Summary:
- [N] achievements from your library
- [N] keywords from job analysis incorporated
- [N] action verbs matched to their language
- 100% verified (no fabricated content)

Next steps:
1. Review the tailored resume
2. Export to Word/PDF for submission
3. Proceed to job fit analysis (identify gaps + plan cover letter)
```

### Phase 6: JSON Export for Wrapper Application

**After generating markdown resume, create structured JSON output:**

**Write to:** `~/career-applications/[job-slug]/resume-alignment-v1.json`

**Structure:**
```json
{
  "metadata": {
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "version": 1,
    "skill": "resume-alignment",
    "job_title": "Position title",
    "company": "Organization name"
  },
  "matched_achievements": [
    {
      "requirement": "Job requirement description",
      "achievement": "Achievement text used in resume",
      "source": "achievement_library.md:lines",
      "alignment_score": 0.95,
      "keyword_matches": ["keyword1", "keyword2", "keyword3"],
      "variation_used": "Variation name (e.g., Project Management Focus)"
    }
  ],
  "keyword_coverage": {
    "critical_keywords": {
      "required_found": [
        {"term": "stakeholder management", "frequency": 3, "locations": ["summary", "line 5", "line 12"]}
      ],
      "required_missing": ["grant writing"],
      "coverage_percentage": 85
    },
    "important_keywords": {
      "optional_found": [
        {"term": "strategic planning", "frequency": 2, "locations": ["line 8", "line 15"]}
      ],
      "optional_missing": ["board governance"]
    }
  },
  "gap_analysis": {
    "missing_requirements": [
      {
        "requirement": "Grant writing experience",
        "severity": "high",
        "reason": "No matching achievements in library",
        "recommendation": "Address in cover letter or consider adding experience"
      }
    ],
    "weak_areas": [
      {
        "area": "Diversity & inclusion language",
        "current_coverage": "Limited",
        "recommendation": "Add DEI initiatives from achievement library Section IV"
      }
    ]
  },
  "recommendations": [
    {
      "type": "content",
      "priority": "high",
      "action": "Add bullet about $8M project to experience section",
      "reason": "Exceeds $5M requirement, strong alignment"
    },
    {
      "type": "keyword",
      "priority": "high",
      "action": "Use 'stakeholder management' terminology 3x",
      "reason": "Critical ATS keyword appearing 5x in job posting"
    },
    {
      "type": "quantification",
      "priority": "medium",
      "action": "Include team size (15 people) for scale demonstration",
      "reason": "Job emphasizes team leadership"
    }
  ],
  "alignment_score": {
    "overall_percentage": 87,
    "category_scores": {
      "experience_match": 90,
      "keyword_coverage": 85,
      "quantifiable_requirements": 95,
      "culture_alignment": 80
    },
    "competitive_position": "strong"
  },
  "evidence_trail": [
    {
      "resume_line": "Stewarded $12.1M adaptive reuse project...",
      "sources": [
        "achievement_library.md:338 (Kirk Douglas Theater, Variation A)",
        "language_bank.md:192 (Strategic Leadership verbs)"
      ],
      "keywords_matched": ["stewarded", "$12.1M", "cross-functional"],
      "user_confirmed": "YYYY-MM-DD",
      "authentic": true
    }
  ],
  "lexicons_referenced": {
    "achievement_library": {
      "file": "02_achievement_library.md",
      "sections_used": ["II.A", "III.A", "IV"],
      "total_achievements": 12
    },
    "language_bank": {
      "file": "04_language_bank.md",
      "sections_used": ["Strategic Leadership", "Stakeholder Engagement"],
      "total_terms": 25
    }
  }
}
```

**Implementation:**
1. Check if `resume-alignment-v1.json` already exists in directory
2. If exists, increment version: `resume-alignment-v2.json`, `resume-alignment-v3.json`, etc.
3. Extract structured data from the selections and evidence trail collected during workflow
4. Calculate alignment scores based on:
   - Percentage of high-priority requirements matched
   - Keyword coverage percentage from job analysis
   - Quantifiable requirement fulfillment
   - User confirmation of authenticity
5. Write JSON file with proper formatting (2-space indentation)
6. Save to same directory as markdown resume

**Final message to user:**
```
Resume alignment complete! Saved to:
- ~/career-applications/[job-slug]/02-resume-tailored.md (formatted resume with evidence trail)
- ~/career-applications/[job-slug]/resume-alignment-v1.json (structured data for analysis)

Alignment Summary:
- Overall match: 87%
- Achievements matched: [N] from your library
- Critical keywords: 85% coverage
- Gaps identified: [N] areas for cover letter
- Competitive position: Strong

Files ready for:
1. Resume export to Word/PDF
2. Gap analysis review
3. Cover letter development (address identified gaps)

Next steps:
1. Review the tailored resume and verify authenticity
2. Use job-fit-analysis skill for detailed competitive assessment
3. Develop cover letter addressing any gaps
```

## Error Handling

### Missing Lexicons

```markdown
**If achievement_library.md not found:**

"I can't find your achievement library at ~/lexicons_llm/02_achievement_library.md

To generate your lexicons:
1. cd /path/to/career-lexicon-builder
2. python run_llm_analysis.py

This analyzes your career documents and creates the lexicons I need
to tailor your resume authentically.

Should I wait while you generate them?"
```

### Missing Job Analysis

```markdown
**If no job analysis found:**

"I need a job analysis to know what requirements to match.

Options:
1. Analyze the job description now (I'll invoke job-description-analysis skill)
2. You already have an analysis - specify the path
3. Cancel and run job analysis separately

Which would you prefer?"
```

### No Matching Achievements

```markdown
**If no lexicon achievements match a requirement:**

"I couldn't find achievements in your library that match:
'[Requirement from job]'

This suggests either:
1. You have this experience but it's not in your lexicons (add documents + regenerate)
2. This is a genuine gap (we'll address in job-fit-analysis skill)
3. The requirement can be reframed using different experiences

What would you like to do:
- Skip this requirement for now
- Describe an unlisted experience (I won't add it without verification)
- Proceed with gaps documented for cover letter reframing
```

### User Rejects Proposed Text

```markdown
**If user says "No, that's not accurate":**

"What's inaccurate about this description?"

[Listen to response]

"Let me revise based on what you've shared:

[Revised text]

Source: [same or adjusted source]

Is this more accurate?"

**If still not accurate after 2 revisions:**

"This achievement may not be the right match for this requirement.

Options:
1. Choose a different achievement from your library
2. Skip this requirement
3. We can address this as a gap in the job-fit-analysis phase

Which would you prefer?"
```

## Success Criteria

✅ Every achievement traces to lexicon (source citations included)
✅ Every language choice references language bank or user's existing materials
✅ ATS keywords from job analysis incorporated appropriately
✅ User confirms: "This resume is authentic to my experience"
✅ No fabricated content (verified through evidence trail)
✅ Resume demonstrates competitive fit for the role
✅ All before/after comparisons approved by user

## Testing Validation

**Before claiming skill is complete:**

1. Test with real job + user's lexicons
2. Verify lexicon loading works
3. Confirm side-by-side achievement presentation
4. Check evidence trail includes all sources
5. Validate user cannot skip authentication without explicit confirmation
6. Ensure no hallucinated achievements
7. Confirm output file saved correctly with metadata

---
**END OF SKILL**
