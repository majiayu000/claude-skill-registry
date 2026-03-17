---
name: faion-net
description: "Universal orchestrator: 54 skills, 1297 methodologies. Development, DevOps, AI/ML, Product, Marketing, PM, BA, UX, Research."
user-invocable: true
---

# Faion Network Orchestrator

**Communication: User's language.**

## How It Works

```
User task → Analyze intent → Skill tool → Domain skill loads → Execute
```

**CRITICAL:** You MUST invoke domain skills using `Skill(skill-name)`. Markdown links do NOT load skills.

---

## Context Discovery

Before routing to a domain skill, gather context to make informed decisions.

### Auto-Investigation

If user has an existing project, check these signals FIRST:

| Signal | How to Check | Detected → Skip Question |
|--------|--------------|--------------------------|
| Python/Django | `Glob("**/manage.py")` | Stack question, route to faion-python-developer |
| Python/FastAPI | `Grep("fastapi", "**/pyproject.toml")` | Stack question, route to faion-python-developer |
| Node.js/React | `Glob("**/package.json")` + check for react | Stack question, route to faion-javascript-developer |
| Go project | `Glob("**/go.mod")` | Stack question, route to faion-backend-systems |
| Rust project | `Glob("**/Cargo.toml")` | Stack question, route to faion-backend-systems |
| Docker setup | `Glob("**/Dockerfile")` | Infra exists, context for faion-devops-engineer |
| CI/CD config | `Glob("**/.github/workflows/*.yml")` | CI exists, context for faion-cicd-engineer |
| SDD docs | `Glob("**/.aidocs/constitution.md")` | SDD project, can read spec/design |

### Discovery Questions

Use `AskUserQuestion` if intent is unclear after auto-investigation.

#### Q1: Primary Intent (required if unclear)

```yaml
question: "What do you need help with?"
header: "Intent"
multiSelect: false
options:
  - label: "Research & Discovery"
    description: "Ideas, market research, competitors, validation"
  - label: "Planning & Strategy"
    description: "Product roadmap, architecture, project planning"
  - label: "Build & Implement"
    description: "Write code, create designs, develop features"
  - label: "Launch & Market"
    description: "GTM, marketing, SEO, ads, content"
  - label: "Fix & Improve"
    description: "Bug fixes, refactoring, optimization, tests"
```

**Routing:**
- "Research & Discovery" → `Skill(faion-researcher)`
- "Planning & Strategy" → Ask Q1b (Planning type)
- "Build & Implement" → Ask Q1c (Build type) or auto-detect from project
- "Launch & Market" → `Skill(faion-marketing-manager)`
- "Fix & Improve" → Auto-detect stack, then route to dev skill

#### Q1b: Planning Type (if "Planning & Strategy")

```yaml
question: "What kind of planning?"
header: "Planning"
multiSelect: false
options:
  - label: "Product scope & roadmap"
    description: "MVP definition, features, priorities"
  - label: "Technical architecture"
    description: "System design, tech stack, APIs"
  - label: "Project schedule & resources"
    description: "Timeline, team, milestones"
  - label: "Business requirements"
    description: "Use cases, processes, stakeholders"
```

**Routing:**
- "Product scope & roadmap" → `Skill(faion-product-manager)`
- "Technical architecture" → `Skill(faion-software-architect)`
- "Project schedule & resources" → `Skill(faion-project-manager)`
- "Business requirements" → `Skill(faion-business-analyst)`

#### Q1c: Build Type (if "Build & Implement" and no auto-detect)

```yaml
question: "What are you building?"
header: "Build"
multiSelect: false
options:
  - label: "Backend / API"
    description: "Server-side code, database, APIs"
  - label: "Frontend / UI"
    description: "User interface, components, styling"
  - label: "Full-stack feature"
    description: "Both frontend and backend"
  - label: "Infrastructure / DevOps"
    description: "Deployment, CI/CD, containers"
  - label: "AI / ML feature"
    description: "LLM integration, RAG, agents"
```

**Routing:**
- "Backend / API" → Detect stack or ask, then route
- "Frontend / UI" → `Skill(faion-frontend-developer)` or `Skill(faion-javascript-developer)`
- "Full-stack feature" → Detect stack, coordinate skills
- "Infrastructure / DevOps" → `Skill(faion-devops-engineer)`
- "AI / ML feature" → `Skill(faion-ml-engineer)`

#### Q2: Project Stage (context for methodology depth)

```yaml
question: "What stage is your project at?"
header: "Stage"
multiSelect: false
options:
  - label: "Idea phase"
    description: "Exploring, not committed yet"
  - label: "Planning phase"
    description: "Defining scope, architecture"
  - label: "Active development"
    description: "Building features"
  - label: "Pre-launch"
    description: "Preparing for release"
  - label: "Live product"
    description: "Has users, iterating"
```

**Context impact:**
- "Idea phase" → Research-heavy, validation methodologies
- "Planning phase" → Architecture, specs, design docs
- "Active development" → Implementation patterns, testing
- "Pre-launch" → QA, performance, launch prep
- "Live product" → Monitoring, optimization, growth

#### Q3: Primary Concerns (optional, multiSelect)

```yaml
question: "What are your main concerns for this task?"
header: "Concerns"
multiSelect: true
options:
  - label: "Speed of delivery"
    description: "Ship fast, iterate later"
  - label: "Code quality"
    description: "Clean, maintainable, tested"
  - label: "Performance"
    description: "Fast, scalable, efficient"
  - label: "Security"
    description: "Protect data, prevent attacks"
```

**Context impact:**
- "Speed of delivery" → Pragmatic patterns, skip optional steps
- "Code quality" → Full testing, code review, documentation
- "Performance" → Optimization methodologies, profiling
- "Security" → Security testing, auth patterns, OWASP

---

## Decision Tree

### What does the user want?

```
RESEARCH & STRATEGY
├── Market research, TAM/SAM, competitors → Skill(faion-researcher)
├── System design, architecture, ADRs → Skill(faion-software-architect)
└── Product planning, MVP, roadmaps → Skill(faion-product-manager)

DEVELOPMENT
├── Python (Django, FastAPI) → Skill(faion-python-developer)
├── JavaScript (React, Node, Next.js) → Skill(faion-javascript-developer)
├── Go, Rust, databases, caching → Skill(faion-backend-systems)
├── Java, C#, PHP, Ruby → Skill(faion-backend-enterprise)
├── Frontend (Tailwind, PWA, a11y) → Skill(faion-frontend-developer)
├── APIs (REST, GraphQL, OpenAPI) → Skill(faion-api-developer)
├── Testing (TDD, E2E, mocking) → Skill(faion-testing-developer)
├── Code quality, refactoring, DDD → Skill(faion-code-quality)
└── Automation, Puppeteer, monorepo → Skill(faion-automation-tooling)

INFRASTRUCTURE & DEVOPS
├── Docker, K8s, Terraform, AWS/GCP → Skill(faion-infrastructure-engineer)
└── CI/CD, GitHub Actions, GitOps → Skill(faion-cicd-engineer)

AI & MACHINE LEARNING
├── LLM APIs (OpenAI, Claude, Gemini) → Skill(faion-llm-integration)
├── RAG, embeddings, vector DBs → Skill(faion-rag-engineer)
├── Fine-tuning, evaluation, ML Ops → Skill(faion-ml-ops)
├── AI agents, LangChain, MCP → Skill(faion-ai-agents)
└── Vision, image/video gen, TTS/STT → Skill(faion-multimodal-ai)

MARKETING
├── GTM, launches, positioning, pricing → Skill(faion-gtm-strategist)
├── Content, SEO copywriting, email → Skill(faion-content-marketer)
├── Growth, AARRR, A/B testing → Skill(faion-growth-marketer)
├── Landing pages, CRO, funnels → Skill(faion-conversion-optimizer)
├── Google/Meta/LinkedIn Ads → Skill(faion-ppc-manager)
├── Technical SEO, link building → Skill(faion-seo-manager)
└── Social media, community → Skill(faion-smm-manager)

PROJECT & BUSINESS
├── Scrum, Kanban, Jira/Linear → Skill(faion-pm-agile)
├── PMBoK, WBS, EVM → Skill(faion-pm-traditional)
├── Requirements, elicitation, strategy → Skill(faion-ba-core)
└── Use cases, BPMN, data models → Skill(faion-ba-modeling)

DESIGN & UX
├── User research, usability testing → Skill(faion-ux-researcher)
├── Wireframes, design systems, Figma → Skill(faion-ui-designer)
└── WCAG, accessibility, a11y → Skill(faion-accessibility-specialist)

SDD WORKFLOW
├── Specs, design docs, impl-plans → Skill(faion-sdd-planning)
├── Quality gates, code review → Skill(faion-sdd-execution)
└── Sequential task execution → Skill(faion-feature-executor)

COMMUNICATION & HR
├── Stakeholder dialogue, Mom Test → Skill(faion-communicator)
└── Recruiting, interviews, onboarding → Skill(faion-hr-recruiter)

CLAUDE CODE
└── Skills, hooks, MCP servers, IDE → Skill(faion-claude-code)
```

---

## Quick Reference

| Domain | Primary Skill | Methodologies |
|--------|--------------|---------------|
| Research | `faion-researcher` | 40 |
| Architecture | `faion-software-architect` | 31 |
| Product | `faion-product-manager` | 69 |
| Development | `faion-software-developer` | 138 |
| DevOps | `faion-devops-engineer` | 87 |
| AI/ML | `faion-ml-engineer` | 140 |
| Marketing | `faion-marketing-manager` | 135 |
| Project Mgmt | `faion-project-manager` | 97 |
| Business Analysis | `faion-business-analyst` | 55 |
| UX/UI | `faion-ux-ui-designer` | 179 |
| SDD | `faion-sdd` | 71 |

---

## Routing Examples

**Research:**
```
"Analyze competitors" → Skill(faion-researcher)
"Design system architecture" → Skill(faion-software-architect)
```

**Development:**
```
"Build Django API" → Skill(faion-python-developer)
"Create React component" → Skill(faion-javascript-developer)
"Write unit tests" → Skill(faion-testing-developer)
```

**AI/ML:**
```
"Integrate OpenAI API" → Skill(faion-llm-integration)
"Build RAG pipeline" → Skill(faion-rag-engineer)
"Create AI agent" → Skill(faion-ai-agents)
```

**Marketing:**
```
"Plan product launch" → Skill(faion-gtm-strategist)
"Optimize landing page" → Skill(faion-conversion-optimizer)
"Run Google Ads" → Skill(faion-ppc-manager)
```

**Multi-domain (sequential):**
```
"Validate and build my SaaS idea"
→ 1. Skill(faion-researcher) - validate
→ 2. Skill(faion-product-manager) - plan MVP
→ 3. Skill(faion-software-architect) - design
→ 4. Skill(faion-software-developer) - build
```

---

## Statistics

| Metric | Count |
|--------|-------|
| Skills | 54 |
| Orchestrators | 3 |
| Leaf skills | 51 |
| Methodologies | 1297 |

## Methodology Structure

Each methodology is a folder with 5 files:
```
{methodology}/
├── README.md       # Main content
├── checklist.md    # Step-by-step checklist
├── templates.md    # Code/config templates
├── examples.md     # Practical examples
└── llm-prompts.md  # AI prompts
```

---

*Faion Network v3.0*
