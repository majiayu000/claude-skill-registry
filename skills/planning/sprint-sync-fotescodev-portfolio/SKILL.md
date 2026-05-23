---
name: sprint-sync
description: Multi-perspective project onboarding and sprint briefing. Simulates a cross-functional leadership team (PM, Designer, Architect, Engineer) ramping up on project status. Updates the Current Status section in PROJECT_STATE.md.
---

# Sprint Sync

<role>
You are a **cross-functional leadership simulator** that provides project context from four perspectives: PM (priorities), Design (system health), Architecture (tech debt), and Engineering (recent changes).
</role>

<purpose>
Provide comprehensive project context from four leadership perspectives. Update the Current Status section in `context/PROJECT_STATE.md` to keep context files manageable.
</purpose>

<when_to_activate>
Activate when the user:
- Says "sprint sync", "/sprint-sync", or "sync me up"
- Starts a new session and needs context
- Asks "where are we?" or "what's the status?"
- Wants to understand current priorities
- Says "onboard me" or "catch me up"

**Trigger phrases:** "sprint sync", "sync me up", "status", "where are we", "catch me up", "onboard"
</when_to_activate>

## Invocation Modes

| Command | Mode | Output |
|---------|------|--------|
| `/sprint-sync` | Quick | Summary briefing + status update |
| `/sprint-sync --hardcore` | Full deep dive | All ASCII diagrams + comprehensive analysis |
| `/sprint-sync --deep pm` | PM focus | Roadmap + priorities + blockers |
| `/sprint-sync --deep design` | Design focus | Design system + theme audit |
| `/sprint-sync --deep arch` | Architect focus | Architecture + dependencies |
| `/sprint-sync --deep eng` | Engineer focus | Recent changes + hot files |

---

## Execution Steps

### Phase 0: Gather Context

**Read this file first:**

| File | Extract |
|------|---------|
| `context/PROJECT_STATE.md` | Parts I-V for strategic context, Part VI for session log |

**Run these commands:**

```bash
git log --oneline -10                    # Recent commits
npm run test 2>&1 | tail -20             # Test status
npm run build 2>&1 | tail -10            # Bundle size
```

---

### Phase 1: Generate Briefing

Output the briefing to the user with multi-perspective analysis.

**Quick Mode Output:**
```
## Sprint Sync — [YYYY-MM-DD]

**Status**: [X]% ready | **Bundle**: [X]KB | **Tests**: [X] passing

### PM View
- **Phase**: [current phase]
- **Focus**: [current objective]
- **Blockers**: [P0 items]

### Architect View
- **Tests**: [passing/failing]
- **Bundle**: [size] (target <200KB)
- **Debt**: [top items]

### Engineer View
- **Last 5 commits**: [summary]
- **Working**: [recent wins]
- **Attention**: [blockers]

### Recommended Actions
1. [P0 priority]
2. [P0 priority]
3. [Next item]
```

---

### Phase 2: Update PROJECT_STATE.md

**CRITICAL**: Update the "Current Status" section in `context/PROJECT_STATE.md`.

**Process:**
1. Read current PROJECT_STATE.md
2. Find the `### Current Status` section (in Part VI)
3. Replace the content between `### Current Status` and the next `### Session:` header
4. Write updated file

**Current Status Format:**
```markdown
### Current Status

**Date**: YYYY-MM-DD
**Objective**: [current focus from analysis]
**Bundle**: [X]KB (target <200KB)
**Tests**: [X] passing, [X] failing
**Variants**: [X] active

**Blockers**:
1. [Most critical blocker]
2. [Second blocker if any]

**Recent Wins**:
- [Win 1]
- [Win 2]
- [Win 3]
```

---

### Phase 3: Add Session Entry (if significant work done)

If the sync reveals significant changes since last session, add a new session entry:

```markdown
### Session: [Month Day, Year] — [Brief Title]

**Summary**: [1-2 sentences]

**Changes**:
- [Key change 1]
- [Key change 2]

**Next**: [What to do next]
```

**Rules for session entries:**
- Only add if there are NEW commits since last session
- Keep only last 3 sessions in PROJECT_STATE.md
- Archive older sessions to `docs/history/session-archive.md`

---

## Hardcore Mode (`--hardcore`)

When `--hardcore` flag is present:

1. Run ALL four deep dives (PM, Design, Arch, Eng)
2. Generate ASCII diagrams for visual context
3. Cross-reference findings between perspectives
4. Generate comprehensive action plan
5. Include risk assessment matrix

**ASCII Diagrams (output to user, not saved):**

```
┌─ ROADMAP STATUS ─────────────────────────────────────────────────────────────┐
│  Phase 1: Foundation    ████████████████████ 100%  COMPLETE                  │
│  Phase 2: Polish        ████████████████████ 100%  COMPLETE                  │
│  Phase 3: Social        ████████████░░░░░░░░  60%  IN PROGRESS               │
│  Phase 4: Performance   ░░░░░░░░░░░░░░░░░░░░   0%  BLOCKED                   │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ PRIORITY MATRIX ────────────────────────────────────────────────────────────┐
│               │  LOW EFFORT   │  MED EFFORT   │  HIGH EFFORT  │              │
│  ─────────────┼───────────────┼───────────────┼───────────────┤              │
│  HIGH IMPACT  │ ★ Code Split  │               │               │              │
│               │ ★ Lazy Load   │               │               │              │
│  ─────────────┼───────────────┼───────────────┼───────────────┤              │
│  MED IMPACT   │               │ Testimonials  │ Scroll Story  │              │
│  ─────────────┼───────────────┼───────────────┼───────────────┤              │
│  LOW IMPACT   │ Dead Code     │ Style Refactor│               │              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## File Locations Reference

| Purpose | Path |
|---------|------|
| **Project State** | `context/PROJECT_STATE.md` |
| **Codebase Docs** | `context/CODEBASE.md` |
| **Design System** | `context/DESIGN.md` |
| **CSS Tokens** | `src/styles/globals.css` |
| **Briefing Archive** | `docs/history/sprint-briefings-archive.md` |
| **Session Archive** | `docs/history/session-archive.md` |

---

## Key Differences from Previous Version

| Before | After |
|--------|-------|
| Append briefings to SOTU Part VIII | Update Current Status section |
| Two files (SOTU + DEVLOG) | One file (PROJECT_STATE.md) |
| Unlimited briefing history | Last 3 sessions only |
| Full briefings saved | Compact status format |

---

## Notes

- Always run tests and build to get current metrics
- Update Current Status, don't append
- Keep session log compact (last 3 sessions only)
- ASCII diagrams are for user display, not saved to file
- Archive old sessions when adding new ones

<skill_compositions>
## Works Well With

- **ultrathink** — Deep analysis of project blockers
- **run-tests** — Get test metrics for status report
- **serghei-qa** — Architect perspective on tech debt
</skill_compositions>
