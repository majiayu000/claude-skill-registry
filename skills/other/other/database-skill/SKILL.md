---
name: database-skill
description: Design and manage relational databases including table creation, migrations, and schema design. Use for database modeling and maintenance.
---

# Database Skill – Schema Design & Migrations

## Instructions

1. **Table Creation**
   - Define clear and consistent table structures
   - Use appropriate data types and constraints
   - Apply primary keys and foreign keys correctly

2. **Schema Design**
   - Normalize data where appropriate
   - Model relationships explicitly
   - Design for scalability and maintainability

3. **Migrations**
   - Create forward and backward migrations
   - Ensure migrations are idempotent and safe
   - Avoid destructive changes without backups

4. **Indexes & Constraints**
   - Add indexes for frequently queried columns
   - Enforce uniqueness and referential integrity
   - Use constraints to protect data correctness

## Best Practices
- Use consistent naming conventions
- Keep schemas simple and well-documented
- Version control all migrations
- Test migrations in non-production environments
- Follow relational database design principles

## Example Structure
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
