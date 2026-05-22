---
name: permission-management
description: Central authority for Claude Code permissions. Covers permission system (tiered model, read-only, bash, file modification), permission rules (allow, ask, deny), rule precedence, permission modes (default, acceptEdits, plan, bypassPermissions), tool-specific permission rules (Bash patterns, Read/Edit patterns, WebFetch domains, MCP tools), /permissions command, and additionalDirectories. Assists with configuring permission rules, understanding permission modes, and troubleshooting permission issues. Delegates 100% to docs-management skill for official documentation.
user-invocable: false
allowed-tools: Read, Glob, Grep, Skill
---

# Permission Management Skill

## MANDATORY: Invoke docs-management First

> **STOP - Before providing ANY response about Claude Code permissions:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**

### Verification Checkpoint

Before responding, verify:

- [ ] Did I invoke docs-management skill?
- [ ] Did official documentation load?
- [ ] Is my response based EXCLUSIVELY on official docs?

If ANY checkbox is unchecked, STOP and invoke docs-management first.

---

## Overview

Central authority for Claude Code permissions. This skill uses **100% delegation to docs-management** - it contains NO duplicated official documentation.

**Architecture:** Pure delegation with keyword registry. All official documentation is accessed via docs-management skill queries.

## When to Use This Skill

**Keywords:** permissions, allow rules, deny rules, ask rules, permission modes, defaultMode, acceptEdits, bypassPermissions, plan mode, tool permissions, Bash permissions, Read permissions, Edit permissions, WebFetch permissions, MCP permissions, additionalDirectories, /permissions

**Use this skill when:**

- Configuring permission rules
- Understanding permission modes
- Setting up tool-specific permissions
- Troubleshooting permission issues
- Adding additional working directories
- Understanding rule precedence

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Permission System

| Topic | Keywords |
| --- | --- |
| Overview | "permission system", "tiered permissions", "approval required" |
| Configuration | "configuring permissions", "/permissions command" |
| Rule Types | "allow rules", "ask rules", "deny rules" |
| Precedence | "rule precedence", "deny > ask > allow" |

### Permission Modes

> ⚠️ **STALENESS WARNING:** Do NOT hardcode permission mode names or values.
> Query docs-management for the authoritative list of permission modes.

| Topic | Query Pattern | What You'll Find |
| --- | --- | --- |
| All Modes | "iam.md permission modes" | Complete list of available modes |
| Mode Behavior | "iam.md defaultMode acceptEdits" | Mode descriptions and effects |
| Mode Configuration | "iam.md configuring permission mode" | How to set modes |

### Tool-Specific Rules

> ⚠️ **STALENESS WARNING:** Do NOT hardcode tool names or pattern syntax.
> Query docs-management for the authoritative list of tools and permission patterns.

| Topic | Query Pattern | What You'll Find |
| --- | --- | --- |
| Bash Rules | "iam.md Bash permissions pattern matching" | Bash permission syntax |
| File Rules | "iam.md Read Edit permissions gitignore" | File permission patterns |
| Path Patterns | "iam.md path pattern types" | Absolute, home, relative patterns |
| WebFetch Rules | "iam.md WebFetch domain permissions" | Domain pattern syntax |
| MCP Rules | "iam.md MCP permissions mcp__server" | MCP tool permission syntax |

### Working Directories

| Topic | Keywords |
| --- | --- |
| Additional Dirs | "additionalDirectories", "--add-dir" |
| Working Directory | "working directories", "file access scope" |

## Quick Decision Tree

**What do you want to do?**

1. **Set up allow rules** -> Query docs-management: "allow rules", "auto-approve"
2. **Set up deny rules** -> Query docs-management: "deny rules", "prevent usage"
3. **Set up ask rules** -> Query docs-management: "ask rules", "confirmation required"
4. **Change permission mode** -> Query docs-management: "permission modes", "defaultMode"
5. **Configure Bash permissions** -> Query docs-management: "Bash permissions", "Bash pattern matching"
6. **Configure file permissions** -> Query docs-management: "Read Edit permissions", "gitignore-style"
7. **Add working directories** -> Query docs-management: "additionalDirectories", "--add-dir"
8. **Configure MCP permissions** -> Query docs-management: "MCP permissions", "mcp__server"

## Topic Coverage

### Permission System Topics

- Tiered permission model (read-only, bash, file modification)
- Allow rules (auto-approve)
- Ask rules (confirmation required)
- Deny rules (prevent usage)
- Rule precedence (deny > ask > allow)
- Permission rule format

### Permission Modes Topics

- default mode (standard prompting)
- acceptEdits mode (auto-accept file edits)
- plan mode (analyze only, no modifications)
- bypassPermissions mode (skip all prompts)

### Tool Permission Rules

- Bash permission patterns (exact match, prefix match)
- Bash pattern limitations
- Read and Edit gitignore-style patterns
- Path pattern types (absolute, home, relative)
- WebFetch domain permissions
- MCP tool permissions (no wildcards)
- Hooks for custom permission evaluation

### Working Directories Topics

- additionalDirectories configuration
- --add-dir CLI flag
- Scope of file access

## Troubleshooting Quick Reference

| Issue | Keywords for docs-management |
| --- | --- |
| Permission too restrictive | "allow rules", "auto-approve" |
| Permission too permissive | "deny rules", "prevent usage" |
| Wrong mode active | "permission modes", "defaultMode" |
| MCP tools blocked | "MCP permissions", "mcp__server" |
| Can't access files | "additionalDirectories", "--add-dir" |

## Related Skills

- **sandbox-configuration** - For sandboxing and isolation
- **enterprise-security** - For managed policies
- **settings-management** - For general configuration

## Version History

- **v1.0.0** (2025-11-30): Initial release (split from security-meta)
  - Focused on permissions only
  - Pure delegation architecture
  - Comprehensive keyword registry

---

## Last Updated

**Date:** 2025-11-30
**Model:** claude-opus-4-5-20251101
