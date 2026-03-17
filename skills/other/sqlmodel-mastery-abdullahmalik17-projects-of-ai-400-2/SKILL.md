---
name: sqlmodel-mastery
description: Comprehensive SQLModel skill for Python database operations with SQL databases. Use when working with SQLModel for (1) Designing database models and table schemas, (2) Creating relationships between tables (foreign keys, one-to-many, many-to-many), (3) Integrating SQLModel with FastAPI for CRUD APIs, (4) Writing queries with select, where, joins, and filtering, (5) Implementing best practices for session management, migrations, and performance optimization. Covers the multiple model pattern (Base, Table, Create, Public, Update), dependency injection, pagination, error handling, and production-ready patterns.
---

# SQLModel Mastery

## Overview

Assist users with SQLModel for database operations, model design, FastAPI integration, and production-ready patterns. SQLModel combines Pydantic and SQLAlchemy, enabling type-safe database models that work seamlessly with FastAPI.

## Quick Start

### When User Needs Help With...

**Model Design**: Load `references/model-patterns.md`
**Relationships**: Load `references/relationships.md`
**Queries**: Load `references/queries.md`
**FastAPI Integration**: Load `references/fastapi-integration.md`
**Best Practices/Production**: Load `references/best-practices.md`

### Common Templates

**Complete CRUD API**: Use `assets/templates/complete-crud-api.py`
**Model Examples**: Use `assets/templates/models-example.py`

---

## Workflow

### Step 1: Understand User's Context

**Identify the task type**:
- New project setup
- Model design questions
- Relationship configuration
- Query writing
- FastAPI integration
- Troubleshooting errors
- Best practices advice

**Gather context**:
- Database type (SQLite, PostgreSQL, MySQL)
- Existing codebase or greenfield
- FastAPI integration status
- Specific error messages or issues

### Step 2: Load Appropriate References

**Progressive disclosure**: Only load what's needed.

```
IF task == "model design" OR "schema design":
    READ references/model-patterns.md
    FOCUS: Multiple model pattern, field configuration, validation

IF task == "relationships" OR "foreign keys" OR "joins":
    READ references/relationships.md
    FOCUS: One-to-many, many-to-many, Relationship() configuration

IF task == "queries" OR "select" OR "filtering":
    READ references/queries.md
    FOCUS: WHERE clauses, joins, pagination, aggregations

IF task == "FastAPI" OR "CRUD" OR "endpoints" OR "dependency injection":
    READ references/fastapi-integration.md
    FOCUS: Dependency pattern, CRUD endpoints, error handling

IF task == "production" OR "performance" OR "migrations" OR "best practices":
    READ references/best-practices.md
    FOCUS: Session management, security, optimization

IF task == "complete example" OR "template":
    PROVIDE assets/templates/complete-crud-api.py OR models-example.py
```

### Step 3: Provide Targeted Guidance

**Be specific and actionable**:
- Reference exact code patterns from loaded references
- Explain the "why" behind recommendations
- Highlight common pitfalls
- Provide file:line references where appropriate

**For model design**:
1. Recommend multiple model pattern (Base, Table, Create, Public, Update)
2. Show field configuration with validation
3. Explain when to use Optional vs required fields

**For relationships**:
1. Identify relationship type (one-to-many, many-to-many)
2. Show foreign key and Relationship() setup
3. Explain back_populates and loading strategies

**For queries**:
1. Build query incrementally (select → where → join → pagination)
2. Show proper session usage
3. Recommend eager loading to avoid N+1 queries

**For FastAPI integration**:
1. Recommend dependency injection pattern
2. Show proper error handling
3. Emphasize using Public models in response_model

**For best practices**:
1. Always recommend session context managers
2. Emphasize pagination on list endpoints
3. Highlight security considerations

### Step 4: Provide Code Examples

**Use examples from references**:
- Copy relevant code snippets from loaded references
- Adapt to user's specific domain
- Include comments explaining key points

**Or provide templates**:
- For complete implementations, copy from `assets/templates/`
- Customize placeholder names to user's domain
- Highlight sections to modify

### Step 5: Address Follow-up Questions

**Common follow-ups**:
- "How do I handle errors?" → Load `fastapi-integration.md` error handling section
- "How do I optimize this query?" → Load `best-practices.md` performance section
- "How do I set up migrations?" → Load `best-practices.md` Alembic section

---

## Reference Files Guide

### references/model-patterns.md

**When to load**: Model design, schema design, validation questions

**Key topics**:
- Multiple model pattern (Base, Table, Create, Public, Update)
- Field configuration (indexes, constraints, defaults)
- Type hints and Pydantic validation
- Complete e-commerce example

**Example prompts**:
- "How do I design SQLModel models?"
- "What's the difference between Create and Update models?"
- "How do I add validation to fields?"

### references/relationships.md

**When to load**: Foreign keys, relationships, joins, related data

**Key topics**:
- Foreign key setup
- One-to-many relationships (Team has many Heroes)
- Many-to-many relationships (link tables)
- Relationship() configuration
- Loading strategies (lazy vs eager)
- Complete blog example with Posts and Comments

**Example prompts**:
- "How do I create a one-to-many relationship?"
- "How do I set up many-to-many with extra fields?"
- "What is back_populates?"

### references/queries.md

**When to load**: SELECT queries, filtering, pagination, aggregations

**Key topics**:
- Basic SELECT statements
- WHERE clauses (equality, comparison, LIKE, IN)
- Joins (implicit and explicit)
- Pagination (offset/limit)
- Ordering and sorting
- Aggregations (COUNT, AVG, GROUP BY)
- Complex query patterns

**Example prompts**:
- "How do I filter Heroes by age?"
- "How do I paginate results?"
- "How do I join two tables?"
- "How do I count records?"

### references/fastapi-integration.md

**When to load**: FastAPI integration, CRUD endpoints, dependency injection

**Key topics**:
- Database setup and configuration
- Dependency injection pattern
- CRUD endpoints (Create, Read, Update, Delete)
- Error handling (404, IntegrityError)
- Request validation
- Response models
- Advanced patterns (bulk operations, transactions)

**Example prompts**:
- "How do I integrate SQLModel with FastAPI?"
- "How do I create CRUD endpoints?"
- "What's the dependency injection pattern?"
- "How do I handle database errors in FastAPI?"

### references/best-practices.md

**When to load**: Production readiness, optimization, security, migrations

**Key topics**:
- Model design best practices (DOs and DON'Ts)
- Session management patterns
- Performance optimization (indexes, eager loading, pagination)
- Security (hiding sensitive fields, password hashing)
- Database migrations with Alembic
- Testing strategies
- Common pitfalls and solutions
- Production checklist

**Example prompts**:
- "What are SQLModel best practices?"
- "How do I optimize performance?"
- "How do I handle database migrations?"
- "How do I test SQLModel code?"

---

## Asset Templates

### assets/templates/complete-crud-api.py

**Complete production-ready FastAPI + SQLModel CRUD API**

**Includes**:
- Database configuration
- Multiple model pattern for Team and Hero
- All CRUD endpoints with proper error handling
- Pagination and filtering
- Dependency injection
- Input validation
- OpenAPI documentation

**When to provide**:
- User needs a complete working example
- Starting a new FastAPI + SQLModel project
- Understanding full CRUD implementation

**How to use**:
1. Copy entire template
2. Customize model names and fields
3. Update database URL
4. Run with `uvicorn main:app --reload`

### assets/templates/models-example.py

**Comprehensive model design examples**

**Includes**:
- Multiple model pattern for Users, Products, Orders
- Relationships (one-to-many, many-to-many)
- Field validation and constraints
- Enums and complex types
- Timestamp and soft delete mixins
- Complete e-commerce schema

**When to provide**:
- User needs model design inspiration
- Learning relationship patterns
- Understanding complex model hierarchies

---

## Common Scenarios

### Scenario 1: New FastAPI + SQLModel Project

**User**: "I want to build a FastAPI app with SQLModel"

**Response**:
1. Provide `assets/templates/complete-crud-api.py`
2. Explain the multiple model pattern
3. Show how to run and test
4. Recommend next steps (add more models, migrations)

### Scenario 2: Designing Models

**User**: "How do I create User and Post models with relationship?"

**Response**:
1. Load `references/model-patterns.md`
2. Load `references/relationships.md`
3. Show multiple model pattern for both entities
4. Demonstrate one-to-many relationship setup
5. Provide code example adapted to their domain

### Scenario 3: Query Optimization

**User**: "My queries are slow"

**Response**:
1. Load `references/queries.md` (join/eager loading sections)
2. Load `references/best-practices.md` (performance section)
3. Diagnose N+1 query problem
4. Show selectinload() solution
5. Recommend adding indexes

### Scenario 4: Error Handling

**User**: "How do I handle 'Hero not found' errors?"

**Response**:
1. Load `references/fastapi-integration.md` (error handling section)
2. Show HTTPException pattern
3. Demonstrate helper function approach
4. Provide complete endpoint example

### Scenario 5: Many-to-Many Relationship

**User**: "How do I create a many-to-many relationship?"

**Response**:
1. Load `references/relationships.md` (many-to-many section)
2. Explain link table concept
3. Show basic many-to-many example
4. If extra fields needed, show link table with additional columns
5. Demonstrate usage in FastAPI endpoint

---

## Key Principles

### Always Recommend

1. **Multiple Model Pattern**: Base, Table, Create, Public, Update
2. **Dependency Injection**: Use `Depends(get_session)` in FastAPI
3. **Pagination**: Always limit list endpoints
4. **Security**: Never expose table models or sensitive fields in responses
5. **Error Handling**: Validate and handle database errors
6. **Type Hints**: Use proper type hints for IDE support
7. **Indexes**: Add to frequently queried fields

### Common Mistakes to Avoid

1. ❌ Exposing Table models in `response_model`
2. ❌ Forgetting `exclude_unset=True` in updates
3. ❌ Not using pagination on list endpoints
4. ❌ Accessing relationships outside session (DetachedInstanceError)
5. ❌ Not handling IntegrityError on unique constraints
6. ❌ Forgetting to commit and refresh after adding records

### Industry Standards

- Use PostgreSQL for production (not SQLite)
- Implement Alembic for database migrations
- Use connection pooling
- Add indexes to foreign keys
- Hash passwords before storing
- Validate all user input
- Use proper HTTP status codes (201, 404, etc.)

---

## Troubleshooting Guide

### DetachedInstanceError

**Problem**: Accessing relationship outside session

**Solution**: Use eager loading with `selectinload()` or access within session

**Reference**: `best-practices.md` → Common Pitfalls

### IntegrityError

**Problem**: Unique constraint or foreign key violation

**Solution**: Wrap in try/except and handle gracefully

**Reference**: `fastapi-integration.md` → Error Handling

### N+1 Query Problem

**Problem**: Separate query for each relationship access

**Solution**: Use `selectinload()` or `lazy="selectin"`

**Reference**: `best-practices.md` → Performance Optimization

### Missing ID after commit

**Problem**: ID is None after session.add() and session.commit()

**Solution**: Call `session.refresh(obj)` after commit

**Reference**: `best-practices.md` → Session Management

---

## Quick Reference Commands

```python
# Create model instance and save
hero = Hero(name="Spider-Boy")
session.add(hero)
session.commit()
session.refresh(hero)  # Load generated fields

# Query
statement = select(Hero).where(Hero.age > 30)
heroes = session.exec(statement).all()

# Update
hero_data = hero_update.model_dump(exclude_unset=True)
db_hero.sqlmodel_update(hero_data)
session.add(db_hero)
session.commit()

# Delete
session.delete(hero)
session.commit()

# FastAPI dependency
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
```
