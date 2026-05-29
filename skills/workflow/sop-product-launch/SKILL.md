/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: SKILL
version: 1.0.0
description: |
  [assert|neutral] SKILL skill for operations workflows [ground:given] [conf:0.95] [state:confirmed]
category: operations
tags:
- general
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute SKILL workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic operations processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "SKILL",
  category: "operations",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["SKILL", "operations", "workflow"],
  context: "user needs SKILL capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# SOP: Product Launch Workflow

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Complete end-to-end product launch process using multi-agent coordination.

## Timeline: 10 Weeks

**Phases**:
1. Research & Planning (Week 1-2)
2. Product Development (Week 3-6)
3. Marketing & Sales Prep (Week 5-8)
4. Launch Execution (Week 9)
5. Post-Launch Monitoring (Week 10+)

---

## Phase 1: Research & Planning (Week 1-2)

### Week 1: Market Research

**Sequential Workflow**:

```javascript
// Step 1: Market Analysis
await Task("Market Researcher", `
Conduct comprehensive market analysis:
- Target market size and demographics
- Competitor analysis (features, pricing, positioning)
- Market trends and opportunities
- Customer pain points and needs

Store findings in memory: market-research/product-launch-2024/analysis
`, "researcher");

// Step 2: Retrieve results and delegate to Business Analyst
const marketData = await memory_retrieve('market-research/product-launch-2024/analysis');

await Task("Business Analyst", `
Using market data: ${marketData}

Perform:
- SWOT analysis
- Business model validation
- Revenue projections
- Risk assessment

Store results: business-analysis/product-launch-2024/strategy
`, "analyst");

// Step 3: Product Strategy
await Task("Product Manager", `
Using:
- Market analysis: market-research/product-launch-2024/analysis
- Business analysis: business-analysis/product-launch-2024/strategy

Define:
- Product positioning
- Feature prioritization (MVP vs future)
- Pricing strategy
- Go-to-market strategy

Store: product-strategy/product-launch-2024/plan
`, "planner");
```

**Deliverables**:
- Market analysis report
- SWOT analysis
- Product strategy document
- Launch timeline

---

## Phase 2: Product Development (Week 3-6)

### Week 3-4: Technical Architecture & Development

**Parallel Workflow** (Backend + Frontend + Mobile):

```javascript
// Initialize development swarm
await mcp__ruv-swarm__swarm_init({
  topology: 'mesh',
  maxAgents: 6,
  strategy: 'adaptive'
});

// Parallel agent spawning
const [backend, frontend, mobile, database, security, tester] = await Promise.all([
  Task("Backend Developer", `
Using product requirements from: product-strategy/product-launch-2024/plan

Build:
- REST API with authentication
- Database schema and migrations
- Business logic layer
- Integration with payment gateway

Store API spec: backend-dev/product-launch-2024/api-spec
Store schema: backend-dev/product-launch-2024/db-schema
`, "backend-dev"),

  Task("Frontend Developer", `
Using API spec from: backend-dev/product-launch-2024/api-spec

Build:
- React web application
- Component library
- State management (Redux/Context)
- API integration layer

Store components: frontend-dev/product-launch-2024/components
`, "coder"),

  Task("Mobile Developer", `
Using API spec from: backend-dev/product-launch-2024/api-spec

Build:
- React Native mobile app (iOS + Android)
- Native modules for device features
- Offline sync capability
- Push notifications

Store builds: mobile-dev/product-launch-2024/builds
`, "mobile-dev"),

  Task("Database Architect", `
Design optimized database:
- Schema design for scalability
- Indexing strategy
- Query optimization
- Backup and recovery plan

Store: database/product-launch-2024/architecture
`, "code-analyzer"),

  Task("Security Specialist", `
Implement security:
- Authentication (OAuth 2.0 + JWT)
- Authorization (RBAC)
- Data encryption (at rest + in transit)
- Security audit and penetration testing

Store audit: security/product-launch-2024/audit
`, "reviewer"),

  Task("QA Engineer", `
Create test suite:
- Unit tests (90%+ coverage)
- Integration tests
- E2E tests
- Performance tests
- Security tests

Store test plan: testing/product-launch-2024/plan
`, "tester")
]);

// Wait for all parallel tasks to complete
await Promise.all([backend, frontend, mobile, database, security, tester]);
```

### Week 5-6: Integration & Testing

**Sequential Workflow**:

```javascr

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/operations/SKILL/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "SKILL-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>SKILL_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
