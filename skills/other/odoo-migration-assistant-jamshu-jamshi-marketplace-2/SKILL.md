---
name: odoo-migration-assistant
description: Helps migrate Odoo modules and customizations between versions, specifically focusing on upgrades to/from Odoo 16.0. This skill should be used when the user requests migration help, such as "Migrate this module to Odoo 16" or "Upgrade from version 15 to 16" or "What changed in Odoo 16 for stock valuation?" or "Migration guide for this module".
---

# Odoo Migration Assistant

## Overview

This skill provides guidance for migrating Odoo modules between versions, with specialized knowledge of Odoo 16.0 changes, API differences, and upgrade procedures.

## Migration Scenarios

### 1. Upgrade TO Odoo 16.0
Migrating modules from older versions (14.0, 15.0) to 16.0.

### 2. Upgrade FROM Odoo 16.0
Preparing modules for future Odoo versions.

### 3. Version Compatibility Check
Determining what changes are needed for version compatibility.

## Migration Workflow

### Step 1: Identify Source and Target Versions

Ask for:
- Current Odoo version
- Target Odoo version
- Module name and purpose
- Dependencies

### Step 2: Assess Changes Required

Review:
- API changes between versions
- Deprecated features
- New required fields or methods
- View structure changes
- Dependency updates

### Step 3: Create Migration Plan

Provide step-by-step migration guide.

## Odoo 16.0 Specific Changes

### Key Changes in Odoo 16.0

**1. Python Version**
- Minimum: Python 3.8
- Recommended: Python 3.10+

**2. Manifest Changes**
```python
# Odoo 15 and earlier
{
    'version': '15.0.1.0.0',
    'depends': ['base', 'stock'],
    'license': 'LGPL-3',
}

# Odoo 16.0
{
    'version': '16.0.1.0.0',  # Updated version
    'depends': ['base', 'stock'],
    'license': 'LGPL-3',
    # New optional keys
    'assets': {  # Replaces some XML asset declarations
        'web.assets_backend': [
            'module/static/src/**/*',
        ],
    },
}
```

**3. Stock Valuation Changes**
```python
# Odoo 15
class StockMove(models.Model):
    _inherit = 'stock.move'

    def _create_account_move_line(self):
        # Old method signature
        pass

# Odoo 16
class StockMove(models.Model):
    _inherit = 'stock.move'

    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
        # Updated method signature with more parameters
        pass
```

**4. Widget Changes**
```xml
<!-- Odoo 15 -->
<field name="amount" widget="monetary" options="{'currency_field': 'currency_id'}"/>

<!-- Odoo 16 - Same, but some widgets renamed or removed -->
<field name="amount" widget="monetary" options="{'currency_field': 'currency_id'}"/>
```

**5. Removed/Deprecated Methods**
- `_update_average_price()` - Replaced with new accounting methods
- Some portal methods reorganized

## Migration Patterns

### Pattern 1: Update Manifest

```python
# Step 1: Update version number
'version': '16.0.1.0.0',

# Step 2: Check dependencies
# Ensure all depends modules are compatible with Odoo 16

# Step 3: Update data files if needed
'data': [
    'security/ir.model.access.csv',
    'views/views.xml',
    # Remove any deprecated files
],

# Step 4: Move assets if needed
'assets': {
    'web.assets_backend': [
        'module_name/static/src/js/*.js',
    ],
},
```

### Pattern 2: Update Model Fields

```python
# Check for removed fields in base models
# Example: If inheriting stock.move, check release notes

class StockMove(models.Model):
    _inherit = 'stock.move'

    # Update field definitions if base definition changed
    custom_field = fields.Char(...)

    # Update method signatures to match new base methods
    def _action_done(self, cancel_backorder=False):
        # Match new signature
        return super()._action_done(cancel_backorder=cancel_backorder)
```

### Pattern 3: Update Views

```xml
<!-- Check for removed/renamed view references -->
<record id="view_form" model="ir.ui.view">
    <field name="inherit_id" ref="stock.view_move_form"/>
    <!-- Update XPath if base view structure changed -->
    <field name="arch" type="xml">
        <xpath expr="//field[@name='product_id']" position="after">
            <field name="custom_field"/>
        </xpath>
    </field>
</record>
```

### Pattern 4: Create Migration Script

```python
# migrations/16.0.1.0.0/pre-migrate.py

def migrate(cr, version):
    """Pre-migration script for 16.0.1.0.0"""
    # Update data before module upgrade
    cr.execute("""
        UPDATE model_table
        SET new_field = old_field
        WHERE new_field IS NULL
    """)

# migrations/16.0.1.0.0/post-migrate.py

def migrate(cr, version):
    """Post-migration script for 16.0.1.0.0"""
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    # Recompute fields
    records = env['model.name'].search([])
    records._compute_field_name()

    # Clean up old data
    old_records = env['old.model'].search([])
    old_records.unlink()
```

### Pattern 5: Update Tests

```python
# Update test imports if needed
from odoo.tests import TransactionCase  # Unchanged

class TestModule(TransactionCase):

    def setUp(self):
        super().setUp()
        # Update test data for new field requirements

    def test_feature(self):
        # Update assertions for new behavior
        record = self.env['model.name'].create({
            'name': 'Test',
            # Add new required fields for Odoo 16
        })
        self.assertTrue(record)
```

## Version-Specific Changes

### Migrating FROM 15.0 TO 16.0

**Major Changes:**
1. Stock accounting methods updated
2. Some JavaScript widgets updated
3. Python 3.10 support added
4. Minor ORM improvements

**Steps:**
1. Update `__manifest__.py` version to `16.0.x.x.x`
2. Test on Odoo 16 test database
3. Check deprecation warnings
4. Update any changed method signatures
5. Test all functionality
6. Create migration scripts if data changes needed

### Migrating FROM 14.0 TO 16.0

**Major Changes:**
- All changes from 14→15 plus 15→16
- Significant OWL (JavaScript framework) changes
- Python 2 completely removed
- Many deprecated features removed

**Steps:**
1. Consider migrating 14→15→16 (two-step migration)
2. Review all custom JavaScript (major changes)
3. Update all deprecated API calls
4. Extensive testing required

## Migration Checklist

- [ ] Update manifest version
- [ ] Check all dependencies compatible with target version
- [ ] Review Odoo release notes for target version
- [ ] Update deprecated method calls
- [ ] Test views render correctly
- [ ] Update method signatures if base methods changed
- [ ] Create migration scripts (pre/post)
- [ ] Update tests
- [ ] Test on copy of production database
- [ ] Check for deprecation warnings in logs
- [ ] Update documentation
- [ ] Test all user workflows
- [ ] Performance test (especially for large datasets)
- [ ] Backup production before upgrade

## Migration Commands

```bash
# Create migration script directory
mkdir -p module_name/migrations/16.0.1.0.0

# Test migration on copy of database
pg_dump production_db > backup.sql
createdb test_migration_db
psql test_migration_db < backup.sql

# Run Odoo with migration
python3 src/odoo-bin -c src/odoo.conf \
    -d test_migration_db \
    -u module_name \
    --stop-after-init

# Check logs for errors
tail -f /var/log/odoo/odoo.log | grep ERROR
```

## Common Migration Issues

### Issue 1: Missing Field Error
```
Error: Field 'xyz' does not exist
```
**Solution:** Add field to model or remove from views

### Issue 2: Method Signature Changed
```
TypeError: method() takes X positional arguments but Y were given
```
**Solution:** Update method call to match new signature

### Issue 3: View Inheritance Broken
```
Error: View inheritance may not use attribute: ...
```
**Solution:** Update XPath or view structure

### Issue 4: Dependencies Not Found
```
Error: Module 'xyz' not found
```
**Solution:** Update dependency version or find replacement

## Testing After Migration

```python
# Run all tests
python3 src/odoo-bin -c src/odoo.conf \
    -d DATABASE_NAME \
    --test-enable \
    --stop-after-init \
    -u module_name

# Check specific functionality
python3 src/odoo-bin shell -c src/odoo.conf -d DATABASE_NAME

>>> env['model.name'].search([]).read()
>>> # Test key functionality manually
```

## Resources

### references/odoo16_changes.md
Comprehensive list of changes introduced in Odoo 16.0 affecting common modules and customizations.

### references/api_changes.md
Detailed API changes by module (stock, account, sale, etc.) between Odoo versions.

### scripts/migration_template.py
Template for creating migration scripts with common patterns and examples.
