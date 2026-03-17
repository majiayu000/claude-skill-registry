---
name: coder-memory-store
description: Store universal coding patterns into vector database. Auto-invokes after difficult tasks with broadly-applicable lessons. Trigger with "--store" or when user expresses frustration (strong learning signals). Uses true two-stage retrieval with MCP server v2.
---

## ⚠️ MANDATORY: Use Task Tool (Sub-Agent)

**NEVER call memory MCP tools directly!** Use Task tool with `subagent_type: "general-purpose"` to keep main context clean.

---

## CRITICAL: When NOT to Store Memory

**Skip storing obvious tasks** - simple commands, basic operations, well-documented patterns, routine fixes.

**Only store hard lessons** - non-obvious bugs, surprising patterns, failures, universal insights, significant struggles.

**Rule**: If it's in docs or Google-able in 30 seconds, skip. Memory is for hard-won lessons.

---

# Embedded Role Configuration

```yaml
# Embedded configuration - no external files needed
role_collections:
  global:
    universal:
      name: "universal-patterns"
      description: "Search here for cross-domain patterns"
      query_hints: ["general", "architecture", "debugging", "performance"]

    backend:
      name: "backend-patterns"
      description: "Backend engineering patterns"
      query_hints: ["api", "database", "auth", "server", "microservices"]

    frontend:
      name: "frontend-patterns"
      description: "Frontend engineering patterns"
      query_hints: ["react", "vue", "component", "ui", "state"]

    quant:
      name: "quant-patterns"
      description: "Quantitative finance patterns"
      query_hints: ["trading", "backtest", "risk", "portfolio"]

    devops:
      name: "devops-patterns"
      description: "DevOps and infrastructure patterns"
      query_hints: ["docker", "kubernetes", "ci-cd", "terraform"]

    ai:
      name: "ai-patterns"
      description: "AI and machine learning patterns"
      query_hints: ["model", "training", "neural", "llm", "embedding"]

    security:
      name: "security-patterns"
      description: "Security engineering patterns"
      query_hints: ["vulnerability", "encryption", "auth", "pentest"]

    mobile:
      name: "mobile-patterns"
      description: "Mobile development patterns"
      query_hints: ["ios", "android", "react-native", "flutter"]

    pm:
      name: "pm-patterns"
      description: "Project management and coordination patterns"
      query_hints: ["coordination", "delegation", "team", "sprint", "planning", "reporting"]

# Role detection from task context
role_detection:
  patterns:
    backend: "api|endpoint|database|server|auth|rest|graphql"
    frontend: "react|vue|component|ui|dom|css|state"
    quant: "trading|backtest|portfolio|risk|market"
    devops: "deploy|docker|kubernetes|ci|cd"
    ai: "model|training|neural|embedding|llm"
    security: "vulnerability|encryption|pentest|jwt"
    mobile: "ios|android|native|flutter|swift"
    pm: "project|coordination|delegation|team|sprint|phase|reporting|stakeholder"

  multi_role_strategy: "search_all"  # When multiple roles detected
  default_role: "universal"          # When no clear role
```
You can create new role if you think it worth it. But be EXTREMELY CONSERVATIVE when creating new roles - when you create a new one, add it in this very doc (~/.claude/skills/coder-memory-recall/SKILL.md and ~/.claude/skills/coder-memory-store/SKILL.md).

## MCP Server Tools

**CRITICAL**: Use tools from the **memory MCP server**:
- `search_memory` - Search and get previews
- `get_memory` - Get full content by ID
- `batch_get_memories` - Get multiple full contents
- `store_memory` - Store new memory
- `update_memory` - Update existing memory
- `delete_memory` - Delete memory
- `list_collections` - List all collections

## PHASE 1: Extract Insights

Analyze conversation for **0-3 insights** (usually 0-1). Be selective.

### Classification

**Episodic**: Concrete debugging/implementation story
Example: "React useEffect dependency array bug caused stale closure"

**Procedural**: Repeatable workflow or process
Example: "Zero-downtime database migration: 1) Create script, 2) Test staging, 3) Run in transaction, 4) Monitor"

**Semantic**: Abstract principle or pattern
Example: "Distributed systems need randomness to avoid synchronization disasters"

### Criteria (ALL must be true)

1. **Non-obvious**: Not well-documented standard practice
   ❌ "Use try-catch for error handling"
   ✅ "useCallback without deps array causes stale closures"

2. **Universal**: Applies beyond specific project/framework
   ❌ "Config for our Jenkins pipeline"
   ✅ "Blue-green deployments reduce downtime risk"

3. **Actionable**: Provides concrete guidance
   ❌ "Performance is important"
   ✅ "Use debouncing (300ms) for autocomplete inputs to reduce API calls"

4. **Valuable**: Would help future similar situations
   ❌ "Fixed typo in variable name"
   ✅ "Binary search debugging: disable half the features to isolate bug source"

### Role Detection

```python
# Scan task context for keywords
context = "Built REST API with JWT authentication and rate limiting"

# Detected keywords: api, rest, authentication, jwt, rate
# → Role: "backend"

# If multiple roles or unclear → "universal"
```

## PHASE 2: Search for Similar (Two-Stage)

### Format Memory First

```
**Title:** API Rate Limiting with Exponential Backoff
**Description:** Exponential backoff with jitter prevents thundering herd.

**Content:** When implementing rate limiting for API calls, simple retry logic caused thundering herd problem. Tried fixed delays but all clients retry simultaneously. Solution: exponential backoff (2^n seconds) with random jitter (±0-30%). This spreads retry attempts preventing server overload. Key lesson: distributed systems need randomness to avoid synchronization.

**Tags:** #backend #api #rate-limiting #success
```

### Stage 1: Search Previews

Use `search_memory` tool (from memory MCP server) with the full formatted memory text as query and correct memory_level (global, project, etc.), default: `memory_level="global"`. Use the full text (not just title) for better semantic matching.

**Why full text as query?** Better semantic matching captures full context.

### Stage 2: Intelligent Preview Analysis

Review previews to decide consolidation action:

**High similarity** → Likely duplicate
→ Retrieve full content for MERGE decision

**Medium similarity** → Possibly related
→ Retrieve full content for UPDATE decision

**Multiple episodic** → Pattern emerges
→ Retrieve all for GENERALIZE decision

**Low similarity** → Different topic
→ CREATE new memory (no retrieval needed)

Use `batch_get_memories` tool (from memory MCP server) with relevant doc_ids and correct memory_level (global, project, etc.), default: `memory_level="global"` to retrieve full content for consolidation candidates.

## PHASE 3: Intelligent Consolidation

### Decision Framework (No Rigid Thresholds)

| Analysis | Signal | Action |
|----------|--------|--------|
| **Near-identical** | Same problem, same solution, same title | **MERGE** - Combine best parts, delete duplicate |
| **Related topic** | Complementary info, overlapping tags | **UPDATE** - Enhance existing with new insights |
| **Pattern emerges** | 2+ episodic show common pattern | **GENERALIZE** - Extract semantic pattern |
| **Different** | Orthogonal concept | **CREATE** - New memory |

## PHASE 4: Store Memory

### Final Storage

Use `store_memory` tool (from memory MCP server) with the final document, metadata, and `memory_level="global"`. Log the result doc_id and action taken.

**CRITICAL - Required metadata fields:**
```json
{
  "memory_type": "episodic|procedural|semantic",
  "role": "backend|frontend|ai|devops|...",
  "title": "Short descriptive title",
  "description": "One-line summary for search previews - REQUIRED!",
  "tags": ["#tag1", "#tag2"],
  "confidence": "high|medium|low",
  "frequency": 1
}
```

**Why `description` is critical:** The `search_memory` tool returns previews with title + description. If description is missing, search results show "No description" making it impossible to identify relevant memories.

### Trigger Words for Strong Learning Signals

When user expresses frustration (trigger words), this is a **critical learning moment**:

**Profanity**: fuck, shit, damn, wtf, ffs
**Frustration**: moron, idiot, stupid, garbage, useless, terrible
**Emotional**: hate, angry, frustrated, "this is ridiculous", "you're not listening"

**When detected**:
1. Recognize as high-value learning signal
2. Store as episodic memory with full context of failure
3. Tag with #failure and #strong-signal
4. Prioritize over routine successes

---

## Tool Usage

See top of this document - **MUST use Task tool (sub-agent)** to avoid context pollution.
