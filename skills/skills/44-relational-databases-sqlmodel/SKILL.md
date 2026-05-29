---
sidebar_position: 0
title: "Build Your Database Skill"
description: "Create a relational-db-agent skill that knows SQLModel async patterns"
keywords: [sqlmodel, skill-first, async, database, skill creation]
chapter: 44
lesson: 0
duration_minutes: 25

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Create"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student creates a functional skill that generates valid SQLModel async code"

  - name: "Documentation Research"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student uses fetching-library-docs to gather official SQLModel patterns"

  - name: "Skill Specification"
    proficiency_level: "A2"
    category: "Applied"
    bloom_level: "Understand"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student writes LEARNING-SPEC.md defining what database skill should know"

learning_objectives:
  - objective: "Create a relational-db-agent skill for async database patterns"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "Skill generates valid SQLModel class with async session code"

  - objective: "Fetch official SQLModel documentation using AI tools"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Successfully retrieves async session patterns from official docs"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (skill-first philosophy, LEARNING-SPEC, docs fetching, skill creation) within B1 limit"

differentiation:
  extension_for_advanced: "Create skill references for specific patterns like JSONB columns or self-referential relationships"
  remedial_for_struggling: "Start with minimal skill that only generates basic SQLModel class, expand later"
---

# Build Your Database Skill

You're about to learn async database patterns with SQLModel. But you won't start with "what is SQLModel?"

You'll start by **building a skill that knows SQLModel**.

This is the skill-first approach: instead of accumulating knowledge that fades, you create an asset that grows. By chapter end, your `relational-db-agent` skill will generate production-quality database code—and you'll own it.

## Why Skill-First for Databases?

Database patterns are precise. Off-by-one errors in async patterns cause `MissingGreenlet` crashes. Forgotten `await` keywords block your entire agent. Wrong relationship configurations cascade into N+1 query disasters.

A skill that knows the correct patterns eliminates these errors. You consult your skill, it generates correct code, you ship faster.

## Step 1: Clone the Skills Lab

Start fresh. Every chapter begins with a clean skills-lab:

```bash
cd ~/projects
git clone https://github.com/panaversity/claude-code-skills-lab.git ch44-skills-lab
cd ch44-skills-lab
```

**Output:**
```
Cloning into 'ch44-skills-lab'...
remote: Enumerating objects: 45, done.
remote: Counting objects: 100% (45/45), done.
Receiving objects: 100% (45/45), done.
```

## Step 2: Write Your Learning Specification

Before building the skill, define what it should know. Create `LEARNING-SPEC.md`:

```markdown
# Learning Specification: Relational Database Skill

## What This Skill Should Know

### Core Patterns
- Async engine creation with `create_async_engine`
- Connection pooling for production (`pool_pre_ping`, `pool_size`)
- AsyncSession from `sqlmodel.ext.asyncio.session`
- Session lifecycle as FastAPI dependency

### Model Patterns
- SQLModel with `table=True`
- JSONB columns for PostgreSQL
- Foreign keys and relationships
- Self-referential relationships (parent/child)

### Operations
- Async CRUD (add, flush, commit, refresh)
- Eager loading with `selectinload`
- Transaction patterns (rollback on error)

### Migrations
- Alembic async template
- Model import requirements
- Autogenerate and upgrade commands

## Success Criteria
The skill generates code that:
1. Compiles without syntax errors
2. Uses correct async/await patterns
3. Includes proper imports
4. Follows SQLModel conventions
```

**Output:**
```
Created LEARNING-SPEC.md (32 lines)
```

## Step 3: Fetch Official Documentation

Use the `/fetching-library-docs` command to get accurate patterns:

```
/fetching-library-docs sqlmodel --topic "async session"
```

The skill retrieves official SQLModel patterns—imports, code examples, and usage notes.

**What you'll receive:**
- `create_async_engine` syntax
- `AsyncSession` import path
- Session lifecycle patterns
- Code examples from official docs

Save the key patterns for your skill. Don't memorize—capture.

## Step 4: Create Your Skill

Use `/skill-creator` to build the `relational-db-agent` skill:

```
/skill-creator relational-db-agent

The skill should:
- Generate async SQLModel code for FastAPI backends
- Know proper async engine and session patterns
- Include PostgreSQL-specific features like JSONB
- Prevent common async pitfalls (MissingGreenlet, N+1 queries)
- Reference SQLModel and SQLAlchemy 2.0 async patterns

Use the patterns from LEARNING-SPEC.md and the fetched documentation.
```

The skill creator generates:
- `SKILL.md` with triggering description and instructions
- `references/` directory for detailed patterns
- `scripts/verify.py` for validation

**Output:**
```
✓ Created .claude/skills/relational-db-agent/SKILL.md
✓ Created .claude/skills/relational-db-agent/references/async-patterns.md
✓ Created .claude/skills/relational-db-agent/scripts/verify.py
```

## Step 5: Test Your Skill

Verify your skill generates valid code:

```
Using my relational-db-agent skill, create a Task model with:
- id as primary key
- title as string
- status as string with default "pending"
- created_at timestamp
```

**Expected output:**

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

If the output includes correct imports, `table=True`, and proper Field usage—your skill works.

## What Happens Next

| Lesson | You Learn | Your Skill Improves |
|--------|-----------|---------------------|
| L01 | Why agents need structured data | Understands relational vs vector DB |
| L02 | Async engine setup | Generates correct engine config |
| L03 | Model design | Handles JSONB and constraints |
| L04 | Session management | Knows AsyncSession lifecycle |
| L05 | CRUD operations | Generates proper async CRUD |
| L06 | Relationships | Includes selectinload patterns |
| L07 | Transactions | Handles rollback correctly |
| L08 | Migrations | Knows Alembic async setup |
| L09 | Complete layer | Generates full database layer |

Each lesson ends with a "Reflect on Your Skill" section where you test what you learned against your skill and improve it.

## Try With AI

### Prompt 1: Verify Your Skill Structure

```
Check my relational-db-agent skill at .claude/skills/relational-db-agent/
Does it have:
1. SKILL.md with proper YAML frontmatter
2. A description starting with "Use when"
3. References for async patterns
Suggest any improvements to the structure.
```

**What you're learning:** Skill validation—ensuring your skill follows the format that makes it discoverable and usable.

### Prompt 2: Test AsyncSession Generation

```
Using my relational-db-agent skill, generate a get_session()
FastAPI dependency that yields an AsyncSession from an async engine.
Include all necessary imports.
```

**What you're learning:** Session management patterns—the foundation of async database operations.

### Prompt 3: Identify Gaps

```
I'm about to learn SQLModel async patterns. Based on my
relational-db-agent skill, what database concepts should
I add to make it more complete? Consider:
- What async pitfalls is it missing?
- What PostgreSQL features should it know?
- What relationship patterns should it include?
```

**What you're learning:** Gap analysis—proactively identifying what your skill needs to become production-ready.

### Safety Note

Your skill will generate database code. Always review generated code before running it—especially CREATE, DROP, or migration operations. Test in development before production.

---

## Reflect on Your Skill

You created a `relational-db-agent` skill. Test it now.

### Test Your Skill

```
Using my relational-db-agent skill, generate a complete
async database setup for a FastAPI app with:
- PostgreSQL connection
- Engine with connection pooling
- get_session dependency
```

### Identify Gaps

Ask yourself:
- Did my skill include `pool_pre_ping=True`?
- Did it use `sqlmodel.ext.asyncio.session.AsyncSession`?
- Did it structure the dependency correctly with `yield`?

### Improve Your Skill

If you found gaps:

```
My relational-db-agent skill is missing connection pool configuration.
Update it to always include pool_pre_ping=True and configurable
pool_size for production deployments.
```

Your skill just got better. This pattern repeats every lesson.
