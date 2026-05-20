---
name: supabase
description: Database, auth, and backend expertise for Supabase operations in [PROJECT_NAME]
last_updated: 2025-12-21
---

# Supabase Skill

## Overview

Provides comprehensive expertise for Supabase development in [PROJECT_NAME] including:
- Database schema design and migrations
- Row Level Security (RLS) policy implementation
- Auth integration debugging
- Performance optimization

## When To Use

- Creating or modifying database schemas
- Writing database migrations
- Implementing RLS policies
- Debugging Supabase auth or query issues
- Optimizing database performance

## Instrumentation

```bash
# Log usage when using this skill
Call MCP `call_tool_logger_manager` { action: "logSkill", name: "supabase", outcome: "manual" }
```

## What do you want to do?

1. **Create Database Migration** → Read `workflows/migration-workflow.md`
2. **Design RLS Policies** → Read `workflows/rls-policies.md`
3. **Debug Supabase Issues** → Read `workflows/debugging.md`
4. **Design Database Schema** → Read `workflows/schema-design.md`
5. **Review Best Practices** → Read `references/best-practices.md`
6. **See Common Patterns** → Read `references/common-patterns.md`

## Quick Reference

**Migration Template:** `templates/migration-template.sql`  
**RLS Template:** `templates/rls-policy-template.sql`  
**Existing Migrations:** `backend/migrations/`  
**Supabase Client:** `lib/supabaseClient.ts`
