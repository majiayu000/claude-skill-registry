---
name: "Literature Review"
description: "Systematic literature search, synthesis, gap identification, and narrative construction for academic research"
---

# Skill: Literature Review

> Systematic literature search, synthesis, gap identification, and narrative construction for academic research.

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | literature-review |
| **Version** | 1.0.0 |
| **Category** | Research |
| **Difficulty** | Advanced |
| **Prerequisites** | None |
| **Related Skills** | academic-paper-drafting, citation-management, dissertation-defense |

---

## Overview

Literature review is foundational to academic research. This skill provides structured workflows for systematic searching, critical synthesis, and gap identification—transforming scattered sources into coherent scholarly narratives.

### Core Competencies

1. **Systematic Search** - Reproducible, comprehensive search strategies
2. **Critical Appraisal** - Quality assessment of sources
3. **Synthesis** - Thematic integration across sources
4. **Gap Identification** - Locating research opportunities
5. **Narrative Construction** - Weaving sources into argument

---

## Module 1: Systematic Search Strategy

### The PICO(S) Framework

For empirical research questions:

| Element | Description | Example (AIRS) |
|---------|-------------|----------------|
| **P**opulation | Who is studied | Knowledge workers, AI users |
| **I**ntervention | What is applied | AI-powered tools, copilots |
| **C**omparison | Alternative | Traditional tools, no AI |
| **O**utcome | What is measured | Adoption intention, behavioral intention |
| **S**tudy type | Research design | Quantitative survey, SEM |

### Database Selection

| Database | Best For | Coverage |
|----------|----------|----------|
| **Google Scholar** | Broad discovery, citation tracking | All disciplines |
| **Web of Science** | High-impact journals, citation analysis | STEM, social sciences |
| **Scopus** | Comprehensive coverage, author metrics | Multidisciplinary |
| **ACM Digital Library** | Computer science, HCI | CS, CHI proceedings |
| **PsycINFO** | Psychology, behavioral research | Psychology, social sciences |
| **SSRN** | Working papers, preprints | Business, economics, law |

### Search String Construction

**Boolean operators:**
```
("artificial intelligence" OR "AI" OR "machine learning")
AND
("adoption" OR "acceptance" OR "intention")
AND
("UTAUT" OR "TAM" OR "technology acceptance")
```

**Truncation and wildcards:**
- `adopt*` → adoption, adopting, adopter
- `behavio?r` → behavior, behaviour

### Search Protocol Template

```markdown
## Search Protocol

**Research Question**: [Your RQ]
**Date Conducted**: [Date]
**Databases Searched**: [List]

### Search Terms
- Primary: [terms]
- Secondary: [terms]
- Exclusions: [terms with NOT]

### Inclusion Criteria
- Published: [date range]
- Language: [languages]
- Study type: [empirical, theoretical, etc.]
- Peer-reviewed: [yes/no]

### Exclusion Criteria
- [List exclusions]

### Results
| Database | Initial Hits | After Dedup | After Title Screen | After Abstract Screen | Final |
|----------|--------------|-------------|--------------------|-----------------------|-------|
```

---

## Module 2: Source Management

### The Funnel Process

```
Initial Search Results (hundreds)
        ↓ Title screening
Potentially Relevant (~50-100)
        ↓ Abstract screening
Candidates for Full-Text (~30-50)
        ↓ Full-text review
Included Sources (~15-30)
        ↓ Backward/forward citation
Final Corpus (~20-40)
```

### Screening Criteria

**Quick reject (title/abstract):**
- Wrong population
- Wrong intervention
- Wrong outcome
- Non-empirical (if seeking empirical)
- Wrong language
- Duplicate

**Full-text assessment:**
- Methodological rigor
- Relevance to research question
- Contribution to synthesis

### Citation Tracking

**Backward citation** (reference mining):
- Review reference lists of key papers
- Find foundational works
- Identify theoretical ancestry

**Forward citation** (cited by):
- Use Google Scholar "Cited by"
- Find recent developments
- Identify methodological improvements

---

## Module 3: Critical Appraisal

### Quality Assessment Dimensions

| Dimension | Questions |
|-----------|-----------|
| **Validity** | Are findings believable? Methods appropriate? |
| **Reliability** | Would study replicate? Measures consistent? |
| **Generalizability** | To what populations/contexts? |
| **Rigor** | Adequate sample? Controls? Analysis? |
| **Transparency** | Can methods be reproduced? |

### Study Type Checklists

**Quantitative survey studies:**
- [ ] Sample size adequate (power analysis?)
- [ ] Response rate reported
- [ ] Validated instruments used
- [ ] Reliability reported (Cronbach's α)
- [ ] Common method bias addressed
- [ ] Appropriate statistical analysis

**Qualitative studies:**
- [ ] Sampling strategy justified
- [ ] Data saturation discussed
- [ ] Researcher positionality stated
- [ ] Coding process transparent
- [ ] Member checking or triangulation

**SEM/CFA studies:**
- [ ] Model fit indices reported (CFI, RMSEA, SRMR)
- [ ] Convergent validity (AVE ≥ .50)
- [ ] Discriminant validity (HTMT < .85)
- [ ] Sample size adequate (N ≥ 200 preferred)

---

## Module 4: Synthesis Strategies

### Thematic Synthesis

1. **Code individual sources** - Key concepts, findings, methods
2. **Group codes into themes** - Patterns across sources
3. **Develop analytical narrative** - What themes mean together

**Example themes for AIRS research:**
- Trust and reliance
- Value perception
- Effort-benefit trade-offs
- Social and organizational factors

### Comparative Matrix

| Source | Theory | Method | Sample | Key Finding | Limitation |
|--------|--------|--------|--------|-------------|------------|
| Author1 (Year) | TAM | Survey | N=312 | PE→BI significant | Cross-sectional |
| Author2 (Year) | UTAUT2 | SEM | N=523 | PV strongest | Self-report |

### Theoretical Integration

**Identifying theoretical tensions:**
- Where do theories contradict?
- What boundary conditions apply?
- How can conflicts be resolved?

**Building theoretical contribution:**
- What's missing from current theories?
- How does your work extend understanding?
- What new constructs are needed?

---

## Module 5: Gap Identification

### Types of Research Gaps

| Gap Type | Description | Signal Phrases |
|----------|-------------|----------------|
| **Empirical** | Untested relationships | "No study has examined..." |
| **Theoretical** | Missing constructs or mechanisms | "Theory does not account for..." |
| **Methodological** | Better methods needed | "Prior studies relied on..." |
| **Contextual** | Untested populations/settings | "Research in [context] is lacking..." |
| **Temporal** | Outdated findings | "Since [year], technology has changed..." |

### Gap Articulation Template

```markdown
## Research Gap

**What we know**: [Summary of existing knowledge]

**What we don't know**: [The gap]

**Why it matters**: [Significance of filling gap]

**How this study addresses it**: [Your contribution]
```

---

## Module 6: Writing the Literature Review

### Structure Options

**Chronological:**
- Best for: Tracing evolution of a concept
- Risk: Can become mere historical summary

**Thematic:**
- Best for: Synthesizing diverse perspectives
- Risk: May obscure temporal development

**Methodological:**
- Best for: Evaluating research approaches
- Risk: Can be dry, less engaging

**Theoretical:**
- Best for: Comparing frameworks
- Risk: Requires deep theory knowledge

### The Funnel Structure

```
Broad context (the problem space)
    ↓
Theoretical foundations (key theories)
    ↓
Prior empirical work (what's been studied)
    ↓
Gap and contribution (what's missing → your work)
```

### Synthesis vs. Summary

❌ **Summary** (weak):
> "Smith (2020) found X. Jones (2021) found Y. Brown (2022) found Z."

✅ **Synthesis** (strong):
> "While early studies emphasized X (Smith, 2020), subsequent research revealed the moderating role of Y (Jones, 2021), leading to more nuanced frameworks that integrate both factors (Brown, 2022)."

### Transition Phrases for Synthesis

| Purpose | Phrases |
|---------|---------|
| Agreement | "Consistent with...", "Similarly...", "Extending this..." |
| Contrast | "However...", "In contrast...", "Alternatively..." |
| Extension | "Building on...", "Taking this further...", "Integrating..." |
| Gap signal | "Yet...", "Nevertheless...", "What remains unclear..." |

---

## Quick Reference

### Literature Review Checklist

- [ ] Search strategy documented and reproducible
- [ ] Multiple databases searched
- [ ] Inclusion/exclusion criteria explicit
- [ ] Backward and forward citation completed
- [ ] Sources critically appraised
- [ ] Themes identified across sources
- [ ] Gaps clearly articulated
- [ ] Synthesis (not just summary)
- [ ] Clear link to research questions

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too narrow search | Use multiple databases, synonyms |
| Uncritical acceptance | Apply quality assessment |
| Descriptive only | Focus on synthesis and analysis |
| No clear gap | Explicitly state what's missing |
| Outdated sources | Include recent (last 5 years) work |
| Missing seminal works | Track backward citations |

---

## Activation Patterns

| Trigger | Response |
|---------|----------|
| "literature review", "lit review", "sources" | Full skill activation |
| "search strategy", "database search" | Module 1: Systematic Search |
| "synthesize", "themes", "patterns" | Module 4: Synthesis |
| "research gap", "what's missing" | Module 5: Gap Identification |
| "how to write lit review" | Module 6: Writing |

---

*Skill created: 2026-02-10 | Category: Research | Status: Active*

---

## Synapses

- [.github/skills/citation-management/SKILL.md] (High, Uses, Bidirectional) - "Lit review requires proper citations"
- [.github/skills/academic-paper-drafting/SKILL.md] (High, Feeds, Forward) - "Lit review becomes paper section"
- [.github/instructions/empirical-validation.instructions.md] (Medium, Applies, Forward) - "Evidence-based source evaluation"
