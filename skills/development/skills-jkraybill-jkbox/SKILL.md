---
name: skills-jkraybill-jkbox
description: 'Version: 2.0.0 (jkbox adaptive edition)'
---

# Skill: AI-Driven Collaboration Health Check

**Status:** active
**Version:** 2.0.0 (jkbox adaptive edition)
**Created:** 2025-11-12 (Session 1)
**Last Updated:** 2025-11-12

---

## Purpose

**AI-DRIVEN ADAPTIVE HEALTH CHECKS** - Not your grandpa's calendar-based 1:1s.

Gordo self-assesses collaboration quality and only asks questions when friction patterns detected. Like good management: "Hey I noticed you struggled with X, let's fix it" beats "It's been 14 days, mandatory check-in time!"

**Assess when needed across:**
1. **Communication** - Shortcuts working? Misunderstandings?
2. **Framework** - Docs helping or hindering?
3. **Fun** - JKLES trends, morale, humor landing
4. **Tech** - Party failures, test issues, recurring bugs
5. **Trust** - Autonomy appropriate? Too restricted/loose?

---

## When to Use

**AI-DRIVEN (BOS Step 12 - Self-Assessment):**

Gordo reviews last 5-10 sessions for friction patterns:
- Communication unclear 2+ times → Ask about shortcuts
- JKLES < 7/10 for 2 sessions → Humor calibration
- Test failures 3+ sessions → Quality workflow
- Party crash occurred → Stress testing protocol
- Trust friction detected → Autonomy adjustment

**IF concerns detected:** Ask up to 5 targeted questions NOW
**ELSE:** Update config.json with future trigger patterns, proceed

**On-demand:**
- Human requests: "health check" or "how are we doing?"
- Before party deployment (stakes = high)

**NOT when:**
- Mid-session focused work
- Human says "skip" or "not now"
- Smooth sailing (don't interrupt momentum)

---

## Process

### Phase 1: BOS Self-Assessment (AI-Driven)

Gordo evaluates collaboration health by reviewing recent patterns:

**Friction indicators:**
- Communication: Repeated clarifications needed, shortcuts misunderstood
- Framework: Docs ignored, prompts skipped, constitution violated
- Fun: JKLES declining, jokes not landing, morale down
- Technical: Recurring bugs, party failures, test issues
- Trust: Gordo asking permission excessively OR steamrolling decisions

**Decision:**
```
IF friction detected:
  → Identify 1-5 targeted questions
  → Ask NOW (don't wait for calendar)
  → Document in config.json healthCheck.triggerHistory

ELSE:
  → Update config.json with future trigger patterns
  → Document smooth session streak
  → Proceed with session work
```

**Example triggers (config.json):**
```json
"futureTriggers": [
  "If 3+ sessions with test failures → quality workflow discussion",
  "If JKLES < 7/10 for 2 sessions → humor calibration",
  "If party crash → stress testing protocol",
  "If communication unclear 2+ times → shortcuts review"
]
```

### Phase 2: Targeted Questions (If Triggered)

**Ask 1-5 specific questions based on detected friction:**

**Communication friction example:**
```
I noticed we had 3 clarification cycles about game modularity in the last 2 sessions.

Questions:
1. Are the "WWGD" variants clear? (WWGD? vs WWGD+ vs WWGD++)
2. Do we need a shortcut for "describe architecture without implementing"?
3. Is the 30-line limit working for mobile readability?
```

**JKLES/Morale friction example:**
```
JKLES has been 6-7/10 for last 3 sessions (down from 9-10 earlier).

Questions:
1. Is humor style drifting? (Too meta? Not meta enough?)
2. Are commit message jokes landing or annoying?
3. Need different comedy references? (Less Conan, more Rick & Morty?)
```

**Technical friction example:**
```
We've had reconnection bugs in 4 of last 5 sessions.

Questions:
1. Should we add dedicated reconnection stress tests?
2. Is TDD workflow working for async/network code?
3. Need separate testing protocol for party scenarios?
```

### Phase 3: Document & Act

**Update config.json:**
```json
{
  "healthCheck": {
    "mode": "ai-driven",
    "lastAssessment": "Session_05",
    "questionsAsked": 3,
    "outcome": "Added 'architecture-only' shortcut, adjusted humor balance",
    "smoothSessionStreak": 0,
    "futureTriggers": [
      "If 3+ sessions with test failures → quality workflow",
      "If JKLES < 7/10 for 2 sessions → humor calibration",
      "If party crash → stress testing"
    ],
    "triggerHistory": [
      {
        "session": "Session_05",
        "trigger": "Communication unclear on modularity",
        "questionsAsked": 3,
        "outcome": "Clarified plugin architecture, added shortcut"
      }
    ]
  }
}
```

**IF smooth sailing:**
```json
{
  "healthCheck": {
    "lastAssessment": "Session_12",
    "smoothSessionStreak": 7,
    "note": "Collaboration quality high, no intervention needed"
  }
}
```

---

## Success Criteria

**AI self-assessment:**
- [ ] Reviewed last 5-10 sessions for patterns
- [ ] Evaluated all 5 friction dimensions
- [ ] Made intelligent trigger decision (ask vs proceed)

**If questions asked:**
- [ ] Questions targeted to specific friction
- [ ] Concrete actions identified
- [ ] config.json updated with trigger history

**If smooth sailing:**
- [ ] config.json updated with smooth streak
- [ ] Future triggers documented
- [ ] No unnecessary interruption

---

## Key Differences from Calendar-Based

**Calendar-based (v1.0):**
- ❌ "It's been 14 sessions, mandatory check-in"
- ❌ Same 4 questions every time
- ❌ Interrupts momentum when unnecessary
- ❌ Misses urgent issues between scheduled checks

**AI-driven adaptive (v2.0 jkbox):**
- ✅ "I noticed friction pattern X, let's address it"
- ✅ Targeted questions (1-5) based on actual issues
- ✅ Only interrupts when value-add detected
- ✅ Catches issues immediately when patterns emerge

**Like good management:** Responsive > Bureaucratic

---

## jkbox Customizations

**Entertainment context:**
- JKLES (JK Laughing Extremity Scale) tracking
- Humor calibration (comedy references, joke density)
- Party failure impact (stakes = social reputation)
- Mobile UX (30-line limit compliance)

**Integration:**
- BOS Step 12 (near-end self-assessment)
- config.json AI-driven trigger tracking
- HUMOR.md for morale patterns
- JOURNAL.md for session quality trends

---

## Version History

### 2.0.0 (2025-11-12 jkbox)
- **MAJOR:** Shifted from calendar-based to AI-driven adaptive
- Added 5-dimension assessment (communication, framework, fun, tech, trust)
- Targeted questions (1-5) instead of fixed 4
- Trigger pattern documentation in config.json
- Smooth session streak tracking
- jkbox humor/morale customizations

### 1.0.0 (2025-10-30 gordo-framework)
- Calendar-based health checks
- 4-dimension fixed assessment
- Scheduled every N sessions

---

**Skill maintained by:** JK + Gordo
**Framework innovation:** AI-driven > calendar-based (v0.9.0+ upstream candidate)
