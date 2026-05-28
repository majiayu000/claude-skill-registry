---
name: global-state
description: Global state management for cross-session persistence. Reference this skill to read/write global config, history, learnings, and statistics.
---

// Project Autopilot - Cross-Session State Management
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Global State Skill

Manage persistent state across Claude Code sessions. Works on macOS, Linux, and Windows.

---

## Directory Location

### Platform-Specific Paths

| Platform | Path |
|----------|------|
| macOS/Linux | `~/.claude/autopilot/` |
| Windows | `%USERPROFILE%\.claude\autopilot\` |

### Resolving the Path

```
FUNCTION getGlobalStateDir():
    IF platform == "windows":
        RETURN env.USERPROFILE + "\\.claude\\autopilot\\"
    ELSE:
        RETURN expandPath("~/.claude/autopilot/")
```

Or use Node.js style:
```javascript
const os = require('os');
const path = require('path');
const globalDir = path.join(os.homedir(), '.claude', 'autopilot');
```

---

## Directory Structure

```
{globalDir}/
├── config.json        # User preferences and defaults
├── history.json       # All projects built with outcomes
├── learnings.json     # Cross-project patterns and knowledge
└── statistics.json    # Aggregate stats and estimation accuracy
```

---

## File Schemas

### config.json

User preferences that persist across sessions.

```json
{
  "version": "1.0",
  "defaults": {
    "maxCost": 50,
    "warnCost": 10,
    "alertCost": 25,
    "maxTokens": 2000000,
    "warnTokens": 500000,
    "alertTokens": 1000000,
    "preferredModel": "sonnet",
    "autoApprove": false,
    "verboseOutput": false
  },
  "ui": {
    "compactStatus": false,
    "showEstimates": true,
    "showVariance": true
  },
  "created": "2026-01-28T00:00:00Z",
  "updated": "2026-01-28T00:00:00Z"
}
```

### history.json

Project history for estimation and resume.

```json
{
  "version": "1.0",
  "projects": [
    {
      "id": "uuid-v4",
      "name": "my-project",
      "path": "/Users/user/projects/my-project",
      "description": "User authentication system",
      "techStack": ["node", "typescript", "postgres"],
      "started": "2026-01-25T10:00:00Z",
      "completed": "2026-01-25T14:30:00Z",
      "status": "completed",
      "phases": {
        "total": 10,
        "completed": 10
      },
      "costs": {
        "estimated": 6.52,
        "actual": 5.89,
        "variance": -9.7
      },
      "tokens": {
        "input": 1250000,
        "output": 480000
      },
      "checkpointPath": ".autopilot/checkpoint.md",
      "outcome": "success",
      "notes": "Completed under budget"
    }
  ],
  "totalProjects": 1,
  "updated": "2026-01-28T00:00:00Z"
}
```

### learnings.json

Cross-project knowledge and patterns.

```json
{
  "version": "1.0",
  "techStacks": {
    "node-typescript-postgres": {
      "seenCount": 5,
      "avgPhaseCost": {
        "setup": 0.12,
        "database": 0.35,
        "auth": 0.38,
        "api": 0.85,
        "testing": 0.45
      },
      "commonDependencies": ["express", "prisma", "jest"],
      "typicalPhaseCount": 8,
      "notes": ["Always add input validation early", "Tests save time later"]
    }
  },
  "estimationAccuracy": {
    "byPhaseType": {
      "setup": { "avgVariance": -15, "samples": 12 },
      "database": { "avgVariance": 8, "samples": 10 },
      "auth": { "avgVariance": 12, "samples": 8 },
      "api": { "avgVariance": 5, "samples": 15 },
      "testing": { "avgVariance": -5, "samples": 11 }
    },
    "overall": {
      "avgVariance": 3,
      "samples": 56
    }
  },
  "commonPatterns": [
    {
      "pattern": "API with auth",
      "requiredPhases": ["setup", "database", "auth", "api", "testing"],
      "avgTotalCost": 3.50,
      "avgDuration": "4h"
    }
  ],
  "errorPatterns": [
    {
      "error": "Missing environment variables",
      "frequency": 15,
      "solution": "Add .env.example and validation on startup",
      "preventionPhase": "setup"
    }
  ],
  "updated": "2026-01-28T00:00:00Z"
}
```

### statistics.json

Aggregate metrics across all projects.

```json
{
  "version": "1.0",
  "totals": {
    "projects": 25,
    "successfulProjects": 23,
    "failedProjects": 2,
    "totalCost": 89.45,
    "totalTokens": {
      "input": 28500000,
      "output": 11200000
    },
    "totalPhases": 187,
    "totalTasks": 1245
  },
  "averages": {
    "costPerProject": 3.58,
    "tokensPerProject": 1588000,
    "phasesPerProject": 7.5,
    "tasksPerProject": 49.8,
    "durationPerProject": "3.5h"
  },
  "accuracy": {
    "overallEstimateAccuracy": 94.5,
    "bestPhaseType": "setup",
    "worstPhaseType": "frontend",
    "improvementTrend": "+2.3%"
  },
  "timeline": {
    "firstProject": "2026-01-01T00:00:00Z",
    "lastProject": "2026-01-28T00:00:00Z"
  },
  "updated": "2026-01-28T00:00:00Z"
}
```

---

## Operations

### Initialize Global State

First time setup - create directory and default files.

```
FUNCTION initializeGlobalState():

    dir = expandPath("~/.claude/autopilot/")

    IF NOT exists(dir):
        mkdir(dir)

    # Create default config if missing
    IF NOT exists(dir + "config.json"):
        WRITE defaultConfig to dir + "config.json"

    # Create empty history if missing
    IF NOT exists(dir + "history.json"):
        WRITE emptyHistory to dir + "history.json"

    # Create empty learnings if missing
    IF NOT exists(dir + "learnings.json"):
        WRITE emptyLearnings to dir + "learnings.json"

    # Create empty statistics if missing
    IF NOT exists(dir + "statistics.json"):
        WRITE emptyStatistics to dir + "statistics.json"

    RETURN success
```

### Read Global Config

Load user preferences with defaults fallback.

```
FUNCTION getGlobalConfig():

    path = expandPath("~/.claude/autopilot/config.json")

    IF NOT exists(path):
        initializeGlobalState()

    config = parseJSON(readFile(path))

    # Merge with defaults for any missing keys
    RETURN mergeWithDefaults(config, DEFAULT_CONFIG)
```

### Update Global Config

Save configuration changes.

```
FUNCTION updateGlobalConfig(updates):

    config = getGlobalConfig()

    # Deep merge updates
    FOR key, value IN updates:
        config[key] = deepMerge(config[key], value)

    config.updated = now()

    WRITE config to "~/.claude/autopilot/config.json"

    RETURN config
```

### Add Project to History

Record a completed project.

```
FUNCTION addProjectToHistory(project):

    path = expandPath("~/.claude/autopilot/history.json")
    history = parseJSON(readFile(path))

    projectEntry = {
        id: generateUUID(),
        name: project.name,
        path: project.path,
        description: project.description,
        techStack: project.techStack,
        started: project.started,
        completed: now(),
        status: project.status,
        phases: {
            total: project.totalPhases,
            completed: project.completedPhases
        },
        costs: {
            estimated: project.estimatedCost,
            actual: project.actualCost,
            variance: calculateVariance(project.estimatedCost, project.actualCost)
        },
        tokens: project.tokens,
        checkpointPath: project.checkpointPath,
        outcome: project.outcome,
        notes: project.notes
    }

    history.autopilots.push(projectEntry)
    history.totalProjects = history.autopilots.length
    history.updated = now()

    WRITE history to path

    # Also update statistics
    updateStatistics(projectEntry)

    # And learnings
    updateLearnings(projectEntry)

    RETURN projectEntry.id
```

### Find Similar Projects

Get historical projects for estimation.

```
FUNCTION findSimilarProjects(techStack, description):

    history = getHistory()
    matches = []

    FOR project IN history.autopilots:
        score = 0

        # Tech stack similarity
        commonTech = intersection(techStack, project.techStack)
        score += commonTech.length * 20

        # Description similarity (simple keyword match)
        IF hasCommonKeywords(description, project.description):
            score += 30

        IF score >= 40:
            matches.push({
                project: project,
                similarity: score
            })

    # Sort by similarity descending
    RETURN matches.sortBy(m => m.similarity).reverse()
```

### Get Estimation Adjustment

Calculate adjustment factor from historical accuracy.

```
FUNCTION getEstimationAdjustment(phaseType, techStack):

    learnings = getLearnings()

    # Check phase-specific accuracy
    IF learnings.estimationAccuracy.byPhaseType[phaseType]:
        phaseVariance = learnings.estimationAccuracy.byPhaseType[phaseType].avgVariance
    ELSE:
        phaseVariance = 0

    # Check tech stack accuracy
    stackKey = techStack.sort().join("-")
    IF learnings.techStacks[stackKey]:
        stackData = learnings.techStacks[stackKey]
        IF stackData.avgPhaseCost[phaseType]:
            # Use historical average if we have enough data
            RETURN {
                type: "historical",
                adjustment: 1 + (phaseVariance / 100),
                confidence: "high",
                historicalCost: stackData.avgPhaseCost[phaseType]
            }

    # Fall back to general phase variance
    RETURN {
        type: "estimated",
        adjustment: 1 + (phaseVariance / 100),
        confidence: phaseVariance != 0 ? "medium" : "low",
        historicalCost: null
    }
```

### Update Learnings

Extract and store knowledge from completed project.

```
FUNCTION updateLearnings(project):

    path = expandPath("~/.claude/autopilot/learnings.json")
    learnings = parseJSON(readFile(path))

    # Update tech stack knowledge
    stackKey = project.techStack.sort().join("-")
    IF NOT learnings.techStacks[stackKey]:
        learnings.techStacks[stackKey] = {
            seenCount: 0,
            avgPhaseCost: {},
            commonDependencies: [],
            typicalPhaseCount: 0,
            notes: []
        }

    stack = learnings.techStacks[stackKey]
    stack.seenCount++
    stack.typicalPhaseCount = runningAverage(
        stack.typicalPhaseCount,
        project.phases.total,
        stack.seenCount
    )

    # Update estimation accuracy
    variance = project.costs.variance
    overall = learnings.estimationAccuracy.overall
    overall.avgVariance = runningAverage(
        overall.avgVariance,
        variance,
        overall.samples + 1
    )
    overall.samples++

    learnings.updated = now()

    WRITE learnings to path
```

### Update Statistics

Aggregate project stats.

```
FUNCTION updateStatistics(project):

    path = expandPath("~/.claude/autopilot/statistics.json")
    stats = parseJSON(readFile(path))

    # Update totals
    stats.totals.autopilots++
    IF project.outcome == "success":
        stats.totals.successfulProjects++
    ELSE:
        stats.totals.failedProjects++

    stats.totals.totalCost += project.costs.actual
    stats.totals.totalTokens.input += project.tokens.input
    stats.totals.totalTokens.output += project.tokens.output
    stats.totals.totalPhases += project.phases.total

    # Update averages
    n = stats.totals.autopilots
    stats.averages.costPerProject = stats.totals.totalCost / n
    stats.averages.tokensPerProject = (
        stats.totals.totalTokens.input +
        stats.totals.totalTokens.output
    ) / n
    stats.averages.phasesPerProject = stats.totals.totalPhases / n

    # Update accuracy
    IF project.costs.variance != null:
        accuracy = 100 - Math.abs(project.costs.variance)
        oldAcc = stats.accuracy.overallEstimateAccuracy
        stats.accuracy.overallEstimateAccuracy = runningAverage(oldAcc, accuracy, n)

    # Update timeline
    stats.timeline.lastProject = now()
    stats.updated = now()

    WRITE stats to path
```

### Get Resumable Projects

Find projects that can be resumed.

```
FUNCTION getResumableProjects():

    history = getHistory()
    resumable = []

    FOR project IN history.autopilots:
        IF project.status == "in_progress" OR project.status == "paused":
            # Check if checkpoint exists
            checkpointPath = project.path + "/" + project.checkpointPath
            IF exists(checkpointPath):
                resumable.push({
                    id: project.id,
                    name: project.name,
                    path: project.path,
                    lastActivity: project.updated OR project.started,
                    progress: (project.phases.completed / project.phases.total) * 100,
                    remainingCost: project.costs.estimated - project.costs.actual
                })

    # Sort by last activity (most recent first)
    RETURN resumable.sortBy(p => p.lastActivity).reverse()
```

---

## Default Values

### DEFAULT_CONFIG

```json
{
  "version": "1.0",
  "defaults": {
    "maxCost": 50,
    "warnCost": 10,
    "alertCost": 25,
    "maxTokens": 2000000,
    "warnTokens": 500000,
    "alertTokens": 1000000,
    "preferredModel": "sonnet",
    "autoApprove": false,
    "verboseOutput": false
  },
  "ui": {
    "compactStatus": false,
    "showEstimates": true,
    "showVariance": true
  }
}
```

### EMPTY_HISTORY

```json
{
  "version": "1.0",
  "projects": [],
  "totalProjects": 0,
  "updated": null
}
```

### EMPTY_LEARNINGS

```json
{
  "version": "1.0",
  "techStacks": {},
  "estimationAccuracy": {
    "byPhaseType": {},
    "overall": {
      "avgVariance": 0,
      "samples": 0
    }
  },
  "commonPatterns": [],
  "errorPatterns": [],
  "updated": null
}
```

### EMPTY_STATISTICS

```json
{
  "version": "1.0",
  "totals": {
    "projects": 0,
    "successfulProjects": 0,
    "failedProjects": 0,
    "totalCost": 0,
    "totalTokens": {
      "input": 0,
      "output": 0
    },
    "totalPhases": 0,
    "totalTasks": 0
  },
  "averages": {
    "costPerProject": 0,
    "tokensPerProject": 0,
    "phasesPerProject": 0,
    "tasksPerProject": 0,
    "durationPerProject": "0h"
  },
  "accuracy": {
    "overallEstimateAccuracy": 0,
    "bestPhaseType": null,
    "worstPhaseType": null,
    "improvementTrend": null
  },
  "timeline": {
    "firstProject": null,
    "lastProject": null
  },
  "updated": null
}
```

---

## Integration Points

### Commands Using Global State

| Command | Reads | Writes |
|---------|-------|--------|
| `/autopilot:takeoff` | config, history, learnings | history, learnings, statistics |
| `/autopilot:radar` | config, history, learnings | - |
| `/autopilot:cockpit` | config, history | history |
| `/autopilot:altitude --global` | config, history, statistics | - |
| `/autopilot:config` | all | config |
| `/autopilot:portfolio` | history, statistics, learnings | history (archive) |
| `/autopilot:compare` | history, learnings, statistics | - |
| `/autopilot:estimate` | history, learnings | - |

---

## Portfolio Queries

### Get All Projects

```
FUNCTION getAllProjects(filters):

    history = readJSON("~/.claude/autopilot/history.json")

    projects = history.autopilots

    # Apply filters
    IF filters.status:
        projects = projects.filter(p => p.status == filters.status)

    IF filters.stack:
        projects = projects.filter(p =>
            p.techStack.some(t => filters.stack.includes(t))
        )

    IF filters.archived !== undefined:
        projects = projects.filter(p => p.archived == filters.archived)

    # Sort by last activity
    projects.sort((a, b) =>
        new Date(b.updated || b.completed) - new Date(a.updated || a.completed)
    )

    RETURN projects
```

### Get Portfolio Summary

```
FUNCTION getPortfolioSummary():

    history = readJSON("~/.claude/autopilot/history.json")
    statistics = readJSON("~/.claude/autopilot/statistics.json")

    RETURN {
        totalProjects: history.totalProjects,
        byStatus: {
            active: countByStatus(history, "in_progress"),
            paused: countByStatus(history, "paused"),
            completed: countByStatus(history, "completed"),
            failed: countByStatus(history, "failed")
        },
        costs: {
            total: statistics.totals.totalCost,
            average: statistics.averages.costPerProject
        },
        accuracy: statistics.accuracy.overallEstimateAccuracy,
        tokens: statistics.totals.totalTokens
    }
```

### Get Project By Name

```
FUNCTION getProjectByName(name):

    history = readJSON("~/.claude/autopilot/history.json")

    # Exact match
    project = history.autopilots.find(p =>
        p.name.toLowerCase() == name.toLowerCase()
    )

    IF NOT project:
        # Partial match
        project = history.autopilots.find(p =>
            p.name.toLowerCase().includes(name.toLowerCase())
        )

    RETURN project
```

### Archive Project

```
FUNCTION archiveProject(projectId):

    history = readJSON("~/.claude/autopilot/history.json")

    project = history.autopilots.find(p => p.id == projectId)

    IF NOT project:
        ERROR "Project not found"
        RETURN false

    project.archived = true
    project.archivedAt = now()

    writeJSON("~/.claude/autopilot/history.json", history)

    LOG "Project archived: {project.name}"
    RETURN true
```

### Get Cost Analysis

```
FUNCTION getCostAnalysis():

    history = readJSON("~/.claude/autopilot/history.json")
    statistics = readJSON("~/.claude/autopilot/statistics.json")

    analysis = {
        total: statistics.totals.totalCost,
        byProject: [],
        byStatus: {},
        byStack: {},
        trend: []
    }

    # By project
    FOR each project IN history.autopilots:
        analysis.byProject.push({
            name: project.name,
            cost: project.costs.actual,
            variance: project.costs.variance
        })

    # By status
    statuses = groupBy(history.autopilots, "status")
    FOR each status, projects IN statuses:
        analysis.byStatus[status] = {
            count: projects.length,
            total: sum(projects.map(p => p.costs.actual)),
            average: avg(projects.map(p => p.costs.actual))
        }

    # By tech stack
    stacks = {}
    FOR each project IN history.autopilots:
        stackKey = project.techStack.sort().join("-")
        IF NOT stacks[stackKey]:
            stacks[stackKey] = []
        stacks[stackKey].push(project)

    FOR each stack, projects IN stacks:
        analysis.byStack[stack] = {
            count: projects.length,
            total: sum(projects.map(p => p.costs.actual)),
            average: avg(projects.map(p => p.costs.actual))
        }

    RETURN analysis
```

### When to Read Global State

1. **Session Start** - Load config defaults
2. **Cost Estimation** - Get historical accuracy adjustments
3. **Project Scan** - Find similar projects for comparison
4. **Resume** - Find resumable projects

### When to Write Global State

1. **Project Completion** - Add to history, update learnings and stats
2. **Config Changes** - User updates preferences
3. **Phase Completion** - Update estimation accuracy
4. **Checkpoint Save** - Mark project status in history

---

## Error Handling

### File Access Errors

```
TRY:
    data = readGlobalFile(filename)
CATCH FileNotFound:
    initializeGlobalState()
    data = readGlobalFile(filename)
CATCH ParseError:
    # Backup corrupted file
    mv(filename, filename + ".backup." + timestamp)
    # Create fresh default
    data = getDefaultFor(filename)
    writeFile(filename, data)
    LOG warning: "Corrupted {filename} backed up and reset"
CATCH PermissionError:
    LOG error: "Cannot access ~/.claude/autopilot/ - check permissions"
    RETURN null
```

### Data Migration

When schema version changes:

```
FUNCTION migrateIfNeeded(data, filename):

    currentVersion = SCHEMA_VERSIONS[filename]
    dataVersion = data.version OR "0.0"

    IF dataVersion < currentVersion:
        data = applyMigrations(data, dataVersion, currentVersion)
        data.version = currentVersion
        writeFile(filename, data)
        LOG "Migrated {filename} from v{dataVersion} to v{currentVersion}"

    RETURN data
```

---

## Performance Notes

- Global state files are small (<1MB typically)
- Read at session start, cache in memory
- Write atomically (temp file + rename)
- Don't re-read during execution unless explicitly needed
