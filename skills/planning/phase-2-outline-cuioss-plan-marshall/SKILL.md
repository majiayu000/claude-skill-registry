---
name: phase-2-outline
description: Architecture-driven solution outline creation with intelligent module selection and Skills by Profile assignment
allowed-tools: Read, Glob, Grep, Bash
---

# Phase Refine Outline Skill

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin executing the workflow steps below, starting with Step 1.

**Role**: Architecture-driven workflow skill for creating solution outlines. Uses pre-computed architecture data to make intelligent module and package placement decisions.

**Key Insight**: Module and package matching is **semantic analysis** that requires LLM reasoning. Scripts provide DATA, the LLM provides REASONING.

---

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `plan_id` | string | Yes | Plan identifier |
| `feedback` | string | No | User feedback from review (for revision iterations) |

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                ARCHITECTURE-DRIVEN WORKFLOW                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Load architecture context                               │
│          → architecture info                                     │
│                                                                  │
│  Step 2: Load and understand requirements                        │
│          → manage-plan-documents read --type request             │
│                                                                  │
│  Step 2.5: Load outline extension skills (if domain has one)     │
│          → resolve-workflow-skill-extension --type outline       │
│          → Extensions provide Domain Constraints, Patterns       │
│                                                                  │
│  Step 3: Assess complexity (simple vs complex)                   │
│          → Decompose if multi-module                             │
│                                                                  │
│  Step 4: Select target modules                                   │
│          → Score by responsibility, purpose, packages            │
│                                                                  │
│  Step 5: Determine package placement                             │
│          → architecture module --name X --full                   │
│                                                                  │
│  Step 6: Create deliverables with Skills by Profile              │
│          → One deliverable per module                            │
│          → Skills by Profile from module.skills_by_profile       │
│                                                                  │
│  Step 7: Create IT deliverable (optional)                        │
│          → architecture modules --command integration-tests      │
│          → Separate deliverable targeting IT module              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Load Architecture Context

Query project architecture BEFORE any codebase exploration. Architecture data is pre-computed and compact (~500 tokens).

**EXECUTE**:
```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture info
```

Output format: `plan-marshall:analyze-project-architecture/standards/client-api.md`

**If status=error or architecture not found**: Return error and abort:
```toon
status: error
message: Run /marshall-steward first
```

---

## Step 2: Load and Understand Requirements

Load the request document and extract actionable requirements.

**EXECUTE**:
```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents read \
  --plan-id {plan_id} --type request
```

Output format: `pm-workflow:manage-plan-documents/documents/request.toon`

**Parse for**:
- Functional requirements (what to build)
- Constraints (technology, patterns, compatibility)
- Explicit test requirements (unit, integration, E2E)
- Acceptance criteria

**EXECUTE**:
```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config read \
  --plan-id {plan_id}
```

Output format: `pm-workflow:manage-config`

Extract `domains` array - each deliverable will be assigned a single domain from this array.

---

## Step 2.5: Load Outline Extension Skills

For each domain in config.toon, check if an outline extension exists and load it as context.

**Purpose**: Outline extensions provide domain-specific knowledge (Domain Constraints, Deliverable Patterns) that augment the standard workflow. They are skills loaded as context, not workflow replacements.

**For each domain** from Step 2:

**EXECUTE**:
```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  resolve-workflow-skill-extension --domain {domain} --type outline
```

**Output (TOON)**:
```toon
status: success
domain: {domain}
type: outline
extension: pm-plugin-development:ext-outline-plugin  # or null if no extension
```

**If extension exists (not null)**, load it as context:

```
Skill: {resolved_extension}
```

The extension skill provides:
- **Domain Constraints**: Rules for deliverable creation (component rules, dependency rules)
- **Deliverable Patterns**: Grouping strategies, file structures, verification commands
- **Impact Analysis Patterns**: Discovery commands for cross-cutting changes

These are applied naturally during deliverable creation (Steps 4-6) - no special processing needed.

**If no extension exists**: Continue with standard workflow. Most domains (java, javascript) don't need outline extensions.

---

## Step 3: Assess Complexity (Simple vs Complex)

Determine if task is single-module (simple) or multi-module (complex):

| Scope | Workflow | Action |
|-------|----------|--------|
| Single module affected | **Simple** | Proceed to module selection |
| Multiple modules affected | **Complex** | Decompose first, then simple workflow per sub-task |

### Simple Workflow (single module)

```
┌───────────────────────────────┐
│       SIMPLE WORKFLOW         │
├───────────────────────────────┤
│ 1. Select target module       │
│ 2. Select target package      │
│ 3. Create deliverables        │
└───────────────────────────────┘
```

### Complex Workflow (multi-module)

```
┌───────────────────────────────┐
│       COMPLEX WORKFLOW        │
├───────────────────────────────┤
│ 1. Load dependency graph      │
│ 2. Decompose into sub-tasks   │
│ 3. Run simple workflow each   │
│ 4. Aggregate deliverables     │
│ 5. Order by layers (graph)    │
└───────────────────────────────┘
```

For complex tasks, load the complete dependency graph to determine execution ordering.

**EXECUTE**:
```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture graph
```

Output format: `plan-marshall:analyze-project-architecture/standards/module-graph-format.md` (force load)

**Detail**: See `standards/module-selection.md` for decomposition patterns and dependency ordering.

---

## Step 4: Select Target Modules

For simple tasks: identify the single affected module. For complex tasks: select module for each sub-task.

### Module Selection Analysis

For each candidate module, evaluate:

| Factor | Weight | Score Criteria |
|--------|--------|----------------|
| responsibility match | 3 | Keywords in task match responsibility |
| purpose fit | 2 | Purpose compatible with change type |
| key_packages match | 3 | Task aligns with package descriptions |
| dependency position | 2 | Correct layer for the change |

**Selection threshold**: Modules with weighted score >= 6 are candidates.

### Query Module Details

For each candidate module:

**EXECUTE**:
```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture module \
  --name {module}
```

### Document Selection Reasoning

**Template**: `templates/module-selection-analysis.md` (force load)

---

## Step 5: Determine Package Placement

For each selected module, determine where new code belongs.

### Load Complete Package Structure

**EXECUTE**:
```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture module \
  --name {module} --full
```

### Package Selection Decision Matrix

| Scenario | Action |
|----------|--------|
| Task matches key_package description | Place in that key_package |
| Task needs utility location | Check for existing util package |
| New cross-cutting concern | Create new package (document reasoning) |
| Unclear placement | Check has_package_info packages first |

**Detail**: See `standards/module-selection.md` for key_packages guidance and validation checklist.

### Document Package Reasoning

**Template**: `templates/package-selection.md` (force load)

---

## Step 6: Create Deliverables with Skills by Profile

Create deliverables with module context and skills organized by profile.

**Core constraint**: One deliverable = one module.

### Check Module Test Infrastructure

**EXECUTE**:
```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture modules \
  --command module-tests
```

Returns list of module names that have unit test infrastructure.

### Skills by Profile Block

- `skills-implementation`: Always included
- `skills-testing`: Only if module has test infrastructure

**Detail**: See `standards/skills-by-profile.md` for profile design rationale and task-plan integration.

### Deliverable Structure

**Contract**: `pm-workflow:manage-solution-outline/standards/deliverable-contract.md` (force load)

Each deliverable MUST include all required fields from the contract:
- Metadata (change_type, execution_mode, domain, depends)
- Module Context (module, package, placement_rationale)
- Skills by Profile (skills-implementation; skills-testing if test infra exists)
- Affected files (explicit list)
- Verification (command and criteria)

---

## Step 7: Create IT Deliverable (Optional)

If integration tests are needed, create a **separate deliverable** targeting the IT module.

### When to Create IT Deliverable

| Change Type | IT Needed? | Rationale |
|-------------|------------|-----------|
| API endpoint (REST, GraphQL) | **YES** | External contract |
| UI component | **YES** | User-facing behavior |
| Public library API | **YES** | Consumer contract |
| Configuration/properties | **YES** | Runtime behavior |
| Internal implementation | NO | No external impact |
| Refactoring (same behavior) | NO | Behavior unchanged |
| Private/internal classes | NO | Not externally visible |

### Check IT Infrastructure

**EXECUTE**:
```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture modules \
  --command integration-tests
```

**If result is empty**: Skip IT deliverable (no IT module exists).

**Detail**: See `standards/integration-tests.md` for IT decision flow, module patterns, and verification commands.

### IT Deliverable Structure

IT deliverables follow the same contract as implementation deliverables.

**Contract**: `pm-workflow:manage-solution-outline/standards/deliverable-contract.md`

**Key Differences**:
- IT is always a **separate deliverable** - not embedded in implementation deliverable
- IT targets the **IT module** - found via `architecture modules --command integration-tests`
- IT depends on implementation - set `depends:` to reference the implementation deliverable
- IT has only `skills-implementation` - IT code is "implementation" of test code

---

## Step 8: Write Solution Document

Write the solution document using heredoc.

**Skill**: `pm-workflow:manage-solution-outline` (force load)

Provides complete guidance on solution document structure, diagram patterns, and examples by task type.

**EXECUTE**:
```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline \
  write \
  --plan-id {plan_id} <<'EOF'
{content per manage-solution-outline skill with deliverables per deliverable-contract.md}
EOF
```

Validation runs automatically on every write.

---

## Step 9: Set Detected Domains

**EXECUTE**:
```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config set-domains \
  --plan-id {plan_id} --domains {detected_domains}
```

This is an **intelligent decision output** - not a copy of marshal.json domains, but Claude's analysis of which domains are relevant to the specific request.

---

## Step 10: Record Issues as Lessons

**EXECUTE**:
```bash
python3 .plan/execute-script.py plan-marshall:lessons-learned:manage-lesson add \
  --component-type skill \
  --component-name phase-2-outline \
  --category observation \
  --title "{issue summary}" \
  --detail "{context and resolution approach}"
```

---

## Step 11: Return Results

Return structured output:
```toon
status: success
plan_id: {plan_id}
deliverable_count: {N}
domains_detected: [{detected_domains}]
lessons_recorded: {count}
message: {error message if status=error}
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Architecture not found | Return `{status: error, message: "Run /marshall-steward first"}` and abort |
| Request not found | Return `{status: error, message: "Request not found"}` |
| Validation fails | Fix issues or return partial with error list |
| Domain unknown | Return error with valid domains |
| Script execution fails | Record lesson-learned, return error |

---

## Integration

**Invoked by**: `pm-workflow:solution-outline-agent` (thin agent)

**Script Notations** (use EXACTLY as shown):
- `plan-marshall:analyze-project-architecture:architecture` - Architecture queries
- `pm-workflow:manage-solution-outline:manage-solution-outline` - Write solution document
- `pm-workflow:manage-plan-documents:manage-plan-documents` - Request operations
- `pm-workflow:manage-config:manage-config` - Plan config operations
- `pm-workflow:manage-references:manage-references` - Plan references
- `plan-marshall:lessons-learned:manage-lesson` - Record lessons on issues

**Consumed By**:
- `pm-workflow:phase-3-plan` skill (reads deliverables for task creation)

---

## Output Validation

The workflow skill MUST validate that each deliverable contains all required fields from the deliverable contract:

- [ ] `change_type` metadata
- [ ] `execution_mode` metadata
- [ ] `domain` metadata (valid domain from marshal.json)
- [ ] `depends` field (`none` or valid deliverable references)
- [ ] Module context (module, package, placement_rationale)
- [ ] Skills by Profile (`skills-implementation` always; `skills-testing` if module has test infra)
- [ ] Explicit file list (not "all files matching X")
- [ ] Verification command and criteria

---

## Related Documents

- `pm-workflow:workflow-extension-api/standards/extensions/outline-extension.md` - Outline extension contract
- `pm-workflow:manage-solution-outline/standards/deliverable-contract.md` - Deliverable structure
- `pm-workflow:workflow-architecture` - Workflow architecture overview
- `plan-marshall:analyze-project-architecture` - Architecture API documentation
- `plan-marshall:analyze-project-architecture/standards/module-graph-format.md` - Module dependency graph format
