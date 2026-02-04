---
activation_code: PRD_TO_TASKS_V1
phase: 5
prerequisites: []
outputs: 
  - .taskmaster/tasks/tasks.json
  - .signals/phase1-start.json
description: |
  Generates production-grade TaskMaster tasks.json from Product Requirements Documents (PRD).
  Activates via codeword [ACTIVATE:PRD_TO_TASKS_V1] injected by hooks when PRD is detected.
  Always generates integration tasks (Tasks #N-2, #N-1, #N) for component integration testing,
  E2E workflows, and production readiness validation.
  
  Activation trigger: [ACTIVATE:PRD_TO_TASKS_V1]
---

# PRD-to-Tasks Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:PRD_TO_TASKS_V1]
```

This occurs when:
- User mentions "PRD", "generate tasks", or "parse requirements"
- PRD.md or requirements.md exists in context
- Phase 2 is complete and user wants to start development

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in a dedicated worktree `phase-5-task-1`:

```bash
# Before skill activation:
./lib/worktree-manager.sh create 5 1
cd ./worktrees/phase-5-task-1

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# Skill execution with worktree validation
```

### Worktree Validation Steps
1. **Pre-execution**: Verify worktree isolation before any operations
2. **During execution**: All file operations confined to worktree
3. **Post-execution**: Merge changes to main branch and cleanup

## Execution Steps (MANDATORY)

**CRITICAL:** This skill generates MASTER TASKS ONLY (no subtasks). DO NOT call `task-master parse-prd` or generate subtasks. Subtasks will be added later by task-master expand in Phase 5.

**Goal:** Create granular master tasks (as many as needed for the project) to keep LLM context small during development.

When this skill activates, follow these steps in order:

### Step 1: Read PRD with large-file-reader
```bash
# ALWAYS use large-file-reader - DO NOT use Read tool
echo "📖 Reading PRD with large-file-reader..."
./lib/large-file-reader.sh docs/PRD.md
```

**DO NOT** store output in variable - just run the command so PRD content enters your context.

### Step 2: Analyze PRD Structure (AI Analysis)

**CRITICAL: Check for Explicit Task Breakdown FIRST**

Before analyzing features, search for explicit task breakdowns in the PRD:

**Step 2a: Look for Explicit Task Sections**

Search for sections like:
- "Task Decomposition"
- "Task Breakdown"
- "Implementation Tasks"
- "Development Tasks"
- Section 7, Section 7.1, or Appendix with task lists

**If found:**
- ✅ Use the PRD's explicit task list as the **source of truth**
- ✅ Extract ALL tasks defined (even if 50-70 tasks)
- ✅ Preserve task IDs, titles, descriptions from PRD
- ✅ Maintain PRD's category structure
- ✅ Capture complexity classifications if provided
- ✅ Map dependencies explicitly stated

**Example:** If PRD has:
```
7.1 Task Decomposition (67 tasks across 13 categories)
  Category 1: Foundation & Infrastructure (tasks 1-8)
    Task 1: Docker Environment Setup
    Task 2: CI/CD Pipeline Configuration
    ...
  Category 2: Parent GraphRAG Server (tasks 9-13)
    Task 9: Neo4j Server Configuration
    ...
```

→ Generate 67 master tasks matching this structure

**Step 2b: If NO Explicit Task Breakdown Found**

Fall back to feature-based analysis:

1. **Feature Requirements** (typically Section 3):
   - List each major feature/capability
   - Extract acceptance criteria per feature
   - Note architecture components affected

2. **Non-Functional Requirements**:
   - Performance requirements
   - Security requirements
   - Scalability targets

3. **Integration Requirements** (typically Section 4):
   - Component integration points
   - E2E testing requirements
   - Production validation criteria

4. **Dependencies**:
   - What must be built before what
   - Shared infrastructure needs
   - External service integrations

**Step 2c: Extract Performance Targets**

Look for explicit performance targets:
- Response time requirements (e.g., "<10s UI response p95")
- Generation time limits (e.g., "<15min config generation")
- Query performance (e.g., "<10s GraphRAG queries")
- Throughput requirements

These will be used in performance testing tasks.

### Step 3: Generate Master Tasks (DIRECT AI GENERATION)

**DO NOT call task-master parse-prd!** Instead, YOU will create the master tasks directly.

#### 3a. Task Generation Strategy

**Strategy A: PRD Has Explicit Task Breakdown (PREFERRED)**

If Step 2a found explicit tasks (e.g., Section 7.1 with 67 tasks):

1. **Extract ALL tasks from PRD** - Do not compress or consolidate
2. **Preserve PRD task structure** - Maintain categories, IDs, titles
3. **Map 1:1 where possible** - PRD Task 1 → Master Task 1
4. **Add TaskMaster required fields** - id, title, description, status
5. **Add optional fields** - priority, dependencies (NO subtasks field yet)
6. **Capture PRD metadata** - Add `prd_category`, `prd_task_range` to description

**Example mapping:**
```
PRD Section 7.1:
  Category 1: Foundation & Infrastructure (tasks 1-8)
    Task 1: Docker Environment Setup
    Task 2: CI/CD Pipeline Configuration
    ...
  Category 11: UI Components (tasks 54-60)
    Task 54: Three-Panel Configuration Interface
    Task 55: LLM Chat Integration
    Task 56: Deployment Dashboard
    Task 57: Configuration Comparison
    Task 58: Search and History
    Task 59: In-App Help System
    Task 60: Responsive Design

→ Generate 60 master tasks preserving this structure
→ Add 3 integration tasks (61-63) for total of 63 master tasks
```

**Strategy B: PRD Has NO Explicit Task Breakdown (FALLBACK)**

If Step 2b fallback analysis was used:

1. **Generate granular master tasks** - Right-size for project complexity
2. **Target task count:**
   - Simple projects: 10-15 tasks
   - Medium projects: 20-35 tasks
   - Complex projects: 40-70 tasks
3. **Key principle:** More granular tasks = smaller LLM context per task

Break down each PRD section/feature into multiple focused master tasks:
- **Foundation tasks**: Setup, CI/CD, infrastructure, database
- **Feature tasks**: ONE task per specific feature component (not one task per entire feature)
- **Integration tasks**: Component integration, E2E testing, production validation

**Task Granularity Examples:**

❌ **TOO COARSE - Monolithic Tasks (WRONG):**
```
Task 1: "User Authentication System"
  - Combines: registration, login, logout, password reset, session management, OAuth
  - Problem: Too large for single LLM context, multiple developers blocked

Task 4: "LLM Configuration Engine"
  - Combines: orchestrator, device LLMs, two-phase workflow, prompt injection prevention,
    requirements checklist, live preview, document tracking
  - Problem: 7+ separate concerns in one task
```

✅ **PROPER GRANULARITY - Focused Tasks (CORRECT):**
```
Authentication Feature → 6 Master Tasks:
  Task 5: "Implement User Registration API Endpoint"
  Task 6: "Implement Login/Logout with JWT Token Generation"
  Task 7: "Implement Password Reset Flow with Email Notifications"
  Task 8: "Implement Session Management and Token Refresh"
  Task 9: "Implement OAuth2 Integration (Google/GitHub)"
  Task 10: "Implement Two-Factor Authentication (2FA)"

LLM Configuration Feature → 6 Master Tasks:
  Task 11: "Implement Hierarchical LLM Orchestrator"
  Task 12: "Implement Device-Specific LLM Strategy Selection"
  Task 13: "Implement Phase 1 Operational Configuration Generation"
  Task 14: "Implement Phase 2 STIG Compliance Layer"
  Task 15: "Implement Prompt Injection Prevention System"
  Task 16: "Implement Requirements Checklist Engine"
```

**Rule of Thumb:** If task description contains >3 "AND" conjunctions, split it into multiple tasks.

**Infrastructure Decomposition Pattern:**

When PRD describes complex infrastructure (multiple containers, services, databases), break into focused tasks:

❌ **TOO COARSE - Monolithic Infrastructure Task:**
```
Task 1: "Docker Environment Setup"
  - Set up complete 11-container architecture
  - Configure Docker Compose with all services
  - Set up networking (client, server, internet networks)
  - Configure volumes for Neo4j, Git, Ollama
  - Add health checks for all containers
  - Configure resource limits
  - Problem: Single huge infrastructure task blocks everything
```

✅ **PROPER DECOMPOSITION - Focused Infrastructure Tasks:**
```
Infrastructure → 5 Master Tasks:
  Task 1: "Docker Compose Master Configuration - Define 11 Containers"
    - Define all 11 services in docker-compose.yml with base configuration
    - Set container names, images, and basic ports

  Task 2: "Docker Network Configuration - Create Isolated Networks"
    - Create client, server, and internet networks
    - Configure network isolation and service communication rules

  Task 3: "Volume Management Strategy - Configure Persistent Storage"
    - Set up volumes for Neo4j, Git, Ollama, and application data
    - Configure volume mounts and permissions

  Task 4: "Health Check Implementation - Add Service Monitoring"
    - Add health check endpoints for all services
    - Configure health check intervals and timeouts

  Task 5: "Container Resource Limits - Configure Memory and CPU"
    - Set memory limits per container
    - Configure CPU allocation
    - Add restart policies
```

**Why This Matters:**
- Each task is independently testable
- Multiple developers can work in parallel
- Smaller context per task = better LLM performance
- Failures are isolated and easier to debug

#### 3b. Create JSON Structure (NATIVE TASK-MASTER SCHEMA)

Construct tasks.json matching task-master's native parse-prd output format:

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Specific, focused task name (Action Verb + Object)",
      "description": "Detailed explanation of what this task accomplishes",
      "status": "todo",
      "priority": "high",
      "dependencies": []
    },
    {
      "id": 2,
      "title": "Another focused task",
      "description": "Detailed explanation of the next task",
      "status": "todo",
      "priority": "medium",
      "dependencies": [1]
    }
  ]
}
```

**CRITICAL - Native Task-Master Schema (Phase 1 - Master Tasks Only):**
- **Required**: `id` (integer), `title` (string), `description` (string), `status` (string)
- **Optional**: `priority` (high/medium/low), `dependencies` (array of IDs)
- **Omit these fields**: `subtasks`, `details`, `testStrategy` (added later by task-master expand)
- Task IDs: 1, 2, 3, ... (numeric, sequential)
- Status: Always "todo" for new tasks
- Each title should be granular and focused
- Last 3 tasks MUST be: Component Integration Testing, E2E Workflow Testing, Production Readiness Validation

**Note:** The `subtasks`, `details`, and `testStrategy` fields are added in Phase 2/3 when `task-master expand` is run.

#### 3c. Write tasks.json File

Use the Write tool to create `.taskmaster/tasks/tasks.json`:

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Initialize Project Repository with CI/CD Pipeline",
      "description": "Set up Git repository, initialize project structure, and configure GitHub Actions for automated testing and deployment",
      "status": "todo",
      "priority": "high",
      "dependencies": []
    },
    {
      "id": 2,
      "title": "Configure PostgreSQL Database and Migrations",
      "description": "Set up PostgreSQL database, create initial schema, and configure migration framework",
      "status": "todo",
      "priority": "high",
      "dependencies": [1]
    }
    // ... (as many tasks as needed for the project)
  ]
}
```

### Step 4: Validate Output

**CRITICAL: PRD Coverage Validation**

If PRD had explicit task breakdown (Step 2a), perform coverage check:

```bash
# Count tasks generated vs PRD tasks
echo "Generated: $(jq '.tasks | length' .taskmaster/tasks/tasks.json) tasks"
echo "PRD specified: [X] tasks (from Section 7.1)"
```

**Coverage Requirements:**
- ✅ **If PRD specifies 67 tasks → generate 60-70 master tasks**
- ✅ **If PRD has 13 categories → ensure all 13 represented**
- ✅ **Missing categories = FAILURE** - go back and add them
- ❌ **14 tasks when PRD specifies 67 = 21% coverage = UNACCEPTABLE**

**Example check:**
```
PRD Category Checklist:
 ✅ Category 1: Foundation & Infrastructure (tasks 1-8)
 ✅ Category 2: Parent GraphRAG Server (tasks 9-13)
 ❌ Category 8: Rollback System (tasks 42-44) ← MISSING!
 ❌ Category 11: UI Components (tasks 54-60) ← COMPRESSED TO 1 TASK!

 ACTION REQUIRED: Add missing Category 8, expand Category 11 to 7 tasks
```

**Standard Validation:**

After writing tasks.json, verify:
- ✅ File exists: `.taskmaster/tasks/tasks.json`
- ✅ Valid JSON (use `jq . .taskmaster/tasks/tasks.json`)
- ✅ Task count appropriate for project complexity:
  - Simple PRDs: 10-20 tasks
  - Medium PRDs: 20-40 tasks
  - Complex PRDs with explicit breakdown: 50-70 tasks
- ✅ All required fields present: id, title, description, status
- ✅ **NO subtasks, details, or testStrategy fields** (added later in Phase 2/3)
- ✅ Each task title is specific and focused
- ✅ Last 3 tasks are Integration, E2E, Production Validation
- ✅ All PRD features/categories mapped to tasks
- ✅ Tasks are granular enough for small LLM context windows
- ✅ Performance targets captured in description (if specified in PRD)

### Step 5: Generate Summary

**If PRD had explicit task breakdown:**
```
✅ Master tasks generated: X tasks
📋 PRD Coverage:
   - PRD specified: 67 tasks across 13 categories
   - Generated: X master tasks
   - Coverage: X% (target: >90%)

📊 Category Breakdown:
   ✅ Category 1: Foundation & Infrastructure (8 tasks)
   ✅ Category 2: Parent GraphRAG Server (5 tasks)
   ✅ Category 3: Client Local GraphRAG (4 tasks)
   ...
   ✅ Category 11: UI Components (7 tasks)
   ✅ Category 13: Documentation (3 tasks)

📝 Next Steps:
   1. Review: task-master list
   2. Complexity analysis: task-master analyze-complexity --research
   3. Expand high-complexity tasks: task-master expand --id=<X> --research
```

**If PRD had NO explicit task breakdown:**
```
✅ Master tasks generated: X tasks
📊 Breakdown:
   - Foundation & Setup: X tasks
   - Feature Implementation: X tasks
   - Integration & Validation: 3 tasks

📝 Next Steps:
   1. Review: task-master list
   2. Complexity analysis: task-master analyze-complexity --research
   3. Expand complex tasks: task-master expand --id=<X> --research
```

## Common Mistakes to AVOID

### ❌ Mistake #0: Ignoring Explicit Task Breakdown in PRD

**WRONG:**
```
PRD has Section 7.1 "Task Decomposition" with 67 explicit tasks
→ Skill ignores it, invents own 14 tasks from features
→ Result: 21% coverage, missing entire categories (Rollback System)
```

**WHY WRONG:**
- PRD author spent significant time defining 67 specific tasks
- Explicit task breakdown is the **source of truth**
- Compressing 67 tasks into 14 loses critical detail
- Missing categories will cause project failures

**CORRECT:**
1. Search for Section 7, Section 7.1, "Task Decomposition", etc.
2. If found with 50-70 explicit tasks → **USE THOSE**
3. Extract ALL tasks, preserve structure, maintain categories
4. Add TaskMaster fields (subtasks: [], status: "todo", etc.)
5. Result: 60-70 master tasks matching PRD

**Example:**
```
PRD Section 7.1 lists:
  Category 8: Rollback System (tasks 42-44)
    Task 42: Pre-deployment Snapshot System
    Task 43: Rollback Command Generation
    Task 44: Rollback Execution Workflow

→ Generate 3 master tasks (42, 43, 44) for this category
→ DO NOT compress into "Deployment Workflows" task
```

### ❌ Mistake #1: Calling task-master parse-prd

**WRONG:**
```bash
task-master parse-prd docs/PRD.md
```

**WHY WRONG:** task-master parse-prd fails on large PRDs (>25K tokens), times out, and produces no output.

**CORRECT:** Generate tasks.json directly using AI analysis as shown in Step 3 above.

### ❌ Mistake #2: Using Read tool for PRD

**WRONG:**
```
Read tool: docs/PRD.md
```

**WHY WRONG:** Read tool has 25,000 token hard limit. Large PRDs will fail with "token limit exceeded."

**CORRECT:**
```bash
./lib/large-file-reader.sh docs/PRD.md
```

### ❌ Mistake #3: Storing large-file-reader output in variable

**WRONG:**
```bash
prd_content=$(./lib/large-file-reader.sh docs/PRD.md)
echo $prd_content  # Then try to use
```

**WHY WRONG:** Shell variables can't hold 30K+ tokens. Content gets truncated.

**CORRECT:** Just run the command. The output enters your context automatically:
```bash
./lib/large-file-reader.sh docs/PRD.md
# PRD content is now in your context - proceed to analyze
```

### ❌ Mistake #4: Including subtasks field

**WRONG:**
```json
{
  "id": 1,
  "title": "Set Up Database",
  "subtasks": [...]  // ❌ NO SUBTASKS!
}
```

**CORRECT:**
```json
{
  "id": 1,
  "title": "Configure PostgreSQL Database and Migrations",
  "description": "Set up PostgreSQL database, create initial schema, and configure migration framework",
  "status": "todo",
  "priority": "high",
  "dependencies": []
}
```

**WHY:** Phase 1 generates master tasks only. Subtasks added later in Phase 2/3 by `task-master expand`.

### ❌ Mistake #5: Too few or too coarse tasks

**WRONG:** 5-8 big tasks like "Implement User Authentication System"

**CORRECT:** Break into granular tasks (as many as needed):
- "Implement User Registration API Endpoint"
- "Implement Login/Logout with JWT Tokens"
- "Implement Password Reset Flow"
- "Implement Session Management"

**WHY:** Smaller, focused tasks = smaller LLM context during development. Don't artificially limit task count - generate what's needed for the project.

### ❌ Mistake #6: Missing integration tasks

**WRONG:** Tasks end with last feature, no integration/E2E/validation tasks.

**CORRECT:** Last 3 master tasks MUST be:
1. "Component Integration Testing"
2. "End-to-End Workflow Testing"
3. "Production Readiness Validation"

## What This Skill Does

Automatically generates high-quality TaskMaster tasks.json from Product Requirements Documents in isolated worktree, ensuring:
- Complete PRD coverage (all features mapped to tasks)
- Proper task dependencies (no circular dependencies)
- **Critical:** Always includes integration tasks (#N-2, #N-1, #N)
- OpenSpec mapping strategy per task
- Production-grade acceptance criteria
- **NEW**: Worktree isolation for each task generation phase
- **NEW**: Cross-worktree contamination prevention
- **NEW**: Support for large PRD files (>25,000 tokens) via large-file-reader utility

## Reading Large PRD Files

**CRITICAL:** This skill ALWAYS uses the large-file-reader utility for PRDs to avoid Claude Code's Read tool 25,000 token limit.

### Automatic Large File Reading

When this skill activates, it MUST use this approach:

```bash
# Step 1: Check file size and get metadata
echo "📊 Analyzing PRD file size..."
./lib/large-file-reader.sh docs/PRD.md --metadata

# Step 2: Read PRD using large-file-reader (bypasses 25K token limit)
echo "📖 Reading comprehensive PRD..."
prd_content=$(./lib/large-file-reader.sh docs/PRD.md)

# Step 3: Analyze and generate tasks
echo "🔨 Generating TaskMaster tasks from PRD..."
# Use $prd_content for analysis
```

**Why Always Use large-file-reader:**
- ✅ No 25,000 token limit (Read tool constraint)
- ✅ Handles files of any size (35,000+ tokens)
- ✅ Atomic document analysis (entire PRD in context)
- ✅ No chunking or pagination needed
- ✅ Prevents "token limit exceeded" errors

**DO NOT use Read tool for PRDs** - it will fail for comprehensive documents.

### File Size Guidelines

| PRD Size | Lines | Tokens | Approach |
|----------|-------|--------|----------|
| Small | <500 | <10K | large-file-reader (consistent) |
| Medium | 500-1000 | 10K-20K | large-file-reader (consistent) |
| Large | 1000-2000 | 20K-40K | large-file-reader (required) |
| Very Large | 2000+ | 40K+ | large-file-reader (required) |

**Consistency Rule:** Always use large-file-reader for PRDs regardless of size to ensure reliable operation.

## What This Skill Does

### 1. PRD Structure Analysis
Automatically identifies and extracts:
- Feature requirements (Section 3)
- Non-functional requirements (NFRs)
- Integration requirements (Section 4)
- Test strategy per requirement
- Architecture components affected
- Dependencies between requirements

### 2. Task Generation Rules

**Task Count (Master Tasks ONLY - No Subtasks):**
- Generate as many tasks as needed to properly decompose the PRD
- Simple projects: ~10-15 tasks
- Medium projects: ~20-30 tasks
- Complex projects: ~30-50+ tasks

**CRITICAL:** Granularity matters - more focused tasks = smaller LLM context during development. Don't artificially limit or expand task count - right-size for the project.

**Task Granularity Strategy:**
- Break down features into specific,focused tasks
- ONE task per API endpoint/component/feature
- NOT one task per entire feature
- Use numeric IDs only (no strings like "TASK-001")
- **NO subtasks field** - subtasks added later by task-master expand

**Task Categories (Auto-Generated):**
```
Foundation & Setup: 2-3 tasks
├─ Repository/environment setup
├─ CI/CD pipeline
└─ Testing framework

Data Layer: 2-4 tasks
├─ Schema design
├─ Models
└─ Migrations

Business Logic: 5-8 tasks per feature
├─ One task per PRD Feature section
└─ Core services, APIs, workflows

Integration Layer: 1-3 tasks
├─ External APIs
├─ Message queues
└─ Event handling

Frontend: 3-5 tasks (if applicable)
├─ UI components
├─ State management
└─ User workflows

Testing Infrastructure: 1-2 tasks
├─ Test framework setup
└─ Coverage configuration

Documentation: 1-2 tasks
├─ API docs
└─ Architecture docs

Operational Readiness: 2-3 tasks
├─ Monitoring
├─ Logging
└─ Deployment automation

Integration & Validation: 2-3 tasks (CRITICAL)
├─ Task #N-2: Component Integration Testing
├─ Task #N-1: E2E Workflow Testing
└─ Task #N: Production Readiness Validation
```

### 3. Dependency Analysis

**Automatic Dependency Detection:**
```
IF Task B requires output from Task A:
  → dependencies: ["A"]

IF Task mentions "database" AND database task exists:
  → dependencies: [database-task-id]

IF Task is integration/validation:
  → dependencies: [ALL feature task IDs]

IF Task has NO dependencies:
  → dependencies: []
```

**Sequential Dependencies:**
- Database schema → Data models → Services → APIs → Frontend
- Testing framework → Test suites
- Feature work → Integration testing → System validation

**Parallel Opportunities:**
- Independent services
- UI components (with mocked APIs)
- Documentation (ongoing)

### 4. Integration Task Generation (CRITICAL)

**Always Generate These Final 3 Master Tasks:**

Integration tasks are SEPARATE master tasks (not subtasks of a parent). They should be the last 3 tasks in your task list:

**Task #N-2: Component Integration Testing**
```json
{
  "id": 38,
  "title": "Component Integration Testing",
  "description": "Test all component interfaces and inter-container communication. Validate API contracts, database queries, and message passing between services.",
  "status": "todo",
  "priority": "critical",
  "dependencies": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
```

**Task #N-1: End-to-End Workflow Testing**
```json
{
  "id": 39,
  "title": "End-to-End Workflow Testing",
  "description": "Execute complete user workflows from start to finish. Test all critical user journeys and workflows defined in PRD success criteria.",
  "status": "todo",
  "priority": "critical",
  "dependencies": [38]
}
```

**Task #N: Production Readiness Validation**
```json
{
  "id": 40,
  "title": "Production Readiness Validation",
  "description": "Final validation of all production-ready criteria from PRD. Execute checklist validation, performance benchmarks, security scanning, and deployment readiness checks.",
  "status": "todo",
  "priority": "critical",
  "dependencies": [39]
}
```

**Note:** These are THREE SEPARATE master tasks. The `subtasks`, `details`, and `testStrategy` fields will be added in Phase 2/3 by `task-master expand`.

### 5. Quality Checks

**Before Outputting tasks.json:**
- [ ] All PRD features mapped to tasks
- [ ] Section 4 (Integration) generates Tasks #N-2, #N-1, #N
- [ ] Integration tasks depend on ALL feature tasks
- [ ] No circular dependencies
- [ ] All tasks have testStrategy
- [ ] All tasks have acceptanceCriteria
- [ ] All tasks have architectureComponent
- [ ] OpenSpec mapping defined per task
- [ ] Task count within target range (15-25 typical)

## TaskMaster Schema Requirements

**CRITICAL: PRD-to-Tasks generates MASTER TASKS ONLY (no subtasks):**

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "[Action Verb] + [Object]",
      "description": "Detailed explanation of what this task accomplishes",
      "status": "todo",
      "priority": "high",
      "dependencies": []
    },
    {
      "id": 2,
      "title": "Another focused task",
      "description": "Detailed explanation of the next task",
      "status": "todo",
      "priority": "medium",
      "dependencies": [1]
    }
  ]
}
```

**Field Requirements (Phase 1 - Master Tasks Only):**
- **Required:** `id` (number), `title` (string), `description` (string), `status` (string)
- **Optional:** `priority` (high/medium/low), `dependencies` (array of task IDs)
- **Omit:** `subtasks`, `details`, `testStrategy` (added later by task-master expand)
- **NO string IDs** like "TASK-001" - use numeric IDs: 1, 2, 3, etc.

**Subtasks added LATER by task-master:**
```bash
# After PRD-to-Tasks creates master tasks:
task-master analyze-complexity --research
task-master expand --id=5 --research  # For complex tasks
```

**Final structure (AFTER expand):**
```json
{
  "id": 5,
  "title": "Implement User Authentication API",
  "description": "Create registration endpoint with email validation, password hashing, and user creation",
  "status": "in-progress",
  "priority": "high",
  "dependencies": [2, 4],
  "details": "Use bcrypt for password hashing, JWT for tokens",
  "testStrategy": "Unit tests for validation, integration tests for API endpoints",
  "subtasks": [
    {
      "id": 1,
      "title": "Create user registration endpoint",
      "description": "POST /api/auth/register endpoint with validation",
      "status": "done",
      "dependencies": [],
      "details": "Use express-validator for input validation"
    },
    {
      "id": 2,
      "title": "Implement password hashing with bcrypt",
      "description": "Hash passwords before storing in database",
      "status": "done",
      "dependencies": [1],
      "details": "Use bcrypt with salt rounds = 10"
    }
  ]
}
```

**Note:** This shows the task AFTER Phase 2 `task-master expand` has been run. The PRD-to-Tasks skill in Phase 1 would have generated this task with `"subtasks": []`.

## OpenSpec Mapping Strategy

**Analyze PRD feature requirements:**

```
IF feature has ≤2 requirements:
  → openspecMapping.proposalStrategy = "single-task"
  → One proposal per task

ELSE IF requirements share code/models:
  → openspecMapping.proposalStrategy = "tightly-coupled"
  → One proposal covers multiple requirements
  → List related task IDs

ELSE IF requirements are independent:
  → openspecMapping.proposalStrategy = "loosely-coupled"
  → Separate proposal per requirement
  → Can implement in parallel
```

## Output Format

**CRITICAL: Generate TaskMaster-compliant format only:**

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Docker Environment Setup",
      "description": "Set up Docker Compose configuration for all 11 containers with networking, volumes, and health checks",
      "status": "todo",
      "priority": "high",
      "dependencies": []
    },
    {
      "id": 2,
      "title": "Configure Environment Variables",
      "description": "Set up .env files and environment variable management for all containers and services",
      "status": "todo",
      "priority": "high",
      "dependencies": [1]
    }
  ]
}
```

**Note:** Phase 1 master tasks omit `subtasks`, `details`, and `testStrategy` fields. These are added later in Phase 2/3 by `task-master expand`.

**After Generation, Provide:**

### Task Summary
```
Total Tasks: [X]
├─ Foundation: [count] (tasks 1-Y)
├─ Features: [count] (tasks Y+1-Z)
├─ Integration: [count] (tasks Z+1-N)
└─ Total: [X] tasks

Task Distribution:
├─ Data Layer: [count]
├─ Business Logic: [count]
├─ API Layer: [count]
├─ Frontend: [count]
├─ Testing Infrastructure: [count]
├─ Documentation: [count]
└─ Integration & Validation: [count]
```

### Dependency Analysis
```
Critical Path:
[Task 1] → [Task 2] → [Task 5] → [Task N-2] → [Task N-1] → [Task N]

Parallel Opportunities:
Branch A: [Tasks 3, 4, 6] (can run simultaneously)
Branch B: [Tasks 7, 8, 9] (can run simultaneously)

Integration Dependencies:
Task #N-2 depends on: [list ALL feature task IDs]
```

### OpenSpec Proposal Estimate
```
Based on coupling analysis:
├─ Tightly coupled features: [count] → [count] proposals
├─ Loosely coupled features: [count] → [count] proposals
└─ Estimated total proposals: [count]
```

### Validation Report
```
✅ All PRD features mapped
✅ Integration tasks present (Tasks #N-2, #N-1, #N)
✅ Dependencies validated (no circular)
✅ All tasks have test strategies
✅ Task count within target: [X] tasks
⚠️ Issues found: [list any gaps/inconsistencies]
```

## Common Issues to Prevent

### ❌ Missing Integration Tasks
**Problem:** Tasks for component integration/E2E/validation not generated  
**Solution:** Always generate Tasks #N-2, #N-1, #N from PRD Section 4

### ❌ Incomplete Test Strategy
**Problem:** testStrategy field is generic or empty  
**Solution:** Extract specific test scenarios from PRD acceptance criteria

### ❌ Wrong Dependencies
**Problem:** Integration task doesn't depend on all features  
**Solution:** Task #N-2 dependencies = ["1", "2", ..., "N-3"]

### ❌ Poor OpenSpec Mapping
**Problem:** All tasks marked "tightly-coupled" or all "loosely-coupled"  
**Solution:** Analyze each feature's requirements individually

### ❌ Task Count Too Coarse
**Problem:** Too few tasks (e.g. 5-8 big monolithic tasks)
**Solution:** Break down into granular, focused tasks. Generate as many as needed - don't artificially limit.

**Example:** A complex multi-service application might need 40-50 tasks. A simple CRUD app might need 12-15. Right-size for the project.

## Complete Example: PRD → tasks.json (MASTER TASKS ONLY)

### Example PRD (Simplified)

```markdown
# E-Commerce Platform PRD

## 3. Features

### 3.1 User Authentication
- User registration with email validation
- Login/logout with JWT tokens
- Password reset via email
- Session management and refresh tokens

### 3.2 Product Catalog
- Product CRUD operations
- Product search functionality
- Category filtering
- Price range filtering

### 3.3 Shopping Cart
- Add/remove cart items
- Update item quantities
- Guest cart support
- Persist cart across sessions

### 3.4 Checkout
- Stripe payment integration
- Order creation
- Order confirmation emails
- Order history tracking

## 4. Integration Requirements
- Component integration testing
- E2E user journey testing
- Production readiness validation
```

### Example tasks.json Output (MASTER TASKS ONLY - NO SUBTASKS)

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Initialize Project Repository with CI/CD Pipeline",
      "description": "Set up Git repository, initialize project structure, and configure GitHub Actions for automated testing and deployment",
      "status": "todo",
      "priority": "high",
      "dependencies": []
    },
    {
      "id": 2,
      "title": "Configure PostgreSQL Database and Migrations Framework",
      "description": "Set up PostgreSQL database, create initial schema, and configure migration framework for version control",
      "status": "todo",
      "priority": "high",
      "dependencies": [1]
    },
    {
      "id": 3,
      "title": "Set Up Testing Framework (Jest/Pytest) and Coverage Tools",
      "description": "Install and configure testing framework with coverage reporting and CI integration",
      "status": "todo",
      "priority": "high",
      "dependencies": [1]
    },
    {
      "id": 4,
      "title": "Configure Environment Variables and Secrets Management",
      "description": "Set up .env files, secrets management, and environment configuration for all environments",
      "status": "todo",
      "priority": "high",
      "dependencies": [1]
    },
    {
      "id": 5,
      "title": "Implement User Registration API Endpoint",
      "description": "Create registration endpoint with email validation, password hashing, and user creation",
      "status": "todo",
      "priority": "high",
      "dependencies": [2, 4]
    }
  ]
}
```

**Note:**
- Phase 1 master tasks omit `subtasks`, `details`, and `testStrategy` fields
- These fields are added in Phase 2/3 by `task-master expand`
- Full example shows only first 5 tasks for brevity - actual output would have 25-70 tasks

### Key Points from Example

✅ **Granular Master Tasks**: Focused tasks, not monolithic (Registration, Login, Password Reset separate)
✅ **NO Optional Fields Yet**: subtasks, details, testStrategy added later by task-master expand
✅ **Numeric IDs**: Sequential 1, 2, 3...
✅ **One Task Per Component**: Registration, Login, Password Reset are separate tasks
✅ **Last 3 Tasks**: Integration Testing, E2E Testing, Production Validation
✅ **Smaller Context**: Each task is focused, keeping LLM context small during development
✅ **PRD Coverage**: All Section 3 features + Section 4 requirements mapped

## Integration with Workflow

**In Claude Projects session:**
1. User pastes PRD content
2. This skill activates automatically
3. Skill enhances task generation with quality checks
4. User receives validated tasks.json ready for Phase 1

**Human validation still required:**
- Review task count and structure
- Verify PRD coverage
- Confirm integration tasks present
- Approve before proceeding to Claude Code