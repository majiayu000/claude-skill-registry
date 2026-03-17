---
name: investigate-create-doc
description: Investigate a codebase topic and produce structured markdown documentation. Collects investigation scope, explores the code, and writes a README plus sub-docs for each area. Use when the user asks to investigate, spike, research, analyze, or document how something works in the codebase.
---

# Investigate & Document

Investigate a codebase topic and produce a structured set of markdown documents with findings.

## Phase 1 — Scope the Investigation

Use AskQuestion to collect:

### 1. Topic

Ask: "What should I investigate?" — free text. Examples:
- "How account context works"
- "All the ways we fetch user data"
- "The authentication flow"

### 2. Context

Ask: "Any context I should know before starting?" — free text, optional. Examples:
- "We're planning to refactor this area"
- "Focus on hooks that query GraphQL"
- "Related to ticket RETIRE-1874"

### 3. Known areas / entry points

Ask: "Any specific files, functions, or areas I should start from?" — free text, optional.

### 4. Directory name

Suggest a kebab-case name derived from the topic. Ask the user to confirm or override.
Output goes to: `docs/{directory-name}/`

---

## Phase 2 — Define Questions (DO NOT INVESTIGATE YET)

The goal of this phase is to understand **what needs to be answered**, not to answer anything.

1. Do a **light** codebase scan — just enough to identify the shape of the problem (file names, export names, rough structure). Do NOT read full files or trace consumers yet.
2. From the topic, context, and light scan, produce a list of **questions that need answering**.
3. Group questions by area/theme. Each group may become a sub-doc later.
4. Write the questions to the README immediately using the "Questions to Answer" section in the template.

**STOP HERE.** Review the questions with the user using AskQuestion.

### Review: one call, all areas

Make a **single** AskQuestion call with an array containing **one question per area**. Each question in the array shows that area's proposed questions and lets the user approve, adjust, or remove it.

```json
AskQuestion({
  "title": "Review Investigation Questions",
  "questions": [
    {
      "id": "area-1",
      "prompt": "Area: {area-1-name}\n\n1. {q1}?\n2. {q2}?\n3. {q3}?",
      "options": ["Looks good", "Adjust (I'll explain)", "Remove this area"]
    },
    {
      "id": "area-2",
      "prompt": "Area: {area-2-name}\n\n1. {q1}?\n2. {q2}?",
      "options": ["Looks good", "Adjust (I'll explain)", "Remove this area"]
    },
    {
      "id": "add-more",
      "prompt": "Any other questions or areas to add?",
      "options": ["No, this covers it — proceed", "Yes, I want to add more (I'll explain)"]
    }
  ]
})
```

If the user says "Adjust" for any area, apply their changes and re-present just that area. If they want to add more, collect the additions and re-confirm.

Only after all areas are confirmed, write the finalized questions to the README and proceed to Phase 3.

---

## Phase 3 — Plan the Investigation

After the user confirms the questions:

1. Map each question group to a sub-doc
2. Decide scope:
   - **Single doc** — if all questions fit in one cohesive document (under ~200 lines of findings)
   - **Multi-doc** — if there are 2+ distinct areas worth their own deep-dive
3. Present the proposed doc structure:

```
docs/{dir-name}/README.md          ← overview, questions, links
docs/{dir-name}/{area-name}.md     ← answers for each area
```

Get confirmation before investigating.

---

## Phase 4 — Investigate Each Area (Parallel Subagents)

**Launch one subagent per area** using the Task tool. Run up to 4 in parallel; queue the rest.

Each subagent receives a self-contained prompt with:
1. The area name and its questions to answer
2. Known entry points / file paths for that area
3. The full context from Phase 1 (topic, background, any user notes)
4. Instructions on what to return

### Subagent prompt template

```
Investigate "{area-name}" in this codebase. Answer these questions:

{paste the questions for this area from the README}

Context: {topic and background from Phase 1}
Entry points: {known files/functions for this area}

For each question, gather evidence by:
- Finding definitions: where the code lives, what it exports
- Tracing dependencies: what it imports/calls/depends on
- Finding ALL consumers: grep for imports, exclude .spec. and .test. files
- Reading each consumer to confirm what specific data it uses
- Checking for overlap: does other code do the same thing differently?
- Noting issues: bugs, tech debt, deprecations, inconsistencies

Return a structured report with:
- A 1-3 sentence Recommendation / TLDR — an opinionated verdict on the area
- A plain-language Definition of the concept/approach (2-4 sentences)
- Deliverables: answer to each question as a heading + answer (Q&A format), with evidence (file paths, code refs, links)
- Pros list — advantages, benefits
- Cons list — disadvantages, risks, tech debt
- Links & References — relevant PRs, docs, external resources
- Related areas that connect to other parts of the investigation
```

Use `subagent_type: "explore"` with thoroughness "very thorough" for each.

### After all subagents return

1. Collect all results
2. Cross-reference findings between areas (look for contradictions or missing connections)
3. Proceed to Phase 5

---

## Phase 5 — Write the Documents

### Directory structure

```
docs/{investigation-name}/
├── README.md                    ← main overview, links to sub-docs
├── {area-1}.md                  ← deep-dive on first area
├── {area-2}.md                  ← deep-dive on second area
└── ...
```

For single-doc investigations, just create `docs/{investigation-name}/README.md`.

### README.md format

Use the template at [templates/readme-template.md](templates/readme-template.md).

Key rules:
- **Summary first** — open with an opinionated, narrative summary (1-3 paragraphs). Lead with the key takeaway or recommendation. Someone who only reads this section should walk away informed.
- **Table of contents** — numbered list linking to each area and Next Steps
- Brief intro paragraph explaining the document's purpose and what prompted it
- **Numbered areas** — each area gets a numbered heading with a description and "Ideas / questions" list
- **Explorations table** — if the investigation is split across people, include an assignment table (Exploration | Description | Suggested Lead)
- **Next Steps** over "Recommendations" — concrete, actionable items
- Link to every sub-doc from each area section
- Cross-link sub-docs to each other where they relate

### Sub-doc format

Use the template at [templates/sub-doc-template.md](templates/sub-doc-template.md).

Key rules:
- **Recommendation / TLDR first** — bold, opinionated conclusion at the top. The reader should know the verdict before reading details.
- **Definition** — plain-language explanation of the concept/approach (2-4 sentences)
- **Deliverables** — answer each question as a heading + answer (Q&A format), not checkboxes
- **Pros / Cons** — separate sections with bullet lists, replacing "Issues & Observations"
- **Links & References** — inline links to PRs, docs, external resources, branches
- Self-contained — readable without the README
- Link back to README and to related sub-docs
- Include code references with file paths where relevant

### Cross-linking

When sub-docs reference each other, use relative links:

```markdown
See [Account Capabilities](./account-capabilities.md) for how capabilities are fetched.
```

In the README, link to each sub-doc:

```markdown
| Area | Document |
|------|----------|
| Account Capabilities | [account-capabilities.md](./account-capabilities.md) |
```

---

## Phase 6 — Review & Finalize

1. Re-read all generated docs for consistency
2. Verify all cross-links are correct
3. Check that every sub-doc is linked from the README
4. Confirm no placeholder text remains
5. Present a summary to the user of what was created
