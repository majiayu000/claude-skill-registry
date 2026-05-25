---
name: achievements
description: "Steam-style achievement system with XP, levels, streaks, and skill trees. Gamifies the development workflow. 25 achievements across 5 categories."
---

# Achievement System

Steam-style gamification for the development workflow. Earn XP by coding, fixing bugs, shipping features, and collaborating with agents. Level up, maintain streaks, and unlock achievements across 5 skill trees.

## XP Level Thresholds

| Level | XP Required | Title |
|-------|-------------|-------|
| 1 | 0 | Apprentice |
| 2 | 100 | Developer |
| 3 | 300 | Engineer |
| 5 | 500 | Senior Engineer |
| 10 | 1000 | Staff Engineer |
| 20 | 3000 | Principal Engineer |
| 50 | 10000 | Legendary |

## Streak System

Consecutive days of coding activity multiply XP earned:

| Streak | Multiplier |
|--------|-----------|
| 1-2 days | 1.0x |
| 3-6 days | 1.25x |
| 7-13 days | 1.5x |
| 14-29 days | 2.0x |
| 30+ days | 3.0x |

Missing a day resets the streak to 0.

## Skill Trees

### Tree 1: Code Warrior

Achievements for writing and shipping code.

**First Blood** (10 XP)
- Description: Complete your first code review
- Unlock: First time a commit or diff is reviewed in a session
- Badge: Sword icon

**Speed Demon** (25 XP)
- Description: Fix a bug in under 2 minutes from identification to resolution
- Unlock: Bug-fix tool sequence completes in < 120 seconds
- Badge: Lightning bolt

**Polyglot** (50 XP)
- Description: Work in 3 or more programming languages in a single session
- Unlock: Edit files with 3+ distinct language extensions in one session
- Badge: Globe

**Marathon Runner** (100 XP)
- Description: Sustain an 8-hour coding session without stopping
- Unlock: Session active for 8+ hours (tracked via tool call timestamps)
- Badge: Running figure

**Perfectionist** (50 XP)
- Description: All tests pass on the very first run after a feature implementation
- Unlock: Test suite passes immediately after the first Write/Edit sequence with no retries
- Badge: Gold star

### Tree 2: Bug Slayer

Achievements for hunting and eliminating bugs.

**Bug Whisperer** (25 XP)
- Description: Fix 5 bugs in a single session
- Unlock: 5 bug-fix tool sequences detected in one session
- Badge: Magnifying glass

**The Exterminator** (75 XP)
- Description: Fix 25 bugs across your lifetime
- Unlock: Cumulative bugs-fixed counter reaches 25
- Badge: Skull

**Regression Hunter** (40 XP)
- Description: Catch a bug introduced in the last 24 hours before it ships
- Unlock: Bug identified and fixed that was introduced in recent session
- Badge: Net

**Flaky Tamer** (35 XP)
- Description: Stabilize a flaky test that was failing intermittently
- Unlock: A previously failing test now passes consistently across 3 runs
- Badge: Anchor

**Zero to Hero** (60 XP)
- Description: Reduce error count from 10+ to 0 in a single session
- Unlock: Session starts with 10+ errors, ends with 0
- Badge: Phoenix

### Tree 3: Architecture Master

Achievements for system design and planning.

**Architect's Vision** (50 XP)
- Description: Create an implementation plan with 10 or more steps
- Unlock: Plan document written with 10+ numbered steps or tasks
- Badge: Blueprint

**The Refactorer** (45 XP)
- Description: Reduce a file from 300+ lines to under 200 lines without losing functionality
- Unlock: File shrinks by 100+ lines in a single edit session
- Badge: Scissors

**Dependency Auditor** (30 XP)
- Description: Audit and clean up project dependencies in one session
- Unlock: package.json or requirements.txt modified to remove 3+ entries
- Badge: Package box

**API Architect** (55 XP)
- Description: Design and implement a REST or GraphQL API with 5+ endpoints
- Unlock: 5+ route or resolver definitions written in one session
- Badge: Cloud diagram

**The Modularizer** (40 XP)
- Description: Split a monolithic file into 3+ focused modules
- Unlock: One file becomes 3+ new files in a refactoring session
- Badge: Puzzle piece

### Tree 4: Security Guardian

Achievements for security-conscious development.

**Security Hawk** (30 XP)
- Description: Identify a security vulnerability during review
- Unlock: Security review flags a CRITICAL or HIGH severity finding
- Badge: Shield with eye

**Secret Keeper** (20 XP)
- Description: Catch and remove a hardcoded credential before it commits
- Unlock: Credential-deny hook triggers and the file is subsequently fixed
- Badge: Lock

**Input Validator** (25 XP)
- Description: Add Zod or schema validation to an unvalidated input
- Unlock: Zod schema or validation logic added to an API handler or form
- Badge: Checklist

**Dependency Guardian** (35 XP)
- Description: Identify and update a dependency with a known CVE
- Unlock: CVE-flagged dependency version bumped in package.json
- Badge: Shield with checkmark

**The Auditor** (80 XP)
- Description: Complete a full security audit with no CRITICAL findings
- Unlock: security-reviewer agent completes a full sweep and returns clean
- Badge: Gold shield

### Tree 5: Team Player

Achievements for collaboration, mentoring, and cross-agent work.

**The Mentor** (75 XP)
- Description: An agent's error triggers cross-training that updates the full team's knowledge
- Unlock: Canavar cross-training propagates a learning from one agent to all others
- Badge: Teacher at board

**Night Owl** (15 XP)
- Description: Write code after midnight local time
- Unlock: Tool call timestamp is between 00:00 and 04:00 local time
- Badge: Owl

**The Reviewer** (20 XP)
- Description: Complete 10 code reviews across your lifetime
- Unlock: Cumulative commits-reviewed counter reaches 10
- Badge: Magnifying glass over code

**Streak Master** (50 XP)
- Description: Maintain a 7-day coding streak
- Unlock: streak field reaches 7 in achievements.json
- Badge: Fire

**Knowledge Hoarder** (65 XP)
- Description: Store 20 learnings in the memory system across your lifetime
- Unlock: Cumulative learnings-stored counter reaches 20
- Badge: Brain

## Achievement State File

Achievements are tracked in `~/.claude/achievements.json`:

```json
{
  "xp": 350,
  "level": 5,
  "streak": 7,
  "lastActive": "2026-04-08",
  "unlocked": {
    "first-blood": { "unlockedAt": "2026-04-01T10:00:00Z", "xp": 10 },
    "bug-whisperer": { "unlockedAt": "2026-04-05T14:22:00Z", "xp": 25 }
  },
  "progress": {
    "bugs-fixed": 3,
    "commits-reviewed": 12,
    "tests-passed": 45,
    "learnings-stored": 8,
    "session-bugs-fixed": 1,
    "session-languages": ["ts", "py"],
    "session-start": "2026-04-08T09:00:00Z"
  }
}
```

## Leaderboard (Team Usage)

When multiple developers use the same vibecosystem config, achievements can be shared via a leaderboard file at `~/.claude/team-leaderboard.json`. Each entry includes:

```json
{
  "entries": [
    {
      "name": "batuhan",
      "xp": 1250,
      "level": 10,
      "streak": 14,
      "unlockedCount": 18,
      "topAchievement": "Legendary Streak"
    }
  ],
  "updatedAt": "2026-04-08T12:00:00Z"
}
```

Rankings are sorted by XP descending. Ties are broken by streak length.

## Integration Points

- **achievement-tracker.ts** (PostToolUse hook): Detects events and awards XP in real time
- **canavar-cross-review**: Triggers "The Mentor" achievement on cross-training events
- **session-analytics**: Provides session duration for "Marathon Runner"
- **credential-deny**: Triggers "Secret Keeper" progress when a credential is blocked
- **passive-learner**: Increments the learnings-stored counter for "Knowledge Hoarder"
