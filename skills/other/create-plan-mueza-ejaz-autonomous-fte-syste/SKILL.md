---
name: create-plan
description: Create structured Plan.md files for complex multi-step tasks. Analyzes task requirements, breaks them down into actionable steps with estimates, identifies dependencies between steps, flags steps requiring human approval, and generates comprehensive plans with success criteria. Use when task requires planning, user asks to "create a plan", "plan this task", "break this down", "what are the steps", or when task has multiple components or dependencies.
user-invocable: true
allowed-tools: [Read, Write, Glob, Grep]
---

# Create Plan Skill

Generates structured **Plan.md** files for complex tasks requiring multi-step reasoning and execution.

---

## Core Responsibilities

1. Analyze task requirements and understand objectives
2. Break down complex tasks into 3-7 actionable steps
3. Identify dependencies between steps
4. Flag steps requiring human approval
5. Provide realistic time/effort estimates
6. Define measurable success criteria

---

## When This Skill Activates

**Trigger phrases:**
- "create a plan"
- "plan this task"
- "break this down"
- "what are the steps"
- "generate plan.md"
- "how should I approach this"

**Auto-activates when:**
- Task has 3+ distinct components
- Task requires coordination of multiple actions
- User explicitly requests planning
- Task involves external dependencies or approval stages

---

## Step-by-Step Workflow

### Phase 1: Task Analysis

1. **Read Source Task**
   - Locate task file in `Vault/Needs_Action`
   - Read full description and context
   - Identify task type and desired outcome

2. **Understand Requirements**
   - What is the goal?
   - Who are the stakeholders?
   - What constraints exist (time, budget, approval)?
   - What resources are available?

3. **Check Business Context**
   - Read `Vault/Business_Goals.md` for alignment
   - Read `Vault/Company_Handbook.md` for guidelines
   - Verify task supports business objectives

4. **Assess Complexity**
   - Simple (1-2 steps): May not need full plan
   - Moderate (3-5 steps): Standard plan
   - Complex (6+ steps): Detailed plan with phases

See [best practices](./reference/best-practices.md) for when to create plans.

---

### Phase 2: Plan Generation

1. **Define Clear Objective**
   - Write one-sentence objective statement
   - Be specific and measurable
   - Example: "Send project proposal to Client A with pricing and timeline by Friday"

2. **Identify Major Steps (3-7 steps)**
   - Each step should be actionable and atomic
   - Use action verbs (Research, Draft, Send, Review, etc.)
   - Keep steps focused and clear

3. **Add Step Details**
   For each step include:
   - **Description**: What needs to be done
   - **Estimate**: Time/effort (5m, 30m, 2h, etc.)
   - **Dependencies**: What must complete first
   - **Approval**: Does this need human approval? (yes/no)
   - **Resources**: Tools/files/information needed

4. **Identify Dependencies**
   - Sequential: Steps that must happen in order
   - Parallel: Steps that can run simultaneously
   - External: Dependencies on things outside our control

5. **Flag Approval Requirements**
   Mark steps that require approval with `[REQUIRES APPROVAL]` tag:
   - External communications (emails, social posts)
   - Payments or financial actions
   - Public-facing content
   - Data deletion
   - Actions requiring human judgment

6. **Define Success Criteria**
   - How will we know the task is complete?
   - What are the quality standards?
   - What deliverables must exist?

See [best practices](./reference/best-practices.md) for detailed guidance.

---

### Phase 3: Plan Creation

1. **Generate Plan Filename**
   - Format: `PLAN_[task-description]_[date].md`
   - Example: `PLAN_ClientA_Proposal_2026-01-11.md`
   - Keep filename descriptive but < 80 characters

2. **Create Plan File**
   - Save to `Vault/Plans` folder
   - Use [standard template](./reference/plan-template.md)
   - Include all required sections with proper markdown

3. **Required Sections**
   - **YAML Frontmatter**: Metadata (created, status, priority, estimated_duration)
   - **Objective**: Clear goal statement
   - **Background**: Context and rationale (optional but recommended)
   - **Steps**: Numbered checklist with details
   - **Dependencies**: Relationships between steps
   - **Approval Requirements**: Steps needing approval
   - **Success Criteria**: Measurable completion indicators
   - **Notes**: Additional context (optional)
   - **Execution Log**: Empty placeholder for updates

4. **Write Clear Step Descriptions**
   Good example:
   ```markdown
   - [ ] Draft proposal with pricing ($2,500), timeline (3 weeks), deliverables
         Est: 1h | Depends on: Step 1 | Approval: no | Resources: pricing-template.md
   ```

   See [examples](./reference/plan-examples.md) for more patterns.

---

### Phase 4: Plan Finalization

1. **Review for Completeness**
   - [ ] All steps are actionable
   - [ ] Dependencies are clear and non-circular
   - [ ] Estimates are reasonable
   - [ ] Approval needs are flagged
   - [ ] Success criteria are measurable

2. **Check for Missing Steps**
   Common forgotten steps:
   - Testing/validation
   - Getting approval
   - Notifying stakeholders
   - Documentation
   - Follow-up actions

3. **Assign Priority**
   - **Urgent**: Complete today, blocking other work
   - **High**: Important, 2-3 days
   - **Normal**: Standard, within week
   - **Low**: Nice to have, no deadline

4. **Save & Update Dashboard**
   - Save plan to `Vault/Plans` folder
   - Log creation to `Vault/Dashboard.md` with timestamp, task name, priority
   - Provide summary to user (steps, approvals, duration)

---

## Plan Template Structure

Use the [full template](./reference/plan-template.md) for complete details.

**Minimal structure:**

```markdown
---
created: [timestamp]
status: pending_approval | in_progress | completed | blocked
priority: low | normal | high | urgent
task_source: Vault/Needs_Action/[source-file].md
estimated_duration: [e.g., "30 minutes", "3 hours"]
---

## Objective
[One clear sentence]

## Steps
- [ ] **Step 1:** [Action description]
      Est: [time] | Depends on: [none/step] | Approval: [yes/no]
      [REQUIRES APPROVAL] [if applicable]

[... more steps ...]

## Dependencies
[Sequential, parallel, external]

## Approval Requirements
[List steps requiring approval and why]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

---
## Execution Log
[Updates as work progresses]
```

---

## Integration with Other Skills

**Workflow:**
1. `create-plan` generates Plan.md
2. `process-tasks` reads and executes steps
3. `handle-approval` manages approval for flagged steps
4. Action skills (`process-emails`, `post-to-linkedin`) execute specific actions
5. Completed plans move to `Vault/Done`

---

## Reference Files

**Progressive disclosure - load on demand:**

1. **[plan-template.md](./reference/plan-template.md)**
   - Complete template with all sections
   - Field descriptions
   - Minimal plan template for simple tasks

2. **[plan-examples.md](./reference/plan-examples.md)**
   - Email response plan
   - Complex project plan
   - Research & report plan
   - Multi-phase project
   - Minimal quick task plan

3. **[best-practices.md](./reference/best-practices.md)**
   - When to create plans (complexity guidelines)
   - Writing effective steps and objectives
   - Time estimation guidelines
   - Success criteria best practices
   - Common mistakes to avoid

---

## Dashboard Logging Format

```markdown
### [Timestamp] - Plan Created

**Plan:** [Task name]
- File: Vault/Plans/PLAN_[name]_[date].md
- Priority: [priority]
- Total Steps: [number]
- Requires Approval: [yes/no, which steps]
- Estimated Duration: [time]
- Status: Ready for execution
```

---

## Success Criteria

This skill works correctly when:

✅ Plans clearly decompose complex tasks
✅ All approval needs identified upfront
✅ Steps have realistic estimates
✅ Dependencies are explicit and non-circular
✅ Success criteria are measurable
✅ Plans integrate smoothly with process-tasks skill
✅ Dashboard logs all plan creations

---

*Skill Version: 2.1 (Updated for Vault structure)*
*Last Updated: 2026-01-11*
*Branch: feat/silver-core-workflows*