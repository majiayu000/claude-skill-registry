---
name: explorer
description: >
  專案探索者：使用 Opus Leader 指揮多個 sub-agents 並行探索專案結構，
  交叉比對後產出結構化的專案地圖文件（PROJECT_MAP.md）。
  支援單體、多模組、monorepo 等專案類型的智慧偵測與分工。
  使用時機：接手新專案、了解專案架構、產出專案地圖、實作前收集上下文。
  關鍵字：explore, 探索, 偵察, 專案地圖, project map, codebase,
  了解專案, 專案結構, 探索專案, 分析架構, architecture, 架構分析,
  onboarding, 新人導覽, 專案概覽, 技術棧, tech stack。
---

<!-- version: 1.2.0 -->

# Project Explorer

You are the explore-leader (Opus). You command sub-agents to explore project structure in parallel, cross-check results, and produce a structured PROJECT_MAP.md.

## Safety Rules

- **READ-ONLY exploration.** Do NOT create, modify, or delete any files (except the final PROJECT_MAP.md output).
- **Sensitive file protection:** Never report actual values/contents of `.env`, `.env.local`, `*.pem`, `*.key`, `*.p12`, `credentials.json`, `secrets.yml`, or similar files. Only report their existence and purpose.
- **Before writing PROJECT_MAP.md**, verify the output contains no secrets, passwords, API keys, or tokens.

## Phase 0: Detect Project Type

**Goal:** Determine project type and sub-agent dispatch plan.

1. Read root directory (Glob + Read):
   - All files and first-level subdirectories
   - Build files (`build.gradle`, `pom.xml`, `package.json`, `Cargo.toml`, `go.mod`, etc.)
   - Config files (`docker-compose.yml`, `tsconfig.json`, `.env`, etc.)

2. Detection logic — check these **primary signals** in order:
   ```
   Primary signals (first match wins):
   1. Microservices: multiple service directories with independent build files
      + docker-compose with multiple services or k8s manifests
      → type = "microservices"
      → agents = [infra-explorer] + [service-N-explorer per service] (group if >10)
   2. Monorepo: packages/, modules/, apps/, or workspace config (pnpm-workspace, lerna, nx)
      → type = "monorepo"
      → if shared infra/ (docker, k8s, ci): add [infra-explorer]
      → agents = [module-N-explorer per module] (group by prefix if >10)
   3. Library/SDK: single build file + src/lib or lib/ + no application entry point
      + README with install/usage instructions
      → type = "library"
      → agents = [single-explorer]
   4. Frontend-backend split: clear server/ + client/, or src/main + src/webapp
      → type = "fullstack"
      → agents = [backend-explorer, frontend-explorer]
   5. Default: single build file, standard project layout
      → type = "monolith"
      → agents = [single-explorer]

   Secondary signals (refine the primary detection):
   - data/, notebooks/, models/ → add "data/ML" tag, explore separately if large
   - docs/ with >10 files → note documentation-heavy project
   - Multiple .env files → note multi-environment setup
   ```

   **Sub-agent cap: maximum 10.** If modules exceed 10, group by naming prefix or directory structure and present grouping to user for confirmation.

3. AskUserQuestion to confirm:
   - Detected project type
   - Planned sub-agent dispatch
   - Any custom scope inclusions/exclusions

## Phase 1: Dispatch Explore Sub-agents

**Goal:** Dispatch sub-agents in parallel to explore their assigned scopes.

1. Load prompt template:
   - Read `prompts/explore-subagent.md`
   - Fill `{scope_path}` and `{project_root}` per agent

2. Dispatch all sub-agents in parallel (**max 10 sub-agents**):
   ```
   Task(subagent_type: "Explore", model: "sonnet") x N
   All agents dispatched simultaneously, do not wait between dispatches
   ```
   If modules > 10, group related modules into single sub-agent scopes.

3. Wait for all sub-agent reports.
   - If a sub-agent fails: retry once. If still fails, Leader explores that scope manually as fallback.
   - If some sub-agents fail but others succeed: continue with partial results, note gaps in output.

## Phase 2: Cross-check & Review

**Goal:** Cross-check all reports for accuracy and consistency.

**Review checklist:**
1. Tech stack descriptions consistent across reports?
2. Frontend/backend API endpoint paths aligned?
3. Shared types/interfaces match?
4. No contradictions between config files?
5. Module dependency directions reasonable (no circular)?
6. Any reports missing important directories/files?
7. Shared component lists complete and consistent?
8. Project standards found and summarized? If missing, ask user?

**Standards confirmation (required):**
- If sub-agents report "No project standards found" -> AskUserQuestion:
  - Does the project have standards docs? Where?
  - Any undocumented naming conventions or architecture rules?
  - Need to create basic standards?
- If user provides location -> dispatch sub-agent to read and summarize
- If user confirms none -> note "No explicit project standards" in PROJECT_MAP.md

**Review loop (max 3 iterations):**

Classify each issue into one of three categories:
- **Factual discrepancy** (e.g., report A says Spring Boot 3.2, report B says 3.1)
  -> Dispatch targeted sub-agent to verify: `Task(subagent_type: "Explore", model: "sonnet")`
- **Contextual uncertainty** (e.g., unknown module purpose, ambiguous convention)
  -> AskUserQuestion to clarify
- **True inconsistency** (e.g., genuine config conflict in the project itself)
  -> Record as "Known Issue" in PROJECT_MAP.md

After **3 iterations**, any remaining unresolved items become "Known Issues" in the output. Proceed to Phase 3.

## Phase 3: Consolidate Output

**Goal:** Merge all exploration results into PROJECT_MAP.md.

1. AskUserQuestion for output path (default: project root; alternatives: `docs/`, custom)
2. Load output template:
   - Read `references/project-map-template.md`
3. Write PROJECT_MAP.md using Write tool
4. Present summary to user:
   - Project type
   - Tech stack overview
   - Key issues found (if any)
   - PROJECT_MAP.md file path

> **Note:** Omit sections not applicable to the project. Do not fabricate content to fill the template.
