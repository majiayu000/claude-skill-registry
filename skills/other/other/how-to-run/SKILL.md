---
description: >-
  Generates or updates a project's HOW-TO-RUN.md — a single document that
  teaches a new developer how to set up their environment and run the project
  locally. Detects build system, toolchain, SDKs, source dependencies (git
  submodules, sibling repos), external services, environment config, and
  hardware/OS requirements. Works for web apps, C++ desktop apps, native
  mobile, game engines, embedded/firmware, and backend services. Audits an
  existing HOW-TO-RUN.md against actual project state. Learns from setup
  info found in README.md / CONTRIBUTING.md / docs but never modifies those
  files — any outdated info found elsewhere is reported to the user at the
  end. Use after /optimus:init or standalone when onboarding feels broken.
  Handles single projects, monorepos, and multi-repo workspaces.
disable-model-invocation: true
---

# How to Run

Generate or update a `HOW-TO-RUN.md` at the project (or workspace) root that teaches a new developer who has just cloned the repo how to set up their environment and run the project locally — covering OS/hardware prerequisites, toolchain & SDKs, source dependencies (submodules, sibling repos), language-level install, external services, env config, build, run, and tests.

**Write scope:** The only file this skill is ever permitted to create or modify is `HOW-TO-RUN.md`. It never modifies `README.md`, `CONTRIBUTING.md`, `docs/*`, `BUILDING.md`, `INSTALL.md`, or any other file — not even to add a link. Existing docs are *input only*: the skill learns from them but always verifies every fact against the actual codebase before using it.

## Step 1: Detect Full Project Context (agent-assisted)

Delegate project scanning to a detection agent to keep the main context clean for content generation.

Read `$CLAUDE_PLUGIN_ROOT/skills/how-to-run/agents/shared-constraints.md` for agent constraints.
Read `$CLAUDE_PLUGIN_ROOT/skills/how-to-run/agents/project-environment-detector.md` for the full prompt template, detection tasks, and return format for the Project Environment Detector Agent.

Read these reference files and provide their content to the agent as context before the agent prompt:
- `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` — workspace detection
- `$CLAUDE_PLUGIN_ROOT/skills/init/references/project-detection.md` — monorepo/single-project detection
- `$CLAUDE_PLUGIN_ROOT/skills/init/references/tech-stack-detection.md` — manifest → tech stack + package manager
- `$CLAUDE_PLUGIN_ROOT/skills/how-to-run/references/how-to-run-sections.md` — signal-to-section mapping, build-system signals, source-dependency signals

The detector only needs to set `Triggered: yes` when no manifest or build-system signal matches; it does NOT execute the fallback procedure. The procedure itself is loaded by the main SKILL context only when the trigger fires (see Step 1 Checkpoint).

Launch 1 `general-purpose` Agent tool call using the prompt from project-environment-detector.md, prepended with the shared constraints and reference file contents above. The agent detects: build system & toolchain, source dependencies, SDKs & system packages, hardware/OS requirements, tech stack, package manager, project structure, external services, env config, infrastructure signals, and dev workflow signals.

Wait for the agent to complete. Use the agent's **Context Detection Results** to populate the Step 1 Checkpoint below.

### Step 1 Checkpoint

Print a **Context Summary** from the agent's Context Detection Results. For the External-service-default-endpoints bullet, read each config file the agent flagged as the service source (e.g., `docker-compose.yml`, `.env.example`, `appsettings.json`, `application.yml`) and derive the endpoint label yourself before printing — the detector does not produce this field.

- **Build system & toolchain** (e.g., CMake >= 3.20 with MSVC, cargo, npm scripts, Gradle 8.x)
- **Tech stack(s)** and **package manager(s)**
- **Project structure** (single / monorepo with subprojects / multi-repo with repos)
- **Workspace kind** (value from the detector's *Workspace kind* field — see `how-to-run-sections.md` §Workspace-Kind Command Branches for the per-kind install/build/run command table Step 4 consumes). Never emit workspace-wide commands that don't match the detected kind.
- **Source dependencies** (git submodules from `.gitmodules`, sibling repos detected in build/CI files, CMake `FetchContent` / `ExternalProject`)
- **SDKs & system packages** (Vulkan, CUDA, Qt, JDK, .NET SDK, MSVC Build Tools, etc. — only if detected)
- **External services detected** (list each service with a trailing `(candidate)` marker when the detector's `Confidence` column is `candidate`, and its source — e.g., "PostgreSQL — source: docker-compose.yml; OpenIdConnect (candidate) — source: appsettings.development.json:42"). Compose-confirmed services render with no marker; Task 5b framework-config candidates render with `(candidate)`.
- **External service default endpoints** (per service: raw default endpoint from the referenced config file + one label — `local-endpoint` for `localhost` / empty / unknown, `remote-endpoint` for any other hostname/FQDN, `ambiguous` if the config file is missing or unreadable).
- **Environment config files found** — list each file reported by the detector's Environment Setup table with its format appended in brackets (e.g., `src/Web/config/appsettings.development.json [json]`, `config/application.yml [yaml]`, `.env.example [dotenv]`).
- **Schema bootstrap scripts** (list the detector's Schema Bootstrap table entries with their invocation hint — e.g., "db/DatabaseNew.sql (sqlcmd -i db/DatabaseNew.sql), db/seeds.rb (rails db:seed)" — or "none" when the detector reports none).
- **Recommended developer tools** (list the detector's Recommended Developer Tools entries — e.g., "Google Chrome, SSMS, Visual Studio" — or "none" when empty).
- **Runtime version constraints** (e.g., "Node.js >=18 (engines.node), Python >=3.11 (python_requires)")
- **Runnable components** (one line per row of the detector's Components table, e.g., "`<WebProject>` (web) — requires PostgreSQL, Redis; `<WorkerProject>` (worker) — requires PostgreSQL, Redis, AWS SNS; `<frontend-pkg>` (frontend) — requires `<WebProject>`" — when the table has exactly one row, render the single row only; when the detector emits the literal `No runnable components detected.`, render that sentinel verbatim). Step 4 renders one `#### <Component> (shell N)` subsection per component in Running in Development, with a `Boot order:` header and per-component `Requires:` list.
- **Runtime bind ports** (per-component bound port from launch configs or source grep, e.g., "`<WebProject>`: 51914 (launchSettings.json:6), `<WorkerProject>`: 51915 (launchSettings.json:20)" — when the detector emits the literal `No bound runtime ports detected.`, render that sentinel verbatim). These are the ports Step 4 may quote in `Expected result:` URLs; any port the detector could not attribute to a file MUST be absent from this bullet.
- **Hardware / OS requirements** (GPU, USB/serial, OS version — only if detected)
- **Dev workflow signals** (Docker-based, Makefile-based, script-based, process runner, etc.)

Use `AskUserQuestion` — header "Context review", question "Does this capture the project correctly?":
- **Looks good** — "Proceed with detected context"
- **Correct first** — "Some details are wrong or missing"

If "Correct first": use `AskUserQuestion` — header "Corrections", question "What should be changed?" (free text). Apply the corrections to the Context Detection Results in memory, recomputing the `Unsupported-Stack Fallback → Triggered` flag if the correction changes the detected language or stack, and re-print the updated Context Summary. Re-confirm.

**Unsupported-Stack Fallback.** If the Context Detection Results show `Unsupported-Stack Fallback → Triggered: yes`, read `$CLAUDE_PLUGIN_ROOT/skills/init/references/unsupported-stack-fallback.md` and run its 5-step procedure here, using the reported **Detected language(s)** and **Evidence** as input. Use `WebSearch` for step 2 (research); enforce the step 3 validation rules before presenting any command; use `AskUserQuestion` for step 4 (approval). Commands approved here feed Step 4 content generation as if from a recognized stack; commands skipped (search failed or user declined) render as `"not found"` in the affected sections.

**LLM-knowledge fallback (how-to-run only).** If WebSearch is unavailable or returns no results for the detected language, use general knowledge to propose standard install/build/run/test commands for that language. Mark these commands as "inferred (not web-verified)" when presenting them for user approval in step 4. If the user declines, treat as a graceful skip.

## Step 2: Scan Existing Instructions (agent-assisted)

Delegate documentation scanning to an audit agent that cross-checks existing docs against the detected project state.

**Framing:** The auditor treats findings in every file *except* `HOW-TO-RUN.md` as hypotheses. Every fact will be verified against the detector's Context Detection Results before being used in generated content. Facts that contradict the codebase are logged as outdated and will be reported in Step 6 — they are NOT corrected in their source files.

Read `$CLAUDE_PLUGIN_ROOT/skills/how-to-run/agents/shared-constraints.md` for agent constraints.
Read `$CLAUDE_PLUGIN_ROOT/skills/how-to-run/agents/how-to-run-auditor.md` for the full prompt template, audit tasks, and return format for the How-to-Run Auditor Agent.

Read these reference files and provide their content to the agent as context before the agent prompt:
- `$CLAUDE_PLUGIN_ROOT/skills/init/references/readme-section-detection.md` — heading patterns, section boundary detection, classification rules

Launch 1 `general-purpose` Agent tool call using the prompt from how-to-run-auditor.md, prepended with the shared constraints and reference file contents above. **Provide the Context Detection Results from Step 1 as context** at the start of the agent prompt (before the shared constraints, readme-section-detection.md content, and agent template). The agent reads existing docs in priority order, applies heading detection, classifies each aspect against the detected state, and identifies outdated-elsewhere and unverifiable claims.

Wait for the agent to complete. Use the agent's **How-to-Run Audit Results** for the Step 3 assessment.

## Step 3: Present Assessment and Plan

Present findings as a table with status per aspect (use the classification from the How-to-Run Audit Results).

For the **External Services** aspect, expand it into a sub-table with columns **Service | Recommended runtime | Alternative | Reason**:

- Recommended runtime values: `Docker-preferred` / `Shared-cloud primary (<provider>)` / `Local install only`.
- Alternative values: `Docker (offline)` / `Local install` / `—`.
- Read `$CLAUDE_PLUGIN_ROOT/skills/how-to-run/references/external-services-docker.md` and produce one row per service by applying its Decision Heuristics to the Step 1 Checkpoint's endpoint labels.
- Do not emit a per-service `AskUserQuestion` here — the reference file documents the single exception (the Step 4 multi-select downgrade prompt for rule 5's post-web-search re-confirmation).

**If a `HOW-TO-RUN.md` already exists and all aspects are "Found & accurate":** Report to user — no action needed. Skip to Step 6 (report only).

**If outdated items found:** Show current content vs proposed correction for each.

**Caution rule:** For existing content that seems intentionally unusual or whose purpose is beyond what the codebase reveals — **flag explicitly and ask** rather than silently including or excluding. Examples: custom startup scripts with non-obvious flags, environment variables with no clear source, instructions referencing external systems not visible in the codebase, documented hardware requirements the detector cannot confirm.

For each "Documented but unverifiable" item from the audit, use `AskUserQuestion` to ask whether to include it in `HOW-TO-RUN.md`. Show the source file and heading so the user can judge. When the user approves an item, record it in an in-memory `approved-unverifiable-items` list as `{aspect, source_file, source_heading, text, rendered_line}`. Validate `source_file` strictly against `^[A-Za-z0-9][A-Za-z0-9._/-]{0,128}$`, then split on `/` and drop the entry if any resulting segment is empty, `.`, or `..` — mirrors the submodule/sibling path validation in project-environment-detector.md Task 0b so `docs/../etc/passwd` cannot render as a plausible-looking attribution. Sanitize `source_heading`: truncate to 80 chars; strip backtick, `` ` ``, `<`, `>`, `\`, newline, carriage return, NUL, and any Cc/Cf character; then escape every remaining `[` as `\[` and every `]` as `\]` before rendering, so a heading like `[Source](javascript:alert(1))` cannot form a clickable link inside the attribution preamble `Per <source_file> "<source_heading>": ...`. `\` is stripped (not escaped) because stacked backslashes combined with bracket escapes can produce unclosed link labels that confuse downstream markdown consumers. Do not whitelist heading characters — legitimate markdown headings routinely contain `:`, `'`, `!`, `?`, `+`, `#`, en/em dashes, and other punctuation. `rendered_line` is populated in Step 4 (it is the exact line Step 6 will exempt).

Use `AskUserQuestion` — header "How to Run Documentation", question "How would you like to proceed?":
- **Create/Update** — "Generate HOW-TO-RUN.md (I'll write directly if no file exists; show diff first if one exists)"
- **Skip** — "No changes needed"

If user selects **Skip**, jump to Step 6 (report only).

## Step 4: Generate Content

Read these reference files before generating content:

- `$CLAUDE_PLUGIN_ROOT/skills/how-to-run/references/how-to-run-sections.md` — section templates and signal-to-section mapping.
- `$CLAUDE_PLUGIN_ROOT/skills/how-to-run/references/external-services-docker.md` — Docker-vs-local-vs-shared-cloud decision heuristics, web-search recipe, snippet templates, citation format, and registry allowlist for the External Services section.

Before generating content, run `external-services-docker.md` §Web-Search Recipe for every Step 3 row whose Recommended runtime is **Docker-preferred** or whose Alternative is **Docker (offline)**. After the recipe runs, if at least one service was downgraded per §Decision Heuristics rule 5, emit a single **multi-select downgrade prompt** before Step 5 writes the file:

- `AskUserQuestion` with `multiSelect: true`, header `"Docker alternative"`, question `"The Docker alternative failed validation for these services. Keep Docker anyway or fall back?"`.
- One option per downgraded service, labelled `<service>: <one-line failure reason>` (examples: `Redis: Docker Hub page did not list port in structured form and no catalogue rescue`; `LocalStack: pro-tier signal detected — LOCALSTACK_AUTH_TOKEN listed in env-var names`). The failure reason comes from the specific validation that tripped in §Web-Search Recipe.
- Each option's description states what will be written if checked (Docker alternative kept) vs unchecked (Shared-cloud no-Docker template).
- Checked services render the Docker alternative template; unchecked render the [Shared-cloud, no Docker alternative](references/external-services-docker.md#shared-cloud-no-docker-alternative) template.
- Skip the prompt entirely if no services failed validation.

Generate only sections with at least one detected signal. Order is fixed; only inclusion varies. Full catalog:

1. **Prerequisites** — OS version constraints, hardware requirements (GPU, USB, serial), system tools (docker, make, etc.), version managers (nvm, pyenv, rustup) if config files detected
2. **Toolchain & SDKs** — compiler, build-tool, language SDK, and domain SDK requirements. See *Additional Detection Hints* in `how-to-run-sections.md` for additional detection signals and the *Build System Detection* table below it for per-file extraction rules. Group per-OS install commands (Windows / macOS / Linux) when multiple OSes are plausible.
3. **Source Dependencies** — fix-after-clone only: `git submodule update --init --recursive` when `.gitmodules` is present (the primary `git clone [--recursive]` lives in Installation, section 4), sibling repos that must be cloned alongside this one (list paths + clone URLs), CMake `FetchContent`/`ExternalProject` notes.
4. **Installation** — clone command, language-level package install (correct PM and prefix), post-install steps (code generation, database migrations, raw-SQL schema bootstrap, seed scripts, asset compilation), vendored-dependency bootstrap (vcpkg, Conan).
5. **External Services** — render per `how-to-run-sections.md` §External Services (Branch A/B/Hybrid); apply `external-services-docker.md` for per-service classification, snippets, web-search recipe, citations, allowlist, and sanitization (single source of truth for these rules). For env-var name slots use `<REQUIRED_ENV_VAR>` or the actual vendor-documented name; for value slots use `<placeholder>` or a vendor-documented constant. Substitute every template placeholder with the Step 4 WebFetch-derived values before writing the file: `<host-port>` and `<container-port>` with numeric ports, `<container-volume-path>` with the absolute volume mount path, and `<registry>/<name>:<stable-tag>` with the validated image reference. Substitute `<project-slug>` with the kebab-cased project name from the Step 1 Checkpoint and `<service-slug>` with the kebab-cased service name from the detector's External Services table — both lowercased, ASCII-only, with `[^A-Za-z0-9]+` collapsed to a single `-`, and any leading/trailing `-` trimmed. The literal `<REQUIRED_ENV_VAR>`/`<placeholder>` forms are the only placeholders permitted to remain unsubstituted (by design — they signal a required user action). Never copy real secrets and never use model-memory image names.
6. **Environment Setup** — render the sub-template that matches the detector's Environment Setup table: (a) dotenv — `cp .env.example .env` plus variable descriptions for `.env.example` / `.env.sample` / `.env.template` rows; (b) config-file-driven — list top-level sections from rows whose Format is `json` / `yaml` / `properties` / `exs` / `php` / `toml`. When both kinds of rows exist, render (a) first and (b) second under the same H3. See `how-to-run-sections.md` §Environment Setup for the exact templates. Never include real secret values — only describe what each variable or section is for.
7. **Build** — explicit compile/link command for compiled stacks (e.g., `cmake --build build --config Debug`). Omit for interpreted stacks where build is conflated with run.
8. **Running in Development** — the primary dev command(s) OR the command to launch the produced binary OR the engine launcher. What URL/port to expect for web/server stacks, what window/output to expect for desktop/game stacks. For monorepos: how to run specific subprojects AND how to run everything together. For docker-only setups (Dockerfile + docker-compose + no obvious local-run scripts): Docker-based instructions as the primary path.
9. **Running Tests** — test command, coverage command if available.
10. **Common Issues** — only if clear signals exist (e.g., `.nvmrc` → mention `nvm use`; docker services → mention `docker compose up -d` must run first; private registry → mention authentication; submodules → mention `git submodule update --init --recursive` after pull).

**Content principles:**
- Direct, imperative instructions ("Install dependencies:" not "You should install dependencies")
- Exact commands with detected package manager and build system (from `tech-stack-detection.md` prefix rules and `how-to-run-sections.md` build-system rows)
- Version numbers from manifest / build-file constraints only — never guess versions
- Commands ordered as a new developer would run them (prerequisites → toolchain → source deps → install → services → env → build → run)
- For monorepos: workspace-level install first, then per-subproject run instructions. When more than 5 subprojects, use a quick-reference table (columns: Subproject, Dev command, URL/port) instead of inline per-subproject listings — see *Scaling Guidance* in `how-to-run-sections.md`.
- For docker-only dev setups: Docker-based instructions as primary path, bare-metal as secondary if discernible
- **Table of contents:** if generating more than 4 sections, include a linked markdown TOC immediately after the H1 heading
- **Verify before including:** any content sourced from existing docs (README.md, CONTRIBUTING.md, etc.) must match the detector's Context Detection Results. Contradictions go to the Step 6 "Outdated info elsewhere" report and are NOT copied into `HOW-TO-RUN.md`.
- **Candidate services** (detector Task 5b rows with `Confidence: candidate`): render in the External Services overview table with a `(candidate)` marker in the Service column (e.g., `OpenIdConnect (candidate)`), and in the per-service H3 subsection heading. Do NOT emit a per-service `AskUserQuestion` prompt for candidates — the user already reviewed and approved the Context Summary in Step 1 and can drop any incorrect candidate via the Step 1 "Correct first" flow. Silent inclusion (no marker) is disallowed because the reader cannot otherwise distinguish a config-file grep hit from a compose-confirmed service.
- **Humanize caveats.** Any caveat emitted from a Step-4 recipe must describe *what the reader should know or do*, not *why the skill decided something*. See `external-services-docker.md` §Web-Search Recipe step 3 "Caveat rendering" for the canonical phrasings and the full list of caveat kinds.
- **Reject unverifiable exact counts.** Do not write exact numeric counts ("15 `.csproj` projects", "23 services", "7 subprojects") unless Step 6 verification can re-derive the count from the filesystem via `Glob`. When the detector cannot confirm a count, use "multiple", "several", or omit the quantifier entirely. Exception: counts the detector explicitly reports (subproject enumeration, environment variable counts, repo counts in a multi-repo workspace) are verified by construction and may be cited verbatim.
- **Never assert an unobserved path.** Do not render a specific filesystem path (e.g., `scripts/database/26.10.00/`, `migrations/0042_add_users.py`, `docs/release/2026.03/`) in prose unless the path appears verbatim in one of the detector's return-format tables (Source Dependencies, Environment Setup, Schema Bootstrap, Subprojects, Repos) or the path can be re-observed via `Glob` at Step 6 time. When the doc needs to reference "the latest version folder" or "the newest migration", use a generic phrasing — "the latest folder under `scripts/database/`", "the newest file under `migrations/`" — and do NOT extrapolate a leaf name from the version string in package metadata, from the current date, or from general knowledge. Paths from manifests, lock files, and explicit detector enumerations are verified by construction and may be cited verbatim.
- **Never guess runtime ports.** Runtime port numbers in `Expected result:` lines, troubleshooting bullets, and any URL of the form `http://localhost:<N>` or `http://127.0.0.1:<N>` must come from the Step 1 Checkpoint *Runtime bind ports* bullet (sourced from the detector's Runtime Ports table) OR from the detector's External Services table Port column (compose / config-file ports). When no bound port is found for a component, OMIT the port from the `Expected result:` URL — write `Expected result: <component> starts listening (see <launch-config-file> for the bound port).` Never substitute a framework default port.
- **Explain non-idiomatic wrapper commands.** When the detected dev/build/test command is a wrapper that invokes non-obvious additional steps, render a single-line `> <wrapper> runs: <expanded form>` explanation below the code block. See `how-to-run-sections.md` §Running in Development for the exact template and when to skip (direct aliases like `npm run dev` → `next dev`).
- **Approved unverifiable items (from Step 3):** for each entry in the `approved-unverifiable-items` list, render it as a sentence or bullet in the matching aspect's section. The inner content uses the exact form `Per <source_file> "<source_heading>": <sanitized_text>` (e.g., `Per README.md "Source Dependencies": Developers without access can still build the frontend, but custom theming will be missing.`); `source_file` and `source_heading` were already validated/sanitized at record time in Step 3 and render as-is. Sanitize `text`: truncate to 240 characters, then strip every backtick, `` ` ``, `<`, `>`, `\`, `&`, newline, carriage return, NUL, and any Unicode category Cc/Cf character. (`&` is stripped because CommonMark-conformant renderers — including VS Code's preview and most IDE markdown previewers — decode HTML numeric character references inside link destinations and inline text per CommonMark §6.5; without this strip, an approved fragment like `[docs](&#106;avascript&#58;alert(1))` would survive both the `](` URL allowlist below and the `!`-preceding-`](` image check, then decode to `<a href="javascript:alert(1)">` at render time.) Keep `[`, `]`, `(`, `)` so existing markdown links render — but scan EVERY `](` in the sanitized text and reject the entry entirely if ANY of them is followed by anything other than `https://`, `http://`, or a relative-path target matching `^[^:/\s\\][^:)%\s\\]*\)` (the `\\` exclusion in both the first-char class and the body class is a defense-in-depth backstop — `\` is also pre-stripped above, but keeping it in the regex means a future strip-list edit cannot accidentally allow `\\evil.com\share` UNC-path targets through) (first char is not `:`/`/`/whitespace AND the inner class excludes `:` so embedded schemes like `javascript:` / `data:` / `file:` / `mailto:` are rejected, AND excludes `%` so percent-encoded schemes like `javascript%3Aalert(1)` are rejected on renderers that pre-decode; additionally split the matched path on `/` and reject the entry if any segment equals `..`). Reject every `](` whose preceding character is `!` — that is markdown image syntax, and an approved README attribution never legitimately needs an inline image (an `https://attacker/x.svg` payload would otherwise pass the URL check and active-content-rendering markdown previewers could execute embedded scripts). Also reject the entry if the sanitized text contains a reference-style link definition — a `]` followed by optional whitespace, `:`, optional whitespace, and a token containing `://` whose scheme (the characters before `://`, case-insensitive) is not exactly `http` or `https` (e.g., `[click][x]` paired with `[x]: javascript://alert(1)` or `[x]: data://text/html,...` would otherwise bypass the inline-link scan above because `[x]` never forms a `](` sequence). Tokens with no `://` are not rejected — a benign `[note]: description here` passes. If the entry passes every check, store the full rendered line — exactly as it will be written to `HOW-TO-RUN.md`, including any leading list marker (`- `, `* `, `1. `) or indentation — back into the entry's `rendered_line` field so Step 6 can exempt it by exact match. Entries that fail any check are **removed** from `approved-unverifiable-items` (so their `rendered_line` cannot remain unset and accidentally exempt blank lines in Step 6).

## Step 5: Place Content

**Write scope (repeat):** The only file this skill is ever permitted to create or modify is `HOW-TO-RUN.md` at the project / workspace root. Never modify `README.md`, `CONTRIBUTING.md`, `docs/*`, `BUILDING.md`, `INSTALL.md`, or any other file — not even to add a link. Existing docs are input only.

**Approval rule:**
- **If `HOW-TO-RUN.md` does not exist yet:** write it directly without asking for approval. The user already approved the plan in Step 3 and there is nothing to overwrite.
- **If `HOW-TO-RUN.md` already exists:** show the full diff (section-by-section when updating, full content when replacing) and wait for user approval before writing. Never silently replace existing content in a file that already exists.

### Placement rules by topology

**Single project:** Create or update `HOW-TO-RUN.md` at the repo root.

**Monorepo:** Create or update `HOW-TO-RUN.md` at the repo root, covering whole-project scope — workspace-level install, how to start shared services, how to run specific subprojects, how to run everything together.

**Multi-repo workspace:** Create or update `HOW-TO-RUN.md` at the workspace root. Direct-to-the-point content: repo map (name, path, purpose), how to clone all repos (submodules if applicable), shared prerequisites, how to start shared external services, how to run the full system. This file is not version-controlled (the workspace root has no `.git`).

### When dev instructions already live in README.md / CONTRIBUTING.md / etc.

No `AskUserQuestion` prompt. The skill silently copies any *verified* content from those files into `HOW-TO-RUN.md` (verification happened in Step 2 + Step 4 against the detector's results). Source files are not modified and the original content stays where it is. Any *contradicting* content is logged for the Step 6 "Outdated info elsewhere" report and is NOT copied into `HOW-TO-RUN.md`. Any *unverifiable* content was already resolved in Step 3's per-item user prompts.

### Cautious editing rules (for existing HOW-TO-RUN.md)

- **Never delete** existing content outside the sections being replaced.
- Preserve formatting, badges, images, and links inside sections not being updated.
- If the existing `HOW-TO-RUN.md` structure is too unusual to safely update a section, show the generated content to the user and ask where to place it manually.

## Step 6: Verify and Report

If no files were modified (skip or no-action path), skip verification and proceed directly to the report.

- Read back the modified or created `HOW-TO-RUN.md`.
- **Verify:** all commands use the correct package manager prefix, prerequisite versions match manifest constraints, build-system commands correspond to the detected build files, submodule paths in `HOW-TO-RUN.md` actually exist in `.gitmodules`, sibling-repo paths actually appear in build/CI files, directory paths match the actual filesystem, external service names match docker-compose service definitions, environment variable names match `.env.example`.
- **Verify External Services subsections** — re-apply every rule from `external-services-docker.md` §Citation Format (for every `- Source: [<title>](<url>)` line), §Web-Search Recipe step 4 and §Registry Allowlist (for every `docker run` snippet's image reference), §Web-Search Recipe step 5 (for every `-e`, `-p`, `-v`, and image-reference line — `- Source:` lines are governed by §Citation Format, not step 5's URL regex), and the Snippet Templates' env-var rule. Step-6-only additions:
  - Tag preference: reject any bare moving label (`latest`, `stable`, `edge`, `nightly`, `canary`, `main`, `current`, `rolling`) written into any image reference. The "no numeric tag on the vendor page" exception from §Web-Search Recipe step 6 must have been applied at Step 4 and is not re-checked here; Step 6 enforces the stricter rule because at read-back time the vendor-page tag list is no longer available.
  - Volume-path slug check: every `-v` flag's left side must match `^[A-Za-z0-9][A-Za-z0-9._-]*-[A-Za-z0-9][A-Za-z0-9._-]*-data$` (the rendered `<project-slug>-<service-slug>-data` shape, with placeholders substituted by Step 5).
  - **User-override audit:** if any Docker alternative section in the written file corresponds to a service the user elected to keep via the Step 4 multi-select downgrade prompt, verify that the written snippet still passes §Web-Search Recipe step 5 sanitization (image-ref regex, env-var name/value regex, port regex, volume-path regex, URL regex), the §Registry Allowlist match, and the §Web-Search Recipe step 6 tag-preference rule. The override permits the user to accept a weaker source (e.g., port or volume rescued from the §Canonical Image Catalogue per §Web-Search Recipe step 3's catalogue short-circuit) — it does NOT permit bypassing regex sanitization, allowlist matching, or tag preference. If the snippet cannot pass these checks even with the override, surface the specific failing rule to the user; after user approval rewrite the affected section of the already-written `HOW-TO-RUN.md`, either with a corrected snippet or by replacing it with the [Shared-cloud, no Docker alternative](references/external-services-docker.md#shared-cloud-no-docker-alternative) template, then re-verify.
- **Re-validate detector-sourced tokens** in the written file: every package identifier in `HOW-TO-RUN.md` must still match `^[A-Za-z0-9][A-Za-z0-9._+:@/-]{0,99}$` with no `://`, `.`, `..`, or empty path segments after splitting on `/` or `:`; the project name must match `^[A-Za-z0-9._ -]{1,64}$` or be exactly `(unknown)`; hardware/OS mentions must correspond to a canonical token from the detector's Task 0d search lists; recommended developer tool mentions (under Prerequisites' *Recommended developer tools* sub-list) must correspond to a canonical token from the detector's Task 0d2 search lists; schema-bootstrap filenames emitted in Installation's Schema Bootstrap block (`sqlcmd -i <file>`, `psql -f <file>`, `mysql < <file>`, `python manage.py loaddata <file>`, `tsx prisma/seed.ts`, etc.) must still match `^[A-Za-z0-9][A-Za-z0-9._/-]{0,128}$` with no empty/`.`/`..` segments after splitting on `/` and no segment whose first character is `-` (which would otherwise be parsed as a CLI option by `psql -f` / `sqlcmd -i`); config-file section names echoed under Environment Setup's config-file-driven body and as `(candidate)` service H3 headings must still match the shared top-level-section-name allowlist `^:?[A-Za-z_][A-Za-z0-9_.-]{0,63}$`; config-file paths echoed in External Services *Source* columns and Environment Setup listings (e.g., `src/Web/config/appsettings.development.json`) must still match `^[A-Za-z0-9][A-Za-z0-9._/-]{0,128}$` with no empty/`.`/`..` segments after splitting on `/`. Reject any line, outside fenced code blocks the skill itself generated, that echoes free-text prose — whether taken from `README.md`/`CONTRIBUTING.md`/`docs/*` or supplied by the user in the Step 1 "Corrections" response — EXCEPT lines that match (by full-line equality after trimming leading/trailing whitespace) the `rendered_line` field of any entry in the `approved-unverifiable-items` list recorded in Steps 3–4. Substring matches are NOT exempt: an exempted line must be *exactly* the approved rendering, otherwise adversarial README prose containing an approved fragment as a substring could bypass the check.
- **Specific-Token Audit** — prevents hallucinated ports, paths, versions, and counts from reaching the reader. Build a `grounded-tokens` set from the detector's return format:
  - **Ports:** every `Port` cell in the External Services table, plus every `Port` cell in the Runtime Ports table — the latter carries a `Source: <file>:<line>` citation the skill re-reads at audit time.
  - **Paths:** every path cell in Source Dependencies, Environment Setup (the *File* column), Schema Bootstrap (*File* + *Directory*), Subprojects (*Path*), Repos (*Path*). A path counts as grounded only if the detector reported it verbatim; no prefix/suffix expansion is allowed (the detector reporting `scripts/database/` does NOT ground `scripts/database/26.10.00/`).
  - **Version strings:** every `Constraint` cell in the Runtime Version Constraints table, every `Min version` cell in the Build System & Toolchain table, every literal pinned version from a `.python-version` / `.ruby-version` / `.nvmrc` / `rust-toolchain.toml` / `.tool-versions` file when that file is listed in the detector's Dev Workflow Signals *Version managers* field (re-read the file at audit time).
  - **Counts:** the row count of any detector table (Subprojects, Repos, External Services, Environment Setup, Schema Bootstrap); the `Variable count` cell of each Environment Setup row.

  For every specific token appearing **in prose** (outside fenced code blocks the skill itself generated) in the written file:
  - **Port check:** any integer 1–65535 that appears immediately after `port`, `localhost:`, `127.0.0.1:`, `listens on`, `bound to`, `listening at`, or `:`-prefixed at the end of a `http(s)://<host>:` URL, must appear in the grounded ports set. Inside an `Expected result:` line, apply the same port-context requirement — only flag integers that carry one of these port-context tokens, so a phrase like `Expected result: health probe responds within 5 seconds` does not trigger on `5`. On miss, re-read the cited Runtime Ports source file; if the file's current value differs from the generated text, reject and force either a rewrite with the observed value or deletion of the port (per the *Never guess runtime ports* Content Principle — omit the URL, do not substitute a framework default).
  - **Path check:** every `<dir>/<subdir>` or `<name>.<ext>` fragment in Installation / Source Dependencies / Environment Setup / Running in Development / Common Issues prose must either (a) be in the grounded paths set verbatim, OR (b) still exist on the filesystem. **Before globbing, escape glob metacharacters in the prose-derived fragment** — `*`, `?`, `[`, `]`, `{`, `}` survive the approved-unverifiable-items sanitization above, so an unescaped fragment like `src/[a-z]/secret.txt` would be interpreted as a glob character class and spuriously "exist" whenever any single-letter directory matches (a `**/*` fragment would always pass). For fragments that contain `/`, `Glob` the escaped literal fragment. For bare-filename fragments (no `/`, e.g., `appsettings.Development.json`, `docker-compose.yml`, `Dockerfile`, `Makefile`), `Glob` `**/<escaped-full-name>` (the entire fragment as one literal token — do NOT split on `.` and re-join, because extensionless idiomatic filenames like `Dockerfile` / `Makefile` / `Gemfile` / `Procfile` / `Justfile` / `Rakefile` would otherwise produce `**/Dockerfile.` and never match). **Exclude generated/dependency directories** from the filesystem check — pass `node_modules/`, `vendor/`, `.venv/`, `venv/`, `target/`, `dist/`, `build/`, `.git/`, `.next/`, `.nuxt/`, `coverage/`, `__pycache__/` to Glob's exclude list (a hallucinated `src/utils/helpers.js` would otherwise spuriously match a transitive `node_modules/<pkg>/src/utils/helpers.js` and bypass the *Never assert an unobserved path* principle). Reject paths that fail both checks (per the *Never assert an unobserved path* Content Principle).
  - **Version check:** any `X.Y.Z`, `vX.Y`, or `X.Y+` that appears in Prerequisites / Toolchain & SDKs prose must match either a grounded version string verbatim OR a version-manager file's current content at audit time.

  When a token fails the audit, the skill MUST either rewrite the line using a grounded token or delete the specific token entirely and fall back to a hedged phrasing (`"the bound port"`, `"the latest folder"`, `"a supported version"`) before finalising. Never silently accept an ungrounded token.
- **Unverified-Count filter** — catches "15 `.csproj` projects", "47 modules", "23 services" style prose the Step 4 *Reject unverifiable exact counts* Content Principle forbids. **Strip backticks from each line first** (so `15 \`.csproj\` projects` is normalised to `15 .csproj projects` — without this, the modifier character class below would not match the file-extension token wrapped in backticks, which is the canonical rendered form). Then scan every line outside fenced code blocks against the case-insensitive regex `\b\d{1,4}\s+(?:[\w.@/_-]+\s+){0,2}(?:projects?|modules?|packages?|services?|subprojects?|repos?|files?|dependencies|jars?|binaries|microservices?|workspaces?|crates?|components?|containers?|env(?:ironment)?[\s-]*(?:vars?|files?|variables?)|configurations?|profiles?|endpoints?|schemas?|tables?)\b`. On match, the count passes only when it equals one of: (a) the row count of one of the detector's tables named in the grounded-tokens *Counts* clause above, OR (b) the result of a `Glob` performed at Step 6 time for the claimed noun (e.g., count of `**/*.csproj` files for "N .csproj projects"). Unbacked counts MUST be rewritten — drop the number ("15 `.csproj` projects" → "the `.csproj` projects", or "`.csproj` projects in the solution") or swap it for a hedged quantifier (`"multiple"`, `"several"`). The detector's own enumeration tables may cite counts verbatim because they are re-derivable from the filesystem at Step 6 time.
- **If any check fails:** show the correction to the user, wait for approval, apply it, then re-verify.

**Report** to the user: what was created or updated in `HOW-TO-RUN.md`, which sections were included, and any aspects that were intentionally skipped (with reason).

**Outdated info found in other files (not modified):** Grouped by source file, list every fact the auditor found in `README.md` / `CONTRIBUTING.md` / `BUILDING.md` / `INSTALL.md` / `docs/*` that contradicted the detector's Context Detection Results. For each entry show: source file + heading + the documented text + what the detector found instead + suggested fix for the user to apply manually. Make explicit: **"The skill did NOT modify any of these files. They are listed so you can update them yourself if you want them to match reality."** If no contradictions were found, state "No stale setup info found in other files."

**Recommend next skill:**
- If `HOW-TO-RUN.md` was created or updated: recommend `/optimus:commit` to commit the new or modified file.
- If `/optimus:init` has not been run (no `.claude/.optimus-version`): recommend `/optimus:init` for AI-assisted development setup.
- If test instructions were thin or absent: recommend `/optimus:unit-test` to establish test coverage.
- Otherwise: recommend `/optimus:tdd` for new feature work.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
