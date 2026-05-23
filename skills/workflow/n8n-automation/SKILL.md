---
name: n8n-automation
description: n8n workflow automation for building analytics including SkySpark multi-agent systems, FastAPI tool servers, workflow orchestration, and automated building system alert triage
---

# n8n Automation Skill

This skill provides expertise in building automation workflows using n8n, specifically focused on SkySpark integration and multi-agent systems for building analytics.

## Core Capabilities

### SkySpark Multi-Agent Architecture
- Gatekeeper agent with specialist routing
- Automated spark triage and prioritization
- HVAC specialist for mechanical system analysis
- Energy calculation agent for savings estimates
- Automated report generation workflows

### n8n Workflow Development
- REST API integrations with building systems
- Multi-agent coordination patterns
- Error handling and logging strategies
- Scheduled automation and notifications

### SkySpark Integration
- Haystack REST API connectivity
- ZINC and JSON data format handling
- Spark and trend data extraction
- Authentication and security patterns

## Available Scripts
- scripts/fastapi_tool_server.py: Template for FastAPI tool servers
- scripts/n8n_workflow_templates/: Common workflow patterns
- scripts/skyspark_mock_data.py: Generate test data for development

## Reference Materials
- references/multi_agent_patterns.md: Proven multi-agent architectures
- references/skyspark_api.md: SkySpark Haystack API documentation
- references/n8n_best_practices.md: Workflow development guidelines
- references/roadmap.md: 5-phase project roadmap (Foundation → Production)

## Asset Templates
- assets/workflow_exports/: n8n workflow export files
- assets/api_schemas/: OpenAPI schemas for tool servers
- assets/mock_data/: Sample SkySpark data for testing

## Current Project: SkySpark Multi-Agent System

### 5-Phase Roadmap
1. **Foundation**: FastAPI tool server + basic agent interaction
2. **Mock Integration**: Agent logic with simulated SkySpark data
3. **Real SkySpark**: Live Haystack API connection
4. **Multi-Agent**: Full specialist coordination
5. **Production**: Error handling, scheduling, notifications

### Multi-Agent Pattern
```
User Request → Gatekeeper Agent (routes by intent)
                ↓
    ┌───────────┼───────────┬──────────────┐
    ↓           ↓           ↓              ↓
Triage      HVAC        Energy         Report
Agent       Specialist  Calc Agent     Generator
```

## Agent Architecture for Future RL Orchestration

### Stateless Agent Design Principles
All SkySpark agents should be designed with future dynamic orchestration in mind:

**Statelessness Requirements:**
- Agents receive complete diagnostic context as input (no persistent memory)
- All necessary context passed in, new state returned out
- Enables any agent to follow any agent (maximum routing flexibility)
- Simplifies debugging and testing

**Standardized I/O Schema:**

Input: `DiagnosticState` object containing:
- `alert_context`: Current alert/issue details (Haystack tags, spark data)
- `prior_actions`: Array of prior agent outputs/reasoning
- `available_tools`: List of tool endpoints and capabilities
- `token_budget_remaining`: Tokens available for continued diagnosis
- `confidence_score`: Current diagnostic confidence (0.0-1.0)
- `metadata`: Alert severity, facility info, timestamps

Output: `AgentResponse` object containing:
- `updated_state`: Refreshed DiagnosticState with new findings
- `agent_findings`: This agent's analysis, calculations, or actions
- `recommended_next_agents`: Suggested routing (even if not used in Phase 0-1)
- `token_cost`: Tokens consumed by this agent call
- `confidence_delta`: Change in diagnostic confidence (+/- 0.0-1.0)
- `actions_taken`: List of tools called or queries executed

**Role-Based Architecture:**
Separate agent identity (role prompts) from action logic:

*Tool-Use Agents:*
- `SkySpark_Query_Agent`: Execute Axon queries against SkySpark database
- `Python_Analysis_Agent`: Statistical analysis, calculations, trending
- `File_Reader_Agent`: Parse equipment specs, CSV logs, JSON configs
- `Weather_Data_Agent`: Fetch external weather data via API
- `Documentation_Agent`: Search equipment manuals, ASHRAE standards

*Reasoning Agents:*
- `Diagnostic_Planner_Agent`: Decompose complex issues into sub-diagnostics
- `Root_Cause_Analyzer_Agent`: Synthesize data to identify probable causes
- `Validation_Agent`: Verify diagnostic logic and calculations
- `Reflection_Agent`: Assess diagnostic trajectory, propose refinements
- `Summary_Agent`: Generate concise diagnostic reports
- `Resolution_Agent`: Recommend corrective actions
- `Modification_Agent`: Correct errors in prior reasoning

### Orchestration Evolution Roadmap

**Phase 0-1: Static n8n Workflows (Current)**
- Hardcoded agent routing via n8n nodes is acceptable
- BUT design workflows to call centralized routing functions
- Log every routing decision with full context
- Focus: Get agents working with standardized I/O

**Phase 2-3: Rule-Based Orchestrator**
- Implement `agent_router` function (Python/FastAPI endpoint)
- Route based on: alert type/severity, confidence score, prior sequence
- Manually tune rules based on logged diagnostic patterns
- A/B test against static workflows
- Focus: Data-driven routing without ML complexity

**Phase 4-5: RL-Based Orchestrator**
- Replace rule-based router with learned policy
- Train on logged diagnostic trajectories (minimum 200 episodes)
- Optimize for: `R = accuracy - λ × token_cost - β × time_penalty`
- Enable online learning from production outcomes
- Focus: Continuous optimization and adaptation

### Instrumentation & Logging Requirements

**Critical: Start logging from Day 1, even with static workflows**

Log every diagnostic episode with schema:
```json
{
  "episode_id": "alert_123456_2025-12-02",
  "facility_name": "Building XYZ",
  "alert_context": {
    "alert_type": "High AHU static pressure",
    "severity": "warning",
    "haystack_refs": [...],
    "triggered_at": "2025-12-02T10:15:00Z"
  },
  "agent_sequence": [
    {
      "timestamp": "2025-12-02T10:30:00Z",
      "agent_type": "SkySpark_Query_Agent",
      "input_state": {...},
      "output_state": {...},
      "tokens_used": 1500,
      "duration_ms": 3400,
      "tools_called": ["read_trends", "eval_axon"]
    },
    ...
  ],
  "final_outcome": {
    "diagnostic_correct": true,
    "root_cause_identified": "Filter 80% loaded",
    "resolution_actions": ["Schedule filter replacement"],
    "total_tokens": 8500,
    "total_duration_ms": 15200,
    "human_intervention_required": false,
    "human_feedback": "Diagnosis accurate, action appropriate"
  }
}
```

**Storage Strategy:**
- Store in n8n database OR dedicated TimescaleDB
- Retain minimum 200 episodes per alert type for RL training
- Enable easy export for offline analysis and model training
- Version control state schemas alongside agents

**What to Log:**
- Complete agent call sequence per diagnostic episode
- Full input/output states at each step
- Token consumption per agent (measure via API or estimate)
- Human validation/corrections (critical for reward labels)
- Final diagnostic outcome and resolution effectiveness
- Time to resolution relative to SLA thresholds

### Reward Function Design

**Preliminary specification for future RL training:**

```
R = accuracy_score - λ × token_cost - β × time_penalty
```

Where:
- `accuracy_score ∈ [0, 1]` - Validated against human review OR resolution outcome
- `token_cost = tokens_used / max_token_budget` - Normalized efficiency metric
- `time_penalty = max(0, (time_to_resolve / sla_threshold) - 1)` - Timeliness factor
- `λ = 0.1` - Efficiency weight (tunable based on production costs)
- `β = 0.05` - Timeliness weight (varies by alert severity)

**Accuracy Validation:**
- Binary: Did diagnostic identify correct root cause? (0 or 1)
- Graduated: Partial credit for narrowing to subsystem (0.0-1.0 scale)
- Ground truth: FM confirmation or system behavior post-resolution

**Efficiency Considerations:**
- Critical alerts: Prioritize accuracy over token cost (λ → 0)
- Informational alerts: Prioritize efficiency (λ → 0.2)
- Balance prevents both over-analysis and premature conclusions

**Timeliness Thresholds:**
- Critical: 15 min SLA → high β penalty if exceeded
- Warning: 60 min SLA → moderate β penalty
- Info: 4 hour SLA → minimal β penalty

### SkySpark Agent Taxonomy

Agents aligned with Puppeteer research categories:

**Tool-Use Agents (External data access):**
1. SkySpark_Query_Agent - Axon query execution
2. Python_Analysis_Agent - Statistical calculations, trending
3. File_Reader_Agent - Equipment specs, logs, configs
4. Weather_Data_Agent - External weather APIs
5. Documentation_Agent - Manuals, standards, knowledge base

**Reasoning Agents (Internal cognition):**
1. Diagnostic_Planner_Agent - Task decomposition
2. Root_Cause_Analyzer_Agent - Data synthesis
3. Validation_Agent - Logic verification
4. Reflection_Agent - Meta-reasoning
5. Summary_Agent - Report generation
6. Resolution_Agent - Action recommendation
7. Modification_Agent - Error correction

### Critical Don'ts

**Avoid these pitfalls:**
- ❌ Don't jump to RL before having logged data (minimum 200 episodes)
- ❌ Don't hardcode agent sequences into prompts (keep routing external)
- ❌ Don't skip instrumentation "for now" (you'll never add it later)
- ❌ Don't design agents that assume specific predecessors
- ❌ Don't sacrifice debuggability for sophistication
- ❌ Don't optimize prematurely (get working system first)
- ❌ Don't force-fit RL where rules work fine

**Do these instead:**
- ✅ Keep current n8n approach for Phase 0-1 (it's pragmatic)
- ✅ Design agents with standardized I/O from day 1
- ✅ Start logging immediately, even with static workflows
- ✅ Validate every agent output initially (build ground truth dataset)
- ✅ Build tooling to visualize agent sequences (aid debugging)
- ✅ Document reward function assumptions (evolve with data)
- ✅ Plan human override mechanisms (safety net)

### Success Metrics by Phase

**Phase 1 (Static n8n + Logging):**
- [ ] 5+ agents implemented with standardized I/O
- [ ] 100% of diagnostic episodes logged with schema
- [ ] Static workflow resolves 70%+ of test alerts correctly
- [ ] Average 8-12k tokens per diagnostic episode

**Phase 2 (Rule-Based Router):**
- [ ] Rule-based router handles 80%+ of alert types
- [ ] 10% reduction in average tokens vs. static workflow
- [ ] Diagnostic accuracy maintained or improved (≥70%)
- [ ] Routing decisions explainable to FM stakeholders

**Phase 3 (RL Orchestrator):**
- [ ] RL policy trained on 200+ episodes
- [ ] Matches or exceeds rule-based accuracy
- [ ] 20%+ token reduction vs. static baseline
- [ ] Cyclic reasoning patterns emerge for complex diagnostics

**Phase 4 (Production RL):**
- [ ] Online learning maintains 90%+ diagnostic accuracy
- [ ] 30%+ token reduction vs. baseline
- [ ] Handles novel alert types through adaptation
- [ ] Human intervention required <10% of cases

### Integration with Existing Architecture

**Compatible with current project structure:**
- Project instructions: `Project-Specific-Instructions/SkySpark-n8n-Workflow.md`
- n8n workflows: `n8n/`
- Agent design aligns with FastAPI tool server architecture
- State schema accommodates SkySpark Haystack data model
- Reward function maps to ComEd program requirements

**Backward Compatibility:**
- Phase 0-1 static workflows remain fully functional
- Standardized I/O is additive, not breaking
- Logging infrastructure runs alongside existing logic
- Can defer RL indefinitely if rule-based routing suffices

## Usage Examples
- "Build n8n workflow to triage SkySpark alerts"
- "Create FastAPI server for energy calculations"
- "Set up multi-agent routing for HVAC diagnostics"
- "Design workflow for automated building system reports"
- "Integrate n8n with SkySpark Haystack API"
- "Design stateless agent with standardized I/O for future RL"
- "Set up diagnostic episode logging infrastructure"
- "Implement rule-based agent router for Phase 2"

---

## Model Selection Constraints (Added 2025-01-01)

### Hard Requirement: US/EU Origin Only
Company works with US government - **no Chinese-origin models permitted**.

This excludes: Qwen, DeepSeek, Yi, Baichuan, ChatGLM, and derivatives.

### Approved Local Models

| Agent Role | Model | Origin | Size | Rationale |
|------------|-------|--------|------|-----------|
| Classifier | Microsoft Phi-4 | 🇺🇸 US | 14B | Fast, accurate structured output, MIT license |
| Test Designer | Mistral Codestral 22B | 🇫🇷 EU | 22B | Purpose-built for code |
| Physics Explainer | Meta Llama 3.1 70B | 🇺🇸 US | 70B | Best open reasoning model |
| Reporter | Mistral Small 24B | 🇫🇷 EU | 24B | High quality summaries |
| Triage (local option) | Meta Llama 3.1 8B | 🇺🇸 US | 8B | Good balance for routine alerts |
| Coder Agent | Claude API | 🇺🇸 US | - | Best for code generation (keep on API) |

### Alternative Smaller Models (CPU/Light GPU)
- Microsoft Phi-4-mini-reasoning (3.8B) - Classification tasks
- Mistral 7B Instruct v0.3 - General purpose
- Meta CodeLlama-7B-Instruct - Code understanding

---

## Physics Checker Design (Added 2025-01-01)

### Two-Layer Architecture

**Layer 1: Rule Engine (Python, deterministic)**
- ASHRAE bounds checking
- Equipment capacity limits
- Thermodynamic constraints (energy balance)
- Returns: PASS/FAIL + which rule violated
- **No LLM involved** - pure Python logic

**Layer 2: Explanation Agent (local LLM, only if FAIL)**
- Takes: rule violation details + equipment context
- Returns: human-readable explanation of why it's impossible
- Model: Meta Llama 3.1 8B Instruct (US origin)
- Only invoked when Layer 1 fails

### Initial Physics Bounds
```python
PHYSICS_BOUNDS = {
    "zone_temp": {"min": 55, "max": 85, "unit": "°F"},
    "supply_air_temp": {"min": 50, "max": 65, "unit": "°F"},
    "chilled_water_delta_t": {"min": 8, "max": 16, "unit": "°F"},
    "hot_water_delta_t": {"min": 15, "max": 40, "unit": "°F"},
    "airflow_per_sqft": {"min": 0.5, "max": 3.0, "unit": "CFM/sqft"},
    "cooling_efficiency": {"min": 0.3, "max": 1.0, "unit": "kW/ton"},
    "boiler_efficiency": {"min": 0.75, "max": 0.98, "unit": "fraction"},
    "fan_static_pressure": {"min": 0.5, "max": 6.0, "unit": "inWG"},
}
```

### Integration with Agent Taxonomy
Physics Checker slots into the **Reasoning Agents** category:
- Input: Recommendation from Triage Agent + equipment context
- Output: PASS (proceed) or FAIL (block + explain)
- Invoked before any recommendation reaches the Reporter

---

## Calculation Tool Verification Pipeline (Added 2025-01-01)

### Core Principle: Agents Don't Do Math
- All calculations performed by human-approved Python scripts
- Scripts wrapped as callable tools for agents
- Results are auditable and reproducible
- Minimizes token count and eliminates hallucinated math

### Verification Workflow
```
Coder Agent (Claude) → Test Designer (Codestral) → Static Analyzer (AST)
       ↓                        ↓                         ↓
  Initial script         Edge cases, bounds         Security check
                         Reference values           Purity check
                                                    Type hints
       ↓                        ↓                         ↓
       └────────────────────────┴─────────────────────────┘
                                ↓
                    Test Executor (pytest)
                                ↓
                    Documentation Generator
                                ↓
                    Human Review Package
                    [Approve / Reject / Edit]
```

### Verification Types (Diversity = Trust)
| Type | What It Catches | Implementation |
|------|-----------------|----------------|
| Generated tests | Logic errors, edge cases | Local LLM (Codestral 22B) |
| Reference tests | Wrong formulas | Human-provided ASHRAE examples |
| Static analysis | Security, side effects | Python AST parsing |
| Type checking | Interface mismatches | mypy |
| Unit conversion | Dimensional errors | pint library |
| Bounds checking | Impossible outputs | Physics Checker rules |

### CalcTool Registration Schema
```python
@dataclass
class CalcTool:
    id: str
    name: str                    # e.g., "chw_energy"
    version: str                 # Semantic versioning
    description: str
    script_path: str             # Path to .py file
    function_name: str           # Entry point
    
    # Interface
    input_schema: dict           # JSON schema for inputs
    output_schema: dict          # JSON schema for outputs
    
    # Approval chain
    approved_by: str             # Human who reviewed
    approved_at: datetime
    test_cases: List[dict]       # Input/output pairs that must pass
    
    # Usage tracking
    invocation_count: int
    last_invoked: datetime
    error_count: int
```

---

## Value Economy System (Added 2025-01-01)

### Core Concept
Treat diagnostic strategies as an economy:
- Strategies have **value scores** that change based on outcomes
- Usefulness pays rent; wrongness gets evicted
- High-value strategies get promoted to **Skills**
- Unused strategies decay over time

### Strategy Artifact Schema
```python
@dataclass
class StrategyArtifact:
    id: str
    created_at: datetime
    updated_at: datetime
    
    # What it matches
    alert_pattern: dict               # Conditions this strategy applies to
    building_types: List[str]         # Hospital, university, office, etc.
    system_types: List[str]           # AHU, VAV, chiller, etc.
    
    # What it recommends
    diagnosis_template: str
    action_template: str
    calc_tools: List[str]             # Which calculation scripts to invoke
    
    # Value economy
    status: Literal["candidate", "validated", "skill"]
    value_score: float
    confidence: float
    
    # Evidence counters
    times_matched: int
    times_confirmed: int              # Human said "yes, correct"
    times_rejected: int               # Human said "no, wrong"
    energy_saved_kbtu: float          # Cumulative attributed savings
    last_used: datetime
    
    # Lineage
    source: Literal["human", "synthesized", "promoted"]
    parent_ids: List[str]
```

### Promotion Gates

**Candidate → Validated:**
```python
VALIDATION_THRESHOLDS = {
    "min_matches": 3,
    "min_confirmations": 2,
    "max_rejection_rate": 0.3,
    "min_distinct_buildings": 2,
    "physics_check_pass": True,
}
```

**Validated → Skill:**
```python
SKILL_PROMOTION_THRESHOLDS = {
    "min_matches": 10,
    "min_confirmations": 7,
    "max_rejection_rate": 0.15,
    "min_distinct_buildings": 3,
    "min_age_days": 14,
    "attributed_savings_kbtu": 1000,
}
```

### Decay Function
```python
def calculate_decay(artifact: StrategyArtifact, days_since_use: int) -> float:
    """Value decays 2% per day of non-use, floor at 0.1"""
    decay_factor = 0.98 ** days_since_use
    return max(artifact.value_score * decay_factor, 0.1)
```

### Value Update Logic
```python
REWARDS = {
    "confirmed_correct": 1.0,
    "energy_saved_per_1000_kbtu": 0.5,
    "reused_different_building": 0.3,
}

PENALTIES = {
    "rejected_wrong": -2.0,
    "physics_violation": -3.0,
    "caused_comfort_complaint": -1.5,
}
```

---

## Governance Layer (Added 2026-01-05)

### Core Principle

**Derive "goodness" from observable deltas, not model judgments.**

The governance layer monitors agent and strategy performance through measurable signals, uses a small local LLM for classification only, and modifies routing weights and configuration—never prompts or training data.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TELEMETRY LAYER                          │
│  Captures: latency, retries, overrides, tool failures,     │
│           user edits, session completion                    │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              CLASSIFICATION ENGINE (Ollama)                 │
│  Model: Llama 3.1 8B Instruct (Q8)                         │
│  Task: Categorize failure types, edit substantiveness      │
│  Output: Strict JSON enums only (no explanatory text)      │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│           SCORE CALCULATOR (Deterministic)                  │
│  Computes health scores from weighted signals              │
│  NO LLM INVOLVED - pure Python logic                       │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  CONFIG MUTATOR                             │
│  Writes to: routing weights, canary patterns, deprecation  │
│  NEVER modifies: agent prompts, training data              │
└─────────────────────────────────────────────────────────────┘
```

### Measurable Signals (Observable Deltas)

**What we measure:**
- **User acceptance:** Did user accept recommendation without edits?
- **Edit size:** How much did user modify agent output? (character delta)
- **Override frequency:** How often did user reject and provide alternative?
- **Session completion:** Did diagnostic episode complete successfully?
- **Latency:** Time to produce recommendation
- **Retry count:** How many attempts before acceptable output?
- **Tool failures:** Number of failed tool calls during episode

**What we DON'T measure:**
- ❌ LLM judgment of "quality"
- ❌ Subjective ratings
- ❌ Vibes-based assessment

### Classification Engine Specs

**Model:** Llama 3.1 8B Instruct (Q8 quantization)
**Deployment:** Ollama (local)
**Temperature:** 0.0 (deterministic)
**Max Tokens:** 50
**Output Format:** Strict JSON schema with enums only

**Example Classification Task:**
```json
{
  "edit_type": "substantive" | "formatting" | "none",
  "failure_mode": "incorrect_diagnosis" | "missing_context" | "tool_failure" | "physics_violation" | "null",
  "confidence": 0.0-1.0
}
```

**Acceptable Failures:**
- Misclassification (wrong enum selected)
- Refusal to classify (null output)

**Unacceptable Failures:**
- Hallucinated categories not in schema
- Explanatory text instead of enum
- Non-JSON output

### Health Score Calculation (Deterministic)

```python
health_score = (
    success_rate * 0.40 +
    non_replacement_rate * 0.25 +
    non_override_rate * 0.20 +
    completion_rate * 0.15
)
```

**Where:**
- `success_rate` = accepted recommendations / total recommendations
- `non_replacement_rate` = 1 - (substantive edits / total recommendations)
- `non_override_rate` = 1 - (explicit rejections / total recommendations)
- `completion_rate` = completed episodes / started episodes

**Thresholds:**
- **Reinforce** (≥0.80): Increase routing weight, consider promotion
- **Stable** (0.50-0.80): Maintain current routing
- **Decay Warning** (<0.50): Flag for review, reduce routing weight
- **Deprecation Candidate** (<0.35 for 14+ days): Human review required

### Strategy Lifecycle Management

**Canary Pattern (Gradual Rollout):**
```
New Strategy → 10% of matching alerts
  ↓ (5 successful uses)
50% of matching alerts
  ↓ (20 successful uses)
100% of matching alerts (promoted)
```

**Deprecation Workflow:**
1. Automated flag when health <0.35 for 14+ days
2. Generate deprecation report with metrics
3. Human review REQUIRED before archiving
4. Archive strategy with audit log

**Skill Cap:** Maximum 50 active strategies
- Prevents strategy sprawl
- Forces prioritization and consolidation
- Must deprecate before adding when at cap

### Phased Implementation

**Phase 1: Telemetry Foundation** (2-3 weeks)
- [ ] Add telemetry emission endpoints to tool_server.py
- [ ] Define event schema (JSON)
- [ ] Create append-only event store (SQLite or JSONL)
- [ ] Instrument agent call sites with telemetry
- [ ] Verify data collection end-to-end

**Phase 2: Deterministic Scoring** (1 week)
- [ ] Implement health score calculation (pure Python)
- [ ] Create scoring dashboard/report script
- [ ] Test with historical data (if available)
- [ ] Define threshold policies

**Phase 3: Classification Engine** (1-2 weeks)
- [ ] Deploy Ollama locally
- [ ] Install Llama 3.1 8B Instruct
- [ ] Create classification service (FastAPI endpoint)
- [ ] Define JSON schemas for classification tasks
- [ ] Test enum-only output enforcement
- [ ] Integrate with telemetry pipeline

**Phase 4: Config Mutation** (1 week)
- [ ] Implement routing weight adjustment logic
- [ ] Create canary pattern manager
- [ ] Build deprecation workflow with human approval
- [ ] Add audit logging for all config changes
- [ ] Test end-to-end governance loop

### Integration Points

**SkySpark n8n Workflow:**
- Monitor agent tool calls via telemetry
- Capture user acceptance/rejection signals
- Log session completion status

**Tool Server (FastAPI):**
- Add `/telemetry/emit` endpoint
- Add `/governance/health-score` endpoint
- Add `/governance/classify` endpoint (calls Ollama)

**Event Store Schema:**
```json
{
  "event_id": "uuid",
  "timestamp": "2026-01-05T10:30:00Z",
  "event_type": "agent_recommendation" | "user_feedback" | "session_complete",
  "agent_id": "triage_agent_v1",
  "strategy_id": "ahu_vfd_savings_v2",
  "signals": {
    "latency_ms": 3400,
    "retry_count": 0,
    "tool_failures": 0,
    "user_accepted": true,
    "edit_delta_chars": 0,
    "override": false,
    "session_completed": true
  },
  "classification": {
    "edit_type": "none",
    "failure_mode": null
  }
}
```

### Observability Stack (LangSmith + Telemetry)

**Two-Layer Observability:**

1. **LangSmith** - Agent execution tracing and evaluation
   - Traces all LangGraph agent calls within n8n workflows
   - Captures input/output for each agent step
   - Evaluation metrics for agent performance
   - Token usage tracking per agent call

2. **Governance Telemetry** - Outcome measurement
   - User acceptance signals
   - Edit deltas and overrides
   - Session completion status
   - Feeds into health score calculation

**Integration Architecture:**

```
n8n Workflow
  ↓
LangGraph Agent Node
  ├─→ LangSmith (trace execution, token costs)
  └─→ Governance Telemetry (emit outcome signals)
        ↓
  Event Store → Health Score → Config Mutation
```

**LangSmith Setup:**

```bash
# Install LangSmith
pip install langsmith langchain-anthropic

# Set API key
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="your-key-here"
export LANGCHAIN_PROJECT="skyspark-alert-triage"
```

**LangGraph Integration in n8n:**

```python
# In n8n Code node or custom LangGraph service
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph
from langsmith import traceable

@traceable(name="alert_router")
def route_alert(state: DiagnosticState) -> str:
    """Route alert to appropriate specialist agent."""
    # LangSmith automatically traces this function
    # Governance telemetry emits outcome after completion
    router = ChatAnthropic(model="claude-sonnet-4")
    routing_decision = router.invoke(state)

    # Emit telemetry event
    emit_telemetry({
        "event_type": "routing_decision",
        "decision": routing_decision,
        "confidence": state.confidence_score
    })

    return routing_decision
```

**What LangSmith Captures:**
- Agent call sequences and routing decisions
- Token usage per agent (for cost optimization)
- Latency per agent step
- Input/output schemas validation
- Error traces and retry patterns

**What Governance Telemetry Captures:**
- User accepted/rejected recommendation
- Edit delta size (character count)
- Override frequency
- Session completion status
- Final diagnostic outcome

**Why Both?**
- **LangSmith:** Observability during execution (what agents did)
- **Telemetry:** Observability of outcomes (did it work?)
- Together: Complete feedback loop for continuous improvement

### Ollama Deployment

**Installation:**

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Llama 3.1 8B Instruct
ollama pull llama3.1:8b-instruct-q8_0

# Verify
ollama run llama3.1:8b-instruct-q8_0 "Classify this edit: {'type': 'formatting'}"
```

**FastAPI Integration:**

```python
import requests

def classify_edit(edit_context: dict) -> dict:
    """Call Ollama for classification."""
    prompt = f"""Classify this edit strictly using the schema:
{json.dumps(edit_context)}

Output ONLY valid JSON with these exact enums:
{{"edit_type": "substantive" | "formatting" | "none"}}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1:8b-instruct-q8_0",
            "prompt": prompt,
            "temperature": 0.0,
            "max_tokens": 50,
            "format": "json"  # Enforce JSON output
        }
    )

    return response.json()
```

### Success Metrics

**Phase 1 (Telemetry) Complete When:**
- [ ] 100% of agent calls emit telemetry events
- [ ] Event store captures all signals defined in schema
- [ ] No data loss or missing events
- [ ] Dashboard shows real-time event stream

**Phase 2 (Scoring) Complete When:**
- [ ] Health scores calculated for all active strategies
- [ ] Thresholds trigger correct workflow actions
- [ ] Scores correlate with manual assessment
- [ ] Report generation automated

**Phase 3 (Classification) Complete When:**
- [ ] Ollama classification endpoint working
- [ ] 95%+ enum-only outputs (no hallucinated categories)
- [ ] Classification latency <500ms per event
- [ ] Integrates with telemetry pipeline

**Phase 4 (Mutation) Complete When:**
- [ ] Routing weights auto-adjust based on health scores
- [ ] Canary pattern deployed for new strategies
- [ ] Deprecation workflow tested end-to-end with human approval
- [ ] Audit log captures all config changes

### Critical Don'ts

❌ **DON'T** use governance layer to modify agent prompts
❌ **DON'T** let classification LLM make "goodness" judgments
❌ **DON'T** skip human review for deprecation decisions
❌ **DON'T** use cloud-based LLMs for governance (privacy/cost)
❌ **DON'T** allow governance to modify training data directly

✅ **DO** use observable signals only
✅ **DO** keep classification deterministic (temp=0.0)
✅ **DO** require human approval for all deprecations
✅ **DO** use local Ollama for privacy and zero cost
✅ **DO** modify routing config, not agent logic

---

## Related Documentation

- **[NEXT-STEPS.md](./NEXT-STEPS.md)** - Implementation roadmap and action items
- **[PHASE_2B_SUMMARY.md](./PHASE_2B_SUMMARY.md)** - Current SkySpark endpoint status
- **[references/integration-architecture.md](./references/integration-architecture.md)** - n8n + pyHVAC design
- **[../../engineering_calcs/README.md](../../engineering_calcs/README.md)** - Calculation tools project


## Saving Next Steps

When n8n-automation work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "n8n-automation" \
  --content "## Priority Tasks
1. Build n8n workflow for SkySpark alert triage
2. Test multi-agent system integration
3. Deploy FastAPI tool server"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`
