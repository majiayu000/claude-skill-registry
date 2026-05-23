---
name: when-managing-github-projects-use-github-project-management
description: Comprehensive GitHub project management with swarm-coordinated issue tracking, project board automation, and sprint planning. Coordinates planner, issue-tracker, and project-board-sync agents to automate issue triage, sprint planning, milestone tracking, and project board updates. Integrates with GitHub Projects v2 API for advanced automation, custom fields, and workflow orchestration. Use when managing development projects, coordinating team workflows, or automating project management tasks.
agents:
  - planner
  - issue-tracker
  - project-board-sync
  - coordinator
topology: star
mcp_tools:
  - mcp__claude-flow__swarm_init
  - mcp__claude-flow__agent_spawn
  - mcp__claude-flow__task_orchestrate
---

# GitHub Project Management Skill

## Overview

Automate and orchestrate GitHub project management workflows using intelligent agent coordination. This skill provides comprehensive project management capabilities including automated issue triage, sprint planning, milestone tracking, project board synchronization, and team coordination through GitHub Projects v2 integration.

## When to Use This Skill

Activate this skill when planning and executing development sprints, managing issue backlogs and triage queues, coordinating work across distributed teams, automating project board updates and status tracking, tracking milestones and release schedules, or establishing project management workflows for new teams.

Use for both small team projects (2-5 developers) and large-scale coordination (10+ team members), agile/scrum sprint management, kanban-style continuous delivery, or hybrid project management approaches.

## Agent Coordination Architecture

### Swarm Topology

Initialize a **star topology** with a central coordinator agent managing specialized agents for issue tracking, planning, and board synchronization. Star topology enables centralized control with efficient communication to specialized agents.

```bash
# Initialize star swarm for project management
npx claude-flow@alpha swarm init --topology star --max-agents 6 --strategy balanced
```

### Specialized Agent Roles

**Central Coordinator** (`coordinator`): Hub agent that orchestrates all project management activities. Makes prioritization decisions, coordinates between teams, and ensures consistency across project artifacts. Acts as project manager.

**Planner** (`planner`): Handles sprint planning, capacity estimation, and resource allocation. Creates sprint goals, breaks down epics into stories, estimates effort, and balances workload across team members.

**Issue Tracker** (`issue-tracker`): Automates issue triage, labeling, assignment, and lifecycle management. Monitors new issues, applies initial classification, routes to appropriate team members, and tracks resolution progress.

**Project Board Sync** (`project-board-sync`): Maintains GitHub Projects v2 boards, updates issue status, manages custom fields, and enforces workflow automation. Ensures boards accurately reflect current project state.

## Project Management Workflows (SOP)

### Workflow 1: Automated Issue Triage

Process incoming issues with intelligent classification and routing.

**Phase 1: Issue Ingestion**

**Step 1.1: Initialize Star Topology**

```bash
# Set up star swarm with coordinator hub
mcp__claude-flow__swarm_init topology=star maxAgents=6 strategy=balanced

# Spawn coordinator and specialists
mcp__claude-flow__agent_spawn type=coordinator name=coordinator
mcp__claude-flow__agent_spawn type=researcher name=issue-tracker
mcp__claude-flow__agent_spawn type=researcher name=planner
mcp__claude-flow__agent_spawn type=coordinator name=project-board-sync
```

**Step 1.2: Monitor New Issues**

Set up real-time monitoring for new issues:

```bash
# Subscribe to new issues
bash scripts/github-webhook.sh subscribe \
  --repo <owner/repo> \
  --events "issues" \
  --callback "scripts/process-new-issue.sh"
```

Or use MCP real-time subscription if Flow-Nexus available:

```bash
mcp__flow-nexus__realtime_subscribe table=issues event=INSERT
```

**Step 1.3: Fetch Issue Details**

When new issue created, fetch comprehensive context:

```bash
# Get issue details with comments and reactions
bash scripts/github-api.sh fetch-issue \
  --repo <owner/repo> \
  --issue <number> \
  --include-comments true
```

**Phase 2: Intelligent Classification**

**Step 2.1: Analyze Issue Content**

```plaintext
Task("Issue Tracker", "
  Analyze and classify new issue #<NUMBER>:

  1. Read issue body and comments from memory: github/issues/<NUMBER>
  2. Classify issue type: bug|feature|enhancement|documentation|question
  3. Determine severity: critical|high|medium|low
  4. Identify affected components using references/component-map.md
  5. Estimate complexity: simple|moderate|complex
  6. Check for duplicates using similarity search
  7. Extract key entities: affected files, error messages, user impact

  Use scripts/issue-classifier.sh for ML-based classification
  Store classification in memory: github/triage/<NUMBER>
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'issue triage'
", "issue-tracker")
```

**Step 2.2: Apply Labels and Metadata**

Based on classification, apply appropriate labels:

```bash
# Apply automated labels
bash scripts/github-api.sh add-labels \
  --repo <owner/repo> \
  --issue <number> \
  --labels "<type>,<severity>,<component>"

# Set custom fields in project board
bash scripts/project-api.sh set-field \
  --project <project-id> \
  --issue <number> \
  --field "Complexity" \
  --value "<complexity>"
```

**Step 2.3: Assign Team Member**

Route to appropriate team member based on expertise:

```plaintext
Task("Coordinator", "
  Assign issue #<NUMBER> to appropriate team member:

  1. Review team expertise map in references/team-skills.md
  2. Check current workload using scripts/team-capacity.sh
  3. Match issue requirements with team member skills
  4. Consider time zone and availability
  5. Assign issue via GitHub API

  Store assignment decision in memory: github/assignments/<NUMBER>
", "coordinator")
```

```bash
# Assign issue
bash scripts/github-api.sh assign-issue \
  --repo <owner/repo> \
  --issue <number> \
  --assignee <username>
```

**Phase 3: Priority and Milestone Assignment**

**Step 3.1: Determine Priority**

```plaintext
Task("Planner", "
  Prioritize issue #<NUMBER> within backlog:

  1. Assess business impact (user-facing, revenue, compliance)
  2. Evaluate technical risk (security, stability, data loss)
  3. Consider dependencies (blocking other work?)
  4. Review stakeholder input from issue comments
  5. Calculate priority score using references/priority-matrix.md

  Store priority in memory: github/priorities/<NUMBER>
", "planner")
```

**Step 3.2: Assign to Milestone**

Based on priority and current sprint capacity:

```bash
# Add to appropriate milestone
bash scripts/github-api.sh set-milestone \
  --repo <owner/repo> \
  --issue <number> \
  --milestone "<sprint-name>"
```

**Step 3.3: Update Project Board**

```plaintext
Task("Project Board Sync", "
  Add issue #<NUMBER> to project board:

  1. Determine appropriate project board (team, initiative, sprint)
  2. Add issue to board in 'Triage' column
  3. Set custom fields: Priority, Complexity, Sprint, Team
  4. Link related issues and PRs
  5. Add to sprint view if assigned to active sprint

  Use scripts/project-api.sh for Projects v2 API
  Store board update in memory: github/boards/<NUMBER>
", "project-board-sync")
```

### Workflow 2: Sprint Planning Automation

Plan and execute development sprints with agent coordination.

**Phase 1: Sprint Preparation**

**Step 1.1: Analyze Team Capacity**

```bash
# Calculate available capacity for next sprint
bash scripts/team-capacity.sh calculate \
  --team <team-name> \
  --start-date <YYYY-MM-DD> \
  --duration-days 14 \
  --include-pto true \
  --output references/sprint-capacity.json
```

**Step 1.2: Review Backlog**

```plaintext
Task("Planner", "
  Prepare sprint planning meeting:

  1. Fetch all backlog items using scripts/github-api.sh list-issues
  2. Filter by priority (high and critical first)
  3. Identify dependencies between issues
  4. Group related issues into themes
  5. Create preliminary sprint proposal based on capacity

  Reference references/sprint-capacity.json for team availability
  Store sprint proposal in memory: github/sprint/proposal
", "planner")
```

**Phase 2: Sprint Composition**

**Step 2.1: Create Sprint Milestone**

```bash
# Create new sprint milestone
bash scripts/github-api.sh create-milestone \
  --repo <owner/repo> \
  --title "Sprint <number>: <theme>" \
  --due-date <YYYY-MM-DD> \
  --description "Sprint goals: ..."
```

**Step 2.2: Assign Issues to Sprint**

```plaintext
Task("Coordinator", "
  Compose sprint backlog:

  1. Review planner's proposal from memory: github/sprint/proposal
  2. Validate capacity vs proposed work
  3. Ensure mix of feature work, bugs, and technical debt
  4. Balance workload across team members
  5. Assign issues to sprint milestone
  6. Create sprint goal document

  Use scripts/sprint-composer.sh for optimization
  Store final sprint composition in memory: github/sprint/final
", "coordinator")
```

**Step 2.3: Initialize Sprint Board**

```bash
# Create sprint project board
bash scripts/project-api.sh create-sprint-board \
  --title "Sprint <number>" \
  --template "references/sprint-board-template.json" \
  --issues-milestone "<milestone-name>"
```

**Phase 3: Sprint Execution Tracking**

**Step 3.1: Daily Status Updates**

```plaintext
Task("Project Board Sync", "
  Update sprint board daily:

  1. Sync issue statuses from PR activity
  2. Move completed issues to 'Done' column
  3. Flag blocked issues with 'blocked' label
  4. Update burndown chart data
  5. Identify issues without recent activity
  6. Generate daily standup summary

  Use scripts/sprint-tracker.sh for automation
  Store daily metrics in memory: github/sprint/daily/<DATE>
", "project-board-sync")
```

**Step 3.2: Generate Sprint Reports**

```bash
# Generate sprint health report
bash scripts/sprint-reporter.sh generate \
  --sprint "<milestone-name>" \
  --metrics "velocity,burndown,completion-rate,blocked-count" \
  --output "references/sprint-report-<DATE>.md"
```

**Step 3.3: Sprint Retrospective Data**

At sprint end, collect retrospective data:

```plaintext
Task("Planner", "
  Prepare sprint retrospective report:

  1. Calculate actual vs planned velocity
  2. Analyze completion rate by issue type
  3. Identify bottlenecks and blockers
  4. Collect cycle time metrics
  5. Generate improvement recommendations

  Use scripts/sprint-analytics.sh for metrics
  Store retrospective in memory: github/sprint/retro
", "planner")
```

### Workflow 3: Milestone and Release Tracking

Track progress toward major milestones and releases.

**Phase 1: Milestone Definition**

**Step 1.1: Create Milestone Structure**

```bash
# Create milestone with metadata
bash scripts/github-api.sh create-milestone \
  --repo <owner/repo> \
  --title "v2.0.0 Release" \
  --due-date <YYYY-MM-DD> \
  --description "$(cat references/v2-release-plan.md)"
```

**Step 1.2: Break Down Release Plan**

```plaintext
Task("Planner", "
  Decompose release plan into actionable items:

  1. Read release requirements from references/v2-release-plan.md
  2. Break down features into user stories
  3. Create issues for each story with acceptance criteria
  4. Estimate effort for each issue
  5. Assign to milestone
  6. Identify dependencies and critical path

  Use scripts/release-planner.sh for decomposition
  Store release breakdown in memory: github/releases/v2.0.0
", "planner")
```

**Phase 2: Progress Monitoring**

**Step 2.1: Track Milestone Progress**

```bash
# Generate milestone progress report
bash scripts/milestone-tracker.sh report \
  --milestone "v2.0.0 Release" \
  --include-burndown true \
  --output "references/milestone-progress.md"
```

**Step 2.2: Identify Risks**

```plaintext
Task("Coordinator", "
  Monitor release health and identify risks:

  1. Check milestone progress vs timeline
  2. Identify issues at risk of missing deadline
  3. Flag critical path issues with blockers
  4. Assess scope creep (new issues added to milestone)
  5. Generate risk mitigation recommendations

  Use scripts/risk-analyzer.sh
  Store risk assessment in memory: github/releases/risks
", "coordinator")
```

**Step 2.3: Stakeholder Communication**

```bash
# Generate stakeholder update
bash scripts/stakeholder-report.sh generate \
  --milestone "v2.0.0 Release" \
  --format "executive-summary" \
  --include-risks true \
  --output "references/stakeholder-update-<DATE>.md"
```

**Phase 3: Release Coordination**

**Step 3.1: Pre-Release Checklist**

```plaintext
Task("Project Board Sync", "
  Validate release readiness:

  1. Verify all milestone issues completed
  2. Check PR review status for milestone
  3. Validate CI/CD pipeline status
  4. Confirm documentation updates
  5. Check release notes completeness
  6. Verify deployment plan exists

  Use references/release-checklist.md
  Store readiness status in memory: github/releases/readiness
", "project-board-sync")
```

**Step 3.2: Create Release**

```bash
# Create GitHub release
bash scripts/github-api.sh create-release \
  --repo <owner/repo> \
  --tag "v2.0.0" \
  --name "Version 2.0.0" \
  --body-file "references/release-notes-v2.0.0.md" \
  --prerelease false
```

## Advanced Features

### Custom Field Automation

Configure GitHub Projects v2 custom fields with automated updates:

```bash
# Set up custom field automation
bash scripts/project-api.sh configure-fields \
  --project <project-id> \
  --config "references/custom-fields.json"
```

Custom field examples:
- **Complexity**: Auto-calculate from file changes
- **Priority Score**: Weighted algorithm based on impact/urgency
- **Cycle Time**: Auto-track time from start to completion
- **Review Status**: Sync with PR approval status
- **Team**: Auto-assign based on component ownership

### Integration with External Tools

Connect project management with external systems:

```bash
# Sync with Jira
bash scripts/external-sync.sh jira \
  --project <jira-project> \
  --github-repo <owner/repo> \
  --sync-direction "bidirectional"

# Push to Slack
bash scripts/notifications.sh slack \
  --webhook <slack-webhook> \
  --events "issue-created,pr-merged,milestone-completed"
```

### Analytics and Insights

Generate comprehensive project analytics:

```bash
# Run analytics suite
bash scripts/project-analytics.sh analyze \
  --repo <owner/repo> \
  --period "last-quarter" \
  --metrics "velocity,lead-time,cycle-time,throughput" \
  --visualize true \
  --output "references/analytics-report.html"
```

## MCP Tool Integration

### Task Orchestration

```bash
# Orchestrate complex project management workflow
mcp__claude-flow__task_orchestrate \
  task="Plan and initialize Sprint 42" \
  strategy=sequential \
  maxAgents=4 \
  priority=high
```

### Swarm Monitoring

```bash
# Monitor project management agent activity
mcp__claude-flow__swarm_status verbose=true

# Get agent performance metrics
mcp__claude-flow__agent_metrics metric=tasks
```

## Best Practices

**Consistent Labeling**: Use standardized label taxonomy across all repositories. Document label meanings in `references/label-taxonomy.md`.

**Automated Triage**: Run triage automation within 1 hour of issue creation to ensure responsive project management.

**Capacity Planning**: Always validate sprint capacity before committing work. Include buffer for unplanned work and meetings.

**Board Hygiene**: Run daily board sync to keep project boards accurate. Stale boards reduce team trust in project management.

**Retrospective Action**: Convert retrospective insights into concrete process improvements. Track improvement initiatives as issues.

**Clear Ownership**: Every issue should have exactly one assignee. Shared ownership leads to unclear accountability.

**Regular Communication**: Generate automated status reports for stakeholders. Transparency builds trust and reduces status meetings.

## Error Handling

**API Rate Limiting**: Implement caching and batching for GitHub API calls. Use GraphQL for complex queries to reduce request count.

**Conflict Resolution**: If issue assigned to multiple milestones, coordinator resolves based on priority and capacity constraints.

**Missing Data**: If issue lacks required classification data, flag for human review rather than making incorrect assumptions.

**Board Sync Failures**: Maintain local state cache to recover from transient API failures. Retry with exponential backoff.

## References

- `references/priority-matrix.md` - Issue prioritization framework
- `references/team-skills.md` - Team member expertise and capacity
- `references/component-map.md` - Repository component ownership
- `references/sprint-board-template.json` - Sprint board configuration
- `references/custom-fields.json` - Projects v2 custom field definitions
- `references/label-taxonomy.md` - Standardized label system
- `references/release-checklist.md` - Release readiness validation
- `scripts/github-api.sh` - GitHub REST/GraphQL API utilities
- `scripts/project-api.sh` - GitHub Projects v2 API integration
- `scripts/issue-classifier.sh` - ML-based issue classification
- `scripts/team-capacity.sh` - Team capacity calculation
- `scripts/sprint-tracker.sh` - Sprint progress tracking
- `scripts/milestone-tracker.sh` - Milestone monitoring
- `scripts/project-analytics.sh` - Project metrics and insights
