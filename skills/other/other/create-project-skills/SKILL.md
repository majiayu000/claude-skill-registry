---
name: create-project-skills
description: "Scans an existing codebase and generates project-specific skills that capture inferred conventions such as naming, file organization, framework usage, data access, error handling, and testing style. Writes into the project's chosen skill directory (e.g., `.claude/skills/`, `.agents/skills/`, or a custom path). Use when the user asks to \"extract skills from the codebase\", \"create project skills\", \"infer project conventions as skills\", \"codify patterns as skills\", or \"mine the repo for best practices\"."
---

# Create Project Skills

Generates one skill per detected convention area in the project's skill directory so future Claude or Codex sessions auto-load them when working in the repo.

## Task Tracking

At the start, use `TaskCreate` to create a task for each phase:

1. Survey codebase
2. Extract patterns in parallel
3. Evaluate patterns
4. Propose skill list
5. Run `/create-skill` skill

## Step 1: Survey Codebase

If `$ARGUMENTS` specifies paths, scope the scan to those paths; otherwise scan the whole repository.

Build the extraction context:

1. Detect primary languages and frameworks from manifest files (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Package.swift`, `pom.xml`, `Gemfile`, and others appropriate to the stack).
2. Map the top-level source directory structure and note test directory conventions.
3. Read `CLAUDE.md`, `.claude/rules/`, `AGENTS.md`, and any `.cursor/rules` or `.cursorrules`. Note the conventions already documented there. The generated skills must not duplicate them.
4. Determine the target skill directory:
   - Check candidate paths `.claude/skills/` (Claude Code), `.agents/skills/` (Codex), and a top-level `skills/` directory (match case-insensitively so `Skills/` or similar non-standard casing is detected too). Resolve symlinks so co-linked paths are treated as one logical location.
   - Use `AskUserQuestion` to confirm where generated skills should live. List each distinct resolved location as an option, noting any symlink alias in the option description. If `.claude/skills/` is not among the detected locations, include it as a default option. The auto-added "Other" option lets users specify a custom path such as a project-specific directory.
5. In the chosen target directory, list existing skills. For each, record the skill name, the description from SKILL.md frontmatter, and the first `##` section heading from the body. These signals feed rename-conflict detection in Step 3.

Output a short text summary of detected stack, top-level layout, chosen target directory, and existing skills before moving on.

## Step 2: Extract Patterns in Parallel

Read [references/pattern-extractor.md](references/pattern-extractor.md) to see the full taxonomy of pattern categories. Decide which categories apply to the detected stack (e.g., drop "Styling and UI" for a backend service, drop "State management" for a static-analysis tool).

Use the Agent tool to launch all extraction agents below in a single message (`model: "opus"`, do not set `run_in_background`) so they run concurrently. Launch one Agent per applicable category. Each agent's prompt must:

- Name its assigned category
- Include the stack summary and directory map from Step 1
- Include the list of conventions already documented in `CLAUDE.md` and `.claude/rules/` so duplicates are skipped
- Instruct the agent to read [references/pattern-extractor.md](references/pattern-extractor.md) as its role brief and return findings in the format defined at the end of that file

## Step 3: Evaluate Patterns

Aggregate findings from all agents. For each finding, score three axes:

- **Consistency**: what share of eligible sites follow the pattern? Drop findings below 30%. Flag findings between 30–70% as "mixed" for Step 4 review.
- **Intentionality**: does the pattern appear across multiple subsystems and recent commits, or is it isolated? Drop findings confined to a single legacy module unless docs or lint config explicitly mark them as the desired convention.
- **Modernity**: does the pattern align with current best practices for the stack? Flag patterns that contradict current idioms (e.g., pre-hooks class components in a React codebase also using hooks elsewhere) as "legacy" for Step 4 review.

Group the surviving findings by topic into candidate skills. Each candidate typically covers one category, but related categories may merge if the patterns are tightly coupled. Split a candidate into two skills if its patterns cover clearly distinct sub-topics.

For each candidate skill, produce:

- A proposed `name` (kebab-case, narrow to the topic, e.g., `swift-naming`, `react-state`, `api-clients`)
- A one-line description with trigger phrases (e.g., "Use when writing or reviewing <topic>...")
- 3–8 concrete convention statements with evidence citations (`file:line`)
- A **Status** tag based on disk comparison:
  - **New**: no skill with that name exists in the target directory.
  - **Update**: a skill with the same name exists in the target directory. Produce a unified diff against the current SKILL.md body.
  - **Rename conflict**: an existing skill in the target directory has a name, description, or first-section heading that covers the same topic under a different name. Flag for user decision.

If rename-conflict detection is ambiguous from the Step 1 signals alone, read the existing skill's SKILL.md body and compare convention statements before finalizing the Status tag.

## Step 4: Propose Skill List

Output the full proposal as text first, not inside `AskUserQuestion`. For each candidate skill, show:

- Status tag, proposed name, one-line description
- The 3–8 convention statements with evidence
- For Update status, the unified diff
- For Rename conflict status, the existing skill name and the overlap summary

After all candidates are listed, use `AskUserQuestion` to confirm the proposal with these options: "Approve all", "Make edits", "Cancel". If the user selects "Make edits", continue in conversation so the user can specify which candidates to drop, merge, or rename before returning here.

For each Rename conflict candidate, use a separate `AskUserQuestion` asking whether to update the existing skill, create the new one alongside it, or skip.

## Step 5: Run `/create-skill` Skill

Build the batch from approved candidates only. Do not include anything not explicitly approved in Step 4.

Output all approved candidates (both **New** and **Update** status) as text in a single batch. For each candidate, list the Status tag, proposed name, description, target path `<target-skill-directory>/<name>/SKILL.md`, and the 3–8 convention statements organized under `## <Section>` headings with inline evidence citations (`file_path:line`). These convention statements define the target state the final SKILL.md should match, regardless of whether the skill is being created or updated.

This gives `/create-skill` everything it needs to skip its Step 1 (usage patterns clearly understood) and Step 2 (project skills typically need no additional reusable resources). For Update candidates, `/create-skill` also skips its Step 3 (initialization) per its own "skill already exists, iteration needed" skip rule and iterates on the existing SKILL.md in Step 4 until it matches the target convention statements.

Run the `/create-skill` skill once with this batch in context. Its batch-aware review, evaluation, and apply cycle then runs across all touched skills.

After `/create-skill` completes, output a summary of created and updated skills, grouped by status. If any candidates were dropped or skipped in Step 4, list them so the user knows what was left out.

## Rules

- Each generated skill stays narrow: one topic per skill. Splitting is preferred over bundling.
- Do not duplicate conventions already documented in `CLAUDE.md` or `.claude/rules/`. Reference them instead if needed.
- Generated skills must be self-contained: no cross-skill routing, no references to pipelines that invoke them.
- Descriptions must be third-person and include trigger phrases a future Claude session would match when working on the topic (e.g., "Use when writing or reviewing <tech>...", "Use when editing <layer>...").
