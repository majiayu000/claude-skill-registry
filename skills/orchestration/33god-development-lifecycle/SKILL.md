---
name: 33god-development-lifecycle
description: Meta-level orchestration for 33GOD platform development. Use when (1) coordinating cross-component features across multiple services, (2) assessing platform-wide status and component maturity, (3) managing hierarchical BMAD workflows (platform-level + component-level), (4) delegating tasks to component teams via Zellij, (5) generating platform architecture artifacts (integration maps, component inventories, system status), (6) planning strategic roadmap for multi-component ecosystem.
---

# 33GOD Development Lifecycle

## Overview

This skill provides meta-level orchestration for the **33GOD event-driven platform**, coordinating development across multiple independent components using hierarchical BMAD workflows and Bloodbank events.

**The Event-Driven Architecture:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    33GOD PLATFORM ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   HOLYFIELDS → BLOODBANK → CANDYSTORE → HOLOCENE → COMPONENTS               │
│   (Schemas)     (Events)    (History)    (View)      (Services)             │
│                    │                              & AGENTS                  │
│                    │                                                         │
│                    ▼                                                         │
│            system.heartbeat.tick                                             │
│            (every 60 seconds)                                                │
│                    │                                                         │
│                    ▼                                                         │
│            HeartbeatRouter                                                   │
│                    │                                                         │
│                    ▼                                                         │
│            Agent Coordination                                                │
│            & Cross-Component Sync                                           │
│                                                                              │
│   This skill operates at the PLATFORM level, coordinating all components     │
│   through BMAD workflows AND Bloodbank events.                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

It enables Director of Engineering level coordination, cross-component story management, and component maturity tracking through both traditional workflows and event-driven automation.

## Core Concepts

### Hierarchical BMAD Structure

The 33GOD platform uses two BMAD levels:

**Meta-Level** (Platform root at `/33GOD`):
- Project Level 4 (Enterprise expansion)
- Coordinates cross-component initiatives
- Tracks integration dependencies
- Manages platform roadmap

**Component-Level** (Each service directory):
- Project Level 0-3 (varies by component)
- Independent BMAD workflows
- Component-specific development
- Reports status to meta-level

See [references/hierarchical-bmad.md](references/hierarchical-bmad.md) for detailed architecture.

### Delegation Model

**Pattern**: Hierarchical command delegation via Zellij

1. Meta-orchestrator identifies cross-component work
2. Decomposes into component-specific tasks
3. Delegates via Zellij tabs (parallel execution)
4. Monitors completion through status aggregation
5. Verifies integration end-to-end

See [references/delegation-patterns.md](references/delegation-patterns.md) for patterns and examples.

## Workflow Decision Tree

```
Is this cross-component work?
├─ YES → Use meta-level orchestration
│   ├─ Check platform status (workflow below)
│   ├─ Create platform story (workflow below)
│   └─ Delegate to components (workflow below)
│
└─ NO → Use component-level BMAD
    └─ Navigate to component directory
    └─ Run component orchestrator
```

## Primary Workflows

### 1. Platform Status Review

**Trigger**: User asks "/platform-status" or "show me component status"

**Purpose**: Aggregate BMAD status across all components

**Steps**:
1. Run platform status script:
   ```bash
   cd /33GOD
   PLATFORM_ROOT=/33GOD ./scripts/platform-status.sh
   ```

2. Script scans all component directories for:
   - `bmad/config.yaml` (component configuration)
   - `docs/bmm-workflow-status.yaml` (workflow completion)

3. Generates `docs/platform-status.md` with:
   - Component-by-component status summary
   - Maturity indicators (✓, ⚠, →, -)
   - Cross-component recommendations
   - Integration readiness assessment

4. Present summary to user with key insights:
   - How many components have completed planning
   - How many are in implementation
   - Critical blockers or gaps

**Output**: Platform status report with actionable recommendations

---

### 2. Component Maturity Assessment

**Trigger**: User asks "/component-inventory" or "assess component maturity"

**Purpose**: Generate comprehensive maturity matrix for all components

**Steps**:
1. Run component inventory script:
   ```bash
   cd /33GOD
   PLATFORM_ROOT=/33GOD ./scripts/component-inventory.sh
   ```

2. Script evaluates each component across dimensions:
   - BMAD initialization (1 point)
   - Planning artifacts (2 points)
   - Architecture docs (2 points)
   - Test coverage (2 points)
   - Documentation (1 point)
   - Production readiness (1 point)

3. Assigns maturity levels:
   - 🔴 Early (0-1): No BMAD, experimental
   - 🟠 Emerging (2-4): BMAD init, planning started
   - 🟡 Developing (5-7): Active development, partial tests
   - 🟢 Mature (8-9): Production-ready, complete

4. Generates `docs/component-inventory.md` with:
   - Maturity matrix table
   - Component-by-component details
   - Recommendations by maturity level

5. Present summary with strategic insights

**Output**: Component inventory report with maturity roadmap

See [references/component-maturity-model.md](references/component-maturity-model.md) for scoring criteria.

---

### 3. Cross-Component Story Creation

**Trigger**: User describes a feature spanning multiple components

**Purpose**: Create platform-level story and delegate to component teams

**Steps**:
1. Use platform story template:
   ```bash
   cp assets/platform-story-template.md docs/stories/{story-name}.md
   ```

2. Populate story template with:
   - User story (who, what, why)
   - Component breakdown (specific tasks per component)
   - Integration requirements (how components interact)
   - Deployment strategy (rollout sequence)
   - Rollback plan (failure recovery)

3. Review story with user for completeness:
   - Are all affected components identified?
   - Are dependencies clear?
   - Is integration testing defined?

4. Delegate to components (next workflow)

**Example Story Types**:
- Schema evolution (event/API contract changes)
- New infrastructure (add shared service)
- Performance optimization (cross-component improvements)
- Security enhancement (unified auth, tracing)

See [references/cross-component-stories.md](references/cross-component-stories.md) for templates and examples.

---

### 4. Story Delegation to Components

**Trigger**: Platform story approved and ready for implementation

**Purpose**: Delegate component-specific tasks via Zellij coordination

**Steps**:
1. Determine delegation approach:
   - **Parallel**: Components can work independently
   - **Sequential**: Dependencies require ordering

2. Run delegation script:
   ```bash
   cd /33GOD
   ./scripts/delegate-story.sh \
     --story docs/stories/{story-name}.md \
     --components "comp1,comp2,comp3"
   ```

3. Script actions:
   - Creates task file in each component: `{component}/docs/delegated-task-{timestamp}.md`
   - Opens/switches to Zellij tabs (one per component)
   - Displays task context in each tab
   - Prompts next steps for component orchestrators

4. Each component tab shows:
   ```
   📋 Delegated task ready: docs/delegated-task-{timestamp}.md

   Run: /workflow-status to check current state
   Run: /create-story to create implementation story
   ```

5. Monitor progress:
   - Option A: Attach to Zellij session to watch real-time
   - Option B: Periodic status checks via `platform-status.sh`

6. Track completion in `docs/delegated-stories-tracking.md`

**Zellij Session Management**:
```bash
# Attach to platform session
zellij attach 33god-platform

# Switch between component tabs to monitor progress
# Tab names = component names (bloodbank, flume, imi, etc)
```

See [references/delegation-patterns.md](references/delegation-patterns.md) for detailed patterns.

---

### 5. Integration Map Generation

**Trigger**: User asks "/integration-map" or "show me component interactions"

**Purpose**: Visualize component architecture and data flows

**Steps**:
1. Run integration map script:
   ```bash
   cd /33GOD
   PLATFORM_ROOT=/33GOD ./scripts/integration-map.sh
   ```

2. Script analyzes:
   - docker-compose.yml (service dependencies)
   - package.json (workspace dependencies)
   - pyproject.toml (Python dependencies)
   - Component types (frontend, backend, event backbone, etc)

3. Generates `docs/integration-map.md` with:
   - Mermaid architecture diagram
   - Component registry (type, purpose, dependencies)
   - Event flow diagrams (if event backbone detected)
   - Integration patterns and guidelines

4. Present visualization to user

**When to Update**:
- New component added to platform
- Integration patterns change
- Architecture review requested
- Onboarding new team members

---

## iMi Cluster Detection

**Critical**: All 33GOD components follow iMi worktree conventions. Scripts detect components by looking for `.iMi/` directories (iMi cluster markers), NOT just any subdirectory.

### iMi Cluster Structure

```
/home/delorenj/code/33GOD/
├── bloodbank/           # iMi cluster
│   ├── .iMi/           # Cluster marker (presence = iMi managed)
│   │   ├── presence/
│   │   ├── links/
│   │   └── registry.toml
│   ├── bmad/           # BMAD at cluster level (NOT in worktrees)
│   ├── trunk-main/     # Trunk worktree
│   └── feat-xyz/       # Feature worktrees (NOT separate components)
```

**Key Points**:
- `.iMi/` directory identifies an iMi cluster (the actual component)
- Worktrees (`trunk-main`, `feat-*`, etc.) are NOT separate components
- BMAD lives at cluster level, shared by all worktrees
- Scripts scan for `.iMi/` to avoid treating worktrees as components

### Multi-Path Configuration

**Problem**: 33GOD components span multiple directory levels:
- Top-level projects: `/home/delorenj/code/ProjectName/`
- Nested 33GOD components: `/home/delorenj/code/33GOD/bloodbank/`

**Solution**: Multi-path search via `PLATFORM_SEARCH_ROOTS`

**Default Search Roots**:
```bash
SEARCH_ROOTS=(
    "/home/delorenj/code"
    "/home/delorenj/code/33GOD"
)
```

**Override with Environment Variable**:
```bash
PLATFORM_SEARCH_ROOTS="/path1:/path2:/path3" ./scripts/platform-status.sh
```

**How It Works**:
1. Scripts iterate through all search roots
2. Find directories containing `.iMi/` (iMi clusters)
3. Check if cluster has `bmad/` initialized
4. Aggregate results across all search roots

### Why This Matters

**Without iMi detection**:
- Scripts would treat every subdirectory as a component
- Worktrees (`feat-user-auth`, `fix-bug-123`) would appear as separate components
- Status reports would be polluted with non-components

**With iMi detection**:
- Only true iMi clusters (components) are detected
- Worktrees are correctly ignored
- Clean, accurate component inventory

---

## Automation Scripts

All scripts support **iMi cluster detection** and **multi-path configuration**.

### platform-status.sh
Aggregates BMAD status from all iMi cluster components
- Input: Multi-path search roots
- Output: `docs/platform-status.md`
- Usage: `./scripts/platform-status.sh`
- Override: `PLATFORM_SEARCH_ROOTS="/custom/path" ./scripts/platform-status.sh`

**Detection Logic**:
- Scans for `.iMi/` directories across all search roots
- Checks if cluster has `bmad/config.yaml`
- Reports components with BMAD workflows

### component-inventory.sh
Generates maturity matrix for all iMi clusters
- Input: Multi-path search roots
- Output: `docs/component-inventory.md`
- Scoring: 9-point maturity scale
- Usage: `./scripts/component-inventory.sh`

**Detection Logic**:
- Finds all iMi clusters (`.iMi/` present)
- Evaluates maturity regardless of BMAD status
- Assesses: BMAD init, planning, architecture, tests, docs, production config

### delegate-story.sh
Delegates tasks to component orchestrators via Zellij
- Input: Story file, component names (comma-separated)
- Output: Task files per component, Zellij tabs
- Usage: `./scripts/delegate-story.sh --story {file} --components "bloodbank,flume,imi"`

**Component Resolution**:
- Takes component names, searches for matching `.iMi/` clusters
- Searches across all search roots
- Reports error if component not found with search paths

### integration-map.sh
Generates Mermaid architecture diagram for iMi clusters
- Input: Multi-path search roots
- Output: `docs/integration-map.md` with diagrams
- Usage: `./scripts/integration-map.sh`

**Detection Logic**:
- Finds all iMi clusters
- Analyzes dependencies (docker-compose, package.json, pyproject.toml)
- Generates visual component interaction map

## Templates and Assets

### Platform Story Template
Location: `assets/platform-story-template.md`

Comprehensive template for cross-component user stories including:
- User story format
- Component breakdown
- Integration requirements
- Deployment strategy
- Rollback plan

Copy to `docs/stories/` when creating new platform story.

### Component Registry Template
Location: `assets/component-registry-template.md`

Template for documenting component inventory with:
- Maturity summary
- Production component details
- Integration points
- Technology stack
- Ownership information

Can be used as starting point for manual registry or reference for script output.

### Integration Map Template
Location: `assets/integration-map-template.mmd`

Mermaid diagram template showing:
- Component types (frontend, backend, event backbone, storage)
- Data flow connections
- Styling by component role

Reference when manually creating architecture diagrams.

## Reference Documentation

### hierarchical-bmad.md
Detailed explanation of two-level BMAD architecture:
- Meta-level vs component-level responsibilities
- Story propagation patterns (top-down)
- Status aggregation patterns (bottom-up)
- Phase alignment strategies
- Independence vs coordination guidelines

**When to read**: Understanding hierarchical BMAD structure, designing platform architecture, planning cross-component initiatives.

### delegation-patterns.md
Comprehensive guide to delegation workflows:
- Zellij-based coordination patterns
- File-based communication protocols
- Parallel vs sequential delegation
- Error handling and rollback
- Example end-to-end delegation

**When to read**: Delegating tasks to components, troubleshooting delegation issues, designing custom delegation workflows.

### component-maturity-model.md
Framework for assessing component production readiness:
- Maturity levels (Early, Emerging, Developing, Mature)
- Scoring criteria (9-point scale)
- Assessment workflows
- Improvement strategies by maturity level
- Cross-component maturity considerations

**When to read**: Assessing component readiness, planning maturity improvements, prioritizing platform investments.

### cross-component-stories.md
Guide to writing effective platform-level stories:
- Story template with complete example
- Story patterns (schema evolution, infrastructure, optimization)
- Component breakdown structure
- Integration requirements definition
- Anti-patterns to avoid

**When to read**: Creating cross-component stories, reviewing story quality, teaching story structure to teams.

## Best Practices

### When to Use Meta-Level Orchestration

**Use meta-level BMAD when**:
- Feature spans 2+ components
- Integration contracts need coordination
- Breaking changes require migration strategy
- Platform-wide standards or architecture
- Strategic roadmap planning

**Use component-level BMAD when**:
- Feature contained in single component
- No breaking changes to APIs/events
- Implementation details local to component
- Standard component development

### Component Independence

**Encourage independence**:
- Each component has its own BMAD workflow
- Components make local decisions autonomously
- Meta-level only coordinates integration points

**Coordinate when necessary**:
- API/event schema changes
- Breaking changes
- Cross-component features
- Shared infrastructure changes

### Status Aggregation Frequency

**Regular checks** (recommended):
- Run `platform-status.sh` weekly or per sprint
- Include in platform status meetings
- Track trends over time

**On-demand checks**:
- Before major releases
- When planning new initiatives
- During architecture reviews
- When assessing technical debt

### Delegation Communication

**Clear task boundaries**:
- Specify exactly what each component must implement
- Include acceptance criteria per component
- Document dependencies explicitly

**Provide full context**:
- Include platform story in delegation file
- Explain why the feature matters
- Link related component work

**Track completion**:
- Use `docs/delegated-stories-tracking.md`
- Update platform status after completion
- Verify integration end-to-end

## Troubleshooting

### Component Not Found in Status

**Symptom**: Script reports "No components with BMAD workflows found"

**Resolution**:
1. Ensure components have `bmad/` directory
2. Check for `docs/bmm-workflow-status.yaml` in each component
3. Run `/workflow-init` in component directories missing BMAD

### Zellij Tab Not Creating

**Symptom**: Delegation script fails to create tabs

**Resolution**:
1. Check if Zellij is installed: `which zellij`
2. Verify session exists: `zellij list-sessions`
3. Create session manually: `zellij --session 33god-platform`
4. Re-run delegation script

### Integration Test Failing

**Symptom**: Components work individually but integration fails

**Resolution**:
1. Check component-to-component dependencies in integration map
2. Verify API contracts match between producer/consumer
3. Review event schemas for compatibility
4. Check sequence of deployment (dependencies first)
5. Add integration test to catch issues early

### Status File Inconsistent

**Symptom**: Component status doesn't match project level

**Resolution**:
1. Read component `bmad/config.yaml` for project level
2. Validate workflow status requirements:
   - Level 0-1: Tech Spec required, PRD recommended
   - Level 2+: PRD required, Tech Spec optional
3. Update status file or config to align
4. Re-run `platform-status.sh`

## Integration with Existing Skills

### Use with bmad-orchestrator

The `bmad-orchestrator` skill handles component-level BMAD workflows. This skill (`33god-development-lifecycle`) coordinates at the platform level.

**Pattern**:
```
User request for cross-component feature
  → This skill: Create platform story, delegate tasks
    → bmad-orchestrator (in each component tab): Run /create-story, /dev-story
      → This skill: Aggregate status, verify integration
```

### Use with zellij-driver

The `zellij-driver` skill provides programmatic Zellij management. This skill uses Zellij for delegation coordination.

**Pattern**:
```
Delegation workflow
  → This skill: Identifies components and tasks
  → zellij-driver: Creates tabs, navigates, executes commands
  → This skill: Monitors completion via status files
```

### Use with 33god-system-expert

The `33god-system-expert` skill provides deep architectural knowledge. This skill uses that knowledge for platform planning.

**Pattern**:
```
Creating platform architecture
  → This skill: Needs component interaction patterns
  → 33god-system-expert: Provides architectural context
  → This skill: Generates integration map with accurate flows
```

## Example Scenarios

### Scenario 1: Add Distributed Tracing

**User Request**: "Add trace IDs across all components"

**Workflow**:
1. Run `/component-inventory` to see affected components
2. Create platform story using template
3. Populate story with:
   - Bloodbank: Add trace_id to event schema
   - Flume: Propagate traces in task execution
   - iMi: Log traces in CLI operations
4. Delegate: `./scripts/delegate-story.sh --story distributed-tracing.md --components "bloodbank,flume,imi"`
5. Monitor via Zellij or periodic status checks
6. Verify integration with end-to-end test

### Scenario 2: Assess Platform Readiness

**User Request**: "Are we ready for production?"

**Workflow**:
1. Run `/component-inventory` for maturity assessment
2. Review maturity scores:
   - Identify components below Developing level (score <5)
   - Check for missing production configurations
3. Run `/platform-status` for workflow completion
4. Run `/integration-map` to verify architecture
5. Create readiness report with gaps and recommendations
6. Prioritize maturity improvements for critical components

### Scenario 3: Onboard New Component

**User Request**: "We're adding a new notifications service"

**Workflow**:
1. Create component directory: `/33GOD/notifications`
2. Navigate to component: `cd /33GOD/notifications`
3. Initialize BMAD: `/workflow-init`
4. Run `/integration-map` to update architecture
5. Document integration points in platform architecture
6. Add component to registry
7. Run `/platform-status` to verify tracking

## Meta-Orchestrator Persona

This skill is designed for use by a **Director of Engineering** persona who:
- Owns platform-wide roadmap
- Coordinates across component teams
- Makes architectural decisions
- Manages cross-component dependencies
- Tracks component maturity and technical debt

**Decision Authority**:
- Component prioritization
- Breaking change approval
- Architecture evolution
- Platform-wide standards

**Delegation Model**:
- Defines platform-level requirements
- Delegates implementation to component teams
- Verifies integration quality
- Ensures platform coherence
