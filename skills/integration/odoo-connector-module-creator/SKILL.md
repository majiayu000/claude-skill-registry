---
name: odoo-connector-module-creator
description: Creates and enhances Odoo 16.0 connector modules that integrate with external systems (e-commerce, logistics, accounting, CRM) using the `generic_connector` framework
---

# Odoo Connector Module Creator and Enhancer

## Description

Creates and enhances Odoo 16.0 connector modules that integrate with external systems (e-commerce, logistics, accounting, CRM) using the `generic_connector` framework. This skill handles:

- **New Connector Creation**: Build complete integration modules for Shopify, WooCommerce, Amazon, or any external API
- **Connector Enhancement**: Add features like inventory sync, webhook support, or new entity types to existing connectors
- **Troubleshooting**: Debug sync issues, API errors, authentication problems, and queue job failures
- **Architecture Implementation**: Properly implement binding models, adapters, mappers, and importers/exporters

The skill leverages production-tested patterns from reference connectors (zid_connector_v2, beatroute_connector) and provides automated scripts for generating boilerplate code.

## Overview

Create production-ready Odoo 16.0 connector modules that integrate with external systems using the `generic_connector` framework. Handle creation of new connectors, enhancement of existing connectors, troubleshooting sync issues, and debugging integration problems.

## When to Use This Skill

Use this skill when the user requests:
- **Creating new connectors**: "Create a Shopify connector", "Build WooCommerce integration", "Connect to Amazon API"
- **Enhancing connectors**: "Add inventory sync to zid_connector", "Implement webhooks for orders", "Add product export"
- **Adding entities**: "Add customer sync to the connector", "Import invoices from the external system"
- **Troubleshooting**: "Orders aren't importing", "Webhook signature verification failing", "Fix sync errors"
- **Debugging**: "Why is the API returning 401?", "Products are duplicating", "Queue jobs not running"

## Key Concepts

### Generic Connector Framework

All connector modules extend `generic_connector`, which provides:

1. **Backend Model** - Configuration and orchestration
2. **Binding Models** - Link Odoo records to external entities
3. **Adapter Component** - HTTP client for API communication
4. **Mapper Components** - Data transformation (import/export)
5. **Importer/Exporter Components** - Sync logic
6. **Webhook System** - Real-time event processing
7. **Queue Job Integration** - Async operations

### Reference Code

Three production connectors serve as references:
- `/Users/jamshid/PycharmProjects/Siafa/odoo16e_simc/addons-connector/generic_connector` - Base framework
- `/Users/jamshid/PycharmProjects/Siafa/odoo16e_simc/addons-connector/zid_connector_v2` - E-commerce example
- `/Users/jamshid/PycharmProjects/Siafa/odoo16e_simc/addons-connector/beatroute_connector` - Logistics example

## Workflow

### Creating a New Connector

When the user requests a new connector:

**Step 1: Gather Requirements**
- External system name (e.g., "Shopify", "WooCommerce")
- Connector type: ecommerce, logistics, accounting, crm
- Entities to sync: products, orders, customers, inventory
- Sync direction: import, export, or bidirectional
- Authentication method: API key, OAuth, basic auth
- API documentation URL (if available)

**Step 2: Initialize Module**
```bash
# Use the init_connector.py script
python3 scripts/init_connector.py <connector_name> --path <output_path> --type <connector_type>

# Example:
python3 scripts/init_connector.py shopify --path ~/odoo/addons --type ecommerce
```

**Step 3: Review Generated Structure**

The script creates:
```
shopify_connector/
├── __manifest__.py              # Module metadata
├── __init__.py                  # Python imports
├── models/
│   ├── backend.py              # Backend configuration
│   ├── adapter.py              # API client
│   ├── product_binding.py      # Product sync
│   └── __init__.py
├── views/
│   ├── backend_views.xml       # Backend UI
│   ├── binding_views.xml       # Binding UI
│   └── menu_views.xml          # Menu structure
├── security/
│   ├── security.xml            # Access groups
│   └── ir.model.access.csv     # Access rules
├── wizards/
│   ├── sync_wizard.py          # Manual sync wizard
│   └── __init__.py
├── data/
│   ├── ir_cron_data.xml        # Scheduled jobs
│   └── queue_job_function_data.xml
└── README.md
```

**Step 4: Customize Backend Model**

Edit `models/backend.py`:

1. **Update API configuration fields** to match the external system:
   ```python
   # Example for Shopify
   shop_url = fields.Char(string='Shop URL', required=True)
   api_version = fields.Selection([
       ('2024-01', '2024-01'),
       ('2024-04', '2024-04'),
   ], default='2024-04')
   ```

2. **Implement template methods**:
   ```python
   def _test_connection_implementation(self):
       """Test API connection."""
       adapter = self.get_adapter('shopify.adapter')
       return adapter.test_connection()

   def _sync_orders_implementation(self):
       """Import orders."""
       with self.work_on('shopify.sale.order') as work:
           importer = work.component(usage='batch.importer')
           return importer.run()
   ```

**Step 5: Implement Adapter**

Edit `models/adapter.py`:

1. **Configure authentication** (see `references/authentication.md` for patterns):
   ```python
   def get_api_headers(self):
       headers = super().get_api_headers()
       headers.update({
           'X-Shopify-Access-Token': self.backend_record.api_key,
           'Content-Type': 'application/json',
       })
       return headers
   ```

2. **Add CRUD methods** for each entity type:
   ```python
   def get_products(self, filters=None):
       """Fetch products from Shopify."""
       return self.get('/admin/api/2024-01/products.json', params=filters)

   def create_order(self, data):
       """Create order in Shopify."""
       return self.post('/admin/api/2024-01/orders.json', data={'order': data})
   ```

3. **Handle pagination** (see `references/api_integration.md`):
   ```python
   def get_all_products(self):
       """Fetch all products with pagination."""
       # Implement based on API pagination style
   ```

**Step 6: Create Mapper Components**

Create `components/mapper.py`:

```python
from odoo.addons.generic_connector.components.mapper import GenericImportMapper

class ProductImportMapper(GenericImportMapper):
    _name = 'shopify.product.import.mapper'
    _inherit = 'generic.import.mapper'
    _apply_on = 'shopify.product.template'

    direct = [
        ('title', 'name'),
        ('vendor', 'manufacturer'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def price(self, record):
        variants = record.get('variants', [])
        if variants:
            return {'list_price': float(variants[0].get('price', 0))}
        return {}
```

**Step 7: Implement Importer Components**

Create `components/importer.py`:

```python
from odoo.addons.generic_connector.components.importer import GenericImporter

class ProductImporter(GenericImporter):
    _name = 'shopify.product.importer'
    _inherit = 'generic.importer'
    _apply_on = 'shopify.product.template'

    def _import_record(self, external_id, force=False):
        # Fetch from external system
        adapter = self.component(usage='backend.adapter')
        external_data = adapter.get_product(external_id)

        # Transform data
        mapper = self.component(usage='import.mapper')
        mapped_data = mapper.map_record(external_data).values()

        # Create or update binding
        binding = self._get_binding()
        if binding:
            binding.write(mapped_data)
        else:
            binding = self.model.create(mapped_data)

        return binding
```

**Step 8: Register Components**

Create `components/__init__.py`:
```python
from . import adapter
from . import mapper
from . import importer
from . import exporter
```

Update main `__init__.py`:
```python
from . import models
from . import wizards
from . import components
```

**Step 9: Test the Connector**

```bash
# Install module
odoo-bin -c odoo.conf -d test_db -i shopify_connector

# Test in Odoo UI
# 1. Go to Connector > Shopify > Backends
# 2. Create a new backend
# 3. Configure API credentials
# 4. Click "Test Connection"
# 5. Click "Sync All"
```

### Enhancing an Existing Connector

When the user wants to add functionality to an existing connector:

**Step 1: Identify Enhancement Type**

- Adding a new entity (orders, customers, invoices)
- Adding a new feature (webhooks, batch export)
- Fixing bugs or improving performance
- Adding authentication method

**Step 2: Add New Entity Binding**

Use the `add_binding.py` script:

```bash
python3 scripts/add_binding.py <connector_path> <entity_name> --odoo-model <model>

# Example:
python3 scripts/add_binding.py ~/odoo/addons/shopify_connector customer --odoo-model res.partner
```

This generates:
- `models/customer_binding.py` - Binding model
- `views/customer_views.xml` - UI views
- Updates to `__manifest__.py` and security files
- Adapter methods to implement manually

**Step 3: Implement Components**

Follow steps 6-7 from "Creating a New Connector" to implement mapper and importer/exporter for the new entity.

**Step 4: Add to Backend Orchestration**

Update `models/backend.py`:

```python
def _sync_customers_implementation(self):
    """Import customers."""
    with self.work_on('shopify.res.partner') as work:
        importer = work.component(usage='batch.importer')
        return importer.run()

def action_sync_all(self):
    """Override to include customers."""
    super().action_sync_all()
    self.with_delay().sync_customers()
```

### Implementing Webhooks

When the user requests webhook support:

**Step 1: Create Webhook Controller**

Create `controllers/webhook_controller.py`:

```python
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class ShopifyWebhookController(http.Controller):
    @http.route('/shopify/webhook', type='json', auth='none', csrf=False)
    def webhook(self):
        """Handle Shopify webhooks."""
        try:
            payload = request.httprequest.get_data(as_text=True)
            topic = request.httprequest.headers.get('X-Shopify-Topic')
            hmac_header = request.httprequest.headers.get('X-Shopify-Hmac-SHA256')

            # Find backend
            shop_domain = request.httprequest.headers.get('X-Shopify-Shop-Domain')
            backend = request.env['shopify.backend'].sudo().search([
                ('shop_url', 'ilike', shop_domain)
            ], limit=1)

            if not backend:
                return {'error': 'Backend not found'}, 404

            # Verify signature
            if not self._verify_webhook(payload, hmac_header, backend.webhook_secret):
                return {'error': 'Invalid signature'}, 401

            # Create webhook record
            webhook = request.env['generic.webhook'].sudo().create({
                'backend_id': backend.id,
                'event_type': topic,
                'payload': payload,
                'signature': hmac_header,
                'processing_status': 'pending',
            })

            # Process asynchronously
            webhook.with_delay().process_webhook()

            return {'status': 'accepted', 'webhook_id': webhook.id}

        except Exception as e:
            _logger.exception("Webhook processing failed")
            return {'error': str(e)}, 500

    def _verify_webhook(self, payload, hmac_header, secret):
        """Verify HMAC-SHA256 signature."""
        import hmac
        import hashlib
        import base64

        computed = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).digest()

        computed_base64 = base64.b64encode(computed).decode()

        return hmac.compare_digest(computed_base64, hmac_header)
```

**Step 2: Add Webhook Processing to Backend**

Update `models/backend.py`:

```python
def process_webhook(self, webhook):
    """Process webhook by topic."""
    handlers = {
        'orders/create': self._handle_order_created,
        'orders/updated': self._handle_order_updated,
        'products/update': self._handle_product_updated,
    }

    handler = handlers.get(webhook.event_type)
    if handler:
        try:
            handler(webhook)
            webhook.mark_as_processed()
        except Exception as e:
            _logger.exception("Webhook handler failed")
            webhook.mark_as_failed(str(e))
    else:
        webhook.mark_as_ignored(f"No handler for {webhook.event_type}")

def _handle_order_created(self, webhook):
    """Handle orders/create webhook."""
    payload = json.loads(webhook.payload)
    order_id = payload['id']

    # Import the order
    self.env['shopify.sale.order'].import_record(
        backend=self,
        external_id=str(order_id)
    )
```

### Implementing Export Using Shared Wizard

The `connector_base_backend` module provides a **shared export wizard** (`connector.export.wizard`) that works across all connectors without requiring custom UI for each one.

#### Architecture Overview

The export system uses delegation inheritance to route export requests:

```
User clicks "Export to Connectors" on product.product
    ↓
connector.export.wizard opens (shared UI)
    ↓
User selects backend (e.g., ZID, Shopify)
    ↓
wizard.action_export() calls backend.export_records(model_name, record_ids)
    ↓
connector.base.backend routes to concrete implementation
    ↓ (via _inherits delegation chain)
generic.backend (intermediate)
    ↓
zid.backend.export_product_product(record_ids)
    ↓
Creates bindings + queues async exports
```

**Inheritance Chain**:
```python
connector.base.backend (has export_records() router)
    ↓ _inherits via base_backend_id
generic.backend (intermediate layer)
    ↓ _inherits via generic_backend_id
your_connector.backend (concrete implementation)
```

#### Step-by-Step Implementation

**Step 1: Understand the Routing Mechanism**

The `connector.base.backend.export_records()` method automatically routes to your backend:

```python
# In connector_base_backend/models/connector_base_backend.py
def export_records(self, model_name, record_ids):
    """Generic export method that routes to specific connector implementations"""
    method_name = f'export_{model_name.replace(".", "_")}'

    # Find concrete backend via _inherits chain
    concrete_backend = self
    for model in self._inherits_children:
        child = self.env[model].search([('base_backend_id', '=', self.id)], limit=1)
        if child:
            concrete_backend = child
            break

    # Call export_product_product(), export_sale_order(), etc.
    if hasattr(concrete_backend, method_name):
        return getattr(concrete_backend, method_name)(record_ids)
    else:
        raise UserError(_(
            "Export not implemented for model %s in connector %s"
        ) % (model_name, concrete_backend.name))
```

**Step 2: Implement Export Methods in Your Backend**

For each Odoo model you want to export, implement `export_<model_name>()` in your backend model:

**Example: Export Products**

Add to `models/backend.py`:

```python
def export_product_product(self, record_ids):
    """
    Export product.product records to external system.

    Called by connector.export.wizard when exporting products.

    Args:
        record_ids: List of product.product IDs to export

    Returns:
        dict: Notification action
    """
    self.ensure_one()

    if not record_ids:
        return self._build_notification(
            _('Export Products'),
            _('No products selected for export'),
            'warning'
        )

    products = self.env['product.product'].browse(record_ids)
    exported_count = 0
    created_bindings = 0
    skipped_count = 0
    errors = []

    for product in products:
        try:
            # Find or create binding
            binding = self.env['shopify.product.product'].search([
                ('backend_id', '=', self.id),
                ('odoo_id', '=', product.id)
            ], limit=1)

            if not binding:
                # Create new binding
                binding_vals = {
                    'backend_id': self.id,
                    'odoo_id': product.id,
                    'external_sku': product.default_code or '',
                    'external_name': product.name,
                    'external_price': product.list_price,
                    'external_status': 'active' if product.active else 'inactive',
                }
                binding = self.env['shopify.product.product'].create(binding_vals)
                created_bindings += 1

            # Skip if marked as no_export
            if binding.no_export:
                skipped_count += 1
                continue

            # Queue async export
            binding.with_delay()._export_to_external()
            exported_count += 1

        except Exception as e:
            errors.append(f'Product {product.name}: {str(e)}')
            _logger.error(f'Export failed for {product.name}: {e}', exc_info=True)

    # Build response message
    message_parts = []
    if exported_count > 0:
        message_parts.append(
            _('%d product(s) scheduled for export') % exported_count
        )
    if created_bindings > 0:
        message_parts.append(_('%d new binding(s) created') % created_bindings)
    if skipped_count > 0:
        message_parts.append(_('%d skipped (no_export)') % skipped_count)
    if errors:
        message_parts.append(_('Errors: %d') % len(errors))

    message = '. '.join(message_parts)
    notif_type = 'success' if exported_count > 0 and not errors else 'warning'

    # Update statistics
    if exported_count > 0:
        self.last_export_date = datetime.now()

    return self._build_notification(_('Export Products'), message, notif_type)
```

**Example: Export Partners**

```python
def export_res_partner(self, record_ids):
    """Export res.partner records to external system."""
    self.ensure_one()

    partners = self.env['res.partner'].browse(record_ids)
    exported_count = 0

    for partner in partners:
        # Find or create partner binding
        binding = self.env['shopify.res.partner'].search([
            ('backend_id', '=', self.id),
            ('odoo_id', '=', partner.id)
        ], limit=1)

        if not binding:
            binding = self.env['shopify.res.partner'].create({
                'backend_id': self.id,
                'odoo_id': partner.id,
            })

        # Queue export
        binding.with_delay()._export_to_external()
        exported_count += 1

    return self._build_notification(
        _('Export Customers'),
        _('%d customer(s) scheduled for export') % exported_count,
        'success'
    )
```

**Example: Export Sale Orders**

```python
def export_sale_order(self, record_ids):
    """Export sale.order records to external system."""
    self.ensure_one()

    orders = self.env['sale.order'].browse(record_ids)
    exported_count = 0

    for order in orders:
        # Validate order state
        if order.state not in ['sale', 'done']:
            _logger.warning(f'Skipping order {order.name}: not confirmed')
            continue

        # Find or create order binding
        binding = self.env['shopify.sale.order'].search([
            ('backend_id', '=', self.id),
            ('odoo_id', '=', order.id)
        ], limit=1)

        if not binding:
            binding = self.env['shopify.sale.order'].create({
                'backend_id': self.id,
                'odoo_id': order.id,
            })

        # Export dependencies first (customer, products)
        self._export_order_dependencies(order)

        # Queue order export
        binding.with_delay()._export_to_external()
        exported_count += 1

    return self._build_notification(
        _('Export Orders'),
        _('%d order(s) scheduled for export') % exported_count,
        'success'
    )

def _export_order_dependencies(self, order):
    """Export customer and products before exporting order."""
    # Export customer
    if order.partner_id:
        self.export_res_partner([order.partner_id.id])

    # Export products
    product_ids = order.order_line.mapped('product_id').ids
    if product_ids:
        self.export_product_product(product_ids)
```

**Step 3: The Shared Wizard is Already Configured**

The `connector_base_backend` module already includes action bindings:

```xml
<!-- In connector_base_backend/wizards/connector_export_wizard_view.xml -->

<!-- Export action for products -->
<record id="action_connector_export_wizard_product" model="ir.actions.act_window">
    <field name="name">Export to Connectors</field>
    <field name="res_model">connector.export.wizard</field>
    <field name="view_mode">form</field>
    <field name="target">new</field>
    <field name="binding_model_id" ref="product.model_product_product"/>
    <field name="binding_view_types">list,form</field>
</record>

<!-- Export action for partners -->
<record id="action_connector_export_wizard" model="ir.actions.act_window">
    <field name="name">Export to Connectors</field>
    <field name="res_model">connector.export.wizard</field>
    <field name="view_mode">form</field>
    <field name="target">new</field>
    <field name="binding_model_id" ref="base.model_res_partner"/>
    <field name="binding_view_types">list,form</field>
</record>
```

**To add export for other models**, create similar actions in your connector or in `connector_base_backend`:

```xml
<!-- Export action for sale orders -->
<record id="action_connector_export_wizard_sale_order" model="ir.actions.act_window">
    <field name="name">Export to Connectors</field>
    <field name="res_model">connector.export.wizard</field>
    <field name="view_mode">form</field>
    <field name="target">new</field>
    <field name="binding_model_id" ref="sale.model_sale_order"/>
    <field name="binding_view_types">list,form</field>
</record>
```

**Step 4: Testing the Export**

```bash
# 1. Update your connector module
odoo-bin -c odoo.conf -d your_db -u your_connector

# 2. Test from UI
# Navigate to: Inventory → Products → Products
# Select one or more products
# Click: Action → Export to Connectors
# Select your backend
# Click: Export

# 3. Verify in logs
tail -f /var/log/odoo/odoo.log | grep "export\|binding"

# 4. Check queue jobs
# Navigate to: Queue Jobs → Jobs
# Look for: your_connector.product.product._export_to_external

# 5. Check bindings created
# Navigate to: Connector → Your Connector → Products
# Verify bindings were created with correct external_id
```

**Step 5: Advanced Export Patterns**

**Pattern 1: Conditional Export**

```python
def export_product_product(self, record_ids):
    """Export only published products."""
    products = self.env['product.product'].browse(record_ids)

    # Filter products
    exportable_products = products.filtered(
        lambda p: p.active and getattr(p, 'website_published', True)
    )

    if len(exportable_products) < len(products):
        skipped = len(products) - len(exportable_products)
        _logger.info(f'Skipped {skipped} unpublished products')

    # Export only exportable products
    for product in exportable_products:
        # ... create binding and export
```

**Pattern 2: Batch Export with Progress**

```python
def export_product_product(self, record_ids):
    """Export products in batches."""
    products = self.env['product.product'].browse(record_ids)
    batch_size = 50

    for i in range(0, len(products), batch_size):
        batch = products[i:i + batch_size]
        # Process batch with delay
        self.with_delay()._export_product_batch(batch.ids)

    return self._build_notification(
        _('Export Products'),
        _('Queued %d products in %d batches') % (
            len(products),
            (len(products) + batch_size - 1) // batch_size
        ),
        'success'
    )

def _export_product_batch(self, product_ids):
    """Process a batch of products."""
    for product_id in product_ids:
        # Create binding and export
        pass
```

**Pattern 3: Export with Validation**

```python
def export_sale_order(self, record_ids):
    """Export orders with validation."""
    orders = self.env['sale.order'].browse(record_ids)
    validation_errors = []

    for order in orders:
        # Validate before export
        if not order.partner_id:
            validation_errors.append(f'{order.name}: Missing customer')
            continue

        if not order.order_line:
            validation_errors.append(f'{order.name}: No order lines')
            continue

        if order.state not in ['sale', 'done']:
            validation_errors.append(f'{order.name}: Not confirmed')
            continue

        # Export if valid
        # ... create binding and export

    if validation_errors:
        message = '\n'.join(validation_errors[:10])
        return self._build_notification(
            _('Export Validation Errors'),
            message,
            'warning'
        )
```

#### Method Naming Convention

The export method name **must** follow this pattern:

```python
export_{model_name_with_underscores}

# Examples:
export_product_product      # for product.product
export_product_template     # for product.template
export_sale_order           # for sale.order
export_res_partner          # for res.partner
export_stock_picking        # for stock.picking
export_account_move         # for account.move
```

The wizard automatically converts model names:
- Replaces dots (`.`) with underscores (`_`)
- `product.product` → calls `export_product_product()`
- `sale.order` → calls `export_sale_order()`

#### Benefits of Shared Export Wizard

1. **Single UI**: One wizard works for all models across all connectors
2. **Consistent UX**: Users learn once, use everywhere
3. **No Custom Code**: No need to create custom wizards or actions
4. **Multi-Backend**: Users can export to multiple backends
5. **Extensible**: Add new models just by implementing one method
6. **Backend Filtering**: Wizard shows only relevant backends via domain

#### Complete Implementation Checklist

When implementing export for a new model:

- [ ] Implement `export_<model_name>()` method in backend model
- [ ] Handle binding creation (find or create)
- [ ] Queue export using `with_delay()._export_to_external()`
- [ ] Handle errors gracefully with try/except
- [ ] Return notification with detailed status
- [ ] Update backend statistics (last_export_date)
- [ ] Add export action binding (if not exists for this model)
- [ ] Test from UI (Action → Export to Connectors)
- [ ] Verify queue jobs are created
- [ ] Check bindings are created correctly
- [ ] Review logs for errors

#### Troubleshooting Export Issues

**Issue**: "Export not implemented" error

```python
# Solution: Check method name matches pattern
# Model: product.product → Method: export_product_product()
# Model: sale.order → Method: export_sale_order()
```

**Issue**: Backend not showing in wizard

```python
# Solution: Check inheritance chain
# Ensure your backend inherits from generic.backend
# which inherits from connector.base.backend

class YourBackend(models.Model):
    _name = 'your.backend'
    _inherits = {'generic.backend': 'generic_backend_id'}
```

**Issue**: Export creates duplicates

```python
# Solution: Ensure unique constraint on binding
# In binding model:
_sql_constraints = [
    ('backend_odoo_uniq',
     'unique(backend_id, odoo_id)',
     'A binding already exists for this record on this backend.')
]
```

**Issue**: Export completes but nothing happens

```python
# Solution: Check queue_job is running
# 1. Verify queue_job channel exists
# 2. Start queue job worker:
odoo-bin gevent -c odoo.conf --workers=2

# 3. Or run job manually:
>>> job = env['queue.job'].search([...])
>>> job.requeue()
```

### Troubleshooting

When the user reports sync issues or errors:

**Step 1: Identify the Problem**

Common issues:
- Connection/authentication failures → Check `references/authentication.md`
- Import not working → Check component registration
- Duplicates being created → Check SQL constraints
- Queue jobs not running → Check queue_job configuration
- Webhooks not received → Check controller route

**Step 2: Use Diagnostic Tools**

```python
# Test in Odoo shell
odoo-bin shell -c odoo.conf -d your_db

# Find backend
>>> backend = env['shopify.backend'].browse(1)

# Test connection
>>> backend.action_test_connection()

# Test adapter
>>> with backend.work_on('shopify.product.template') as work:
...     adapter = work.component(usage='backend.adapter')
...     products = adapter.get_products()
...     print(f"Fetched {len(products)} products")

# Test mapper
...     mapper = work.component(usage='import.mapper')
...     if products:
...         mapped = mapper.map_record(products[0])
...         print(mapped.values())
```

**Step 3: Enable Debug Logging**

Add to backend or adapter:
```python
import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def make_request(self, method, endpoint, **kwargs):
    _logger.debug("API Request: %s %s", method, self.build_url(endpoint))
    _logger.debug("Params: %s", kwargs.get('params'))
    _logger.debug("Data: %s", kwargs.get('data'))

    response = super().make_request(method, endpoint, **kwargs)

    _logger.debug("Response: %s", str(response)[:500])
    return response
```

**Step 4: Check Reference Documentation**

Refer the user to:
- `references/troubleshooting.md` - Common issues and solutions
- `references/architecture.md` - Component structure
- `references/patterns.md` - Design patterns
- `references/api_integration.md` - API communication patterns
- `references/authentication.md` - Authentication methods

## Available Scripts

### init_connector.py

Generate a complete new connector module.

**Usage**:
```bash
python3 scripts/init_connector.py <connector_name> --path <output_path> --type <connector_type>
```

**Arguments**:
- `connector_name`: Name (e.g., 'shopify', 'woocommerce')
- `--path`: Output directory (default: current directory)
- `--type`: Connector type - 'ecommerce', 'logistics', 'accounting', 'crm'

**Output**: Complete module with backend, adapter, binding, views, security

### add_binding.py

Add a new entity binding to existing connector.

**Usage**:
```bash
python3 scripts/add_binding.py <connector_path> <entity_name> --odoo-model <model>
```

**Arguments**:
- `connector_path`: Path to existing connector module
- `entity_name`: Entity name (e.g., 'order', 'customer')
- `--odoo-model`: Odoo model to bind (e.g., 'sale.order', 'res.partner')

**Output**: Binding model, views, security rules, adapter methods template

### validate_connector.py

Validate connector module structure.

**Usage**:
```bash
python3 scripts/validate_connector.py <connector_path>
```

**Checks**:
- Required files and directories
- Manifest dependencies
- Backend model structure
- Component registration
- Security configuration

## Reference Documentation

Load references as needed using the Read tool:

### references/architecture.md
Comprehensive guide to generic_connector architecture:
- Backend model patterns
- Binding model structure
- Adapter, mapper, importer, exporter components
- Queue job integration
- Security model
- View patterns

**When to read**: Creating new connectors, understanding component relationships

### references/patterns.md
Design patterns used in connectors:
- Template Method, Adapter, Strategy, Factory patterns
- Observer pattern for webhooks
- Retry and circuit breaker patterns
- Rate limiting patterns
- Anti-patterns to avoid

**When to read**: Implementing complex sync logic, handling failures

### references/api_integration.md
API integration techniques:
- REST, GraphQL, SOAP integrations
- Pagination handling (offset, cursor, link header)
- Response envelope handling
- Webhook integration
- Rate limiting implementation
- Error handling and retries

**When to read**: Implementing adapters, handling API specifics

### references/authentication.md
Authentication patterns:
- API key authentication
- OAuth 2.0 (authorization code flow)
- Bearer token
- Basic auth
- HMAC signatures
- JWT tokens
- Webhook signature verification

**When to read**: Configuring authentication, debugging 401 errors

### references/troubleshooting.md
Common issues and solutions:
- Connection issues
- Authentication failures
- Import/export problems
- Queue job issues
- Webhook problems
- Data mapping errors
- Performance optimization
- Debugging tips

**When to read**: Debugging sync issues, performance problems

## Best Practices

1. **Always extend generic_connector** - Never build from scratch
2. **Use bindings** - Never directly modify Odoo records from external data
3. **Queue long operations** - Use `with_delay()` for anything >2 seconds
4. **Implement retry logic** - Use binding's retry_count and max_retries
5. **Log extensively** - Debug logging helps troubleshoot production issues
6. **Handle API errors** - Wrap adapter calls in try/except
7. **Validate data** - Check required fields before creating records
8. **Test connection** - Always implement `_test_connection_implementation()`
9. **Use transactions** - Leverage Odoo's automatic transaction management
10. **Document the API** - Add docstrings to all adapter methods

## Component Registration Checklist

When creating components, ensure:

```python
class MyComponent(BaseComponent):
    _name = 'unique.component.name'      # ✓ Unique identifier
    _inherit = 'parent.component'        # ✓ Parent component
    _apply_on = 'model.name'             # ✓ Model this applies to
    _usage = 'component.usage'           # ✓ Usage context
```

Common usages:
- `backend.adapter` - API communication
- `record.importer` - Single record import
- `batch.importer` - Batch import
- `record.exporter` - Single record export
- `batch.exporter` - Batch export
- `import.mapper` - Import data transformation
- `export.mapper` - Export data transformation

## Testing Checklist

Before delivering a connector:

**Backend Configuration**:
- [ ] Backend configuration form loads
- [ ] "Test Connection" button works
- [ ] Backend inherits from generic.backend correctly
- [ ] Backend statistics update (last_sync_date, counters)

**Import Functionality**:
- [ ] Manual sync imports data
- [ ] No duplicate records created on import
- [ ] External IDs are set correctly
- [ ] Bindings link Odoo records to external records
- [ ] Import handles API pagination correctly
- [ ] Import handles API errors gracefully

**Export Functionality**:
- [ ] "Export to Connectors" action appears on models (Action menu)
- [ ] Export wizard shows only relevant backends
- [ ] `export_<model_name>()` methods implemented in backend
- [ ] Export creates bindings if they don't exist
- [ ] Export queues async jobs via `with_delay()`
- [ ] Export notifications show correct counts (exported, created, skipped, errors)
- [ ] Export respects `no_export` flag on bindings
- [ ] Export updates backend statistics (last_export_date)

**Queue Jobs**:
- [ ] Queue jobs are registered and visible
- [ ] Jobs execute successfully in queue_job worker
- [ ] Failed jobs can be retried
- [ ] Job logs provide useful debugging info

**Scheduled Jobs**:
- [ ] Scheduled cron jobs exist (disabled by default)
- [ ] Cron jobs can be enabled and run on schedule

**Security & Access**:
- [ ] Security access rules allow users to view data
- [ ] Users can access backend, bindings, and wizards
- [ ] Proper groups assigned (connector_manager, connector_user)

**Integration**:
- [ ] Webhooks received and processed (if applicable)
- [ ] Webhook signature verification works
- [ ] Components registered correctly (adapters, mappers, importers, exporters)

**Error Handling**:
- [ ] Error handling works (test with invalid credentials)
- [ ] API errors don't crash Odoo
- [ ] User-friendly error messages displayed
- [ ] Detailed errors logged for debugging

**Logging & Debugging**:
- [ ] Logging provides useful debug information
- [ ] Log levels appropriate (INFO for success, ERROR for failures)
- [ ] Sensitive data (tokens, passwords) not logged

## Module Update Process

When updating an existing connector:

```bash
# 1. Update module files
# 2. Upgrade module
odoo-bin -c odoo.conf -d your_db -u connector_module_name

# 3. Test thoroughly
# 4. Check logs for errors
tail -f /var/log/odoo/odoo.log
```

## Common Workflows

### Workflow: Add Product Sync

1. Generate binding: `python3 scripts/add_binding.py <path> product --odoo-model product.template`
2. Implement adapter methods in `models/adapter.py`
3. Create mapper in `components/mapper.py`
4. Create importer in `components/importer.py`
5. Update backend `_sync_products_implementation()`
6. Update module: `odoo-bin -u connector_name`
7. Test sync

### Workflow: Add Order Import

1. Generate binding: `python3 scripts/add_binding.py <path> order --odoo-model sale.order`
2. Implement adapter methods
3. Create import mapper (transform external order to Odoo format)
4. Create importer (handle order lines, customer lookup)
5. Update backend `_sync_orders_implementation()`
6. Configure webhook for real-time import (optional)
7. Test import

### Workflow: Debug Sync Failure

1. Check logs: `tail -f /var/log/odoo/odoo.log`
2. Enable debug logging in adapter
3. Test in Odoo shell
4. Check component registration
5. Verify API credentials
6. Test adapter methods directly
7. Check mapper output
8. Review binding constraints
9. Refer to `references/troubleshooting.md`

## Output Format

When creating or enhancing connectors:

1. **Use scripts** whenever possible (init_connector.py, add_binding.py)
2. **Provide code** for custom components (mappers, importers, exporters)
3. **Show configuration** (backend fields, view changes)
4. **Include testing steps** (how to verify it works)
5. **Reference docs** when needed (point to specific reference sections)
6. **Explain patterns** used (why this approach was chosen)

## Error Prevention

Common mistakes to avoid:

- ❌ Missing `_apply_on` in components
- ❌ Wrong model name in `_apply_on`
- ❌ Forgetting to register components in `__init__.py`
- ❌ Not setting `external_id` in mapper
- ❌ Missing SQL constraint on bindings
- ❌ Using synchronous operations for long tasks
- ❌ Not handling API pagination
- ❌ Hardcoding configuration instead of using backend fields
- ❌ Not implementing retry logic
- ❌ Insufficient error handling

## Success Criteria

A successfully created/enhanced connector should:

1. ✅ Install without errors
2. ✅ Test connection successfully
3. ✅ Import/export data correctly
4. ✅ Handle API errors gracefully
5. ✅ Log useful information for debugging
6. ✅ Use queue jobs for async operations
7. ✅ Not create duplicate records
8. ✅ Follow generic_connector patterns
9. ✅ Have proper security configuration
10. ✅ Be maintainable and extensible

## When to Use Each Reference

| Situation | Reference |
|-----------|-----------|
| Creating new connector | architecture.md |
| Implementing OAuth | authentication.md |
| Adding webhooks | api_integration.md |
| Sync not working | troubleshooting.md |
| Implementing retry logic | patterns.md |
| Understanding components | architecture.md |
| API pagination | api_integration.md |
| 401 errors | authentication.md, troubleshooting.md |
| Performance issues | troubleshooting.md, patterns.md |
| Best practices | patterns.md (anti-patterns section) |

## Final Notes

- Always test in a development database first
- Use the reference connectors (zid, beatroute) as examples
- Leverage the scripts to generate boilerplate code
- Refer to documentation for specific patterns
- Focus on extensibility and maintainability
- Follow Odoo and generic_connector conventions
