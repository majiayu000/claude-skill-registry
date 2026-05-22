---
name: odoo-code-reviewer
description: Reviews Odoo 16.0 code for best practices, security issues, performance problems, and OCA guidelines compliance. This skill should be used when the user requests code review, such as "Review this code" or "Check this module for issues" or "Is this code optimized?" or "Security review needed for this module".
---

# Odoo Code Reviewer

## Overview

This skill provides comprehensive code review for Odoo 16.0 modules, checking for security vulnerabilities, performance issues, OCA guideline compliance, and general best practices.

## Review Categories

### 1. Security Issues
SQL injection, XSS vulnerabilities, improper sudo() usage, missing input validation.

### 2. Performance Problems
N+1 queries, inefficient searches, unnecessary database operations.

### 3. OCA Guidelines Compliance
Code style, structure, naming conventions, documentation.

### 4. Best Practices
Proper API usage, error handling, logging, testing.

### 5. Maintainability
Code organization, readability, documentation, modularity.

## Review Process

### Step 1: Identify Review Scope

Determine what to review:
- Complete module
- Specific model files
- View files
- Security configuration
- Specific functionality

### Step 2: Systematic Review

Check each category systematically following the patterns below.

## Review Patterns

### Security Review Checklist

**1. SQL Injection Risk**
```python
# BAD - SQL injection vulnerability
self.env.cr.execute("SELECT * FROM table WHERE id = %s" % record_id)

# GOOD - Parameterized query
self.env.cr.execute("SELECT * FROM table WHERE id = %s", (record_id,))
```

**2. XSS Vulnerabilities**
```python
# BAD - Unescaped HTML field
description = fields.Char(string='Description')

# GOOD - Use Text or Html field with sanitization
description = fields.Html(string='Description', sanitize=True)
```

**3. Improper sudo() Usage**
```python
# BAD - sudo() without justification
records = self.env['model'].sudo().search([])

# GOOD - Check permissions properly
if self.env.user.has_group('base.group_system'):
    records = self.env['model'].search([])
```

**4. Missing Input Validation**
```python
# BAD - No validation
def process(self, value):
    return int(value)

# GOOD - Proper validation
def process(self, value):
    if not value or not isinstance(value, (int, str)):
        raise ValueError('Invalid value')
    try:
        return int(value)
    except ValueError:
        raise ValidationError('Value must be a valid integer')
```

### Performance Review Checklist

**1. N+1 Query Problem**
```python
# BAD - N+1 queries
for order in orders:
    print(order.partner_id.name)  # Database query for each iteration

# GOOD - Prefetch
for order in orders:
    pass  # partner_id prefetched automatically
print([o.partner_id.name for o in orders])

# EVEN BETTER - Explicit prefetch
orders = orders.with_prefetch(['partner_id'])
```

**2. Inefficient Searches**
```python
# BAD - Search in loop
for partner in partners:
    orders = self.env['sale.order'].search([('partner_id', '=', partner.id)])

# GOOD - Single search
orders = self.env['sale.order'].search([('partner_id', 'in', partners.ids)])
```

**3. Unnecessary Database Operations**
```python
# BAD - Multiple writes
for line in lines:
    line.write({'processed': True})

# GOOD - Batch write
lines.write({'processed': True})
```

**4. Inefficient Computed Fields**
```python
# BAD - Not stored, recalculated every time
total = fields.Float(compute='_compute_total')

# GOOD - Stored with proper depends
total = fields.Float(compute='_compute_total', store=True)

@api.depends('line_ids.amount')
def _compute_total(self):
    for record in self:
        record.total = sum(record.line_ids.mapped('amount'))
```

### OCA Guidelines Checklist

**1. Naming Conventions**
- Module: `snake_case` (e.g., `stock_batch_tracking`)
- Model: `model.name` (e.g., `stock.batch`)
- Fields: `snake_case`
- Methods: `snake_case` with verb prefix
- Private methods: `_method_name`

**2. Import Order**
```python
# Standard library
import logging
from datetime import datetime

# Third-party
from lxml import etree

# Odoo
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
```

**3. Docstrings**
```python
class Model(models.Model):
    """Brief description of model."""

    _name = 'model.name'
    _description = 'Model Description'

    def method(self, param):
        """Brief description of method.

        Args:
            param: Description of parameter

        Returns:
            Description of return value
        """
        pass
```

**4. Field Attributes**
```python
# GOOD - Complete field definition
name = fields.Char(
    string='Name',
    required=True,
    index=True,
    tracking=True,
    help='Detailed help text'
)
```

### Best Practices Checklist

**1. Error Handling**
```python
# BAD - Generic exception
try:
    value = int(data)
except:
    pass

# GOOD - Specific exception with logging
try:
    value = int(data)
except ValueError as e:
    _logger.error('Invalid data: %s', e)
    raise ValidationError('Please provide a valid number')
```

**2. Logging**
```python
# BAD - Print statements
print("Processing record", record.id)

# GOOD - Proper logging
_logger.info('Processing record %s', record.id)
_logger.debug('Record data: %s', record.read())
```

**3. Method Decorators**
```python
# Ensure proper decorator usage
@api.depends('field1', 'field2')  # For computed fields
def _compute_field(self): pass

@api.onchange('field1')  # For onchange methods
def _onchange_field(self): pass

@api.constrains('field1')  # For constraints
def _check_field(self): pass

@api.model  # For class-level methods
def create_from_ui(self, vals): pass
```

**4. Transaction Safety**
```python
# BAD - Commit in method
def method(self):
    self.process()
    self.env.cr.commit()  # Don't do this!

# GOOD - Let Odoo handle transactions
def method(self):
    self.process()
    # Transaction committed automatically
```

## Review Output Format

Provide review results in this format:

### Critical Issues
- **Security**: List any security vulnerabilities
- **Data Loss Risk**: Operations that could cause data loss

### High Priority Issues
- **Performance**: Major performance problems
- **Incorrect Logic**: Business logic errors

### Medium Priority Issues
- **OCA Compliance**: Guideline violations
- **Code Quality**: Maintainability issues

### Low Priority Issues
- **Style**: Minor style issues
- **Documentation**: Missing or incomplete docs

### Recommendations
- Suggested improvements
- Best practice suggestions
- Refactoring opportunities

## Common Anti-Patterns

1. **Using search() in loops**
2. **Not using prefetch**
3. **Missing translations** (`string` without `_()` for translatable text)
4. **Hardcoded values** instead of configuration
5. **Incorrect sudo() usage**
6. **Missing input validation**
7. **Poor error messages**
8. **Inefficient computed fields**
9. **Missing access rights**
10. **No unit tests**

## Example Review

```python
# CODE BEING REVIEWED
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_weight = fields.Float(compute='_compute_weight')

    def _compute_weight(self):
        for order in self:
            weight = 0
            for line in order.order_line:
                product = self.env['product.product'].search([('id', '=', line.product_id.id)])
                weight += product.weight * line.product_uom_qty
            order.total_weight = weight
```

**Review Findings:**

**HIGH - Performance Issues:**
1. Unnecessary search in loop (line 10)
   - FIX: Use `line.product_id.weight` directly
2. Not storing computed field
   - FIX: Add `store=True` and `@api.depends` decorator

**MEDIUM - Best Practices:**
1. Missing `@api.depends` decorator
   - FIX: Add `@api.depends('order_line.product_id.weight', 'order_line.product_uom_qty')`
2. Variable could be clearer
   - FIX: Rename `weight` to `total_weight`

**Improved Code:**
```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_weight = fields.Float(
        string='Total Weight',
        compute='_compute_weight',
        store=True,
        help='Total weight of all order lines'
    )

    @api.depends('order_line.product_id.weight', 'order_line.product_uom_qty')
    def _compute_weight(self):
        """Compute total weight from order lines."""
        for order in self:
            order.total_weight = sum(
                line.product_id.weight * line.product_uom_qty
                for line in order.order_line
            )
```

## Resources

### references/oca_guidelines.md
Complete OCA (Odoo Community Association) coding guidelines for Odoo modules.

### references/security_checklist.md
Comprehensive security checklist for Odoo development.

### references/performance_patterns.md
Common performance patterns and anti-patterns with examples and fixes.
