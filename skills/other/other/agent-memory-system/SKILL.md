---
name: agent-memory-system
description: Persistent memory architecture for AI agents across sessions. Episodic memory (past events), procedural memory (learned skills), semantic memory (knowledge graph), short-term memory (active context). Use when implementing cross-session persistence, skill learning, context preservation, personalization, or building truly adaptive AI systems with long-term memory.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Agent Memory System

## Overview

agent-memory-system provides persistent memory architecture enabling AI agents to remember across sessions, learn from experience, and build long-term knowledge.

**Purpose**: Enable true continuous improvement through persistent memory

**Pattern**: Capabilities-based (4 memory types with independent operations)

**Key Innovation**: Multi-layered memory architecture (episodic, procedural, semantic, short-term) enabling agents to learn and adapt over time

**Core Principles**:
1. **Episodic Memory** - Remember specific past events and decisions
2. **Procedural Memory** - Learn and improve skills over time
3. **Semantic Memory** - Build knowledge graphs of facts and relationships
4. **Short-Term Memory** - Active working context

---

## When to Use

Use agent-memory-system when:

- Building agents that learn from experience
- Preserving context across multiple sessions
- Implementing personalization (remember user preferences)
- Creating adaptive systems (improve over time)
- Long-running projects (remember decisions made weeks ago)
- Skill improvement tracking (what works, what doesn't)

---

## Prerequisites

### Required
- File system access (for file-based memory)
- JSON support (for structured memory storage)

### Optional
- Vector database (Pinecone, Weaviate, Chroma) for episodic memory
- Graph database (Neo4j) for semantic memory
- Redis for fast short-term memory

### Understanding
- Memory types and when to use each
- Trade-offs (file-based vs. database)

---

## Memory Types

### Memory Type 1: Episodic Memory

**What**: Remembers specific past events, decisions, and their outcomes

**Use When**: Need to recall "What happened last time we tried X?"

**Storage**: Vector database (similarity search) or timestamped JSON files

**Structure**:
```json
{
  "episode_id": "ep_20250115_1530",
  "timestamp": "2025-01-15T15:30:00Z",
  "event_type": "implementation",
  "description": "Implemented user authentication with OAuth",
  "context": {
    "objective": "Add OAuth to existing password auth",
    "approach": "Expand-migrate-contract pattern",
    "decisions": [
      {
        "question": "JWT vs Sessions?",
        "choice": "JWT",
        "rationale": "Stateless, scales better"
      }
    ],
    "outcomes": {
      "quality_score": 94,
      "test_coverage": 89,
      "time_actual": "6.5 hours",
      "time_estimated": "5 hours"
    },
    "learnings": [
      "OAuth token refresh needs explicit testing",
      "Expand-migrate-contract took longer than estimated"
    ]
  },
  "tags": ["authentication", "oauth", "implementation"],
  "embedding": [0.123, -0.456, ...] // For similarity search
}
```

**Operations**:
1. **Store Episode**: Save event after completion
2. **Recall Similar**: Find similar past episodes (vector similarity)
3. **Query by Tag**: Retrieve all episodes with specific tags
4. **Learn from Outcomes**: Extract patterns from successful episodes

**Queries**:
```bash
# Find similar past implementations
recall-episode --similar "implementing OAuth" --top 5

# Find all authentication-related episodes
recall-episode --tag authentication

# Learn from failures
recall-episode --filter "quality_score < 80" --analyze
```

**Benefits**:
- Avoid repeating mistakes
- Apply successful patterns
- Improve estimation accuracy
- Faster decision-making

**Storage**:
- **Simple**: JSON files in `.memory/episodic/YYYY-MM-DD/`
- **Advanced**: Vector DB for semantic search

---

### Memory Type 2: Procedural Memory

**What**: Learned skills, successful patterns, automation rules

**Use When**: "How do we usually do X?" or "What's our standard approach for Y?"

**Storage**: Structured files or code patterns

**Structure**:
```json
{
  "skill_id": "implement_authentication",
  "skill_name": "Implementing Authentication Systems",
  "learned_from": [
    "ep_20250115_1530",
    "ep_20250120_1045",
    "ep_20250125_1400"
  ],
  "pattern": {
    "approach": "Expand-migrate-contract",
    "steps": [
      "1. Add new auth alongside existing",
      "2. Dual-write period (both methods work)",
      "3. Migrate users gradually",
      "4. Deprecate old auth"
    ],
    "pitfalls": [
      "Always test token refresh explicitly",
      "Plan for 20% longer than estimated (migrations complex)"
    ],
    "success_criteria": {
      "quality_score": ">= 90",
      "test_coverage": ">= 85",
      "backward_compatible": true
    }
  },
  "usage_count": 3,
  "success_rate": 1.0,
  "avg_quality_score": 93.3,
  "avg_time_hours": 6.2,
  "last_used": "2025-01-25T14:00:00Z"
}
```

**Operations**:
1. **Extract Pattern**: Learn pattern from successful episodes
2. **Store Skill**: Save learned procedural knowledge
3. **Apply Skill**: Use learned pattern for new task
4. **Improve Skill**: Update based on new experiences

**Queries**:
```bash
# Get learned pattern for authentication
get-skill "authentication implementation"

# Find most successful patterns
list-skills --sort-by success_rate --top 10

# Update skill with new learning
update-skill "authentication" --episode ep_20250125_1400
```

**Benefits**:
- Codify successful patterns
- Improve patterns over time
- Share knowledge across team
- Faster implementation (apply proven patterns)

**Storage**: `.memory/procedural/skills/`

---

### Memory Type 3: Semantic Memory

**What**: Facts, relationships, knowledge graph of concepts

**Use When**: "What's the relationship between X and Y?" or "What do we know about Z?"

**Storage**: Graph database (Neo4j) or JSON with relationships

**Structure**:
```json
{
  "concepts": [
    {
      "id": "oauth",
      "type": "technology",
      "description": "OAuth 2.0 authorization framework",
      "properties": {
        "security_level": "high",
        "complexity": "medium",
        "browser_required": true
      },
      "relationships": [
        {
          "type": "used_by",
          "target": "user_authentication",
          "weight": 0.95
        },
        {
          "type": "requires",
          "target": "jwt",
          "weight": 0.85
        },
        {
          "type": "alternative_to",
          "target": "password_auth",
          "weight": 0.7
        }
      ]
    }
  ],
  "facts": [
    {
      "subject": "oauth",
      "predicate": "supports",
      "object": "multiple_providers",
      "confidence": 1.0,
      "source": "ep_20250115_1530"
    }
  ]
}
```

**Operations**:
1. **Store Fact**: Add new knowledge
2. **Query Knowledge**: Retrieve facts about concepts
3. **Find Relationships**: Navigate knowledge graph
4. **Infer Knowledge**: Deduce new facts from relationships

**Queries**:
```bash
# What do we know about OAuth?
query-knowledge "oauth"

# What are alternatives to password auth?
query-knowledge "password_auth" --relationship alternative_to

# Find all authentication methods
query-knowledge --type authentication_method
```

**Benefits**:
- Build institutional knowledge
- Understand concept relationships
- Make informed decisions
- Avoid knowledge loss

**Storage**:
- **Simple**: JSON files in `.memory/semantic/`
- **Advanced**: Neo4j graph database

---

### Memory Type 4: Short-Term Memory

**What**: Active working context, current session state

**Use When**: Need to remember within current conversation

**Storage**: RAM or Redis (fast access)

**Structure**:
```json
{
  "session_id": "session_20250126_1200",
  "started_at": "2025-01-26T12:00:00Z",
  "current_task": "Implementing user authentication",
  "context": {
    "files_read": [
      "src/auth/login.ts",
      "src/auth/tokens.ts"
    ],
    "decisions_made": [
      {"what": "Use JWT", "why": "Stateless scaling"}
    ],
    "next_steps": [
      "Implement token refresh",
      "Add rate limiting"
    ]
  },
  "temporary_data": {
    "research_findings": "...",
    "plan_summary": "..."
  }
}
```

**Operations**:
1. **Set Context**: Store current working data
2. **Get Context**: Retrieve active context
3. **Update Context**: Modify current state
4. **Clear Context**: Reset working memory

**Benefits**:
- Fast access to current state
- No context window pollution
- Efficient session management

**Storage**: File in `.memory/short-term/current-session.json`

---

## Core Operations

### Operation 1: Store Memory

**Purpose**: Save information to appropriate memory type

**Process**:

```typescript
// Store episodic memory
await storeMemory({
  type: 'episodic',
  event: {
    description: 'Implemented OAuth authentication',
    decisions: [...],
    outcomes: {...},
    learnings: [...]
  },
  tags: ['authentication', 'oauth', 'implementation']
});

// Store procedural memory (learned pattern)
await storeMemory({
  type: 'procedural',
  skillName: 'Implementing Authentication',
  pattern: {
    approach: 'Expand-migrate-contract',
    steps: [...],
    pitfalls: [...]
  }
});

// Store semantic memory (fact)
await storeMemory({
  type: 'semantic',
  fact: {
    subject: 'oauth',
    predicate: 'requires',
    object: 'jwt',
    confidence: 0.95
  }
});
```

**Outputs**:
- Memory persisted to storage
- Indexed for retrieval
- Timestamped

---

### Operation 2: Recall Memory

**Purpose**: Retrieve relevant memories for current task

**Process**:

```typescript
// Recall similar episodes
const similarEpisodes = await recallMemory({
  type: 'episodic',
  query: 'implementing authentication',
  limit: 5
});

// Recall learned patterns
const authPattern = await recallMemory({
  type: 'procedural',
  skillName: 'Implementing Authentication'
});

// Query knowledge
const oauthFacts = await recallMemory({
  type: 'semantic',
  concept: 'oauth'
});
```

**Outputs**:
- Relevant memories retrieved
- Ranked by relevance/recency
- Ready to inform current decisions

---

### Operation 3: Learn from Experience

**Purpose**: Extract patterns and update procedural memory

**Process**:

1. **Analyze Episodes**:
   ```typescript
   // Get all authentication implementations
   const authEpisodes = await recallMemory({
     type: 'episodic',
     tags: ['authentication', 'implementation']
   });

   // Extract patterns
   const patterns = analyzePatterns(authEpisodes);
   // - Approach used: expand-migrate-contract (3/3 times)
   // - Avg quality score: 93.3
   // - Common pitfall: Token refresh testing (3/3 missed initially)
   ```

2. **Update Procedural Memory**:
   ```typescript
   await storeMemory({
     type: 'procedural',
     skillName: 'Implementing Authentication',
     pattern: {
       approach: 'expand-migrate-contract', // Learned from all 3 episodes
       common_pitfall: 'Always test token refresh explicitly', // Learned
       quality_target: '>= 93', // Based on historical avg
       time_estimate: '6-7 hours' // Based on historical data
     },
     learnedFrom: authEpisodes.map(ep => ep.id),
     confidence: 0.95 // High (based on 3 episodes)
   });
   ```

**Outputs**:
- Learned patterns codified
- Procedural memory updated
- Future decisions informed by experience

---

### Operation 4: Personalize

**Purpose**: Adapt to user preferences and patterns

**Process**:

```typescript
// Track user preferences
const preferences = await recall Memory({
  type: 'semantic',
  concept: 'user_preferences'
});

// Learn from usage patterns
const userPatterns = {
  preferred_approach: 'TDD', // User always uses TDD
  testing_thoroughness: 'high', // User requests >=95% coverage
  verification_level: 'all_layers', // User runs all 5 layers
  commit_style: 'conventional' // User uses conventional commits
};

// Apply personalization
if (userPatterns.preferred_approach === 'TDD') {
  // Auto-suggest TDD workflow
  // Skip asking "test-first or code-first?"
}
```

**Outputs**:
- Personalized recommendations
- Reduced repetitive questions
- Faster workflows

---

## Cross-Session Integration

### Session Start Integration

**Hook**: SessionStart hook loads memory

```bash
#!/bin/bash
# .claude/hooks/load-memory.sh (SessionStart)

echo "📚 Loading agent memory..."

# Load short-term memory from last session
if [ -f ".memory/short-term/last-session.json" ]; then
  echo "  └─ Previous session context available"
  # Claude can read this file to continue work
fi

# Load recent episodic memories (last 7 days)
RECENT_EPISODES=$(find .memory/episodic/ -name "*.json" -mtime -7 | wc -l)
echo "  └─ Recent episodes: $RECENT_EPISODES"

# Load active skills
LEARNED_SKILLS=$(ls .memory/procedural/skills/ | wc -l)
echo "  └─ Learned skills: $LEARNED_SKILLS"

echo "✅ Memory loaded"
```

---

### Session End Integration

**Hook**: SessionEnd hook saves memory

```bash
#!/bin/bash
# .claude/hooks/save-memory.sh (SessionEnd)

echo "💾 Saving agent memory..."

# Save current session to episodic memory
if [ -f ".memory/short-term/current-session.json" ]; then
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  cp .memory/short-term/current-session.json \
     .memory/episodic/$(date +%Y-%m-%d)/session_$TIMESTAMP.json

  echo "  └─ Episode saved"
fi

# Extract learnings if quality was high
# (Automated learning extraction)

echo "✅ Memory saved"
```

---

## Memory Architecture

### File-Based Memory (Simple)

**Structure**:
```
.memory/
├── episodic/              # Past events
│   ├── 2025-01-15/
│   │   ├── session_153000.json
│   │   └── decision_153045.json
│   └── 2025-01-16/
│       └── session_090000.json
├── procedural/            # Learned skills
│   └── skills/
│       ├── authentication_impl.json
│       ├── testing_pattern.json
│       └── verification_approach.json
├── semantic/              # Knowledge graph
│   ├── concepts.json
│   └── relationships.json
└── short-term/            # Active session
    ├── current-session.json
    └── last-session.json (backup)
```

**Benefits**:
- Simple (no database required)
- Version-controllable
- Human-readable
- Easy backup

**Limitations**:
- No semantic search
- Manual indexing needed
- Slower for large datasets

---

### Database-Backed Memory (Advanced)

**Episodic** (Vector DB):
- **Pinecone**: Managed, fast, expensive
- **Weaviate**: Self-hosted, flexible
- **Chroma**: Lightweight, good for prototypes

**Semantic** (Graph DB):
- **Neo4j**: Industry standard
- **AgensGraph**: PostgreSQL-based
- **NetworkX**: Python library (simple graphs)

**Short-Term** (Cache):
- **Redis**: Fast, ephemeral
- **Memcached**: Simple caching

**Benefits**:
- Semantic search (similarity, relationships)
- Fast queries at scale
- Advanced capabilities

**Limitations**:
- Infrastructure complexity
- Cost (hosted solutions)
- Deployment overhead

---

## Integration with Multi-AI Skills

### With multi-ai-implementation

**Before Implementation** (recall relevant patterns):
```typescript
// Step 1: Explore - Check memory for similar implementations
const similarWork = await recallMemory({
  type: 'episodic',
  query: currentObjective,
  limit: 3
});

// Apply learnings
if (similarWork.length > 0) {
  console.log("📚 Found similar past work:");
  similarWork.forEach(episode => {
    console.log(`  - ${episode.description}`);
    console.log(`    Quality: ${episode.outcomes.quality_score}`);
    console.log(`    Learnings: ${episode.learnings.join(', ')}`);
  });
}

// Step 2: Plan - Use learned patterns
const authPattern = await recallMemory({
  type: 'procedural',
  skillName: 'Implementing Authentication'
});

if (authPattern) {
  console.log("📖 Applying learned pattern:");
  console.log(`  Approach: ${authPattern.pattern.approach}`);
  console.log(`  Estimated time: ${authPattern.avg_time_hours} hours`);
}
```

**After Implementation** (save episode):
```typescript
// Step 6: Commit - Save to episodic memory
await storeMemory({
  type: 'episodic',
  event: {
    description: 'Implemented user authentication',
    decisions: capturedDuringImplementation,
    outcomes: {
      quality_score: 94,
      test_coverage: 89,
      time_actual: 6.5,
      time_estimated: 5
    },
    learnings: [
      'Token refresh needs explicit testing',
      'Estimation was 30% low'
    ]
  }
});

// Extract and update patterns
await learnFromExperience(['authentication', 'implementation']);
```

---

### With multi-ai-planning

**Before Planning**:
```typescript
// Recall similar plans
const similarPlans = await recallMemory({
  type: 'episodic',
  query: 'plan for ' + objective,
  filter: 'event_type == "planning"'
});

// Check quality of past plans
if (similarPlans.length > 0) {
  const avgQuality = average(similarPlans.map(p => p.outcomes.quality_score));
  console.log(`📊 Past similar plans averaged ${avgQuality}/100`);
}
```

**After Planning**:
```typescript
// Save plan to memory
await storeMemory({
  type: 'episodic',
  event: {
    event_type: 'planning',
    description: 'Planned OAuth implementation',
    context: {
      tasks: planGenerated.tasks.length,
      quality_score: planGenerated.quality_score,
      estimated_hours: planGenerated.metadata.estimated_total_hours
    }
  }
});
```

---

### With multi-ai-verification

**Before Verification**:
```typescript
// Recall common issues for this type of code
const commonIssues = await recallMemory({
  type: 'semantic',
  concept: 'authentication',
  relationship: 'common_issues'
});

// Focus verification on known problem areas
verificationFocus = commonIssues.map(issue => issue.description);
```

**After Verification**:
```typescript
// Save verification results
await storeMemory({
  type: 'episodic',
  event: {
    event_type: 'verification',
    description: 'Verified OAuth implementation',
    outcomes: {
      quality_score: 92,
      layers_passed: 5,
      issues_found: 3,
      time_minutes: 85
    }
  }
});

// Update semantic memory with new facts
if (issues_found.includes('bcrypt_rounds_low')) {
  await storeMemory({
    type: 'semantic',
    fact: {
      subject: 'bcrypt',
      predicate: 'recommended_rounds',
      object: '12-14',
      confidence: 0.95,
      source: 'verification_20250126'
    }
  });
}
```

---

## Memory Management

### Memory Lifecycle

**Creation** (automatic):
- After every skill completion
- After significant decisions
- On verification completion
- On failure (for learning)

**Retention** (configurable):
- Episodic: 90 days (can extend for important episodes)
- Procedural: Indefinite (patterns persist)
- Semantic: Indefinite (facts persist)
- Short-term: Until session end + 1 backup

**Cleanup** (automatic):
- Old episodic memories: archive or delete
- Unused procedural patterns: mark inactive
- Low-confidence facts: deprecate
- Short-term: clear after session end

### Memory Consolidation

**Nightly Process**:
```bash
#!/bin/bash
# Run nightly (cron job)

# 1. Consolidate recent episodes into patterns
node .memory/scripts/consolidate-episodes.js --days 7

# 2. Update procedural memory
node .memory/scripts/update-skills.js

# 3. Clean up old short-term memory
find .memory/short-term/ -name "*.json" -mtime +7 -delete

# 4. Archive old episodes
find .memory/episodic/ -name "*.json" -mtime +90 -exec mv {} .memory/archive/ \;

# 5. Update knowledge graph
node .memory/scripts/update-knowledge-graph.js
```

---

## Best Practices

### 1. Store After Every Significant Event
Don't wait until end of project - save continuously

### 2. Tag Generously
More tags = better recall ("authentication", "security", "oauth", "implementation")

### 3. Include Context in Episodes
Store enough context to understand decision later

### 4. Extract Learnings Explicitly
Don't just store what happened - store what you learned

### 5. Review Memory Periodically
Monthly review: what patterns emerged, what improved, what to change

### 6. Share Memory Across Team
Semantic and procedural memory are team assets

---

## Appendix A: Memory Integration with Hooks

### SessionStart: Load Memory

```json
{
  "event": "SessionStart",
  "description": "Load agent memory on session start",
  "handler": {
    "command": ".claude/hooks/load-memory.sh"
  }
}
```

### SessionEnd: Save Memory

```json
{
  "event": "SessionEnd",
  "description": "Save agent memory on session end",
  "handler": {
    "command": ".claude/hooks/save-memory.sh"
  }
}
```

### PostToolUse: Track Decisions

```json
{
  "event": "PostToolUse",
  "tools": ["Write"],
  "description": "Track significant code changes",
  "handler": {
    "command": ".claude/hooks/track-change.sh \"$FILE\" \"$TOOL\""
  }
}
```

---

## Appendix B: Vector DB Integration

### Simple Vector Search (File-Based)

```python
# Calculate similarity using embeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Get embedding for current query
query_embedding = get_embedding(current_objective)

# Load all episode embeddings
episodes = load_all_episodes()

# Calculate similarities
similarities = cosine_similarity(
    [query_embedding],
    [ep['embedding'] for ep in episodes]
)[0]

# Get top 5 most similar
top_indices = np.argsort(similarities)[-5:][::-1]
similar_episodes = [episodes[i] for i in top_indices]
```

### Advanced Vector DB (Pinecone)

```python
import pinecone

# Initialize
pinecone.init(api_key="...", environment="...")
index = pinecone.Index("agent-memory")

# Store episode
index.upsert([
    ("ep_20250115_1530", episode_embedding, episode_metadata)
])

# Recall similar
results = index.query(
    query_embedding,
    top_k=5,
    include_metadata=True
)

similar_episodes = [r['metadata'] for r in results['matches']]
```

---

## Quick Reference

### The 4 Memory Types

| Type | Storage | Retrieval | Retention | Use For |
|------|---------|-----------|-----------|---------|
| **Episodic** | Vector DB or timestamped JSON | Similarity search | 90 days | "What happened when we did X?" |
| **Procedural** | JSON files | Name/tag lookup | Indefinite | "How do we usually do Y?" |
| **Semantic** | Graph DB or JSON | Concept queries | Indefinite | "What do we know about Z?" |
| **Short-Term** | RAM/Redis or JSON | Direct access | Session only | "What's the current context?" |

### Memory Operations

| Operation | Purpose | Complexity | Time |
|-----------|---------|------------|------|
| **Store** | Save memory | Low | Instant |
| **Recall** | Retrieve memory | Low-Medium | <1s file, <100ms DB |
| **Learn** | Extract patterns | Medium | Minutes |
| **Personalize** | Adapt to user | Medium | Ongoing |

---

**agent-memory-system enables persistent memory across sessions, allowing agents to learn from experience, improve over time, and build institutional knowledge - the foundation for truly adaptive AI systems.**

For integration examples, see examples/. For database setup, see Appendix B.
