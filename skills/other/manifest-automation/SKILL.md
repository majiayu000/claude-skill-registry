---
name: manifest-automation
description: Create and update manifest files using advanced web automation with Playwright, intelligent retry logic, and smart merge capabilities
---

# Manifest Automation Skill

Automate the creation and updating of manifest files for AI coding tools using advanced browser automation, web search, and intelligent field-level retry logic.

## Overview

This skill extends beyond the existing `manifest-creator` by adding:

- **Dual Mode Operation**: CREATE new manifests or UPDATE existing ones with smart merge
- **Advanced Web Automation**: Playwright MCP for dynamic content, pricing calculators, and marketplace navigation
- **Intelligent Retry Logic**: 3-attempt strategy per field with graceful degradation to TODO comments
- **Smart Merge**: UPDATE mode preserves user-curated data while refreshing auto-discoverable fields
- **Type-Optimized Workflows**: Dedicated extraction strategies for each manifest type

## Supported Manifest Types

1. **CLI** - Command-line tools with platform-specific install commands
2. **Extension** - IDE extensions with marketplace URLs and install URIs
3. **IDE** - Integrated development environments with GUI installers
4. **Model** - AI models with technical specs and token pricing
5. **Provider** - Model providers (foundation or service)
6. **Vendor** - Companies and organizations

## Usage

### CREATE Mode

Create a new manifest from scratch:

```bash
# CLI tool
node .claude/skills/manifest-automation/scripts/automate.mjs create cli cursor-cli https://cursor.com/cli

# Extension
node .claude/skills/manifest-automation/scripts/automate.mjs create extension copilot https://github.com/features/copilot

# Model
node .claude/skills/manifest-automation/scripts/automate.mjs create model claude-opus https://anthropic.com/claude

# Provider
node .claude/skills/manifest-automation/scripts/automate.mjs create provider openrouter https://openrouter.ai

# IDE
node .claude/skills/manifest-automation/scripts/automate.mjs create ide cursor https://cursor.com

# Vendor
node .claude/skills/manifest-automation/scripts/automate.mjs create vendor anthropic https://anthropic.com
```

### UPDATE Mode

Update an existing manifest with fresh data:

```bash
# Update existing CLI manifest
node .claude/skills/manifest-automation/scripts/automate.mjs update cli cursor-cli https://cursor.com/cli

# Update extension (URL optional if already in manifest)
node .claude/skills/manifest-automation/scripts/automate.mjs update extension copilot
```

## How It Works

### CREATE Mode Workflow

1. **Load Schema & Workflow**
   - Read JSON schema for manifest type
   - Load type-specific workflow instructions
   - Initialize field tracker for retry logic

2. **Extract Information**
   - Use Playwright MCP to navigate websites
   - Use WebSearch to discover GitHub repos, marketplaces, social media
   - Extract data following type-specific workflow
   - Track attempts per field (max 3)

3. **Handle Failures Gracefully**
   - After 3 failed attempts per field: add TODO comment
   - Continue with partial data (save as draft)
   - Generate completion report

4. **Validate & Save**
   - Write manifest JSON to appropriate path
   - For IDE/CLI/Extension: check vendor manifest exists, create if missing
   - Update `data/github-stars.json`
   - Run `npm run generate` to regenerate TypeScript data files
   - Run schema validation
   - Report success/failures to user

### UPDATE Mode Workflow

1. **Load Existing Manifest**
   - Read current manifest from disk
   - Parse and validate structure

2. **Extract Fresh Data**
   - Follow same extraction workflow as CREATE
   - Use Playwright and WebSearch for current data

3. **Smart Merge**
   - **AUTO_UPDATE**: Replace with new values (versions, descriptions, pricing, specs)
   - **PRESERVE**: Keep existing (id, name, verified, i18n, relatedProducts)
   - **MERGE_ADDITIVE**: Add new items to arrays/objects (communityUrls, platforms)
   - **CONDITIONAL**: Present both for manual review (license)

4. **Generate Change Report**
   - Show what was updated, added, preserved
   - Flag fields needing manual review
   - Validate and save merged manifest

## Field Extraction Strategies

### CLI Workflow Focus
- Platform-specific install commands (brew, npm, apt, winget)
- Launch commands and installation paths
- GitHub releases for version tracking
- Cross-platform support detection

### Extension Workflow Focus
- IDE marketplace URLs (VS Code, JetBrains, Open VSX)
- Install URIs (vscode:extension/, cursor:extension/)
- Supported IDE detection and compatibility
- Publisher and extension ID extraction

### Model Workflow Focus
- Technical specifications (parameter size, context window, max output)
- Token pricing ($/M tokens for input/output/cache)
- Platform URLs (HuggingFace, Artificial Analysis, OpenRouter)
- Model card information extraction

### Provider Workflow Focus
- Provider type detection (foundation vs service)
- API key application URLs
- Platform integration discovery
- Developer documentation

### IDE Workflow Focus
- GUI installation (DMG, EXE, DEB installers)
- Download page navigation
- App Store distributions
- GUI-based installation steps

### Vendor Workflow Focus
- Company mission and description
- Official social media accounts
- Community links and presence
- Organization-level information

## Tool Integration

### When to Use Each Tool

**Playwright MCP** (mcp__playwright__browser_*):
- Dynamic JavaScript-rendered content
- Multi-step navigation (tabs, dropdowns, modals)
- IDE marketplace pages
- Pricing calculators and forms
- Interactive website elements
- LinkedIn company pages (verification and metadata)

**WebSearch**:
- Discovering GitHub repositories
- Finding marketplace URLs
- Locating social media profiles
- Platform-specific pages (HuggingFace, npm, PyPI)
- Validation and alternatives
- Wikipedia for cross-referencing company information
- LinkedIn company pages for authoritative metadata

**WebFetch** (fallback):
- Static documentation pages
- Simple content fetching
- Direct URL access for known pages

### Reference-Only Sources

**Wikipedia**:
- Use for verifying company descriptions and basic facts
- Cross-reference founding dates, headquarters, official names
- Validate social media links listed in Wikipedia infobox
- **NEVER store Wikipedia URLs in manifests** - use only for verification

**LinkedIn Company Pages**:
- Primary authoritative source for company metadata
- Verify company size, industry, official description
- Store the LinkedIn URL in `communityUrls.linkedin`
- Use company description to validate website description accuracy

### Playwright Patterns

**Pattern 1: Navigate → Snapshot → Extract**
```
1. mcp__playwright__browser_navigate(url)
2. mcp__playwright__browser_snapshot()
3. Extract data from snapshot elements
```

**Pattern 2: Interactive Navigation**
```
1. Take initial snapshot
2. mcp__playwright__browser_click(element)
3. mcp__playwright__browser_wait_for(text)
4. Take new snapshot and extract
```

**Pattern 3: Form Interaction**
```
1. mcp__playwright__browser_fill_form(fields)
2. Click submit button
3. Extract results from response
```

## Retry Logic

### 3-Attempt Strategy

Each field gets up to 3 extraction attempts before falling back to TODO comment:

**Attempt 1**: Direct extraction from primary source
- Official website, documentation, or main page
- Most authoritative source

**Attempt 2**: Alternative sources or search
- WebSearch for the information
- Alternative URL patterns
- Related pages or sections

**Attempt 3**: Final fallback sources
- Third-party platforms
- Package manager websites
- Community resources

**After 3 failures**: Add TODO comment with reason

### Retry Examples

**Installation Commands**:
1. Official installation docs page
2. WebSearch for package manager (brew, npm, PyPI)
3. GitHub README or package manager sites
4. TODO if still not found

**Pricing**:
1. Official pricing page
2. Footer/header navigation links
3. Documentation pricing mentions
4. TODO if behind "Contact Sales"

**Community URLs**:
1. Website footer social links
2. WebSearch "<product> official <platform>"
3. Common URL patterns validation
4. Set to null if not found

### TODO Comment Format

```json
{
  "communityUrls": {
    "discord": null, // TODO: Could not auto-discover after 3 attempts. Not found in footer or search results.
    "twitter": "https://x.com/product"
  }
}
```

## Smart Merge Field Categories

### AUTO_UPDATE Fields
Always replaced with freshly discovered values:
- `latestVersion` - Always fetch latest
- `description` - From official source
- `websiteUrl` - Official URL
- `docsUrl` - Documentation URL
- `tokenPricing` - Model pricing (changes frequently)
- `size`, `contextWindow`, `maxOutput` - Model specs

### PRESERVE Fields
Never updated (user-curated):
- `id` - Core identifier
- `name` - Display name
- `verified` - Manual verification status
- `i18n` - User translations
- `relatedProducts` - Manually curated relationships

### MERGE_ADDITIVE Fields
Add new items, keep existing:
- `communityUrls` - Add newly discovered social links
- `platformUrls` - Add new platform integrations
- `supportedIdes` - Add new IDE support
- `platforms` - Add new OS support
- `pricing` - Add new tiers, preserve existing

### CONDITIONAL Fields
Require manual review:
- `license` - Only update if from authoritative source (GitHub)
- `vendor` - Review name changes carefully

## Error Handling

### Graceful Degradation

1. **Field-Level Failures**: Track each field independently
2. **Partial Manifests**: Save draft even with missing fields
3. **TODO Comments**: Mark failed fields with reason
4. **Completion Reports**: Show what succeeded/failed

### Completion Report Format

```
📊 Manifest Automation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: DRAFT (3 fields incomplete)

✅ Successfully Extracted (42 fields)
❌ Failed Extraction (3 fields):
   1. communityUrls.discord (3 attempts)
      Reason: Not found in website footer or WebSearch
   2. pricing[2].value (3 attempts)
      Reason: Enterprise pricing behind contact form
   3. platforms[1].installCommand (3 attempts)
      Reason: Windows installation docs incomplete

⚠️  Cross-Reference Validation:
   ✓ Wikipedia: Company description verified
   ✓ LinkedIn: Company metadata matches
   ⚠️ Description length mismatch: Website (180 chars) vs LinkedIn (220 chars)

🌐 i18n Consistency Warnings (UPDATE mode only):
   ⚠️ English description updated - review i18n translations
   ⚠️ i18n.zh-Hans may be outdated (last updated: previous description)
   ⚠️ i18n.de may be outdated (last updated: previous description)
   → Add TODO comments to i18n fields requiring manual review

📝 Next Steps:
1. Review manifest file: manifests/clis/cursor-cli.json
2. Manually fill TODO-marked fields if information available
3. Add i18n translations (zh-Hans, de, ko)
4. Update verified field once data confirmed accurate
5. Run validation: npm run test:validate

Note: Vendor manifest, github-stars.json, and TypeScript files already updated.
```

## Comparison with manifest-creator

| Feature | manifest-creator | manifest-automation |
|---------|------------------|---------------------|
| **Tools** | WebFetch only | Playwright MCP + WebSearch + WebFetch |
| **Modes** | CREATE only | CREATE + UPDATE |
| **Retry Logic** | Manual/ask user | Automatic 3-attempt per field |
| **Dynamic Content** | Limited | Full Playwright support |
| **Merge Logic** | N/A | Smart field categorization |
| **Error Handling** | Stop and ask | TODO + draft + report |
| **Workflows** | Generic 7-step | Type-optimized phases |
| **Community Discovery** | Basic | Advanced WebSearch |
| **Pricing Extraction** | Static pages | Dynamic calculators |
| **Marketplace Support** | Limited | Full automation (VS Code, JetBrains) |

## Best Practices

### Accuracy
- Never generate or guess data - always extract from authoritative sources
- Validate URLs exist and are official
- Verify version numbers from releases, not estimates
- Check social media accounts are official (verification badges, content)
- **Use Wikipedia for cross-referencing** company facts, model specs, and historical data
- **Use LinkedIn as authoritative source** for company metadata and descriptions

### Completeness
- Follow type-specific workflow completely
- Don't skip optional fields - attempt extraction
- Use full 3-attempt retry strategy before TODO
- Generate comprehensive completion reports
- **Cross-reference with Wikipedia and LinkedIn** to ensure no critical information is missed
- Validate i18n translations match English default content

### Validation
- Always run schema validation after manifest creation
- Fix validation errors before marking complete
- Verify enum values (os, ideId, pricing categories)
- Check URL formats (https://, proper domains)
- **Verify company information** against Wikipedia and LinkedIn
- **Ensure i18n consistency** - all languages must reflect the same content

### Smart Merge
- In UPDATE mode, trust the merge categories
- Review CONDITIONAL fields manually
- Don't blindly replace PRESERVE fields
- Validate MERGE_ADDITIVE doesn't create duplicates
- **Flag i18n fields for review** when English content changes
- Include i18n drift warnings in completion reports

### Cross-Referencing Strategy
1. **Primary source**: Official website and documentation
2. **Verification source 1**: LinkedIn company page (for vendors/companies)
3. **Verification source 2**: Wikipedia (for well-known entities)
4. **Conflict resolution**: Official website > LinkedIn > Wikipedia
5. **Never store reference URLs**: Wikipedia and verification sources are for validation only

## Troubleshooting

### Playwright Navigation Fails
- Wait 2 seconds, retry navigation
- Check for redirects or authentication walls
- Try alternative URLs or WebSearch fallback

### Element Not Found in Snapshot
- Take screenshot for debugging
- Search page text directly (not by element ref)
- Try WebSearch as alternative approach

### Dynamic Content Doesn't Load
- Use `mcp__playwright__browser_wait_for` with specific text
- Scroll page to trigger lazy loading
- Click "Load More" or "Show All" buttons
- Fallback to WebSearch

### Rate Limiting or Blocking
- Add delays between requests
- Use WebSearch as alternative data source
- Mark field as TODO if consistently blocked

## Files Created

After running this skill, expect:

1. **Manifest file**: `manifests/<type>s/<name>.json`
2. **With TODO comments**: For failed field extractions
3. **Valid against schema**: `manifests/$schemas/<type>.schema.json`
4. **Ready for validation**: Run `npm run test:validate`

## GitHub Stars Update

After creating or updating a manifest, you **MUST** update the `data/github-stars.json` file:

### Why Update github-stars.json?

The `github-stars.json` file tracks GitHub star counts for all manifests. When you create or update a manifest:
- A new entry must be added for tracking
- The entry is initialized with `null` (stars not yet fetched)
- A scheduled job will automatically fetch the actual star count later

### How to Update

Use the `updateGithubStarsEntry()` function from `github-stars-updater.mjs`:

```javascript
import { updateGithubStarsEntry } from './lib/github-stars-updater.mjs'

// After creating a new manifest
const result = updateGithubStarsEntry('cli', 'cursor-cli', { isNew: true })

// After updating an existing manifest
const result = updateGithubStarsEntry('extension', 'claude-code', { isNew: false })
```

### CLI Usage

You can also use the CLI directly:

```bash
# Add new entry
node .claude/skills/manifest-automation/scripts/lib/github-stars-updater.mjs add cli cursor-cli

# Update existing entry
node .claude/skills/manifest-automation/scripts/lib/github-stars-updater.mjs update extension claude-code

# Remove entry
node .claude/skills/manifest-automation/scripts/lib/github-stars-updater.mjs remove ide windsurf
```

### What It Does

The updater will:
1. Load the current `github-stars.json` file
2. Add or update the entry: `<category>["<id>"] = null`
3. Sort entries alphabetically within the category
4. Save the updated file back to disk

### Example Result

For a new CLI manifest `cursor-cli`:

```json
{
  "clis": {
    "claude-code-cli": 43.5,
    "cursor-cli": null,  // ← newly added
    "kode": 3.6
  }
}
```

### Integration with Workflow

The `automate.mjs` script exports the necessary information for you to call the updater:

```javascript
// After workflow completes and manifest is saved:
import {
  updateGithubStarsEntry,
  manifestType,
  manifestName,
  operationMode
} from './automate.mjs'

updateGithubStarsEntry(manifestType, manifestName, { isNew: operationMode === 'create' })
```

## Next Steps After Creation

1. **Review manifest**: Check all extracted values for accuracy
2. **Fill TODOs**: Manually add fields that couldn't be auto-discovered
3. **Add translations**: Populate `i18n` object with localized content (zh-Hans, de, ko)
4. **Set verified**: Change `verified` to `true` if data is confirmed accurate
5. **Add related products**: Manually curate `relatedProducts` array
6. **Run validation**: Ensure schema compliance with `npm run test:validate`
7. **Commit changes**: Add manifest to git repository

Note: Vendor manifest and github-stars.json are automatically handled during creation.

## i18n Consistency Requirements

**IMPORTANT**: When creating or updating manifests with i18n content:

1. **Default Language (English)**:
   - All English content should be in top-level fields (e.g., `description`, `name`)
   - English should NEVER appear in the `i18n` object

2. **Multi-Language Support**:
   - Support at least 3 languages: English (default), Simplified Chinese (`zh-Hans`), German (`de`)
   - NEVER hardcode only `'en' | 'zh-Hans'` - always include `de` and support extensibility

3. **Content Synchronization**:
   - All i18n translations must reflect the SAME content as the English default
   - When updating default English fields, flag i18n fields for manual review
   - Never auto-translate - mark translations as TODO if not manually provided

4. **Validation Checks**:
   - After UPDATE mode, verify i18n content hasn't become stale
   - Flag i18n fields that may need updating when English content changes
   - Include i18n consistency warnings in completion reports

5. **Structure Example**:
```json
{
  "name": "Example Product",
  "description": "This is the default English description",
  "i18n": {
    "zh-Hans": {
      "name": "示例产品",
      "description": "这是默认的英文描述"
    },
    "de": {
      "name": "Beispielprodukt",
      "description": "Dies ist die englische Standardbeschreibung"
    }
  }
}
```

**In UPDATE mode**:
- If default English fields change, add comment: `// TODO: Update i18n translations to match new English content`
- Report i18n drift in completion report
- Preserve existing i18n content (PRESERVE category) but flag for review


