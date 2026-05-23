---
name: codebase-analysis
description: Produce a structured codebase analysis report with architecture overview, critical files, patterns, and actionable recommendations. Use when asked to "analyze codebase", "explore codebase", "understand this codebase", "map the codebase", "give me an overview of this project", "what does this codebase do", "codebase report", "project analysis", "audit this codebase", or "how is this project structured".
dependencies:
  - deep-analysis
  - technical-diagrams
---

# Codebase Analysis Workflow

Execute a structured 3-phase codebase analysis workflow to gather insights.

## Phase Overview

1. **Deep Analysis** -- Explore and synthesize codebase findings via the deep-analysis skill
2. **Reporting** -- Present structured analysis to the user
3. **Post-Analysis Actions** -- Save, document, or retain analysis insights

---

## Phase 1: Deep Analysis

**Goal:** Explore the codebase and synthesize findings.

1. **Determine analysis context:**
   - Accept the following inputs: an analysis context or feature description
   - If no inputs provided, set context to "general codebase understanding"

2. **Check for cached results:**
   - Check if `.agents/sessions/exploration-cache/manifest.md` exists
   - If found, read the manifest and verify: `codebase_path` matches the current working directory, and `timestamp` is within the configured cache TTL (default 24 hours)
   - **If cache is valid**, prompt the user to choose:
     - **Use cached results** (show the formatted cache date) -- Read cached synthesis from `.agents/sessions/exploration-cache/synthesis.md` and recon from `recon_summary.md`. Set `CACHE_HIT = true` and `CACHE_TIMESTAMP` to the cache's timestamp. Skip step 3 and proceed directly to step 4.
     - **Run fresh analysis** -- Remove the cache manifest file, set `CACHE_HIT = false`, and proceed to step 3
   - **If no valid cache**: set `CACHE_HIT = false` and proceed to step 3

3. **Run deep-analysis workflow:**
   - Refer to the **deep-analysis** skill and follow its workflow
   - Pass the analysis context from step 1
   - This handles reconnaissance, team planning, approval (auto-approved when invoked by another skill), team creation, parallel exploration, and synthesis
   - After completion, set `CACHE_TIMESTAMP = null` (fresh results, no prior cache)

4. **Verify results and capture metadata:**
   - Ensure the synthesis covers the analysis context adequately
   - If critical gaps remain, search for files and file contents to fill them directly
   - Record analysis metadata for Phase 2 reporting: whether results were cached (`CACHE_HIT`), cache timestamp if applicable (`CACHE_TIMESTAMP`), and the number of exploration workers used (from the deep-analysis team plan, or 0 if cached)

---

## Phase 2: Reporting

**Goal:** Present a structured analysis to the user.

1. **Load diagram guidance:**
   - Refer to the **technical-diagrams** skill for Mermaid diagram syntax and styling rules
   - Use Mermaid diagrams in the Architecture Overview and Relationship Map sections

2. **Use report template:**
   - Follow the report template structure below (see Report Template section)

3. **Present the analysis:**
   Structure the report with these sections:
   - **Executive Summary** -- Lead with the most important finding
   - **Architecture Overview** -- How the codebase is structured
   - **Tech Stack** -- Core technologies, frameworks, and tools detected
   - **Critical Files** -- The 5-10 most important files with details
   - **Patterns & Conventions** -- Recurring patterns and coding conventions
   - **Relationship Map** -- How components connect to each other
   - **Challenges & Risks** -- Technical risks and complexity hotspots
   - **Recommendations** -- Actionable next steps, each citing the challenge it addresses
   - **Analysis Methodology** -- Workers used, cache status, scope, and duration

4. Proceed immediately to Phase 3.

---

## Phase 3: Post-Analysis Actions

**Goal:** Let the user save, document, or retain analysis insights from the report through a multi-step interactive flow.

### Step 1: Select actions

Prompt the user to choose (multiple selections allowed):

- **Save Codebase Analysis Report** -- Write the structured report to a markdown file
- **Save a custom report** -- Generate a report tailored to your specific goals (you'll provide instructions next)
- **Update project documentation** -- Add/update README.md, CLAUDE.md, or AGENTS.md with analysis insights
- **Keep a condensed summary in memory** -- Retain a quick-reference summary in conversation context

If the user selects no actions, the workflow is complete. Thank the user and end.

### Step 2: Execute selected actions

Process selected actions in the following fixed order. Complete all sub-steps for each action before moving to the next.

#### Action: Save Codebase Analysis Report

**Step 2a-1: Prompt for file location**

- Check if an `internal/docs/` directory exists in the project root
  - If yes, suggest default path: `internal/docs/codebase-analysis-report-{YYYY-MM-DD}.md`
  - If no, suggest default path: `codebase-analysis-report-{YYYY-MM-DD}.md` in the project root
- Prompt the user to confirm or customize the file path

**Step 2a-2: Generate and save the report**

- Generate the full structured report using the Phase 2 analysis findings and the template structure
- Write the report to the confirmed path
- Confirm the file was saved

#### Action: Save Custom Report

**Step 2b-1: Gather report requirements**

- Ask the user to describe the goals and requirements for their custom report -- what it should focus on, what questions it should answer, and any format preferences

**Step 2b-2: Prompt for file location**

- Check if an `internal/docs/` directory exists in the project root
  - If yes, suggest default path: `internal/docs/custom-report-{YYYY-MM-DD}.md`
  - If no, suggest default path: `custom-report-{YYYY-MM-DD}.md` in the project root
- Prompt the user to confirm or customize the file path

**Step 2b-3: Generate and save the custom report**

- Generate a report shaped by the user's requirements from Step 2b-1, drawing from the Phase 2 analysis data -- this is a repackaging of existing findings, not a re-analysis
- Write the report to the confirmed path
- Confirm the file was saved

#### Action: Update Project Documentation

**Step 2c-1: Select documentation files and gather directions**

Prompt the user to choose which files to update (multiple selections allowed):

- **README.md** -- Add architecture, structure, and tech stack information
- **CLAUDE.md** -- Add patterns, conventions, critical files, and architectural decisions
- **AGENTS.md** -- Add agent descriptions, capabilities, and coordination patterns

Then ask the user: "What content from the analysis should be added or updated? Provide general directions or specific sections to focus on (applies across all selected files, or specify per-file directions)."

**Step 2c-2: Generate and approve documentation drafts**

For each selected file, read the existing file and generate a draft based on the user's directions and Phase 2 analysis data:

- **README.md**: Read existing file at project root. If no README.md exists, skip and inform the user. Draft updates focusing on architecture, project structure, and tech stack.
- **CLAUDE.md**: Read existing file at project root. If none exists, ask if one should be created (if declined, skip). Draft updates focusing on patterns, conventions, critical files, and architectural decisions.
- **AGENTS.md**: Read existing file at project root (create new if none exists). Draft content focusing on agent inventory (name, model, purpose), capabilities and tool access, coordination patterns, skill-agent mappings, and model tiering rationale.

Present all drafts together in a single output, clearly labeled by file. Then prompt the user to choose:

- **Apply all** -- Apply all drafted updates
- **Modify** -- Specify which file(s) to revise and what to change (max 3 revision cycles, then must Apply or Skip)
- **Skip all** -- Skip all documentation updates

If approved, apply updates.

#### Action: Keep Insights in Memory

- Present a condensed **Codebase Quick Reference** inline in the conversation:
  - **Architecture** -- 1-2 sentence summary of how the codebase is structured
  - **Key Files** -- 3-5 most critical files with one-line descriptions
  - **Conventions** -- Important patterns and naming conventions
  - **Tech Stack** -- Core technologies and frameworks
  - **Watch Out For** -- Top risks or complexity hotspots
- No file is written -- this summary stays in conversation context for reference during the session

### Step 3: Actionable Insights Follow-up

This step always executes after Step 2 completes. The Phase 2 analysis is available in conversation context regardless of whether a report file was saved.

Prompt the user to choose:
- **Address actionable insights** -- Fix challenges and implement recommendations from the report
- **Skip** -- No further action needed

If the user selects "Skip", proceed to Step 4.

If the user selects "Address actionable insights":

**Step 3a: Extract actionable items from the report**

Parse the Phase 2 report (in conversation context) to extract items from:
- **Challenges & Risks** table rows -- title from Challenge column, severity from Severity column, description from Impact column
- **Recommendations** section -- each numbered item with an _(addresses: {Challenge name})_ citation; inherit the cited challenge's severity (High/Medium/Low). If no citation is present, default to Medium.
- **Other findings** with concrete fixes -- default to Low severity

If no actionable items are found, inform the user and skip to Step 4.

**Step 3b: Present severity-ranked item list**

- Follow the actionable insights template structure below (see Actionable Insights Template section)
- Present items sorted High -> Medium -> Low, each showing:
  - Title
  - Severity (High / Medium / Low)
  - Source section (Challenges & Risks, Recommendations, or Other)
  - Brief description
- Prompt the user to select which items to address (multiple selections allowed)
- If no items selected, skip to Step 4

**Step 3c: Process each selected item in priority order (High -> Medium -> Low)**

For each item:

1. **Assess complexity:**
   - **Simple** -- Single file, clear fix, localized change
   - **Complex** -- Multi-file, architectural impact, requires investigation

2. **Plan the fix:**
   - Simple: Read the target file, propose changes directly
   - Complex (architectural): Delegate to an architecture specialist with context: the item title, severity, description, the relevant report section text, and any files or components mentioned. The specialist designs the fix and returns a proposal.
   - Complex (needs investigation): Delegate to an exploration specialist with context: the item title, description, suspected files/components, and what needs investigation. The specialist explores and returns findings for you to formulate a fix proposal.
   - If delegation fails, fall back to direct investigation using file reading and searching, and propose a simpler fix based on available information.

3. **Present proposal:** Show files to modify, specific changes, and rationale

4. **User approval** -- prompt the user to choose:
   - **Apply** -- Execute changes, confirm success
   - **Skip** -- Record the skip, move to next item
   - **Modify** -- User describes adjustments, re-propose the fix (max 3 revision cycles, then must Apply or Skip)

**Step 3d: Summarize results**

Present a summary covering:
- Items addressed (with list of files modified per item)
- Items skipped
- Total files modified table

### Step 4: Complete the workflow

Summarize which actions were executed and confirm the workflow is complete.

---

## Error Handling

### General

If any phase fails:
1. Explain what went wrong
2. Ask the user how to proceed:
   - Retry the phase
   - Skip to next phase (with partial results)
   - Abort the workflow

### Documentation Update Failures (Step 2c)

If writing documentation updates fails:
1. Retry the operation once
2. If still failing, present the drafted content to the user inline and suggest they apply it manually
3. Continue with the remaining selected files

### Specialist Delegation Failures (Step 3c)

If an architecture or exploration specialist fails during actionable insight processing:
1. Fall back to direct investigation using file reading and searching
2. Propose a simpler fix based on available information
3. If the item is too complex to address without specialist assistance, inform the user and offer to skip

---

## Coordination

Exploration and synthesis coordination is handled by the **deep-analysis** skill in Phase 1, which uses hub-and-spoke coordination. Deep-analysis performs reconnaissance, composes a team plan (auto-approved when invoked by another skill), assembles workers, and manages the exploration/synthesis lifecycle. See that skill for team setup, approval flow, and failure handling details.

---

## Report Template

Use this structure when presenting analysis findings in Phase 2.

```markdown
# Codebase Analysis Report

**Analysis Context**: {What was analyzed and why}
**Codebase Path**: {Path analyzed}
**Date**: {YYYY-MM-DD}

{If the report exceeds approximately 100 lines, add a **Table of Contents** here linking to each major section.}

---

## Executive Summary

{Lead with the most important finding. 2-3 sentences covering: what was analyzed, the key architectural insight, and the primary recommendation or risk.}

---

## Architecture Overview

{2-3 paragraphs describing:}
- How the codebase is structured (layers, modules, boundaries)
- The design philosophy and architectural style
- Key architectural decisions and their rationale

{Include a Mermaid architecture diagram showing the major layers/components. Follow technical-diagrams styling rules.}

---

## Tech Stack

| Category | Technology | Version (if detected) | Role |
|----------|-----------|----------------------|------|
| Language | {e.g., TypeScript} | {e.g., 5.x} | Primary language |
| Framework | {e.g., Next.js} | {e.g., 16} | Web framework |

{Include only technologies actually detected in config files or code.}

---

## Critical Files

{Limit to 5-10 most important files}

| File | Purpose | Relevance |
|------|---------|-----------|
| `path/to/file` | Brief description | High/Medium |

### File Details

#### `path/to/critical-file`
- **Key exports**: What this file provides to others
- **Core logic**: What it does
- **Connections**: What depends on it and what it depends on

---

## Patterns & Conventions

### Code Patterns
- **Pattern**: Description and where it's used

### Naming Conventions
- **Convention**: Description and examples

### Project Structure
- **Organization**: How files and directories are organized

---

## Relationship Map

{Describe how key components connect. Use Mermaid flowcharts for data flows and dependency maps. Cap at 15-20 connections.}

---

## Challenges & Risks

| Challenge | Severity | Impact |
|-----------|----------|--------|
| {Description} | High/Medium/Low | {What could go wrong} |

---

## Recommendations

1. **{Recommendation}** _(addresses: {Challenge name})_: {Brief rationale}
2. **{Recommendation}** _(addresses: {Challenge name})_: {Brief rationale}

---

## Analysis Methodology

- **Exploration workers**: {Number} workers with focus areas: {list}
- **Synthesis**: Findings merged and critical files read in depth
- **Scope**: {What was included and what was intentionally excluded}
- **Cache status**: {Fresh analysis / Cached results from YYYY-MM-DD}
```

### Report Section Guidelines

- **Executive Summary**: Lead with the most important finding, not a generic overview. Keep to 2-3 sentences.
- **Critical Files**: Limit to 5-10 files. Include both the "what" and "why".
- **Patterns & Conventions**: Only include consistently applied patterns. Note deviations.
- **Relationship Map**: Focus on the most important connections. Use Mermaid flowcharts with `classDef` and `color:#000`. Cap at 15-20 connections.
- **Challenges & Risks**: Rate severity based on likelihood and impact combined.
- **Recommendations**: Make actionable. Each must cite the challenge it addresses using _(addresses: {Challenge name})_.

---

## Actionable Insights Template

### Item List Format

Present extracted items grouped by severity, highest first:

### High Severity

1. **{Title}** -- _{Source: Challenges & Risks}_
   {Brief description of the issue and its impact}

### Medium Severity

2. **{Title}** -- _{Source: Recommendations}_
   {Brief description and rationale}

### Low Severity

3. **{Title}** -- _{Source: Other Findings}_
   {Brief description}

### Severity Assignment Guidelines

**From Challenges & Risks Table:** Use the Severity column value directly.

**From Recommendations Section:** Use the cited challenge's severity. If no citation, default to Medium.

**From Other Findings:** Default to Low unless explicitly critical.

### Complexity Assessment

| Complexity | Typical Effort | Description |
|-----------|---------------|-------------|
| Simple | Low (~minutes) | Single targeted change, clear fix |
| Complex -- Architectural | Medium-High (~30min-1hr+) | Multi-file refactoring, design decisions |
| Complex -- Investigation | Medium (~15-30min) + varies | Investigation phase + fix implementation |

### Summary Format

After processing all selected items:

| # | Item | Severity | Files Modified |
|---|------|----------|----------------|
| 1 | {Title} | High | `file1.ts`, `file2.ts` |

**Total:** {N} items addressed, {M} items skipped, {P} files modified

## Integration Notes

**What this component does:** Orchestrates a full codebase analysis workflow: exploration via deep-analysis, structured reporting with Mermaid diagrams, interactive post-analysis actions (save reports, update docs, address insights), and actionable insight processing with complexity-based specialist delegation.

**Origin:** Skill (orchestrator)

**Capabilities needed:**
- File reading and writing (for reports and documentation updates)
- File search (for gap-filling after synthesis)
- User interaction/prompting (multi-step interactive flow with selections)
- Delegation to sub-skills (deep-analysis for exploration, technical-diagrams for visualization)
- Delegation to specialists (architecture and exploration specialists for complex actionable insights)

**Adaptation guidance:**
- The multi-select user prompts were originally `AskUserQuestion` calls with structured YAML options. Adapt to whatever user interaction mechanism the target harness provides.
- Specialist delegation for actionable insights (Step 3c) originally used platform-specific agent spawning. Adapt to the target harness's delegation mechanism, or simplify to direct investigation if no delegation is available.
- The report and actionable insights templates are inlined in this skill. They were originally separate reference files.
