---
name: uni-airtable
description: |
  Airtable bases, tables, and records via uni CLI. Use when user wants to query Airtable data, create/update records, or list bases and tables.
  Requires AIRTABLE_API_KEY (Personal Access Token).
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Airtable (uni)

Manage Airtable bases, tables, and records from the terminal.

## Authentication

```bash
uni airtable auth patXXX.XXXXX                    # Set API key
uni airtable auth patXXX.XXXXX -b appXXXXX        # With default base
uni airtable auth --status                         # Check configuration
uni airtable auth --logout                         # Remove credentials

# Or use environment variable
export AIRTABLE_API_KEY="patXXX.XXXXX"
```

Get your Personal Access Token from: https://airtable.com/create/tokens

## Bases

```bash
uni airtable bases                   # List all accessible bases
```

## Tables

```bash
uni airtable tables appXXXXX         # List tables in base
uni airtable tables appXXXXX --fields  # Show field definitions
```

## Records

```bash
# List records
uni airtable records Tasks -b appXXXXX
uni airtable records tblXXX -b appXXXXX -n 50     # Limit results
uni airtable records tblXXX -b appXXXXX -f "{Status}='Done'"  # Filter

# Get single record
uni airtable records tblXXX get recXXX -b appXXXXX

# Create record
uni airtable records tblXXX create -b appXXXXX -d '{"Name":"New Task","Status":"To Do"}'

# Update record
uni airtable records tblXXX update recXXX -b appXXXXX -d '{"Status":"Done"}'

# Delete record
uni airtable records tblXXX delete recXXX -b appXXXXX
```

## Notes

- Base IDs start with `app`, table IDs with `tbl`, record IDs with `rec`
- Can use table name instead of ID
- Filter uses Airtable formula syntax: `{Field}='Value'`
- JSON data for create/update uses field names as keys
