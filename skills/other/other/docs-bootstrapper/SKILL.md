---
name: docs-bootstrapper
description: Bootstraps documentation structure for projects. Creates initial README, architecture docs, and API documentation with project-aware templates.
allowed-tools: Read, Grep, Glob, Write, Edit
user-invocable: true
---

# Documentation Bootstrapper Skill

## Purpose

This skill creates initial documentation structure for projects that lack proper documentation. It detects project type and generates appropriate documentation templates, including README, architecture overview, and API documentation.

## When to Activate

Use this skill when:
- Starting a new project without documentation
- Existing project lacks basic documentation structure
- docs-analyzer identifies missing documentation structure
- User explicitly requests documentation bootstrapping
- Migrating from undocumented codebase

## Core Workflow

### Step 1: Check Existing Documentation

Before bootstrapping, verify what documentation already exists:

**Check for**:
- README.md (root)
- docs/ directory
- CONTRIBUTING.md
- Architecture documentation
- API documentation

**Decision**:
- If comprehensive docs exist: Skip bootstrapping, report status
- If partial docs exist: Ask user if they want to supplement
- If no docs exist: Proceed with full bootstrap

### Step 2: Detect Project Type

Analyze the codebase to determine project type and technology stack.

#### Backend Projects

**Django**:
- Indicators: `manage.py`, `settings.py`, `requirements.txt` with Django
- Framework: Django + DRF
- Components: ViewSets, Models, Serializers, Migrations

**FastAPI**:
- Indicators: `main.py`, `requirements.txt` with fastapi
- Framework: FastAPI + Pydantic
- Components: Route handlers, Schemas, Dependencies

**Express**:
- Indicators: `package.json` with express, `app.js` or `server.js`
- Framework: Express.js
- Components: Routes, Controllers, Middleware

**NestJS**:
- Indicators: `nest-cli.json`, `package.json` with @nestjs
- Framework: NestJS
- Components: Controllers, Services, Modules

**Flask**:
- Indicators: `app.py`, `requirements.txt` with flask
- Framework: Flask
- Components: Routes, Blueprints

**Spring Boot**:
- Indicators: `pom.xml` or `build.gradle`, `Application.java`
- Framework: Spring Boot
- Components: Controllers, Services, Repositories

#### Frontend Projects

**React**:
- Indicators: `package.json` with react, `.jsx` or `.tsx` files
- Framework: React
- Components: Functional components, Hooks, Context

**Vue**:
- Indicators: `package.json` with vue, `vue.config.js`, `.vue` files
- Framework: Vue 3
- Components: Single File Components, Composition API

**Angular**:
- Indicators: `angular.json`, `package.json` with @angular
- Framework: Angular
- Components: Components, Services, Modules

**Next.js**:
- Indicators: `next.config.js`, `pages/` directory
- Framework: Next.js (React)
- Components: Pages, API routes, Components

**Svelte**:
- Indicators: `svelte.config.js`, `.svelte` files
- Framework: Svelte
- Components: Svelte components

#### Full-Stack Projects

**Indicators**:
- Both frontend and backend markers present
- Monorepo structure (`apps/`, `packages/`, `workspaces`)
- Multiple package.json files

#### Infrastructure Projects

**Terraform**:
- Indicators: `.tf` files
- Type: Infrastructure as Code
- Resources: Providers, Modules, Resources

**Kubernetes**:
- Indicators: `.yaml` files with `kind:`, `apiVersion:`
- Type: Container orchestration
- Resources: Pods, Services, Deployments

**Docker**:
- Indicators: `Dockerfile`, `docker-compose.yml`
- Type: Containerization
- Resources: Services, Images, Networks

**Ansible**:
- Indicators: `playbook.yml`, `ansible.cfg`
- Type: Configuration management
- Resources: Playbooks, Roles, Tasks

#### Library/Package Projects

**Python Package**:
- Indicators: `setup.py`, `pyproject.toml` without web framework
- Type: Library
- Structure: Package with __init__.py

**JavaScript/TypeScript Library**:
- Indicators: `package.json` with `"main"` field, no web framework
- Type: Library
- Structure: Exported modules

**Rust Crate**:
- Indicators: `Cargo.toml`, `src/lib.rs`
- Type: Library
- Structure: Cargo package

**Go Package**:
- Indicators: `go.mod`, package structure
- Type: Library
- Structure: Go module

**Detection Method**:
```bash
# Use Glob to find indicator files
Glob: "manage.py"  # Django
Glob: "main.py"    # FastAPI
Glob: "package.json"  # Node.js

# Use Read to check file contents
Read: "package.json"  # Check dependencies

# Use Grep to find specific patterns
Grep: pattern="from django" glob="*.py"  # Django imports
Grep: pattern="from fastapi" glob="*.py"  # FastAPI imports
```

### Step 3: Generate README.md

Create comprehensive README based on project type using template.

**README Sections** (adapt based on project type):

1. **Project Header**
   - Project name (from directory or package.json/setup.py)
   - Brief description (placeholder for user to fill)
   - Badges (build status, coverage - placeholders)

2. **Overview**
   - What the project does
   - Key features (placeholder with examples)
   - Technology stack (detected technologies)

3. **Installation**
   - Prerequisites (based on project type)
   - Installation steps (framework-specific)
   - Environment setup

4. **Usage**
   - Quick start example
   - Common commands (framework-specific)
   - Configuration options

5. **Project Structure**
   - Directory tree (generated from actual structure)
   - Key directories explanation

6. **Development**
   - Setup development environment
   - Running tests (framework-specific commands)
   - Code style guidelines

7. **API Documentation** (for backend projects)
   - Link to detailed API docs
   - Example endpoints

8. **Deployment** (if applicable)
   - Deployment prerequisites
   - Deployment steps
   - Environment variables

9. **Contributing**
   - Link to CONTRIBUTING.md
   - Basic contribution workflow

10. **License**
    - License type (detect from LICENSE file or placeholder)

**Use template**: `templates/README.template.md` with placeholders replaced

### Step 4: Create docs/ Directory Structure

Generate standard documentation directory:

```
docs/
├── architecture.md
├── api.md (for backend/full-stack)
└── .gitkeep (if empty)
```

### Step 5: Generate architecture.md

Create architecture documentation using template.

**Architecture Sections** (adapt based on project type):

1. **System Overview**
   - High-level description
   - Main components
   - Technology choices

2. **Architecture Diagram** (Mermaid placeholder)
   - Component diagram
   - Data flow diagram
   - Deployment diagram (for infrastructure)

3. **Components**
   - Component 1: Description
   - Component 2: Description
   - (Based on detected project structure)

4. **Data Flow**
   - Request/response flow (backend)
   - State management flow (frontend)
   - Resource provisioning (infrastructure)

5. **Technology Stack**
   - Languages
   - Frameworks
   - Libraries
   - Infrastructure

6. **Design Decisions**
   - Key architectural choices (placeholders)
   - Trade-offs considered

**Use template**: `templates/architecture.template.md`

### Step 6: Generate api.md (Backend/Full-Stack Only)

Create API documentation template.

**API Documentation Sections**:

1. **Overview**
   - API base URL (placeholder)
   - Authentication method (detect or placeholder)
   - Response format (JSON, XML, etc.)

2. **Authentication**
   - Auth type (JWT, OAuth, API Key)
   - How to authenticate
   - Example auth request

3. **Endpoints**
   - Table of endpoints (detect from code or placeholders)
   - Method | Endpoint | Description
   - Request/response examples

4. **Error Handling**
   - Error response format
   - Common error codes

5. **Rate Limiting** (if applicable)
   - Rate limit rules
   - Headers

**Use template**: `templates/api.template.md`

### Step 7: Create Directory Structure Visual

Generate directory tree for README using Bash:

```bash
# Generate tree (if tree command available)
tree -L 3 -I 'node_modules|__pycache__|*.pyc|.git'

# Or use find
find . -type d -maxdepth 3 | grep -v node_modules | grep -v __pycache__
```

Insert into README.md

### Step 8: Populate Placeholders

Replace template placeholders with detected values:

**Replacements**:
- `{{PROJECT_NAME}}`: From directory name, package.json, setup.py
- `{{DESCRIPTION}}`: Placeholder or from package.json
- `{{FRAMEWORK}}`: Detected framework (Django, React, etc.)
- `{{LANGUAGE}}`: Detected language (Python, JavaScript, etc.)
- `{{INSTALL_COMMAND}}`: Framework-specific (`pip install`, `npm install`)
- `{{RUN_COMMAND}}`: Framework-specific (`python manage.py runserver`, `npm start`)
- `{{TEST_COMMAND}}`: Framework-specific (`pytest`, `npm test`)

### Step 9: Report Creation

After creating files, report to user:

```markdown
# Documentation Bootstrap Complete ✅

## Created Files
- README.md (X lines)
- docs/architecture.md (Y lines)
- docs/api.md (Z lines) [if applicable]

## Project Type Detected
- Type: [Django Backend / React Frontend / etc.]
- Framework: [framework name]
- Language: [language]

## Next Steps
1. Review generated documentation
2. Fill in placeholders marked with [PLACEHOLDER] or {{VARIABLE}}
3. Add project-specific details
4. Update Mermaid diagrams with actual architecture
5. Add real API endpoint examples

## Customization Needed
- [ ] Add project description in README.md
- [ ] Fill technology stack details
- [ ] Add real API endpoints in docs/api.md
- [ ] Update architecture diagram
- [ ] Add deployment instructions
- [ ] Update environment variables
```

## Templates

Templates are located in `skills/docs-bootstrapper/templates/`:

1. **README.template.md**: Main README template
2. **architecture.template.md**: Architecture doc template
3. **api.template.md**: API documentation template

Templates use placeholders:
- `{{VARIABLE}}`: Auto-replaced with detected values
- `[PLACEHOLDER]`: User must fill in
- `[OPTIONAL]`: Optional section, can be removed

## Integration with Other Skills

- **docs-manager**: Invokes bootstrapper when no docs exist
- **docs-analyzer**: Identifies when bootstrapping is needed
- **mermaid-expert**: Called after bootstrapping to fill diagram placeholders

## Example Usage

**Scenario 1: New Django Project**

```bash
User: /docs-bootstrapper

docs-bootstrapper:
Checking existing documentation...
No comprehensive docs found.

Detecting project type...
✓ Detected: Django Backend
✓ Framework: Django 4.2 + DRF
✓ Database: PostgreSQL (from settings)

Creating documentation...
✓ README.md created (180 lines)
✓ docs/architecture.md created (120 lines)
✓ docs/api.md created (90 lines)

Bootstrap complete! Review and customize generated docs.
```

**Scenario 2: React Project**

```bash
User: Bootstrap documentation for this React app

docs-bootstrapper:
Detecting project type...
✓ Detected: React Frontend
✓ Framework: React 18 + TypeScript
✓ State: Redux Toolkit

Creating documentation...
✓ README.md created (160 lines)
✓ docs/architecture.md created (100 lines)

Bootstrap complete! Frontend project detected, no API docs generated.
```

## Guidelines

### Do:
- ✅ Detect project type accurately
- ✅ Use appropriate templates for project type
- ✅ Generate realistic directory structures
- ✅ Provide clear placeholders for user input
- ✅ Report what was created
- ✅ Give next steps guidance

### Don't:
- ❌ Overwrite existing comprehensive documentation
- ❌ Make assumptions about business logic
- ❌ Generate fake/incorrect API endpoints
- ❌ Include overly generic content
- ❌ Skip project type detection
- ❌ Create docs without user awareness

## Standalone Usage

Can be invoked directly when starting new projects:

```
User: /docs-bootstrapper

Skill: Detects project, creates comprehensive documentation structure
```

Or called by docs-manager when gap analysis shows no docs exist.
