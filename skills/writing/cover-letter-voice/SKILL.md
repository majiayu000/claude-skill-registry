---
name: cover-letter-voice
description: Develop authentic cover letter narrative using philosophy, patterns, and job's cultural requirements
---

# Cover Letter Voice Development

## Purpose
Develop authentic cover letter narrative framework grounded in your career philosophy, established narrative patterns, and the job's cultural requirements. This skill creates a complete narrative framework—not a draft letter, but the strategic foundation for writing one.

## Invocation Triggers
- "Develop my cover letter narrative"
- "Help me find my voice for this letter"
- "What story should I tell?"
- "Create a cover letter framework"
- "Build my cover letter strategy"

## Required Inputs

**Lexicon Dependencies (must exist):**
- `~/career-applications/[job-slug]/01-job-analysis.md` (their values/tone)
- `~/lexicons_llm/01_career_philosophy.md` (your values)
- `~/lexicons_llm/03_narrative_patterns.md` (your storytelling)
- `~/lexicons_llm/04_language_bank.md` (your voice)

**Optional Inputs:**
- `~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md` (strategic plan from job-fit-analysis)
- Previous cover letters (for tone reference)

## Process

---

## Phase 0: Lexicon Loading

**Load required files:**

1. **Identify job slug**
   - Ask user: "What is the job slug (directory name) for this application?"
   - Example: "ucla-arts-director"
   - Construct path: `~/career-applications/[job-slug]/`

2. **Ask about current work-in-progress (three separate questions)**

   Ask these questions one at a time, waiting for response to each:

   **Question 1:**
   ```
   "Have you started writing any rough drafts or paragraphs for this cover letter yet?"
   ```
   - If yes → Ask them to share what they have
   - If no → Continue to Question 2

   **Question 2:**
   ```
   "Do you have bullet points, notes, or a list of ideas about what you want to include?"
   ```
   - If yes → Ask them to share
   - If no → Continue to Question 3

   **Question 3:**
   ```
   "What initial thoughts or direction are you considering for this letter?
   Any ideas about the narrative approach or key points you want to emphasize?"
   ```
   - Capture any thoughts shared
   - Store all responses for integration into framework development

   - **Why this matters:** User may have already started thinking/writing; we should build on their work, not ignore it

3. **Load job analysis**
   ```
   Read: ~/career-applications/[job-slug]/01-job-analysis.md
   ```
   - If missing → Error Handler A

4. **Load career philosophy**
   ```
   Read: ~/lexicons_llm/01_career_philosophy.md
   Store entire content as context
   ```
   - If missing → Error Handler B

5. **Load narrative patterns**
   ```
   Read: ~/lexicons_llm/03_narrative_patterns.md
   Store entire content as context
   ```
   - If missing → Error Handler B

6. **Load language bank**
   ```
   Read: ~/lexicons_llm/04_language_bank.md
   Store entire content as context
   ```
   - If missing → Error Handler B

7. **Check for optional files**
   ```
   Check: ~/career-applications/[job-slug]/03-gap-analysis-and-cover-letter-plan.md
   If exists → Read and note strategic guidance
   ```

8. **Ask about past cover letters**
   ```
   "Do you have previous cover letters you'd like me to analyze for tone patterns?
   If so, please provide them now."
   ```
   - If provided → Analyze tone, structure, patterns (see Phase 2A)

**Confirmation message:**
```
✓ Loaded successfully:
  - Job analysis for [job title] at [company]
  - Career philosophy (X core values, Y leadership approaches)
  - Narrative patterns (X opening strategies, Y evidence patterns)
  - Language bank (action verbs, power phrases, industry terms)
  [If applicable]: Cover letter strategic plan from gap analysis
  [If applicable]: 3 previous cover letters for tone reference

Ready to develop your narrative framework.
```

---

## Phase 1: Context Review

**Summarize loaded context:**

### 1A. Job Analysis Review

**Extract and present:**
- **Section I: Cultural & Values Analysis**
  - Organization's cultural tone
  - Core values emphasized
  - Mission/vision elements

- **Section III: Communication & Narrative Requirements**
  - Expected tone/formality level
  - Communication style preferences
  - Cultural fit indicators

**Example output:**
```
## Job Context Summary

Organization: UCLA School of the Arts and Architecture
Role: Senior Director, Center for the Arts

Cultural Requirements:
- Tone: Collaborative-innovative (balanced, not startup-disruptive)
- Values emphasis: DEI, student-centered mission, artistic excellence
- Communication style: Professional but approachable, mission-driven
- Cultural fit: Values both strategic vision and practical execution

Key Communication Requirements:
- Demonstrate stakeholder engagement capability
- Show commitment to mission/values alignment
- Balance visionary thinking with operational expertise
- Professional tone without excessive formality
```

### 1B. Cover Letter Plan Review (if available)

**If `03-gap-analysis-and-cover-letter-plan.md` exists:**
```
## Strategic Plan from Gap Analysis

Your gap analysis recommended:
- Address [specific gap] by reframing as [strategy]
- Emphasize [strength] to counter [concern]
- Use narrative thread: [recommended thread]
- Length: [recommended word count]

I'll incorporate this strategic guidance into the framework.
```

### 1C. Philosophy & Pattern Summary

**Present overview:**
```
## Your Established Voice & Patterns

From career_philosophy.md:
- Core Values: [list 3-5 key values]
- Leadership Approaches: [list 2-3 approaches]
- Most prominent themes: [identify 2-3 recurring themes]

From narrative_patterns.md:
- Opening Strategies: [list available patterns with usage frequency if noted]
- Evidence Patterns: [list established narrative structures]
- Most frequent pattern: [identify most-used approach]

From language_bank.md:
- Action verb categories: [list categories]
- Power phrases: [note key recurring phrases]
- Industry language: [sector-specific terminology]
```

**Transition:**
```
Now let's explore which narrative thread will create the most authentic
and compelling story for this opportunity.
```

---

## Phase 2: Content & Pattern Analysis

### Phase 2A: Past Cover Letters Analysis (if provided)

**For each letter provided, analyze:**

```
## Past Cover Letter Analysis

Letter 1: [Title/Organization, Year]
- Opening Pattern: [identify: institutional positioning, personal connection, etc.]
- Tone: [warm/authoritative/collaborative/formal - describe with specific adjectives]
- Evidence Pattern: [Challenge→Action→Result, Context→Insight→Application, etc.]
- Length: [X paragraphs, ~Y words]
- Notable phrases: [quote 2-3 distinctive phrases that show voice]
- Role level: [director/VP/etc. - if applicable]

Letter 2: [Title/Organization, Year]
- Opening Pattern: [pattern]
- Tone: [describe]
- Evidence Pattern: [pattern]
- Length: [X paragraphs, ~Y words]
- Notable phrases: [quote phrases]
- Role level: [level]

Cross-Letter Patterns Observed:
- Tone variation: [e.g., "You shift from collaborative to authoritative based on role level"]
- Consistent elements: [e.g., "All letters use institutional positioning opening"]
- Length patterns: [e.g., "Director roles: ~450 words, VP roles: ~550 words"]
- Signature phrases: [phrases that appear across multiple letters]
```

**Example:**
```
From your 2023 CSUF letter (Director of Arts Programs):
- Opening: Institutional positioning ("CSUF is uniquely positioned by...")
- Tone: Warm, collaborative, student-centered
- Evidence pattern: Challenge → Action → Result
- Length: 3 paragraphs, ~450 words
- Notable: "I believe [role] should be..." appears in opening

From your 2024 UCLA letter (VP of Academic Affairs):
- Opening: Personal connection to mission
- Tone: Authoritative, visionary, strategic
- Evidence pattern: Context → Insight → Application
- Length: 4 paragraphs, ~550 words
- Notable: "Our moment demands..." framing

Pattern observation: You adjust formality and tone based on role level
(collaborative-warm for director, authoritative-strategic for VP)
```

### Phase 2B: Narrative Patterns from Lexicon

**Extract and present established patterns:**

```
## Your Narrative Pattern Library

From narrative_patterns.md:

### Opening Strategies Available:

1. Institutional Positioning
   - Template: "[Institution] is uniquely positioned by..."
   - When used: Academic organizations, mission-driven roles
   - Frequency: [if noted in lexicon]
   - Source: narrative_patterns.md:[line number]

2. Personal Connection
   - Template: "My commitment to [value] was shaped by..."
   - When used: Values-driven roles, mission emphasis
   - Frequency: [if noted]
   - Source: narrative_patterns.md:[line number]

3. [Continue for all opening patterns identified]

### Evidence Patterns Available:

1. Challenge → Action → Result
   - Structure: Set context/challenge, describe your actions, state measurable outcome
   - When used: Achievement-focused narratives, operational roles
   - Source: narrative_patterns.md:[line numbers]
   - Example from lexicon: [quote example if available]

2. Context → Insight → Application
   - Structure: Establish situation, share strategic insight, show implementation
   - When used: Strategic roles, change leadership
   - Source: narrative_patterns.md:[line numbers]

3. [Continue for all evidence patterns identified]

### Closing Patterns Available:

1. Values Reaffirmation + Forward-Looking
   - Template: [if available in lexicon]
   - Source: narrative_patterns.md:[line number]

2. [Continue for all closing patterns]
```

### Phase 2C: Job Requirements Alignment

**Synthesize analysis:**

```
## Pattern-to-Job Alignment

Based on job analysis Section III and your established patterns:

Recommended Opening Pattern: [Pattern Name]
Why: [Explain how this pattern matches job's cultural tone + your authentic voice]
Example: [Show how it would work for this specific job]

Recommended Evidence Pattern: [Pattern Name]
Why: [Explain alignment with job requirements + your storytelling style]

Recommended Closing Pattern: [Pattern Name]
Why: [Explain fit]

Length Guidance:
- Role level: [Director/VP/etc.]
- Your historical pattern for this level: [~X words]
- Industry standard for this role: [Y-Z words]
- Recommended: [specific word count range]
```

**Example:**
```
## Pattern-to-Job Alignment

Recommended Opening: Institutional Positioning
Why:
- Job emphasizes mission-driven culture (matches pattern's use case)
- You've used this successfully in 60% of academic applications
- Their collaborative-innovative tone aligns with this pattern's professional-warm style

Recommended Evidence Pattern: Challenge → Action → Result
Why:
- Job requires demonstrated operational expertise
- This pattern showcases concrete achievements (their priority)
- Matches your most frequent narrative structure

Recommended Closing: Values Reaffirmation + Forward-Looking
Why:
- Reinforces mission alignment (critical for this role)
- Creates invitation for dialogue (collaborative tone they value)

Length Guidance:
- Role level: Director
- Your pattern for director roles: ~450 words
- Industry standard: 400-500 words
- Recommended: 480-520 words (3-4 paragraphs)
```

---

## Phase 3: Narrative Thread Exploration

**Use Socratic questioning to identify core story**

### 3A. Present Narrative Thread Options

**Based on philosophy lexicon + job requirements, generate 3 narrative thread options**

Use AskUserQuestion tool:

```
Based on your career philosophy and this role's requirements, I've identified
three potential narrative threads. Each connects your authentic values to what
this opportunity represents.

Which thread resonates most for this application?
```

**Structure each option:**
- **Thread name** (clear, compelling label)
- **Philosophy anchor:** Quote specific element from `01_career_philosophy.md` with line reference
- **Job connection:** Quote specific requirement from job analysis
- **Story arc:** Describe the narrative journey this creates
- **Why this thread:** Brief explanation of authentic fit

**Example using AskUserQuestion:**

Question: "Which narrative thread feels most authentic for this opportunity?"
Header: "Narrative Thread"
multiSelect: false

Options:

**Option A: Arts Leadership as Social Transformation**
Label: "Arts as Social Transformation"
Description: "Your philosophy emphasizes 'Arts as Social Justice' (philosophy.md:215). Job emphasizes 'Advancing arts for social impact.' Story arc: Your journey from believing arts = access to leading institutions that embody this. Frames your capital projects and program development as tools for community transformation."

**Option B: Listening-First Leadership in Complex Environments**
Label: "Listening-First Leadership"
Description: "Your philosophy: 'Listening-First Leadership' (philosophy.md:85). Job context: Large organization, diverse stakeholders, collaborative culture. Story arc: How your leadership approach builds consensus and drives change in complex institutional settings. Frames your stakeholder successes as evidence of this approach."

**Option C: Building Infrastructure for Creative Excellence**
Label: "Infrastructure for Excellence"
Description: "Your achievements: Capital projects, systems building, resource development. Job requirements: Facility stewardship, program development, financial management. Story arc: How you create conditions for artistic excellence through strategic infrastructure. Frames your operational expertise as enabler of mission."

**User selects thread → Store selection**

### 3B. Deepen Selected Thread

**Explore the chosen narrative:**

```
You selected: [Thread Name]

Let's develop this thread with specific examples from your experience.
```

**Ask follow-up questions to build narrative depth:**

**Question 1: Evidence Selection**
```
From your [philosophy/achievement lexicon], which experience best illustrates
this philosophy in action for this specific opportunity?

[Present 3 options from achievement library or past work, each with:]
- Achievement name
- Why it demonstrates the philosophy
- How it connects to job requirement
- Source citation (achievement_library.md:line numbers)
```

Use AskUserQuestion:
- Header: "Key Evidence"
- multiSelect: false (choose primary)
- Options: 3 relevant achievements

**User selects → Store as primary evidence**

**Question 2: Tension/Opportunity Framing**
```
How do you want to position what this role represents for you?
```

Use AskUserQuestion:
- Header: "Positioning"
- multiSelect: false
- Options:
  - "Continuing [thread] work at larger scale/scope"
  - "Bringing [your expertise] to [their context] setting"
  - "Bridging [element 1] with [element 2]"
  - [Generate third option based on thread]

**User selects → Store positioning**

**Question 3: Supporting Evidence**
```
Which additional achievements or experiences strengthen this narrative thread?
(Select 1-2 more)
```

Use AskUserQuestion:
- Header: "Supporting Evidence"
- multiSelect: true (can select multiple)
- Options: 3-4 additional relevant achievements from lexicon

**User selects → Store as supporting evidence**

### 3C. Build Narrative Map

**Document the complete narrative thread:**

```
## Narrative Thread Map

Core Thread: [Selected Thread Name]
Philosophy Anchor: [Quote from philosophy.md with line reference]
Job Connection: [Quote from job analysis]

Primary Evidence:
- Achievement: [Name]
- Demonstrates: [Key qualities]
- Source: achievement_library.md:[lines]

Supporting Evidence:
- Achievement 2: [Name]
  Demonstrates: [Qualities]
  Source: [Citation]
- Achievement 3: [Name] (if selected)
  Demonstrates: [Qualities]
  Source: [Citation]

Positioning Frame: [How role is positioned]

This narrative map will guide the structure and tone development.
```

---

## Phase 4: Tone & Structure Framing

### 4A. Develop Tone Profile

**Match job requirements to user's natural voice:**

```
## Tone Profile Development

### Job's Tone Requirements (from analysis):
- Formality level: [from job analysis Section III]
- Cultural style: [collaborative/innovative/traditional/etc.]
- Values emphasis: [key values to emphasize]
- Communication preferences: [any specific guidance from analysis]

### Your Natural Voice (from lexicon + past letters):
- Characteristic tone: [describe from past letters if available, or from language bank]
- Sentence patterns: [longer vision statements, concrete examples, etc.]
- Recurring phrases: [from language bank power phrases]
- Emotional register: [warm/reflective/strategic/authoritative/committed/etc.]

### Recommended Tone Synthesis:
- **Formality level:** [Specific recommendation, e.g., "Professional-collaborative (not academic, not casual)"]
- **Sentence structure:** [Specific guidance, e.g., "Mix longer vision statements (25-30 words) with concrete examples (15-20 words)"]
- **Vocabulary approach:** [e.g., "Mission-oriented language, avoid jargon, emphasize values"]
- **Emotional register:** [e.g., "Committed optimism (not neutral, not effusive)"]

### Example Opening Sentence (Tone Demonstration):

"[Draft opening sentence that demonstrates the recommended tone synthesis]"

Tone Notes on This Example:
- "[Phrase 1]" = [explanation, e.g., "institutional positioning pattern"]
- "[Phrase 2]" = [explanation, e.g., "complexity acknowledgment (collaborative tone)"]
- "[Word choice]" = [explanation, e.g., "confident but not presumptuous"]
- "[Specific detail]" = [explanation, e.g., "credibility through specificity"]

Does this tone feel authentic to how you want to present in this letter?
[Wait for user confirmation or adjustment request]
```

**Example:**
```
## Tone Profile Development

### Job's Tone Requirements:
- Formality: Professional but not overly formal
- Cultural style: Collaborative-innovative
- Values emphasis: Mission-driven, DEI, student-centered
- Communication: Clear, concrete, values-aligned

### Your Natural Voice:
- From CSUF letter: Warm, reflective, student-centered
- From UCLA VP letter: Strategic, visionary, authoritative
- Language bank shows: Action-oriented, evidence-based framing
- Power phrases: "I believe [role] should be...", "uniquely positioned by..."

### Recommended Tone Synthesis:
- **Formality level:** Professional-collaborative (not academic formal, not casual conversational)
- **Sentence structure:** Mix of longer vision statements (25-30 words) with concrete examples (15-20 words) and impact summaries (10-12 words)
- **Vocabulary approach:** Mission-oriented language, avoid corporate jargon, emphasize collaboration and impact
- **Emotional register:** Committed optimism (enthusiastic but grounded, not neutral, not effusive)

### Example Opening Sentence:

"UCLA's School of the Arts and Architecture is uniquely positioned by its intersection of artistic excellence, research innovation, and public mission to advance arts as a tool for social transformation—a vision that aligns precisely with my 15-year commitment to arts-as-social-justice practice."

Tone Notes:
- "uniquely positioned by" = your institutional positioning pattern (from narrative_patterns.md)
- "intersection of" = acknowledges complexity (collaborative tone)
- "aligns precisely" = confident but not presumptuous
- "15-year commitment" = credibility through specific timeframe

Does this tone feel authentic to how you want to present?
```

**Wait for user response:**
- If "Yes" → Proceed to 4B
- If "Needs adjustment" → Ask: "What feels off? Too formal? Too casual? Different emphasis needed?" → Adjust and re-present

### 4B. Recommend Structure

**Based on selected thread + patterns + job requirements:**

```
## Recommended Narrative Structure

Total Target Length: [X-Y words] ([Z] paragraphs)
Based on: [role level + your historical pattern + industry standard]

---

### Opening Paragraph (~X words)
**Pattern:** [Pattern name from narrative_patterns.md]
**Purpose:** [What this paragraph accomplishes]
**Content:** [Describe what goes in this paragraph]
**Source:** narrative_patterns.md:[line reference]

**Draft Guidance:**
[Provide specific guidance on how to construct this paragraph]

**Example opening line:**
"[Show example sentence]"

**Philosophy Connection:**
Links to career_philosophy.md:[line reference] ([value/approach name])

---

### Development Paragraph 2: [Theme/Achievement] (~X words)
**Pattern:** [Evidence pattern name]
**Achievement:** [Specific achievement from narrative map]
**Source:** achievement_library.md:[line reference] OR narrative_patterns.md:[line reference]

**Structure:**
1. Context/Challenge: [What to establish]
2. Action (your role): [What to describe]
3. Result: [What outcome to highlight]

**Draft Guidance:**
- Begin with: [Specific opening approach]
- Action section: [What verbs/approaches to use from language bank]
- Result: [What to emphasize - metrics, impact, outcomes]

**Why This Achievement:**
- Demonstrates: [Key quality/requirement from job]
- Scale/Scope: [How it relates to their requirements]
- Approach: [How it shows your philosophy/values]

**Language Notes:**
- "[Verb/phrase]" ← language_bank.md:[line] ([category])
- "[Term]" ← [source: philosophy.md or achievement_library.md]
- "[Metric]" ← achievement_library.md:[line] (specific, credible)

---

### Development Paragraph 3: [Theme/Achievement] (~X words)
**Pattern:** [Evidence pattern name]
**Achievement:** [Second achievement from narrative map]
**Source:** [Citation]

[Repeat structure from Paragraph 2]

---

### [Optional] Development Paragraph 4: [If gap to address or third achievement]
**Purpose:** [Address gap OR add third achievement]
**Pattern:** [Pattern name]
**Source:** [Citation]

[If addressing gap]:
**Gap Reframing Strategy:** [From 03-gap-analysis-and-cover-letter-plan.md if available]
**Approach:** [How to frame the gap as growth opportunity]

[If third achievement]:
[Follow Paragraph 2 structure]

---

### Closing Paragraph (~X words)
**Pattern:** [Closing pattern from narrative_patterns.md]
**Purpose:** [What this accomplishes]
**Source:** narrative_patterns.md:[line reference]

**Content:**
- Reaffirm: [What value/thread to reinforce]
- Forward-looking: [What invitation/next step to create]
- Tone: [How to strike enthusiasm without presumption]

**Draft Guidance:**
[Specific guidance on constructing close]

**Example closing:**
"[Show example sentence or two]"

---

### Structure Summary:

Opening: [Pattern] - [Purpose] (~X words)
Development 2: [Achievement] - [Pattern] (~X words)
Development 3: [Achievement] - [Pattern] (~X words)
[Paragraph 4: if applicable] (~X words)
Closing: [Pattern] - [Purpose] (~X words)

Total: [X-Y words] ([Z] paragraphs)
```

**Ask user:**
```
Does this structure feel right for telling your story?
Any adjustments needed before we develop the detailed framework?
```

**Wait for confirmation or adjustment requests**

---

## Phase 5: Voice Consistency Check

**Review all proposed language against language bank:**

```
## Language Consistency Review

Checking proposed narrative framework against your established voice...

### Action Verbs (from language_bank.md)

Verbs proposed in framework:
✅ "[Verb 1]" - Found in [Category] (language_bank.md:[line])
✅ "[Verb 2]" - Found in [Category] (language_bank.md:[line])
❌ "[Verb 3]" - NOT in your lexicon
   → Sounds unlike your voice
   → Replacement options: "[Alternative 1]" or "[Alternative 2]" (both in language_bank.md)
✅ "[Verb 4]" - Found in [Category] (language_bank.md:[line])

[Continue for all action verbs in framework]

### Power Phrases (from language_bank.md)

Phrases proposed in framework:
✅ "I believe [role] should be..." - Your leadership philosophy template (language_bank.md:[line])
✅ "uniquely positioned by..." - Your institutional positioning template (language_bank.md:[line])
❌ "[Phrase X]" - NOT in your lexicon
   → Replacement: "[Alternative phrase]" (language_bank.md:[line])

[Continue for all power phrases]

### Industry Language & Terminology

Terms proposed in framework:
✅ "[Term 1]" - Technical term from your sector (appears in achievement_library.md:[line])
✅ "[Term 2]" - Standard in your industry (language_bank.md:[line])
❌ "[Term 3]" - Corporate jargon, not in your lexicon
   → Replacement: "[Alternative]" (more authentic to your voice)

[Continue for all industry terms]

---

## Voice Consistency Assessment:

Overall consistency: [STRONG/MODERATE/NEEDS ADJUSTMENT]

[If STRONG]:
✓ Narrative framework uses your established language patterns throughout
✓ All proposed verbs and phrases match your lexicon
✓ No fabricated language detected

[If MODERATE or NEEDS ADJUSTMENT]:
⚠ Found [X] terms not in your lexicon
⚠ Recommended replacements shown above
⚠ Will revise framework to use only verified language before proceeding

[If any ❌ items found]:
I've flagged language that doesn't appear in your lexicon. Should I:
A) Replace with alternatives from your language bank (recommended)
B) Add these new terms to your language bank for future use
C) Keep them but mark as new language (use sparingly)
```

**Wait for user decision on any flagged items**

**Once all language verified:**
```
✓ Voice consistency check complete
✓ All language traceable to your lexicon
✓ Framework ready for authenticity review
```

---

## Phase 6: Authenticity Review

**Final Socratic check before creating framework document:**

### 6A. Open-Ended Questions

**Ask these questions one at a time, wait for response to each:**

1. **Voice authenticity:**
   ```
   "Does this narrative framework sound like your real voice?

   Not 'could you write this' but 'does this feel like something you would
   naturally say about yourself and this opportunity?'"
   ```

   **Wait for response → If concerns raised, explore and adjust**

2. **Performativity check:**
   ```
   "Are there any elements that feel performative or unlike you?

   Sometimes we include things because they 'sound good' rather than because
   they're genuinely true. Anything feel that way here?"
   ```

   **Wait for response → If yes, identify and remove/replace**

3. **Enthusiasm indicator:**
   ```
   "Which part of this story excites you most to tell?

   This can help us ensure that excitement comes through in the framework."
   ```

   **Wait for response → Note what energizes user, ensure it's prominent**

4. **Completeness check:**
   ```
   "Is there anything missing that feels important?

   A value that matters to you, an achievement that should be included,
   or an aspect of your approach that isn't represented?"
   ```

   **Wait for response → If yes, explore and incorporate**

### 6B. Philosophy Alignment Check

**Compare framework to philosophy lexicon:**

```
## Authenticity Alignment Check

Reviewing framework against your core values and leadership approaches...

### Your Core Values (from career_philosophy.md):

1. [Value 1 - name/description from philosophy.md:line]
   ✅ Represented: [How/where in framework]
   OR
   ❌ Missing: [Not present in current framework]

2. [Value 2]
   ✅ Represented: [How/where]
   OR
   ⚠️ Implied but not explicit: [Where it could be strengthened]

3. [Value 3]
   [Continue for all core values]

### Your Leadership Approaches (from career_philosophy.md):

1. [Approach 1 - name/description from philosophy.md:line]
   ✅ Central to narrative: [How demonstrated]
   OR
   ⚠️ Not explicit: [Could be strengthened by...]

2. [Approach 2]
   [Continue for all approaches]

---

## Gaps or Opportunities:

[If any ❌ or ⚠️ items]:

I notice [value/approach X] is missing or understated in the current framework.

Options:
A) Add explicit mention in [paragraph Y]
   - Suggestion: [Specific way to incorporate]
   - Would strengthen: [What this adds to narrative]

B) Let it remain implicit
   - Rationale: [Why it might not need explicit mention]
   - Already evident through: [How it shows up indirectly]

Which feels more authentic to you?

[Wait for user decision → Adjust framework as needed]
```

### 6C. Final Authenticity Confirmation

**Ask directly:**

```
## Final Authenticity Check

Before I create your cover letter framework document, I need your confirmation:

This framework—the narrative thread, tone, structure, language, and evidence—
does it feel authentic to:
- How you actually think about your work?
- How you naturally talk about your experience?
- What genuinely excites you about this opportunity?
- The values you truly hold (not just what sounds good)?

Please answer honestly: Does this framework feel authentic to your voice?

[Wait for explicit "Yes" or concerns]
```

**If YES:**
```
✓ Authenticity confirmed
✓ Ready to create framework document
```

**If concerns raised:**
```
Let's address what doesn't feel right.

What specifically feels inauthentic or off?
[Explore concern]
[Make adjustments]
[Re-confirm authenticity]
```

**Do not proceed to output file creation without explicit user confirmation of authenticity**

---

## Output File Creation

**Once authenticity confirmed, create framework document and JSON export:**

### File Details
- **Markdown Path:** `~/career-applications/[job-slug]/04-cover-letter-framework.md`
- **JSON Path:** `~/career-applications/[job-slug]/cover-letter-draft-v1.json`
- **Format:** Markdown with YAML frontmatter + structured JSON data
- **Purpose:** Complete narrative framework for cover letter development + machine-readable export

### Output Template

```markdown
---
job_title: [Job Title]
company: [Company/Organization]
date_created: [YYYY-MM-DD]
lexicons_referenced:
  - 01-job-analysis.md (Sections I & III)
  - 01_career_philosophy.md ([specific values/approaches referenced])
  - 03_narrative_patterns.md ([specific patterns used])
  - 04_language_bank.md ([specific categories used])
narrative_thread: [Selected Thread Name]
authenticity_confirmed: [YYYY-MM-DD]
---

# Cover Letter Narrative Framework
## [Job Title] - [Company/Organization]

## I. Tone Profile

**Recommended Voice:**
- [Formality level - specific description]
- [Emotional register - specific description]
- [Overall approach - specific description]
- [Additional characteristics]

**Sentence Structure:**
Mix of:
- Vision statements ([X-Y words per sentence])
- Concrete examples ([X-Y words per sentence])
- Impact summaries ([X-Y words per sentence])

**Vocabulary Guidelines:**
✅ Use: [List 8-10 key verbs/phrases from language bank]
❌ Avoid: [List 3-5 terms NOT in lexicon that might be tempting but don't match voice]

**Tone Calibration Notes:**
[Any specific guidance on maintaining tone - e.g., "Balance enthusiasm with groundedness", "Lead with mission, support with metrics", etc.]

---

## II. Narrative Structure

**Total Target Length:** [X-Y words] ([Z] paragraphs)

---

### Opening Paragraph (~X words)
**Pattern:** [Pattern Name]
**Source:** narrative_patterns.md:[line reference]

**Draft Guidance:**
[Provide 3-5 sentences of specific guidance on constructing this paragraph]

**Example Draft:**
"[Provide full example draft of opening paragraph showing tone and approach]"

**Philosophy Connection:**
Links to career_philosophy.md:[line reference] ([Value/Approach Name])

**Evidence & Credibility:**
- "[Specific phrase]" = [explanation of why this works]
- "[Metric/detail]" = [explanation of credibility element]
- "[Value term]" = [connection to their requirements]

---

### Development Paragraph 2: [Achievement/Theme Name] (~X words)
**Pattern:** [Evidence Pattern Name]
**Achievement:** [Specific achievement name]
**Source:** achievement_library.md:[line reference] OR narrative_patterns.md:[line reference]

**Structure:**
1. **Context/Challenge:** [What to establish - 2-3 sentences of guidance]
2. **Action (your role):** [What to describe - 2-3 sentences of guidance]
3. **Result:** [What outcome to highlight - 1-2 sentences of guidance]

**Draft Guidance:**

*Begin with context/challenge:*
"[Provide example opening sentence with guidance]"

*Action (your role):*
"[Provide example sentences showing how to describe actions]"

*Result:*
"[Provide example of outcome description with metrics if applicable]"

**Why This Achievement:**
- Demonstrates: [Key quality/requirement from job - be specific]
- Scale/Scope: [How it relates to their requirements]
- Approach: [How it shows your philosophy/values]

**Language Notes:**
- "[Verb]" ← language_bank.md:[line] ([Category name])
- "[Phrase]" ← [specific source: philosophy.md:line or achievement_library.md:line]
- "[Metric/detail]" ← achievement_library.md:[line] (verifiable, specific)

**Philosophy Connection:**
Links to career_philosophy.md:[line reference] ([Value/Approach that this demonstrates])

---

### Development Paragraph 3: [Achievement/Theme Name] (~X words)
**Pattern:** [Evidence Pattern Name]
**Achievement:** [Specific achievement name]
**Source:** [Citation]

[Repeat full structure from Development Paragraph 2]

**Structure:**
1. **Context/Challenge:** [Guidance]
2. **Action:** [Guidance]
3. **Result:** [Guidance]

**Draft Guidance:**
[Full guidance as in Paragraph 2]

**Why This Achievement:**
[Full explanation as in Paragraph 2]

**Language Notes:**
[Full language sourcing as in Paragraph 2]

**Philosophy Connection:**
[Full connection as in Paragraph 2]

---

### [OPTIONAL] Development Paragraph 4: [If gap to address OR third achievement] (~X words)

[If addressing a gap from gap analysis]:
**Purpose:** Address [specific gap identified in gap analysis]
**Pattern:** [Reframing pattern]
**Source:** 03-gap-analysis-and-cover-letter-plan.md:[section reference]

**Gap Reframing Strategy:**
[Describe the gap and how to reframe it]

**Draft Guidance:**
[Specific guidance on how to address without sounding defensive]

[If including third achievement]:
[Follow Development Paragraph 2 structure with full detail]

---

### Closing Paragraph (~X words)
**Pattern:** [Closing Pattern Name]
**Source:** narrative_patterns.md:[line reference]

**Purpose:**
- Reaffirm [what value/thread to reinforce]
- Create [what invitation/connection to establish]
- Tone: [How to balance enthusiasm with professionalism]

**Draft Guidance:**
[Provide 2-4 sentences of specific guidance on constructing close]

**Example Draft:**
"[Provide full example closing paragraph]"

**Tone Notes:**
- "[Phrase]" = [explanation - e.g., "enthusiastic but not presumptuous"]
- "[Callback element]" = [explanation - e.g., "echoes opening for structural cohesion"]
- "[Invitation language]" = [explanation - e.g., "collaborative, not demanding"]

---

## III. Evidence & Source Map

**Complete traceability of all framework elements to lexicon sources:**

### Narrative Thread
- **Thread:** [Thread Name]
- **Philosophy anchor:** career_philosophy.md:[line reference]
- **Job connection:** 01-job-analysis.md:Section [I/III]

### Opening Paragraph
- **Pattern:** [Pattern name] ← narrative_patterns.md:[line reference]
- **Philosophy:** [Value/approach referenced] ← career_philosophy.md:[line reference]
- **Language:** [Key phrase] ← language_bank.md:[line reference]

### Development Paragraph 2
- **Achievement:** [Achievement name] ← achievement_library.md:[line reference]
- **Evidence pattern:** [Pattern name] ← narrative_patterns.md:[line reference]
- **Action verbs:** "[verb 1]", "[verb 2]" ← language_bank.md:[line references]
- **Philosophy:** [Value demonstrated] ← career_philosophy.md:[line reference]

### Development Paragraph 3
- **Achievement:** [Achievement name] ← achievement_library.md:[line reference]
- **Evidence pattern:** [Pattern name] ← narrative_patterns.md:[line reference]
- **Action verbs:** "[verb 1]", "[verb 2]" ← language_bank.md:[line references]
- **Philosophy:** [Value demonstrated] ← career_philosophy.md:[line reference]

### [Development Paragraph 4 - if applicable]
[Same structure]

### Closing Paragraph
- **Pattern:** [Pattern name] ← narrative_patterns.md:[line reference]
- **Language:** [Key phrase] ← language_bank.md:[line reference]

### Language Bank Usage Summary
- Action verbs used: [List all with line references]
- Power phrases used: [List all with line references]
- Industry terms used: [List all with line references]

**Fabrication Check:** ✓ All elements traced to lexicon sources
**Voice Consistency:** ✓ All language verified against language_bank.md
**Philosophy Alignment:** ✓ All values/approaches referenced from career_philosophy.md

---

## IV. Authenticity Confirmation

User confirmation checklist completed on [YYYY-MM-DD]:

☑ Narrative thread resonates with actual motivations
☑ Examples feel accurate (not exaggerated)
☑ Language sounds like authentic voice (per language bank)
☑ Values alignment is genuine (per philosophy lexicon)
☑ Tone feels comfortable and natural
☑ Story excites user (not performative)
☑ All core values/approaches represented
☑ Nothing important missing

**User Confirmation:** ✅ Framework confirmed authentic - [YYYY-MM-DD]

**User's Note on Authenticity:**
[If user provided specific feedback on what feels most authentic, include brief quote here]

---

## V. Next Steps

You now have a complete narrative framework for your cover letter.

**Options for proceeding:**

**A) Begin collaborative drafting now**
- Work together to develop full draft using this framework
- Iterate paragraph by paragraph
- Maintain voice consistency throughout
- Next: [If collaborative-writing skill exists, reference it; otherwise: "Let me know when you're ready to begin drafting"]

**B) Draft independently and return for review**
- Use this framework as your guide
- Write at your own pace
- Return for voice consistency check and refinement
- Next: Share draft for review when ready

**C) Adjust framework first**
- Revise narrative thread, tone, or structure
- Re-confirm authenticity before drafting
- Next: Tell me what needs adjustment

**Which approach works best for you?**

---

**Framework generated:** [YYYY-MM-DD] via cover-letter-voice skill
**Lexicons used:** career_philosophy.md, narrative_patterns.md, achievement_library.md, language_bank.md
**Job analysis:** 01-job-analysis.md (Sections I & III)
[If applicable]: **Strategic plan:** 03-gap-analysis-and-cover-letter-plan.md
```

### After Markdown File Creation - JSON Export Phase

**Once markdown file is saved, create structured JSON export:**

### JSON Export Details

**Check version number:**
1. Check if `cover-letter-draft-v1.json` exists in directory
2. If exists, increment: `cover-letter-draft-v2.json`, `cover-letter-draft-v3.json`, etc.
3. Use next available version number

**Write to:** `~/career-applications/[job-slug]/cover-letter-draft-v[N].json`

**Structure:**
```json
{
  "metadata": {
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "version": 1,
    "skill": "cover-letter-voice",
    "job_slug": "[job-slug]",
    "framework_file": "04-cover-letter-framework.md"
  },
  "job_context": {
    "job_title": "[Full position title]",
    "company": "[Organization name]",
    "narrative_thread": "[Selected thread name]",
    "target_word_count": [480],
    "paragraph_count": [3-4]
  },
  "tone_profile": {
    "formality_level": "[e.g., professional-collaborative]",
    "emotional_register": "[e.g., committed-optimistic]",
    "sentence_structure": "Mix of vision statements (25-30 words), concrete examples (15-20 words), impact summaries (10-12 words)",
    "authenticity_score": 0.95,
    "confidence_level": 0.90,
    "enthusiasm_level": 0.85
  },
  "structure": {
    "opening": {
      "pattern": "[Pattern name from narrative_patterns.md]",
      "target_words": 85,
      "purpose": "Hook with institutional positioning and mission alignment",
      "philosophy_anchor": "[Value/approach from philosophy.md:line]",
      "example_draft": "[Full example paragraph from framework]",
      "key_phrases": ["phrase 1", "phrase 2"]
    },
    "body_paragraphs": [
      {
        "paragraph_number": 2,
        "theme": "[Achievement/Theme name]",
        "pattern": "[Evidence pattern name]",
        "target_words": 150,
        "purpose": "Demonstrate [key quality]",
        "achievement_cited": "[Achievement name from library]",
        "source": "achievement_library.md:[line reference]",
        "structure_elements": {
          "context": "Brief description of guidance",
          "action": "Brief description of guidance",
          "result": "Brief description of guidance"
        },
        "philosophy_connection": "[Value demonstrated from philosophy.md:line]"
      },
      {
        "paragraph_number": 3,
        "theme": "[Achievement/Theme name]",
        "pattern": "[Evidence pattern name]",
        "target_words": 140,
        "purpose": "Demonstrate [key quality]",
        "achievement_cited": "[Achievement name]",
        "source": "[Citation]",
        "philosophy_connection": "[Value demonstrated]"
      }
    ],
    "closing": {
      "pattern": "[Pattern name from narrative_patterns.md]",
      "target_words": 75,
      "purpose": "Reaffirm values and create invitation",
      "example_draft": "[Full example paragraph from framework]",
      "tone_notes": "Enthusiastic but not presumptuous, collaborative invitation"
    }
  },
  "narrative_elements": {
    "primary_thread": "[Thread name]",
    "philosophy_anchor_quote": "[Quote from philosophy.md with line reference]",
    "achievements_featured": [
      {
        "name": "[Achievement 1 name]",
        "source": "achievement_library.md:[line]",
        "demonstrates": "[Key quality]",
        "in_paragraph": 2
      },
      {
        "name": "[Achievement 2 name]",
        "source": "achievement_library.md:[line]",
        "demonstrates": "[Key quality]",
        "in_paragraph": 3
      }
    ],
    "values_represented": [
      {
        "value": "[Value name]",
        "source": "career_philosophy.md:[line]",
        "where_shown": "opening paragraph + body paragraph 2"
      }
    ]
  },
  "language_sources": {
    "action_verbs": [
      {"verb": "[verb1]", "source": "language_bank.md:[line]", "category": "[category]"},
      {"verb": "[verb2]", "source": "language_bank.md:[line]", "category": "[category]"}
    ],
    "power_phrases": [
      {"phrase": "[phrase1]", "source": "language_bank.md:[line]"},
      {"phrase": "[phrase2]", "source": "language_bank.md:[line]"}
    ],
    "fabrication_check": "PASSED",
    "voice_consistency": "VERIFIED"
  },
  "authenticity_confirmation": {
    "confirmed_date": "YYYY-MM-DD",
    "user_feedback": "[Brief quote from user about what feels most authentic, if provided]",
    "checklist_completed": true,
    "concerns_addressed": []
  },
  "suggestions": [
    "Use example opening as tone calibration guide",
    "Maintain sentence length variety per structure guidance",
    "Reference source map in framework for additional language options",
    "Ensure all achievements mentioned are accurate to experience",
    "Consider collaborative drafting if tone calibration feels uncertain"
  ],
  "next_steps": [
    "Begin drafting using framework guidance",
    "Maintain authenticity throughout - use own words while following structure",
    "Return for voice consistency review after first draft",
    "Consider collaborative-writing skill for paragraph-by-paragraph development"
  ]
}
```

**Implementation:**
1. Extract structured data from the framework document
2. Calculate scores based on tone profile (authenticity/confidence/enthusiasm as decimals 0.0-1.0)
3. Include only the specific data from the user's framework (don't fabricate placeholder content)
4. Format with 2-space indentation for readability
5. Save to same directory as markdown framework

**Present to user:**
```
✓ Cover letter framework created successfully
✓ JSON export generated for wrapper application

Files saved:
- ~/career-applications/[job-slug]/04-cover-letter-framework.md (complete framework)
- ~/career-applications/[job-slug]/cover-letter-draft-v[N].json (structured data export)

Framework includes:
- Complete tone profile with example opening
- Detailed structure for each paragraph (opening + [X] development + closing)
- Draft guidance for all sections
- Full source map linking all content to your lexicons
- Authenticity confirmation timestamp

JSON export includes:
- Structured narrative elements and achievements
- Tone analysis with quantified scores
- Language sources with traceability
- Paragraph-by-paragraph breakdown
- Suggestions and next steps

The framework is ready to use for writing your cover letter.

Would you like to:
A) Begin drafting now (collaborative)
B) Review the framework file first
C) Adjust anything in the framework
```

---

## Error Handling

### Error Handler A: Missing Job Analysis

**If `01-job-analysis.md` not found:**

```
❌ I cannot find the job analysis file for this application.

Path checked: ~/career-applications/[job-slug]/01-job-analysis.md

The cover letter framework requires analysis of the job's cultural requirements,
values, and communication style (from Sections I & III of the job analysis).

Options:

A) Run job-description-analysis skill now
   - I can analyze the job description to create the required analysis file
   - This will give me the cultural/values context needed for your cover letter
   - Recommended: Start with this option

B) Provide job analysis manually
   - If you have analysis in a different location, share the path
   - I'll use that instead

C) Create framework without job analysis (not recommended)
   - Will base framework solely on your lexicons
   - Risk: May not match organization's tone/cultural requirements
   - Only use if you deeply understand the organization already

Which option would you like?
```

**If user selects A:**
```
Let me invoke the job-description-analysis skill to create the required analysis.

[Invoke job-description-analysis skill or guide user to do so]
```

### Error Handler B: Missing Lexicon Files

**If philosophy, narrative patterns, or language bank missing:**

```
❌ Required lexicon files are missing

I cannot find these essential files:
[List missing files with full paths]

The cover letter framework must be grounded in YOUR authentic voice and patterns.
I cannot create a framework without these lexicons—doing so would risk
fabricating language and narrative approaches that don't reflect your real voice.

What's missing and why it matters:

[If career_philosophy.md missing]:
- career_philosophy.md: Your core values and leadership approaches
- Without this: Cannot ensure narrative aligns with what you genuinely believe
- Path expected: ~/lexicons_llm/01_career_philosophy.md

[If narrative_patterns.md missing]:
- narrative_patterns.md: Your established storytelling patterns
- Without this: Cannot use narrative structures you've successfully used before
- Path expected: ~/lexicons_llm/03_narrative_patterns.md

[If language_bank.md missing]:
- language_bank.md: Your authentic voice and word choices
- Without this: Cannot verify language sounds like you
- Path expected: ~/lexicons_llm/04_language_bank.md

---

How to generate missing lexicons:

These lexicons are created by analyzing your existing career materials
(philosophy statements, past cover letters, resumes, teaching statements, etc.)

To generate them:

1. Collect source materials:
   - Career philosophy statements
   - Past cover letters and application materials
   - Resume/CV
   - Teaching philosophy (if applicable)
   - Any documents that reflect your authentic professional voice

2. Run the lexicon generation system:
   [Provide instructions based on how lexicons are generated in this system]

   OR

   If you have the career-lexicon-builder system:
   - Place documents in ~/my_documents/
   - Run: python run_llm_analysis.py
   - Lexicons will be generated in ~/lexicons_llm/

3. Return to this skill once lexicons exist

---

I cannot proceed without these foundational lexicons. They are what ensure
your cover letter framework will be authentic to your voice, not fabricated.

Would you like guidance on generating these lexicons?
```

### Error Handler C: User Rejects Narrative Thread

**If user doesn't like any of the 3 narrative thread options:**

```
I understand none of these narrative threads feel quite right.

Let's explore what's missing or what would work better.

A few questions to help me understand:

1. What specifically felt off about the options I presented?
   - Too narrow in focus?
   - Missing a key aspect of your motivation?
   - Not capturing the real opportunity?
   - Something else?

[Wait for response]

2. When you think about this role, what excites you most?
   - What draws you to it?
   - What do you hope to accomplish there?
   - What aspect of your experience feels most relevant?

[Wait for response]

3. Looking at your career philosophy lexicon, which values or approaches
   feel most important to emphasize for THIS specific opportunity?

[Wait for response]

---

Based on your responses, let me develop alternative narrative threads:

[Generate 2-3 new options based on user's feedback]

[Use AskUserQuestion to present new options]

Do any of these resonate better?
```

**If user still uncertain:**
```
It sounds like we need to explore this more deeply before choosing a thread.

Would it help to:
A) Review the job analysis together to clarify what they're really looking for
B) Review your philosophy lexicon to identify what matters most to you about this
C) Look at past cover letters to see what narrative approaches have felt authentic before
D) Take a break and return to this—sometimes these decisions benefit from time

Which approach feels most useful?
```

### Error Handler D: Tone Feels Inauthentic

**If user says tone profile doesn't feel right:**

```
Let's adjust the tone to match your authentic voice.

What specifically feels off?

Is it:
A) Too formal / not formal enough
B) Too enthusiastic / not enthusiastic enough
C) Too strategic-visionary / not strategic enough
D) Wrong emotional register (too warm? too detached?)
E) Something else

[Wait for response]

---

[Based on response, ask follow-up]:

[If formality issue]:
"On a scale where 1 is very casual/conversational and 5 is academic-formal,
where should this letter land? (Their culture seems to be around [X] based
on job analysis)"

[If enthusiasm issue]:
"Should the tone be more [grounded/excited/measured]? What word describes
the energy level that feels right?"

[If strategic vs. operational balance]:
"Should this emphasize more [vision/execution]? More [big picture/concrete details]?"

[If emotional register]:
"What emotional quality should come through? [committed? warm? authoritative?
reflective? optimistic? pragmatic?]"

---

Let me also check: Looking at your past cover letters [if available],
which one's tone felt most authentic to you?

[If user identifies one]:
Let me analyze that tone more carefully and adjust the profile to match.

[Analyze identified letter's tone]
[Revise tone profile]
[Re-present with new example opening sentence]

Does this feel closer?
```

**If still not right after adjustment:**
```
I want to make sure we get this right. Your tone needs to feel authentic,
not like you're performing.

Let me try a different approach:

Could you draft just the first sentence of the letter—write it in whatever
tone feels natural to you? Don't overthink it, just how you'd naturally begin.

[Wait for user to provide example]

[Analyze user's example for:]
- Formality level
- Sentence structure
- Word choices
- Emotional register

[Create tone profile based on user's actual writing]
[Present revised profile]

This is based on YOUR actual voice. Does this feel authentic now?
```

---

## Success Criteria

A cover letter framework is successful when:

✓ **Grounded in Philosophy**
- All narrative elements trace to career_philosophy.md
- Core values explicitly represented
- Leadership approaches evident in structure/examples

✓ **Language Authenticity**
- All verbs/phrases verified against language_bank.md
- No fabricated language (everything has lexicon source)
- Tone matches user's natural voice

✓ **Pattern Consistency**
- Uses established patterns from narrative_patterns.md
- Structure reflects user's proven approaches
- Evidence patterns match past successful narratives

✓ **Job Alignment**
- Tone matches cultural requirements from job analysis
- Narrative addresses their stated priorities
- Structure appropriate for role level

✓ **Complete Evidence Trail**
- Every element has source citation (file:line)
- Source map documents all connections
- No unsourced claims or language

✓ **User Confirmation**
- User explicitly confirms: "This framework feels authentic"
- User excited about at least one element
- No concerns about performativity or inauthenticity

✓ **Actionable Framework**
- Clear draft guidance for each paragraph
- Specific examples with tone notes
- Structure ready to use for writing

**The ultimate test:**
User can take this framework and write a cover letter that sounds genuinely like them,
using their real voice to tell a true story about their authentic interest in the role.

---

## Notes for Skill Users

**This skill creates a FRAMEWORK, not a draft letter.**

The output is:
- Strategic foundation for writing
- Tone guidance with examples
- Structure with detailed paragraph guidance
- Complete source documentation

The output is NOT:
- A ready-to-send cover letter
- A full draft requiring only minor edits
- A template you fill in

**Why framework instead of draft?**

1. **Authenticity:** You write in your real voice, not an AI approximation
2. **Ownership:** You make the specific word choices that feel right
3. **Flexibility:** You can adjust as you write based on what flows
4. **Truth:** You ensure every claim is accurate to your experience

**Next steps after framework:**
- Use framework as guide for independent drafting, OR
- Collaborate on drafting with AI using framework as foundation, OR
- Refine framework further before writing

**The framework ensures your letter will:**
- Sound like you (verified through language bank)
- Tell your authentic story (grounded in philosophy)
- Use proven patterns (from narrative patterns)
- Match the opportunity (aligned with job analysis)

---

## Skill Metadata

**Version:** 1.0
**Last Updated:** 2025-10-31
**Part of:** Socratic Career Skills suite
**Dependencies:** job-description-analysis (recommended), lexicon generation system (required)
**Related Skills:** job-fit-analysis (provides strategic plan), collaborative-writing (for drafting)

**Typical Duration:** 30-45 minutes for complete framework development
**User Involvement:** High (Socratic questioning throughout, multiple confirmation points)
**Output Quality Gate:** User must confirm authenticity before file creation
