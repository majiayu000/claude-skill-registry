---
name: frappe-impl-ui-components
description: >
  Use when building custom dialogs, extending List View, creating Page controllers, or adding Kanban/Calendar views and realtime updates.
  Prevents UI freezes from synchronous calls, broken dialogs from wrong field definitions, and missed socket events.
  Covers frappe.ui.Dialog, frappe.ui.form.MultiSelectDialog, List View customization, frappe.pages, Kanban Board, Calendar View, frappe.realtime, socket.io publish/subscribe.
  Keywords: Dialog, List View, Page, Kanban, Calendar, realtime, socket.io, frappe.ui, MultiSelectDialog, publish_realtime.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe UI Components & Realtime — Implementation Workflows

Step-by-step workflows for building client-side UI. For form scripting see `frappe-impl-clientscripts`. For server-side API see `frappe-syntax-serverscripts`.

**Version**: v14/v15/v16 | **Note**: v15+ uses Bootstrap 5; Dialog API is stable across all versions.

## Quick Decision: Which UI Component?

```
WHAT do you need?
├── Prompt user for input         → frappe.prompt (simple) or frappe.ui.Dialog (complex)
├── Show a message/alert          → frappe.msgprint / frappe.show_alert / frappe.throw
├── Confirm an action             → frappe.confirm
├── Multi-field data entry popup  → frappe.ui.Dialog with fields
├── Select from a list of records → frappe.ui.form.MultiSelectDialog
├── Full custom page (not a form) → frappe.ui.Page
├── Customize list columns/colors → frappe.listview_settings
├── Visual board for workflow     → Kanban Board (Select field based)
├── Date-based record view        → Calendar View ({doctype}_calendar.js)
├── Hierarchical data display     → Tree View (is_tree DocType)
├── Live updates without refresh  → frappe.publish_realtime + frappe.realtime.on
├── Show background job progress  → frappe.publish_progress
├── Scan barcode/QR code          → frappe.ui.Scanner
└── Custom cell formatting        → formatters in listview_settings or form
```

See `references/decision-tree.md` for the complete decision tree.

## Workflow 1: Dialogs (frappe.ui.Dialog)

### Simple Dialog

```javascript
let d = new frappe.ui.Dialog({
    title: "Enter Details",
    fields: [
        { label: "Full Name", fieldname: "full_name", fieldtype: "Data", reqd: 1 },
        { label: "Email", fieldname: "email", fieldtype: "Data", options: "Email" },
        { label: "Role", fieldname: "role", fieldtype: "Select",
          options: "Developer\nManager\nDesigner" },
    ],
    size: "small",  // "small", "large", or "extra-large"
    primary_action_label: "Create",
    primary_action(values) {
        frappe.call({
            method: "myapp.api.create_user",
            args: values,
            callback(r) {
                if (!r.exc) {
                    frappe.show_alert({ message: "User created", indicator: "green" });
                    d.hide();
                }
            }
        });
    }
});
d.show();
```

**Rule**: ALWAYS call `d.hide()` inside the callback, NEVER before the async call completes.

### Dialog with Table Field

```javascript
let d = new frappe.ui.Dialog({
    title: "Add Items",
    fields: [
        { label: "Customer", fieldname: "customer", fieldtype: "Link",
          options: "Customer", reqd: 1 },
        { fieldtype: "Section Break" },
        { label: "Items", fieldname: "items", fieldtype: "Table",
          in_place_edit: true, reqd: 1,
          fields: [
              { fieldname: "item", label: "Item", fieldtype: "Link",
                options: "Item", in_list_view: 1, reqd: 1 },
              { fieldname: "qty", label: "Qty", fieldtype: "Int",
                in_list_view: 1, default: 1 },
              { fieldname: "rate", label: "Rate", fieldtype: "Currency",
                in_list_view: 1 },
          ],
        },
    ],
    primary_action_label: "Submit",
    primary_action(values) {
        console.log(values);  // { customer: "...", items: [{item, qty, rate}] }
        d.hide();
    }
});
d.show();
```

**Rule**: ALWAYS set `in_list_view: 1` on table child fields you want visible. Fields without it are hidden in the grid.

### Multi-Step Dialog

```javascript
let d = new frappe.ui.Dialog({
    title: "Setup Wizard",
    fields: [
        // Page 1
        { fieldtype: "Section Break", label: "Step 1: Basic Info",
          collapsible: 0 },
        { label: "Name", fieldname: "name", fieldtype: "Data", reqd: 1 },
        // Page 2
        { fieldtype: "Section Break", label: "Step 2: Configuration",
          collapsible: 0 },
        { label: "Option", fieldname: "option", fieldtype: "Select",
          options: "A\nB\nC" },
    ],
    primary_action_label: "Finish",
    primary_action(values) {
        d.hide();
    }
});
d.show();
```

### Key Dialog Methods

| Method | Purpose |
|--------|---------|
| `d.show()` | Display the dialog |
| `d.hide()` | Close the dialog |
| `d.get_values()` | Get all field values as object |
| `d.set_values({field: val})` | Set field values |
| `d.get_field("name")` | Get a specific field control |
| `d.set_df_property("name", "hidden", 1)` | Show/hide fields dynamically |
| `d.disable_primary_action()` | Grey out submit button |
| `d.enable_primary_action()` | Re-enable submit button |

## Workflow 2: Messages & Alerts

### frappe.msgprint — Modal Message

```javascript
// Simple message
frappe.msgprint("Record saved successfully");

// With options
frappe.msgprint({
    title: "Warning",
    message: "This action cannot be undone",
    indicator: "orange",     // green, blue, orange, red
    primary_action: {
        label: "Proceed",
        action() { do_something(); }
    }
});

// List of messages
frappe.msgprint({
    title: "Validation Errors",
    message: "Please fix the following:",
    as_list: true,
    indicator: "red",
});
```

### frappe.throw — Error with Exception

```javascript
// Client-side: shows msgprint and stops execution
frappe.throw("Amount cannot be negative");
```

```python
# Server-side: raises ValidationError, shown as red msgprint
frappe.throw("Amount cannot be negative")
frappe.throw("Not Permitted", frappe.PermissionError)  # specific exception
```

**Rule**: ALWAYS use `frappe.throw` for validation errors. NEVER use `frappe.msgprint` for errors — it does not stop execution.

### frappe.confirm — Yes/No Dialog

```javascript
frappe.confirm(
    "Are you sure you want to delete this record?",
    () => { /* Yes callback */ delete_record(); },
    () => { /* No callback (optional) */ }
);
```

### frappe.prompt — Quick Single-Field Input

```javascript
frappe.prompt(
    { label: "Reason", fieldname: "reason", fieldtype: "Small Text", reqd: 1 },
    (values) => {
        console.log(values.reason);
    },
    "Enter Reason",    // dialog title
    "Submit"           // primary action label
);

// Multiple fields
frappe.prompt([
    { label: "Reason", fieldname: "reason", fieldtype: "Small Text", reqd: 1 },
    { label: "Priority", fieldname: "priority", fieldtype: "Select",
      options: "Low\nMedium\nHigh" },
], (values) => { console.log(values); }, "Details");
```

### frappe.show_alert — Toast Notification

```javascript
// Simple
frappe.show_alert("Saved");

// With indicator and duration
frappe.show_alert({ message: "Email sent", indicator: "green" }, 5);
// Duration in seconds (default: 7)
```

**Rule**: Use `frappe.show_alert` for non-blocking success messages. Use `frappe.msgprint` when the user MUST acknowledge.

## Workflow 3: List View Customization

Create `{doctype_name}_list.js` in the DocType directory:

```javascript
// myapp/doctype/task/task_list.js
frappe.listview_settings["Task"] = {
    // Extra fields to fetch (beyond standard)
    add_fields: ["priority", "status", "assigned_to"],

    // Hide the name column
    hide_name_column: true,

    // Row indicator (colored dot)
    get_indicator(doc) {
        // MUST return [label, color, comma-separated-filter]
        if (doc.status === "Completed") return ["Completed", "green", "status,=,Completed"];
        if (doc.status === "Overdue") return ["Overdue", "red", "status,=,Overdue"];
        return ["Open", "orange", "status,=,Open"];
    },

    // Custom column formatters
    formatters: {
        priority(val) {
            const colors = { High: "red", Medium: "orange", Low: "green" };
            return `<span class="indicator-pill ${colors[val] || ""}">${val}</span>`;
        }
    },

    // Row action button
    button: {
        show(doc) { return doc.status === "Open"; },
        get_label() { return __("Complete"); },
        get_description(doc) { return __("Mark {0} as complete", [doc.name]); },
        action(doc) {
            frappe.xcall("myapp.api.complete_task", { task: doc.name })
                .then(() => cur_list.refresh());
        }
    },

    // Lifecycle hooks
    onload(listview) {
        listview.page.add_inner_button("Export", () => export_tasks());
    },

    refresh(listview) {
        // Runs on every list refresh
    },

    // Default filters
    filters: [["status", "!=", "Cancelled"]],
};
```

**Rule**: ALWAYS return a 3-element array from `get_indicator`. The third element is the filter string for click-to-filter.

## Workflow 4: Custom Page (frappe.ui.Page)

### Step 1: Register in hooks.py

```python
# hooks.py
page_js = { "my-custom-page": "public/js/my_custom_page.js" }
```

### Step 2: Create page definition

```javascript
// myapp/myapp/my_custom_page/my_custom_page.js
frappe.pages["my-custom-page"].on_page_load = function(wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: "My Custom Page",
        single_column: true,
    });

    // Primary action button
    page.set_primary_action("Create", () => create_new(), "octicon octicon-plus");

    // Secondary action
    page.set_secondary_action("Refresh", () => refresh_data());

    // Dropdown menu
    page.add_menu_item("Export CSV", () => export_csv());
    page.add_menu_item("Settings", () => frappe.set_route("Form", "My Settings"));

    // Inner toolbar buttons
    page.add_inner_button("Update All", () => update_all());
    page.add_inner_button("New Post", () => new_post(), "Make");  // grouped

    // Toolbar filter fields
    let status_field = page.add_field({
        label: "Status",
        fieldtype: "Select",
        fieldname: "status",
        options: ["", "Open", "Closed", "Cancelled"],
        change() { refresh_data(); }
    });

    // Status indicator
    page.set_indicator("Active", "green");

    // Content area
    $(page.body).html(`<div class="my-page-content"></div>`);

    // Load initial data
    refresh_data();
};
```

### Key Page Methods

| Method | Purpose |
|--------|---------|
| `page.set_title(title)` | Set page heading |
| `page.set_indicator(label, color)` | Status badge (green/red/orange/blue) |
| `page.set_primary_action(label, fn, icon)` | Main action button |
| `page.set_secondary_action(label, fn)` | Secondary button |
| `page.add_menu_item(label, fn)` | Dropdown menu entry |
| `page.add_inner_button(label, fn, group)` | Toolbar button (optional group) |
| `page.add_field({...})` | Add filter/input to toolbar |
| `page.get_form_values()` | Get all toolbar field values |
| `page.clear_fields()` | Remove all toolbar fields |
| `page.clear_primary_action()` | Remove primary button |

## Workflow 5: Calendar View

Create `{doctype}_calendar.js` in the DocType directory:

```javascript
// myapp/doctype/event/event_calendar.js
frappe.views.calendar["Event"] = {
    field_map: {
        start: "starts_on",
        end: "ends_on",
        id: "name",
        title: "subject",
        allDay: "all_day",
        color: "color",
    },
    gantt: true,  // Enable Gantt view toggle
    get_events_method: "myapp.api.get_events",  // Optional custom event source
    filters: [
        { fieldtype: "Link", fieldname: "event_type", label: "Type",
          options: "Event Type" }
    ],
};
```

**Rule**: ALWAYS map `start` and `end` to actual Date or Datetime fields on the DocType. Missing mappings cause blank calendars.

## Workflow 6: Kanban Board

Kanban boards work on any DocType with a **Select** field. No code needed:

1. Open List View → sidebar → **Kanban** → **New Kanban Board**
2. Select the **Select field** (e.g., `status`) — options become columns
3. Save — cards are draggable between columns

**Rule**: NEVER create Kanban boards for DocTypes without a Select field. See `references/examples.md` for programmatic configuration.

## Workflow 7: Realtime Updates (Socket.IO)

### Server: Publish Events

```python
# Broadcast to all users
frappe.publish_realtime("task_updated", {"task": task.name, "status": "Done"})

# Send to specific user
frappe.publish_realtime("notification", {"msg": "Your report is ready"},
    user="admin@example.com")

# Send to users viewing a specific document
frappe.publish_realtime("doc_updated", {"field": "status"},
    doctype="Task", docname="TASK-001")

# ALWAYS use after_commit=True in document events
frappe.publish_realtime("order_created", message, after_commit=True)
```

### Client: Subscribe to Events

```javascript
// Listen for events
frappe.realtime.on("task_updated", (data) => {
    frappe.show_alert({ message: `Task ${data.task}: ${data.status}`, indicator: "green" });
    cur_list && cur_list.refresh();
});

// Stop listening
frappe.realtime.off("task_updated");
```

### Progress Indicator

```python
# Server: publish progress during long operations
def process_items(items):
    total = len(items)
    for i, item in enumerate(items):
        process(item)
        frappe.publish_progress(
            percent=(i + 1) / total * 100,
            title="Processing Items",
            description=f"Processing {item.name}",
        )
```

**Rule**: ALWAYS use `after_commit=True` when publishing from document events. Without it, the event fires even if the transaction rolls back.

### Realtime Rooms

| Room | Audience | Use Case |
|------|----------|----------|
| (default) | All System Users | Global notifications |
| `user:{email}` | Single user | Personal alerts |
| `doctype:{dt}` | Users viewing list | List refresh triggers |
| `doc:{dt}/{name}` | Users viewing document | Document change alerts |
| `website` | All users including guests | Public announcements |

## Workflow 8: Scanner API (Barcode/QR)

```javascript
// Single scan — closes after first scan
new frappe.ui.Scanner({
    dialog: true, multiple: false,
    on_scan(data) {
        frappe.set_route("Form", "Item", data.decodedText);
    }
});

// Continuous scanning — stays open for multiple scans
let scanner = new frappe.ui.Scanner({
    dialog: true, multiple: true,
    on_scan(data) { add_item_to_list(data.decodedText); }
});
// Stop: scanner.stop_scan() or close the dialog
```

**Rule**: ALWAYS set `multiple: false` for single-item lookups. See `references/examples.md` for a full barcode-in-Stock-Entry example.

## Anti-Patterns Summary

| Anti-Pattern | Correct Approach |
|---|---|
| `frappe.msgprint` for errors | Use `frappe.throw` — it stops execution |
| Hiding dialog before async completes | Hide in the callback: `callback() { d.hide(); }` |
| Synchronous API calls in dialogs | ALWAYS use `frappe.call` / `frappe.xcall` (async) |
| Missing `in_list_view` on table fields | Set `in_list_view: 1` on visible columns |
| `publish_realtime` without `after_commit` | ALWAYS use `after_commit=True` in doc events |
| Kanban on DocType without Select field | Kanban requires a Select field for columns |
| Missing start/end in calendar field_map | ALWAYS map both `start` and `end` fields |
| 2-element array from get_indicator | ALWAYS return 3 elements: [label, color, filter] |

## Reference Files

- `references/controls-api.md` — Standalone controls via `frappe.ui.form.make_control()`, full control type reference, control methods and events
- `references/tree-view.md` — Tree DocType configuration, `frappe.views.TreeView` API, `frappe.ui.Tree` low-level API, tree node operations
- `references/workflows.md` — Extended workflow walkthroughs
- `references/examples.md` — Complete code examples
- `references/decision-tree.md` — Full UI component decision tree
- `references/anti-patterns.md` — Expanded anti-patterns with code examples

## See Also

- `frappe-impl-clientscripts` — Form-level client scripts
- `frappe-syntax-clientscripts` — Client-side API syntax reference
- `frappe-impl-hooks` — Hook registration for pages and routes
