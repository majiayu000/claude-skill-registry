---
name: automating-reminders
description: Automates Apple Reminders using JavaScript for Automation (JXA). Use when asked to "create reminders programmatically", "automate reminder lists", "JXA Reminders scripting", or "manage reminders via automation". Covers list/reminder management, filtering with 'whose' queries, efficient creation via constructors and push operations, and copy-delete patterns for moving items.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Reminders (JXA-first, AppleScript discovery)

## Relationship to the macOS automation skill
- Standalone for Reminders; reuse `automating-mac-apps` for permissions, shell helpers, and ObjC debugging patterns.
- **PyXA Installation:** To use PyXA examples in this skill, see the installation instructions in `automating-mac-apps` skill (PyXA Installation section).

## Core Framing
Reminders works like a database: everything is accessed via specifiers (references to objects). Start by exploring the Reminders dictionary in Script Editor (switch to JavaScript view). Read properties with methods like `name()` or `id()`; write with assignments. Use `.whose` for efficient server-side filtering to minimize performance overhead. For creation, use constructors + `.push()` instead of `make` to avoid errors. Note: no native `move` command—use copy-delete instead. Priority: 1 (high), 5 (medium), 9 (low), 0 (none). Recurrence/location scripting is limited; use Shortcuts for advanced features.

## Quickstart (create + alerts)
First, ensure Reminders permissions are granted (see `automating-mac-apps` for setup).

**JXA:**
```javascript
try {
  const app = Application("Reminders");

  // Get list by name, or fall back to first available list
  let list;
  try {
    list = app.lists.byName("Reminders");
    list.name(); // Verify it exists
  } catch (e) {
    // Fall back to first available list
    const lists = app.lists();
    if (lists.length === 0) {
      throw new Error("No reminder lists found");
    }
    list = lists[0];
  }

  const r = app.Reminder({
    name: "Prepare deck",
    body: "Client review",
    dueDate: new Date(Date.now() + 3*86400*1000), // 3 days from now
    remindMeDate: new Date(Date.now() + 2*86400*1000), // Reminder 1 day before due
    priority: 1 // High priority
  });
  list.reminders.push(r);
  console.log("Reminder created in '" + list.name() + "'");
} catch (error) {
  console.error("Failed to create reminder: " + error.message);
  // Common errors: Permissions denied, list not found
}
```

> **Note:** The list name varies by system. Common names include "Reminders", "Inbox", or localized versions. Using `app.lists()[0]` as a fallback ensures the script works across different configurations.

**PyXA (Recommended Modern Approach):**
```python
import PyXA
from datetime import datetime, timedelta

try:
    reminders = PyXA.Reminders()

    # Get Inbox list
    inbox = reminders.lists().by_name("Inbox")

    # Create reminder with due date and reminder alert
    reminder = inbox.reminders().push({
        "name": "Prepare deck",
        "body": "Client review",
        "due_date": datetime.now() + timedelta(days=3),
        "remind_me_date": datetime.now() + timedelta(days=2),
        "priority": 1  # High priority
    })

    print("Reminder created successfully")

except Exception as error:
    print(f"Failed to create reminder: {error}")
    # Common errors: Permissions denied, Inbox list not found
```

**PyObjC with Scripting Bridge:**
```python
from ScriptingBridge import SBApplication
from Foundation import NSDate

try:
    reminders = SBApplication.applicationWithBundleIdentifier_("com.apple.Reminders")

    # Get Inbox list
    lists = reminders.lists()
    inbox = None
    for lst in lists:
        if lst.name() == "Inbox":
            inbox = lst
            break

    if inbox:
        # Create reminder
        reminder = reminders.classForScriptingClass_("reminder").alloc().init()
        reminder.setName_("Prepare deck")
        reminder.setBody_("Client review")

        # Set due date (3 days from now)
        due_date = NSDate.dateWithTimeIntervalSinceNow_(3 * 24 * 60 * 60)
        reminder.setDueDate_(due_date)

        # Set reminder date (2 days from now)
        remind_date = NSDate.dateWithTimeIntervalSinceNow_(2 * 24 * 60 * 60)
        reminder.setRemindMeDate_(remind_date)

        reminder.setPriority_(1)  # High priority

        # Add to inbox
        inbox.reminders().addObject_(reminder)

        print("Reminder created successfully")
    else:
        print("Inbox list not found")

except Exception as error:
    print(f"Failed to create reminder: {error}")
```

## Workflow (default)
1) **Discover**: Open Script Editor, view Reminders dictionary in JavaScript mode to learn available properties.
2) **Target List**: Get your list by name (e.g., `app.lists.byName('Work')`) or ID.
3) **Filter**: Use `.whose` for queries (e.g., `reminders.whose({name: {_contains: 'meeting'}})`). For dates, use `_lessThan`/`_greaterThan`.
4) **Create**: Build with `Reminder({...})` then add via `.push()` to avoid errors.
5) **Batch Operations**: Collect IDs before changes, update/delete in batches.
6) **Move**: Copy item to new list, then delete original (no native move).
7) **Advanced Features**: For recurrence/location, call Shortcuts or clone template item.

**Example: Filter overdue reminders:**
```javascript
const overdue = list.reminders.whose({dueDate: {_lessThan: new Date()}})();
```

## Validation Checklist
After implementing Reminders automation:
- [ ] Verify Reminders permissions granted
- [ ] Test list access: `app.lists().length > 0`
- [ ] Confirm reminder creation with valid dates
- [ ] Check reminder appears in Reminders UI
- [ ] Validate `.whose` queries return expected results

## Common Pitfalls
- **Permission errors**: Grant Reminders access in System Preferences > Security & Privacy.
- **-10024 errors**: Use constructor + push instead of make.
- **Invalid dates**: Validate before assignment.
- **Missing lists**: Check existence with `app.lists.byName(name)` before use.

## When Not to Use
- For cross-platform task management (use Todoist API or similar)
- When complex recurrence patterns are needed (limited JXA support; use Shortcuts)
- For non-macOS platforms
- When location-based reminders require programmatic setup (use Shortcuts)

## What to Load
Load progressively as needed:
- **Basics**: Start with `automating-reminders/references/reminders-basics.md` for specifiers and simple operations.
- **Recipes**: Add `automating-reminders/references/reminders-recipes.md` for practical create/query/batch examples.
- **Advanced**: For complex scenarios, load `automating-reminders/references/reminders-advanced.md` (priority, limits, debugging).
- **Dictionary**: Reference `automating-reminders/references/reminders-dictionary.md` for full type mappings.
- **PyXA API Reference** (complete class/method docs): `automating-reminders/references/reminders-pyxa-api-reference.md`