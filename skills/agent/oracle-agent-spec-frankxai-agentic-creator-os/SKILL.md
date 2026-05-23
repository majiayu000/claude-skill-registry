---
name: Oracle Agent Spec Expert
description: Design framework-agnostic AI agents using Oracle's Open Agent Specification for portable, interoperable agentic systems with JSON/YAML definitions
version: 1.0.0
---

# Oracle Agent Spec Expert Skill

## Purpose
Master Oracle's Open Agent Specification (Agent Spec) to design framework-agnostic, declarative AI agents that can be authored once and deployed across multiple frameworks and runtimes.

## What is Agent Spec?

### Open Agent Specification
Framework-agnostic declarative language for defining agentic systems, building blocks for standalone agents and structured workflows, plus composition patterns for multi-agent systems.

**Key Innovation:** Decouple design from execution - write agents once, run anywhere.

**Release:** Technical report published October 2025 (arXiv:2510.04173)

## Core Philosophy

**The Problem:** Fragmented agent development - each framework requires different implementation.

**The Solution:** Unified representation - Agent Spec defines structure and behavior in JSON/YAML that any compatible runtime can execute.

**Benefit:** Author agents once → Deploy across frameworks → Reduce redundant development.

## Architecture

### Component Model
Agent Spec defines **conceptual building blocks** (components) that make up agent-based systems.

**Key Property:** All components are trivially serializable to JSON/YAML.

### Core Components

#### 1. LLMNode
**Purpose:** Text generation via LLM

**Definition:**
```yaml
type: LLMNode
name: "text_generator"
model: "claude-sonnet-4-5"
system_prompt: "You are a helpful assistant"
temperature: 0.7
max_tokens: 2000
```

#### 2. APINode
**Purpose:** External API calls

**Definition:**
```yaml
type: APINode
name: "weather_api"
endpoint: "https://api.weather.com/v1/current"
method: "GET"
parameters:
  location: "{input.location}"
headers:
  Authorization: "Bearer {env.API_KEY}"
```

#### 3. AgentNode
**Purpose:** Multi-round conversational agent

**Definition:**
```yaml
type: AgentNode
name: "support_agent"
model: "gpt-4"
system_prompt: "You are a customer support specialist"
tools:
  - type: function
    name: "lookup_order"
  - type: function
    name: "process_refund"
```

#### 4. WorkflowNode
**Purpose:** Orchestrate sequence of nodes

**Definition:**
```yaml
type: WorkflowNode
name: "data_pipeline"
steps:
  - node: extract_node
  - node: transform_node
  - node: load_node
error_handling: retry
```

## Agent Specification Format

### Basic Agent
```json
{
  "version": "1.0",
  "agent": {
    "name": "CustomerSupportAgent",
    "description": "Handles customer inquiries and support requests",
    "components": {
      "classifier": {
        "type": "LLMNode",
        "model": "claude-haiku-4",
        "system_prompt": "Classify customer inquiry type",
        "output": "inquiry_type"
      },
      "technical_support": {
        "type": "AgentNode",
        "model": "claude-sonnet-4-5",
        "tools": ["diagnose_issue", "escalate_ticket"]
      },
      "billing_support": {
        "type": "AgentNode",
        "model": "gpt-4",
        "tools": ["lookup_invoice", "process_refund"]
      },
      "router": {
        "type": "ConditionalNode",
        "conditions": [
          {
            "if": "inquiry_type == 'technical'",
            "then": "technical_support"
          },
          {
            "if": "inquiry_type == 'billing'",
            "then": "billing_support"
          }
        ]
      }
    },
    "entry_point": "classifier"
  }
}
```

### Multi-Agent System
```yaml
version: "1.0"
system:
  name: "ResearchSystem"
  description: "Multi-agent research and analysis system"

  agents:
    researcher:
      type: AgentNode
      model: claude-sonnet-4-5
      tools:
        - web_search
        - fetch_document
      system_prompt: "Research topics thoroughly"

    analyzer:
      type: AgentNode
      model: gpt-4o
      tools:
        - analyze_data
        - generate_insights
      system_prompt: "Analyze research findings"

    synthesizer:
      type: AgentNode
      model: claude-sonnet-4-5
      system_prompt: "Synthesize findings into coherent report"

  workflow:
    - step: researcher
      output: research_data
    - step: analyzer
      input: research_data
      output: analysis
    - step: synthesizer
      input: [research_data, analysis]
      output: final_report

  output: final_report
```

## Node Library

### Orchestration Nodes

**SequentialNode:**
```yaml
type: SequentialNode
nodes:
  - step1_node
  - step2_node
  - step3_node
```

**ParallelNode:**
```yaml
type: ParallelNode
nodes:
  - agent_a
  - agent_b
  - agent_c
aggregator: synthesis_node
```

**ConditionalNode:**
```yaml
type: ConditionalNode
condition: "{output.confidence} > 0.8"
if_true: high_confidence_path
if_false: manual_review_path
```

**LoopNode:**
```yaml
type: LoopNode
condition: "{not output.success}"
max_iterations: 3
body: retry_agent
```

### Integration Nodes

**MCPNode:**
```yaml
type: MCPNode
server: "github-server"
resource: "issues"
operation: "list"
filters:
  assignee: "me"
```

**DatabaseNode:**
```yaml
type: DatabaseNode
connection: "postgresql://..."
query: "SELECT * FROM customers WHERE id = {input.customer_id}"
```

## Design Patterns

### Pattern 1: Triage and Route
```yaml
name: TriageSystem
components:
  classifier:
    type: LLMNode
    model: claude-haiku-4
    prompt: "Classify: {input}"

  router:
    type: ConditionalNode
    conditions:
      - if: "category == 'urgent'"
        then: urgent_agent
      - if: "category == 'standard'"
        then: standard_agent
      - default: fallback_agent
```

### Pattern 2: Research-Analyze-Report
```yaml
name: ResearchPipeline
workflow:
  - name: gather
    type: AgentNode
    tools: [web_search, fetch_docs]

  - name: analyze
    type: LLMNode
    prompt: "Analyze: {gather.output}"

  - name: report
    type: LLMNode
    prompt: "Generate report from: {analyze.output}"
```

### Pattern 3: Parallel Processing with Synthesis
```yaml
name: MultiPerspective
components:
  parallel_agents:
    type: ParallelNode
    nodes:
      - technical_expert
      - business_expert
      - user_perspective

  synthesizer:
    type: AgentNode
    system_prompt: "Synthesize perspectives into unified recommendation"
    input: "{parallel_agents.outputs}"
```

## Framework Portability

### Supported Runtimes
Agent Spec can be executed by any compatible runtime:

- **Oracle ADK** - Native support via `agent_spec` package
- **LangGraph** - Via Agent Spec → LangGraph compiler
- **AutoGen** - Via Agent Spec → AutoGen adapter
- **Custom Runtimes** - Implement Agent Spec interpreter

### Compilation Example
```python
# Load Agent Spec definition
from agent_spec import load_spec

spec = load_spec("my_agent.yaml")

# Compile to target framework
langgraph_agent = spec.compile(target="langgraph")
autogen_agent = spec.compile(target="autogen")
oracle_adk_agent = spec.compile(target="oracle_adk")

# All three agents have identical behavior
```

## Best Practices

### DO:
✅ Use descriptive names for all components
✅ Document purpose in description fields
✅ Define explicit input/output schemas
✅ Specify error handling strategies
✅ Version your agent specifications
✅ Test across multiple runtimes for true portability

### DON'T:
❌ Embed runtime-specific logic in specs
❌ Hardcode credentials or secrets
❌ Use framework-specific syntax
❌ Skip input validation definitions
❌ Ignore version compatibility

## Integration with Other Specs

### MCP (Model Context Protocol)
**Relationship:** MCP standardizes tool/resource provisioning; Agent Spec standardizes agent configuration.

**Together:**
```yaml
agent:
  name: DataAgent
  tools:
    - type: MCPTool
      server: "postgres-mcp"
      resource: "customers"
    - type: MCPTool
      server: "github-mcp"
      resource: "issues"
```

### A2A (Agent-to-Agent Communication)
**Relationship:** A2A standardizes inter-agent communication; Agent Spec defines agent structure.

**Together:**
```yaml
multi_agent_system:
  agents:
    - name: agent1
      a2a_endpoint: "https://agent1.example.com"
    - name: agent2
      a2a_endpoint: "https://agent2.example.com"
  communication: a2a_protocol
```

## Ecosystem Benefits

### For Developers
- **Write Once, Run Anywhere** - Single specification, multiple runtimes
- **Reusable Components** - Share agent definitions across projects
- **Version Control** - Track agent evolution in Git
- **Collaboration** - Common language for team communication

### For Frameworks
- **Standardized Input** - Consistent agent definitions
- **Faster Adoption** - Lower barrier to entry
- **Interoperability** - Agents can migrate between frameworks

### For Enterprises
- **Vendor Independence** - Not locked into single framework
- **Reproducible Deployments** - Consistent behavior across environments
- **Compliance** - Audit trail through declarative definitions

## Tools & Resources

### PyAgentSpec (Python Package)
```bash
pip install pyagentspec
```

```python
from pyagentspec import AgentSpec, LLMNode, AgentNode

spec = AgentSpec(
    name="MyAgent",
    components=[
        LLMNode(name="classifier", model="claude-haiku-4"),
        AgentNode(name="executor", model="gpt-4")
    ]
)

spec.save("my_agent.yaml")
spec.compile(target="oracle_adk")
```

### Validation
```python
from pyagentspec import validate_spec

is_valid, errors = validate_spec("agent.yaml")
if not is_valid:
    print(f"Validation errors: {errors}")
```

## Decision Framework

**Use Agent Spec when:**
- Need framework portability (deploy across multiple platforms)
- Want declarative, version-controlled agent definitions
- Building reusable agent components
- Require reproducible deployments
- Team collaboration on agent design

**Combine with:**
- Oracle ADK (for OCI deployment)
- LangGraph (for complex state machines)
- Claude SDK (for Anthropic models)
- MCP (for data source standardization)

## Resources

**Official:**
- GitHub: https://github.com/oracle/agent-spec
- Documentation: https://oracle.github.io/agent-spec/
- Technical Paper: https://arxiv.org/pdf/2510.04173
- PyAgentSpec: https://pypi.org/project/pyagentspec/

**Citation:**
```
Oracle Corporation. (2025). Open Agent Specification (Agent Spec) Technical Report.
```

## Final Principles

1. **Framework-Agnostic** - Design once, deploy anywhere
2. **Declarative** - Describe what, not how
3. **Composable** - Build complex systems from simple components
4. **Versioned** - Track evolution over time
5. **Portable** - Migrate between frameworks without rewrite
6. **Interoperable** - Works with MCP, A2A, and other standards

---

*This skill enables you to design portable, reusable AI agents using Oracle's open specification standard for 2025 and beyond.*
