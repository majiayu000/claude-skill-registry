---
name: brainstorm-with-file
description: Interactive brainstorming with parallel subagent collaboration, idea expansion, and documented thought evolution. Parallel multi-perspective analysis for Codex.
argument-hint: "TOPIC=\"<idea or topic>\" [--perspectives=creative,pragmatic,systematic] [--max-ideas=<n>]"
---

# Codex Brainstorm-With-File Workflow

## Quick Start

Interactive brainstorming workflow with **documented thought evolution**. Expands initial ideas through questioning, **parallel subagent analysis**, and iterative refinement.

**Core workflow**: Seed Idea → Expand → Parallel Subagent Explore → Synthesize → Refine → Crystallize

**Key features**:
- **brainstorm.md**: Complete thought evolution timeline
- **Parallel multi-perspective**: Creative + Pragmatic + Systematic (concurrent subagents)
- **Idea expansion**: Progressive questioning and exploration
- **Diverge-Converge cycles**: Generate options then focus on best paths

**Codex-Specific Features**:
- Parallel subagent execution via `spawn_agent` + batch `wait({ ids: [...] })`
- Role loading via path (agent reads `~/.codex/agents/*.md` itself)
- Deep interaction with `send_input` for multi-round refinement within single agent
- Explicit lifecycle management with `close_agent`

## Overview

This workflow enables iterative exploration and refinement of ideas through parallel-capable phases:

1. **Seed Understanding** - Parse the initial idea and identify exploration vectors
2. **Divergent Exploration** - Gather codebase context and execute parallel multi-perspective analysis
3. **Interactive Refinement** - Multi-round idea selection, deep-dive, and refinement via send_input
4. **Convergence & Crystallization** - Synthesize final ideas and generate recommendations

The key innovation is **documented thought evolution** that captures how ideas develop, perspectives differ, and insights emerge across all phases.

## Output Structure

```
{projectRoot}/.workflow/.brainstorm/BS-{slug}-{date}/
├── brainstorm.md                  # ⭐ Complete thought evolution timeline
├── exploration-codebase.json      # Phase 2: Codebase context
├── perspectives/                  # Phase 2: Individual perspective outputs
│   ├── creative.json
│   ├── pragmatic.json
│   └── systematic.json
├── perspectives.json              # Phase 2: Aggregated parallel findings with synthesis
├── synthesis.json                 # Phase 4: Final synthesis
└── ideas/                         # Phase 3: Individual idea deep-dives
    ├── idea-1.md
    ├── idea-2.md
    └── merged-idea-1.md
```

## Output Artifacts

### Phase 1: Seed Understanding

| Artifact | Purpose |
|----------|---------|
| `brainstorm.md` | Initialized with session metadata, seed expansion, and exploration vectors |
| Session variables | Topic slug, brainstorm mode, dimensions, exploration vectors |

### Phase 2: Divergent Exploration

| Artifact | Purpose |
|----------|---------|
| `exploration-codebase.json` | Codebase context: relevant files, patterns, architecture constraints |
| `perspectives/*.json` | Individual perspective outputs from parallel subagents |
| `perspectives.json` | Aggregated parallel findings with synthesis (convergent/conflicting themes) |
| Updated `brainstorm.md` | Round 2: Exploration results and multi-perspective analysis |

### Phase 3: Interactive Refinement

| Artifact | Purpose |
|----------|---------|
| `ideas/{idea-slug}.md` | Deep-dive analysis for selected ideas |
| Updated `brainstorm.md` | Round 3-6: User feedback, idea selections, refinement cycles |

### Phase 4: Convergence & Crystallization

| Artifact | Purpose |
|----------|---------|
| `synthesis.json` | Final synthesis: top ideas, recommendations, insights |
| Final `brainstorm.md` | Complete thought evolution with conclusions |

---

## Implementation Details

### Session Initialization

##### Step 0: Determine Project Root

检测项目根目录，确保 `.workflow/` 产物位置正确：

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

优先通过 git 获取仓库根目录；非 git 项目回退到 `pwd` 取当前绝对路径。
存储为 `{projectRoot}`，后续所有 `.workflow/` 路径必须以此为前缀。

The workflow automatically generates a unique session identifier and directory structure based on the topic and current date (UTC+8).

**Session ID Format**: `BS-{slug}-{date}`
- `slug`: Lowercase alphanumeric + Chinese characters, max 40 chars
- `date`: YYYY-MM-DD format (UTC+8)

**Session Directory**: `{projectRoot}/.workflow/.brainstorm/{sessionId}/`

**Auto-Detection**: If session folder exists with brainstorm.md, automatically enters continue mode. Otherwise, creates new session.

**Brainstorm Modes**:
- `creative`: Emphasize novelty and innovation, relaxed constraints
- `structured`: Balance creativity with feasibility, realistic scope
- `balanced`: Default, moderate innovation with practical considerations

---

## Phase 1: Seed Understanding

**Objective**: Parse the initial idea, identify exploration vectors, scope preferences, and initialize the brainstorm document.

### Step 1.1: Parse Seed & Identify Dimensions

The workflow analyzes the topic text against predefined brainstorm dimensions.

**Brainstorm Dimensions**:

| Dimension | Keywords |
|-----------|----------|
| technical | 技术, technical, implementation, code, 实现, architecture |
| ux | 用户, user, experience, UX, UI, 体验, interaction |
| business | 业务, business, value, ROI, 价值, market |
| innovation | 创新, innovation, novel, creative, 新颖 |
| feasibility | 可行, feasible, practical, realistic, 实际 |
| scalability | 扩展, scale, growth, performance, 性能 |
| security | 安全, security, risk, protection, 风险 |

**Matching Logic**: Compare topic text against keyword lists to identify relevant dimensions.

### Step 1.2: Role Selection

Recommend roles based on topic keywords, then let user confirm or override.

**Professional Roles** (recommended based on topic keywords):

| Role | Perspective Agent Focus | Keywords |
|------|------------------------|----------|
| system-architect | Architecture, patterns | 架构, architecture, system, 系统, design pattern |
| product-manager | Business value, roadmap | 产品, product, feature, 功能, roadmap |
| ui-designer | Visual design, interaction | UI, 界面, interface, visual, 视觉 |
| ux-expert | User research, usability | UX, 体验, experience, user, 用户 |
| data-architect | Data modeling, storage | 数据, data, database, 存储, storage |
| test-strategist | Quality, testing | 测试, test, quality, 质量, QA |
| subject-matter-expert | Domain knowledge | 领域, domain, industry, 行业, expert |

**Simple Perspectives** (fallback - always available):

| Perspective | Focus | Best For |
|-------------|-------|----------|
| creative | Innovation, cross-domain | Generating novel ideas |
| pragmatic | Implementation, feasibility | Reality-checking ideas |
| systematic | Architecture, structure | Organizing solutions |

**Selection Strategy**:
1. **Auto mode**: Select top 3 recommended professional roles based on keyword matching
2. **Manual mode**: Present recommended roles + "Use simple perspectives" option
3. **Continue mode**: Use roles from previous session

### Step 1.3: Initial Scoping (New Session Only)

For new brainstorm sessions, gather user preferences before exploration.

**Brainstorm Mode** (Single-select):
- 创意模式 (Creative mode - 15-20 minutes, 1 subagent)
- 平衡模式 (Balanced mode - 30-60 minutes, 3 parallel subagents)
- 深度模式 (Deep mode - 1-2+ hours, 3 parallel subagents + deep refinement)

**Focus Areas** (Multi-select):
- 技术方案 (Technical solutions)
- 用户体验 (User experience)
- 创新突破 (Innovation breakthroughs)
- 可行性评估 (Feasibility assessment)

**Constraints** (Multi-select):
- 现有架构 (Existing architecture constraints)
- 时间限制 (Time constraints)
- 资源限制 (Resource constraints)
- 无约束 (No constraints)

### Step 1.4: Expand Seed into Exploration Vectors

Generate key questions that guide the brainstorming exploration. Use a subagent for vector generation.

**Exploration Vectors**:
1. **Core question**: What is the fundamental problem/opportunity?
2. **User perspective**: Who benefits and how?
3. **Technical angle**: What enables this technically?
4. **Alternative approaches**: What other ways could this be solved?
5. **Challenges**: What could go wrong or block success?
6. **Innovation angle**: What would make this 10x better?
7. **Integration**: How does this fit with existing systems/processes?

**Subagent for Vector Generation**:

```javascript
const vectorAgent = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-explore-agent.md (MUST read first)

---

## Context
Topic: ${idea_or_topic}
User focus areas: ${userFocusAreas.join(', ')}
Constraints: ${constraints.join(', ')}

## Task
Generate 5-7 exploration vectors (questions/directions) to expand this idea:
1. Core question: What is the fundamental problem/opportunity?
2. User perspective: Who benefits and how?
3. Technical angle: What enables this technically?
4. Alternative approaches: What other ways could this be solved?
5. Challenges: What could go wrong or block success?
6. Innovation angle: What would make this 10x better?
7. Integration: How does this fit with existing systems/processes?

## Deliverables
Return structured exploration vectors for multi-perspective analysis.
`
})

const result = wait({ ids: [vectorAgent], timeout_ms: 120000 })
close_agent({ id: vectorAgent })
```

**Purpose**: These vectors guide each perspective subagent's analysis and ensure comprehensive exploration.

### Step 1.5: Initialize brainstorm.md

Create the main brainstorm document with session metadata and expansion content.

**brainstorm.md Structure**:
- **Header**: Session ID, topic, start time, brainstorm mode, dimensions
- **Initial Context**: Focus areas, depth level, constraints
- **Roles**: Selected roles (professional or simple perspectives)
- **Seed Expansion**: Original idea + exploration vectors
- **Thought Evolution Timeline**: Round-by-round findings
- **Current Ideas**: To be populated after exploration

**Success Criteria**:
- Session folder created successfully
- brainstorm.md initialized with all metadata
- 1-3 roles selected (professional or simple perspectives)
- Brainstorm mode and dimensions identified
- Exploration vectors generated
- User preferences captured

---

## Phase 2: Divergent Exploration

**Objective**: Gather codebase context and execute parallel multi-perspective analysis via subagents to generate diverse viewpoints.

**Execution Model**: Parallel subagent execution - spawn 3 perspective agents simultaneously, batch wait for all results, then aggregate.

**Key API Pattern**:
```
spawn_agent × 3 → wait({ ids: [...] }) → aggregate → close_agent × 3
```

### Step 2.1: Codebase Context Gathering

Use built-in tools to understand the codebase structure before spawning perspective agents.

**Context Gathering Activities**:
1. **Get project structure** - Execute `ccw tool exec get_modules_by_depth '{}'`
2. **Search for related code** - Use Grep/Glob to find files matching topic keywords
3. **Read project tech context** - Load `{projectRoot}/.workflow/project-tech.json` if available
4. **Analyze patterns** - Identify common code patterns and architecture decisions

**exploration-codebase.json Structure**:
- `relevant_files[]`: Files related to the topic with relevance indicators
- `existing_patterns[]`: Common code patterns and architectural styles
- `architecture_constraints[]`: Project-level constraints
- `integration_points[]`: Key integration patterns between modules
- `_metadata`: Timestamp and context information

### Step 2.2: Parallel Multi-Perspective Analysis

**⚠️ IMPORTANT**: Role files are NOT read by main process. Pass path in message, agent reads itself.

Spawn 3 perspective agents in parallel: Creative + Pragmatic + Systematic.

**Perspective Definitions**:

| Perspective | Role File | Focus |
|-------------|-----------|-------|
| Creative | `~/.codex/agents/cli-explore-agent.md` | Innovation, cross-domain inspiration, challenging assumptions |
| Pragmatic | `~/.codex/agents/cli-explore-agent.md` | Implementation feasibility, effort estimates, blockers |
| Systematic | `~/.codex/agents/cli-explore-agent.md` | Problem decomposition, patterns, scalability |

**Parallel Subagent Execution**:

```javascript
// Build shared context from codebase exploration
const explorationContext = `
CODEBASE CONTEXT:
- Key files: ${explorationResults.relevant_files.slice(0,5).map(f => f.path).join(', ')}
- Existing patterns: ${explorationResults.existing_patterns.slice(0,3).join(', ')}
- Architecture constraints: ${explorationResults.architecture_constraints.slice(0,3).join(', ')}`

// Define perspectives
const perspectives = [
  {
    name: 'creative',
    focus: 'Innovation and novelty',
    tasks: [
      'Think beyond obvious solutions - what would be surprising/delightful?',
      'Explore cross-domain inspiration',
      'Challenge assumptions - what if the opposite were true?',
      'Generate moonshot ideas alongside practical ones'
    ]
  },
  {
    name: 'pragmatic',
    focus: 'Implementation reality',
    tasks: [
      'Evaluate technical feasibility of core concept',
      'Identify existing patterns/libraries that could help',
      'Estimate implementation complexity',
      'Highlight potential technical blockers'
    ]
  },
  {
    name: 'systematic',
    focus: 'Architecture thinking',
    tasks: [
      'Decompose the problem into sub-problems',
      'Identify architectural patterns that apply',
      'Map dependencies and interactions',
      'Consider scalability implications'
    ]
  }
]

// Parallel spawn - all agents start immediately
const agentIds = perspectives.map(perspective => {
  return spawn_agent({
    message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-explore-agent.md (MUST read first)
2. Read: ${projectRoot}/.workflow/project-tech.json
3. Read: ${projectRoot}/.workflow/project-guidelines.json

---

## Brainstorm Context
Topic: ${idea_or_topic}
Perspective: ${perspective.name} - ${perspective.focus}
Session: ${sessionFolder}

${explorationContext}

## ${perspective.name.toUpperCase()} Perspective Tasks
${perspective.tasks.map(t => `• ${t}`).join('\n')}

## Deliverables
Write findings to: ${sessionFolder}/perspectives/${perspective.name}.json

Schema: {
  perspective: "${perspective.name}",
  ideas: [{ title, description, novelty, feasibility, rationale }],
  key_findings: [],
  challenged_assumptions: [],
  open_questions: [],
  _metadata: { perspective, timestamp }
}

## Success Criteria
- [ ] Role definition read
- [ ] 3-5 ideas generated with ratings
- [ ] Key findings documented
- [ ] JSON output follows schema
`
  })
})

// Batch wait - TRUE PARALLELISM (key Codex advantage)
const results = wait({
  ids: agentIds,
  timeout_ms: 600000  // 10 minutes for all
})

// Handle timeout
if (results.timed_out) {
  // Some agents may still be running
  // Option: continue waiting or use completed results
}

// Collect results from all perspectives
const completedFindings = {}
agentIds.forEach((agentId, index) => {
  const perspective = perspectives[index]
  if (results.status[agentId].completed) {
    completedFindings[perspective.name] = results.status[agentId].completed
  }
})

// Batch cleanup
agentIds.forEach(id => close_agent({ id }))
```

### Step 2.3: Aggregate Multi-Perspective Findings

Consolidate results from all three parallel perspective agents.

**perspectives.json Structure**:
- `session_id`: Reference to brainstorm session
- `timestamp`: Completion time
- `topic`: Original idea/topic
- `creative`: Creative perspective findings (ideas with novelty ratings)
- `pragmatic`: Pragmatic perspective findings (approaches with effort ratings)
- `systematic`: Systematic perspective findings (architectural options)
- `synthesis`: {convergent_themes, conflicting_views, unique_contributions}
- `aggregated_ideas[]`: Merged ideas from all perspectives
- `key_findings[]`: Main insights across all perspectives

**Aggregation Activities**:
1. Extract ideas and findings from each perspective's output
2. Identify themes all perspectives agree on (convergent)
3. Note conflicting views and tradeoffs
4. Extract unique contributions from each perspective
5. Merge and deduplicate similar ideas

```javascript
const synthesis = {
  session_id: sessionId,
  timestamp: new Date().toISOString(),
  topic: idea_or_topic,

  // Individual perspective findings
  creative: completedFindings.creative || {},
  pragmatic: completedFindings.pragmatic || {},
  systematic: completedFindings.systematic || {},

  // Cross-perspective synthesis
  synthesis: {
    convergent_themes: extractConvergentThemes(completedFindings),
    conflicting_views: extractConflicts(completedFindings),
    unique_contributions: extractUniqueInsights(completedFindings)
  },

  // Aggregated for refinement
  aggregated_ideas: mergeAllIdeas(completedFindings),
  key_findings: mergeKeyFindings(completedFindings)
}
```

### Step 2.4: Update brainstorm.md

Append exploration results to the brainstorm timeline.

**Round 2 Sections** (Multi-Perspective Exploration):
- **Creative Perspective**: Novel ideas with novelty/impact ratings
- **Pragmatic Perspective**: Practical approaches with effort/risk ratings
- **Systematic Perspective**: Architectural options with tradeoff analysis
- **Perspective Synthesis**: Convergent themes, conflicts, unique contributions

**Documentation Standards**:
- Include evidence from codebase exploration
- Organize findings by perspective
- Highlight areas of agreement and disagreement
- Note key assumptions and reasoning

**Success Criteria**:
- All 3 subagents spawned and completed (or timeout handled)
- `exploration-codebase.json` created with comprehensive context
- `perspectives/*.json` created for each perspective
- `perspectives.json` created with aggregated findings and synthesis
- `brainstorm.md` updated with Round 2 results
- All agents closed properly
- Ready for interactive refinement phase

---

## Phase 3: Interactive Refinement

**Objective**: Iteratively refine ideas through multi-round user-guided exploration cycles with deep dives, challenge testing, and idea merging.

**Max Rounds**: 6 refinement rounds (can exit earlier if user indicates completion)

**Execution Model**: Use `send_input` for deep interaction within same agent context, or spawn new agent for significantly different exploration angles.

### Step 3.1: Present Findings & Gather User Direction

Display current ideas and perspectives to the user.

**Presentation Content**:
- Top ideas from each perspective with ratings
- Convergent themes and areas of agreement
- Conflicting views and tradeoffs
- Open questions for further exploration

**User Feedback Options** (Single-select):

| Option | Purpose | Next Action |
|--------|---------|------------|
| **深入探索** | Explore selected ideas in detail | `send_input` to active agent OR spawn deep-dive agent |
| **继续发散** | Generate more ideas | Spawn new agent with different angles |
| **挑战验证** | Test ideas critically | Spawn challenge agent (devil's advocate) |
| **合并综合** | Combine multiple ideas | Spawn merge agent to synthesize |
| **准备收敛** | Begin convergence | Exit refinement loop for synthesis |

### Step 3.2: Deep Dive on Selected Ideas (via send_input or new agent)

When user selects "deep dive", provide comprehensive analysis.

**Option A: send_input to Existing Agent** (preferred if agent still active)

```javascript
// Continue with existing agent context
send_input({
  id: perspectiveAgent,  // Reuse agent from Phase 2 if not closed
  message: `
## CONTINUATION: Deep Dive Analysis

Based on your initial exploration, the user wants deeper investigation on these ideas:
${selectedIdeas.map((idea, i) => `${i+1}. ${idea.title}`).join('\n')}

## Deep Dive Tasks
• Elaborate each concept in detail
• Identify implementation requirements and dependencies
• Analyze potential challenges and propose mitigations
• Suggest proof-of-concept approach
• Define success metrics

## Deliverables
Write to: ${sessionFolder}/ideas/{idea-slug}.md for each selected idea

## Success Criteria
- [ ] Each idea has detailed breakdown
- [ ] Technical requirements documented
- [ ] Risk analysis with mitigations
`
})

const deepDiveResult = wait({ ids: [perspectiveAgent], timeout_ms: 600000 })
```

**Option B: Spawn New Deep-Dive Agent** (if prior agents closed)

```javascript
const deepDiveAgent = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-explore-agent.md (MUST read first)
2. Read: ${sessionFolder}/perspectives.json (prior findings)
3. Read: ${projectRoot}/.workflow/project-tech.json

---

## Deep Dive Context
Topic: ${idea_or_topic}
Selected Ideas: ${selectedIdeas.map(i => i.title).join(', ')}

## Deep Dive Tasks
${selectedIdeas.map(idea => `
### ${idea.title}
• Elaborate the core concept in detail
• Identify implementation requirements
• List potential challenges and mitigations
• Suggest proof-of-concept approach
• Define success metrics
`).join('\n')}

## Deliverables
Write: ${sessionFolder}/ideas/{idea-slug}.md for each idea

Include for each:
- Detailed concept description
- Technical requirements list
- Risk/challenge matrix
- MVP definition
- Success criteria
`
})

const result = wait({ ids: [deepDiveAgent], timeout_ms: 600000 })
close_agent({ id: deepDiveAgent })
```

### Step 3.3: Devil's Advocate Challenge (spawn new agent)

When user selects "challenge", spawn a dedicated challenge agent.

```javascript
const challengeAgent = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-explore-agent.md (MUST read first)
2. Read: ${sessionFolder}/perspectives.json (ideas to challenge)

---

## Challenge Context
Topic: ${idea_or_topic}
Ideas to Challenge:
${selectedIdeas.map((idea, i) => `${i+1}. ${idea.title}: ${idea.description}`).join('\n')}

## Devil's Advocate Tasks
• For each idea, identify 3 strongest objections
• Challenge core assumptions
• Identify scenarios where this fails
• Consider competitive/alternative solutions
• Assess whether this solves the right problem
• Rate survivability after challenge (1-5)

## Deliverables
Return structured challenge results:
{
  challenges: [{
    idea: "...",
    objections: [],
    challenged_assumptions: [],
    failure_scenarios: [],
    alternatives: [],
    survivability_rating: 1-5,
    strengthened_version: "..."
  }]
}

## Success Criteria
- [ ] 3+ objections per idea
- [ ] Assumptions explicitly challenged
- [ ] Survivability ratings assigned
`
})

const result = wait({ ids: [challengeAgent], timeout_ms: 300000 })
close_agent({ id: challengeAgent })
```

### Step 3.4: Merge Multiple Ideas (spawn merge agent)

When user selects "merge", synthesize complementary ideas.

```javascript
const mergeAgent = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-explore-agent.md (MUST read first)
2. Read: ${sessionFolder}/perspectives.json (source ideas)

---

## Merge Context
Topic: ${idea_or_topic}
Ideas to Merge:
${selectedIdeas.map((idea, i) => `
${i+1}. ${idea.title} (${idea.source_perspective})
   ${idea.description}
   Strengths: ${idea.strengths?.join(', ') || 'N/A'}
`).join('\n')}

## Merge Tasks
• Identify complementary elements
• Resolve contradictions
• Create unified concept
• Preserve key strengths from each
• Describe the merged solution
• Assess viability of merged idea

## Deliverables
Write to: ${sessionFolder}/ideas/merged-idea-{n}.md

Include:
- Merged concept description
- Elements taken from each source idea
- Contradictions resolved (or noted as tradeoffs)
- New combined strengths
- Implementation considerations

## Success Criteria
- [ ] Coherent merged concept
- [ ] Source attributions clear
- [ ] Contradictions addressed
`
})

const result = wait({ ids: [mergeAgent], timeout_ms: 300000 })
close_agent({ id: mergeAgent })
```

### Step 3.5: Document Each Round

Update brainstorm.md with results from each refinement round.

**Round N Sections** (Rounds 3-6):

| Section | Content |
|---------|---------|
| User Direction | Action taken and ideas selected |
| Findings | New findings and clarifications |
| Idea Updates | Changes to idea scores and status |
| Insights | Key learnings and realizations |
| Next Directions | Suggested follow-up investigations |

**Documentation Standards**:
- Clear timestamps and action taken
- Evidence-based findings with code references
- Updated idea rankings and status changes
- Explicit tracking of assumption changes
- Organized by exploration vector

**Success Criteria**:
- User feedback processed for each round
- `brainstorm.md` updated with all refinement rounds
- Ideas in `ideas/` folder for selected deep-dives
- All spawned agents closed properly
- Exit condition reached (user selects converge or max rounds)

---

## Phase 4: Convergence & Crystallization

**Objective**: Synthesize final ideas, generate conclusions and recommendations, and offer next steps.

### Step 4.1: Consolidate Insights

Extract and synthesize all findings from refinement rounds into final conclusions.

**Consolidation Activities**:
1. Review all refinement rounds and accumulated findings
2. Rank ideas by score, feasibility, and impact
3. Identify top 5 viable ideas
4. Extract key learnings and insights
5. Generate recommendations with rationale

**synthesis.json Structure**:
- `session_id`: Session identifier
- `topic`: Original idea/topic
- `completed`: Completion timestamp
- `total_rounds`: Number of refinement rounds
- `top_ideas[]`: Top 5 ranked ideas with scores and next steps
- `parked_ideas[]`: Ideas parked for future consideration
- `key_insights[]`: Key learnings from brainstorming process
- `recommendations`: Primary recommendation and alternatives
- `follow_up[]`: Suggested next steps (implementation, research, validation)

**Idea Format**:
- `title`: Clear, descriptive title
- `description`: Complete concept description
- `source_perspective`: Which perspective(s) contributed
- `score`: Final viability score (1-10)
- `novelty`: Novelty/innovation rating (1-5)
- `feasibility`: Implementation feasibility (1-5)
- `key_strengths`: Main advantages and benefits
- `main_challenges`: Key challenges and limitations
- `next_steps`: Recommended actions to pursue

### Step 4.2: Final brainstorm.md Update

Append conclusions section and finalize the thinking document.

**Synthesis & Conclusions Section**:
- **Executive Summary**: High-level overview of brainstorming results
- **Top Ideas**: Ranked list with descriptions and strengths/challenges
- **Primary Recommendation**: Best path forward with clear rationale
- **Alternative Approaches**: Other viable options with tradeoff analysis
- **Parked Ideas**: Future considerations with potential triggers
- **Key Insights**: Important learnings from the process

**Session Statistics**:
- Total refinement rounds completed
- Ideas generated and evaluated
- Ideas survived challenges
- Perspectives used (creative, pragmatic, systematic)
- Artifacts generated

### Step 4.3: Post-Completion Options

Offer user follow-up actions based on brainstorming results.

**Available Options**:

| Option | Purpose | Action |
|--------|---------|--------|
| **创建实施计划** | Plan implementation of top idea | Launch `workflow:lite-plan` |
| **创建Issue** | Track top ideas for later | Launch `issue:new` with ideas |
| **深入分析** | Analyze top idea in detail | Launch `workflow:analyze-with-file` |
| **导出分享** | Generate shareable report | Create formatted report document |
| **完成** | No further action | End workflow |

**Success Criteria**:
- `synthesis.json` created with complete synthesis
- `brainstorm.md` finalized with all conclusions
- User offered meaningful next step options
- Session complete and all artifacts available

---

## Configuration

### Brainstorm Dimensions Reference

Dimensions guide brainstorming scope and focus:

| Dimension | Keywords | Best For |
|-----------|----------|----------|
| technical | 技术, technical, implementation, code | Implementation approaches |
| ux | 用户, user, experience, UI | User-facing design ideas |
| business | 业务, business, value | Business model innovations |
| innovation | 创新, innovation, novel | Breakthrough ideas |
| feasibility | 可行, feasible, practical | Realistic approaches |
| scalability | 扩展, scale, growth | Large-scale solutions |
| security | 安全, security, risk | Security considerations |

### Brainstorm Modes

| Mode | Duration | Intensity | Subagents |
|------|----------|-----------|-----------|
| Creative | 15-20 min | High novelty | 1 agent, short timeout |
| Balanced | 30-60 min | Mixed | 3 parallel agents |
| Deep | 1-2+ hours | Comprehensive | 3 parallel agents + deep refinement |

### Collaboration Patterns

| Pattern | Usage | Description |
|---------|-------|-------------|
| Parallel Divergence | New topic | All perspectives explore simultaneously via parallel subagents |
| Sequential Deep-Dive | Promising idea | `send_input` to one agent for elaboration, others critique via new agents |
| Debate Mode | Controversial approach | Spawn opposing agents to argue for/against |
| Synthesis Mode | Ready to decide | Spawn synthesis agent combining insights from all perspectives |

### Context Overflow Protection

**Per-Agent Limits**:
- Main analysis output: < 3000 words
- Sub-document (if any): < 2000 words each
- Maximum sub-documents: 5 per perspective

**Synthesis Protection**:
- If total analysis > 100KB, synthesis reads only main analysis files (not sub-documents)
- Large ideas automatically split into separate idea documents in ideas/ folder

**Recovery Steps**:
1. Check agent outputs for truncation or overflow
2. Reduce scope: fewer perspectives or simpler topic
3. Use structured brainstorm mode for more focused output
4. Split complex topics into multiple sessions

---

## Error Handling & Recovery

| Situation | Action | Recovery |
|-----------|--------|----------|
| **Subagent timeout** | Check `results.timed_out`, continue `wait()` or use partial results | Reduce scope, use 2 perspectives instead of 3 |
| **Agent closed prematurely** | Cannot recover closed agent | Spawn new agent with prior context from perspectives.json |
| **Parallel agent partial failure** | Some perspectives complete, some fail | Use completed results, note gaps in synthesis |
| **send_input to closed agent** | Error: agent not found | Spawn new agent with prior findings as context |
| **No good ideas** | Reframe problem or adjust constraints | Try new exploration angles |
| **User disengaged** | Summarize progress and offer break | Save state, keep agents alive for resume |
| **Perspectives conflict** | Present as tradeoff options | Let user select preferred direction |
| **Max rounds reached** | Force synthesis phase | Highlight unresolved questions |
| **Session folder conflict** | Append timestamp suffix | Create unique folder |

### Codex-Specific Error Patterns

```javascript
// Safe parallel execution with error handling
try {
  const agentIds = perspectives.map(p => spawn_agent({ message: buildPrompt(p) }))

  const results = wait({ ids: agentIds, timeout_ms: 600000 })

  if (results.timed_out) {
    // Handle partial completion
    const completed = agentIds.filter(id => results.status[id].completed)
    const pending = agentIds.filter(id => !results.status[id].completed)

    // Option 1: Continue waiting for pending
    // const moreResults = wait({ ids: pending, timeout_ms: 300000 })

    // Option 2: Use partial results
    // processPartialResults(completed, results)
  }

  // Process all results
  processResults(agentIds, results)

} finally {
  // ALWAYS cleanup, even on errors
  agentIds.forEach(id => {
    try { close_agent({ id }) } catch (e) { /* ignore */ }
  })
}
```

---

## Iteration Patterns

### First Brainstorm Session (Parallel Mode)

```
User initiates: TOPIC="idea or topic"
   ├─ No session exists → New session mode
   ├─ Parse topic and identify dimensions
   ├─ Scope with user (focus, depth, mode)
   ├─ Create brainstorm.md
   ├─ Expand seed into vectors
   ├─ Gather codebase context
   │
   ├─ Execute parallel perspective exploration:
   │   ├─ spawn_agent × 3 (Creative + Pragmatic + Systematic)
   │   ├─ wait({ ids: [...] })  ← TRUE PARALLELISM
   │   └─ close_agent × 3
   │
   ├─ Aggregate findings with synthesis
   └─ Enter multi-round refinement loop
```

### Continue Existing Session

```
User resumes: TOPIC="same topic"
   ├─ Session exists → Continue mode
   ├─ Load previous brainstorm.md
   ├─ Load perspectives.json
   └─ Resume from last refinement round
```

### Refinement Loop (Rounds 3-6)

```
Each round:
   ├─ Present current findings and top ideas
   ├─ Gather user feedback (deep dive/diverge/challenge/merge/converge)
   ├─ Process response:
   │   ├─ Deep Dive → send_input to active agent OR spawn deep-dive agent
   │   ├─ Diverge → spawn new agent with different angles
   │   ├─ Challenge → spawn challenge agent (devil's advocate)
   │   ├─ Merge → spawn merge agent to synthesize
   │   └─ Converge → Exit loop for synthesis
   ├─ wait({ ids: [...] }) for result
   ├─ Update brainstorm.md
   └─ Repeat until user selects converge or max rounds reached
```

### Agent Lifecycle Management

```
Subagent lifecycle:
   ├─ spawn_agent({ message }) → Create with role path + task
   ├─ wait({ ids, timeout_ms }) → Get results (ONLY way to get output)
   ├─ send_input({ id, message }) → Continue interaction (if not closed)
   └─ close_agent({ id }) → Cleanup (MUST do, cannot recover)

Key rules:
   ├─ NEVER close before you're done with an agent
   ├─ ALWAYS use wait() to get results, NOT close_agent()
   ├─ Batch wait for parallel agents: wait({ ids: [a, b, c] })
   └─ Consider keeping agents alive for send_input during refinement
```

### Completion Flow

```
Final synthesis:
   ├─ Consolidate all findings into top ideas
   ├─ Generate synthesis.json
   ├─ Update brainstorm.md with final conclusions
   ├─ close_agent for any remaining active agents
   ├─ Offer follow-up options
   └─ Archive session artifacts
```

---

## Best Practices

### Before Starting Brainstorm

1. **Clear Topic Definition**: Detailed topics lead to better dimension identification
2. **User Context**: Understanding preferences helps guide brainstorming intensity
3. **Scope Understanding**: Being clear about time/scope expectations sets correct exploration level

### During Brainstorming

1. **Review Perspectives**: Check all three perspectives before refinement rounds
2. **Document Assumptions**: Track what you think is true for correction later
3. **Use Continue Mode**: Resume sessions to build on previous exploration
4. **Embrace Conflicts**: Perspective conflicts often reveal important tradeoffs
5. **Iterate Thoughtfully**: Each refinement round should meaningfully advance ideas

### Codex Subagent Best Practices

1. **Role Path, Not Content**: Pass `~/.codex/agents/*.md` path in message, let agent read itself
2. **Parallel for Perspectives**: Use batch spawn + wait for 3 perspective agents
3. **Delay close_agent for Refinement**: Keep perspective agents alive for `send_input` reuse
4. **Batch wait**: Use `wait({ ids: [a, b, c] })` for parallel agents, not sequential waits
5. **Handle Timeouts**: Check `results.timed_out` and decide: continue waiting or use partial results
6. **Explicit Cleanup**: Always `close_agent` when done, even on errors (use try/finally pattern)
7. **send_input vs spawn**: Prefer `send_input` for same-context deep-dive, `spawn` for new exploration angles

### Documentation Practices

1. **Evidence-Based**: Every idea should reference codebase patterns or feasibility analysis
2. **Perspective Diversity**: Capture viewpoints from all three perspectives
3. **Timeline Clarity**: Use clear timestamps for traceability
4. **Evolution Tracking**: Document how ideas changed and evolved
5. **Action Items**: Generate specific, implementable recommendations
6. **Synthesis Quality**: Ensure convergent/conflicting themes are clearly documented

---

**Now execute the brainstorm-with-file workflow for topic**: $TOPIC
