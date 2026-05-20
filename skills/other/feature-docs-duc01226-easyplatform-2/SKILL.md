---
name: feature-docs
version: 2.0.0
description: '[Documentation] Create or update business feature documentation in docs/business-features/{Module}/. Generates comprehensive 26-section docs with verified code evidence and AI companion files. Triggers on: feature docs, business feature documentation, module documentation, document feature, update feature docs, ai companion, ai context file, quick feature docs, feature readme, single file docs, verified documentation.'
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Generate comprehensive 26-section business feature documentation with mandatory code evidence for all test cases, plus AI companion file.

**Workflow:**

1. **Detect & Gather** — Auto-detect modules from git changes OR user-specified module, read existing docs
2. **Investigate Code** — Grep/glob codebase to gather evidence (`file:line` format) for every test case
3. **Write Documentation** — Follow exact 26-section structure, place in `docs/business-features/{Module}/`
4. **Generate AI Companion** — Create `.ai.md` file (max 300 lines) with domain model, file locations, key expressions
5. **Verification** — 3-pass system: evidence audit, domain model verification, cross-reference audit

**Key Rules:**

- EVERY test case MUST have verifiable code evidence (`FilePath:LineNumber`), no exceptions
- Output must have exactly 26 sections matching the master template
- Always update CHANGELOG.md and Version History (Section 26) when modifying docs
- When writing Section 17 test cases: include an `IntegrationTest` field pointing to the test file and method name. Format: `IntegrationTest: Goals/GoalCommandIntegrationTests.cs::{MethodName}`. If no integration test exists yet, set `Status: Untested`.
- Verify every TC-{MOD}-XXX in Section 17 has a corresponding `[Trait("TestSpec", "TC-{MOD}-XXX")]` in the integration test codebase. If missing, flag as `Status: Untested`.
- If third verification pass finds >5 issues, HALT and re-run verification

## Project Pattern Discovery

Before implementation, search your codebase for project-specific patterns:

- Search for: `business-features`, `detailed-features`, `feature-docs-template`
- Look for: existing feature doc folders, 26-section templates, AI companion files

> **MANDATORY IMPORTANT MUST** Read the `feature-docs-reference.md` companion doc for project-specific patterns and code examples.
> If file not found, continue with search-based discovery above.

# Feature Documentation Generation & Verification

Generate comprehensive feature documentation following project conventions and folder structure.

**GOLD STANDARD References**:

Search your codebase for existing feature docs to use as reference:

```bash
find docs/business-features -name "README.*.md" -type f | head -5
```

**Template File**: `docs/templates/detailed-feature-docs-template.md`
**AI Companion Template**: `docs/templates/feature-docs-ai-template.md`

---

## [CRITICAL] MANDATORY CODE EVIDENCE RULE

**EVERY test case MUST have verifiable code evidence.** This is non-negotiable.

### Evidence Format

```markdown
**Evidence**: `{RelativeFilePath}:{LineNumber}` or `{RelativeFilePath}:{StartLine}-{EndLine}`
```

### Valid vs Invalid Evidence

| Valid                           | Invalid                             |
| ------------------------------- | ----------------------------------- |
| `ErrorMessage.cs:83`            | `{FilePath}:{LineRange}` (template) |
| `Handler.cs:42-52`              | `SomeFile.cs` (no line)             |
| `interviews.service.ts:115-118` | "Based on CQRS pattern" (vague)     |

---

## Output Structure

All documentation MUST be placed in the correct folder structure:

```
docs/
├── BUSINESS-FEATURES.md              # Master index (UPDATE if new module)
├── templates/
│   └── detailed-feature-docs-template.md  # MASTER TEMPLATE
└── business-features/
    ├── {Module}/                     # One folder per service/module in your project
    │   ├── README.md                 # Complete module documentation
    │   ├── INDEX.md                  # Navigation hub
    │   ├── API-REFERENCE.md          # Endpoint documentation
    │   ├── TROUBLESHOOTING.md        # Issue resolution guide
    │   └── detailed-features/
    │       ├── README.{FeatureName}.md     # Comprehensive (human-facing, 1000+ lines)
    │       └── README.{FeatureName}.ai.md  # AI companion (code-focused, 300-500 lines)
    └── ...
```

### Module Mapping

Search your codebase to discover the module-to-folder mapping:

```bash
# Find all service directories
ls -d src/Services/*/

# Find all existing feature doc modules
ls -d docs/business-features/*/
```

Map each module code to its folder name and service path. Example pattern:

| Module Code | Folder Name | Service Path              |
| ----------- | ----------- | ------------------------- |
| {Module1}   | `{Module1}` | `src/Services/{Module1}/` |
| {Module2}   | `{Module2}` | `src/Services/{Module2}/` |

---

## MANDATORY 26-SECTION STRUCTURE

All feature documentation MUST follow this section order:

| #   | Section                    | Stakeholder Focus      |
| --- | -------------------------- | ---------------------- |
| 1   | Executive Summary          | PO, BA                 |
| 2   | Business Value             | PO, BA                 |
| 3   | Business Requirements      | PO, BA                 |
| 4   | Business Rules             | BA, Dev                |
| 5   | Process Flows              | BA, Dev, Architect     |
| 6   | Design Reference           | BA, UX, Dev            |
| 7   | System Design              | Dev, Architect         |
| 8   | Architecture               | Dev, Architect         |
| 9   | Domain Model               | Dev, Architect         |
| 10  | API Reference              | Dev, Architect         |
| 11  | Frontend Components        | Dev                    |
| 12  | Backend Controllers        | Dev                    |
| 13  | Cross-Service Integration  | Dev, Architect         |
| 14  | Security Architecture      | Dev, Architect         |
| 15  | Performance Considerations | Dev, Architect, DevOps |
| 16  | Implementation Guide       | Dev                    |
| 17  | Test Specifications        | QA                     |
| 18  | Test Data Requirements     | QA                     |
| 19  | Edge Cases Catalog         | QA, Dev                |
| 20  | Regression Impact          | QA                     |
| 21  | Troubleshooting            | Dev, QA, DevOps        |
| 22  | Operational Runbook        | DevOps                 |
| 23  | Roadmap and Dependencies   | PO, BA                 |
| 24  | Related Documentation      | All                    |
| 25  | Glossary                   | PO, BA                 |
| 26  | Version History            | All                    |

### Stakeholder Quick Navigation

| Audience                | Sections                                                           |
| ----------------------- | ------------------------------------------------------------------ |
| **Product Owner**       | Executive Summary, Business Value, Roadmap                         |
| **Business Analyst**    | Business Requirements, Business Rules, Process Flows, Domain Model |
| **Developer**           | Architecture, Domain Model, API Reference, Implementation Guide    |
| **Technical Architect** | System Design, Cross-Service Integration, Security, Performance    |
| **QA/QC**               | Test Specifications, Test Data, Edge Cases, Regression Impact      |
| **DevOps/Support**      | Troubleshooting, Operational Runbook                               |

---

## Phase 1: Module Detection & Context Gathering

### Step 1.0: Auto-Detect Modules from Git Changes (Default)

When no module or feature is explicitly specified, automatically detect affected modules from git changes:

1. Run `git diff --name-only HEAD` (captures both staged and unstaged changes)
2. If no uncommitted changes, run `git diff --name-only HEAD~1` (last commit)
3. Extract unique module names from changed file paths using the Module Mapping table
4. For each detected module, check if a business feature doc exists in `docs/business-features/{Module}/`
5. If docs exist → proceed to **Phase 1.5 (Update Mode)** for each module
6. If no docs exist → skip (do not create docs from scratch without explicit user request)
7. If no service-layer files changed (e.g., only `.claude/`, `docs/`, config files) → report "No business feature docs impacted" and exit

**Path-to-Module Detection Rules:**

Search your codebase to build the path-to-module mapping. Common patterns:

| Changed File Path Pattern                           | Detected Module                   |
| --------------------------------------------------- | --------------------------------- |
| `src/Services/{Module}/**`                          | {Module}                          |
| `{frontend-apps-dir}/{app-name}/**`                 | {Module} (map app name to module) |
| `{frontend-libs-dir}/{domain-lib}/src/{feature}/**` | {Module} (map feature to module)  |

Build a project-specific mapping by examining:

```bash
ls -d src/Services/*/
ls -d {frontend-apps-dir}/*/
```

### Step 1.1: Identify Target Module

Determine which module the feature belongs to by:

1. User explicitly specifies module name
2. Feature name/domain implies module (search codebase to verify mapping)
3. Search codebase for feature-related entities/commands
4. **Auto-detected from git diff** (Step 1.0 above) — used when invoked as a workflow step without explicit module

### Step 1.2: Read Existing Documentation

Before creating new docs, read existing structure:

1. Read `docs/BUSINESS-FEATURES.md` (master index)
2. Read `docs/business-features/{Module}/INDEX.md` (if exists)
3. Read `docs/business-features/{Module}/README.md` (if exists)
4. Identify what already exists vs what needs creation/update

### Step 1.3: Codebase Analysis

Gather evidence from source code:

- **Entities**: `src/Services/{Module}/{Module}.Domain/Entities/`
- **Commands**: `src/Services/{Module}/{Module}.Application/UseCaseCommands/`
- **Queries**: `src/Services/{Module}/{Module}.Application/UseCaseQueries/`
- **Controllers**: `src/Services/{Module}/{Module}.Service/Controllers/`
- **Frontend**: `{frontend-apps-dir}/{app-name}/` or `{frontend-libs-dir}/{domain-lib}/`

### Step 1.4: Feature Analysis

Build knowledge model in `.ai/workspace/analysis/[feature-name].md`.

#### Discovery Areas

1. **Domain Entity Discovery**: Entities, value objects, enums
2. **Workflow Discovery**: Commands, Queries, Event Handlers, Background Jobs
3. **API Discovery**: Controllers, endpoints, DTOs
4. **Frontend Discovery**: Components, Services, Stores
5. **Cross-Service Discovery**: Message Bus messages, producers, consumers

---

## Phase 1.5: Update Mode (when updating existing docs)

When UPDATING an existing business feature document (not creating from scratch):

### Step 1.5.1: Diff Analysis

1. Identify the source of changes (git diff, branch comparison, commit history)
2. Categorize changes by type: backend entity, command, query, frontend component, i18n, etc.
3. Map each change to impacted documentation sections (use table below)

### Step 1.5.2: Section Impact Mapping

| Change Type            | Impacted Sections                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| New entity property    | 3 (Business Requirements), 9 (Domain Model), 10 (API Reference)                          |
| New API endpoint       | 10 (API Reference), 12 (Backend Controllers), 14 (Security)                              |
| New frontend component | 11 (Frontend Components)                                                                 |
| New filter/query       | 3 (Business Requirements), 10 (API Reference)                                            |
| New i18n keys          | 11 (Frontend Components)                                                                 |
| Any new functionality  | **17 (Test Specs), 18 (Test Data), 19 (Edge Cases), 20 (Regression Impact)** — MANDATORY |
| Any change             | 1 (Executive Summary), 26 (Version History) — ALWAYS UPDATE                              |

### Step 1.5.3: Mandatory Test Coverage (Sections 17-20)

**CRITICAL**: When documenting ANY new functionality, you MUST update:

- **Section 17 (Test Specifications)**: Add test cases (TC-{MOD}-XXX) for new features with GIVEN/WHEN/THEN format. Each TC entry should include:

    ```markdown
    #### TC-GM-001: Create SMART Goal Successfully

    **Priority**: P0-Critical
    **Status**: Tested | Untested
    **IntegrationTest**: `Goals/GoalCommandIntegrationTests.cs::SaveGoal_WhenValidData_ShouldCreateSuccessfully`
    **Evidence**: `Growth.Application/Goals/Commands/SaveGoalCommand.cs:42-68`
    ```

- **Section 18 (Test Data)**: Add seed data required for new test cases
- **Section 19 (Edge Cases)**: Add edge cases for boundary conditions, error states, permission checks
- **Section 20 (Regression Impact)**: Add regression risk rows for impacted areas, update test suite counts

**Failure to update test sections is a blocking quality issue.**

### Step 1.5.4: CHANGELOG Entry

Always create/update `CHANGELOG.md` entry under `[Unreleased]` following Keep a Changelog format.

---

## Phase 2: Documentation Generation

Generate at `docs/business-features/{Module}/detailed-features/README.{FeatureName}.md`.

### Key Format Examples

**Business Requirements (FR-XX)**:

```markdown
#### FR-{MOD}-01: {Requirement Title}

| Aspect          | Details                           |
| --------------- | --------------------------------- |
| **Description** | {What this requirement enables}   |
| **Scope**       | {Who can use / affected entities} |
| **Evidence**    | `{FilePath}:{LineRange}`          |
```

**User Stories (US-XX)**:

```markdown
#### US-{MOD}-01: {Story Title}

**As a** {role}
**I want** {goal/desire}
**So that** {benefit/value}

**Acceptance Criteria**:

- [ ] AC-01: {Criterion with evidence reference}
- [ ] AC-02: {Criterion with evidence reference}

**Related Requirements**: FR-{MOD}-01, FR-{MOD}-02
**Evidence**: `{FilePath}:{LineRange}`
```

**Test Summary Table (MANDATORY)**:

```markdown
| Category    | P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low) |  Total  |
| ----------- | :-----------: | :-------: | :---------: | :------: | :-----: |
| {Category1} |      {N}      |    {N}    |     {N}     |   {N}    |   {N}   |
| **Total**   |    **{N}**    |  **{N}**  |   **{N}**   | **{N}**  | **{N}** |
```

**Test Case Format (TC-XX)**:

```markdown
#### TC-{MOD}-001: {Test Name} [P0]

**Acceptance Criteria**:

- {Passing criteria 1}
- {Passing criteria 2}

**GIVEN** {initial context}
**WHEN** {action performed}
**THEN** {expected outcome}

**Edge Cases**:

- {Invalid scenario} → {Expected error/behavior}

**Evidence**: `{FilePath}:{LineRange}`
```

**Troubleshooting Format**:

```markdown
#### {Issue Title}

**Symptoms**: {Observable problem}

**Causes**:

1. {Cause 1}
2. {Cause 2}

**Resolution**:

- {Step 1}
- {Step 2}
```

**Permission Matrix**:

```markdown
| Role  | View | Create | Edit | Delete | Special     |
| ----- | :--: | :----: | :--: | :----: | ----------- |
| Admin |  ✅  |   ✅   |  ✅  |   ✅   | Full access |
```

---

## Phase 2.5: AI Companion Generation

Generate AI-agent optimized companion file alongside the comprehensive documentation.

**Output**: `docs/business-features/{Module}/detailed-features/README.{FeatureName}.ai.md`
**Template**: `docs/templates/detailed-feature-docs-template.ai.md`

### AI Companion Structure (10 Sections, ~260 lines)

| Section         | Content                            | Source from Full Doc      |
| --------------- | ---------------------------------- | ------------------------- |
| Context         | Purpose, entities, service         | Executive Summary         |
| File Locations  | Exact paths to all key files       | Implementation Guide      |
| Domain Model    | Properties, expressions            | Domain Model              |
| API Contracts   | Endpoints, request/response shapes | API Reference             |
| Business Rules  | Validation, state transitions      | Business Rules            |
| Patterns        | Required / Anti-patterns           | Architecture              |
| Integration     | Events, dependencies               | Cross-Service Integration |
| Security        | Authorization matrix               | Security Architecture     |
| Test Scenarios  | Key GIVEN/WHEN/THEN cases          | Test Specifications       |
| Quick Reference | Decision tree, code snippets       | Implementation Guide      |

### Compression Rules

1. **Tables over prose** - Convert paragraphs to table rows
2. **Paths over descriptions** - `File:Line` over "located in..."
3. **Signatures over examples** - `{ id: string } → { entity: Dto }` over full code
4. **Decisions over explanations** - What to do, not why

### AI Companion Extended (6-Section Variant, ~420 lines)

For larger features, use the extended companion format:

1. **Quick Reference** (~40 lines) - Module, service, file locations
2. **Domain Model** (~80 lines) - Entities, enums, value objects (condensed)
3. **API Contracts** (~100 lines) - Signatures with DTOs only
4. **Validation Rules** (~80 lines) - BR-XX table format
5. **Service Boundaries** (~60 lines) - Cross-service integration
6. **Critical Paths** (~60 lines) - Key workflows as decision trees

### AI Companion Header

```markdown
# {FeatureName} Feature - AI Context

> AI-optimized context file for code generation tasks.
> Full documentation: [README.{FeatureName}Feature.md](./README.{FeatureName}Feature.md)
> Last synced: {YYYY-MM-DD}
```

### Skip These Sections in AI Companion

- Troubleshooting (operational)
- Operational Runbook (DevOps)
- Business Value (stakeholder)
- Version History (changelog)
- Glossary (definitions)

### AI Companion Quality Check

- [ ] File size ≤300 lines (standard) or ≤500 lines (extended)
- [ ] All file paths are exact and current
- [ ] API contracts include request/response shapes
- [ ] Business rules have evidence references
- [ ] Patterns section has required/anti-pattern markers
- [ ] Evidence chain preserved from full doc
- [ ] Links back to comprehensive doc
- [ ] 'Last synced' timestamp included

---

## Phase 3: Master Index Update

After creating/updating module docs, update `docs/BUSINESS-FEATURES.md`:

1. Read current content
2. Verify module is listed in the "Detailed Module Documentation" table
3. Add link if missing:
    ```markdown
    | **{Module}** | [Description] | [View Details](./business-features/{Module}/README.md) |
    ```

---

## Anti-Hallucination Protocols

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

### DOCUMENTATION_ACCURACY_CHECKPOINT

Before writing any documentation:

- "Have I read the actual code that implements this?"
- "Are my line number references accurate and current?"
- "Can I provide a code snippet as evidence?"

### TEST CASE EVIDENCE VERIFICATION

**For EVERY test case:**

1. Read the Evidence file at claimed line number
2. Verify: Does code at that line support test assertion?
3. Check Edge Cases: Find error constants in `ErrorMessage.cs`
4. Fix immediately if line numbers wrong

---

## Phase 3.5: Verification (3 Passes)

### First Pass - Test Case Evidence Audit

**For EVERY test case in documentation:**

1. **Read the Evidence file** at the claimed line number
2. **Verify match**: Does the code at that line support the test assertion?
3. **Check Edge Cases**: Find error message constants in `ErrorMessage.cs`
4. **Fix immediately** if line numbers are wrong

### Second Pass - Domain Model Verification

- Read EACH entity file referenced in Domain Model section
- Verify property names, types, and line numbers
- Check enum values exist in actual source
- Remove any documented properties not found in source

### Third Pass - Cross-Reference Audit

- Test Summary counts match actual test case count
- All internal links work
- No template placeholders remain (`{FilePath}`, `{LineRange}`)
- ErrorMessage.cs constants match edge case messages

**CRITICAL**: If ANY pass finds hallucinated content, re-investigate and fix before completing.

---

## Quality Checklist

### Structure

- [ ] Documentation placed in correct folder structure
- [ ] README.md follows template format (26 sections)
- [ ] INDEX.md created with navigation links
- [ ] Master index (BUSINESS-FEATURES.md) updated
- [ ] Stakeholder navigation table present
- [ ] ASCII diagrams for architecture
- [ ] API endpoints documented with examples
- [ ] CHANGELOG.md updated with entry under `[Unreleased]`

### Test Case Evidence (MANDATORY)

- [ ] **EVERY test case has Evidence field** with `file:line` format
- [ ] **No template placeholders** remain (`{FilePath}`, `{LineRange}`)
- [ ] **Line numbers verified** by reading actual source files
- [ ] **Edge case errors match** constants from `ErrorMessage.cs`
- [ ] **Test Summary counts match** actual number of test cases

### Anti-Hallucination

- [ ] All entity properties verified against source code
- [ ] All enum values verified against actual enum definitions
- [ ] No invented methods, properties, or models
- [ ] All code snippets copied from actual files

## Related

- `documentation`
- `feature-implementation`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
