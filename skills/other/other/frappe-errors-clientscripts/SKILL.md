---
name: frappe-errors-clientscripts
description: >
  Use when debugging or preventing errors in Frappe Client Scripts.
  Prevents TypeError, frappe.call failures, async/await mistakes,
  cur_frm vs frm confusion, field not found, child table access errors,
  timing issues, CSRF token errors, and permission denied on frappe.call.
  Covers error diagnosis flowchart and debug tools for v14/v15/v16.
  Keywords: client script error, TypeError, frappe.call, async await,
  cur_frm, field not found, child table, CSRF, permission denied.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Client Script Errors — Diagnosis and Resolution

Cross-refs: `frappe-syntax-clientscripts` (syntax), `frappe-impl-clientscripts` (workflows), `frappe-errors-serverscripts` (server-side).

---

## Error Diagnosis Flowchart

```
ERROR IN CLIENT SCRIPT
│
├─► TypeError: Cannot read properties of undefined
│   ├─► "frm.doc.fieldname" → Field does not exist on DocType
│   ├─► "r.message.value" → Server returned null/error
│   └─► "row.fieldname" in child table → Row not fetched correctly
│
├─► frappe.call fails silently
│   ├─► Missing error callback → Add error handler
│   ├─► 403 Forbidden → Method not whitelisted (@frappe.whitelist)
│   ├─► 417 Expectation Failed → Server-side frappe.throw()
│   └─► 401 Unauthorized → Session expired or CSRF token invalid
│
├─► Uncaught (in promise) → Missing try/catch on async frappe.call
│
├─► Field appears blank after set_value → Timing issue (setup vs refresh)
│
├─► cur_frm is undefined → Using cur_frm in list/report context
│
└─► frappe.throw() does not prevent save → Used outside validate event
```

---

## Error Message → Cause → Fix Table

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `TypeError: Cannot read properties of undefined (reading 'fieldname')` | Field does not exist on DocType or doc not loaded | ALWAYS check `frm.doc` exists before accessing fields |
| `TypeError: frm.set_value is not a function` | Using `cur_frm` shortcut that is undefined | ALWAYS use the `frm` parameter from event handler |
| `Uncaught (in promise)` | Unhandled async rejection from frappe.call | ALWAYS wrap async calls in try/catch |
| `CSRFTokenError` / `403 with CSRF` | Token mismatch after session timeout | ALWAYS use `frappe.call()` (handles CSRF automatically) |
| `Not permitted` / 403 on frappe.call | Server method missing `@frappe.whitelist()` | ALWAYS add `@frappe.whitelist()` decorator to API methods |
| `frappe.throw() not preventing save` | `frappe.throw()` used outside `validate` event | ALWAYS use `frappe.throw()` only in `validate` |
| `field not found: xyz` in set_query | Fieldname typo or field not in child table | Verify exact fieldname against DocType definition |
| `row.item_code is undefined` | Accessing child row wrong — `locals` not synced | Use `frappe.get_doc(cdt, cdn)` in child table events |
| `frm.set_value not working` | Called in `setup` before form fully loaded | Move field-setting logic to `refresh` event |
| `Maximum call stack exceeded` | Circular trigger — field change fires own handler | Use `frm.flags` guard to break recursion |

---

## Critical Error Patterns

### 1. cur_frm vs frm — The #1 Beginner Mistake

```javascript
// ❌ WRONG — cur_frm is undefined in many contexts
frappe.ui.form.on('Sales Order', {
    customer(frm) {
        cur_frm.set_value('territory', 'Default');  // BREAKS in list view
    }
});

// ✅ CORRECT — ALWAYS use the frm parameter
frappe.ui.form.on('Sales Order', {
    customer(frm) {
        frm.set_value('territory', 'Default');
    }
});
```

**Rule**: NEVER use `cur_frm`. ALWAYS use the `frm` parameter passed to every event handler.

### 2. Async/Await — Silent Failure Without try/catch

```javascript
// ❌ WRONG — Unhandled rejection crashes silently
frappe.ui.form.on('Sales Order', {
    async customer(frm) {
        let r = await frappe.call({
            method: 'myapp.api.get_data',
            args: { customer: frm.doc.customer }
        });
        frm.set_value('credit_limit', r.message.limit);  // r.message may be null
    }
});

// ✅ CORRECT — try/catch with null check
frappe.ui.form.on('Sales Order', {
    async customer(frm) {
        if (!frm.doc.customer) return;
        try {
            let r = await frappe.call({
                method: 'myapp.api.get_data',
                args: { customer: frm.doc.customer }
            });
            if (r.message) {
                frm.set_value('credit_limit', r.message.limit || 0);
            }
        } catch (error) {
            console.error('Customer fetch failed:', error);
            frappe.show_alert({
                message: __('Could not load customer details'),
                indicator: 'red'
            }, 5);
        }
    }
});
```

### 3. Child Table Access — Wrong Pattern

```javascript
// ❌ WRONG — frm.doc.items[0] may not reflect latest state
frappe.ui.form.on('Sales Order Item', {
    item_code(frm, cdt, cdn) {
        let row = frm.doc.items.find(r => r.name === cdn);  // fragile
        row.rate = 100;  // Does not trigger UI refresh
    }
});

// ✅ CORRECT — Use frappe.get_doc and frappe.model.set_value
frappe.ui.form.on('Sales Order Item', {
    item_code(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (!row.item_code) return;
        frappe.model.set_value(cdt, cdn, 'rate', 100);  // Triggers refresh
    }
});
```

### 4. Timing — setup vs refresh

```javascript
// ❌ WRONG — set_value in setup, form not ready
frappe.ui.form.on('Sales Order', {
    setup(frm) {
        frm.set_value('company', 'My Company');  // May not work
    }
});

// ✅ CORRECT — set_query in setup, set_value in refresh/onload
frappe.ui.form.on('Sales Order', {
    setup(frm) {
        // Filters belong in setup
        frm.set_query('customer', () => ({ filters: { disabled: 0 } }));
    },
    refresh(frm) {
        // Value changes belong in refresh (or onload for new docs)
        if (frm.is_new()) {
            frm.set_value('company', 'My Company');
        }
    }
});
```

### 5. frappe.throw() Scope — Only Works in validate

```javascript
// ❌ WRONG — throw in customer change does NOT prevent save
frappe.ui.form.on('Sales Order', {
    customer(frm) {
        if (!frm.doc.customer) {
            frappe.throw(__('Customer required'));  // Stops script, NOT save
        }
    }
});

// ✅ CORRECT — throw in validate prevents save
frappe.ui.form.on('Sales Order', {
    customer(frm) {
        if (!frm.doc.customer) {
            frappe.msgprint({ message: __('Customer required'), indicator: 'orange' });
        }
    },
    validate(frm) {
        if (!frm.doc.customer) {
            frappe.throw(__('Customer is required'));  // Prevents save
        }
    }
});
```

### 6. Recursion Guard with Flags

```javascript
// ❌ WRONG — discount change triggers amount recalc, which triggers discount...
frappe.ui.form.on('Sales Order', {
    discount_percent(frm) {
        frm.set_value('grand_total', calculate(frm));  // Fires on_change loop
    }
});

// ✅ CORRECT — Use flags to break the cycle
frappe.ui.form.on('Sales Order', {
    discount_percent(frm) {
        if (frm.flags.skip_recalc) return;
        frm.flags.skip_recalc = true;
        frm.set_value('grand_total', calculate(frm));
        frm.flags.skip_recalc = false;
    }
});
```

---

## Debug Tools

| Tool | How to Use | When |
|------|-----------|------|
| Browser Console (F12) | `console.log(frm.doc)` | Inspect form state |
| `console.table()` | `console.table(frm.doc.items)` | View child table rows |
| `JSON.parse(JSON.stringify(frm.doc))` | Deep-clone for snapshot | Avoid circular refs in console |
| `frappe.boot.developer_mode` | Check if dev mode on | Conditional debug logging |
| `frappe.ui.toolbar.clear_cache()` | Clear client cache | After deploying script changes |
| Network tab (F12) | Filter XHR requests | Inspect frappe.call payloads |
| `frappe.show_alert({message: 'debug', indicator: 'blue'}, 5)` | Visual debug in UI | Quick feedback without console |

---

## ALWAYS / NEVER Rules

### ALWAYS

1. **Use the `frm` parameter** — NEVER use `cur_frm` [v14+]
2. **Wrap async frappe.call in try/catch** — Unhandled rejections fail silently
3. **Use `__()` for all user-facing strings** — Required for translation
4. **Collect multiple validation errors** before calling `frappe.throw()`
5. **Use `frappe.get_doc(cdt, cdn)`** to access child table rows in events
6. **Put `frappe.throw()` only in `validate`** to prevent save
7. **Check `r.message` for null** before accessing server response properties
8. **Use `frappe.model.set_value(cdt, cdn, field, value)`** in child table events

### NEVER

1. **NEVER use `alert()`, `confirm()`, or `prompt()`** — Use frappe.msgprint / frappe.confirm
2. **NEVER expose stack traces to users** — Log to console, show friendly message
3. **NEVER use `cur_frm`** — It is unreliable and undefined in many contexts
4. **NEVER leave `console.log` in production** — Use conditional `frappe.boot.developer_mode` check
5. **NEVER mix `.then()` and `await`** in the same function — Pick one pattern
6. **NEVER call `frm.set_value` in `setup`** — Form is not ready; use `refresh` or `onload`
7. **NEVER ignore the `error` callback** on `frappe.call` when using callback style

---

## Reference Files

| File | Contents |
|------|----------|
| `references/examples.md` | Real error scenarios with diagnosis |
| `references/anti-patterns.md` | Common mistakes with before/after fixes |
| `references/patterns.md` | Defensive error handling patterns |
