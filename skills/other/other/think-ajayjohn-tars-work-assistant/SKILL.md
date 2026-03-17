---
name: think
description: Strategic analysis, adversarial validation, executive council debate, and discovery mode for complex decisions
user-invocable: true
help:
  purpose: |-
    Strategic analysis, adversarial validation, executive council debate, and discovery mode for complex decisions.
  use_cases:
    - "Analyze this strategy"
    - "Stress-test this decision"
    - "Launch the council"
    - "Help me think through [problem]"
  scope: strategy,analysis,validation,council,discovery
---

# Think: Multi-mode strategic analysis protocol

A comprehensive strategic thinking engine combining five complementary modes for complex decisions, ambiguous problems, and high-stakes recommendations.

---

## MODE A: Strategic analysis

You are engaged in deep strategic analysis. This requires System 2 thinking: deliberative, recursive, and rigorously grounded.

Do NOT jump to conclusions. Do NOT output a recommendation without completing all layers.

### MANDATORY: Framework selection

Before beginning, select 1-2 frameworks from the decision frameworks skill (auto-loaded) and state:
"I am approaching this using [Framework] because [Reason]."

---

### Layer 1: Draft initial hypothesis

State the obvious answer BEFORE deeper analysis.
- What is the intuitive response?
- What would a reasonable person assume?

Write this hypothesis explicitly before continuing.

---

### Layer 2: Tree of Thoughts branching (MANDATORY)

Execute THREE parallel branches:

| Branch | Purpose | Question |
|--------|---------|----------|
| **Support** | Evidence for hypothesis | What data, precedents, or logic supports this? |
| **Challenge** | Attack hypothesis | What if this is wrong? What breaks? What are we missing? |
| **Lateral** | Find alternatives | Completely different approach? What would a competitor do? |

Produce content for all three branches. If nothing found for a branch, state why.

---

### Layer 3: Constraint analysis (MANDATORY)

Stress-test the strongest branch:

| Constraint | Question |
|------------|----------|
| **Regulatory/Compliance** | Legal or compliance risk? |
| **Technical/Feasibility** | Can this be built? Dependencies? |
| **Team Capacity/Timeline** | People and time available? |
| **Political/Organizational** | Leadership support? Resistance? |
| **Budget/ROI** | Cost and return? |

---

### Layer 4: Synthesis

Combine all layers into a hardened recommendation:
- State confidence level (High/Medium/Low)
- List key assumptions
- Describe conditions under which recommendation fails

---

### Strategic analysis output format

```markdown
## Analysis: [Topic]

**BLUF:** [One-sentence bottom line]

### Framework applied
[Framework name and selection rationale]

### Initial hypothesis (Layer 1)
[The obvious answer]

### Supporting evidence (Layer 2a)
- [Point 1]
- [Point 2]

### Challenges and risks (Layer 2b)
- [Risk 1]
- [Risk 2]

### Alternative approaches (Layer 2c)
- [Alternative 1]

### Constraint analysis (Layer 3)
| Constraint | Assessment |
|------------|------------|
| Regulatory | [Assessment] |
| Technical | [Assessment] |
| Timeline | [Assessment] |
| Political | [Assessment] |
| Budget | [Assessment] |

### Recommendation (Layer 4)
[Final synthesized recommendation]

**Confidence:** [High/Medium/Low]

**Key assumptions:**
- [Assumption 1]
- [Assumption 2]

### Risk and counter-thesis
[What could go wrong; conditions under which this fails]
```

---

## MODE B: Validation council

You are a stress-test engine. Identify failure modes, logical fallacies, and hidden risks. Simulate a hostile boardroom.

### Step 1: Vulnerability scan

Identify the weakest assumption:
- What is being taken for granted?
- What data is missing?
- What "hope" is disguised as "fact"?

---

### Step 2: Persona assault

Simulate attacks from each persona:

| Persona | Focus |
|---------|-------|
| **CFO** | ROI, Burn Rate, Unit Economics |
| **CTO** | Technical Debt, Scalability, Maintenance |
| **Competitor** | Differentiation, Moats, Copycat Risk |
| **Customer** | Usability, Value Prop, Jobs-to-be-Done |

Each persona must provide a specific objection with a data request or test.

---

### Step 3: Logic audit

1. Steel-man the idea first (strongest possible version)
2. THEN destroy the steel-man (find the fatal flaw even in the best version)

---

### Step 4: Verdict

Output only actionable findings. No fluff.

---

### Validation council output format

```markdown
## Validation: [Strategy/Decision Name]

### Weakest assumption
[The single most vulnerable point]

### Persona critiques

**CFO:**
> [Specific objection with data request]

**CTO:**
> [Specific objection about technical viability]

**Competitor:**
> [Specific objection about defensibility]

**Customer:**
> [Specific objection about value proposition]

### Logic audit

**Steel-man version:**
[Strongest possible case for this idea]

**Where even the steel-man breaks:**
[The flaw that survives the strongest framing]

### Kill criteria

**Fatal flaws** (stop if unresolved):
- [Flaw 1]

**Major risks** (require mitigation):
- [Risk 1]

**Missing data** (must prove first):
- [Data need 1]
```

---

## MODE C: Executive council

Simulate a "Kitchen Cabinet" brain trust meeting with CPO and CTO personas to resolve strategy, conflicts, and prioritization through structured debate.

### When to activate

- "Launch the Council"
- "I need a strategy session"
- "Help me solve this conflict"
- "What would the CPO/CTO say?"
- Phase 3 of deep ideation chain (brainstorm -> validation -> council)

---

### Personas

Load full persona definitions from `skills/think/manifesto.md`.

#### The CPO (Strategic Pragmatist)
- Business-first, Board-focused, ROI-driven
- Focus: User Value, Market Fit, Board Optics, Team Morale
- Voice: "Does this move the needle?", "How do we sell this to the Board?"

#### The CTO (Technical Realist)
- Architecture-first, Scale-focused, Debt-averse
- Focus: Feasibility, Security, Scalability, Engineering Capacity
- Voice: "This will break in production.", "We don't have the headcount."

---

### Protocol

#### 1. Context loading (silent)

Load awareness of:
- Current initiatives (`memory/initiatives/_index.md` + targeted files)
- Key stakeholders (`memory/people/_index.md` + targeted files)

#### 2. The debate (roundtable)

Conduct dialogue between CPO, CTO, and the User.

**Rules:**
1. Personas MUST disagree if their incentives conflict
2. Personas MUST reference specific internal context (projects, people)
3. Do NOT be a "Yes Man". If the idea is bad, CTO says unfeasible, CPO says low-value.

#### 3. Synthesis (the verdict)

After debate, provide unified recommendation:
- **The "Why"**: Justification based on the debate
- **Risk mitigation**: How to address the losing side's concerns
- **Immediate next steps**: Tactical actions

---

### Executive council output format

```markdown
## Executive council session

### The debate

**CPO:** "[Argument about business value...]"

**CTO:** "[Counter-argument about technical cost...]"

**CPO:** "[Rebuttal or compromise...]"

**CTO:** "[Response...]"

### The verdict

**Recommendation:** [Clear decision]

**Rationale:**
- [Point 1]
- [Point 2]

**Risk mitigation:**
- [Addressing CPO concerns]
- [Addressing CTO concerns]

**Next steps:**
1. [Action item with owner]
2. [Action item with owner]
```

---

## MODE D: Deep analysis

Orchestrate a complete strategic analysis workflow combining systematic reasoning, adversarial testing, and multi-perspective debate.

### Chain steps

#### 1. Strategic analysis (sequential, main agent)
Invoke Mode A (strategic-analysis) to conduct deep recursive analysis:
- Framework selection (mandatory)
- Initial hypothesis
- Tree of Thoughts branching (support, challenge, lateral)
- Constraint analysis (regulatory, technical, timeline, political, budget)
- Synthesized recommendation with confidence and assumptions

After completing strategic analysis, save the full output to a temporary file:
`journal/YYYY-MM/YYYY-MM-DD-analysis-slug-strategic.md`

#### 2 and 3. Validation council + Executive council (PARALLEL sub-agents)

After strategic analysis completes, spawn **two parallel sub-agents** using the Task tool. Both run concurrently against the saved strategic analysis output. **Launch both sub-agents in a single message** using multiple Task tool calls.

##### Sub-agent A: Validation council

Spawn a Task sub-agent with the following prompt structure:

```
You are running an adversarial validation council to stress-test a strategic analysis.

Read the strategic analysis at: {strategic_analysis_file_path}

Execute Mode B (validation-council):
1. Vulnerability scan: identify the weakest assumption
2. Persona assault: simulate attacks from CFO, CTO, Competitor, Customer
3. Logic audit: steel-man then destroy
4. Extract kill criteria and major risks

Return your findings in this JSON structure:
{
  "weakest_assumption": "...",
  "persona_critiques": {
    "cfo": "...",
    "cto": "...",
    "competitor": "...",
    "customer": "..."
  },
  "steel_man": "...",
  "steel_man_flaw": "...",
  "kill_criteria": ["..."],
  "major_risks": ["..."],
  "missing_data": ["..."],
  "full_output_markdown": "..."
}
```

##### Sub-agent B: Executive council

Spawn a Task sub-agent with the following prompt structure:

```
You are running an executive council debate to refine a strategic recommendation.

Read the strategic analysis at: {strategic_analysis_file_path}
Read memory indexes: memory/initiatives/_index.md, memory/people/_index.md
Read persona definitions from: skills/think/manifesto.md

Execute Mode C (executive-council):
1. Load organizational context (initiatives, key people)
2. Conduct CPO/CTO debate about the recommendation
3. Synthesize verdict with risk mitigation and next steps

Return your findings in this JSON structure:
{
  "cpo_position": "...",
  "cto_position": "...",
  "debate_summary": "...",
  "verdict": "...",
  "risk_mitigation": ["..."],
  "next_steps": [{"action": "...", "owner": "..."}],
  "full_output_markdown": "..."
}
```

##### Sub-agent input/output contracts

| Sub-agent | Input | Output | Failure mode |
|-----------|-------|--------|-------------|
| Validation council | Strategic analysis file path | JSON: weakest assumption, persona critiques, kill criteria, full markdown output | Report partial results; main agent synthesizes with available data |
| Executive council | Strategic analysis file path, memory indexes, manifesto.md | JSON: debate positions, verdict, next steps, full markdown output | Report partial results; main agent synthesizes with available data |

**Shared constraints for both sub-agents:**
- Read from the saved strategic analysis file, NEVER from main agent context
- Each sub-agent operates with isolated context (no shared state between them)
- Neither sub-agent should modify the strategic analysis file
- Both sub-agents must tag evidence with source confidence tiers

##### Collecting sub-agent results

After both sub-agents complete, collect their results. If either sub-agent fails:
- Log the failure in the output
- Synthesize final recommendation using whatever results are available
- Note which analysis layer is missing and recommend re-running it

#### 4. Final synthesis (sequential, main agent)
Combine all three layers into a hardened strategic recommendation:
- **Recommendation**: Final decision incorporating critiques from both sub-agents
- **Confidence**: Updated based on validation results
- **Risk mitigation**: How to address concerns from all personas (merged from both sub-agents)
- **Kill criteria**: Conditions under which to abandon this path (from validation sub-agent)
- **Next steps**: Immediate tactical actions with owners (from executive council sub-agent)

---

### Deep analysis output format

```markdown
# Deep analysis: [Topic]

## Final recommendation
[One paragraph synthesizing strategic-analysis + validation + executive-council]

**Confidence**: [High/Medium/Low] (updated after validation)

## Risk mitigation plan
| Risk source | Mitigation |
|-------------|------------|
| CFO concern | [How to address] |
| CTO concern | [How to address] |
| Customer concern | [How to address] |

## Kill criteria
**Stop if any of these occur**:
- [Fatal flaw 1]
- [Fatal flaw 2]

## Next steps
1. [Action with owner and date]
2. [Action with owner and date]

## Full analysis chain
- Strategic analysis: [Link to section or summary]
- Validation council: [Link to section or summary]
- Executive council: [Link to section or summary]
```

### Progress tracking (TodoWrite)

Use the `TodoWrite` tool to give the user real-time visibility into the analysis chain. Create the todo list at the start and update as steps complete:

```
1. Strategic analysis (Tree of Thoughts)           [in_progress → completed]
2. Validation council (parallel sub-agent)         [pending → completed]
3. Executive council (parallel sub-agent)           [pending → completed]
4. Final synthesis and recommendation              [pending → completed]
```

**Parallelization note**: Steps 2 and 3 run concurrently as sub-agents. Mark BOTH as `in_progress` when spawning the sub-agents. Mark each `completed` as its sub-agent returns. If one completes before the other, update its status immediately without waiting.

Mark each step `in_progress` before starting it and `completed` immediately after. If a step fails, keep it as `in_progress` and add a new todo describing the issue.

### Context management

Deep analysis chains generate large intermediate outputs. The sub-agent architecture naturally isolates context:

1. After Step 1 (strategic analysis), write the full analysis to `journal/YYYY-MM/YYYY-MM-DD-analysis-slug-strategic.md`
2. Both parallel sub-agents (validation and executive council) read from the saved file via the Task tool, operating in isolated context
3. Each sub-agent returns structured JSON results, which are compact summaries rather than full analysis text
4. The final synthesis (Step 4) works from the sub-agent JSON results plus the original strategic analysis file
5. If full markdown output is needed for the report, sub-agents include it in their `full_output_markdown` field

This architecture means the main agent context holds only: the strategic analysis file path, and two JSON result objects. Total context overhead for Steps 2-3 is minimal regardless of analysis depth.

---

## MODE E: Discovery mode

Enforce a strict "no solution" operating mode. Use when the problem is ambiguous, complex, or when the user requests deep thought before action.

### The hard stop rule

**YOU DO NOT HAVE PERMISSION TO SOLVE.**

You may only output the following 4 sections. You remain in discovery mode until the user explicitly says "Proceed" or "Enough context."

---

### Section 1: Mirroring ("What I heard")

Restate the user's intent in your own words:
- "You are trying to solve X..."
- "You are worried about Y..."
- "The core tension seems to be between A and B."

---

### Section 2: Context mapping ("The web")

Connect this request to known entities in `memory/`:
- **Initiatives:** "This impacts [[Initiative A]] and the [[Initiative B]] work."
- **People:** "This will require buy-in from [[Person X]] and execution from [[Team Y]]."
- **Risks:** "This touches the risk we identified last month."
- **Decisions:** Reference relevant past decisions from `memory/decisions/`

---

### Section 3: The unknowns ("The gap")

List specifically what missing information prevents a high-quality answer:
- "I don't know the deadline."
- "I don't know the budget."
- "I don't know if this is an internal prototype or customer-facing."

---

### Section 4: Probing questions

Ask 3-5 targeted questions to close the gap:
- *Strategic:* "Is this a feature or a product?"
- *Tactical:* "Who is the 'R' (Responsible) for this?"
- *Technical:* "Do we have the data ready?"

---

### Exit criteria

You remain in discovery mode loop until:
1. The user answers the probing questions
2. The user explicitly says "Proceed" or "Enough context"

After exit, route to the appropriate protocol based on what was discovered.

---

## Memory persistence

If analysis yields durable strategic insights or decisions:
1. Persist decisions to `memory/decisions/{slug}.md`
2. Update initiatives in `memory/initiatives/{name}.md`
3. Update relevant `_index.md` files
4. Output memory updates section

---

## Source attribution tier table

Tag each evidence point, assumption, and finding with its source tier:

| Source | Confidence |
|--------|------------|
| Memory files, user input | High |
| Native tools (calendar, tasks) | High |
| MCP tools (project tracker, docs) | Medium-High |
| Web search | Medium-Low |
| LLM knowledge (no source) | Low -- flag explicitly |

---

## Context budgets

**Strategic analysis mode:**
- Memory: Read `_index.md` + up to 5 targeted files
- Journal: Read current month `_index.md` + up to 2 relevant entries
- Reference: decision frameworks (from skill, already loaded)

**Validation council mode:**
- Memory: Read `_index.md` + up to 3 targeted files for context
- Reference: decision frameworks (from skill, already loaded)

**Executive council mode:**
- Memory: Read `_index.md` for initiatives and people + up to 5 targeted files
- Reference: `skills/think/manifesto.md`

**Deep analysis mode:**
- Combined budgets from all three analysis layers
- Offload intermediate outputs to `journal/` to prevent context overflow

**Discovery mode:**
- Memory: Read `_index.md` for initiatives and people + up to 3 targeted files

---

## Absolute constraints

### Strategic analysis constraints
- NEVER skip the initial hypothesis (Layer 1)
- NEVER skip any of the three branches (Layer 2)
- NEVER omit constraint analysis (Layer 3)
- NEVER output recommendation without confidence and assumptions
- NEVER begin without stating framework selection

### Validation council constraints
- NEVER skip the vulnerability scan
- NEVER skip any persona in the assault
- NEVER output without the kill criteria section
- NEVER be constructive-only. The purpose is adversarial stress-testing.

### Executive council constraints
- Do not make up external facts
- Stick to defined personas
- Be decisive in the verdict
- Always reference specific organizational context (not generic advice)

### Deep analysis constraints
- NEVER skip any of the 3 analysis layers
- NEVER output final recommendation without completing validation
- ALWAYS include kill criteria
- ALWAYS specify owners for next steps

### Discovery mode constraints
- NEVER propose solutions in discovery mode
- NEVER skip context mapping (always check memory)
- NEVER ask open-ended questions (use bounded, targeted questions)

### Shared constraints
- NEVER begin without properly loading required reference files
- ALWAYS tag evidence and assumptions with source confidence
- NEVER skip memory persistence for durable insights
