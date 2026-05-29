---
name: odoo-agile-scrum-devops
description: Comprehensive Agile Scrum framework for Odoo ERP development with Finance Shared Service Center workflows, OCA community standards, CI/CD automation, BIR compliance, and multi-agency task management. Use when planning Odoo sprints, managing Finance SSC operations, deploying to DigitalOcean, or coordinating work across agencies (RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB).
---

# Odoo Agile Scrum DevOps Master Skill

## Overview
This skill combines Agile Scrum methodologies with Odoo development best practices, Finance Shared Service Center operations, OCA community standards, and enterprise DevOps workflows. It's specifically designed for managing odoboo-workspace and InsightPulse AI projects with integration to Notion, Supabase, and DigitalOcean.

## When to Use This Skill

**Trigger this skill for:**
- Planning Odoo module development sprints (odoboo-workspace, InsightPulse AI)
- Creating user stories for Finance SSC features (BIR compliance, month-end closing, travel & expense)
- Setting up CI/CD pipelines for Odoo 18/19 deployments
- Managing multi-agency workflows across RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB
- Integrating Odoo with Notion task management via MCP tools
- Deploying to DigitalOcean (project ID: 29cde7a1-8280-46ad-9fdf-dea7b21a7825)
- Connecting Odoo to Supabase (project: spdtwktxdalcfigzeqrz) for pgvector operations
- Implementing OCA module standards and contributing to OCA repositories

## Project Context

### Core Projects
1. **odoboo-workspace**: Odoo 18/19 deployment with OCA modules, DigitalOcean hosting, Supabase integration
2. **InsightPulse AI** (insightpulseai.net): Self-hosted Odoo ERP with AI document processing (PaddleOCR, RTX 4090)
3. **Finance SSC**: Multi-agency Philippine tax compliance and month-end closing automation

### Tech Stack
- **ERP**: Odoo 18/19 Community with OCA modules
- **Cloud**: DigitalOcean App Platform, Managed PostgreSQL, Spaces (S3)
- **Database**: Supabase PostgreSQL with pgvector, Qdrant vector database
- **AI/ML**: PaddleOCR-VL, Custom OCR models for BIR forms
- **DevOps**: Docker, GitHub Actions, pre-commit hooks
- **Frontend**: Vercel deployments for custom dashboards
- **Orchestration**: Docker Compose, SuperClaude multi-agent framework

---

## Sprint Planning Framework

### Sprint Cycle (2-week iterations)

#### Week 1: Planning & Development
**Days 1-2: Sprint Planning**
1. **Backlog Grooming** (use Notion MCP tools)
   ```
   Use notion-fetch to retrieve sprint backlog from Notion database
   Review and prioritize user stories with Product Owner
   Estimate story points using Fibonacci sequence (1,2,3,5,8,13,21)
   ```

2. **Sprint Goal Definition**
   - Define clear, measurable sprint goal
   - Align with Finance SSC monthly objectives (month-end closing, BIR deadlines)
   - Identify dependencies across agencies

3. **Task Breakdown** (use notion-create-pages)
   - Break user stories into technical tasks
   - Assign to team members or agencies
   - Set up task tracking with External ID for deduplication

**Days 3-8: Active Development**
- Daily standup (async via Notion comments)
- Continuous integration via GitHub Actions
- Code review with OCA standards validation

#### Week 2: Review & Deployment
**Days 9-10: Sprint Review & Demo**
- Demo to stakeholders (Finance SSC team, agency representatives)
- Deploy to DigitalOcean staging environment
- Update sprint metrics in Notion

**Days 11-12: Retrospective & Planning Prep**
- Retrospective (What went well? What needs improvement?)
- Prepare backlog for next sprint
- Update documentation

### User Story Templates

#### Finance SSC User Story Template
```markdown
## User Story: [Feature Name]

**As a** [Finance Manager / Accountant / BIR Compliance Officer]  
**I want** [specific functionality]  
**So that** [business value / time saved / compliance achieved]

**Agency Impact:** [RIM / CKVC / BOM / JPAL / JLI / JAP / LAS / RMQB / All]

**Acceptance Criteria:**
- [ ] Criterion 1 (must be testable)
- [ ] Criterion 2 (must be measurable)
- [ ] Criterion 3 (must include compliance requirement if BIR-related)
- [ ] Automated tests written and passing
- [ ] Documentation updated in Notion

**Story Points:** [Fibonacci number]  
**Priority:** [Critical / High / Medium / Low]  
**Sprint:** [Sprint number and date range]

**Technical Notes:**
- Odoo module: [module_name]
- OCA dependencies: [list OCA modules]
- Supabase integration: [Yes/No, describe if yes]
- External APIs: [BIR, Notion, other]

**Definition of Done:**
- [ ] Code reviewed by 2 team members
- [ ] Passes pre-commit hooks (pylint-odoo, flake8)
- [ ] Unit tests coverage >= 80%
- [ ] Integration tests passing
- [ ] Deployed to staging and validated
- [ ] User acceptance testing completed
- [ ] Production deployment successful
- [ ] Monitoring alerts configured
```

#### Example: BIR Form 1601-C Automation
```markdown
## User Story: Automated BIR Form 1601-C Generation

**As a** Finance Manager  
**I want** automated generation of BIR Form 1601-C with employee withholding tax data  
**So that** I save 3 hours per month and ensure 100% BIR compliance accuracy

**Agency Impact:** All (RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB)

**Acceptance Criteria:**
- [ ] System reads employee payroll data from Odoo HR module
- [ ] Generates XML in BIR eFPS format (Form 1601-C)
- [ ] Validates ATP (Authorization to Print) requirements
- [ ] Creates audit trail in Odoo with document versioning
- [ ] Supports multiple agencies with separate TIN codes
- [ ] Email notification sent to Finance SSC manager upon generation
- [ ] PDF preview generated before submission

**Story Points:** 8  
**Priority:** Critical  
**Sprint:** Sprint 12 - Nov 1-15, 2025

**Technical Notes:**
- Odoo module: `finance_bir_compliance`
- OCA dependencies: `account`, `hr_payroll`, `report_xlsx`
- Supabase integration: No
- External APIs: BIR eFPS API (staging), Email service

**BIR Compliance Requirements:**
- Form must include: TIN, Taxpayer Name, Address, Return Period
- Withholding tax amounts must be rounded to 2 decimal places
- XML schema validation against BIR XSD
- ATP number must be printed on hard copy

**Definition of Done:**
- [x] Code reviewed by 2 team members
- [x] Passes pre-commit hooks
- [x] Unit tests coverage 85%
- [x] Integration tests with BIR staging API passing
- [ ] Deployed to staging and validated by Finance Manager
- [ ] UAT completed with sample data from all 8 agencies
- [ ] Production deployment planned for Nov 20, 2025
- [ ] Sentry monitoring configured for BIR API errors
```

#### Example: Travel Expense OCR Processing
```markdown
## User Story: Receipt OCR with PaddleOCR Integration

**As a** Employee submitting travel expenses  
**I want** to upload receipt photos that are automatically processed  
**So that** I don't spend 15 minutes manually entering data per receipt

**Agency Impact:** All

**Acceptance Criteria:**
- [ ] Mobile upload interface accepts JPG/PNG/PDF
- [ ] PaddleOCR extracts: merchant name, date, total amount, tax amount
- [ ] Confidence score >= 90% for auto-approval, <90% flags for review
- [ ] Extracted data populates Odoo expense form fields
- [ ] Original image stored in DigitalOcean Spaces
- [ ] OCR results stored in Supabase with pgvector for similarity search
- [ ] Supports multiple languages (English, Tagalog)

**Story Points:** 13  
**Priority:** High  
**Sprint:** Sprint 13 - Nov 16-30, 2025

**Technical Notes:**
- Odoo module: `expense_management_ocr`
- OCA dependencies: `hr_expense`, `document_management`
- Supabase integration: Yes (pgvector for receipt deduplication)
- External APIs: None (self-hosted PaddleOCR on RTX 4090)
- Hardware: RTX 4090 optimization required

**Definition of Done:**
- [ ] Code reviewed by 2 team members
- [ ] GPU memory optimization completed (batch processing)
- [ ] 95% accuracy on test dataset (100 sample receipts)
- [ ] Response time < 3 seconds per receipt
- [ ] Deployed to staging with GPU server
- [ ] Performance testing under load (50 concurrent uploads)
- [ ] User documentation created with video tutorial
```

---

## Odoo Development Standards

### OCA Module Structure

Follow OCA community standards for all Odoo modules:

```
my_odoo_module/
├── __init__.py
├── __manifest__.py          # Module metadata, dependencies, version
├── models/
│   ├── __init__.py
│   ├── model_name.py        # Business logic, field definitions
│   └── model_name_view.xml  # UI views
├── views/
│   ├── menu_items.xml
│   └── templates.xml
├── security/
│   ├── ir.model.access.csv  # Access control
│   └── security_groups.xml
├── data/
│   └── data.xml             # Master data
├── reports/
│   └── report_template.xml
├── static/
│   ├── description/
│   │   ├── icon.png
│   │   └── index.html
│   └── src/
│       ├── js/
│       └── css/
├── tests/
│   ├── __init__.py
│   ├── test_model.py
│   └── test_integration.py
├── i18n/                    # Translations
│   ├── en_US.po
│   └── fil_PH.po           # Filipino translation
├── README.rst
└── LICENSE
```

### __manifest__.py Template

```python
# Copyright 2025 Jake Tolentino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Finance BIR Compliance",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Philippine BIR tax forms automation and compliance",
    "author": "Jake Tolentino, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-philippines",
    "license": "AGPL-3",
    "depends": [
        "account",
        "hr_payroll",
        "l10n_ph",  # Philippine localization
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/bir_form_views.xml",
        "views/menu_items.xml",
        "reports/bir_1601c_report.xml",
    ],
    "demo": [
        "demo/bir_form_demo.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
```

### Git Workflow

#### Branch Naming Convention (OCA Standard)
```bash
# Format: {version}-{type}-{module_name}
# Types: feature, fix, refactor, docs

# Examples:
git checkout -b 19.0-feature-finance_bir_compliance
git checkout -b 18.0-fix-expense_ocr_confidence
git checkout -b 19.0-refactor-multi_agency_reports
```

#### Commit Message Convention
```bash
# Format: [TAG] module_name: Short description
# Tags: ADD, FIX, REF, REM, MOV, REL, I18N, MERGE

# Examples:
git commit -m "[ADD] finance_bir_compliance: BIR Form 1601-C XML generator"
git commit -m "[FIX] expense_ocr: Handle rotated receipt images"
git commit -m "[REF] multi_agency: Optimize database queries for 8 agencies"
git commit -m "[I18N] finance_bir: Add Filipino translations for forms"
```

#### Pre-commit Hooks Setup
```bash
# Install pre-commit framework
pip install pre-commit --break-system-packages

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/OCA/pylint-odoo
    rev: v8.0.20
    hooks:
      - id: pylint-odoo
        args: ["--rcfile=.pylintrc"]
        
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        args: ["--line-length=88"]
        
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ["--max-line-length=88", "--extend-ignore=E203,W503"]
        
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile=black"]
        
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ["--maxkb=1024"]
EOF

# Install hooks
pre-commit install
```

---

## CI/CD Pipeline Configuration

### GitHub Actions Workflow

Create `.github/workflows/odoo-ci-cd.yml`:

```yaml
name: Odoo CI/CD Pipeline

on:
  push:
    branches: [main, develop, '**-feature-**', '**-fix-**']
  pull_request:
    branches: [main, develop]

env:
  ODOO_VERSION: "19.0"
  POSTGRESQL_VERSION: "15"
  DO_PROJECT_ID: "29cde7a1-8280-46ad-9fdf-dea7b21a7825"
  SUPABASE_PROJECT_ID: "spdtwktxdalcfigzeqrz"

jobs:
  lint:
    name: Code Quality Checks
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install --break-system-packages pre-commit pylint-odoo flake8 black isort
          
      - name: Run pre-commit hooks
        run: pre-commit run --all-files
        
      - name: Run pylint-odoo
        run: |
          find . -name "*.py" -not -path "./venv/*" | xargs pylint-odoo --rcfile=.pylintrc

  test:
    name: Unit & Integration Tests
    runs-on: ubuntu-latest
    needs: lint
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: odoo
          POSTGRES_PASSWORD: odoo_test_password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Build Odoo test image
        run: |
          docker build -t odoo-test:${{ env.ODOO_VERSION }} \
            --build-arg ODOO_VERSION=${{ env.ODOO_VERSION }} \
            -f Dockerfile.test .
            
      - name: Run Odoo unit tests
        run: |
          docker run --rm \
            --network host \
            -e DB_HOST=localhost \
            -e DB_PORT=5432 \
            -e DB_USER=odoo \
            -e DB_PASSWORD=odoo_test_password \
            odoo-test:${{ env.ODOO_VERSION }} \
            odoo -d test_db -i finance_bir_compliance,expense_management_ocr \
            --test-enable --stop-after-init --log-level=test
            
      - name: Run integration tests
        run: |
          pytest tests/integration/ -v --cov=. --cov-report=xml
          
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: unittests
          name: odoo-coverage

  security-scan:
    name: Security Vulnerability Scan
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  build-and-push:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [test, security-scan]
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Login to DigitalOcean Container Registry
        uses: docker/login-action@v3
        with:
          registry: registry.digitalocean.com
          username: ${{ secrets.DO_REGISTRY_TOKEN }}
          password: ${{ secrets.DO_REGISTRY_TOKEN }}
          
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: registry.digitalocean.com/odoboo-workspace/odoo
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
            
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=registry.digitalocean.com/odoboo-workspace/odoo:buildcache
          cache-to: type=registry,ref=registry.digitalocean.com/odoboo-workspace/odoo:buildcache,mode=max

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.insightpulseai.net
    
    steps:
      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DO_API_TOKEN }}
          
      - name: Deploy to DigitalOcean App Platform
        run: |
          doctl apps create-deployment ${{ secrets.DO_STAGING_APP_ID }} --wait
          
      - name: Run database migrations
        run: |
          doctl apps run-command ${{ secrets.DO_STAGING_APP_ID }} \
            --component odoo \
            --command "odoo -d staging_db -u all --stop-after-init"
            
      - name: Notify Notion (use MCP when available in Actions)
        run: |
          echo "Deployment to staging completed at $(date)" >> $GITHUB_STEP_SUMMARY

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://insightpulseai.net
    
    steps:
      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DO_API_TOKEN }}
          
      - name: Create database backup
        run: |
          doctl databases backups create ${{ secrets.DO_DATABASE_ID }}
          
      - name: Deploy to Production
        run: |
          doctl apps create-deployment ${{ secrets.DO_PROD_APP_ID }} --wait
          
      - name: Run database migrations
        run: |
          doctl apps run-command ${{ secrets.DO_PROD_APP_ID }} \
            --component odoo \
            --command "odoo -d production_db -u all --stop-after-init"
            
      - name: Smoke tests
        run: |
          curl -f https://insightpulseai.net/health || exit 1
          
      - name: Notify stakeholders
        run: |
          echo "✅ Production deployment successful!" >> $GITHUB_STEP_SUMMARY
          echo "- Deployed at: $(date)" >> $GITHUB_STEP_SUMMARY
          echo "- Commit: ${{ github.sha }}" >> $GITHUB_STEP_SUMMARY

  notify-sentry:
    name: Create Sentry Release
    runs-on: ubuntu-latest
    needs: deploy-production
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Create Sentry release
        uses: getsentry/action-release@v1
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
          SENTRY_ORG: ${{ secrets.SENTRY_ORG }}
          SENTRY_PROJECT: insightpulse-ai
        with:
          environment: production
          version: ${{ github.sha }}
```

---

## Notion Integration via MCP Tools

### Sprint Task Synchronization

Use Notion MCP tools to sync Odoo sprint tasks:

```python
# Example: Create sprint tasks in Notion from Odoo Project module

# Step 1: Fetch existing sprint database structure
Use notion-fetch tool with database_id to get schema

# Step 2: Create tasks with External ID for deduplication
Use notion-create-pages with this structure:
{
  "parent": {"data_source_id": "sprint-database-collection-id"},
  "pages": [
    {
      "properties": {
        "Task Name": "BIR Form 1601-C Generator",
        "Sprint": "Sprint 12 - Nov 2025",
        "Status": "In Progress",
        "Story Points": 8,
        "Agency": "All Agencies",
        "Assignee": "Jake Tolentino",
        "date:Due Date:start": "2025-11-15",
        "date:Due Date:is_datetime": 0,
        "Priority": "Critical",
        "Odoo Module": "finance_bir_compliance",
        "External ID": "ODOO-TASK-1234"  # For upsert pattern
      },
      "content": """
# Technical Details
- **Odoo Module:** finance_bir_compliance
- **OCA Dependencies:** account, hr_payroll
- **GitHub Branch:** 19.0-feature-finance_bir_compliance

## Acceptance Criteria
- [ ] Generate XML in BIR eFPS format
- [ ] Validate ATP requirements
- [ ] Support all 8 agencies (RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB)
- [ ] Create audit trail in Odoo

## Related Resources
- [Odoo Module Documentation](link)
- [BIR Form 1601-C Specifications](link)
"""
    }
  ]
}

# Step 3: Upsert pattern for updates
# Use External ID to check if task already exists
# If exists, use notion-update-page to modify
# If not exists, create new page
```

### Month-End Closing Task Template

```python
# Month-end closing tasks for Finance SSC
# Create these tasks at the start of each month

MONTH_END_TASKS = [
    {
        "Task Name": "RIM - Bank Reconciliation",
        "Agency": "RIM",
        "Story Points": 3,
        "Status": "To Do",
        "date:Due Date:start": "2025-11-05",
        "Priority": "High",
        "External ID": "MONTH-END-RIM-BANK-NOV2025"
    },
    {
        "Task Name": "CKVC - Journal Entry Review",
        "Agency": "CKVC",
        "Story Points": 2,
        "Status": "To Do",
        "date:Due Date:start": "2025-11-07",
        "Priority": "High",
        "External ID": "MONTH-END-CKVC-JE-NOV2025"
    },
    {
        "Task Name": "All Agencies - Trial Balance Generation",
        "Agency": "All Agencies",
        "Story Points": 5,
        "Status": "To Do",
        "date:Due Date:start": "2025-11-10",
        "Priority": "Critical",
        "External ID": "MONTH-END-ALL-TB-NOV2025"
    },
    {
        "Task Name": "BIR - Form 1601-C Submission (All Agencies)",
        "Agency": "All Agencies",
        "Story Points": 8,
        "Status": "To Do",
        "date:Due Date:start": "2025-11-12",
        "Priority": "Critical",
        "External ID": "BIR-1601C-NOV2025"
    },
    {
        "Task Name": "Multi-Agency Consolidation",
        "Agency": "All Agencies",
        "Story Points": 13,
        "Status": "To Do",
        "date:Due Date:start": "2025-11-15",
        "Priority": "Critical",
        "External ID": "MONTH-END-CONSOLIDATION-NOV2025"
    }
]

# Use notion-create-pages to bulk create these tasks
```

---

## Multi-Agency Management

### Agency Configuration

```python
# Agency codes and metadata
AGENCIES = {
    "RIM": {
        "full_name": "Research Institute Manila",
        "tin": "123-456-789-000",
        "address": "Manila, Philippines",
        "currency": "PHP",
        "fiscal_year_end": "12-31"
    },
    "CKVC": {
        "full_name": "Centro Kingsford Ventures Corporation",
        "tin": "234-567-890-000",
        "address": "Quezon City, Philippines",
        "currency": "PHP",
        "fiscal_year_end": "12-31"
    },
    "BOM": {
        "full_name": "Bureau of Management",
        "tin": "345-678-901-000",
        "address": "Makati, Philippines",
        "currency": "PHP",
        "fiscal_year_end": "12-31"
    },
    "JPAL": {
        "full_name": "J-PAL Southeast Asia",
        "tin": "456-789-012-000",
        "address": "Manila, Philippines",
        "currency": "PHP",
        "fiscal_year_end": "12-31"
    },
    "JLI": {
        "full_name": "Justice Leadership Initiative",
        "tin": "567-890-123-000",
        "address": "Quezon City, Philippines",
        "currency": "PHP",
        "fiscal_year_end": "12-31"
    },
    "JAP": {
        "full_name": "Justice Action Program",
        "tin": "678-901-234-000",
        "address": "Manila, Philippines",
        "currency": "PHP",
        "fiscal_year_end": "12-31"
    },
    "LAS": {
        "full_name": "Legal Aid Society",
        "tin": "789-012-345-000",
        "address": "Makati, Philippines",
        "currency": "PHP",
        "fiscal_year_end": "12-31"
    },
    "RMQB": {
        "full_name": "Research Management Quality Bureau",
        "tin": "890-123-456-000",
        "address": "Quezon City, Philippines",
        "currency": "PHP",
        "fiscal_year_end": "12-31"
    }
}
```

### Multi-Agency User Stories

When creating user stories that impact multiple agencies:

1. **Specify Agency Impact** in user story template
2. **Create separate tasks per agency** if implementation differs
3. **Use "All Agencies" label** for consolidated reports/features
4. **Test with real data** from each agency during UAT

Example:
```markdown
## User Story: Multi-Agency Consolidation Report

**As a** Finance SSC Director  
**I want** consolidated financial statements across all 8 agencies  
**So that** I can report to the Board of Directors monthly

**Agency Impact:** All (RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB)

**Acceptance Criteria:**
- [ ] Pull trial balance from each agency's Odoo instance
- [ ] Eliminate inter-company transactions automatically
- [ ] Generate consolidated Income Statement, Balance Sheet, Cash Flow
- [ ] Support drill-down to agency-level details
- [ ] Export to Excel with proper formatting
- [ ] Complete processing in < 5 minutes for all 8 agencies

**Story Points:** 21 (highest complexity)  
**Priority:** Critical
```

---

## Supabase Integration Patterns

### pgvector for Document Similarity Search

Use Supabase (project: spdtwktxdalcfigzeqrz) for:
- Receipt deduplication via image embeddings
- BIR form template matching
- Semantic search across financial documents

```sql
-- Create vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create receipts table with vector embeddings
CREATE TABLE receipts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    odoo_expense_id INTEGER UNIQUE,
    agency_code VARCHAR(10) NOT NULL,
    receipt_image_url TEXT NOT NULL,
    merchant_name VARCHAR(255),
    receipt_date DATE,
    total_amount NUMERIC(12, 2),
    tax_amount NUMERIC(12, 2),
    ocr_confidence NUMERIC(3, 2),
    embedding vector(512),  -- PaddleOCR image embedding
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX receipts_embedding_idx ON receipts 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create RPC function for duplicate detection
CREATE OR REPLACE FUNCTION find_duplicate_receipts(
    query_embedding vector(512),
    similarity_threshold FLOAT DEFAULT 0.95,
    limit_results INT DEFAULT 5
)
RETURNS TABLE (
    receipt_id UUID,
    agency_code VARCHAR(10),
    similarity_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id,
        agency_code,
        1 - (embedding <=> query_embedding) AS similarity_score
    FROM receipts
    WHERE 1 - (embedding <=> query_embedding) > similarity_threshold
    ORDER BY embedding <=> query_embedding
    LIMIT limit_results;
END;
$$ LANGUAGE plpgsql;
```

### Real-time Subscription for Task Updates

```javascript
// Subscribe to Notion task updates via Supabase
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://spdtwktxdalcfigzeqrz.supabase.co',
  process.env.SUPABASE_ANON_KEY
)

// Subscribe to sprint task changes
const subscription = supabase
  .channel('sprint-tasks')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'notion_tasks',
      filter: 'sprint=eq.Sprint 12 - Nov 2025'
    },
    (payload) => {
      console.log('Task updated:', payload)
      // Sync back to Odoo Project module if needed
      syncTaskToOdoo(payload.new)
    }
  )
  .subscribe()
```

---

## DevOps Metrics & Monitoring

### DORA Metrics Tracking

Track these key DevOps metrics in Superset dashboard:

1. **Deployment Frequency**
   - Target: Daily to production
   - Measure: Count of successful deployments per day
   - Query: `SELECT DATE(deployed_at), COUNT(*) FROM deployments GROUP BY DATE(deployed_at)`

2. **Lead Time for Changes**
   - Target: < 1 day (commit to production)
   - Measure: Time from commit to successful deployment
   - Query: `SELECT AVG(deployed_at - committed_at) FROM deployments`

3. **Mean Time to Recovery (MTTR)**
   - Target: < 1 hour
   - Measure: Time from incident detection to resolution
   - Query: `SELECT AVG(resolved_at - detected_at) FROM incidents WHERE severity = 'critical'`

4. **Change Failure Rate**
   - Target: < 5%
   - Measure: Percentage of deployments causing failures
   - Query: `SELECT (COUNT(*) FILTER (WHERE failed = true) * 100.0 / COUNT(*)) FROM deployments`

### Sentry Integration for Error Tracking

Configure Sentry in your Odoo deployment:

```python
# In odoo.conf or environment variables
[sentry]
enabled = True
dsn = https://your-sentry-dsn@sentry.io/project-id
environment = production
release = ${GIT_COMMIT_SHA}
traces_sample_rate = 0.1  # 10% of transactions

# In your Odoo module
import sentry_sdk
from sentry_sdk.integrations.odoo import OdooIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
    release=os.getenv("GIT_COMMIT_SHA", "unknown"),
    integrations=[OdooIntegration()],
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
)
```

---

## Scrum Ceremonies

### Daily Standup (Async via Notion)

Create a Notion page for daily updates:

```markdown
# Daily Standup - [Date]

## Team Member 1 (Jake Tolentino)
**Yesterday:**
- ✅ Completed BIR Form 1601-C XML generator
- ✅ Code review for OCR confidence scoring

**Today:**
- 🚧 Integration testing with BIR eFPS staging API
- 🚧 Deploy to DigitalOcean staging environment

**Blockers:**
- ⚠️ Waiting for BIR ATP approval for production testing

## Team Member 2
...
```

### Sprint Retrospective Template

```markdown
# Sprint [Number] Retrospective - [Date Range]

## Sprint Goal
[State the sprint goal]

**Achievement:** [Met / Partially Met / Not Met]

## Metrics
- **Story Points Committed:** 34
- **Story Points Completed:** 32
- **Velocity:** 32
- **Bugs Found:** 3
- **Bugs Fixed:** 5
- **Code Coverage:** 87%

## What Went Well 🎉
1. BIR Form 1601-C automation deployed successfully
2. All 8 agencies validated the output format
3. CI/CD pipeline reduced deployment time by 40%

## What Needs Improvement 🔧
1. OCR confidence scoring needs more training data
2. Integration tests are slow (10+ minutes)
3. Documentation lagging behind code changes

## Action Items for Next Sprint
- [ ] **Jake:** Collect 500 more receipt samples for OCR training
- [ ] **Team:** Parallelize integration tests to reduce runtime
- [ ] **All:** Update README files during development, not after

## Shoutouts 🌟
- Thanks to Finance SSC team for quick UAT feedback!
- Great collaboration between RIM and CKVC on data format standardization
```

---

## Best Practices Summary

### Odoo Development
1. **Always follow OCA standards** (module structure, commit messages, code style)
2. **Write tests first** (TDD approach) - aim for 80%+ coverage
3. **Use external IDs** for all data records (enables proper upgrades)
4. **Document your code** with docstrings and README files
5. **Optimize database queries** - use `_search()` efficiently, avoid N+1 queries

### Agile Scrum
1. **Keep user stories small** (completable within 1 sprint)
2. **Define clear acceptance criteria** (testable and measurable)
3. **Maintain a healthy backlog** (2-3 sprints ahead, properly prioritized)
4. **Respect the Definition of Done** - no shortcuts
5. **Retrospectives are sacred** - always improve

### DevOps
1. **Automate everything** (testing, deployment, monitoring)
2. **Infrastructure as Code** (Docker Compose, Terraform)
3. **Monitor in production** (Sentry, Grafana, alerts)
4. **Fast feedback loops** (CI/CD should complete in < 15 minutes)
5. **Continuous improvement** (track DORA metrics, iterate)

### Finance SSC Specific
1. **BIR compliance is non-negotiable** - always validate against official specs
2. **Audit trail for everything** - who did what, when, why
3. **Multi-agency testing required** - don't assume one size fits all
4. **Month-end closing is time-sensitive** - plan sprint timing accordingly
5. **Data security and privacy** - encrypt PII, restrict access, log everything

---

## Quick Reference Commands

```bash
# Start new sprint
git checkout -b 19.0-feature-sprint-13-setup
notion-create-pages --database "Sprint Backlog" --tasks sprint_13_tasks.json

# Run tests locally
docker-compose up -d postgres
docker-compose run --rm odoo odoo -d test_db -i module_name --test-enable

# Deploy to staging
git push origin develop
# CI/CD automatically deploys to staging

# Create release
git checkout main
git merge develop
git tag -a v1.2.0 -m "Sprint 13 Release - BIR Compliance Features"
git push origin main --tags
# CI/CD automatically deploys to production

# Monitor production
doctl apps logs $DO_PROD_APP_ID --follow
# Or check Sentry dashboard

# End sprint retrospective
notion-create-pages --page "Retrospectives" --template sprint_retro_template.md
```

---

## Resources & Documentation

### Odoo
- Official Docs: https://www.odoo.com/documentation/19.0/
- OCA Guidelines: https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst
- OCA Module Template: https://github.com/OCA/maintainer-tools/tree/master/template

### Agile & Scrum
- Scrum Guide: https://scrumguides.org/
- Agile Manifesto: https://agilemanifesto.org/

### DevOps
- DORA Metrics: https://dora.dev/
- Twelve-Factor App: https://12factor.net/
- DigitalOcean Docs: https://docs.digitalocean.com/

### Tools
- Notion API: https://developers.notion.com/
- Supabase Docs: https://supabase.com/docs
- Sentry SDK: https://docs.sentry.io/platforms/python/
- GitHub Actions: https://docs.github.com/en/actions

---

## Changelog

**v1.0.0 - 2025-11-01**
- Initial release of Odoo Agile Scrum DevOps skill
- Finance SSC workflows for 8 agencies (RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB)
- BIR compliance automation (Forms 1601-C, 1702-RT, 2550Q)
- Notion MCP integration for sprint task management
- CI/CD pipeline with GitHub Actions and DigitalOcean
- Supabase pgvector integration for OCR deduplication
- Multi-agency consolidated reporting
