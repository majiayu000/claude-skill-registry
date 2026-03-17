---
name: database
description: Database design, SQL queries, migrations, and optimization. Activate for PostgreSQL, MySQL, SQLite, schema design, queries, indexes, and data modeling.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Database Skill

Provides comprehensive database capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Database schema design
- SQL query writing and optimization
- Database migrations
- Index optimization
- Data modeling

## PostgreSQL Quick Reference

### Connection
\`\`\`bash
# Connect
psql -h localhost -U postgres -d golden_armada

# Connection string
postgresql://user:password@host:5432/database

# Common psql commands
\l                  # List databases
\c database_name    # Connect to database
\dt                 # List tables
\d table_name       # Describe table
\di                 # List indexes
\q                  # Quit
\`\`\`

### Schema Design

\`\`\`sql
-- Create table with common patterns
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('claude', 'gpt', 'gemini')),
    status VARCHAR(20) DEFAULT 'idle',
    config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ  -- Soft delete
);

-- Create index
CREATE INDEX idx_agents_type ON agents(type);
CREATE INDEX idx_agents_status ON agents(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_agents_config ON agents USING GIN(config);

-- Add foreign key
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    result TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
\`\`\`

### Common Queries

\`\`\`sql
-- Basic CRUD
INSERT INTO agents (name, type) VALUES ('agent-1', 'claude') RETURNING *;
SELECT * FROM agents WHERE type = 'claude' AND deleted_at IS NULL;
UPDATE agents SET status = 'active' WHERE id = $1 RETURNING *;
DELETE FROM agents WHERE id = $1;

-- Joins
SELECT a.name, COUNT(t.id) as task_count
FROM agents a
LEFT JOIN tasks t ON a.id = t.agent_id
WHERE a.deleted_at IS NULL
GROUP BY a.id;

-- JSON operations
SELECT * FROM agents WHERE config->>'model' = 'claude-sonnet-4-20250514';
SELECT * FROM agents WHERE config @> '{"enabled": true}';
UPDATE agents SET config = config || '{"version": "2.0"}' WHERE id = $1;

-- Window functions
SELECT
    name,
    created_at,
    ROW_NUMBER() OVER (ORDER BY created_at) as row_num,
    LAG(created_at) OVER (ORDER BY created_at) as prev_created
FROM agents;

-- CTEs
WITH active_agents AS (
    SELECT * FROM agents WHERE status = 'active'
)
SELECT * FROM active_agents WHERE type = 'claude';
\`\`\`

### Migrations

\`\`\`sql
-- Migration: 001_create_agents.sql
BEGIN;

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_agents_type ON agents(type);

COMMIT;

-- Rollback: 001_create_agents.sql
BEGIN;
DROP TABLE IF EXISTS agents;
COMMIT;
\`\`\`

### Performance Optimization

\`\`\`sql
-- Analyze query plan
EXPLAIN ANALYZE SELECT * FROM agents WHERE type = 'claude';

-- Check index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read
FROM pg_stat_user_indexes;

-- Find slow queries
SELECT
    query,
    calls,
    mean_time,
    total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Vacuum and analyze
VACUUM ANALYZE agents;
\`\`\`

## SQLAlchemy ORM

\`\`\`python
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Agent(Base):
    __tablename__ = 'agents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(20), default='idle')
    config = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tasks = relationship("Task", back_populates="agent", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'), nullable=False)
    message = Column(String, nullable=False)
    result = Column(String)

    agent = relationship("Agent", back_populates="tasks")
\`\`\`

## Best Practices

1. **Use UUIDs** for primary keys in distributed systems
2. **Add indexes** for frequently queried columns
3. **Use soft deletes** (`deleted_at`) for important data
4. **JSONB for flexible data**, with GIN indexes
5. **Foreign key constraints** for data integrity
6. **Created/updated timestamps** for auditing
7. **Connection pooling** for performance
