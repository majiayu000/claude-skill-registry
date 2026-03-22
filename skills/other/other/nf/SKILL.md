---
name: nf
description: >-
  Conduct in-depth feature discovery interview to explore, challenge, and document a new feature.
  Use when asked to 'detail a feature', 'explore a new feature', 'feature discovery',
  'interview about feature', or 'spec out a feature'. NOT for quick brainstorming (use /brainstorm),
  NOT for PRD/JTBD docs (use /product), NOT for implementation tasks (use /ct).
argument-hint: [feature-name]
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion, Task, Skill
---

# New Feature Discovery

## Objective
Conduct a comprehensive interview to fully understand and document a new feature using collaborative brainstorming, then create a formal specification.

## Guidelines
- Invoke design-exploration skill first for discovery and exploration
- **Use `AskUserQuestion` tool for ALL clarifications** - provides interactive options for user to choose from
- **Never assume behavior**: if any behavior is unclear/ambiguous (UX flow, edge cases, error handling, states), you MUST ask the user to define expected behavior (preferred via `AskUserQuestion`).
- Ask non-obvious and thought-provoking questions
- Actively challenge assumptions; do not be a yes-boy. Grill.
- Offer alternatives, shortcuts, and "go deeper" paths
- Continue until the feature is fully understood
- Document everything in the specification file

## Workflow

### Mobile-app Skill Gate (MANDATORY when feature touches `mobile-app/`)

**Trigger:** If the feature will **create or modify any code under `mobile-app/`** (new screens/components, animations, lists, navigation, Expo APIs).

**MANDATORY steps (do BEFORE writing recommendations/implementation details in the discovery/spec):**
- Read the skill docs:
  - `.claude/skills/react-native-expo-mobile/SKILL.md`
  - `.claude/skills/react-native-expo-mobile/AGENTS.md`
- Explicitly state in the discovery/spec that the skill was read and will be applied in implementation.
- Extract the relevant rules for this feature area (minimum: Core Rendering; plus Animation/List Performance/React Compiler/UI as applicable) and record them under a short section like: "Skill Compliance: react-native-expo-mobile".

### Step 1: Codebase Exploration

Launch 1-3 parallel Explore agents (with Sonnet) based on feature complexity. Use Task tool in **single message**.

**Agents:**
1. Code & patterns in `backend/`
2. Data models, schemas, APIs (if 2+ agents)
3. Docs, ADRs, tests (if 3 agents)

Synthesize findings, then proceed to design exploration.

### Step 2: External Research (If Needed)

When you need current information, best practices, or technical research:

- **Quick lookups**: Use Exa MCP tools (`get_code_context_exa`, `web_search_exa`) directly
- **In-depth research**: Spawn `comprehensive-researcher` subagent via Task tool for complex topics requiring multiple sources and cross-verification

Topics to research:
- Industry best practices for the feature type
- Competitor implementations and patterns
- API/library capabilities and limitations
- Security considerations and compliance requirements

### Step 3: Design Exploration Phase
**Invoke the `design-exploration` skill** with gathered context:
- Ask questions to refine the idea (batch related questions)
- Propose 2-3 different approaches with trade-offs
- Present design incrementally (200-300 word sections) for validation

### Step 4: "Grill Me" Challenge Round
After initial design exploration, run a structured challenge:
- Identify assumptions and question each one
- Suggest 2-3 alternative approaches (including a "lean/shortcut" path), if applicable and worth it
- Flag potential risks, hidden costs, or complexity traps
- Recommend where to cut scope vs where to deepen investment

### Step 5: Deep-Dive Questions
After design exploration, ask additional **non-obvious** questions if needed:

**Technical Implementation:**
- Edge cases and failure scenarios
- Performance implications at scale
- Integration points with existing systems
- Security and privacy implications

**UI/UX:**
- User mental models and expectations
- Error states and recovery flows
- Accessibility considerations

**Business & Product:**
- Success metrics and how to measure them
- MVP vs future scope boundaries
- Potential abuse scenarios

**Tradeoffs:**
- Complexity vs flexibility
- Development speed vs technical debt
- Short-term wins vs long-term maintainability

### Step 6: Specification Writing

After design exploration and interview completion:

1. **Read template**: Read `docs/product-docs/templates/discovery-template.md` to load the structure
2. **Create task directory**: `tasks/task-YYYY-MM-DD-[feature-name]/`
3. **Write specification** following the template structure
   - Output file: `discovery-[feature-name].md`
4. **Present summary** to user for confirmation

**If design exploration reveals the feature is not viable**: Document the reasons in a brief `discovery-[feature-name]-rejected.md` with rationale, and stop here.

### Step 7: Codex Validation

After discovery document is created, invoke `/codex-cli` skill for cross-AI validation.

**Verification focus:** Discovery document review as senior product analyst
- Completeness, consistency, clarity, feasibility, scope definition
- No conflicts with existing codebase architecture and patterns
- No critical gaps or missing considerations

**Process feedback:** Update discovery if needed, add "Cross-AI Validation: PASSED" when approved.

**If validation fails:** Present the issues to the user via `AskUserQuestion` with options: "Revise discovery doc", "Override and proceed", "Abandon feature".

## Output
`tasks/task-YYYY-MM-DD-[feature-name]/discovery-[feature-name].md`
