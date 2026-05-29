---
name: todo-domain-expert
description: Provides domain knowledge and rules for Todo task management systems.
---

# Todo Domain Rules

## Core Entities
- Task
- User

## Task Attributes
- id
- title
- description
- status (pending, completed)
- created_at
- updated_at

## Domain Rules
- Every task belongs to exactly one user
- Users cannot access others’ tasks
- Status transitions must be valid
- Deletion must be explicit

## UX Expectations
- Clear confirmations
- Helpful error messages
- Predictable behavior

Apply consistently across CLI, Web, and AI Agent phases.
