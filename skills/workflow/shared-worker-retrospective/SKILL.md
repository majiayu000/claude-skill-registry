---
name: shared-worker-retrospective
description: Retrospective contribution format for Developer, Tech Artist, QA, and Game Designer workers. Use proactively when retrospective is triggered to contribute your perspective.
category: workflow
tags: [retrospective, contribution, feedback, improvement]
dependencies: [shared-worker-task-memory, shared-ralph-core]
---

# Worker Retrospective Contributions

> "When retrospective triggers, contribute your perspective – read memory, write separate file, delete memory."

## When to Use This Skill

Use **when**:
- `prd.json.agents.{agent}.status == "awaiting_retrospective"`
- `.claude/session/retrospective.txt` exists

Use **proactively**:
- **MANDATORY**: Read ALL task memory files first
- Create your own contribution file (separate file per agent)
- Delete ALL task memory files after contributing

---

## Quick Start

<examples>
Example 1: Developer contribution
```json
// File: .claude/session/retrospective-developer.json
{
  "taskId": "feat-001",
  "agent": "developer",
  "timestamp": "2026-01-23T15:45:00Z",
  "contribution": {
    "implementationDecisions": [
      "Used React Three Fiber for scene composition",
      "Chose Rapier for physics simulation"
    ],
    "technicalChallenges": [
      "Synchronizing physics with rendering loop"
    ],
    "whatWorkedWell": [
      "Component-based architecture made testing easier"
    ],
    "areasForImprovement": [
      "Need better error handling in physics sync"
    ],
    "lessonsLearned": [
      "Prefer R3F abstractions over raw Three.js"
    ]
  }
}
```

Example 2: QA contribution
```json
// File: .claude/session/retrospective-qa.json
{
  "taskId": "feat-001",
  "agent": "qa",
  "timestamp": "2026-01-23T16:00:00Z",
  "contribution": {
    "validationResultsSummary": {
      "typeScript": "pass",
      "lint": "pass",
      "tests": "pass",
      "build": "pass",
      "browser": "pass"
    },
    "codeQualityObservations": [
      "Code is maintainable with clear structure",
      "Proper error handling throughout"
    ],
    "qualityConcerns": [],
    "suggestionsForImprovement": [
      "Consider adding more edge case tests"
    ]
  }
}
```

Example 3: Tech Artist contribution
```json
// File: .claude/session/retrospective-techartist.json
{
  "taskId": "vis-002",
  "agent": "techartist",
  "timestamp": "2026-01-23T14:30:00Z",
  "contribution": {
    "visualAssetsCreated": [
      "Custom shader for water effects",
      "Particle system for explosions"
    ],
    "visualQualityAssessment": "Matches GDD specifications",
    "performanceMetrics": {
      "frameRateImpact": "minimal",
      "drawCalls": "+15",
      "shaderComplexity": "medium"
    },
    "whatWorkedWell": [
      "Shader compilation succeeded on first try"
    ],
    "lessonsLearned": [
      "Test shaders on mobile targets early"
    ]
  }
}
```
</examples>

---

## Contribution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. READ ALL TASK MEMORY (MANDATORY)                         │
│     Directory: .claude/session/agents/{agent}/               │
│     Pattern: task-*.md                                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  2. READ retrospective.txt for context                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  3. CREATE YOUR CONTRIBUTION FILE                           │
│     .claude/session/retrospective-{agent}.json              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  4. DELETE ALL TASK MEMORY FILES                            │
│     .claude/session/agents/{agent}/task-*.md                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  5. UPDATE STATUS, LOG, EXIT                                │
│     PM will merge all contributions                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Why Separate Files?

**Previous Problem**: All workers writing to single `retrospective.txt`
- Race conditions: last write wins
- File watcher triggers multiple times
- No atomic write guarantees

**Solution**: Each agent writes to their own file
- No contention between agents
- PM reads all files and merges atomically
- Clear ownership of each contribution

---

## Contribution File Locations

| Agent | Contribution File |
|-------|------------------|
| Developer | `.claude/session/retrospective-developer.json` |
| Tech Artist | `.claude/session/retrospective-techartist.json` |
| QA | `.claude/session/retrospective-qa.json` |
| Game Designer | `.claude/session/retrospective-gamedesigner.json` |

---

## Contribution Structure

All contributions follow this JSON structure:

```json
{
  "taskId": "string",
  "agent": "developer|techartist|qa|gamedesigner",
  "timestamp": "ISO 8601",
  "contribution": {
    // Agent-specific fields
  }
}
```

---

## Agent-Specific Fields

### Developer
| Field | Description |
|-------|-------------|
| `implementationDecisions` | Key technical decisions made |
| `technicalChallenges` | Difficulties faced and solutions |
| `whatWorkedWell` | Effective solutions/patterns |
| `areasForImprovement` | What could be better |
| `lessonsLearned` | Suggestions for future tasks |

### QA
| Field | Description |
|-------|-------------|
| `validationResultsSummary` | TypeScript, lint, test, build, browser results |
| `codeQualityObservations` | Maintainability, smells, error handling |
| `qualityConcerns` | Performance, test coverage, patterns |
| `suggestionsForImprovement` | What would make code better |

### Tech Artist
| Field | Description |
|-------|-------------|
| `visualAssetsCreated` | Materials, shaders, effects implemented |
| `visualQualityAssessment` | How well visuals match GDD |
| `performanceMetrics` | Frame rate, draw calls, triangles, memory |
| `challengesFaced` | Shader/asset integration difficulties |
| `whatWorkedWell` | Effective visual techniques |
| `lessonsLearned` | Shader patterns, pipeline improvements |

### Game Designer
| Field | Description |
|-------|-------------|
| `designDecisionsMade` | Key design choices |
| `gddClarityIssues` | Unclear specifications |
| `playtestFindings` | Mechanics needing refinement |
| `whatWorkedWell` | Effective design patterns |
| `lessonsLearned` | Design process improvements |

---

## Contribution Guidelines

### Be Specific
- Mention specific files, functions, patterns
- Note unexpected issues
- Share what surprised you

### Be Honest
- If you took shortcuts, mention them
- If something felt hacky, say so
- If PRD was unclear, explain why

### Be Constructive
- Suggest improvements for future tasks
- Note what would have helped
- Identify areas needing refactoring

---

## Anti-Patterns

❌ **DON'T**:
- Skip contributing to retrospective
- Write generic/vague contributions
- Edit other agents' sections
- Delete or modify retrospective structure
- **FORGET** to read task memory first
- **FORGET** to delete ALL task memory files

✅ **DO**:
- Read ALL task memory files first
- Write specific, detailed contributions
- Use your own contribution file
- Delete memory after contributing
- Be honest and constructive

---

## ⚠️ Critical Reminder

**Your retrospective contribution will be GENERIC and USELESS without reading task memory first!**

Task memory files contain everything you noted during execution. Read them ALL before writing your contribution.

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-worker-task-memory` | Task memory tracking during execution |
| `shared-ralph-core` | Session structure and state management |
| `shared-ralph-event-protocol` | Event-driven messaging protocol |
