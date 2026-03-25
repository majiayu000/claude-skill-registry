---
name: system-cleaner
description: PAL system housekeeping audits. USE WHEN audit system, check references, validate naming, find orphans, health report, system health, clean system. AgentSearch('system-cleaner') for docs.
user-invocable: false
---

# system-cleaner

System-wide housekeeping skill for auditing PAL integrity, naming conventions, and hygiene.

## Authoritative Sources

**Before running ANY audit, reference:**

- `.claude/core/reference/ROUTING_TABLE.md` — Agent routing entries
- `.claude/core/reference/SYSTEM_INDEX.md` — System-wide capability index
- Each agent's **Section 5: My Capabilities** — Source of truth for capabilities
- `CLAUDE.md` — Naming conventions and domain workspace structure

## Workflow Routing

| Workflow             | Trigger                                              | File                            |
| :------------------- | :--------------------------------------------------- | :------------------------------ |
| **audit_references** | "audit references", "check references", "sync index" | `workflows/audit_references.md` |
| **audit_domains**    | "audit domains", "check domains", "domain health"    | `workflows/audit_domains.md`    |
| **audit_naming**     | "audit naming", "check names", "naming conventions"  | `workflows/audit_naming.md`     |
| **audit_orphans**    | "audit orphans", "find orphans", "clean system"      | `workflows/audit_orphans.md`    |
| **health_report**    | "health report", "system health", "full audit"       | `workflows/health_report.md`    |

---

## What Each Audit Covers

| Audit                | Checks                                                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **audit_references** | Unregistered agents/skills/workflows, dead references in ROUTING_TABLE & SYSTEM_INDEX, agent Section 5 ↔ SYSTEM_INDEX mismatches |
| **audit_domains**    | Missing domain folders, INDEX.md consistency, Active Work table ↔ 01_PROJECTS/ sync, agent ↔ domain cross-check                  |
| **audit_naming**     | File/folder naming convention violations, YAML frontmatter validation for agents, skills, and domain INDEX files                 |
| **audit_orphans**    | Unclaimed skills, unreferenced domain files, stale session logs (>30 days), empty folders                                        |
| **health_report**    | Runs ALL four audits and generates a consolidated dashboard                                                                      |

---

## Examples

**Example 1: Run a full system health check**

```
User: "Run a system health report"
1. Execute health_report workflow
2. Runs all 4 sub-audits sequentially
3. Generates consolidated dashboard with per-category status
```

**Example 2: Check if all agents are registered**

```
User: "Are all my agents in the routing table?"
1. Execute audit_references workflow
2. Scans .claude/agents/ for files on disk
3. Parses ROUTING_TABLE.md and SYSTEM_INDEX.md
4. Reports unregistered agents and dead references
```

**Example 3: Clean up stale sessions**

```
User: "Find old session logs I should archive"
1. Execute audit_orphans workflow
2. Scans all 04_SESSIONS/ folders across domains
3. Flags files older than 30 days
4. Suggests archiving to 05_ARCHIVE/
```

**Example 4: Check naming conventions**

```
User: "Are my files named correctly?"
1. Execute audit_naming workflow
2. Checks system files, domain folders, skill folders, agent files, domain content files
3. Validates YAML frontmatter in agents, skills, and INDEX files
4. Reports violations with suggested fixes
```

---

## Quick Reference

**Skill Location:** `.claude/skills/system-cleaner/`

**Workflows:**

1. `audit_references` — Reference integrity (ROUTING_TABLE, SYSTEM_INDEX, agent capabilities)
2. `audit_domains` — Domain structure and INDEX consistency
3. `audit_naming` — Naming conventions and frontmatter validation
4. `audit_orphans` — Orphan files, stale sessions, empty folders
5. `health_report` — Full system dashboard (runs all audits)

**Owner:** `pal-master` (system-level skill)

**Report Output:** All audits generate markdown reports. `health_report` generates a consolidated dashboard.
