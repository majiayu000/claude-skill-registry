---
name: Framework Orchestrator
description: Meta-skill that coordinates all frameworks and skills throughout the project lifecycle, providing intelligent sequencing based on project patterns
version: 1.0.0
category: orchestration
triggers:
  - 'framework-orchestrator'
  - 'framework orchestrator'
  - 'orchestrate frameworks'
  - 'coordinate skills'
  - 'project orchestration'
dependencies:
  required_mcps: []
  required_tools: []
  required_integrations: []
---

# Framework Orchestrator

## Overview

The Framework Orchestrator is the meta-skill that coordinates all other skills and frameworks throughout your project lifecycle. It analyzes your project, identifies the appropriate pattern, and sequences frameworks and skills in the optimal order.

**Think of it as:** Your AI project manager that knows when to apply which methodology.

## When to Use This Skill

Use Framework Orchestrator when:

- Starting a new project and need guidance on methodology
- Unsure which frameworks or skills to apply first
- Want a complete orchestrated plan for your project
- Need to understand your project's complexity pattern
- Transitioning between project phases
- Managing multiple workstreams in parallel

## Key Capabilities

- Analyze projects and identify complexity patterns (A, B, C)
- Recommend optimal framework sequences
- Coordinate skill activation at appropriate phases
- Provide phase-gate validation
- Adapt orchestration based on project evolution
- Ensure comprehensive coverage across all dimensions

## Workflow

### Step 1: Pattern Identification

**Analyze the project and categorize into one of three patterns:**

#### Pattern A: Simple Feature/Enhancement

**Characteristics:**

- Adding to existing system
- Well-understood requirements
- Low risk, minimal security impact
- Single-team, short timeline (days to 1-2 weeks)

**Examples:**

- Add filter to existing search
- New dashboard widget
- Form field additions
- UI styling updates

**Timeline:** 1-5 days

---

#### Pattern B: New Product/System

**Characteristics:**

- Building from scratch or major module
- User validation needed
- Security/compliance important
- Multiple considerations (UX, architecture, testing)
- Medium timeline (weeks to months)

**Examples:**

- New SaaS product
- Customer portal
- Internal tool
- API platform

**Timeline:** 4-12 weeks

---

#### Pattern C: AI-Native/Complex System

**Characteristics:**

- All Pattern B characteristics, PLUS:
- AI agents, RAG systems, or knowledge graphs
- Complex orchestration
- Novel technology
- Higher uncertainty and iteration

**Examples:**

- Multi-agent AI system
- RAG-powered knowledge base
- Intelligent automation platform
- AI-assisted decision support

**Timeline:** 8-20 weeks

---

### Step 2: Framework Selection

**Based on pattern, recommend framework sequence:**

#### Pattern A Sequence (Simple Feature)

1. **simple_feature_framework** - Lightweight requirements and validation
2. **code-quality-enforcer** - Ensure code standards
3. **testing-strategist** - Unit test coverage
4. **deployment-advisor** - Ship quickly

**Coordinating Skills:**

- quality-assurance (testing)
- performance-optimizer (if needed)

---

#### Pattern B Sequence (New Product)

**Phase 1: Discovery & Validation**

- **discovery_validation_framework** - User research and problem validation
- **product_market_fit_framework** - Market analysis and positioning
- **prp-generator** skill - Create Product Requirements Prompt
- **user-researcher** skill - Conduct user interviews

**Phase 2: Architecture & Design**

- **bmad-method** skill - Business model and architecture alignment
- **design_prototyping_framework** - Wireframes and prototypes
- **ux-designer** skill - User journey mapping
- **security-architect** skill - Threat modeling and security design
- **api-designer** skill (if applicable) - API contract design

**Phase 3: Development**

- **full_stack_dev_framework** - Implementation guidance
- **frontend-builder** / **api-designer** skills - Build UI and backend
- **quality-assurance** skill - Code quality and testing

**Phase 4: Testing & Validation**

- **testing_validation_framework** - Comprehensive testing strategy
- **quality-assurance** skill - Test pyramid execution
- **usability-tester** skill - User acceptance testing
- **security-architect** skill - Security testing

**Phase 5: Deployment & Launch**

- **deployment_devops_framework** - CI/CD and infrastructure
- **deployment-advisor** skill - Deployment strategy
- **go-to-market-planner** skill - Launch planning

---

#### Pattern C Sequence (AI-Native)

**All Pattern B phases, PLUS:**

**Phase 2b: AI Architecture (parallel with standard architecture)**

- **multi-agent-architect** skill - Agent system design
- **rag-implementer** skill - RAG architecture (if applicable)
- **knowledge-graph-builder** skill - Knowledge structure (if applicable)
- **agentic-workflow-orchestration-framework** - Agent coordination

**Phase 3b: AI Development (integrated with standard development)**

- **context_engineering_framework** - Prompt and context design
- **multi_agent_orchestration_framework** - Agent implementation

**Phase 4b: AI Testing (additional testing layer)**

- Test agent behaviors and edge cases
- Validate RAG retrieval quality
- Benchmark LLM performance

---

### Step 3: Phase Orchestration

**Execute phases with validation gates:**

#### Phase Gate Structure

**Entry to Phase 2 (Design):**

- PRP document complete
- Problem statement validated
- Success metrics defined
- User stories documented

**Entry to Phase 3 (Development):**

- Architecture documented
- Data model designed
- Security threats identified
- Mitigations planned

**Entry to Phase 4 (Testing):**

- Features complete
- Unit tests >80% coverage
- Code review passed
- SAST scans clean

**Entry to Phase 5 (Deployment):**

- All tests passing
- UAT completed
- Security testing done
- Coverage >90%

---

### Step 4: Skill Coordination

**Orchestrate skills based on current phase:**

**Discovery Phase Skills:**

- user-researcher
- product-strategist
- product-analyst

**Design Phase Skills:**

- ux-designer
- design-system-architect
- bmad-method
- security-architect

**Development Phase Skills:**

- frontend-builder
- api-designer
- multi-agent-architect (Pattern C)
- rag-implementer (Pattern C)
- mvp-builder

**Testing Phase Skills:**

- quality-assurance
- usability-tester
- security-architect

**Deployment Phase Skills:**

- deployment-advisor
- go-to-market-planner
- performance-optimizer

**Post-Launch Skills:**

- product-analyst
- customer-feedback-analyzer
- performance-optimizer

---

## Examples

### Example 1: SaaS Analytics Platform (Pattern B)

**Project Analysis:**

- New product from scratch
- B2B SaaS model
- Security and compliance important
- 8-week timeline

**Recommended Sequence:**

**Week 1: Discovery**

1. discovery_validation_framework
2. user-researcher skill → User interviews
3. product-strategist skill → Market validation
4. prp-generator skill → Create PRP

**Week 2: Architecture** 5. bmad-method skill → Business model + architecture alignment 6. design_prototyping_framework → Wireframes 7. ux-designer skill → User journeys 8. api-designer skill → API design 9. security-architect skill → Threat model

**Week 3-6: Development** 10. full_stack_dev_framework 11. frontend-builder skill → Build React UI 12. api-designer skill → Build backend 13. quality-assurance skill → Continuous testing

**Week 7: Testing** 14. testing_validation_framework 15. quality-assurance skill → Test pyramid 16. usability-tester skill → User testing 17. security-architect skill → Security testing

**Week 8: Deployment** 18. deployment_devops_framework 19. deployment-advisor skill → Deploy to production 20. go-to-market-planner skill → Launch plan

---

### Example 2: Multi-Agent Customer Support System (Pattern C)

**Project Analysis:**

- AI-native system with multiple agents
- RAG for knowledge retrieval
- Complex orchestration
- 12-week timeline

**Recommended Sequence:**

**Week 1-2: Discovery (same as Pattern B)**

**Week 3-4: Architecture**

- bmad-method skill
- security-architect skill
- **multi-agent-architect skill** → Agent system design
- **rag-implementer skill** → RAG architecture
- **knowledge-graph-builder skill** → Knowledge structure
- agentic-workflow-orchestration-framework

**Week 5-9: Development**

- full_stack_dev_framework
- frontend-builder skill
- **multi-agent-architect skill** → Agent implementation
- **rag-implementer skill** → Vector DB + embeddings
- context_engineering_framework → Prompt design
- quality-assurance skill

**Week 10-11: Testing**

- testing_validation_framework
- quality-assurance skill
- **Test agent behaviors, RAG quality, LLM performance**
- usability-tester skill

**Week 12: Deployment**

- deployment_devops_framework
- deployment-advisor skill
- go-to-market-planner skill

---

### Example 3: Add User Export Feature (Pattern A)

**Project Analysis:**

- Enhancement to existing system
- Well-understood requirements
- Low complexity
- 3-day timeline

**Recommended Sequence:**

**Day 1:**

1. simple_feature_framework → Define requirements
2. api-designer skill → Design export endpoint

**Day 2:** 3. Build backend + frontend 4. quality-assurance skill → Unit tests

**Day 3:** 5. testing-strategist skill → Integration tests 6. deployment-advisor skill → Deploy to staging, then production

---

## Best Practices

### 1. Always Start with Pattern Identification

Don't jump to frameworks. First understand:

- Scope (simple feature, new product, AI system)
- Timeline (days, weeks, months)
- Risk (low, medium, high)

### 2. Respect Phase Gates

Don't skip validation checkpoints. Each gate ensures:

- Previous work is complete
- Next phase has proper foundation
- Risks are identified and mitigated

### 3. Parallelize When Possible

Some work can run in parallel:

- UX design + Architecture design (Phase 2)
- Frontend + Backend development (Phase 3)
- Test writing + Feature development (Phase 3)

### 4. Adapt Orchestration Based on Reality

If project evolves:

- Pattern A → Pattern B: Add discovery and design phases
- Pattern B → Pattern C: Add AI architecture and testing
- Scope reduction: Simplify orchestration

### 5. Coordinate Skills, Don't Overwhelm

Don't activate all skills at once. Sequence them:

- 1-3 skills per phase maximum
- Clear handoffs between skills
- Each skill has specific deliverable

---

## Common Pitfalls

### 1. Mis-Identifying Pattern

**Antipattern:** Treating Pattern B (new product) as Pattern A (simple feature)
**Result:** Skip discovery, build wrong thing

**Fix:** If any uncertainty exists, default to Pattern B

### 2. Skipping Phases

**Antipattern:** Jump straight to development without design
**Result:** Rework, missed requirements, security gaps

**Fix:** Respect the sequence, validate phase gates

### 3. Over-Orchestrating Simple Features

**Antipattern:** Use full Pattern B orchestration for a button color change
**Result:** Waste time on unnecessary process

**Fix:** Pattern A is valid for truly simple work

### 4. Under-Orchestrating Complex Projects

**Antipattern:** Build AI system without proper architecture phase
**Result:** Technical debt, poor performance, rewrites

**Fix:** Pattern C requires comprehensive orchestration

### 5. Ignoring Phase Gates

**Antipattern:** Move to development with incomplete architecture
**Result:** Build on shaky foundation, blockers mid-development

**Fix:** Enforce phase gates, document readiness

---

## Related Skills

- **prp-generator** - Creates requirements (called by orchestrator in Phase 1)
- **bmad-method** - Business/architecture alignment (Phase 2)
- **security-architect** - Security design (Phase 2 & 4)
- **quality-assurance** - Testing strategy (Phase 3 & 4)
- **deployment-advisor** - Infrastructure (Phase 5)
- **All other skills** - Activated by orchestrator at appropriate phases

---

## Deliverables

When using Framework Orchestrator, produce:

1. **Pattern Identification**
   - Pattern: A, B, or C
   - Rationale for classification
   - Estimated timeline

2. **Orchestration Plan**
   - Phase breakdown
   - Framework sequence
   - Skill activation points
   - Phase gate criteria

3. **Current Phase Status**
   - Where you are now
   - Completion percentage
   - Gate criteria readiness
   - Next steps

4. **Risk & Adaptation Plan**
   - Identified risks
   - Contingency plans
   - When to adapt orchestration

---

## Success Metrics

Successful orchestration means:

- Right pattern identified (no mis-classification)
- Frameworks applied in optimal sequence
- Phase gates enforced and passed
- Skills activated at appropriate times
- No major rework due to skipped phases
- Team clarity on current phase and next steps
- Project delivered with appropriate quality for pattern

---

**Remember:** The orchestrator ensures you apply the right methodology at the right time. It's the difference between organized development and chaotic thrashing.
