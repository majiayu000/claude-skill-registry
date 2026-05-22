---
name: uni-google
description: |
  Google Suite via uni CLI. Use when user mentions: calendar, events, schedule, meetings, Gmail, email, Drive, files, Sheets, spreadsheet, Docs, documents, Slides, presentations, Forms, surveys, Meet, video call, Tasks, todos, Contacts.
  Trigger words: calendar, gcal, gmail, email, drive, sheets, docs, slides, forms, meet, tasks, contacts, google.
  Services: gcal, gmail, gdrive, gsheets, gdocs, gslides, gforms, gmeet, gtasks, gcontacts.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Google Suite (uni)

All Google services use OAuth. Run `uni <service> auth` to authenticate.

## Calendar (gcal)

```bash
uni gcal list                           # Today's events
uni gcal list --date tomorrow           # Tomorrow
uni gcal list --days 7                  # Next 7 days
uni gcal add "Meeting" --time 10am --duration 30m
uni gcal add "Lunch" --time 12:30pm --date tomorrow
uni gcal next                           # Next event
uni gcal update "Meeting" --title "Team Sync"
uni gcal delete "Cancelled Meeting"
```

## Tasks (gtasks)

```bash
uni gtasks list                         # Default list
uni gtasks list --completed             # Include completed
uni gtasks add "Buy groceries"
uni gtasks add "Report" --due tomorrow
uni gtasks done "Buy groceries"         # Mark done
uni gtasks delete "Old task"
uni gtasks lists                        # All task lists
```

## Gmail

```bash
uni gmail list                          # Recent emails
uni gmail list --unread                 # Unread only
uni gmail search "flight booking"       # Search
uni gmail read <id-or-query>            # Read email
uni gmail send -t to@email.com -s "Subject" -b "Body"
uni gmail send -t to@email.com -s "Report" --attach file.pdf
uni gmail delete "Newsletter"           # Trash
```

## Drive (gdrive)

```bash
uni gdrive list                         # List files
uni gdrive search "report"              # Search
uni gdrive upload ./file.pdf            # Upload
uni gdrive download <id-or-name>        # Download
uni gdrive share <id> user@email.com    # Share
uni gdrive delete <id>                  # Delete
```

## Sheets (gsheets)

```bash
# Basic operations
uni gsheets list                        # List spreadsheets
uni gsheets get <id>                    # Spreadsheet info
uni gsheets get <id> A1:C10             # Get range data
uni gsheets get <id> --data             # Dump all data
uni gsheets get <id> --data --tsv       # Export as TSV
uni gsheets get <id> A1:D100 --filter "C>100"  # Filter rows
uni gsheets get <id> A1:B10 --json --cells     # Cell-keyed JSON

# Write data
uni gsheets create "Budget 2025"        # Create spreadsheet
uni gsheets set <id> A1 "Hello"         # Set single cell
uni gsheets set <id> A1:C1 "Col1|Col2|Col3"    # Batch write row
uni gsheets set <id> A1:B3 "H1|H2\nV1|V2\nV3|V4"  # Multi-row
uni gsheets append <id> "Name|Age|Email"       # Append row
uni gsheets clear <id> A1:Z100          # Clear range (keeps formatting)

# Sheet management
uni gsheets sheets <id>                 # List sheets/tabs
uni gsheets sheets <id> add "New Tab"   # Add sheet
uni gsheets sheets <id> rename "Old" "New"     # Rename
uni gsheets sheets <id> delete <sheetId>       # Delete sheet
uni gsheets copy <id> "Backup"          # Duplicate sheet

# Sharing
uni gsheets share <id> user@email.com   # Share with user
uni gsheets share <id> anyone           # Public link (editable)
uni gsheets share <id> anyone --role reader    # Public read-only

# Formatting
uni gsheets format <id> A1:B1 --bold    # Bold text
uni gsheets format <id> A1:C10 --bg yellow     # Background color
uni gsheets format <id> A1:Z100 --header-row --alternating  # Auto-format

# Charts
uni gsheets chart <id> B1:B10 --labels A1:A10  # Column chart
uni gsheets chart <id> B1:C20 --labels A1:A20 --type bar --title "Sales"
# Types: bar, line, pie, column

# Comparison formulas
uni gsheets compare <id> A1:B10         # Add % change column
uni gsheets compare <id> A1:B10 --type diff --header "Difference"

# Import data
uni gsheets import <id> data.csv        # Import CSV
uni gsheets import <id> data.tsv --append      # Append TSV
```

## Docs (gdocs)

```bash
uni gdocs list                          # List docs
uni gdocs get <id>                      # Get content
uni gdocs get <id> --text               # Plain text
uni gdocs create "Meeting Notes"        # Create
uni gdocs append <id> "New paragraph"   # Append
uni gdocs export <id> pdf               # Export (pdf/docx/md)
uni gdocs share <id> user@email.com
```

## Slides (gslides)

```bash
uni gslides list                        # List presentations
uni gslides get <id>                    # Get info
uni gslides create "Q1 Review"          # Create
uni gslides add-slide <id>              # Add slide
uni gslides add-text <id> "Hello"       # Add text
uni gslides export <id> pdf             # Export (pdf/pptx)
uni gslides share <id> user@email.com
```

## Forms (gforms)

```bash
uni gforms list                         # List forms
uni gforms get <id>                     # Get questions
uni gforms create "Survey"              # Create
uni gforms add-question <id> "Name" text
uni gforms add-question <id> "Rating" scale --low 1 --high 5
uni gforms responses <id>               # View responses
uni gforms share <id> user@email.com
```

## Meet (gmeet)

```bash
uni gmeet create                        # Instant meeting
uni gmeet create --title "Standup"      # Named
uni gmeet schedule "Sync" --date tomorrow --time 10am
uni gmeet list                          # Upcoming meetings
uni gmeet delete "Team Sync"            # Cancel
```

## Contacts (gcontacts)

```bash
uni gcontacts list                      # List contacts
uni gcontacts search "John"             # Search
uni gcontacts get "John Doe"            # Details
uni gcontacts add "John" --email j@example.com
uni gcontacts delete "Old Contact"
```
