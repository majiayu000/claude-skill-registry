---
name: page-import
description: Import a single webpage from any URL to structured HTML content for authoring in AEM Edge Delivery Services. Scrapes the page, analyzes structure, maps to existing blocks, and generates HTML for immediate local preview. Also triggered by terms like "migrate", "migration", or "migrating".
---

# Page Import Orchestrator

You are an orchestrator of a website page import/migration. You have specialized Skills at your disposal for each phase of the import workflow. Below is a high-level overview of what you're going to do.

## When to Use This Skill

Use this skill when:
- Importing or migrating individual pages from existing websites
- Converting competitor pages for reference or analysis
- Creating content files from design prototypes or staging sites

**Do NOT use this skill for:**
- Building new blocks from scratch (use **content-driven-development** skill)
- Modifying existing block code (use **building-blocks** skill)
- Designing content models (use **content-modeling** skill)

## Scope

**This skill imports/migrates main content only:**
- ✅ Import: Hero sections, features, testimonials, CTAs, body content
- ❌ Skip: Header, navigation, footer (handled by dedicated skills)

## Philosophy

Follow **David's Model** (https://www.aem.live/docs/davidsmodel):
- Prioritize authoring experience over developer convenience
- Ask "How would an author in Word/Google Docs create this?"
- Minimize blocks - prefer default content where possible
- Use Block Collection content models

## Available Sub-Skills

This orchestrator delegates work to:
- **scrape-webpage** - Extract content, metadata, and images from source URL
- **identify-page-structure** - Identify section boundaries and content sequences
- **authoring-analysis** - Make authoring decisions (default content vs blocks)
- **generate-import-html** - Create structured HTML file
- **preview-import** - Verify in local dev server

These skills invoke additional skills as needed:
- **page-decomposition** - (via identify-page-structure) Analyze content sequences per section
- **block-inventory** - (via identify-page-structure) Survey available blocks
- **content-modeling** - (via authoring-analysis) Validate unclear block selections
- **block-collection-and-party** - (via authoring-analysis) Validate block existence

## Import Workflow

### Step 0: Create TodoList

Use the TodoWrite tool to create a todo list with the following tasks:

1. **Scrape the webpage** (scrape-webpage skill)
   - Success: metadata.json, screenshot.png, cleaned.html, images/ folder exist

2. **Identify page structure** (identify-page-structure skill)
   - Success: Section boundaries identified, content sequences documented, block inventory complete

3. **Analyze authoring approach** (authoring-analysis skill)
   - Success: Every content sequence has decision (default content OR block name), section styling validated

4. **Generate HTML file** (generate-import-html skill)
   - Success: HTML file exists, images folder copied, validation checklist passed

5. **Preview and verify** (preview-import skill)
   - Success: Page renders correctly in browser, matches original structure

---

### Step 1: Scrape Webpage

**Invoke:** scrape-webpage skill

**Provide:**
- Target URL
- Output directory: `./import-work`

**Success criteria:**
- ✅ metadata.json exists with paths, metadata, image mapping
- ✅ screenshot.png saved for visual reference
- ✅ cleaned.html with local image paths
- ✅ images/ folder with all downloaded images

**Mark todo complete when:** All files verified to exist

---

### Step 2: Identify Page Structure

**Invoke:** identify-page-structure skill

**Provide:**
- screenshot.png from Step 1
- cleaned.html from Step 1
- metadata.json from Step 1

**Success criteria:**
- ✅ Section boundaries identified with styling notes
- ✅ Content sequences documented for each section (neutral descriptions)
- ✅ Block inventory completed (local + Block Collection)

**Mark todo complete when:** All outputs documented

---

### Step 3: Analyze Authoring Approach

**Invoke:** authoring-analysis skill

**Provide:**
- Section list with content sequences from Step 2
- Block inventory from Step 2
- screenshot.png from Step 1

**Success criteria:**
- ✅ Every content sequence has decision: default content OR block name
- ✅ Block structures fetched for all blocks to be used
- ✅ Single-block sections validated for styling (Step 3e if applicable)

**Mark todo complete when:** All sequences have authoring decisions

---

### Step 4: Generate HTML File

**Invoke:** generate-import-html skill

**Provide:**
- Authoring analysis from Step 3
- Section styling decisions from Step 3
- metadata.json from Step 1
- cleaned.html from Step 1

**Success criteria:**
- ✅ HTML file saved at correct path (from metadata.json)
- ✅ All sections imported (no truncation)
- ✅ Images folder copied to correct location
- ✅ Metadata block included (unless skipped)
- ✅ Validation checklist passed

**Mark todo complete when:** HTML file written, images copied, validation passed

---

### Step 5: Preview and Verify

**Invoke:** preview-import skill

**Provide:**
- HTML file path from Step 4
- screenshot.png from Step 1 (for comparison)
- documentPath from metadata.json

**Success criteria:**
- ✅ Page loads in browser
- ✅ Blocks render correctly
- ✅ Layout matches original (compare with screenshot)
- ✅ No console errors
- ✅ Images load or show placeholders

**Mark todo complete when:** Visual verification passed

---

## High-Level Dos and Don'ts

**DO:**
- ✅ Follow the workflow steps in order
- ✅ Mark each todo complete after verification
- ✅ Use TodoWrite to track progress
- ✅ Import ALL content (partial import is failure)
- ✅ Compare final preview with original screenshot

**DON'T:**
- ❌ Skip steps or combine steps
- ❌ Make authoring decisions without block inventory
- ❌ Generate HTML before completing authoring analysis
- ❌ Truncate or summarize content
- ❌ Consider import complete without visual verification

## Success Criteria

Import is complete when:
- ✅ All 5 todos marked complete
- ✅ HTML file renders in browser
- ✅ Visual structure matches original page
- ✅ All content imported (no truncation)
- ✅ Images accessible

## Limitations

This orchestrator manages single-page import with existing blocks. It does NOT:
- Custom variant creation (blocks are used as-is)
- Multi-page batch processing (import one page at a time)
- Block code development (assumes blocks exist)
- Advanced reuse detection across imports
- Automatic block matching algorithms

For those features, consider more comprehensive import workflows in specialized tools.
