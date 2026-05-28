---
name: librarian-indexer
description: Meta-skill that indexes, optimizes, and auto-generates Claude skills with GitOps automation, OCA GitHub bot integration, and Odoo developer tools. Use for skill creation, CI/CD workflows, OCA module management, and advanced Odoo development.
---

# Librarian Indexer Skill v2.0

## Purpose
Advanced meta-skill that combines knowledge base optimization, skill auto-generation, GitOps automation, OCA GitHub bot workflows, and Odoo developer mode expertise for maximum development efficiency.

## Version History
```yaml
v2.0.0 (2025-10-30):
  added:
    - GitOps expertise (CI/CD, GitHub Actions)
    - OCA GitHub bot integration and commands
    - Odoo Developer Mode tools and techniques
    - Automated workflow patterns
    - Advanced debugging capabilities
  
v1.0.0 (2025-10-30):
  - Initial release
  - Core skill templates
  - Knowledge base optimization
  - Skill taxonomy
```

## Core Functions

### 1. Skill Taxonomy & Indexing
Automatically catalog all skills with metadata:
- **Category**: Technical, Business, Integration, Domain-Specific
- **Dependencies**: Which skills/tools/APIs this skill relies on
- **Cross-references**: Related skills, overlapping functionality
- **Complexity**: Beginner, Intermediate, Advanced, Expert
- **Update frequency**: Static knowledge vs. rapidly evolving domains
- **GitOps**: CI/CD pipeline requirements, automated testing

### 2. GitOps Expertise

#### CI/CD Pipeline Architecture
```yaml
github_actions_workflows:
  
  module_testing:
    name: "Test Odoo Module"
    trigger: [push, pull_request]
    steps:
      - checkout_code
      - setup_odoo_environment
      - install_dependencies
      - run_unit_tests
      - run_integration_tests
      - generate_coverage_report
    best_practices:
      - Use OCA's maintainer-tools for testing
      - Test against multiple Odoo versions
      - Cache dependencies for speed
      - Fail fast on critical errors
  
  docker_build_push:
    name: "Build and Push Docker Image"
    trigger: [push_to_main, release]
    steps:
      - checkout_code
      - setup_docker_buildx
      - login_to_registry
      - build_multi_arch_image  # AMD64, ARM64
      - push_to_dockerhub
      - create_github_release
    best_practices:
      - Use multi-stage builds
      - Tag with version + latest
      - Sign images for security
      - Use BuildKit for caching
  
  oca_bot_integration:
    name: "OCA Bot Automated Workflows"
    trigger: [pull_request_review, schedule]
    commands:
      - /ocabot merge [major|minor|patch|nobump]
      - /ocabot rebase
      - /ocabot migration <module_name>
    automation:
      - Auto-generate README.rst from fragments
      - Auto-generate addon icons
      - Auto-update setup.py
      - Auto-approve with 2+ approvals
      - Auto-merge after 5 days + green CI
  
  deployment_pipeline:
    name: "Deploy to Production"
    trigger: [release, manual_dispatch]
    environments: [staging, production]
    steps:
      - run_all_tests
      - build_docker_image
      - push_to_registry
      - deploy_to_staging
      - run_smoke_tests
      - manual_approval
      - deploy_to_production
      - rollback_on_failure
```

#### Git Workflow Patterns
```bash
# OCA-compliant Git workflow

# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/OCA_REPO.git
cd OCA_REPO
git remote add upstream https://github.com/OCA/OCA_REPO.git

# 2. Create feature branch from target version
git checkout -b 19.0-feat-new-feature origin/19.0

# 3. Make changes following OCA conventions
# - One commit per logical change
# - Conventional commit messages: feat:, fix:, docs:, etc.
# - Sign commits: git commit -s

# 4. Pre-commit hooks (OCA maintainer-tools)
pre-commit install
pre-commit run --all-files

# 5. Push and create PR
git push origin 19.0-feat-new-feature
# Create PR via GitHub UI targeting OCA/19.0

# 6. Use OCA bot commands in PR
# /ocabot merge minor  (auto-merge with version bump)
# /ocabot rebase       (rebase on target branch)
# /ocabot migration module_name  (track migration)

# 7. After merge, sync fork
git checkout 19.0
git fetch upstream
git merge upstream/19.0
git push origin 19.0
```

#### GitHub Actions Templates
```yaml
# .github/workflows/test.yml
name: Test Odoo Modules

on:
  push:
    branches: [19.0, 18.0]
  pull_request:
    branches: [19.0, 18.0]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        odoo-version: ['19.0']
        python-version: ['3.11']
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          
      - name: Install OCA maintainer-tools
        run: |
          git clone https://github.com/OCA/maintainer-tools.git
          cd maintainer-tools
          pip install -r requirements.txt
          
      - name: Install Odoo
        run: |
          git clone --depth=1 --branch=${{ matrix.odoo-version }} https://github.com/odoo/odoo.git
          pip install -r odoo/requirements.txt
          
      - name: Install module dependencies
        run: |
          # Auto-detect and install OCA dependencies
          python maintainer-tools/tools/install_odoo_modules.py
          
      - name: Run tests
        run: |
          export ODOO_RC=/dev/null
          python -m pytest tests/ --cov=. --cov-report=xml
          
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

# .github/workflows/dockerhub-publish.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']
  release:
    types: [published]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
        
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
          
      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: yourorg/insightpulse-odoo
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 3. OCA GitHub Bot Integration

#### Bot Commands
```bash
# Available commands in OCA repositories

# Merge with version bump
/ocabot merge major     # Breaking changes (1.0.0 -> 2.0.0)
/ocabot merge minor     # New features (1.0.0 -> 1.1.0)
/ocabot merge patch     # Bug fixes (1.0.0 -> 1.0.1)
/ocabot merge nobump    # No version change (tests, docs)

# Rebase PR on target branch
/ocabot rebase

# Track module migration
/ocabot migration account_payment_order
# Links PR to migration issue for version tracking

# Bot will automatically:
# ✅ Merge when CI is green and approved
# ✅ Bump version in __manifest__.py
# ✅ Update CHANGELOG with oca-towncrier
# ✅ Generate wheels and upload to PyPI
# ✅ Run all post-merge operations
```

#### Bot Automated Operations

**Webhooks (Real-time)**:
```yaml
on_pull_request_opened:
  - mention_maintainers  # @-mention addon maintainers
  - call_for_maintainers # If no maintainers, ask for volunteers
  
on_pull_request_approved:
  - set_approved_label  # When 2+ approvals
  - set_ready_to_merge_label  # When >5 days old
  
on_ci_success:
  - set_needs_review_label  # Unless "wip:" in title
  
on_merge:
  - delete_pr_branch  # Auto-cleanup
  - bump_version  # If requested
  - update_changelog  # With oca-towncrier
  - generate_wheel  # Upload to PyPI
```

**Scheduled Tasks (Nightly)**:
```yaml
daily_maintenance:
  - update_readme_table  # Addons table in README.md
  - generate_addon_readme  # From readme/ fragments
  - generate_addon_icons  # Default OCA icon if missing
  - update_setup_py  # Via setuptools-odoo-make-defaults
  - generate_wheels  # For all addons
  - upload_to_pypi  # Or rsync to PEP 503 index
```

#### Setting Up OCA Bot for Your Org

```bash
# 1. Clone and configure
git clone https://github.com/OCA/oca-github-bot.git
cd oca-github-bot

# 2. Create .env file
cp environment.sample .env

# Edit .env with your settings:
GITHUB_TOKEN=ghp_xxxxx  # GitHub PAT with repo access
GITHUB_SECRET=your_webhook_secret
BOT_TASKS=all  # Or specific tasks
BOT_TASKS_DISABLED=  # Tasks to disable

# 3. Docker Compose deployment
docker-compose up -d

# Services started:
# - Bot webhook server (port 8080)
# - Celery worker (task processor)
# - Celery beat (scheduler)
# - Flower (monitoring at port 5555)
# - Redis (message queue)

# 4. Configure GitHub webhook
# URL: https://your-bot-url.com/webhooks
# Content type: application/json
# Secret: [value from GITHUB_SECRET]
# Events: All or specific (pull_request, push, etc.)

# 5. Test locally with ngrok
ngrok http 8080
# Use ngrok URL for GitHub webhook during development
```

#### Custom Bot Tasks

```python
# src/oca_github_bot/tasks/custom_validation.py

from celery import task
from ..github import gh_call

@task()
def validate_module_structure(org, repo, pr_number):
    """Custom task: Validate Odoo module structure"""
    
    # Get PR files
    files = gh_call(f'repos/{org}/{repo}/pulls/{pr_number}/files')
    
    required_files = [
        '__manifest__.py',
        '__init__.py',
        'README.rst',
        'security/ir.model.access.csv'
    ]
    
    for module_path in detect_modules(files):
        missing = []
        for req_file in required_files:
            if not file_exists(module_path, req_file):
                missing.append(req_file)
        
        if missing:
            # Post comment on PR
            gh_call(
                f'repos/{org}/{repo}/issues/{pr_number}/comments',
                method='POST',
                data={
                    'body': f'⚠️ Module `{module_path}` is missing: {", ".join(missing)}'
                }
            )
            return False
    
    return True
```

### 4. Odoo Developer Mode

#### Activation Methods
```python
# Method 1: Settings app
# Settings → Developer Tools → Activate the developer mode

# Method 2: URL parameter
https://example.odoo.com/odoo?debug=1      # Standard mode
https://example.odoo.com/odoo?debug=assets # With JS assets
https://example.odoo.com/odoo?debug=tests  # With test tours
https://example.odoo.com/odoo?debug=0      # Deactivate

# Method 3: Command palette (Ctrl+K or Cmd+K)
# Type "debug" → select activation mode

# Method 4: Browser extension
# Chrome: https://chromewebstore.google.com/detail/odoo-debug/...
# Firefox: https://addons.mozilla.org/firefox/addon/odoo-debug/
```

#### Developer Mode Tools

**View Architecture:**
```python
# In any view, click "Developer Mode" menu
→ Edit View: Form / Tree / Kanban / etc.
→ View Fields: See all field definitions
→ View Metadata: Created, modified, version info
→ Manage Filters: Edit search filters
→ Edit Action: Modify window actions
→ Edit Workflow: (Legacy) View state transitions

# Access technical info on any field
→ Hover over field → See technical name
→ Right-click field → "View Field"
  - Name: account_id
  - Model: account.move
  - Type: many2one
  - Widget: many2one
  - Required: True
  - Readonly: False
```

**Database Tools:**
```python
# Technical Menu Access
Settings → Technical

# Key sections:
Database Structure/
  ├── Models          # All Odoo models (res.partner, sale.order, etc.)
  ├── Fields          # Field definitions across all models
  ├── Menu Items      # Application menu structure
  ├── Views           # Form, tree, kanban, search views
  ├── Actions         # Window actions, server actions, reports
  ├── Translations    # i18n strings
  └── Parameters      # System parameters (ir.config_parameter)

Sequences/
  └── Sequences       # Number sequences (SO001, INV/2024/0001, etc.)

Automation/
  ├── Scheduled Actions (Cron)  # Background jobs
  ├── Automation Rules          # Trigger-based automation
  └── Server Actions            # Python code execution

Security/
  ├── Users & Companies
  ├── Groups                    # Access groups
  ├── Access Rights             # Model-level (ir.model.access)
  ├── Record Rules              # Row-level security
  └── Access Control Lists      # File access
```

**Python Debugging:**
```python
# In Odoo shell or code

# 1. Enable debug mode programmatically
self.env.user.write({'debug': True})

# 2. Debug ORM queries
import logging
_logger = logging.getLogger(__name__)

# Log SQL queries
_logger.setLevel(logging.DEBUG)
self.env['sale.order'].search([('state', '=', 'draft')])
# SQL: SELECT "sale_order".id FROM "sale_order" WHERE ...

# 3. Inspect recordsets
order = self.env['sale.order'].browse(1)
_logger.info(f"Order: {order}")
_logger.info(f"Fields: {order.fields_get()}")
_logger.info(f"Values: {order.read()}")

# 4. Test computed fields
order._compute_amount_total()

# 5. Check access rights
self.env['sale.order'].check_access_rights('write', raise_exception=False)
order.check_access_rule('write')

# 6. View active context
_logger.info(f"Context: {self.env.context}")

# 7. Use debugger breakpoints
import pdb; pdb.set_trace()
# Or use built-in debugger in IDE
```

**XML ID Inspector:**
```python
# Find XML ID for any record

# Method 1: Developer mode menu
→ View Metadata → External ID

# Method 2: Python
record = self.env['res.partner'].browse(1)
xml_id = record.get_external_id()
# Returns: {'1': 'base.main_partner'}

# Method 3: Search by XML ID
partner = self.env.ref('base.main_partner')

# Method 4: Create with XML ID
self.env['ir.model.data'].create({
    'module': 'my_module',
    'name': 'partner_demo',
    'model': 'res.partner',
    'res_id': partner.id,
})
```

**Performance Profiling:**
```python
# Enable profiling in odoo.conf
[options]
limit_time_cpu = 3600
limit_time_real = 7200
log_level = debug
log_db = True
log_db_level = debug

# Or via URL
?debug=1&profile=1

# View profiles at:
# /web/profiler

# Python profiling
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
self.env['sale.order'].search([])

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slow functions
```

### 5. Knowledge Base Optimization

#### Information Architecture Patterns

**Pattern 1: API-First Documentation**
Best for: Odoo, OCA, Salesforce, SAP
```markdown
Structure:
1. Quick Reference (most common operations)
2. API Endpoints/Methods (with examples)
3. Data Models/Schema
4. Integration Patterns
5. GitOps/CI-CD workflows
6. Troubleshooting Guide
7. Deep Reference (comprehensive docs)
```

**Pattern 2: Decision Tree Format**
Best for: Module selection, architecture decisions
```markdown
Structure:
1. Decision flowchart (IF/THEN logic)
2. Comparison matrices
3. Use case mappings
4. Cost/benefit analysis
5. Implementation priorities
6. GitOps automation opportunities
```

**Pattern 3: Recipe Book**
Best for: Deployment, automation, scripts
```markdown
Structure:
1. Prerequisites checklist
2. Step-by-step instructions (copy-paste ready)
3. Configuration templates
4. GitHub Actions workflows
5. OCA bot commands
6. Validation steps
7. Common pitfalls & solutions
8. Real examples from your stack
```

### 6. Skill Generation Templates

#### Template A: SaaS Replacement Skill
```markdown
# [SaaS Product] → Odoo Replacement

## Gap Analysis
- Feature comparison matrix
- OCA module coverage
- Custom module requirements
- GitOps considerations

## Implementation Guide
- Module installation order
- Configuration steps
- Integration points (Supabase, Superset, Notion)
- CI/CD pipeline setup

## Migration Path
- Data export from SaaS
- Import scripts/mappings
- User training plan
- Rollback strategy

## GitOps Automation
- GitHub Actions workflows
- Automated testing
- Deployment pipelines
- OCA bot integration

## Cost Savings
- Annual licensing: $XXX
- Self-hosted cost: $XX
- Net savings: $XXX

## Maintenance
- Update schedule
- Backup strategy
- Monitoring setup
- Support resources
```

#### Template B: GitOps Workflow Skill
```markdown
# [Project] GitOps Automation

## Repository Structure
- Branch strategy
- Commit conventions
- PR templates
- Code review process

## CI/CD Pipeline
- Test workflows
- Build processes
- Deployment stages
- Rollback procedures

## OCA Bot Integration
- Webhook configuration
- Automated tasks
- Bot commands
- Custom workflows

## Monitoring
- GitHub Actions logs
- Deployment metrics
- Error tracking
- Performance monitoring
```

#### Template C: Odoo Development Skill
```markdown
# [Module/Feature] Development Guide

## Developer Mode Setup
- Activation methods
- Debugging tools
- Performance profiling

## Module Structure
- Required files
- Naming conventions
- OCA compliance

## Development Workflow
- Local development setup
- Git workflow with OCA bot
- Testing strategy
- CI/CD integration

## Debugging Techniques
- ORM query inspection
- Computed field testing
- Access rights validation
- XML ID management
```

### 7. Skill Dependency Mapping

```yaml
skill_dependencies:
  odoo-finance-automation:
    requires:
      - odoo19-oca-devops (deployment)
      - supabase-rpc-manager (database)
      - paddle-ocr-validation (document processing)
      - gitops-odoo (CI/CD workflows)
      - oca-bot-integration (automated merges)
    integrates_with:
      - superset-dashboard-automation (reporting)
      - notion-workflow-sync (task management)
      - travel-expense-management (AP integration)
    gitops:
      - .github/workflows/test-finance-module.yml
      - .github/workflows/deploy-finance.yml
    
  oca-module-development:
    requires:
      - gitops-odoo (GitHub Actions)
      - oca-bot-integration (merge automation)
      - odoo-developer-mode (debugging)
    tools:
      - pre-commit hooks
      - OCA maintainer-tools
      - pytest for testing
    workflows:
      - Fork → Feature branch → PR → OCA bot → Merge
```

### 8. GitOps Best Practices

#### Repository Organization
```bash
odoo-project/
├── .github/
│   ├── workflows/
│   │   ├── test.yml                 # Run tests on PR
│   │   ├── deploy-staging.yml       # Auto-deploy to staging
│   │   ├── deploy-production.yml    # Manual production deploy
│   │   ├── oca-bot-sync.yml         # Sync with OCA upstream
│   │   └── security-scan.yml        # Dependency vulnerabilities
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── .pre-commit-config.yaml          # Code quality checks
├── .dockerignore
├── .gitignore
├── docker-compose.yml               # Local development
├── docker-compose.prod.yml          # Production config
├── Dockerfile                       # Multi-stage build
├── odoo.conf                        # Odoo configuration
├── requirements.txt                 # Python dependencies
└── addons/                          # Custom and OCA modules
    ├── custom_module_1/
    ├── custom_module_2/
    └── README.md
```

#### Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203,W503']
  
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile', 'black']
  
  - repo: https://github.com/OCA/pylint-odoo
    rev: 8.0.23
    hooks:
      - id: pylint_odoo
        args: ['--load-plugins=pylint_odoo']
```

#### Conventional Commits
```bash
# Format: <type>(<scope>): <subject>

# Types:
feat: New feature
fix: Bug fix
docs: Documentation only
style: Code style changes (formatting, etc.)
refactor: Code refactoring
perf: Performance improvement
test: Add or update tests
build: Build system changes
ci: CI/CD changes
chore: Other changes (dependencies, etc.)

# Examples:
git commit -m "feat(account): add BIR 1601-C report generation"
git commit -m "fix(sale): correct tax calculation for multi-currency"
git commit -m "docs(readme): update installation instructions"
git commit -m "ci: add automated testing workflow"
git commit -m "refactor(purchase): optimize RFQ performance"

# Use -s to sign commits (required by OCA)
git commit -s -m "feat(stock): add warehouse optimization"
```

### 9. Advanced Debugging Techniques

#### Debug Mode Shortcuts
```python
# Browser console tricks (with debug mode active)

# 1. Access Odoo client-side
window.odoo.__DEBUG__.services

# 2. Inspect current view
window.odoo.__DEBUG__.services.action.currentController

# 3. Call RPC from browser
await window.odoo.__DEBUG__.services.rpc('/web/dataset/call_kw', {
    model: 'sale.order',
    method: 'read',
    args: [[1], ['name', 'amount_total']],
    kwargs: {}
})

# 4. Reload assets without restart
window.location = window.location.href.replace(/\?.*/, '?debug=assets')

# 5. View loaded modules
window.odoo.define.modules
```

#### Server-side Debugging
```python
# 1. Odoo shell access
odoo-bin shell -d database_name -c /etc/odoo/odoo.conf

# In shell:
>>> env = api.Environment(cr, SUPERUSER_ID, {})
>>> partners = env['res.partner'].search([('is_company', '=', True)])
>>> partners.mapped('name')

# 2. Remote debugging (PyCharm, VSCode)
# In odoo.conf:
[options]
dev_mode = reload,qweb,werkzeug,xml

# In code:
import pydevd_pycharm
pydevd_pycharm.settrace('localhost', port=5678, stdoutToServer=True)

# 3. Logging
import logging
_logger = logging.getLogger(__name__)

_logger.debug("Debug message")
_logger.info("Info message")
_logger.warning("Warning message")
_logger.error("Error message")
_logger.exception("Exception with traceback")

# 4. SQL debugging
self.env.cr.execute("SELECT * FROM sale_order WHERE state = %s", ('draft',))
results = self.env.cr.dictfetchall()
_logger.info(f"SQL Results: {results}")
```

### 10. Skill Quality Checklist

Every skill should have:
- [ ] Clear purpose statement (1-2 sentences)
- [ ] When to use this skill (trigger patterns)
- [ ] Prerequisites/dependencies
- [ ] Quick reference section (most common operations)
- [ ] Detailed reference (comprehensive)
- [ ] Real examples from your stack
- [ ] Integration points with other skills
- [ ] GitOps automation examples
- [ ] OCA bot commands (if applicable)
- [ ] Debugging techniques
- [ ] Common pitfalls & solutions
- [ ] Update date & version info
- [ ] Links to authoritative sources
- [ ] CI/CD pipeline examples

### 11. Skill Optimization Techniques

#### Information Density
```markdown
❌ Low Density:
"You can use GitHub Actions to automate testing."

✅ High Density:
"GitHub Actions workflow: .github/workflows/test.yml
trigger: push, pull_request
steps: checkout → setup python → install deps → pytest
OCA bot auto-merges after 2 approvals + green CI + 5 days"
```

#### Actionable Focus
```markdown
❌ Vague:
"Consider using OCA bot for automation."

✅ Actionable:
"In PR comment:
/ocabot merge minor  # Auto-merge with version bump
/ocabot rebase      # Rebase on target branch
Bot runs: tests → bump version → update changelog → generate wheels → upload PyPI"
```

#### Context Embedding
```markdown
✅ Include YOUR specific context:
- "For InsightPulse-Odoo deployment..."
- "In .github/workflows/deploy.yml..."
- "Using OCA/account-financial-tools modules..."
- "Supabase project: spdtwktxdalcfigzeqrz"
- "/ocabot merge patch for hotfixes"
```

### 12. Skill Library Structure

```
/skills/
├── meta/
│   ├── librarian-indexer/           # This skill v2.0
│   ├── gitops-automation/           # CI/CD patterns
│   └── skill-creator/               # Anthropic's skill creator
├── platform/
│   ├── odoo19-oca-devops/          # OCA bot, developer mode
│   ├── github-actions/              # Workflow templates
│   ├── supabase-rpc-manager/
│   └── superset-dashboard-automation/
├── domain/
│   ├── odoo-finance-automation/
│   ├── oca-module-development/      # OCA standards
│   └── philippines-tax-compliance/
├── integration/
│   ├── oca-bot-integration/         # Bot setup & commands
│   ├── notion-workflow-sync/
│   ├── paddle-ocr-validation/
│   └── multi-agency-orchestrator/
├── saas-replacement/
│   ├── travel-expense-management/
│   ├── procurement-sourcing/
│   ├── salesforce-crm-parity/
│   └── netsuite-erp-parity/
└── templates/
    ├── saas-replacement.template.md
    ├── gitops-workflow.template.md
    ├── oca-module.template.md
    └── domain-knowledge.template.md
```

### 13. Auto-Generation Workflows

#### Workflow 1: New OCA Module Skill
```bash
Input: "Create OCA module skill for account_financial_report"

Steps:
1. Clone OCA/account-financial-tools repository
2. Analyze module structure with appsrc.py
3. Extract README.rst content
4. Document dependencies from __manifest__.py
5. Generate usage examples
6. Add OCA bot workflow integration
7. Create GitHub Actions test workflow
8. Include debugging techniques
9. Output: Complete skill file
```

#### Workflow 2: GitOps Automation Skill
```bash
Input: "Create CI/CD pipeline for [project]"

Steps:
1. Analyze project structure
2. Generate .github/workflows/*.yml
3. Configure OCA bot (if OCA repo)
4. Set up pre-commit hooks
5. Create Docker build workflow
6. Add deployment pipelines
7. Configure monitoring
8. Output: Complete GitOps setup
```

#### Workflow 3: Debug Skill Enhancement
```bash
Input: "Add debugging guide to [skill]"

Steps:
1. Load existing skill
2. Add Odoo developer mode section
3. Include ORM debugging techniques
4. Add performance profiling
5. Document common issues
6. Provide troubleshooting flowchart
7. Output: Enhanced skill
```

### 14. Skill Triggers for Auto-Loading

When Jake mentions:
- "Odoo", "OCA", "module" → Load odoo19-oca-devops + oca-bot-integration
- "GitHub Actions", "CI/CD", "workflow" → Load gitops-automation
- "debug", "developer mode", "troubleshoot" → Load odoo-developer-mode
- "/ocabot", "bot command", "auto-merge" → Load oca-bot-integration
- "BIR", "1601-C", "month-end" → Load odoo-finance-automation  
- "Supabase", "pgvector", "RPC" → Load supabase-rpc-manager
- "Superset", "dashboard", "chart" → Load superset-dashboard-automation
- "pre-commit", "pylint", "black" → Load gitops-automation
- "pytest", "test", "coverage" → Load odoo-testing-guide
- "Docker", "build", "deploy" → Load docker-deployment + gitops-automation

### 15. Best Practices Database

#### Odoo Development
```python
# ORM Best Practices
✅ DO: Use search_read for better performance
records = self.env['sale.order'].search_read(
    [('state', '=', 'draft')],
    ['name', 'amount_total']
)

❌ DON'T: Use search then read separately
records = self.env['sale.order'].search([('state', '=', 'draft')])
for record in records:
    name = record.name  # N+1 query problem

# Computed Fields
✅ DO: Use @api.depends properly
@api.depends('order_line.price_total')
def _compute_amount_total(self):
    for order in self:
        order.amount_total = sum(order.order_line.mapped('price_total'))

❌ DON'T: Forget dependencies
def _compute_amount_total(self):  # Will not recompute!
    for order in self:
        order.amount_total = sum(order.order_line.mapped('price_total'))

# Security
✅ DO: Use ir.model.access.csv + record rules
# ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sale_order_user,sale.order.user,model_sale_order,sales_team.group_sale_salesman,1,1,1,0

❌ DON'T: Use sudo() everywhere
records = self.env['sale.order'].sudo().search([])  # Bypasses security!
```

#### OCA Module Compliance
```python
# __manifest__.py Structure
{
    'name': 'Module Name',
    'version': '19.0.1.0.0',  # Major.Minor.Patch.Fix.Build
    'category': 'Accounting',
    'summary': 'Short description',
    'author': 'Your Company, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/project-name',
    'license': 'AGPL-3',  # or LGPL-3, GPL-3
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_views.xml',
        'data/account_data.xml',
    ],
    'demo': [
        'demo/account_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# Module Structure
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── account_move.py
├── views/
│   └── account_move_views.xml
├── security/
│   └── ir.model.access.csv
├── data/
│   └── account_data.xml
├── static/
│   └── description/
│       ├── index.html
│       └── icon.png
├── readme/
│   ├── CONFIGURE.rst
│   ├── USAGE.rst
│   └── CONTRIBUTORS.rst
└── tests/
    ├── __init__.py
    └── test_account.py
```

#### GitOps Best Practices
```yaml
# Workflow Optimization
✅ DO: Use caching
- name: Cache pip
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

✅ DO: Use matrix strategy for multiple versions
strategy:
  matrix:
    odoo-version: ['18.0', '19.0']
    python-version: ['3.10', '3.11']

✅ DO: Fail fast for critical issues
strategy:
  fail-fast: true
  matrix:
    ...

❌ DON'T: Hardcode secrets in workflows
# Use GitHub Secrets instead:
- name: Deploy
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}

❌ DON'T: Run expensive operations on every commit
# Use path filters:
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
```

### 16. Success Metrics

Track for each skill:
- **Usage frequency**: How often referenced
- **Success rate**: Solves problem first time?
- **Completeness**: Needs follow-up searches?
- **Accuracy**: Examples/commands correct?
- **Integration**: Works with other skills?
- **GitOps efficiency**: Reduces manual work?
- **Debugging effectiveness**: Resolves issues faster?
- **OCA compliance**: Follows standards?

### 17. Meta Notes

This skill v2.0 demonstrates advanced principles:
- ✅ Clear purpose statement
- ✅ GitOps automation integration
- ✅ OCA bot command reference
- ✅ Odoo developer mode techniques
- ✅ Actionable templates with workflows
- ✅ Real examples from CI/CD pipelines
- ✅ Decision trees and debugging flowcharts
- ✅ Integration with other skills
- ✅ Maintenance strategy
- ✅ Versioning approach

**When to use this skill:**
- Creating any new skill
- Setting up GitOps workflows
- Configuring OCA bot automation
- Debugging Odoo issues
- Optimizing existing skills
- Planning skill architecture
- Resolving skill conflicts
- Maintaining skill library
- Auto-generating documentation
- Troubleshooting CI/CD pipelines

**Success criteria:**
- Reduced time to create new skills (50% faster)
- Automated CI/CD reduces deployment time (80% faster)
- Higher quality skills (fewer iterations)
- Better debugging efficiency (70% faster issue resolution)
- Easier maintenance
- More effective Claude responses
- OCA-compliant code by default
