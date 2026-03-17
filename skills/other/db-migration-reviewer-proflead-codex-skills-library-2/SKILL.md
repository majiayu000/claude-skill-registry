---
name: db-migration-reviewer
description: Review database migrations for safety and rollback. Use when a mid-level developer needs validation of schema changes.
---

# DB Migration Reviewer

## Purpose
Review database migrations for safety and rollback.

## Inputs to request
- Migration scripts and execution order.
- Database size and traffic patterns.
- Rollback strategy and downtime tolerance.

## Workflow
1. Check for locks, long-running operations, and data backfills.
2. Ensure forward and rollback paths are defined.
3. Confirm migration order and dependency handling.

## Output
- Migration risks and recommended changes.

## Quality bar
- Flag operations that lock large tables.
- Call out data loss risks explicitly.
