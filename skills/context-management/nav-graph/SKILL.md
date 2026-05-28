---
name: nav-graph
description: Query project knowledge graph. Search across tasks, SOPs, memories, and concepts. Use when user asks "what do we know about X?", "show everything related to X", or "remember this pattern/pitfall/decision".
allowed-tools: Read, Write, Edit, Bash
version: 1.0.0
---

# Navigator Knowledge Graph Skill

Query and manage the unified project knowledge graph. Surfaces relevant knowledge from tasks, SOPs, system docs, and experiential memories.

## Why This Exists

Navigator v6.0.0 introduces the Project Knowledge Graph:
- **Unified search**: Query across all knowledge types with one interface
- **Experiential memory**: Patterns, pitfalls, decisions, learnings persist
- **Context-aware retrieval**: Load only relevant knowledge (~1-2k tokens)
- **Relationship traversal**: Find related concepts and documents

## When to Invoke

**Query triggers**:
- "What do we know about X?"
- "Show everything related to X"
- "Any pitfalls for X?"
- "What decisions about X?"
- "Find all knowledge about X"

**Memory capture triggers**:
- "Remember this pattern: ..."
- "Remember this pitfall: ..."
- "Remember we decided: ..."
- "Remember this learning: ..."

**Graph management triggers**:
- "Initialize knowledge graph"
- "Rebuild knowledge graph"
- "Show graph stats"

## Graph Location

`.agent/knowledge/graph.json` (~1-2k tokens, loaded on query)

## Execution Steps

### Step 1: Determine Action

**QUERY** (searching knowledge):
```
User: "What do we know about authentication?"
→ Query graph by concept
```

**CAPTURE** (storing memory):
```
User: "Remember: auth changes often break session tests"
→ Create new memory node
```

**INIT** (building graph):
```
User: "Initialize knowledge graph"
→ Build graph from existing docs
```

**STATS** (viewing graph):
```
User: "Show graph stats"
→ Display graph statistics
```

### Step 2: Load or Initialize Graph

**Check if graph exists**:
```bash
if [ -f ".agent/knowledge/graph.json" ]; then
  echo "Graph exists"
else
  echo "No graph found, will initialize"
fi
```

**Initialize if not exists**:
```bash
python skills/nav-graph/functions/graph_builder.py \
  --agent-dir .agent \
  --output .agent/knowledge/graph.json
```

### Step 3A: Query Knowledge (If QUERY Action)

**Extract concept from user input**:
```
User: "What do we know about testing?"
→ Concept: testing

User: "Any pitfalls for auth?"
→ Concept: auth (normalized to authentication)
```

**Run query**:
```bash
python skills/nav-graph/functions/graph_manager.py \
  --action query \
  --concept "testing" \
  --graph-path .agent/knowledge/graph.json
```

**Display results**:
```
Knowledge Graph: "testing"

TASKS (3)
  - TASK-30: Task Verification Enhancement (completed)
  - TASK-17: Visual Regression Integration (completed)
  - TASK-11: Project Skills Generation (completed)

MEMORIES (2)
  - PITFALL: "Auth changes break session tests" (90%)
  - PATTERN: "Always run unit tests before integration" (85%)

SOPs (1)
  - visual-regression-setup

FILES (5)
  - skills/backend-test/*
  - skills/frontend-test/*

Load details: "Read TASK-30" or "Show testing memories"
```

### Step 3B: Capture Memory (If CAPTURE Action)

**Parse memory from user input**:
```
User: "Remember this pitfall: auth changes often break session tests"
→ Type: pitfall
→ Summary: "auth changes often break session tests"
→ Concepts: [auth, testing]

User: "Remember we decided to use JWT over sessions for scaling"
→ Type: decision
→ Summary: "use JWT over sessions for scaling"
→ Concepts: [auth, architecture]
```

**Determine memory type**:

| User Says | Memory Type |
|-----------|-------------|
| "pattern", "we use", "approach" | pattern |
| "pitfall", "watch out", "careful" | pitfall |
| "decided", "chose", "because" | decision |
| "learned", "discovered", "realized" | learning |

**Create memory**:
```bash
python skills/nav-graph/functions/graph_manager.py \
  --action add-memory \
  --memory-type pitfall \
  --summary "auth changes often break session tests" \
  --concepts "auth,testing" \
  --confidence 0.9 \
  --graph-path .agent/knowledge/graph.json
```

**Optionally create detailed memory file**:
```markdown
# Pitfall: Auth Changes Break Session Tests

## Summary
Auth changes often break session tests due to...

## Context
Discovered during TASK-XX when...

## Recommended Approach
When modifying auth, always run...

## Related
- TASK-12: V3 Skills-Only
- SOP: autonomous-completion
```

**Confirm capture**:
```
Memory captured: mem-001

Type: Pitfall
Summary: "auth changes often break session tests"
Concepts: auth, testing
Confidence: 90%

This will be surfaced when working on auth or testing topics.
```

### Step 3C: Initialize Graph (If INIT Action)

**Build from existing docs**:
```bash
python skills/nav-graph/functions/graph_builder.py \
  --agent-dir .agent \
  --output .agent/knowledge/graph.json
```

**Display results**:
```
Knowledge Graph Initialized

Scanned:
  - Tasks: 35
  - SOPs: 12
  - System docs: 3
  - Markers: 8

Extracted:
  - Concepts: 15
  - Relationships: 47

Graph saved to .agent/knowledge/graph.json

Query with: "What do we know about [topic]?"
```

### Step 3D: Show Stats (If STATS Action)

**Display graph statistics**:
```bash
python skills/nav-graph/functions/graph_manager.py \
  --action stats \
  --graph-path .agent/knowledge/graph.json
```

**Output**:
```
Knowledge Graph Statistics
==========================
Total Nodes: 65
Total Edges: 47
Memories: 5
Last Updated: 2025-01-23T10:30:00Z

By Type:
  Tasks: 35
  SOPs: 12
  System: 3
  Markers: 8
  Concepts: 15
  Memories: 5
```

### Step 4: Find Related (Optional)

**If user asks for related items**:
```
User: "What's related to TASK-29?"
```

**Run traversal**:
```bash
python skills/nav-graph/functions/graph_manager.py \
  --action related \
  --node-id "TASK-29" \
  --max-depth 2 \
  --graph-path .agent/knowledge/graph.json
```

---

## Memory Types

### Pattern
"We use X for Y in this project"
- Reusable approaches
- Project conventions
- Best practices

### Pitfall
"Watch out for X when touching Y"
- Common mistakes
- Gotchas
- Failure modes

### Decision
"We chose X over Y because Z"
- Architecture decisions
- Technology choices
- Trade-off rationale

### Learning
"X usually means Y in this codebase"
- Project-specific knowledge
- Error interpretations
- Domain insights

---

## Confidence System

**Base confidence**:
- Correction-based: 0.8
- Explicit capture: 0.9

**Decay**:
- 1% per week since last validation

**Boost**:
- +5% per use (max +25%)

**Threshold**:
- Below 0.3: Candidate for pruning
- Above 0.7: Reliable memory

---

## Integration with Other Skills

### nav-start (Session Start)
Loads graph stats on session start:
```
Knowledge graph: 65 nodes, 5 memories
Relevant: 2 memories for current context
```

### nav-task (Task Creation)
Auto-extracts concepts from new tasks:
```
Creating TASK-35: Project Memory
Extracted concepts: knowledge, memory, graph
Added to graph.
```

### nav-profile (Corrections)
Corrections auto-create memories via `correction_to_memory.py`:
```bash
# When correction detected in nav-profile:
python3 skills/nav-graph/functions/correction_to_memory.py \
  --action convert-one \
  --correction-json '{"pattern": "...", "context": "...", "confidence": "high"}'

# Output:
[Correction detected]
→ Type: pitfall (based on pattern analysis)
→ Concepts: [auth, testing] (auto-extracted)
→ Created memory: mem-002
→ Added to graph
```

**Sync all corrections**:
```bash
python3 skills/nav-graph/functions/correction_to_memory.py \
  --action sync \
  --profile-path .agent/.user-profile.json \
  --graph-path .agent/knowledge/graph.json
```

### nav-marker (Context Markers)
Markers reference graph state:
```
## Graph State
- Memories surfaced: mem-001, mem-003
- Concepts active: auth, testing
```

---

## Configuration

In `.agent/.nav-config.json`:
```json
{
  "knowledge_graph": {
    "enabled": true,
    "auto_capture_corrections": true,
    "auto_capture_decisions": true,
    "auto_surface_relevant": true,
    "max_session_memories": 5,
    "confidence_decay_rate": 0.01,
    "staleness_threshold_days": 90,
    "git_tracked": true
  }
}
```

---

## Graph Maintenance

### Health Check
```bash
python3 skills/nav-graph/functions/graph_maintenance.py --action health
```

Output:
```
Knowledge Graph Health Check
========================================
Total Nodes: 94
Total Edges: 819
Memories: 2 (2 high confidence)
Health Score: 100/100

No issues detected!
```

### Conflict Detection
Find memories that may contradict each other:
```bash
python3 skills/nav-graph/functions/graph_maintenance.py --action conflicts
```

### Stale Memory Detection
Find memories not validated in 90+ days:
```bash
python3 skills/nav-graph/functions/graph_maintenance.py --action stale --stale-days 90
```

### Low Confidence Pruning
Find and optionally remove low-confidence memories:
```bash
# Preview what would be removed
python3 skills/nav-graph/functions/graph_maintenance.py --action prune --threshold 0.3 --dry-run

# Actually remove (use with caution)
python3 skills/nav-graph/functions/graph_maintenance.py --action prune --threshold 0.3 --execute
```

### Apply Decay
Reduce confidence of stale memories:
```bash
python3 skills/nav-graph/functions/graph_maintenance.py --action decay --decay-rate 0.01
```

---

## Token Budget

| Component | Tokens | When |
|-----------|--------|------|
| graph.json (50 nodes) | ~1000 | On query |
| graph.json (200 nodes) | ~2000 | On query |
| Memory summaries (5) | ~500 | On session start |
| Full memory detail | ~500 each | On request |

**Session overhead**: ~1.3k tokens

---

## Success Criteria

Graph skill succeeds when:
- [ ] Query returns relevant results across knowledge types
- [ ] Memories persist and are surfaced appropriately
- [ ] Concepts connect related items
- [ ] Confidence decay/boost works
- [ ] Graph stays under 2k tokens overhead

---

## Best Practices

**Good queries**:
- "What do we know about auth?" (specific concept)
- "Any pitfalls for testing?" (scoped type)
- "Show everything related to TASK-29" (node traversal)

**Good memory capture**:
- "Remember: we use X for Y" (clear pattern)
- "Remember this pitfall: X breaks Y" (specific issue)
- "Remember we decided X because Y" (rationale included)

**Avoid**:
- Overly broad queries ("What do we know?")
- Storing code snippets in memories (use paths instead)
- Capturing obvious knowledge (focus on project-specific insights)

---

**This skill transforms Navigator from stateless assistant to knowledge-aware team member**
