---
name: odoo-feature-enhancer
description: Extends existing Odoo 16.0 modules with new features, fields, views, business logic, wizards, and reports. This skill should be used when the user requests enhancements to existing functionality, such as "Add a field to track serial numbers in stock.picking" or "Create a wizard for bulk invoice generation" or "Add a report for vendor bill analysis".
---

# Odoo Feature Enhancer

## Overview

This skill enables extension of existing Odoo 16.0 modules by adding new fields, views, business logic, wizards, reports, and automated actions. It follows module inheritance patterns and ensures proper integration with existing functionality.

## Enhancement Categories

When a user requests a feature enhancement, identify the category and follow the appropriate workflow:

### 1. Field Additions
Add new fields to existing models (stored, computed, related).

### 2. View Modifications
Extend existing views (tree, form, kanban, calendar, pivot, graph) using XML inheritance.

### 3. Business Logic
Add computed methods, onchange handlers, constraints, and custom business rules.

### 4. Wizards
Create transient models for user interactions and batch operations.

### 5. Reports
Generate PDF (QWeb) or Excel reports with custom data aggregation.

### 6. Server Actions
Create automated actions, scheduled actions (cron jobs), and workflow automations.

### 7. Buttons and Actions
Add action buttons to forms and tree views.

## Enhancement Workflow

### Step 1: Identify the Enhancement Type

Ask clarifying questions based on the request:

**For Field Additions:**
- Field technical name (snake_case)
- Field type (Char, Integer, Float, Boolean, Selection, Many2one, One2many, Many2many, Date, Datetime, Text, Html, Binary, Monetary)
- Field label and help text
- Required or optional?
- Computed field or stored?
- Should it appear in specific views?

**For View Modifications:**
- Which view(s) to modify? (form, tree, search, kanban)
- Which model?
- Where to add the element? (header, group, notebook page, after specific field)
- Any conditional visibility?

**For Business Logic:**
- Trigger condition (onchange, compute, constraint, button click)
- Dependencies (which fields trigger the logic)
- Expected behavior

**For Wizards:**
- Wizard purpose (batch update, data export, configuration, etc.)
- Input fields needed
- Target models to affect
- Where to trigger (menu, button on form, action)

**For Reports:**
- Report format (PDF or Excel)
- Data to include
- Grouping and aggregation
- Filters needed

### Step 2: Create or Identify Extension Module

Determine if enhancement goes in:
- New extension module (e.g., `stock_picking_serial_tracking`)
- Existing extension module

If creating new module, provide:
- Module name: `[base_module]_[feature]` (e.g., `stock_picking_enhancements`)
- Dependencies: base module being extended
- Target directory: appropriate `addons-*` folder

### Step 3: Implement the Enhancement

Follow the appropriate implementation pattern below.

## Implementation Patterns

### Pattern 1: Adding Fields to Existing Models

Create model inheritance file:

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class StockPickingInherit(models.Model):
    """Extend stock.picking with additional fields."""

    _inherit = 'stock.picking'

    # Simple stored field
    serial_number = fields.Char(
        string='Serial Number',
        index=True,
        tracking=True,
        help='Serial number for tracking purposes'
    )

    # Selection field
    priority_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority Level', default='medium', required=True)

    # Many2one field
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        default=lambda self: self.env.user,
        tracking=True
    )

    # Computed field (stored)
    total_weight = fields.Float(
        string='Total Weight',
        compute='_compute_total_weight',
        store=True,
        digits=(10, 2)
    )

    # Computed field (non-stored, real-time)
    is_urgent = fields.Boolean(
        string='Is Urgent',
        compute='_compute_is_urgent'
    )

    # Related field (from related record)
    partner_country_id = fields.Many2one(
        'res.country',
        string='Partner Country',
        related='partner_id.country_id',
        store=True,
        readonly=True
    )

    @api.depends('move_line_ids', 'move_line_ids.qty_done', 'move_line_ids.product_id.weight')
    def _compute_total_weight(self):
        """Compute total weight from move lines."""
        for picking in self:
            total = sum(
                line.qty_done * line.product_id.weight
                for line in picking.move_line_ids
                if line.product_id.weight
            )
            picking.total_weight = total

    @api.depends('priority_level', 'scheduled_date')
    def _compute_is_urgent(self):
        """Determine if picking is urgent."""
        from datetime import datetime, timedelta
        for picking in self:
            is_urgent = picking.priority_level == 'urgent'
            if picking.scheduled_date:
                due_soon = picking.scheduled_date <= datetime.now() + timedelta(hours=24)
                is_urgent = is_urgent or due_soon
            picking.is_urgent = is_urgent

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Auto-fill fields when partner changes."""
        if self.partner_id and self.partner_id.user_id:
            self.responsible_id = self.partner_id.user_id

    @api.constrains('serial_number')
    def _check_serial_number(self):
        """Validate serial number format."""
        for picking in self:
            if picking.serial_number and len(picking.serial_number) < 5:
                raise ValidationError('Serial number must be at least 5 characters long!')
```

Create view inheritance to display the new fields:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Extend stock.picking form view -->
    <record id="view_picking_form_inherit" model="ir.ui.view">
        <field name="name">stock.picking.form.inherit</field>
        <field name="model">stock.picking</field>
        <field name="inherit_id" ref="stock.view_picking_form"/>
        <field name="arch" type="xml">
            <!-- Add fields in header -->
            <xpath expr="//header" position="after">
                <div class="alert alert-danger" role="alert" attrs="{'invisible': [('is_urgent', '=', False)]}">
                    <strong>URGENT:</strong> This picking requires immediate attention!
                </div>
            </xpath>

            <!-- Add field after existing field -->
            <xpath expr="//field[@name='partner_id']" position="after">
                <field name="responsible_id"/>
                <field name="serial_number"/>
            </xpath>

            <!-- Add field inside existing group -->
            <xpath expr="//group[@name='other_info']//field[@name='origin']" position="after">
                <field name="priority_level"/>
                <field name="total_weight"/>
            </xpath>

            <!-- Add new notebook page -->
            <xpath expr="//notebook" position="inside">
                <page string="Tracking Info">
                    <group>
                        <field name="serial_number"/>
                        <field name="is_urgent"/>
                        <field name="partner_country_id"/>
                    </group>
                </page>
            </xpath>
        </field>
    </record>

    <!-- Extend tree view -->
    <record id="view_picking_tree_inherit" model="ir.ui.view">
        <field name="name">stock.picking.tree.inherit</field>
        <field name="model">stock.picking</field>
        <field name="inherit_id" ref="stock.view_picking_internal_search"/>
        <field name="arch" type="xml">
            <xpath expr="//tree" position="attributes">
                <attribute name="decoration-danger">is_urgent</attribute>
            </xpath>
            <xpath expr="//field[@name='name']" position="after">
                <field name="serial_number"/>
                <field name="priority_level"/>
                <field name="is_urgent" invisible="1"/>
            </xpath>
        </field>
    </record>

    <!-- Extend search view with filters -->
    <record id="view_picking_search_inherit" model="ir.ui.view">
        <field name="name">stock.picking.search.inherit</field>
        <field name="model">stock.picking</field>
        <field name="inherit_id" ref="stock.view_picking_internal_search"/>
        <field name="arch" type="xml">
            <xpath expr="//search" position="inside">
                <field name="serial_number"/>
                <filter string="Urgent" name="urgent" domain="[('is_urgent', '=', True)]"/>
                <filter string="High Priority" name="high_priority" domain="[('priority_level', '=', 'high')]"/>
                <group expand="0" string="Group By">
                    <filter string="Priority Level" name="priority" context="{'group_by': 'priority_level'}"/>
                </group>
            </xpath>
        </field>
    </record>
</odoo>
```

### Pattern 2: Creating Wizards

Wizard model (transient):

```python
from odoo import models, fields, api
from odoo.exceptions import UserError


class BulkInvoiceWizard(models.TransientModel):
    """Wizard for bulk invoice generation."""

    _name = 'bulk.invoice.wizard'
    _description = 'Bulk Invoice Generation Wizard'

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Leave empty to process all partners'
    )
    date_from = fields.Date(
        string='Date From',
        required=True
    )
    date_to = fields.Date(
        string='Date To',
        required=True
    )
    invoice_date = fields.Date(
        string='Invoice Date',
        required=True,
        default=fields.Date.context_today
    )
    group_by_partner = fields.Boolean(
        string='Group by Partner',
        default=True,
        help='Create one invoice per partner'
    )

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        """Validate date range."""
        if self.date_from > self.date_to:
            raise UserError('Date From must be before Date To!')

    def action_generate_invoices(self):
        """Generate invoices based on wizard parameters."""
        self.ensure_one()

        # Get records to invoice
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('invoice_status', '=', 'to invoice'),
        ]
        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))

        orders = self.env['sale.order'].search(domain)
        if not orders:
            raise UserError('No orders found matching the criteria!')

        # Group by partner if requested
        if self.group_by_partner:
            partners = orders.mapped('partner_id')
            invoices = self.env['account.move']
            for partner in partners:
                partner_orders = orders.filtered(lambda o: o.partner_id == partner)
                invoice = partner_orders._create_invoices()
                invoices |= invoice
        else:
            invoices = orders._create_invoices()

        # Update invoice dates
        invoices.write({'invoice_date': self.invoice_date})

        # Return action to view created invoices
        return {
            'name': 'Generated Invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', invoices.ids)],
            'context': {'create': False},
        }
```

Wizard view:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_bulk_invoice_wizard_form" model="ir.ui.view">
        <field name="name">bulk.invoice.wizard.form</field>
        <field name="model">bulk.invoice.wizard</field>
        <field name="arch" type="xml">
            <form string="Generate Bulk Invoices">
                <group>
                    <group>
                        <field name="partner_id"/>
                        <field name="group_by_partner"/>
                    </group>
                    <group>
                        <field name="date_from"/>
                        <field name="date_to"/>
                        <field name="invoice_date"/>
                    </group>
                </group>
                <footer>
                    <button string="Generate Invoices" name="action_generate_invoices"
                            type="object" class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <!-- Action to open wizard -->
    <record id="action_bulk_invoice_wizard" model="ir.actions.act_window">
        <field name="name">Generate Bulk Invoices</field>
        <field name="res_model">bulk.invoice.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>

    <!-- Menu item -->
    <menuitem id="menu_bulk_invoice_wizard"
              name="Generate Bulk Invoices"
              parent="account.menu_finance"
              action="action_bulk_invoice_wizard"
              sequence="100"/>
</odoo>
```

For more implementation patterns including action buttons, reports (PDF/Excel), and scheduled actions, reference the `references/implementation_patterns.md` file.

## Update Instructions

After implementing enhancements:

1. **Update __manifest__.py** - Add new data files and dependencies
2. **Update security** - Add access rights for new models
3. **Update module** - Run with `-u module_name`
4. **Test** - Verify all functionality works

```bash
# Update module
python3 /Users/jamshid/PycharmProjects/Siafa/src/odoo-bin \
    -c /Users/jamshid/PycharmProjects/Siafa/src/odoo.conf \
    -d DATABASE_NAME \
    -u module_name

# Run tests if available
python3 /Users/jamshid/PycharmProjects/Siafa/src/odoo-bin \
    -c /Users/jamshid/PycharmProjects/Siafa/src/odoo.conf \
    -d DATABASE_NAME \
    --test-enable \
    --stop-after-init \
    -u module_name
```

## Resources

### references/xpath_patterns.md
Comprehensive collection of XPath expressions for view inheritance - how to add fields before/after elements, replace content, add attributes, etc.

### references/field_types.md
Complete reference of Odoo field types with examples and common attributes for each type.

### references/implementation_patterns.md
Additional implementation patterns for action buttons, PDF reports, Excel reports, and scheduled actions (cron jobs).
