---
name: plan:findings:resume
description: Triage findings from a plan into issues and research. Reads findings/ from a plan directory, decides what becomes an issue or research update, and writes them to the appropriate locations.
allowed-tools: Bash(git log:*), Bash(git diff:*)
---

# Plan Findings Resume Skill

Triage findings recorded during plan implementation into issues and research updates.

## Process

1. **Identify the target plan:**

   - If the user provides a plan number (e.g., `/plan:findings:resume 0018`), use that plan directly: `plans/NNNN-*/`
   - If no number is provided, scan for plans with findings:
     - Look for `plans/*/findings/` directories (exclude `plans/archive/`)
     - Read `.plan-state.json` for each to check status
     - If one plan has findings, use it
     - If multiple plans have findings, list them and ask the user to choose:
       ```
       Found findings in multiple plans:

       1. `plans/0018-lr-rl-remaining-fixes/` - 4 findings (in_progress)
       2. `plans/0020-edge-routing/` - 2 findings (in_progress)

       Which plan's findings should I triage?
       ```
     - If no plans have findings, report that and suggest `/plan:findings:create`

2. **Read all findings:**
   - Read every `.md` file in `plans/NNNN-name/findings/`
   - Parse the finding metadata: Type, Task, Date
   - Group findings by type: discovery, diversion, plan-error, note, todo, cleanup

3. **Present findings summary to the user:**
   ```
   **Plan:** `plans/NNNN-feature-name/`
   **Findings:** N total

   | # | Finding | Type | Task | Proposed Action |
   |---|---------|------|------|-----------------|
   | 1 | Short title | todo | 2.1 | Issue |
   | 2 | Short title | discovery | 1.3 | Research update |
   | 3 | Short title | note | 3.1 | No action needed |

   **Proposed actions:**
   - **Issues (N):** Findings 1, 4, 5 → new issue set `issues/NNNN-description/`
   - **Research (N):** Finding 2 → update `research/NNNN-topic/`; Finding 6 → new research
   - **No action (N):** Findings 3, 7 — informational only

   Should I proceed with these actions? You can adjust any finding's disposition.
   ```

4. **Wait for user approval** before creating any issues or research.

5. **Create issues** from findings that warrant them:

   - Find the next issue set number by checking `issues/` for the highest `NNNN-*` prefix
   - Create `issues/NNNN-kebab-description/` directory
   - Write `issues.md` index file with:
     - Summary of how issues were identified (from plan findings)
     - Issue index table linking to individual issue files
     - Categories grouping related issues
     - Cross-references back to the source plan and findings
   - Create `issues/issues/` subdirectory with individual issue files
   - Each issue file includes:
     - Severity, category, status (Open)
     - Description derived from the finding
     - Reproduction steps (from finding details or plan context)
     - Link back to the source finding: `plans/NNNN-name/findings/finding-name.md`
   - Follow the format conventions in `issues/CLAUDE.md`

6. **Route research findings** to the appropriate location:

   For each finding that warrants research:

   **Update existing research** if the finding relates to an active or archived research topic:
   - Scan `research/NNNN-*/research-plan.md` and `research/archive/NNNN-*/research-plan.md` for topic matches
   - If a matching research directory exists and is active (`research/NNNN-*/`):
     - Add a new findings file: `research/NNNN-topic/from-plan-MMMM-description.md`
     - Use the standard research findings format (Summary, Where, What, How, Why, Key Takeaways)
     - Note the source: "Discovered during implementation of plan MMMM"
   - If the matching research is archived:
     - Note this in the output — the user may want to create follow-up research

   **Create new research** if the finding opens a new topic not covered by existing research:
   - Find the next research number by checking both `research/` and `research/archive/`
   - Create `research/NNNN-topic-name/` with a research plan
   - Follow `research/CLAUDE.md` conventions
   - Set status to `PLANNED` — the user can run `/research:resume` to investigate

7. **Report results:**
   ```
   **Findings triage complete for plan NNNN:**

   **Issues created:** `issues/NNNN-description/`
   - Issue 01: [title] (High)
   - Issue 02: [title] (Medium)

   **Research updated:** `research/NNNN-topic/`
   - Added: `from-plan-MMMM-description.md`

   **Research created:** `research/NNNN-new-topic/`
   - Status: PLANNED — run `/research:resume` to investigate

   **No action:** 2 findings (informational)

   **Source:** `plans/MMMM-name/findings/` (N findings triaged)
   ```

## Finding Type → Action Mapping

These are defaults — the user can override any finding's disposition:

| Finding Type | Default Action | Rationale |
|-------------|---------------|-----------|
| `todo` | Issue | Deferred work needs tracking |
| `cleanup` | Issue | Technical debt needs tracking |
| `plan-error` | Research update or issue | Incorrect assumptions may need investigation or just a fix |
| `discovery` | Research update | New understanding should feed back to research |
| `diversion` | Note in issue or research | Document why the plan changed |
| `note` | No action | Informational, already captured in findings |

## Example Output

---

**Plan:** `plans/0020-edge-routing/`
**Findings:** 5 total

| # | Finding | Type | Task | Proposed Action |
|---|---------|------|------|-----------------|
| 1 | Diamond nodes need special attachment logic | discovery | 2.1 | Research update → `research/0013-visual-comparison-fixes/` |
| 2 | Router doesn't handle 3+ waypoints | todo | 3.2 | Issue (High) |
| 3 | Plan assumed edges sorted by rank | plan-error | 2.3 | Issue (Medium) |
| 4 | Refactored render_edge to take PathSegment | diversion | 3.1 | No action |
| 5 | Need to revisit label placement after routing | todo | 3.4 | Issue (Low) |

**Proposed actions:**
- **Issues (3):** Findings 2, 3, 5 → new issue set `issues/0003-edge-routing-findings/`
- **Research (1):** Finding 1 → update `research/0013-visual-comparison-fixes/`
- **No action (1):** Finding 4 — informational diversion

Should I proceed with these actions?

---
