---
name: multi-agent-parallel-investigation
description: Decompose complex questions into 4-6 parallel investigations with different perspectives, synthesize into phased decision framework. Use when facing architecture decisions with multiple unknowns in crypto/trading data platforms.
---

# Multi-Agent Parallel Investigation

## Overview

This skill provides a systematic approach to answering complex architecture questions by decomposing them into 4-6 parallel investigations, each with a specialized perspective. Each agent investigates independently, then findings are synthesized into a phased decision framework with concrete recommendations.

**Core Pattern**: Spawn multiple Task tool agents in parallel → Each investigates specific dimension → Synthesize findings → Deliver phased implementation plan

## When to Use This Skill

Use this skill when you encounter:

1. **Complex Architecture Decisions** with multiple unknowns requiring investigation from different angles (API capabilities, performance, documentation quality, feasibility)
2. **Trade-off Analysis** where multiple solutions exist with competing priorities (complexity vs performance, cost vs developer UX)
3. **Technology Evaluation** when assessing if a platform/tool/library meets requirements across multiple dimensions
4. **Data Platform Questions** in crypto/trading domains with concerns about availability, correctness, observability, and maintainability
5. **Implementation Planning** when you need phased rollout with clear decision gates based on empirical findings

**Typical Question Patterns**:
- "How should we distribute our Parquet database to external users?"
- "What's the best approach for querying remote data without downloads?"
- "Should we build a CLI tool, improve documentation, or create an API?"
- "How can we validate data quality across multiple sources?"

## Workflow

### Step 1: Decompose Question into Investigation Dimensions

Identify 4-6 specialist perspectives needed to answer the question comprehensively:

**Common Agent Roles** (select 4-6 based on question):
- **API Capabilities Analyst** - Platform API evaluation, endpoint discovery
- **Performance Analyst** - Benchmarking, latency measurements, optimization
- **Documentation Analyst** - Quality assessment, gap identification, UX evaluation
- **Feasibility Engineer** - Prototyping, proof-of-concept, effort estimation
- **Security Analyst** - Threat modeling, credential management, compliance
- **Cost Analyst** - Pricing, rate limits, resource consumption
- **Integration Specialist** - Third-party service integration, compatibility
- **Data Quality Analyst** - Schema validation, coverage assessment, correctness

See [`references/agent-templates.md`](references/agent-templates.md) for detailed role templates.

### Step 2: Spawn Agents in Parallel

Use **single message with multiple Task tool calls** to maximize performance:

```markdown
I'll spawn 4 parallel agents to investigate this question from different perspectives:

[Task tool call 1: API Capabilities Agent with prompt from agent-templates.md]
[Task tool call 2: Performance Analyst Agent with prompt from agent-templates.md]
[Task tool call 3: Documentation Analyst Agent with prompt from agent-templates.md]
[Task tool call 4: Feasibility Engineer Agent with prompt from agent-templates.md]
```

**Key Requirements**:
- Each agent gets ROLE, OBJECTIVE, CONTEXT, DYNAMIC WRITETODO APPROACH, INVESTIGATION QUESTIONS, DELIVERABLES, WORKSPACE
- Agents work independently (no inter-agent communication)
- Each agent uses `/tmp/{role-slug}/` workspace for artifacts
- Each agent reports structured findings back to main context

### Step 3: Dynamic WriteTodo Within Each Agent

**CRITICAL**: Agents use emergent task creation, NOT pre-planned task lists.

**Pattern**:
1. Agent creates ONE initial writeTodo (e.g., "Search for API documentation")
2. Agent completes task → Analyzes findings → Creates NEXT writeTodo based on discoveries
3. Agent marks completed → Executes next → Repeats until investigation complete
4. Let writeTodos emerge naturally from findings

**Example Flow** (API Capabilities Agent):
```
writeTodo 1: "Search for GitHub REST API documentation for release assets"
→ Discovery: Found API endpoints for listing release assets
→ writeTodo 2: "Test HTTP range request support on release asset URL"
→ Discovery: Range requests NOT supported
→ writeTodo 3: "Investigate CDN proxy alternatives (jsDelivr, Cloudflare)"
→ Discovery: jsDelivr supports range requests
→ Investigation complete
```

### Step 4: Wait for Agent Reports

Each agent returns structured report with:
- **Findings Summary** (2-3 sentences)
- **Data/Measurements** (performance numbers, API endpoints, examples)
- **Confidence Level** (HIGH/MEDIUM/LOW with %)
- **Recommendation** (specific action with justification)

### Step 5: Synthesize Findings into Decision Framework

Use patterns from [`references/synthesis-patterns.md`](references/synthesis-patterns.md):

**Choose synthesis pattern based on agent findings**:
- **Consensus Building** - When agents agree on direction, use voting matrix to validate
- **Trade-off Matrix** - When agents have competing priorities, score solutions across dimensions
- **Risk-Based Synthesis** - When findings reveal risks, prioritize by likelihood × impact
- **80/20 Synthesis** - When one solution covers most use cases, identify highest ROI option
- **Confidence Aggregation** - When confidence varies, defer low-confidence phases
- **Phased Decision Framework** - DEFAULT pattern for most investigations

**Example Synthesis** (Phased Decision Framework):

```markdown
## Summary of Parallel Investigations

**Agent 1 (API Capabilities)**: GitHub Releases API supports listing assets but NOT range requests. jsDelivr CDN proxy enables range requests with 95% reliability.

**Agent 2 (Performance)**: DuckDB httpfs queries complete in 2.8s (cold start), bandwidth efficiency 97% vs full download. Range requests work via jsDelivr.

**Agent 3 (Documentation)**: Current README rated 7/10. Missing Quick Start, Prerequisites unclear, no copy-paste examples. Gap: remote query workflow.

**Agent 4 (Feasibility)**: CLI tool buildable in 4-6 hours but adds complexity. Documentation improvements solve 80% of use cases in 2 hours.

## Decision Framework

### Phase 1: Documentation Quick Start (Priority: HIGH)
**Objective**: Enable developers to query remote Parquet in <60 seconds
**Based on**: Agent 3 (documentation gaps) + Agent 2 (proven performance)
**Effort**: 2 hours
**Impact**: Solves 80% of use cases (Agent 4 finding)
**Recommendation**: Add Quick Start section with DuckDB httpfs example, jsDelivr URL pattern, prerequisites

### Phase 2: Performance Optimization (Priority: MEDIUM)
**Objective**: Document query optimization patterns (column pruning, filtering)
**Based on**: Agent 2 (performance benchmarks show 10x speedup with WHERE clauses)
**Effort**: 1 hour
**Impact**: Reduces query time from 2.8s → 0.3s for filtered queries
**Decision Criteria**: Proceed after Phase 1 validates user adoption

### Phase 3: CLI Tool (Priority: LOW, Optional)
**Objective**: Standalone tool for non-Python users
**Based on**: Agent 4 (feasibility prototype)
**Effort**: 4-6 hours
**Impact**: Serves remaining 20% of use cases
**Decision Criteria**: Only proceed if user feedback shows demand after Phase 1+2

## Total Effort Estimate
- **Phase 1**: 2 hours (HIGH confidence)
- **Phase 2**: 1 hour (MEDIUM confidence)
- **Phase 3**: 4-6 hours (LOW confidence, optional)
- **Total**: 3-9 hours depending on user feedback
```

### Step 6: Deliver Actionable Recommendations

Final output should include:
1. **Summary** - What was investigated, what agents found
2. **Decision Framework** - Phased implementation plan with priorities
3. **Success Criteria** - Measurable outcomes (from synthesis-patterns.md → Success Criteria Synthesis)
4. **Validation Plan** - How to test recommendations
5. **Next Steps** - Immediate action items

## Using Bundled Resources

### `references/agent-templates.md`

Contains 10 example agent prompts with complete structure:
- ROLE, OBJECTIVE, CONTEXT
- DYNAMIC WRITETODO APPROACH
- INVESTIGATION QUESTIONS (5-7 specific questions)
- DELIVERABLES (structured output format)
- WORKSPACE (temp directory for artifacts)

**Usage**: Copy relevant template → Customize CONTEXT and QUESTIONS for your specific investigation → Use as Task tool prompt

### `references/synthesis-patterns.md`

Contains 8 frameworks for synthesizing agent findings:
1. **Phased Decision Framework** - Default pattern, structures findings into HIGH/MEDIUM/LOW priority phases
2. **Consensus-Building Pattern** - Voting matrix for conflicting findings
3. **Trade-off Matrix** - Score solutions across dimensions (Complexity, Cost, Performance, UX)
4. **Risk-Based Synthesis** - Prioritize by risk mitigation (P0/P1/P2)
5. **Confidence Level Aggregation** - Defer low-confidence phases
6. **80/20 Synthesis** - Identify highest ROI solution
7. **Integration Strategy** - Structure complementary solutions
8. **Success Criteria Synthesis** - Measurable outcomes from agent findings

**Usage**: After agents report findings, select appropriate synthesis pattern → Fill in template with agent data → Present decision framework

## Domain Context: Crypto/Trading Data Platforms

This skill is optimized for questions about:
- **Data Distribution** - How to serve historical OHLCV data, orderbook snapshots, trade ticks
- **Query Performance** - Remote vs local access, bandwidth optimization, latency requirements
- **Documentation Quality** - Developer onboarding friction, example coverage, troubleshooting guides
- **API Design** - REST endpoints, WebSocket streams, bulk download vs query endpoints
- **Storage Technologies** - Parquet, DuckDB, CSV/JSON, compression formats
- **Infrastructure Decisions** - GitHub Releases, S3, CDN proxies, self-hosted APIs
- **SLO Dimensions** - Availability, Correctness, Observability, Maintainability (NOT speed/performance/security)

**Example Questions from Domain**:
- "Should we use DuckDB httpfs for remote Parquet queries or build a REST API?"
- "How do we balance query latency vs bandwidth efficiency for 20MB Parquet files?"
- "Is documentation sufficient for developers to query our database in <60 seconds?"
- "What's the feasibility of a CLI tool vs extending existing tooling?"

## Tips for Success

1. **Parallel Execution**: Always spawn agents in single message with multiple Task calls (NOT sequential)
2. **Role Specialization**: Each agent should have narrow, distinct focus (avoid overlap)
3. **Dynamic WriteTodos**: Agents discover next steps based on findings, not pre-planned lists
4. **Empirical Evidence**: Agents should measure/test/validate, not speculate
5. **Confidence Levels**: Agents report HIGH/MEDIUM/LOW confidence with percentages
6. **Synthesis Pattern Selection**: Choose pattern based on agent findings (consensus vs conflict vs risk)
7. **Phased Implementation**: Default to 3 phases (HIGH/MEDIUM/LOW priority) with decision gates
8. **Measurable Success**: Define concrete validation criteria (timing, percentages, user counts)

## Common Pitfalls to Avoid

1. **Too Many Agents** (>6) - Synthesis becomes unwieldy, prefer 4-6 focused roles
2. **Pre-planned WriteTodos** - Defeats purpose of emergent investigation, let findings guide tasks
3. **Sequential Agent Execution** - Wastes time, always spawn in parallel unless dependencies exist
4. **Vague Investigation Questions** - Each agent needs 5-7 specific, answerable questions
5. **No Workspace** - Agents need `/tmp/{role}/` directories for artifacts/tests/prototypes
6. **Ignoring Confidence Levels** - Low-confidence findings should trigger Phase 3 (optional), not Phase 1
7. **Skipping Synthesis** - Raw agent reports are not actionable, must synthesize into decision framework
8. **No Validation Plan** - Recommendations need measurable success criteria and test approach
