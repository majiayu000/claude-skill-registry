---
name: Thanos Management
description: System maintenance, memory queries, and pattern analysis. USE WHEN user mentions system, memory, patterns, history, past conversations, what did I, or meta-level system questions.
---

# Thanos Management Skill

## System Overview
Thanos is Jeremy's external prefrontal cortex - managing tasks, tracking commitments, surfacing patterns, and providing total recall across all life domains.

## Core Components
- **State/**: Current state (focus, commitments, waiting-for)
- **History/**: All past sessions, logs, decisions
- **Memory/**: Vector store for semantic search
- **Skills/**: Domain expertise and workflows
- **Agents/**: Specialized personas (Ops, Coach, Health, Strategy)
- **Inbox/**: Mobile capture landing zone

## Workflow Routing
- System maintenance → Workflows/SystemMaintenance.md
- Memory queries → Workflows/MemoryQuery.md
- Pattern analysis → Workflows/PatternAnalysis.md

## Memory System
- **Storage**: ChromaDB for vector embeddings
- **Collections**: conversations, commitments, decisions, daily_logs, learnings
- **Query**: Natural language search across all history

### Memory Query Examples
- "What did I decide about X?"
- "When did I last talk about Y?"
- "What patterns do I have around Z?"
- "What commitments have I made to Ashley?"
- "What were my energy levels like last week?"

## Pattern Detection
The system watches for:
- Recurring avoidance behaviors
- Energy patterns (best times, crash patterns)
- Commitment follow-through rates
- Client interaction patterns
- Relationship maintenance gaps

## System Health Checks
- [ ] State files current? (updated today)
- [ ] Inbox empty? (processed)
- [ ] Memory indexed? (recent sessions captured)
- [ ] Commitments reviewed? (nothing stale)
- [ ] Weekly review done? (this week)

## Maintenance Tasks

### Daily
- Process Inbox/
- Update State/Today.md
- Log to History/DailyLogs/

### Weekly
- Full weekly review
- Pattern analysis
- Memory cleanup if needed
- State file refresh

### Monthly
- Archive old sessions
- Review and prune commitments
- System performance check
- Backup Memory/

## Troubleshooting
- **Memory not finding things**: Check if sessions are being indexed
- **Patterns not surfacing**: Need more history data
- **State feels stale**: Run SystemMaintenance workflow
- **Inbox overflowing**: Schedule processing time
