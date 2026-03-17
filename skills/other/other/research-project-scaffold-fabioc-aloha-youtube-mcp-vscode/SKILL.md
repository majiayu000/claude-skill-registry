---
name: "Research Project Scaffold"
description: "Scaffolding academic research projects and refactoring existing ones for Alex-assisted workflows"
---

# Research Project Scaffold Skill

> Scaffolding new academic research projects and refactoring existing ones for Alex-assisted workflows.

## Purpose

Provide standardized structures and refactoring procedures for academic research projects that maximize Alex's ability to assist throughout the research lifecycle.

---

## Scaffolding New Projects

### Recommended Folder Structure

```
project-root/
├── .github/
│   ├── copilot-instructions.md    # Research-specific Alex context
│   └── prompts/
│       └── literature-synthesis.prompt.md
├── docs/
│   ├── RESEARCH-PLAN.md           # Objectives, timeline, milestones
│   ├── METHODOLOGY.md             # Research design decisions
│   └── DECISION-LOG.md            # Key decisions with rationale
├── data/
│   ├── raw/                       # Untouched source data
│   ├── processed/                 # Cleaned/transformed data
│   └── DATA-DICTIONARY.md         # Variable definitions
├── analysis/
│   ├── scripts/                   # Analysis code
│   ├── outputs/                   # Generated figures, tables
│   └── notebooks/                 # Exploratory analysis
├── writing/
│   ├── drafts/                    # Work in progress
│   ├── figures/                   # Publication-ready figures
│   └── submissions/               # Submitted versions
├── references/
│   ├── LITERATURE-MATRIX.md       # Systematic literature tracking
│   ├── pdfs/                      # Source papers (if permitted)
│   └── notes/                     # Reading notes
└── README.md                      # Project overview
```

### Essential Files

#### RESEARCH-PLAN.md Template

```markdown
# Research Plan: [Title]

## Research Questions
1. Primary: [Main question]
2. Secondary: [Supporting questions]

## Methodology
- Type: [Qualitative/Quantitative/Mixed/Case Study]
- Design: [Experimental/Survey/Longitudinal/etc.]
- Participants: [Sample description]

## Timeline
| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Literature Review | Weeks 1-4 | LITERATURE-MATRIX.md complete |
| Data Collection | Weeks 5-12 | Raw data in data/raw/ |
| Analysis | Weeks 13-16 | Results in analysis/outputs/ |
| Writing | Weeks 17-20 | Draft in writing/drafts/ |
| Revision | Weeks 21-24 | Submission-ready manuscript |

## Success Criteria
- [ ] [Specific measurable outcome]
- [ ] [Publication target]
- [ ] [Other goals]

## Risks & Mitigations
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| [Risk 1] | Medium | [Plan] |
```

#### LITERATURE-MATRIX.md Template

```markdown
# Literature Matrix

## Search Strategy
- Databases: [List sources]
- Keywords: [Search terms]
- Inclusion criteria: [What qualifies]
- Exclusion criteria: [What's out]

## Matrix

| Citation | Year | Methodology | Key Findings | Gaps | Relevance | Notes |
|----------|------|-------------|--------------|------|-----------|-------|
| Author1 et al. | 2024 | Controlled study | Finding X | Gap Y | ⭐⭐⭐ | Foundational |
| Author2 | 2023 | Survey (n=500) | Finding Z | — | ⭐⭐ | Supports H2 |

## Synthesis Notes
- Theme 1: [Pattern across sources]
- Theme 2: [Another pattern]
- Gap: [What's missing that your research addresses]
```

#### METHODOLOGY.md Template

```markdown
# Methodology

## Research Design
**Approach**: [Paradigm - positivist, interpretivist, pragmatic]
**Strategy**: [Case study, experiment, survey, ethnography, etc.]

## Data Collection
**Sources**: [What data, from where]
**Instruments**: [Surveys, interviews, logs, artifacts]
**Procedure**: [Step-by-step process]

## Analysis Method
**Technique**: [Thematic analysis, statistical tests, content analysis]
**Tools**: [Software, frameworks]
**Validation**: [Member checking, triangulation, statistical power]

## Ethical Considerations
- IRB Status: [Approved/Exempt/N/A]
- Consent: [Process]
- Data protection: [How handled]

## Limitations
1. [Known limitation and why acceptable]
2. [Another limitation]
```

#### copilot-instructions.md Template (Research Projects)

```markdown
# [Project Title] - Research Context

## Project Overview
[2-3 sentence summary of research focus and goals]

## Current Phase
- [x] Literature Review
- [ ] Data Collection  
- [ ] Analysis
- [ ] Writing

## Key Files
- Research plan: docs/RESEARCH-PLAN.md
- Literature: references/LITERATURE-MATRIX.md
- Methodology: docs/METHODOLOGY.md

## Alex Guidance
- When reviewing literature: Add entries to LITERATURE-MATRIX.md
- When analyzing data: Document steps in DECISION-LOG.md
- When writing: Check references against LITERATURE-MATRIX.md
- Citation style: [APA 7 / Chicago / IEEE / etc.]

## Domain Context
[Key concepts, terminology, or background Alex needs]

## Quality Standards
- All claims require citations or data references
- Methodology decisions logged with rationale
- Raw data never modified (work from processed/)
```

---

## Refactoring Existing Projects

### Assessment Checklist

Run this audit on any existing research project:

```markdown
## Research Project Audit

### Structure Assessment
- [ ] Has dedicated .github/ folder with copilot-instructions.md
- [ ] Data separated: raw vs processed
- [ ] Clear separation: analysis code vs writing
- [ ] References organized and tracked

### Documentation Assessment  
- [ ] Research questions documented
- [ ] Methodology decisions recorded
- [ ] Literature systematically tracked (not scattered notes)
- [ ] Decision rationale captured

### Alex-Readiness Assessment
- [ ] Context file exists (copilot-instructions.md or equivalent)
- [ ] Current phase clearly marked
- [ ] Key terminology defined
- [ ] Citation style specified

### Data Management Assessment
- [ ] Raw data preserved unchanged
- [ ] Data dictionary exists
- [ ] Analysis reproducible
- [ ] Sensitive data protected
```

### Refactoring Procedure

#### Phase 1: Inventory (Non-Destructive)

1. **Create inventory file**:
   ```markdown
   # Refactoring Inventory - [Project Name]
   
   ## Current Structure
   [Tree output of existing folders]
   
   ## Identified Files by Type
   ### Writing/Drafts
   - file1.docx - [description]
   
   ### Data
   - dataset.csv - [raw/processed?]
   
   ### Analysis
   - script.py - [purpose]
   
   ### References
   - [scattered papers, notes]
   
   ### Unknown/Misc
   - [files needing classification]
   ```

2. **Identify gaps**:
   - Missing: RESEARCH-PLAN? METHODOLOGY? LITERATURE-MATRIX?
   - Undocumented: Key decisions made but not recorded?
   - Scattered: References in multiple locations?

#### Phase 2: Scaffold Creation

1. Create target structure (empty folders):
   ```
   mkdir .github docs data data/raw data/processed analysis writing references
   ```

2. Create missing essential files:
   - RESEARCH-PLAN.md (even if retrospective)
   - METHODOLOGY.md
   - LITERATURE-MATRIX.md
   - copilot-instructions.md

3. Populate retrospectively:
   - Extract research questions from drafts
   - Document methodology from what was done
   - Build literature matrix from existing citations

#### Phase 3: File Migration

**Principle**: Move, don't copy (avoid duplicates). Use git.

```bash
# Example migration commands
git mv old-data.csv data/raw/
git mv cleaned-data.csv data/processed/
git mv draft-v3.docx writing/drafts/
git mv analysis.py analysis/scripts/
```

**Migration mapping template**:

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `data.csv` | `data/raw/original-data.csv` | Rename + move |
| `data_cleaned.csv` | `data/processed/data-cleaned.csv` | Move |
| `paper.docx` | `writing/drafts/paper-v1.docx` | Version + move |
| `notes.txt` | `references/notes/reading-notes.md` | Convert + move |

#### Phase 4: Retroactive Documentation

Fill in documentation from what exists:

1. **RESEARCH-PLAN.md**: Extract from proposal, drafts, or reconstruct
2. **DECISION-LOG.md**: Interview yourself about choices made
3. **LITERATURE-MATRIX.md**: Build from reference list in drafts
4. **DATA-DICTIONARY.md**: Document variables from analysis code

**Retroactive documentation prompts**:
- "What was I trying to answer?"
- "Why did I choose this method over alternatives?"
- "What did Author X contribute to my thinking?"
- "What does this variable actually represent?"

#### Phase 5: Link Updates

1. Update any internal links in documents
2. Update file paths in analysis scripts
3. Update .gitignore for new structure
4. Update any build/compile scripts

#### Phase 6: Validation

- [ ] All files accounted for (nothing lost)
- [ ] Analysis scripts run from new locations
- [ ] Links in documents work
- [ ] Git history preserved (used mv, not delete+create)
- [ ] README.md updated with new structure

---

## Best Practices

### By Research Phase

| Phase | Alex Integration | Key Actions |
|-------|------------------|-------------|
| **Planning** | Research design consultation | Create RESEARCH-PLAN.md, set up structure |
| **Literature** | Summarization, gap analysis | Build LITERATURE-MATRIX.md systematically |
| **Data Collection** | Instrument review, protocol checking | Document in METHODOLOGY.md |
| **Analysis** | Code review, interpretation checking | Log decisions, version scripts |
| **Writing** | Drafting, citation checking, editing | Use references/ for fact-checking |
| **Revision** | Peer review response, formatting | Track versions in writing/submissions/ |

### Common Refactoring Patterns

| Smell | Refactoring |
|-------|-------------|
| All files in root | Create folder hierarchy |
| Data mixed with analysis | Separate data/raw, data/processed, analysis/ |
| Multiple draft versions scattered | Consolidate in writing/drafts with clear naming |
| References in random locations | Centralize in references/ |
| No context for AI assistance | Create copilot-instructions.md |
| Decisions made but not recorded | Create retrospective DECISION-LOG.md |
| Literature notes disorganized | Build structured LITERATURE-MATRIX.md |

### File Naming Conventions

```
# Data files
data/raw/survey-responses-2024-01-15.csv     # Source + date
data/processed/survey-clean-v2.csv           # Description + version

# Writing
writing/drafts/paper-draft-01.md             # Numbered versions
writing/submissions/journal-name-2024-03.pdf # Venue + date

# Analysis
analysis/scripts/01-data-cleaning.py         # Numbered sequence
analysis/scripts/02-descriptive-stats.py
analysis/outputs/figure-1-demographics.png   # Matches paper reference
```

### Version Control Practices

- Commit at logical checkpoints (completed section, working analysis)
- Use meaningful commit messages: "Add literature synthesis for RQ1"
- Tag important versions: `git tag submission-v1`
- Never commit sensitive data (use .gitignore)

---

## Integration with Other Skills

- **academic-research**: Use for methodology guidance, committee navigation
- **practitioner-research**: Use for publication workflows (Ship→Document→Promote)
- **project-scaffolding**: Base patterns for folder structure
- **bootstrap-learning**: For learning new research methods
- **writing-publication**: For manuscript preparation

---

## Clinical Research Extension

*Patterns from Lithium Alzheimer's prevention research project (Feb 2026)*

### Clinical Research Folder Structure

```
project-root/
├── .github/
│   └── copilot-instructions.md
├── clinical/
│   ├── IRB-PROTOCOL.md           # Full IRB submission document
│   ├── IRB-SELECTION-GUIDE.md    # IRB comparison if no internal IRB
│   ├── INFORMED-CONSENT.md       # English consent form
│   ├── INFORMED-CONSENT-ES.md    # Spanish translation
│   ├── INFORMED-CONSENT-PT.md    # Portuguese translation
│   ├── CASE-REPORT-FORMS.md      # Data collection instruments
│   ├── SCREENING-CHECKLIST.md    # Eligibility criteria forms
│   ├── FUNDING-STRATEGY.md       # Grant/funding applications
│   └── MASTER-CHECKLIST.md       # Project-wide task tracker
├── literature/
│   ├── LITERATURE-MATRIX.md      # Systematic evidence tracking
│   ├── PRIMARY-SOURCES.md        # Key papers with PMIDs
│   ├── CLINICAL-TRIALS.md        # Existing trial summaries
│   └── EPIDEMIOLOGICAL-STUDIES.md # Population-level evidence
├── research/
│   └── RESEARCH-PROTOCOL.md      # Scientific methodology
├── analysis/
│   ├── EVIDENCE-SYNTHESIS.md     # Meta-analysis results
│   └── HYPOTHESIS-EVALUATION.md  # Systematic claim validation
├── docs/
│   ├── EXECUTIVE-SUMMARY.md      # Leadership/stakeholder brief
│   ├── CLINICAL-IMPLICATIONS.md  # Provider guidance
│   ├── STUDY-GOALS.md            # Research objectives
│   └── FUTURE-RESEARCH.md        # Next steps, Phase 2+
└── README.md                     # 3-minute pitch + overview
```

### IRB Protocol Template Sections

1. **Protocol Information** — Title, version, sponsor, IND status
2. **Principal Investigators** — Names, credentials, roles, contacts
3. **Study Synopsis** — Background, rationale, objectives, design
4. **Study Population** — Inclusion/exclusion criteria with rationale
5. **Study Intervention** — What is being tested, dosing, duration
6. **Study Procedures** — Visit schedule, assessments, data collection
7. **Safety Monitoring** — Adverse event definitions, reporting, stopping rules
8. **Data Management** — Collection, storage, HIPAA compliance
9. **Statistical Analysis** — Power calculation, analysis plan
10. **Ethical Considerations** — Risk/benefit, consent process, vulnerable populations

### Inclusion/Exclusion Criteria Pattern

```markdown
### Inclusion Criteria
1. Age ≥ [minimum] years
2. [Clinical condition or symptom]
3. [Baseline test values] (e.g., eGFR > 60)
4. Ability to provide informed consent
5. Willing to comply with study procedures

### Exclusion Criteria
1. **Organ impairment**: [specific threshold]
2. **Current medication use**: [contraindicated drugs]
3. **Comorbid conditions**: [list with rationale]
4. **Concurrent medications** due to interaction risk:
   - [Drug class 1] (rationale)
   - [Drug class 2] (rationale)
5. **Pregnancy or planning pregnancy**
6. **Life expectancy < [study duration]**
```

### External IRB Selection (Non-Academic Settings)

| IRB | Cost Range | Timeline | Best For |
|-----|------------|----------|----------|
| **Sterling IRB** | $1,500-3,000 | 2-3 weeks | Supplement studies |
| **Solutions IRB** | $1,000-2,500 | 2-3 weeks | Budget-conscious |
| **Advarra** | $2,000-4,000 | 2-4 weeks | Academic spinoffs |
| **WCG IRB** | $2,500-5,000 | 2-4 weeks | Large commercial |

**Budget**: Add $2,000-3,000 for IRB fees + 4-6 weeks to timeline.

### Evidence Confidence Levels

| Level | Meaning | Basis |
|-------|---------|-------|
| **HIGH** | Strong consensus | Multiple RCTs, mechanisms confirmed |
| **MODERATE** | Promising | Animal studies, small human trials |
| **LOW** | Emerging | Case reports, theoretical basis only |
| **INSUFFICIENT** | Unknown | No quality evidence available |

### Stakeholder Materials

- **README.md** — 3-minute pitch for decision-makers
- **EXECUTIVE-SUMMARY.md** — 1-page BLUF for busy executives
- **CLINICAL-IMPLICATIONS.md** — Provider-focused guidance

### Clinical Research Localization

For multi-language studies, maintain parallel informed consent documents. Use standard suffixes:

| Language | Suffix | Example |
|----------|--------|---------|
| English | (none) | INFORMED-CONSENT.md |
| Spanish | -ES | INFORMED-CONSENT-ES.md |
| Portuguese | -PT | INFORMED-CONSENT-PT.md |
| Chinese | -ZH | INFORMED-CONSENT-ZH.md |

---

## Quick Commands

```
# New project setup
mkdir -p .github/prompts docs data/{raw,processed} analysis/{scripts,outputs} writing/{drafts,figures} references/notes
touch docs/RESEARCH-PLAN.md docs/METHODOLOGY.md docs/DECISION-LOG.md references/LITERATURE-MATRIX.md .github/copilot-instructions.md README.md

# Audit existing project
find . -type f -name "*.md" -o -name "*.csv" -o -name "*.py" | head -50

# Migration with git tracking
git mv source destination
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Project too messy to audit | Start with just essential files, refactor incrementally |
| Lost track of versions | Use git log, create retrospective changelog |
| Data too sensitive for repo | Use .gitignore, document in DATA-DICTIONARY.md what exists |
| Analysis scripts break after move | Update relative paths, consider using project root as working directory |
| Can't remember decisions | Check email, drafts, commit messages for clues |

---

*This skill makes research projects Alex-ready from day one, or gets them there through systematic refactoring.*
