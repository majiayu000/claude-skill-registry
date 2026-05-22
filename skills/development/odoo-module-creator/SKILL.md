---
name: odoo-module-creator
description: Creates complete Odoo 16.0 modules with proper structure, manifests, models, views, and security. This skill should be used when the user requests creation of a new Odoo module, such as "Create a new module for inventory tracking" or "I need a new POS customization module" or "Generate module structure for vendor management".
---

# Odoo Module Creator

## Overview

This skill enables creation of complete, production-ready Odoo 16.0 Enterprise modules with proper directory structure, manifest files, models, views, security configurations, and documentation. It follows OCA guidelines and Siafa project standards.

## Module Creation Workflow

### Step 1: Gather Module Requirements

Ask clarifying questions to collect essential information:

1. **Module technical name** (snake_case format, e.g., `stock_batch_tracking`, `pos_custom_receipt`)
2. **Module display name** (human-readable, e.g., "Stock Batch Tracking", "POS Custom Receipt")
3. **Module purpose** (1-2 sentence description of functionality)
4. **Module category** (select from: Sales, Inventory, Accounting, Point of Sale, Human Resources, Manufacturing, Purchases, Warehouse, Website, etc.)
5. **Dependencies** (base modules required, e.g., `stock`, `account`, `point_of_sale`)
6. **Module type** (see Module Types section below)
7. **Target addon directory** (e.g., `addons-stock`, `addons-pos`, `addons-account`)

### Step 2: Determine Module Type

Identify which type of module to create based on the purpose:

**A. Simple Model Module** - CRUD operations for a new business entity
- Creates new models with fields and views
- Example: Customer feedback tracking, equipment registry

**B. Extension Module** - Extends existing Odoo models
- Inherits and adds fields/methods to existing models
- Example: Add serial number tracking to stock.picking

**C. POS Customization** - Point of Sale enhancements
- Extends POS models, screens, or receipts
- Example: Custom receipt format, loyalty points integration

**D. Stock/Inventory Enhancement** - Warehouse and inventory features
- Stock valuation, warehouse operations, batch tracking
- Example: Inter-warehouse transit, GRN-invoice linking

**E. Accounting Customization** - Financial module extensions
- Account moves, vendor bills, analytic accounting
- Example: Multi-dimensional analytics, custom invoicing

**F. Report Module** - Custom reports (PDF, Excel)
- QWeb templates, data aggregation, export functionality
- Example: Sales analysis, inventory valuation reports

**G. Integration Module** - External API/service connectors
- REST API clients, webhooks, data synchronization
- Example: Beatroute connector, payment gateway integration

**H. Widget/UI Customization** - Frontend enhancements
- JavaScript widgets, custom views, web controllers
- Example: Kanban view customizations, dashboard widgets

### Step 3: Generate Module Structure

Create the complete directory structure with all required files:

```
module_name/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── [model_files].py
├── views/
│   ├── [model]_views.xml
│   └── menu_views.xml
├── security/
│   ├── security_groups.xml (if needed)
│   └── ir.model.access.csv
├── data/ (optional)
│   └── data.xml
├── wizards/ (if needed)
│   ├── __init__.py
│   └── [wizard_name].py
├── report/ (if reports needed)
│   ├── __init__.py
│   ├── [report_name].py
│   └── templates/
│       └── [report_template].xml
├── static/
│   ├── description/
│   │   ├── icon.png
│   │   └── index.html
│   └── src/ (for JS/CSS if needed)
│       ├── js/
│       └── css/
└── tests/ (recommended)
    ├── __init__.py
    └── test_[module].py
```

### Step 4: Generate __manifest__.py

Create manifest with standard metadata:

```python
{
    'name': '[Module Display Name]',
    'version': '16.0.1.0.0',
    'category': '[Category]',
    'summary': '[Brief one-line description]',
    'description': """
[Detailed multi-line description of module functionality]

Key Features:
- Feature 1
- Feature 2
- Feature 3
    """,
    'author': 'Jamshid K',
    'website': 'https://siafadates.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        # Additional dependencies
    ],
    'data': [
        'security/security_groups.xml',  # Load first
        'security/ir.model.access.csv',
        'views/[model]_views.xml',
        'views/menu_views.xml',
        'data/data.xml',  # If needed
        'report/templates/[report].xml',  # If needed
    ],
    'assets': {  # If JS/CSS needed
        'web.assets_backend': [
            'module_name/static/src/js/*.js',
            'module_name/static/src/css/*.css',
        ],
    },
    'demo': [],  # Demo data if applicable
    'installable': True,
    'auto_install': False,
    'application': False,  # True for standalone apps
}
```

### Step 5: Generate Model Files

Create model files following Odoo ORM best practices:

```python
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class ModelName(models.Model):
    """Description of the model."""

    _name = 'module.model'
    _description = 'Model Description'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # If needed
    _order = 'create_date desc'

    # Fields
    name = fields.Char(
        string='Name',
        required=True,
        index=True,
        tracking=True,
        help='Primary identifier for this record'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this record will be hidden'
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    # Relational fields
    partner_id = fields.Many2one('res.partner', string='Partner')
    line_ids = fields.One2many('module.model.line', 'parent_id', string='Lines')

    # Computed fields
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True
    )

    # Constraints
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name, company_id)', 'Name must be unique per company!'),
    ]

    @api.depends('line_ids', 'line_ids.amount')
    def _compute_total_amount(self):
        """Compute total amount from lines."""
        for record in self:
            record.total_amount = sum(record.line_ids.mapped('amount'))

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Update fields when partner changes."""
        if self.partner_id:
            # Logic here
            pass

    @api.constrains('total_amount')
    def _check_total_amount(self):
        """Validate total amount is positive."""
        for record in self:
            if record.total_amount < 0:
                raise ValidationError('Total amount must be positive!')

    def action_confirm(self):
        """Confirm the record."""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError('Only draft records can be confirmed!')
        self.write({'state': 'confirmed'})
        _logger.info('Record %s confirmed by user %s', self.name, self.env.user.name)
```

### Step 6: Generate View Files

Create XML view definitions:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Tree View -->
    <record id="view_model_tree" model="ir.ui.view">
        <field name="name">module.model.tree</field>
        <field name="model">module.model</field>
        <field name="arch" type="xml">
            <tree string="Model Name">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="state" decoration-info="state == 'draft'"
                       decoration-success="state == 'done'"/>
                <field name="total_amount" sum="Total"/>
                <field name="company_id" groups="base.group_multi_company"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_model_form" model="ir.ui.view">
        <field name="name">module.model.form</field>
        <field name="model">module.model</field>
        <field name="arch" type="xml">
            <form string="Model Name">
                <header>
                    <button name="action_confirm" string="Confirm" type="object"
                            class="oe_highlight" states="draft"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="draft,confirmed,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="Name..."/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id"/>
                            <field name="company_id" groups="base.group_multi_company"/>
                        </group>
                        <group>
                            <field name="total_amount"/>
                            <field name="active"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Lines">
                            <field name="line_ids">
                                <tree editable="bottom">
                                    <field name="name"/>
                                    <field name="amount"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_model_search" model="ir.ui.view">
        <field name="name">module.model.search</field>
        <field name="model">module.model</field>
        <field name="arch" type="xml">
            <search string="Search Model">
                <field name="name"/>
                <field name="partner_id"/>
                <filter string="Draft" name="draft" domain="[('state', '=', 'draft')]"/>
                <filter string="Done" name="done" domain="[('state', '=', 'done')]"/>
                <separator/>
                <filter string="Archived" name="inactive" domain="[('active', '=', False)]"/>
                <group expand="0" string="Group By">
                    <filter string="Partner" name="partner" context="{'group_by': 'partner_id'}"/>
                    <filter string="Status" name="state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Action -->
    <record id="action_model" model="ir.actions.act_window">
        <field name="name">Model Name</field>
        <field name="res_model">module.model</field>
        <field name="view_mode">tree,form</field>
        <field name="context">{}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first record!
            </p>
            <p>
                Click the create button to add a new record.
            </p>
        </field>
    </record>
</odoo>
```

### Step 7: Generate Security Files

Create security groups (if needed):

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="module_category" model="ir.module.category">
        <field name="name">Module Category</field>
        <field name="sequence">100</field>
    </record>

    <record id="group_user" model="res.groups">
        <field name="name">User</field>
        <field name="category_id" ref="module_category"/>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    </record>

    <record id="group_manager" model="res.groups">
        <field name="name">Manager</field>
        <field name="category_id" ref="module_category"/>
        <field name="implied_ids" eval="[(4, ref('group_user'))]"/>
    </record>
</odoo>
```

Create access rights CSV:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_model_user,module.model.user,model_module_model,group_user,1,1,1,0
access_model_manager,module.model.manager,model_module_model,group_manager,1,1,1,1
```

### Step 8: Generate Tests (Recommended)

**Use the `odoo-test-creator` skill** to create comprehensive test suites for the module. The odoo-test-creator skill provides:
- Test templates for different module types (basic models, constraints, inheritance)
- Best practices specific to Siafa project standards
- Solutions to common testing pitfalls (database constraints, HTML fields, permissions)
- Proper import patterns and setUp methods

To create tests with the odoo-test-creator skill, simply invoke:

```
Use the odoo-test-creator skill to create tests for [module_name]
```

The skill will:
1. Analyze the module structure to determine what needs testing
2. Select appropriate test templates based on module type
3. Generate comprehensive test methods for CRUD operations, constraints, computed fields, and business logic
4. Handle database constraints properly (using existing records vs. creating with .sudo())
5. Apply Siafa-specific patterns and best practices

**Quick Test Example** (if not using the skill):

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestModel(TransactionCase):
    """Test cases for module.model"""

    def setUp(self):
        """Set up test data"""
        super().setUp()

        self.Model = self.env['module.model']

        # Use existing records when possible
        self.partner = self.env['res.partner'].search([], limit=1)
        if not self.partner:
            self.skipTest("No partner available for testing")

    def test_01_create_model(self):
        """Test creating a model record"""
        record = self.Model.create({
            'name': 'Test Record',
            'partner_id': self.partner.id,
        })
        self.assertTrue(record)
        self.assertEqual(record.state, 'draft')

    def test_02_constraint_validation(self):
        """Test constraint validation"""
        record = self.Model.create({
            'name': 'Test Record',
            'partner_id': self.partner.id,
        })
        with self.assertRaises(UserError) as context:
            record.write({'invalid_field': 'invalid_value'})

        self.assertIn('expected error', str(context.exception))
```

**Important:** For production modules, always use the `odoo-test-creator` skill to ensure comprehensive test coverage and proper handling of Siafa-specific constraints.



## Code Standards and Best Practices

Follow these standards when generating module code:

1. **Naming Conventions**
   - Module name: `snake_case` (e.g., `stock_batch_tracking`)
   - Model name: `module.model` (e.g., `stock.batch.tracking`)
   - Fields: `snake_case` (e.g., `batch_number`, `expiry_date`)
   - Methods: `snake_case` with verb prefix (e.g., `action_confirm`, `_compute_total`)
   - XML IDs: `view_model_type` (e.g., `view_batch_tracking_form`)

2. **Import Order**
   ```python
   # Standard library
   import logging
   from datetime import datetime

   # Odoo imports
   from odoo import models, fields, api, _
   from odoo.exceptions import UserError, ValidationError
   from odoo.tools import float_compare, float_is_zero
   ```

3. **Field Attributes**
   - Always provide `string` parameter
   - Add `help` text for complex fields
   - Use `tracking=True` for important fields
   - Set `index=True` for searchable fields
   - Include `company_id` for multi-company support

4. **Method Decorators**
   - Use `@api.depends()` for computed fields
   - Use `@api.onchange()` for onchange methods
   - Use `@api.constrains()` for validation
   - Use `@api.model` for class-level methods

5. **Error Handling**
   - Use `UserError` for user-facing errors
   - Use `ValidationError` for constraint violations
   - Always log important actions with `_logger`

6. **Security**
   - Always create access rights CSV
   - Use security groups for sensitive operations
   - Add record rules if row-level security needed
   - Test with different user permissions

## Module Type Templates

Reference the `assets/templates/` directory for complete templates by module type:
- `simple_model/` - Basic CRUD module
- `extension/` - Inheriting existing models
- `pos_custom/` - POS customizations
- `stock_enhancement/` - Inventory features
- `report_module/` - Custom reports

## Resources

### assets/templates/
Contains complete module templates for different module types. Use these as starting points and customize based on specific requirements.

### assets/icon.png
Default module icon. Replace with custom icon if needed (PNG, 128x128px recommended).

### assets/index.html
Module description HTML template for the Apps menu.
