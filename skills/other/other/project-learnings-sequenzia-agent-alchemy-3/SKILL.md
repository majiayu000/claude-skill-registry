---
name: project-learnings
description: Captures project-specific patterns and anti-patterns into the project documentation. Loaded by other skills when they discover project-specific knowledge worth encoding for future sessions.
dependencies: []
---

# Project Learnings

Capture project-specific patterns and anti-patterns into the project's instruction file (e.g., CLAUDE.md). This creates a self-improving feedback loop where discoveries from debugging, development, and review make future sessions smarter.

**Only project-specific knowledge qualifies.** Generic programming advice does not belong in the project instruction file.

---

## Step 1: Evaluate Discovery

Determine if the finding qualifies as project-specific. The finding must pass at least ONE of these criteria:

| Criteria | Example That Qualifies | Example That Doesn't |
|----------|------------------------|----------------------|
| Would a developer unfamiliar with this project likely hit this issue? | "The `processOrder()` function expects amounts in cents, not dollars" | "Always validate function inputs" |
| Is this pattern specific to this codebase's architecture, APIs, or conventions? | "The `UserProfile` type has an optional `metadata` field that is always present at runtime" | "Use TypeScript strict mode" |
| Is it something generic training data wouldn't cover? | "Never call `db.query()` without the `timeout` option — the default is infinite" | "Use async/await instead of callbacks" |

**If NO to all criteria, STOP.** Do not add generic programming knowledge to the project instruction file. Return to the calling skill and report that no project-specific learning was found.

**If YES to any, proceed to Step 2.**

---

## Step 2: Read Existing Project Instruction File

1. **Find the project's instruction file:**
   - Check the repository root first for CLAUDE.md or equivalent
   - If not found, check if there's a project-level `.agents/` directory

2. **Parse existing content:**
   - Understand the existing structure, headings, and conventions
   - Look for sections where this learning would fit (e.g., "Known Gotchas", "Bug Patterns", "Conventions", "Known Challenges")
   - Check for duplicate or similar entries already present

3. **If a similar entry already exists, STOP.** Report to the calling skill that this knowledge is already captured. Do not create duplicates.

4. **Identify placement:**
   - If an appropriate section exists, plan to add the entry there
   - If no appropriate section exists, plan to propose a new section (e.g., `## Known Gotchas` or `## Project-Specific Patterns`)
   - New sections should be placed after the main documentation sections but before appendices or settings

---

## Step 3: Format the Learning

Write a concise, actionable instruction following these rules:

**Format:**
- Use imperative form: "Always validate X before calling Y"
- Include the WHY: "...because the API returns dates as strings, not Date objects"
- Keep it to 1-3 lines
- Follow the existing file style and conventions

**Templates:**

For bug patterns:
```
- **[Area/Component]**: [What to do/avoid] — [why, with specific details]
```

For API gotchas:
```
- `functionName()` in `path/to/file`: [What's surprising about it] — [consequence if ignored]
```

For architectural constraints:
```
- [Constraint description] — [why it exists and what breaks if violated]
```

**Examples of well-formatted learnings:**
- **Order processing**: Always multiply amounts by 100 before passing to `processOrder()` — it expects cents, not dollars
- `db.query()` in `src/database.ts`: Always pass the `timeout` option — the default is infinite and has caused production hangs (30 second timeout recommended)
- Never import from `internal/` directories in `src/api/` — the build system treats these as separate compilation units and circular dependencies will silently break HMR

---

## Step 4: Confirm with User

Prompt the user:

Show:
1. The exact text to be added
2. Where it will be placed in the project instruction file (section name, after which line/entry)
3. Why this qualifies as project-specific

Options:
- **"Add this"** — Write the entry as proposed
- **"Edit before adding"** — User provides modified text, then write that instead
- **"Skip"** — Do not add anything, return to calling skill

---

## Step 5: Write Update

If the user confirmed (or provided edited text):

1. Add the entry to the project instruction file at the identified location
2. If a new section was needed, create the section heading first
3. Verify the edit was applied correctly by reading the modified area
4. Report success to the calling skill with a summary of what was added

If the user chose "Skip":
- Report to the calling skill that the learning was declined
- Do not modify any files

---

## Integration Notes

This skill was converted from the dev-tools plugin package. It is typically loaded by other skills (such as bug-killer and feature-dev) when they discover project-specific knowledge worth encoding for future sessions. No external dependencies are required.
