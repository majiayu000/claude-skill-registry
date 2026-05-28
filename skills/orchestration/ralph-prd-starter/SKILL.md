---
name: ralph-prd-starter
description: Project-agnostic agent setup wizard for Ralph Orchestra with Quick Start, Standard, and Expert modes
category: orchestration
depends-on: [shared-ralph-core]
version: 4.0
---

# Ralph PRD Starter

> "Set up Ralph Orchestra for YOUR project - custom agents, skills, and configs in minutes."

## Quick Start

Invoke this command to start the setup wizard:
```
/ralph-prd-starter
```

The wizard will guide you through configuring Ralph Orchestra for your project.

## When to Use This Skill

Use `/ralph-prd-starter` when:
- Setting up Ralph Orchestra for a new project
- Adding custom agents to your project
- Reconfiguring existing agents
- Generating initial PRD from feature ideas
- Updating orchestration mode or workflow patterns

## Wizard Overview

### Three Configuration Modes

```
┌─────────────────────────────────────────────────────────────┐
│                    WIZARD ENTRY POINTS                      │
├─────────────────────────────────────────────────────────────┤
│  ⚡ Quick Start   (5 min)   → Choose a preset template      │
│  🎯 Standard      (15 min)  → Guided with recommendations   │
│  🔧 Expert        (30+ min) → Full customization            │
└─────────────────────────────────────────────────────────────┘
```

### Quick Start Flow (5 minutes)
1. Select project template (14 presets available)
2. Project name
3. Generate!

### Standard Mode Flow (15 minutes)
1. Deep project understanding
2. Agent selection with recommendations
3. Skill/sub-agent confirmation
4. Generate!

### Expert Mode Flow (30+ minutes)
1. Everything from Standard Mode
2. Per-agent skill configuration
3. Per-agent sub-agent selection
4. MCP server customization
5. Advanced settings

---

## Phase 1: Entry Point Selection

**Question:** How would you like to configure Ralph Orchestra?

| Option | Description | Best For |
|--------|-------------|----------|
| ⚡ **Quick Start** | Choose a named preset and customize project name | First-time users, common scenarios |
| 🎯 **Standard Mode** | Guided questions with AI recommendations | Most users, balanced approach |
| 🔧 **Expert Mode** | Full control over every configuration | Advanced users, custom needs |

**Flow Decision:**
- **Quick Start** → Go to Phase 2 (Presets)
- **Standard/Expert** → Go to Phase 3 (Project Deep Dive)

---

## Phase 2: Named Presets (Quick Start)

**Question:** Select a preset configuration for your project:

### 🎮 Game Development Presets

| Preset | Agents | Skills | Sub-Agents | Description |
|--------|--------|--------|------------|-------------|
| **Indie Game Dev** | PM, Dev, TA, QA, GD | 45 game dev skills | 18 sub-agents | Solo/small team 3D games with R3F |
| **Game Studio** | PM, Dev, TA, QA, GD | 50+ full stack skills | 25+ sub-agents | Professional game studio with multiplayer |
| **Mobile Game** | PM, Dev, TA, QA | Mobile-optimized skills | Mobile-specific sub-agents | iOS/Android games with performance focus |
| **Multiplayer Arena** | PM, Dev, TA, QA, GD | All networking + game skills | Colyseus-focused sub-agents | Server-authoritative multiplayer games |

### 🌐 Web Application Presets

| Preset | Agents | Skills | Sub-Agents | Description |
|--------|--------|--------|------------|-------------|
| **Modern Web App** | PM, Dev, QA | 25 web skills | 10 web sub-agents | React/Vue/Svelte single-page apps |
| **Full Stack SaaS** | PM, Dev, QA | 35 full-stack skills | 15 full-stack sub-agents | Complete web applications with backend |
| **Dashboard/Analytics** | PM, Dev, QA | Data visualization skills | Chart/visualization focused | Data-heavy applications with charts |
| **Content Platform** | PM, Dev, QA, GD | CMS + SEO skills | Content-focused | Blogs, docs, content sites |

### 🏢 Business & Commerce Presets

| Preset | Agents | Skills | Sub-Agents | Description |
|--------|--------|--------|------------|-------------|
| **E-Commerce Store** | PM, Dev, QA, GD | Payment + inventory skills | Domain-specific sub-agents | Online stores with checkout flow |
| **SaaS Product** | PM, Dev, QA, GD | Auth + billing + subscription | Full-stack sub-agents | Subscription-based products |
| **Enterprise Suite** | PM, Dev, QA | Security + compliance skills | Enterprise-focused | Large-scale business applications |

### 🔧 Technical Presets

| Preset | Agents | Skills | Sub-Agents | Description |
|--------|--------|--------|------------|-------------|
| **API Server** | PM, Dev, QA | Server + database skills | Backend sub-agents | Node.js/Python/Go API services |
| **Data/ML Pipeline** | PM, Dev, QA | Python + TensorFlow skills | Data pipeline sub-agents | ML models and data processing |
| **DevOps/Infrastructure** | PM, Dev, QA | CI/CD + Terraform skills | Infrastructure sub-agents | Deployment and automation |
| **Custom** | - | - | - | Build your own from scratch |

**After Preset Selection:**
1. Confirm project name
2. Review preset summary
3. Generate! (or customize further)

---

## Phase 3: Project Deep Dive (Standard/Expert)

### 3.1 Project Identity

**Question:** What is your project's name and purpose?

```
Project Name: _______________

One-Line Summary: _________________________________

[Example: "A multiplayer space exploration game with base building"]
```

**Question:** Which category best describes your project?

| Category | Description | Recommended Tech Stack |
|----------|-------------|------------------------|
| 🎮 **Game Development** | Interactive games, simulations | R3F, Rapier, Colyseus |
| 🌐 **Web Application** | SPA, dashboards, tools | React, Vue, Svelte |
| 📱 **Mobile App** | iOS/Android applications | React Native, Flutter |
| 🔌 **API/Backend** | Servers, microservices | Node.js, Python, Go |
| 📊 **Data/ML** | Analytics, AI models | Python, TensorFlow |
| 🛒 **E-Commerce** | Online stores, marketplaces | Full-stack + payments |
| 📦 **SaaS** | Subscription products | Full-stack + billing |
| 🧪 **DevOps/Infrastructure** | CI/CD, deployment | Terraform, Docker |

**Question:** What is the primary technology stack?

| Stack | Includes | Use When |
|-------|----------|----------|
| **React Three Fiber** | R3F, Drei, Rapier, Zustand | 3D games, visual experiences |
| **React Modern** | React 18+, Vite, TypeScript | Modern web apps |
| **Vue 3** | Vue 3, Vite, Pinia | Vue ecosystem |
| **SvelteKit** | Svelte, SvelteKit | Lightweight apps |
| **Next.js** | Next.js, App Router | Full-stack React |
| **React Native** | RN, Expo | Mobile apps |
| **Node.js + TypeScript** | Express, Fastify | API servers |
| **Python + FastAPI** | FastAPI, SQLAlchemy | Python backends |
| **Go + gRPC** | Go, gRPC, PostgreSQL | High-performance APIs |
| **Custom** | Specify below | Other stacks |

### 3.2 Project Scope & Scale

**Question:** What is your team size?

| Team Size | Recommended Orchestration | Agent Configuration |
|-----------|--------------------------|-------------------|
| 👤 **Solo** | Sequential Mode | All agents, you wear all hats |
| 👥 **Small Team (2-5)** | Event-Driven Mode | Split agents among team |
| 🏢 **Medium Team (6-20)** | Event-Driven Mode | Dedicated roles |
| 🏛️ **Enterprise (20+)** | Event-Driven + Custom | Multiple instances |

**Question:** What is the project scale?

| Scale | Description | PM Planning Approach |
|-------|-------------|---------------------|
| 🐣 **Prototype/MVP** | Proof of concept, < 20 tasks | Scale-adaptive (0-4 tasks) |
| 🚀 **Startup Product** | Launch-ready, 20-100 tasks | Balanced planning |
| 🏭 **Production System** | Enterprise, 100+ tasks | Full PRD management |

**Question:** What are your critical success factors? (Multi-select)

- [ ] Speed to market (fast iteration)
- [ ] Code quality (strict standards)
- [ ] Visual excellence (polish, effects)
- [ ] Multiplayer reliability (server-authoritative)
- [ ] Mobile performance (optimization)
- [ ] Accessibility (WCAG compliance)
- [ ] SEO optimization
- [ ] Real-time features
- [ ] Data processing (ML, analytics)

---

## Phase 4: Agent Configuration (Standard/Expert)

### 4.1 Core Agent Selection

**Question:** Which agents do you need? (Multi-select)

| Agent | Purpose | Required For | Recommended Skills Count |
|-------|---------|--------------|-------------------------|
| ✅ **PM (Coordinator)** | Task assignment, coordination | ALL projects | 12 PM skills |
| ✅ **Developer** | Feature implementation | Any coding | 20-40 dev skills |
| **Tech Artist** | Visuals, shaders, effects | 3D, games, visual apps | 10-20 TA skills |
| ✅ **QA** | Testing, validation | ALL projects | 8-10 QA skills |
| **Game Designer** | GDD, design, playtesting | Games, simulations | 8-10 GD skills |

**Smart Recommendations:**
```
Based on your project type (Game Development), I recommend:
  ✅ PM, Developer, QA (required)
  ✅ Tech Artist (3D graphics, shaders, effects)
  ✅ Game Designer (GDD, mechanics, balance)
```

### 4.2 Per-Agent Skill Configuration (Expert Only)

For each selected agent, ask about skill categories. See **Skill Catalog** below for complete list.

#### Developer Agent Skills

| Category | Skills to Enable | Description |
|----------|-----------------|-------------|
| **R3F Fundamentals** | `dev-r3f-r3f-fundamentals` | Core R3F patterns |
| **Physics** | `dev-r3f-r3f-physics` | Rapier physics integration |
| **Materials** | `dev-r3f-r3f-materials` | Custom material creation |
| **Multiplayer: Server** | `dev-multiplayer-server-authoritative`, `dev-multiplayer-colyseus-server` | Server-side game logic |
| **Multiplayer: Client** | `dev-multiplayer-prediction-basics`, `dev-multiplayer-colyseus-client` | Client prediction |
| **Multiplayer: State** | `dev-multiplayer-colyseus-state` | State schema definition |
| **Multiplayer: Prediction** | `dev-multiplayer-prediction-movement`, `dev-multiplayer-prediction-shooting` | Input prediction |
| **Multiplayer: Anti-Cheat** | `dev-multiplayer-anti-cheat-validation` | Server validation |
| **TypeScript Basics** | `dev-typescript-typescript-basics` | Core TypeScript patterns |
| **TypeScript Advanced** | `dev-typescript-typescript-advanced` | Generics, utilities |
| **Patterns** | `dev-patterns-*` | Object pooling, UI animations, coverage, haptics |
| **Performance** | `dev-performance-*` | Basics, instancing, LOD, mobile |
| **Assets** | `dev-assets-*` | Vite, audio, models, textures |
| **Research** | `dev-research-*` | Codebase, GDD, patterns |
| **Validation** | `dev-validation-*` | Feedback loops, quality gates, browser |

#### Tech Artist Skills

| Category | Skills to Enable | Description |
|----------|-----------------|-------------|
| **R3F Fundamentals** | `ta-r3f-fundamentals` | Core R3F for visuals |
| **Materials** | `ta-r3f-r3f-materials` | PBR materials |
| **Performance** | `ta-r3f-r3f-performance` | Visual optimization |
| **Physics Assets** | `ta-r3f-r3f-physics` | Physics visualization |
| **Shader Development** | `ta-shader-development` | GLSL/TSL shaders |
| **SDF Geometry** | `ta-shader-sdf` | Signed distance functions |
| **VFX Particles** | `ta-vfx-particles` | GPU particle systems |
| **VFX PostFX** | `ta-vfx-postfx` | Post-processing effects |
| **Camera TPS** | `ta-camera-tps` | Third-person camera |
| **UI Polish** | `ta-ui-polish` | UI/UX polish |
| **UI Debug Helpers** | `ta-ui-debug-helpers` | Leva debug panels |
| **Assets** | `ta-assets-*` | Workflow, pipeline optimization |
| **Validation** | `ta-validation-typescript` | Code quality for TA |
| **Networking** | `ta-networking-visual-feedback` | Multiplayer VFX |
| **Input** | `ta-input-validation` | Control testing |

#### QA Skills

| Category | Skills to Enable | Description |
|----------|-----------------|-------------|
| **Browser Testing** | `qa-browser-testing` | Playwright MCP |
| **Code Review** | `qa-code-review` | Pre-validation checks |
| **Gameplay Testing** | `qa-gameplay-testing` | E2E gameplay |
| **Multiplayer Testing** | `qa-multiplayer-testing` | Server validation |
| **Bug Reporting** | `qa-reporting-bug-reporting` | Structured reports |
| **Asset Validation** | `qa-validation-asset` | Asset quality checks |
| **Validation Workflow** | `qa-validation-workflow` | Complete QA flow |
| **Visual Testing** | `qa-visual-testing` | Regression testing |
| **QA Workflow** | `qa-workflow` | Complete QA process |

#### PM Skills

| Category | Skills to Enable | Description |
|----------|-----------------|-------------|
| **Workflow** | `pm-workflow` | Core PM flow |
| **Task Selection** | `pm-organization-task-selection` | Priority algorithm |
| **Task Research** | `pm-organization-task-research` | Pre-assignment research |
| **Scale Adaptive** | `pm-organization-scale-adaptive` | 0-4 task planning |
| **PRD Reorganization** | `pm-organization-prd-reorganization` | Backlog management |
| **Self Improvement** | `pm-improvement-self-improvement` | Retrospective-driven |
| **Skill Research** | `pm-improvement-skill-research` | Skill updates |
| **Test Planning** | `pm-planning-test-planning` | QA coordination |
| **Retrospective** | `pm-retrospective-facilitation` | Session facilitation |
| **Playtest Session** | `pm-retrospective-playtest-session` | GD coordination |
| **Architecture Validation** | `pm-validation-architecture` | Client/server validation |
| **Vite Assets** | `pm-configuration-vite-assets` | Asset coordination |
| **Asset Coordination** | `pm-configuration-asset-coordination` | TA collaboration |

#### Game Designer Skills

| Category | Skills to Enable | Description |
|----------|-----------------|-------------|
| **GDD Creation** | `gd-gdd-creation` | GDD structure |
| **Character Design** | `gd-design-character` | Character classes |
| **Game Loop** | `gd-design-game-loop` | Core loop design |
| **Level Design** | `gd-design-level` | Map layout |
| **Mechanic Design** | `gd-design-mechanic` | Gameplay systems |
| **Weapon Design** | `gd-design-weapon` | Item/weapon design |
| **Asset Impact** | `gd-assets-impact-analysis` | Asset requirements |
| **Thermite** | `gd-thermite-integration` | Design sessions |
| **Playtest** | `gd-validation-playtest` | Playtesting |

### 4.3 Per-Agent Sub-Agent Configuration (Expert Only)

#### Developer Sub-Agents

| Sub-Agent | Model | Purpose | Enable When |
|-----------|-------|---------|------------|
| `code-research` | Haiku | Pre-implementation pattern research | **Always (Required)** |
| `implementation` | Sonnet | Core feature implementation | **Always (Required)** |
| `validation` | Haiku | Feedback loops before commit | **Always (Required)** |
| `commit` | Haiku | Git operations, PRD updates | **Always (Required)** |

#### Tech Artist Sub-Agents

| Sub-Agent | Model | Purpose | Enable When |
|-----------|-------|---------|------------|
| `asset-researcher` | Haiku | Find existing assets before creating | **Always (Required)** |
| `asset-creator` | Sonnet | Create 3D/2D visual assets | Creating assets |
| `shader-compiler` | Sonnet | Create and compile shaders | Shader work |
| `particle-system-designer` | Sonnet | Create GPU particle systems | VFX work |
| `visual-validator` | Haiku | Pre-commit visual quality check | **Always (Required)** |
| `visual-tester` | Sonnet | Visual regression testing | After visual changes |
| `performance-profiler` | Haiku | Analyze performance bottlenecks | Performance issues |
| `code-quality` | Haiku | TypeScript quality checks | **Always (Required)** |

#### QA Sub-Agents

| Sub-Agent | Model | Purpose | Enable When |
|-----------|-------|---------|------------|
| `browser-validator` | Sonnet | Playwright browser testing | **Always (Required)** |
| `multiplayer-validator` | Sonnet | Multiplayer E2E testing | Multiplayer features |
| `visual-regression-tester` | Sonnet | UI comparison with Vision MCP | Visual/UI changes |
| `gameplay-tester` | Sonnet | E2E gameplay testing | Gameplay features |
| `code-review` | Haiku | Code quality pre-validation | **Always (Required)** |

#### PM Sub-Agents

| Sub-Agent | Model | Purpose | Enable When |
|-----------|-------|---------|------------|
| `task-researcher` | Sonnet | Research tasks before assignment | **Always (Recommended)** |
| `retrospective-facilitator` | Sonnet | Run retrospective sessions | After task completion |
| `skill-researcher` | Sonnet | Research skill improvements | During retrospectives |
| `prd-organizer` | Sonnet | Reorganize PRD after retrospectives | After retrospectives |
| `test-planner` | Sonnet | Create test plans for features | Before QA validation |
| `architecture-validator` | Sonnet | Validate architecture decisions | Before implementation |

#### Game Designer Sub-Agents

| Sub-Agent | Model | Purpose | Enable When |
|-----------|-------|---------|------------|
| `asset-analyst` | Haiku | Review existing assets before requests | **Always (Required)** |
| `visual-reference-researcher` | Sonnet | Find visual inspiration online | Visual asset creation |
| `reference-game-researcher` | Sonnet | Research reference games | Mechanic/level design |
| `thermite-facilitator` | Opus | Run thermite-design sessions | Design discussions |
| `gdd-documenter` | Sonnet | Create and maintain GDDs | Documentation needs |
| `playtest-evidence-collector` | Sonnet | Collect playtest evidence | Playtesting sessions |

---

## Phase 5: Orchestration Configuration (Standard/Expert)

**Question:** Which orchestration mode matches your needs?

| Mode | Token Usage | Parallelization | Best For |
|------|-------------|-----------------|----------|
| ⚡ **Event-Driven** | Medium | Full parallel | Production, complex tasks |
| 💰 **Sequential** | Low (~70% savings) | One at a time | Learning, debugging, budget |
| 🔄 **Polling** | High | Full parallel | Legacy compatibility |
| 👤 **HITL** | Varies | Single iteration | Learning the flow |

**Question:** Max iterations before automatic stop?

```
[ 200 ] ← Default safe limit

Tip: Set higher for large projects, lower for testing
```

**Question:** Context reset behavior?

| Option | Description |
|--------|-------------|
| **Auto-reset at 70%** | Recommended, maintains freshness |
| **Auto-reset at 80%** | Aggressive, more context |
| **Manual only** | You control resets |

---

## Phase 6: MCP Server Configuration (Expert Only)

**Question:** Which MCP servers does each agent need?

### PM Agent MCP Servers

| MCP Server | Purpose | Enable When |
|------------|---------|------------|
| `github` | Repository operations | **Always (Required)** |
| `filesystem` | Project file access | **Always (Required)** |
| `web-search` | Research templates/patterns | **Always (Recommended)** |
| `brave-search` | Alternative search | Backup search |

### Developer Agent MCP Servers

| MCP Server | Purpose | Enable When |
|------------|---------|------------|
| `github` | Git operations | **Always (Required)** |
| `filesystem` | Source file access | **Always (Required)** |
| `web-search` | Research stack patterns | **Always (Recommended)** |
| `brave-search` | Alternative search | Backup search |

### Tech Artist MCP Servers

| MCP Server | Purpose | Enable When |
|------------|---------|------------|
| `playwright` | Browser visual testing | Visual testing |
| `vision` | Image analysis | Asset validation |
| `blender` | 3D software integration | Using Blender |
| `shadertoy` | Shader development research | Shader work |
| `image-process` | Image manipulation | Asset optimization |
| `filesystem` | Asset file access | **Always (Required)** |
| `github` | Asset repository | **Always (Required)** |

### QA Agent MCP Servers

| MCP Server | Purpose | Enable When |
|------------|---------|------------|
| `playwright` | Browser testing | **Always (Required)** |
| `vision` | Screenshot comparison | Visual regression |
| `filesystem` | Test file access | **Always (Required)** |
| `github` | Bug reporting | **Always (Required)** |

### Game Designer MCP Servers

| MCP Server | Purpose | Enable When |
|------------|---------|------------|
| `playwright` | Playtesting in browser | **Always (Recommended)** |
| `vision` | Visual reference analysis | Reference gathering |
| `filesystem` | GDD file access | **Always (Required)** |
| `github` | Design repository | **Always (Required)** |
| `web-search` | Reference game research | **Always (Recommended)** |

---

## Phase 7: Quality Standards (Standard/Expert)

**Question:** What are your quality standards?

| Standard | Options | Recommended |
|----------|---------|-------------|
| **TypeScript Strictness** | Strict / Standard / Loose | Strict |
| **Test Coverage Target** | 95% / 80% / 60% / None | 80% |
| **Lint Rules** | ESLint Recommended / Custom / None | ESLint Recommended |
| **Commit Convention** | [ralph] format / Conventional / Custom | [ralph] format |
| **CI/CD Integration** | GitHub Actions / GitLab CI / None | GitHub Actions |

**Question:** Additional quality gates? (Multi-select)

- [ ] No `any` types (strict enforcement)
- [ ] No `@ts-ignore` (zero tolerance)
- [ ] All feedback loops must pass
- [ ] Visual regression testing
- [ ] Server-authoritative validation
- [ ] Mobile performance checks
- [ ] Accessibility auditing
- [ ] Security scanning

---

## Phase 8: Initial Features (All Modes)

**Question:** Describe your initial features in natural language

```
Example input:
"I need a player character that can move around with WASD, jump with spacebar,
and has a health system. There should be enemies that chase the player and
deal damage on contact. When health reaches zero, respawn at the start."
```

**AI Processing:**
- Parse into structured PRD items
- Categorize by type (architectural, feature, bug, chore)
- Assign priority (high/medium/low)
- Suggest acceptance criteria
- Map to appropriate agent

---

## Phase 8b: Deep Research (All Modes)

After collecting initial features, launch the `pm-research-specialist` sub-agent for deep domain research.

### Research Specialist Invocation

Launch the pm-research-specialist sub-agent:

```
Task("pm-research-specialist", {
  prompt: """
  Research this project idea deeply:

  Project: {project.name}
  Description: {project.description}
  Category: {project.category}
  Tech Stack: {project.techStack}
  Initial Features: {features}

  Research:
  1. Similar projects and their architectures (use WebSearch, GitHub repo search)
  2. Best practices for this tech stack
  3. Common pitfalls and challenges
  4. Questions we should ask the user (5-10 targeted questions)

  Return structured output with:
  1. Research summary (3-5 key insights)
  2. List of clarifying questions with context and impact
  3. Recommended feature refinements
  4. References to useful resources
  """
})
```

### User Questions Phase

Present research findings and ask clarifying questions:

```
═══════════════════════════════════════════════════════════════
                    RESEARCH FINDINGS
═══════════════════════════════════════════════════════════════

{research_findings_summary}

Similar Projects Found:
- [{Project 1}]({url}) - {relevance}
- [{Project 2}]({url}) - {relevance}

Best Practices:
- {practice 1} - {reason}
- {practice 2} - {reason}

═══════════════════════════════════════════════════════════════
                    CLARIFYING QUESTIONS
═══════════════════════════════════════════════════════════════

{generated_questions}

Please answer each question to help tailor your project setup.
[You can also request more research or modify questions]
```

Store answers in state file under `researchData.questionsAnswered`.

### Research Data Storage

Update state file with research results:

```json
{
  "researchData": {
    "similarProjects": [...],
    "bestPractices": [...],
    "commonPitfalls": [...],
    "techStackInsights": {...},
    "questionsAsked": [...],
    "questionsAnswered": [...],
    "recommendedRefinements": [...],
    "references": [...]
  }
}
```

### User Review Gate 1: After Research

User reviews:
- Research findings
- Generated questions
- Can request more research or modify questions

Options: [Continue to Next Phase] [Request More Research] [Modify Questions]

---

## Phase 8c: GDD Creation (Game Projects Only)

**Condition:** Only runs if `project.category === "game-development"`

### Thermite Session

Launch thermite facilitator for game design:

```
Task("gamedesigner-thermite-facilitator", {
  prompt: """
  Run a Thermite Design Session for this game:

  Project: {project.name}
  Description: {project.description}
  Features: {features}
  Research Findings: {researchData}
  User Answers: {researchData.questionsAnswered}

  Session Type: Boardroom Retreat (4 personas)

  Run the session to:
  1. Establish core design pillars
  2. Define key mechanics
  3. Identify design tensions
  4. Create initial design decisions (DEC-NNN format)
  5. Document open questions (OQ-NNN format)

  Output structured GDD data including:
  - Design decisions with rationale
  - Open questions with priority
  - Design pillars
  - Core mechanics
  """
})
```

### GDD Output

Save to `docs/design/`:
- `decision_log.md` - All design decisions
- `open_questions.md` - Unresolved design questions
- `gdd.md` - Game Design Document summary

### GDD Data Storage

Update state file with GDD results:

```json
{
  "gddData": {
    "designDecisions": [
      {
        "id": "DEC-001",
        "title": "Player Movement Model",
        "decision": "Use player-relative WASD controls...",
        "rationale": "Accessibility design pillar requires..."
      }
    ],
    "openQuestions": [...],
    "designPillars": [...],
    "coreMechanics": [...],
    "thermiteSessionType": "boardroom-retreat",
    "participants": [...]
  }
}
```

### User Review Gate 2: After GDD (Games Only)

User reviews:
- Design decisions
- Open questions
- Design pillar compliance
- Can request additional thermite sessions

Options: [Continue to PRD Creation] [Request Additional Thermite Session] [Modify GDD]

---

## Phase 8d: PRD Creation (All Modes)

### PM Agent Handoff

**CRITICAL:** The final PRD.json must be created by a PM agent, not the generator script.

```
Task("pm-prd-creator", {
  prompt: """
  Create the final prd.json using your PM expertise:

  Project Specification:
  - Name: {project.name}
  - Description: {project.description}
  - Category: {project.category}
  - Tech Stack: {project.techStack}
  - Agents: {configured_agents}

  Research Data:
  {researchData}

  GDD Data (if game project):
  {gddData}

  User Answers:
  {researchData.questionsAnswered}

  Initial Features:
  {features}

  Create prd.json with:
  1. Properly structured PRD items based on research
  2. Acceptance criteria derived from user input + research
  3. Correct agent assignments (considering skills)
  4. Dependency mapping between items
  5. Priority assignment based on user goals
  6. Feedback loops configured for tech stack
  7. Quality standards from Phase 7

  For game projects, include GDD references in PRD item descriptions.

  Write the file to: prd.json
  """
})
```

### PRD Review

Display generated PRD for user review:

```
═══════════════════════════════════════════════════════════════
                    PRD REVIEW
═══════════════════════════════════════════════════════════════

Project: {project.name}

Summary:
{brief_project_overview}

Items ({count}):
───────────────────────────────────────────────────────────────
| ID    | Title                    | Category | Priority | Agent |
───────────────────────────────────────────────────────────────
{prd_items_table}
───────────────────────────────────────────────────────────────

Agent Assignment:
- Developer: {n} tasks
- Tech Artist: {n} tasks
- QA: {n} tasks
- Game Designer: {n} tasks

Feedback Loops:
{feedback_loops}

Quality Standards:
- TypeScript: {mode}
- Test Coverage: {target}%
- Linting: {tools}

═══════════════════════════════════════════════════════════════

Approve this PRD? [Yes/No/Modify]
```

### User Review Gate 3: After PRD

User reviews:
- Complete prd.json content
- All PRD items
- Agent assignments
- Can request modifications before final approval

Options: [Approve and Continue] [Modify PRD] [Request New Research]

### PRD Specification Storage

Update state file with PRD specification:

```json
{
  "prdSpecification": {
    "refinedFeatures": [...],
    "dependencies": [...],
    "priorities": {...},
    "technicalRecommendations": [...]
  }
}
```

---

## Phase 9: Review and Generate (All Modes)

### Summary Display

```
═══════════════════════════════════════════════════════════════
                    RALPH ORCHESTRA SETUP
═══════════════════════════════════════════════════════════════

📁 PROJECT: My Awesome Game
📋 TYPE: Game Development (React Three Fiber)
👥 TEAM: Solo Developer
🎯 MODE: Sequential (Token-Efficient)

───────────────────────────────────────────────────────────────
AGENTS (5)
───────────────────────────────────────────────────────────────
  ✅ PM          • 12 skills • 6 sub-agents
  ✅ Developer   • 28 skills • 4 sub-agents
  ✅ Tech Artist • 12 skills • 8 sub-agents
  ✅ QA          • 9 skills  • 5 sub-agents
  ✅ Game Designer • 9 skills • 6 sub-agents

───────────────────────────────────────────────────────────────
FEATURES (8)
───────────────────────────────────────────────────────────────
  feat-001  [high]   Player movement system     → Developer
  feat-002  [high]   Player health system       → Developer
  feat-003  [medium] Enemy AI                    → Developer
  feat-004  [medium] Combat system               → Developer
  feat-005  [low]    Respawn mechanic            → Developer
  feat-006  [high]   Visual effects              → Tech Artist
  feat-007  [medium] UI HUD                      → Tech Artist
  feat-008  [low]    GDD documentation           → Game Designer

───────────────────────────────────────────────────────────────
GENERATION
───────────────────────────────────────────────────────────────
  📄 agents/pm/AGENT.md
  📄 agents/developer/AGENT.md
  📄 agents/techartist/AGENT.md
  📄 agents/qa/AGENT.md
  📄 agents/gamedesigner/AGENT.md
  📁 .claude/agents/*.agent.md (31 sub-agents)
  📁 .claude/skills/*/SKILL.md (70 skills)
  ⚙️  .claude/settings.*.json (5 configs)
  📋 prd.json (8 features)

═══════════════════════════════════════════════════════════════

[Generate Setup]  [Back]  [Save Configuration]
```

---

## Phase 10: Project Initialization (All Modes)

**Question:** How would you like to handle project dependencies?

| Option | Description |
|--------|-------------|
| **Auto-Initialize** | Ralph runs setup automatically on first coordinator start |
| **Manual Setup** | You'll handle dependencies yourself before starting Ralph |
| **Ask Me Later** | Prompt after generating files |

**If Auto-Initialize or Ask Me Later is selected:**

**Question:** What is your primary runtime environment?

| Runtime | Package Manager | Init Command | Install Command | Dev Command |
|---------|----------------|--------------|-----------------|-------------|
| **Node.js** | npm / yarn / pnpm | `npm init -y` | `npm install` | `npm run dev` |
| **Python** | pip / poetry | `python -m venv venv` | `pip install -r requirements.txt` | `python main.py` |
| **Rust** | cargo | `cargo init` | `cargo build` | `cargo run` |
| **Go** | go mod | `go mod init` | `go mod tidy` | `go run main.go` |
| **Java** | mvn | `mvn archetype:generate` | `mvn install` | `mvn spring-boot:run` |
| **.NET** | dotnet | `dotnet new console` | `dotnet restore` | `dotnet run` |

**Question:** What are your feedback loop commands? (Auto-populated based on runtime)

| Loop Type | Command | Required? |
|-----------|---------|-----------|
| **Type Check** | `npm run type-check` / `mypy --strict .` / `cargo clippy` | ✅ |
| **Lint** | `npm run lint` / `ruff check .` / `golangci-lint run` | ✅ |
| **Test** | `npm run test` / `pytest` / `cargo test` | ✅ |
| **Build** | `npm run build` / `python -m build` / `cargo build` | ✅ |

**Customization:**
- Users can customize any command based on their project setup
- Commands will be written to `prd.json.feedbackLoops` for agent use
- Initialization script will be generated as `.claude/scripts/init-project.sh` and `.ps1`

**Initialization Flow:**
1. Wizard collects runtime, package manager, and commands
2. Generator creates `init-project.sh` and `init-project.ps1` scripts
3. Scripts check for package manager availability
4. Scripts run init, install, and verify commands
5. Coordinator checks `prd.json.projectInitialization.status` on startup
6. If "pending", coordinator runs init script before task coordination
7. Status updated to "completed" on success, "failed" on error (with retry)

**If Manual Setup selected:**
- `projectInitialization.status` set to "skipped"
- Coordinator skips auto-init and proceeds directly to task coordination
- User is responsible for running setup before starting Ralph

---

## Phase 11: Workflow Documentation Generation (All Modes)

After all files are generated, create comprehensive workflow documentation for all agents.

### Summary

Generate workflow documentation that describes:
- How each agent operates (startup, decision framework, exit conditions)
- The complete task lifecycle across all agents
- Communication protocols and handoff mechanisms
- File permissions and commit standards

### Process

**1. Create workflows directory** (if not exists):
```bash
mkdir -p docs/workflows
```

**2. Launch parallel sub-agents** using the Task tool in a single message:

```
Task("workflow-generator", {
  agent_name: "pm",
  output_file: "pm-coordinator.md",
  source_file: "agents/pm/AGENT.md"
})

Task("workflow-generator", {
  agent_name: "developer",
  output_file: "developer.md",
  source_file: "agents/developer/AGENT.md"
})

Task("workflow-generator", {
  agent_name: "techartist",
  output_file: "techartist.md",
  source_file: "agents/techartist/AGENT.md"
})

Task("workflow-generator", {
  agent_name: "qa",
  output_file: "qa.md",
  source_file: "agents/qa/AGENT.md"
})

Task("workflow-generator", {
  agent_name: "gamedesigner",
  output_file: "gamedesigner.md",
  source_file: "agents/gamedesigner/AGENT.md"
})

Task("devcycle-generator", {
  output_file: "development-cycle.md"
})
```

**3. Wait for all to complete** - Each sub-agent reports when done

**4. Verify outputs** - Check all expected files exist:
```bash
ls docs/workflows/
# Expected: pm-coordinator.md, developer.md, techartist.md, qa.md, gamedesigner.md, development-cycle.md
```

**5. Create index file** - Generate `docs/workflows/index.md` with links to all workflows

### Success Criteria

- All enabled agent workflow files created
- `development-cycle.md` created
- All files follow template structure (`docs/workflows/_template.md`)
- YAML frontmatter present and valid
- ASCII diagrams render correctly
- Index file created with proper cross-references

### Output Files Generated

| File | Description |
|------|-------------|
| `docs/workflows/pm-coordinator.md` | PM workflow documentation |
| `docs/workflows/developer.md` | Developer workflow documentation |
| `docs/workflows/techartist.md` | Tech Artist workflow documentation |
| `docs/workflows/qa.md` | QA workflow documentation |
| `docs/workflows/gamedesigner.md` | Game Designer workflow documentation |
| `docs/workflows/development-cycle.md` | Complete task lifecycle documentation |
| `docs/workflows/index.md` | Index with links to all workflows |

### Skip Condition

If the user is in a hurry or wants to generate workflows later, they can choose to skip this phase. Workflows can be generated later by invoking the `shared-workflow-generation` skill directly.

---

## Implementation Steps

### 1. Initialize State Management

On first invocation, create the state file:

```powershell
# Read or create state file
$statePath = ".claude/session/prd-starter-state.json"
if (-not (Test-Path $statePath)) {
    $state = @{
        version = "4.0.0"
        startedAt = (Get-Date).ToUniversalTime().ToString("o")
        completedAt = $null
        wizardMode = $null
        currentPhase = "entry_point_selection"
        currentSubPhase = $null
        phases = @{}
        researchData = @{}
        gddData = @{}
        prdSpecification = @{}
    } | ConvertTo-Json -Depth 20
    $state | Out-File -FilePath $statePath -Encoding utf8
}
```

### 2. Run Phase Questions

Use `AskUserQuestion` for all user inputs. Always include "Other" for free-form input.

### 3. Update State File

After each phase completion, update the state with collected data.

### 4. Load Preset (Quick Start Mode)

For Quick Start mode, load the preset from `.claude/presets/{preset-name}.json`:

```powershell
$presetPath = ".claude/presets/$selectedPreset.json"
$preset = Get-Content $presetPath | ConvertFrom-Json
# Merge preset into state configuration
```

### 5. Generate Files

After Phase 9 (Review and Confirm), invoke the generator:

**Windows:**
```powershell
.\.claude\scripts\prd-starter\prd-starter-generator.ps1 -Action generate -StateFile .claude\session\prd-starter-state.json
```

**Mac/Linux:**
```bash
python3 .claude/scripts/prd-starter/prd-starter-generator.py --action generate --state .claude/session/prd-starter-state.json
```

### 6. Verify Generation

After generation completes, verify:
1. Check all agent directories exist
2. Verify AGENT.md files have correct frontmatter
3. Confirm MCP settings are valid
4. Validate prd.json format
5. Check scripts were updated

---

## State Persistence

The state file persists across invocations:
- Location: `.claude/session/prd-starter-state.json`
- Resumable from any phase
- Tracks wizard mode (quick-start/standard/expert)
- Records preset selection (if Quick Start)
- Stores per-agent skill/sub-agent selections (if Expert)
- Records quality standards and orchestration settings

---

## Output Files

| File | Generated When |
|------|----------------|
| `agents/{name}/AGENT.md` | Each agent configured |
| `.claude/agents/{subagent-name}.agent.md` | Sub-agent configured |
| `.claude/skills/{skill-name}/SKILL.md` | Custom skill configured (folder-based) |
| `.claude/settings.{name}.json` | Each agent configured |
| `prd.json` | Phase 8d complete (created by PM agent) |
| Watchdog scripts updated | After generation |

**Architecture Notes:**
- **Agents**: Single `AGENT.md` file per agent (no subdirectories)
- **Sub-agents**: Flat `.claude/agents/*.agent.md` with YAML frontmatter
- **Skills**: Folder-based `.claude/skills/{name}/SKILL.md` with naming prefixes (dev-, ta-, qa-, pm-, gd-, shared-)

---

## Anti-Patterns

- **Don't skip questions**: All phases are required for complete setup
- **Don't skip research**: Research provides context for better decisions
- **Don't hardcode values**: Always gather from user or research
- **Don't bypass validation**: Use schemas before generating files
- **Don't forget "Other" option**: Allow free-form for every question

---

## Cross-Platform Support

The generator works on all platforms:
- **Windows**: Use `.prd-starter-generator.ps1`
- **Mac/Linux**: Use `.prd-starter-generator.sh` or call Python directly
- **Python 3.8+** required with jinja2, pyyaml, jsonschema

---

## See Also

- [shared-ralph-core.md](../shared-ralph-core/SKILL.md) - Core Ralph Orchestra concepts
- [shared-worker-protocol.md](../shared-worker-protocol/SKILL.md) - Agent lifecycle
- [shared-ralph-event-protocol.md](../shared-ralph-event-protocol/SKILL.md) - Event-driven messaging
- `.claude/schemas/prd-starter-state.schema.json` - Configuration validation
- `.claude/scripts/prd-starter/prd-starter-generator.py` - Generator implementation
- `.claude/presets/` - Preset configuration files
