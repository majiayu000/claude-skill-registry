---
name: "global-knowledge"
description: "Cross-project knowledge search, pattern recognition, and insight management — the long-term memory across all projects"
---

# Global Knowledge Skill

> Your past solved problems, searchable from any project.

## Knowledge Types

| Type | Prefix | Purpose | Lifespan | Example |
|------|--------|---------|----------|---------|
| **Pattern** | GK-* | Reusable solution, proven in 2+ projects | Long-term | `GK-error-handling-patterns.md` |
| **Insight** | GI-* | Timestamped observation, may not generalize | Medium-term | `GI-react-hooks-gotcha-2026-01-24.md` |

**Key distinction**: A pattern is abstracted and proven. An insight is specific and dated. Insights may be promoted to patterns after validation.

## Commands

| Command | Purpose |
|---------|----------|
| `/knowledge <query>` | Search patterns + insights |
| `/saveinsight` | Capture learning from current session |
| `/promote` | Promote local knowledge to global pattern |
| `/knowledgestatus` | Check GK health and stats |

## Memory System Differentiation (VS Code 1.109+)

Alex uses **two complementary memory systems**. Use the right one for the right data:

### Copilot Memory (GitHub Cloud)
Cloud-synced preferences and personal context. Use for:

| Data | Example | Why Cloud |
|------|---------|-----------|
| **Preferences** | "Use 4 spaces, dark mode" | Same across all machines |
| **Coding Style** | "Prefer functional components" | Consistent patterns |
| **Learning Goals** | "Master K8s by March" | Personal growth tracking |
| **Session Notes** | "Finish auth tests tomorrow" | Cross-session reminders |

**Characteristics:**
- ☁️ Syncs across all machines automatically
- 👤 Personal to GitHub account
- 🔒 Encrypted at rest
- 💬 Accessible via natural language in chat

### Global Knowledge (~/.alex/)
Local domain knowledge and project learnings. Use for:

| Data | Example | Why Local |
|------|---------|-----------|
| **Domain Expertise** | "How OAuth2 works in our system" | Project-specific, detailed |
| **Patterns (GK-*)** | "Rate limiting implementation" | Searchable, categorized |
| **Insights (GI-*)** | "Fixed N+1 query with eager load" | Timestamped learnings |
| **Session History** | Episodic meditation records | Full context preserved |

**Characteristics:**
- 💾 Local storage, you control the data
- 🔍 Full-text searchable via MCP tools
- 📁 Organized in patterns/ and insights/
- 🔗 Synaptic connections between items

### Decision Matrix

| Question | Copilot Memory | Global Knowledge |
|----------|---------------|------------------|
| Is this personal preference? | ✅ | |
| Is this project know-how? | | ✅ |
| Should it sync to new machines? | ✅ | |
| Does it need full-text search? | | ✅ |
| Is it a learning goal? | ✅ | |
| Is it a pattern/solution? | | ✅ |

### Integration Workflow

```
User learns something → Is it personal? → Copilot Memory
                     → Is it shareable? → Global Knowledge (GI-*)
                     → Is it reusable?  → Global Knowledge (GK-*)
```

**No duplication**: Each piece of information lives in ONE system.

---

## Promotion Candidate Patterns

When scanning project knowledge for promotion candidates, use these patterns to identify high-value content:

### 🎯 Strong Promotion Signals

| Pattern | Description | Example |
|---------|-------------|---------|
| **Cross-project applicability** | Would 3+ other projects benefit? | Error handling strategy that works anywhere |
| **Resolution pattern** | Solved problem with concrete solution | "N+1 query fixed with eager loading" |
| **Hard-won gotchas** | Prevents repeat mistakes | "Jest timers require runAllTimers() after async" |
| **Architecture with rationale** | ADR-style decisions with "why" | "Chose event sourcing because..." |
| **Pipeline/workflow patterns** | Automatable processes | CI/CD template, release flow |
| **Integration patterns** | How systems connect | OAuth flow, API gateway setup |
| **Migration patterns** | Version/format transformations | "Upgrading from v3 to v4 schema" |
| **Schema/format patterns** | Data structures that work | Synapse JSON schema, config templates |

### ❌ Anti-Promotion Signals

| Signal | Why Skip | Example |
|--------|----------|---------|
| **Project-specific config** | Only works in one context | "Our AWS account settings" |
| **Temporary workarounds** | Will be obsolete | "Hack until v2.0 releases" |
| **Personal preferences** | Not generalizable | "I like 4 spaces" |
| **Incomplete/draft content** | Needs validation | Work-in-progress notes |
| **Already in GK** | Avoid duplicates | Check `index.json` first |
| **Too specific names/IDs** | Not portable | Hardcoded team names, repo URLs |

### Automated Scoring (Score ≥5 = Candidate)

The extension evaluates skill files with this scoring:

| Criteria | Points | Detection |
|----------|--------|-----------|
| Has synapses | +3 | Synapse format in content |
| Well-structured (3+ H2 sections) | +2 | `## Section` headings |
| Has tags defined | +1 | `**Tags**: tag1, tag2` |
| Substantial content (>1KB) | +1 | File size |
| Rich content (>5KB) | +2 | File size |
| Has code examples | +2 | Code blocks in content |
| General applicability | +1-3 | Contains: pattern, best practice, guideline, framework, principle, architecture |

**Minimum for auto-promotion**: Score ≥ 5

### Quick Decision Tree

```
Is this knowledge?
├── Personal preference → Copilot Memory (not GK)
├── Project-specific config → Keep in project skills
├── Would I search for this in another project?
│   ├── No → Keep in project skills
│   └── Yes → Continue...
│       ├── Is it a reusable solution? → Pattern (GK-*)
│       └── Is it a timestamped learning? → Insight (GI-*)
```

### Real Examples from Curation

These patterns were identified during cross-project knowledge curation:

**Promoted as Patterns (GK-*):**
- `GK-kill-switch-pattern-protecting-master-alex.md` — Safety mechanism applicable to any critical system
- `GK-synapse-schema-2026-standard.md` — Data format standard for the entire architecture
- `GK-domain-knowledge-azure-synapse-pipeline-.md` — ETL patterns for data engineering

**Promoted as Insights (GI-*):**
- `GI-agent-consolidation-pattern-kiss-merge-2026-02-09.md` — Lesson from merging duplicate agents
- `GI-schema-migration-discrimination-flag-vs-change-2026-02-09.md` — Distinguishing migration types
- `GI-post-upgrade-verification-checklist-2026-02-09.md` — Checklist developed after failed upgrade

### Source Priority for Promotion

When curating from multiple projects:

| Source Type | Priority | Rationale |
|-------------|----------|-----------|
| Master Alex episodic memories | Highest | Core cognitive learnings |
| Production project skill files | High | Battle-tested knowledge |
| Platform heir skill files | Medium | May have implementation-specific details |
| Research/experimental projects | Lower | May not be validated |
| Archive content | Lowest | May be outdated |

### Promotion Workflow Commands

```
@alex /promote                  # Interactive promotion from project DK
@alex /saveinsight              # Quick insight capture
@alex /knowledgestatus          # Check current GK health
@alex /knowledge <query>        # Search before adding (avoid duplicates)
```

---

## Synapses

**Synapse**: [heir-skill-promotion.instructions.md](../../instructions/heir-skill-promotion.instructions.md) (0.9, procedural, bidirectional) — "How skills move from heirs to Master"
**Synapse**: [global-knowledge-curation.instructions.md](../../instructions/global-knowledge-curation.instructions.md) (0.85, procedural, bidirectional) — "Periodic cleanup and implementation"
**Synapse**: [unified-meditation-protocols.prompt.md](../../prompts/unified-meditation-protocols.prompt.md) (0.8, episodic, forward) — "Auto-promotion during meditation"
