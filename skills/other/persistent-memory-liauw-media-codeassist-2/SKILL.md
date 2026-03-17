---
name: persistent-memory
description: "Use when working on long-running projects or needing context across sessions. Covers memory architecture, privacy controls, efficient retrieval, and integration with claude-mem plugin. Apply when building features that span multiple sessions or need historical context."
---

# Persistent Memory

## Core Principle

Memory is context that survives sessions. Use it strategically—store what matters, retrieve efficiently, protect what's private.

## When to Use This Skill

- Working on multi-session projects
- Need to recall previous decisions
- Building on past work
- Maintaining project context
- Debugging issues that span sessions
- Onboarding to existing projects

## The Iron Law

**MEMORY IS NOT FREE. RETRIEVE SELECTIVELY.**

Every token of context costs. Don't dump entire history—search and fetch only what's relevant.

## Why Persistent Memory?

**Benefits:**
- Continue where you left off
- Recall past decisions and rationale
- Maintain consistency across sessions
- Build institutional knowledge
- Reduce repetitive explanations
- Track project evolution

**Without persistent memory:**
- Start fresh every session
- Repeat context explanations
- Forget past decisions
- Lose architectural rationale
- Inconsistent approaches
- No learning from history

## Memory Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM                         │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Capture    │───▶│    Store     │───▶│  Retrieve │ │
│  │  (Hooks)     │    │  (SQLite +   │    │  (Search) │ │
│  │              │    │   Vectors)   │    │           │ │
│  └──────────────┘    └──────────────┘    └───────────┘ │
│         │                   │                   │       │
│         ▼                   ▼                   ▼       │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │ Session      │    │ Observations │    │ Summaries │ │
│  │ Lifecycle    │    │ & Context    │    │ & Answers │ │
│  └──────────────┘    └──────────────┘    └───────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Setup with claude-mem

### Installation

```bash
# Install the plugin
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem

# Restart Claude Code
# Memory automatically starts capturing
```

### Verify Installation

```bash
# Check the web UI
open http://localhost:37777

# Memory service should be running on port 37777
```

### Configuration

The plugin captures automatically via lifecycle hooks:
- `SessionStart` - New session begins
- `UserPromptSubmit` - User sends message
- `PostToolUse` - Tool execution complete
- `Stop` - Task completed
- `SessionEnd` - Session ends

## Memory Best Practices

### 1. What to Remember

**DO store:**
- Architectural decisions and rationale
- Project conventions and patterns
- Bug fixes and their root causes
- Configuration choices
- API contracts and schemas
- Team preferences

**DON'T store:**
- Temporary debugging output
- Sensitive credentials
- Large file contents
- Trivial operations

### 2. Privacy Controls

Use `<private>` tags to exclude sensitive content:

```markdown
Here's the database config:
<private>
DATABASE_URL=postgres://user:password@host:5432/db
API_KEY=sk-secret-key-here
</private>

The schema uses PostgreSQL with these tables...
```

Content within `<private>` tags is NOT stored in memory.

### 3. Efficient Retrieval

Memory retrieval uses a three-layer workflow:

```
Layer 1: Search Index
  └── Quick keyword/semantic match
  └── Returns: observation IDs + snippets
  └── Cost: ~100 tokens

Layer 2: Timeline Context
  └── Fetch surrounding observations
  └── Returns: chronological context
  └── Cost: ~500 tokens

Layer 3: Full Details
  └── Fetch complete observations
  └── Returns: full content
  └── Cost: varies (can be large)
```

**Best practice**: Start with Layer 1, only go deeper if needed.

### 4. Querying Memory

```
# Good queries (specific)
"How did we implement authentication?"
"What was the decision on database schema?"
"Why did we choose React over Vue?"

# Poor queries (too broad)
"What did we do?"
"Show me everything"
"All past work"
```

### 5. Memory Hygiene

Periodically review and clean:

```bash
# Access web UI to browse memory
open http://localhost:37777

# Review recent sessions
# Delete irrelevant observations
# Check storage usage
```

## Integration Patterns

### Pattern 1: Session Continuity

```markdown
# At session start
"Check memory for our previous work on the authentication feature.
What was our approach and what's left to do?"

# Memory retrieves relevant context automatically
```

### Pattern 2: Decision Recall

```markdown
# When making architectural decisions
"Search memory for past discussions about state management.
What approaches did we consider and why did we choose Redux?"
```

### Pattern 3: Bug Investigation

```markdown
# When debugging recurring issues
"Search memory for similar errors we've seen before.
How did we fix the authentication timeout issue last time?"
```

### Pattern 4: Onboarding Context

```markdown
# When starting on existing project
"Retrieve memory summaries for this project.
What are the key architectural decisions and conventions?"
```

## Memory-Aware Workflow

### Starting a Session

```
1. Claude automatically loads relevant memory
2. Review injected context (check token cost)
3. Ask clarifying questions if context seems incomplete
4. Proceed with task
```

### During Work

```
1. Important decisions → explicitly note rationale
2. Sensitive data → use <private> tags
3. Complex solutions → document approach
4. Errors fixed → note root cause
```

### Ending a Session

```
1. Summarize what was accomplished
2. Note any pending work
3. Document blockers or questions
4. Memory auto-captures on session end
```

## Token Efficiency

### Understanding Costs

The web UI shows token costs for context injection:

| Context Type | Typical Tokens | When to Use |
|--------------|----------------|-------------|
| Session summary | 100-300 | Always (automatic) |
| Search results | 200-500 | Specific queries |
| Full observation | 500-2000 | Deep dive needed |
| Timeline context | 300-800 | Understanding sequence |

### Optimization Strategies

```
1. Use specific queries
   ❌ "What do you know?"
   ✅ "What's our API rate limiting strategy?"

2. Progressive disclosure
   - Start with summaries
   - Drill down only if needed
   - Don't fetch everything

3. Prune irrelevant results
   - Skip old/outdated context
   - Focus on recent sessions
   - Filter by relevance
```

## Troubleshooting

### Memory Not Capturing

```bash
# Check if service is running
curl http://localhost:37777/health

# Verify plugin is installed
/plugin list

# Reinstall if needed
/plugin uninstall claude-mem
/plugin install claude-mem
```

### Search Not Finding Results

```
1. Try different keywords
2. Use semantic queries (describe what you mean)
3. Check date range
4. Verify content wasn't marked <private>
```

### High Token Usage

```
1. Review what's being injected
2. Use more specific queries
3. Disable automatic context for trivial tasks
4. Clean old irrelevant observations
```

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Storing secrets | Security risk | Use `<private>` tags |
| Retrieving everything | Token explosion | Query specifically |
| Ignoring memory | Repeated work | Check memory first |
| No privacy tags | Credentials exposed | Tag sensitive content |
| Stale memory | Wrong context | Periodically clean |

## Integration with Other Skills

**Use with:**
- `rag-architecture` - Memory as knowledge source
- `agentic-design` - Long-term agent memory
- `llm-integration` - Context management
- `subagent-driven-development` - Cross-task context

**Enhances:**
- `brainstorming` - Recall past ideas
- `code-review` - Remember past issues
- `writing-plans` - Build on previous plans

## Checklist

Before relying on memory:
- [ ] Plugin installed and running
- [ ] Web UI accessible at localhost:37777
- [ ] Privacy tags used for sensitive data
- [ ] Token costs understood
- [ ] Retrieval queries specific

During sessions:
- [ ] Important decisions documented
- [ ] Rationale captured
- [ ] Sensitive content tagged private
- [ ] Context retrieved efficiently

## Authority

**Based on:**
- claude-mem plugin by [@thedotmack](https://github.com/thedotmack/claude-mem)
- Vector database best practices
- Information retrieval research
- Context window optimization patterns

---

**Bottom Line**: Memory extends context across sessions. Store decisions, protect secrets, retrieve selectively. Every token costs—be strategic about what you recall.
