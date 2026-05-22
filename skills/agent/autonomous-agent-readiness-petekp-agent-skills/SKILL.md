---
name: autonomous-agent-readiness
description: Assess a codebase's readiness for autonomous agent development and provide tailored recommendations. Use when asked to evaluate how well a project supports unattended agent execution, assess development practices for agent autonomy, audit infrastructure for agent reliability, or improve a codebase for autonomous agent workflows. Triggers on requests like "assess this project for agent readiness", "how autonomous-ready is this codebase", "evaluate agent infrastructure", or "improve development practices for agents".
---

# Autonomous Agent Readiness Assessment

Evaluate a codebase against proven patterns for autonomous agent execution and provide tailored recommendations.

## Core Philosophy

Most agent failures are system design failures, not model failures. An agent that requires human approval at every step or depends on a developer's laptop being open is not autonomous. Autonomy is an infrastructure decision.

## Assessment Workflow

### Phase 1: Discovery

Gather information about the project's current state:

1. **Examine project structure**
   - Look for CI/CD configuration (`.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`)
   - Check for containerization (`Dockerfile`, `docker-compose.yml`, `devcontainer.json`)
   - Identify test infrastructure (`tests/`, `__tests__/`, test config files)
   - Find environment management (`.env.example`, `requirements.txt`, `package.json`)

2. **Review development workflow**
   - Read contributing guidelines, README, or developer docs
   - Check for sandbox/isolation patterns
   - Look for database setup scripts or fixtures
   - Identify how dependencies are managed

3. **Assess current automation**
   - Review existing CI/CD pipelines
   - Check for automated testing patterns
   - Look for environment provisioning scripts
   - Identify cleanup/teardown procedures

### Phase 2: Evaluate Against Principles

Score the project (0-3) on each dimension. See `references/assessment-criteria.md` for detailed rubrics.

| Dimension | What to Look For |
|-----------|------------------|
| Sandbox Isolation | Ephemeral environments, container support, clean state per run |
| Database Independence | Local DB setup, migrations in code, no external DB dependencies |
| Environment Reproducibility | Explicit dependencies, no hidden state, deterministic setup |
| Session Independence | Remote execution capability, no user session dependencies |
| Outcome-Oriented Design | Clear acceptance criteria, minimal procedural coupling |
| Direct Interfaces | CLI-first tools, OS primitives, minimal abstraction layers |
| Minimal Framework Overhead | Simple interfaces, no heavy orchestration, composable CLI tools |
| Explicit State | Workspace directories, file-based artifacts, inspectable logs |
| Benchmarking | Measurable quality criteria, automated verification |
| Cost Awareness | Resource limits, usage tracking, explicit provisioning |
| Verifiable Output | Automated validation, deterministic results, clear exit codes |
| Infrastructure-Bounded Permissions | System-enforced constraints, least-privilege, no runtime prompts |

### Phase 3: Generate Recommendations

For each dimension scoring below 2, provide:

1. **Current state**: What exists today
2. **Gap**: What's missing for autonomous execution
3. **Recommendation**: Specific, actionable improvement
4. **Priority**: High/Medium/Low based on impact and effort

Tailor recommendations to the project's:
- Technology stack
- Team size and workflow
- Existing infrastructure
- Deployment targets

## Output Format

```markdown
# Autonomous Agent Readiness Assessment

## Project: [name]
## Assessment Date: [date]

## Executive Summary

[1-2 paragraphs summarizing overall readiness and top priorities]

**Overall Readiness Score: X/36** (sum of dimension scores)

## Dimension Scores

| Dimension | Score | Status |
|-----------|-------|--------|
| Sandbox Isolation | X/3 | [emoji] |
| Database Independence | X/3 | [emoji] |
| ... | ... | ... |

Status: 0-1 = needs work, 2 = adequate, 3 = strong

## Detailed Findings

### [Dimension Name] (X/3)

**Current State:**
[What exists]

**Gap:**
[What's missing]

**Recommendation:**
[Specific action]

**Priority:** [High/Medium/Low]

[Repeat for each dimension]

## Prioritized Action Plan

### Immediate (This Week)
1. [Highest impact, lowest effort items]

### Short-term (This Month)
1. [Important foundational changes]

### Medium-term (This Quarter)
1. [Larger infrastructure investments]

## Quick Wins

[2-3 changes that can be made today with minimal effort]
```

## Key Principles Reference

### Sandbox Everything
Every agent run executes in its own ephemeral, isolated, disposable environment. Clean environment, writable filesystem, command execution, scoped network access. Environment destroyed after verified output.

### No External Databases
Agents create their own databases inside the sandbox. Install packages on demand, spin up DBs locally, run migrations, seed data explicitly, tear down at end. Reproducible runs without shared state.

### Environment Garbage Is Real
Long-lived environments accumulate stray files, half-installed packages, cached state, orphaned processes. Fresh environments surface correctness; persistent environments obscure it.

### Run Independently of User Sessions
Agent loop decoupled from browser tabs, terminal sessions, developer machines. Start task, close laptop, return to completed artifacts. Control via wall-clock limits, resource limits, automatic cleanup.

### Define Outcomes, Not Procedures
Avoid step-by-step plans and tool-level micromanagement. Define desired outcome, acceptance criteria, constraints. Planning and execution belong to the agent.

### Direct, Low-Level Interfaces
Direct access to command execution, persistent files, network requests. OS primitives over abstraction layers. CLI-first systems are easier to debug and more capable than they look.

### Persist State Explicitly
Writable workspace directory for intermediate results, logs, partial outputs, planning artifacts. Files are inspectable, deterministic, and enable post-run analysis.

### Benchmarks Early
Introduce benchmarks as early as possible. Representative and repeatable metrics for quality. Even crude benchmarks beat none.

### Minimal Framework Overhead
Most real-world agent workflows reduce to running commands, reading/writing files, and making network calls. CLI-first systems are easier to reason about, debug, and more capable than they look. When an abstraction layer is more complex than the task, it becomes the bottleneck.

### Plan for Cost
Provision token usage, allocate compute explicitly, enforce limits by system. Autonomy shifts where costs appear, doesn't remove them.

### Verifiable Output
Output must be verifiable without human review. Automated validation, deterministic results, clear success/failure exit codes. If quality cannot be measured, it cannot be trusted in autonomous operation.

### Infrastructure-Bounded Permissions
Permissions are constrained by the environment, not by prompts or runtime decisions. Explicit capability grants, sandbox restrictions on dangerous operations, least-privilege by default. No runtime permission prompts required.
