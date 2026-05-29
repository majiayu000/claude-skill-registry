---
name: insightpulse-connection-manager
description: Supabase-style connection UI for managing InsightPulse AI infrastructure (Supabase, Odoo, Superset, MCP servers, PostgreSQL, APIs). Self-hosted connection manager module for Odoo 19 that provides unified connection management, auto-generated configurations, connection testing, and beautiful Kanban interface.
---

# InsightPulse Connection Manager

## When to Use This Skill

Use this skill when you need to:
- Manage multiple database and API connections for Finance SSC operations
- Generate connection strings, .env files, or Docker Compose configs
- Test and monitor connection health across infrastructure
- Integrate Supabase, Odoo, Superset, MCP servers, and PostgreSQL
- Build self-hosted connection management without vendor lock-in
- Create unified connection dashboard for multi-agency operations

## Core Capabilities

### Connection Management
- Unified interface for all connections (Supabase, Odoo, Superset, MCP, PostgreSQL, APIs)
- Pre-configured connections for InsightPulse AI stack
- Support for 8 agencies: RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB
- Color-coded connection types with visual status indicators

### Auto-Generated Configuration
- Connection string generation (PostgreSQL, MySQL, MongoDB formats)
- Environment variables in .env format with copy-to-clipboard
- Docker Compose service definitions
- Kubernetes ConfigMap snippets

### Connection Testing & Monitoring
- One-click connection testing
- Real-time connection health monitoring
- Active connection count tracking
- Connection latency measurement

### Beautiful UI
- Supabase-inspired Kanban interface
- Color-coded by connection type
- Visual status indicators (green/yellow/red)
- Quick-access copy buttons

## Prerequisites

### Required Software
- Odoo 19 Community Edition
- PostgreSQL 16+ (for connection testing)
- Python 3.11+ with psycopg2

### Optional Integrations
- Supabase project (ref: spdtwktxdalcfigzeqrz)
- Apache Superset instance
- MCP servers (Notion, Google Drive)
- DigitalOcean PostgreSQL cluster

### Access Requirements
- Odoo administrator access
- Database credentials for systems being managed
- API keys for external services

## Implementation Patterns

### Module Structure

```python
insightpulse_connection_manager/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── connection_endpoint.py      # Main model
├── views/
│   ├── connection_endpoint_views.xml
│   └── connection_endpoint_kanban.xml
├── security/
│   ├── ir.model.access.csv
│   └── connection_security.xml
├── data/
│   └── default_endpoints.xml       # Pre-configured connections
└── static/
    ├── description/
    │   └── index.html
    └── src/
        └── scss/
            └── connection_manager.scss
```

### Model Definition

```python
# models/connection_endpoint.py
from odoo import models, fields, api
import psycopg2

class ConnectionEndpoint(models.Model):
    _name = 'insightpulse.connection.endpoint'
    _description = 'Connection Endpoint'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    connection_type = fields.Selection([
        ('supabase', 'Supabase'),
        ('postgresql', 'PostgreSQL'),
        ('odoo', 'Odoo Database'),
        ('superset', 'Apache Superset'),
        ('mcp', 'MCP Server'),
        ('api', 'REST API'),
    ], required=True)
    
    base_url = fields.Char(string='Server/Host')
    port = fields.Integer(default=5432)
    database_name = fields.Char()
    username = fields.Char()
    password = fields.Char()
    api_key = fields.Char()
    
    connection_string = fields.Text(compute='_compute_connection_string')
    env_vars = fields.Text(compute='_compute_env_vars')
    docker_compose = fields.Text(compute='_compute_docker_compose')
    
    status = fields.Selection([
        ('draft', 'Not Tested'),
        ('success', 'Connected'),
        ('failed', 'Failed'),
    ], default='draft')
    
    @api.depends('connection_type', 'base_url', 'port', 'database_name', 'username', 'password')
    def _compute_connection_string(self):
        for rec in self:
            if rec.connection_type in ['supabase', 'postgresql', 'odoo']:
                rec.connection_string = (
                    f"postgresql://{rec.username}:{rec.password}@"
                    f"{rec.base_url}:{rec.port}/{rec.database_name}"
                )
            elif rec.connection_type == 'superset':
                rec.connection_string = f"http://{rec.base_url}:{rec.port}"
            else:
                rec.connection_string = f"{rec.base_url}"
    
    @api.depends('name', 'connection_string')
    def _compute_env_vars(self):
        for rec in self:
            safe_name = rec.name.upper().replace(' ', '_').replace('-', '_')
            rec.env_vars = (
                f"{safe_name}_URL={rec.connection_string}\n"
                f"{safe_name}_USER={rec.username}\n"
                f"{safe_name}_PASSWORD={rec.password}"
            )
    
    def action_test_connection(self):
        """Test database connection"""
        for rec in self:
            try:
                if rec.connection_type in ['supabase', 'postgresql', 'odoo']:
                    conn = psycopg2.connect(rec.connection_string)
                    conn.close()
                    rec.status = 'success'
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'message': f'✅ Connected to {rec.name}',
                            'type': 'success',
                            'sticky': False,
                        }
                    }
            except Exception as e:
                rec.status = 'failed'
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': f'❌ Connection failed: {str(e)}',
                        'type': 'danger',
                        'sticky': True,
                    }
                }
```

### View Definition (Kanban)

```xml
<!-- views/connection_endpoint_kanban.xml -->
<record id="view_connection_endpoint_kanban" model="ir.ui.view">
    <field name="name">insightpulse.connection.endpoint.kanban</field>
    <field name="model">insightpulse.connection.endpoint</field>
    <field name="arch" type="xml">
        <kanban class="o_kanban_mobile" sample="1">
            <field name="id"/>
            <field name="name"/>
            <field name="connection_type"/>
            <field name="status"/>
            <field name="connection_string"/>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_global_click o_kanban_record_has_image_fill">
                        <div class="o_kanban_record_top">
                            <div class="o_kanban_record_headings">
                                <strong class="o_kanban_record_title">
                                    <field name="name"/>
                                </strong>
                                <span class="badge badge-pill" 
                                      t-attf-class="badge-{{status == 'success' and 'success' or status == 'failed' and 'danger' or 'secondary'}}">
                                    <field name="status"/>
                                </span>
                            </div>
                        </div>
                        <div class="o_kanban_record_body">
                            <field name="connection_type" widget="badge"/>
                            <div class="text-muted">
                                <i class="fa fa-server"/> <field name="base_url"/>:<field name="port"/>
                            </div>
                        </div>
                        <div class="o_kanban_record_bottom">
                            <div class="oe_kanban_bottom_left">
                                <button type="object" name="action_test_connection" 
                                        class="btn btn-sm btn-secondary">
                                    <i class="fa fa-plug"/> Test
                                </button>
                            </div>
                            <div class="oe_kanban_bottom_right">
                                <button type="object" name="action_copy_connection_string"
                                        class="btn btn-sm btn-link">
                                    <i class="fa fa-clipboard"/> Copy
                                </button>
                            </div>
                        </div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

### Default Data

```xml
<!-- data/default_endpoints.xml -->
<odoo>
    <data noupdate="1">
        <!-- Supabase Production -->
        <record id="endpoint_supabase_prod" model="insightpulse.connection.endpoint">
            <field name="name">Supabase Production</field>
            <field name="connection_type">supabase</field>
            <field name="base_url">db.spdtwktxdalcfigzeqrz.supabase.co</field>
            <field name="port">5432</field>
            <field name="database_name">postgres</field>
            <field name="username">postgres</field>
            <field name="sequence">10</field>
        </record>

        <!-- Odoo Database -->
        <record id="endpoint_odoo_db" model="insightpulse.connection.endpoint">
            <field name="name">Odoo 19 Database</field>
            <field name="connection_type">odoo</field>
            <field name="base_url">localhost</field>
            <field name="port">5432</field>
            <field name="database_name">odoo19</field>
            <field name="username">odoo</field>
            <field name="sequence">20</field>
        </record>

        <!-- Apache Superset -->
        <record id="endpoint_superset" model="insightpulse.connection.endpoint">
            <field name="name">Apache Superset Dashboard</field>
            <field name="connection_type">superset</field>
            <field name="base_url">localhost</field>
            <field name="port">8088</field>
            <field name="username">admin</field>
            <field name="sequence">30</field>
        </record>

        <!-- MCP Server - Notion -->
        <record id="endpoint_mcp_notion" model="insightpulse.connection.endpoint">
            <field name="name">MCP Server - Notion</field>
            <field name="connection_type">mcp</field>
            <field name="base_url">http://localhost:3000</field>
            <field name="sequence">40</field>
        </record>
    </data>
</odoo>
```

## Integration Points

### With Odoo Finance Modules
```python
# Access connections from other modules
connection = self.env['insightpulse.connection.endpoint'].search([
    ('name', '=', 'Supabase Production')
], limit=1)

if connection:
    # Use connection string for external API calls
    import requests
    response = requests.get(
        f"{connection.connection_string}/rest/v1/bir_forms",
        headers={'apikey': connection.api_key}
    )
```

### With Superset Dashboards
```python
# Auto-configure Superset database connections
superset_conn = self.env['insightpulse.connection.endpoint'].search([
    ('connection_type', '=', 'superset')
], limit=1)

# Generate Superset database URI
db_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
```

### With MCP Servers
```python
# Manage MCP server endpoints
mcp_servers = self.env['insightpulse.connection.endpoint'].search([
    ('connection_type', '=', 'mcp')
])

for server in mcp_servers:
    # Register MCP server URL for bridge connections
    mcp_config[server.name] = {
        'url': server.base_url,
        'api_key': server.api_key,
    }
```

## Output Formats

### Connection String
```
postgresql://postgres:password@db.spdtwktxdalcfigzeqrz.supabase.co:5432/postgres
```

### Environment Variables
```bash
SUPABASE_PRODUCTION_URL=postgresql://postgres:password@db.spdtwktxdalcfigzeqrz.supabase.co:5432/postgres
SUPABASE_PRODUCTION_USER=postgres
SUPABASE_PRODUCTION_PASSWORD=password
```

### Docker Compose
```yaml
services:
  app:
    environment:
      - DATABASE_URL=postgresql://postgres:password@db.spdtwktxdalcfigzeqrz.supabase.co:5432/postgres
```

## BIR Compliance Integration

### Connection for BIR Systems
```xml
<record id="endpoint_bir_portal" model="insightpulse.connection.endpoint">
    <field name="name">BIR eFPS Portal API</field>
    <field name="connection_type">api</field>
    <field name="base_url">https://efps.bir.gov.ph</field>
    <field name="api_key">YOUR_BIR_API_KEY</field>
</record>
```

### Usage in BIR Module
```python
# Fetch BIR connection for form submission
bir_conn = self.env['insightpulse.connection.endpoint'].search([
    ('name', 'ilike', 'BIR')
], limit=1)

# Submit Form 1601-C via API
import requests
response = requests.post(
    f"{bir_conn.base_url}/api/submit/1601-c",
    headers={'Authorization': f'Bearer {bir_conn.api_key}'},
    json=form_data
)
```

## Security Best Practices

### Access Control
```xml
<!-- security/connection_security.xml -->
<record id="group_connection_manager" model="res.groups">
    <field name="name">Connection Manager</field>
    <field name="category_id" ref="base.module_category_administration"/>
</record>

<record id="group_connection_admin" model="res.groups">
    <field name="name">Connection Administrator</field>
    <field name="category_id" ref="base.module_category_administration"/>
    <field name="implied_ids" eval="[(4, ref('group_connection_manager'))]"/>
</record>
```

### Password Encryption
```python
from cryptography.fernet import Fernet

def _encrypt_password(self, password):
    """Encrypt sensitive credentials"""
    key = self.env['ir.config_parameter'].sudo().get_param('connection.encryption.key')
    f = Fernet(key.encode())
    return f.encrypt(password.encode()).decode()

def _decrypt_password(self, encrypted_password):
    """Decrypt credentials for use"""
    key = self.env['ir.config_parameter'].sudo().get_param('connection.encryption.key')
    f = Fernet(key.encode())
    return f.decrypt(encrypted_password.encode()).decode()
```

## Examples

### Example 1: Multi-Agency Database Connections

```python
# Create connections for 8 agencies
agencies = ['RIM', 'CKVC', 'BOM', 'JPAL', 'JLI', 'JAP', 'LAS', 'RMQB']

for agency in agencies:
    self.env['insightpulse.connection.endpoint'].create({
        'name': f'{agency} Database',
        'connection_type': 'postgresql',
        'base_url': 'db.spdtwktxdalcfigzeqrz.supabase.co',
        'port': 5432,
        'database_name': f'{agency.lower()}_db',
        'username': 'postgres',
        'password': os.getenv(f'{agency}_DB_PASSWORD'),
    })
```

### Example 2: Connection Health Dashboard

```python
def get_connection_health_dashboard(self):
    """Generate health metrics for all connections"""
    connections = self.env['insightpulse.connection.endpoint'].search([])
    
    health_data = {
        'total': len(connections),
        'active': len(connections.filtered(lambda c: c.status == 'success')),
        'failed': len(connections.filtered(lambda c: c.status == 'failed')),
        'not_tested': len(connections.filtered(lambda c: c.status == 'draft')),
        'by_type': {}
    }
    
    for conn_type in ['supabase', 'postgresql', 'odoo', 'superset', 'mcp', 'api']:
        type_conns = connections.filtered(lambda c: c.connection_type == conn_type)
        health_data['by_type'][conn_type] = len(type_conns)
    
    return health_data
```

### Example 3: Auto-Generate .env File

```python
def generate_env_file(self):
    """Generate complete .env file for deployment"""
    connections = self.env['insightpulse.connection.endpoint'].search([])
    
    env_content = "# InsightPulse AI - Connection Configuration\n"
    env_content += "# Auto-generated from Connection Manager\n\n"
    
    for conn in connections:
        safe_name = conn.name.upper().replace(' ', '_').replace('-', '_')
        env_content += f"# {conn.name}\n"
        env_content += f"{safe_name}_URL={conn.connection_string}\n"
        env_content += f"{safe_name}_USER={conn.username}\n"
        env_content += f"{safe_name}_PASSWORD={conn.password}\n"
        if conn.api_key:
            env_content += f"{safe_name}_API_KEY={conn.api_key}\n"
        env_content += "\n"
    
    return env_content
```

## Cost Savings

By using this self-hosted connection manager:
- **No vendor lock-in**: Own your infrastructure
- **Zero licensing costs**: Open-source solution  
- **Integrated workflow**: All connections in one place
- **Replaces**: Paid connection management tools ($50-200/month)

**Annual Savings**: $600-2,400

## Production Deployment

### Installation
```bash
# Copy module to Odoo addons
cp -r insightpulse_connection_manager /odoo/addons/

# Update module list in Odoo
# Apps → Update Apps List

# Install module
# Apps → Search "InsightPulse Connection Manager" → Install
```

### Docker Deployment
```yaml
# docker-compose.yml
services:
  odoo:
    image: odoo:19
    volumes:
      - ./insightpulse_connection_manager:/mnt/extra-addons/insightpulse_connection_manager
```

### Kubernetes Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: odoo
spec:
  template:
    spec:
      containers:
      - name: odoo
        volumeMounts:
        - name: addons
          mountPath: /mnt/extra-addons/insightpulse_connection_manager
```

## Troubleshooting

### Connection Test Fails
```python
# Check psycopg2 is installed
pip install psycopg2-binary

# Verify firewall rules
# Ensure port 5432 is open for PostgreSQL connections

# Check credentials
# Verify username/password in Supabase/Odoo settings
```

### Permission Denied
```bash
# Add user to connection manager group
# Settings → Users → Select User → Groups → Add "Connection Manager"
```

## License

LGPL-3.0 (required for Odoo modules)

## References

- [Supabase Connection Strings](https://supabase.com/docs/guides/database/connecting-to-postgres)
- [Odoo 19 Models Guide](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html)
- [Apache Superset Database Connections](https://superset.apache.org/docs/databases/installing-database-drivers/)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

**Built for Finance Shared Service Centers managing multi-agency operations with self-hosted infrastructure.**
