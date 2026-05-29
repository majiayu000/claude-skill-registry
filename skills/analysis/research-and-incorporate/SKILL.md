---
name: research-and-incorporate
version: 1.0.0
description: Research external topics, create comprehensive analysis, determine project
  applicability, and incorporate learnings into Serena and Forgetful memory systems.
  Transforms knowledge into searchable, actionable project context.
license: MIT
model: claude-opus-4-5
metadata:
  timelessness: 8/10
  source: Chesterton's Fence research workflow (Session 203)
---
# Research and Incorporate

Transform external knowledge into actionable, searchable project context through structured research, analysis, and memory integration.

## Quick Start

```text
/research-and-incorporate

Topic: Chesterton's Fence
Context: Decision-making principle for understanding existing systems before changing them
URLs: https://fs.blog/chestertons-fence/, https://en.wikipedia.org/wiki/G._K._Chesterton
```

| Input | Output | Duration |
|-------|--------|----------|
| Topic + Context + URLs | Analysis doc + Serena memory + 5-10 Forgetful memories | 20-40 min |

## Triggers

- `/research-and-incorporate` - Main invocation
- "research and incorporate {topic}" - Natural language
- "study {topic} and add to memory" - Alternative phrasing
- "deep dive on {topic}" - Research focus
- "learn about {topic} for the project" - Project integration focus

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `TOPIC` | Yes | Subject to research (e.g., "Chesterton's Fence") |
| `CONTEXT` | Yes | Why this matters to the project |
| `URLS` | No | Comma-separated source URLs |

## Workflow Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: RESEARCH (BLOCKING)                                    │
│ • Check existing knowledge (Serena + Forgetful)                 │
│ • Fetch URLs with quote extraction                              │
│ • Web search for additional context                             │
│ • Synthesize: principles, frameworks, examples, failure modes   │
├─────────────────────────────────────────────────────────────────┤
│ Phase 2: ANALYSIS DOCUMENT (BLOCKING)                           │
│ • Write 3000-5000 word analysis to .agents/analysis/            │
│ • Include: concepts, frameworks, applications, failure modes    │
│ • Verify: 3+ examples, 3+ failure modes, 2+ relationships       │
├─────────────────────────────────────────────────────────────────┤
│ Phase 3: APPLICABILITY (BLOCKING)                               │
│ • Map integration points: agents, protocols, memory, skills     │
│ • Propose applications with effort estimates                    │
│ • Prioritize: High/Medium/Low based on project goals            │
├─────────────────────────────────────────────────────────────────┤
│ Phase 4: MEMORY INTEGRATION (BLOCKING)                          │
│ • Create Serena project memory with cross-references            │
│ • Create 5-10 atomic Forgetful memories (importance 7-10)       │
│ • Link memories to related concepts (auto + manual)             │
├─────────────────────────────────────────────────────────────────┤
│ Phase 5: ACTION ITEMS                                           │
│ • Create GitHub issue if implementation work identified         │
│ • Document in session log                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Quality Gates (BLOCKING)

| Gate | Requirement | Phase |
|------|-------------|-------|
| Research depth | Core principles + frameworks + 3 examples | 1 |
| Analysis length | 3000-5000 words minimum | 2 |
| Concrete examples | 3+ with context and outcomes | 2 |
| Failure modes | 3+ anti-patterns with corrections | 2 |
| Relationships | 2+ connections to existing concepts | 2 |
| Memory atomicity | Each memory <2000 chars, ONE concept | 4 |
| Memory count | 5-10 Forgetful memories created | 4 |

## Verification Checklist

After completion, verify:

- [ ] Analysis document exists at `.agents/analysis/{topic-slug}.md`
- [ ] Analysis is 3000-5000 words with concrete examples
- [ ] Applicability section documents integration opportunities
- [ ] Serena memory created with cross-references
- [ ] 5-10 Forgetful memories created (importance 7-10)
- [ ] Memories linked to related concepts
- [ ] Each memory is atomic (<2000 chars, one concept)
- [ ] Action items documented (issue or next steps)

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Superficial research | Surface definitions miss actionable insights | Dig into frameworks, examples, failure modes |
| Missing applicability | Research without integration is wasted | Every insight must show HOW it applies |
| Non-atomic memories | >2000 chars or multiple concepts pollutes graph | ONE concept per memory |
| Disconnected knowledge | Orphaned artifacts aren't discoverable | Link memories to related concepts |
| Template over-compliance | Forcing irrelevant sections wastes tokens | Organize for the topic, not the template |
| Skipping verification | Quality gates exist for a reason | Verify each phase before proceeding |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `using-forgetful-memory` | Memory creation best practices |
| `encode-repo-serena` | Similar but for codebase analysis |
| `exploring-knowledge-graph` | Navigate created knowledge |
| `memory` | Search and retrieve incorporated knowledge |

## References

| Document | Content |
|----------|---------|
| [workflow.md](references/workflow.md) | Detailed phase workflows with templates |
| [memory-templates.md](references/memory-templates.md) | Forgetful memory structure templates |

## Extension Points

1. **Additional research sources**: Add MCP tools for specialized domains
2. **Custom analysis templates**: Topic-specific document structures
3. **Automated validation**: Scripts to verify memory atomicity
4. **Integration hooks**: Connect to ADR review for architecture topics
