---
name: ralph-prompt-builder
description: Master orchestrator for generating Ralph Wiggum-compatible prompts. Analyzes task requirements and routes to appropriate generator (single-task, multi-task, project, or research). Use when you need to create any Ralph loop prompt and want automatic selection of the right generator.
---

# Ralph Prompt Builder (Master Orchestrator)

## Overview

Master skill for generating prompts optimized for the Ralph Wiggum autonomous loop technique. This orchestrator analyzes your task description and routes to the appropriate specialized generator:

| Task Type | Generator | Best For |
|-----------|-----------|----------|
| Single focused task | `ralph-prompt-single-task` | Bug fixes, single features, refactoring |
| Multiple related tasks | `ralph-prompt-multi-task` | CRUD, multi-step features, migrations |
| Complete project | `ralph-prompt-project` | Greenfield apps, libraries, tools |
| Research/Analysis | `ralph-prompt-research` | Audits, planning, investigations |

## Quick Start

**Generate any Ralph prompt:**
```
Use ralph-prompt-builder to create a prompt for: [describe your task]
```

**Example:**
```
Use ralph-prompt-builder to create a prompt for: Implementing user authentication with JWT for our Express API
```

The skill will:
1. Classify your task
2. Route to the appropriate generator
3. Guide you through required inputs
4. Output a ready-to-use Ralph prompt

## Task Classification

### How Tasks Are Classified

| Indicators | Classification | Generator |
|------------|----------------|-----------|
| Fix, repair, single change, one module | Single Task | `ralph-prompt-single-task` |
| Multiple features, CRUD, several endpoints | Multi-Task | `ralph-prompt-multi-task` |
| Build from scratch, new app, create tool | Project | `ralph-prompt-project` |
| Analyze, audit, compare, plan, investigate | Research | `ralph-prompt-research` |

### Classification Questions

To classify your task, consider:

1. **Is this creating something new from scratch or modifying existing code?**
   - New from scratch → Project or Multi-Task
   - Modifying existing → Single Task or Multi-Task

2. **How many distinct deliverables?**
   - One deliverable → Single Task
   - 2-5 related deliverables → Multi-Task
   - Complete application/tool → Project
   - Analysis document → Research

3. **Does it involve investigation before action?**
   - Yes, research required → Research
   - No, implementation focus → Single/Multi/Project

4. **What's the completion criteria?**
   - Tests pass → Single Task
   - Multiple features working → Multi-Task
   - Complete app running → Project
   - Document produced → Research

## Classification Examples

### Single Task Examples
- "Fix the race condition in token refresh"
- "Add pagination to the users endpoint"
- "Refactor database queries to use async/await"
- "Write tests for the auth module"
- "Optimize the image upload function"

### Multi-Task Examples
- "Implement CRUD for Products resource"
- "Add login, signup, logout, and password reset"
- "Set up CI/CD pipeline with lint, test, build, deploy"
- "Add validation, error handling, and logging to API"
- "Create user, profile, and settings endpoints"

### Project Examples
- "Build a REST API for a todo list application"
- "Create a CLI tool for database migrations"
- "Build a URL shortener service"
- "Create a markdown documentation generator"
- "Build an authentication microservice"

### Research Examples
- "Analyze the codebase for security vulnerabilities"
- "Compare React vs Vue vs Svelte for our needs"
- "Create a migration plan from MongoDB to PostgreSQL"
- "Audit dependencies for outdated packages"
- "Document the current API architecture"

## Workflow

### Step 1: Describe Your Task

Provide a description including:
- What needs to be done
- What technology/context
- Any specific requirements
- Desired outcome

**Template:**
```
Task: [What you want to accomplish]
Context: [Relevant background - tech stack, existing code, etc.]
Requirements: [Specific requirements or constraints]
Outcome: [What success looks like]
```

### Step 2: Review Classification

The orchestrator will classify your task and explain why:

```
CLASSIFICATION: [Task Type]
REASONING: [Why this classification]
GENERATOR: ralph-prompt-[type]

Does this classification look correct? If not, specify your preferred type.
```

### Step 3: Provide Generator Inputs

Each generator requires specific inputs:

**Single Task:**
- Task description
- Success criteria (how to verify)
- Completion promise text

**Multi-Task:**
- List of tasks
- Dependencies between tasks
- Final completion promise

**Project:**
- Project description
- Tech stack
- Feature list
- Completion promise

**Research:**
- Research objective
- Scope (in/out)
- Deliverable format
- Completion promise

### Step 4: Generate & Review

The appropriate generator creates the prompt. Review and customize:

1. Verify requirements are complete
2. Check verification commands are correct
3. Confirm completion criteria match your needs
4. Adjust max-iterations recommendation

### Step 5: Execute with Ralph

```bash
/ralph-wiggum:ralph-loop "[generated prompt]" --completion-promise "[YOUR_PROMISE]" --max-iterations [recommended]
```

## Generator Summaries

### ralph-prompt-single-task

**Purpose:** Focused tasks with clear success criteria

**Structure:**
1. Task title and objective
2. Context
3. Requirements
4. Success criteria (checkboxes)
5. Verification steps with commands
6. TDD approach
7. Completion conditions
8. If stuck guidance

**Best practices:**
- Include actual test commands
- Make criteria binary (pass/fail)
- Include TDD loop

**Recommended iterations:** 15-35

---

### ralph-prompt-multi-task

**Purpose:** Multiple related tasks organized in phases

**Structure:**
1. Task inventory table
2. Phase breakdown (Foundation → Core → Enhancement → Validation)
3. Per-phase tasks with deliverables
4. Phase checkpoints
5. Progress tracking
6. Final verification

**Best practices:**
- Group tasks into logical phases
- Clear dependencies
- Document checkpoints

**Recommended iterations:** 35-100

---

### ralph-prompt-project

**Purpose:** Complete projects from scratch

**Structure:**
1. Project vision and specs
2. Six phases:
   - Phase 0: Setup
   - Phase 1: Architecture
   - Phase 2: Core
   - Phase 3: Features
   - Phase 4: Testing
   - Phase 5: Documentation
3. Per-phase tasks and deliverables
4. Final verification
5. Progress tracking

**Best practices:**
- Define non-goals explicitly
- Complete all phases in order
- Don't skip testing/documentation

**Recommended iterations:** 60-200

---

### ralph-prompt-research

**Purpose:** Analysis, audits, planning, investigations

**Structure:**
1. Research objective and scope
2. Five phases:
   - Phase 1: Discovery
   - Phase 2: Analysis
   - Phase 3: Synthesis
   - Phase 4: Recommendations
   - Phase 5: Documentation
3. Deliverables at each phase
4. Evidence-based conclusions

**Best practices:**
- Define scope boundaries clearly
- Create artifacts as you go
- Support conclusions with evidence

**Recommended iterations:** 30-100

## Common Patterns

### Choosing a Completion Promise

**Good promises are:**
- Specific to the task
- Verifiable (you can check if it's true)
- Action-oriented

**Examples:**
| Task Type | Good Promise | Why |
|-----------|--------------|-----|
| Bug fix | `AUTH_FIX_COMPLETE` | Specific to what was fixed |
| CRUD | `PRODUCT_CRUD_DONE` | Names the resource |
| Project | `TODO_API_V1_COMPLETE` | Identifies the project |
| Research | `SECURITY_AUDIT_DELIVERED` | References deliverable |

### The Ralph Philosophy

The Ralph Wiggum technique is built on a key insight: **failures are deterministic and fixable**.

- **Deterministically bad**: When prompts fail, they fail in predictable ways
- **Fixable through iteration**: Each failure provides data to improve
- **Prompt tuning > tool changing**: Fix failures by improving the prompt, not switching approaches

This means: Don't fear failures. They're expected and correctable. The loop will iterate until success.

### Setting Max Iterations

Base recommendations by complexity:

| Complexity | Single Task | Multi-Task | Project | Research |
|------------|-------------|------------|---------|----------|
| Simple | 15 | 35 | 60 | 30 |
| Medium | 25 | 50 | 100 | 50 |
| Complex | 35 | 70 | 150 | 80 |
| Very Complex | - | 100 | 200 | 100 |

**Adjust based on:**
- Familiarity with codebase (-20%)
- External dependencies (+30%)
- Unclear requirements (+50%)
- Comprehensive testing needed (+25%)

### Splitting Large Tasks

If task feels too large, consider splitting:

**Project → Multiple Projects:**
```
Instead of: "Build complete e-commerce platform"
Split into:
1. Project: User authentication service
2. Project: Product catalog API
3. Project: Shopping cart service
4. Project: Order processing service
```

**Multi-Task → Separate Multi-Tasks:**
```
Instead of: "Build full admin dashboard"
Split into:
1. Multi-Task: User management (CRUD + roles)
2. Multi-Task: Analytics dashboard
3. Multi-Task: Settings panel
```

## Troubleshooting

### Task Won't Complete

**Symptoms:** Hitting max iterations without completion

**Causes and fixes:**
1. **Scope too large** → Split into smaller tasks
2. **Unclear criteria** → Make success criteria more specific
3. **External dependencies** → Document or mock dependencies
4. **Infinite tests** → Check for flaky tests

### Wrong Generator Selected

**Fix:** Specify the generator explicitly:
```
Use ralph-prompt-single-task (not multi-task) for: [task]
```

### Prompt Too Vague

**Fix:** Ensure your input includes:
- Specific files/modules affected
- Actual test commands
- Concrete success criteria
- Technology context

## Integration with Ralph Loop

After generating a prompt:

```bash
# Copy the generated prompt to a file or use directly
/ralph-wiggum:ralph-loop "[YOUR_GENERATED_PROMPT]" \
  --completion-promise "YOUR_PROMISE" \
  --max-iterations 50

# Monitor progress
head -10 .claude/ralph-loop.local.md

# Cancel if needed
/ralph-wiggum:cancel-ralph
```

## Best Practices

### DO:
- Start with the right generator for your task type
- Provide complete context and requirements
- Include specific verification commands
- Set appropriate max-iterations for complexity
- Review generated prompts before running

### DON'T:
- Use vague task descriptions
- Skip the classification step
- Ignore the "If Stuck" guidance in generated prompts
- Set max-iterations too low (iterations are normal)
- Expect first-try perfection—Ralph embraces iteration

## Quick Reference

### Task Type Decision Tree

```
Is this research/analysis/planning?
├─ YES → ralph-prompt-research
└─ NO → Is this building a complete app from scratch?
         ├─ YES → ralph-prompt-project
         └─ NO → Are there multiple related deliverables?
                  ├─ YES → ralph-prompt-multi-task
                  └─ NO → ralph-prompt-single-task
```

### Input Checklist

Before generating, have ready:
- [ ] Clear task description
- [ ] Technology context (language, framework)
- [ ] Success criteria (how to verify done)
- [ ] Completion promise text
- [ ] Any specific requirements

### Output Checklist

Before running the prompt:
- [ ] All requirements captured
- [ ] Verification commands are correct
- [ ] Success criteria are binary (pass/fail)
- [ ] TDD/iteration approach included
- [ ] "If Stuck" guidance provided
- [ ] Max iterations set appropriately

---

**Specialized Generators:**
- `ralph-prompt-single-task` - Single focused implementations
- `ralph-prompt-multi-task` - Multiple related tasks
- `ralph-prompt-project` - Complete projects
- `ralph-prompt-research` - Analysis and planning

**Ralph Loop Commands:**
- `/ralph-wiggum:ralph-loop` - Start a loop
- `/ralph-wiggum:cancel-ralph` - Cancel active loop
- `/ralph-wiggum:help` - Get help
