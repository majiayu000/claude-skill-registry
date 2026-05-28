---
name: odoo-app-automator
description: "AI agent for automated Odoo module creation, deployment, and third-party integration. Scaffolds custom modules, generates Odoo Studio configurations, sets up containers, and automates app deployment following Odoo 19 best practices."
---

# Odoo App Automator

AI-powered automation for creating, deploying, and managing Odoo modules and custom applications. This skill enables AI agents to generate production-ready Odoo modules, configure Studio customizations, set up containerized deployments, and integrate third-party services.

## Purpose

Automate the entire lifecycle of Odoo custom module development:
- **Module Scaffolding**: Generate complete Odoo module structures with models, views, security, and data
- **Studio Integration**: Programmatically configure Odoo Studio customizations
- **Container Deployment**: Set up Odoo.sh containers with dependencies and configurations
- **Third-Party Integration**: Connect external APIs, payment providers, and business services
- **Upgrade Management**: Handle version upgrades and module migrations

## When to Use This Skill

Use this skill when the user requests:
- "Create a custom Odoo module for [purpose]"
- "Build an Odoo app for [business process]"
- "Automate [workflow] in Odoo"
- "Deploy a custom Odoo module"
- "Integrate [third-party service] with Odoo"
- "Set up Odoo Studio customizations"
- "Migrate custom module from Odoo [version] to [version]"

## Core Capabilities

### 1. Module Scaffolding

Generate complete Odoo module structures following best practices:

**Module Structure:**
```
custom_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── custom_model.py
├── views/
│   ├── custom_views.xml
│   └── menu_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security_groups.xml
├── data/
│   └── default_data.xml
├── static/
│   ├── description/
│   │   ├── index.html
│   │   └── icon.png
│   └── src/
│       ├── js/
│       ├── css/
│       └── xml/
├── wizards/
├── reports/
├── controllers/
└── README.md
```

**Key Files to Generate:**

1. **`__manifest__.py`**: Module metadata
2. **`models/*.py`**: Business logic and database models
3. **`views/*.xml`**: UI definitions (form, tree, kanban, search)
4. **`security/ir.model.access.csv`**: Access control rules
5. **`data/*.xml`**: Default data and demo data
6. **`README.md`**: Documentation

### 2. Odoo Studio Automation

Configure Studio customizations programmatically:

**Studio Capabilities:**
- Add/modify fields to existing models
- Create custom views (form, list, kanban, pivot, graph)
- Define automated actions and workflows
- Set up filters and default values
- Configure access rights and security rules
- Create reports and dashboards

**Workflow:**
1. Export Studio customizations as modules
2. Version control Studio-created modules
3. Deploy to production via git
4. Update Studio configs via XML data files

### 3. Container Setup (Odoo.sh)

Configure Odoo.sh containers with custom requirements:

**Directory Structure:**
```
/home/odoo/
├── src/
│   ├── odoo/          # Odoo Community
│   ├── enterprise/    # Odoo Enterprise
│   ├── themes/        # Themes
│   └── user/          # Custom modules
├── data/
│   ├── filestore/     # Attachments
│   └── sessions/      # User sessions
└── logs/
    ├── odoo.log
    ├── install.log
    └── pip.log
```

**Dependencies Management:**

Create `requirements.txt` in repository root:
```txt
# Python dependencies
pandas>=1.5.0
requests>=2.28.0
pillow>=9.0.0
paddleocr>=2.6.0
supabase>=1.0.0
```

**Custom Commands:**

```bash
# Install module
odoo-bin -i custom_module --stop-after-init

# Update module
odoo-bin -u custom_module --stop-after-init

# Run tests
odoo-bin -i custom_module --test-enable --log-level=test --stop-after-init

# Odoo shell
odoo-bin shell
```

### 4. Third-Party Integration

Integrate external services into Odoo:

**Common Integrations:**
- **Payment Providers**: Stripe, PayPal, Paymongo (PH)
- **Shipping**: FedEx, DHL, LBC (PH)
- **Accounting**: QuickBooks, Xero
- **CRM**: Salesforce, HubSpot
- **Communication**: Slack, Microsoft Teams
- **Storage**: Google Drive, Dropbox, Supabase
- **AI/ML**: OpenAI, Anthropic Claude, PaddleOCR

**Integration Pattern:**

1. **Create API Wrapper Model:**
```python
class ExternalService(models.Model):
    _name = 'external.service'
    
    api_key = fields.Char(string='API Key')
    base_url = fields.Char(string='Base URL')
    
    def call_api(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.request(method, url, headers=headers, json=data)
        return response.json()
```

2. **Add Configuration UI**
3. **Implement Webhook Handlers**
4. **Set Up Scheduled Actions**

### 5. Upgrade Management

Handle version migrations for custom modules:

**Upgrade Workflow:**
1. Request test upgrade from Odoo.sh or upgrade.odoo.com
2. Update custom module code for new version
3. Test upgraded database thoroughly
4. Deploy to production

**Module Version Compatibility:**
```python
# __manifest__.py
{
    'name': 'Custom Module',
    'version': '19.0.1.0.0',  # Format: {odoo_version}.{major}.{minor}.{patch}
    'depends': ['base', 'sale', 'account'],
}
```

## Practical Examples for Finance SSC

### Example 1: BIR Tax Filing Module

**User Request:** "Create an Odoo module for BIR tax form filing (1601-C, 2550Q, 1702-RT)"

**Module Structure:**
```
bir_tax_filing/
├── models/
│   ├── bir_form_1601c.py
│   ├── bir_form_2550q.py
│   └── bir_form_1702rt.py
├── views/
│   ├── bir_form_views.xml
│   └── bir_filing_schedule_views.xml
├── wizards/
│   └── bir_filing_wizard.py
├── reports/
│   ├── bir_pdf_reports.xml
│   └── bir_dat_export.py
└── data/
    └── bir_default_schedules.xml
```

**Key Features:**
- Automated form generation from accounting data
- Filing schedule tracking
- .DAT file export for eBIRForms
- Compliance dashboard
- Multi-agency support (RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB)

### Example 2: Travel & Expense Management (SAP Concur Alternative)

**User Request:** "Build a self-hosted travel and expense management app"

**Module Features:**
- Travel request workflow
- Expense report submission
- Receipt OCR with PaddleOCR
- Policy validation
- Multi-level approvals
- GL account posting
- Budget tracking

**Cost Savings:** $15,000/year in licensing fees

### Example 3: Superset Dashboard Integration

**User Request:** "Connect Odoo data to Apache Superset dashboards"

**Implementation:**
1. Create database connector in Superset
2. Build Odoo API endpoints for dashboard data
3. Set up scheduled data synchronization
4. Create pre-built dashboard templates

**Use Cases:**
- BIR compliance metrics
- Month-end closing progress
- Multi-agency financial KPIs

### Example 4: Notion Workflow Sync

**User Request:** "Sync finance tasks between Notion and Odoo"

**Implementation:**
1. Notion API integration module
2. Task synchronization with external ID upserts
3. Webhook handlers for real-time updates
4. Scheduled actions for batch sync

## Module Generation Workflow

### Step 1: Requirements Gathering

Ask the user:
1. **Module Purpose**: What business process does this automate?
2. **Core Entities**: What are the main data models?
3. **User Workflows**: What actions will users perform?
4. **Integrations**: Which external systems need to connect?
5. **Security**: Who should have access to what?
6. **Reporting**: What reports/dashboards are needed?

### Step 2: Generate Module Structure

Create all necessary files:
1. **__manifest__.py** with dependencies and metadata
2. **models/** with Python classes for each entity
3. **views/** with XML definitions for UI
4. **security/** with access control rules
5. **data/** with default records
6. **README.md** with usage instructions

### Step 3: Add Business Logic

Implement:
- Field validations and constraints
- Computed fields
- CRUD operations
- Workflow automation
- API integrations

### Step 4: Configure Security

Define:
- User groups
- Access rights (read, write, create, unlink)
- Record rules (domain-based access)
- Field-level security

### Step 5: Create UI Views

Build:
- Form views (detail page)
- Tree views (list page)
- Kanban views (card layout)
- Search views (filters, group by)
- Dashboard widgets

### Step 6: Testing & Deployment

1. **Local Testing**:
```bash
odoo-bin -d test_db -i custom_module --test-enable
```

2. **Deploy to Odoo.sh**:
```bash
git add custom_module/
git commit -m "Add custom module"
git push origin staging
```

3. **Install in Production**:
   - Test in staging branch first
   - Merge to production branch
   - Auto-deployment triggered

## Best Practices

### Code Quality

1. **Follow OCA Guidelines**: Use Odoo Community Association standards
2. **Use Python Type Hints**: Improve code readability
3. **Write Docstrings**: Document all models and methods
4. **Add Unit Tests**: Ensure reliability
5. **Validate XML**: Check view definitions

### Performance

1. **Optimize Queries**: Use `_read_group()` for aggregations
2. **Lazy Loading**: Use `@api.depends` wisely
3. **Index Database Fields**: Add `index=True` to frequently queried fields
4. **Cache Computed Fields**: Use `store=True` when appropriate

### Security

1. **Never Trust User Input**: Validate and sanitize
2. **Use Record Rules**: Restrict data access by domain
3. **Encrypt Sensitive Data**: Use `password=True` for password fields
4. **Audit Logging**: Track important changes
5. **Rate Limiting**: Prevent API abuse

### Maintenance

1. **Version Control**: Use git with semantic versioning
2. **Migration Scripts**: Provide upgrade paths
3. **Backup Data**: Regular database backups
4. **Monitor Logs**: Watch for errors and performance issues
5. **Documentation**: Keep README up-to-date

## Common Pitfalls to Avoid

1. **Missing Dependencies**: Always declare in `__manifest__.py`
2. **Hardcoded Values**: Use configuration parameters instead
3. **No Access Rules**: Module won't be accessible without security/ir.model.access.csv
4. **Circular Dependencies**: Check module dependency graph
5. **Unused Fields**: Don't add fields you won't use
6. **Poor Naming**: Use clear, descriptive names
7. **Skipping Tests**: Test before deploying to production

## Integration with User's Stack

### InsightPulse AI Infrastructure

**Components:**
- **Odoo 19 ERP**: Primary application (self-hosted with OCA modules)
- **Apache Superset**: BI dashboards (replaces Tableau, saves $4,728/year)
- **Supabase**: PostgreSQL database (project: spdtwktxdalcfigzeqrz)
- **MCP Servers**: Notion, Google Drive integration
- **PaddleOCR**: Receipt and BIR form processing

**Module Integration Points:**
1. Connect to Supabase for centralized data
2. Sync with Notion for task management
3. Send analytics to Superset dashboards
4. Process documents with PaddleOCR
5. Store files in Google Drive

### Multi-Agency Configuration

Support for 8 agencies:
- RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB

**Implementation:**
```python
class FinanceAgency(models.Model):
    _name = 'finance.agency'
    
    code = fields.Selection([
        ('RIM', 'RIM'),
        ('CKVC', 'CKVC'),
        ('BOM', 'BOM'),
        ('JPAL', 'JPAL'),
        ('JLI', 'JLI'),
        ('JAP', 'JAP'),
        ('LAS', 'LAS'),
        ('RMQB', 'RMQB'),
    ], required=True)
    
    name = fields.Char(required=True)
    tin = fields.Char(string='TIN')
    rdo_code = fields.Char(string='RDO Code')
```

## Output Format

When generating a module, provide:

1. **Complete Module ZIP**: Ready to install in Odoo
2. **Installation Instructions**: Step-by-step deployment guide
3. **Configuration Guide**: How to set up after installation
4. **User Documentation**: How to use the module
5. **Developer Notes**: Architecture decisions and extension points

## References

- [Odoo 19 Developer Documentation](https://www.odoo.com/documentation/19.0/developer.html)
- [Odoo.sh Containers Guide](https://www.odoo.com/documentation/19.0/administration/odoo_sh/advanced/containers.html)
- [Odoo Studio Documentation](https://www.odoo.com/documentation/19.0/applications/studio.html)
- [Odoo Apps & Modules Management](https://www.odoo.com/documentation/19.0/applications/general/apps_modules.html)
- [Odoo Upgrade Process](https://www.odoo.com/documentation/19.0/administration/upgrade.html)
- [OCA Guidelines](https://github.com/OCA/odoo-community.org)

---

**Built for Finance Shared Service Centers managing multi-agency operations with self-hosted infrastructure.**
