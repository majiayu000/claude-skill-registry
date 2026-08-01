---
name: internet-research-orchestrator
description: Orchestrate comprehensive TODAS research for novel/emerging domains (1-7
  subagents adaptive). Specializes in unprecedented topics, post-training data, and
  emerging technologies. Uses adaptive depth-ba
---

---
name: internet-research-orchestrator
description: Orchestrate comprehensive TODAS research for novel/emerging domains (1-7 subagents adaptive). Specializes in unprecedented topics, post-training data, and emerging technologies. Uses adaptive depth-based methodology: straightforward queries (1 agent), standard queries (2-3 agents), complex queries (5-7 agents). Handles depth-first (multiple perspectives), breadth-first (distinct sub-topics), and straightforward investigations. Triggers include "novel", "emerging", "2025", "2026", "unprecedented", "new technology", research on topics that didn't exist during training cutoff.
---

# Novel Domain Research Orchestration (Tier 5 TODAS)

**What is TODAS**: Tactical Optimization & Depth-Adaptive System - an adaptive research methodology that adjusts agent count (1-7) and research depth based on query complexity and novelty. Optimized for emerging domains and post-training information.

## Quick Start

1. **Analyze query novelty**: Assess if topic is novel/emerging (post-training, unprecedented, 2025+ developments)
2. **Determine query type**: Depth-first (multiple perspectives), Breadth-first (distinct sub-topics), or Straightforward
3. **Setup progress tracking**: Use TodoWrite to create task list for research phases
4. **Calculate adaptive agent count**: 1 (simple) to 7 (complex) based on query dimensions and novelty
5. **Execute TODAS workflow**: Assessment → Query Type → Plan → Execution
6. **Spawn research-subagent instances**: Use Task tool with adaptive count (1-7 agents in parallel)
7. **Synthesize findings**: Integrate results from all subagents into coherent analysis
8. **Report completion**: Summary with source attribution and novelty assessment

## TODAS Methodology Overview

**Tier 5 specialization**: Novel and emerging domains requiring adaptive orchestration.

**When to use this skill**:
- ✅ Novel/emerging domains (didn't exist during training)
- ✅ Post-training developments (2025, 2026 technologies)
- ✅ Unprecedented topics (new paradigms, bleeding-edge tech)
- ✅ Rapidly evolving fields (AI agents, quantum computing, Web3)
- ✅ Multi-faceted queries requiring coordination (1-7 dimensions)

**When NOT to use this skill**:
- ❌ Established domains with known patterns (use Tier 4 internet-deep-orchestrator)
- ❌ Simple lookups (use Tier 1 web-researcher)
- ❌ Specialist queries (use Tier 2: academic-researcher, trend-analyst, etc.)
- ❌ Standard multi-dimensional research (use Tier 3 internet-light-orchestrator)

**Adaptive depth**: TODAS adjusts research depth dynamically:
- **Straightforward queries**: 1 subagent (direct investigation)
- **Standard complexity**: 2-3 subagents (multiple perspectives or sub-topics)
- **Medium complexity**: 3-5 subagents (multi-faceted approaches)
- **High complexity**: 5-7 subagents (broad coverage, many dimensions)

**Tactical optimization**: Stop research when diminishing returns reached (efficiency over completeness).

## Workflow: 4-Phase TODAS Process

### Phase 1: Assessment and Breakdown

**Analyze the user's query thoroughly**:

1. **Identify core concepts**: Main entities, relationships, key questions
2. **List required data**: Specific facts, temporal constraints, contextual boundaries
3. **Assess novelty**: Is this topic post-training? Emerging? Unprecedented?
4. **User expectations**: What form should answer take? (Report, analysis, comparison, list, etc.)
5. **Critical analysis**: What features are most important? What does user care about most?

**Output**: Clear understanding of query scope, novelty level, and expected deliverable format.

### Phase 2: Query Type Determination

**Explicitly classify query into one of three types**:

#### Depth-First Query
**When**: Multiple perspectives on SAME issue (going deep from many angles)

**Characteristics**:
- Single core question benefiting from diverse approaches
- Requires different viewpoints, methodologies, or sources
- Example: "What are the most effective treatments for depression?" (explore different treatments/approaches)
- Example: "What caused the 2008 financial crisis?" (economic, regulatory, behavioral, historical perspectives)
- Example: "Best approach to building AI finance agents in 2025?" (multiple methodologies)

**Research strategy**:
- Deploy 3-5 subagents exploring different methodological approaches
- Each subagent investigates from unique perspective
- Synthesis integrates diverse viewpoints into coherent analysis

#### Breadth-First Query
**When**: Distinct, independent sub-questions (going wide across topics)

**Characteristics**:
- Naturally divides into multiple parallel research streams
- Sub-topics can be researched independently
- Example: "Compare economic systems of three Nordic countries" (3 independent country researches)
- Example: "Fortune 500 CEOs net worths and names" (intractable as single thread, split into batches)
- Example: "Compare major frontend frameworks" (identify frameworks, then research each)

**Research strategy**:
- Enumerate all distinct sub-questions/sub-tasks
- Deploy subagents with clear, crisp boundaries (prevent overlap)
- Prioritize by importance and complexity
- Aggregate findings into coherent whole

#### Straightforward Query
**When**: Focused, well-defined, single investigation sufficient

**Characteristics**:
- Simple fact-finding or basic analysis
- Does not benefit from extensive multi-agent research
- Example: "What is current population of Tokyo?" (simple lookup)
- Example: "List all Fortune 500 companies" (single resource fetch)
- Example: "Tell me about bananas" (basic query, short answer expected)

**Research strategy**:
- Deploy 1 subagent with clear, focused instructions
- Specify exact data points required
- Include basic verification methods
- Synthesize findings efficiently

**Output**: Explicit query type classification with reasoning.

### Phase 3: Detailed Research Plan Development

**Based on query type, develop specific plan**:

#### For Depth-First Queries:
1. Define 3-5 different methodological approaches or perspectives
2. List specific expert viewpoints or sources of evidence
3. Plan how each perspective contributes unique insights
4. Specify synthesis strategy for integrating findings
5. Example: "What causes obesity?" → genetic factors, environmental influences, psychological aspects, socioeconomic patterns, biomedical evidence

#### For Breadth-First Queries:
1. Enumerate all distinct sub-questions/sub-tasks
2. Identify most critical sub-questions (focus on essential, avoid every angle)
3. Prioritize by importance and expected complexity
4. Define clear boundaries between sub-topics (prevent overlap)
5. Plan aggregation strategy
6. Example: "Compare EU country tax systems" → retrieve EU countries list, define comparison metrics, batch research by region (Northern, Western, Eastern, Southern Europe)

#### For Straightforward Queries:
1. Identify most direct, efficient path to answer
2. Determine if basic fact-finding or minor analysis needed
3. Specify exact data points required
4. Determine most relevant sources
5. Plan basic verification methods
6. Create extremely clear task description for subagent

**For all query types, evaluate each step**:
- Can this be broken into independent subtasks? (efficiency)
- Would multiple perspectives benefit this? (depth)
- What specific output is expected? (clarity)
- Is this strictly necessary to answer query? (focus)

**Output**: Concrete research plan with clear subagent allocation.

### Phase 3a: Dimension Complexity Assessment (Resource Planning)

**Before selecting specialists, assess each dimension's complexity to guide resource allocation**:

#### Complexity Scoring Framework

**For EACH dimension, evaluate these factors**:

1. **Sub-domains Count**: How many distinct research areas?
   - Example: Security dimension = academic papers + current threats + compliance standards = 3 sub-domains
   - Scoring: 1 sub-domain = +1, 2 sub-domains = +2, 3+ sub-domains = +3

2. **Criticality Level**: High-stakes domain requiring extra rigor?
   - HIGH criticality: Security, medical, financial, legal, compliance
   - MODERATE criticality: Business strategy, market analysis
   - LOW criticality: General information, non-critical topics
   - Scoring: HIGH = +2, MODERATE = +1, LOW = +0

3. **Novelty/Uncertainty**: Emerging or post-training topic?
   - HIGH novelty: 2025+ developments, unprecedented topics, emerging tech
   - MODERATE novelty: Recent 2024 developments, evolving fields
   - LOW novelty: Established topics, well-documented areas
   - Scoring: HIGH = +1, MODERATE = +0.5, LOW = +0

4. **Source Diversity Needed**: How many different source types required?
   - Examples: Academic journals, industry blogs, official docs, market reports, standards/regulations
   - Scoring: 1-2 source types = +2, 3+ source types = +3

**Complexity Classification** (total score):
- **Simple** (1-3 points): 1 specialist sufficient
- **Moderate** (4-6 points): 1-2 specialists recommended
- **Complex** (7-9 points): 2-3 specialists recommended
- **Critical** (10+ points): 3+ specialists + dedicated fact-checker REQUIRED

#### Example Complexity Assessment

**Dimension 4: Security and Multi-Tenancy Architectures**

Factors:
- Sub-domains: Academic security papers + Current 2025 threats + Compliance standards = 3 sub-domains → +3
- Criticality: HIGH (security domain) → +2
- Novelty: MODERATE (2025 emerging security patterns) → +0.5
- Source diversity: Academic + Industry + Regulatory = 3 types → +3

**Total Score**: 3 + 2 + 0.5 + 3 = **8.5 points → COMPLEX**

**Recommendation**: 2-3 specialists for comprehensive coverage
- Consider: academic-researcher (papers) + web-researcher (threats) + search-specialist (standards)

**Dimension 1: Mobile-Native Push Notifications**

Factors:
- Sub-domains: Platform implementations only = 1 sub-domain → +1
- Criticality: LOW (informational) → +0
- Novelty: LOW (established patterns) → +0
- Source diversity: Official docs + Engineering blogs = 2 types → +2

**Total Score**: 1 + 0 + 0 + 2 = **3 points → SIMPLE**

**Recommendation**: 1 specialist sufficient
- Likely match: web-researcher (current platform documentation)

**Output**: Complexity score and allocation recommendation for each dimension.

### Phase 3b: Specialist Selection with Self-Challenge (CRITICAL QUALITY GATE)

**For EACH dimension, perform rigorous specialist selection with adversarial validation**:

#### Step 1: Requirements Analysis & Initial Selection

**Dimension [N]: [Dimension Name]**

**Requirements Analysis**:
- What information is needed? (facts, trends, papers, market data, standards)
- What sources are required? (academic journals, industry blogs, official docs, regulations)
- Current vs future focus? (2024 current state vs 2025+ emerging trends)
- Theoretical vs production focus? (research papers vs real-world implementations)

**Candidate Specialists** (list 2-3 types that COULD handle this dimension):
- **Candidate A**: [specialist_type] - **Strengths**: [what they excel at for this dimension]
- **Candidate B**: [specialist_type] - **Strengths**: [what they excel at for this dimension]
- **Candidate C**: [specialist_type] - **Strengths**: [what they excel at for this dimension]

**Initial Selection**: [specialist_type]

**Initial Rationale**: [Why this specialist best matches the dimension requirements - be specific about the match between requirements and specialist capabilities]

#### Step 2: Self-Challenge Phase (🚨 MANDATORY - DO NOT SKIP)

**The self-challenge phase prevents lazy defaulting and ensures optimal specialist matching.**

🚨 **CHALLENGE**: "Wait, why didn't I choose [alternative_specialist] instead of [initial_selection]?"

**For EACH alternative candidate** (repeat 2-3 times per dimension):

**Alternative: [alternative_specialist_type]**

**Gains if chosen**:
- What unique value would this specialist provide?
- What perspectives/sources/capabilities does it have that initial selection lacks?
- What dimension requirements would it serve BETTER?
- Example: "trend-analyst would provide emerging 2025 patterns and weak signal detection that web-researcher doesn't offer"

**Cons if chosen**:
- What would this specialist LACK compared to initial selection?
- What dimension requirements would be UNDERSERVED?
- What trade-offs would we accept?
- Example: "trend-analyst forecasts FUTURE trends but dimension needs CURRENT production implementations"

**Comparison**: [initial_selection] vs [alternative]
- **Where initial wins**: [Specific requirements where initial is stronger]
- **Where alternative wins**: [Specific requirements where alternative is stronger]
- **Net assessment**: [Which better matches the dimension's PRIMARY requirements?]
- **🚨 Critical question**: Does this comparison reveal initial selection was suboptimal?

**Verdict**:
- ✅ **KEEP [initial_selection]** - Rationale: [Why initial still best after challenge]
- OR
- ❌ **SWITCH to [alternative]** - Rationale: [Why alternative is actually better - challenge caught a mismatch]

**Repeat challenge for Alternative B, Alternative C**

#### Step 3: Final Selection Documentation

**Dimension [N] - FINAL SELECTION**: [specialist_type]

**Final Rationale** (after surviving self-challenge):
- **Chosen because**: [Strengths that best match dimension requirements]
- **Alternatives considered and rejected**:
  - [Alternative A]: Rejected because [specific weakness or mismatch for THIS dimension]
  - [Alternative B]: Rejected because [specific weakness or mismatch for THIS dimension]
- **Decision confidence**: HIGH (explicit adversarial challenge performed and passed)

#### Example Self-Challenge Workflow

**Dimension 5: Real-Time Coordination Mechanisms**

**Requirements**:
- WebSocket/SSE/WebRTC protocol documentation
- Shopify Mobile Bridge architecture (current)
- W3C MiniApp standardization status
- **Novel aspect**: Query mentions "emerging in 2025" (cutting-edge focus)

**Candidates**:
- web-researcher: Current documentation, engineering blogs, official specs
- trend-analyst: Emerging real-time trends, future forecasts, 2025+ developments
- search-specialist: Deep protocol search, technical specifications

**Initial Selection**: web-researcher

**Initial Rationale**: Can access Shopify engineering blog, W3C specification documents, WebSocket/SSE/WebRTC official protocol documentation

🚨 **CHALLENGE**: "Wait, why didn't I choose trend-analyst instead?"

**Alternative: trend-analyst**

**Gains**:
- Query EXPLICITLY mentions "emerging in 2025" and "cutting-edge"
- trend-analyst excels at identifying future real-time coordination trends
- Could forecast WebTransport, WebRTC 2.0, bleeding-edge 2025+ protocols
- Weak signal detection for emerging patterns

**Cons**:
- Might miss current production implementations (Shopify Mobile Bridge is CURRENT, not future)
- Could over-focus on speculative technologies not yet production-ready
- W3C current standardization status needs CURRENT docs, not future speculation

**Comparison**: web-researcher vs trend-analyst
- **Where web-researcher wins**: Current production (Shopify), W3C current status (documentation)
- **Where trend-analyst wins**: Emerging 2025 protocols, future forecasting ("cutting-edge" keyword match)
- **Net assessment**: This dimension has BOTH current (Shopify, W3C status) AND future ("emerging 2025") aspects
- **🚨 WAIT**: The "emerging in 2025" and "cutting-edge" keywords suggest future focus is PRIMARY!

**Verdict**: ❌ **SWITCH to trend-analyst**

**Justification**: Self-challenge revealed the "emerging 2025" and "cutting-edge" keywords indicate this is a FUTURE-focused dimension. trend-analyst's forecasting strength better matches the PRIMARY requirement (emerging patterns) than web-researcher's current documentation strength. **Initial selection was suboptimal - self-challenge caught this mismatch.**

**Final Selection**: trend-analyst ✅ (REVISED from web-researcher)

**Final Rationale**:
- Chosen because: "Emerging 2025" focus requires forecasting capability > current documentation
- web-researcher rejected: Strength is current state, but dimension emphasizes emerging/cutting-edge
- search-specialist rejected: Deep search less valuable than trend forecasting for future-focused dimension
- Decision confidence: HIGH (self-challenge caught keyword mismatch and corrected suboptimal initial choice)

**Output**: Final specialist selection per dimension with explicit challenge-survived rationales.

### Phase 3c: Resource Allocation Challenge (Quantity per Dimension)

**After selecting specialist TYPES, determine COUNTS (how many specialists per dimension)**:

#### Resource Allocation Framework

**Default**: 1 specialist per dimension (efficiency)

**Upgrade to 2-3 specialists when**:
- Complexity score ≥7 (Complex or Critical dimensions)
- Coverage analysis reveals significant gaps with single specialist
- Critical domain requires redundancy (security, medical, financial)

#### For EACH Dimension: Allocation Decision

**Dimension [N]: [Dimension Name]**

**Complexity Score**: [score from Phase 3a]
**Selected Specialist(s)**: [type(s)]
**Current Allocation**: 1 specialist (default)

🚨 **CHALLENGE**: "Should this dimension get MORE than 1 specialist?"

**Coverage Analysis** (with current 1-specialist allocation):
- **Specialist covers**: [What research areas/sources this specialist will handle]
- **Missing coverage**: [What important areas/sources remain uncovered]
- **Estimated coverage**: [Percentage estimate, e.g., "40%" or "85%"]
- **Risk assessment**: [LOW/MODERATE/HIGH - Is the coverage gap acceptable?]

**Allocation Options**:

**Option A: Keep 1 specialist** (default)
- Coverage: [percentage]
- Cost: 1 agent
- Risk: [risk level] - [Explanation of what might be missed]
- Justification: [When is single specialist sufficient?]

**Option B: Add 1 more specialist** (upgrade to 2)
- **Additional specialist**: [type] covering [specific gaps]
- **Coverage improvement**: [X% → Y%]
- **Cost**: +1 agent (total research count: [N])
- **Risk**: [Reduced risk] - [How second specialist reduces gap]
- **Justification**: [Why second specialist worth the cost]

**Option C: Add 2 more specialists** (upgrade to 3)
- **Additional specialists**:
  - [type1] covering [gaps]
  - [type2] covering [gaps]
- **Coverage improvement**: [X% → 95%+]
- **Cost**: +2 agents (total research count: [N])
- **Risk**: ✅ LOW (comprehensive multi-source coverage)
- **Justification**: [Why CRITICAL dimension needs 3 specialists]

**Decision**: [Option A / B / C]

**Allocation Justification**: [Explicit reasoning for chosen option]

#### Example Resource Allocation Decision

**Dimension 4: Security and Multi-Tenancy Architectures**

**Complexity Score**: 8.5 (COMPLEX)
**Selected Specialist**: academic-researcher
**Current Allocation**: 1

🚨 **CHALLENGE**: "Should this dimension get MORE than 1 specialist?"

**Coverage Analysis**:
- academic-researcher covers: Security research papers, theoretical frameworks, academic studies
- Missing: Current 2025 threat landscape (industry reports, CVEs), Compliance standards (ISO 27001, SOC 2, GDPR)
- Estimated coverage: 40% (academic only, missing 60% of security dimension)
- Risk: 🔴 HIGH - Security is CRITICAL domain, 40% coverage unacceptable

**Option A: Keep 1 specialist**
- Coverage: 40%
- Cost: 1 agent
- Risk: 🔴 HIGH - Major gaps in threat landscape and compliance
- Justification: NOT ACCEPTABLE for security domain

**Option B: Add web-researcher** (2 specialists total)
- Additional: web-researcher covering current 2025 threats, CVE databases, industry security reports
- Coverage: 40% → 70%
- Cost: +1 agent (total 6 for research)
- Risk: ⚠️ MODERATE - Still missing compliance/standards coverage
- Justification: Improvement but still gaps

**Option C: Add web-researcher + search-specialist** (3 specialists total)
- Additional:
  - web-researcher: Current threats, CVEs, industry reports (40% → 70%)
  - search-specialist: ISO 27001, SOC 2, GDPR standards, compliance docs (70% → 95%)
- Coverage: 40% → 95% (comprehensive)
- Cost: +2 agents (total 7 for research)
- Risk: ✅ LOW - Comprehensive coverage across papers, threats, compliance
- Justification: Security is CRITICAL. 95% coverage justifies +2 agents. Meets professional security audit standards.

**Decision**: Option C (3 specialists for this dimension)

**Allocation Justification**: Security domain criticality + 40% baseline coverage gap = REQUIRE comprehensive 3-specialist approach. Cost (+2 agents) justified by risk reduction (HIGH → LOW) and professional coverage standard (95%).

**Dimension 1: Mobile-Native Push Notifications**

**Complexity Score**: 3 (SIMPLE)
**Selected Specialist**: web-researcher
**Current Allocation**: 1

🚨 **CHALLENGE**: "Should this dimension get MORE than 1 specialist?"

**Coverage Analysis**:
- web-researcher covers: Platform docs (iOS/Android), engineering blogs (Shopify, Gojek), official documentation (Apple, Google)
- Missing: Limited academic theory (but not needed for production-focused dimension)
- Estimated coverage: 85%
- Risk: ✅ LOW - Simple dimension, single specialist provides strong coverage

**Option A: Keep 1 specialist**
- Coverage: 85%
- Cost: 1 agent
- Risk: ✅ LOW - Minor academic gap not relevant to production focus
- Justification: Simple dimension, 85% coverage sufficient

**Decision**: Option A (1 specialist)

**Allocation Justification**: Simple dimension (score 3) with production focus. web-researcher provides 85% coverage. Academic gap irrelevant. Single specialist efficient and sufficient.

**Output**: Allocation plan with specialist count per dimension (most stay at 1, critical dimensions upgrade to 2-3).

### Phase 3d: Budget Optimization & Final Verification

**After all allocation decisions complete, perform final budget validation and repetition challenge**:

#### Budget Summary

**Total Research Allocation**:
- Dimension 1: [X] specialist(s) - [types]
- Dimension 2: [X] specialist(s) - [types]
- Dimension 3: [X] specialist(s) - [types]
- Dimension 4: [X] specialist(s) - [types]
- Dimension 5: [X] specialist(s) - [types]
- ...
- **Total Specialists**: [count]
- **Fact-Checkers**: [count] (1 per critical dimension)
- **Grand Total**: [count] agents

#### Budget Status

**Target Range**: 5-7 agents (optimal for novel domain depth)
**Maximum**: 10 agents (cost ceiling)

**Status**:
- ✅ **Within Target** (5-7): Optimal allocation for novel domain research
- ⚠️ **Above Target** (8-10): Justification required - explain why complexity necessitates additional agents
- 🔴 **Overrun** (>10): MUST optimize or provide exceptional justification

#### Repetition Challenge (Quality Gate for Lazy Defaults)

🚨 **CHALLENGE**: "Did I default to [specialist] out of laziness rather than intentional strategy?"

**If ANY specialist type used MORE than 1 time, re-examine EACH usage**:

**Specialist Type**: [type used multiple times, e.g., "web-researcher"]
**Used For**: Dimension [A], Dimension [B], Dimension [C]

**For EACH Dimension**:

**Dimension [A]: [Dimension Name]**
- **Why this specialist?**: [Original rationale from Phase 3b]
- **🚨 Repetition Challenge**: "Did I choose web-researcher because it's GENUINELY optimal, or because I already chose it for Dimension B and defaulted to familiarity?"
- **Fresh Comparison**:
  - web-researcher provides: [specific value for THIS dimension]
  - Alternative ([other specialist]) would provide: [what alternative offers]
  - Net assessment: Which BETTER matches Dimension A's PRIMARY requirements?
- **Verdict**:
  - ✅ **REPETITION JUSTIFIED**: [Why web-researcher genuinely optimal for THIS specific dimension, independent of other dimensions]
  - ❌ **LAZY DEFAULT DETECTED**: Switch to [alternative] - [Why alternative actually better match]

**Example Repetition Challenge**:

**Specialist Type**: web-researcher
**Used For**: Dimension 1 (Push Notifications), Dimension 3 (Infrastructure), Dimension 5 (Coordination)

**Dimension 1: Push Notifications**
- Why web-researcher: Platform docs (iOS/Android), engineering blogs (Shopify, Gojek)
- 🚨 Challenge: "Genuine or lazy default?"
- Fresh comparison: web-researcher (platform docs) vs academic-researcher (push theory)
- Net: Platform docs > theory for production focus
- Verdict: ✅ JUSTIFIED - Production implementation focus requires platform docs

**Dimension 3: Infrastructure**
- Why web-researcher: Current cloud providers (AWS, GCP), infrastructure blogs
- 🚨 Challenge: "Genuine or lazy default?"
- Fresh comparison: web-researcher (current providers) vs trend-analyst (emerging infrastructure patterns)
- Net: Query asks "current state", not "2025 trends"
- Verdict: ✅ JUSTIFIED - "Current state" keyword = web-researcher correct

**Dimension 5: Real-Time Coordination**
- Why web-researcher: WebSocket docs, real-time protocols
- 🚨 Challenge: "Genuine or lazy default?"
- Fresh comparison: web-researcher (protocols) vs academic-researcher (coordination algorithms, research papers)
- Net: Query dimension includes "emerging 2025 approaches" → academic papers valuable
- Verdict: ❌ LAZY DEFAULT - Switch to academic-researcher (coordination research papers better match emerging focus)

**Outcome**: Dimension 5 revised from web-researcher → academic-researcher (repetition challenge caught lazy default)

#### Final Diversity Assessment (Not Enforced, But Informative)

**Unique Specialist Types**: [count]
**Total Specialists**: [count]
**Diversity Ratio**: [unique / total]

**Assessment**:
- ✅ **High Diversity** (≥80%): Strong variety, low repetition
- ⚠️ **Moderate Diversity** (50-79%): Some repetition, verify justified
- 🟡 **Low Diversity** (<50%): Significant repetition, ensure NOT lazy defaults

**Note**: Low diversity acceptable IF repetition challenge passed (justified repetition > arbitrary diversity)

#### Budget Overrun Handling (If >10 agents)

**Option 1: Justify Overrun**
- Exceptional research complexity: [Explain why >10 agents necessary]
- Critical domain requirements: [Security, medical, financial justification]
- Cost < value: [Why research value justifies budget overrun]

**Option 2: Optimize Allocation**
- Review dimensions with 3 specialists → Can any drop to 2?
- Consolidate overlapping specialists → Can fact-checker cover verification?
- Reduce total to ≤10 while maintaining coverage

**Decision**: [Option 1 (justify) or Option 2 (optimize)]

**Output**: Final validated allocation plan with budget summary, repetition justification, and diversity assessment.

### Phase 3e: Decision Logging (Traceability)

**After completing Phase 3d, log allocation decisions to project_logs/ for validation and debugging**:

#### Log Files (Both in project_logs/)

**File 1: allocation-decision.json** (Complete decision trace)

```json
{
  "session_id": "[session_id from researchPath]",
  "timestamp": "[ISO 8601 timestamp]",
  "query": "[original user query]",
  "tier": 5,
  "methodology": "TODAS",

  "phase_1_2_analysis": {
    "query_type": "[straightforward/depth-first/breadth-first]",
    "novelty": "[low/moderate/high/very high]",
    "dimensions": [
      {"id": 1, "name": "[name]", "description": "[brief description]"}
    ]
  },

  "phase_3a_complexity": [
    {
      "dimension_id": 1,
      "dimension_name": "[name]",
      "factors": {
        "sub_domains": {"count": 3, "score": 3},
        "criticality": {"level": "HIGH", "score": 2},
        "novelty": {"level": "MODERATE", "score": 0.5},
        "source_diversity": {"types": 3, "score": 3}
      },
      "total_score": 8.5,
      "classification": "COMPLEX",
      "recommendation": "2-3 specialists"
    }
  ],

  "phase_3b_self_challenge": [
    {
      "dimension_id": 1,
      "initial_selection": "academic-researcher",
      "initial_rationale": "[why initially chosen]",
      "challenge": {
        "alternative": "search-specialist",
        "gains": "[what alternative would provide]",
        "cons": "[what alternative would lack]",
        "comparison": "[initial vs alternative]",
        "net_assessment": "[which better matches requirements]",
        "verdict": "SWITCH to BOTH / KEEP [initial] / SWITCH to [alternative]",
        "decision": "[final decision with reasoning]"
      },
      "final_selection": ["type1", "type2"],
      "final_rationale": "[why final selection optimal]"
    }
  ],

  "phase_3c_resource_allocation": [
    {
      "dimension_id": 1,
      "current_allocation": 2,
      "coverage_analysis": {
        "specialist_coverage": {"specialist1": "40%", "specialist2": "30%"},
        "total_coverage": "70%",
        "missing": "[what gaps remain]",
        "risk": "LOW/MODERATE/HIGH"
      },
      "options": {
        "option_a": {"count": 2, "coverage": "70%", "cost": 5, "risk": "MODERATE"},
        "option_b": {"count": 3, "coverage": "95%", "cost": 6, "risk": "LOW"}
      },
      "decision": "option_a/option_b/option_c",
      "final_allocation": 3,
      "specialists": ["type1", "type2", "type3"],
      "justification": "[why this allocation chosen]"
    }
  ],

  "phase_3d_budget_optimization": {
    "budget_summary": {
      "dimension_allocations": {
        "1": {"specialists": 3, "types": ["academic-researcher", "search-specialist", "web-researcher"]},
        "2": {"specialists": 1, "types": ["web-researcher"]}
      },
      "total_specialists": 6,
      "fact_checkers": 1,
      "grand_total": 7
    },
    "budget_status": {
      "target_range": "5-7",
      "maximum": 10,
      "actual": 7,
      "status": "within_target/above_target/overrun"
    },
    "repetition_challenge": {
      "specialist_type": "web-researcher",
      "usage_count": 3,
      "dimensions": [1, 2, 4],
      "validations": [
        {
          "dimension_id": 1,
          "challenge": "Lazy default or genuine need?",
          "fresh_comparison": "[comparison details]",
          "verdict": "JUSTIFIED/LAZY_DEFAULT_DETECTED",
          "rationale": "[justification]"
        }
      ]
    },
    "final_diversity": {
      "unique_types": 4,
      "total_specialists": 6,
      "diversity_ratio": 0.67,
      "assessment": "HIGH/MODERATE/LOW",
      "acceptable": true,
      "reason": "[why acceptable/unacceptable]"
    }
  },

  "final_allocation": {
    "specialists": [
      {"type": "academic-researcher", "dimension": 1, "rationale": "[why chosen for this dimension]"},
      {"type": "web-researcher", "dimension": 2, "rationale": "[why chosen]"}
    ],
    "fact_checkers": [
      {"dimension": 1, "rationale": "[why fact-checker needed]"}
    ]
  },

  "spawned_by": "internet-research-orchestrator",
  "version": "1.0-self-challenge"
}
```

**File 2: allocation-decision-summary.json** (Quick reference)

```json
{
  "session_id": "[session_id from researchPath]",
  "timestamp": "[ISO 8601 timestamp]",
  "query": "[original user query]",
  "tier": 5,
  "methodology": "TODAS",

  "final_allocation": {
    "specialists": [
      {"type": "academic-researcher", "dimension": 1, "rationale": "[brief rationale]"},
      {"type": "search-specialist", "dimension": 1, "rationale": "[brief rationale]"},
      {"type": "web-researcher", "dimension": 1, "rationale": "[brief rationale]"},
      {"type": "web-researcher", "dimension": 2, "rationale": "[brief rationale]"},
      {"type": "academic-researcher", "dimension": 3, "rationale": "[brief rationale]"},
      {"type": "web-researcher", "dimension": 4, "rationale": "[brief rationale]"}
    ],
    "fact_checkers": [
      {"dimension": 1, "rationale": "Security dimension verification"}
    ],
    "total_agents": 7
  },

  "spawned_by": "internet-research-orchestrator"
}
```

#### Implementation Instructions

**When to log**: After Phase 3d completion, BEFORE spawning any agents (Task tool calls)

**Location**: `project_logs/allocation-decisions/[session_folder]/` (session-based organization matching research-sessions pattern)

**Directory structure**:
```
project_logs/allocation-decisions/
└── [session_id]/              # e.g., 17112025_115042_mini_app_notification_test3/
    ├── decision.json          # Full decision trace (19KB)
    └── summary.json           # Quick reference (768B)
```

**Session folder naming**: Use session_id from researchPath (format: `DDMMYYYY_HHMMSS_topic`)

**How to write**:
```python
# Extract session_id from researchPath
# Example: docs/research-sessions/17112025_115042_mini_app_notification_test3/
# → session_id = "17112025_115042_mini_app_notification_test3"

session_folder = f"project_logs/allocation-decisions/{session_id}/"

# MANDATORY: Write BOTH files - failure to write either = CRITICAL ERROR
Write(
  file_path: f"{session_folder}decision.json",
  content: [full JSON with all Phase 3a-3d details]
)

Write(
  file_path: f"{session_folder}summary.json",
  content: [summary JSON with session_id, timestamp, query, tier, methodology, final_allocation, spawned_by]
)

# CHECKPOINT: Verify BOTH files contain valid JSON with current session_id
# decision.json MUST have: phase_3a_complexity, phase_3b_self_challenge, phase_3c_resource_allocation, phase_3d_budget_optimization
# summary.json MUST have: final_allocation.specialists[]
# If incomplete: RETRY - NEVER proceed to Phase 4 without complete decision logs
```

**Benefits**:
- ✅ **No Data Loss**: Each Tier 5 run creates new folder, never overwrites
- ✅ **Traceability**: Session ID links to research outputs in docs/research-sessions/
- ✅ **Validation**: Verify self-challenge ran (check phase_3b_self_challenge for verdict changes)
- ✅ **Debugging**: If test shows web-researcher × 3, check repetition_challenge validations
- ✅ **Historical Analysis**: Compare allocation decisions across multiple runs
- ✅ **Easy Archival**: Move entire session folders to archive
- ✅ **Quality Metrics**: Analyze self-challenge patterns across all sessions

**Example validation queries**:
```bash
# Check latest session's self-challenge verdicts
jq '.phase_3b_self_challenge[] | select(.challenge.verdict | contains("SWITCH"))' \
  project_logs/allocation-decisions/$(ls -t project_logs/allocation-decisions/ | head -1)/decision.json

# Verify repetition challenge ran
jq '.phase_3d_budget_optimization.repetition_challenge.validations' \
  project_logs/allocation-decisions/17112025_115042_mini_app_notification_test3/decision.json

# Quick check: What was final allocation?
jq '.final_allocation.specialists | length' \
  project_logs/allocation-decisions/17112025_115042_mini_app_notification_test3/summary.json

# Compare allocations across sessions
for session in project_logs/allocation-decisions/*/; do
  echo "$(basename $session): $(jq '.final_allocation.total_agents' $session/summary.json) agents"
done
```

**Output**: Session folder with both decision files for test validation, debugging, and historical analysis.

### Phase 4: Methodical Plan Execution

**Execute the plan using adaptive subagent count**:

#### Parallelizable Steps:
1. **Deploy research-subagent instances** using Task tool
   - Provide extremely clear task descriptions
   - Pass researchPath to ALL subagents (if provided to skill)
   - Include tracking parameters (SPAWNED_BY, SESSION_ID, INVOCATION_CONTEXT)
2. **Spawn in parallel**: All Task calls in ONE message (efficiency)
3. **Wait for completion**: Let subagents execute research
4. **Synthesize findings**: Integrate results when complete

#### Non-Parallelizable/Critical Steps:
1. **Reasoning-only tasks**: Perform yourself (calculations, analysis, formatting)
2. **Web research tasks**: Deploy subagent (orchestrator delegates, not executes)
3. **Challenging steps**: Deploy additional subagents for more perspectives
4. **Compare results**: Use ensemble approach and critical reasoning

#### Throughout Execution:
- **Monitor progress**: Continuously check if query being answered
- **Update plan**: Adapt based on findings from subagents
- **Bayesian reasoning**: Update priors based on new information
- **Adjust depth**: If running out of time or diminishing returns, stop spawning and synthesize
- **Tactical optimization**: Efficiency over completeness when appropriate

**Output**: Complete research findings from all subagents ready for synthesis.

## TodoWrite Integration

**Use TodoWrite to track research progress**:

```
Before starting research:
TodoWrite([
  {content: "Analyze query and determine type (Phase 1-2)", status: "in_progress", activeForm: "Analyzing query type"},
  {content: "Assess dimension complexity scores (Phase 3a)", status: "pending", activeForm: "Assessing dimension complexity"},
  {content: "Execute self-challenge phase for specialist selection (Phase 3b)", status: "pending", activeForm: "Executing self-challenge phase"},
  {content: "Determine resource allocation counts per dimension (Phase 3c)", status: "pending", activeForm: "Determining resource allocation"},
  {content: "Perform budget optimization and repetition challenge (Phase 3d)", status: "pending", activeForm: "Performing budget optimization"},
  {content: "Log allocation decisions to project_logs/ (Phase 3e)", status: "pending", activeForm: "Logging allocation decisions"},
  {content: "Spawn specialist agents based on final allocation (Phase 4)", status: "pending", activeForm: "Spawning specialist agents"},
  {content: "Spawn fact-checker for critical dimension verification (Phase 4)", status: "pending", activeForm: "Spawning fact-checker"},
  {content: "Synthesize findings from all specialists (Phase 5)", status: "pending", activeForm": "Synthesizing findings"},
  {content: "Report completion with attribution and novelty assessment (Phase 6)", status: "pending", activeForm": "Reporting completion"}
])

As you progress, mark tasks completed and update status. The new Phase 3a-3e steps ensure quality decisions through:
- Complexity assessment (avoid under/over-allocation)
- Self-challenge (catch suboptimal selections)
- Resource allocation (justify specialist counts)
- Repetition challenge (prevent lazy defaults)
- Decision logging (traceability and validation)
```

**Benefits**:
- User visibility into research progress
- Clear phase tracking
- Helps avoid skipping steps

## Specialist Agent Selection (CRITICAL)

🚨 **DO NOT use `research-subagent`** - This is a generic worker type lacking specialized capabilities. You MUST use specialist agents based on research needs.

**Available Specialist Agents**:

| Agent Type | Use When | Specialized Capabilities |
|------------|----------|--------------------------|
| **web-researcher** | General web queries, current information, broad topics | WebSearch, WebFetch, comprehensive web coverage |
| **academic-researcher** | Scholarly papers, research publications, scientific topics | Academic databases, peer-reviewed sources, citations |
| **search-specialist** | Complex queries, deep investigation, hard-to-find info | Boolean operators, advanced search techniques, deep web |
| **trend-analyst** | Future forecasting, emerging trends, predictions | Weak signal detection, scenario planning, trend analysis |
| **market-researcher** | Market sizing, segmentation, business intelligence | TAM/SAM/SOM analysis, consumer insights, market data |
| **competitive-analyst** | Competitor analysis, SWOT, strategic intelligence | Competitive profiling, positioning, industry dynamics |
| **synthesis-researcher** | Combine findings from multiple sources, meta-analysis | Pattern identification, cross-source integration, synthesis |
| **fact-checker** | Verify claims, validate sources, check accuracy | Source credibility assessment, claim verification, validation |

**Selection Strategy**:
- **Novel/emerging topics**: web-researcher + trend-analyst
- **Academic/research topics**: academic-researcher + search-specialist
- **Market/business topics**: market-researcher + competitive-analyst
- **Security/compliance**: academic-researcher + fact-checker (MANDATORY)
- **Multi-source synthesis**: synthesis-researcher + fact-checker

**Agent Registry Location**: `.claude/agents/` directory contains all specialist agent definitions.

## Subagent Count Guidelines (Adaptive)

**TODAS adjusts agent count based on complexity**:

| Query Complexity | Subagent Count | Example |
|------------------|----------------|---------|
| **Straightforward** | 1 specialist | "What is tax deadline this year?" → 1 web-researcher |
| **Standard** | 2-3 specialists | "Compare top 3 cloud providers" → 3 web-researchers (one per provider) |
| **Medium** | 3-5 specialists | "Analyze AI impact on healthcare" → 4 agents (academic-researcher, market-researcher, trend-analyst, web-researcher) |
| **High** | 5-7 specialists | "Fortune 500 CEOs birthplaces/ages" → 7 web-researchers in wave 1, then 7 more (sequential batching) |

**Claude Code parallel limit**: Maximum 10 parallel tasks, cap at 7 for safety (hooks overhead).

**For queries requiring >7 agents**: Use sequential batching:
1. Spawn 7 specialist agents in parallel
2. Wait for completion
3. Spawn next 7 specialist agents
4. Repeat until coverage complete

**Principle**: Prefer fewer, more capable specialists over many narrow ones (reduces overhead).

**Minimum**: Always spawn at least 1 specialist agent for ANY research task (orchestrator delegates, not executes).

**Verification Phase**: After specialists complete, spawn fact-checker for critical domains (security, compliance, novel topics).

## Task Tool Spawning Instructions

**How to spawn specialist agent instances**:

### Step 1: Plan Research Dimensions & Select Specialists

Example: "WebRTC + Web3 convergence in 2025" → 3 dimensions:
1. WebRTC current state and 2025 developments → **web-researcher** (current info)
2. Web3 technologies and decentralization trends → **trend-analyst** (emerging tech)
3. Convergence patterns and integration architectures → **academic-researcher** (research patterns)

### Step 2: Call Task Tool for EACH Dimension in ONE Message

🚨 **CRITICAL**: Use SPECIALIST agent types (web-researcher, academic-researcher, etc.), NOT research-subagent

**Correct parallel spawning pattern**:

```
[Call Task tool:]
subagent_type: "web-researcher"  ← USE SPECIALIST TYPE
description: "Research WebRTC 2025 developments"
prompt: "Research WebRTC's current state and 2025 roadmap. Focus on:
- Latest WebRTC implementations (2025 features)
- New codec support and performance improvements
- Browser compatibility and adoption trends

Research Path: docs/research-sessions/{session_id}/
SESSION_ID: {session_id}
SPAWNED_BY: internet-research-orchestrator
INVOCATION_CONTEXT: subagent

Output Requirements:
- Save findings to Research Path above
- File naming: webrtc-2025-research-subagent-001.json
- Follow schema: .claude/skills/research/json-schemas/research-output-schema.json
- Size limit: 22K tokens or 20K characters"

[Call Task tool again in SAME message:]
subagent_type: "trend-analyst"  ← SPECIALIST for emerging tech
description: "Research Web3 decentralization trends"
prompt: "Research Web3 technologies and decentralization in 2025. Focus on:
- Emerging Web3 protocols (2025)
- Decentralized infrastructure architectures
- Real-world adoption and use cases

[Same tracking parameters and output requirements]"

[Call Task tool again in SAME message:]
subagent_type: "academic-researcher"  ← SPECIALIST for patterns/research
description: "Research WebRTC+Web3 convergence patterns"
prompt: "Research integration patterns between WebRTC and Web3. Focus on:
- Decentralized video streaming architectures
- P2P communication with blockchain integration
- Novel use cases emerging in 2025

[Same tracking parameters and output requirements]"
```

**All Task calls in ONE message = parallel execution** (Claude Code optimization).

### Step 3: Spawn Fact-Checker (After Specialists Complete)

**For critical domains** (security, compliance, novel topics), spawn fact-checker:

```
[After specialists complete, call Task tool:]
subagent_type: "fact-checker"
description: "Verify critical claims from research"
prompt: "Verify key claims from WebRTC, Web3, and convergence research. Check:
- Citation accuracy and source credibility
- Conflicting information across sources
- Confidence levels for novel 2025 claims
- Gaps in coverage or missing perspectives

Research Path: docs/research-sessions/{session_id}/
SESSION_ID: {session_id}
SPAWNED_BY: internet-research-orchestrator

Target verification rate: >75% (good), >85% (excellent)"
```

### What NOT to Do

❌ **Using research-subagent** (lacks specialized capabilities):
```
Task(subagent_type="research-subagent", ...)  ← WRONG - use specialist agents
```

❌ **Sequential spawning** (slow):
```
Task(...), wait for completion, then Task(...), wait, then Task(...)
```

❌ **Bash workarounds** (breaks hooks integration):
```
Bash: claude_cli task run research-subagent "$(cat /tmp/task.md)" &
```

❌ **Creating task files and stopping** (NOT spawning):
```
Write task description to .txt file, then don't call Task tool
```

❌ **Skipping fact-checker for critical domains** (security, compliance, novel topics):
```
[Spawn specialists, synthesize, report] ← Missing verification phase
```

### What to ALWAYS Do

✅ **Use SPECIALIST agent types** (web-researcher, academic-researcher, trend-analyst, etc.)
✅ **Use Task tool** (it's available to you)
✅ **Call Task multiple times in ONE message** (parallel spawning)
✅ **Spawn specialists IMMEDIATELY after planning** (efficiency)
✅ **Spawn fact-checker for critical domains** (security, compliance, novel topics)
✅ **Pass researchPath to ALL agents** (when provided to skill)
✅ **Include tracking parameters** (SPAWNED_BY, SESSION_ID, INVOCATION_CONTEXT)

## Delegation Rules (CRITICAL)

**Main Claude delegates ALL research to subagents**:

### Core Orchestration Principles

1. **Orchestrator role**: You coordinate and synthesize, NOT execute primary research
   - Spawn 1-7 research-subagent instances (adaptive based on complexity)
   - Provide each subagent with extremely detailed, specific instructions
   - Let subagents perform all web searches, fact-finding, and information gathering
   - Focus on planning, analyzing, integrating findings, identifying gaps

2. **Verification requirement**: After planning, count how many subagents you plan to spawn
   - If count = 0, revise plan immediately
   - Every query requires AT LEAST 1 research-subagent
   - Your value is orchestration and synthesis, not execution

3. **ResearchPath coordination**: When invoked with researchPath parameter
   - ALL subagents MUST save outputs to SAME researchPath
   - Pass researchPath to EVERY subagent you spawn
   - File coordination is MANDATORY for multi-agent research

### Subagent Task Descriptions

**Provide each subagent with**:
1. **Specific research objective**: Ideally 1 core objective per subagent
2. **Expected output format**: List, report, answer, analysis, etc.
3. **Background context**: How subagent contributes to overall research plan
4. **Key questions**: What to answer as part of research
5. **Starting points and sources**: Define reliable information, list unreliable sources to avoid
6. **Specific tools**: WebSearch, WebFetch for internet information gathering
7. **Scope boundaries**: Prevent research drift (if needed)
8. **Output requirements**: When researchPath provided (see section above)

**Validation**: If all subagents follow instructions well, aggregate results should allow EXCELLENT answer to user query (complete, thorough, detailed, accurate).

### Deployment Strategy

**Priority and dependency**:
- Deploy most important subagents first
- If tasks depend on results from specific task, create that blocking subagent first
- Ensure sufficient coverage for comprehensive research
- All substantial information gathering delegated to subagents

**Avoid overlap**:
- Every subagent should have distinct, clearly separate tasks
- Prevent replicating work unnecessarily
- Avoid wasting resources on redundant research

**Efficiency while waiting**:
- Analyze previous results
- Update research plan
- Reason about user's query and how to best answer it
- Do NOT idle waiting for subagents

## Response Instructions

### Before Providing Final Answer

1. Review most recent facts compiled during research process
2. Reflect deeply: Can these facts answer query sufficiently?
3. Provide final answer in format best for user's query
4. **When invoked with researchPath**: Return summary of research completed and file locations (research skill handles synthesis)
5. **When invoked standalone**: Format final research report in Markdown with proper source attribution

### Source Attribution (Tier 5 Critical)

**For novel/emerging domains, transparency is essential**:

- **Inline references**: "According to [Source Name]", "Research from [Organization] shows..."
- **Sources section**: At end of report, list all key sources consulted
- **Credibility**: Builds trust and allows verification
- **Recency**: Note publication dates (critical for 2025+ topics)

### Novelty Assessment

**Include in synthesis**:
- **Novelty level**: Is this truly emerging? Post-training? Unprecedented?
- **Confidence**: How much information available? (Emerging topics = less data)
- **Gaps**: What's unknown? What requires future research?
- **Verification challenges**: Difficult to verify emerging claims (note limitations)

## Examples

### Example 1: Straightforward Novel Query (1 Subagent)

**User query**: "What is Claude Sonnet 4.5 and when was it released?"

**Main Claude reasoning**:
- Query type: Straightforward (single focused investigation)
- Novelty: High (Sonnet 4.5 released post-training)
- Subagent count: 1 (simple lookup)

**TodoWrite tracking**:
```
[
  {content: "Determine query type: Straightforward", status: "completed"},
  {content: "Spawn 1 research-subagent for Sonnet 4.5 info", status: "in_progress"},
  {content: "Synthesize findings and report", status: "pending"}
]
```

**Task tool call**:
```
Task(
  subagent_type: "research-subagent",
  description: "Research Claude Sonnet 4.5 release",
  prompt: "Research Claude Sonnet 4.5 model. Find:
  - Official release date
  - Model capabilities and improvements
  - Comparison to previous Sonnet versions
  - Anthropic's official announcements

  Sources: Prioritize Anthropic official site, reputable tech news

  SESSION_ID: {session_id}
  SPAWNED_BY: internet-research-orchestrator"
)
```

**Synthesis**: After subagent returns, Main Claude synthesizes findings with source attribution and reports completion.

### Example 2: Depth-First Novel Query (3-5 Subagents)

**User query**: "Analyze multimodal AI agent frameworks emerging in 2025 - what are the leading approaches and their trade-offs?"

**Main Claude reasoning**:
- Query type: Depth-first (multiple perspectives on same issue)
- Novelty: Very high (2025 developments, post-training)
- Subagent count: 4 (different approaches/perspectives)

**Research plan**:
1. Subagent 1: Tool-augmented agents (AutoGPT, LangChain evolution)
2. Subagent 2: Reasoning-first agents (Chain-of-Thought, ReAct patterns)
3. Subagent 3: Vision-language agents (GPT-4V descendants, Gemini Ultra)
4. Subagent 4: Code-execution agents (Code Interpreter evolution)

**TodoWrite tracking**:
```
[
  {content: "Determine query type: Depth-first", status: "completed"},
  {content: "Develop 4-perspective research plan", status: "completed"},
  {content: "Spawn 4 research-subagents in parallel", status: "in_progress"},
  {content: "Synthesize findings with trade-off analysis", status: "pending"}
]
```

**Task tool calls** (all in ONE message for parallel execution):
```
Task(subagent_type: "research-subagent", description: "Research tool-augmented agents", prompt: "[Detailed instructions for tool-augmented approach research]")
Task(subagent_type: "research-subagent", description: "Research reasoning-first agents", prompt: "[Detailed instructions for reasoning patterns research]")
Task(subagent_type: "research-subagent", description: "Research vision-language agents", prompt: "[Detailed instructions for multimodal capabilities research]")
Task(subagent_type: "research-subagent", description: "Research code-execution agents", prompt: "[Detailed instructions for code generation research]")
```

**Synthesis**: After all 4 subagents return, Main Claude integrates findings, identifies trade-offs across approaches, assesses novelty and emerging trends, provides source-attributed analysis.

### Example 3: Breadth-First Novel Query (5-7 Subagents)

**User query**: "Compare the top 5 decentralized video streaming platforms in 2025 across performance, cost, adoption, and technology stack."

**Main Claude reasoning**:
- Query type: Breadth-first (5 independent platform researches)
- Novelty: High (2025 platforms, emerging Web3 space)
- Subagent count: 5 (one per platform)

**Research plan**:
1. Identify top 5 decentralized video platforms (preliminary research)
2. For each platform, research: performance, cost, adoption, tech stack
3. Spawn 5 parallel subagents (one per platform)
4. Aggregate findings into comparison table

**TodoWrite tracking**:
```
[
  {content: "Identify top 5 decentralized video platforms", status: "completed"},
  {content: "Spawn 5 research-subagents (one per platform)", status: "in_progress"},
  {content: "Aggregate findings into comparison analysis", status: "pending"}
]
```

**Task tool calls** (all in ONE message):
```
Task(subagent_type: "research-subagent", description: "Research Platform A", prompt: "[Detailed instructions for Platform A across 4 dimensions]")
Task(subagent_type: "research-subagent", description: "Research Platform B", prompt: "[...]")
Task(subagent_type: "research-subagent", description: "Research Platform C", prompt: "[...]")
Task(subagent_type: "research-subagent", description: "Research Platform D", prompt: "[...]")
Task(subagent_type: "research-subagent", description: "Research Platform E", prompt: "[...]")
```

**Synthesis**: After all 5 subagents return, Main Claude creates comparison table, identifies patterns across platforms, assesses maturity and adoption trends, provides source-attributed recommendations.

### Example 4: Multi-Dimensional Query with Self-Challenge & Resource Allocation (5-7 Specialists)

**User query**: "Research emerging approaches for secure push notifications in multi-tenant mini-app platforms for 2025, covering security architecture, infrastructure scalability, real-time coordination, and mobile-native implementations."

**Phase 1-2: Query Analysis & Dimension Breakdown**

**Query type**: Breadth-first (4 distinct dimensions)
**Novelty**: Very high (2025 emerging approaches, post-training)
**Dimensions identified**:
1. Security architecture (multi-tenant isolation, encryption)
2. Infrastructure scalability (cloud, edge, hybrid)
3. Real-time coordination (WebSocket, MQTT, emerging protocols)
4. Mobile-native implementations (iOS/Android push mechanisms)

**Phase 3a: Dimension Complexity Assessment**

**Dimension 1: Security Architecture**
- Sub-domains: 3 (isolation, encryption, compliance) → +3
- Criticality: HIGH (security domain) → +2
- Novelty: MODERATE (2025 approaches) → +0.5
- Source diversity: 3 types (papers, standards, blogs) → +3
- **Complexity Score**: 8.5 (COMPLEX)

**Dimension 2: Infrastructure Scalability**
- Sub-domains: 2 (cloud, edge) → +2
- Criticality: MODERATE → +1
- Novelty: MODERATE → +0.5
- Source diversity: 2 types (vendor docs, case studies) → +2
- **Complexity Score**: 5.5 (MODERATE)

**Dimension 3: Real-Time Coordination**
- Sub-domains: 2 (protocols, patterns) → +2
- Criticality: MODERATE → +1
- Novelty: HIGH (emerging 2025 protocols) → +1
- Source diversity: 2 types (research, blogs) → +2
- **Complexity Score**: 6 (MODERATE)

**Dimension 4: Mobile-Native Implementations**
- Sub-domains: 1 (push APIs) → +1
- Criticality: LOW → +0
- Novelty: LOW (established APIs) → +0
- Source diversity: 1 type (platform docs) → +2
- **Complexity Score**: 3 (SIMPLE)

**Phase 3b: Self-Challenge Phase (Specialist Selection)**

**Dimension 1: Security Architecture (score 8.5 = COMPLEX)**

**Initial Selection**: academic-researcher
- Rationale: Security research papers, theoretical frameworks, cryptography studies

🚨 **CHALLENGE**: "Wait, why didn't I choose search-specialist instead?"

**Alternative: search-specialist**
- **Gains if chosen**: Deep investigation, compliance standards (ISO 27001, SOC 2), hard-to-find threat reports
- **Cons if chosen**: Less academic rigor, may miss theoretical security frameworks
- **Comparison**: academic-researcher (theory + papers) vs search-specialist (standards + compliance)
- **Net assessment**: Dimension needs BOTH theory AND compliance
- **Verdict**: ❌ SWITCH to BOTH → Upgrade to 2 specialists (academic-researcher + search-specialist)

**Dimension 2: Infrastructure Scalability (score 5.5 = MODERATE)**

**Initial Selection**: web-researcher
- Rationale: Cloud provider docs (AWS, GCP, Azure), infrastructure engineering blogs

🚨 **CHALLENGE**: "Wait, why didn't I choose market-researcher instead?"

**Alternative: market-researcher**
- **Gains**: Market sizing, vendor comparisons, adoption trends
- **Cons**: Less technical depth, focus on business metrics vs technical scalability
- **Comparison**: web-researcher (technical docs) vs market-researcher (business analysis)
- **Net**: Query asks "scalability approaches" (technical), not "market landscape" (business)
- **Verdict**: ✅ KEEP web-researcher (technical focus matches dimension requirements)

**Dimension 3: Real-Time Coordination (score 6 = MODERATE)**

**Initial Selection**: web-researcher
- Rationale: WebSocket docs, MQTT protocols, real-time coordination blogs

🚨 **CHALLENGE**: "Wait, why didn't I choose academic-researcher instead?"

**Alternative: academic-researcher**
- **Gains**: Coordination algorithms, distributed systems research papers, emerging 2025 academic protocols
- **Cons**: Less practical implementation guidance
- **Comparison**: web-researcher (protocols + docs) vs academic-researcher (algorithms + research)
- **Net**: Dimension includes "emerging 2025 approaches" → academic research valuable
- **Verdict**: ❌ SWITCH to academic-researcher (self-challenge caught "emerging 2025" keyword mismatch)

**Dimension 4: Mobile-Native (score 3 = SIMPLE)**

**Initial Selection**: web-researcher
- Rationale: Apple/Google platform docs, push notification guides
- **Verdict**: ✅ KEEP (simple dimension, platform docs sufficient)

**Phase 3c: Resource Allocation Challenge**

**Dimension 1: Security Architecture (COMPLEX, score 8.5)**

**Current Allocation**: 1 specialist (academic-researcher → revised to academic-researcher + search-specialist in Phase 3b)

🚨 **CHALLENGE**: "Should this dimension get MORE than 2 specialists?"

**Coverage Analysis** (with 2 specialists):
- academic-researcher: Security theory, cryptography papers (40%)
- search-specialist: Compliance standards, threat landscape (30%)
- **Total Coverage**: 70%
- **Missing**: Current 2025 threat intelligence, industry security reports (30%)
- **Risk**: ⚠️ MODERATE - Security domain, 70% may be insufficient

**Option C: Add web-researcher** (3 specialists total)
- Additional: web-researcher covering 2025 CVEs, industry security blogs, vendor security docs
- Coverage: 70% → 95%
- Cost: +1 agent (total 6)
- Risk: ✅ LOW
- **Decision**: ✅ UPGRADE to 3 specialists (security criticality justifies comprehensive coverage)

**Dimension 2, 3, 4**: All remain at 1 specialist (coverage >80%, moderate/simple complexity)

**Phase 3d: Budget Optimization & Final Verification**

**Budget Summary**:
- Dimension 1 (Security): 3 specialists (academic-researcher, search-specialist, web-researcher)
- Dimension 2 (Infrastructure): 1 specialist (web-researcher)
- Dimension 3 (Real-Time): 1 specialist (academic-researcher)
- Dimension 4 (Mobile-Native): 1 specialist (web-researcher)
- **Total Specialists**: 6
- **Fact-Checkers**: 1 (for security dimension verification)
- **Grand Total**: 7 agents

**Budget Status**: ⚠️ **Within Max** (7 agents, target 5-7) ✅

**Repetition Challenge**:

**Specialist Type**: web-researcher (used 3 times)
**Used For**: Dimension 1 (Security - 3rd specialist), Dimension 2 (Infrastructure), Dimension 4 (Mobile-Native)

**Dimension 1 Security - web-researcher (3rd specialist)**:
- 🚨 Challenge: "Lazy default or genuine need?"
- Fresh comparison: web-researcher (2025 CVEs, blogs) vs trend-analyst (future threats)
- Net: Query asks "2025 approaches" (current + emerging), not "2026 forecast"
- Verdict: ✅ JUSTIFIED - 2025 current threat intelligence required

**Dimension 2 Infrastructure - web-researcher**:
- 🚨 Challenge: Already using for Dim 1, genuine here?
- Fresh comparison: web-researcher (cloud docs) vs market-researcher (vendor comparison)
- Net: Technical scalability > vendor comparison
- Verdict: ✅ JUSTIFIED - Technical dimension match

**Dimension 4 Mobile-Native - web-researcher**:
- 🚨 Challenge: Third usage, lazy default?
- Fresh comparison: web-researcher (platform docs) vs academic-researcher (push theory)
- Net: Production implementation focus
- Verdict: ✅ JUSTIFIED - Platform docs optimal for mobile-native

**Final Diversity**: 4 unique types / 6 specialists = 67% (MODERATE) ✅ Acceptable (all repetitions justified)

**Phase 3e: Decision Logging**

Before spawning agents, log decisions to `project_logs/`:

**allocation-decision.json** (full trace):
```json
{
  "session_id": "17112025_112316_mini_app_notification",
  "timestamp": "2025-11-17T11:23:16Z",
  "query": "Research emerging approaches for secure push notifications in multi-tenant mini-app platforms for 2025...",
  "tier": 5,
  "methodology": "TODAS",
  "phase_3a_complexity": [
    {"dimension_id": 1, "dimension_name": "Security Architecture", "total_score": 8.5, "classification": "COMPLEX"},
    {"dimension_id": 2, "dimension_name": "Infrastructure Scalability", "total_score": 5.5, "classification": "MODERATE"},
    {"dimension_id": 3, "dimension_name": "Real-Time Coordination", "total_score": 6, "classification": "MODERATE"},
    {"dimension_id": 4, "dimension_name": "Mobile-Native Implementations", "total_score": 3, "classification": "SIMPLE"}
  ],
  "phase_3b_self_challenge": [
    {"dimension_id": 3, "initial_selection": "web-researcher", "challenge": {"verdict": "SWITCH to academic-researcher"}, "final_selection": ["academic-researcher"]}
  ],
  "phase_3c_resource_allocation": [
    {"dimension_id": 1, "final_allocation": 3, "specialists": ["academic-researcher", "search-specialist", "web-researcher"]}
  ],
  "phase_3d_budget_optimization": {
    "budget_summary": {"total_specialists": 6, "fact_checkers": 1, "grand_total": 7},
    "repetition_challenge": {"specialist_type": "web-researcher", "usage_count": 3, "all_justified": true}
  },
  "spawned_by": "internet-research-orchestrator"
}
```

**allocation-decision-summary.json** (quick reference):
```json
{
  "session_id": "17112025_112316_mini_app_notification",
  "timestamp": "2025-11-17T11:23:16Z",
  "query": "Research emerging approaches for secure push notifications...",
  "tier": 5,
  "methodology": "TODAS",
  "final_allocation": {
    "specialists": [
      {"type": "academic-researcher", "dimension": 1, "rationale": "Security theory, cryptography papers"},
      {"type": "search-specialist", "dimension": 1, "rationale": "Compliance standards"},
      {"type": "web-researcher", "dimension": 1, "rationale": "2025 threat intelligence"},
      {"type": "web-researcher", "dimension": 2, "rationale": "Cloud infrastructure docs"},
      {"type": "academic-researcher", "dimension": 3, "rationale": "Emerging 2025 coordination algorithms"},
      {"type": "web-researcher", "dimension": 4, "rationale": "Mobile platform documentation"}
    ],
    "fact_checkers": [{"dimension": 1, "rationale": "Security verification"}],
    "total_agents": 7
  },
  "spawned_by": "internet-research-orchestrator"
}
```

**TodoWrite tracking**:
```
[
  {content: "Analyze query and determine type (Phase 1-2)", status: "completed"},
  {content: "Assess dimension complexity scores (Phase 3a)", status: "completed"},
  {content: "Execute self-challenge phase for specialist selection (Phase 3b)", status: "completed"},
  {content: "Determine resource allocation counts per dimension (Phase 3c)", status: "completed"},
  {content: "Perform budget optimization and repetition challenge (Phase 3d)", status: "completed"},
  {content: "Log allocation decisions to project_logs/ (Phase 3e)", status: "completed"},
  {content: "Spawn 6 specialist agents based on final allocation (Phase 4)", status: "in_progress"},
  {content: "Spawn 1 fact-checker for security verification (Phase 4)", status: "pending"},
  {content: "Synthesize findings from all 7 agents (Phase 5)", status: "pending"}
]
```

**Task tool calls** (Phase 4 - all in ONE message for parallel execution):
```
Task(subagent_type: "academic-researcher", description: "Research security architecture theory", prompt: "[Security papers, cryptography, isolation frameworks]")
Task(subagent_type: "search-specialist", description: "Research security compliance standards", prompt: "[ISO 27001, SOC 2, GDPR for multi-tenant]")
Task(subagent_type: "web-researcher", description: "Research 2025 security threat intelligence", prompt: "[CVEs, security blogs, vendor advisories]")
Task(subagent_type: "web-researcher", description: "Research infrastructure scalability", prompt: "[Cloud providers, edge computing, hybrid architectures]")
Task(subagent_type: "academic-researcher", description: "Research real-time coordination algorithms", prompt: "[Emerging 2025 protocols, distributed coordination papers]")
Task(subagent_type: "web-researcher", description: "Research mobile-native push implementations", prompt: "[iOS APNs, Android FCM, platform best practices]")
Task(subagent_type: "fact-checker", description: "Verify security dimension claims", prompt: "[Validate Dimension 1 findings for accuracy]")
```

**Key Decisions Demonstrated**:
- ✅ Self-challenge caught suboptimal selection (Dimension 3: web-researcher → academic-researcher)
- ✅ Resource allocation upgraded critical dimension (Dimension 1: 1 → 3 specialists)
- ✅ Repetition challenge validated all web-researcher × 3 usage (not lazy defaults)
- ✅ Budget within target (7 agents, justified by security criticality)
- ✅ Final allocation: 6 specialists + 1 fact-checker = comprehensive multi-dimensional coverage

## Key Differences from Other Tiers

**Tier 5 (TODAS) vs Tier 4 (RBMAS)**:
- **Adaptive agent count**: 1-7 (vs fixed 3-7)
- **Tactical optimization**: Stop at diminishing returns (vs complete phases)
- **Novel domain focus**: Post-training, emerging (vs established domains)
- **Query type classification**: Depth/Breadth/Straightforward (vs dimension counting)
- **Synthesis approach**: Novelty assessment, uncertainty quantification (vs cross-dimensional patterns)

**Tier 5 (TODAS) vs Tier 3 (Light Parallel)**:
- **Complexity**: Novel/emerging domains (vs standard 2-4 dimensions)
- **Agent range**: 1-7 adaptive (vs 2-4 fixed)
- **Methodology**: TODAS 4-phase (vs simple parallel coordination)
- **Synthesis**: Novelty assessment (vs aggregation)

**When to use Tier 5 vs others**:
- ✅ Tier 5: Novel domains, post-training data, emerging tech, unprecedented topics
- ✅ Tier 4: Established domains, comprehensive multi-dimensional research (4+ dimensions)
- ✅ Tier 3: Standard research, 2-4 dimensions, known patterns
- ✅ Tier 1-2: Simple lookups, specialist queries

---

**Skill Type**: Research Orchestration (Tier 5 - Novel Domains)
**Methodology**: TODAS (Tactical Optimization & Depth-Adaptive System)
**Agent Range**: 1-7 subagents (adaptive based on complexity)
**Specialization**: Novel/emerging domains, post-training information, unprecedented topics
**Created**: Phase 4 of agent-to-skill migration
**Version**: 1.0
