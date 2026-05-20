---
name: codebase-analysis
description: Produce a structured codebase analysis report with architecture overview, critical files, patterns, and actionable recommendations. Use when asked to "analyze codebase", "explore codebase", "understand this codebase", "map the codebase", "give me an overview of this project", "what does this codebase do", "codebase report", "project analysis", "audit this codebase", or "how is this project structured".
dependencies:
  - deep-analysis
  - technical-diagrams
---

# Codebase Analysis Workflow

Execute a structured 3-phase codebase analysis workflow to gather insights.

Accept the following inputs:
- **analysis-context** (optional): What to analyze and why. Defaults to "general codebase understanding" if not provided.

## Phase Overview

1. **Deep Analysis** — Explore and synthesize codebase findings via the deep-analysis skill
2. **Reporting** — Present structured analysis to the user
3. **Post-Analysis Actions** — Save, document, or retain analysis insights

---

## Phase 1: Deep Analysis

**Goal:** Explore the codebase and synthesize findings.

1. **Determine analysis context:**
   - If analysis-context input is provided, use it as the analysis context
   - If no input, set context to "general codebase understanding"

2. **Check for cached results:**
   - Check if `.agents/sessions/exploration-cache/manifest.md` exists
   - If found, read the manifest and verify: `codebase_path` matches the current working directory, and `timestamp` is within the configured cache TTL (default 24 hours)
   - **If cache is valid**, prompt the user to choose:
     - **Use cached results** (show the formatted cache date) — Read cached synthesis from `.agents/sessions/exploration-cache/synthesis.md` and recon from `recon_summary.md`. Set `CACHE_HIT = true` and `CACHE_TIMESTAMP` to the cache's timestamp. Skip step 3 and proceed directly to step 4.
     - **Run fresh analysis** — Remove the cache manifest file, set `CACHE_HIT = false`, and proceed to step 3
   - **If no valid cache**: set `CACHE_HIT = false` and proceed to step 3

3. **Run deep-analysis workflow:**
   - Refer to the **deep-analysis** skill for the full exploration and synthesis workflow.
   - Pass the analysis context from step 1
   - This handles reconnaissance, team planning, approval (auto-approved when skill-invoked), team creation, parallel exploration (code-explorer agents), and synthesis (code-synthesizer agent)
   - After completion, set `CACHE_TIMESTAMP = null` (fresh results, no prior cache)

4. **Verify results and capture metadata:**
   - Ensure the synthesis covers the analysis context adequately
   - If critical gaps remain, search for files and file contents to fill them directly
   - Record analysis metadata for Phase 2 reporting: whether results were cached (`CACHE_HIT`), cache timestamp if applicable (`CACHE_TIMESTAMP`), and the number of explorer agents used (from the deep-analysis team plan, or 0 if cached)

---

## Phase 2: Reporting

**Goal:** Present a structured analysis to the user.

1. **Load diagram guidance:**
   - Refer to the **technical-diagrams** skill for Mermaid diagram syntax and styling rules.
   - Use Mermaid diagrams in the Architecture Overview and Relationship Map sections

2. **Use the report template** (see Report Template section below) to structure the presentation.

3. **Present the analysis:**
   Structure the report with these sections:
   - **Executive Summary** — Lead with the most important finding
   - **Architecture Overview** — How the codebase is structured
   - **Tech Stack** — Core technologies, frameworks, and tools detected
   - **Critical Files** — The 5-10 most important files with details
   - **Patterns & Conventions** — Recurring patterns and coding conventions
   - **Relationship Map** — How components connect to each other
   - **Challenges & Risks** — Technical risks and complexity hotspots
   - **Recommendations** — Actionable next steps, each citing the challenge it addresses
   - **Analysis Methodology** — Agents used, cache status, scope, and duration

4. **Proceed immediately to Phase 3.**
   Do NOT stop here. Do NOT wait for user input. The report is presented, but the workflow requires Post-Analysis Actions. Continue directly to Phase 3 now.

---

## Phase 3: Post-Analysis Actions

**Goal:** Let the user save, document, or retain analysis insights from the report through a multi-step interactive flow.

### Step 1: Select actions

Prompt the user to choose (the user may select multiple options):

- **Save Codebase Analysis Report** — Write the structured report to a markdown file
- **Save a custom report** — Generate a report tailored to your specific goals (you'll provide instructions next)
- **Update project documentation** — Add/update README.md, CLAUDE.md, or AGENTS.md with analysis insights
- **Keep a condensed summary in memory** — Retain a quick-reference summary in conversation context

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

- Use the report template already loaded in Phase 2 Step 1
- Generate the full structured report using the Phase 2 analysis findings and the template structure
- Create the file at the confirmed path
- Confirm the file was saved

#### Action: Save Custom Report

**Step 2b-1: Gather report requirements**

- Prompt the user to describe the goals and requirements for their custom report — what it should focus on, what questions it should answer, and any format preferences

**Step 2b-2: Prompt for file location**

- Check if an `internal/docs/` directory exists in the project root
  - If yes, suggest default path: `internal/docs/custom-report-{YYYY-MM-DD}.md`
  - If no, suggest default path: `custom-report-{YYYY-MM-DD}.md` in the project root
- Prompt the user to confirm or customize the file path

**Step 2b-3: Generate and save the custom report**

- Generate a report shaped by the user's requirements from Step 2b-1, drawing from the Phase 2 analysis data — this is a repackaging of existing findings, not a re-analysis
- Create the file at the confirmed path
- Confirm the file was saved

#### Action: Update Project Documentation

**Step 2c-1: Select documentation files and gather directions**

Prompt the user to choose (the user may select multiple options):

- **README.md** — Add architecture, structure, and tech stack information
- **CLAUDE.md** — Add patterns, conventions, critical files, and architectural decisions
- **AGENTS.md** — Add agent descriptions, capabilities, and coordination patterns

Then prompt the user for update directions for all selected files: "What content from the analysis should be added or updated? Provide general directions or specific sections to focus on (applies across all selected files, or specify per-file directions)."

**Step 2c-2: Generate and approve documentation drafts**

For each selected file, read the existing file and generate a draft based on the user's directions and Phase 2 analysis data:

- **README.md**: Read existing file at project root. If no README.md exists, skip and inform the user. Draft updates focusing on architecture, project structure, and tech stack.
- **CLAUDE.md**: Read existing file at project root. If none exists, ask if one should be created (if declined, skip). Draft updates focusing on patterns, conventions, critical files, and architectural decisions.
- **AGENTS.md**: Read existing file at project root (create new if none exists). Draft content focusing on agent inventory (name, model, purpose), capabilities and tool access, coordination patterns, skill-agent mappings, and model tiering rationale.

Present **all drafts together** in a single output, clearly labeled by file. Then prompt the user to choose:

- **Apply all** — Apply all drafted updates
- **Modify** — Specify which file(s) to revise and what to change (max 3 revision cycles, then must Apply or Skip)
- **Skip all** — Skip all documentation updates

If approved, apply updates by modifying existing files or creating new files.

#### Action: Keep Insights in Memory

- Present a condensed **Codebase Quick Reference** inline in the conversation:
  - **Architecture** — 1-2 sentence summary of how the codebase is structured
  - **Key Files** — 3-5 most critical files with one-line descriptions
  - **Conventions** — Important patterns and naming conventions
  - **Tech Stack** — Core technologies and frameworks
  - **Watch Out For** — Top risks or complexity hotspots
- No file is written — this summary stays in conversation context for reference during the session

### Step 3: Actionable Insights Follow-up

**Condition:** This step always executes after Step 2 completes. The Phase 2 analysis is available in conversation context regardless of whether a report file was saved.

Prompt the user to choose:
- **Address actionable insights** — Fix challenges and implement recommendations from the report
- **Skip** — No further action needed

If the user selects "Skip", proceed to Step 4.

If the user selects "Address actionable insights":

**Step 3a: Extract actionable items from the report**

Parse the Phase 2 report (in conversation context) to extract items from:
- **Challenges & Risks** table rows — title from Challenge column, severity from Severity column, description from Impact column
- **Recommendations** section — each numbered item with an _(addresses: {Challenge name})_ citation; inherit the cited challenge's severity (High/Medium/Low). If no citation is present, default to Medium.
- **Other findings** with concrete fixes — default to Low severity

If no actionable items are found, inform the user and skip to Step 4.

**Step 3b: Present severity-ranked item list**

- Use the actionable insights template format (see Actionable Insights Template section below)
- Present items sorted High to Medium to Low, each showing:
  - Title
  - Severity (High / Medium / Low)
  - Source section (Challenges & Risks, Recommendations, or Other)
  - Brief description
- Prompt the user to select which items to address (the user may select multiple options)
- If no items selected, skip to Step 4

**Step 3c: Process each selected item in priority order (High to Medium to Low)**

For each item:

1. **Assess complexity:**
   - **Simple** — Single file, clear fix, localized change
   - **Complex** — Multi-file, architectural impact, requires investigation

2. **Plan the fix:**
   - Simple: Read the target file, propose changes directly
   - Complex (architectural): Delegate to a code-architect instance with context: the item title, severity, description, the relevant report section text (copy the specific Challenges/Recommendations entry), and any files or components mentioned. The architect designs the fix and returns a proposal.
   - Complex (needs investigation): Delegate to a code-explorer instance with context: the item title, description, suspected files/components, and what needs investigation. The explorer investigates and returns findings for formulating a fix proposal.
   - If delegation fails, fall back to direct investigation using file reading and searching, and propose a simpler fix based on available information.

3. **Present proposal:** Show files to modify, specific changes, and rationale

4. **User approval** — prompt the user to choose:
   - **Apply** — Execute changes, confirm success
   - **Skip** — Record the skip, move to next item
   - **Modify** — User describes adjustments, re-propose the fix (max 3 revision cycles, then must Apply or Skip)

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

If a file modification or creation call fails when applying documentation updates:
1. Retry the operation once
2. If still failing, present the drafted content to the user inline and suggest they apply it manually
3. Continue with the remaining selected files

### Agent Delegation Failures (Step 3c)

If a code-architect or code-explorer delegation fails during actionable insight processing:
1. Fall back to direct investigation using file reading and searching
2. Propose a simpler fix based on available information
3. If the item is too complex to address without agent assistance, inform the user and offer to skip

---

## Agent Coordination

Exploration and synthesis agent coordination is handled by the deep-analysis skill in Phase 1, which uses agent teams with hub-and-spoke coordination. Deep-analysis performs reconnaissance, composes a team plan (auto-approved when invoked by another skill), assembles the team, and manages the exploration/synthesis lifecycle. Refer to the **deep-analysis** skill for team setup, approval flow, and failure handling details.

---

## Report Template

Use this template when presenting analysis findings in Phase 2.

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

{Include a Mermaid architecture diagram (flowchart or C4 Context) showing the major layers/components. Use `classDef` with `color:#000` for all node styles.}

---

## Tech Stack

| Category | Technology | Version (if detected) | Role |
|----------|-----------|----------------------|------|
| Language | {e.g., TypeScript} | {e.g., 5.x} | Primary language |
| Framework | {e.g., Next.js} | {e.g., 16} | Web framework |
| Styling | {e.g., Tailwind CSS} | {e.g., v4} | UI styling |
| Testing | {e.g., Jest} | — | Test runner |
| Build | {e.g., esbuild} | — | Bundler |

{Include only technologies actually detected in config files or code. Omit categories that don't apply.}

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

{Describe how key components connect — limit to 15-20 most significant connections. Use Mermaid flowcharts for both data flows and dependency maps.}

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

- **Exploration agents**: {Number} agents with focus areas: {list}
- **Synthesis**: Findings merged and critical files read in depth
- **Scope**: {What was included and what was intentionally excluded}
- **Cache status**: {Fresh analysis / Cached results from YYYY-MM-DD}
- **Config files detected**: {List of config files found during reconnaissance}
- **Gap-filling**: {Whether direct search investigation was needed after synthesis, and what areas were filled}
```

### Section Guidelines

#### Executive Summary
- Lead with the most important finding, not a generic overview
- Keep to 2-3 sentences maximum
- Include at least one actionable insight

#### Critical Files
- Limit to 5-10 files — these should be the files someone must understand
- Include both the "what" (purpose) and "why" (relevance to analysis context)
- File Details should cover exports, logic, and connections

#### Patterns & Conventions
- Only include patterns that are consistently applied (not one-off occurrences)
- Note deviations from patterns — these are often more interesting than the patterns themselves

#### Relationship Map
- Focus on the most important connections, not an exhaustive dependency graph
- Use directional language (calls, depends on, triggers, reads from)
- Highlight any circular dependencies or unexpected couplings
- **Depth**: Include 2-3 levels of dependency depth
- **Format**: Use Mermaid flowcharts. Apply `classDef` with `color:#000` for readability.
- **Scope limit**: Cap at 15-20 connections. If more exist, group related connections under subsystem labels.

#### Challenges & Risks
- Rate severity based on likelihood and impact combined
- Include specific details, not vague warnings
- Focus on challenges relevant to the analysis context

#### Recommendations
- Make recommendations actionable — "consider" is weaker than "use X for Y"
- **Cite source challenge**: Each recommendation must reference the specific challenge it addresses using the format: _(addresses: {Challenge name})_.
- Limit to 3-5 recommendations to maintain focus

### Adapting the Template

#### For Feature-Focused Analysis
- Emphasize integration points and files that would need modification
- Include a "Feature Implementation Context" section before Recommendations
- Focus Challenges on implementation risks

#### For General Codebase Understanding
- Broader Architecture Overview with layer descriptions
- More extensive Patterns & Conventions section
- Focus Recommendations on areas for improvement or further investigation

#### For Debugging/Investigation
- Emphasize the execution path and data flow
- Include a "Relevant Execution Paths" section
- Focus Critical Files on the suspected problem area

---

## Actionable Insights Template

Use this format when presenting and processing actionable items in Phase 3's "Address Actionable Insights" action.

### Item List Format

Present extracted items grouped by severity, highest first:

```markdown
### High Severity

1. **{Title}** — _{Source: Challenges & Risks}_
   {Brief description of the issue and its impact}

2. **{Title}** — _{Source: Recommendations}_
   {Brief description and rationale}

### Medium Severity

3. **{Title}** — _{Source: Recommendations}_
   {Brief description and rationale}

### Low Severity

4. **{Title}** — _{Source: Other Findings}_
   {Brief description}
```

### Severity Assignment Guidelines

#### From Challenges & Risks Table
- Use the **Severity** column value directly (High, Medium, or Low)
- Title comes from the **Challenge** column
- Description comes from the **Impact** column

#### From Recommendations Section
- Each recommendation in the report should explicitly cite which challenge it addresses (see report template). Use this citation to inherit severity:
  - Recommendation cites a **High** challenge: assign **High**
  - Recommendation cites a **Medium** challenge: assign **Medium**
  - Recommendation cites a **Low** challenge: assign **Low**
- If a recommendation addresses multiple challenges, use the highest severity among them
- If no challenge link is present (legacy reports or standalone recommendations), infer from context or default to **Medium**

#### From Other Findings
- Default to **Low** unless the finding explicitly describes a critical issue
- Only include findings that have a concrete, implementable fix

### Complexity Assessment Criteria

#### Simple (No agent needed)
- Single file change
- Clear, localized fix (rename, add validation, fix import, update config)
- No architectural impact
- Change is self-contained — no cascading modifications needed

#### Complex — Architectural (Delegate to code-architect)
- Requires refactoring across multiple files
- Introduces or changes a pattern (new abstraction, restructured module boundaries)
- Affects system architecture (data flow, component relationships, API contracts)
- Requires design decisions about approach

#### Complex — Investigation Needed (Delegate to code-explorer)
- Root cause is unclear or needs tracing through the codebase
- Multiple potential locations for the fix
- Requires understanding current behavior before proposing changes
- Dependencies or side effects need mapping

#### Effort Estimates

Provide rough effort alongside complexity to help users prioritize:

| Complexity | Typical Effort | Description |
|-----------|---------------|-------------|
| Simple | Low (~minutes) | Single targeted change, clear fix |
| Complex — Architectural | Medium-High (~30min-1hr+) | Multi-file refactoring, design decisions |
| Complex — Investigation | Medium (~15-30min) + varies | Investigation phase + fix implementation |

### Change Proposal Format

Present each proposed fix using this structure:

```markdown
#### {Item Title} ({Severity})

**Complexity:** Simple / Complex (architectural) / Complex (investigation)
**Effort:** Low (~minutes) / Medium (~30min) / High (~1hr+)

**Files to modify:**
| File | Change Type |
|------|-------------|
| `path/to/file` | Edit / Create / Delete |

**Proposed changes:**
{Description of what will change and why. For simple fixes, show the specific code changes. For complex fixes, describe the approach.}

**Rationale:**
{Why this approach was chosen. Reference the original finding.}
```

### Summary Format

After processing all selected items, present:

```markdown
## Actionable Insights Summary

### Items Addressed
| # | Item | Severity | Files Modified |
|---|------|----------|----------------|
| 1 | {Title} | High | `file1.ts`, `file2.ts` |
| 2 | {Title} | Medium | `file3.ts` |

### Items Skipped
| # | Item | Severity | Reason |
|---|------|----------|--------|
| 3 | {Title} | Low | User skipped |

### Files Modified
| File | Changes |
|------|---------|
| `path/to/file` | {Brief description of change} |

**Total:** {N} items addressed, {M} items skipped, {P} files modified
```

### Item Extraction Guidelines
- Only extract items with concrete, actionable fixes — skip vague observations
- **Deduplication criteria** — Merge items that match on any of:
  - Same target file or component mentioned in both items
  - Significant keyword overlap in titles (2+ shared meaningful words)
  - One item is a superset of the other
- When deduplicating, keep the higher severity, merge descriptions, and note both source sections

### Processing Order
- Process items in the order the user selected them, but within that, prioritize by severity
- **Conflict detection** — Before starting fixes, scan the selected items for potential conflicts:
  - **Same-file modifications**: Two items targeting the same file(s) — flag ordering risk
  - **Contradictory changes**: One item adds what another removes, or they modify the same function/component in incompatible ways
  - **Ordering dependencies**: One fix creates a prerequisite for another
- If conflicts are detected, present them to the user before proceeding and suggest a processing order that resolves dependencies

### Revision Cycles
- Maximum 3 revision cycles per item when user selects "Modify"
- After 3 cycles, present final proposal with Apply or Skip only
- Track what the user changed in each cycle to converge on the right fix

## Integration Notes

**What this component does:** Orchestrates a complete codebase analysis workflow from deep exploration through structured reporting to actionable follow-up, producing architecture overviews, critical file maps, and prioritized recommendations.

**Capabilities needed:**
- File reading, file search, and content search (for gap-filling and documentation updates)
- File writing and modification (for saving reports and updating documentation)
- Shell command execution (inherited from deep-analysis for synthesis investigation)
- Agent/sub-task spawning (for deep-analysis team and actionable insight processing)
- User interaction (for action selection, approval flows, and revision cycles)

**Adaptation guidance:**
- This skill depends on the **deep-analysis** skill for Phase 1 exploration. If deep-analysis is unavailable, the reconnaissance and synthesis steps would need to be performed inline.
- The **technical-diagrams** skill is used for Mermaid diagram guidance in reports. If unavailable, diagrams can still be created following the inline styling rules in the report template.
- The actionable insights flow in Phase 3 delegates to **code-architect** and **code-explorer** skills for complex items. If those skills are unavailable, fall back to direct investigation.
- Report and actionable insights templates are inlined in this skill (formerly separate reference files).
