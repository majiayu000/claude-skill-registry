---
name: job-description-analysis
description: Analyze job postings for requirements, culture, and values - outputs structured analysis matching lexicon categories for comparison and gap analysis
---

# Job Description Analysis

## Overview

Analyze job postings to identify requirements, extract ATS keywords, decode organizational culture, and surface values alignment opportunities. Output is structured to enable direct comparison with your career lexicons.

**Core principle:** Interpretive analysis that goes beyond literal reading - decode culture, identify priorities, read omissions, and structure findings for gap analysis.

**Announce at start:** "I'm analyzing this job description to identify requirements, culture signals, and strategic opportunities."

## When to Use

**Standalone:**
- "Analyze this job description"
- "Help me understand this job posting"
- "What are the key requirements for this role?"

**As prerequisite for:**
- Resume alignment (need job analysis first)
- Job fit analysis (need job analysis first)
- Cover letter development (need job analysis first)

## Lexicon Integration

**Reads:** NONE (standalone analysis of job posting only)

**IMPORTANT:** This skill analyzes the job posting without reading your career lexicons. It provides market analysis and job decoding but does NOT compare requirements against your specific background. Use the `job-fit-analysis` skill for personalized gap analysis and competitive assessment.

**Outputs structure matching:**
- Section I → Compare with `01_career_philosophy.md`
- Section II → Compare with `02_achievement_library.md`
- Section III → Compare with `03_narrative_patterns.md`
- Section IV → Compare with `04_language_bank.md`

## Configuration

**Default paths (user can override):**
```python
APPLICATIONS_DIR = "~/career-applications/"
OUTPUT_FILE_PATTERN = "{date}-{job-slug}/01-job-analysis.md"
```

## Workflow

### Phase 0: Setup

**Actions:**
- Accept job posting (paste, upload, or URL)
- Create job slug from title (lowercase, hyphens, max 50 chars)
- Initialize output directory

**Example:**
```
Input: "Senior Director, Center for the Arts - UCLA"
Slug: "senior-director-arts-ucla"
Directory: ~/career-applications/2025-10-31-senior-director-arts-ucla/
```

### Phase 1: Document Intake

**Accept formats:**
- Pasted text
- Uploaded PDF/Word document
- URL (extract with WebFetch tool)

**Validation:**
- Minimum 100 words (if less, ask: "Is this the complete posting?")
- Extract full text successfully
- Confirm with user: "I have the job description. Ready to analyze?"

### Phase 2: Structured Analysis (4 Sections)

**Generate analysis matching lexicon structure:**

#### Section I: Values & Philosophy Requirements

**Extract:**
- Leadership expectations (stated + implied)
- Core values signals (explicit statements + language patterns)
- Problem-solving philosophy (data-driven? collaborative? innovative?)
- Decision-making approach indicators

**Output format:**
```markdown
## I. Values & Philosophy Requirements

### Leadership Expectations
[What leadership style/approach do they signal?]
**Evidence:** "[Quote from posting]"

### Core Values Signals
**Explicit:** [Values they state directly]
**Implicit:** [Values evident from emphasis/language]
**Evidence:** "[Quotes supporting interpretation]"

### Problem-Solving Philosophy
[How do they approach challenges? What evidence?]
```

**Purpose:** Enables comparison with `01_career_philosophy.md`

#### Section II: Experience & Achievement Requirements

**Extract and categorize by achievement types:**
- Capital Projects & Infrastructure
- Organizational Transformation
- Revenue Generation & Growth
- Academic Leadership
- Team Building & Management
- Technical/Specialized Skills

**For each category, identify:**
- Required experience (explicit must-haves)
- Preferred experience (nice-to-haves)
- Quantifiable expectations (budget sizes, team sizes, scope)
- Scale indicators (project complexity, stakeholder range)

**Output format:**
```markdown
## II. Experience & Achievement Requirements

### Capital Projects & Infrastructure
**Required:** [Explicit requirements with quotes]
**Preferred:** [Nice-to-have elements]
**Quantifiable Expectations:**
- Budget range: $X-Y mentioned
- Team size: N+ people
- Project duration: [if specified]

**Evidence:** "[Quotes from posting]"

### [Continue for each relevant category...]
```

**Purpose:** Enables comparison with `02_achievement_library.md`

#### Section III: Communication & Narrative Requirements

**Extract:**
- What storytelling approaches will resonate?
- Tone & voice requirements (formal? collaborative? innovative?)
- Cultural communication style
- Narrative patterns they use in posting

**Output format:**
```markdown
## III. Communication & Narrative Requirements

### Resonant Narratives
**Challenge-Solution Stories:** [Evidence they value this]
**Transformation Arcs:** [Evidence they value this]
**Collaboration Narratives:** [Evidence they value this]

### Tone & Voice Requirements
**Formality:** [Formal / Professional-Collaborative / Casual]
**Innovation:** [Traditional / Balanced / Cutting-Edge]
**Collaboration:** [Independent / Balanced / Highly Collaborative]

**Evidence:** "[Quotes demonstrating tone]"

### Cultural Communication Style
[How they talk about work, people, mission]
```

**Purpose:** Enables comparison with `03_narrative_patterns.md`

#### Section IV: Language & Terminology Requirements

**Extract and rank:**
- ATS keywords by importance (frequency + positioning + context)
- Action verbs they use (frequency analysis)
- Industry-specific terminology
- Power phrases and signature language
- Synonym mapping opportunities

**Output format:**
```markdown
## IV. Language & Terminology Requirements

### Critical ATS Keywords (Use in BOTH resume + cover letter)
1. **stakeholder management** (appears 5x, explicit requirement)
   - Context: "manage relationships with campus stakeholders"
   - Recommended frequency: 2-3x in materials
   - Placement: Resume (summary + 2 bullets), Cover letter (paragraph 2)

### Important Keywords (Emphasize in resume)
[Ranked by priority with context]

### Action Verbs They Use
**Strategic Leadership:** stewarded, cultivated, advanced (3x each)
**Operational:** managed, implemented, coordinated
**Collaborative:** partnered, engaged, facilitated

### Industry-Specific Language
[Terminology specific to sector/role]

### Synonym Mapping
- "stakeholder management" → "partner engagement", "relationship building"
- [Additional mappings]
```

**Purpose:** Enables comparison with `04_language_bank.md`

### Phase 3: Sophistication Analysis

**Go beyond literal requirements:**

#### Cultural Decoding

**Analyze:**
- Stated culture vs. implied culture (language patterns reveal reality)
- Contradictions (e.g., "innovative" + "established processes")
- What company emphasizes vs. what role actually requires

**Output:**
```markdown
## V. Sophistication Analysis

### Cultural Reality Check
**Stated:** "[What they say about culture]"
**Implied:** "[What language patterns reveal]"
**Interpretation:** [What daily work likely involves]
**Evidence:** "[Specific language choices]"
```

#### Reading What's NOT Said

**Identify meaningful omissions:**
- No team size → possible new team or restructuring
- No salary range → negotiation strategy or budget uncertainty
- No reporting structure → organizational flux
- No diversity statement → cultural blind spot
- Vague requirements → role still being defined

#### Ideal Candidate Profile (Market Analysis Only)

**CRITICAL INSTRUCTION:** You MUST describe ideal candidates in generic third-person terms. DO NOT assess user's personal fit. NO second-person language ("you", "your"). Personal fit analysis belongs ONLY in `job-fit-analysis` skill.

**Analyze:**
- Ideal candidate archetype: Who will win this role?
- Strong candidate characteristics: What qualifications, backgrounds, and experiences position someone well?
- Competitive candidates: What profiles will likely be in the applicant pool?
- Trade-offs employer might make: Where might they compromise? (e.g., accept less experience for strong culture fit)

**Output format:**
```markdown
### Ideal Candidate Profile

**Profile:** [Describe in third person - "A strong candidate will have...", "Ideal candidates typically possess..."]

**Strong Candidate Characteristics:**
- [Generic qualification/background, no personal assessment]
- [Generic qualification/background, no personal assessment]

**Likely Competitive Applicants:**
- [Profile type 1]
- [Profile type 2]

**Possible Trade-Offs:**
- IF [condition], employer might accept [compromise]
```

#### Priority Decoding

**Determine true vs. stated importance:**
- Analyze by: repetition, positioning, specificity, emphasis words
- Distinguish must-haves from boilerplate
- Rank requirements by "true importance"

**Method:**
```
High Priority Indicators:
- Mentioned 3+ times in different contexts
- Appears in first paragraph or summary
- Has specific quantifiable requirements
- Uses emphatic language ("critical", "essential")

Low Priority Indicators:
- Mentioned once at end of list
- Vague language ("familiarity with", "some experience")
- No specifics or examples
```

#### Risk & Red Flag Assessment

**Identify concerns with severity and context:**

```markdown
### Risk Assessment

⚠️ MODERATE: "Fast-paced environment" + "manage multiple priorities"
- **Context:** Also mentions "work-life balance" support
- **Interpretation:** Likely typical workload, not crisis mode
- **Severity:** Monitor during interview
- **Matters if:** Candidate values clear boundaries and predictable hours

🚩 HIGH: No mention of team size + "build from scratch"
- **Context:** New role, unclear resources
- **Interpretation:** Possible under-resourcing or ambiguous scope
- **Severity:** Clarify expectations before accepting
- **Matters if:** Candidate needs clear structure and adequate support

✅ POSITIVE: Strong DEI commitment with specific initiatives
- **Context:** Multiple references, budget allocated
- **Interpretation:** Authentic commitment, not performative
- **Opportunity:** Strong alignment opportunity for equity-focused candidates
```

#### Strategic Timing Analysis

**Assess:**
- New role vs. backfill (affects expectations and flexibility)
- Urgency signals ("immediate start", "fast-growing team")
- Organizational stability indicators
- How quickly to apply

### Phase 4: Output Generation

**Write to:** `~/career-applications/[job-slug]/01-job-analysis.md`

**Template:**
```markdown
---
job_title: [Exact title from posting]
company: [Company name]
date_analyzed: YYYY-MM-DD
posting_url: [if available]
analyst: Claude Code (job-description-analysis skill)
---

# Job Analysis: [Title] - [Company]

## Executive Summary
[2-3 sentences: role type, seniority, top 3 priorities, culture signal, ideal candidate profile]

## I. Values & Philosophy Requirements
[Full content from Phase 2, Section I]

## II. Experience & Achievement Requirements
[Full content from Phase 2, Section II]

## III. Communication & Narrative Requirements
[Full content from Phase 2, Section III]

## IV. Language & Terminology Requirements
[Full content from Phase 2, Section IV]

## V. Sophistication Analysis
[Full content from Phase 3]

## VI. Strategic Recommendations

### For Resume
1. [Top priority based on analysis]
2. [Second priority]
3. [Third priority]

### For Cover Letter
1. [Opening strategy recommendation]
2. [Middle development suggestion]
3. [Closing approach]

### For Interview Preparation
[Likely questions based on posting emphasis]

---
Generated: YYYY-MM-DD via job-description-analysis skill
Version: 1.0
```

### Phase 5: JSON Export for Wrapper Application

**After generating markdown analysis, create structured JSON output:**

**Write to:** `~/career-applications/[job-slug]/job-analysis-v1.json`

**Structure:**
```json
{
  "metadata": {
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "input_file": "job-posting.pdf",
    "version": 1,
    "analyst": "Claude Code (job-description-analysis skill)"
  },
  "job_title": "Full position title",
  "institution": "Organization name",
  "position": "Position title (short)",
  "requirements": {
    "required": [
      "Explicit must-have requirement 1",
      "Explicit must-have requirement 2"
    ],
    "preferred": [
      "Nice-to-have 1",
      "Nice-to-have 2"
    ],
    "quantifiable": {
      "budget_range": "$5M+",
      "team_size": "10+",
      "years_experience": "5-7"
    }
  },
  "culture": {
    "values_explicit": ["value 1", "value 2"],
    "values_implicit": ["implied value 1", "implied value 2"],
    "tone": {
      "formality": "professional-collaborative",
      "innovation": "balanced",
      "collaboration": "highly-collaborative"
    },
    "keywords": ["keyword1", "keyword2", "keyword3"]
  },
  "key_responsibilities": [
    "Primary responsibility 1",
    "Primary responsibility 2",
    "Primary responsibility 3"
  ],
  "ats_keywords": {
    "critical": [
      {"term": "stakeholder management", "frequency": 5, "context": "relationship building"},
      {"term": "budget oversight", "frequency": 3, "context": "financial management"}
    ],
    "important": [
      {"term": "strategic planning", "frequency": 2, "context": "organizational development"}
    ]
  },
  "strategic_analysis": {
    "priority_requirements": [
      "Top priority based on analysis",
      "Second priority",
      "Third priority"
    ],
    "red_flags": [
      {"severity": "moderate", "description": "Fast-paced environment mention", "context": "Also mentions work-life balance"},
      {"severity": "high", "description": "No team size specified", "context": "Build from scratch language"}
    ],
    "ideal_candidate_profile": "Brief description of ideal candidate archetype",
    "competitive_landscape": "Description of likely competitive applicants"
  }
}
```

**Implementation:**
1. Check if `job-analysis-v1.json` already exists
2. If exists, increment version number: `job-analysis-v2.json`, `job-analysis-v3.json`, etc.
3. Extract structured data from the markdown analysis
4. Write JSON file with proper formatting (2-space indentation)
5. Save to same directory as markdown file

**Present to user:**
```
Analysis complete! Saved to:
- ~/career-applications/[job-slug]/01-job-analysis.md (full analysis)
- ~/career-applications/[job-slug]/job-analysis-v1.json (structured data)

Key findings:
- Role type: [IC/Manager/Executive, seniority]
- Top 3 priorities: [list]
- Culture: [primary signal]
- Ideal candidate profile: [brief description]
- Red flags: [count] identified

Next steps - Use job-fit-analysis skill to compare this role against your lexicons and get personalized competitive assessment.

Would you like to:
1. Review the full analysis
2. Proceed to job fit analysis (compare against your background)
3. Proceed to resume alignment (tailor your resume)
```

## Error Handling

### Missing or Invalid Input

```markdown
## Startup Checks

**If no job description provided:**
"I need a job description to analyze. You can:
- Paste the text directly
- Upload a PDF or Word document
- Provide a URL to the posting"

**If posting too short (<100 words):**
"This seems incomplete (only [N] words). Is this the full posting?"

**If multiple postings detected:**
"I see content that looks like multiple job descriptions. Which one should I analyze?"

**If extraction fails:**
"I couldn't extract text from that file. Can you try:
- Copy/pasting the text
- Saving as PDF first
- Providing the URL instead"
```

### Output Directory Issues

```markdown
**If cannot create output directory:**
"Cannot write to ~/career-applications/.

Options:
1. Check permissions: ls -la ~/career-applications/
2. Specify different directory
3. Save to current directory instead"
```

## Reference Materials

### ats-keyword-framework.md

**Purpose:** Detailed ATS optimization guidance

**Contents:**
- How ATS systems work (resume screening algorithms)
- Keyword density best practices (frequency without stuffing)
- Strategic placement patterns (where keywords matter most)
- Context matching (keywords need proper context)
- Synonym strategies (variations that match intent)
- Industry-specific keyword patterns
- Common ATS pitfalls to avoid

### tone-analysis-guide.md

**Purpose:** Culture decoding patterns

**Contents:**
- Tone classification taxonomy (formality, innovation, collaboration spectrums)
- Signal patterns by category
- Industry comparison benchmarks
- Writing style matching guidance

### values-alignment-patterns.md

**Purpose:** Identify mission/values hooks for cover letters

**Contents:**
- Common organizational values categories
- Recognizing implicit values
- Connecting personal experience to organizational values
- Authentic vs. performative alignment
- Cover letter integration techniques

## Success Criteria

✅ All 4 lexicon-aligned sections populated with specific content
✅ Requirements ranked by true importance (not just listed order)
✅ Cultural decoding goes beyond literal reading
✅ Red flags identified with severity and context
✅ Output structure enables direct comparison with lexicons
✅ User understands job deeply enough to make informed decision
✅ **NO personal assessment language** - all candidate descriptions use third-person generic language ("strong candidates will have", "ideal profiles include")
✅ **NO second-person pronouns** - zero instances of "you", "your", "you're" in analysis sections

## Pre-Output Validation

**Before saving analysis, verify:**
1. Search document for "you", "your" - if found in analysis sections (not quotes), revise to third-person
2. Search for "Your Competitive" - should not appear (use "Ideal Candidate Profile" instead)
3. All candidate descriptions are generic market analysis, not personal fit assessment
4. Any strength/weakness lists describe market expectations, not specific individuals

## Example Output Excerpt

```markdown
## II. Experience & Achievement Requirements

### Capital Projects & Infrastructure
**Required:** "Proven experience managing capital projects with budgets exceeding $5M"
**Preferred:** "Experience with adaptive reuse projects in educational or cultural settings"

**Quantifiable Expectations:**
- Budget range: $5M+ explicitly mentioned
- Project complexity: Multi-stakeholder (campus, city, donors mentioned)
- Duration: Multi-year projects implied ("long-term planning")

**Evidence:**
- "stewarded completion of $8M renovation" (exact quote)
- "managed relationships with campus facilities, city planning, donor community"

**Priority Assessment:** HIGH
- Mentioned 3x in different contexts
- First requirement in qualifications section
- Specific minimum ($5M) not vague
- Uses emphatic language ("proven", "exceeding")

→ **Ready for comparison with achievement_library.md Section II.A (Capital Projects)**
```

---
**END OF SKILL**