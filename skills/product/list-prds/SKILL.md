---
name: list-prds
description: List all PRDs with status, progress, and metadata
argument-hint: "[--status <status>] [--type <type>]"
---

# list-prds

**Category**: Product & Strategy

## Usage

```bash
list-prds [--status <status>] [--type <type>] [--format <format>]
```

## Arguments

- `--status`: Optional - Filter by status (draft, review, approved, active, complete, archived)
- `--type`: Optional - Filter by type (product, feature, simple)
- `--format`: Optional - Output format (table, list, json). Default: table

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Search for all PRD files in the `product-docs/` directory structure
2. Read the YAML metadata header from each PRD file
3. Extract key information: title, status, version, dates, linked task file
4. If a task file is linked, calculate implementation progress
5. Apply any filters specified in the arguments
6. Format and display the results according to the specified format

## Output Format

### Table Format (default)
```
PRD List - Found 12 PRDs

Status    | Type    | Name                      | Version | Progress | Updated
----------|---------|---------------------------|---------|----------|------------
ACTIVE    | Feature | user-authentication-frd   | 1.2     | 67%      | 2025-01-06
ACTIVE    | Product | inventory-system-prd      | 2.0     | 45%      | 2025-01-05
REVIEW    | Feature | quick-search-simple-frd   | 1.0     | N/A      | 2025-01-04
APPROVED  | Feature | data-export-frd          | 1.1     | 0%       | 2025-01-03
```

### List Format
```
📄 user-authentication-frd.md
   Status: ACTIVE | Version: 1.2 | Progress: 67%
   Location: product-docs/prds/active/feature-prds/
   Tasks: ./tasks/user-authentication-frd-tasks.md

📄 inventory-system-prd.md
   Status: ACTIVE | Version: 2.0 | Progress: 45%
   Location: product-docs/prds/active/product-prds/
   Tasks: ./tasks/inventory-system-prd-tasks.md
```

## Error Handling

- If no `product-docs/` directory exists: Create it with proper structure
- If PRD has no metadata: Show with status "UNKNOWN"
- If linked task file not found: Show progress as "N/A"

## Example

```bash
# List all PRDs
list-prds

# List only active PRDs
list-prds --status active

# List only feature PRDs in list format
list-prds --type feature --format list

# List all PRDs in review status
list-prds --status review
```

## Implementation Tips for Claude Code

1. **Directory Traversal**: Use recursive search through all PRD directories
2. **Metadata Parsing**: Use YAML parsing for the header between `---` markers
3. **Progress Calculation**: Count `[x]` vs `[ ]` in linked task files
4. **Sorting**: Default sort by status (active first) then by last updated date
5. **Type Detection**: Infer from filename suffix (-prd, -frd, -simple-frd)
