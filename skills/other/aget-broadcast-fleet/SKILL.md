---
name: aget-broadcast-fleet
description: Send communications to fleet members
archetype: supervisor
allowed-tools:
  - Read
  - Glob
  - Write
---

# aget-broadcast-fleet

Send communications to multiple fleet members. Supports announcements, directives, and release handoffs.

## Instructions

When this skill is invoked:

1. **Determine Message Type**
   - Announcement: Informational
   - Directive: Action required
   - Handoff: Release notification

2. **Resolve Targets**
   - All fleet
   - By portfolio
   - Specific agents

3. **Format Message**
   - Apply type-appropriate template
   - Include required fields
   - Set priority

4. **Create Artifacts**
   - Generate handoff files per target
   - Track delivery status
   - Log broadcast

## Message Types

| Type | Purpose | Template |
|------|---------|----------|
| Announcement | Inform | `ANNOUNCE_*.md` |
| Directive | Instruct | `DIRECTIVE_*.md` |
| Handoff | Release | `RELEASE_HANDOFF_*.md` |

## Output Format

```markdown
## Fleet Broadcast

### Message Info

| Field | Value |
|-------|-------|
| Type | [Announcement/Directive/Handoff] |
| From | [Supervisor Agent] |
| Date | [YYYY-MM-DD HH:MM] |
| Priority | [Normal/Urgent] |

---

### Targets

| Agent | Portfolio | Status |
|-------|-----------|--------|
| [agent-1] | [main] | [Pending/Sent] |
| [agent-2] | [main] | [Pending/Sent] |

**Total**: [N] agents

---

### Message Content

**Subject**: [Title]

[Message body]

---

### Artifacts Created

| Agent | Artifact | Location |
|-------|----------|----------|
| [agent-1] | RELEASE_HANDOFF_vX.Y.Z.md | [path] |

---

### Tracking

- [ ] All targets notified
- [ ] Delivery confirmed
```

## Handoff Template

```markdown
# Release Handoff: vX.Y.Z

**From**: [Supervisor]
**To**: [Agent]
**Date**: [YYYY-MM-DD]

## Release Summary
[What changed]

## Upgrade Guide
[How to upgrade]

## Action Required
- [ ] Acknowledge receipt
- [ ] Schedule upgrade
- [ ] Report completion
```

## Constraints

- **C1**: NEVER broadcast without target confirmation — accidental broadcasts waste agent attention
- **C2**: NEVER modify agent configurations during broadcast — broadcast is communication, not configuration
- **C3**: NEVER suppress delivery failures — failures must be visible

## Related

- SKILL-035: aget-broadcast-fleet specification
- ONTOLOGY_supervisor.yaml: Fleet, Broadcast, Release_Handoff concepts
- CAP-SUP-001: Fleet Broadcast capability
- L511: Release-to-Fleet Propagation
