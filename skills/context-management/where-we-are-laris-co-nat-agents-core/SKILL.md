---
name: where-we-are
description: Session awareness - what we're doing now. Use when user asks "now", "where are we", "what are we doing", "status". Quick mode for timeline, deep mode for full context.
---

# /where-we-are - Session Awareness

AI buddy confirms current session state with human.

## Usage

```
/where-we-are           # Quick: timeline + jump tracking
/where-we-are deep      # Full: + bigger picture + pending + connections
/now                    # Alias for /where-we-are
```

## Mode 1: Quick (default)

**AI reconstructs session from memory** — no file reading needed.

```markdown
## 🕐 This Session

| Time | Duration | Topic | Jump |
|------|----------|-------|------|
| HH:MM | ~Xm | First topic | - |
| HH:MM | ~Xm | Second topic | 🌟 spark |
| HH:MM | ongoing | **Now**: Current | ✅ complete |

**🔍 Noticed**:
- [Pattern - energy/mode]
- [Jump pattern: sparks vs escapes vs completions]

**📍 Status**:
- 🔥/🟡/🔴 Energy: [level]
- ⚠️ Loose ends: [unfinished]
- 📍 Parked: [topics we'll return to]

**💭 My Read**: [1-2 sentences]

---
**Next?**
```

## Mode 2: Deep (/where-we-are deep)

Adds bigger picture, pending, and connections.

### Step 1: Gather Context (parallel)

```
1. Current session from AI memory
2. Read latest handoff: ls -t ψ/inbox/handoff/*.md | head -1
3. Git status: git status --short
4. Tracks: cat ψ/inbox/tracks/INDEX.md 2>/dev/null
```

### Step 2: Output Format

```markdown
## 📍 /where-we-are deep

### This Session

| Time | Topic | Jump |
|------|-------|------|
| HH:MM | [Topic] | |
| HH:MM | **Now**: [Current] | |

---

### Bigger Picture

**Came from**: [Last session/handoff summary - 1 line]
**Working on**: [Current thread/goal]
**Thread**: [Larger pattern this connects to]

---

### Pending

| Priority | Item | Source |
|----------|------|--------|
| 🔥 Now | [Current task] | This session |
| 🟠 Soon | [Next up] | Tracks/discussion |
| 🟡 Later | [Backlog] | GitHub/tracks |

---

### Connections

**Pattern**: [What pattern emerged]
**Learning**: [Key insight from session]
**Oracle**: [Related past pattern, if any]

---

**💭 My Read**: [2-3 sentences - deeper reflection]

**Next action?**
```

## Jump Types

| Icon | Type | Meaning |
|------|------|---------|
| 🌟 | **Spark** | New idea, exciting |
| ✅ | **Complete** | Finished, moving on |
| 🔄 | **Return** | Coming back to parked |
| 📍 | **Park** | Intentional pause |
| 🚪 | **Escape** | Avoiding difficulty |

**Healthy session**: Mostly 🌟 sparks and ✅ completes
**Warning sign**: Too many 🚪 escapes = avoidance pattern

## Philosophy

> `/now` = "What time is it?"
> `/where-we-are deep` = "Where are we in the journey?"

---

*"Not just the clock. The map."*

ARGUMENTS: $ARGUMENTS
