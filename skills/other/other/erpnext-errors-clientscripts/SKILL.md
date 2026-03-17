---
name: erpnext-errors-clientscripts
description: "Error handling patterns for ERPNext/Frappe Client Scripts. Use when implementing try/catch, user feedback, server call error handling, validation errors, and debugging. Covers async error handling, graceful degradation, and user-friendly error messages. V14/V15/V16 compatible. Triggers: client script error, try catch, frappe.throw, error handling, async error, validation error."
---

# ERPNext Client Scripts - Error Handling

This skill covers error handling patterns for Client Scripts. For syntax, see `erpnext-syntax-clientscripts`. For implementation workflows, see `erpnext-impl-clientscripts`.

**Version**: v14/v15/v16 compatible

---

## Main Decision: How to Handle the Error?

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHAT TYPE OF ERROR ARE YOU HANDLING?                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► Validation error (must prevent save)?                                 │
│   └─► frappe.throw() in validate event                                  │
│                                                                         │
│ ► Warning (inform user, allow continue)?                                │
│   └─► frappe.msgprint() with indicator                                  │
│                                                                         │
│ ► Server call might fail?                                               │
│   └─► try/catch with async/await OR callback error handling             │
│                                                                         │
│ ► Field value invalid (not blocking)?                                   │
│   └─► frm.set_intro() or field description                              │
│                                                                         │
│ ► Need to debug/trace?                                                  │
│   └─► console.log/warn/error + frappe.show_alert for dev                │
│                                                                         │
│ ► Unexpected error in any code?                                         │
│   └─► Wrap in try/catch, log error, show user-friendly message          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Error Feedback Methods

### Quick Reference

| Method | Blocks Save? | User Action | Use For |
|--------|:------------:|-------------|---------|
| `frappe.throw()` | ✅ YES | Must dismiss | Validation errors |
| `frappe.msgprint()` | ❌ NO | Must dismiss | Important info/warnings |
| `frappe.show_alert()` | ❌ NO | Auto-dismiss | Success/info feedback |
| `frm.set_intro()` | ❌ NO | None | Form-level warnings |
| `frm.dashboard.set_headline()` | ❌ NO | None | Status indicators |
| `console.error()` | ❌ NO | None | Debugging only |

### frappe.throw() - Blocking Error

```javascript
// Basic throw - stops execution, prevents save
frappe.throw(__('Customer is required'));

// With title
frappe.throw({
    title: __('Validation Error'),
    message: __('Amount cannot be negative')
});

// With indicator color
frappe.throw({
    message: __('Credit limit exceeded'),
    indicator: 'red'
});
```

**CRITICAL**: Only use `frappe.throw()` in `validate` event to prevent save. Using it elsewhere stops script execution but doesn't prevent form actions.

### frappe.msgprint() - Non-Blocking Alert

```javascript
// Simple message
frappe.msgprint(__('Document will be processed'));

// With title and indicator
frappe.msgprint({
    title: __('Warning'),
    message: __('Stock is running low'),
    indicator: 'orange'
});

// With primary action button
frappe.msgprint({
    title: __('Confirm Action'),
    message: __('This will archive 50 records. Continue?'),
    primary_action: {
        label: __('Yes, Archive'),
        action: () => {
            // perform action
            frappe.hide_msgprint();
        }
    }
});
```

### frappe.show_alert() - Toast Notification

```javascript
// Success (green, auto-dismiss)
frappe.show_alert({
    message: __('Saved successfully'),
    indicator: 'green'
}, 3);  // 3 seconds

// Warning (orange)
frappe.show_alert({
    message: __('Some items are out of stock'),
    indicator: 'orange'
}, 5);

// Error (red)
frappe.show_alert({
    message: __('Failed to fetch data'),
    indicator: 'red'
}, 5);
```

---

## Error Handling Patterns

### Pattern 1: Synchronous Validation

```javascript
frappe.ui.form.on('Sales Order', {
    validate(frm) {
        // Multiple validations - collect errors
        let errors = [];
        
        if (!frm.doc.customer) {
            errors.push(__('Customer is required'));
        }
        
        if (frm.doc.grand_total <= 0) {
            errors.push(__('Total must be greater than zero'));
        }
        
        if (!frm.doc.items || frm.doc.items.length === 0) {
            errors.push(__('At least one item is required'));
        }
        
        // Throw all errors at once
        if (errors.length > 0) {
            frappe.throw({
                title: __('Validation Errors'),
                message: errors.join('<br>')
            });
        }
    }
});
```

### Pattern 2: Async Server Call with Error Handling

```javascript
frappe.ui.form.on('Sales Order', {
    async customer(frm) {
        if (!frm.doc.customer) return;
        
        try {
            let r = await frappe.call({
                method: 'myapp.api.get_customer_details',
                args: { customer: frm.doc.customer }
            });
            
            if (r.message) {
                frm.set_value('credit_limit', r.message.credit_limit);
            }
        } catch (error) {
            console.error('Failed to fetch customer:', error);
            frappe.show_alert({
                message: __('Could not load customer details'),
                indicator: 'red'
            }, 5);
            // Don't throw - allow user to continue
        }
    }
});
```

### Pattern 3: Async Validation with Server Check

```javascript
frappe.ui.form.on('Sales Order', {
    async validate(frm) {
        // Server-side validation
        try {
            let r = await frappe.call({
                method: 'myapp.api.validate_order',
                args: { 
                    customer: frm.doc.customer,
                    total: frm.doc.grand_total 
                }
            });
            
            if (r.message && !r.message.valid) {
                frappe.throw({
                    title: __('Validation Failed'),
                    message: r.message.error
                });
            }
        } catch (error) {
            // Server error - decide: block or allow?
            console.error('Validation call failed:', error);
            
            // Option 1: Block save on server error (safer)
            frappe.throw(__('Could not validate. Please try again.'));
            
            // Option 2: Allow save with warning (use with caution)
            // frappe.show_alert({
            //     message: __('Validation skipped due to server error'),
            //     indicator: 'orange'
            // }, 5);
        }
    }
});
```

### Pattern 4: frappe.call Callback Error Handling

```javascript
// When not using async/await
frappe.call({
    method: 'myapp.api.process_data',
    args: { doc_name: frm.doc.name },
    freeze: true,
    freeze_message: __('Processing...'),
    callback: (r) => {
        if (r.message) {
            frappe.show_alert({
                message: __('Processing complete'),
                indicator: 'green'
            });
            frm.reload_doc();
        }
    },
    error: (r) => {
        // Server returned error (4xx, 5xx)
        console.error('API Error:', r);
        frappe.msgprint({
            title: __('Error'),
            message: __('Processing failed. Please try again.'),
            indicator: 'red'
        });
    }
});
```

### Pattern 5: Child Table Validation

```javascript
frappe.ui.form.on('Sales Invoice', {
    validate(frm) {
        let errors = [];
        
        (frm.doc.items || []).forEach((row, idx) => {
            if (!row.item_code) {
                errors.push(__('Row {0}: Item is required', [idx + 1]));
            }
            if (row.qty <= 0) {
                errors.push(__('Row {0}: Quantity must be positive', [idx + 1]));
            }
            if (row.rate < 0) {
                errors.push(__('Row {0}: Rate cannot be negative', [idx + 1]));
            }
        });
        
        if (errors.length > 0) {
            frappe.throw({
                title: __('Item Errors'),
                message: errors.join('<br>')
            });
        }
    }
});
```

### Pattern 6: Graceful Degradation

```javascript
frappe.ui.form.on('Sales Order', {
    async refresh(frm) {
        // Try to load extra data, but don't fail if unavailable
        try {
            let stock = await frappe.call({
                method: 'myapp.api.get_stock_summary',
                args: { items: frm.doc.items.map(r => r.item_code) }
            });
            
            if (stock.message) {
                render_stock_dashboard(frm, stock.message);
            }
        } catch (error) {
            // Log but don't disturb user
            console.warn('Stock dashboard unavailable:', error);
            // Optionally show subtle indicator
            frm.dashboard.set_headline(
                __('Stock info unavailable'),
                'orange'
            );
        }
    }
});
```

> **See**: `references/patterns.md` for more error handling patterns.

---

## Debugging Techniques

### Console Logging

```javascript
// Development debugging
frappe.ui.form.on('Sales Order', {
    customer(frm) {
        console.log('Customer changed:', frm.doc.customer);
        console.log('Full doc:', JSON.parse(JSON.stringify(frm.doc)));
        
        // Trace child table
        console.table(frm.doc.items);
    }
});
```

### Conditional Debugging

```javascript
// Only log in development
const DEBUG = frappe.boot.developer_mode;

function debugLog(...args) {
    if (DEBUG) {
        console.log('[MyApp]', ...args);
    }
}

frappe.ui.form.on('Sales Order', {
    validate(frm) {
        debugLog('Validating:', frm.doc.name);
        // validation logic
    }
});
```

### Error Stack Traces

```javascript
try {
    riskyOperation();
} catch (error) {
    console.error('Error details:', {
        message: error.message,
        stack: error.stack,
        doc: frm.doc.name
    });
    
    // User-friendly message (no technical details)
    frappe.msgprint({
        title: __('Error'),
        message: __('An unexpected error occurred. Please contact support.'),
        indicator: 'red'
    });
}
```

---

## Critical Rules

### ✅ ALWAYS

1. **Wrap async calls in try/catch** - Uncaught Promise rejections crash silently
2. **Use `__()` for error messages** - All user-facing text must be translatable
3. **Log errors to console** - Helps debugging without exposing to users
4. **Collect multiple validation errors** - Don't throw on first error
5. **Provide actionable error messages** - Tell user how to fix it

### ❌ NEVER

1. **Don't expose technical errors to users** - Catch and translate
2. **Don't use `frappe.throw()` outside validate** - It stops execution but doesn't prevent save
3. **Don't ignore server call failures** - Always handle error callback
4. **Don't use `alert()` or `confirm()`** - Use frappe methods instead
5. **Don't leave `console.log` in production** - Use conditional debugging

---

## Quick Reference: Error Message Quality

```javascript
// ❌ BAD - Technical, not actionable
frappe.throw('NullPointerException in line 42');
frappe.throw('Query failed');
frappe.throw('Error');

// ✅ GOOD - Clear, actionable
frappe.throw(__('Please select a customer before adding items'));
frappe.throw(__('Amount {0} exceeds credit limit of {1}', [amount, limit]));
frappe.throw(__('Could not save. Please check your internet connection and try again.'));
```

---

## Reference Files

| File | Contents |
|------|----------|
| `references/patterns.md` | Complete error handling patterns |
| `references/examples.md` | Full working examples |
| `references/anti-patterns.md` | Common mistakes to avoid |

---

## See Also

- `erpnext-syntax-clientscripts` - Client Script syntax
- `erpnext-impl-clientscripts` - Implementation workflows
- `erpnext-errors-serverscripts` - Server-side error handling
