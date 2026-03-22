---
name: frappe-syntax-clientscripts
description: >
  Use when writing client-side JavaScript for ERPNext/Frappe form events,
  field manipulation, server calls, or child table handling in v14/v15/v16.
  Covers exact syntax for frappe.ui.form.on, frm methods, frappe.call,
  and browser-side validation. Keywords: client script, form event, frm,
  frappe.call, frappe.ui.form.on, JavaScript, UI interaction, field validation.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Client Scripts Syntax

Client Scripts run in the browser and control all UI interactions in Frappe/ERPNext. Create them via **Setup > Client Script** or in custom apps under `public/js/`.

**CRITICAL**: Client Script validations ONLY apply in the browser form view. API calls and System Console bypass them. ALWAYS pair with Server Scripts for security-critical validation.

## Quick Reference

| Action | Code |
|--------|------|
| Set value | `frm.set_value('field', value)` |
| Get value | `frm.doc.fieldname` |
| Hide field | `frm.toggle_display('field', false)` |
| Make mandatory | `frm.toggle_reqd('field', true)` |
| Make read-only | `frm.toggle_enable('field', false)` |
| Set field property | `frm.set_df_property('field', 'options', [...])` |
| Filter Link field | `frm.set_query('field', () => ({filters: {}}))` |
| Call server | `frappe.call({method: 'path.to.fn', args: {}})` |
| Call doc method | `frm.call('method_name', {args})` |
| Prevent save | `frappe.throw(__('Error message'))` |
| Add button | `frm.add_custom_button(__('Label'), callback, group)` |
| Add child row | `frm.add_child('table', {values}); frm.refresh_field('table')` |
| Show alert | `frappe.show_alert({message: __('Done'), indicator: 'green'})` |
| Translate string | `__('Text')` or `__('Hello {0}', [name])` |

## Event Decision Tree

```
What do you need to do?
│
├─ One-time setup (queries, formatters)?
│  └─ ALWAYS use setup — runs once per form instance
│
├─ Show/hide fields, add buttons, update UI?
│  └─ ALWAYS use refresh — fires after every load/reload
│
├─ Validate data before save?
│  └─ ALWAYS use validate — use frappe.throw() to block save
│
├─ Modify data right before server save?
│  └─ Use before_save — last chance to change values
│
├─ Run logic after successful save?
│  └─ Use after_save — document is persisted
│
├─ React to a field value change?
│  └─ Use the fieldname as the event name
│
├─ Intercept workflow state change?
│  └─ Use before_workflow_action / after_workflow_action
│
└─ Manipulate DOM after full render?
   └─ Use onload_post_render — NEVER use jQuery selectors directly
```

> See [references/events.md](references/events.md) for complete event list and execution order.

## Form Event Registration

```javascript
// Parent form events
frappe.ui.form.on('Sales Order', {
    setup(frm) { },           // Once per form instance
    refresh(frm) { },         // After every load/reload
    validate(frm) { },        // Before save — throw to block
    fieldname(frm) { }        // On field value change
});

// Child table events — ALWAYS register on the CHILD doctype
frappe.ui.form.on('Sales Order Item', {
    qty(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate);
    },
    items_add(frm, cdt, cdn) { },     // Row added
    items_remove(frm) { },            // Row removed (no cdt/cdn)
    items_move(frm) { }               // Row reordered
});
```

## Value Manipulation

```javascript
// ALWAYS use frm.set_value() — NEVER assign frm.doc.field directly
frm.set_value('status', 'Approved');                        // Single
frm.set_value({status: 'Approved', priority: 'High'});      // Multiple

// Read values (read-only — NEVER write via frm.doc)
let val = frm.doc.fieldname;
let items = frm.doc.items;  // Child table array
```

## Field Properties

```javascript
// Show/hide (accepts single field or array)
frm.toggle_display(['priority', 'due_date'], frm.doc.status === 'Open');

// Mandatory toggle
frm.toggle_reqd('due_date', true);

// Read-only toggle
frm.toggle_enable('amount', false);  // false = read-only

// Arbitrary property change
frm.set_df_property('status', 'options', ['New', 'Open', 'Closed']);
frm.set_df_property('amount', 'read_only', 1);
frm.set_df_property('notes', 'label', 'Internal Notes');

// Intro message at form top
frm.set_intro('This document is pending review', 'orange');
```

## Link Field Filters

```javascript
// ALWAYS set queries in setup event — NEVER in refresh
frappe.ui.form.on('Sales Order', {
    setup(frm) {
        // Simple filter
        frm.set_query('customer', () => ({
            filters: { disabled: 0 }
        }));

        // Child table filter
        frm.set_query('item_code', 'items', (doc, cdt, cdn) => {
            let row = locals[cdt][cdn];
            return { filters: { is_sales_item: 1 } };
        });

        // Server-side query for complex logic
        frm.set_query('customer', () => ({
            query: 'myapp.queries.get_filtered_customers',
            filters: { region: frm.doc.region }
        }));
    }
});
```

## Server Communication

```javascript
// frappe.call — whitelisted Python method
let r = await frappe.call({
    method: 'myapp.api.process_data',
    args: { customer: frm.doc.customer },
    freeze: true,
    freeze_message: __('Processing...')
});
if (r.message) { /* use r.message */ }

// frm.call — document controller method
let result = await frm.call('calculate_taxes', { include_shipping: true });

// frappe.db shortcuts
let val = await frappe.db.get_value('Customer', name, 'credit_limit');
let list = await frappe.db.get_list('Sales Order', {
    filters: { customer: frm.doc.customer },
    fields: ['name', 'grand_total'],
    order_by: 'creation desc',
    limit: 10
});
```

## Child Table Operations

```javascript
// Add row — ALWAYS call refresh_field after
let row = frm.add_child('items', { item_code: 'ITEM-001', qty: 5 });
frm.refresh_field('items');

// Clear all rows
frm.clear_table('items');
frm.refresh_field('items');

// Modify existing rows — refresh_field ONCE after loop
frm.doc.items.forEach(row => {
    row.discount = row.qty > 10 ? 5 : 0;
});
frm.refresh_field('items');

// Set child row value (inside child event handler)
frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate);

// Mark form dirty after programmatic changes
frm.dirty();
```

## Custom Buttons

```javascript
refresh(frm) {
    if (frm.doc.docstatus === 1) {
        // Grouped dropdown
        frm.add_custom_button(__('Invoice'), () => {
            frappe.model.open_mapped_doc({
                method: 'erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice',
                frm: frm
            });
        }, __('Create'));

        // Primary action
        frm.page.set_primary_action(__('Process'), () => {
            frm.call('process').then(() => frm.reload_doc());
        });
    }

    // ALWAYS guard buttons with state checks
    if (!frm.is_new() && frm.doc.docstatus === 0) {
        frm.add_custom_button(__('Validate'), () => { /* ... */ });
    }
}
```

## List View Customization

```javascript
frappe.listview_settings['Task'] = {
    add_fields: ['status', 'priority'],
    filters: [['status', '!=', 'Cancelled']],
    hide_name_column: true,

    get_indicator(doc) {
        // ALWAYS return [label, color, filter_field + ',' + filter_value]
        if (doc.status === 'Open') return [__('Open'), 'orange', 'status,=,Open'];
        if (doc.status === 'Closed') return [__('Closed'), 'green', 'status,=,Closed'];
    },

    button: {
        show(doc) { return doc.status === 'Open'; },
        get_label() { return __('Close'); },
        action(doc) { frappe.call({method: 'myapp.api.close', args: {name: doc.name}}); }
    },

    formatters: {
        priority(val) { return val === 'High' ? `<b>${val}</b>` : val; }
    },

    onload(listview) { /* runs once */ },
    refresh(listview) { /* runs on every refresh */ }
};
```

## Dialogs and Prompts

```javascript
// Quick prompt
frappe.prompt({label: 'Reason', fieldname: 'reason', fieldtype: 'Data'},
    (values) => { console.log(values.reason); },
    __('Enter Reason')
);

// Full dialog
let d = new frappe.ui.Dialog({
    title: __('Enter Details'),
    fields: [
        {label: 'Name', fieldname: 'name', fieldtype: 'Data', reqd: 1},
        {label: 'Date', fieldname: 'date', fieldtype: 'Date'}
    ],
    size: 'small',
    primary_action_label: __('Submit'),
    primary_action(values) { d.hide(); /* use values */ }
});
d.show();

// Progress indicator
frappe.show_progress(__('Importing'), 45, 100, __('Please wait'));
```

## Critical Rules

1. **ALWAYS** call `frm.refresh_field('table')` after ANY child table modification
2. **NEVER** assign `frm.doc.field = value` — ALWAYS use `frm.set_value()`
3. **ALWAYS** use `__('text')` for every user-facing string
4. **ALWAYS** place `set_query` in `setup` — NEVER in `refresh`
5. **NEVER** use `async: false` — it freezes the browser
6. **ALWAYS** check `frm.is_new()` before adding action buttons
7. **NEVER** use direct jQuery selectors for field manipulation — use Frappe API
8. **NEVER** store state in global variables — attach to `frm` object instead
9. **ALWAYS** check `r.message` before using server call responses
10. **ALWAYS** use `frappe.throw()` inside `validate` to block save — NEVER `return false` in async handlers

> See [references/methods.md](references/methods.md) for complete API reference.
> See [references/examples.md](references/examples.md) for real-world patterns.
> See [references/anti-patterns.md](references/anti-patterns.md) for common mistakes.

## Related Skills

- `frappe-impl-clientscripts` — Implementation workflows and decision trees
- `frappe-errors-clientscripts` — Error handling and debugging patterns
- `frappe-syntax-whitelisted` — Server-side methods called from client scripts
- `frappe-syntax-doctypes` — DocType field definitions referenced in scripts
