---
name: ln-150-presentation-creator
description: Builds interactive HTML presentation with 6 tabs (Overview, Requirements, Architecture/C4, Tech Spec, Roadmap, Guides). Creates presentation/README.md hub. L2 Worker under ln-100-documents-pipeline.
---

# HTML Presentation Builder

This skill creates an interactive, self-contained HTML presentation from existing project documentation. It transforms Markdown documents into a professional, navigable web presentation with diagrams, collapsible sections, and modern UI.

## When to Use This Skill

**This skill is a L2 WORKER** invoked by **ln-100-documents-pipeline** orchestrator OR used standalone.

Use this skill when:
- Building HTML presentation from existing documentation
- Rebuilding presentation after documentation updates
- Creating standalone presentation for sharing (no full documentation setup needed)
- Validating that source documentation is ready for presentation generation

**Part of workflow**: ln-100-documents-pipeline → ln-110-project-docs-coordinator → ln-120-reference-docs-creator → ln-130-tasks-docs-creator → ln-140-test-docs-creator (optional) → **ln-150-presentation-creator**

**Prerequisites**: Existing documentation in `docs/` directory with **required files**:
- `docs/project/requirements.md` (REQUIRED)
- `docs/project/architecture.md` (REQUIRED)
- `docs/project/tech_stack.md` (REQUIRED)

**Optional files** (enhance presentation but not blocking):
- `docs/project/api_spec.md`, `database_schema.md`, `design_guidelines.md`, `runbook.md`
- `docs/reference/adrs/*.md` (ADRs with Category: Strategic|Technical)
- `docs/reference/guides/*.md` (How-to guides)
- `docs/tasks/kanban_board.md` (Epic Story Counters for Roadmap)

## How It Works

The skill follows a **7-phase workflow**: READ DOCS → VALIDATE SOURCE EXISTS → VALIDATE SOURCE QUALITY → CREATE DIR → COPY TEMPLATES → INJECT CONTENT → BUILD HTML.

**Phase 1: READ DOCS** - Load all project documentation from docs/
**Phase 2: VALIDATE SOURCE EXISTS** - Check required files exist (requirements.md, architecture.md, tech_stack.md), warn if optional missing
**Phase 3: VALIDATE SOURCE QUALITY** - Check diagrams, placeholders, content length (read-only validation)
**Phase 4: CREATE DIR** - Create presentation/ directory + README.md navigation hub
**Phase 5: COPY TEMPLATES** - Copy HTML/CSS/JS templates to assets/
**Phase 6: INJECT CONTENT** - Parse MD docs → replace placeholders in tab files → delete example blocks
**Phase 7: BUILD HTML** - Assemble modular components into standalone presentation_final.html

---

## Phase 1: Read Documentation

**Objective**: Load all project documentation for transformation.

**When to execute**: Always (first phase)

**Process**:

1. **Use docs/ as source**:
   - Read documentation from `docs/project/`, `docs/reference/`, `docs/tasks/` directories
   - Standard locations created by ln-114, ln-112, ln-113

2. **Read Core MD Documents**:
   - `project/requirements.md` - Functional Requirements
   - `project/architecture.md` - Architecture design, C4 diagrams
   - `project/tech_stack.md` - Technology versions, Docker configuration
   - `project/api_spec.md` - API endpoints, authentication (if exists)
   - `project/database_schema.md` - Database schema, ER diagrams (if exists)
   - `project/design_guidelines.md` - UI/UX design system (if exists)
   - `project/runbook.md` - Operational procedures (if exists)

3. **Read ADRs** (if exist):
   - `reference/adrs/adr-001-*.md` through `adr-NNN-*.md`
   - Parse ADR metadata (status, date, title, Category: Strategic|Technical)

4. **Read Guides** (if exist):
   - `reference/guides/*.md` - How-to guides for Guides tab

5. **Read Kanban Board** (if exists):
   - `tasks/kanban_board.md` - Epic Story Counters table for Roadmap progress

6. **Extract metadata**:
   - Project name, date, version from documents
   - Preserve Mermaid diagram blocks

**Output**: Loaded documentation data ready for validation and HTML generation

---

## Phase 2: Validate Source Documentation Exists

**Objective**: Verify that required source documentation exists before building presentation. Prevent building incomplete presentations.

**When to execute**: After Phase 1 (documentation loaded)

**Process**:

### 2.1 Check required files

**REQUIRED** (must exist - block execution if missing):
- ✅ `docs/project/requirements.md`
- ✅ `docs/project/architecture.md`
- ✅ `docs/project/tech_stack.md`

For each required file:
1. Use Glob tool: `pattern: "docs/project/{filename}"`
2. If NOT found:
   - Add to missing list
3. If found:
   - Check file size > 100 bytes (not empty)

**If ANY required file missing or empty:**
```
❌ ERROR: Cannot build presentation - missing required documentation:
  - docs/project/requirements.md [missing/empty]
  - docs/project/architecture.md [missing/empty]

Suggestion: Run ln-111-project-docs-creator to create missing files.

STOP execution.
```

### 2.2 Check optional files

**OPTIONAL** (enhance presentation - warn if missing but continue):
- ⚠️ `docs/project/api_spec.md` (for backend projects)
- ⚠️ `docs/project/database_schema.md` (for projects with database)
- ⚠️ `docs/project/design_guidelines.md` (for frontend projects)
- ⚠️ `docs/project/runbook.md` (for operational projects)

For each optional file:
1. Use Glob tool: `pattern: "docs/project/{filename}"`
2. If NOT found:
   - Add to optional missing list

**If optional files missing:**
```
⚠ WARN: Optional files missing: [list]
Presentation will have reduced content in some tabs.
Continue execution.
```

### 2.3 Check optional directories

**OPTIONAL directories:**
- `docs/reference/adrs/` - check if any ADR files exist (`adrs/*.md`)
- `docs/reference/guides/` - check if any guide files exist (`guides/*.md`)
- `docs/tasks/kanban_board.md` - check for Roadmap data

For each directory:
1. Use Glob tool to find files
2. If empty/missing:
   - Log: `ℹ Optional directory empty: {directory} - related tab will show placeholder`

### 2.4 Report validation summary

Log summary:
```
✓ Source documentation validation completed:
  Required files:
    - ✅ requirements.md (found, 8.5 KB)
    - ✅ architecture.md (found, 15.2 KB)
    - ✅ tech_stack.md (found, 3.1 KB)
  Optional files:
    - ⚠️ api_spec.md (missing - Technical Spec tab will have reduced content)
    - ✅ database_schema.md (found, 4.7 KB)
    - ⚠️ design_guidelines.md (missing)
  Optional directories:
    - ✅ adrs/ (5 ADR files found)
    - ⚠️ guides/ (empty - Guides tab will show placeholder)
    - ✅ kanban_board.md (found - Roadmap will show progress)
```

**Output**: Validation passed (all required files exist) OR error (stop execution)

---

## Phase 3: Validate Source Content Quality

**Objective**: Verify source docs contain sufficient content. Warn about incomplete content but don't block execution.

**When to execute**: After Phase 2 (source files exist)

**Checks performed** (warnings only, non-blocking):
1. **Mermaid diagrams**: architecture.md must have ≥1 diagram, database_schema.md must have ER diagram
2. **Placeholders**: Detect `{{PLACEHOLDER}}`, `[Add your ...]`, `TODO:` patterns
3. **Content length**: requirements.md >500 words, architecture.md >1000 words, tech_stack.md >200 words

**Auto-fix**: None - ln-115 is read-only. Run ln-111-project-docs-creator to fix issues.

**Output**: Content quality report with warnings

📖 **Detailed workflow**: See [references/phases_detailed.md](references/phases_detailed.md#phase-3-validate-source-content-quality)

---

## Phase 4: Create Presentation Directory & README

**Objective**: Setup presentation directory structure and navigation hub.

**When to execute**: After Phase 3 (source validation complete, warnings logged)

**Process**:

1. **Create presentation directory**:
   ```bash
   mkdir -p docs/presentation/
   ```

2. **Check if presentation/README.md exists**:
   - Use Glob tool: `pattern: "docs/presentation/README.md"`
   - If file exists:
     - Skip creation
     - Log: `✓ docs/presentation/README.md already exists (preserved)`
     - Proceed to Phase 5
   - If NOT exists:
     - Continue to step 3

3. **Create presentation/README.md from template**:
   - Copy template: `references/presentation_readme_template.md` → `docs/presentation/README.md`
   - Replace placeholders:
     - `{{PROJECT_NAME}}` — from requirements.md
     - `{{LAST_UPDATED}}` — current date (YYYY-MM-DD)
   - Content structure:
     - **Purpose**: What is this presentation
     - **Quick Navigation**: Links to presentation_final.html and assets/
     - **Customization Guide**: How to edit source files in assets/
     - **Build Instructions**: How to rebuild after changes
     - **Maintenance**: When to rebuild, verification checklist

4. **Notify user**:
   - If created: `✓ Created docs/presentation/README.md (navigation hub)`
   - If skipped: `✓ docs/presentation/README.md already exists (preserved)`

**Output**: docs/presentation/README.md (created or existing)

---

## Phase 5: Copy Templates to Project

**Objective**: Copy HTML/CSS/JS templates from skill references/ to presentation directory.

**When to execute**: After Phase 4 (presentation directory exists)

**Process**:

1. **Check if assets exist**:
   - Use Glob tool: `pattern: "docs/presentation/assets/"`
   - If `docs/presentation/assets/` exists:
     - Skip copying (user may have customized files)
     - Log: `✓ Presentation assets already exist - preserving user customizations`
     - Proceed to Phase 6
   - If NOT exists:
     - Continue to step 2

2. **Copy template files**:
   ```bash
   cp references/presentation_template.html → docs/presentation/assets/
   cp references/styles.css → docs/presentation/assets/
   cp references/scripts.js → docs/presentation/assets/
   cp references/build-presentation.js → docs/presentation/assets/
   cp -r references/tabs/ → docs/presentation/assets/tabs/
   ```

3. **Verify copied structure**:
   ```
   docs/presentation/assets/
   ├── presentation_template.html   # Base HTML5 + 6 tab navigation
   ├── styles.css                    # ~400-500 lines
   ├── scripts.js                    # Tab switching + Mermaid init
   ├── build-presentation.js         # Node.js build script
   └── tabs/
       ├── tab_overview.html         # Landing page
       ├── tab_requirements.html     # FRs + ADRs
       ├── tab_architecture.html     # C4 diagrams
       ├── tab_technical_spec.html   # API + Data + Deployment
       ├── tab_roadmap.html          # Epic list
       └── tab_guides.html           # How-to guides
   ```

**Output**: Template files copied to docs/presentation/assets/ (or skipped if already exist)

**Note**: Templates contain placeholders (`{{VARIABLE_NAME}}`) that will be replaced in Phase 6.

---

## Phase 6: Content Injection & Example Cleanup

**Objective**: Parse MD docs, inject into HTML templates, remove example blocks.

**When to execute**: After Phase 5 (templates exist in assets/)

**Process**:
1. **Parse MD docs** (10 sources): requirements, architecture, tech_stack, api_spec, database_schema, design_guidelines, runbook, adrs/*.md, kanban_board, guides/*.md
2. **Inject content**: Replace `{{PLACEHOLDER}}` in 6 tab files with parsed content
3. **Delete examples**: Remove `<!-- EXAMPLE START -->...<!-- EXAMPLE END -->` blocks from all tabs

**Tab placeholders**: Overview (5), Requirements (4 + NFR ban), Architecture (5), Technical Spec (4), Roadmap (3), Guides (6)

**Validation**: No example markers, no hardcoded e-commerce data, only project-specific content

**Output**: Clean, project-specific tab files ready for build

📖 **Placeholder reference & example transformation**: See [references/phases_detailed.md](references/phases_detailed.md#phase-6-content-injection--example-cleanup)

---

## Phase 7: Build Final Presentation

**Objective**: Assemble modular components into standalone HTML file.

**When to execute**: After Phase 6 (content injected, examples deleted)

**Process**:

1. **Check if presentation_final.html exists (Auto-rebuild for automation)**:
   - Use Glob tool: `pattern: "docs/presentation/presentation_final.html"`
   - If file exists:
     - **✓ Auto-rebuild** (generated file, safe operation)
     - Log: `ℹ Rebuilding presentation_final.html (generated file, safe to rebuild)`
     - Continue to step 2
   - If NOT exists:
     - Log: `Creating presentation_final.html`
     - Continue to step 2

   **Why auto-rebuild:**
   - presentation_final.html is a **generated file** (source of truth: assets/ directory)
   - Rebuilding is safe - no data loss (source files preserved in assets/)
   - Maintains fully automatic workflow when invoked by ln-110-documents-pipeline
   - User customizations in assets/ are preserved (only final HTML is regenerated)

2. **Navigate to presentation assets directory**:
   ```bash
   cd docs/presentation/assets/
   ```

3. **Run build script**:
   ```bash
   node build-presentation.js
   ```

4. **Build Script Process**:
   - **Step 1**: Read presentation_template.html
   - **Step 2**: Read and inline styles.css → `<style>` tag
   - **Step 3**: Read and inline scripts.js → `<script>` tag
   - **Step 4**: Read all 6 tab files → inject into empty `<div>` containers
   - **Step 5**: Replace {{PLACEHOLDERS}} with actual values
   - **Step 6**: Write `../presentation_final.html`

5. **Validate Output** (only if file was built):
   - Check file size (~120-150 KB expected)
   - Verify Mermaid diagrams syntax is valid
   - Log: `✓ Build completed successfully`

6. **Notify user**:
   - If rebuilt (file existed): `✓ Rebuilt docs/presentation/presentation_final.html (~120-150 KB)`
   - If created (file NOT existed): `✓ Created docs/presentation/presentation_final.html (~120-150 KB)`
   - Remind: `Test in browser: Double-click to open, or use http-server`

**Output**: docs/presentation/presentation_final.html (self-contained, ~120-150 KB, no external dependencies except Mermaid.js CDN)

**⚠️ Important Note:**

`presentation_final.html` is a **generated file** built from modular source files in `assets/`.

- ❌ **DO NOT edit `presentation_final.html` directly** — changes will be lost on next rebuild
- ✅ **DO edit source files** in `assets/` directory (template, tabs, styles, scripts)
- 🔄 **Rebuild after changes**: `cd assets/ && node build-presentation.js`

---

## Complete Output Structure

```
docs/
├── project/                      # Source documentation (input)
│   ├── requirements.md
│   ├── architecture.md
│   ├── tech_stack.md
│   ├── api_spec.md (conditional)
│   ├── database_schema.md (conditional)
│   ├── design_guidelines.md (conditional)
│   └── runbook.md (conditional)
├── reference/                    # Source documentation (input)
│   ├── adrs/
│   │   └── *.md (Category: Strategic | Technical)
│   └── guides/
│       └── *.md (optional)
├── tasks/                        # Source documentation (input)
│   └── kanban_board.md (Epic Story Counters)
└── presentation/                 # Output directory
    ├── README.md                 # Navigation hub
    ├── presentation_final.html   # Final standalone HTML (~120-150 KB)
    └── assets/                   # Modular HTML structure
        ├── presentation_template.html  # Base HTML5 + 6 tabs
        ├── styles.css                  # ~400-500 lines
        ├── scripts.js                  # Tab switching + Mermaid
        ├── build-presentation.js       # Node.js build script
        └── tabs/
            ├── tab_overview.html       # Landing page
            ├── tab_requirements.html   # FRs + ADRs
            ├── tab_architecture.html   # C4 diagrams
            ├── tab_technical_spec.html # API + Data + Deployment
            ├── tab_roadmap.html        # Epic list
            └── tab_guides.html         # How-to guides
```

**Note**: Presentation READS from docs/project/, docs/reference/, docs/tasks/ but OUTPUTS to docs/presentation/.

---

## HTML Features

- **Single Source of Truth**: No information duplication - each piece lives in exactly ONE tab
- **Landing Page (Overview)**: Problem/Solution/Business Value, Stakeholders, Documentation Guide, Quick Facts, Tech Stack badges
- **Interactive Navigation**: 6 tabs with SCOPE tags, state persistence (localStorage), smooth transitions
- **Table-Based Layout**: FRs table only (Non-Functional Requirements are forbidden), Architecture highlights table
- **Roadmap Simplified**: Vertical Epic list with In/Out Scope sections, status badges, Dependencies/Success Criteria
- **ADR Organization**: Grouped by category (Strategic/Technical) with accordion, full content inline
- **Diagram Visualization**: Mermaid.js with tab-switch rerender (C4, ER, Sequence, Deployment)
- **Responsive Design**: Mobile-first (320px/768px/1024px+ breakpoints)
- **Collapsible Sections**: Auto-collapse with scroll preservation
- **Modern UI**: Clean professional design, WCAG 2.1 Level AA compliant
- **English Language**: All presentation content in English

---

## Best Practices

**Idempotent operation**: Preserves README.md, preserves assets/ (user customizations), auto-rebuilds presentation_final.html.

**Key rules by phase**:
- **Phase 2**: STOP if required files missing; **Phase 3**: WARN only (non-blocking)
- **Phase 5**: Don't overwrite existing assets (user customizations)
- **Phase 6**: Delete ALL example blocks, escape XSS, valid Mermaid syntax
- **Phase 7**: Warn if output >200 KB

---

## Customization Options

Edit `assets/styles.css` (CSS variables for theming), `assets/presentation_template.html` (layout/tabs), or `assets/tabs/*.html` (tab content).

**⚠️ After any customization:** Always rebuild the presentation:
```bash
cd assets/
node build-presentation.js
```

**Important:** Never edit `presentation_final.html` directly — it's a generated file that gets overwritten on each build.

---

## Prerequisites

**Orchestrator**: ln-110-documents-pipeline | **Standalone**: Yes (rebuild/validate existing docs)

**Required files**: requirements.md, architecture.md, tech_stack.md (in docs/project/)
**Optional files**: api_spec, database_schema, design_guidelines, runbook, adrs/*.md, guides/*.md, kanban_board.md

**Dependencies**: Node.js v18+, Modern browser, Internet (Mermaid CDN)

---

## Definition of Done

| Phase | Critical Checkpoints |
|-------|---------------------|
| **1. READ DOCS** | ✅ All docs loaded from docs/project/, docs/reference/, docs/tasks/ ✅ Metadata extracted ✅ Mermaid blocks preserved |
| **2. VALIDATE EXISTS** | ✅ Required files exist (requirements.md, architecture.md, tech_stack.md) ✅ ERROR if missing |
| **3. VALIDATE QUALITY** | ✅ Diagrams checked ✅ Placeholders detected ✅ Content length checked ✅ WARN only (non-blocking) |
| **4. CREATE DIR** | ✅ docs/presentation/ created ✅ README.md created/preserved |
| **5. COPY TEMPLATES** | ✅ assets/ created with all templates OR preserved if exists |
| **6. INJECT CONTENT** | ✅ All 6 tabs populated ✅ **CRITICAL: Example blocks deleted** ✅ No `<!-- EXAMPLE -->` markers ✅ No hardcoded e-commerce data |
| **7. BUILD HTML** | ✅ `node build-presentation.js` executed ✅ presentation_final.html created (~120-150 KB) ✅ Tested in browser |

**Output:** docs/presentation/presentation_final.html + assets/ + README.md

---

## Troubleshooting

- **ERROR: Missing required files**: Run ln-111-project-docs-creator to create requirements.md, architecture.md, tech_stack.md
- **WARN: Missing diagrams**: Add Mermaid diagrams to architecture.md (C4 Context/Container/Component) and database_schema.md (ER diagram)
- **WARN: Placeholders found**: Complete documentation in source MD files before building
- **WARN: Sparse content**: Expand documentation (requirements.md >500 words, architecture.md >1000 words, tech_stack.md >200 words)
- **Build script fails**: Check Node.js v18+, navigate to assets/, verify all files exist
- **Mermaid diagrams not rendering**: Check syntax with Mermaid Live Editor, verify CDN loaded
- **Tabs not switching**: Check JavaScript loaded, open browser console for errors
- **File too large (>200 KB)**: Reduce diagrams, minify CSS/JS, remove unused rules

---

**Version:** 8.0.0
**Last Updated:** 2025-12-12
