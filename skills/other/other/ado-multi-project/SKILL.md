---
description: Organize specs and tasks across multiple Azure DevOps projects with intelligent content-based mapping. Use when working with project-per-team, area-path-based, or team-based ADO architectures. Handles cross-project coordination and folder structure organization.
allowed-tools: Read, Write, Edit, Glob
---

# Azure DevOps Multi-Project Skill

**Purpose**: Organize specs and increments across multiple Azure DevOps projects with intelligent mapping and folder organization.

## What This Skill Does

This skill handles complex multi-project Azure DevOps organizations by:

1. **Analyzing increment content** to determine which project it belongs to
2. **Creating project-specific folder structures** in `.specweave/docs/internal/specs/`
3. **Mapping user stories to correct projects** based on keywords and context
4. **Splitting tasks across projects** when increments span multiple teams
5. **Maintaining bidirectional sync** between local specs and Azure DevOps work items

## Supported Architectures

### 1. Project-per-team (Recommended for Microservices)

```
Organization: mycompany
├── AuthService (Project)
├── UserService (Project)
├── PaymentService (Project)
└── NotificationService (Project)

Local Structure:
.specweave/docs/internal/specs/
├── AuthService/
├── UserService/
├── PaymentService/
└── NotificationService/
```

### 2. Area-path-based (Monolithic Applications)

```
Organization: enterprise
└── ERP (Project)
    ├── Finance (Area Path)
    ├── HR (Area Path)
    ├── Inventory (Area Path)
    └── Sales (Area Path)

Local Structure:
.specweave/docs/internal/specs/ERP/
├── Finance/
├── HR/
├── Inventory/
└── Sales/
```

### 3. Team-based (Small Organizations)

```
Organization: startup
└── Platform (Project)
    ├── Alpha Team
    ├── Beta Team
    └── Gamma Team

Local Structure:
.specweave/docs/internal/specs/Platform/
├── AlphaTeam/
├── BetaTeam/
└── GammaTeam/
```

## Intelligent Project Detection

The skill analyzes increment content to determine the correct project:

### Detection Patterns

```typescript
const projectPatterns = {
  'AuthService': {
    keywords: ['authentication', 'login', 'oauth', 'jwt', 'session', 'password'],
    filePatterns: ['auth/', 'login/', 'security/'],
    confidence: 0.0
  },
  'UserService': {
    keywords: ['user', 'profile', 'account', 'registration', 'preferences'],
    filePatterns: ['users/', 'profiles/', 'accounts/'],
    confidence: 0.0
  },
  'PaymentService': {
    keywords: ['payment', 'stripe', 'billing', 'invoice', 'subscription'],
    filePatterns: ['payment/', 'billing/', 'checkout/'],
    confidence: 0.0
  }
};

// Analyze spec content
const spec = readSpec(incrementId);
for (const [project, pattern] of Object.entries(projectPatterns)) {
  pattern.confidence = calculateConfidence(spec, pattern);
}

// Select project with highest confidence
const selectedProject = Object.entries(projectPatterns)
  .sort((a, b) => b[1].confidence - a[1].confidence)[0][0];
```

### Confidence Calculation

- **Keyword match**: +0.2 per keyword found
- **File pattern match**: +0.3 per pattern
- **Explicit mention**: +1.0 if project name in spec
- **Team mention**: +0.5 if team name matches

**Threshold**: Confidence > 0.7 = auto-assign, otherwise prompt user

## Usage Examples

### Example 1: Single-Project Increment

**Scenario**: Authentication feature for AuthService

**Spec Analysis**:
```
Title: "Add OAuth 2.0 authentication"
Keywords found: authentication, oauth, jwt
File patterns: src/auth/oauth-provider.ts
Confidence: AuthService = 0.9 ✅
```

**Action**:
```bash
# Auto-creates folder structure
.specweave/docs/internal/specs/AuthService/
└── spec-001-oauth-authentication.md

# Maps to Azure DevOps
Project: AuthService
Work Item: Epic "OAuth 2.0 Authentication"
```

### Example 2: Multi-Project Increment

**Scenario**: Checkout flow spanning multiple services

**Spec Analysis**:
```
Title: "Implement checkout flow with payment processing"
Keywords found: user, cart, payment, stripe, notification
Confidence:
  - UserService = 0.6
  - PaymentService = 0.8 ✅
  - NotificationService = 0.5
```

**Action**:
```bash
# Creates multi-project structure
.specweave/docs/internal/specs/
├── PaymentService/
│   └── spec-002-checkout-payment.md (primary)
├── UserService/
│   └── spec-002-checkout-user.md (linked)
└── NotificationService/
    └── spec-002-checkout-notifications.md (linked)

# Creates linked work items in Azure DevOps
PaymentService: Epic "Checkout Payment Processing" (primary)
UserService: Feature "User Cart Management" (links to primary)
NotificationService: Feature "Order Notifications" (links to primary)
```

### Example 3: Area Path Organization

**Scenario**: ERP system with module-based organization

**Configuration**:
```bash
AZURE_DEVOPS_STRATEGY=area-path-based
AZURE_DEVOPS_PROJECT=ERP
AZURE_DEVOPS_AREA_PATHS=Finance,HR,Inventory
```

**Spec Analysis**:
```
Title: "Add payroll calculation engine"
Keywords found: payroll, salary, tax, employee
Area match: HR (confidence = 0.85)
```

**Action**:
```bash
# Creates area-based structure
.specweave/docs/internal/specs/ERP/HR/
└── spec-003-payroll-engine.md

# Maps to Azure DevOps
Project: ERP
Area Path: ERP\HR
Work Item: Epic "Payroll Calculation Engine"
```

## Task Splitting Across Projects

When an increment spans multiple projects, tasks are intelligently split:

### Input: Unified tasks.md
```markdown
# Tasks for Checkout Flow

- T-001: Create shopping cart API (UserService)
- T-002: Implement Stripe integration (PaymentService)
- T-003: Add order confirmation email (NotificationService)
- T-004: Update user order history (UserService)
- T-005: Process payment webhook (PaymentService)
```

### Output: Project-specific work items

**UserService** (2 tasks):
- Task: Create shopping cart API
- Task: Update user order history

**PaymentService** (2 tasks):
- Task: Implement Stripe integration
- Task: Process payment webhook

**NotificationService** (1 task):
- Task: Add order confirmation email

## Folder Structure Creation

The skill automatically creates and maintains folder structure:

### On Increment Creation

```typescript
async function createProjectFolders(increment: Increment) {
  const projects = detectProjects(increment);

  for (const project of projects) {
    const specPath = `.specweave/docs/internal/specs/${project}/`;
    await ensureDir(specPath);

    // Create project-specific spec
    const spec = extractProjectSpec(increment, project);
    await writeSpec(`${specPath}/spec-${increment.number}-${increment.name}.md`, spec);

    // Create README if first spec in project
    if (isFirstSpec(project)) {
      await createProjectReadme(project);
    }
  }
}
```

### Project README Template

```markdown
# {Project} Specifications

## Overview
This folder contains specifications for the {Project} project.

## Architecture
{Brief description of project architecture}

## Team
- Team Lead: {name}
- Developers: {list}

## Specifications
- [spec-001-feature.md](spec-001-feature.md) - {description}

## External Links
- Azure DevOps: https://dev.azure.com/{org}/{project}
- Repository: {git-url}
```

## Sync Commands

### Sync Increment to Projects

```bash
/sw-ado:sync-increment 0014

# Detects projects from spec
# Creates work items in each project
# Links work items together
```

### Sync Spec to Project

```bash
/sw-ado:sync-spec AuthService/spec-001

# Syncs single spec to specific project
# Updates existing work item or creates new
```

### Sync All Specs

```bash
/sw-ado:sync-all

# Syncs all specs across all projects
# Maintains relationships
# Updates bidirectionally
```

## Project Mapping Configuration

### Manual Mapping (config.json)

```json
{
  "ado": {
    "projectMappings": {
      "auth-.*": "AuthService",
      "user-.*": "UserService",
      "payment-.*": "PaymentService",
      "notification-.*": "NotificationService"
    },
    "defaultProject": "Platform",
    "crossProjectLinking": true
  }
}
```

### Auto-Detection Rules

```typescript
const autoDetectionRules = [
  {
    pattern: /auth|login|oauth|security/i,
    project: "AuthService"
  },
  {
    pattern: /user|profile|account/i,
    project: "UserService"
  },
  {
    pattern: /payment|billing|stripe/i,
    project: "PaymentService"
  }
];
```

## Cross-Project Coordination

### Dependency Management

When increments span projects, dependencies are tracked:

```yaml
# .specweave/increments/0014-checkout-flow/metadata.yml
projects:
  primary: PaymentService
  dependencies:
    - UserService: [T-001, T-004]
    - NotificationService: [T-003]

ado_mappings:
  PaymentService:
    epic: 12345
    work_items: [12346, 12347]
  UserService:
    feature: 12348
    work_items: [12349, 12350]
  NotificationService:
    feature: 12351
    work_items: [12352]
```

### Cross-Project Queries

```typescript
// Find all work items for an increment across projects
async function getIncrementWorkItems(incrementId: string) {
  const metadata = await readMetadata(incrementId);
  const workItems = [];

  for (const [project, mapping] of Object.entries(metadata.ado_mappings)) {
    const items = await adoClient.getWorkItems(project, mapping.work_items);
    workItems.push(...items);
  }

  return workItems;
}
```

## Best Practices

### 1. Consistent Naming

Use consistent naming across projects:
```
spec-001-oauth-authentication.md    # Good
spec-001-auth.md                    # Too vague
SPEC_001_OAuth.md                   # Inconsistent format
```

### 2. Clear Project Boundaries

Define clear boundaries between projects:
```yaml
AuthService:
  owns: [authentication, authorization, sessions]
  not: [user profiles, user preferences]

UserService:
  owns: [profiles, preferences, user data]
  not: [authentication, passwords]
```

### 3. Link Related Specs

Link specs that span projects:
```markdown
# spec-002-checkout-payment.md

Related Specs:
- [User Cart](../UserService/spec-002-checkout-user.md)
- [Notifications](../NotificationService/spec-002-checkout-notifications.md)
```

### 4. Use Project Prefixes

Prefix increment names with primary project:
```bash
/sw:increment "payment-stripe-integration"
/sw:increment "auth-oauth-provider"
/sw:increment "user-profile-redesign"
```

## Error Handling

### Project Not Found

```
❌ Project "AuthService" not found in Azure DevOps

Options:
1. Create project "AuthService"
2. Map to existing project
3. Skip this project

Your choice [1]:
```

### Ambiguous Project Detection

```
⚠️ Cannot determine project for increment 0014

Multiple projects detected:
- UserService (confidence: 0.6)
- PaymentService (confidence: 0.6)

Please select primary project:
1. UserService
2. PaymentService
3. Both (multi-project)

Your choice [3]:
```

### Sync Conflicts

```
⚠️ Sync conflict detected

Local: spec-001 updated 2 hours ago
Azure DevOps: Work item updated 1 hour ago

Options:
1. Use local version
2. Use Azure DevOps version
3. Merge changes
4. View diff

Your choice [3]:
```

## Integration with CI/CD

### Auto-sync on Commit

```yaml
# .github/workflows/specweave-sync.yml
on:
  push:
    paths:
      - '.specweave/docs/internal/specs/**'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npx specweave ado-sync-all
        env:
          AZURE_DEVOPS_PAT: ${{ secrets.ADO_PAT }}
```

### Project-specific Pipelines

```yaml
# azure-pipelines.yml
trigger:
  paths:
    include:
      - .specweave/docs/internal/specs/$(System.TeamProject)/**

variables:
  - name: project
    value: $(System.TeamProject)

steps:
  - script: npx specweave ado-sync-project $(project)
```

## Summary

This skill enables sophisticated multi-project Azure DevOps organizations by:

1. ✅ **Intelligent project detection** from spec content
2. ✅ **Automatic folder organization** by project/area/team
3. ✅ **Task splitting** across multiple projects
4. ✅ **Cross-project linking** and dependency tracking
5. ✅ **Bidirectional sync** with Azure DevOps work items

**Result**: Seamless multi-project coordination with zero manual overhead!

---

**Skill Version**: 1.0.0
**Introduced**: SpecWeave v0.17.0
**Last Updated**: 2025-11-11