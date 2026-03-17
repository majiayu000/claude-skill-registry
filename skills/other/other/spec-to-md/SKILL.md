---
name: spec-to-md
description: >
  讀取規格文件轉換為 AI coding 實作文件（.md），產出技術規格、後端實作指示、前端實作指示等結構化文件。
  使用時機：當使用者提供規格文件並要求產生實作文件、轉換規格為 coding 文件時觸發。
  關鍵字：規格轉換、spec to md、產生實作文件、讀取規格、分析需求、coding 文件、開發文件、
  to md、toMD、toMd、TOMD、specification, 規格文件, 需求文件, 需求轉換, 實作指示, 實作文件, 技術規格, 文件生成, 文件產生, 前端實作, 後端實作, convert, 轉換。
---

<!-- version: 1.2.0 -->

# Spec-to-MD

You are the spec-to-md lead. You transform specification documents into structured AI coding implementation files.

## Step 1: Confirm Inputs

Use AskUserQuestion to gather:

1. **Functional spec files**: How many? Paths? (requirements, screen specs, SQL, etc.)
2. **Project standard files**: Paths? (DEVELOP.md, NAMING_CONVENTIONS.md, API_SPECIFICATION.md, etc.)
3. **Shared component files**: Paths? (component docs directory, shared component source paths)
4. **Output directory**: Where to write files? (default: `Docs/<feature-id>/`)

Wait for complete answers before proceeding.

## Step 2: Read & Analyze (Parallel Subagents)

Launch 3 parallel Task agents in a single message (each with `model: "opus"`, no `run_in_background`). Wait for all results.

**Agent A — Functional Specs**:
- Read all functional spec files.
- Output: feature name, ID, frontend/backend requirements, business rules, screen structure, field descriptions, operation flow.

**Agent B — Project Standards**:
- Read all project standard files.
- Output: naming conventions, architecture patterns, API format, response format, Entity patterns, error code standards.

**Agent C — Existing Code Style**:
- Read shared component files. Search similar existing code (Glob/Grep).
- Output: actual code style, reusable component list, Processor/Store/Vue component patterns.

Only read user-specified files. Do not scan entire directories. If additional files needed, AskUserQuestion.

> If any subagent fails, AskUserQuestion to verify file paths before retrying. If retry also fails, perform that agent's work in the main flow.

## Step 3: Confirm Understanding

> **Optional integration** — if superpowers plugin is installed, use `superpowers:brainstorming` to explore requirements. Otherwise, independently brainstorm edge cases and design alternatives.

Present summary to user:

- Feature name and ID
- Frontend summary (pages, main operations, key components)
- Backend summary (APIs, main business logic, key validation rules)
- Involved tables and Entities
- Expected Processor count and Vue component count
- Questions or uncertainties (list explicitly)

**Wait for user confirmation before writing documents.**

## Step 4: Produce Documents

Read `references/template-structure.md` for document format guidance.

### 4a: prompt.md (Main Flow)

> **Optional integration** — if superpowers plugin is installed, use `superpowers:writing-plans` methodology.

AI navigation guide for md-to-code skill:
- Feature overview (purpose, trigger conditions, prerequisites)
- Implementation scope summary (Processor count, component count)
- Reference list pointing to detailed documents
- Suggested implementation order
- Project standard file reference paths

prompt.md contains NO technical details — navigation and orchestration only.
Present to user, wait for confirmation.

### 4b: 01_技術規格.md (Main Flow)

Full technical details — API, database, Entity:
- API endpoint table (endpoint, method, permission, description)
- Per-API request params, response format, error codes
- Table structure and relationships (ER diagram)
- Entity field mapping
- Business rule definitions
- Related SQL reference

Present key design decisions to user, wait for confirmation.

### 4c: 02_後端實作.md + 03_前端實作.md (Agent Teams)

After 01 confirmation, create team and spawn teammates:

1. `TeamCreate`: team_name = `"spec-<feature-name>"` (lowercase, no spaces, use hyphens), description = "Parallel backend + frontend spec production"

2. Load spawn prompts on demand:
   - Glob `**/spec-to-md/**/prompts/backend-spec.md` then Read. Fill variables, spawn backend-spec teammate.
   - Glob `**/spec-to-md/**/prompts/frontend-spec.md` then Read. Fill variables, spawn frontend-spec teammate.

3. **Prepare shared context file** before spawning:
   - Write `{output_dir}/context/spec-context.md` containing:
     - Agent A output (func spec summary) from Step 2
     - Agent B output (project standards summary) from Step 2
     - Full path to 01_技術規格.md (do NOT embed the full content)
   - This avoids context window overload in teammate prompts.

4. Variables to fill in prompts:
   - `{team_name}`: the created team name
   - `{context_file_path}`: path to `{output_dir}/context/spec-context.md`
   - `{tech_spec_path}`: path to 01_技術規格.md

5. Cross-check: Both teammates report completion to TL. TL extracts API endpoint list from backend-spec output and sends to frontend-spec for verification. frontend-spec verifies Types and Store Actions alignment. Inconsistencies resolved via TL-coordinated SendMessage.

6. After both complete, summarize:
   - Backend Processor responsibility breakdown
   - Frontend component split logic
   - Cross-layer consistency check results

Present both documents to user for confirmation.

## Step 5: Close Team + Final Verification

> **Optional integration** — if superpowers plugin is installed, use `superpowers:verification-before-completion` principles. Otherwise, apply thorough self-review before closing.

1. **Shutdown team**: shutdown_request to all teammates → confirm → TeamDelete. If a teammate rejects shutdown, SendMessage asking them to wrap up current work first, then retry shutdown_request.

2. **Completeness**: compare against Step 3 summary — all requirements covered?

3. **Consistency checklist** — verify 02/03 documents match 01:
   - [ ] Every API endpoint in 01 has a corresponding handler/controller in 02
   - [ ] Request parameter names and types match between 01 and 02
   - [ ] Response format in 01 matches what frontend consumes in 03
   - [ ] Entity/model field names are identical across 01, 02, and 03
   - [ ] Error codes defined in 01 are handled in both 02 and 03
   - [ ] Permission/auth requirements in 01 are enforced in 02
   - [ ] Component names in 03 match the references in prompt.md
   - List cross-layer check records (teammate communication and fixes).

4. **Self-sufficiency**: confirm 02/03 each contain enough context to work independently without frequent cross-referencing.

Present final checklist:
- One-line summary per document
- Verification results (gaps or inconsistencies)
- Cross-layer consistency results
- Remind user: use md-to-code skill to begin implementation

## Principles

- Code snippets MUST match existing project style (learned from Step 2).
- 02/03 documents must be self-contained — no frequent cross-referencing to 01 needed.
- Keep each document at reasonable length — avoid exceeding Claude Code effective processing range.
- Reference shared context file instead of embedding large documents in spawn prompts. For files over ~200 lines, provide path and let teammate Read on demand.
- Step 2 uses subagents (efficient, low-cost, no inter-agent communication needed).
- Step 4c uses Agent Teams (cross-layer consistency check, human intervention support).
- Teammate prompts include context file path + doc paths. Teammates Read files themselves at startup.
