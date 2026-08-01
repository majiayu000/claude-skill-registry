---
name: site-visit-report
description: Create a typed, source-linked site visit report from field notes, photos, files, or conversation. Use for site observations, field reports, walkthrough records, existing-condition visits, and follow-up capture. Separate direct observations, participant-reported information, interpretation, limitations, issues, and proposed follow-ups. Saving a report never changes PROJECT.md, decisions/, or TASKS.md; promote only user-selected items afterward.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /as:site-visit-report — Typed Field Evidence

Create an auditable record of a site visit without turning limited observation, hearsay, or interpretation into verified professional conclusions.

## Usage

```text
/as:site-visit-report from field-notes/2026-07-21.md
/as:site-visit-report document today's walkthrough and attached photos
/as:site-visit-report revise site-reports/2026-07-21-roof-walkthrough.md
```

## Hard rules

1. **Classify every substantive item.** Keep direct observations, participant-reported information, interpretation, issues, and proposed follow-ups separate.
2. **State the observation boundary.** Record access, visibility, weather, destructive-testing, equipment, and document limitations. An inaccessible or concealed area is `Not observed`, never “no issue observed.”
3. **Do not claim concealed-condition certainty.** Report only visible conditions within the stated visit scope. Do not infer what is behind finishes, underground, inaccessible, or otherwise concealed.
4. **Do not claim compliance.** Never declare code, zoning, life-safety, structural, MEP, accessibility, environmental, or contractual compliance. Route analysis to the appropriate specialist workflow and licensed professional.
5. **Save before promotion.** Complete and save the report before offering follow-up. Saving must not create or modify `PROJECT.md`, `decisions/*.md`, or `TASKS.md`.
6. **Promote item by item.** Require exact labels for every proposed fact, durable decision, or task; approval of the report as a whole is not promotion approval.
7. **Preserve dates and provenance.** Distinguish visit date, created date, source date, and photo/file metadata. Store project-relative links rather than absolute machine paths.
8. **Never overwrite implicitly.** Use deterministic numeric suffixes for collisions. Revise an existing report only when the user explicitly requests that exact revision.
9. **Do not fabricate gaps.** Unknown participants, locations, dates, conditions, photo identities, owners, or due dates remain `Unknown`, `Not recorded`, or `Not observed`.

## Step 1 — Resolve the project root

Run the shared resolver and follow `skills/project/references/context-resolution.md`. Resolve exactly one validated project before reading sources or choosing a target. A `studio-picker` result requires one structured project-selection gate; do not ask first in prose. Stop on `invalid`, `no-projects`, or `no-context`. Resolve all inputs, the report target, and links relative to the selected project.

## Step 2 — Establish visit scope, sources, and dates

Read the supplied notes, photos, drawings, files, and relevant conversation. Preserve each input as a project-relative source reference. For a conversational source, record `Current conversation (not separately archived)`.

Determine independently:

- **Visit date:** when the visit occurred. Prefer an explicit source or user date. Ask when unavailable because it controls the canonical filename.
- **Created date:** when this artifact is written.
- **Visit purpose and scope:** why the visit occurred and which locations or systems were intended for observation.
- **Participants:** people present and their roles, only when supported.
- **Conditions:** weather, lighting, occupancy, access, or active work that materially affected observation.

Never infer the visit date from file metadata. Treat photo timestamps and filesystem modification times as metadata, not proof of the visit date.

## Step 3 — Classify the evidence

Assign stable labels and do not merge categories:

- `O1`, `O2` — **direct observations:** what was visible or otherwise directly perceived, with location and source/photo references.
- `R1`, `R2` — **participant-reported information:** what someone stated, attributed when known, and marked `Reported; not independently verified`.
- `I1`, `I2` — **interpretations:** a limited inference from identified observations, explicitly marked as interpretation and never presented as fact or compliance analysis.
- `ISS1`, `ISS2` — **issues:** conditions requiring review, clarification, testing, or action; state urgency only when the source supports it.
- `F1`, `F2` — **proposed follow-ups:** candidate actions, with proposed owner and due date when known; not canonical tasks until selected through `/as:tasklist`.

Link photographs and files to the exact item they support. Do not describe an image you cannot inspect. Do not use a participant statement to populate Direct Observations, even when the statement seems plausible. A contractor statement that a wall is non-load-bearing remains participant-reported and unverified; it is not a structural finding.

For each inaccessible, obscured, untested, or concealed area relevant to the visit, record a specific limitation. Absence of an observation is not evidence of absence.

## Step 4 — Write a collision-safe report

Use:

```text
site-reports/YYYY-MM-DD-<descriptive-slug>.md
```

Use the visit date in the filename. Resolve and show the exact project-relative target. If it exists:

- When the user explicitly asked to revise that exact report, preserve the original visit date, **Created** date, and sources; set **Updated** to today and add a concise revision note.
- Otherwise preserve the existing file and select the next available suffix: `-02`, `-03`, and so on. Check the suffixed path before writing. Never overwrite merely because date and title match.

Resolve the bundled template relative to the loaded `skills/site-visit-report/SKILL.md` when the harness exposes that path. On Claude Code, `${CLAUDE_PLUGIN_ROOT}/skills/site-visit-report/templates/site-visit-report.md` is the fallback. If bundled resources are unavailable, reproduce every section required by Step 3 plus visit metadata, sources, photos/files, limitations, and the disclaimer behavior below.

Write the complete report and confirm its saved path. At this point stop all other mutation and verify that `PROJECT.md`, `decisions/`, and `TASKS.md` were not changed by saving the report.

## Step 5 — Apply the professional boundary

Append the canonical disclaimer block at the very end when either condition is true:

- the report is client-facing, authority-facing, issued externally, or may reasonably be submitted to a client or authority; or
- the artifact includes regulated analysis or conclusions involving code, zoning, occupancy, life safety, structural or MEP adequacy, accessibility, environmental risk, or similar professional judgment.

If uncertain whether the report will be submitted externally, include it. A purely internal administrative draft containing observations, logistics, photo references, and follow-up coordination—but no regulated conclusion—may omit it. Omission does not relax the concealed-condition, certainty, or compliance prohibitions.

When the bundled rule is available, read `rules/professional-disclaimer.md`. Otherwise use this exact fallback as the final content, with one blank line between the block and marker:

> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->

The marker is a terminal sentinel. Do not place anything after it.

## Step 6 — Preview optional promotions

After saving, present separate candidate lists:

1. **Potential project facts:** selected observations that may warrant verification and entry through `/as:project remember`. Do not propose reported information or interpretation as verified facts.
2. **Durable decisions:** an explicitly documented choice, if any, suitable for `/as:project record-decision`; observations and issues are not decisions.
3. **Canonical tasks:** selected `F#` follow-ups suitable for `/as:tasklist`.

Explain that no downstream record has changed. Require exact item labels such as `O2, F1`, or none. Before handoff, search the owning record for the same project-relative report link and item label; when found, show it and offer link/update/new rather than silently duplicating it. Do not promote unselected siblings.

## Step 7 — Hand off without hard dependencies

When direct skill invocation exists, invoke the owning skill once per selected record type and pass the report path and exact labels. The destination skill owns confirmation and mutation.

When direct invocation is unavailable, leave the report intact and print only applicable copyable commands in this form:

```text
/as:project remember selected verified observation O2 from site-reports/2026-07-21-roof-walkthrough.md; preserve the source backlink and verify it before recording as a project fact
/as:project record-decision selected durable choice from site-reports/2026-07-21-roof-walkthrough.md; preserve the exact source item label and backlink
/as:tasklist import selected follow-ups F1, F3 from site-reports/2026-07-21-roof-walkthrough.md; preview duplicates and changes before writing
```

If nothing is selected, finish with the site report only.
