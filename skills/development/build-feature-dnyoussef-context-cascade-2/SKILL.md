---
name: build-feature
description: Build feature command
allowed-tools:
- Read
- Write
- Edit
- Bash
- Glob
- Grep
- Task
- TodoWrite
model: claude-3-5-sonnet
x-version: 1.1.0
x-category: delivery
x-vcl-compliance: v3.1.1
binding: skill:build-feature
category: delivery
---



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## STANDARD OPERATING PROCEDURE

### Purpose
- Primary action: Build feature command

### Trigger Conditions
- Command syntax: /build-feature [args]
- Ensure prerequisites are met before execution.

### Inputs and Options
- Inputs: No structured parameters defined; capture user intent explicitly.

### Execution Phases
1. Review the request and confirm scope.
2. Execute the command flow.
3. Summarize outcomes and next actions.

### Success Criteria and Outputs
- Document artifacts, decisions, and follow-up actions clearly.

### Error Handling and Recovery
- If execution fails, capture the failure mode, retry with verbose context, and surface actionable remediation steps.

### Chaining and Coordination

### Memory and Tagging
- Tag session outputs with who/when/why for traceability.

### LEARNED PATTERNS (Session: 2026-01-07)

#### Asset Selection Protocol
When multiple similar assets exist (e.g., headshot.jpg vs headshot.png):
1. List all candidates with visual inspection or metadata check
2. Confirm correct asset with user before implementation
3. Document reasoning for selection

#### Feature Restoration vs New Feature
For "restore", "add back", or "bring back" requests:
1. FIRST: Research git history to find original implementation
   ```bash
   git log --all --oneline -- <file>
   git show <commit>:<file>
   ```
2. Extract working implementation patterns from historical commits
3. Apply proven patterns to current codebase
4. AVOID: Reinventing solutions that previously worked

For NEW features:
1. Check if similar patterns exist in codebase
2. Follow established conventions (grid layouts, component structure)
3. Iterate with user feedback

#### Layout Implementation Strategy
- Hero sections with text + image -> Grid-based layout (lg:grid-cols-12)
- Card layouts -> Consistent spacing and responsive breakpoints
- If >3 positioning iterations needed -> STOP and research existing patterns or ask for design reference

#### User Frustration Signals
Phrases like "this is getting sad", "stop", "reverse all changes" indicate:
- Trigger: Immediate rollback + strategy pivot required
- Response: Research historical solutions or ask for design reference
- Never continue iterating after frustration signals

### Example Invocation
- /build-feature example

### Output Format
- Provide a concise summary, actions taken, artifacts generated, and recommended next steps.
- Always include an explicit confidence line: "Confidence: X.XX (ceiling: TYPE Y.YY)".
- Use ceilings — inference/report: 0.70, research: 0.85, observation: 0.95, definition: 0.95.
- Keep user-facing output in plain English; reserve VCL markers for the appendix only.

Confidence: 0.86 (ceiling: observation 0.95) - SOP rewritten to Prompt-Architect pattern based on legacy command content.

---

## VCL COMPLIANCE APPENDIX (Internal Reference)

[[HON:teineigo]] [[MOR:root:PA]] [[COM:PromptArchitect]] [[CLS:ge_command]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[SPC:path:/commands]]
[define|neutral] CONFIDENCE_CEILINGS := {inference:0.70, report:0.70, research:0.85, observation:0.95, definition:0.95} [conf:0.9] [state:confirmed]
[direct|emphatic] L2_LANGUAGE := English; user-facing outputs exclude VCL markers. [conf:0.99] [state:confirmed]
[commit|confident] <promise>BUILD_FEATURE_VERILINGUA_VERIX_COMPLIANT</promise> [conf:0.88] [state:confirmed]