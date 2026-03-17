---
name: coder-memory-recall
description: Retrieve universal coding patterns from vector database using true two-stage retrieval. Auto-invokes before complex tasks or when user says "--recall". Searches relevant role collections based on task context.
---

## ⚠️ MANDATORY: Use Task Tool (Sub-Agent)

**NEVER call memory MCP tools directly!** Use Task tool with `subagent_type: "general-purpose"` to keep main context clean.

---

## CRITICAL: When NOT to Search Memory

**Skip memory search for obvious tasks** - killing processes, starting servers, basic file operations, standard workflows.

**Only search for hard problems** - non-obvious bugs, complex architectures, performance issues, unfamiliar domains.

**Rule**: If basic knowledge suffices, skip memory. Memory is for hard-won lessons.

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

## PHASE 1: Intelligent Query Construction

**Note**: Claude Code automatically determines relevant roles from task context. No explicit role detection logic needed - Claude is smart enough to select appropriate roles when calling MCP tools.

### Query Building

Build semantic query (2-3 sentences) capturing:
1. What is the problem/goal?
2. What is the technical context?
3. What outcome is desired?

## MCP Server Tools

**CRITICAL**: Use tools from the **memory MCP server**:
- `search_memory` - Search and get previews
- `get_memory` - Get full content by ID
- `batch_get_memories` - Get multiple full contents
- `store_memory` - Store new memory
- `update_memory` - Update existing memory
- `delete_memory` - Delete memory
- `list_collections` - List all collections

## PHASE 2: Two-Stage Retrieval

### Stage 1: Search for Previews (Cast Wide Net)

Use `search_memory` tool (from memory MCP server) with the query and correct memory_level (global, project, etc.), default: `memory_level="global"`. Claude Code determines relevant roles automatically. Default limit is 20 previews.

### Stage 2: Analyze Previews (Intelligence Over Thresholds)

**Analyze each preview**:
- Does title match the problem domain?
- Does description indicate relevant solution?
- Do tags align with task?
- Is memory type appropriate? (episodic for debugging, procedural for workflows, semantic for principles)

**Select 3-5 most relevant** based on your judgement.

### Stage 3: Retrieve Full Content

Use `batch_get_memories` tool (from memory MCP server) with the selected doc_ids and `memory_level="global"`. This retrieves full content for 3-5 most relevant memories.


## PHASE 3: Present Results

Format for Claude to consume:
**Key**: Let Claude read and decide what to use. Don't force-fit patterns.

---

## Tool Usage

See top of this document - **MUST use Task tool (sub-agent)** to avoid context pollution.
