---
name: erpnext-syntax-clientscripts
description: "Exact JavaScript syntax for ERPNext/Frappe Client Scripts. Use when writing client-side code for form events, field manipulation, server calls, or child table handling in ERPNext v14/v15/v16. Triggers: client script, form event, frm methods, frappe.call, frappe.ui.form.on, JavaScript in ERPNext, browser-side code, UI interaction, client-side field validation."
---

# ERPNext Client Scripts Syntax (EN)

Client Scripts run in the browser and control all UI interactions in ERPNext/Frappe. They are created via **Setup → Client Script** or in custom apps under `public/js/`.

**Version**: v14/v15/v16 compatible (unless noted otherwise)

## Quick Reference

### Basic Structure

```javascript
frappe.ui.form.on('DocType Name', {
    // Form-level events
    setup(frm) { },
    refresh(frm) { },
    validate(frm) { },
    
    // Field change events
    fieldname(frm) { }
});
```

### Most Used Patterns

| Action | Code |
|--------|------|
| Set value | `frm.set_value('field', value)` |
| Hide field | `frm.toggle_display('field', false)` |
| Make field mandatory | `frm.toggle_reqd('field', true)` |
| Call server | `frappe.call({method: 'path.to.method', args: {}})` |
| Prevent save | `frappe.throw('Error message')` |

## Event Selection

Which event should I use?

```
One-time setup (queries, defaults)?
└── setup

Show/hide UI, add buttons?
└── refresh

Validation before save?
└── validate

Do something right after save?
└── after_save

React to field change?
└── {fieldname}
```

→ See [references/events.md](references/events.md) for complete event list and execution order.

## Essential Methods

### Value Manipulation

```javascript
// Set single value (async, returns Promise)
frm.set_value('status', 'Approved');

// Set multiple values at once
frm.set_value({
    status: 'Approved',
    priority: 'High'
});

// Get value
let value = frm.doc.fieldname;
```

### Field Properties

```javascript
// Show/hide
frm.toggle_display('priority', condition);

// Make mandatory
frm.toggle_reqd('due_date', true);

// Make read-only
frm.toggle_enable('amount', false);

// Advanced property change
frm.set_df_property('status', 'options', ['New', 'Open', 'Closed']);
frm.set_df_property('amount', 'read_only', 1);
```

### Link Field Filters

```javascript
// Simple filter
frm.set_query('customer', () => ({
    filters: { disabled: 0 }
}));

// Filter in child table
frm.set_query('item_code', 'items', (doc, cdt, cdn) => ({
    filters: { is_sales_item: 1 }
}));
```

→ See [references/methods.md](references/methods.md) for complete method signatures.

## Server Communication

### frappe.call (Whitelisted Methods)

```javascript
frappe.call({
    method: 'myapp.api.process_data',
    args: { customer: frm.doc.customer },
    freeze: true,
    freeze_message: __('Processing...'),
    callback: (r) => {
        if (r.message) {
            frm.set_value('result', r.message);
        }
    }
});
```

### frm.call (Document Methods)

```javascript
// Calls method on document controller
frm.call('calculate_taxes', { include_shipping: true })
    .then(r => frm.reload_doc());
```

### Async/Await Pattern

```javascript
async function fetchData(frm) {
    let r = await frappe.call({
        method: 'frappe.client.get_value',
        args: {
            doctype: 'Customer',
            filters: { name: frm.doc.customer },
            fieldname: 'credit_limit'
        }
    });
    return r.message.credit_limit;
}
```

## Child Table Handling

### Adding Rows

```javascript
let row = frm.add_child('items', {
    item_code: 'ITEM-001',
    qty: 5,
    rate: 100
});
frm.refresh_field('items');  // REQUIRED after modification
```

### Editing Rows

```javascript
frm.doc.items.forEach((row) => {
    if (row.qty > 10) {
        row.discount_percentage = 5;
    }
});
frm.refresh_field('items');
```

### Child Table Events

```javascript
frappe.ui.form.on('Sales Invoice Item', {
    qty(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate);
    },
    
    items_add(frm, cdt, cdn) {
        // New row added
    },
    
    items_remove(frm) {
        // Row removed
    }
});
```

→ See [references/examples.md](references/examples.md) for complete child table examples.

## Custom Buttons

```javascript
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            // Grouped buttons
            frm.add_custom_button(__('Invoice'), () => {
                // action
            }, __('Create'));
            
            // Primary action
            frm.page.set_primary_action(__('Process'), () => {
                frm.call('process').then(() => frm.reload_doc());
            });
        }
    }
});
```

## Critical Rules

1. **ALWAYS** call `frm.refresh_field('table')` after child table modifications
2. **NEVER** use `frm.doc.field = value` — use `frm.set_value()`
3. **ALWAYS** use `__('text')` for translatable strings
4. **validate** event: use `frappe.throw()` to prevent save
5. **setup** event: only for one-time configuration (not repeated)

→ See [references/anti-patterns.md](references/anti-patterns.md) for common mistakes.

## Related Skills

- `erpnext-impl-clientscripts` — Implementation workflows and decision trees
- `erpnext-errors-clientscripts` — Error handling patterns
- `erpnext-syntax-whitelisted` — Server-side methods to call
