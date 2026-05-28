/*============================================================================*/
/* WHEN-RELEASING-NEW-PRODUCT-ORCHESTRATE-PRODUCT-LAUNCH SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-releasing-new-product-orchestrate-product-launch
version: 1.0.0
description: |
  [assert|neutral] Use when launching a new product end-to-end from market research through post-launch monitoring. Orchestrates 15+ specialist agents across 5 phases in a 10-week coordinated workflow including research [ground:given] [conf:0.95] [state:confirmed]
category: orchestration
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-releasing-new-product-orchestrate-product-launch workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic orchestration processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-releasing-new-product-orchestrate-product-launch",
  category: "orchestration",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["when-releasing-new-product-orchestrate-product-launch", "orchestration", "workflow"],
  context: "user needs when-releasing-new-product-orchestrate-product-launch capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Product Launch Orchestration Workflow

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Complete end-to-end product launch workflow orchestrating 15+ specialist agents across research, development, marketing, launch execution, and post-launch monitoring. Designed for comprehensive product launches requiring coordination across technical, marketing, sales, and operations teams.

## Overview

This SOP orchestrates a complete 10-week product launch using multi-agent coordination with hierarchical topology. The workflow balances sequential dependencies with parallel execution to optimize both speed and quality. Each phase produces specific deliverables stored in memory for subsequent phases to consume, ensuring continuity and context preservation.

## Trigger Conditions

Use this workflow when:
- Launching a new product or major feature requiring comprehensive go-to-market
- Coordinating across multiple teams (engineering, marketing, sales, support)
- Need systematic approach covering all launch aspects from research to post-launch
- Timeline spans multiple weeks with clear phases and deliverables
- Require coordination between development, marketing campaigns, and sales enablement
- Post-launch monitoring and optimization are critical to success

## Orchestrated Agents (15 Total)

### Research & Planning Agents
- **`market-researcher`** - Market analysis, competitive research, customer insights, trend identification
- **`business-analyst`** - SWOT analysis, business model validation, revenue projections, risk assessment
- **`product-manager`** - Product strategy, feature prioritization, positioning, go-to-market planning

### Development & Engineering Agents
- **`backend-developer`** - REST/GraphQL API development, server-side logic, business layer implementation
- **`frontend-developer`** - Web UI development, React/Vue components, state management, client integration
- **`mobile-developer`** - iOS/Android applications, React Native, cross-platform, offline sync
- **`database-architect`** - Schema design, query optimization, indexing strategy, data modeling
- **`security-specialist`** - Security audits, vulnerability scanning, compliance validation, penetration testing
- **`qa-engineer`** - Test suite creation, integration testing, E2E testing, performance validation

### Marketing & Sales Agents
- **`marketing-specialist`** - Campaign creation, audience segmentation, multi-channel strategy, KPI tracking
- **`sales-specialist`** - Sales enablement, pipeline setup, lead qualification, revenue forecasting
- **`content-creator`** - Blog posts, social media content, email sequences, video scripts, landing pages
- **`seo-specialist`** - Keyword research, on-page SEO, link building, search optimization

### Launch & Operations Agents
- **`devops-engineer`** - CI/CD pipelines, Docker/K8s deployment, infrastructure setup, monitoring configuration
- **`production-validator`** - Production readiness assessment, go/no-go decision, deployment validation
- **`performance-monitor`** - Metrics collection, alert configuration, anomaly detection, dashboard setup
- **`customer-support-specialist`** - Support infrastructure, knowledge base, ticket workflows, team training

## Workflow Phases

### Phase 1: Research & Planning (Week 1-2, Sequential → Parallel)

**Duration**: 2 weeks
**Execution Mode**: Sequential analysis then parallel strategy
**Agents**: `market-researcher`, `business-analyst`, `product-manager`

**Process**:

1. **Conduct Comprehensive Market Analysis** (Day 1-3)
   ```bash
   npx claude-flow hooks pre-task --description "Product launch: ${PRODUCT_NAME}"
   npx claude-flow swarm init --topology hierarchical --max-agents 15
   npx claude-flow agent spawn --type researcher
   ```

   Spawn `market-researcher` agent to:
   - Analyze target market size, demographics, and segmentation
   - Research competitors (features, pricing, positioning, market share)
   - Identify market trends, opportunities, 

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
  pattern: "skills/orchestration/when-releasing-new-product-orchestrate-product-launch/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-releasing-new-product-orchestrate-product-launch-{session_id}",
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

[commit|confident] <promise>WHEN_RELEASING_NEW_PRODUCT_ORCHESTRATE_PRODUCT_LAUNCH_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
