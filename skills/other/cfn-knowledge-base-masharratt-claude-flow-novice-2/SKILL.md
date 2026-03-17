---
name: cfn-knowledge-base
description: "Organizational learning from CFN Loop execution - workflow codification and playbooks. Use when you need to store successful patterns, query past learnings, track edge cases and failures, or retrieve agent configurations and iteration strategies from previous tasks."
version: 1.0.0
tags: [mega-skill, learning, workflow, playbook]
status: production
---

# Knowledge Base Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Organizational learning from CFN Loop execution
**Status:** Production
**Consolidates:** workflow-codification, cfn-playbook
**Confidence:** 7.0/10 (dual learning systems)

---

## Overview

This mega-skill provides organizational learning:
- **Workflow** - Track edge cases, failures, cost metrics, ROI
- **Playbook** - Store successful patterns, agent configs, iteration strategies

---

## Directory Structure

```
knowledge-base/
├── SKILL.md              # This file
├── execute.sh            # Main entry point
├── cli/
│   └── knowledge-base.sh # Unified CLI interface
├── lib/
│   ├── workflow/         # From workflow-codification
│   └── playbook/         # From cfn-playbook
└── data/                 # Database files (created on init)
    ├── workflows.db
    ├── playbooks.db
    └── learnings.db
```

---

## Learning System

- **Successes** → Playbook (what worked)
- **Failures** → Workflow codification (what to avoid)
- Combined: Complete organizational memory

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| workflow-codification/ | knowledge-base/lib/workflow/ |
| cfn-playbook/ | knowledge-base/lib/playbook/ |

---

## Usage

### Main Entry Point
```bash
# Initialize databases
./execute.sh init

# Query for patterns
./execute.sh query 'authentication'

# Store new learning
./execute.sh store playbook '{"task_type": "auth", "pattern": "..."}'

# Show help
./execute.sh help
```

### Advanced CLI Usage
```bash
# Direct CLI access
./cli/knowledge-base.sh --help

# Query workflow patterns
./cli/knowledge-base.sh query-workflow --pattern 'auth'

# Query playbook entries
./cli/knowledge-base.sh query-playbook --task-type bugfix

# Store learning with metadata
./cli/knowledge-base.sh store-learning \
  --type workflow \
  --category edge-case \
  --data '...' \
  --confidence 0.85
```

## Version History

### 1.1.0 (2025-12-08)
- Fixed bootstrap utilities path to use shared location
- Created unified CLI interface
- Added main execute.sh entry point
- Integrated workflow and playbook functionality

### 1.0.0 (2025-12-02)
- Consolidated workflow + playbook into unified knowledge base

