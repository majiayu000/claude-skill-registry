---
name: buslog
description: Skill from PoulpYBifle/BusLog
---

# BusLog Skill - Business Logic Documentation

**Purpose**: Use BusLog to analyze and document business logic workflows in the current codebase.

---

## When to Use This Skill

Invoke this skill when:
- User asks to document business logic or workflows
- User wants to understand how a feature works across files
- User needs to map dependencies (APIs, services, libraries)
- User requests architecture documentation
- User asks "how does [feature] work?"

Do NOT use for:
- Simple code explanations (use direct response)
- Single file analysis (use Read tool)
- General questions about the codebase

---

## Skill Execution Steps

### Phase 1: Initialize BusLog

1. Check if BusLog is initialized:
   ```bash
   python -m buslog.cli list
   ```

2. If not initialized, run:
   ```bash
   python -m buslog.cli init --name "{project_name}"
   ```

3. Generate analysis prompt:
   ```bash
   python -m buslog.cli analyze
   ```

### Phase 2: Analyze Codebase

4. Read the generated analysis prompt from `.business-logic/` or command output

5. Identify business workflows by:
   - Scanning API endpoints (routes, controllers)
   - Finding event handlers and listeners
   - Locating scheduled jobs or background tasks
   - Tracking database operations and transactions

6. For each workflow identified, gather:
   - **Entry points**: Endpoints, events, CLI commands
   - **Files involved**: Controllers, services, models (with line numbers)
   - **External dependencies**: APIs called, third-party services
   - **Internal dependencies**: Services, repositories, utilities used
   - **Libraries**: npm/pip packages and their purpose
   - **Flow**: Step-by-step execution path

### Phase 3: Document Workflows

7. For each workflow, create documentation using:
   ```bash
   python -m buslog.cli add workflow-name
   ```

8. Edit the workflow file at `.business-logic/workflows/workflow-name.md` with:

   ```markdown
   # Workflow: [Name]

   ## Description
   [Business purpose - what problem does this solve?]

   ## Déclencheurs
   - **Endpoint**: `POST /api/path`
   - **Event**: `event.name`
   - **CLI**: `command-name`

   ## Composants Utilisés

   ### Fichiers
   - `path/to/file.ts:10-45` - [Role in workflow]

   ### APIs Externes
   - **Service Name** (`api.example.com/endpoint`) - [Purpose]

   ### Services Internes
   - `ServiceName` - [What it does]

   ### Librairies Tierces
   - `package-name` (v1.0.0) - [How it's used]

   ## Flux d'Exécution

   ```mermaid
   graph TD
       A[Start] --> B{Decision}
       B -->|Success| C[Action]
       B -->|Error| D[Handle Error]
       C --> E[End]
       D --> E
   ```

   ## Dépendances Métier
   - Déclenche: `other-workflow`
   - Requis par: `other-workflow`

   ## Notes & Annotations
   - Important business rules
   - Edge cases to watch
   - Performance considerations
   ```

### Phase 4: Present Results

9. Inform the user:
   ```
   I've documented [N] business workflows in BusLog:

   1. [Workflow Name] - [Brief description]
   2. [Workflow Name] - [Brief description]

   View the documentation:
   - Run: python -m buslog.cli serve
   - Open: http://localhost:8080

   All workflows are saved in .business-logic/workflows/
   ```

10. Optionally, suggest next steps:
    - "Would you like me to add diagrams for specific workflows?"
    - "Should I analyze dependencies between workflows?"
    - "Do you want me to add more details to any workflow?"

---

## Output Format

Always provide:
1. **Summary**: List of workflows identified
2. **Location**: Where documentation was saved
3. **Next steps**: How to view and use the documentation

Example:
```
✅ BusLog Analysis Complete

Documented 5 workflows:
1. User Registration - POST /api/auth/register
2. Payment Processing - Stripe webhook handling
3. Email Notifications - Background job queue
4. Data Export - GET /api/export/csv
5. Admin Dashboard - Aggregated metrics

📁 Documentation: .business-logic/workflows/
🌐 View UI: python -m buslog.cli serve

Next: Would you like me to add more details to any workflow?
```

---

## Best Practices

1. **Be thorough**: Include ALL files involved, even small utilities
2. **Trace dependencies**: Follow the execution path completely
3. **Use Mermaid diagrams**: Visual flow helps understanding
4. **Note business rules**: Document WHY, not just WHAT
5. **Include line numbers**: Make it easy to find code
6. **Keep updated**: Update workflows when code changes

---

## Common Patterns to Look For

### API Endpoints
- Express: `app.get()`, `router.post()`
- FastAPI: `@app.get`, `@router.post`
- Django: `path()`, `url()`
- NestJS: `@Get()`, `@Post()`

### Event Handlers
- Node: `.on()`, `addEventListener()`
- Python: `@event.listens_for`
- Custom: `@subscribe`, `@handler`

### Background Jobs
- Bull/BullMQ: `queue.add()`
- Celery: `@task`, `@periodic_task`
- Cron: `@schedule`, `cron.schedule()`

### Database Operations
- ORMs: Sequelize, TypeORM, SQLAlchemy, Prisma
- Transactions: `BEGIN`, `COMMIT`, `ROLLBACK`
- Migrations: Version control for schema

---

## Error Handling

If BusLog is not installed:
```bash
pip install -e /path/to/AIDD-logic-metier-workflow
```

If commands fail:
- Use `python -m buslog.cli` instead of `buslog`
- Check that you're in the correct project directory
- Verify BusLog is initialized with `python -m buslog.cli list`

---

## Skill Metadata

- **Version**: 1.0
- **Author**: PoulpYBifle
- **Compatible with**: Any codebase (language-agnostic)
- **Requirements**: Python 3.10+, BusLog installed
