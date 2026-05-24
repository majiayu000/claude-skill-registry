---
name: work-decomposer
description: Transform any intellectual work into AI-promptable systems. Use when user wants to automate business processes, create multi-agent workflows, decompose complex work into AI-delegatable tasks, or build frameworks for recurring intellectual work (competitive analysis, strategic planning, BMC, OKRs, reports, etc.). Applies to work with clear inputs, context, and expected outputs.
---

# Work Decomposer

## Core Principle

**Any intellectual work = Input + Context + Process → Output**

If you can formalize these components, you can prompt it. This skill helps decompose complex intellectual work into multi-agent AI systems.

## When to Use

Use this skill when:
- User wants to automate recurring analytical or strategic work
- Task involves creating artifacts (reports, strategies, analyses, frameworks)
- Work follows a pattern but requires intelligence (not simple templates)
- Multiple decision points or steps exist
- Examples: competitive analysis, BMC creation, OKR planning, market research, GTM strategy, customer segmentation

## Decomposition Workflow

### Step 1: Identify Work Components

Ask user to provide or help identify:

1. **Input**: What information is needed to start?
   - Documents, data, requirements, constraints
   - Example: "List of competitors, their websites"

2. **Context**: What knowledge enables good execution?
   - Domain knowledge, frameworks, best practices, company specifics
   - Example: "Understanding of ICP, positioning frameworks"

3. **Process**: What steps are performed?
   - Decision points, analysis phases, synthesis methods
   - Example: "Analyze landing pages → Extract positioning → Compare offers"

4. **Output**: What artifact is produced?
   - Format, structure, quality criteria
   - Example: "Excel with columns: Competitor, ICP, UVP, Pricing, Positioning"

### Step 2: Design Agent Architecture

Based on complexity, choose architecture:

**Simple (1-2 agents):**
- Single input → Single analysis → Structured output
- Example: Landing page analysis → Extract key elements

**Orchestrated (3-5 agents):**
- Orchestrator assigns tasks to specialized sub-agents
- Example: Main agent → Discovery agent + Analysis agent + Synthesis agent

**Complex (5+ agents):**
- Multiple orchestration levels, iterative refinement
- Example: Strategy → Research agents → Analysis agents → Critique agent → Synthesis

Decision heuristic:
- 1 clear step = Simple
- 3-5 distinct subtasks = Orchestrated
- Multiple phases or iterations = Complex

### Step 3: Define Agent Roles

For each agent, specify:

**Role name**: What it does (e.g., "Competitive Positioning Analyzer")

**Input**: What it receives
- From user, from other agents, or from external sources

**Task**: Specific instructions
- Be concrete: "Extract ICP indicators from landing page: job titles mentioned, company size signals, pain points addressed"

**Output**: What it produces
- Format: JSON, table, text, structured list
- Required fields
- Quality criteria

**Context/Constraints**:
- What it should know or follow
- Examples of good output
- Common pitfalls to avoid

### Step 4: Define Data Flow

Map how information moves:

```
User Input → Agent 1 (discovers competitors) → List of URLs
           → Agent 2 (analyzes each URL) → Raw analysis per competitor
           → Agent 3 (synthesizes) → Structured table
           → Human review → Corrections
           → Agent 4 (refines) → Final output
```

Specify:
- Where human review/input is needed
- What gets stored/cached vs. regenerated
- Error handling (what if URL is broken, data is missing)

### Step 5: Implement Prompt Templates

For each agent, create prompt template:

**Orchestrator template:**
```
You are [role]. Your goal: [goal].

Available agents:
1. [Agent name]: [What it does]
2. [Agent name]: [What it does]

User input: {user_input}

Steps:
1. [What to do first]
2. [What to do next]
3. [How to synthesize]

Output format: [Specification]
```

**Sub-agent template:**
```
You are [specific role]. 

Input: {input_from_orchestrator}

Task: [Concrete instruction]

Context: [Domain knowledge, examples, constraints]

Output: [Exact format specification]
```

### Step 6: Specify Quality Gates

Define how to validate:

**Self-critique prompts:**
- "Review your output against these criteria: [criteria]"
- "What assumptions did you make? Are they justified?"

**Validation checks:**
- Required fields present
- Data format correct
- Logical consistency
- Example: "All competitors must have at least one pricing tier identified"

**Human review points:**
- Where expertise matters
- Where errors are costly
- Where creative input is needed

## Implementation Patterns

### Pattern 1: Sequential Analysis
For work with clear linear steps.

See `references/sequential-pattern.md` for competitive analysis, market research examples.

### Pattern 2: Framework Completion
For work filling structured frameworks (BMC, OKRs, SWOT).

See `references/framework-pattern.md` for BMC, GTM strategy, OKR examples.

### Pattern 3: Iterative Refinement
For work needing multiple passes (strategy, positioning, messaging).

See `references/iterative-pattern.md` for strategy development, messaging examples.

### Pattern 4: Parallel Research
For work with independent research threads.

See `references/parallel-pattern.md` for multi-source research, due diligence examples.

## Output Delivery

Provide user with:

1. **Architecture diagram** (text-based):
```
Orchestrator
├── Agent 1: [Role]
├── Agent 2: [Role]
└── Agent 3: [Role]
```

2. **Prompt templates** for each agent (ready to use)

3. **Implementation guide**:
   - Recommended tools (n8n, Python, API calls)
   - Data storage approach
   - How to iterate and improve

4. **Test scenario** to validate system works


## Resources

### references/
Pattern libraries with concrete examples:
- `sequential-pattern.md` - Linear analysis workflows (competitive intel, market research)
- `framework-pattern.md` - Structured frameworks (BMC, OKRs, GTM)
- `iterative-pattern.md` - Multi-pass refinement (strategy, positioning)
- `parallel-pattern.md` - Independent research threads (due diligence, multi-source analysis)

Load specific pattern file based on user's work type.
