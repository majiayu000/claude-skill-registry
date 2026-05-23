---
name: faion-net
description: "Universal orchestrator for software projects: SDD workflow, research, product planning, development, marketing, project/business analysis, UX. 60+ agents, 40+ skills, 250+ methodologies."
user-invocable: true
---

# Faion Network Orchestrator

**Communication: User's language.**

Universal skill for end-to-end software project lifecycle. From idea to production, from research to marketing.

---

## Step 1: Knowledge Freshness Check

**MANDATORY at session start.**

Calculate and acknowledge knowledge gap:

```
Current date: [TODAY]
Model training cutoff: [CUTOFF_DATE]
Knowledge gap: [DIFF] months

Areas likely outdated:
- Library versions (npm, pip, cargo)
- Framework APIs (React, Next.js, Django)
- Cloud services pricing and features
- AI model capabilities and pricing
- Security vulnerabilities and patches
```

**Action:** For time-sensitive info (versions, APIs, pricing), use WebSearch to get current data before implementing.

---

## Step 2: Execution Mode Selection

**Ask user at session start:**

```python
AskUserQuestion([
    {
        "question": "How should I execute tasks?",
        "header": "Execution",
        "options": [
            {"label": "Sub-agents (Recommended)", "description": "Use Task/Explore agents. Better for complex tasks, parallel execution, isolated context."},
            {"label": "Main flow", "description": "Execute directly in conversation. Better for simple tasks, visibility, interactive work."}
        ]
    }
])
```

**If sub-agents selected:**
- Use `Task` tool with appropriate `subagent_type` for all significant work
- Use `Explore` agent for codebase analysis and research
- Run multiple agents in parallel when independent
- Return concise summaries to user

**If main flow selected:**
- Execute all tools directly in conversation
- Provide step-by-step visibility
- Ask for confirmation on significant changes

---

## Capabilities

**Idea → Validation:**
- Generate startup/product ideas (7 frameworks)
- Research pain points via Reddit, forums, reviews
- Validate problems with evidence (frequency, severity, willingness to pay)
- Evaluate niche viability (market size, competition, barriers)
- Generate product names, check domain availability

**Research → Strategy:**
- Market research (TAM/SAM/SOM, trends, growth drivers)
- Competitor analysis (features, pricing, positioning)
- User personas from real feedback
- Pricing strategies and models
- Problem validation with evidence

**Product Planning:**
- MVP scope from competitor analysis
- MLP planning (gap analysis, WOW moments)
- Feature prioritization (RICE, MoSCoW)
- Roadmap design, release planning
- User story mapping, OKRs

**SDD Workflow:**
- Project bootstrap (constitution, roadmap)
- Specification writing with acceptance criteria
- Technical design documents
- Implementation plans with task parallelization
- Task execution with quality gates
- Reflexion learning (patterns, mistakes)

**Development:**
- Code generation (Python, JS/TS, Go, Ruby, PHP, Java, C#, Rust)
- Code review and refactoring
- Testing (unit, integration, E2E, TDD)
- API design (REST, GraphQL, OpenAPI)
- DevOps (CI/CD, Docker, K8s, Terraform, AWS)
- Browser automation (Puppeteer, Playwright)

**AI/LLM:**
- RAG pipelines (document Q&A, knowledge bases)
- Embeddings (generation, indexing, search)
- Fine-tuning (LoRA, QLoRA, PEFT)
- Prompt engineering and optimization
- Multimodal (image, video, audio generation)
- Voice agents (STT, TTS, real-time)
- Autonomous agents (LangGraph, ReAct)

**Marketing:**
- GTM strategy and execution
- Landing pages with high conversion
- Content marketing and SEO
- Paid ads (Meta, Google)
- Email campaigns and automation
- Social media strategy

**Project Management (PMBOK 7/8):**
- Stakeholder management
- Risk management
- Earned Value Management (EVM)
- Change control
- Agile, Waterfall, Hybrid delivery

**Business Analysis (BABOK v3):**
- Requirements elicitation
- Traceability matrices
- Solution assessment
- 6 Knowledge Areas, 30 tasks

**UX:**
- User research (interviews, surveys, contextual inquiry)
- Usability testing (moderated, unmoderated)
- Heuristic evaluation (Nielsen Norman 10)
- Personas, journey mapping
- Wireframing, prototyping

---

## Domain Skills (13)

| Skill | Purpose |
|-------|---------|
| `faion-sdd` | SDD orchestrator: specs, designs, implementation plans, constitutions, task lifecycle, quality gates, reflexion |
| `faion-feature-executor` | SDD feature executor: sequential tasks with quality gates, tests/coverage, code review |
| `faion-researcher` | Idea generation (SCAMPER), market research, competitors, personas, pricing, validation. 9 modes |
| `faion-product-manager` | MVP/MLP planning, RICE/MoSCoW prioritization, roadmaps, backlog, user stories, OKRs. 18 methodologies |
| `faion-software-developer` | Python, JS/TS, Django, FastAPI, React, APIs, testing, DevOps, UI design. 68 methodologies |
| `faion-devops-engineer` | Docker, K8s, Terraform, AWS/GCP/Azure, CI/CD, monitoring, IaC, nginx |
| `faion-ml-engineer` | LLM APIs, RAG, embeddings, fine-tuning, LangChain, vector DBs, prompt engineering |
| `faion-marketing-manager` | GTM, landing pages, SEO/SEM, content, ads, email, social media. 72 methodologies |
| `faion-project-manager` | PMBOK 7/8 (8 Domains, 12 Principles), PM tools, risk, EVM, agile. 32 methodologies |
| `faion-business-analyst` | IIBA BABOK v3: 6 Knowledge Areas, requirements, stakeholders, process modeling. 30 tasks |
| `faion-ux-ui-designer` | Nielsen Norman 10, UX research, usability testing, personas, journey mapping. 32 methodologies |
| `faion-claude-code` | Claude Code config: skills, agents, commands, hooks, MCP servers, IDE integrations |
| `faion-net` | This orchestrator (recursive for complex multi-domain tasks) |

---

## All Methodologies (250+)

### Research (M-RES-*)
| ID | Name |
|----|------|
| M-RES-001 | SCAMPER Ideation |
| M-RES-002 | Mind Mapping |
| M-RES-003 | Reverse Engineering Ideas |
| M-RES-004 | Problem-First Discovery |
| M-RES-005 | Trend Surfing |
| M-RES-006 | Skill-Stack Analysis |
| M-RES-007 | Market Gap Analysis |
| M-RES-008 | Pain Point Research |
| M-RES-009 | Competitor Feature Matrix |
| M-RES-010 | Pricing Strategy Analysis |
| M-RES-011 | Persona Building |
| M-RES-012 | Niche Evaluation |
| M-RES-013 | Problem Validation |
| M-RES-014 | Project Naming |

### Product (M-PRD-*)
| ID | Name |
|----|------|
| M-PRD-001 | MVP Scoping |
| M-PRD-002 | MLP Planning |
| M-PRD-003 | RICE Prioritization |
| M-PRD-004 | MoSCoW Prioritization |
| M-PRD-005 | Roadmap Design |
| M-PRD-006 | User Story Mapping |
| M-PRD-007 | OKR Setting |
| M-PRD-008 | Problem Validation |
| M-PRD-009 | Assumption Mapping |
| M-PRD-010 | Lean Canvas |
| M-PRD-011 | Jobs To Be Done |
| M-PRD-012 | Opportunity Scoring |
| M-PRD-013 | Value Proposition Canvas |
| M-PRD-014 | Sprint Planning |
| M-PRD-015 | Release Planning |
| M-PRD-016 | Backlog Refinement |
| M-PRD-017 | Five Whys Analysis |
| M-PRD-018 | Impact Mapping |

### Development (M-DEV-*)
| ID | Name |
|----|------|
| M-DEV-001 | Django Coding Standards |
| M-DEV-002 | Django Code Decision Tree |
| M-DEV-003 | Django Base Model Pattern |
| M-DEV-004 | Django Testing with pytest |
| M-DEV-005 | FastAPI Standards |
| M-DEV-006 | Python Async Patterns |
| M-DEV-007 | Python Type Hints |
| M-DEV-008 | Poetry Project Setup |
| M-DEV-009 | React Component Architecture |
| M-DEV-010 | TypeScript Strict Mode |
| M-DEV-011 | React Hooks Best Practices |
| M-DEV-012 | Next.js App Router |
| M-DEV-013 | Node.js Service Layer |
| M-DEV-014 | Express/Fastify Patterns |
| M-DEV-015 | Bun Runtime |
| M-DEV-016 | Package Management (pnpm) |
| M-DEV-017 | Monorepo Setup (Turborepo) |
| M-DEV-018 | Go Project Structure |
| M-DEV-019 | Go Error Handling |
| M-DEV-020 | Go Concurrency Patterns |
| M-DEV-021 | Rust Ownership Model |
| M-DEV-022 | Rust Error Handling |
| M-DEV-023 | Ruby on Rails Patterns |
| M-DEV-024 | PHP Laravel Patterns |
| M-DEV-025 | Java Spring Boot |
| M-DEV-026 | C# .NET Patterns |
| M-DEV-027 | Clean Architecture |
| M-DEV-028 | Domain-Driven Design |
| M-DEV-029 | CQRS Pattern |
| M-DEV-030 | Event Sourcing |
| M-DEV-031 | Microservices Design |
| M-DEV-032 | API Design (REST) |
| M-DEV-033 | API Design (GraphQL) |
| M-DEV-034 | OpenAPI Specification |
| M-DEV-035 | Database Design |
| M-DEV-036 | SQL Optimization |
| M-DEV-037 | NoSQL Patterns |
| M-DEV-038 | Caching Strategy |
| M-DEV-039 | Message Queues |
| M-DEV-040 | WebSocket Design |
| M-DEV-041 | Unit Testing |
| M-DEV-042 | Integration Testing |
| M-DEV-043 | E2E Testing |
| M-DEV-044 | TDD Workflow |
| M-DEV-045 | Test Fixtures |
| M-DEV-046 | Mocking Strategies |
| M-DEV-047 | Code Coverage |
| M-DEV-048 | Security Testing |
| M-DEV-049 | Performance Testing |
| M-DEV-050 | Documentation |
| M-DEV-051 | CLAUDE.md Creation |
| M-DEV-052 | Code Review |
| M-DEV-053 | Refactoring Patterns |
| M-DEV-054 | Technical Debt |
| M-DEV-055 | Error Handling |
| M-DEV-056 | Logging Patterns |
| M-DEV-057 | Feature Flags |
| M-DEV-058 | A/B Testing |
| M-DEV-059 | Internationalization |
| M-DEV-060 | Accessibility |
| M-DEV-061 | SEO for SPAs |
| M-DEV-062 | PWA Development |
| M-DEV-063 | Mobile Responsive |
| M-DEV-064 | UI Component Library |
| M-DEV-065 | Storybook Setup |
| M-DEV-066 | Design Tokens |
| M-DEV-067 | CSS-in-JS |
| M-DEV-068 | Tailwind Patterns |

### DevOps (M-OPS-*)
| ID | Name |
|----|------|
| M-OPS-001 | Docker Containerization |
| M-OPS-002 | Docker Compose |
| M-OPS-003 | Kubernetes Deployment |
| M-OPS-004 | Helm Charts |
| M-OPS-005 | Terraform IaC |
| M-OPS-006 | AWS Architecture |
| M-OPS-007 | GCP Architecture |
| M-OPS-008 | Azure Architecture |
| M-OPS-009 | GitHub Actions CI/CD |
| M-OPS-010 | GitLab CI/CD |
| M-OPS-011 | Jenkins Pipelines |
| M-OPS-012 | ArgoCD GitOps |
| M-OPS-013 | Prometheus Monitoring |
| M-OPS-014 | Grafana Dashboards |
| M-OPS-015 | ELK Stack Logging |
| M-OPS-016 | Nginx Configuration |
| M-OPS-017 | Load Balancing |
| M-OPS-018 | SSL/TLS Setup |
| M-OPS-019 | Secrets Management |
| M-OPS-020 | Backup Strategies |

### ML/AI (M-ML-*)
| ID | Name |
|----|------|
| M-ML-001 | OpenAI API Integration |
| M-ML-002 | Claude API Integration |
| M-ML-003 | Gemini API Integration |
| M-ML-004 | Local LLM (Ollama) |
| M-ML-005 | Embedding Generation |
| M-ML-006 | Vector Database Setup |
| M-ML-007 | RAG Pipeline Design |
| M-ML-008 | RAG Evaluation |
| M-ML-009 | Hybrid Search |
| M-ML-010 | Reranking |
| M-ML-011 | Chunking Strategies |
| M-ML-012 | Fine-tuning (OpenAI) |
| M-ML-013 | Fine-tuning (LoRA) |
| M-ML-014 | Prompt Engineering |
| M-ML-015 | Chain-of-Thought |
| M-ML-016 | Tool Use / Function Calling |
| M-ML-017 | Structured Output |
| M-ML-018 | Guardrails |
| M-ML-019 | Cost Optimization |
| M-ML-020 | Model Evaluation |
| M-ML-021 | LangChain Patterns |
| M-ML-022 | LlamaIndex Patterns |
| M-ML-023 | Autonomous Agents |
| M-ML-024 | Multi-Agent Systems |
| M-ML-025 | Image Generation (DALL-E, Midjourney) |
| M-ML-026 | Image Analysis (Vision) |
| M-ML-027 | Speech-to-Text |
| M-ML-028 | Text-to-Speech |
| M-ML-029 | Voice Agents |
| M-ML-030 | Video Generation |

### Marketing (M-MKT-*)
| ID | Name |
|----|------|
| M-MKT-001 | GTM Strategy |
| M-MKT-002 | ICP Definition |
| M-MKT-003 | Value Proposition |
| M-MKT-004 | Positioning Statement |
| M-MKT-005 | Messaging Framework |
| M-MKT-006 | Landing Page Design |
| M-MKT-007 | Hero Section |
| M-MKT-008 | Social Proof |
| M-MKT-009 | CTA Optimization |
| M-MKT-010 | A/B Testing |
| M-MKT-011 | Copywriting Formulas |
| M-MKT-012 | AIDA Framework |
| M-MKT-013 | PAS Framework |
| M-MKT-014 | Feature-Benefit Mapping |
| M-MKT-015 | SEO On-Page |
| M-MKT-016 | SEO Technical |
| M-MKT-017 | Keyword Research |
| M-MKT-018 | Content Strategy |
| M-MKT-019 | Blog Writing |
| M-MKT-020 | Guest Posting |
| M-MKT-021 | Link Building |
| M-MKT-022 | Google Ads |
| M-MKT-023 | Meta Ads |
| M-MKT-024 | LinkedIn Ads |
| M-MKT-025 | Retargeting |
| M-MKT-026 | Email Welcome Sequence |
| M-MKT-027 | Newsletter |
| M-MKT-028 | Drip Campaigns |
| M-MKT-029 | Email Deliverability |
| M-MKT-030 | Social Media Strategy |
| M-MKT-031 | Twitter/X Growth |
| M-MKT-032 | LinkedIn Growth |
| M-MKT-033 | Community Building |
| M-MKT-034 | Influencer Marketing |
| M-MKT-035 | Product Hunt Launch |
| M-MKT-036 | Press Release |
| M-MKT-037 | Analytics Setup |
| M-MKT-038 | Conversion Tracking |
| M-MKT-039 | Funnel Analysis |
| M-MKT-040 | Customer Journey |

### Project Management (M-PM-*)
| ID | Name |
|----|------|
| M-PM-001 | Stakeholder Register |
| M-PM-002 | Stakeholder Analysis Matrix |
| M-PM-003 | RACI Matrix |
| M-PM-004 | Team Charter |
| M-PM-005 | Development Approach Selection |
| M-PM-006 | Project Life Cycle Design |
| M-PM-007 | WBS Creation |
| M-PM-008 | Schedule Development |
| M-PM-009 | Cost Estimation |
| M-PM-010 | Communication Management Plan |
| M-PM-011 | Change Management Process |
| M-PM-012 | Quality Management Plan |
| M-PM-013 | Acceptance Criteria Definition |
| M-PM-014 | Earned Value Management |
| M-PM-015 | Project Dashboard Design |
| M-PM-016 | Risk Register |
| M-PM-017 | Risk Response Planning |
| M-PM-018 | Lessons Learned |
| M-PM-019 | Project Closure Checklist |
| M-PM-020 | Project Status Report |

### PM Tools (M-PMT-*)
| ID | Name |
|----|------|
| M-PMT-001 | Jira Workflow Management |
| M-PMT-002 | ClickUp Setup |
| M-PMT-003 | Linear Issue Tracking |
| M-PMT-004 | GitHub Projects |
| M-PMT-005 | GitLab Boards |
| M-PMT-006 | Azure DevOps Boards |
| M-PMT-007 | Notion PM |
| M-PMT-008 | Trello Kanban |
| M-PMT-009 | Cross-Tool Migration |
| M-PMT-010 | PM Tool Selection |
| M-PMT-011 | Agile Ceremonies Setup |
| M-PMT-012 | Reporting & Dashboards |

### Business Analysis (M-BA-*)
| ID | Name |
|----|------|
| M-BA-001 | Business Case Development |
| M-BA-002 | Stakeholder Analysis |
| M-BA-003 | Requirements Elicitation |
| M-BA-004 | Use Case Modeling |
| M-BA-005 | User Story Writing |
| M-BA-006 | Acceptance Criteria |
| M-BA-007 | Traceability Matrix |
| M-BA-008 | Gap Analysis |
| M-BA-009 | Process Modeling (BPMN) |
| M-BA-010 | Data Modeling |
| M-BA-011 | Solution Assessment |
| M-BA-012 | Feasibility Study |

### UX/UI (M-UX-*)
| ID | Name |
|----|------|
| M-UX-001 | User Interviews |
| M-UX-002 | Surveys |
| M-UX-003 | Contextual Inquiry |
| M-UX-004 | Competitive Analysis |
| M-UX-005 | Persona Development |
| M-UX-006 | Empathy Mapping |
| M-UX-007 | Journey Mapping |
| M-UX-008 | Service Blueprint |
| M-UX-009 | Information Architecture |
| M-UX-010 | Card Sorting |
| M-UX-011 | Wireframing |
| M-UX-012 | Prototyping |
| M-UX-013 | Usability Testing |
| M-UX-014 | Heuristic Evaluation |
| M-UX-015 | A/B Testing |
| M-UX-016 | Accessibility Audit |
| M-UX-017 | Design System |
| M-UX-018 | Component Library |
| M-UX-019 | Typography System |
| M-UX-020 | Color System |
| M-UX-021 | Spacing System |
| M-UX-022 | Icon System |
| M-UX-023 | Motion Design |
| M-UX-024 | Micro-interactions |
| M-UX-025 | Form Design |
| M-UX-026 | Navigation Patterns |
| M-UX-027 | Search UX |
| M-UX-028 | Error States |
| M-UX-029 | Empty States |
| M-UX-030 | Loading States |
| M-UX-031 | Onboarding |
| M-UX-032 | Dark Mode |

### SDD (M-SDD-*)
| ID | Name |
|----|------|
| M-SDD-001 | Constitution Creation |
| M-SDD-002 | Roadmap Planning |
| M-SDD-003 | Feature Specification |
| M-SDD-004 | Technical Design |
| M-SDD-005 | Implementation Plan |
| M-SDD-006 | Task Breakdown |
| M-SDD-007 | Task Execution |
| M-SDD-008 | Quality Gate |
| M-SDD-009 | Code Review Cycle |
| M-SDD-010 | Reflexion Learning |
| M-SDD-011 | Pattern Memory |
| M-SDD-012 | Mistake Memory |

---

## References

**Workflow:**
- [SDD Workflow](references/workflow.md) - Phases, project/feature selection
- [Directory Structure](references/directory-structure.md) - SDD folder layout
- [Quality Assurance](references/quality-assurance.md) - Confidence checks, reflexion

**Domains:**
- [SDD](references/sdd-domain.md) | [Research](references/research-domain.md) | [Product](references/product-domain.md)
- [Development](references/development-domain.md) | [Marketing](references/marketing-domain.md)
- [PMBOK](references/pm-domain.md) | [BABOK](references/ba-domain.md) | [UX](references/ux-domain.md)
- [AI/LLM](references/ai-llm-domain.md)

---

*Faion Network v2.0*
*13 Domain Skills | 250+ Methodologies | 60+ Agents*
