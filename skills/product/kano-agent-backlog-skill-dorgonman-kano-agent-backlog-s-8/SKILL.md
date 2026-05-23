---
name: kano-agent-backlog-skill
description: Local-first, multi-product backlog management with agent collaboration discipline.
---

# kano-agent-backlog-skill

**Claude/Goose Skill Adapter** - This is a thin wrapper that points to the canonical skill documentation.

---

## 🎯 Quick Start

This skill provides **local-first, multi-product backlog management** with agent collaboration discipline.

**📚 Canonical Documentation**: @skills/kano-agent-backlog-skill/SKILL.md

> [!IMPORTANT]
> **You MUST read the canonical SKILL.md** before using this skill. The sections below provide quick navigation to key topics.

---

## Essential Reading (From Canonical SKILL.md)

### 1. **Overview and Core Concepts**
   - Read: [Purpose](../../../skills/kano-agent-backlog-skill/SKILL.md#purpose)
   - Read: [Core Concepts](../../../skills/kano-agent-backlog-skill/SKILL.md#core-concepts)

### 2. **CLI Commands**
   - Reference: [CLI Reference](../../../skills/kano-agent-backlog-skill/SKILL.md#cli-reference)
   - Bootstrap: `kano-backlog admin init --product <name> --agent <id>`
   - Create item: `kano-backlog workitem create --type Task --title "..." --agent <id>`
   - Update state: `kano-backlog workitem update-state <ID> --state Done --agent <id>`
   - Refresh views: `kano-backlog view refresh --agent <id>`

### 3. **Workflows and Discipline**
   - Read: [Agent Workflows](../../../skills/kano-agent-backlog-skill/SKILL.md#agent-workflows)
   - Read: [Backlog Discipline](../../../skills/kano-agent-backlog-skill/SKILL.md#backlog-discipline)

---

## Installation

```bash
cd skills/kano-agent-backlog-skill
pip install -e .
```

---

## Common Tasks

### Create a New Work Item
```bash
python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem create \
  --type Task \
  --title "Implement feature X" \
  --product kano-agent-backlog-skill \
  --agent claude
```

### Update Item State
```bash
python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem update-state KABSD-TSK-0001 \
  --state InProgress \
  --agent claude
```

---

## References

| Topic | Link |
|-------|------|
| **Full Documentation** | [`SKILL.md`](../../../skills/kano-agent-backlog-skill/SKILL.md) |
| **CLI Reference** | [`SKILL.md#cli-reference`](../../../skills/kano-agent-backlog-skill/SKILL.md#cli-reference) |
| **Architecture ADRs** | [`decisions/`](../../../_kano/backlog/products/kano-agent-backlog-skill/decisions/) |
