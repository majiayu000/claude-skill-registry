---
name: postgresql-plpgsql
description: Write PL/pgSQL - functions, procedures, triggers, error handling
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 06-postgresql-plpgsql
bond_type: PRIMARY_BOND
category: database
difficulty: advanced
estimated_time: 4h
---

# PostgreSQL PL/pgSQL Skill

> Atomic skill for procedural programming

## Overview

Production-ready patterns for functions, procedures, triggers, and exception handling.

## Prerequisites

- PostgreSQL 16+
- Understanding of SQL

## Parameters

```yaml
parameters:
  code_type:
    type: string
    required: true
    enum: [function, procedure, trigger, aggregate]
  volatility:
    type: string
    enum: [IMMUTABLE, STABLE, VOLATILE]
```

## Quick Reference

### Function Template
```sql
CREATE OR REPLACE FUNCTION func_name(p_param TYPE)
RETURNS return_type
LANGUAGE plpgsql STABLE SECURITY DEFINER
SET search_path = app, public
AS $$ DECLARE v_result TYPE; BEGIN
    -- Logic
    RETURN v_result;
EXCEPTION WHEN OTHERS THEN
    RAISE WARNING '%', SQLERRM;
    RETURN NULL;
END; $$;
```

### Trigger Template
```sql
CREATE OR REPLACE FUNCTION trigger_func() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN NEW.updated_at := NOW(); END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_name BEFORE UPDATE ON t FOR EACH ROW EXECUTE FUNCTION trigger_func();
```

### Volatility
| Category | Use Case |
|----------|----------|
| IMMUTABLE | Math, formatting |
| STABLE | Lookups (no writes) |
| VOLATILE | INSERT, random() |

## Exception Handling

```sql
EXCEPTION
    WHEN unique_violation THEN ...  -- 23505
    WHEN foreign_key_violation THEN ...  -- 23503
    WHEN OTHERS THEN RAISE EXCEPTION '% [%]', SQLERRM, SQLSTATE;
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `42883` | Function not found | Check signature |
| `42P13` | Invalid definition | Review syntax |
| Trigger not firing | Wrong timing | Check BEFORE/AFTER |

## Usage

```
Skill("postgresql-plpgsql")
```
