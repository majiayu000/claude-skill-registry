---
name: "Goal-Seeking Agent Pattern"
version: 1.0.0
description: |
  Guides architects on when and how to use goal-seeking agents as a design pattern.
  This skill helps evaluate whether autonomous agents are appropriate for a given
  problem, how to structure their objectives, integrate with goal_agent_generator,
  and reference real amplihack examples like AKS SRE automation, CI diagnostics,
  pre-commit workflows, and fix-agent pattern matching.
auto-detection:
  triggers:
    - "complex workflow"
    - "autonomous agent"
    - "goal-seeking"
    - "adaptive behavior"
    - "multi-phase processing"
    - "task automation design"
    - "autonomous decision-making"
    - "multi-step process"
    - "workflow orchestration"
    - "self-directed agent"
allowed-tools: ["Read", "Grep", "Glob", "WebSearch"]
target-agents: ["architect"]
priority: "medium"
complexity: "medium"
---

# Goal-Seeking Agent Pattern Skill

## 1. What Are Goal-Seeking Agents?

Goal-seeking agents are autonomous AI agents that execute multi-phase objectives by:

1. **Understanding High-Level Goals**: Accept natural language objectives without explicit step-by-step instructions
2. **Planning Execution**: Break goals into phases with dependencies and success criteria
3. **Autonomous Execution**: Make decisions and adapt behavior based on intermediate results
4. **Self-Assessment**: Evaluate progress against success criteria and adjust approach
5. **Resilient Operation**: Handle failures gracefully and explore alternative solutions

### Core Characteristics

**Autonomy**: Agents decide HOW to achieve goals, not just follow prescriptive steps

**Adaptability**: Adjust strategy based on runtime conditions and intermediate results

**Goal-Oriented**: Focus on outcomes (what to achieve) rather than procedures (how to achieve)

**Multi-Phase**: Complex objectives decomposed into manageable phases with dependencies

**Self-Monitoring**: Track progress, detect failures, and course-correct autonomously

### Distinction from Traditional Agents

| Traditional Agent             | Goal-Seeking Agent            |
| ----------------------------- | ----------------------------- |
| Follows fixed workflow        | Adapts workflow to context    |
| Prescriptive steps            | Outcome-oriented objectives   |
| Human intervention on failure | Autonomous recovery attempts  |
| Single-phase execution        | Multi-phase with dependencies |
| Rigid decision tree           | Dynamic strategy adjustment   |

### When Goal-Seeking Makes Sense

Goal-seeking agents excel when:

- **Problem space is large**: Many possible paths to success
- **Context varies**: Runtime conditions affect optimal approach
- **Failures are expected**: Need autonomous recovery without human intervention
- **Objectives are clear**: Success criteria well-defined but path is flexible
- **Multi-step complexity**: Requires coordination across phases with dependencies

### When to Avoid Goal-Seeking

Use traditional agents or scripts when:

- **Single deterministic path**: Only one way to achieve goal
- **Latency-critical**: Need fastest possible execution (no decision overhead)
- **Safety-critical**: Human verification required at each step
- **Simple workflow**: Complexity of goal-seeking exceeds benefit
- **Audit requirements**: Need deterministic, reproducible execution

## 2. When to Use This Pattern

### Problem Indicators

Use goal-seeking agents when you observe these patterns:

#### Pattern 1: Workflow Variability

**Indicators**:

- Same objective requires different approaches based on context
- Manual decisions needed at multiple points
- "It depends" answers when mapping workflow

**Example**: Release workflow that varies by:

- Environment (staging vs production)
- Change type (hotfix vs feature)
- Current system state (healthy vs degraded)

**Solution**: Goal-seeking agent evaluates context and adapts workflow

#### Pattern 2: Multi-Phase Complexity

**Indicators**:

- Objective requires 3-5+ distinct phases
- Phases have dependencies (output of phase N feeds phase N+1)
- Parallel execution opportunities exist
- Success criteria differ per phase

**Example**: Data pipeline with phases:

1. Data collection (multiple sources, parallel)
2. Transformation (depends on collection results)
3. Validation (depends on transformation output)
4. Publishing (conditional on validation pass)

**Solution**: Goal-seeking agent orchestrates phases, handles dependencies

#### Pattern 3: Autonomous Recovery Needed

**Indicators**:

- Failures are expected and recoverable
- Multiple retry/fallback strategies exist
- Human intervention is expensive or slow
- Can verify success programmatically

**Example**: CI diagnostic workflow:

- Test failures (retry with different approach)
- Environment issues (reconfigure and retry)
- Dependency conflicts (resolve and rerun)

**Solution**: Goal-seeking agent tries strategies until success or escalation

#### Pattern 4: Adaptive Decision Making

**Indicators**:

- Need to evaluate trade-offs at runtime
- Multiple valid solutions with different characteristics
- Optimization objectives (speed vs quality vs cost)
- Context-dependent best practices

**Example**: Fix agent pattern matching:

- QUICK mode for obvious issues
- DIAGNOSTIC mode for unclear problems
- COMPREHENSIVE mode for complex solutions

**Solution**: Goal-seeking agent selects strategy based on problem analysis

#### Pattern 5: Domain Expertise Required

**Indicators**:

- Requires specialized knowledge to execute
- Multiple domain-specific tools/approaches
- Best practices vary by domain
- Coordination of specialized sub-agents

**Example**: AKS SRE automation:

- Azure-specific operations (ARM, CLI)
- Kubernetes expertise (kubectl, YAML)
- Networking knowledge (CNI, ingress)
- Security practices (RBAC, Key Vault)

**Solution**: Goal-seeking agent with domain expertise coordinates specialized actions

### Decision Framework

Use this 5-question framework to evaluate goal-seeking applicability:

#### Question 1: Is the objective well-defined but path flexible?

**YES if**:

- Clear success criteria exist
- Multiple valid approaches
- Runtime context affects optimal path

**NO if**:

- Only one correct approach
- Path is deterministic
- Success criteria ambiguous

**Example YES**: "Ensure AKS cluster is production-ready" (many paths, clear criteria)
**Example NO**: "Run specific kubectl command" (one path, prescriptive)

#### Question 2: Are there multiple phases with dependencies?

**YES if**:

- Objective naturally decomposes into 3-5+ phases
- Phase outputs feed subsequent phases
- Some phases can execute in parallel
- Failures in one phase affect downstream phases

**NO if**:

- Single-phase execution sufficient
- No inter-phase dependencies
- Purely sequential with no branching

**Example YES**: Data pipeline (collect → transform → validate → publish)
**Example NO**: Format code with ruff (single atomic operation)

#### Question 3: Is autonomous recovery valuable?

**YES if**:

- Failures are common and expected
- Multiple recovery strategies exist
- Human intervention is expensive/slow
- Can verify success automatically

**NO if**:

- Failures are rare edge cases
- Manual investigation always required
- Safety-critical (human verification needed)
- Cannot verify success programmatically

**Example YES**: CI diagnostic workflow (try multiple fix strategies)
**Example NO**: Deploy to production (human approval required)

#### Question 4: Does context significantly affect approach?

**YES if**:

- Environment differences change strategy
- Current system state affects decisions
- Trade-offs vary by situation (speed vs quality vs cost)
- Domain-specific best practices apply

**NO if**:

- Same approach works for all contexts
- No environmental dependencies
- No trade-off decisions needed

**Example YES**: Fix agent (quick vs diagnostic vs comprehensive based on issue)
**Example NO**: Generate UUID (context-independent)

#### Question 5: Is the complexity justified?

**YES if**:

- Problem is repeated frequently (2+ times/week)
- Manual execution takes 30+ minutes
- High value from automation
- Maintenance cost is acceptable

**NO if**:

- One-off or rare problem
- Quick manual execution (< 5 minutes)
- Simple script suffices
- Maintenance cost exceeds benefit

**Example YES**: CI failure diagnosis (frequent, time-consuming, high value)
**Example NO**: One-time data migration (rare, script sufficient)

### Decision Matrix

| All 5 YES | Use Goal-Seeking Agent |
| 4 YES, 1 NO | Probably use Goal-Seeking Agent |
| 3 YES, 2 NO | Consider simpler agent or hybrid |
| 2 YES, 3 NO | Traditional agent likely better |
| 0-1 YES | Script or simple automation |

## 3. Architecture Pattern

### Component Architecture

Goal-seeking agents have four core components:

```python
# Component 1: Goal Definition
class GoalDefinition:
    """Structured representation of objective"""
    raw_prompt: str              # Natural language goal
    goal: str                    # Extracted primary objective
    domain: str                  # Problem domain (security, data, automation, etc.)
    constraints: list[str]       # Technical/operational constraints
    success_criteria: list[str]  # How to verify success
    complexity: str              # simple, moderate, complex
    context: dict                # Additional metadata

# Component 2: Execution Plan
class ExecutionPlan:
    """Multi-phase plan with dependencies"""
    goal_id: uuid.UUID
    phases: list[PlanPhase]
    total_estimated_duration: str
    required_skills: list[str]
    parallel_opportunities: list[list[str]]  # Phases that can run parallel
    risk_factors: list[str]

# Component 3: Plan Phase
class PlanPhase:
    """Individual phase in execution plan"""
    name: str
    description: str
    required_capabilities: list[str]
    estimated_duration: str
    dependencies: list[str]          # Names of prerequisite phases
    parallel_safe: bool              # Can execute in parallel
    success_indicators: list[str]    # How to verify phase completion

# Component 4: Skill Definition
class SkillDefinition:
    """Capability needed for execution"""
    name: str
    description: str
    capabilities: list[str]
    implementation_type: str  # "native" or "delegated"
    delegation_target: str    # Agent to delegate to
```

### Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. GOAL ANALYSIS                                            │
│                                                             │
│  Input: Natural language objective                         │
│  Process: Extract goal, domain, constraints, criteria      │
│  Output: GoalDefinition                                    │
│                                                             │
│  [PromptAnalyzer.analyze_text(prompt)]                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. PLANNING                                                 │
│                                                             │
│  Input: GoalDefinition                                     │
│  Process: Decompose into phases, identify dependencies     │
│  Output: ExecutionPlan                                     │
│                                                             │
│  [ObjectivePlanner.generate_plan(goal_definition)]        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. SKILL SYNTHESIS                                          │
│                                                             │
│  Input: ExecutionPlan                                      │
│  Process: Map capabilities to skills, identify agents      │
│  Output: list[SkillDefinition]                            │
│                                                             │
│  [SkillSynthesizer.synthesize(execution_plan)]            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. AGENT ASSEMBLY                                           │
│                                                             │
│  Input: GoalDefinition, ExecutionPlan, Skills              │
│  Process: Combine into executable bundle                   │
│  Output: GoalAgentBundle                                   │
│                                                             │
│  [AgentAssembler.assemble(goal, plan, skills)]            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. EXECUTION (Auto-Mode)                                    │
│                                                             │
│  Input: GoalAgentBundle                                    │
│  Process: Execute phases, monitor progress, adapt          │
│  Output: Success or escalation                             │
│                                                             │
│  [Auto-mode with initial_prompt from bundle]              │
└─────────────────────────────────────────────────────────────┘
```

### Phase Dependency Management

Phases can have three relationship types:

**Sequential Dependency**: Phase B depends on Phase A completion

```
Phase A → Phase B → Phase C
```

**Parallel Execution**: Phases can run concurrently

```
Phase A ──┬→ Phase B ──┐
          └→ Phase C ──┴→ Phase D
```

**Conditional Branching**: Phase selection based on results

```
Phase A → [Decision] → Phase B (success path)
                    └→ Phase C (recovery path)
```

### State Management

Goal-seeking agents maintain state across phases:

```python
class AgentState:
    """Runtime state for goal-seeking agent"""
    current_phase: str
    completed_phases: list[str]
    phase_results: dict[str, Any]  # Output from each phase
    failures: list[FailureRecord]  # Track what didn't work
    retry_count: int
    total_duration: timedelta
    context: dict                  # Shared context across phases
```

### Error Handling

Three error recovery strategies:

**Retry with Backoff**: Same approach, exponential delay

```python
for attempt in range(MAX_RETRIES):
    try:
        result = execute_phase(phase)
        break
    except RetryableError as e:
        wait_time = INITIAL_DELAY * (2 ** attempt)
        sleep(wait_time)
```

**Alternative Strategy**: Different approach to same goal

```python
for strategy in STRATEGIES:
    try:
        result = execute_phase(phase, strategy)
        break
    except StrategyFailedError:
        continue  # Try next strategy
else:
    escalate_to_human("All strategies exhausted")
```

**Graceful Degradation**: Accept partial success

```python
try:
    result = execute_phase_optimal(phase)
except OptimalFailedError:
    result = execute_phase_fallback(phase)  # Lower quality but works
```

## 4. Integration with goal_agent_generator

The `goal_agent_generator` module provides the implementation for goal-seeking agents. Here's how to integrate:

### Core API

```python
from amplihack.goal_agent_generator import (
    PromptAnalyzer,
    ObjectivePlanner,
    SkillSynthesizer,
    AgentAssembler,
    GoalAgentPackager,
)

# Step 1: Analyze natural language goal
analyzer = PromptAnalyzer()
goal_definition = analyzer.analyze_text("""
Automate AKS cluster production readiness verification.
Check security, networking, monitoring, and compliance.
Generate report with actionable recommendations.
""")

# Step 2: Generate execution plan
planner = ObjectivePlanner()
execution_plan = planner.generate_plan(goal_definition)

# Step 3: Synthesize required skills
synthesizer = SkillSynthesizer()
skills = synthesizer.synthesize(execution_plan)

# Step 4: Assemble complete agent
assembler = AgentAssembler()
agent_bundle = assembler.assemble(
    goal_definition=goal_definition,
    execution_plan=execution_plan,
    skills=skills,
    bundle_name="aks-readiness-checker"
)

# Step 5: Package for deployment
packager = GoalAgentPackager()
packager.package(
    bundle=agent_bundle,
    output_dir=".claude/agents/goal-driven/aks-readiness-checker"
)
```

### CLI Integration

```bash
# Generate agent from prompt file
amplihack goal-agent-generator create \
  --prompt ./prompts/aks-readiness.md \
  --output .claude/agents/goal-driven/aks-readiness-checker

# Generate agent from inline prompt
amplihack goal-agent-generator create \
  --inline "Automate CI failure diagnosis and fix iteration" \
  --output .claude/agents/goal-driven/ci-fixer

# List generated agents
amplihack goal-agent-generator list

# Test agent execution
amplihack goal-agent-generator test \
  --agent-path .claude/agents/goal-driven/ci-fixer \
  --dry-run
```

### PromptAnalyzer Details

Extracts structured information from natural language:

```python
from amplihack.goal_agent_generator import PromptAnalyzer
from pathlib import Path

analyzer = PromptAnalyzer()

# From file
goal_def = analyzer.analyze(Path("./prompts/my-goal.md"))

# From text
goal_def = analyzer.analyze_text("Deploy and monitor microservices to AKS")

# GoalDefinition contains:
print(goal_def.goal)               # "Deploy and monitor microservices to AKS"
print(goal_def.domain)             # "deployment"
print(goal_def.constraints)        # ["Zero downtime", "Rollback capability"]
print(goal_def.success_criteria)   # ["All pods running", "Metrics visible"]
print(goal_def.complexity)         # "moderate"
print(goal_def.context)            # {"priority": "high", "scale": "medium"}
```

Domain classification:

- `data-processing`: Data transformation, analysis, ETL
- `security-analysis`: Vulnerability scanning, audits
- `automation`: Workflow automation, scheduling
- `testing`: Test generation, validation
- `deployment`: Release, publishing, distribution
- `monitoring`: Observability, alerting
- `integration`: API connections, webhooks
- `reporting`: Dashboards, metrics, summaries

Complexity determination:

- `simple`: Single-phase, < 50 words, basic operations
- `moderate`: 2-4 phases, 50-150 words, some coordination
- `complex`: 5+ phases, > 150 words, sophisticated orchestration

### ObjectivePlanner Details

Generates multi-phase execution plans:

```python
from amplihack.goal_agent_generator import ObjectivePlanner

planner = ObjectivePlanner()
plan = planner.generate_plan(goal_definition)

# ExecutionPlan contains:
for i, phase in enumerate(plan.phases, 1):
    print(f"Phase {i}: {phase.name}")
    print(f"  Description: {phase.description}")
    print(f"  Duration: {phase.estimated_duration}")
    print(f"  Capabilities: {', '.join(phase.required_capabilities)}")
    print(f"  Dependencies: {', '.join(phase.dependencies)}")
    print(f"  Parallel Safe: {phase.parallel_safe}")
    print(f"  Success Indicators: {phase.success_indicators}")

print(f"\nTotal Duration: {plan.total_estimated_duration}")
print(f"Required Skills: {', '.join(plan.required_skills)}")
print(f"Parallel Opportunities: {plan.parallel_opportunities}")
print(f"Risk Factors: {plan.risk_factors}")
```

Phase templates by domain:

- **data-processing**: Collection → Transformation → Analysis → Reporting
- **security-analysis**: Reconnaissance → Vulnerability Detection → Risk Assessment → Reporting
- **automation**: Setup → Workflow Design → Execution → Validation
- **testing**: Test Planning → Implementation → Execution → Results Analysis
- **deployment**: Pre-deployment → Deployment → Verification → Post-deployment
- **monitoring**: Setup Monitors → Data Collection → Analysis → Alerting

### SkillSynthesizer Details

Maps capabilities to skills:

```python
from amplihack.goal_agent_generator import SkillSynthesizer

synthesizer = SkillSynthesizer()
skills = synthesizer.synthesize(execution_plan)

# list[SkillDefinition]
for skill in skills:
    print(f"Skill: {skill.name}")
    print(f"  Description: {skill.description}")
    print(f"  Capabilities: {', '.join(skill.capabilities)}")
    print(f"  Type: {skill.implementation_type}")
    if skill.implementation_type == "delegated":
        print(f"  Delegates to: {skill.delegation_target}")
```

Capability mapping:

- `data-*` → `data-processor` skill
- `security-*`, `vulnerability-*` → `security-analyzer` skill
- `test-*` → `tester` skill
- `deploy-*` → `deployer` skill
- `monitor-*`, `alert-*` → `monitor` skill
- `report-*`, `document-*` → `documenter` skill

### AgentAssembler Details

Combines components into executable bundle:

```python
from amplihack.goal_agent_generator import AgentAssembler

assembler = AgentAssembler()
bundle = assembler.assemble(
    goal_definition=goal_definition,
    execution_plan=execution_plan,
    skills=skills,
    bundle_name="custom-agent"  # Optional, auto-generated if omitted
)

# GoalAgentBundle contains:
print(bundle.id)                    # UUID
print(bundle.name)                  # "custom-agent" or auto-generated
print(bundle.version)               # "1.0.0"
print(bundle.status)                # "ready"
print(bundle.auto_mode_config)      # Configuration for auto-mode execution
print(bundle.metadata)              # Domain, complexity, skills, etc.

# Auto-mode configuration
config = bundle.auto_mode_config
print(config["max_turns"])          # Based on complexity
print(config["initial_prompt"])     # Generated execution prompt
print(config["success_criteria"])   # From goal definition
print(config["constraints"])        # From goal definition
```

Auto-mode configuration:

- `max_turns`: 5 (simple), 10 (moderate), 15 (complex), +20% per extra phase
- `initial_prompt`: Full markdown prompt with goal, plan, success criteria
- `working_dir`: Current directory
- `sdk`: "claude" (default)
- `ui_mode`: False (headless by default)

### GoalAgentPackager Details

Packages bundle for deployment:

```python
from amplihack.goal_agent_generator import GoalAgentPackager
from pathlib import Path

packager = GoalAgentPackager()
packager.package(
    bundle=agent_bundle,
    output_dir=Path(".claude/agents/goal-driven/my-agent")
)

# Creates:
# .claude/agents/goal-driven/my-agent/
# ├── agent.md           # Agent definition
# ├── prompt.md          # Initial prompt
# ├── metadata.json      # Bundle metadata
# ├── plan.yaml          # Execution plan
# └── skills.yaml        # Required skills
```

## 5. Recent Amplihack Examples

Real goal-seeking agents from the amplihack project:

### Example 1: AKS SRE Automation (Issue #1293)

**Problem**: Manual AKS cluster operations are time-consuming and error-prone

**Goal-Seeking Solution**:

```python
# Goal: Automate AKS production readiness verification
goal = """
Verify AKS cluster production readiness:
- Security: RBAC, network policies, Key Vault integration
- Networking: Ingress, DNS, load balancers
- Monitoring: Container Insights, alerts, dashboards
- Compliance: Azure Policy, resource quotas
Generate actionable report with recommendations.
"""

# Agent decomposes into phases:
# 1. Security Audit (parallel): RBAC check, network policies, Key Vault
# 2. Networking Validation (parallel): Ingress test, DNS resolution, LB health
# 3. Monitoring Verification (parallel): Metrics, logs, alerts configured
# 4. Compliance Check (depends on 1-3): Azure Policy, quotas, best practices
# 5. Report Generation (depends on 4): Markdown report with findings

# Agent adapts based on findings:
# - If security issues found: Suggest fixes, offer to apply
# - If monitoring missing: Generate alert templates
# - If compliance violations: List remediation steps
```

**Key Characteristics**:

- **Autonomous**: Checks multiple systems without step-by-step instructions
- **Adaptive**: Investigation depth varies by findings
- **Multi-Phase**: Parallel security/networking/monitoring, sequential reporting
- **Domain Expert**: Azure + Kubernetes knowledge embedded
- **Self-Assessing**: Validates each check, aggregates results

**Implementation**:

```python
# Located in: .claude/agents/amplihack/specialized/azure-kubernetes-expert.md
# Uses knowledge base: .claude/data/azure_aks_expert/

# Integrates with goal_agent_generator:
from amplihack.goal_agent_generator import (
    PromptAnalyzer, ObjectivePlanner, AgentAssembler
)

analyzer = PromptAnalyzer()
goal_def = analyzer.analyze_text(goal)

planner = ObjectivePlanner()
plan = planner.generate_plan(goal_def)  # Generates 5-phase plan

# Domain-specific customization:
plan.phases[0].required_capabilities = [
    "rbac-audit", "network-policy-check", "key-vault-integration"
]
```

**Lessons Learned**:

- Domain expertise critical for complex infrastructure
- Parallel execution significantly reduces total time
- Actionable recommendations increase agent value
- Comprehensive knowledge base (Q&A format) enables autonomous decisions

### Example 2: CI Diagnostic Workflow

**Problem**: CI failures require manual diagnosis and fix iteration

**Goal-Seeking Solution**:

```python
# Goal: Diagnose CI failure and iterate fixes until success
goal = """
CI pipeline failing after push.
Diagnose failures, apply fixes, push updates, monitor CI.
Iterate until all checks pass.
Stop at mergeable state without auto-merging.
"""

# Agent decomposes into phases:
# 1. CI Status Monitoring: Check current CI state
# 2. Failure Diagnosis: Analyze logs, compare environments
# 3. Fix Application: Apply fixes based on failure patterns
# 4. Push and Wait: Commit fixes, push, wait for CI re-run
# 5. Success Verification: Confirm all checks pass

# Iterative loop:
# Phases 2-4 repeat until success or max iterations (5)
```

**Key Characteristics**:

- **Iterative**: Repeats fix cycle until success
- **Autonomous Recovery**: Tries multiple fix strategies
- **State Management**: Tracks attempted fixes, avoids repeating failures
- **Pattern Matching**: Recognizes common CI failure types
- **Escalation**: Reports to user after max iterations

**Implementation**:

```python
# Located in: .claude/agents/amplihack/specialized/ci-diagnostic-workflow.md

# Fix iteration loop:
MAX_ITERATIONS = 5
iteration = 0

while iteration < MAX_ITERATIONS:
    status = check_ci_status()

    if status["conclusion"] == "success":
        break

    # Diagnose failures
    failures = analyze_ci_logs(status)

    # Apply pattern-matched fixes
    for failure in failures:
        if "test" in failure["type"]:
            fix_test_failure(failure)
        elif "lint" in failure["type"]:
            fix_lint_failure(failure)
        elif "type" in failure["type"]:
            fix_type_failure(failure)

    # Commit and push
    git_commit_and_push(f"fix: CI iteration {iteration + 1}")

    # Wait for CI re-run
    wait_for_ci_completion()

    iteration += 1

if iteration >= MAX_ITERATIONS:
    escalate_to_user("CI still failing after 5 iterations")
```

**Lessons Learned**:

- Iteration limits prevent infinite loops
- Pattern matching (test/lint/type) enables targeted fixes
- Smart waiting (exponential backoff) reduces wait time
- Never auto-merge: human approval always required

### Example 3: Pre-Commit Diagnostic Workflow

**Problem**: Pre-commit hooks fail with unclear errors

**Goal-Seeking Solution**:

```python
# Goal: Fix pre-commit hook failures before commit
goal = """
Pre-commit hooks failing.
Diagnose issues (formatting, linting, type checking).
Apply fixes locally, re-run hooks.
Ensure all hooks pass before allowing commit.
"""

# Agent decomposes into phases:
# 1. Hook Failure Analysis: Identify which hooks failed
# 2. Environment Check: Compare local vs pre-commit versions
# 3. Targeted Fixes: Apply fixes per hook type
# 4. Hook Re-run: Validate fixes, iterate if needed
# 5. Commit Readiness: Confirm all hooks pass
```

**Key Characteristics**:

- **Pre-Push Focus**: Fixes issues before pushing to CI
- **Tool Version Management**: Ensures local matches pre-commit config
- **Hook-Specific Fixes**: Tailored approach per hook type
- **Fast Iteration**: No wait for CI, immediate feedback

**Implementation**:

```python
# Located in: .claude/agents/amplihack/specialized/pre-commit-diagnostic.md

# Hook failure patterns:
HOOK_FIXES = {
    "ruff": lambda: subprocess.run(["ruff", "check", "--fix", "."]),
    "black": lambda: subprocess.run(["black", "."]),
    "mypy": lambda: add_type_ignores(),
    "trailing-whitespace": lambda: subprocess.run(["pre-commit", "run", "trailing-whitespace", "--all-files"]),
}

# Execution:
failed_hooks = detect_failed_hooks()

for hook in failed_hooks:
    if hook in HOOK_FIXES:
        HOOK_FIXES[hook]()
    else:
        generic_fix(hook)

# Re-run to verify
rerun_result = subprocess.run(["pre-commit", "run", "--all-files"])
if rerun_result.returncode == 0:
    print("All hooks passing, ready to commit!")
```

**Lessons Learned**:

- Pre-commit fixes are faster than CI iteration
- Tool version mismatches are common culprit
- Automated fixes for 80% of cases
- Remaining 20% escalate with clear diagnostics

### Example 4: Fix-Agent Pattern Matching

**Problem**: Different issues require different fix approaches

**Goal-Seeking Solution**:

```python
# Goal: Select optimal fix strategy based on problem context
goal = """
Analyze issue and select fix mode:
- QUICK: Obvious fixes (< 5 min)
- DIAGNOSTIC: Unclear root cause (investigation)
- COMPREHENSIVE: Complex issues (full workflow)
"""

# Agent decomposes into phases:
# 1. Issue Analysis: Classify problem type and complexity
# 2. Mode Selection: Choose QUICK/DIAGNOSTIC/COMPREHENSIVE
# 3. Fix Execution: Apply mode-appropriate strategy
# 4. Validation: Verify fix resolves issue
```

**Key Characteristics**:

- **Context-Aware**: Selects strategy based on problem analysis
- **Multi-Mode**: Three fix modes for different complexity levels
- **Pattern Recognition**: Learns from past fixes
- **Adaptive**: Escalates complexity if initial mode fails

**Implementation**:

```python
# Located in: .claude/agents/amplihack/specialized/fix-agent.md

# Mode selection logic:
def select_fix_mode(issue: Issue) -> FixMode:
    if issue.is_obvious() and issue.scope == "single-file":
        return FixMode.QUICK
    elif issue.root_cause_unclear():
        return FixMode.DIAGNOSTIC
    elif issue.is_complex() or issue.requires_architecture_change():
        return FixMode.COMPREHENSIVE
    else:
        return FixMode.DIAGNOSTIC  # Default to investigation

# Pattern frequency (from real usage):
FIX_PATTERNS = {
    "import": 0.15,      # Import errors (15%)
    "config": 0.12,      # Configuration issues (12%)
    "test": 0.18,        # Test failures (18%)
    "ci": 0.20,          # CI/CD problems (20%)
    "quality": 0.25,     # Code quality (linting, types) (25%)
    "logic": 0.10,       # Logic errors (10%)
}

# Template-based fixes for common patterns:
if issue.pattern == "import":
    apply_template("import-fix-template", issue)
elif issue.pattern == "config":
    apply_template("config-fix-template", issue)
# ... etc
```

**Lessons Learned**:

- Pattern matching enables template-based fixes (80% coverage)
- Mode selection reduces over-engineering (right-sized approach)
- Diagnostic mode critical for unclear issues (root cause analysis)
- Usage data informs template priorities

## 6. Design Checklist

Use this checklist when designing goal-seeking agents:

### Goal Definition

- [ ] Objective is clear and well-defined
- [ ] Success criteria are measurable and verifiable
- [ ] Constraints are explicit (time, resources, safety)
- [ ] Domain is identified (impacts phase templates)
- [ ] Complexity is estimated (simple/moderate/complex)

### Phase Design

- [ ] Decomposed into 3-5 phases (not too granular, not too coarse)
- [ ] Phase dependencies are explicit
- [ ] Parallel execution opportunities identified
- [ ] Each phase has clear success indicators
- [ ] Phase durations are estimated

### Skill Mapping

- [ ] Required capabilities identified per phase
- [ ] Skills mapped to existing agents or tools
- [ ] Delegation targets specified
- [ ] No missing capabilities

### Error Handling

- [ ] Retry strategies defined (max attempts, backoff)
- [ ] Alternative strategies identified
- [ ] Escalation criteria clear (when to ask for help)
- [ ] Graceful degradation options (fallback approaches)

### State Management

- [ ] State tracked across phases
- [ ] Phase results stored for downstream use
- [ ] Failure history maintained
- [ ] Context shared appropriately

### Testing

- [ ] Success scenarios tested
- [ ] Failure recovery tested
- [ ] Edge cases identified
- [ ] Performance validated (duration, resource usage)

### Documentation

- [ ] Goal clearly documented
- [ ] Phase descriptions complete
- [ ] Usage examples provided
- [ ] Integration points specified

### Philosophy Compliance

- [ ] Ruthless simplicity (no unnecessary complexity)
- [ ] Single responsibility per phase
- [ ] No over-engineering (right-sized solution)
- [ ] Regeneratable (clear specifications)

## 7. Agent SDK Integration (Future)

When the Agent SDK Skill is integrated, goal-seeking agents can leverage:

### Enhanced Autonomy

```python
# Agent SDK provides enhanced context management
from claude_agent_sdk import AgentContext, Tool

class GoalSeekingAgent:
    def __init__(self, context: AgentContext):
        self.context = context
        self.state = {}

    async def execute_phase(self, phase: PlanPhase):
        # SDK provides tools, memory, delegation
        tools = self.context.get_tools(phase.required_capabilities)
        memory = self.context.get_memory()

        # Execute with SDK support
        result = await phase.execute(tools, memory)

        # Store in context for downstream phases
        self.context.store_result(phase.name, result)
```

### Tool Discovery

```python
# SDK enables dynamic tool discovery
available_tools = context.discover_tools(capability="data-processing")

# Select optimal tool for task
tool = context.select_tool(
    capability="data-transformation",
    criteria={"performance": "high", "accuracy": "required"}
)
```

### Memory Management

```python
# SDK provides persistent memory across sessions
context.memory.store("deployment-history", deployment_record)
previous = context.memory.retrieve("deployment-history")

# Enables learning from past executions
if previous and previous.failed:
    # Avoid previous failure strategy
    strategy = select_alternative_strategy(previous.failure_reason)
```

### Agent Delegation

```python
# SDK simplifies agent-to-agent delegation
result = await context.delegate(
    agent="security-analyzer",
    task="audit-rbac-policies",
    input={"cluster": cluster_name}
)

# Parallel delegation
results = await context.delegate_parallel([
    ("security-analyzer", "audit-rbac-policies"),
    ("network-analyzer", "validate-ingress"),
    ("monitoring-validator", "check-metrics")
])
```

### Observability

```python
# SDK provides built-in tracing and metrics
with context.trace("data-transformation"):
    result = transform_data(input_data)

context.metrics.record("transformation-duration", duration)
context.metrics.record("transformation-accuracy", accuracy)
```

### Integration Example

```python
from claude_agent_sdk import AgentContext, create_agent
from amplihack.goal_agent_generator import GoalAgentBundle

# Create SDK-enabled goal-seeking agent
def create_goal_agent(bundle: GoalAgentBundle) -> Agent:
    context = AgentContext(
        name=bundle.name,
        version=bundle.version,
        capabilities=bundle.metadata["required_capabilities"]
    )

    # Register phases as agent tasks
    for phase in bundle.execution_plan.phases:
        context.register_task(
            name=phase.name,
            capabilities=phase.required_capabilities,
            executor=create_phase_executor(phase)
        )

    # Create agent with SDK
    agent = create_agent(context)

    # Execute goal
    return agent

# Usage:
agent = create_goal_agent(agent_bundle)
result = await agent.execute(bundle.auto_mode_config["initial_prompt"])
```

## 8. Trade-Off Analysis

### Goal-Seeking vs Traditional Agents

| Dimension            | Goal-Seeking Agent                    | Traditional Agent         |
| -------------------- | ------------------------------------- | ------------------------- |
| **Flexibility**      | High - adapts to context              | Low - fixed workflow      |
| **Development Time** | Moderate - define goals & phases      | Low - script steps        |
| **Execution Time**   | Higher - decision overhead            | Lower - direct execution  |
| **Maintenance**      | Lower - self-adapting                 | Higher - manual updates   |
| **Debuggability**    | Harder - dynamic behavior             | Easier - predictable flow |
| **Reusability**      | High - same agent, different contexts | Low - context-specific    |
| **Failure Handling** | Autonomous recovery                   | Manual intervention       |
| **Complexity**       | Higher - multi-phase coordination     | Lower - linear execution  |

### When to Choose Each

**Choose Goal-Seeking when**:

- Problem space is large with many valid approaches
- Context varies significantly across executions
- Autonomous recovery is valuable
- Reusability across contexts is important
- Development time investment is justified

**Choose Traditional when**:

- Single deterministic path exists
- Performance is critical (low latency required)
- Simplicity is paramount
- One-off or rare execution
- Debugging and auditability are critical

### Cost-Benefit Analysis

**Goal-Seeking Costs**:

- Higher development time (define goals, phases, capabilities)
- Increased execution time (decision overhead)
- More complex testing (dynamic behavior)
- Harder debugging (non-deterministic paths)

**Goal-Seeking Benefits**:

- Autonomous operation (less human intervention)
- Adaptive to context (works in varied conditions)
- Reusable across problems (same agent, different goals)
- Self-recovering (handles failures gracefully)

**Break-Even Point**: Goal-seeking justified when problem is:

- Repeated 2+ times per week, OR
- Takes 30+ minutes manual execution, OR
- Requires expert knowledge hard to document, OR
- High value from autonomous recovery

## 9. When to Escalate

Goal-seeking agents should escalate to humans when:

### Hard Limits Reached

**Max Iterations Exceeded**:

```python
if iteration_count >= MAX_ITERATIONS:
    escalate(
        reason="Reached maximum iterations without success",
        context={
            "iterations": iteration_count,
            "attempted_strategies": attempted_strategies,
            "last_error": last_error
        }
    )
```

**Timeout Exceeded**:

```python
if elapsed_time > MAX_DURATION:
    escalate(
        reason="Execution time exceeded limit",
        context={
            "elapsed": elapsed_time,
            "max_allowed": MAX_DURATION,
            "completed_phases": completed_phases
        }
    )
```

### Safety Boundaries

**Destructive Operations**:

```python
if operation.is_destructive() and not operation.has_approval():
    escalate(
        reason="Destructive operation requires human approval",
        operation=operation.description,
        impact=operation.estimate_impact()
    )
```

**Production Changes**:

```python
if target_environment == "production":
    escalate(
        reason="Production deployments require human verification",
        changes=proposed_changes,
        rollback_plan=rollback_strategy
    )
```

### Uncertainty Detection

**Low Confidence**:

```python
if decision_confidence < CONFIDENCE_THRESHOLD:
    escalate(
        reason="Confidence below threshold for autonomous decision",
        decision=decision_description,
        confidence=decision_confidence,
        alternatives=alternative_options
    )
```

**Conflicting Strategies**:

```python
if len(viable_strategies) > 1 and not clear_winner:
    escalate(
        reason="Multiple viable strategies, need human judgment",
        strategies=viable_strategies,
        trade_offs=strategy_trade_offs
    )
```

### Unexpected Conditions

**Unrecognized Errors**:

```python
if error_type not in KNOWN_ERROR_PATTERNS:
    escalate(
        reason="Encountered unknown error pattern",
        error=error_details,
        context=execution_context,
        recommendation="Manual investigation required"
    )
```

**Environment Mismatch**:

```python
if detected_environment != expected_environment:
    escalate(
        reason="Environment mismatch detected",
        expected=expected_environment,
        detected=detected_environment,
        risk="Potential for incorrect behavior"
    )
```

### Escalation Best Practices

**Provide Context**:

- What was attempted
- What failed and why
- What alternatives were considered
- Current system state

**Suggest Actions**:

- Recommend next steps
- Provide diagnostic commands
- Offer manual intervention points
- Suggest rollback if needed

**Enable Recovery**:

- Save execution state
- Document failures
- Provide resume capability
- Offer manual override

**Example Escalation**:

```python
escalate(
    reason="CI failure diagnosis unsuccessful after 5 iterations",
    context={
        "iterations": 5,
        "attempted_fixes": [
            "Import path corrections (iteration 1)",
            "Type annotation fixes (iteration 2)",
            "Test environment setup (iteration 3)",
            "Dependency version pins (iteration 4)",
            "Mock configuration (iteration 5)"
        ],
        "persistent_failures": [
            "test_integration.py::test_api_connection - Timeout",
            "test_models.py::test_validation - Assertion error"
        ],
        "system_state": "2 of 25 tests still failing",
        "ci_logs": "https://github.com/.../actions/runs/123456"
    },
    recommendations=[
        "Review test_api_connection timeout - may need increased timeout or mock",
        "Examine test_validation assertion - data structure may have changed",
        "Consider running tests locally with same environment as CI",
        "Check if recent changes affected integration test setup"
    ],
    next_steps={
        "manual_investigation": "Run failing tests locally with verbose output",
        "rollback_option": "git revert HEAD~5 if fixes made things worse",
        "resume_point": "Fix failures and run /amplihack:ci-diagnostic to resume"
    }
)
```

## 10. Example Workflow

Complete example: Building a goal-seeking agent for data pipeline automation

### Step 1: Define Goal

```markdown
# Goal: Automate Multi-Source Data Pipeline

## Objective

Collect data from multiple sources (S3, database, API), transform to common schema, validate quality, publish to data warehouse.

## Success Criteria

- All sources successfully ingested
- Data transformed to target schema
- Quality checks pass (completeness, accuracy)
- Data published to warehouse
- Pipeline completes within 30 minutes

## Constraints

- Must handle source unavailability gracefully
- No data loss (failed records logged)
- Idempotent (safe to re-run)
- Resource limits: 8GB RAM, 4 CPU cores

## Context

- Daily execution (automated schedule)
- Priority: High (blocking downstream analytics)
- Scale: Medium (100K-1M records per source)
```

### Step 2: Analyze with PromptAnalyzer

```python
from amplihack.goal_agent_generator import PromptAnalyzer

analyzer = PromptAnalyzer()
goal_definition = analyzer.analyze_text(goal_text)

# Result:
# goal_definition.goal = "Automate Multi-Source Data Pipeline"
# goal_definition.domain = "data-processing"
# goal_definition.complexity = "moderate"
# goal_definition.constraints = [
#     "Must handle source unavailability gracefully",
#     "No data loss (failed records logged)",
#     "Idempotent (safe to re-run)",
#     "Resource limits: 8GB RAM, 4 CPU cores"
# ]
# goal_definition.success_criteria = [
#     "All sources successfully ingested",
#     "Data transformed to target schema",
#     "Quality checks pass (completeness, accuracy)",
#     "Data published to warehouse",
#     "Pipeline completes within 30 minutes"
# ]
```

### Step 3: Generate Plan with ObjectivePlanner

```python
from amplihack.goal_agent_generator import ObjectivePlanner

planner = ObjectivePlanner()
execution_plan = planner.generate_plan(goal_definition)

# Result: 4-phase plan
# Phase 1: Data Collection (parallel)
#   - Collect from S3 (parallel-safe)
#   - Collect from database (parallel-safe)
#   - Collect from API (parallel-safe)
#   Duration: 15 minutes
#   Success: All sources attempted, failures logged
#
# Phase 2: Data Transformation (depends on Phase 1)
#   - Parse raw data
#   - Transform to common schema
#   - Handle missing fields
#   Duration: 15 minutes
#   Success: All records transformed or logged as failed
#
# Phase 3: Quality Validation (depends on Phase 2)
#   - Completeness check
#   - Accuracy validation
#   - Consistency verification
#   Duration: 5 minutes
#   Success: Quality thresholds met
#
# Phase 4: Data Publishing (depends on Phase 3)
#   - Load to warehouse
#   - Update metadata
#   - Generate report
#   Duration: 10 minutes
#   Success: Data in warehouse, report generated
```

### Step 4: Synthesize Skills

```python
from amplihack.goal_agent_generator import SkillSynthesizer

synthesizer = SkillSynthesizer()
skills = synthesizer.synthesize(execution_plan)

# Result: 3 skills
# Skill 1: data-collector
#   Capabilities: ["s3-read", "database-query", "api-fetch"]
#   Implementation: "native" (built-in)
#
# Skill 2: data-transformer
#   Capabilities: ["parsing", "schema-mapping", "validation"]
#   Implementation: "native" (built-in)
#
# Skill 3: data-publisher
#   Capabilities: ["warehouse-load", "metadata-update", "reporting"]
#   Implementation: "delegated" (delegates to warehouse tool)
```

### Step 5: Assemble Agent

```python
from amplihack.goal_agent_generator import AgentAssembler

assembler = AgentAssembler()
agent_bundle = assembler.assemble(
    goal_definition=goal_definition,
    execution_plan=execution_plan,
    skills=skills,
    bundle_name="multi-source-data-pipeline"
)

# Result: GoalAgentBundle
# - Name: multi-source-data-pipeline
# - Max turns: 12 (moderate complexity, 4 phases)
# - Initial prompt: Full execution plan with phases
# - Status: "ready"
```

### Step 6: Package Agent

```python
from amplihack.goal_agent_generator import GoalAgentPackager
from pathlib import Path

packager = GoalAgentPackager()
packager.package(
    bundle=agent_bundle,
    output_dir=Path(".claude/agents/goal-driven/multi-source-data-pipeline")
)

# Creates agent package:
# .claude/agents/goal-driven/multi-source-data-pipeline/
# ├── agent.md           # Agent definition
# ├── prompt.md          # Execution prompt
# ├── metadata.json      # Bundle metadata
# ├── plan.yaml          # Execution plan (4 phases)
# └── skills.yaml        # 3 required skills
```

### Step 7: Execute Agent (Auto-Mode)

```bash
# Execute via CLI
amplihack goal-agent-generator execute \
  --agent-path .claude/agents/goal-driven/multi-source-data-pipeline \
  --auto-mode \
  --max-turns 12

# Or programmatically:
```

```python
from claude_code import execute_auto_mode

result = execute_auto_mode(
    initial_prompt=agent_bundle.auto_mode_config["initial_prompt"],
    max_turns=agent_bundle.auto_mode_config["max_turns"],
    working_dir=agent_bundle.auto_mode_config["working_dir"]
)
```

### Step 8: Monitor Execution

Agent executes autonomously:

```
Phase 1: Data Collection [In Progress]
├── S3 Collection: ✓ COMPLETED (50K records, 5 minutes)
├── Database Collection: ✓ COMPLETED (75K records, 8 minutes)
└── API Collection: ✗ FAILED (timeout, retrying...)
    └── Retry 1: ✓ COMPLETED (25K records, 4 minutes)

Phase 1: ✓ COMPLETED (150K records total, 3 sources, 17 minutes)

Phase 2: Data Transformation [In Progress]
├── Parsing: ✓ COMPLETED (150K records parsed)
├── Schema Mapping: ✓ COMPLETED (148K records mapped, 2K failed)
└── Missing Fields: ✓ COMPLETED (defaults applied)

Phase 2: ✓ COMPLETED (148K records ready, 2K logged as failed, 12 minutes)

Phase 3: Quality Validation [In Progress]
├── Completeness: ✓ PASS (98.7% complete, threshold 95%)
├── Accuracy: ✓ PASS (99.2% accurate, threshold 98%)
└── Consistency: ✓ PASS (100% consistent)

Phase 3: ✓ COMPLETED (All checks passed, 4 minutes)

Phase 4: Data Publishing [In Progress]
├── Warehouse Load: ✓ COMPLETED (148K records loaded)
├── Metadata Update: ✓ COMPLETED (pipeline_run_id: 12345)
└── Report Generation: ✓ COMPLETED (report.html)

Phase 4: ✓ COMPLETED (Data published, 8 minutes)

Total Execution: ✓ SUCCESS (41 minutes, all success criteria met)
```

### Step 9: Review Results

```markdown
# Pipeline Execution Report

## Summary

- **Status**: SUCCESS
- **Duration**: 41 minutes (estimated: 30 minutes)
- **Records Processed**: 150K ingested, 148K published
- **Success Rate**: 98.7%

## Phase Results

### Phase 1: Data Collection

- S3: 50K records (5 min)
- Database: 75K records (8 min)
- API: 25K records (4 min, 1 retry)

### Phase 2: Data Transformation

- Successfully transformed: 148K records
- Failed transformations: 2K records (logged to failed_records.log)
- Failure reasons: Schema mismatch (1.5K), Invalid data (500)

### Phase 3: Quality Validation

- Completeness: 98.7% ✓
- Accuracy: 99.2% ✓
- Consistency: 100% ✓

### Phase 4: Data Publishing

- Warehouse load: Success
- Pipeline run ID: 12345
- Report: report.html

## Issues Encountered

1. API timeout (Phase 1): Resolved with retry
2. 2K transformation failures: Logged for manual review

## Recommendations

1. Investigate schema mismatches in API data
2. Add validation for API data format
3. Consider increasing timeout for API calls
```

### Step 10: Iteration (If Needed)

If pipeline fails, agent adapts:

```python
# Example: API source completely unavailable
if phase1_result["api"]["status"] == "unavailable":
    # Agent adapts: continues with partial data
    log_warning("API source unavailable, continuing with S3 + database")
    proceed_to_phase2_with_partial_data()

    # Report notes partial data
    add_to_report("Data incomplete: API source unavailable")

# Example: Quality validation fails
if phase3_result["completeness"] < THRESHOLD:
    # Agent tries recovery: fetch missing data
    missing_records = identify_missing_records()
    retry_collection_for_missing(missing_records)
    rerun_transformation()
    rerun_validation()

    # If still fails after retry, escalate
    if still_below_threshold:
        escalate("Quality threshold not met after retry")
```

## 11. Related Patterns

Goal-seeking agents relate to and integrate with other patterns:

### Debate Pattern (Multi-Agent Decision Making)

**When to Combine**:

- Goal-seeking agent faces complex decision with trade-offs
- Multiple valid approaches exist
- Need consensus from different perspectives

**Example**:

```python
# Goal-seeking agent reaches decision point
if len(viable_strategies) > 1:
    # Invoke debate pattern
    result = invoke_debate(
        question="Which data transformation approach?",
        perspectives=["performance", "accuracy", "simplicity"],
        context=current_state
    )

    # Use debate result to select strategy
    selected_strategy = result.consensus
```

### N-Version Pattern (Redundant Implementation)

**When to Combine**:

- Goal-seeking agent executing critical phase
- Error cost is high
- Multiple independent implementations possible

**Example**:

```python
# Critical security validation phase
if phase.is_critical():
    # Generate N versions
    results = generate_n_versions(
        phase=phase,
        n=3,
        independent=True
    )

    # Use voting or comparison to select result
    validated_result = compare_and_validate(results)
```

### Cascade Pattern (Fallback Strategies)

**When to Combine**:

- Goal-seeking agent has preferred approach but needs fallbacks
- Quality/performance trade-offs exist
- Graceful degradation desired

**Example**:

```python
# Data transformation with fallback
try:
    # Optimal: ML-based transformation
    result = ml_transform(data)
except MLModelUnavailable:
    try:
        # Pragmatic: Rule-based transformation
        result = rule_based_transform(data)
    except RuleEngineError:
        # Minimal: Manual templates
        result = template_transform(data)
```

### Investigation Workflow (Knowledge Discovery)

**When to Combine**:

- Goal requires understanding existing system
- Need to discover architecture or patterns
- Knowledge excavation before execution

**Example**:

```python
# Before automating deployment, understand current system
if goal.requires_system_knowledge():
    # Run investigation workflow
    investigation = run_investigation_workflow(
        scope="deployment pipeline",
        depth="comprehensive"
    )

    # Use findings to inform goal-seeking execution
    adapt_plan_based_on_investigation(investigation.findings)
```

### Document-Driven Development (Specification First)

**When to Combine**:

- Goal-seeking agent generates or modifies code
- Clear specifications prevent drift
- Documentation is single source of truth

**Example**:

```python
# Goal: Implement new feature
if goal.involves_code_changes():
    # DDD Phase 1: Generate specifications
    specs = generate_specifications(goal)

    # DDD Phase 2: Review and approve specs
    await human_review(specs)

    # Goal-seeking agent implements from specs
    implementation = execute_from_specifications(specs)
```

### Pre-Commit / CI Diagnostic (Quality Gates)

**When to Combine**:

- Goal-seeking agent makes code changes
- Need to ensure quality before commit/push
- Automated validation and fixes

**Example**:

```python
# After goal-seeking agent generates code
if changes_made:
    # Run pre-commit diagnostic
    pre_commit_result = run_pre_commit_diagnostic()

    if pre_commit_result.has_failures():
        # Agent fixes issues
        apply_pre_commit_fixes(pre_commit_result.failures)

    # After push, run CI diagnostic
    ci_result = run_ci_diagnostic_workflow()

    if ci_result.has_failures():
        # Agent iterates fixes
        iterate_ci_fixes_until_pass(ci_result)
```

## 12. Quality Standards

Goal-seeking agents must meet these quality standards:

### Correctness

**Success Criteria Verification**:

- [ ] Agent verifies all success criteria before completion
- [ ] Intermediate phase results validated
- [ ] No silent failures (all errors logged and handled)

**Testing Coverage**:

- [ ] Happy path tested (all success criteria met)
- [ ] Failure scenarios tested (phase failures, retries)
- [ ] Edge cases identified and tested
- [ ] Integration with real systems validated

### Resilience

**Error Handling**:

- [ ] Retry logic with exponential backoff
- [ ] Alternative strategies for common failures
- [ ] Graceful degradation when optimal path unavailable
- [ ] Clear escalation criteria

**State Management**:

- [ ] State persisted across phase boundaries
- [ ] Resume capability after failures
- [ ] Idempotent execution (safe to re-run)
- [ ] Cleanup on abort

### Performance

**Efficiency**:

- [ ] Phases execute in parallel when possible
- [ ] No unnecessary work (skip completed phases on retry)
- [ ] Resource usage within limits (memory, CPU, time)
- [ ] Timeout limits enforced

**Latency**:

- [ ] Decision overhead acceptable for use case
- [ ] No blocking waits (async where possible)
- [ ] Progress reported (no black box periods)

### Observability

**Logging**:

- [ ] Phase transitions logged
- [ ] Decisions logged with reasoning
- [ ] Errors logged with context
- [ ] Results logged with metrics

**Metrics**:

- [ ] Duration per phase tracked
- [ ] Success/failure rates tracked
- [ ] Resource usage monitored
- [ ] Quality metrics reported

**Tracing**:

- [ ] Execution flow traceable
- [ ] Correlations across phases maintained
- [ ] Debugging information sufficient

### Usability

**Documentation**:

- [ ] Goal clearly stated
- [ ] Success criteria documented
- [ ] Usage examples provided
- [ ] Integration guide complete

**User Experience**:

- [ ] Clear progress reporting
- [ ] Actionable error messages
- [ ] Human-readable outputs
- [ ] Easy to invoke and monitor

### Philosophy Compliance

**Ruthless Simplicity**:

- [ ] No unnecessary phases or complexity
- [ ] Simplest approach that works
- [ ] No premature optimization

**Single Responsibility**:

- [ ] Each phase has one clear job
- [ ] No overlapping responsibilities
- [ ] Clean phase boundaries

**Modularity**:

- [ ] Skills are reusable across agents
- [ ] Phases are independent
- [ ] Clear interfaces (inputs/outputs)

**Regeneratable**:

- [ ] Can be rebuilt from specifications
- [ ] No hardcoded magic values
- [ ] Configuration externalized

## 13. Getting Started

### Quick Start: Build Your First Goal-Seeking Agent

**Step 1**: Install amplihack (if not already)

```bash
pip install amplihack
```

**Step 2**: Write a goal prompt

```bash
cat > my-goal.md << 'EOF'
# Goal: Automated Security Audit

Check application for common security issues:
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure dependencies
- Missing security headers

Generate report with severity levels and remediation steps.
EOF
```

**Step 3**: Generate agent

```bash
amplihack goal-agent-generator create \
  --prompt my-goal.md \
  --output .claude/agents/goal-driven/security-auditor
```

**Step 4**: Review generated plan

```bash
cat .claude/agents/goal-driven/security-auditor/plan.yaml
```

**Step 5**: Execute agent

```bash
amplihack goal-agent-generator execute \
  --agent-path .claude/agents/goal-driven/security-auditor \
  --auto-mode
```

### Common Use Cases

**Use Case 1: Workflow Automation**

```bash
# Create release automation agent
echo "Automate release workflow: tag, build, test, deploy to staging" | \
  amplihack goal-agent-generator create --inline --output .claude/agents/goal-driven/release-automator
```

**Use Case 2: Data Pipeline**

```bash
# Create ETL pipeline agent
echo "Extract from sources, transform to schema, validate quality, load to warehouse" | \
  amplihack goal-agent-generator create --inline --output .claude/agents/goal-driven/etl-pipeline
```

**Use Case 3: Diagnostic Workflow**

```bash
# Create performance diagnostic agent
echo "Diagnose application performance issues, identify bottlenecks, suggest optimizations" | \
  amplihack goal-agent-generator create --inline --output .claude/agents/goal-driven/perf-diagnostic
```

### Learning Resources

**Documentation**:

- Review examples in `.claude/skills/goal-seeking-agent-pattern/examples/`
- Read real agent implementations in `.claude/agents/amplihack/specialized/`
- Check integration guide in `.claude/skills/goal-seeking-agent-pattern/templates/integration_guide.md`

**Practice**:

1. Start simple: Build single-phase agent (e.g., file formatter)
2. Add complexity: Build multi-phase agent (e.g., test generator + runner)
3. Add autonomy: Build agent with error recovery (e.g., CI fixer)
4. Build production: Build full goal-seeking agent (e.g., deployment pipeline)

**Get Help**:

- Review decision framework (Section 2)
- Check design checklist (Section 6)
- Study real examples (Section 5)
- Ask architect agent for guidance

### Next Steps

After building your first goal-seeking agent:

1. **Test thoroughly**: Cover success, failure, and edge cases
2. **Monitor in production**: Track metrics, logs, failures
3. **Iterate**: Refine based on real usage
4. **Document learnings**: Update DISCOVERIES.md with insights
5. **Share patterns**: Add successful approaches to PATTERNS.md

**Success Indicators**:

- Agent completes goal autonomously 80%+ of time
- Failures escalate with clear context
- Execution time is acceptable
- Users trust agent to run autonomously

---

**Remember**: Goal-seeking agents should be ruthlessly simple, focused on clear objectives, and adaptive to context. Start simple, add complexity only when justified, and always verify against success criteria.
