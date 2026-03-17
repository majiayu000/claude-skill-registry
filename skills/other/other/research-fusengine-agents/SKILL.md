---
name: research
description: Technical research methodology using Context7, Exa, and Sequential Thinking for documentation, best practices, and complex investigations.
argument-hint: "[topic] [--deep]"
context: fork
agent: fuse-ai-pilot:research-expert
user-invocable: false
---

**Session:** ${CLAUDE_SESSION_ID}

**Research Topic:** $ARGUMENTS

# Research Skill

## Research Workflows

### Standard Query
```
1. THINK → Sequential Thinking decomposition
2. RESOLVE → Context7 resolve-library-id
3. DOCUMENT → Context7 query-docs (5000-10000 tokens)
4. SUPPLEMENT → Exa code context search
5. SYNTHESIZE → Structured answer with sources
```

### Complex Investigation
```
1. DEEP THINK → Multi-hypothesis Sequential Thinking
2. DEEP RESEARCH → Exa deep researcher (45s-2min)
3. MONITOR → Check status until completed
4. VALIDATE → Cross-check Context7 official sources
5. REPORT → Comprehensive solution
```

### Technology Trends
```
1. WEB SCAN → Exa search latest developments
2. CODE PATTERNS → Exa code context for practices
3. ECOSYSTEM → Company research for key players
4. ANALYSIS → Sequential Thinking for implications
5. RECOMMENDATIONS → Actionable insights
```

## Context7 Usage

```typescript
// Step 1: Resolve library ID
mcp__context7__resolve-library-id({
  libraryName: "next.js",
  query: "App Router server actions"
})

// Step 2: Query docs
mcp__context7__query-docs({
  libraryId: "/vercel/next.js",
  query: "server actions authentication"
})
```

**Best Practices**:
- Always `resolve-library-id` BEFORE `query-docs`
- Specify `topic` parameter to focus retrieval
- Start with 5000 tokens, increase to 10000 if needed
- Handle variations: "nextjs" vs "/vercel/next.js"

## Exa Search Types

| Type | Use Case | Time | numResults |
|------|----------|------|------------|
| `fast` | Quick lookups | <5s | 3-5 |
| `auto` | Balanced | 5-15s | 5-8 |
| `deep` | Comprehensive | 15-45s | 8+ |

```typescript
// Code context search
mcp__exa__get_code_context_exa({
  query: "Next.js 16 server actions authentication",
  tokensNum: 5000
})

// Web search
mcp__exa__web_search_exa({
  query: "React 2025 best practices",
  type: "auto",
  numResults: 5
})
```

## Exa Deep Research

**Reserve for** investigations requiring >30min manual effort.

```typescript
// Start research
const { taskId } = await mcp__exa__deep_researcher_start({
  instructions: "Compare authentication solutions for Node.js",
  model: "exa-research-pro" // or "exa-research" for faster
})

// Poll until complete
mcp__exa__deep_researcher_check({ taskId })
```

**Models**:
- `exa-research`: Standard depth (15-45s)
- `exa-research-pro`: Complex topics (45s-2min)

## Sequential Thinking

```typescript
mcp__sequential-thinking__sequentialthinking({
  thought: "Analyzing authentication approaches",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true,
  // Optional for revisions:
  isRevision: false,
  revisesThought: null,
  branchId: null,
  branchFromThought: null,
  needsMoreThoughts: false
})
```

**Best Practices**:
- Start with realistic `totalThoughts`, adjust dynamically
- Use `isRevision: true` to reconsider hypotheses
- Create branches (`branchId`) for alternatives
- Set `needsMoreThoughts: true` if incomplete

## Multi-Source Synthesis

**Parallelization**:
- Run `resolve-library-id` + `web_search_exa` simultaneously
- Launch multiple Exa searches concurrently
- Execute Context7 docs + Exa code search in parallel

**Source Priority**:
1. Official documentation (Context7)
2. Recent tutorials (Exa, <6 months)
3. Older content (with version verification)

## Response Format

```markdown
## 🔍 Research: [Topic]

### Methodology
- Sequential Thinking: [N thoughts, M revisions]
- Context7: [Library@version consulted]
- Exa: [Search types performed]

### Key Findings
1. **[Finding 1]** (Source: [URL])
   - Technical details
   - Code examples

2. **[Finding 2]** (Source: [URL])

### Recommendations
- [Action 1]: [Why + How]
- [Action 2]: [Why + How]

### Sources
- Context7: [Exact library IDs]
- Exa: [X results analyzed]
- Deep Research: [Task ID if used]
```

## Error Handling

**Context7 Failures**:
- Verify library name spelling
- Try different formats ("/org/project" vs "project-name")
- Fallback to Exa code context

**Exa Timeouts**:
- Reduce `numResults`
- Simplify query
- Switch `type: "deep"` → `type: "fast"`

**Sequential Thinking Blocks**:
- Revise with `isRevision: true`
- Increase `totalThoughts`
- Create new branch

## Forbidden Behaviors

- ❌ Guess library IDs without `resolve-library-id`
- ❌ Start deep researcher without checking completion
- ❌ Mix opinions with facts without distinction
- ❌ Provide code without version verification
- ❌ Ignore WebFetch redirects
- ❌ Recommend without citing sources
- ❌ Skip Sequential Thinking for multi-step problems
