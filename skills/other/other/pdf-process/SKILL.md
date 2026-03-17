---
name: pdf-process
description: >-
  Run the complete PDF processing pipeline to convert the manual PDF into Next.js application data.
  This command executes all steps automatically: split, render, extract, translate, build, and
  manifest.
allowed-tools: Bash, Read, Task, TaskOutput
---

# PDF Processing Command

Run the complete PDF processing pipeline automatically.

## CRITICAL INSTRUCTION FOR CLAUDE CODE

**MANDATORY: You MUST follow the documented translation process EXACTLY as written in this skill. NO EXCEPTIONS.**

### Absolute Requirements During Execution:

1. **NEVER ask questions or suggest alternatives during translation execution**
2. **NEVER use MCP Codex (`mcp__codex__spawn_agents_parallel` or any codex tools) for translation**
3. **NEVER try to "optimize" or "improve" the process mid-execution**
4. **ONLY use the Task tool with `subagent_type="manual-translator"` as documented**
5. **Follow the exact worker pool pattern documented below**

### During Execution:

- GOAL: Translate ALL pages for the specified manual - continue until done or out of tokens
- Follow the documented process exactly - word for word
- Use ONLY the Task tool for translation (NOT MCP Codex)
- Execute all steps to completion without stopping
- Handle errors by retrying or continuing
- **Process pages in batches, spawning workers continuously**
- **Continue processing until ALL pages done OR token budget exhausted**
- **Save results after each batch and continue to next batch**
- DO NOT stop to ask "what approach should we take?"
- DO NOT suggest "better ways" mid-process
- DO NOT ask for user permission during execution
- DO NOT use MCP Codex or any other translation method
- DO NOT implement "improvements" you discover mid-process
- **NEVER ask user to choose between Options A/B/C**
- **NEVER ask "which approach would you prefer?"**
- **NEVER stop to explain limitations - just continue working**
- **NEVER stop after completing just one batch - keep going**

### If You Discover Improvements:

- Note them internally
- Report them AFTER all translation is 100% complete
- DO NOT implement them during execution
- DO NOT stop the process to discuss them

**This process has been run many times successfully. Trust the documentation and execute it exactly as written.**

---

## Usage

Run with a manual slug:

```
/pdf-process <slug>
```

## Parameters

- `slug`: Manual slug (e.g., oxi-one-mk2, oxi-coral)

## Examples

```
/pdf-process oxi-one-mk2
/pdf-process oxi-coral
```

## What This Does

This will execute all pipeline steps in order:

**Phase 1: PDF Processing**

0. **Ask User** - Collect manifest metadata (brand name, PDF title) from user
1. **Validate** - Check slug parameter and source directory
2. **Clean** - Remove all existing generated files (images, data, split PDFs)
3. **Split** - Split PDF into parts (30 pages each)
4. **Render** - Render pages to PNG images (150 DPI)
5. **Extract** - Extract text from PDFs
6. **Translate** - Translate to Japanese using manual-translator subagents (Task tool)
7. **Build** - Build final JSON files
8. **Manifest** - Create manifest.json
9. **Update Manifest** - Add brand name and title to manifest (from Step 0)
10. **Update Registry** - Add manual to `lib/manual-registry.ts` for Next.js build

**Phase 2: Verification (AI-Powered)**

11. **Build Production** - Run `pnpm build` for production build
12. **Serve** - Start production server on port 8030
13. **Capture** - Capture all pages using lightweight script
14. **Verify** - AI verification of each page (compare PDF image vs translation)
15. **Fix** - Fix extraction failures by regenerating text from images
16. **Re-translate** - Re-translate pages that had extraction issues
17. **Report** - Generate verification report

The entire process takes approximately 20-40 minutes for a 280-page manual.

## Implementation Logic

**BEFORE starting the pipeline, Claude Code MUST perform these steps:**

### Step 0: Gather Manifest Metadata (ASK USER)

**Before any processing, ask the user for manifest metadata using AskUserQuestion:**

Required information:

1. **Brand name**: The manufacturer/company name (e.g., "OXI Instruments", "ADDAC System")
2. **PDF title**: The title for the manual (e.g., "OXI E16: Manual", "OXI ONE MKII: Manual")
3. **Product slug**: The product identifier from takazudomodular repo (for linking manual to product)

#### Question 1: Brand Name

Use AskUserQuestion tool to ask for brand name:

- Question: "What is the brand name for this manual?"
- Options based on existing brands in the project (run `grep '"brand"' public/*/data/manifest.json` to find existing brands):
  - "OXI Instruments" (for OXI products)
  - "ADDAC System" (for ADDAC products)
  - Other (user can specify custom brand)

#### Question 2: PDF Title

Use AskUserQuestion tool to ask for PDF title:

- Question: "What is the title for this manual?"
- This should be a free-form text input (use "Other" option for custom input)
- Example titles from existing manuals:
  - "OXI ONE MKII: Manual"
  - "OXI Coral: Manual"
  - "OXI E16: Manual"
  - "ADDAC112 VC Looper: Manual"

#### Question 3: Product Slug (Auto-Detect with User Confirmation)

**Environment variable required:** `TAKAZUDO_MODULAR_REPO_PATH` must be set in `.env`

1. **Read product data** from takazudomodular repo:
   ```bash
   # Read product slugs from product-master-data.mjs
   grep -o "slug: '[^']*'" ${TAKAZUDO_MODULAR_REPO_PATH}/src/data/product-master-data.mjs | \
     sed "s/slug: '//g" | sed "s/'//g"
   ```

2. **Auto-detect matching product** based on manual slug:
   - Extract base name from manual slug (e.g., `oxi-e16-manual` → `oxi-e16`)
   - Search for matching product slug in product data
   - If found, suggest as default option

3. **Ask user to confirm or select product:**
   - Question: "Which product does this manual belong to?"
   - Options:
     - Auto-detected product (if found, marked as recommended)
     - Other matching products (if slug pattern matches multiple)
     - "None / Not applicable" (for standalone manuals)
     - "Other" (user can specify custom slug)

**Example logic:**
```javascript
// Read .env
const envPath = '/Users/takazudo/repos/personal/zmanuals/.env';
const envContent = fs.readFileSync(envPath, 'utf8');
const repoPath = envContent.match(/TAKAZUDO_MODULAR_REPO_PATH=(.+)/)?.[1];

// Read product-master-data.mjs
const productDataPath = `${repoPath}/src/data/product-master-data.mjs`;
const productData = fs.readFileSync(productDataPath, 'utf8');

// Extract all product slugs
const slugMatches = productData.match(/slug: '([^']+)'/g);
const productSlugs = slugMatches?.map(s => s.replace("slug: '", '').replace("'", ''));

// Find matching product for manual slug
const manualSlug = 'oxi-e16-manual';  // from command argument
const baseSlug = manualSlug.replace(/-manual|-quick-start|-guide/g, '');
const matchedProduct = productSlugs?.find(p => baseSlug.includes(p) || p.includes(baseSlug));
```

**Note:** All three questions can be asked in a single AskUserQuestion call with multiple questions.

Store all values for use in manifest creation (Step 7).

**Example existing manifests:**
```bash
# Check existing manifests for reference
grep -E '"(brand|title)"' public/*/data/manifest.json
# OXI Instruments - OXI ONE MKII, OXI Coral, OXI E16
# ADDAC System - ADDAC112
```

### Step 1: Validate Source Files

**Then perform these validation steps:**

```bash
# 1. Extract slug from command arguments
SLUG=$1

# 2. Validate slug is provided
if [ -z "$SLUG" ]; then
  echo "Error: Manual slug required"
  echo "Usage: /pdf-process <slug>"
  echo ""
  echo "Examples:"
  echo "  /pdf-process oxi-one-mk2"
  echo "  /pdf-process oxi-coral"
  exit 1
fi

# 3. Validate slug format (only lowercase letters, numbers, and hyphens)
if ! [[ "$SLUG" =~ ^[a-z0-9-]+$ ]]; then
  echo "Error: Invalid slug format: $SLUG"
  echo "Slug must contain only lowercase letters, numbers, and hyphens"
  echo ""
  echo "Valid examples:"
  echo "  oxi-one-mk2"
  echo "  oxi-coral"
  exit 1
fi

# 4. Check source directory exists
if [ ! -d "manual-pdf/$SLUG" ]; then
  echo "Error: Source directory not found: manual-pdf/$SLUG"
  echo ""
  echo "Please create the directory and add a PDF file:"
  echo "  mkdir -p manual-pdf/$SLUG"
  echo "  cp /path/to/manual.pdf manual-pdf/$SLUG/"
  exit 1
fi

# 5. Check if PDF file exists in source directory
PDF_COUNT=$(find "manual-pdf/$SLUG" -maxdepth 1 -name "*.pdf" | wc -l)
if [ "$PDF_COUNT" -eq 0 ]; then
  echo "Error: No PDF file found in manual-pdf/$SLUG"
  echo ""
  echo "Please add a PDF file to the directory:"
  echo "  cp /path/to/manual.pdf manual-pdf/$SLUG/"
  exit 1
fi

# 6. All validations passed - proceed with pipeline
echo "Validation successful"
echo "Processing manual: $SLUG"
echo ""
```

**THEN run the pipeline with the slug parameter:**

```bash
pnpm run pdf:all --slug "$SLUG"
```

**Translation Quality:**

- The manual-translator subagent automatically formats translations with proper paragraph breaks
- Numbered items are separated with blank lines (`\n\n`) for better readability
- Sub-items (I., II., III.) stay with their parent items
- This ensures the Japanese translation is easy to read on the web interface

---

## Internal Steps (For Claude Code Reference Only)

The pipeline consists of the following steps. **Users should not invoke these individually** - they are documented here for Claude Code's internal use only.

### Step 0: Clean (Run via Bash)

**ALWAYS run this first to ensure clean state:**

- `pnpm run pdf:clean --slug <slug>` - Remove all generated files for the specified manual

This ensures no stale data from previous runs interferes with the new processing.

### Step 1-3: Basic Processing (Run via Bash)

These steps can be run directly using pnpm with the --slug parameter:

- `pnpm run pdf:split --slug <slug>` - Split PDF into parts (30 pages each)
- `pnpm run pdf:render --slug <slug>` - Render pages to PNG images (150 DPI)
- `pnpm run pdf:extract --slug <slug>` - Extract text from PDFs

**Note:** All commands now require the --slug parameter to specify which manual to process.

### Step 4: Translation (Optimized Worker Pool with Direct File Writing)

**IMPORTANT:** Translation uses Claude Code's Task tool to spawn manual-translator subagents.

**DO NOT stop to ask questions during this process. Execute completely as documented.**

#### Translation Process (Optimized Workflow):

**Key Optimization:** Subagents write translation files directly instead of returning full text to main agent. This significantly reduces token consumption in main agent context.

**Workflow:**

1. **Prepare file paths**: For each page, determine source text file and output JSON file paths
2. **Spawn workers**: Create 5 concurrent background Task workers
3. **Workers execute autonomously**:
   - Each worker receives source file path and output file path
   - Worker reads source text using Read tool
   - Worker translates content following manual-translator guidelines
   - Worker writes JSON result directly to output file using Write tool
   - Worker returns only brief status message (not full translation text)
4. **Main agent verification**:
   - Wait for all workers to complete
   - Verify all output JSON files exist
   - Retry any failures with new workers

#### Example Implementation:

```javascript
// Prepare all page file paths
const slug = 'oxi-coral';
const totalPages = 46;
const workers = [];

// Spawn 5 concurrent workers
const MAX_CONCURRENT = 5;
for (let i = 0; i < Math.min(MAX_CONCURRENT, totalPages); i++) {
  const pageNum = i + 1;
  workers.push(spawnTranslationWorker(slug, pageNum, totalPages));
}

// Continue spawning workers as they complete
let nextPage = MAX_CONCURRENT + 1;
while (workers.some(w => w)) {
  for (let i = 0; i < workers.length; i++) {
    if (workers[i] && checkCompleted(workers[i])) {
      if (nextPage <= totalPages) {
        workers[i] = spawnTranslationWorker(slug, nextPage++, totalPages);
      } else {
        workers[i] = null;
      }
    }
  }
}

// Verify all files exist
const failures = verifyTranslationFiles(slug, totalPages);

// Retry failures
if (failures.length > 0) {
  retryFailedPages(failures);
}
```

#### Task Invocation (per page):

**CRITICAL:** Pass file paths to the subagent, NOT the page content.

```xml
<invoke name="Task">
  <parameter name="subagent_type">manual-translator</parameter>
  <parameter name="description">Translate page 1/46</parameter>
  <parameter name="prompt">Translate page 1 of the OXI CORAL manual.

Source text file:
/Users/takazudo/repos/personal/zmanuals/public/oxi-coral/processing/extracted/page-001.txt

Output JSON file:
/Users/takazudo/repos/personal/zmanuals/public/oxi-coral/processing/translations-draft/page-001.json

Page: 1
Total pages: 46

Read the source file, translate the content, and write the JSON result directly to the output file using JSON.stringify() for proper escaping. Return only a brief status message.</parameter>
  <parameter name="run_in_background">true</parameter>
</invoke>
```

#### Verification and Retry:

After all workers complete, verify and retry:

```javascript
function verifyTranslationFiles(slug, totalPages) {
  const failures = [];
  for (let i = 1; i <= totalPages; i++) {
    const pageStr = String(i).padStart(3, '0');
    const outputFile = `public/${slug}/processing/translations-draft/page-${pageStr}.json`;

    if (!fs.existsSync(outputFile)) {
      failures.push(i);
    }
  }
  return failures;
}

function retryFailedPages(failures) {
  for (const pageNum of failures) {
    // Spawn retry worker
    spawnTranslationWorker(slug, pageNum, totalPages);
  }
}
```

**Key Benefits:**

- **Token savings**: Workers return only status messages, not full translations
- **Autonomous execution**: Workers handle file I/O independently
- **Verification**: Main agent checks all files exist after completion
- **Retry logic**: Automatic retry for failed translations
- **Scalability**: Can process hundreds of pages without token overflow

**Key Points:**

- Use `run_in_background=true` for all workers
- Pass file paths, not content, to workers
- Workers use Read and Write tools directly
- Main agent verifies all files after completion
- Retry any missing files automatically

### Step 5-6: Final Processing (Run via Bash)

- `pnpm run pdf:build --slug <slug>` - Build final JSON files from translation drafts
- `pnpm run pdf:manifest --slug <slug>` - Create manifest.json

**Note:** Both commands require the --slug parameter to specify which manual to process.

### Step 7: Update Manifest with User-Provided Metadata (REQUIRED)

**After manifest creation, update the manifest with brand name, title, productSlug, and updatedAt collected in Step 0:**

```javascript
// Read the manifest
const manifestPath = `public/${slug}/data/manifest.json`;
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

// Update with user-provided values (collected in Step 0)
manifest.title = pdfTitle;         // e.g., "OXI E16: Manual"
manifest.brand = brandName;        // e.g., "OXI Instruments"
manifest.productSlug = productSlug; // e.g., "oxi-e16" (from takazudomodular product data)

// Add updatedAt with current date in YYYYMMDD format
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0');
const day = String(today.getDate()).padStart(2, '0');
manifest.updatedAt = `${year}${month}${day}`;  // e.g., "20260112"

// Write back
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
```

Or use the Edit tool to update all fields:

```json
{
  "title": "OXI E16: Manual",      // Update this with user-provided title
  "brand": "OXI Instruments",      // Add this with user-provided brand
  "productSlug": "oxi-e16",        // Add product slug from takazudomodular
  "updatedAt": "20260112",         // Add current date in YYYYMMDD format
  "version": "1.0.0",
  ...
}
```

**This step is REQUIRED to ensure:**

- The correct title appears on the manual page
- The brand name appears on the manual index page
- The updatedAt date is displayed on the landing page
- The productSlug links this manual to the product in takazudomodular (for auto-sync)

### Step 8: Update Manual Registry (REQUIRED)

**After manifest update, add the new manual to `lib/manual-registry.ts` so Next.js can generate pages for it.**

This step is CRITICAL - without it, the build will not generate HTML pages for the new manual.

#### 8.1 Generate Variable Name from Slug

Convert the slug to a camelCase variable name:
```javascript
// Example: "ai008-matrix-mixer" → "ai008MatrixMixer"
function slugToVarName(slug) {
  return slug.replace(/-([a-z0-9])/g, (_, char) => char.toUpperCase());
}
```

#### 8.2 Check if Already Registered

Read `lib/manual-registry.ts` and check if the manual is already imported:
```javascript
const registryPath = 'lib/manual-registry.ts';
const content = fs.readFileSync(registryPath, 'utf8');
const isAlreadyRegistered = content.includes(`'${slug}':`);
```

If already registered, skip this step.

#### 8.3 Add Import Statements

Find the last import block and add new imports after it:
```typescript
// Import {slug}
import {varName}Manifest from '@/public/{slug}/data/manifest.json';
import {varName}Pages from '@/public/{slug}/data/pages-ja.json';
```

**Example:**
```typescript
// Import ai008-matrix-mixer
import ai008MatrixMixerManifest from '@/public/ai008-matrix-mixer/data/manifest.json';
import ai008MatrixMixerPages from '@/public/ai008-matrix-mixer/data/pages-ja.json';
```

Use the Edit tool to insert after the last existing import (before `export interface ManualRegistryEntry`).

#### 8.4 Add Registry Entry

Find the closing `};` of the MANUAL_REGISTRY object and add new entry before it:
```typescript
  '{slug}': {
    manifest: {varName}Manifest as unknown as ManualManifest,
    pages: {varName}Pages as unknown as ManualPagesData,
  },
```

**Example:**
```typescript
  'ai008-matrix-mixer': {
    manifest: ai008MatrixMixerManifest as unknown as ManualManifest,
    pages: ai008MatrixMixerPages as unknown as ManualPagesData,
  },
```

Use the Edit tool to insert before the closing `};` of MANUAL_REGISTRY.

#### Implementation Example:

```javascript
const slug = 'ai008-matrix-mixer';
const varName = 'ai008MatrixMixer';  // converted from slug

// 1. Add imports (find last import, add after it)
const importBlock = `
// Import ${slug}
import ${varName}Manifest from '@/public/${slug}/data/manifest.json';
import ${varName}Pages from '@/public/${slug}/data/pages-ja.json';
`;

// 2. Add registry entry
const registryEntry = `  '${slug}': {
    manifest: ${varName}Manifest as unknown as ManualManifest,
    pages: ${varName}Pages as unknown as ManualPagesData,
  },`;

// Use Edit tool to:
// - Insert importBlock before "export interface ManualRegistryEntry"
// - Insert registryEntry before the closing "};" of MANUAL_REGISTRY
```

**Why this step is REQUIRED:**

- Next.js static export requires explicit imports (no dynamic require())
- Without registry entry, `generateStaticParams()` won't include this manual
- Build will succeed but the manual pages won't be generated
- Users will see 404 when accessing the manual URL

### Steps 9-16: Verification Phase (MANDATORY)

**After all translation and build steps are complete, execute the verification phase directly (do NOT call /verify-translation as a separate skill).**

#### Step 9: Build Production

```bash
pnpm build
```

This creates an optimized production build in `/out/` directory.

#### Step 10: Start Production Server

```bash
# Start serve in background
pnpm serve &

# Wait for server to be ready
sleep 3

# Verify server is running (port 8030)
curl -s -o /dev/null -w "%{http_code}" http://localhost:8030/manuals/$SLUG/page/1
```

#### Step 11: Capture All Pages

**Use the lightweight capture script (NOT MCP Playwright):**

```bash
node .claude/skills/verify-translation/scripts/capture-pages.js \
  --slug $SLUG \
  --pages $TOTAL_PAGES \
  --port 8030
```

This script:

- Uses direct Playwright scripting (much lighter than MCP)
- Captures all pages at 2000x1600 resolution
- Saves to `__inbox/verify-{slug}-{date}-{session}/`
- Outputs summary.json with results

#### Step 12: AI-Powered Verification

**For EACH captured page, perform visual verification:**

1. **Read the screenshot** using the Read tool
2. **Compare** the LEFT side (PDF image) with RIGHT side (translation)
3. **Check** if translation covers ALL visible content in PDF image

**Issues to detect:**

| Issue | Description |
|-------|-------------|
| Missing header | PDF shows section header but translation starts mid-content |
| Missing paragraphs | PDF has more paragraphs than translation shows |
| Content order wrong | Translation starts from middle of page |
| Extraction failure | Large portions of PDF text not in translation |

**Record findings for each page:**

```json
{
  "pageNum": 49,
  "status": "needs_fix",
  "issues": ["Missing header: 'Scenes 3'", "Missing paragraph"]
}
```

#### Step 13: Fix Extraction Failures

For each page flagged as needing fix:

**13.1 Regenerate extracted text from PDF image:**

Look at the PDF image (left side of screenshot) and extract ALL visible English text in correct reading order.

**13.2 Update the extracted text file:**

```bash
Write to: public/$SLUG/processing/extracted/page-XXX.txt
```

**13.3 Re-translate the page:**

```xml
<invoke name="Task">
  <parameter name="subagent_type">manual-translator</parameter>
  <parameter name="description">Re-translate page XXX</parameter>
  <parameter name="prompt">Translate page XXX of the manual.
Source: /path/to/extracted/page-XXX.txt
Output: /path/to/translations-draft/page-XXX.json
Page: XXX, Total: YYY</parameter>
</invoke>
```

#### Step 14: Rebuild After Fixes

If any pages were fixed:

```bash
# Copy translations to expected location
mkdir -p public/manuals/$SLUG/processing/translations-draft
cp public/$SLUG/processing/translations-draft/*.json public/manuals/$SLUG/processing/translations-draft/

# Rebuild pages.json
pnpm run pdf:build --slug $SLUG

# Copy back to correct location
cp public/manuals/$SLUG/data/pages.json public/$SLUG/data/pages.json
rm -rf public/manuals/

# Format
pnpm format:fix
```

#### Step 15: Stop Serve Process

```bash
lsof -ti:8030 | xargs kill -9 2>/dev/null || true
```

#### Step 16: Generate Report

Output a verification report:

```markdown
## Translation Verification Report

**Manual:** {slug}
**Total Pages:** {totalPages}
**Date:** {date}

### Verification Results

| Status | Count |
|--------|-------|
| Passed | XX |
| Fixed | XX |

### Pages Fixed

| Page | Issues Found | Fix Applied |
|------|--------------|-------------|
| 35 | Missing header | Regenerated, re-translated |
| 49 | Missing paragraph | Regenerated, re-translated |

### Verification Complete

All pages now match their PDF images.
Manual is ready for deployment.
```

**Why verification is mandatory:**

PDF text extraction (`pdf-parse`) can fail silently. The `manual-translator` subagent only sees extracted text, not images, so it cannot detect missing content. This verification step catches those failures.

---

## Quick Reference

### Run Full Pipeline

```bash
/pdf-process <slug>
```

This runs everything automatically including verification.

### Individual Steps (for debugging)

```bash
pnpm run pdf:clean --slug <slug>     # Clean existing files
pnpm run pdf:split --slug <slug>     # Split PDF
pnpm run pdf:render --slug <slug>    # Render pages
pnpm run pdf:extract --slug <slug>   # Extract text
# Translation via Task tool (manual-translator subagents)
pnpm run pdf:build --slug <slug>     # Build JSON
pnpm run pdf:manifest --slug <slug>  # Create manifest
```

### Manual Verification (if needed separately)

```bash
pnpm build
pnpm serve &
node .claude/skills/verify-translation/scripts/capture-pages.js --slug <slug> --pages <total>
# Then manually verify captured screenshots
```

## Requirements

- PDF file in `manual-pdf/{slug}/` directory
- Claude Code CLI installed (for translation subagents)
- pnpm package manager

## Output Structure

```
manual-pdf/{slug}/               # Source PDF directory
  └── *.pdf                      # Source PDF file

public/{slug}/                   # Output directory
  ├── data/                      # Final JSON files (committed)
  │   ├── manifest.json
  │   └── pages.json
  ├── pages/                     # Rendered PNG images (300 DPI)
  │   ├── page-001.png
  │   └── ... (page-XXX.png)
  └── processing/                # Intermediate files (gitignored)
      ├── extracted/             # Extracted text
      └── translations-draft/    # Translation drafts
```

## Configuration

Edit `pdf-config.json` to customize:

- Image DPI (default: 300)
- Translation model
- Max retry attempts

## Error Handling

- Error reports saved to `__inbox/`
- Scripts can resume from failed step
- Retry logic for API failures (3 attempts)

## Performance

**Estimated time (280-page manual):**

- Total: 15-30 minutes
- Translation: 10-20 minutes (most time-consuming)

**Estimated cost:**

- Translation: Free (uses Claude Code subagents, not API)
