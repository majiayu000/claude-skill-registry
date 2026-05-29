---
name: job-fit-analysis
description: Analyze fit between job requirements and background using lexicons - identifies gaps, develops reframing strategies, creates cover letter plan
---

# Job Fit Analysis

## Overview

Analyze fit between job requirements and your background using career lexicons. Identifies strengths, gaps, and develops strategic reframing approaches. Creates detailed cover letter plan grounded in authentic experience.

**Core principle:** Trust the job analysis output - don't re-parse requirements. Focus on gap identification and strategic positioning.

**Announce at start:** "I'm analyzing your fit for this role by comparing the job requirements with your career lexicons to identify strengths, gaps, and opportunities for strategic positioning."

## When to Use

**Standalone:**
- "Analyze my fit for this role"
- "What are my gaps for this position?"
- "Help me plan my cover letter"

**As follow-up to:**
- Job description analysis (need requirements first)
- Resume alignment (understand competitive position)

## Lexicon Integration

**Reads:**
- ✅ `~/career-applications/[job-slug]/01-job-analysis.md` (requirements)
- ✅ `~/lexicons_llm/01_career_philosophy.md` (values)
- ✅ `~/lexicons_llm/02_achievement_library.md` (experience)

**Outputs:**
- Gap analysis with ✅/⚠️/❌ symbols
- Reframing strategies for partial matches
- Cover letter strategic plan
- Evidence trail linking recommendations to lexicons

## Configuration

**Default paths (user can override):**
```python
LEXICONS_DIR = "~/lexicons_llm/"
APPLICATIONS_DIR = "~/career-applications/"
OUTPUT_FILE_PATTERN = "{job-slug}/03-gap-analysis-and-cover-letter-plan.md"
```

## Workflow

### Phase 0: Lexicon Loading

**Required files:**

1. Read: `~/career-applications/[job-slug]/01-job-analysis.md`
   - If missing: "I need a job analysis first. Should I analyze the job description now?"

2. Read: `~/lexicons_llm/01_career_philosophy.md` → store as context
   - If missing: "I need your career lexicons. Run: python run_llm_analysis.py"

3. Read: `~/lexicons_llm/02_achievement_library.md` → store as context

**Important:** Trust the job analysis - don't re-parse the job description. Use the structured analysis directly.

**Verification:** Confirm all files loaded successfully before proceeding

### Phase 1: Load & Review

**Actions:**
- Display job analysis summary (key requirements by priority)
- Review relevant lexicon sections
- Identify potentially matching categories
- Confirm understanding with user

**User Communication:**
```
I've loaded:
- Job analysis for [Job Title] at [Company]
- Your career philosophy ([N] leadership approaches, [N] core values)
- Your achievement library ([N] major categories, [N] key achievements)

Key Job Requirements (from analysis):
1. [Requirement 1] - Priority: HIGH
2. [Requirement 2] - Priority: HIGH
3. [Requirement 3] - Priority: MEDIUM

Relevant sections of your achievement library:
- Section II.A: Capital Projects (3 achievements)
- Section III.A: Revenue Generation (2 achievements)
- Section IV: Academic Leadership (4 achievements)

Ready to analyze your fit and identify opportunities for strategic positioning.
```

### Phase 2: Gap Analysis (Direct Comparison)

**For each requirement category from job analysis:**

Compare job requirements against lexicon achievements using direct matching:

**Output Format:**
```markdown
## Fit Analysis: Section II - Experience & Achievement Requirements

### Capital Projects & Infrastructure
JD Requirement: "$10M+ budget experience, adaptive reuse preferred"
Priority: HIGH (mentioned 7x, specific budget minimums)

Your Achievement Library:
✅ STRONG MATCH: Kirk Douglas Theater
   - $12.1M budget (exceeds requirement)
   - Adaptive reuse project (exact match)
   - 4 variations available for different emphases
   - Source: achievement_library.md:320-430
   - Assessment: COMPETITIVE STRENGTH - exceeds requirement

✅ STRONG MATCH: Outdoor Amphitheater
   - 600-seat venue, ground-up construction
   - Demonstrates range (new build + adaptive reuse)
   - Source: achievement_library.md:405-450
   - Assessment: Additional supporting evidence

Overall Assessment: COMPETITIVE STRENGTH - you exceed this requirement

---

### Team Leadership
JD Requirement: "Experience managing teams of 25+ in complex environments"
Priority: HIGH (mentioned 5x, organizational requirement)

Your Achievement Library:
✅ STRONG MATCH: Kirk Douglas Theater
   - Managed 50 full- and part-time staff
   - Cross-functional team complexity
   - Source: achievement_library.md:371
   - Assessment: STRONG - direct evidence with scale

⚠️  PARTIAL MATCH: Academic Advising Crisis
   - Leadership demonstrated, but not direct management
   - Team coordination vs. formal reporting structure
   - Source: achievement_library.md:890-920
   - Assessment: SUPPORTING - shows leadership capability

Overall Assessment: STRONG - direct evidence available

---

### Change Management Certification
JD Requirement: "Certified change management professional preferred"
Priority: MEDIUM (preferred, not required)

Your Achievement Library:
❌ GAP: No certification mentioned

⚠️  REFRAMING OPPORTUNITY:
   - Practical experience: Free-to-Earned Revenue Model transformation
   - Organizational change: 200+ employees affected
   - Evidence: achievement_library.md:520-560
   - Additional: Data Infrastructure Implementation (systems change)
   - Additional: Strategic Planning Leadership (cultural change)

Reframing Strategy Needed: Emphasize practical expertise, frame cert as growth opportunity

Overall Assessment: ADDRESSABLE GAP - strong practical foundation

---

### Values Alignment
JD Requirement: "Commitment to equity, diversity, inclusion, access, and belonging"
Priority: HIGH (mentioned throughout, cultural priority)

Your Career Philosophy:
✅ STRONG MATCH: Core Value - Arts as Social Justice
   - Direct alignment with DEI emphasis
   - Evidence from philosophy lexicon
   - Source: career_philosophy.md:215-240
   - Assessment: AUTHENTIC ALIGNMENT

✅ STRONG MATCH: Leadership Approach - Equity-Centered Practice
   - Structural commitment, not just values statement
   - Source: career_philosophy.md:125-160
   - Assessment: This is a strength to emphasize

Overall Assessment: AUTHENTIC ALIGNMENT - exceptional match
```

**Summary Matrix:**

After completing all categories, present summary:

```markdown
## Overall Fit Summary

**Competitive Position:** STRONG CANDIDATE

### Strengths (✅ Direct Matches)
1. Capital Projects & Infrastructure - EXCEEDS requirement
2. Team Leadership - STRONG with direct evidence
3. Values Alignment - EXCEPTIONAL (authentic overlap)
4. Stakeholder Management - COMPETITIVE STRENGTH
5. [Continue for all strong matches]

Total: 8 of 10 key requirements

### Partial Matches (⚠️ Need Reframing)
1. Change Management - Strong practical experience, no certification
2. [Other partial matches]

Total: 2 requirements

### Gaps (❌ Missing Requirements)
1. [If any critical gaps exist]

Total: 0 critical, 1 preferred (certification)

**Recommended Application Strategy:**
Lead with capital project + stakeholder strength, emphasize values alignment,
address certification gap proactively through reframing
```

### Phase 2.5: Gap Verification with User

**CRITICAL: Before proceeding to reframing or document creation, verify all identified gaps with the user.**

**Why this phase exists:**
- Ensure gaps are genuine (not analysis errors)
- Identify information missing from lexicons
- Catch achievements that exist but weren't surfaced
- Prevent inaccurate competitive positioning

**Process for each identified gap (❌) or partial match (⚠️):**

1. **Present the gap clearly:**
```
I identified a potential gap:

Requirement: [Exact requirement from job]
Priority: [HIGH/MEDIUM/LOW from job analysis]
Current Assessment: ❌ GAP or ⚠️ PARTIAL MATCH

My analysis: [Brief explanation of why assessed as gap]

Is this truly a gap in your background?
```

2. **Ask yes/no question using AskUserQuestion:**
```
Is "[requirement]" a genuine gap in your experience?
- Yes, I don't have this experience
- No, I do have this experience
```

3. **If user says "No" (gap is incorrect):**
```
You indicated you DO have experience with [requirement].

Help me understand what I missed:

A) This experience exists in different documents not yet in lexicons
   → Which documents should I look for?
   → What role/timeframe had this experience?

B) This experience is in the lexicon but I missed the connection
   → Can you point me to where this appears?
   → What achievement/section should I review?

C) The requirement is being interpreted too narrowly
   → How should I understand this requirement?
   → What experience of yours actually meets it?

D) This is captured under a different category/label
   → Where in your background does this appear?
```

4. **If user says "Yes" (confirmed gap):**
```
Confirmed gap: [requirement]

Follow-up questions:

A) Do you have ANY related experience (even if not exact match)?
   → What's the closest experience you have?
   → This helps us build reframing strategy

B) Is this a learnable skill or fixed requirement?
   → Can you develop this if hired?
   → Should we frame as growth opportunity?

C) How critical is this gap to your competitiveness?
   → Deal-breaker or addressable?
   → Should we apply anyway?
```

**Document all verification outcomes:**

```markdown
## Gap Verification Summary

### Verified Gaps (User Confirmed)
1. **[Requirement]** - Priority: [HIGH/MEDIUM/LOW]
   - User confirmation: "Yes, genuine gap"
   - Related experience: [If any]
   - Reframing potential: [HIGH/MEDIUM/LOW]
   - User notes: "[Any context provided]"
   - Verified: YYYY-MM-DD

### Corrected Assessments (Analysis Errors)
1. **[Requirement]** - Originally assessed as GAP
   - User correction: "I have this experience"
   - Location in background: [User's explanation]
   - Action needed:
     * ✅ Update lexicons with [specific documents]
     * ✅ Re-analyze Section [X] for this experience
     * ✅ Verify achievement at [lexicon location]
   - Status: REQUIRES LEXICON UPDATE

### Lexicon Gaps Identified
[List of missing information that should be added to lexicons]

### Analysis Improvements Needed
[List of misinterpretations or narrow readings to correct]
```

**Example Verification Conversation:**

```
I identified 3 potential gaps. Let's verify each:

GAP 1 of 3:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Requirement: "5+ years budget management experience with budgets exceeding $1M"
Priority: HIGH (mentioned 4x, critical competency)
My Assessment: ⚠️ PARTIAL MATCH

Why: I found your Shakespeare Center budget ($1.6M) but this was 3 years, not 5.

Is this a genuine gap? (Yes/No)

[User answers: "No"]

You indicated you DO have 5+ years of $1M+ budget experience.

What did I miss?
A) Experience in documents not yet in lexicons
B) Experience is in lexicon but I missed it
C) I'm interpreting the requirement too narrowly
D) This appears under different category/label

[User answers: "B - My current COTA Associate Dean role has $29M budget and I've been in it for 2 years, plus Shakespeare Center was 3 years = 5 years total"]

Thank you! I see the issue. I didn't connect your COTA role budget to this requirement.

Let me update my analysis:
✅ STRONG MATCH - EXCEEDS:
- Current role: $29M budget (2 years and ongoing)
- Previous role: $1.6M budget (3 years)
- Total: 5+ years with budgets exceeding $1M
- Actually EXCEEDS requirement substantially

This changes your competitive position significantly. Continuing verification...
```

**Timing:**
- Complete gap verification BEFORE Phase 3 (Reframing)
- May need to loop back to Phase 2 if major corrections needed
- Document updates required before proceeding to cover letter plan

**Success Criteria:**
✅ Every gap/partial match verified with user
✅ User had opportunity to correct analysis errors
✅ Missing lexicon content identified for future updates
✅ User confirms final gap list before reframing strategies developed
✅ Competitive position assessment is accurate

---

### Phase 3: Reframing Strategy Development

**For each VERIFIED gap or partial match from Phase 2.5:**

Use AskUserQuestion tool to present reframing options:

**Example:**
```markdown
Gap Identified: "Change management certification preferred"

Your Background: Extensive practical change management experience
- Free-to-Earned Revenue Model (organizational transformation)
- Data Infrastructure Implementation (systems change)
- Strategic Planning Leadership (cultural change)

Reframing Options:

A) Emphasize Practical Expertise
"While not formally certified in change management, I have led three major
organizational transformations affecting 200+ employees, applying change
management principles including stakeholder analysis, communication planning,
and resistance mitigation"

Best for: When practical experience is extensive and certification is "preferred" not "required"
Philosophy connection: Evidence-based practice (career_philosophy.md:280)
Achievement sources: achievement_library.md:520, 670, 890

B) Frame as Growth Opportunity
"My practical change management experience positions me to pursue formal
certification, which would formalize the expertise gained through [specific examples]"

Best for: When showing commitment to professional development
Demonstrates: Growth mindset, continuous learning
Complements: Your other certifications/credentials

C) Highlight Transferable Framework
"Applied evidence-based change management frameworks in [specific transformation],
including Kotter's 8-step model for the revenue transition and adaptive leadership
principles for the data infrastructure implementation"

Best for: When you've used recognized frameworks even without formal training
Demonstrates: Theoretical grounding + practical application
Achievement sources: achievement_library.md:520-560

Which approach feels most authentic and strategic?
```

**Process:**
- Present 2-3 reframing options for each gap
- Ground each option in actual lexicon achievements
- User confirms preferred approach
- Document chosen strategy with sources
- Build reframing list for cover letter integration

**Build Reframing Documentation:**
```python
reframing_strategies = {
    "change_management_certification": {
        "gap": "Certification preferred",
        "background": "Extensive practical experience",
        "chosen_approach": "A) Emphasize Practical Expertise",
        "sources": ["achievement_library.md:520", "achievement_library.md:670"],
        "cover_letter_integration": "Paragraph 3: Transformation Experience",
        "user_confirmed": "2025-10-31"
    }
}
```

### Phase 4: Cover Letter Plan Development

**Based on gaps + reframing + strengths:**

**Structure:**
```markdown
## Cover Letter Strategic Plan

### Opening Strategy (Values Alignment)
**Recommendation:** Institutional Positioning pattern
**Why:** Job emphasizes [Company]'s unique assets in [sector/context]

**From your narrative patterns:**
- Pattern: "[Institution] is uniquely positioned by..."
- Source: narrative_patterns.md:130-145
- When to use: Academic, mission-driven organizations

**Application to this role:**
"[Company's] [Department] is uniquely positioned by its intersection
of [asset 1], [asset 2], and [asset 3] to [mission]—a vision that aligns
precisely with my [N]-year commitment to [your philosophy value]."

**Example:**
"UCLA's School of the Arts and Architecture is uniquely positioned by its intersection
of artistic excellence, research innovation, and public mission to advance arts as
a tool for social transformation—a vision that aligns precisely with my 15-year
commitment to arts-as-social-justice practice."

**Philosophy connection:**
Links to career_philosophy.md:215 (Arts as Social Justice value)

**Keywords to incorporate:**
- [Keyword 1 from job analysis]
- [Keyword 2 from job analysis]

---

### Middle Development (Achievements + Reframing)

**Paragraph 2: [Primary Strength - Achievement Category]**
**Recommended Achievement:** [Achievement Name]
**Variation:** [Variation type from library]
**Why this achievement:**
- Connects to: Their emphasis on "[requirement]"
- Scale: [Exceeds/Meets/Demonstrates] requirement
- Demonstrates: [Key competency]

**Source:** achievement_library.md:[line numbers]

**Narrative Pattern:** Challenge → Action → Result
**Estimated length:** 120-140 words

**Draft Guidance:**
Context/Challenge: "[Set up the situation]"
Action: "[Your role and approach]"
Result: "[Quantifiable outcome and impact]"

**Language notes:**
- Use verb: "[verb from language bank]" (language_bank.md:[line])
- Incorporate keyword: "[job priority keyword]"
- Emphasize: [competency they prioritized]

---

**Paragraph 3: [Secondary Strength or Transformation + Reframe]**
**Recommended Achievement:** [Achievement Name]
**Connects to:** [Job requirement and any gap to address]
**Reframing strategy:** [If addressing gap, reference strategy from Phase 3]

**Source:** achievement_library.md:[line numbers]

**Narrative Pattern:** Context → Insight → Application
**Estimated length:** 120-140 words

**Draft Guidance:**
Context: "[Situational setup that shows understanding]"
Insight: "[Your recognition or learning]"
Application: "[How you applied this, with results]"

[If reframing a gap:]
**Reframe language:** "[Approved reframing approach from Phase 3]"

---

**Paragraph 4: [Values-Driven Leadership or Additional Strength]**
**Recommended Focus:** [Philosophy theme or achievement]
**Connects to:** Their [value/requirement] commitment

**Source:** career_philosophy.md:[line numbers]

**Purpose:** Deepen values alignment, show cultural fit
**Estimated length:** 100-120 words

---

### Closing Strategy
**Recommendation:** Values Reaffirmation + Forward-Looking Invitation
**Pattern:** Synthesize alignment + vision + invitation
**Source:** narrative_patterns.md:155-165

**Template:**
"The [Job Title] role offers the opportunity to bring my [strength 1],
[strength 2], and [philosophy value] to an institution uniquely positioned
to [their mission]. I would welcome the opportunity to discuss how my
experience aligns with [Company]'s vision for [department/initiative]."

**Tone notes:**
- "offers the opportunity" = enthusiastic but not presumptuous
- "uniquely positioned" = callback to opening (structural cohesion)
- "discuss how" = invitation, collaborative tone
- Avoid: "I am the ideal candidate" (presumptuous)

**Estimated length:** 70-80 words

---

### Tone Profile
**Job requirement (from analysis Section III):**
- [Formality level from job analysis]
- [Innovation level from job analysis]
- [Collaboration level from job analysis]

**Your natural voice (from past letters + lexicon):**
- [Your established tone patterns]
- [Your preferred narrative structures]
- [Your characteristic language]

**Recommended synthesis:**
- Formality level: [Specific recommendation]
- Sentence structure: [Mix description]
- Vocabulary: [Guidance on word choices]
- Emotional register: [Tone description]

**Language guidance:**
- ✅ Use: [Verbs/phrases from your language bank that match their culture]
- ✅ Mirror their verbs: "[verb 1]," "[verb 2]," "[verb 3]"
- ❌ Avoid: [Language not in your lexicon or mismatched to their culture]

---

### Total Estimated Length
- Opening: ~100 words
- Development: ~360 words (3 paragraphs × 120 words)
- Closing: ~75 words
- **Total: 535 words** (appropriate for this role level)

---

### Integration with Resume
**Ensure complementarity, not duplication:**

**Resume emphasizes:** [Achievement aspects highlighted in resume]
**Cover letter emphasizes:** [Different aspects or additional context]

**Example:**
- Resume bullet: "Stewarded $12.1M capital project from conception through delivery"
- Cover letter expansion: Context of partnership complexity, stakeholder navigation, community impact
```

### Phase 5: JSON Export for Wrapper Application

**After completing cover letter plan development, create structured JSON output:**

**Write to:** `~/career-applications/[job-slug]/job-fit-analysis-v1.json`

**Structure:**
```json
{
  "metadata": {
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "version": 1,
    "skill": "job-fit-analysis",
    "job_analysis_file": "job-analysis-v1.json",
    "lexicons_referenced": [
      "01_career_philosophy.md",
      "02_achievement_library.md"
    ]
  },
  "fit_assessment": {
    "overall_match_percentage": 82,
    "match_level": "strong",
    "confidence": "high",
    "summary": "Strong candidate with most requirements met",
    "direct_matches": 8,
    "total_requirements": 10,
    "partial_matches": 2,
    "missing_requirements": 0,
    "competitive_position": "STRONG CANDIDATE"
  },
  "strengths": [
    {
      "category": "Capital Projects",
      "requirement": "Experience managing $5M+ capital projects",
      "evidence": "Managed $12.1M Kirk Douglas Theater renovation, exceeds requirement by 140%",
      "achievement_source": "achievement_library.md:320-430",
      "competitive_advantage": "high",
      "assessment": "EXCEEDS requirement",
      "recommendation": "Lead with this in resume and cover letter"
    },
    {
      "category": "Stakeholder Management",
      "requirement": "Multi-stakeholder engagement experience",
      "evidence": "Cross-functional teams, city planning, donor partnerships",
      "achievement_source": "achievement_library.md:358-370",
      "competitive_advantage": "medium",
      "assessment": "STRONG match",
      "recommendation": "Emphasize breadth of stakeholders"
    }
  ],
  "gaps": [
    {
      "requirement": "Grant writing experience",
      "priority": "medium",
      "verified": true,
      "verification_date": "YYYY-MM-DD",
      "your_experience": "none_mentioned",
      "related_experience": "Budget management and fundraising partnerships",
      "severity": "medium",
      "mitigation_strategy": "Emphasize budget management and fundraising partnerships",
      "reframing_approach": "Emphasize Practical Expertise",
      "addressable": true,
      "user_confirmed": true,
      "cover_letter_integration": "Paragraph 3: Transformation Experience"
    },
    {
      "requirement": "Higher ed specific experience",
      "priority": "low",
      "verified": true,
      "verification_date": "YYYY-MM-DD",
      "your_experience": "performing_arts_education",
      "related_experience": "Colburn School educational leadership",
      "severity": "low",
      "mitigation_strategy": "Frame Colburn School as educational institution",
      "reframing_approach": "Highlight Transferable Framework",
      "addressable": true,
      "user_confirmed": true,
      "cover_letter_integration": "Opening: Institutional positioning"
    }
  ],
  "competitive_analysis": {
    "your_profile": "Capital projects leader with strong stakeholder management",
    "ideal_candidate": "Higher ed facilities director with fundraising experience",
    "competitive_position": "strong",
    "likely_competitors": [
      "Current higher ed facilities managers",
      "Capital project directors from similar institutions"
    ],
    "your_differentiation": "Broader stakeholder range, larger project scale",
    "estimated_competitiveness": 0.82
  },
  "recommendations": {
    "resume": [
      "Lead with $12.1M project and scale",
      "Use 'stakeholder management' 3x minimum",
      "Frame Colburn as educational institution",
      "Emphasize budget management expertise"
    ],
    "cover_letter": [
      "Open with capital projects strength",
      "Address grant gap by emphasizing fundraising partnerships",
      "Connect performing arts education to higher ed mission",
      "Use institutional positioning pattern"
    ],
    "interview_prep": [
      "Prepare grant writing interest story",
      "Emphasize quick learning and adaptability",
      "Have DEI initiatives ready",
      "Prepare questions about team structure and resources"
    ]
  },
  "risk_assessment": {
    "deal_breakers": [],
    "concerns": [
      {
        "issue": "Limited direct grant writing",
        "severity": "medium",
        "addressability": "high",
        "strategy": "Express willingness to learn, cite related experience"
      }
    ],
    "red_flags_for_you": [
      {
        "flag": "No team size mentioned",
        "interpretation": "Unclear support structure",
        "action": "Ask in interview about team and resources",
        "severity": "low"
      }
    ]
  },
  "cover_letter_plan": {
    "opening_strategy": {
      "pattern": "Institutional Positioning",
      "source": "narrative_patterns.md:130-145",
      "estimated_length": 100,
      "keywords_to_incorporate": ["keyword1", "keyword2"]
    },
    "development_paragraphs": [
      {
        "paragraph_number": 2,
        "focus": "Capital Projects Leadership",
        "achievement": "Kirk Douglas Theater",
        "variation": "Stakeholder Engagement Focus",
        "source": "achievement_library.md:358-370",
        "narrative_pattern": "Challenge → Action → Result",
        "estimated_length": 130,
        "connects_to_requirement": "Capital projects with $5M+ budgets"
      },
      {
        "paragraph_number": 3,
        "focus": "Transformation + Reframe grant gap",
        "achievement": "Free-to-Earned Revenue Model",
        "variation": "Change Management Focus",
        "source": "achievement_library.md:520-560",
        "narrative_pattern": "Context → Insight → Application",
        "estimated_length": 130,
        "connects_to_requirement": "Change management and fundraising",
        "reframing_strategy": "Emphasize practical expertise"
      },
      {
        "paragraph_number": 4,
        "focus": "Values-Driven Leadership",
        "achievement": "Arts as Social Justice commitment",
        "source": "career_philosophy.md:215-240",
        "narrative_pattern": "Values alignment",
        "estimated_length": 110,
        "connects_to_requirement": "DEI and mission alignment"
      }
    ],
    "closing_strategy": {
      "pattern": "Values Reaffirmation + Forward-Looking Invitation",
      "source": "narrative_patterns.md:155-165",
      "estimated_length": 75
    },
    "tone_profile": {
      "formality": "professional-collaborative",
      "sentence_structure": "mix of simple and complex",
      "vocabulary": "accessible expertise",
      "emotional_register": "enthusiastic but measured"
    },
    "total_estimated_length": 535
  },
  "application_priority": "high",
  "recommended_next_steps": [
    "Align resume emphasizing capital projects",
    "Draft cover letter addressing gaps proactively",
    "Prepare grant writing learning story for interviews"
  ]
}
```

**Implementation:**
1. Check if `job-fit-analysis-v1.json` already exists
2. If exists, increment version number: `job-fit-analysis-v2.json`, `job-fit-analysis-v3.json`, etc.
3. Extract structured data from the markdown analysis completed in Phases 2-4
4. Populate all fields based on verified gap analysis and user-confirmed reframing strategies
5. Write JSON file with proper formatting (2-space indentation)
6. Save to same directory as markdown file and job analysis

**Data Mapping Guide:**

- `fit_assessment` → Extract from Phase 2 summary matrix
- `strengths` → Extract from Phase 2 ✅ STRONG MATCH assessments
- `gaps` → Extract from Phase 2.5 verified gaps with user confirmation
- `competitive_analysis` → Extract from Phase 2 overall assessment
- `recommendations` → Extract from Phase 4 cover letter plan
- `risk_assessment` → Combine Phase 2.5 gap verification with job analysis red flags
- `cover_letter_plan` → Extract from Phase 4 detailed plan structure

**Final Message After JSON Export:**
```
Gap analysis, cover letter plan, and structured data export complete! Saved to:
- ~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md (full analysis)
- ~/career-applications/[job-slug]/job-fit-analysis-v1.json (structured data)

Summary:
- Competitive position: [STRONG/MODERATE/STRETCH CANDIDATE]
- Direct matches: [N] of [N] key requirements
- Gaps requiring reframing: [N] (all verified with you)
- Strategic approach: [1-sentence summary]

Your competitive strengths:
1. [Top strength]
2. [Second strength]
3. [Third strength]

Addressable gaps:
1. [Gap with reframing strategy]

Cover letter plan created with:
- Opening strategy: [pattern name]
- [N] development paragraphs using [N] achievements
- Tone profile: [description]

Next steps:
1. Review the complete analysis
2. Proceed to cover letter voice development
3. Begin collaborative drafting
```

## Output Generation

**Write to:** `~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md`

**File template:**
```markdown
---
job_title: [from job analysis]
company: [from job analysis]
date_created: YYYY-MM-DD
lexicons_referenced:
  - file: 01-job-analysis.md
    sections: [All sections]
  - file: 01_career_philosophy.md
    sections: [I.C, II.A]
  - file: 02_achievement_library.md
    sections: [II.A, II.B, III.A]
competitive_position: STRONG CANDIDATE
---

# Job Fit Analysis & Cover Letter Plan
## [Job Title] - [Company]

## I. Overall Fit Assessment

**Competitive Position:** STRONG CANDIDATE
- Direct matches: 8 of 10 key requirements
- Partial matches: 2 (with reframing strategies)
- Missing requirements: 0 critical, 1 preferred (certification)
- Values alignment: EXCEPTIONAL (authentic overlap)

**Recommended Application Strategy:**
[Strategic summary: what to lead with, what to emphasize, how to address gaps]

---

## II. Detailed Gap Analysis

[Full analysis from Phase 2, organized by requirement category]

### [Category 1]: [Requirement Name]
[Complete analysis with ✅/⚠️/❌ symbols, sources, assessments]

### [Category 2]: [Requirement Name]
[Complete analysis]

[Continue for all categories...]

---

## III. Reframing Strategies

**Gaps and Partial Matches Requiring Strategic Positioning:**

### 1. [Gap or Partial Match Name]
**Requirement:** [What they're asking for]
**Your Background:** [What you have]
**Chosen Reframing Approach:** [User-confirmed strategy from Phase 3]
**Sources:** [Lexicon citations]
**Cover Letter Integration:** [Where/how to incorporate]
**User Confirmed:** YYYY-MM-DD

### 2. [Next Gap if any]
[Same format]

---

## IV. Cover Letter Strategic Plan

[Complete plan from Phase 4 with narrative structure]

### Opening Strategy
[Detailed opening recommendation with template, sources, and rationale]

### Middle Development
#### Paragraph 2: [Focus]
[Achievement, variation, narrative pattern, draft guidance, sources]

#### Paragraph 3: [Focus]
[Achievement, variation, narrative pattern, draft guidance, sources]

#### Paragraph 4: [Focus]
[Achievement or philosophy focus, pattern, guidance, sources]

### Closing Strategy
[Template, tone notes, estimated length]

### Tone Profile
[Detailed tone guidance matching job culture + your voice]

### Total Estimated Length
[Word count breakdown by section]

### Integration with Resume
[Complementarity guidance]

---

## V. Evidence & Source Map

**All recommendations linked to lexicon sources:**

Opening strategy ← narrative_patterns.md:130
Capital project emphasis ← achievement_library.md:358
Values alignment ← career_philosophy.md:215
Reframing approach ← achievement_library.md:520 + user confirmation (2025-10-31)
Tone guidance ← job-analysis.md Section III + language_bank.md
Closing pattern ← narrative_patterns.md:160

[Continue for all major recommendations...]

---

## VI. Next Steps

**Options:**

A) Proceed to cover letter voice development
   - Invoke: cover-letter-voice skill
   - Reads this plan + narrative patterns + language bank
   - Develops detailed narrative framework

B) Begin collaborative drafting
   - Invoke: collaborative-writing skill
   - Uses this plan as guide
   - Co-creates draft iteratively

C) Draft independently and return for review
   - Use this plan as roadmap
   - Return for voice/consistency check

---
Generated: YYYY-MM-DD via job-fit-analysis skill
Version: 1.0
```

**Present to user:**
```
Gap analysis, cover letter plan, and structured data export complete! Saved to:
- ~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md (full analysis)
- ~/career-applications/[job-slug]/job-fit-analysis-v1.json (structured data)

Summary:
- Competitive position: [STRONG/MODERATE/STRETCH CANDIDATE]
- Direct matches: [N] of [N] key requirements
- Gaps requiring reframing: [N] (all verified with you)
- Strategic approach: [1-sentence summary]

Your competitive strengths:
1. [Top strength]
2. [Second strength]
3. [Third strength]

Addressable gaps:
1. [Gap with reframing strategy]

Cover letter plan created with:
- Opening strategy: [pattern name]
- [N] development paragraphs using [N] achievements
- Tone profile: [description]

Next steps:
1. Review the complete analysis
2. Proceed to cover letter voice development
3. Begin collaborative drafting
```

## Error Handling

### Missing Lexicons

```markdown
**If career_philosophy.md not found:**

"I can't find your career philosophy lexicon at ~/lexicons_llm/01_career_philosophy.md

I need this to analyze values alignment and develop authentic positioning.

To generate your lexicons:
1. cd /path/to/career-lexicon-builder
2. python run_llm_analysis.py

This analyzes your career documents and creates the lexicons I need.

Should I wait while you generate them?"
```

```markdown
**If achievement_library.md not found:**

"I can't find your achievement library at ~/lexicons_llm/02_achievement_library.md

I need this to match your verified achievements to job requirements.

To generate your lexicons:
1. cd /path/to/career-lexicon-builder
2. python run_llm_analysis.py

Should I wait while you generate them?"
```

### Missing Job Analysis

```markdown
**If no job analysis found:**

"I need a job analysis to know what requirements to compare against.

Options:
1. Analyze the job description now (I'll invoke job-description-analysis skill)
2. You already have an analysis - specify the path
3. Cancel and run job analysis separately

Which would you prefer?"

[If user chooses option 1:]
"I'll analyze the job description first, then return to the fit analysis.
Please paste or upload the job posting."
```

### No Matching Achievements

```markdown
**If no lexicon achievements match a HIGH priority requirement:**

"I couldn't find achievements in your library that directly match this HIGH priority requirement:
'[Requirement from job]'

This suggests either:
1. You have this experience but it's not in your lexicons
   → Add documents covering this experience and regenerate lexicons

2. This is a genuine gap (significant competitive concern)
   → We can develop reframing strategy but it may be a stretch

3. The requirement can be demonstrated through different achievements
   → Let's explore transferable experience

What would you like to do:
- Explore transferable achievements in your library
- Add this as a critical gap requiring cover letter attention
- Update lexicons with missing experience first
- Proceed with gaps documented for transparent assessment
```

### User Rejects Reframing Strategy

```markdown
**If user says "None of these reframing approaches feel authentic":**

"I understand these don't resonate. Let's explore this differently.

For the gap: [Requirement]

What is it about these approaches that feels inauthentic?
- The language doesn't sound like you?
- The framing feels like spin?
- The achievement examples don't truly connect?
- Something else?

[Listen to response]

Based on what you've shared, let me try a different approach:

[Generate new reframing options based on user feedback]

Or we can:
- Acknowledge this as a straightforward gap in cover letter
- Focus on compensating strengths instead
- Skip addressing this requirement entirely

What feels most aligned with your values?"
```

### Weak Competitive Position

```markdown
**If overall assessment shows user is under-qualified:**

"Based on this analysis, I need to share a strategic concern:

You match [N] of [N] requirements, but the gaps are in HIGH priority areas:
- [Critical gap 1]
- [Critical gap 2]

This suggests you may be under-qualified for this specific role as posted.

However, consider:

A) Strategic Application Anyway
   - Possible: if you have unique value proposition they haven't considered
   - Risk: Time investment with low conversion probability
   - Approach: Very strong values alignment story + long-term potential framing

B) Wait for Better Fit
   - Look for similar roles with requirements better matched to your background
   - Build missing experience first
   - Apply when competitive position is stronger

C) Networking Approach
   - Connect with hiring manager before formal application
   - Learn if requirements are flexible
   - Understand if they'd consider candidates with different profile

What's your instinct about how to proceed?"
```

## Success Criteria

✅ Gaps identified and ranked by job priority (not random order)
✅ Reframing strategies grounded in actual lexicon achievements (no fabrication)
✅ Cover letter plan has clear narrative direction and structure
✅ User feels confident about positioning (not anxious about gaps)
✅ All recommendations linked to specific lexicon sources
✅ Authentic alignment opportunities identified (not manufactured)
✅ User understands competitive position realistically
✅ Strategic approach is actionable and authentic

## Example Output Excerpt

```markdown
## II. Detailed Gap Analysis

### Capital Projects & Infrastructure
JD Requirement: "Proven experience managing capital projects with budgets exceeding $5M"
Priority: HIGH (mentioned 7x, first requirement in qualifications section)

Your Achievement Library:
✅ STRONG MATCH: Kirk Douglas Theater
   - $12.1M budget (EXCEEDS requirement by 140%)
   - Adaptive reuse project (matches sector context)
   - Multi-stakeholder complexity (public-private partnership)
   - Source: achievement_library.md:320-430
   - Variations available:
     * Variation A: Project Management Focus (lines 338-342)
     * Variation B: Financial Stewardship Focus (lines 348-352)
     * Variation C: Stakeholder Engagement Focus (lines 358-370)

✅ STRONG MATCH: Outdoor Amphitheater
   - 600-seat venue, ground-up construction
   - Demonstrates range: new construction + adaptive reuse
   - Source: achievement_library.md:405-450
   - Purpose: Supporting evidence of consistent capital project success

Assessment: COMPETITIVE STRENGTH
You don't just meet this requirement—you exceed it with verified, large-scale experience.
This should be a PRIMARY emphasis in both resume and cover letter.

Recommendation: Use Kirk Douglas Theater (Variation C: Stakeholder focus) in cover letter
to connect capital project expertise with their collaboration culture emphasis.

→ **Ready for cover letter paragraph 2 (primary achievement story)**
```

---
**END OF SKILL**
