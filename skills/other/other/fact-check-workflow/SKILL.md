---
name: fact-check-workflow
description: Structured workflow for fact-checking claims in journalism. Use when verifying statements for publication, rating claims for fact-check articles, or building pre-publication verification processes. Includes claim extraction, evidence gathering, rating scales, and correction protocols.
---

# Fact-check workflow

Fact-checking is systematic, not intuitive. This skill provides structure for claim verification, evidence documentation, and rating decisions.

## When to use

- Pre-publication fact-checking of articles
- Dedicated fact-check stories (rating claims)
- Verifying source statements during reporting
- Building fact-checking protocols for a newsroom
- Training staff on verification standards

## The fact-check process

```
1. Identify claim → 2. Research claim → 3. Gather evidence →
4. Contact sources → 5. Rate/verify → 6. Document → 7. Publish/correct
```

## Step 1: Claim extraction

### What to check

**Check:**
- Factual assertions ("X happened," "Y is true")
- Statistics and numbers
- Dates and timelines
- Quotes and attributions
- Causal claims ("X caused Y")

**Don't check (opinions):**
- "This policy is good/bad"
- "We should do X"
- Predictions about the future
- Matters of taste or preference

### Claim extraction template

```markdown
## Claim log

**Article/Source:** [where the claim appeared]
**Date:** [when]

### Claim 1
**Statement:** [exact quote or paraphrase]
**Speaker:** [who said it]
**Context:** [surrounding context]
**Type:** [statistic/historical/quote/causal]
**Priority:** [high/medium/low based on importance to story]
**Status:** [pending/verified/false/unverifiable]

### Claim 2
[same structure]
```

### Prioritizing claims

| Priority | Criteria |
|----------|----------|
| **High** | Central to the story's thesis, easily checkable, high consequence if wrong |
| **Medium** | Supporting detail, takes more effort to verify |
| **Low** | Peripheral detail, commonly accepted, minimal consequence |

Check high-priority claims first. Check all claims if time allows.

## Step 2: Research the claim

### Primary sources first

| Claim type | Primary sources |
|------------|-----------------|
| Statistics | Original study, government data, survey methodology |
| Quotes | Audio/video recording, transcript, direct confirmation |
| Historical | Contemporary news accounts, official records |
| Scientific | Peer-reviewed research, expert consensus |
| Legal | Court documents, official filings |
| Financial | SEC filings, audited statements |

### Secondary source evaluation

If you must use secondary sources:
- How close are they to the original?
- Do they cite their sources?
- Do multiple independent sources confirm?
- Is there any contradicting coverage?

### Research documentation template

```markdown
## Research for Claim: [brief description]

### Primary sources checked
| Source | What it says | Confirms/Contradicts |
|--------|--------------|---------------------|
| [source] | [finding] | [confirms/contradicts/partial] |

### Secondary sources checked
| Source | What it says | Reliability |
|--------|--------------|-------------|
| [source] | [finding] | [high/medium/low] |

### Gaps in evidence
- [What you couldn't find]
- [What you still need]
```

## Step 3: Evidence gathering

### Types of evidence

| Evidence type | Strength | Notes |
|---------------|----------|-------|
| Official documents | Strong | Court records, government reports, filings |
| Primary data | Strong | Original datasets, your own analysis |
| Expert consensus | Strong | Multiple independent experts agree |
| On-record sources | Medium | Named source with direct knowledge |
| Contemporary accounts | Medium | News coverage from the time |
| Off-record sources | Weak | Use to guide reporting, not as evidence |
| Social media posts | Weak | Can be deleted, context matters |

### Evidence checklist

```markdown
## Evidence for: [claim]

### Documentary evidence
- [ ] Government records
- [ ] Court documents
- [ ] Corporate filings
- [ ] Published research
- [ ] Official statements/press releases

### Human sources
- [ ] Direct witnesses
- [ ] Subject matter experts
- [ ] Involved parties (on record)
- [ ] Involved parties (for response)

### Data verification
- [ ] Original dataset obtained
- [ ] Methodology reviewed
- [ ] Calculations independently verified
- [ ] Sample size adequate

### Contradicting evidence
- [ ] Searched for conflicting sources
- [ ] Contradictions documented
- [ ] Discrepancies explained
```

## Step 4: Contact sources

### Right of response

**Always contact:**
- People/organizations being fact-checked
- Give specific claims you're checking
- Give reasonable deadline (24-48 hours minimum)
- Document their response (or non-response)

### Source contact template

```markdown
Subject: Request for comment - [Publication] fact-check

Dear [Name],

I'm a [title] at [publication] working on a fact-check of [context].

Specifically, I'm examining this claim:

"[Exact claim being checked]"

I want to give you the opportunity to provide any evidence supporting this claim, clarify the context, or offer any corrections.

My deadline is [date/time]. Please let me know if you need more time.

[Your name]
[Contact info]
```

### Document responses

```markdown
## Source response log

### [Source name]
**Contacted:** [date/time, method]
**Deadline given:** [date/time]
**Response received:** [date/time] / No response
**Summary:** [what they said]
**Evidence provided:** [any documentation]
**Direct quote for publication:** "[quote]"
```

## Step 5: Rating the claim

### Standard rating scales

**Binary (for internal fact-checking):**
- ✅ Verified
- ❌ False
- ⚠️ Unverifiable

**Graduated (for fact-check articles):**

| Rating | Criteria |
|--------|----------|
| **True** | Accurate and complete, nothing significant omitted |
| **Mostly true** | Accurate but needs context or minor clarification |
| **Half true** | Partially accurate but leaves out critical context |
| **Mostly false** | Contains some truth but overall misleading |
| **False** | Not accurate; contradicted by evidence |
| **Pants on fire** | Not accurate AND ridiculous (use sparingly) |

### Rating decision template

```markdown
## Rating decision: [claim]

**Claim:** [exact statement]
**Speaker:** [who said it]
**Our rating:** [rating]

### Evidence supporting the claim
- [Evidence 1]
- [Evidence 2]

### Evidence contradicting the claim
- [Evidence 1]
- [Evidence 2]

### Key context missing from the claim
- [Context 1]
- [Context 2]

### Source response
[What they said when contacted]

### Reasoning
[Explain why this rating, not another]

### Confidence level
[High/Medium/Low and why]
```

## Step 6: Documentation

### The fact-check file

For every claim verified, maintain:

```markdown
## Fact-check record

**Claim:** [exact statement]
**Source:** [who said it, where, when]
**Checked by:** [your name]
**Date checked:** [date]

### Verification
**Rating:** [rating]
**Primary evidence:** [list with links/locations]
**Supporting evidence:** [list]
**Contradicting evidence:** [if any]

### Sources contacted
- [Name]: [response summary]
- [Name]: [no response as of date]

### Notes
[Any additional context, caveats, future considerations]

### Files
- [List of saved documents, screenshots, etc.]
```

### Archiving evidence

- Save screenshots with timestamps (URLs can change)
- Archive web pages (Wayback Machine, Archive.today)
- Download documents (don't just link)
- Keep original files separate from your analysis

## Step 7: Corrections

### When to correct

| Situation | Action |
|-----------|--------|
| Factual error | Correct immediately, note correction |
| Missing context | Add context, may not need formal correction |
| Updated information | Update, note "Updated: [date]" |
| Source disputes characterization | Evaluate claim, correct if warranted |

### Correction template

```markdown
**Correction [date]:** An earlier version of this article stated [incorrect claim].
In fact, [correct information]. We regret the error.
```

### Correction log

```markdown
## Correction record

**Article:** [title/URL]
**Original publication:** [date]
**Error discovered:** [date]
**Error type:** [factual/context/attribution/etc.]

**Original text:**
[what was published]

**Corrected text:**
[what it now says]

**How discovered:**
[reader tip, internal review, source complaint, etc.]

**Correction published:** [date]
**Location:** [in article, separate correction page, both]
```

## Pre-publication checklist

Before any story publishes:

```markdown
## Pre-publication fact-check

**Article:** [title]
**Reporter:** [name]
**Editor:** [name]
**Fact-checker:** [name, if separate]
**Publish date:** [date]

### Claims verified
| Claim | Status | Evidence | Notes |
|-------|--------|----------|-------|
| [claim 1] | ✅ | [source] | |
| [claim 2] | ✅ | [source] | |

### Sources contacted for comment
| Source | Contacted | Response |
|--------|-----------|----------|
| [name] | [date] | [received/no response] |

### Numbers and statistics
- [ ] All statistics sourced
- [ ] Calculations independently verified
- [ ] Context provided (per capita, adjusted for inflation, etc.)

### Quotes
- [ ] All quotes verified against recording/transcript
- [ ] Attribution is accurate
- [ ] Context preserved

### Names and titles
- [ ] All names spelled correctly
- [ ] Titles current and accurate
- [ ] Affiliations verified

### Legal review (if applicable)
- [ ] Defamation risk assessed
- [ ] All claims supported by evidence
- [ ] Response from subjects documented

### Sign-off
**Reporter:** [name, date]
**Editor:** [name, date]
**Fact-checker:** [name, date]
```

## Fact-check article structure

For dedicated fact-check stories:

```markdown
# [Headline: Claim being checked]

**Claim:** [Exact claim in quotes]
**Source:** [Who said it, where, when]
**Our rating:** [Rating with visual indicator]

## What was said
[Context of the claim, full quote, circumstances]

## What the evidence shows
[Present evidence for and against]

## The verdict
[Explanation of rating decision]

## Sources
[List all sources with links]

---
*Published: [date] | Updated: [date if applicable]*
```

---

*Fact-checking isn't about gotchas. It's about accuracy. The goal is truth, not points.*
