---
name: grant-application-setup
description: Expert guidance for setting up and organising research grant applications following established patterns for UKRI, EU, and other funding bodies
---

# Grant Application Setup

Use this skill when creating new grant application repositories, organising proposal documents, or setting up collaborative grant writing workflows.

## Project Structure

Standard grant application repository:

```
grant-name/
├── .claude/                    # Claude Code config (optional)
├── .gitignore
├── CLAUDE.md                   # Claude instructions
├── README.md                   # Overview, timeline, collaborators
├── coapplicant_details/        # Co-applicant information
│   ├── coapplicant1.md
│   └── coapplicant2.md
├── correspondence/             # Email correspondence, queries
├── data/                       # Planning data
│   ├── milestones.csv          # Milestone tracking
│   └── plan.csv                # Work package timeline
├── docs/                       # Call documentation, guidance
│   └── call-specification.pdf
├── submission/                 # Main submission documents
│   ├── application.qmd         # Full application
│   ├── research_vision.qmd     # Research vision/summary
│   ├── approach.qmd            # Technical approach
│   ├── team_capability.qmd     # Team and capability
│   ├── references.bib          # Bibliography
│   ├── schematics/             # Figures and diagrams
│   └── cell-numeric.csl        # Citation style
└── slides/                     # Presentation materials (optional)
```

## Document Templates

### README.md

```markdown
# [Grant Title]

[Brief description of the grant application]

## Timeline

| Date | Milestone |
|------|-----------|
| [Date] | Collaborator list agreed |
| [Date] | Case for support drafted |
| [Date] | All sections complete |
| [Date] | Final submission deadline |

## Collaborators

| Name | Institution | Role |
|------|-------------|------|
| PI Name | Institution | Lead applicant |
| Co-I Name | Institution | [Work package/expertise] |

## Structure

- `/submission/`: Main application documents
- `/docs/`: Call documentation and guidance
- `/coapplicant_details/`: Co-applicant information
- `/data/`: Planning data (milestones, timeline)
```

### CLAUDE.md Template

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

This repository contains a [FUNDER] grant application focused on [TOPIC].
The project aims to [BRIEF OBJECTIVE].

## Document Structure

- `/submission/`: Main application documents
- `/docs/`: Call documentation and guidance
- `/coapplicant_details/`: Co-applicant information
- `/data/`: Planning data (milestones, timeline)

## Language Requirements

Always respond in British English (UK).

## Word Count Utilities

```bash
# Count words in a QMD file (excluding YAML header and references)
cat submission/document.qmd | sed '1,4d' | sed '/# References/,$d' | sed 's/\[@[^]]*\]//g' > temp.txt && wc -w temp.txt && rm temp.txt
```

## Working with Citations

- Reference files are stored in `submission/references.bib`
- Use `@placeholder` for unavailable references (never invent citations)
- Format: `[@author2024]` or `[@author2024;@author2025]` for multiple

## Preferred Text Style

[Include example text in preferred style]
```

### .gitignore

```
.DS_Store
*.pdf
!submission/*.pdf
*.html
*_files/
temp*.txt
.Rhistory
```

## Quarto Document Setup

### Application Document Header

```yaml
---
title: "Application Title"
format:
  pdf:
    documentclass: article
    geometry:
      - margin=2.5cm
    fontsize: 11pt
    include-in-header:
      - text: |
          \usepackage{fancyhdr}
          \pagestyle{fancy}
bibliography: references.bib
csl: cell-numeric.csl
---
```

### Research Vision Header

```yaml
---
title: "Research Vision"
format:
  pdf:
    documentclass: article
    geometry:
      - margin=2.5cm
    fontsize: 11pt
bibliography: references.bib
csl: cell-numeric.csl
---
```

## Planning Data Templates

### milestones.csv

```csv
milestone_id,work_package,description,month,type,deliverable
M1,WP1,Initial framework design complete,6,S,Software prototype
M2,WP1,Core module implementation,12,S,Release v1.0
M3,WP2,First training workshop,12,T,Workshop materials
M4,WP3,Methods paper submitted,18,P,Publication
```

Types:
- S = Software
- P = Publication
- T = Training
- W = Workshop
- D = Data release

### plan.csv

```csv
activity_id,work_package,activity,lead,start_month,end_month,dependencies
A1.1,WP1,Literature review,PI,1,3,
A1.2,WP1,Framework design,PI,3,6,A1.1
A2.1,WP2,Training materials,Co-I,6,12,A1.2
```

## Word Count Management

Grant applications have strict word limits. Track counts regularly:

```bash
# Basic word count
wc -w submission/document.qmd

# Accurate count (excludes YAML header, references section, citations)
cat submission/document.qmd | \
  sed '1,/^---$/d' | \
  sed '/^---$/,$d' | \
  sed '/# References/,$d' | \
  sed 's/\[@[^]]*\]//g' | \
  wc -w
```

## Writing Style

### Principles

- Simple, direct prose without unnecessary adjectives
- One sentence per line in markdown
- UK English spelling
- Max 80 characters per line
- Use `@placeholder` for missing citations

### Example Style

```markdown
Recent outbreaks of Ebola, COVID-19 and mpox have demonstrated the value of
modelling for synthesising data for rapid evidence to inform decision making.
Methods used to synthesise available data in real time broadly fall into two
classes: either combining results from multiple, smaller models calibrated in
isolation (the _pipeline approach_, e.g., [@huisman2022]), or representing a
single model tuned to the specific scenario (the _joint model_ approach,
e.g., [@birrell2024;@Watson2024-vj]).
```

## Funder-Specific Patterns

### UKRI

- Case for support (main technical content)
- Research vision summary
- Team capability (track record)
- Pathways to impact
- Data management plan
- Justification of resources

### EU Horizon

- Excellence (scientific quality)
- Impact (wider benefits)
- Implementation (work plan)
- Work packages with deliverables
- Gantt chart timeline
- Consortium description

## Collaboration Workflows

### Co-applicant Information

Store in `coapplicant_details/`:

```markdown
# [Name]

## Affiliation
[Institution, Department]

## Role in Project
[Specific responsibilities, work packages]

## Track Record
[Key achievements relevant to the grant]

## Contribution
[What they bring to the project]
```

### Version Control

- Use branches for major revisions
- Tag versions at key milestones
- Keep submission PDFs in repository for reference

## When to Use This Skill

Activate when:
- Creating a new grant application repository
- Organising proposal documents
- Setting up collaborative writing workflows
- Managing word counts and document structure
- Preparing submission materials

For compliance checking against existing grants, see the **grant-compliance-checking** skill.
