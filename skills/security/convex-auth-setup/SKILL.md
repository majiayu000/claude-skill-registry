---
name: convex-auth-setup
description: Set up Convex authentication, user mapping, authorization, and custom function wrappers for data protection.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Auth Setup

Use this skill when the task involves auth providers, `users` tables, `getCurrentUser` helpers, access control, or multi-tenant data protection.

## Default approach

- Map auth identity to an application user record.
- Centralize auth helpers instead of repeating lookup logic everywhere.
- Verify both authentication and authorization in public functions.
- Prefer custom function wrappers for repeated access-control behavior.

## AgentForge-specific guidance

- Keep auth in Convex focused on data access, identity mapping, and encrypted key storage where applicable.
- Do not treat Convex auth as a place to run Mastra or general agent orchestration.

## References

- Read [auth-patterns.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-auth-setup/references/auth-patterns.md) for helper patterns and data-protection wrappers.
