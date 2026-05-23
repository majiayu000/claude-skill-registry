---
name: resume-generator
description: Generate tailored, ATS-optimized resumes from job descriptions with psychology-informed placement optimization. Use when the user asks to create a resume, tailor a resume for a job, apply to a position, update their CV, or generate application materials. Triggers include phrases like "tailor my resume for", "I'm applying to", "generate resume for this JD", "update my resume", or "help me apply to". Produces Markdown output rendered as an artifact with knockout prevention, authenticity scoring, context-calibrated weighting, and above-the-fold optimization for the 7-second recruiter scan.
---

# Resume Generator

Generate tailored, ATS-optimized resumes that survive both algorithmic screening AND the 7-second human scan.

## Critical Context

**The 7-Second Reality**: Recruiters spend 6-7 seconds on initial scan. 80% of viewing time concentrates on: name, current title/company, previous title/company, dates, education. Everything below the fold is largely ignored during yes/no/maybe sorting.

**Dual-Audience Optimization**: Resume must pass ATS keyword matching AND create human excitement. Optimize for both without alienating either.

## Workflow Overview

```
0. KNOCKOUT SCREENING (Mandatory)
   └─ Verify no disqualifying factors before proceeding

1. CONTEXT SELECTION
   └─ User selects: seniority level, function type, company type

2. PARSE JOB DESCRIPTION
   └─ Extract: keywords, requirements, culture signals, seniority indicators

3. RETRIEVE & MATCH
   └─ Load achievements; score against JD; apply context-specific weights

4. ABOVE-THE-FOLD OPTIMIZATION
   └─ Place strongest evidence in high-attention zones (top-third, left-aligned)

5. GENERATE WITH AUTHENTICITY
   └─ Apply frameworks; vary patterns; use precise metrics

6. QUALITY VERIFICATION
   └─ Knockout re-check, authenticity audit, parsing confidence

7. PRODUCE OUTPUT
   └─ Render artifact; save file; provide tailoring summary with LinkedIn alert
```

## Step 0: Knockout Screening (MANDATORY)

Complete before any optimization. A single knockout negates all other work.

### Hard Knockouts (Flag if present)
| Factor | Action |
|--------|--------|
| Missing required degree/certification | Flag gap; recommend addressing in cover letter |
| Below minimum experience threshold | Calculate actual years; if close, emphasize depth |
| Employment gap >6 months | Develop proactive framing (see references/gap-strategies.md) |
| Job hopping (<1yr tenures × 3+) | Prepare context (contracts, acquisitions, reorgs) |
| Title inflation risk | Verify claimed titles match LinkedIn exactly |

### Format Knockouts (Verify clean)
- [ ] Professional email address
- [ ] Phone in standard format
- [ ] LinkedIn URL functional
- [ ] No special characters that may corrupt parsing

**STOP if hard knockout present without mitigation strategy.**

## Step 1: Context Selection

User MUST specify (ask if not provided):

### Seniority Level
| Level | Weight Profile |
|-------|---------------|
| **Entry-level** | Education 40%, Skills 35%, Potential indicators HIGH |
| **Mid-career** | Skills 40%, Experience 25%, Progression 20% |
| **Senior/Executive** | Strategic impact 30%, Leadership 25%, Education MINIMAL |

### Function Type
| Function | Optimization Focus |
|----------|-------------------|
| **Technical** | Boolean skills match, specific tools/versions, penalize fluff |
| **Sales** | Quota attainment %, deal metrics, HIGH skepticism on claims |
| **Operations** | Operational metrics (OEE, yield), certifications, safety |
| **Executive** | P&L, board exposure, transformation narratives |

### Company Type
| Type | Signals to Emphasize |
|------|---------------------|
| **Startup** | Adaptability, breadth, speed, "wore multiple hats" |
| **Enterprise** | Brand recognition, specialization, stability, process |

Load weight profile from `references/context-profiles.md` based on selection.

## Step 2: Parse Job Description

Extract and categorize:

| Category | Extract |
|----------|---------|
| **Hard requirements** | Required skills, certs, years (these are knockout criteria) |
| **Soft requirements** | Preferred qualifications, nice-to-haves |
| **Keywords** | Technical terms, tools, methodologies—exact phrasing |
| **Culture signals** | Values language, team descriptors |
| **Success metrics** | How performance measured (informs achievement selection) |

Create keyword frequency map. Top 10 keywords MUST appear in resume.

## Step 3: Retrieve & Match Achievements

For each JD requirement, scan achievements-bank.md:

**Scoring (apply context weights from Step 1):**
- Direct match (same skill/outcome): 3 points × context weight
- Adjacent match (transferable): 2 points × context weight
- Contextual match (similar domain): 1 point × context weight

**Prioritization:**
1. Ensure ALL hard requirements have evidence
2. Rank by weighted score
3. Flag gaps (requirements without strong matches)

## Step 4: Above-the-Fold Optimization

**The First Screen Rule**: What appears in top-third, left-aligned determines whether deeper engagement occurs.

### Placement Requirements
| Element | Location | Purpose |
|---------|----------|---------|
| Name | Top center | Anchor point |
| Current title | Immediately below name | Pattern-match to role |
| Top 3-5 keywords | Summary section | ATS + human scan |
| Strongest achievement | First bullet of current role | Anchoring effect |
| Second strongest | Second bullet OR summary highlight | Reinforcement |

### Achievement Promotion Rules
If strongest achievements are from older roles:
- Option A: Promote to summary as "Career Highlights"
- Option B: Add "Key Achievement" callout in summary
- Option C: Restructure current role to demonstrate continued excellence

**Verify**: Can recruiter see qualification evidence within 7 seconds?

## Step 5: Generate with Authenticity

### Apply CAR Framework
See `references/achievement-frameworks.md` for full guidance.

```
[Action verb] [specific what] to address [challenge], resulting in [quantified outcome]
```

### Authenticity Requirements

**AVOID these AI-detection patterns:**
- Consecutive buzzwords ("spearheaded... orchestrated... leveraged...")
- Same verb starting 3+ bullets
- All round numbers (50%, 25%, 100%)
- Generic phrases without specificity

**INCLUDE these authenticity markers:**
- At least one non-round metric (47.3%, $892K, 23-27%)
- Named projects, tools, or systems
- Exact team sizes when known
- Varied sentence structures

### Factual Integrity (MANDATORY)

All data from XML source files is treated as immutable fact. Wording may be adjusted for flow and keyword optimization, but the underlying facts must not change.

**Protected Facts (NEVER modify):**

| Element | Rule |
|---------|------|
| Job titles | Use exact title from XML—no "equivalents" |
| Company names | Exact spelling from XML |
| Dates | Exact MM/YYYY from XML |
| Metrics/results | Numbers must match XML exactly |
| Team sizes | Exact counts from XML |
| Project/product names | Verbatim from XML |
| Scope descriptors | "enterprise-wide", "global" etc. only if in XML |

**Allowed Modifications:**

- Verb substitution (same meaning, different word)
- Sentence structure variation
- Condensing (omit details, but don't change remaining facts)
- Keyword insertion (add context, don't alter facts)

**Prohibited:**

- Inflating metrics (47% → 50%)
- Expanding scope ("team" → "cross-functional organization")
- Adding responsibilities not in XML
- Creating achievements not documented
- Rounding for readability (keep $892K, don't write $900K)

**Excluded from Resume (interview prep only):**

- `<departure-context>` elements — NEVER include departure reasons on resume
- `<vulnerability>` elements — for interview preparation only
- `<reframe>` elements — for interview preparation only
- Any explanation of why a role ended

### Precision Metrics Rules
| Type | Format | Example |
|------|--------|---------|
| Percentages | One decimal when accurate | 47.3% improvement |
| Currency <$1M | Exact | $892K savings |
| Currency >$1M | Nearest $0.1M | $2.4M revenue |
| Ranges | When genuinely uncertain | 15-22% across regions |

**Rule**: Only use precise metrics you can defend in interview.

## Step 6: Quality Verification

### Knockout Re-Check
- [ ] Zero typos (spell-check + read aloud)
- [ ] Zero grammatical errors
- [ ] Consistent date formatting (MM/YYYY)
- [ ] All claims verifiable if asked
- [ ] No orphan bullets

### Authenticity Audit
- [ ] Power verbs vary (no verb used >2 times)
- [ ] At least one non-round metric present
- [ ] At least one named project/tool/system
- [ ] No 3+ consecutive bullets with identical structure

### Above-the-Fold Check
- [ ] Current title visible in first screen
- [ ] Top 3 keywords visible in first screen
- [ ] Strongest achievement visible in first screen

### Parsing Confidence
- [ ] Single-column layout
- [ ] Standard section headers
- [ ] No tables, graphics, or text boxes
- [ ] Dates in parseable format

### Source Validation (MANDATORY)

Before generating final output, validate ALL facts against XML source files:

**Validation Checklist:**

- [ ] Each job title matches `<title>` element exactly
- [ ] Each company name matches `<company>` element exactly
- [ ] Each date range matches `<start>` and `<end>` elements exactly
- [ ] Each metric matches value in `<result>` element exactly
- [ ] Each team size matches count in source activity
- [ ] Each project/product name matches `<activity>` or `<initiative>` elements

**Validation Process:**

1. For each Experience entry, identify source `<position>` by matching company + date range
2. For each bullet, identify source `<activity>` by ID or content match
3. Verify all numerical claims trace to XML `<result>` elements
4. Flag any claim without XML source attribution

**If validation fails:** Do NOT generate output. List discrepancies and request correction.

## Step 7: Produce Output

### File Output
Save as `resume-[company]-[role].md` in `/mnt/user-data/outputs/`

### Markdown Structure
```markdown
# [Full Name]
[Email] | [Phone] | [Location] | [LinkedIn URL]

---

## Professional Summary
[3-5 lines: specific identity + top achievements + value proposition for THIS role]
[Include top 5 JD keywords naturally]

---

## Professional Experience

**[Job Title]** | [Company Name] | [Location]
*[MM/YYYY] – [MM/YYYY or Present]*

- [Strongest achievement—quantified, specific]
- [Second achievement—different verb, different structure]
- [Third achievement—demonstrates another JD requirement]

[Repeat for relevant roles]

---

## Skills
**[Category aligned to JD]:** [Skill 1], [Skill 2], [Skill 3]
**[Second category]:** [Skill 1], [Skill 2], [Skill 3]

---

## Education
**[Degree]** | [Institution] | [Year]
[Certifications if relevant to role]
```

### Tailoring Summary (in conversation, not resume)

Provide:
1. **Keywords incorporated**: List with placement locations
2. **Requirements matched**: Each requirement → supporting achievement
3. **Coverage gaps**: Requirements without strong evidence
4. **Authenticity score**: Count of specificity markers
5. **LinkedIn consistency alert**: Flag any resume/LinkedIn divergence risk
6. **Source attribution**: For each bullet, note the XML activity ID it derives from

```
⚠️ LinkedIn Consistency Check:
Ensure your LinkedIn reflects [specific elements] before applying.
Recruiters cross-check—discrepancies trigger investigation.
```

### Excitement Assessment
Rate candidate's "excitement potential" for this role:
- **High**: Multiple quantified wins visible in 7-second scan, unexpected specificity
- **Medium**: Meets requirements, lacks standout evidence
- **Low**: Gaps in hard requirements, may land in "maybe pile"

If LOW, explicitly flag: "Candidacy may be weak regardless of optimization. Consider: [specific strengthening recommendations]"

## Reference Files

Load as needed:
- `references/context-profiles.md` — Weight calibration by seniority/function/company
- `references/achievement-frameworks.md` — CAR framework, power verbs, quantification, soft skill inference
- `references/ats-optimization.md` — Keyword placement, formatting, parsing rules
