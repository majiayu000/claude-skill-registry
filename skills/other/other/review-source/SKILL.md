---
name: review-source
description: Source code health assessment. Dispatches language-specific SMEs to evaluate idiomatic usage, consistency, and quality across all project languages. Advisory only — no changes made.
model: opus
---

# Source Review - Code Health Assessment

Advisory-only assessment of source code health across all languages in the project. Dispatches language-specific SME agents to evaluate idiomatic usage, consistency, modernness, and quality. For languages without a specialist, a generalist reviews for common issues. Produces a consolidated health report — no changes are made.

## Philosophy

**Diagnostic, not therapeutic.** This skill assesses health. It does not fix anything. Use `/refactor` to act on findings.

**Summary over specifics.** Each reviewer produces a narrative assessment, not a line-by-line audit. The goal is to answer "how healthy is this code?" — not "what are all the issues?"

**Specialist when possible, generalist otherwise.** Languages with SME agents get expert review. Languages without SMEs still get reviewed — a generalist can catch structural problems, inconsistencies, and obvious anti-patterns even without deep language expertise.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                  SOURCE REVIEW                       │
├──────────────────────────────────────────────────────┤
│  1. Detect languages in project                      │
│  2. User selects which languages to review           │
│  3. Dispatch review agents (parallel)                │
│     ├─ SME agent for supported languages             │
│     └─ Generalist for unsupported languages          │
│  4. Aggregate and present health report              │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Detect Languages

Scan the project (or user-specified scope) for source files. Map file extensions to languages and identify SME availability:

| Extensions                     | Language   | SME Agent              |
|--------------------------------|------------|------------------------|
| `.go`                          | Go         | `SWE - SME Golang`     |
| `.zig`                         | Zig        | `SWE - SME Zig`        |
| `.js`, `.mjs`, `.cjs`          | JavaScript | `SWE - SME JavaScript` |
| `.ts`, `.tsx`, `.mts`, `.cts`  | TypeScript | `SWE - SME TypeScript` |
| `.html`, `.htm`                | HTML       | `SWE - SME HTML`       |
| `.css`                         | CSS        | `SWE - SME CSS`        |
| `.graphql`, `.gql`             | GraphQL    | `SWE - SME GraphQL`    |
| `Dockerfile`, `Dockerfile.*`   | Docker     | `SWE - SME Docker`     |
| `Makefile`, `*.mk`             | Makefile   | `SWE - SME Makefile`   |

**Ansible detection:** Only classify `.yml`/`.yaml` files as Ansible if `ansible.cfg` exists or Ansible directory structures are present (`roles/`, `playbooks/`, `inventory/`, `group_vars/`, `host_vars/`). If detected, the Ansible SME is `SWE - SME Ansible`. Generic YAML config files are not a reviewable language.

**All other recognized source languages** (Python, Rust, Java, Ruby, C, C++, Shell, etc.) are detected but flagged as having no specialist available.

**Exclude from detection:**
- Generated/vendored directories (`vendor/`, `node_modules/`, `dist/`, `build/`, `.git/`)
- Binary files
- Data files (JSON, YAML config, TOML, CSV, etc.) — unless they are a build/automation language (Makefile, Dockerfile, Ansible)

Present detected languages to the user with file counts and SME availability:

```
Detected languages:
  1. Go (42 files) — SME available
  2. TypeScript (18 files) — SME available
  3. Python (15 files) — no specialist available
  4. Shell (8 files) — no specialist available
  5. CSS (5 files) — SME available
  6. Makefile (1 file) — SME available

Which languages would you like to review? (default: all)
```

### 2. User Selection

Accept the user's selection. Default: review all detected languages.

Also ask about scope if not already determined:
- Default: entire codebase (version-controlled files only)
- User may narrow to specific directories or modules

### 3. Dispatch Reviews

Spawn one agent per selected language, **in parallel**.

**For languages with an SME,** spawn the corresponding SME agent with:

```
You are reviewing [LANGUAGE] code in this project — advisory only. Do NOT
make any changes.

Scope: [SCOPE]

Read all [LANGUAGE] files within scope and produce a health assessment
covering:

1. **Idiomatic usage** — Does the code follow [LANGUAGE] conventions and
   community best practices? Would an experienced [LANGUAGE] developer
   feel at home?
2. **Consistency** — Are patterns, naming conventions, and style consistent
   across files? Or does it look like multiple authors with different habits?
3. **Modernness** — Is the code using current [LANGUAGE] features, or
   relying on legacy/deprecated patterns?
4. **Error handling** — Is error handling appropriate, consistent, and
   complete?
5. **Complexity** — Are there areas of unnecessary complexity that hurt
   readability or maintainability?
6. **Code organization** — Are files well-structured internally? Reasonable
   sizes? Logical grouping?

Produce your assessment in this format:

HEALTH: [Excellent / Good / Fair / Poor]

SUMMARY:
[2-4 paragraph narrative assessment covering the dimensions above. Do NOT
enumerate individual findings — describe patterns and overall quality.
Highlight the 2-3 most significant concerns if any exist.]

REFACTORING RECOMMENDED: [No / Minor — not urgent / Yes — moderate priority / Yes — high priority]

RELATED REVIEWS: [Optional — note if /review-arch, /review-test, or other
skills would be particularly valuable based on what you observed. Only
mention if clearly warranted.]
```

**For languages without an SME,** spawn a `general-purpose` agent with:

```
You are reviewing [LANGUAGE] code in this project — advisory only. Do NOT
make any changes. Note: no [LANGUAGE] specialist is available, so this is
a generalist review.

Scope: [SCOPE]

Read all [LANGUAGE] files within scope and produce a health assessment
covering:

1. **Code quality** — Is the code well-written? Clear naming, reasonable
   structure, appropriate abstraction level?
2. **Consistency** — Are patterns, naming, and style consistent across
   files?
3. **Error handling** — Is error handling present and reasonable?
4. **Complexity** — Are there areas of unnecessary complexity?
5. **Obvious issues** — Any clear anti-patterns, dead code, or structural
   problems visible to a non-specialist?

Note: As a generalist, you may miss language-specific idioms or best
practices. Focus on universal code quality dimensions.

Produce your assessment in this format:

HEALTH: [Excellent / Good / Fair / Poor]

SUMMARY:
[2-4 paragraph narrative assessment. Describe patterns and overall quality.
Highlight the 2-3 most significant concerns if any exist. Note any areas
where a specialist review would add value.]

REFACTORING RECOMMENDED: [No / Minor — not urgent / Yes — moderate priority / Yes — high priority]
```

### 4. Aggregate and Present

Collect all agent responses. Present a consolidated health report:

```
## Source Health Report

### Go (42 files) · SME review
**Health: Good**

[SME's summary]

**Refactoring recommended:** Minor — not urgent

---

### Python (15 files) · Generalist review (no specialist available)
**Health: Fair**

[Generalist's summary]

**Refactoring recommended:** Yes — moderate priority

---

### Overall Assessment

[Your synthesis — not a repetition of the individual summaries. Look for
cross-language patterns: if multiple reviewers flag the same concern (e.g.,
inconsistent error handling), call it out as a project-level issue. If
everything is healthy, say so concisely.]

### Suggested Next Steps

[Based on findings, recommend specific skills:
- /refactor — if any language needs refactoring
- /review-arch — if structural concerns were noted across languages
- /review-test — if test quality concerns were noted
- "No action needed" — if the codebase is healthy]
```

**The overall assessment is your synthesis.** Look for patterns across languages. If three reviewers all note inconsistent error handling, that's a project-level concern. If every reviewer reports healthy code, don't belabor it.

## Agent Coordination

- All review agents run **in parallel** (they are read-only and independent)
- Wait for all agents to complete before presenting the consolidated report
- Sequential execution only: detect languages → user selection → dispatch all → aggregate
- If an agent fails or times out, note the failure in the report and continue with other results

## SME Agent Mapping

| Language   | Agent Type             |
|------------|------------------------|
| Go         | `SWE - SME Golang`     |
| Zig        | `SWE - SME Zig`        |
| JavaScript | `SWE - SME JavaScript` |
| TypeScript | `SWE - SME TypeScript` |
| HTML       | `SWE - SME HTML`       |
| CSS        | `SWE - SME CSS`        |
| GraphQL    | `SWE - SME GraphQL`    |
| Docker     | `SWE - SME Docker`     |
| Makefile   | `SWE - SME Makefile`   |
| Ansible    | `SWE - SME Ansible`    |
| All others | `general-purpose`      |

## Abort Conditions

**Abort:**
- Not a git repository
- No source files detected in scope

**Do NOT abort:**
- No SME available for any detected language (use generalist for all)
- A single agent fails (report failure, continue with others)
- User selects only one language (still valuable)
