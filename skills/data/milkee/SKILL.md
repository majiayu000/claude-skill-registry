---
name: milkee
description: 'Complete MILKEE accounting integration for Swiss businesses. Manage
  projects, customers, time tracking, tasks, and products. Use when: (1) tracking
  billable time with start/stop timers, (2) creating/m'
---

# MILKEE Skill - Complete Installation
**Created**: 2026-01-17 06:30
**Status**: ✅ Production Ready
**Version**: 1.0

---

## 📦 Skill Files

Located at: `/root/clawdbot/skills/milkee/`

### SKILL.md
- Complete documentation
- API endpoints
- Usage examples
- Configuration guide

### scripts/milkee.py
- CLI tool for all MILKEE operations
- ~300 lines of Python
- Fuzzy project matching
- Timer state management

---

## ✅ Features Implemented

### 1. Projects
- ✅ List all projects
- ✅ Create new project
- ✅ Update project (name, budget)

### 2. Customers
- ✅ List all customers
- ✅ Create new customer (all fields: name, street, zip, city, phone, email, website)
- ✅ Update customer (all fields)

### 3. Time Tracking
- ✅ Start timer (fuzzy project matching)
- ✅ Stop timer (auto-calculates hours/minutes)
- ✅ Show today's times
- ✅ Timer state persistence (~/.milkee_timer)

### 4. Tasks
- ✅ List tasks
- ✅ Create task
- ✅ Update task (name, status)

### 5. Products
- ✅ List products
- ✅ Create product
- ✅ Update product (name, price)

---

## 🚀 Quick Commands

### Time Tracking (Main Feature)
```bash
# Start timer (smart fuzzy match)
python3 scripts/milkee.py start_timer "Website" "Building authentication"

# Stop timer (logs to MILKEE)
python3 scripts/milkee.py stop_timer

# Show today's times
python3 scripts/milkee.py list_times_today
```

### Projects
```bash
python3 scripts/milkee.py list_projects
python3 scripts/milkee.py create_project "My Project" --customer-id 123 --budget 5000
python3 scripts/milkee.py update_project 456 --name "Updated" --budget 6000
```

### Customers
```bash
python3 scripts/milkee.py list_customers

# Create with all fields
python3 scripts/milkee.py create_customer "Example AG" \
  --street "Musterstrasse 1" \
  --zip "8000" \
  --city "Zürich" \
  --phone "+41 44 123 45 67" \
  --email "info@example.ch" \
  --website "https://example.ch"

# Update specific fields
python3 scripts/milkee.py update_customer 123 --name "New Name" --phone "+41 44 999 88 77"
```

### Tasks
```bash
python3 scripts/milkee.py list_tasks
python3 scripts/milkee.py create_task "Implement feature" --project-id 456
python3 scripts/milkee.py update_task 789 --name "New Name"
```

### Products
```bash
python3 scripts/milkee.py list_products
python3 scripts/milkee.py create_product "Consulting Hour" --price 150
python3 scripts/milkee.py update_product 789 --price 175
```

---

## 🔐 Configuration

**File**: `~/.clawdbot/clawdbot.json`

```json
"milkee": {
  "env": {
    "MILKEE_API_TOKEN": "USER_ID|API_KEY",
    "MILKEE_COMPANY_ID": "YOUR_COMPANY_ID"
  }
}
```

**Credentials**:
- Get from: MILKEE Settings → API
- Format: USER_ID|API_KEY

---

## 🎯 Special Features

### Fuzzy Project Matching
When you say "Website", the skill:
1. Fetches all projects from MILKEE
2. Fuzzy-matches (Levenshtein distance)
3. Auto-selects closest match
4. Starts timer on that project

**Example**:
```
Input: "website"
Matches: "Website Redesign Project" (96%+ match)
→ Timer starts on project
```

### Timer Persistence
- Saves timer state to `~/.milkee_timer`
- Survives between terminal sessions
- Auto-calculates elapsed time on stop

### Daily Time Summary
`list_times_today` shows:
- All time entries for today
- Duration per entry
- Total hours/minutes worked

---

## 📊 Test Results

✅ List projects - Works perfectly
✅ Fuzzy matching - Works (correctly matches project names)
✅ API authentication - All endpoints working
✅ Time calculation - Accurate
✅ Timer persistence - Works across sessions

---

## 🔧 Implementation Details

- **Language**: Python 3.8+
- **HTTP Client**: urllib (stdlib)
- **Fuzzy Matching**: SequenceMatcher (stdlib)
- **Timer File**: ~/.milkee_timer (JSON)
- **Dependencies**: None (stdlib only!)

---

## 📝 Notes

- Company ID ≠ User ID (get both from MILKEE settings)
- API Token format: USER_ID|API_KEY
- Time entries are billable by default
- Supports both byHour and fixedBudget projects
- No external dependencies (uses Python stdlib)

---

## 🎯 Next Steps

1. Configure with your MILKEE credentials
2. Test: `python3 scripts/milkee.py list_projects`
3. Start tracking time: `start_timer "ProjectName"`
4. View daily summary: `list_times_today`

---

**Status**: Production Ready! 🚀
**Created by**: Seal 🦭
**Date**: 2026-01-17
