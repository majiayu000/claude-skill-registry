---
name: pi-messenger-crew
description: Use pi-messenger for multi-agent coordination and Crew task orchestration. Covers joining the mesh, planning from PRDs, working on tasks, file reservations, and agent messaging. Load this skill when using pi_messenger or building with Crew.
---

# Pi-Messenger Crew Skill

Use pi-messenger for multi-agent coordination and Crew task orchestration.

## Quick Reference

### Join the Mesh (Required First)
```typescript
pi_messenger({ action: "join" })
```

### Check Status
```typescript
pi_messenger({ action: "status" })
pi_messenger({ action: "list" })  // See other agents
```

### Crew Workflow

#### 1. Install Crew Agents (one-time)
```typescript
pi_messenger({ action: "crew.install" })
pi_messenger({ action: "crew.agents" })  // Verify 5 agents
```

#### 2. Plan from PRD
```typescript
// Auto-discover PRD.md in current directory
pi_messenger({ action: "plan" })

// Or specify path
pi_messenger({ action: "plan", prd: "path/to/PRD.md" })
```

#### 3. Work on Tasks
```typescript
// Single wave (runs ready tasks once)
pi_messenger({ action: "work" })

// Autonomous (keeps running until done/blocked)
pi_messenger({ action: "work", autonomous: true })
```

#### 4. Task Management
```typescript
pi_messenger({ action: "task.list" })
pi_messenger({ action: "task.ready" })  // Tasks with no pending deps
pi_messenger({ action: "task.show", id: "task-1" })
pi_messenger({ action: "task.start", id: "task-1" })
pi_messenger({ action: "task.done", id: "task-1", summary: "What was done" })
pi_messenger({ action: "task.block", id: "task-1", reason: "Why blocked" })
pi_messenger({ action: "task.unblock", id: "task-1" })
pi_messenger({ action: "task.reset", id: "task-1" })
pi_messenger({ action: "task.reset", id: "task-1", cascade: true })  // Reset dependents too
```

#### 5. Review
```typescript
// Review a task implementation
pi_messenger({ action: "review", target: "task-1" })

// Review the overall plan
pi_messenger({ action: "review", target: "plan", type: "plan" })
```

### File Coordination

```typescript
// Reserve files before editing
pi_messenger({ action: "reserve", paths: ["src/index.ts", "src/types.ts"], reason: "Working on core" })

// Release when done
pi_messenger({ action: "release" })
```

### Agent Communication

```typescript
// Rename yourself
pi_messenger({ action: "rename", name: "MyAgentName" })

// Send message to specific agent
pi_messenger({ action: "send", to: "OtherAgent", message: "Hello!" })

// Broadcast to all
pi_messenger({ action: "send", broadcast: true, message: "Announcement" })
```

## Typical Crew Session

```typescript
// 1. Join
pi_messenger({ action: "join" })

// 2. Plan (spawns planner agent)
pi_messenger({ action: "plan" })

// 3. Check tasks
pi_messenger({ action: "task.list" })

// 4. Work
pi_messenger({ action: "work", autonomous: true })

// 5. Status
pi_messenger({ action: "status" })
```

## Data Storage

Crew stores data in `.pi/messenger/crew/`:
```
.pi/messenger/crew/
├── config.json       # Project config (concurrency, etc.)
├── plan.json         # Plan metadata
├── plan.md           # Planner output
├── tasks/
│   ├── task-1.json   # Task metadata
│   ├── task-1.md     # Task spec
│   └── ...
├── blocks/
│   └── task-N.md     # Block context
└── artifacts/        # Debug artifacts
```

## Config Options

Create `.pi/messenger/crew/config.json`:
```json
{
  "concurrency": {
    "workers": 3    // Max parallel workers (default: 2)
  },
  "planning": {
    "maxPasses": 3  // Max planner passes before accepting last output
  }
}
```
