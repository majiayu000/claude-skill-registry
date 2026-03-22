---
name: frappe-impl-clientscripts
description: >
  Use when implementing client-side form features in Frappe/ERPNext:
  field visibility, cascading filters, calculated fields, custom buttons,
  server calls, form validation, child table logic, debugging.
  Covers step-by-step workflows from Setup > Client Script through
  migration to custom app JS. Keywords: how to implement client script,
  form logic workflow, dynamic UI, calculate fields, frm.call, frappe.call,
  frappe.xcall, client script testing, field dependency, custom button.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Client Scripts — Implementation Workflows

Step-by-step workflows for building client-side form features. For exact API syntax, see `frappe-syntax-clientscripts`.

**Version**: v14/v15/v16 | **Note**: v13 renamed "Custom Script" to "Client Script"

## Quick Decision: Client or Server?

```
MUST the logic ALWAYS execute (imports, API, Data Import)?
├── YES → Server Script or Controller
└── NO  → What is the goal?
         ├── UI feedback / UX → Client Script
         ├── Show/hide fields → Client Script
         ├── Link filters → Client Script
         ├── Data validation → BOTH (client for UX, server for integrity)
         └── Calculations → Client for display, server for critical
```

**Rule**: ALWAYS use Client Scripts for UX. ALWAYS back critical logic with server-side validation.

## Workflow 1: Create a Client Script via UI

1. Navigate to **Setup > Client Script** (or type "New Client Script" in awesomebar)
2. Select the target **DocType**
3. ALWAYS set **Enabled** checkbox
4. Write script using the `frappe.ui.form.on` pattern
5. Save — script is active immediately (no restart needed)
6. Open target DocType form → test behavior
7. Open browser DevTools Console (F12) for debugging

**When to migrate to custom app**: ALWAYS migrate when the script exceeds 50 lines, needs version control, or must be deployed across environments.

## Workflow 2: Choose the Right Event

```
WHAT DO YOU WANT?
├── Set link filters         → setup (once, earliest lifecycle)
├── Add custom buttons       → refresh (re-added after each render)
├── Show/hide fields         → refresh + {fieldname} (BOTH needed)
├── Validate before save     → validate (frappe.throw stops save)
├── Action after save        → after_save
├── Calculate on change      → {fieldname} handler
├── Child row added          → {tablename}_add
├── Child row removed        → {tablename}_remove
├── Child field changed      → Child DocType: {fieldname}
├── One-time init            → setup or onload
└── After full DOM render    → onload_post_render
```

> See [references/decision-tree.md](references/decision-tree.md) for complete event timing matrix.

## Workflow 3: Field Visibility Toggle

**Goal**: Show "delivery_date" only when "requires_delivery" is checked.

**Step 1**: Implement BOTH refresh and fieldname events:

```javascript
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        frm.trigger('requires_delivery'); // Set initial state
    },
    requires_delivery(frm) {
        frm.toggle_display('delivery_date', frm.doc.requires_delivery);
        frm.toggle_reqd('delivery_date', frm.doc.requires_delivery);
    }
});
```

**Why both?** `refresh` sets state on form load. `{fieldname}` responds to user interaction. NEVER use only one — the form will show wrong state on load or on change.

## Workflow 4: Cascading Link Filters

**Goal**: Filter "city" based on selected "country".

```javascript
frappe.ui.form.on('Customer', {
    setup(frm) {
        // ALWAYS set filters in setup — ensures consistency
        frm.set_query('city', () => ({
            filters: { country: frm.doc.country || '' }
        }));
    },
    country(frm) {
        frm.set_value('city', ''); // ALWAYS clear dependent field
    }
});
```

**Rule**: ALWAYS put `set_query` in `setup`. ALWAYS clear child fields when parent changes.

## Workflow 5: Calculated Fields (Child Table)

**Goal**: Calculate row amounts and document totals.

```javascript
frappe.ui.form.on('Invoice Item', {
    qty(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    rate(frm, cdt, cdn) { calculate_row(frm, cdt, cdn); },
    amount(frm) { calculate_totals(frm); }
});

frappe.ui.form.on('Invoice', {
    items_remove(frm) { calculate_totals(frm); }
});

function calculate_row(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    frappe.model.set_value(cdt, cdn, 'amount',
        flt(row.qty) * flt(row.rate));
}

function calculate_totals(frm) {
    let total = (frm.doc.items || []).reduce(
        (sum, row) => sum + flt(row.amount), 0);
    frm.set_value('grand_total', flt(total, 2));
}
```

**Rules**:
- ALWAYS use `flt()` for numeric operations (handles null/undefined)
- ALWAYS handle `items_remove` — totals must recalculate on row deletion
- NEVER call `refresh_field` after `set_value` — it triggers automatically

## Workflow 6: Server Calls — Which Method to Use

```
NEED TO CALL THE SERVER?
├── Fetch a single value?
│   └── frappe.db.get_value(doctype, name, fields)
│       Returns: Promise — lightweight, no whitelist needed
│
├── Call a document's controller method?
│   └── frm.call(method, args)
│       Requires: @frappe.whitelist() on controller method
│       Auto-includes: doctype, docname, doc context
│
├── Call a standalone whitelisted function?
│   └── frappe.call({method: 'dotted.path', args: {}})
│       Requires: @frappe.whitelist() decorator
│       Returns: Promise with r.message
│
└── Need Promise-only (no callback)?
    └── frappe.xcall('dotted.path', args)
        Same as frappe.call but returns clean Promise
```

**Example — frm.call**:
```javascript
frm.call('calculate_taxes').then(r => {
    frm.reload_doc();  // Refresh after server-side changes
});
```

**Example — frappe.xcall**:
```javascript
let result = await frappe.xcall(
    'myapp.api.check_credit', { customer: frm.doc.customer });
```

## Workflow 7: Custom Button Implementation

```javascript
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        // ALWAYS check conditions before adding buttons
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Invoice'), () => {
                create_invoice(frm);
            }, __('Create'));  // Group label
        }
    }
});
```

**Rules**:
- ALWAYS add buttons in `refresh` — they are cleared on each render
- ALWAYS check `frm.is_new()` — buttons on unsaved docs cause errors
- ALWAYS wrap button labels in `__()` for translation
- NEVER add buttons in `setup` or `onload` — UI not ready

## Workflow 8: Async Validation with Server Check

```javascript
frappe.ui.form.on('Sales Order', {
    async validate(frm) {
        if (!frm.doc.customer || !frm.doc.grand_total) return;

        let r = await frappe.call({
            method: 'myapp.api.check_credit',
            args: {
                customer: frm.doc.customer,
                amount: frm.doc.grand_total
            }
        });

        if (r.message && !r.message.allowed) {
            frappe.throw(__('Credit limit exceeded. Available: {0}',
                [r.message.available]));
        }
    }
});
```

**Rules**:
- ALWAYS use `async/await` for server calls in `validate`
- ALWAYS use `frappe.throw()` to stop save — `msgprint` does NOT stop it
- NEVER put slow server calls in `validate` without user expectation

## Workflow 9: Debugging in Browser

1. Open **F12 DevTools > Console**
2. Add `console.log(frm.doc)` in your event handler
3. Use `cur_frm` in Console to inspect current form state
4. Check **Network** tab for failed `frappe.call` requests
5. Use `frappe.ui.form.handlers` to see registered event handlers

**Debug pattern**:
```javascript
frappe.ui.form.on('MyDocType', {
    my_field(frm) {
        console.log('Field changed:', frm.doc.my_field);
        // ... actual logic
    }
});
```

## Workflow 10: Migrate Client Script to Custom App

1. Create JS file: `myapp/myapp/public/js/sales_order.js`
2. Move script content to the file (keep `frappe.ui.form.on` wrapper)
3. Register in `hooks.py`:
   ```python
   doctype_js = {
       "Sales Order": "public/js/sales_order.js"
   }
   ```
4. Run `bench build` (or `bench watch` for development)
5. Delete the Client Script document from Setup
6. Test on the form — behavior must be identical

**ALWAYS migrate when**: version control needed, multi-environment deployment, script > 50 lines, team collaboration required.

## Performance Rules

| Rule | Why |
|------|-----|
| `set_query` in `setup` only | Prevents re-registration on every refresh |
| Batch `set_value` calls | `frm.set_value({a: 1, b: 2})` — one update, not two |
| Cache server responses | Store in `frm._cache_key` to avoid repeat calls |
| NEVER query in loops | Fetch all data once, build lookup map |
| Use `frappe.db.get_value` | Lighter than `frappe.call` for simple lookups |

## Related Skills

- `frappe-syntax-clientscripts` — Exact API syntax and method signatures
- `frappe-errors-clientscripts` — Error handling and common pitfalls
- `frappe-syntax-whitelisted` — Server methods callable from client
- `frappe-core-database` — `frappe.db.*` client-side API
- `frappe-impl-serverscripts` — When to move logic server-side

> See [references/decision-tree.md](references/decision-tree.md) for event selection.
> See [references/workflows.md](references/workflows.md) for extended patterns.
> See [references/examples.md](references/examples.md) for 10+ complete examples.
