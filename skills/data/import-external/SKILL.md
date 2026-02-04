---
name: import-external
description: AUTO-EXECUTE import of external work items (GitHub/JIRA/ADO) since last import. NO PROMPTS - immediately runs with defaults. Creates READ-ONLY references in living docs. Options available but NOT required.
---

# Import External Work Items (Reference Import)

Import work items from GitHub (issues/milestones), JIRA (epics/stories), or Azure DevOps (work items) into SpecWeave living docs **as read-only references**.

> **Important**: This command creates a **reference catalog**, NOT increments. Imported items have E-suffix IDs (US-001E, FS-042E). To implement an imported item, you must **manually create an increment** that references it.

## CRITICAL: Default Behavior (NO PROMPTS!)

**When user runs `/sw:import-external` with NO arguments:**
1. **IMMEDIATELY execute** with default settings - DO NOT show menus or ask questions
2. **Default = "since last import"** - auto-detects from `.specweave/sync-metadata.json`
3. **If first import ever** - defaults to last 1 month
4. **Import from ALL configured platforms** (GitHub, JIRA, ADO - whichever are configured)

**WRONG behavior** (DO NOT DO THIS):
```
❌ "What would you like to import?"
❌ "Which option would you like?"
❌ "Should I run a dry run first?"
❌ Showing a menu of options
```

**CORRECT behavior**:
```
✅ Immediately start importing
✅ Show progress: "🔄 Importing from GitHub... [25/150]"
✅ Show summary when done
```

## What This Does

1. **Detects configured external tools** (GitHub, JIRA, ADO) from environment/config
2. **Fetches work items** based on time range filter (since last import by default)
3. **Assigns IDs with E suffix and validation**
   - IDs have E suffix to indicate external origin (US-001E, T-001E, FS-042E)
   - **Validates FS (Feature) IDs** to avoid conflicts:
     ```typescript
     import { validateIncrementNumber, logValidationResult } from './src/core/increment-validator.js';

     // Get all existing feature IDs (including E-suffix ones)
     const existingFeatures = [
       ...fs.readdirSync('.specweave/docs/internal/specs/'),
       ...fs.readdirSync('.specweave/increments/').map(parseFeatureId),
     ].filter(f => /^FS-\d{3}E?$/.test(f));

     // For external feature FS-042E, validate base number 042
     const baseNumber = featureId.replace('E', '').replace('FS-', '');
     const result = validateIncrementNumber(baseNumber, existingFeatures);

     // Log warnings if non-sequential
     if (result.warnings.length > 0) {
       console.log('ℹ️  External feature ID validation:');
       logValidationResult(result);
       console.log('   This is normal for external imports (IDs from external system)');
     }
     ```
   - Note: External IDs may be non-sequential (they come from external systems)
   - Validation ensures awareness of gaps, not enforcement

4. **Creates living docs files** in `.specweave/docs/internal/specs/FS-XXXE/`
5. **Updates sync metadata** (`.specweave/sync-metadata.json`) with import timestamp
6. **Skips duplicates** automatically (checks existing external IDs)
7. **Shows progress** indicator and summary report

## Usage

```bash
/sw:import-external [options]
```

### Options (ALL OPTIONAL - defaults work without them)

- `--since=<range>` - Time range filter (default: since last import)
  - `last` - Since last import (uses sync metadata) **← DEFAULT**
  - `1m`, `3m`, `6m` - Last 1/3/6 months
  - `all` - All items (no time filter)
  - Custom: `2025-01-01` - Since specific date (ISO format)
- `--github-only` - Import from GitHub only
- `--jira-only` - Import from JIRA only
- `--ado-only` - Import from Azure DevOps only
- `--dry-run` - Preview what would be imported without creating files

## Examples

### Example 1: Import New Items (Default - NO PROMPTS!)

```bash
/sw:import-external

# IMMEDIATELY executes with defaults:
# - Since last import (or 1 month if first import)
# - All configured platforms

# Output (NO QUESTIONS ASKED):
# 📥 Import External Work Items
#
# 📋 Import Configuration:
#   Platforms: GITHUB
#   Time range: last
#   Dry run: No
#
# 🔗 Imported from GITHUB: 15 items
#
# 📊 Import Summary:
#    Total imported: 15 items
#    🔗 GITHUB: 15 items
# ✅ Import complete!
```

### Example 2: GitHub Only (Last 3 Months)

```bash
/sw:import-external --github-only --since=3m

# Imports only from GitHub
# Items created in last 3 months
```

### Example 3: Dry Run (Preview)

```bash
/sw:import-external --dry-run --since=1m

# Shows what would be imported without creating files
# Useful for checking item counts before actual import

# Result:
# 🔍 Dry run - no files will be created
# 📊 Preview:
#    GitHub: 25 items (5 duplicates skipped)
#    JIRA: 10 items (2 duplicates skipped)
#    Total: 35 new items, 7 existing
# ⚠️  Remove --dry-run to perform actual import
```

### Example 4: JIRA Only (All Items)

```bash
/sw:import-external --jira-only --since=all

# Imports all JIRA items (no time filter)
# ⚠️  Warning shown if > 100 items detected
```

## Time Range Filters

### Since Last Import (Default)

```bash
/sw:import-external

# Reads last import timestamp from:
# .specweave/sync-metadata.json
# {
#   "github": { "lastImport": "2025-11-15T10:30:00Z" },
#   "jira": { "lastImport": "2025-11-10T14:20:00Z" }
# }
#
# GitHub: imports items created after 2025-11-15T10:30:00Z
# JIRA: imports items created after 2025-11-10T14:20:00Z
```

### Relative Time Ranges

```bash
--since=1m   # Last 1 month
--since=3m   # Last 3 months
--since=6m   # Last 6 months
```

### Absolute Date

```bash
--since=2025-01-01   # Since January 1, 2025 (ISO format: YYYY-MM-DD)
```

### All Items

```bash
--since=all   # Import all items (no time filter)
# ⚠️  Warning: May import hundreds of items
```

## Configured Platforms

The command auto-detects configured platforms from:

### GitHub
- **Detection**: `.git/config` remote URL
- **Auth**: `GITHUB_TOKEN` environment variable
- **Format**: `github.com/{owner}/{repo}`

### JIRA
- **Detection**: `JIRA_HOST` environment variable
- **Auth**: `JIRA_EMAIL` + `JIRA_API_TOKEN`
- **Format**: `https://{company}.atlassian.net`

### Azure DevOps
- **Detection**: `ADO_ORG_URL` environment variable
- **Auth**: `ADO_PAT` (Personal Access Token)
- **Format**: `https://dev.azure.com/{org}` + `ADO_PROJECT`

## Progress Indicator

During import, you'll see real-time progress:

```
🔄 Importing from GitHub... [25/150] ⠋
⚠️  GitHub rate limit low: 42/5000 remaining. Resets at 10:45 AM (in 300s).
🔄 Importing from GitHub... [150/150] ✓

🔄 Importing from JIRA... [12/12] ✓
```

- **Spinner**: Shows active import
- **Counter**: `[current/total]` items processed
- **Rate limit warnings**: Shown if remaining requests drop below threshold
- **Checkmark**: `✓` when platform import completes

## Summary Report

After import, a detailed summary is shown:

```
📊 Import Summary:
   Total imported: 162 items
   - GitHub: 150 items (US-201E to US-350E)
   - JIRA: 12 items (US-351E to US-362E)

   Duplicates skipped: 8 items
   - GitHub: 5 items (already imported)
   - JIRA: 3 items (already imported)

   Rate limit status:
   - GitHub: 3842/5000 remaining (resets at 11:00 AM)
   - JIRA: Estimated 950/1000 remaining

✅ Import complete!
   Living docs updated: .specweave/docs/internal/specs/
   Sync metadata updated: .specweave/sync-metadata.json
```

## Duplicate Detection

The command automatically skips items that have already been imported:

- Scans all `us-*.md` files in living docs
- Checks `external_id` frontmatter field
- Skips if external ID already exists (e.g., `GH-#638`, `JIRA-PROJ-123`)
- Reports skipped count in summary

## Rate Limiting

The command monitors API rate limits and handles them gracefully:

### Warning Threshold (100 requests remaining)

```
⚠️  GitHub rate limit low: 42/5000 remaining. Resets at 10:45 AM (in 300s).
```

- Import continues normally
- Warning shown to user

### Pause Threshold (10 requests remaining)

```
⚠️  GitHub rate limit critically low. Waiting 60s before continuing...
```

- Import pauses automatically
- Resumes after wait period
- No user action required

### Retry Suggestions (Rate limit exceeded)

```
❌ GitHub rate limit exceeded.
   Remaining: 0/5000
   Resets at: 10:45 AM (in 300 seconds)

💡 Suggestions:
   - Wait 5 minutes and retry
   - Use --github-only next time to avoid hitting limit
   - Increase time range to reduce item count (--since=1m instead of --since=all)
```

## Large Import Confirmation

If import detects > 100 items, you'll be prompted:

```
⚠️  Found 250 items to import:
   - GitHub: 200 items
   - JIRA: 50 items

   This may take 5-10 minutes and use significant API quota.

Continue? (Y/n) _
```

- Press `Y` or `Enter` to proceed
- Press `n` to cancel
- Use `--since=1m` to reduce item count

## Sync Metadata

After successful import, sync metadata is updated:

**File**: `.specweave/sync-metadata.json`

```json
{
  "github": {
    "lastImport": "2025-11-19T10:30:00Z",
    "lastImportCount": 150,
    "lastSkippedCount": 5,
    "lastSyncResult": "success"
  },
  "jira": {
    "lastImport": "2025-11-19T10:32:00Z",
    "lastImportCount": 12,
    "lastSkippedCount": 3,
    "lastSyncResult": "success"
  }
}
```

- `lastImport`: Timestamp of most recent successful import
- `lastImportCount`: Number of items imported in last sync
- `lastSkippedCount`: Number of duplicates skipped
- `lastSyncResult`: `success`, `partial`, or `failed`

## Living Docs Structure

Imported items create living docs files with E suffix:

```
.specweave/docs/internal/specs/
├── FS-042E/                    ← Feature (external)
│   ├── README.md               ← Feature metadata
│   ├── us-001e-login.md        ← User Story (external)
│   └── us-002e-signup.md       ← User Story (external)
└── FS-043E/                    ← Feature (external)
    └── us-001e-api-auth.md     ← User Story (external)
```

### User Story File Format

```markdown
---
us_id: US-001E
title: "User Login"
feature_id: FS-042E
origin: external
external_platform: github
external_id: GH-#638
external_url: https://github.com/owner/repo/issues/638
imported_at: 2025-11-19T10:30:00Z
status: open
---

# US-001E: User Login

**Origin**: 🔗 GitHub (GH-#638)

## Description

[Original GitHub issue description]

## Acceptance Criteria

[Parsed from GitHub issue body or comments]

## Tasks

No tasks defined.

## Implementation Notes

[Original labels, comments, metadata from GitHub]
```

## When to Use

- **After initial setup**: Import new external items created after `specweave init`
- **Periodic sync**: Weekly/monthly imports to stay in sync with external tools
- **Brownfield onboarding**: Import historical items missed during initialization
- **Cross-team collaboration**: Pull work items from other teams' external tools

## Limitations

- **NO automatic increment creation**: Imported items live in living docs ONLY
  - User must manually create increment when ready to work on external item
- **Read-only snapshot**: External items are imported as static snapshots
  - No two-way sync (external tool → SpecWeave only)
- **Pagination**: Large imports (500+ items) may take several minutes
- **API quota**: Uses GitHub/JIRA/ADO API quota
  - GitHub: 5000 requests/hour (authenticated)
  - JIRA: ~1000 requests/hour (Cloud estimate)
  - ADO: 200 requests/minute

## Differences from `specweave init`

| Feature | `specweave init` | `/sw:import-external` |
|---------|------------------|------------------------------|
| When to use | First-time setup | Ongoing imports after init |
| User prompts | Interactive setup | **NONE** (auto-execute with defaults) |
| Time range | Configurable (default: 1 month) | Since last import (auto-detected) |
| Config update | Creates `.specweave/config.json` | Uses existing config |
| Primary use case | Brownfield onboarding | Stay in sync with external tools |
| Execution | Step-by-step wizard | **Immediate** (no questions asked) |

## Troubleshooting

### Error: "No platforms configured"

```
❌ No external platforms configured.

💡 Ensure one of these is set:
   - GitHub: GITHUB_TOKEN + .git/config remote
   - JIRA: JIRA_HOST + JIRA_EMAIL + JIRA_API_TOKEN
   - Azure DevOps: ADO_ORG_URL + ADO_PROJECT + ADO_PAT
```

**Solution**: Set environment variables for at least one platform

### Error: "Rate limit exceeded"

```
❌ GitHub rate limit exceeded (0/5000 remaining).
   Resets at: 10:45 AM (in 300 seconds)
```

**Solution**: Wait for rate limit reset, or use platform filter (`--jira-only`) to avoid GitHub

### Warning: "Found 0 items to import"

```
⚠️  No new items found since last import (2025-11-19T10:30:00Z).
```

**Solution**: This is expected if no new work items created since last import. Use `--since=all` to re-import all items (will skip duplicates).

## See Also

- `specweave init` - Initial project setup with external tool import
- [External Import Guide](https://docs.spec-weave.com/guides/external-import)
- [GitHub Integration](https://docs.spec-weave.com/integrations/github)
- [JIRA Integration](https://docs.spec-weave.com/integrations/jira)
- [Azure DevOps Integration](https://docs.spec-weave.com/integrations/ado)

---

**Implementation**: `src/cli/commands/import-external.ts`
