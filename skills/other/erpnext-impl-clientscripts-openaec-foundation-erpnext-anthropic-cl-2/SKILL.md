---
name: erpnext-impl-clientscripts
description: "Implementation workflows and decision trees for ERPNext Client Scripts. Use when determining HOW to implement client-side features: form validations, dynamic UI, server integration, child table logic. Triggers: how do I implement, when to use, which approach, client script workflow, build form logic, make UI dynamic, calculate fields."
---

# ERPNext Client Scripts - Implementation (EN)

This skill helps you determine HOW to implement client-side features. For exact syntax, see `erpnext-syntax-clientscripts`.

**Version**: v14/v15/v16 compatible

## Main Decision: Client or Server?

```
┌─────────────────────────────────────────────────────────┐
│ Must the logic ALWAYS execute?                          │
│ (including imports, API calls, Server Scripts)          │
├─────────────────────────────────────────────────────────┤
│ YES → Server-side (Controller or Server Script)         │
│ NO  → What is the primary goal?                         │
│       ├── UI feedback/UX improvement → Client Script    │
│       ├── Show/hide fields → Client Script              │
│       ├── Link filters → Client Script                  │
│       ├── Data validation → BOTH (client + server)      │
│       └── Calculations → Depends on criticality         │
└─────────────────────────────────────────────────────────┘
```

**Rule of thumb**: Client Scripts for UX, Server for integrity.

## Decision Tree: Which Event?

```
WHAT DO YOU WANT TO ACHIEVE?
│
├─► Set link field filters
│   └── setup (once, early in lifecycle)
│
├─► Add custom buttons
│   └── refresh (after each form load/save)
│
├─► Show/hide fields based on condition
│   └── refresh + {fieldname} (both needed)
│
├─► Validation before save
│   └── validate (use frappe.throw on error)
│
├─► Action after successful save
│   └── after_save
│
├─► Calculation on field change
│   └── {fieldname}
│
├─► Child table row added
│   └── {tablename}_add
│
├─► Child table field changed
│   └── Child DocType event: {fieldname}
│
└─► One-time initialization
    └── setup or onload
```

→ See [references/decision-tree.md](references/decision-tree.md) for complete decision tree.

## Implementation Workflows

### Workflow 1: Dynamic Field Visibility

**Scenario**: Show "delivery_date" only when "requires_delivery" is checked.

```javascript
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        // Initial state on form load
        frm.trigger('requires_delivery');
    },
    
    requires_delivery(frm) {
        // Toggle on checkbox change AND refresh
        frm.toggle_display('delivery_date', frm.doc.requires_delivery);
        frm.toggle_reqd('delivery_date', frm.doc.requires_delivery);
    }
});
```

**Why both events?**
- `refresh`: Sets correct state when form opens
- `{fieldname}`: Responds to user interaction

### Workflow 2: Cascading Dropdowns

**Scenario**: Filter "city" based on selected "country".

```javascript
frappe.ui.form.on('Customer', {
    setup(frm) {
        // Filter MUST be in setup for consistency
        frm.set_query('city', () => ({
            filters: {
                country: frm.doc.country || ''
            }
        }));
    },
    
    country(frm) {
        // Clear city when country changes
        frm.set_value('city', '');
    }
});
```

### Workflow 3: Automatic Calculations

**Scenario**: Calculate total in child table with discount.

```javascript
frappe.ui.form.on('Sales Invoice', {
    discount_percentage(frm) {
        calculate_totals(frm);
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    qty(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    },
    
    rate(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    },
    
    amount(frm) {
        // Recalculate document total on row change
        calculate_totals(frm);
    }
});

function calculate_row_amount(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate);
}

function calculate_totals(frm) {
    let total = 0;
    (frm.doc.items || []).forEach(row => {
        total += row.amount || 0;
    });
    
    let discount = total * (frm.doc.discount_percentage || 0) / 100;
    frm.set_value('grand_total', total - discount);
}
```

### Workflow 4: Fetching Server Data

**Scenario**: Populate customer details on customer selection.

```javascript
frappe.ui.form.on('Sales Order', {
    async customer(frm) {
        if (!frm.doc.customer) {
            // Clear fields if customer cleared
            frm.set_value({
                customer_name: '',
                territory: '',
                credit_limit: 0
            });
            return;
        }
        
        // Fetch customer details
        let r = await frappe.db.get_value('Customer', 
            frm.doc.customer, 
            ['customer_name', 'territory', 'credit_limit']
        );
        
        if (r.message) {
            frm.set_value({
                customer_name: r.message.customer_name,
                territory: r.message.territory,
                credit_limit: r.message.credit_limit
            });
        }
    }
});
```

### Workflow 5: Validation with Server Check

**Scenario**: Check credit limit before save.

```javascript
frappe.ui.form.on('Sales Order', {
    async validate(frm) {
        if (frm.doc.customer && frm.doc.grand_total) {
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
    }
});
```

→ See [references/workflows.md](references/workflows.md) for more workflow patterns.

## Integration Matrix

| Client Script Action | Requires Server-side |
|----------------------|----------------------|
| Link filters | Optional: custom query |
| Fetch server data | `frappe.db.*` or whitelisted method |
| Call document method | `@frappe.whitelist()` in controller |
| Complex validation | Server Script or controller validation |
| Create document | `frappe.db.insert` or whitelisted method |

### Client + Server Combination

```javascript
// CLIENT: frm.call invokes controller method
frm.call('calculate_taxes')
    .then(() => frm.reload_doc());

// SERVER (controller): MUST have @frappe.whitelist
class SalesInvoice(Document):
    @frappe.whitelist()
    def calculate_taxes(self):
        # complex calculation
        self.tax_amount = self.grand_total * 0.21
        self.save()
```

## Checklist: Implementation Steps

### New Client Script Feature

1. **[ ] Determine scope**
   - UI/UX only? → Client script only
   - Data integrity? → Also server validation

2. **[ ] Choose events**
   - Use decision tree above
   - Combine refresh + fieldname for visibility

3. **[ ] Implement basics**
   - Start with `frappe.ui.form.on`
   - Test with console.log first

4. **[ ] Add error handling**
   - `try/catch` around async calls
   - `frappe.throw` for validation errors

5. **[ ] Test edge cases**
   - New document (frm.is_new())
   - Empty field (null checks)
   - Child table empty/filled

6. **[ ] Translate strings**
   - All UI text in `__()`

## Critical Rules

| Rule | Why |
|------|-----|
| `refresh_field()` after child table change | UI synchronization |
| `set_query` in `setup` event | Consistent filter behavior |
| `frappe.throw()` for validation, not `msgprint` | Stops save action |
| Async/await for server calls | Prevent race conditions |
| Check `frm.is_new()` for buttons | Prevent errors on new doc |

## Related Skills

- `erpnext-syntax-clientscripts` — Exact syntax and method signatures
- `erpnext-errors-clientscripts` — Error handling patterns
- `erpnext-syntax-whitelisted` — Server methods for frm.call
- `erpnext-database` — frappe.db.* client-side API

→ See [references/examples.md](references/examples.md) for 10+ complete implementation examples.
