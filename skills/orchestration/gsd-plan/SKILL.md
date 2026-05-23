---
name: gsd-plan
description: Create a phased execution plan with fresh-context architecture
argument-hint: "<feature-description>"
tags: [orchestration, planning, gsd, context-engineering]
user-invocable: true
---

# GSD Plan -- Phased Execution Planning

Create a structured, phased plan inspired by GSD (Get Shit Done). Each phase runs in a fresh agent context to prevent context rot.

## What To Do

1. **Analyze the feature request**: Break into atomic phases completable in a single agent session.

2. **Create phased plan** using TodoWrite with clear inputs/outputs/verification per phase.

3. **Write plan files**:
   ```
   .planning/
     PROJECT.md      -- Feature vision and scope
     REQUIREMENTS.md -- Acceptance criteria
     ROADMAP.md      -- Phased plan with waves
     STATE.md        -- Progress and decisions
   ```

4. **Plan structure** (XML-optimized for Claude):
   ```xml
   <phase number="1" name="Data Models">
     <task type="auto">
       <name>Create CandidateProfile model</name>
       <files>src/backend/Models/CandidateProfile.cs</files>
       <action>Create domain model with GDPR compliance</action>
       <verify>dotnet build succeeds</verify>
       <done>Model compiles with all required properties</done>
     </task>
   </phase>
   ```

5. **Wave parallelism**: Independent tasks in the same wave run in parallel via Task tool.

## Context Rot Prevention
- Each phase executes in a FRESH agent context (via Task tool)
- Orchestrator stays lean -- only tracks STATE.md
- Main context stays under 40% utilization

## Arguments
- `<feature-description>`: What to build (natural language)