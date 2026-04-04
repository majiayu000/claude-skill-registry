---
name: odoo-debugger
description: Analyzes and resolves Odoo 16.0 issues including SVL linking problems, queue job failures, view errors, and business logic bugs. This skill should be used when the user reports problems such as "Debug this SVL linking issue" or "Queue job is failing" or "View not showing correctly" or "Figure out why this vendor bill isn't linking to stock moves".
---

# Odoo Debugger & Issue Resolver

## Overview

This skill provides systematic debugging approaches for common Odoo 16.0 issues, with specialized knowledge of SVL (Stock Valuation Layer) linking, queue jobs, view inheritance problems, and business logic errors specific to the Siafa project.

## Issue Categories

### 1. SVL (Stock Valuation Layer) Issues
Stock valuation layers not linking properly to vendor bills or account moves.

### 2. Queue Job Failures
Background jobs failing or getting stuck in queue_job system.

### 3. View/XML Errors
Views not rendering, XPath inheritance issues, missing fields.

### 4. Business Logic Bugs
Computed fields not calculating, onchange not triggering, constraints failing.

### 5. Data Integrity Issues
Orphaned records, inconsistent data, broken relationships.

### 6. Performance Problems
Slow queries, N+1 problems, inefficient computed fields.

### 7. Access Rights Issues
Permission errors, record rules blocking access.

## Debugging Workflow

### Step 1: Gather Information

Ask for:
- Error message or traceback (full text)
- Steps to reproduce the issue
- Which module/model is affected
- Recent changes or updates
- Database name and Odoo version

### Step 2: Categorize the Issue

Identify which category the issue falls into and follow the specialized workflow.

## Debugging Patterns by Category

### Pattern 1: SVL Linking Issues

**Common Symptoms:**
- Stock valuation layers exist but not linked to vendor bills
- Account move lines don't reference SVL
- Quantity mismatch between stock moves and SVL
- Missing SVL for stock moves

**Investigation Script:**

```python
# In Odoo shell (python3 src/odoo-bin shell -c src/odoo.conf -d DATABASE_NAME)

# Get SVL record
svl = env['stock.valuation.layer'].browse(SVL_ID)

# Check SVL details
print(f"SVL ID: {svl.id}")
print(f"Product: {svl.product_id.name}")
print(f"Quantity: {svl.quantity}")
print(f"Value: {svl.value}")
print(f"Unit Cost: {svl.unit_cost}")
print(f"Stock Move: {svl.stock_move_id.name if svl.stock_move_id else 'NONE'}")
print(f"Account Move: {svl.account_move_id.name if svl.account_move_id else 'NONE'}")

# Check stock move linkage
if svl.stock_move_id:
    move = svl.stock_move_id
    print(f"\nStock Move Details:")
    print(f"  Name: {move.name}")
    print(f"  State: {move.state}")
    print(f"  Picking: {move.picking_id.name if move.picking_id else 'NONE'}")
    print(f"  Purchase Line: {move.purchase_line_id.id if move.purchase_line_id else 'NONE'}")

    # Check for vendor bill
    if move.purchase_line_id:
        po_line = move.purchase_line_id
        print(f"\nPurchase Order Line:")
        print(f"  Order: {po_line.order_id.name}")
        print(f"  Invoice Lines: {po_line.invoice_lines}")

        for inv_line in po_line.invoice_lines:
            print(f"    Invoice: {inv_line.move_id.name}, State: {inv_line.move_id.state}")

# Check account move lines
if svl.account_move_id:
    print(f"\nAccount Move Lines:")
    for line in svl.account_move_id.line_ids:
        print(f"  Account: {line.account_id.code} - {line.account_id.name}")
        print(f"  Debit: {line.debit}, Credit: {line.credit}")
        print(f"  SVL ID in context: {line.stock_valuation_layer_id.id if line.stock_valuation_layer_id else 'NONE'}")

# Find orphaned SVLs (SQL)
env.cr.execute("""
    SELECT svl.id, svl.product_id, svl.quantity, svl.value
    FROM stock_valuation_layer svl
    WHERE svl.stock_move_id IS NULL
    OR svl.account_move_id IS NULL
    LIMIT 100
""")
orphaned = env.cr.dictfetchall()
print(f"\nFound {len(orphaned)} potentially orphaned SVLs")
```

**Common Fixes:**

1. **Re-link SVL to Account Move:**
```python
svl = env['stock.valuation.layer'].browse(SVL_ID)
account_move = env['account.move'].browse(ACCOUNT_MOVE_ID)

# Update SVL
svl.write({'account_move_id': account_move.id})

# Update account move lines
for line in account_move.line_ids:
    if line.account_id == svl.product_id.categ_id.property_stock_valuation_account_id:
        line.write({'stock_valuation_layer_id': svl.id})
```

2. **Regenerate SVL:**
```python
stock_move = env['stock.move'].browse(MOVE_ID)
stock_move._create_stock_valuation_layers()
```

### Pattern 2: Queue Job Failures

**Investigation:**

```python
# Find failed jobs
failed_jobs = env['queue.job'].search([
    ('state', '=', 'failed'),
    ('date_created', '>=', '2025-01-01')
])

for job in failed_jobs:
    print(f"\nJob: {job.name}")
    print(f"  UUID: {job.uuid}")
    print(f"  State: {job.state}")
    print(f"  Date Failed: {job.date_done}")
    print(f"  Exception:\n{job.exc_info}")

    # Retry the job
    # job.requeue()
```

**Common Fixes:**

1. **Retry failed job:**
```python
job = env['queue.job'].browse(JOB_ID)
job.requeue()
```

2. **Cancel stuck job:**
```python
job.write({'state': 'done'})  # or 'cancelled'
```

### Pattern 3: View/XML Errors

**Common Issues:**
- XPath not finding target element
- Field doesn't exist in model
- View inheritance loop
- Incorrect XML ID reference

**Investigation:**

1. **Check if view exists:**
```python
view = env.ref('module_name.view_id')
print(view.arch_db)  # Print XML
```

2. **Find view by model:**
```python
views = env['ir.ui.view'].search([('model', '=', 'stock.picking')])
for v in views:
    print(f"{v.name}: {v.xml_id}")
```

3. **Test XPath expression:**
```python
from lxml import etree
view = env.ref('stock.view_picking_form')
arch = etree.fromstring(view.arch_db)

# Test xpath
result = arch.xpath("//field[@name='partner_id']")
print(f"Found {len(result)} elements")
```

**Common Fixes:**

1. **Fix XPath - Use Developer Mode to inspect actual view structure**
2. **Ensure field exists in model before adding to view**
3. **Check view priority if inheritance not working**

### Pattern 4: Business Logic Bugs

**Computed Field Not Updating:**

```python
# Force recompute
record = env['model.name'].browse(RECORD_ID)
record._recompute_field('field_name')

# Check dependencies
field = env['model.name']._fields['field_name']
print(f"Depends: {field.depends}")

# Test compute method directly
record._compute_field_name()
```

**Onchange Not Triggering:**

```python
# Onchange methods only work in UI
# Test via form:
record.onchange('field_name', 'partner_id')
```

**Constraint Failing:**

```python
# Test constraint
try:
    record._check_constraint_name()
    print("Constraint passed")
except ValidationError as e:
    print(f"Constraint failed: {e}")
```

### Pattern 5: Data Investigation (SQL)

**Finding Data Inconsistencies:**

```python
# Stock moves without SVL
env.cr.execute("""
    SELECT sm.id, sm.name, sm.product_id, sm.state
    FROM stock_move sm
    LEFT JOIN stock_valuation_layer svl ON svl.stock_move_id = sm.id
    WHERE sm.state = 'done'
    AND svl.id IS NULL
    AND sm.product_id IN (
        SELECT id FROM product_product WHERE type = 'product'
    )
    LIMIT 50
""")
print(env.cr.dictfetchall())

# Vendor bills with no SVL link
env.cr.execute("""
    SELECT am.id, am.name, am.partner_id, am.amount_total
    FROM account_move am
    WHERE am.move_type = 'in_invoice'
    AND am.state = 'posted'
    AND am.id NOT IN (
        SELECT DISTINCT account_move_id
        FROM stock_valuation_layer
        WHERE account_move_id IS NOT NULL
    )
    LIMIT 50
""")
print(env.cr.dictfetchall())
```

## Debugging Tools

### Enable Debug Logging

In `odoo.conf`:
```ini
log_level = debug
log_handler = :DEBUG
```

Or via command line:
```bash
python3 src/odoo-bin -c src/odoo.conf --log-level=debug --log-handler=:DEBUG
```

### Add Logging to Code

```python
import logging
_logger = logging.getLogger(__name__)

def method(self):
    _logger.info('Method called with %s', self)
    _logger.debug('Detailed debug info: %s', self.read())
    _logger.warning('Something unusual: %s', issue)
    _logger.error('Error occurred: %s', error)
```

### Use pdb for Debugging

```python
import pdb; pdb.set_trace()
```

## Common Error Patterns

### AccessError
```
User does not have access rights
```
**Fix:** Check `ir.model.access.csv` and record rules

### ValidationError
```
Constraint validation failed
```
**Fix:** Check `@api.constrains` methods

### MissingError
```
Record does not exist
```
**Fix:** Check if record was deleted, use `exists()` method

### SQL Errors
```
column does not exist
```
**Fix:** Update module to create/modify fields

## Resources

### scripts/investigate_svl.py
Python script for automated SVL investigation - checks linkage, finds orphaned records, validates data consistency.

### scripts/check_queue_jobs.py
Script to analyze queue job status, identify stuck jobs, and generate repair commands.

### references/debugging_queries.md
Collection of useful SQL queries for data investigation and debugging common issues.

### references/common_issues.md
Database of known issues specific to the Siafa project with solutions and workarounds.
