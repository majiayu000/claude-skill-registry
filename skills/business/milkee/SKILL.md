---
name: milkee
description: "Complete MILKEE accounting integration for Swiss businesses. Manage projects, customers, time tracking, tasks, and products. Use when: (1) tracking billable time with start/stop timers, (2) creating/managing projects and customers, (3) recording work entries with descriptions, (4) viewing daily time summaries, (5) managing tasks and products. Features fuzzy project matching, persistent timer state, auto-calculated hours/minutes, and full CRUD operations. Requires MILKEE_API_TOKEN and MILKEE_COMPANY_ID."
---

# MILKEE Accounting Skill

Swiss accounting platform integration for time tracking, project management, customer relations, tasks, and products.

## Quick Start

See [configuration.md](references/configuration.md) to set up:
- `MILKEE_API_TOKEN` (format: `USER_ID|API_KEY`)
- `MILKEE_COMPANY_ID` (from MILKEE URL)

Then run commands below using `scripts/milkee.py`

## Core Commands

### Time Tracking (Primary Feature)
```bash
# Start timer (auto-matches project name via fuzzy matching)
python3 scripts/milkee.py start_timer "Website" "Implementing authentication module"

# Stop timer (auto-calculates hours/minutes, uploads to MILKEE)
python3 scripts/milkee.py stop_timer

# Show today's time entries
python3 scripts/milkee.py list_times_today
```

### Projects
```bash
python3 scripts/milkee.py list_projects
python3 scripts/milkee.py create_project "My Project" --customer-id 123 --budget 5000
python3 scripts/milkee.py update_project 7478 --name "New Name" --budget 6000
```

### Customers
```bash
python3 scripts/milkee.py list_customers
python3 scripts/milkee.py create_customer "ACME Corp" --city "Zürich"
python3 scripts/milkee.py update_customer 123 --name "ACME AG"
```

### Tasks
```bash
python3 scripts/milkee.py list_tasks --project-id 7478
python3 scripts/milkee.py create_task "Implement Auth" --project-id 7478
python3 scripts/milkee.py update_task 456 --name "Updated Task"
```

### Products
```bash
python3 scripts/milkee.py list_products
python3 scripts/milkee.py create_product "Consulting Hour" --price 150
python3 scripts/milkee.py update_product 789 --price 175
```

## Features

✅ **Smart Fuzzy Matching**: "Milkee" → "Milkee Company AG" (auto-selects closest project)
✅ **Timer Persistence**: State saved to `~/.milkee_timer` between sessions
✅ **Auto-Calculation**: Elapsed time computed to hours/minutes
✅ **Full CRUD**: Projects, customers, tasks, products
✅ **Billable Time Tracking**: Daily summaries with total hours
✅ **No External Dependencies**: Uses Python stdlib only

## How Fuzzy Matching Works

1. User says: `start_timer "website"`
2. Skill fetches all projects from MILKEE
3. Uses Levenshtein distance to find best match
4. Auto-starts timer on highest-scoring project

**Example**: "website" matches "Website Redesign Project" with 96.5% confidence

## Bundled Resources

- **scripts/milkee.py**: CLI tool (300 lines, no dependencies)
- **references/configuration.md**: Setup + troubleshooting
- **references/api-endpoints.md**: Full API reference

See these files for:
- Detailed configuration instructions
- API endpoint documentation
- Error handling guide
- Security best practices

## Official Documentation

For complete API reference, see:
- **MILKEE API Docs**: https://apidocs.milkee.ch/api
- **Projects**: https://apidocs.milkee.ch/api/resources/projects.html
- **Customers**: https://apidocs.milkee.ch/api/resources/customers.html
- **Time Entries**: https://apidocs.milkee.ch/api/resources/times.html
- **Tasks**: https://apidocs.milkee.ch/api/resources/tasks.html
- **Products**: https://apidocs.milkee.ch/api/resources/products.html
- **Authentication**: https://apidocs.milkee.ch/api/authentifizierung.html
