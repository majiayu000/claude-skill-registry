---
name: unikit-memory
description: >-
  Add or update rules in .unikit/memory/: core rules (code style, design principles, testing, performance)
  and stack rules (framework-specific patterns — Zenject, DOTween, Addressables, R3, UniTask, etc.).
  Accepts descriptions, URLs, or file paths; enriches docs via Context7 MCP when available.
  Use when user says "add rule", "add core rule", "add stack rule", "document how we use X",
  "add rules for DOTween", "add coding convention", pastes framework docs URLs,
  or wants to codify coding standards, best practices, or tech-specific conventions.
  Use "--migrate-rules" (or pass RULES.md / .unikit/RULES.md as input) to migrate mature rules
  from RULES.md into permanent core/stack files; also trigger on "migrate rules", "transfer rules to memory".
  Use "validate" to sync RULES_INDEX.md with actual files in memory/ — adds missing entries, removes phantom ones.
  Do NOT use for architecture decisions — those belong in ARCHITECTURE.md.
argument-hint: "[description | URL(s) | file path | --migrate-rules | --skip-registry | validate]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
  - Skill
  - WebFetch
  - WebSearch
  - AskUserQuestion
---

# UniKit Rules — Project Knowledge Base

Manage project rules in `.unikit/memory/`. This skill owns two rule categories:

- **Core** (`.unikit/memory/core/`) — universal best practices: code style, design principles, testing conventions, performance guidelines
- **Stack** (`.unikit/memory/stack/`) — framework-specific rules: API patterns, conventions, anti-patterns, code examples for Zenject, DOTween, R3, UniTask, Addressables, etc.

## What Belongs Here

- Code style conventions and naming rules → `core/`
- Design principles and architectural patterns → `core/`
- Testing conventions and best practices → `core/`
- Performance guidelines → `core/`
- Framework usage patterns and conventions → `stack/`
- Library-specific API rules and code examples → `stack/`
- Technology-specific anti-patterns and best practices → `stack/`
- Cross-framework integration guidelines → `stack/` **only when the user explicitly requests them or they are present in provided sources** (see Step 1 Phase C + Branch B.3 "Scope Isolation"). Never auto-generated from the project stack.

## What Does NOT Belong Here

- **Architecture decisions** (module boundaries, dependency flow, DI structure) → `.unikit/ARCHITECTURE.md`
- **Project-specific overrides** (explicit deviations from core/stack rules) → `.unikit/RULES.md` via `unikit-rules` skill

If the user provides content that falls into these categories, inform them and suggest the correct destination. For RULES.md content, suggest using the `unikit-rules` skill instead.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

## Workflow

### Step 0: Load Configuration (silent — do NOT print or announce any of these values)

1. Read `.unikit/config.yaml` — extract `language.ui` for user-facing messages (default: `en`)
2. Read `.unikit/memory/RULES_INDEX.md` — current index of all rule files.
3. **Read `.unikit/skill-context/{{self_name}}/SKILL.md`** — MANDATORY if the file exists.

This file contains project-specific workflow rules added by `/unikit-skills-context` or `/unikit-evolve`.
These rules change how this skill operates (research priorities, cross-check behavior, file format conventions, etc.).

**How to apply skill-context rules:**
- Treat them as **project-level overrides** for this skill's general instructions
- When a skill-context rule conflicts with a general rule written in this SKILL.md,
  **the skill-context rule wins** (more specific context takes priority)
- When there is no conflict, apply both: general rules from SKILL.md + project rules from skill-context
- Do NOT ignore skill-context rules even if they seem to contradict this skill's defaults —
  they exist because the project's experience proved the default insufficient

Do NOT output status messages like "Язык: X". Proceed directly to Step 1.

### Step 1: Parse Input & Classify Intent

Two-phase classification determines both input type and user intent.

**Phase A — Input type:**

```
First, check for --skip-registry anywhere in $ARGUMENTS:
├── Present → Remember skipRegistry=true, strip the flag from $ARGUMENTS before
│             continuing classification. The remaining text is classified normally.
└── Absent  → skipRegistry=false

Then classify the (possibly stripped) $ARGUMENTS:
├── Equals "validate" (case-insensitive) → VALIDATE INDEX (jump to Branch D)
├── Contains "--migrate-rules" →
│   ├── $ARGUMENTS is exactly "--migrate-rules" (no other text) → MIGRATE RULES (jump to Branch C)
│   └── $ARGUMENTS has additional text besides "--migrate-rules" →
│       Report to user: "--migrate-rules must be used alone without additional arguments."
│       STOP. Do not proceed.
├── Matches RULES.md path (case-insensitive):
│   "RULES.md", "rules.md", ".unikit/RULES.md",
│   ".unikit/rules.md", or any path ending with /RULES.md
│   → MIGRATE RULES (jump to Branch C)
├── Contains BOTH http(s):// tokens AND file extension / path tokens → Mixed input (URL + File)
├── Starts with http:// or https:// → URL input (can be multiple, space-separated)
├── Ends with known file extension (.md, .txt, .json, .yaml) or path/folder exists → File input
├── Has text content → Description input
└── No arguments → Interactive mode: ask user what to document, then re-classify
```

The `--skip-registry` flag is an escape hatch for callers that have already performed a registry lookup at a higher level and do not want this skill to repeat it. When the flag is present, Step 1.5 is bypassed entirely and the skill proceeds directly to content classification (Step 2) and generation.

**Phase B — Determine intent based on input type:**

```
Intent?
├── MIGRATE RULES   → Branch C (always — explicit migration request)
├── Mixed (URL + File) → RESEARCH (always — both inputs processed together)
├── URL(s)           → RESEARCH (always — URLs signal delegation)
├── File/Folder path → RESEARCH (always — user provides source material for analysis)
├── Description      → Analyze tone ↓
│   ├── Exploratory  → RESEARCH
│   └── Concrete     → ADD RULE
└── Interactive      → Ask user, then re-classify
```

**Tone signals for Description input:**

| Signal | Intent | Examples |
|--------|--------|----------|
| Vague topic, delegation words | **Research** | "add rules for DOTween", "document how we use Addressables", "figure out best practices for R3" |
| Imperative, specific convention, code examples | **Add Rule** | "add rule: always use `.SetEase(Ease.OutQuad)`", "never use coroutines", "use `NonLazy()` for controllers" |

**Phase C — Detect integration intent (stack rules only):**

Integration content (how framework X combines with framework Y) is off by default. Set `integrationIntent=true` if **any** of the following is true at classification time:

- **T1 (prompt text):** $ARGUMENTS contains any of: `integration`, `интеграция`, `with <framework>`, `связка X и Y`, `X + Y`, `использовать X из Y`, or equivalent phrasing that names two frameworks together.
- **T2 (URL or filename):** any input URL path or file path contains the tokens `integration` / `integrate` (case-insensitive).

If neither T1 nor T2 fires, leave `integrationIntent=false`. Branch B.1.5 may still upgrade it later based on fetched content (T3). Core-rule intents are unaffected — scope isolation applies to stack rules only.

Store `integrationIntent` alongside the classified intent and thread it through to Branch A / Branch B. In Branch A (Add Rule), when `integrationIntent=true` and the rule spans two existing framework files, use `AskUserQuestion` to pick the main framework's file — never split the rule across both files.

### Step 1.5: Registry-first Lookup

**Always try the registry before generating a rule from scratch.** If a matching rule already exists in the remote catalog, the user gets a vetted version by installing it via CLI — much better than spending tokens generating a local copy that duplicates upstream work.

#### 1.5.1: Read CLI contract

Read `.unikit/system/cli-contract.md` to confirm available `unikit-ai rules *` commands and exit codes.

#### 1.5.2: Fetch catalog and installed state

Run two CLI commands (sequential is fine):

```bash
unikit-ai rules list --json
```
```bash
unikit-ai rules status --json
```

Exit code handling:
- `rules list` exit 2 (network error) → skip to Step 2 silently, proceed without registry
- `rules list` exit 1 (`.unikit.json` not found) → the project is not a UniKit project, skip to Step 2
- any other non-zero → report the error and skip to Step 2

Parse `rules list --json` into `catalog.rules[]` and `rules status --json` into `status.rules[]`.

#### 1.5.3: Semantic matching

Match the user's intent against `catalog.rules[]`:

- **Exact id match (case-insensitive):** `"DOTween"` → `dotween`
- **Description match:** `"tweening library"` → `dotween` via the `description` field
- **Synonyms and localized names:** `"контейнер внедрения зависимостей"` → `zenject`

Collect 0..N candidates. If N > 1, treat all as possible matches for the user prompt below.

#### 1.5.4: Join with installed state

For each candidate, look it up in `status.rules[]` by `name` (case-insensitive):
- **Already installed** → note `source`, `version`, and category so the prompt can show accurate state.
- **Not installed** → candidate is offerable as a fresh install.

#### 1.5.5: Decision tree

```
Match result?
├── Exactly 1 match + already installed
│   → Inform user: "{name} is already installed (source={source}, v{version})"
│   → AskUserQuestion: What should we do?
│   │  Options:
│   │  1. Leave as is         → STOP
│   │  2. Edit manually       → Continue to Step 2
│   │  3. Reinstall from registry → Bash: unikit-ai rules install <id> --force → STOP
│
├── Exactly 1 match + NOT installed
│   → AskUserQuestion: Matching rule "{name}" v{version} found in registry. Install it?
│   │  Options:
│   │  1. Yes, install from registry  → install path (below)
│   │  2. Preview before deciding     → preview path (below)
│   │  3. No, generate a new rule     → Continue to Step 2 (research/manual generation)
│   │
│   ├── install path:
│   │   Bash: unikit-ai rules install <id>
│   │   → Report "✓ Installed <id> from registry" and STOP. The CLI already
│   │     regenerates RULES_INDEX.md — no extra sync needed.
│   │
│   └── preview path:
│       Bash: unikit-ai rules show <id> --references
│       → Show content to user, then AskUserQuestion again:
│         1. Install → install path above
│         2. Generate a new rule → Step 2
│
├── Multiple matches
│   → AskUserQuestion: present all candidates + a "none of these, generate a new rule" option
│   → If user picks a candidate → treat as "exactly 1 match" (installed or not)
│   → If "none" → Continue to Step 2
│
└── Zero matches
    → Continue to Step 2 (research/manual generation)
```

**Key behavior guarantees:**
- Agreeing to install always ends with `rules install <id>` and terminates the skill. The content in the registry is the source of truth; the skill does not second-guess it.
- Declining the registry version always routes to Step 2, where the skill generates the rule from the user's description, URL, or file input as usual. No partial install, no mix of registry + local content.

#### When to skip Step 1.5 entirely

Bypass the lookup completely when any of the following is true:

- **`--skip-registry` flag** was present in $ARGUMENTS (a higher-level caller already queried the catalog and does not want redundant prompts)
- **Intent is VALIDATE INDEX** (Branch D) or **MIGRATE RULES** (Branch C) — neither installs new rules, so registry lookup is irrelevant
- **Input is a file path** — the user explicitly wants to process a specific file, not search the catalog
- **`cli-contract.md` doesn't exist** — the UniKit CLI is not available in this project, so `rules *` commands cannot be used

---

### Step 2: Classify Content Category

Analyze the content and determine its category:

1. **Core or Stack?**
   - **Stack** — content about a specific framework or technology (Zenject, DOTween, R3, etc.) → `.unikit/memory/stack/`
   - **Core** — content about universal practices (code style, design principles, testing, performance) → `.unikit/memory/core/`
   - **Neither** — redirect the user to the correct destination:
     - Architecture → `.unikit/ARCHITECTURE.md`
     - Project-specific overrides → `.unikit/RULES.md` via `unikit-rules` skill
     - **Stop here. Do NOT create any files.**

2. **Identify the target file.**
   - For **Stack**: framework name → filename (e.g., `dotween.md`, `zenject.md`, `addressables.md`)
   - For **Core**: topic → filename (e.g., `code-style.md`, `testing.md`, `performance.md`). Consult `RULES_INDEX.md` Core section.

3. **Does the file already exist?** Check the target directory (`.unikit/memory/stack/` or `.unikit/memory/core/`).

### Step 3: Route by Intent

Based on intent (Step 1) and classification (Step 2), follow the appropriate branch:

```
Intent?
├── VALIDATE INDEX → Branch D (skip Steps 2-3 entirely)
├── MIGRATE RULES  → Branch C (skip Step 2 — migration handles its own classification)
├── ADD RULE       → Branch A
└── RESEARCH       → Branch B
```

---

## Branch A: Add Rule

The user has a concrete rule to save. No research, no enrichment — just store what the user explicitly stated.

### A.1: Check Target File

```
File exists?
├── YES → A.2 (Cross-Check & Append)
└── NO
    ├── Core  → A.3 (Create File)
    └── Stack → A.4 (Ask About Research)
```

### A.2: Cross-Check & Append (file exists)

Before appending, compare the new content against existing rules:

1. **Read the target file.**
2. **Read related files** — scan `RULES_INDEX.md` for files with overlapping keywords, then read those too (both `stack/` and `core/`). Also read `.unikit/RULES.md` for project-specific overrides.
3. **Compare each new rule against existing formulations.** A contradiction is when the new content prescribes something different from an existing rule — e.g., "use `await` directly" vs existing "always wrap in `UniTask.Create`", or "bind as Transient" vs existing "bind as Singleton".

**If contradictions found:**

- Report **each** contradiction to the user, quoting both the new statement and the existing rule with its source file.
- For each contradiction, ask via `AskUserQuestion` (batch up to 3 contradictions per question):

  Options:
  1. Replace — update existing rule with new formulation
  2. Keep existing — discard the conflicting part
  3. Keep both — document both with a note on when each applies

  Based on choice:
  - Replace → overwrite the existing rule text in the target file with the new formulation
  - Keep existing → discard the conflicting part from the new content, keep existing rule unchanged
  - Keep both → add the new rule alongside the existing one with a note clarifying when each applies

**After resolution (or if no contradictions):**

- Append the new rule(s) to the existing file, merging into appropriate sections. Do not overwrite useful existing content.
- → Go to **Final Step: Confirm**

### A.3: Create New File (Core, no existing file)

1. Create the rule file following the **File Format Template** below.
2. Write the user's rule(s) as-is — no enrichment, no synthesis.
3. Update `RULES_INDEX.md` — add a new row to the appropriate table in alphabetical order.
4. → Go to **Final Step: Confirm**

### A.4: Ask About Research (Stack, no existing file)

Ask the user: *"I don't have a rules file for {framework} yet. Would you like me to research this framework and create a comprehensive document, or just save your rule as-is?"*

```
User answer?
├── YES (research) → Switch to Branch B (start from B.1)
└── NO (save as-is)
    ├── Create the rule file with user's rule(s) only
    ├── Update RULES_INDEX.md — add to ## Stack table
    └── → Go to Final Step: Confirm
```

---

## Branch B: Research

Full research pipeline — gather material, enrich, synthesize, then write.

### B.1: Gather Material

Depends on the original input type from Step 1:

**URL input** — Two-phase deep extraction.

*Phase A — Collect & Study.* For EACH URL:

1. **Fetch the page** using `WebFetch` with a targeted prompt:
   ```
   WebFetch(url, "Extract ALL key information about this framework/technology:
   - Main topic and purpose
   - Key concepts, terms, and definitions
   - Code examples and usage patterns
   - API methods, parameters, return types
   - Configuration options
   - Best practices and recommendations
   - Anti-patterns and common mistakes
   - Links to related important pages
   Provide a comprehensive, structured summary.")
   ```
2. **Assess depth** — if the page references critical sub-pages (API reference, guides, examples), fetch those too (up to 5 additional pages per source URL, prioritize by relevance).
3. **Record findings** — for each source, capture: topic, core concepts, practical patterns with code examples, configuration / API surface, common pitfalls.
4. If a URL fails, report and continue with others.

*Phase B — Enrich with Web Search.* After collecting all URLs, evaluate coverage gaps. If the fetched URLs don't already provide comprehensive coverage, run 1-3 targeted `WebSearch` queries:

- `"<framework> best practices"` — latest recommendations
- `"<framework> common mistakes"` — pitfalls to document
- `"<framework> cheat sheet"` — concise reference material

Skip this phase if the URLs already cover the topic comprehensively.

**File input** — Two-phase enrichment.

1. Use `Read` to load the file content.
2. Identify the framework/technology/topic from the file content.
3. Run 1-3 targeted `WebSearch` queries to enrich and validate:
   - `"<topic> best practices"` — latest recommendations
   - `"<topic> common mistakes"` — pitfalls to document
   - `"<topic> cheat sheet"` or `"<topic> API reference"` — concise reference material
4. For each promising search result, use `WebFetch` to extract detailed content (up to 3 pages).
5. B.2 will perform Context7 enrichment — do not skip web search here.

**Mixed input (URL + File)** — Process both sources together.

1. Apply the **URL input** pipeline to all http(s) URLs (WebFetch + conditional WebSearch).
2. Apply the **File input** pipeline to all file paths (Read + WebSearch).
3. Merge all gathered material before proceeding to B.2.

**Description input** (exploratory tone):

1. Use the provided text to identify the target framework/technology/topic.
2. Run 1-3 targeted `WebSearch` queries to gather material:
   - `"<topic> best practices {{engine_name}}"` — recommended approaches
   - `"<topic> common mistakes"` — pitfalls to document
   - `"<topic> cheat sheet"` or `"<topic> API reference"` — concise reference material
3. For each promising search result, use `WebFetch` to extract detailed content (up to 3 pages).
4. B.2 will attempt Context7 enrichment — but do not skip web search here.

**Interactive mode**: Ask the user which framework or technology they want to document. Offer examples based on the project's tech stack from `DESCRIPTION.md`.

### B.1.5: Upgrade Integration Intent (post-fetch)

After B.1 finishes gathering material, scan the collected content for integration signals (T3):

- Headings or sections whose titles include `integration`, `integrate`, `with <other framework>`, or equivalent wording
- Substantial blocks dedicated to combining the target framework with another library (not just a one-line mention)
- Code examples whose central point is a cross-framework pattern — **not** a placeholder usage like `.ToUniTask()` on an arbitrary awaitable

If **any** such signal is found AND `integrationIntent` is currently `false`, upgrade it to `true`. This honors user-supplied sources that document an integration even when the original prompt did not explicitly ask for it.

If no signals are found, leave `integrationIntent` unchanged.

### B.2: Enrich with Context7

Always attempt when a specific framework/topic was identified:

1. Use `mcp__context7__resolve-library-id` to find the library ID.
2. Query the documentation with `mcp__context7__query-docs` across **all** topics (separate queries for each):
   - **Usage patterns** — key API conventions, core workflows, typical setup
   - **Best practices** — recommended approaches, idiomatic usage, performance tips
   - **Cheat sheets** — quick reference for common operations, method signatures, configuration options
   - **Common mistakes** — typical errors, pitfalls, misuse patterns, debugging hints
3. Integrate relevant findings into the gathered material.

**Fallback:** If context7 tools are unavailable or the lookup fails — print a yellow warning and proceed with web search results and training knowledge:

```
⚠️ Context7 MCP is not available — documentation enrichment skipped. Results may be less comprehensive.
```

Use yellow/warning styling if the output supports it. Do not block the workflow — this is informational only.

### B.3: Synthesize

Combine all gathered material (B.1 input + B.2 enrichment) into a structured Knowledge Base.

Structure the material into these sections (omit empty ones):

- **Core Concepts** — key terms, definitions, fundamental ideas
- **API / Interface** — method signatures, parameters, return types, key classes
- **Patterns & Examples** — practical code examples with context on when to use each
- **Configuration** — setup options, defaults, valid values, initialization patterns
- **Best Practices** — recommended approaches with reasoning
- **Common Pitfalls** — typical mistakes, what goes wrong, how to avoid

Keep only information relevant to using the framework in a {{engine_name}}/{{engine_code_language}} project. Discard web-framework specifics, non-{{engine_name}} platforms, and irrelevant content. Transform passive documentation into actionable rules ("Use X when..." instead of "X is a feature that...").

**Scope Isolation (stack rules only):**

The rule describes ONLY the target framework/module. Apply this filter as a second, independent pass over the synthesized material — not as a stylistic guideline.

- **Always allowed:** other frameworks may appear as *minimal placeholders* in examples — an arbitrary async method being converted via `.ToUniTask()`, any `IObservable` feeding an R3 subscription, a generic `MonoBehaviour` hosting a binding. The example illustrates the target API; the other framework is incidental.
- **Forbidden when `integrationIntent=false`:**
  - Dedicated "Integration with X" sections (or equivalent wording)
  - Rules that prescribe how to combine the target framework with another library
  - Code examples whose main point is a cross-framework pattern rather than the target API
  - **Do NOT invent integration content from project-stack knowledge.** Even if the project's `DESCRIPTION.md` or installed packages show R3, Zenject, Addressables, or similar libraries, do not generate integration material unless it came from the user's input (prompt, URL, file) or was detected by B.1.5. Project-stack awareness is for routing decisions only, not for content synthesis.
- **Allowed when `integrationIntent=true`:**
  - Integration sections sourced from the user's input or fetched material, written as concrete rules/examples
  - All integration content goes into the **main framework's rule file** (the framework the rule is primarily about). Never create a separate `{X}-{Y}-integration.md` file and never split the integration across both framework files.
  - If the "main" framework is ambiguous (the user's input names two frameworks symmetrically and both files exist), use `AskUserQuestion` to let the user pick the target file before writing.

**Self-test before writing:** mentally remove every mention of other frameworks from the synthesized content. If the rule becomes incoherent, too much integration material leaked in — rewrite with tighter scope (or confirm `integrationIntent=true` applies).

This guardrail applies only to stack rules. Core rules (code style, testing, performance, design principles) are framework-agnostic by construction and are not subject to this filter.

### B.3.5: Identify Reference Candidates

After synthesis, scan the structured content for sections that are **large, rarely needed all at once, or used as a lookup rather than read in full**. Such sections are candidates for extraction into separate reference files.

**Extract to a reference file when the content is:**

| Extract → reference | Keep → main file |
|---------------------|-----------------|
| Large subsystem rarely used alongside other parts | Architecture and lifecycle rules |
| Lookup table with 20+ rows | Code templates and examples |
| Exhaustive index of all variants | Naming and file-structure conventions |
| Data the LLM "looks up", not "reads in full" | Configuration and registration patterns |
| Content large enough to distract from conceptual rules | Workflow and decision instructions |

**Choose a split strategy based on content type. Common strategies:**

- **Module split** — the framework has large, independently-used subsystems. Each subsystem gets its own reference file. File name: `{rule-id}-{module}.md`.
  *Example: Zenject has pools and factories as large, rarely-needed features → `zenject-pools.md`, `zenject-factories.md`.*

- **Lookup tier split** — the framework has a large catalog of variants (classes, components, nodes) where the user needs to "pick one". Split into a compact quick-reference and an exhaustive index. File names: `{rule-id}-{content}-quickref.md` + `{rule-id}-{content}-full.md`.
  *Example: ASPID MVVM has dozens of binders → `aspid-mvvm-binders-quickref.md` + `aspid-mvvm-binders-full.md`.*

- **Single reference** — the data is a standalone catalog that doesn't need tiering (one file is sufficient). File name: `{rule-id}-{content}.md`.
  *Example: `aspid-mvvm-converters.md` — converter catalog, compact enough as one file.*

- **Mixed** — combine strategies when a framework has both large subsystems and lookup catalogs.

The choice of strategy is driven by the content: choose what makes sense for this specific framework, don't force a pattern that doesn't fit.

**If 0 candidates found** — skip to B.4.

**If 1+ candidates found** — propose the split strategy and exact file list before writing anything:

```
I propose extracting the following data into reference files
using a {strategy name} strategy:

1. `.unikit/memory/stack/references/{filename}.md`
   Contains: {what goes here}
   Reason: {why this content warrants a separate file}

2. `.unikit/memory/stack/references/{filename}.md`
   Contains: {what goes here}
   Reason: {why}

The main rule file will list them in a `> **References**:` header line
and include a "{Content} Lookup Workflow" section explaining when to open each file.
```

Use `AskUserQuestion`: Proceed with this breakdown?

Options:
1. Yes — create all proposed reference files
2. Adjust — user specifies changes (rename, merge, split, drop a file, change strategy) → revise proposal and ask again
3. No — keep all data inline in the main rule file

- **Yes / approved Adjust** → mark the approved files for creation; proceed to B.4.
- **No** → skip reference extraction; proceed to B.4 with all content staying inline.

### B.4: Cross-Check (if target file exists)

Same logic as **A.2** — read existing file and related files, compare, resolve contradictions with user.

If the target file doesn't exist — skip this step.

### B.5: Generate / Update File

Create or update the rule file following the **File Format Template** below. If updating, merge into existing sections without overwriting useful content.

If reference files were approved in B.3.5:
1. Create each reference file following the **Reference File Format** section below.
2. Add `> **References**:` to the main rule file header, listing each file with a one-word parenthetical (e.g., `(quick lookup)`, `(exhaustive index)`, `(converter catalog)`).
3. Add a `## {Content} Lookup Workflow` section to the main rule file instructing the LLM when to open which reference. Do **not** duplicate catalog data in the main file — only pointers and instructions.

If a NEW file was created — update `RULES_INDEX.md` (add row to appropriate table in alphabetical order).

→ Go to **Final Step: Confirm**

---

## Branch C: Migrate Rules from RULES.md

Transfer mature entries from `.unikit/RULES.md` (quick-capture staging area) into permanent core/stack rule files in `.unikit/memory/`. RULES.md holds project-specific overrides — over time, entries that clearly belong to a specific rule file should graduate into the knowledge base.

### C.1: Load Context

Read:
1. **`.unikit/RULES.md`** — current entries
3. **`.unikit/memory/RULES_INDEX.md`** — available rule files with descriptions

**Skip entirely** if RULES.md has no entries — report "No entries in RULES.md to migrate" and stop.

### C.2: Classify Entries

For each rule entry in RULES.md:

0. **Check for `@no-migrate` tag** — if the rule line ends with `<!-- @no-migrate -->`, skip it entirely. This tag means the user previously decided this rule must stay in RULES.md. Do not present it as a transfer candidate, do not mention it in the output. Proceed to the next entry.
1. **Classify destination** — match topic against RULES_INDEX.md "Description" and "Load When" columns to find the target file. If no file covers this topic — mark as **New File** candidate (needs a new rule file in memory/).
2. **Check maturity** — ready for transfer when:
   - Clearly belongs to a specific rule file (existing or proposed new one)
   - Specific and actionable (not a vague note)
3. **Detect conflicts** (skip for New File candidates) — read the target rule file and check whether the RULES.md entry **contradicts** an existing rule. Mark each candidate as:
   - **Compatible** — no conflict, standard transfer
   - **Override** — contradicts an existing rule in the target file (e.g., "Never use var" overrides a {{engine_code_language}} convention, "Factory classes instead of Zenject PlaceholderFactory" overrides a DI pattern). Record which specific rule(s) in the target file conflict.
   - **New File** — no existing file covers this topic; propose creating a new rule file

### C.3: Present Transfer Candidates

**Compatible entries:**

```
### Transfer: "[rule text]"
- **From:** `.unikit/RULES.md` (section: {section name})
- **To:** `.unikit/memory/{core|stack}/{FILE}.md` (section: {target section})
- **Reason:** {why this belongs in the target file}
```

Options via `AskUserQuestion` (batches of up to 4):
1. Transfer — move to target file, remove from RULES.md
2. Keep — leave in RULES.md permanently, tag `<!-- @no-migrate -->`
3. Skip — decide later (no tag — will be presented again on next migration)

Based on choice:
- Transfer → apply C.4 "Transfer" procedure for this entry
- Keep → append `<!-- @no-migrate -->` tag, do not touch memory files
- Skip → leave as-is, no changes

**Override entries (conflict detected):**

```
### Override: "[rule text]"
- **From:** `.unikit/RULES.md` (section: {section name})
- **To:** `.unikit/memory/{core|stack}/{FILE}.md` (section: {target section})
- **Conflicts with:** "[existing rule text in memory file]"
- **Reason:** {why the RULES.md entry overrides the base convention}
```

Options via `AskUserQuestion` (batches of up to 4):
1. Replace — delete conflicting rule(s) from memory file, insert RULES.md entry verbatim, remove from RULES.md
2. Keep — leave in RULES.md permanently, tag `<!-- @no-migrate -->`
3. Delete — remove from RULES.md without transferring (base convention wins)

Based on choice:
- Replace → apply C.4 "Replace" procedure for this entry
- Keep → append `<!-- @no-migrate -->` tag, do not touch memory files
- Delete → remove entry from RULES.md, leave memory file unchanged

**New File entries (no matching file in memory/):**

```
### New File: "[rule text]"
- **From:** `.unikit/RULES.md` (section: {section name})
- **Proposed file:** `.unikit/memory/{core|stack}/{PROPOSED-NAME}.md`
- **Category:** {Core / Stack} — {reasoning for the choice}
- **Reason:** {why no existing file covers this topic}
```

Options via `AskUserQuestion` (batches of up to 4):
1. Create & Transfer — create proposed file and move the rule there
2. Custom — user specifies own filename and/or category (core/stack)
3. Keep — leave in RULES.md permanently, tag `<!-- @no-migrate -->`
4. Skip — decide later (no tag — will be presented again on next migration)

Based on choice:
- Create & Transfer → apply C.4 "Create & Transfer" procedure with proposed filename
- Custom → ask user for filename and category, confirm, then apply C.4 "Create & Transfer" with user's values
- Keep → append `<!-- @no-migrate -->` tag, do not touch memory files
- Skip → leave as-is, no changes

If no transfer candidates found across all three types (Compatible, Override, New File) → report "No mature entries to transfer" and stop.

### C.3a: Handle Rephrasing Requests

If the user rephrases a rule, requests changes to the wording, or asks to modify a rule before saving:

1. **Generate a new variant** — rewrite the rule text according to the user's instructions.
2. **Present the updated rule** using the same format as C.3 (Compatible / Override / New File — whichever applies), showing the **new wording** instead of the original.
3. **Offer the same options** as C.3 for this entry (Transfer / Replace / Create & Transfer / Keep / Skip / etc.).
4. **Repeat** if the user requests further changes — keep iterating until the user approves or skips.

The rephrased text replaces the original for all downstream steps (C.4 applies the approved wording, not the original RULES.md text).

### C.4: Apply Approved Actions

**For "Transfer" (compatible entries):**
1. Read the target rule file
2. Add the rule text **verbatim** (or the approved rephrased variant from C.3a) — copy exact wording without rephrasing or paraphrasing
3. Remove the rule from RULES.md using `Edit`
4. If a RULES.md section becomes empty after removal, remove the section header too

**For "Replace" (override entries):**
1. Read the target rule file
2. Locate and **delete** the conflicting rule(s) from the target memory file using `Edit`
3. Insert the RULES.md entry **verbatim** (or the approved rephrased variant from C.3a) in the same section where the conflicting rule was
4. Remove the rule from RULES.md using `Edit`
5. If a RULES.md section becomes empty after removal, remove the section header too

**For "Create & Transfer" (new file entries):**
1. Create the new rule file following the **File Format Template** below, using the approved filename and category
2. Write the rule text (original or approved rephrased variant from C.3a) into the appropriate section
3. Update `RULES_INDEX.md` — add a new row to the appropriate table (Core or Stack) in alphabetical order
4. Remove the rule from RULES.md using `Edit`
5. If a RULES.md section becomes empty after removal, remove the section header too

**For "Delete" (discard override):**
1. Remove the rule from RULES.md using `Edit`
2. If a RULES.md section becomes empty after removal, remove the section header too
3. Do not touch the memory file — the base convention remains

**For "Keep" (leave in RULES.md permanently):**
1. Append ` <!-- @no-migrate -->` to the end of the rule line in RULES.md using `Edit`
2. The tag is an HTML comment — invisible when rendered, but detectable during future migrations (see C.2 step 0)
3. Do not modify any memory files

**Verbatim transfer is critical:** rules in RULES.md were carefully worded. Changing wording during transfer risks losing nuance. The only acceptable change is adding a section header in the target file if needed.

→ Go to **Final Step: Confirm** (report which rules were transferred, replaced, or deleted)

---

## Branch D: Validate Index

Sync `.unikit/memory/RULES_INDEX.md` with the actual files on disk. No user interaction — fully automatic.

### D.1: Scan Actual Files

1. `Glob: .unikit/memory/core/*.md` — collect all real core rule files
2. `Glob: .unikit/memory/stack/*.md` — collect all real stack rule files
3. Read `.unikit/memory/RULES_INDEX.md` — parse both tables (Core and Stack), extract filenames from each row

### D.2: Diff

Compare the two sets:

- **Missing from index** — files that exist on disk but have no row in RULES_INDEX.md
- **Phantom in index** — rows in RULES_INDEX.md whose files don't exist on disk

### D.3: Fix Index

**For each missing file** — read the file, extract the `> **Scope**:` and `> **Load when**:` lines from the header. Add a row to the appropriate table in RULES_INDEX.md (alphabetical order):

```
| {FILENAME}.md | {Scope value} | {Load when value} |
```

If the file has no Scope/Load when header, use the first heading and first paragraph to generate a brief description and keywords.

**For each phantom entry** — remove the row from RULES_INDEX.md using `Edit`.

### D.4: Report

Output a short validation report (in user's configured language):

```
RULES_INDEX.md validation complete.

Core: {N} files, Stack: {M} files
✅ Added to index: {X}
🔄 Removed from index: {Y}

{If X > 0: list added filenames}
{If Y > 0: list removed filenames}
```

Stop. Do not proceed to any other step.

---

## File Format Template

Use existing rules as a template (stack: `reactive-async.md`, `odin.md`; core: `code-style.md`, `testing.md`).

```markdown
# {Framework Name / Topic}

> **Scope**: {What this file covers — specific APIs, patterns, conventions}
> **Load when**: {Comma-separated keywords and contexts that trigger loading this file}
> **References**: {Optional — omit if no reference files. List each with a parenthetical label: `.unikit/memory/stack/references/{rule-id}-binders-quickref.md` (quick lookup), `.unikit/memory/stack/references/{rule-id}-binders-full.md` (exhaustive index).}

---

## {Section 1}

{Rules, code examples, patterns}

## {Section 2}

{More rules}

## {Content} Lookup Workflow

{Optional — include only when reference files exist. Step-by-step instructions for when to open which reference file. Example:
1. First — open `{rule-id}-{content}-quickref.md`. Covers the most common scenarios.
2. If nothing fits — open `{rule-id}-{content}-full.md`. Exhaustive index of all variants.
Do NOT guess — always verify against the reference files.}

## Anti-patterns

{Common mistakes to avoid — if applicable}
```

**Writing `Scope` and `Load when`:**

Both lines must read as **prose**, not as a dump of class names, variable names, or API identifiers. A future LLM must be able to decide from the header alone whether this rule is relevant to the task at hand.

- `> **Scope**:` — one sentence answering *"what does this rule cover?"*. Name the domain (framework, concern, pattern) and the kinds of decisions the rule helps make. Identifiers may appear only as examples of *what* is governed, never as the entire answer.
- `> **Load when**:` — one line listing *developer situations* that should trigger loading this rule. Phrase from the developer's perspective, using actionable gerunds ("authoring …", "wiring …", "debugging …", "designing …"), comma-separated. Identifiers may appear only inside a task phrase, never as standalone tokens.

**Example — `node-canvas.md`**

Bad (reads like a class list, useless for intent matching):

```
> **Scope**: `Graph`, `Task`, `Condition`, `BT`, `ServiceBus`, `INode`, `NodeCanvas.Framework`
> **Load when**: Graph, Task, Condition, BT, ServiceBus, INode, NodeCanvas
```

Good (reads like prose, tells a future LLM *when* to load this rule):

```
> **Scope**: NodeCanvas behavior tree authoring — custom Task and Condition nodes, service injection via ServiceBus, graph composition patterns, and NodeCanvas.Framework lifecycle hooks.
> **Load when**: building AI behaviors with NodeCanvas, authoring custom Tasks or Conditions, wiring services into a behavior tree, debugging graph execution order, designing reusable BT subtrees.
```

Both lines follow `language.rules` from `.unikit/config.yaml` like the rest of the prose. Framework names, type names, and other code identifiers stay in English regardless of the configured language.

**Guidelines:**
- Filename: `lower-case-with-hyphens.md` (e.g., stack: `dotween.md`, `zenject.md`; core: `code-style.md`, `testing.md`)
- Location: `.unikit/memory/stack/` for Stack, `.unikit/memory/core/` for Core
- Language: follow `language.rules` from `.unikit/config.yaml` (default: `en`). Rule prose, section headings, explanations, and examples use that language. Frontmatter keys (`> **Scope**:`, `> **Load when**:`), filenames, rule ids, code identifiers, file paths, and framework names always stay in English regardless of `language.rules`. See `.unikit/system/LANGUAGE_RULES.md` → "Knowledge base rule files" for the full specification. Never prompt the user for this setting and never write to it — it is manually edited only.
- Include code examples wherever they clarify usage
- Keep rules actionable — "Use X", "Never Y", "Prefer Z over W"

## Reference File Format

Reference files live in `.unikit/memory/stack/references/` and hold lookup/catalog data extracted from a main stack rule. They have no frontmatter — they are supplementary documents, not standalone rules.

**Naming convention:** `{rule-id}-{descriptor}.md`

| Part | Meaning | Example |
|------|---------|---------|
| `{rule-id}` | Parent rule filename without `.md` | `zenject`, `aspid-mvvm` |
| `{descriptor}` | Module name, content type, or tier label — whatever best describes the file's scope | `pools`, `factories`, `binders-quickref`, `binders-full`, `converters` |

Examples:
- Module split: `zenject-pools.md`, `zenject-factories.md`
- Lookup tier split: `aspid-mvvm-binders-quickref.md`, `aspid-mvvm-binders-full.md`
- Single reference: `aspid-mvvm-converters.md`

**Internal structure:**

```markdown
# {Parent Rule} — {Descriptor label}

> **Base path:** {optional — package/folder path these names are relative to}
> See also: [{related-reference}.md]({related-reference}.md)    ← cross-link to related reference if applicable

---

## {Lookup Section}

| {Key column} | {Value column} | ... |
|-------------|---------------|-----|
| ...         | ...           | ... |
```

**Writing guidelines:**
- No `Scope` / `Load when` / `References` frontmatter — those belong only to main rule files.
- Lead with the most useful lookup table first (task → answer, or type → class).
- Cross-link to related reference files when applicable (e.g., between `quickref` and `full` tiers, or between module references that overlap).
- Language follows `language.rules` from `.unikit/config.yaml` (same as main rule file).
- Code identifiers, class names, and paths always stay in English regardless of `language.rules`.

## RULES_INDEX.md Format

When adding a new entry to `RULES_INDEX.md`:

```markdown
| {FILENAME}.md | {Brief description of what the file covers} | {Comma-separated keywords and contexts} |
```

Place in alphabetical order within the appropriate table (`## Core` or `## Stack`).

## Final Step: Confirm

**Reconcile `.unikit.json` state with disk (after Branch A / B / C only):**

If the just-completed branch was **Branch A** (Add Rule), **Branch B** (Research), or **Branch C** (Migrate Rules) — i.e. anything that wrote a new or updated rule file into `.unikit/memory/` — run the CLI sync command so the generated file is registered in `.unikit.json.rules.installed` and `RULES_INDEX.md` is regenerated from authoritative state + disk:

```bash
unikit-ai rules sync
```

Why this matters: Branches A/B/C write files via `Write`/`Edit` directly and never touch `.unikit.json`. Without a sync pass, the new rule lives on disk but remains invisible to `rules status`, `rules install <id> --force`, and — most importantly — to `/unikit` Step 9.3, which builds its "already installed" set from `.unikit.json` state. Skipping sync here means the next `/unikit` run can try to reinstall the same rule from the registry and fail with exit 4 ("already installed"). `syncRulesState` Phase 1 picks up untracked `.unikit/memory/**/*.md` files and registers them as `source: local` entries; Phase 3 regenerates `RULES_INDEX.md`. That is exactly the reconciliation the skill needs before printing the report.

Treat a non-zero exit code as non-fatal for the skill: log the CLI output to the report and continue. The file is still on disk — the user can re-run `unikit-ai rules sync` manually.

**Skip the sync entirely when:**
- The branch was **Branch D** (Validate Index) — Branch D already exited with `Stop. Do not proceed to any other step.` and never reaches this Final Step at all.
- An install-from-registry short-circuit ran in Step 1.5 — `rules install` already updated state and regenerated the index, and the short-circuit terminates the skill before reaching Final Step.

**Report to the user (in their configured language):**
- Which file was created or updated
- Summary of what was added
- Which branch was used (Add Rule / Research)
- Whether Context7 enrichment was applied (Research branch only)
- Whether `.unikit.json` state was reconciled via `rules sync` (and whether the index was regenerated)
- Whether RULES_INDEX.md was updated
- If any content was redirected elsewhere (architecture, RULES.md)

**Offer rules-registry promotion (after Branch A / B / C only):**

If the just-completed branch was **Branch A** (Add Rule), **Branch B** (Research), or **Branch C** (Migrate Rules) — i.e. anything that actually wrote into `.unikit/memory/` — check whether the project's registry is local:

```bash
unikit-ai rules registry show --json
```

Parse the JSON. If `.kind == "local"`, ask the user whether to promote the memory changes into the registry **now** via `AskUserQuestion`:

```
AskUserQuestion: A local rules registry is configured at <.url from the JSON>.
Promote the memory changes into the registry now by running /unikit-rules-registry update?

Options:
1. Yes — run /unikit-rules-registry update after the Final Step report
2. No  — skip promotion, keep the changes in memory only
```

- **Yes** → finish the Final Step report first (the user must see exactly what changed in memory before promotion), then transition to `/unikit-rules-registry update` as the next action. Do not collapse the memory report into the promotion run — they are separate, ordered events.
- **No** → finish the Final Step report without adding any promotion hint. The user can always run `/unikit-rules-registry update` manually later; do not repeat the question or nag on the next invocation.

Skip the question entirely (do not ask, do not print a fallback hint) when:
- The branch was **Branch D** (Validate Index) — no memory writes happened.
- An install-from-registry short-circuit ran in Step 1.5 — the registry is already the source of truth for that rule.
- `rules registry show --json` returned a non-zero exit code or `.kind` is not `"local"`.

## Access Rules

**Writable** (this skill can create and edit):
- `.unikit/memory/core/` — core rules: code style, design principles, testing, performance
- `.unikit/memory/stack/` — stack rules: framework-specific patterns and conventions
- `.unikit/memory/stack/references/` — supplementary reference docs for stack rules
- `.unikit/memory/RULES_INDEX.md` — index of all rule files

**Writable only during Branch C (Migrate Rules):**
- `.unikit/RULES.md` — removal of migrated entries only; adding new entries goes through `unikit-rules` skill

**Read-only** (this skill must NEVER modify these files):
- `.unikit/config.yaml` — project settings (language). Read-only for this skill.
