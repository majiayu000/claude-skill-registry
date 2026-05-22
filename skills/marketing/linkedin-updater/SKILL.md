---
name: linkedin-updater
description: Generate LinkedIn profile update instructions based on best practices and career data from XML files. Use when user asks to "update my LinkedIn", "optimize my LinkedIn profile", "improve my LinkedIn", "refresh my LinkedIn", "LinkedIn best practices", "LinkedIn profile update", "LinkedIn SEO", or "make my LinkedIn stand out". Outputs a structured Markdown document with section-by-section instructions including copy-paste content for Headline, About, Experience, Skills, and Featured sections.
---

# LinkedIn Updater

Generate LinkedIn profile update instructions by applying best practices to career data.

## Workflow Overview

```
1. LOAD CAREER DATA
   └─ Read: career-summary.xml (positioning, metrics), career-profile.xml (STAR activities)

2. EXTRACT KEY ELEMENTS
   └─ Identity, headline positioning, key metrics, differentiators, keywords

3. APPLY BEST PRACTICES
   └─ Generate content for each LinkedIn section per formula/structure

4. OUTPUT INSTRUCTIONS
   └─ Save to linkedin/profile-update-{YYYY-MM-DD}.md with copy-paste blocks
```

## Input Requirements

**From Project Knowledge (experience/ directory):**
- `experience/career-summary.xml` — Identity, positioning, key metrics, keywords (quick reference)
- `experience/career-profile.xml` — Full career with STAR-formatted activities for Experience bullets
- `experience/interview-positioning.xml` — Elevator pitch, differentiators, talking points

## Step 1: Load and Extract Career Data

Extract from XML files:

| Element | Source | Usage |
|---------|--------|-------|
| Identity | `<identity>` in career-summary.xml | Name, title, contact info |
| Headline | `<positioning><headline>` | Starting point for Headline optimization |
| Key Metrics | `<key-metrics>` | Proof points for About section |
| Differentiators | `<differentiators>` | Unique value props for About |
| Keywords | `<keywords>` | SEO terms for all sections |
| STAR Activities | `<activity>` in career-profile.xml | CAR bullets for Experience |
| Elevator Pitch | `<elevator-pitch>` in interview-positioning.xml | Hook for About section |

## Step 2: Generate Section Content

### Headline (220 characters max)

**Formula:** `[Role] | [Specialization] | [Quantified Value] | [Key Differentiator]`

Apply formula using:
- Role: Current title from `<current-title>`
- Specialization: Primary profile from `<profile-hierarchy>`
- Quantified Value: Top metric from `<key-metrics>`
- Key Differentiator: Strongest from `<differentiators>`

**Include 2-3 searchable AI keywords:** Generative AI, LLMs, AI Strategy, AI Platform

**Generate 3 headline options** for user to choose from.

### About Section (2600 characters max)

**Five-Part Structure:**

1. **Hook (first 3 lines visible before "see more")**
   - Use `<elevator-pitch>` from interview-positioning.xml
   - Make boldest claim or unique insight

2. **Who You Help + Transformation**
   - Target audience and problems you solve
   - Draw from `<positioning>` section

3. **Proof Points (3-5 bullets)**
   - Select from `<key-metrics>`:
     - $1.5B pipeline (Google Value Engineering)
     - 100% program survival rate (6 programs, 3-7+ years)
     - 10-layer AI platform architecture (McDonald's CIO endorsed)
     - 154 GCP Champs participants (7X completion rate)
     - SME for Stratozone → Google Cloud Migration Center

4. **Philosophy/Unique Lens**
   - Permanence Architecture methodology
   - Builder-architect hybrid approach

5. **Call to Action**
   - DM invitation with specific context

**First-person voice.** Use 8th grade English. Avoid jargon and hyperbole.

### Experience Section

**Per Position (3-5 bullets each):**

Convert STAR activities to CAR format:
- **Challenge:** Combine `<situation>` + `<task>` for context
- **Action:** Use `<action>` with power verbs
- **Result:** Use `<result>` with inline metrics

**Bullet Format:**
```
[Action verb] [what was done] to [address challenge], resulting in [quantified result]
```

**Guidelines:**
- Lead with quantified outcomes, not responsibilities
- Use 8th grade English
- Vary action verbs (no verb used more than twice)
- Include keywords naturally

See `references/linkedin-best-practices.md` for power verb lists.

### Skills Section

**Order by keyword tier:**

| Tier | Count | Strategy |
|------|-------|----------|
| **Core** | Top 3 | Most searched skills for target roles |
| **Secondary** | Next 7 | Supporting technical/domain skills |
| **Long-tail** | Remaining | Niche differentiators |

**Extract from `<keywords>` section and `<expertise>` tiers.**

**Recommended Core Skills:**
1. Generative AI
2. Enterprise Architecture
3. AI Strategy

### Featured Section

**Recommend content to add:**
- Case studies demonstrating Permanence Architecture
- Speaking engagements or thought leadership
- Certifications display
- External validation (articles, awards)

## Step 3: Generate Output

**Save to:** `linkedin/profile-update-{YYYY-MM-DD}.md`

**Document Structure:**

```markdown
# LinkedIn Profile Update Instructions
Generated: {timestamp}

---

## Headline
**Character Count:** [X/220]

### Option 1 (Recommended):
```
[Generated headline]
```

### Option 2:
```
[Alternative headline]
```

---

## About Section
**Character Count:** [X/2600]

### Copy-Paste Version:
```
[Generated about section with all 5 parts]
```

---

## Experience Section Updates

### [Company] | [Title]
**[Dates]**

**Recommended Bullets:**
1. [CAR bullet]
2. [CAR bullet]
3. [CAR bullet]

[Repeat for each position...]

---

## Skills Section

### Recommended Order:

**Top 3 (Core):**
1. [Skill]
2. [Skill]
3. [Skill]

**Next 7 (Secondary):**
4-10. [Skills list]

---

## Featured Section Recommendations

1. [Recommendation]
2. [Recommendation]

---

## Implementation Checklist

- [ ] Update headline
- [ ] Replace About section
- [ ] Update current role bullets
- [ ] Reorder skills
- [ ] Add Featured content
- [ ] Request fresh recommendations
```

## Quality Checklist

Before delivering, verify:

- [ ] Headline under 220 characters with 2-3 AI keywords
- [ ] About section under 2600 characters with all 5 parts
- [ ] About uses first-person voice and 8th grade English
- [ ] Key metrics included as proof points (at least 3)
- [ ] Experience bullets follow CAR format with quantified results
- [ ] Skills ordered by keyword tier (Core → Secondary → Long-tail)
- [ ] Featured section has actionable recommendations
- [ ] Implementation checklist included
- [ ] File saved to `linkedin/profile-update-{date}.md`

## Reference Files

- `references/linkedin-best-practices.md` — Section formulas, keyword strategy, power verbs
- `experience/career-summary.xml` — Quick reference for identity, metrics, keywords
- `experience/career-profile.xml` — Full STAR activities for Experience bullets
- `experience/interview-positioning.xml` — Elevator pitch and differentiators
