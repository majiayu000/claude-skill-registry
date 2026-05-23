---
name: checkpointing
description: |
  Save full session context: git history, CLI consultations, Agent Teams activity,
  and discover reusable skill patterns — all in one run. No flags needed.
  Run at session end, after major milestones, or when you want to capture learnings.
metadata:
  short-description: Full session checkpoint with skill pattern discovery
---

# Checkpointing — セッションの全記録とパターン発見

**セッションの全活動を記録し、再利用可能なパターンを発見する。毎回全部やる。**

## What It Does (Every Time)

```
/checkpointing
    ↓
┌─────────────────────────────────────────────────────────────┐
│  1. Collect Everything                                       │
│     ├── git log (commits, file changes, line stats)          │
│     ├── CLI logs (Codex/Gemini consultations)                │
│     ├── Agent Teams activity (tasks, teammates, messages)    │
│     └── Design decisions (.claude/docs/DESIGN.md changes)    │
│                                                              │
│  2. Generate Checkpoint                                      │
│     → .claude/checkpoints/YYYY-MM-DD-HHMMSS.md              │
│                                                              │
│  3. Update Session History                                   │
│     → CLAUDE.md (cross-session persistence)                  │
│                                                              │
│  4. Discover Skill Patterns                                  │
│     → Subagent analyzes checkpoint                           │
│     → Suggests reusable skills                               │
│     → User reviews and approves                              │
└─────────────────────────────────────────────────────────────┘
```

## Usage

```bash
# Everything. No flags needed.
/checkpointing

# Optional: only look at recent work
/checkpointing --since "2026-02-08"
```

## What Gets Captured

### Git Activity

- Commits (hash, message, date)
- File changes (created, modified, deleted + line counts)
- Branch information

### CLI Consultations

- Codex consultations (prompt, success/failure)
- Gemini researches (prompt, success/failure)

### Agent Teams Activity

- Team composition (Lead + Teammates, roles)
- Shared task list state (completed, in-progress, pending)
- File ownership per teammate
- Communication patterns (who messaged whom, about what)
- Team effectiveness signals (tasks completed vs stuck, file conflicts)

### Teammate Work Logs

- Each Teammate's work log from `.claude/logs/agent-teams/{team-name}/{teammate}.md`
- Contains: Summary, Tasks Completed, Files Modified, Key Decisions, Communication with Teammates, Issues Encountered
- Written by each Teammate upon completing all assigned tasks
- Only present when Agent Teams were used (`/startproject`, `/team-implement`, `/team-review`)

### Design Decisions

- Changes to `.claude/docs/DESIGN.md` since last checkpoint
- New entries in Key Decisions table

## Checkpoint Format

```markdown
# Checkpoint: 2026-02-08 15:30:00 UTC

## Summary
- **Commits**: 12
- **Files changed**: 15 (10 modified, 4 created, 1 deleted)
- **Codex consultations**: 3
- **Gemini researches**: 2
- **Agent Teams sessions**: 1 (3 teammates)
- **Tasks completed**: 8/10

## Git History

### Commits
- `abc1234` feat: redesign startproject for Opus 4.6
- `def5678` feat: add team-implement skill
...

### File Changes
**Created:**
- `.claude/skills/team-implement/SKILL.md` (+180)
...

**Modified:**
- `CLAUDE.md` (+40, -25)
...

## CLI Consultations

### Codex (3 consultations)
- ✓ Design: Architecture for Agent Teams integration
- ✓ Debug: Task dependency resolution
- ✗ Review: (timeout)

### Gemini (2 researches)
- ✓ Research: Agent Teams best practices
- ✓ Research: Library comparison for httpx vs aiohttp

## Agent Teams Activity

### Team: project-planning
**Composition:**
- Lead: Claude (orchestration)
- Researcher: Gemini-powered (external research)
- Architect: Codex-powered (design decisions)

**Task List:**
- [x] Research library options (Researcher)
- [x] Design module architecture (Architect)
- [x] Validate API constraints (Researcher)
- [x] Finalize implementation plan (Architect)

**Communication Patterns:**
- Researcher → Architect: 3 messages (library constraints)
- Architect → Researcher: 2 messages (additional research requests)

**Effectiveness:**
- All tasks completed
- No file conflicts
- 2 design iterations triggered by research findings

## Teammate Work Logs

### Team: project-planning

#### researcher
*Source: `.claude/logs/agent-teams/project-planning/researcher.md`*

# Work Log: Researcher
## Summary
Researched httpx library constraints and API patterns for the new API client module.
## Tasks Completed
- [x] Research libraries: httpx supports HTTP/2 via h2 dependency
- [x] Find documentation: httpx connection pool defaults to 100
## Communication with Teammates
- → Architect: httpx connection pool limit of 100, HTTP/2 requires h2
- ← Architect: Requested HTTP/2 multiplexing research

#### architect
*Source: `.claude/logs/agent-teams/project-planning/architect.md`*

# Work Log: Architect
## Summary
Designed API client module architecture with HTTP/2 support.
## Design Decisions
- Use httpx[http2] for multiplexed connections: reduces latency for parallel requests
## Codex Consultations
- Connection pool sizing strategy: Codex recommended dynamic pool based on load
## Communication with Teammates
- → Researcher: Request HTTP/2 multiplexing research
- ← Researcher: httpx supports HTTP/2 via h2

## Design Decisions (New)
- Agent Teams for Research ↔ Design (bidirectional)
- Gemini role narrowed to external info + multimodal

## Skill Pattern Suggestions

### Pattern 1: Research-Design Iteration (Confidence: 0.85)
**Evidence:** Researcher and Architect exchanged findings 5 times, each
exchange refined the design. This back-and-forth is a repeatable pattern.

**Suggested skill:** Already captured as /startproject Phase 2.

### Pattern 2: Parallel File-Isolated Implementation (Confidence: 0.75)
**Evidence:** 3 implementers worked on separate modules with zero conflicts.
Module boundaries were defined by directory ownership.

**Suggested skill:** Already captured as /team-implement.

---
*Generated by checkpointing skill*
```

## Session History Update

Each checkpoint also appends a concise summary to CLAUDE.md:

```markdown
## Session History

### 2026-02-08
- 12 commits, 15 files changed
- Codex: 3 consultations (design, debug, review)
- Gemini: 2 researches (agent teams, library comparison)
- Agent Teams: 1 session (3 teammates, 8/10 tasks completed)
- New skills: /team-implement, /team-review
- Key decisions: Agent Teams for parallel work, Gemini role narrowed
```

This persists across sessions — new sessions load CLAUDE.md and see what happened before.

## Skill Pattern Discovery

The checkpoint is automatically analyzed to find reusable patterns:

**What it looks for:**
- Sequences of commits forming logical workflows
- File change patterns (e.g., test + implementation together)
- CLI consultation sequences (research → design → implement)
- Agent Teams coordination patterns (team composition, task sizing)
- Multi-step operations that could be templated

**Output:** Skill suggestions with confidence scores. High-confidence patterns (>= 0.8) that don't match existing skills are presented to the user for approval.

## Execution Flow

```
/checkpointing
    │
    ├─ 1. Run checkpoint.py (collects git + CLI + teams data)
    │     → Generates .claude/checkpoints/YYYY-MM-DD-HHMMSS.md
    │
    ├─ 2. Update CLAUDE.md with session summary
    │
    └─ 3. Spawn subagent for skill pattern analysis
          → Reads checkpoint file
          → Identifies reusable patterns
          → Reports suggestions to user
          → User approves → new skills created in .claude/skills/
```

## When to Run

| Timing | Why |
|--------|-----|
| セッション終了前 | 全活動を記録、次セッションへの引き継ぎ |
| `/team-implement` 完了後 | チーム活動パターンを捕捉 |
| `/team-review` 完了後 | レビューパターンを捕捉 |
| 大きな設計決定後 | 決定のコンテキストを永続化 |
| 繰り返しパターンを感じた時 | スキル化の発見チャンス |

## Notes

- チェックポイントは `.claude/checkpoints/` に蓄積される（`.gitignore` 済み）
- ログファイル自体は変更されない（読み取りのみ）
- スキル提案は必ずユーザーがレビューしてから採用すること
- Agent Teams のデータは `~/.claude/teams/` と `~/.claude/tasks/` から収集
