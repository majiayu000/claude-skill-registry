---
name: zachman-analysis
description: Apply Zachman Framework perspective analysis with honest limitations. Analyze architecture from specific row/column perspectives.
allowed-tools: Read, Glob, Grep
---

# Zachman Analysis

## When to Use This Skill

Use this skill when you need to:

- Analyze architecture from a specific stakeholder perspective
- Ensure complete coverage across different viewpoints
- Check which architectural aspects are documented
- Understand what questions each perspective asks

**Keywords:** zachman, viewpoint, perspective, interrogative, what, how, where, who, when, why, planner, owner, designer, builder

## Zachman Framework 3.0 Overview

The Zachman Framework is a **6x6 ontology** for classifying enterprise architecture artifacts. It's a classification schema (taxonomy), not a methodology.

**Key insight:** TOGAF tells you *how* to create architecture. Zachman tells you *how to organize* what you create.

## The Matrix

### Columns (Interrogatives)

Each column answers a fundamental question:

| Column | Interrogative | Focus | Artifacts |
| --- | --- | --- | --- |
| 1 | **What** (Data) | Things of interest | Data models, entity lists |
| 2 | **How** (Function) | Processes and transformations | Process flows, use cases |
| 3 | **Where** (Network) | Locations and distribution | Network diagrams, site maps |
| 4 | **Who** (People) | Roles and responsibilities | Org charts, RACI matrices |
| 5 | **When** (Time) | Events and schedules | Timelines, event models |
| 6 | **Why** (Motivation) | Goals and constraints | Business drivers, rules |

### Rows (Perspectives)

Each row represents a stakeholder level with increasing detail:

| Row | Perspective | Audience | Level |
| --- | --- | --- | --- |
| 1 | **Planner/Executive** | Board, C-suite | Scope/Context |
| 2 | **Owner/Business** | Business managers | Business model |
| 3 | **Designer/Architect** | Solution architects | Logical design |
| 4 | **Builder/Engineer** | Developers, engineers | Physical design |
| 5 | **Subcontractor/Technician** | Implementers | Detailed specs |
| 6 | **User/Operations** | End users, operators | Running system |

## Critical Limitation: Code Extraction Capabilities

**IMPORTANT:** Not all Zachman perspectives can be extracted from code analysis.

| Row | Perspective | Code Extraction | Notes |
| --- | --- | --- | --- |
| 1 | Planner | **Cannot extract** | Requires strategic context, executive input |
| 2 | Owner | **Cannot extract** | Requires business documentation, stakeholder interviews |
| 3 | Designer | **Partial** | Can infer structure; design rationale missing |
| 4 | Builder | **Strong** | Technologies, specs visible in code |
| 5 | Subcontractor | **Strong** | Configurations, implementations in code |
| 6 | User | **Limited** | Requires runtime data, deployment configs |

### What This Means

- **Rows 4-5:** This plugin can analyze code and extract useful information
- **Rows 1-3:** This plugin can **guide** structured interviews and documentation review, but cannot generate content from code alone
- **Row 6:** Requires access to running systems and operational data

## Using the Matrix

### For Coverage Checking

Use the matrix as a checklist to ensure documentation completeness:

```text
         What  How   Where  Who   When  Why
Planner   [ ]   [ ]   [ ]   [ ]   [ ]   [ ]
Owner     [ ]   [ ]   [ ]   [ ]   [ ]   [ ]
Designer  [ ]   [ ]   [ ]   [ ]   [ ]   [ ]
Builder   [x]   [x]   [x]   [ ]   [ ]   [ ]
Subcontr  [x]   [x]   [x]   [ ]   [ ]   [ ]
User      [ ]   [ ]   [ ]   [ ]   [ ]   [ ]
```

### For Specific Analysis

To analyze a specific cell:

1. Identify the row (stakeholder perspective)
2. Identify the column (interrogative)
3. Determine if code extraction is possible
4. If rows 1-3: Guide human input gathering
5. If rows 4-6: Analyze codebase for relevant information

## Cell Examples

### Row 4 (Builder) Examples

| Column | Question | Code Analysis Can Find |
| --- | --- | --- |
| What | What data structures? | Models, schemas, types |
| How | How is it built? | Algorithms, patterns |
| Where | Where does it run? | Deployment configs |
| Who | Who maintains it? | Git history, CODEOWNERS |
| When | When does it execute? | Schedulers, triggers |
| Why | Why this approach? | ADRs, comments |

### Row 1 (Planner) Examples - Require Human Input

| Column | Question | Requires |
| --- | --- | --- |
| What | What are business entities? | Business glossary |
| How | What are core processes? | Process documentation |
| Where | Where do we operate? | Business geography |
| Who | What is the org structure? | Org chart |
| When | What are business cycles? | Business calendar |
| Why | What are strategic goals? | Strategy documents |

## Wizard Mode

If you're unsure which row/column to use:

### Step 1: Who's the audience?

- Executives → Row 1 (Planner)
- Business managers → Row 2 (Owner)
- Architects → Row 3 (Designer)
- Developers → Row 4 (Builder)
- Implementers → Row 5 (Subcontractor)
- Operations → Row 6 (User)

### Step 2: What question?

- About data/things → Column 1 (What)
- About processes → Column 2 (How)
- About locations → Column 3 (Where)
- About people/roles → Column 4 (Who)
- About timing/events → Column 5 (When)
- About goals/rules → Column 6 (Why)

## Practical Application

### Minimum Viable Coverage

For most projects, ensure at least:

- Row 3, Column 1-2 (Designer: What & How) - Architecture diagrams
- Row 4, Column 1-2 (Builder: What & How) - Technical specs
- Row 4, Column 6 (Builder: Why) - ADRs

### Comprehensive Coverage

For enterprise-scale work:

- All cells for rows 3-5
- Key cells for rows 1-2 (with stakeholder input)

## Memory References

For detailed limitations, see `references/zachman-limitations.md`.
For the complete matrix, see `references/zachman-overview.md`.

## Version History

- **v1.0.0** (2025-12-05): Initial release
  - Zachman Framework 3.0 matrix documentation
  - Critical limitation: code extraction capabilities by row
  - Wizard mode for row/column selection
  - Practical application and minimum viable coverage

---

## Last Updated

**Date:** 2025-12-05
**Model:** claude-opus-4-5-20251101
