---
name: codebase-overview
description: "Systematic codebase exploration and architecture mapping."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
context: fork
routing:
  triggers:
    - "onboard to codebase"
    - "codebase structure"
    - "what does this project do"
    - "give me an overview"
    - "summarize this repo"
    - "understand this codebase"
  category: analysis
  pairs_with:
    - codebase-analyzer
    - generate-claudemd
---

# Codebase Overview Skill

Systematic 4-phase codebase exploration that produces an evidence-backed onboarding report. Phases run in strict order — DETECT, EXPLORE, MAP, SUMMARIZE — because later phases depend on context established by earlier ones. This skill accelerates reading the codebase but does not replace it.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| example-driven tasks, errors | `examples-and-errors.md` | Loads detailed guidance from `examples-and-errors.md`. |
| language-specific discovery commands per exploration phase | `exploration-strategies.md` | Loads detailed guidance from `exploration-strategies.md`. |
| writing the 12-section overview report | `report-template.md` | Loads detailed guidance from `report-template.md`. |

## Instructions

Execute all phases autonomously. Verify each gate before advancing. Consult `references/exploration-strategies.md` for language-specific discovery commands.

Before starting any exploration, read and follow any `.claude/CLAUDE.md` or `CLAUDE.md` in the repository root because project-specific instructions override default behavior.

This is a **read-only** skill — keep all project files unmodified because the goal is observation, not mutation. Likewise, leave application execution and test running to other skills because those are execution concerns outside this skill's scope. For deep domain analysis, route to a specialized agent instead.

> See `references/examples-and-errors.md` for worked examples and error handling procedures.

### Sensitive-Files Guardrail

Check every file path against this list BEFORE reading because secrets leaked into exploration output are hard to retract and easy to miss. Skip silently without logging the file contents or path.

```
# Secrets and credentials
.env, .env.*, *.pem, *.key, credentials.json, secrets.*, *secret*, *credential*, *password*

# Authentication tokens
token.json, .npmrc, .pypirc

# Cloud provider credentials
.aws/credentials, .gcloud/, service-account*.json
```

### Phase 1: DETECT

**Goal**: Determine project type, language, framework, and tech stack.

**Step 1: Examine root directory**

Start from the current working directory because that is the project the user is asking about.

```bash
ls -la
```

Identify configuration files that indicate project type:
- `package.json` -> Node.js/JavaScript/TypeScript
- `go.mod` -> Go
- `pyproject.toml`, `requirements.txt`, `setup.py` -> Python
- `pom.xml`, `build.gradle` -> Java
- `Cargo.toml` -> Rust
- See `references/exploration-strategies.md` for complete indicator table

Always detect project type before reading source files because framework context changes how you interpret code (e.g., a `models/` directory means something different in Django vs. Express).

**Step 2: Read primary configuration**

Based on detected type, read the main config file. Preference order:
- Python: `pyproject.toml` > `setup.py` > `requirements.txt`
- Node.js: `package.json`
- Go: `go.mod`

Extract: project name, dependencies, language version, build system, scripts/commands.

**Step 3: Identify frameworks and tooling**

```bash
ls -la manage.py next.config.js nuxt.config.js angular.json 2>/dev/null
ls -la Makefile Dockerfile docker-compose.yml 2>/dev/null
ls -la .github/workflows/ 2>/dev/null
```

**Step 4: Check for CLAUDE.md**

Read any `.claude/CLAUDE.md` or `CLAUDE.md` in the repository root. Follow its instructions throughout remaining phases.

**Step 5: Document findings**

Use the DETECT Results template from `references/examples-and-errors.md`.

**Gate**: Project type identified (language + framework). Tech stack documented. Build/run commands known. Proceed ONLY when gate passes — skipping this gate leads to wrong architectural assumptions downstream.

### Phase 2: EXPLORE

**Goal**: Discover entry points, core modules, data models, API surfaces, configuration, and tests.

Explore only what is needed for the overview because speculative deep-dives waste tokens without proportional value. Limit to 20 files per category because representative samples are more useful than exhaustive coverage. If a category has more than 20 files, note the total count and state that you examined a representative sample.

On explicit user request, deep-dive into specific subsystems, generate architecture diagrams, include full file contents, export findings to a separate file, or analyze dependency vulnerability status. These are off by default because the standard overview does not require them.

**Step 1: Find entry points**

Use language-specific patterns from `references/exploration-strategies.md`. Read each entry point file to understand application bootstrapping.

For any language, look for:
- `main` functions or `__main__` modules
- Server/app initialization files
- CLI entry points declared in config

Config files alone are not enough to understand a project because they show dependencies, not architecture — always read entry points and core modules too.

**Step 2: Map directory structure**

```bash
find . -type d \
  -not -path '*/\.*' \
  -not -path '*/node_modules/*' \
  -not -path '*/venv/*' \
  -not -path '*/vendor/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  | head -50
```

Exclude noise directories (`node_modules/`, `venv/`, `vendor/`, `dist/`, `build/`, `__pycache__/`) because they contain generated or third-party code that obscures the project's own structure.

Categorize directories by layer — see the Directory Layer Categorization table in `references/examples-and-errors.md`.

**Step 3: Examine data layer**

Search for model, schema, and entity files. Read 3-5 representative files. Use the Data Layer Findings template from `references/examples-and-errors.md`.

Document: entity relationships, primary data structures and their fields, database technology, migration strategy.

**Step 4: Discover API surface**

Search for route, handler, and controller files. Read 3-5 key API files. Use the API Surface Findings template from `references/examples-and-errors.md`.

Document: endpoint structure and URL patterns, HTTP methods and request/response formats, authentication and authorization patterns, API versioning strategy.

**Step 5: Identify configuration**

```bash
ls -la .env .env.example config.yaml config.json settings.py 2>/dev/null
ls -la config/*.yaml config/*.json config/*.toml 2>/dev/null
```

Document: required environment variables and their purpose, external service dependencies (databases, APIs, caches, queues), feature flags or runtime options.

**Step 6: Examine test structure**

```bash
find . -name "*_test.*" -o -name "*.test.*" -o -name "*Test.*" -o -path "*/tests/*" \
  2>/dev/null | head -20
```

Document: testing framework, test organization (co-located vs separate directory), common patterns (fixtures, factories, mocks), coverage tooling.

**Gate**: Entry points identified. Core modules mapped. Data layer understood. API surface discovered. Configuration examined. Test structure documented. Proceed ONLY when gate passes.

### Phase 3: MAP

**Goal**: Synthesize findings into architectural understanding.

**Step 1: Identify design patterns**

Based on examined files, identify and document with evidence. Every architectural claim must cite an examined file and path because uncited claims cannot be verified and mislead readers. Use the Design Patterns template from `references/examples-and-errors.md`.

Verify architectural claims against source files because READMEs may be outdated or incomplete.

**Step 2: Map key abstractions**

Identify the 5-10 most important types, classes, or modules. Use the Key Abstractions template from `references/examples-and-errors.md`.

Document: core domain concepts, primary interfaces/abstractions, component communication (direct calls, events, queues).

**Step 3: Document data flow**

Trace a typical request from entry point through the full stack. Use the Request Flow template from `references/examples-and-errors.md`. All file paths in output must be absolute because relative paths are ambiguous when the report is read outside the project directory.

**Step 4: Analyze recent activity**

```bash
git log --oneline --no-decorate -10
```

Include recent commit themes (last 10 commits). Categorize: Feature development, Bug fixes, Refactoring, Infrastructure.

If not a git repository, note this limitation and skip this step.

**Gate**: Design patterns identified with file evidence. Key abstractions mapped (5-10 concepts). Data flow documented with absolute paths. Recent activity analyzed. Proceed ONLY when gate passes.

### Phase 4: SUMMARIZE

**Goal**: Generate structured overview report.

**Step 1: Generate report**

Use the template in `references/report-template.md`. Fill every section with evidence from examined files. Requirements:
- All file paths MUST be absolute
- All architectural claims MUST cite source files
- All commands MUST come from actual config files (package.json, Makefile, etc.)
- Empty sections MUST note why information is unavailable

Report facts without self-congratulation — show evidence, not descriptions of how thorough the exploration was. Every claim must have file-backed evidence because "report looks complete" is not the same as "report is complete."

**Step 2: Quality check**

Before outputting, verify:
- [ ] All 13 template sections addressed
- [ ] No placeholder text remains
- [ ] Every claim backed by file evidence
- [ ] Paths are absolute, not relative
- [ ] Commands are real, not guessed

Adjust the 20-files-per-category limit if a specific area needs deeper sampling — some projects concentrate complexity in one layer. Note any such adjustments in the report.

**Step 3: Generate "Where to Add New Code" section**

Append a prescriptive section to the report. For each major code category discovered during exploration, provide the directory, a concrete example file to use as a template, and any naming conventions.

```markdown
## Where to Add New Code

| I want to add... | Put it in... | Follow the pattern in... |
|-------------------|-------------|-------------------------|
| [category from exploration] | [directory path] | [concrete example file path] |
```

Every entry MUST reference a real file that already exists. If a category has no clear home, note that explicitly rather than guessing.

**Step 4: Post-exploration secret scan**

Before presenting results, scan all output for accidentally captured secrets:

```bash
grep -iE '(password|secret|token|api[_-]?key|auth|credential)\s*[:=]' <output_file> || true
grep -E '(AIza|sk-|ghp_|gho_|AKIA|-----BEGIN)' <output_file> || true
```

If any matches are found: redact the matched lines (replace values with `[REDACTED]`), flag the finding, and note which file to review manually.

**Step 5: Output report**

Display complete markdown report to stdout. Generate the report to stdout by default because most users need inline context, not a separate file. If export behavior is explicitly requested, also write to file.

Remove any temporary files created during exploration.

**Gate**: Report has all sections filled. All paths are absolute. All claims cite evidence. "Where to Add New Code" section populated with real file references. Secret scan passed (no unredacted secrets in output). Report is actionable for onboarding. Quality check passes. Total files examined count is accurate.

---

## Parallel Domain-Specific Mapping (Deep Dive Mode)

When the user requests a full architectural analysis (e.g., "give me the full picture", "I'm new to this codebase", "we're considering a major refactor"), use parallel domain-specific agents instead of single-threaded sequential exploration.

Use parallel mapping when the exploration goal is broad and open-ended — full onboarding, major refactor preparation, or comprehensive architectural review. Use the standard 4-phase flow for targeted questions about a single subsystem.

Launch 4 parallel agents using Task, each focused on a specific domain. Each agent follows the sensitive-files guardrail and writes a structured document.

> See `references/examples-and-errors.md` for the agent domain table, orchestration rules, and the agent instructions template.

**Post-Parallel Gate**: At least 3 of 4 domain agents completed. All output files exist. Secret scan passed across all output files. Each file contains file-backed evidence (not generic descriptions).

---

## References

### Reference Files

- `${CLAUDE_SKILL_DIR}/references/report-template.md`: Standard markdown report template with all sections
- `${CLAUDE_SKILL_DIR}/references/exploration-strategies.md`: Language-specific discovery commands and patterns
- `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md`: Worked examples, error handling, parallel agent template and domain table
