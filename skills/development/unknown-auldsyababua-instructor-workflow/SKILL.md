---
name: multi-agent-research
description: Apply Anthropic's production multi-agent research patterns for complex research tasks. Use when research involves multiple independent dimensions, requires synthesis across many sources, or needs parallelization for speed. Includes query complexity assessment, parallel execution, progressive search refinement, thinking strategies, and findings compression.
---

# Multi-Agent Research

Production patterns from Anthropic's research system for conducting complex, multi-faceted research efficiently.

**Source**: [How we built our multi-agent research system](https://www.anthropic.com/research/building-effective-agents)

## When to Use

Use multi-agent-research patterns when:
- Research has 3+ independent dimensions to explore
- Comparing multiple alternatives simultaneously
- Need to synthesize information from 10+ sources
- Time-sensitive research requiring parallelization
- Complex technical landscape with unclear paths
- Breadth-first exploration needed

**Don't use for**:
- Simple fact-finding (1-2 sources)
- Single-dimension queries
- When sequential research is sufficient

## Core Principles

### 1. Scale Effort to Query Complexity

Assess complexity BEFORE starting research to allocate appropriate resources.

#### Simple Fact-Finding (3-10 tool calls)
- Single specific question with clear answer
- 1-2 authoritative sources needed
- Examples: Version number lookup, API syntax check, single DocType field validation

**Approach**: Direct search → validate → document

```typescript
// Example: Check ERPNext Task field
mcp__ref__ref_search_documentation({
  query: "ERPNext Task DocType fields"
})
// Review results → Document finding with citation
```

#### Direct Comparison (10-15 tool calls)
- Compare 2-3 specific alternatives
- Field mapping between systems
- Feature parity analysis

**Approach**: Parallel searches for each option → compare → recommend

```typescript
// Example: Compare DocTypes - execute in parallel
mcp__ref__ref_search_documentation({ query: "ERPNext Task DocType" })
mcp__ref__ref_search_documentation({ query: "ERPNext Project Task DocType" })
mcp__ref__ref_search_documentation({ query: "ERPNext ToDo DocType" })
// Compare results → Build comparison table → Recommend
```

#### Complex Multi-Faceted Research (20+ tool calls)
- Architecture decision with multiple unknowns
- Integration across multiple systems
- Novel feature requiring ecosystem research
- Multiple independent research dimensions

**Approach**: Use deep researcher OR spawn parallel focused sub-tasks

```typescript
// Example: Complex research with deep researcher
mcp__exasearch__deep_researcher_start({
  instructions: "Research OpenTelemetry integration for AWS Lambda Node.js. Cover: (1) Lambda layer vs manual instrumentation trade-offs, (2) X-Ray backend compatibility, (3) cold start performance impact, (4) 2025 best practices. Include code examples with versions.",
  model: "exa-research"
})
// Poll for completion, extract findings, add to research doc
```

**Complexity Heuristic**: If research question has 3+ independent dimensions, use parallel or deep researcher approach.

### 2. Parallel Tool Execution

Execute independent searches simultaneously for 90% faster results.

#### When to Parallelize

**Comparing alternatives**:
```typescript
// ❌ DON'T: Sequential searches (slow)
await mcp__ref__ref_search_documentation({ query: "Redis session store" });
// wait...
await mcp__ref__ref_search_documentation({ query: "Memcached session store" });
// wait...

// ✅ DO: Parallel searches (single message, multiple tool calls)
mcp__ref__ref_search_documentation({ query: "Redis session store" })
mcp__ref__ref_search_documentation({ query: "Memcached session store" })
mcp__exasearch__web_search_exa({ query: "Redis vs Memcached 2025 comparison" })
```

**Multi-source validation**:
```typescript
// Execute all simultaneously
mcp__ref__ref_search_documentation({ query: "OpenTelemetry Lambda official docs" })
mcp__exasearch__web_search_exa({ query: "OpenTelemetry Lambda examples 2025" })
mcp__exasearch__web_search_exa({ query: "OpenTelemetry Lambda deprecated OR EOL" })
```

**Independent research dimensions**:
```typescript
// All can run in parallel
mcp__ref__ref_search_documentation({ query: "Stripe API authentication" })
mcp__exasearch__web_search_exa({ query: "Stripe API rate limits" })
mcp__exasearch__web_search_exa({ query: "Stripe webhook best practices 2025" })
```

### 3. Search Strategy: Start Wide, Then Narrow

Progressive refinement prevents missing important context.

#### Anti-Pattern: Overly Specific Initial Queries

```
❌ DON'T START WITH:
"how to implement OpenTelemetry auto-instrumentation for AWS Lambda with X-Ray backend using custom sampling rules in Node.js 18"

Result: Few/no results, miss alternative approaches
```

#### Recommended: Progressive Refinement

```
✅ STEP 1 - Broad Exploration (2-5 results):
"OpenTelemetry AWS Lambda Node.js"
→ Discover: What approaches exist? What's recommended?

✅ STEP 2 - Evaluate Landscape:
Review results, identify main approaches (layer vs manual instrumentation)

✅ STEP 3 - Narrow Focus (3-10 results):
"OpenTelemetry Lambda layer vs manual instrumentation"
→ Compare trade-offs

✅ STEP 4 - Specific Details:
"OpenTelemetry Lambda layer installation guide 2025"
→ Find working examples
```

#### Query Pattern Templates

| Purpose | Pattern | Example |
|---------|---------|---------|
| **Discovery** | `[technology] [use case]` | "GraphQL federation microservices" |
| **Comparison** | `[option A] vs [option B] [criteria]` | "REST vs GraphQL performance" |
| **Implementation** | `[specific approach] [version] guide` | "GraphQL Apollo Federation v2 guide" |
| **Validation** | `[library] deprecated OR EOL OR migration` | "Apollo Federation deprecated" |

### 4. Thinking Process for Research

Use extended and interleaved thinking to plan strategy and evaluate results.

#### Planning Phase (Extended Thinking)

Before tool calls, think through:

```
[Extended thinking example]:

This ERPNext DocType selection question has 3 candidates to evaluate.
I need to research each in parallel:
- Field mappings (official docs)
- Custom field requirements (API specs)
- Community usage patterns (real-world examples)

I'll use ref.tools for official ERPNext docs (3 parallel calls) and
exa for community examples (3 parallel calls).

Total: 6 parallel tool calls for comprehensive coverage.
```

**Planning Checklist**:
1. What are the independent sub-questions?
2. Which tools fit this research?
3. What's the complexity level? (Simple/Comparison/Complex)
4. Which searches can run simultaneously?

#### After Tool Results (Interleaved Thinking)

After each set of results, evaluate:

```
[Interleaved thinking example]:

Results from 6 parallel searches received:

Quality check:
- Official docs: High confidence, current (v14)
- Community examples: Medium confidence, mix of v13/v14

Gap analysis:
- Tasks DocType: 80% field coverage, clear
- Project Tasks: 60% coverage, BUT community prefers for workflow integration
- Missing: Understanding WHY community prefers Project Tasks

Next step: Need one more targeted search on workflow capabilities difference
```

**Evaluation Checklist**:
- ✅ Are sources authoritative? Current? Relevant?
- ✅ What's still missing? What contradicts?
- ✅ Should I go deeper or pivot direction?
- ✅ What's my confidence level? (High/Medium/Low)

### 5. Deep Research Delegation

Know when to delegate to specialized deep research vs direct tool calls.

#### Decision Framework

| Use Direct Research | Use Deep Researcher |
|---------------------|---------------------|
| Query scope clear and bounded | Open-ended exploration needed |
| 2-4 specific sources | Unclear which sources to check |
| Can complete in 10-15 tool calls | Requires 10+ sources |
| **Example**: "Compare Redis vs Memcached for sessions" | **Example**: "Research state of GraphQL federation in 2025 - solutions, trade-offs, migration paths" |

#### Deep Researcher Workflow

**1. Start task with detailed instructions**:

```typescript
mcp__exasearch__deep_researcher_start({
  instructions: `Research OpenTelemetry integration for AWS Lambda Node.js functions.

Focus areas:
1. Lambda layer vs manual instrumentation (trade-offs, pros/cons)
2. X-Ray backend compatibility (setup, configuration)
3. Cold start performance impact (benchmarks, mitigation)
4. Current best practices as of 2025 (official recommendations)

Deliverables:
- Code examples with specific version numbers
- Official documentation links
- Deprecation warnings if any
- Recommended approach with justification`,
  model: "exa-research" // or "exa-research-pro" for very complex
})
// Returns: { taskId: "abc123" }
```

**2. Poll for results** (repeat until status: "completed"):

```typescript
mcp__exasearch__deep_researcher_check({
  taskId: "abc123"
})
// Tool includes 5-second delay before checking
// Keep calling until status: "completed"
```

**3. Extract and integrate findings**:

```markdown
## Findings from Deep Research

**Source**: Deep Researcher Task abc123

### Finding 1: Lambda Layer Recommended
- **Summary**: Official docs recommend layer approach over manual
- **Evidence**: "Layer reduces cold start by 200ms, handles auto-instrumentation"
- **Source**: OpenTelemetry Lambda Docs (High confidence)
- **Code Example**: `layers: ['arn:aws:lambda:...:opentelemetry-nodejs']`

[Additional findings...]
```

### 6. Self-Improvement from Tool Failures

Adapt when tools don't work as expected.

#### Document Failure Patterns

When tool repeatedly fails:

```markdown
TOOL FAILURE PATTERN:
- Tool: mcp__ref__ref_search_documentation
- Query: "ERPNext v14 custom fields"
- Parameters: { query: "ERPNext v14 custom field creation API" }
- Expected: Documentation on custom field APIs
- Actual: No results returned (0 matches)
- Frequency: 5/5 attempts with different phrasings
```

#### Adaptation Strategies

1. **Try alternative tool**:
```typescript
// Primary tool failing, switch to web search
mcp__exasearch__web_search_exa({
  query: "ERPNext v14 custom field creation site:erpnext.com"
})
```

2. **Rephrase query**:
```typescript
// Original: "ERPNext v14 custom fields"
// Rephrased: "ERPNext custom field API" (drop version)
// Rephrased: "Frappe custom field creation" (use framework name)
```

3. **Break into smaller queries**:
```typescript
// Original: "ERPNext v14 custom field creation and validation API"
// Split into:
mcp__ref__ref_search_documentation({ query: "ERPNext custom field creation" })
mcp__ref__ref_search_documentation({ query: "ERPNext field validation" })
```

#### Report to Planning

```markdown
TOOL ISSUE REPORT:

**Tool**: mcp__ref__ref_search_documentation
**Issue**: Consistently returns no results for ERPNext v14 queries, v13 queries work
**Attempted**: 5 different query phrasings
**Workaround**: Using web_search_exa with site:erpnext.com filter, then validating
**Impact**: 30% slower research, but results accurate
**Recommendation**: Tool may need ERPNext v14 docs indexed
```

### 7. Findings Compression Strategy

Compress vast research into actionable context for downstream agents.

#### The Problem

Complex research generates 10+ sources with hundreds of pages. Action Agent needs compressed, decision-critical information only.

#### 4-Element Compression Pattern

For each major finding:

1. **Core claim** (1 sentence)
2. **Evidence** (quote or concrete example)
3. **Source** (URL + confidence level)
4. **Relevance** (why this matters for decision)

#### Anti-Pattern: Copying Entire Docs

```markdown
❌ DON'T:
Found 15-page OpenTelemetry Lambda guide covering:
- History of observability (3 pages)
- Architecture deep-dive (4 pages)
- Deployment options (2 pages)
- Configuration reference (5 pages)
- Troubleshooting (1 page)

[Paste entire guide]
```

#### Better: Extract Decision-Critical Information

```markdown
✅ DO:

**Finding**: OpenTelemetry Lambda layer recommended over manual instrumentation

- **Core Claim**: Layer approach reduces cold start by 200ms vs manual
- **Evidence**: Official guide states "Layer handles auto-instrumentation and reduces cold start overhead through optimized initialization"
- **Source**: [OpenTelemetry Lambda Docs - Deployment Options](https://opentelemetry.io/docs/faas/lambda-nodejs/#deployment) (High confidence - official docs)
- **Code Example**:
  ```typescript
  layers: ['arn:aws:lambda:us-east-1:901920570463:layer:aws-otel-nodejs-ver-1-18-0:1']
  ```
- **Relevance**: Meets performance requirement (<500ms cold start) without custom instrumentation code, reduces maintenance burden

**Alternative Considered**: Manual instrumentation - rejected due to cold start penalty and maintenance overhead
```

#### Compression Checklist

Before handing off findings:

- [ ] Each finding fits in 3-5 sentences
- [ ] Code examples are minimal but working (not full files)
- [ ] Links to docs (don't paste full docs)
- [ ] Clear connection to decision criteria
- [ ] Confidence level explicit (High/Medium/Low)
- [ ] Alternatives considered and rejection rationale

## Integration with Existing Workflows

### For Researcher Agent

Apply these patterns in existing research workflow:

1. **Query Complexity Assessment** → Add before "Search Existing Project Documentation"
2. **Parallel Tool Execution** → Use in "Conduct External Research" phase
3. **Search Strategy** → Apply when formulating search queries
4. **Thinking Process** → Use before tool calls and after results
5. **Deep Researcher** → Option in "Conduct External Research" for complex topics
6. **Tool Failures** → Add to Error Handling section
7. **Findings Compression** → Apply in "Document Findings with Citations"

### Output Format

Maintain existing output structure, enhance with compression:

```markdown
## Key Findings

### Finding 1: [Title]
**Core Claim**: [1 sentence]
**Evidence**: [Quote or concrete example]
**Source**: [URL + confidence]
**Relevance**: [Decision impact]

**Code Example** (if applicable):
```[language]
// Minimal working example
```

[Repeat for 3-5 key findings]
```

## Success Metrics

Applying multi-agent research patterns should result in:

- **Speed**: 90% faster for breadth-first queries (via parallelization)
- **Quality**: Higher confidence findings (progressive refinement)
- **Efficiency**: Right-sized effort (complexity assessment)
- **Completeness**: Better coverage (parallel exploration)
- **Usability**: Actionable findings (compression)

## Examples

### Example 1: Simple Query

**Task**: Check if Redis supports session TTL

**Complexity**: Simple fact-finding
**Approach**: Direct search (3 tool calls)

```typescript
// Single targeted search
mcp__ref__ref_search_documentation({
  query: "Redis TTL expire session keys"
})
// Validate in official docs
// Document finding with citation
```

**Result**: 2 minutes, High confidence

### Example 2: Comparison Query

**Task**: Compare Redis vs Memcached for session storage

**Complexity**: Direct comparison
**Approach**: Parallel searches (10 tool calls)

```typescript
// Execute in parallel (single message)
mcp__ref__ref_search_documentation({ query: "Redis session storage features" })
mcp__ref__ref_search_documentation({ query: "Memcached session storage features" })
mcp__exasearch__web_search_exa({ query: "Redis vs Memcached session store 2025" })
mcp__exasearch__web_search_exa({ query: "Redis session TTL persistence" })
mcp__exasearch__web_search_exa({ query: "Memcached session limitations" })
```

**Result**: 8 minutes, comparison table with pros/cons, High confidence recommendation

### Example 3: Complex Multi-Faceted Query

**Task**: Research GraphQL federation migration from REST API

**Complexity**: Complex (architecture decision, multiple unknowns)
**Approach**: Deep researcher (40+ sources)

```typescript
mcp__exasearch__deep_researcher_start({
  instructions: `Research migrating from REST to GraphQL federation for microservices.

Focus areas:
1. Available federation solutions (Apollo, Mercurius, etc.) - compare features, maturity
2. Migration strategies (big bang vs incremental, REST wrapper patterns)
3. Schema stitching vs federation trade-offs
4. Performance implications (n+1 queries, caching)
5. Client migration (breaking changes, backward compatibility)
6. 2025 best practices and anti-patterns

Deliverables:
- Solution comparison table
- Recommended migration path with phases
- Code examples for federation setup
- Known gotchas and mitigation strategies`,
  model: "exa-research-pro"
})

// Poll until complete
mcp__exasearch__deep_researcher_check({ taskId: "..." })

// Extract findings, compress to key decisions
// Build recommendation with phased approach
```

**Result**: 45 minutes, comprehensive analysis with migration roadmap, Medium-High confidence (validated against official docs)

## Anti-Patterns

### ❌ Starting Too Specific

```
Query: "implement OpenTelemetry auto-instrumentation AWS Lambda X-Ray custom sampling Node 18"
Result: 0 results or miss better approaches
```

**Fix**: Start broad, progressively narrow

### ❌ Sequential When Could Parallelize

```typescript
await search("Redis features");
await search("Memcached features");
await search("comparison");
```

**Fix**: Single message with 3 tool calls

### ❌ Pasting Entire Docs

```
Finding: [15 pages of OpenTelemetry docs copied]
```

**Fix**: Extract 4-element compressed findings

### ❌ Skipping Thinking Steps

```
[Immediately calls 10 tools without planning]
```

**Fix**: Extended thinking to plan, interleaved thinking to evaluate

### ❌ Using Deep Researcher for Simple Queries

```
Task: "What's the latest Redis version?"
Approach: deep_researcher_start (overkill)
```

**Fix**: Simple direct search (1-2 tool calls)

## References

- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Agents cookbook - Prompts](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents/prompts)
- [Linear Issue LAW-76](https://linear.app/10netzero/issue/LAW-76) - Implementation tracking
