---
name: review-a11y
description: Accessibility audit. Dispatches an accessibility auditor to identify WCAG conformance gaps, prioritize by user impact, and recommend fixes. Advisory only — no changes made.
model: opus
---

# Accessibility Review - WCAG Conformance Audit

Advisory-only accessibility audit. Dispatches a `QA - Accessibility Auditor` agent to evaluate web content against WCAG 2.2 Level AA, prioritize issues by real-world user impact, and recommend fixes. No changes are made.

## Philosophy

**Impact over compliance.** A missing form label that blocks screen reader users is more important than a redundant ARIA role that harms nobody. The audit prioritizes barriers that prevent or degrade access for people with disabilities.

**Diagnostic, not therapeutic.** This skill identifies accessibility barriers and recommends fixes. It does not implement them. Ask for changes directly after reviewing the findings, or use `/implement` with the audit as context.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│               ACCESSIBILITY REVIEW                   │
├──────────────────────────────────────────────────────┤
│  1. Detect web content                               │
│  2. Determine scope                                  │
│  3. Dispatch accessibility auditor                   │
│  4. Present audit report                             │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Detect Web Content

Scan the project for web content files:

| Extensions                     | Content type         |
|--------------------------------|----------------------|
| `.html`, `.htm`                | HTML documents       |
| `.jsx`, `.tsx`                 | React/JSX components |
| `.vue`                         | Vue components       |
| `.svelte`                      | Svelte components    |
| `.css`, `.scss`, `.less`       | Stylesheets          |
| `.ejs`, `.hbs`, `.pug`, `.njk` | HTML templates       |

**Exclude:** `node_modules/`, `vendor/`, `dist/`, `build/`, `.git/`, and other generated/vendored directories.

**If no web content is found:** Report "No web content detected in this project. Accessibility audits apply to projects with HTML, CSS, or UI component files." and abort.

### 2. Determine Scope

Present detected web content to the user with file counts:

```
Detected web content:
  - HTML: 12 files
  - React (TSX): 28 files
  - CSS: 8 files

What should I audit?
  - Entire project (default)
  - Specific directory (e.g., src/components/)
  - Specific files
```

Accept the user's selection. Default: entire project.

### 3. Dispatch Accessibility Auditor

**Assess scope size** with Glob.

**Small scope (roughly ≤20 web content files):** Spawn a single `QA - Accessibility Auditor` agent with the full scope.

**Large scope (roughly >20 web content files):** Partition by directory or component boundary. Spawn multiple `QA - Accessibility Auditor` agents **in parallel**, each with a focused partition.

**Prompt for each agent:**

```
Audit the following web content for accessibility issues.
Scope: [partition or full scope]

Read all files in scope and perform your full audit:
1. Detect and run any automated accessibility tooling (axe-core, pa11y, etc.)
2. Manual inspection for issues automated tools miss (keyboard navigation,
   semantic correctness, dynamic content, ARIA usage, content quality, media)
3. Classify every issue by severity (CRITICAL / HIGH / LOW)

Produce your standard output format with summary, issues by severity,
and tooling recommendations.
```

### 4. Present Audit Report

Collect all agent responses. If multiple agents were dispatched, merge findings into a single report, deduplicating issues that span partitions.

Present a consolidated report:

```
## Accessibility Audit Report

Conformance target: WCAG 2.2 Level AA
Method: [automated + manual | manual only]
Scope: [what was audited]
Issues found: N (X critical, Y high, Z low)

### CRITICAL
[merged critical findings from all agents]

### HIGH
[merged high findings]

### LOW
[merged low findings]

### Tooling Recommendations
[if applicable — recommendations for adding automated accessibility testing]

### Suggested Next Steps
[Based on findings:
- If critical/high issues found: recommend fixing them, noting which
  would be handled by HTML changes vs CSS changes vs JS changes
- If no significant issues: "No significant accessibility barriers found"
- If no automated tooling exists: recommend adding axe-core or pa11y]
```

**The report is your synthesis.** If multiple agents were dispatched, look for patterns across partitions (e.g., missing labels is a project-wide habit, not an isolated incident). Don't just concatenate agent outputs.

## Agent Coordination

- All auditor agents run **in parallel** (they are read-only and independent)
- Wait for all agents to complete before presenting the consolidated report
- If an agent fails or times out, note the failure in the report and continue with other results

## Abort Conditions

**Abort:**
- No web content files detected in scope
- Not a git repository

**Do NOT abort:**
- No automated accessibility tooling available (proceed with manual audit)
- A single agent fails in a multi-agent dispatch (report failure, continue)
- Few issues found (report "no significant issues" — that's a valid outcome)
