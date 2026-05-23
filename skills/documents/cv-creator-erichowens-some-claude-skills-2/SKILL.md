---
name: cv-creator
description: Professional CV and resume builder transforming career narratives into ATS-optimized, multi-format resumes. Integrates with career-biographer for data and competitive-cartographer for positioning. Generates PDF, DOCX, LaTeX, JSON Resume, HTML, and Markdown. Activate on 'resume', 'CV', 'ATS optimization', 'job application'. NOT for cover letters, portfolio websites (use web-design-expert), LinkedIn optimization, or interview preparation.
allowed-tools: Read,Write,Edit,WebFetch,WebSearch
category: Business & Monetization
tags:
  - resume
  - ats
  - career
  - pdf
  - latex
pairs-with:
  - skill: career-biographer
    reason: Get structured career data
  - skill: job-application-optimizer
    reason: Tailor CVs to specific roles
---

# CV Creator

Professional resume builder that transforms structured career data into ATS-optimized, professionally formatted resumes.

## Integrations

Works with: career-biographer, competitive-cartographer, web-design-expert, typography-expert

## Production Implementation Available!

**GitHub**: [github.com/erichowens/cv-creator](https://github.com/erichowens/cv-creator)
- Status: Production-ready (~2,000 LOC)
- ATS Score: 95/100 achieved
- Deploy: `npm install && npm run example`

Built through multi-skill orchestration (8 skills, 9 phases).

## Quick Start

```
User: "Create a resume for senior software engineer roles"

CV Creator:
1. Request CareerProfile (from biographer or direct input)
2. Request PositioningStrategy (from cartographer or skip)
3. Request target role/company (optional)
4. Generate resume with clean formatting
5. Calculate ATS score and provide recommendations
6. Export in requested formats (PDF, DOCX, JSON Resume)
```

**Key principle**: ATS compatibility first, human readability second, visual flair never.

## Core Capabilities

### 1. Multi-Format Generation
| Format | Use Case |
|--------|----------|
| PDF | Email applications, job boards, print |
| DOCX | Recruiter submissions, editable |
| JSON Resume | Developer portfolios, programmatic |
| HTML | Portfolio websites, responsive |
| Markdown | Version control, git-based management |
| LaTeX | Academic CVs (optional) |

### 2. ATS Optimization Engine
- Keyword analysis and matching from job descriptions
- Formatting validation (single-column, standard fonts)
- Scoring system (0-100) with specific recommendations
- Parsing simulation

### 3. Template System

| Template | Best For |
|----------|----------|
| **Modern Minimalist** | Tech roles (Engineers, Data Scientists) |
| **Professional Traditional** | Finance, Legal, Senior Executives |
| **Creative Hybrid** | Design Engineers, UX Researchers |
| **Academic CV** | PhD, Professors, Researchers |

## ATS Score Breakdown

| Category | Points | Criteria |
|----------|--------|----------|
| Formatting | 30 | Single-column, standard fonts, no graphics |
| Structure | 20 | Summary, Skills, Experience, Education present |
| Content | 30 | Proper lengths, skills count, metrics in bullets |
| Keywords | 20 | Job description coverage (or 15 for general) |

**Target**: 85+ out of 100

## When to Use

**Use for:**
- Creating resume from career-biographer data
- Optimizing resume for specific job posting
- Generating multiple resume variants
- ATS score and improvement recommendations
- Multi-format export

**Do NOT use for:**
- Cover letters (different format)
- Portfolio websites (use web-design-expert)
- LinkedIn profile optimization
- Interview preparation
- Career counseling or job search strategy

## Anti-Patterns

### Anti-Pattern: Creative Resume for Tech Roles
**What it looks like**: Colorful infographics, skill bars, profile photo, two-column layout
**Why wrong**: ATS systems can't parse graphics or complex layouts
**Instead**: Use Minimalist template with clean, single-column text format

### Anti-Pattern: Generic Objective Statement
**What it looks like**: "Seeking a challenging role in a growth-oriented company..."
**Why wrong**: Wastes space, provides no information
**Instead**: Professional summary with specific metrics and target role

### Anti-Pattern: Listing Every Technology Ever Used
**What it looks like**: 40+ skills including outdated technologies
**Why wrong**: Dilutes expertise, unclear proficiency
**Instead**: List 15-20 most relevant skills for target role

### Anti-Pattern: Responsibilities Without Outcomes
**What it looks like**: "Managed a team", "Worked on backend systems"
**Why wrong**: Doesn't show impact or value
**Instead**: "Led team of 5 to deliver microservices migration, reducing deployment time by 70%"

### Anti-Pattern: Inconsistent Formatting
**What it looks like**: Mixed date formats, different bullet styles, varying fonts
**Why wrong**: Looks unprofessional, confuses ATS parsers
**Instead**: Strict consistency throughout

## Troubleshooting Quick Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| ATS Score &lt;70 | Complex formatting, graphics | Switch to Minimalist, remove images |
| Keyword Coverage &lt;60% | Not tailoring to job description | Extract keywords, add to Core Skills |
| Exceeds 2 pages | Too verbose, old roles included | Consolidate old roles, limit bullets |
| Generic summary | No positioning insights | Include specific metric, state target role |
| Long bullets | Trying to explain entire project | Split into multiple bullets, focus on outcome |

## Length Guidelines

| Experience | Pages |
|------------|-------|
| Entry-level (0-3 years) | 1 page |
| Mid-level (3-10 years) | 1-2 pages |
| Senior-level (10+ years) | 2 pages max |

**Never exceed 2 pages**, even for very senior roles.

## Reference Files

- `references/resume-protocol.md` - Complete 8-step generation protocol, ATS scoring, before/after examples
- `references/formatting-rules.md` - Best practices, templates, output formats, success metrics
- `references/interfaces-integration.md` - TypeScript interfaces, multi-skill workflows

---

**Core insight**: ATS compatibility first—the best-written resume is worthless if it never reaches human eyes.

**Use with**: career-biographer (content) | competitive-cartographer (positioning) | web-design-expert (portfolio)
