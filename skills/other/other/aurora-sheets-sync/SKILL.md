---
name: aurora-sheets-sync
description: >
  Bidirectional sync between Aurora YAML schemas and Google Sheets.
  Trigger: When syncing schemas to/from spreadsheets, push/pull commands, google sheets sync.
license: MIT
metadata:
  author: aurora
  version: "2.0"
  auto_invoke: "sync schemas, google sheets, push schemas, pull schemas, spreadsheet sync"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

## When to Use

- User wants to sync YAML schemas to Google Sheets (`push`)
- User wants to sync Google Sheets to YAML schemas (`pull`)
- User mentions "sincronizar", "spreadsheet", "google sheets", "exportar schemas"
- Troubleshooting sync issues or configuration problems

---

## Critical Patterns

### 1. Spreadsheet Structure

| Sheet | Purpose |
|-------|---------|
| `DATA` | Dropdown values, validations (don't modify) |
| `TEMPLATE` | Template duplicated for new modules |
| `MODULES` | Index with hyperlinks to module sheets |
| `{module-name}` | One sheet per module (e.g., `business-partner`) |

### 2. Module Sheet Format

- **Row 1**: Headers (read dynamically)
- **Row 2+**: Properties (one per row)
- **Booleans**: `✓` (CHAR 9989) = true, empty = false

### 3. Pull is Idempotent

**Rule**: If no content changes in spreadsheet, YAML files must NOT be modified.

```typescript
// Content comparison before writing
if (normalizeYamlForComparison(existing) === normalizeYamlForComparison(new)) {
  // Skip write - preserves original formatting
}
```

### 4. Preserve Fields Not in Spreadsheet

Fields in YAML without spreadsheet columns are preserved on pull:
- `relationship.singularName`, `relationship.aggregateName`, `relationship.modulePath`
- `relationship.key`, `relationship.field`, `relationship.avoidConstraint`
- `webComponent`

### 5. Field Mappings

| Sheet Column | YAML Field | Notes |
|--------------|------------|-------|
| `relationship` | `relationship.type` | `1:1`, `N:1`, `1:N`, `N:N` |
| `master` | `relationship.modulePath` | Module name only |
| `subtype` | `arrayOptions.type` | When `type=array` |
| `values` | Multiple | `enumOptions`, `decimals`, or `arrayOptions.enumOptions` |
| `hasAuth` | `hasOAuth` | Header mapping |

### 6. Array Format in YAML

**Inline format** `[A, B, C]`:
- `enumOptions`
- `decimals`
- `defaultValue` (when array)

**Multi-line format** (for readability):
- `excludedOperations`
- `excludedFiles`

### 7. Nullable and DefaultValue Rules

- **nullable**: If not checked (✓), defaults to `false` (never undefined)
- **defaultValue**: Wrapped in array `[value]` when `type=array`
- **description**: Format preserved even when field is renamed (matched by content)

---

## Commands

```bash
# Navigate to tool directory
cd scripts/aurora-sheets-sync

# Install dependencies (first time)
npm install

# Push: YAML → Google Sheets
npx ts-node src/index.ts push --bc business-partner-portal
npx ts-node src/index.ts push --all
npx ts-node src/index.ts push --bc iam --dry-run

# Pull: Google Sheets → YAML
npx ts-node src/index.ts pull --bc business-partner-portal
npx ts-node src/index.ts pull --bc iam --no-backup
npx ts-node src/index.ts pull --all --dry-run

# Validate connection
npx ts-node src/index.ts validate --bc business-partner-portal

# List configured bounded contexts
npx ts-node src/index.ts list
```

---

## Configuration

### aurora-sheets.config.json

```json
{
  "credentialsPath": "./scripts/aurora-sheets-sync/credentials/service-account.json",
  "boundedContexts": {
    "business-partner-portal": {
      "spreadsheetId": "1ABC123xyz...",
      "description": "Business Partner Portal"
    }
  },
  "backupsPath": "backups/aurora-schemas",
  "cliterPath": "cliter"
}
```

### Google Cloud Setup (Quick Reference)

1. Create project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **Google Sheets API** (APIs & Services → Library)
3. Create **Service Account** (APIs & Services → Credentials)
4. Download JSON key → save to `credentials/service-account.json`
5. Share spreadsheet with service account email (Editor role)

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `The caller does not have permission` | Share spreadsheet with service account email |
| `Google Sheets API has not been enabled` | Enable API in Google Cloud Console |
| `Could not load credentials` | Check `credentialsPath` in config |
| `Skipped: X (empty or invalid)` | Sheet missing headers or `name`/`type` columns |
| Pull shows "(no changes)" | Idempotent - content unchanged, file preserved |

---

## Key Files

```
scripts/aurora-sheets-sync/
├── src/
│   ├── index.ts                    # CLI entry point
│   ├── sync/
│   │   ├── yaml-to-sheet.ts        # Push logic
│   │   └── sheet-to-yaml.ts        # Pull logic (idempotent)
│   └── transformers/
│       └── property-transformer.ts  # YAML ↔ Row conversion
├── credentials/
│   └── service-account.json        # Google credentials (gitignored)
├── CONTEXT.md                      # Technical documentation
└── README.md                       # User guide
```

---

## Resources

- **Technical Context**: See [CONTEXT.md](../../../scripts/aurora-sheets-sync/CONTEXT.md)
- **User Guide**: See [README.md](../../../scripts/aurora-sheets-sync/README.md)
