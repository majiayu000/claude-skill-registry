---
name: prose-polish
description: Evaluate and elevate writing effectiveness through multi-dimensional quality assessment. Analyzes craft, coherence, authority, purpose, and voice with genre-calibrated thresholds. Use for refining drafts, diagnosing quality issues, generating quality content, or teaching writing principles.
---

# Prose Polish v2

Evaluate and elevate writing effectiveness through multi-dimensional quality assessment. Goal is not "less AI-like" but genuinely better writing—coherent, credible, purposeful, and distinctive.

## Philosophy

**Writing Effectiveness = f(Text, Author, Audience, Context, Genre)**

We optimize for quality, not undetectability. These often correlate, but the distinction matters:
- Bad goal: "Make this not sound like AI"
- Good goal: "Make this effective writing"

## Quick Start

**Analysis:** Detect genre → Load `detection-patterns.md` → Apply 6-dimension evaluation → Generate quality profile

**Elevation:** Analyze → Load `remediation-strategies.md` → Phase 1 (Structure) → Phase 2 (Style) → Explain changes

**Prevention:** Load `prevention-prompts.md` → Build genre-calibrated constraints → Generate → Self-verify

## Core Capabilities

### 1. Detection & Analysis

**When:** User asks to "analyze," "evaluate," "check," or "score" text

**Process:**
1. **Detect Genre** (before scoring)
   - Technical | Business | Academic | Creative | Personal | Journalistic
   - Apply genre-appropriate thresholds

2. **Load** `references/detection-patterns.md`

3. **Perform 6-Dimension Analysis:**
   - **Craft (0-100):** Lexical patterns, structural variance, rhetorical execution
   - **Coherence (0-100):** Logical flow, functional specificity, earned transitions
   - **Authority (0-100):** Earned vs delegated vs false expertise signals
   - **Purpose (0-100):** Clear intent, stakes, audience calibration
   - **Voice (0-100):** Distinctiveness, embodiment, appropriate register
   - **Effectiveness (0-100):** Genre-weighted synthesis

4. **Generate Quality Profile**

**Report Format:**
```
WRITING EFFECTIVENESS ANALYSIS

Genre: [Detected] | Calibration: [Applied]

QUALITY PROFILE:
           Craft: ████████░░ 80 - [Brief interpretation]
       Coherence: ██████░░░░ 60 - [Brief interpretation]
       Authority: █████░░░░░ 50 - [Brief interpretation]
         Purpose: ███████░░░ 70 - [Brief interpretation]
           Voice: █████████░ 90 - [Brief interpretation]
   Effectiveness: ███████░░░ 70 - [Genre-weighted average]

KEY INSIGHT: [Diagnostic based on dimension gaps]
Example: "High craft but low authority = generic specificity problem"

DETAILED ANALYSIS:

CRAFT ISSUES:
- Lexical: [specific patterns, with genre context]
- Structural: [sentence variance, paragraph patterns]
- Rhetorical: [commitment level, specificity quality]

COHERENCE ISSUES:
- Logical flow: [do ideas connect across paragraphs?]
- Specificity function: [relevant vs decorative details]
- Transition authenticity: [earned vs mechanical]

AUTHORITY ISSUES:
- Type: [Earned / Delegated / False / Mixed]
- Expertise signals: [insider knowledge present/absent]
- Stakes: [skin in the game visible?]

PURPOSE ISSUES:
- Intent clarity: [what is this FOR?]
- Audience calibration: [appropriate for reader?]
- Stakes: [why should reader care?]

VOICE ISSUES:
- Distinctiveness: [recognizable author?]
- Embodiment: [feels like a person?]
- Register: [appropriate for genre?]

TOP 5 PRIORITY IMPROVEMENTS:
1. [Most impactful, actionable fix]
2. [...]
3. [...]
4. [...]
5. [...]
```

**Scoring Philosophy:**
- Be ruthless in scoring. Avoid grade inflation.
- Dimension gaps are diagnostic (high craft + low coherence = decorative writing)
- Genre calibration prevents false positives on appropriate conventions

### 2. Elevation & Remediation

**When:** User asks to "improve," "fix," "elevate," or "rewrite" text

**Process:**
1. Perform quick 6-dimension analysis
2. Load `references/remediation-strategies.md`
3. Apply **Two-Phase Remediation:**

**Phase 1: Structural (The Editor)**
Focus on logic and authority before touching style.

- **Coherence Pass:**
  - Check: Does logic flow across paragraphs?
  - Check: Is every detail doing work?
  - Fix: Remove decorative specificity
  - Fix: Repair logical gaps
  - Fix: Ensure transitions are earned

- **Authority Pass:**
  - Check: Is authority earned or delegated?
  - Fix: Replace institutional voice with speaker
  - Fix: Add demonstrated expertise signals
  - Fix: Introduce appropriate stakes/vulnerability

**Phase 2: Stylistic (The Writer)**
Now refine rhythm, commitment, and voice.

- **Rhythm Pass:**
  - Sentence variance per genre threshold
  - Structural breaks appropriate to genre
  - Information density variance (avoid uniform medium-density)

- **Commitment Pass:**
  - Remove cowardly hedges (opinion avoidance)
  - Preserve protective hedges (epistemic honesty)
  - Add functional specificity
  - Make claims with stakes

- **Voice Pass:**
  - Add embodiment markers
  - Inject appropriate personality (avoid "LinkedIn Influencer" overcorrection)
  - Risk-taking calibrated to genre

**Output:**
```
ELEVATED VERSION:
[Rewritten text]

PHASE 1 CHANGES (Structure):
- Coherence: [What logical issues were fixed]
- Authority: [How expertise was demonstrated]

PHASE 2 CHANGES (Style):
- Rhythm: [Sentence variation details]
- Commitment: [Hedge removal, specificity additions]
- Voice: [Personality calibration]

BEFORE/AFTER EXAMPLES:
[3-5 transformations with principles explained]
```

**Depth Control (Aggressiveness Levels):**

Users can control the extent of remediation:

| Level | What It Does | When to Use |
|-------|--------------|-------------|
| **Conservative** | Phase 1 only (Coherence + Authority) | Preserve voice, fix logic only |
| **Moderate** | Both phases, light Phase 2 | Balance improvement with original tone |
| **Aggressive** | Both phases, full transformation | Complete rewrite for maximum quality |

**How to request:**
- "Fix the logic but keep my voice" → Conservative
- "Improve this while keeping the general tone" → Moderate
- "Rewrite this for maximum effectiveness" → Aggressive

**Default:** Moderate (both phases, respects original intent)

### 3. Prevention & Generation

**When:** User asks to "write" or "generate" with quality emphasis

**Process:**
1. Identify genre and audience
2. Load `references/prevention-prompts.md`
3. Construct genre-calibrated constraints
4. Generate with quality dimensions in mind
5. Self-verify against 6-dimension framework
6. Refine if any dimension scores below threshold

### 4. Training & Teaching

**When:** User wants to learn quality evaluation

**Process:**
1. Load appropriate reference files
2. Explain the 6 dimensions and why they matter
3. Show examples of dimension gaps (high X, low Y)
4. Demonstrate genre calibration effects
5. Practice exercises with real text

## Genre Calibration

**Detect genre before scoring. Apply appropriate thresholds:**

| Genre | Sentence Variance | Hedge Tolerance | Passive Voice | Template OK | Voice Expectation |
|-------|-------------------|-----------------|---------------|-------------|-------------------|
| Technical | 5+ StdDev | Higher (precision) | Higher | Expected | Neutral authority |
| Business | 6+ StdDev | Standard | Lower | Structure OK | Professional human |
| Academic | 6+ StdDev | Higher (epistemic) | Moderate | If fresh content | Measured expertise |
| Creative | 8+ StdDev | Low | Low | = Failure | Distinctive required |
| Personal | 8+ StdDev | Low | Low | Must be organic | Strongly embodied |
| Journalistic | 7+ StdDev | Standard | Low | Lead structure OK | Clear but present |

### Genre-Specific Signals

**Technical Documentation:**
- Allow: "certain," "particular," "specific" (precision, not hedging)
- Allow: Consistent sentence length (clarity, not robotic)
- Require: Explains WHY not just HOW
- Authority: Demonstrated through insider terminology and tradeoff awareness

**Business Writing:**
- Require: Friction acknowledgment (what challenges exist?)
- Require: Clear ownership and next steps
- Watch: Institutional hiding ("it is recommended" vs "I recommend")
- Authority: Numbers with interpretation, not just data dumps

**Academic Writing:**
- Require: Synthesis over summarization
- Require: Clear contribution statement
- Allow: "It appears that" as epistemic honesty
- Authority: Citation genealogy, not just name-dropping

**Creative/Narrative:**
- Require: Surprise, sensory embodiment
- Require: Specificity that reveals character, not decorates
- Watch: Generic emotional beats ("hollow ache" without texture)
- Authority: Earned through embodied experience

## Dimension Deep Dives

### Coherence (NEW in v2)

**What it catches:** Decorative specificity, logic gaps, non-sequiturs

**Red Flags:**
- Details that don't advance understanding
- Causal claims that don't hold ("teaching calculus → cracked hands")
- Transitions that connect syntactically but not semantically
- Specificity that signals "human-ness" rather than builds meaning

**Questions to Ask:**
1. If I remove transitions, do ideas still connect?
2. Could I swap paragraphs without changing meaning? (Bad if yes)
3. Is every specific detail doing work?
4. Would a hostile reader find logical gaps?

### Authority (NEW in v2)

**What it catches:** Performed expertise vs demonstrated expertise

**Authority Types:**
- **Earned:** Insider details, vulnerability, consequences for being wrong
- **Delegated:** Citations without synthesis, institutional voice, numbers without interpretation
- **False:** Stereotypes as expertise, generic specificity, authority cosplay

**Note:** We measure *signaling*, not *truth*. An LLM cannot verify facts—it can only assess whether authority markers are present. Be honest about this limitation.

### Hedge Classification (NEW in v2)

**Not all hedges are bad. Classify before penalizing:**

**Cowardly Hedges (PENALIZE):**
- Avoiding opinion: "Some might say," "It could be argued"
- Diluting claims: "somewhat," "fairly," "rather"
- Escape hatches: "in a sense," "in many ways"

**Protective Hedges (PRESERVE):**
- Epistemic honesty: "The evidence suggests," "Current research indicates"
- Appropriate uncertainty: "appears to," "likely"
- Precision: "certain," "particular," "specific"

## Quality Standards

Every output should pass:

**Coherence Test:** Do ideas connect logically across the piece?
**Authority Test:** Is expertise demonstrated, not just claimed?
**Purpose Test:** Is it clear what this writing is FOR?
**Voice Test:** Would you recognize this author again?
**Embodiment Test:** Does it feel like a person with experiences?
**Surprise Test:** Is there at least one unexpected element?

## Effectiveness Calculation

**Genre-weighted average:**

| Genre | Craft | Coherence | Authority | Purpose | Voice |
|-------|-------|-----------|-----------|---------|-------|
| Technical | 25% | 30% | 20% | 15% | 10% |
| Business | 20% | 25% | 25% | 20% | 10% |
| Academic | 20% | 30% | 20% | 15% | 15% |
| Creative | 15% | 20% | 10% | 15% | 40% |
| Personal | 15% | 20% | 20% | 15% | 30% |

## Reference Files

**When to Load:**
- **detection-patterns.md:** Always for analysis (includes coherence patterns, authority signals, hedge classification)
- **remediation-strategies.md:** Always for elevation (two-phase framework)
- **prevention-prompts.md:** Always for generation (genre-calibrated constraints)
- **ai-vocabulary.md:** When checking specific banned words

## Critical Principles

1. **Effectiveness Over Detection:** Goal is quality writing, not fooling detectors.

2. **Genre Calibration Is Non-Negotiable:** Technical docs and creative fiction have different rules.

3. **Dimension Gaps Are Diagnostic:** High craft + low coherence = decorative writing. High voice + low authority = personality without substance.

4. **Coherence Before Surface:** Fix logic before fixing rhythm. A polished fallacy is still a fallacy.

5. **Authority Is Signaling:** We measure expertise markers, not truth. Be honest about this.

6. **Hedges Need Classification:** Epistemic honesty is not weakness. Only penalize opinion-avoidance.

7. **Avoid Overcorrection:** "LinkedIn Influencer" mode is not the goal. Calibrate voice to genre.

8. **Radical Simplicity Has Value:** Sometimes effectiveness means removing signals, not adding them.

## Examples

### Analysis Example

**Input:** Business quarterly report with strong metrics but institutional voice

**Output:**
```
WRITING EFFECTIVENESS ANALYSIS

Genre: Business | Calibration: Applied

QUALITY PROFILE:
           Craft: ████████░░ 78 - Clean structure, precise numbers
       Coherence: ████████░░ 85 - Logical flow, functional data
       Authority: █████████░ 88 - Genuine SaaS expertise visible
         Purpose: ███████░░░ 75 - Clear reporting, muted stakes
           Voice: ██████░░░░ 62 - Institutional, could be any company
   Effectiveness: ████████░░ 82 - Strong business communication

KEY INSIGHT: High authority through insider metrics (NRR, churn analysis)
compensates for institutional voice. Genre-appropriate execution.

DETAILED ANALYSIS:
...
```

### Elevation Example (Two-Phase)

**Phase 1 Output:**
```
STRUCTURAL FIXES:
- Coherence: Moved security section before feature description (foundations first)
- Authority: Replaced "best practices recommend" with specific tradeoff analysis
```

**Phase 2 Output:**
```
STYLISTIC FIXES:
- Rhythm: Added 5-word punch after long explanation
- Commitment: Removed "somewhat" and "fairly" (cowardly hedges)
- Voice: Added one moment of personality without overdoing it
```

## Success Metrics

**Objective:**
- Coherence score improvement when logic is fixed
- Authority score reflects genuine expertise presence
- No false positives on genre-appropriate conventions
- Dimension gaps correctly diagnose quality issues

**Subjective:**
- Text reads as effective for its purpose
- Domain experts recognize authentic expertise
- Genre conventions respected, not penalized
- User understands WHY changes improve quality

## Notes

- This skill evaluates effectiveness, not truth
- Genre detection happens BEFORE scoring
- Two-phase remediation: structure first, style second
- Hedge classification: epistemic honesty is not weakness
- Avoid overcorrection: "more voice" can become cringe
- Radical simplicity sometimes wins over complexity
