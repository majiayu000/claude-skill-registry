---
name: odoo-test-creator
description: Creates comprehensive test suites for Odoo 16.0 modules following Siafa project standards. This skill should be used when creating tests for Odoo modules, such as "Create tests for this module" or "Generate test cases for stock_location_usage_restriction" or "Add unit tests to validate this functionality". The skill provides test templates, patterns, and best practices specific to Odoo 16.0 Enterprise with knowledge of database constraints and common pitfalls in the Siafa codebase.
---

# Odoo Test Creator

## Overview

Create production-ready test suites for Odoo 16.0 Enterprise modules that follow Siafa project standards, handle database constraints properly, and provide comprehensive test coverage.

## When to Use This Skill

Use this skill when:
- Creating tests for new Odoo modules
- Adding test coverage to existing modules
- Validating model logic, constraints, and workflows
- Testing inherited/extended Odoo models
- Ensuring compliance with Siafa testing standards

## Test Creation Workflow

### Step 1: Analyze Module Structure

Examine the module to understand what needs testing:

1. **Identify Components to Test:**
   - Models (new models or inherited models)
   - Computed fields and @api.depends
   - Constraints (@api.constrains and _sql_constraints)
   - Onchange methods (@api.onchange)
   - Business logic methods
   - State transitions and workflows
   - Wizards and transient models
   - Reports (if applicable)

2. **Review Module Dependencies:**
   - Check `__manifest__.py` for dependencies
   - Identify which models from dependencies will be used
   - Plan to use existing records when possible

3. **Check for Special Requirements:**
   - Database constraints (NOT NULL, UNIQUE)
   - Multi-company considerations
   - Access rights and permissions
   - Integration points with other modules

### Step 2: Set Up Test File Structure

Create the test file following Siafa standards:

```python
# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError


class TestModuleName(TransactionCase):
    """Test cases for module_name functionality."""

    def setUp(self):
        """Set up test data."""
        super().setUp()

        # Initialize model references
        self.Model = self.env['model.name']

        # Set up test data (Step 3)
```

**Critical Import Pattern:**
- ✅ Use `from odoo.tests.common import TransactionCase`
- ❌ NOT `from odoo.tests import TransactionCase`

### Step 3: Set Up Test Data

Use the appropriate pattern based on database constraints:

#### Pattern A: Use Existing Records (Preferred)

Avoid database constraint issues by using existing records:

```python
def setUp(self):
    super().setUp()

    self.Model = self.env['model.name']

    # Use existing records from database
    self.warehouse = self.env['stock.warehouse'].search([], limit=1)
    if not self.warehouse:
        self.skipTest("No warehouse available for testing")

    self.product = self.env['product.product'].search([('type', '=', 'product')], limit=1)
    if not self.product:
        self.skipTest("No storable product available for testing")

    self.partner = self.env['res.partner'].search([], limit=1)
    if not self.partner:
        self.skipTest("No partner available for testing")
```

**When to use:** For models with complex database constraints (products, partners, companies).

#### Pattern B: Create with .sudo() (When Necessary)

Create new records when specific test data is required:

```python
def setUp(self):
    super().setUp()

    self.Model = self.env['model.name']

    # Create test data with .sudo() to bypass permissions
    self.vendor = self.env['res.partner'].sudo().create({
        'name': 'Test Vendor',
        'is_company': True,
        'supplier_rank': 1,
    })

    self.product = self.env['product.product'].sudo().create({
        'name': 'Test Product',
        'type': 'product',
        'purchase_method': 'receive',
        'list_price': 100.0,
        'standard_price': 80.0,
    })
```

**When to use:** When specific field values are required for tests or existing records may not have the right attributes.

#### Pattern C: Class-Level Setup (For Shared Data)

Use `setUpClass` for data shared across all test methods:

```python
@classmethod
def setUpClass(cls):
    """Set up test data shared across all test methods."""
    super().setUpClass()

    cls.vendor = cls.env['res.partner'].sudo().create({
        'name': 'Test Vendor',
        'is_company': True,
    })
```

**When to use:** For immutable test data that doesn't change between tests (saves database operations).

### Step 4: Write Test Methods

Create test methods following these guidelines:

#### Test Naming Convention

```python
def test_01_descriptive_name(self):
    """Test description in docstring."""
    pass

def test_02_another_scenario(self):
    """Test another scenario."""
    pass
```

**Numbering:** Use `01`, `02`, etc. to control execution order.

#### Test Coverage Areas

Create tests for each component identified in Step 1:

**A. CRUD Operations**

```python
def test_01_create_record(self):
    """Test creating a new record with valid data."""
    record = self.Model.create({
        'name': 'Test Record',
        'partner_id': self.partner.id,
    })

    self.assertTrue(record)
    self.assertEqual(record.name, 'Test Record')
    self.assertEqual(record.state, 'draft')

def test_02_update_record(self):
    """Test updating an existing record."""
    record = self.Model.create({
        'name': 'Test Record',
        'partner_id': self.partner.id,
    })

    record.write({'name': 'Updated Record'})

    self.assertEqual(record.name, 'Updated Record')
```

**B. Computed Fields**

```python
def test_03_computed_field(self):
    """Test computed field calculation."""
    record = self.Model.create({
        'name': 'Test Record',
        'quantity': 10,
        'unit_price': 5.0,
    })

    self.assertEqual(record.total_amount, 50.0)

    # Test recomputation on dependency change
    record.write({'quantity': 20})
    self.assertEqual(record.total_amount, 100.0)
```

**C. Constraints**

```python
def test_04_constraint_validation(self):
    """Test constraint prevents invalid data."""
    record = self.Model.create({
        'name': 'Test Record',
        'partner_id': self.partner.id,
    })

    with self.assertRaises(ValidationError) as context:
        record.write({'amount': -10.0})

    self.assertIn('must be positive', str(context.exception).lower())
```

**D. Onchange Methods**

```python
def test_05_onchange_method(self):
    """Test onchange method updates dependent fields."""
    record = self.Model.new({
        'name': 'Test Record',
    })

    record.partner_id = self.partner
    record._onchange_partner_id()

    # Verify onchange updated related fields
    # self.assertEqual(record.expected_field, expected_value)
```

**E. State Transitions**

```python
def test_06_state_transition(self):
    """Test state transition workflow."""
    record = self.Model.create({
        'name': 'Test Record',
        'partner_id': self.partner.id,
    })

    self.assertEqual(record.state, 'draft')

    record.action_confirm()
    self.assertEqual(record.state, 'confirmed')

    # Test invalid transition
    with self.assertRaises(UserError) as context:
        record.action_confirm()  # Already confirmed

    self.assertIn('Cannot confirm', str(context.exception))
```

**F. Inheritance/Extension Tests**

For modules that inherit existing models:

```python
def test_07_inherited_method_override(self):
    """Test overridden method applies custom logic."""
    location = self.Location.create({
        'name': 'Test Location',
        'usage': 'internal',
        'location_id': self.parent_location.id,
    })

    # Create stock move using this location
    self.StockMove.create({
        'name': 'Test Move',
        'product_id': self.product.id,
        'product_uom_qty': 10,
        'product_uom': self.product.uom_id.id,
        'location_id': location.id,
        'location_dest_id': self.parent_location.id,
    })

    # Test that custom validation prevents usage change
    with self.assertRaises(UserError) as context:
        location.write({'usage': 'inventory'})

    self.assertIn('Cannot change the usage type', str(context.exception))
```

### Step 5: Handle Common Pitfalls

Apply fixes for known issues in the Siafa codebase:

#### Pitfall 1: Database Constraints

**Problem:** Creating products fails with "null value in column 'sale_line_warn' violates not-null constraint"

**Solution:** Use existing products:
```python
self.product = self.env['product.product'].search([('type', '=', 'product')], limit=1)
```

#### Pitfall 2: HTML Field Comparisons

**Problem:** HTML fields return `Markup` objects: `Markup('<p>Text</p>') != 'Text'`

**Solution:** Use non-HTML fields or convert to string:
```python
# Instead of comment field
self.assertEqual(record.barcode, 'TEST001')

# Or convert to string
self.assertIn('expected text', str(record.html_field))
```

#### Pitfall 3: Permission Errors

**Problem:** Tests fail with access rights errors.

**Solution:** Use `.sudo()` when creating test data:
```python
self.partner = self.env['res.partner'].sudo().create({...})
```

#### Pitfall 4: Incorrect Super() Call

**Problem:** Using old-style `super(ClassName, self).setUp()`

**Solution:** Use modern syntax:
```python
super().setUp()  # ✅ Correct
```

### Step 6: Run and Validate Tests

Execute tests and verify results:

```bash
# Run tests during module update
python3 src/odoo-bin -c src/odoo.conf -d DATABASE_NAME \
    --test-enable --stop-after-init \
    -u MODULE_NAME

# Run with verbose output
python3 src/odoo-bin -c src/odoo.conf -d DATABASE_NAME \
    --test-enable --stop-after-init \
    --log-level=test \
    -u MODULE_NAME
```

**Expected Output:**
```
INFO MODULE_NAME: 0 failed, 0 error(s) of N tests when loading database 'DATABASE_NAME'
```

**If tests fail:**
1. Read the full traceback carefully
2. Check for database constraint violations
3. Verify test data setup is correct
4. Ensure imports are correct
5. Review field types (especially HTML fields)

### Step 7: Document Tests

Add comprehensive docstrings to each test method:

```python
def test_prevent_usage_change_with_moves(self):
    """
    Test that location usage cannot be changed when moves exist.

    This test verifies that the module prevents changing a location's
    usage type after it has been used in stock movements, protecting
    data integrity.
    """
    # Test implementation
```

## Resources

### references/test_patterns.md

Comprehensive documentation of:
- Test infrastructure patterns
- Common setup patterns for different scenarios
- Database constraint handling strategies
- Test organization best practices
- Assertion patterns
- Complete list of common pitfalls and solutions
- Running tests with various options

Load this reference when:
- Creating complex test scenarios
- Handling database constraints
- Troubleshooting test failures
- Learning Siafa-specific testing patterns

### assets/test_model_basic.py

Template for testing basic model operations:
- CRUD operations (Create, Read, Update, Delete)
- Computed field testing
- Onchange method testing
- Constraint validation
- State transitions
- Search operations

Use as starting point for new model tests.

### assets/test_model_constraints.py

Template for testing constraints:
- Python constraints (@api.constrains)
- SQL constraints (_sql_constraints)
- Required field validation
- Domain constraints
- Dependent field constraints
- Conditional constraints
- Cascading constraints

Use when module has complex validation logic.

### assets/test_model_inheritance.py

Template for testing model inheritance and extensions:
- New field validation
- Overridden method testing
- Super() call behavior
- Added constraints
- Computed field extensions
- Onchange extensions
- Backward compatibility

Use when module extends existing Odoo models.

## Best Practices

1. **Always use existing records when possible** to avoid database constraints
2. **Test both success and failure cases** for comprehensive coverage
3. **Verify error messages** when testing exceptions
4. **Use .sudo() for test data creation** to bypass permission issues
5. **Add descriptive docstrings** to every test method
6. **Number test methods** for predictable execution order
7. **Keep tests isolated** - each test should work independently
8. **Test edge cases** - empty data, maximum values, invalid combinations
9. **Follow naming conventions** - clear, descriptive test names
10. **Run tests frequently** during development to catch issues early

## Example: Complete Test File

For reference, see `/Users/jamshid/PycharmProjects/Siafa/odoo16e_simc/addons-stock/stock_location_usage_restriction/tests/test_stock_location_usage_restriction.py`

This file demonstrates:
- Proper imports (`from odoo.tests.common import TransactionCase`)
- Using existing records (`self.product = self.Product.search(...)`)
- Comprehensive test coverage (7 test methods)
- Exception testing with message validation
- Proper super() call (`super().setUp()`)
- Avoiding HTML field comparison issues
