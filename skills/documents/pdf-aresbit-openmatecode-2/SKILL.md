---
name: pdf
description: Professional PDF solution. Create PDFs using HTML+Paged.js (academic papers, reports, documents). Process existing PDFs using Python (read, extract, merge, split, fill forms). Supports KaTeX math formulas, Mermaid diagrams, three-line tables, citations, and other academic elements. Also use this skill when user explicitly requests LaTeX (.tex) or native LaTeX compilation.
---

## Route Selection

| Route | Trigger | Route File |
|-------|---------|------------|
| **HTML** (default) | All PDF creation requests | `routes/html.md` |
| **LaTeX** | User explicitly requests LaTeX, .tex, or Tectonic | `routes/latex.md` |
| **Process** | Work with existing PDFs (extract, merge, fill forms, etc.) | `routes/process.md` |

**Default to HTML.** Only use LaTeX route when user explicitly requests it.

### MANDATORY: Read Route File Before Implementation

<system-reminder>
You MUST read the corresponding route file before writing ANY code.
Route files contain critical implementation details NOT duplicated here.
Skipping this step leads to incorrect output (wrong scripts, missing CSS, broken layouts).
</system-reminder>

**Before implementation, you MUST:**
1. Determine the route (HTML / LaTeX / Process)
2. **Read the route file** (`routes/html.md`, `routes/latex.md`, or `routes/process.md`)
3. Only then proceed with implementation

This file (SKILL.md) contains constraints and principles. Route files contain **how-to details**.

### Decision Rules

#### Route Selection
| User Says | Route |
|-----------|-------|
| "Create a PDF", "Make a report", "Write a paper" | HTML |
| "Use LaTeX", "Compile .tex", "Use Tectonic" | LaTeX |
| "Extract text from PDF", "Merge these PDFs", "Fill this form" | Process |

#### Cover Style Selection (HTML Route)
| Context | Style |
|---------|-------|
| Academic paper, thesis, formal coursework | **Minimal** (white, centered, no decoration) |
| Reports, proposals, professional documents | **Designed** (choose from style reference in html.md) |
| Uncertain | Default to **Designed** — plain text cover = mediocre |

**Key principle**: Cover background separates "acceptable" from "impressive". See html.md for 11 style options.

#### Citation Format Selection
| Document Language | Format |
|-------------------|--------|
| Chinese | GB/T 7714 (use [J][M][D] identifiers) |
| English | APA |
| Mixed | Chinese refs → GB/T 7714, English refs → APA |

---

## Quick Start

**Use the unified CLI for all operations:**

```bash
# Check environment (JSON output, exit code 0=ok, 2=missing deps)
/app/.kimi/skills/pdf/scripts/pdf.sh check

# Auto-fix missing dependencies (idempotent, safe to run multiple times)
/app/.kimi/skills/pdf/scripts/pdf.sh fix

# Convert HTML to PDF
/app/.kimi/skills/pdf/scripts/pdf.sh html input.html

# Compile LaTeX to PDF
/app/.kimi/skills/pdf/scripts/pdf.sh latex input.tex
```

**Exit codes:**
- `0` = success
- `1` = usage error
- `2` = dependency missing (run `pdf.sh fix`)
- `3` = runtime error

**Dependencies by route:**
- **HTML route**: Node.js, Playwright, Chromium
- **Process route**: Python 3, pikepdf, pdfplumber
- **LaTeX route**: Tectonic

---

## Core Constraints (Must Follow)

### 1. Output Language
**Output language must match user's query language.**
- User writes in Chinese → PDF content in Chinese
- User writes in English → PDF content in English
- User explicitly specifies language → Follow user's specification

### 2. Word Count and Page Constraints
- Strictly follow user-specified word/page count requirements
- Do not arbitrarily inflate content length

### 3. Citation and Search Standards

#### CRITICAL: Search Before Writing
**DO NOT fabricate information. When in doubt, SEARCH.**

If content involves ANY of these, you **MUST search FIRST** before writing:
- Statistics, numbers, percentages, rankings
- Policies, regulations, laws, standards
- Academic research, theories, methodologies
- Current events, recent developments
- **Anything you're not 100% certain about**

<system-reminder>
Never proceed with writing if you need statistics, research data, or policy information without searching first.
Making up facts is strictly prohibited. When uncertain, search.
</system-reminder>

#### When Search is Required
| Scenario | Search? | Notes |
|----------|---------|-------|
| Statistics, data | **Required** | e.g., "2024 employment rate" |
| Policies, regulations | **Required** | e.g., "startup subsidies" |
| Research, papers | **Required** | e.g., "effectiveness of method X" |
| Time-sensitive content | **Required** | Information after knowledge cutoff |
| **Uncertain facts** | **Required** | If unsure, always search |
| Common knowledge | Not needed | e.g., "water boils at 100°C" |

**Search workflow**:
1. Identify facts/data requiring verification
2. Search for authentic sources
3. If results insufficient, **iterate search** until reliable info obtained
4. Include real sources in references
5. **If search fails repeatedly, tell the user** instead of making up data

#### Citations Must Be Real
**Fabricating references is prohibited**. All citations must have:
- Correct author/institution names
- Accurate titles
- Verifiable year, journal/source

#### Cross-references (Must Be Clickable)
```html
As shown in <a href="#fig-1-1">Figure 1-1</a>...
From <a href="#eq-2-1">Equation (2-1)</a>...
See <a href="#sec3">Section 3</a>...
```
**Note**: `id` must be placed at container top (see CSS Counters section in html.md).

---

## Content Quality Constraints

### 1. Word/Page Count Constraints
**Must strictly follow user-specified word or page count requirements**:

| User Request | Execution Standard |
|--------------|-------------------|
| Specific word count (e.g., "3000 words") | Within ±20%, i.e., 2400-3600 words |
| Specific page count (e.g., "5 pages") | Exactly equal, last page may be partial |
| Word count range (e.g., "2000-3000 words") | Must fall within range |
| No explicit requirement | Infer reasonably by document type; prefer thorough over superficial |
| Minimum specified (e.g., "more than 5000 words") | No more than 2x, i.e., 5000-10000 words |

**Prohibited behaviors**:
- Arbitrarily shortening content ("concise" is not an excuse)
- Padding pages with excessive bullet lists (maintain high information density)
- Exceeding twice the user's requested length

**Special case - Resume/CV**:
- Resume should be **1 page** unless user specifies otherwise
- Use compact margins: `margin: 1.5cm`

### 2. Outline Adherence (Mandatory)
**When user provides outline**:
- **Strictly follow** the user-provided outline structure
- Section titles must match outline (minor wording adjustments OK, no level/order changes)
- Do not add or remove sections arbitrarily
- If outline seems problematic, **ask user first** before modifying

**When no user outline**:
- Use standard structures based on document type:
  - **Academic papers**: IMRaD (Introduction-Methods-Results-Discussion) or Introduction-Literature Review-Methods-Results-Discussion-Conclusion
  - **Business reports**: Conclusion-first (Executive Summary → Detailed Analysis → Recommendations)
  - **Technical docs**: Overview → Principles → Usage → Examples → FAQ
  - **Course assignments**: Follow assignment structure requirements
- Sections must have logical progression, no disconnects

---

## Tech Stack Overview

| Route | Tools | Purpose |
|-------|-------|---------|
| HTML | Playwright + Paged.js | HTML → PDF conversion |
| HTML | KaTeX, Mermaid | Math formulas, diagrams |
| Process | pikepdf | Form filling, page operations, metadata |
| Process | pdfplumber | Text and table extraction |
| Process | LibreOffice | Office → PDF conversion |
| LaTeX | Tectonic | LaTeX → PDF compilation |
