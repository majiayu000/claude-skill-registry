---
name: odoo19-oca-devops
description: Build enterprise-grade Odoo 19 ERP using OCA community modules instead of Enterprise licenses. Scaffold modules, vendor OCA dependencies, generate production Docker deployments, and deploy to DigitalOcean with Supabase - saving $4,728/year in licensing costs.
---

# Odoo 19 OCA DevOps Expert

Transform Claude into an Odoo 19 DevOps expert that helps you build enterprise-grade ERP systems using free OCA (Odoo Community Association) modules instead of paying for Odoo Enterprise licenses.

## What This Skill Does

**Replace Odoo Enterprise** ($4,320/year for 10 users) with **OCA modules** ($0/year)  
**Self-host on DigitalOcean** ($288/year) instead of **Odoo.sh** ($720/year)  
**Build custom modules** following OCA standards for your business needs

**Total Annual Savings: $4,752 (94% cost reduction)**

## Quick Start

When asked to build an Odoo 19 system:

1. **Scaffold module**: Create OCA-compliant module structure
2. **Map enterprise features**: Identify OCA alternatives to Enterprise modules
3. **Vendor OCA modules**: Clone and pin OCA repositories with version locking
4. **Generate deployment**: Create production docker-compose with PostgreSQL/Supabase
5. **Deploy**: Provision DigitalOcean droplet and deploy with SSL

## Core Workflows

### Workflow 1: Create Custom Module

```
User asks: "Create a module for expense management"

Steps:
1. Identify requirements and dependencies
2. Use scaffold_oca_module pattern to create structure
3. Generate __manifest__.py with OCA standards
4. Create models/, views/, security/ directories
5. Add README.rst in OCA format
6. Validate module structure

Result: Complete OCA-compliant module ready for development
```

See [examples/scaffold-module.md](examples/scaffold-module.md) for full example.

### Workflow 2: Replace Enterprise Features

```
User asks: "What OCA modules replace Odoo Studio and Accounting Reports?"

Steps:
1. Parse enterprise features requested
2. Map to OCA module equivalents using enterprise_alternatives pattern
3. Provide installation commands
4. Calculate cost savings
5. Show feature comparison

Result: List of OCA modules with installation guide
```

See [reference/enterprise-alternatives.md](reference/enterprise-alternatives.md) for complete mapping.

### Workflow 3: Vendor OCA Dependencies

```
User asks: "Vendor OCA modules for accounting and helpdesk"

Steps:
1. Identify OCA repositories needed
2. Use oca_vendor_pinned pattern
3. Sparse clone specific modules
4. Pin commits for stability
5. Generate repos.yaml lockfile
6. Create requirements-oca.txt
7. Validate Odoo 19 compatibility

Result: Vendored OCA modules with version locking
```

See [examples/vendor-oca.md](examples/vendor-oca.md) for full workflow.

### Workflow 4: Generate Production Deployment

```
User asks: "Deploy Odoo 19 to insightpulseai.net with Supabase"

Steps:
1. Use docker_compose_generate pattern
2. Configure Odoo 19 container with workers
3. Setup PostgreSQL or Supabase connection
4. Configure Nginx reverse proxy
5. Setup Let's Encrypt SSL
6. Generate deployment scripts
7. Create .env template

Result: Production-ready docker-compose.yml
```

See [examples/production-deployment.md](examples/production-deployment.md) for full example.

### Workflow 5: Deploy to DigitalOcean

```
User asks: "Provision DigitalOcean droplet and deploy"

Steps:
1. Use digitalocean_provision pattern
2. Create droplet with Docker pre-installed
3. Attach volume for filestore
4. Copy deployment files
5. Configure SSL with certbot
6. Start services
7. Create production database

Result: Live Odoo 19 instance with SSL
```

See [examples/digitalocean-deploy.md](examples/digitalocean-deploy.md) for deployment guide.

### Workflow 6: Customize with Odoo Studio

```
User asks: "Add custom fields to invoices without coding"

Steps:
1. Identify customization needs (fields, views, automation)
2. Use Odoo Studio for no-code customization
3. Add custom fields to models
4. Customize views (Form, List, Kanban)
5. Create automation rules for workflows
6. Export customizations for version control

Result: Customized Odoo without Python code
```

**What Studio Can Do**:
- Add custom fields (20+ types: Text, Date, Selection, Many2One, etc.)
- Customize views (Form, List, Kanban, Calendar, Map, Timeline)
- Create automation rules (triggers, conditions, actions)
- Design custom reports
- Build workflows without coding

**When to Use Studio vs Python**:
- **Studio**: Simple customizations, prototyping, business user changes
- **Python**: Complex logic, external APIs, performance-critical code, unit tests

See [reference/odoo-studio.md](reference/odoo-studio.md) for complete Studio guide.

## Implementation Patterns

### Module Scaffolding Pattern

**Purpose**: Create OCA-compliant module structure with all required files

**Structure**:
```
addons/[module_name]/
├── __manifest__.py          # OCA-compliant manifest
├── __init__.py              # Module imports
├── README.rst               # OCA documentation format
├── models/                  # Python models
├── views/                   # XML views
├── security/                # Access rules
│   └── ir.model.access.csv
├── data/                    # Master data
├── demo/                    # Demo data
├── static/
│   ├── description/         # Module description
│   └── src/                 # JS/CSS assets
├── tests/                   # Unit tests
├── wizards/                 # Transient models
└── reports/                 # Report templates
```

**Key Files**:
- `__manifest__.py`: AGPL-3 license, proper version (19.0.1.0.0), author, website
- `README.rst`: OCA template with usage, credits, maintainers
- `security/ir.model.access.csv`: Access control rules
- License headers on all Python files

See [reference/oca-module-structure.md](reference/oca-module-structure.md) for details.

### OCA Vendoring Pattern

**Purpose**: Pin OCA modules to specific commits for stability

**Process**:
1. Identify OCA repositories and modules needed
2. Sparse checkout only needed modules
3. Pin to specific git commit SHA
4. Record in repos.yaml lockfile
5. Extract Python requirements

**repos.yaml format**:
```yaml
server-tools:
  url: https://github.com/OCA/server-tools
  branch: "19.0"
  commit: abc123def456
  modules: [base_technical_user, sentry]

account-financial-reporting:
  url: https://github.com/OCA/account-financial-reporting
  branch: "19.0"
  commit: def456abc789
  modules: [account_financial_report, mis_builder]
```

See [reference/oca-vendoring.md](reference/oca-vendoring.md) for full pattern.

### Docker Deployment Pattern

**Purpose**: Production-ready Odoo 19 deployment with security hardening

**Components**:
- **Odoo 19 container**: Multi-worker configuration, memory limits
- **PostgreSQL/Supabase**: Database backend with optional pgvector
- **Nginx**: Reverse proxy, SSL termination, rate limiting, security headers
- **Certbot**: Automatic SSL certificate renewal

**Configuration**:
- Workers: 4 (handles concurrent requests)
- Cron threads: 2 (background jobs)
- Memory limits: 2GB soft, 2.5GB hard
- Database manager: Blocked via Nginx
- SSL: TLS 1.2+, modern cipher suites

See [reference/docker-production.md](reference/docker-production.md) for configuration.

## Enterprise Feature Mapping

Common Odoo Enterprise features and their OCA alternatives:

| Enterprise Feature | OCA Alternative | Repo | Annual Savings |
|-------------------|----------------|------|----------------|
| **Odoo Studio** | Manual customization + OCA tools | See [reference/odoo-studio.md](reference/odoo-studio.md) | $432/user |
| Accounting Reports | account_financial_report | OCA/account-financial-reporting | $432/user |
| Helpdesk | helpdesk_mgmt | OCA/helpdesk | $432/user |
| Project Advanced | project_* modules | OCA/project | $432/user |
| HR Expenses | hr_expense_* modules | OCA/hr-expense | $432/user |
| Dashboards | mis_builder | OCA/reporting-engine | $432/user |
| Manufacturing | mrp_*, quality_control_* | OCA/manufacture | $432/user |
| Sign | agreement_* | OCA/contract | $432/user |

**For 10 users: $4,320/year saved**

See [reference/enterprise-alternatives.md](reference/enterprise-alternatives.md) for complete list.

## Cost Analysis

### Your Stack (Self-Hosted)
```
OCA Modules:                  $0/year    ✅ FREE (AGPL-3)
Odoo Community Edition:       $0/year    ✅ FREE (LGPL-3)
Custom IPAI Modules:          $0/year    ✅ Your IP
DigitalOcean Droplet (4GB):   $288/year  (Infrastructure)
Domain + SSL:                 $24/year   (Let's Encrypt free)
────────────────────────────────────────────────────
TOTAL:                        $312/year
```

### Odoo Enterprise (10 Users)
```
User Licenses (10 × $36):    $4,320/year
Odoo.sh Hosting:             $720/year
────────────────────────────────────────────────────
TOTAL:                       $5,040/year
```

### Savings: $4,728/year (94% reduction)

The more users you have, the more you save - no per-user fees with Community Edition!

## Technical Stack

```
┌─────────────────────────────────┐
│  Your Domain (SSL with Nginx)  │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│  Odoo 19 (Docker Container)    │
│  ├── Custom IPAI Modules       │
│  └── OCA Modules (vendored)    │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│  PostgreSQL 15 + pgvector       │
│  (Supabase or Local)            │
└─────────────────────────────────┘
```

**Deployment Options**:
- **Local Development**: Docker Compose on laptop
- **Production**: DigitalOcean droplet with volumes
- **Database**: Supabase (managed) or local PostgreSQL
- **Storage**: DigitalOcean Spaces or local volumes

## Common Use Cases

### Use Case 1: Document OCR System (Your IPAI Project)
```
1. Scaffold ipai_document_ocr module
2. Integrate PaddleOCR for receipt scanning
3. Connect to Supabase pgvector for embeddings
4. Auto-extract expense line items
5. Deploy with 4 workers for concurrent processing
```

### Use Case 2: Expense Management (SAP Concur Alternative)
```
1. Scaffold ipai_expense_management module
2. Vendor OCA hr-expense modules (hr_expense_advance_clearing)
3. Add multi-level approval workflows
4. Integrate with BIR tax compliance
5. Deploy with expense OCR integration
```

### Use Case 3: BIR Tax Compliance (Philippines)
```
1. Scaffold ipai_bir_compliance module
2. Vendor OCA account-financial-reporting modules
3. Generate Form 1601-C, 2550Q, 1702-RT
4. ATP (Authorization to Print) integration
5. Automated filing workflows
```

## Best Practices

1. **Always use OCA structure**: Follow oca-addons-repo-template standards
2. **Pin OCA versions**: Use repos.yaml with commit SHAs
3. **Separate custom from OCA**: Keep your modules in addons/, OCA in addons/oca/
4. **Document everything**: README.rst in OCA format
5. **Test before deploy**: Local testing with demo data
6. **Version properly**: Use 19.0.x.y.z format (Odoo.series.major.minor.patch)
7. **License correctly**: AGPL-3 for community sharing, proprietary for closed source
8. **Backup regularly**: Database + filestore before upgrades

## Common Issues

**"Can't install module"**: Check dependencies in __manifest__.py, verify addons_path
**"OCA module incompatible"**: Check branch (must be 19.0), vendor specific commit
**"Docker won't start"**: Check .env file exists, ports 8069/8072 not in use
**"Database connection failed"**: Verify DB_PASSWORD in .env, check host/port
**"Nginx 502 error"**: Odoo container not started yet, check logs
**"Module not found"**: Module not in addons_path, verify volume mounts

## Reference Documentation

Implementation patterns and templates:
- [reference/oca-module-structure.md](reference/oca-module-structure.md) - Module scaffolding
- [reference/enterprise-alternatives.md](reference/enterprise-alternatives.md) - Feature mapping
- [reference/oca-vendoring.md](reference/oca-vendoring.md) - Version locking
- [reference/docker-production.md](reference/docker-production.md) - Deployment config
- [reference/supabase-integration.md](reference/supabase-integration.md) - Database setup

## Examples

Complete workflow examples:
- [examples/scaffold-module.md](examples/scaffold-module.md) - Create custom module
- [examples/vendor-oca.md](examples/vendor-oca.md) - Vendor dependencies
- [examples/production-deployment.md](examples/production-deployment.md) - Deploy to production
- [examples/digitalocean-deploy.md](examples/digitalocean-deploy.md) - Infrastructure setup

## Tools Available

This skill uses standard Claude tools:
- **bash_tool**: Execute Docker, git, and system commands
- **create_file**: Generate configuration files
- **str_replace**: Edit existing files
- **view**: Read files and directories

No custom MCP servers required - works with base Claude functionality.

## Success Metrics

After using this skill, you should have:
- ✅ 4+ custom IPAI modules following OCA standards
- ✅ 10+ OCA modules vendored with version locking
- ✅ Production Odoo 19 instance on DigitalOcean
- ✅ SSL configured with Let's Encrypt
- ✅ $4,728/year saved vs Odoo Enterprise
- ✅ Full DevOps automation
- ✅ Unlimited users at no additional cost

## Getting Started

Ask Claude:
```
"Create an OCA module for expense management with approval workflows"
"Show me OCA alternatives for Studio and Helpdesk with installation commands"
"Generate production docker-compose for insightpulseai.net with Supabase"
"Vendor OCA modules: server-tools, account-financial-reporting, helpdesk"
```

Your enterprise-grade ERP for $312/year starts here! 🚀
