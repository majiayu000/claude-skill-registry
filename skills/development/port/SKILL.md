---
name: port
description: >
  Port a documentation-driven project to a new target language — initializes project skeleton,
  analyzes reference implementation, and batch-generates plans for selected features. Use when
  converting a project to another language, rewriting in a different language, or creating a
  multi-language SDK from existing feature specs.
---

# Code Forge — Port

Port a project to a new target language by batch-generating implementation plans from shared feature specs.

## When to Use

- Have a documentation project with feature specs (`docs/features/*.md`) and want to implement in a new language
- Have an existing implementation in one language and want to create another language version
- Need to batch-plan multiple features for a new language SDK

## Command Format

```
/code-forge:port @<docs-project> --ref <reference-impl> --lang <target-language>
```

**Example:**
```
/code-forge:port @../apcore --ref apcore-python --lang java
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `@<docs-project>` | Yes | Path to documentation project containing `docs/features/*.md` |
| `--ref <name>` | No | Reference implementation project name (sibling directory) or absolute path |
| `--lang <language>` | Yes | Target language: `java`, `typescript`, `go`, `rust`, etc. |

Missing required parameters → use `AskUserQuestion` to collect interactively.

## Workflow

```
Step 0 → 1 → 2 → 3 → 4 → 5 → 6 (sub-agent loop) → 7 → 8
```

## Context Management

Step 2 and Step 6 are offloaded to sub-agents. Step 2 uses a single sub-agent to analyze the reference implementation. Step 6 dispatches one sub-agent per feature (serial) to generate plans. The main context retains only concise summaries.

## Detailed Steps

### Step 0: Configuration Detection and Loading

@../shared/configuration.md

**Port-specific additions to Step 0:**

- **0.2 additional defaults:** `port.source_docs` = `""`, `port.reference_impl` = `""`, `port.target_lang` = `""`
- **0.4 note:** During Steps 1-4 (before target project exists), config loading runs against the current working directory. After Step 5 creates the target project, subsequent steps use the target project's config.

---

### Step 1: Parse Arguments and Discover Feature Specs

#### 1.1 Resolve Docs Project Path

**1.1.0 Path-Like Input Guard:** If the docs project argument does NOT start with `@` but looks like a path (contains `/`, starts with `.`, or matches an existing directory on disk), use `AskUserQuestion`:

```
Your input looks like a directory path: "{input}"
Did you mean to use @{input}? (directory paths require an @ prefix)
```

- Options:
  - "Yes, use as directory path" → prepend `@` and continue
  - "No, this is not a path" → display usage instructions and stop

Parse the `@<path>` argument:
1. Resolve to absolute path
2. Validate directory exists
3. Look for feature specs at `<docs-project>/docs/features/*.md`
4. If none found, try `<docs-project>/features/*.md`, then `<docs-project>/*.md`
5. If still none: display error with directory contents and stop

Store `docs_project_path` and `feature_specs[]` (list of absolute file paths).

#### 1.2 Resolve Reference Implementation

If `--ref <name>` is provided:
1. Try sibling directory: `<docs-project>/../<name>/`
2. If not found, try as absolute path
3. Validate: directory exists and contains `planning/` with at least one `*/state.json`
4. If invalid: warn `"Reference '{name}' not found or has no planning data. Continuing without reference."` and set `ref_project_path = null`

If `--ref` not provided: set `ref_project_path = null`.

#### 1.3 Resolve Target Language

Validate `--lang` value. Recognized identifiers:
- `java`, `typescript` (alias: `ts`), `go` (alias: `golang`), `rust`, `python`, `csharp` (alias: `cs`), `kotlin`, `swift`
- Unrecognized value: warn and continue (do not reject — new languages are valid)

#### 1.4 Derive Target Project Path

- Default: `<docs-project>/../<docs-name>-<lang>/` (e.g., `../apcore-java/`)
- Display derived path and use `AskUserQuestion`:
  - "Use `{derived-path}` (Recommended)" — proceed
  - "Custom path" — user provides path

#### 1.5 Display Discovery Summary

```
Docs project:      ../apcore (7 feature specs)
Reference impl:    ../apcore-python (planning/ found)
Target language:   java
Target project:    ../apcore-java
```

Proceed directly — no confirmation needed.

---

### Step 2: Analyze Reference Implementation (Sub-agent)

**Skip if `ref_project_path` is null.**

Spawn an `Agent` tool call with:
- `subagent_type`: `"general-purpose"`
- `description`: `"Analyze reference implementation"`

**Sub-agent prompt:**

```
Analyze the reference implementation at {ref_project_path} for a cross-language porting operation.

Read the following files:
1. {ref_project_path}/planning/overview.md — project-level overview with dependency graph
2. All {ref_project_path}/planning/*/plan.md — implementation plans per feature
3. All {ref_project_path}/planning/*/state.json — completion status per feature

Return ONLY a structured summary in this exact format:

REFERENCE_IMPL: {project-name}
REFERENCE_LANG: {detected language from build files or plan content}
OVERALL_STATUS: {completed-count}/{total-count} features complete

DEPENDENCY_ORDER:
- {feature-1} (no deps)
- {feature-2} (depends on: feature-1)
...

PER_FEATURE:
- {feature-name}:
  STATUS: completed | in_progress | pending
  TASK_COUNT: {N}
  KEY_DECISIONS: {2-3 bullet points of important architecture decisions from plan.md}
  LESSONS: {any notable patterns, gotchas, or non-obvious choices}

Keep the summary concise — target ~2-3KB total.
```

**Main context retains:** Only the returned summary. Store as `reference_summary`.

---

### Step 3: Display Feature List and User Selection

Build a feature display table combining discovered specs with reference data (if available).

**With reference:**
```
Feature specs discovered: 7 (from ../apcore/docs/features/)
Reference: apcore-python (7/7 complete)

  #  Feature              Ref Status    Ref Tasks
  1  acl-system           ✅ complete   5 tasks
  2  core-executor        ✅ complete   5 tasks
  3  decorator-bindings   ✅ complete   6 tasks
  4  middleware-system     ✅ complete   4 tasks
  5  observability        ✅ complete   7 tasks
  6  registry-system      ✅ complete   8 tasks
  7  schema-system        ✅ complete   7 tasks
```

**Without reference:**
```
Feature specs discovered: 7 (from ../apcore/docs/features/)

  #  Feature
  1  acl-system
  2  core-executor
  ...
```

Use `AskUserQuestion`:
- Question: "Which features do you want to port to {lang}?"
- First option: "All features (Recommended)" — if selected, set `selected_features` to the full list
- Remaining options: one per feature — if the user wants multiple (but not all), run additional `AskUserQuestion` rounds until they say "done"

Store `selected_features[]`.

---

### Step 4: Confirm Target Tech Stack

Use a **single** `AskUserQuestion` with up to 3 questions based on target language. Skip questions that have obvious single answers.

**For Java:**
- Question 1 — Build tool: "Maven (Recommended)" / "Gradle"
- Question 2 — Java version: "Java 17+ (Recommended)" / "Java 21+" / "Java 11+"
- Question 3 — Test framework: "JUnit 5 (Recommended)" / "TestNG"

**For TypeScript:**
- Question 1 — Runtime: "Node.js (Recommended)" / "Deno" / "Bun"
- Question 2 — Package manager: "pnpm (Recommended)" / "npm" / "yarn"
- Question 3 — Test framework: "Vitest (Recommended)" / "Jest"

**For Go:**
- Question 1 — Go version: "1.21+ (Recommended)" / "1.22+"
- Question 2 — Test extras: "Standard testing (Recommended)" / "testify"

**For Rust:**
- Question 1 — Async runtime: "tokio (Recommended)" / "async-std" / "None (sync only)"
- Question 2 — Serialization: "serde (Recommended)" / "Other"

**For other languages:** Ask a single open-ended question: "What tech stack and key libraries should be used for {lang}?"

Store `tech_stack` decisions.

---

### Step 5: Initialize Target Project Skeleton

#### 5.1 Create Target Directory

1. If target directory already exists:
   - Use `AskUserQuestion`: "Target directory `{path}` already exists."
     - "Update config only (Recommended)" — overwrite `.code-forge.json`, keep everything else
     - "Use as-is" — skip all initialization, jump to Step 6
     - "Cancel" — stop
2. If not exists: `mkdir -p <target-path>`

**Do NOT copy feature specs:** Never copy `docs/features/` or any feature spec files from the docs project into the target project. Feature specs are accessed from the source docs project via relative paths configured in `directories.input`. The target project must NOT contain its own copy of feature specs.

If the user explicitly requests local copies of feature specs, use `AskUserQuestion` to confirm before copying:
- "Copy feature specs locally (creates `docs/features/` in target)" — copy and update `directories.input` to `"docs/features/"`
- "Keep remote references (Recommended)" — do not copy, keep relative path in config

#### 5.2 Generate .code-forge.json

Write to `<target-path>/.code-forge.json`:

```json
{
  "_tool": {
    "name": "code-forge",
    "description": "Transform documentation into actionable development plans with task breakdown and status tracking",
    "url": "https://github.com/tercel/code-forge"
  },
  "directories": {
    "base": "./",
    "input": "<relative-path-to-docs>/docs/features",
    "output": "planning/"
  },
  "reference_docs": {
    "sources": ["<relative-path-to-ref>/planning/*/plan.md"]
  },
  "port": {
    "source_docs": "<relative-path-to-docs>",
    "reference_impl": "<relative-path-to-ref>",
    "target_lang": "<lang>"
  },
  "execution": {
    "default_mode": "ask",
    "auto_tdd": true,
    "task_granularity": "medium"
  }
}
```

Use relative paths from the target project to the docs and reference projects.

If no reference: omit `reference_docs.sources` and `port.reference_impl`.

#### 5.3 Generate Project Skeleton (Sub-agent)

Spawn an `Agent` sub-agent (`subagent_type: "general-purpose"`):

**Sub-agent prompt:**

```
Initialize a {lang} project skeleton at {target_path}.

Project name: {project-name}
Language: {lang}
Tech stack: {tech_stack decisions from Step 4}

Create the following files:
1. Build file — {pom.xml | package.json | go.mod | Cargo.toml | etc.} with project metadata and minimal dependencies
2. .gitignore — language-appropriate patterns
3. README.md — minimal: project name, one-line description ("apcore SDK for {lang}"), link to docs project

Do NOT create src/ or test/ directories — those are created by feature tasks during implementation.
Do NOT copy docs/features/ or any feature spec files into this project.

You MUST create all three files listed above (build file, .gitignore, README.md). Return the list of files created.
```

**Verify skeleton files:** After sub-agent completes, check that the following files exist in `{target_path}`:
- Build file (`pom.xml` / `package.json` / `go.mod` / `Cargo.toml` / etc.)
- `.gitignore`
- `README.md`

If any are missing, create them directly in the main context. Do NOT skip this verification.

Also verify that `docs/features/` does NOT exist in the target project. If it was created, delete it immediately.

#### 5.4 Initialize Git Repository

```bash
cd <target-path> && git init && git add . && git commit -m "chore: initialize {project-name} project skeleton"
```

Only if not already a git repo.

---

### Step 6: Batch Generate Plans (Sub-agent per Feature, Serial)

Process each selected feature in order. Use dependency order from Step 2 reference summary if available; otherwise alphabetical.

#### 6.0 Display Batch Header

```
Generating plans for {count} features...
```

#### 6.1 Per-Feature Loop

For each feature in `selected_features[]`:

**6.1.1 Check Existing Plan**

If `<target>/planning/<feature>/state.json` exists:
- Display: `[{i}/{total}] {feature} — skipped (plan already exists)`
- Continue to next feature

**6.1.2 Create Feature Directory**

```
mkdir -p <target>/planning/<feature>/tasks/
```

**6.1.3 Dispatch Plan Sub-agent**

Spawn an `Agent` sub-agent (`subagent_type: "general-purpose"`):

**Sub-agent prompt:**

```
Generate an implementation plan for porting the "{feature}" feature to {lang}.

## Input
- Feature spec: {docs_project_path}/docs/features/{feature}.md (read this file)
- Target project: {target_path}
- Target language: {lang}
- Tech stack: {tech_stack}
{if type_mapping_exists:}
- Type mapping reference: {docs_project_path}/docs/spec/type-mapping.md (read this file for cross-language type translations)
{end if}

## Reference Context (from existing {ref_lang} implementation)
{reference_summary — the per-feature section for this feature from Step 2}

## Output Files
Write ALL of the following files:

### 1. {target}/planning/{feature}/plan.md
Required sections:
- **Goal** — one sentence
- **Architecture Design** — component structure, data flow, technology choices with rationale
- **Task Breakdown** — mermaid dependency graph + task list with estimated time and dependencies
- **Risks and Considerations** — technical challenges
- **Acceptance Criteria** — checklist
- **References** — related docs

Ensure the plan uses {lang}-idiomatic patterns (not a line-by-line translation of the reference).

**Task ID naming:** Task IDs must be descriptive names **without numeric prefixes**. Use `setup`, `models`, `api` — NOT `01-setup`, `02-models`. Execution order is defined in overview.md, not by filename ordering.

### 2. {target}/planning/{feature}/tasks/{name}.md (one per task)
Each task file must include:
- **Goal** — what this task accomplishes
- **Files Involved** — files to create/modify
- **Steps** — numbered, TDD-first (write tests → run → implement → verify), with {lang}-specific commands and code examples
- **Acceptance Criteria** — checklist
- **Dependencies** — depends on / required by
- **Estimated Time**

**Naming (critical):** Use descriptive filenames — `setup.md`, `models.md`, `api.md`. **NO numeric prefixes** (`01-setup.md`, `02-models.md` are WRONG). Execution order is controlled by `overview.md` Task Execution Order table and `state.json`, never by filename ordering.

### 3. {target}/planning/{feature}/overview.md
Sections:
- **Overview** — feature summary
- **Scope** — included/excluded
- **Technology Stack** — language, framework, key deps, test tools
- **Task Execution Order** — table: #, Task File, Description, Status
- **Progress** — counts
- **Reference Documents** — link to source spec

## Return Format
Return ONLY a concise summary:
FEATURE: {feature}
STATUS: planned
TASK_COUNT: <N>
TASKS:
- <id>: <title> (~<estimate>)
EXECUTION_ORDER: <id1>, <id2>, ...
```

**6.1.3.1 Verify Plan Output**

After sub-agent completes, verify the following files were created:
- `{target}/planning/{feature}/plan.md` — must exist and be non-empty
- `{target}/planning/{feature}/tasks/` — must contain at least one `.md` file
- `{target}/planning/{feature}/overview.md` — must exist and be non-empty

If any file is missing, this is a sub-agent failure. Follow the error handling in 6.2 (display failure, ask user to skip/retry/stop). Do NOT proceed to state.json creation with missing plan files.

**6.1.4 Initialize state.json**

After sub-agent completes, parse its summary and create `<target>/planning/<feature>/state.json`:

```json
{
  "feature": "{feature}",
  "created": "{ISO timestamp}",
  "updated": "{ISO timestamp}",
  "status": "pending",
  "execution_order": ["{id1}", "{id2}", "..."],
  "progress": {
    "total_tasks": {N},
    "completed": 0,
    "in_progress": 0,
    "pending": {N}
  },
  "tasks": [
    {
      "id": "{task-id}",
      "file": "tasks/{task-id}.md",
      "title": "{task-title}",
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "assignee": null,
      "commits": []
    }
  ],
  "metadata": {
    "source_doc": "{relative-path-to-feature-spec}",
    "created_by": "code-forge:port",
    "version": "1.0",
    "ported_from": {
      "reference_impl": "{ref-project-name or null}",
      "reference_lang": "{ref-lang or null}",
      "target_lang": "{lang}"
    }
  }
}
```

**6.1.5 Display Progress**

```
[{i}/{total}] {feature} planned ({task_count} tasks, ~{estimate})
```

#### 6.2 Error Handling

If a sub-agent fails for a feature:
- Display: `[{i}/{total}] {feature} — FAILED: {error summary}`
- Use `AskUserQuestion`: "Feature planning failed."
  - "Skip and continue" — mark as skipped, continue to next feature
  - "Skip all future failures" — auto-skip any remaining failures without prompting
  - "Retry" — re-dispatch sub-agent
  - "Stop" — exit the batch loop

---

### Step 7: Generate Project Overview

@../shared/overview-generation.md

Scan `<target>/planning/*/state.json` and generate `<target>/planning/overview.md`.

Display: `Project overview generated: planning/overview.md`

---

### Step 8: Display Results and Next Steps

```
Port completed!

Target project: {target_path}
Features planned: {planned}/{selected} ({skipped} skipped)
Total tasks: {total_task_count}

Feature Summary:
  #  Feature              Tasks  Estimated
  1  schema-system        7      ~14h
  2  core-executor        5      ~10h
  ...

Next steps:
  cd {target_path}
  /code-forge:status                         View project dashboard
  /code-forge:impl {first-feature}           Start implementing first feature
```

## Coordination with Other Skills

- **After port:** `cd` to target project, use `/code-forge:impl {feature}` to execute tasks
- **With /code-forge:status:** View overall progress across all ported features
- **With /code-forge:review:** Review completed features
- **With /code-forge:fixbug:** Debug issues in ported code
- Port does NOT invoke impl — the user controls when to start implementation

## Notes

1. **Serial execution:** Features are planned one at a time for cross-feature consistency and user control
2. **Reference is optional:** Port works without `--ref`, just without architecture reference context
3. **Idiomatic porting:** Sub-agents are instructed to use target-language idioms, not translate line-by-line
4. **Type mapping:** If `docs/spec/type-mapping.md` exists in the docs project, it's provided to sub-agents for cross-language type translation guidance
5. **Resumable:** Re-running port skips features that already have `state.json` — safe to resume after interruption
6. **Standard output:** Generated plans are indistinguishable from regular `/code-forge:plan` output — all downstream skills work unchanged
