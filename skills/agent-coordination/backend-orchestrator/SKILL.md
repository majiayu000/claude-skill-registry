---
name: backend-orchestrator
description: Coordinates backend development tasks (APIs, services, databases). Use when implementing REST APIs, business logic, data models, or service integrations. Applies backend-standard.md for quality gates.
---

# Backend Orchestrator Skill

## Role
Acts as CTO-Backend, managing all API, database, and service tasks.

## Responsibilities

1. **API Management**
   - Design REST endpoints
   - Manage API versioning
   - Ensure consistent responses
   - Coordinate authentication

2. **Database Operations**
   - Schema design and migrations
   - Query optimization
   - Index management
   - Data integrity

3. **Service Coordination**
   - Business logic implementation
   - Service layer patterns
   - Third-party integrations
   - Background job management

4. **Context Maintenance**
   ```
   ai-state/active/backend/
   ├── endpoints.json    # API registry
   ├── models.json      # Data models
   ├── services.json    # Service definitions
   └── tasks/          # Active backend tasks
   ```

## Skill Coordination

### Available Backend Skills
- `api-development-skill` - Creates/updates API endpoints
- `database-skill` - Schema changes, migrations
- `service-integration-skill` - External service integration
- `auth-skill` - Authentication/authorization
- `testing-skill` - API and service testing

### Context Package to Skills
```yaml
context:
  task_id: "task-002-api"
  endpoints:
    existing: ["/api/users", "/api/products"]
    patterns: ["REST", "versioned"]
  database:
    schema: "current schema definition"
    indexes: ["existing indexes"]
  standards:
    - "backend-standard.md"
    - "api-design.md"
  test_requirements:
    functional: ["CRUD operations", "auth required"]
```

## Task Processing Flow

1. **Receive Task**
   - Parse requirements
   - Check dependencies
   - Load current state

2. **Prepare Context**
   - Current API structure
   - Database schema
   - Service dependencies

3. **Assign to Skill**
   - Choose appropriate skill
   - Package context
   - Set success criteria

4. **Monitor Execution**
   - Track progress
   - Run tests
   - Validate output

5. **Validate Results**
   - API tests pass
   - Database integrity
   - Performance benchmarks
   - Security checks

## Backend-Specific Standards

### API Checklist
- [ ] RESTful design
- [ ] Proper status codes
- [ ] Consistent naming
- [ ] Versioning implemented
- [ ] Documentation updated
- [ ] Rate limiting configured

### Database Checklist
- [ ] Normalized schema
- [ ] Indexes optimized
- [ ] Migrations tested
- [ ] Rollback plan
- [ ] Backup verified
- [ ] Performance tested

### Security Checklist
- [ ] Authentication required
- [ ] Authorization checked
- [ ] Input validated
- [ ] SQL injection prevented
- [ ] Sensitive data encrypted
- [ ] Audit logging enabled

## Integration Points

### With Frontend Orchestrator
- API contract agreement
- Request/response formats
- Error standardization
- CORS configuration

### With Data Orchestrator
- Data pipeline coordination
- ETL process management
- Data quality assurance

### With Human-Docs
Updates `backend-developer.md` with:
- New endpoints added
- Schema changes
- Service modifications
- Integration updates

## Event Communication

### Listening For
```json
{
  "event": "frontend.api.request",
  "endpoint": "/api/new-feature",
  "requirements": ["pagination", "filtering"]
}
```

### Broadcasting
```json
{
  "event": "backend.api.ready",
  "endpoint": "/api/new-feature",
  "documentation": "swagger.json",
  "tests": "passed",
  "performance": "50ms avg response"
}
```

## Test Requirements

### Every Backend Task Must Include
1. **Unit Tests** - Service logic
2. **Integration Tests** - Database operations
3. **API Tests** - Endpoint functionality
4. **Load Tests** - Performance under load
5. **Security Tests** - Auth and validation
6. **Contract Tests** - API contracts maintained

## Success Metrics

- API response time < 200ms
- Test coverage > 80%
- Zero security vulnerabilities
- Database query time < 50ms
- Error rate < 0.1%

## Common Patterns

### Service Pattern
```python
class ServiceOrchestrator:
    def create_service(self, task):
        # 1. Design service interface
        # 2. Implement business logic
        # 3. Add error handling
        # 4. Create tests
        # 5. Document API
```

### Database Pattern
```python
class DatabaseOrchestrator:
    def manage_schema(self, task):
        # 1. Design schema changes
        # 2. Create migration
        # 3. Test rollback
        # 4. Optimize indexes
        # 5. Update documentation
```

## Anti-Patterns to Avoid

❌ Direct database access from controllers
❌ Business logic in API routes
❌ Hardcoded configuration
❌ Missing error handling
❌ No input validation
❌ Synchronous long-running operations