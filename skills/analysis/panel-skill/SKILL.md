---
name: panel
description: >
  Host interactive expert panel discussions on any topic. Dynamically generates
  master-level expert personas, facilitates structured debate using Hegelian
  dialectic patterns, and synthesizes consensus. Use when exploring complex
  topics, making architectural decisions, evaluating trade-offs, or seeking
  diverse expert perspectives. Triggers on "panel discussion", "expert debate",
  "get multiple perspectives", "what would experts say about", "/panel".
---

# Panel Discussion Skill

Generate 3-7 diverse expert personas, facilitate structured debate, and synthesize actionable recommendations.

## Arguments

Parse `$ARGUMENTS`:
- `size:N` → panel size (3-7, default: auto)
- `depth:X` → quick (1 round), standard (2-3), deep (4+)
- `style:X` → collaborative, adversarial, academic
- Remaining text → topic

## Flow

```
COMPLEXITY_CHECK → EXPERT_GENERATION → DISCUSSION → SYNTHESIS → REPORT
      ↓                                     ↑
[5-7: Warn+Offer direct answer]      [Multiple rounds]
```

## Complexity Check

| Score | Action |
|-------|--------|
| 5-7 | Warn: "This may not benefit from panel discussion." Offer [1] Proceed [2] Direct answer |
| 8-11 | Standard panel (3-4 experts, 2 rounds) |
| 12-15 | Deep panel (5-7 experts, 3+ rounds) |

## Expert Generation

**Required archetypes** (every panel):
1. **Contrarian** - challenges consensus, offers alternatives
2. **Synthesizer** - connects perspectives, finds common ground
3. **Specialist** - deep domain expertise, grounds discussion

**Additional**: Optimist, Skeptic, Pragmatist, Theorist

**Panel size by breadth**:
- Narrow (single tech): 3-4 experts
- Medium (cross-functional): 4-5 experts
- Broad (strategic): 5-7 experts

**Diversity score ≥60 required**:
- All 3 required archetypes: +20
- No archetype >30%: +10
- 4+ archetypes: +10
- 2+ domains: +15
- Optimist + Skeptic mix: +15
- User/external perspective: +15

## Discussion Phases

### Phase 1: Opening (Thesis)
```
🎤 Expert (Role): "[Initial position, 3-5 sentences]"
```

### Phase 2: Cross-Examination (Antithesis)
Experts challenge and build. Patterns: Question→Response, Claim→Counter-claim, Challenge→Defense.

**Contrarian protection**: Before any synthesis, ask: "Before we synthesize, [Contrarian], what are we missing?"

### Phase 3: Synthesis
```
📋 Round N Synthesis:
   • Agreement: [point]
   • Tension: [disagreement]
   • Open question: [needs exploration]
```

**Convergence**: End early if all agree or cycling. Extend if major tension unexplored.

## Output Formats

### Panel Header
```
╭─ Panel Discussion: [Topic] ────────────────────────────────╮
│ Experts: [Name] ([Role]), [Name] ([Role]), [Name] ([Role]) │
╰────────────────────────────────────────────────────────────╯
```

### User Menu
```
╭───────────────────────────────────────────────────────────╮
│ [1] Continue  [2] Follow-up  [3] Redirect  [4] Conclude   │
╰───────────────────────────────────────────────────────────╯
```

### Final Report
```
╔═══════════════════════════════════════════════════════════╗
║                    PANEL CONCLUSIONS                       ║
╚═══════════════════════════════════════════════════════════╝

## Executive Summary
[1-2 sentences]

## Consensus Points
1. **[Point]**: [Details]

## Key Trade-offs
- Trade-off: [Description]
- Recommendation: [Action]
- Dissent: [If any]

## Actionable Recommendations
### Immediate (Week 1)
### Short-term (Month 1)

## Dissenting Views
### [Expert]: "[Direct quote]"

## Open Questions
```

## Synthesis Rules

**Labels**: UNANIMOUS | STRONG | MAJORITY | CONTESTED | CONTEXT-DEPENDENT

**Weight by confidence × domain relevance**:
- High + Core: 1.0
- Medium + Adjacent: 0.49
- Low + Outside: 0.16

**Never say**: "Both make valid points" or "It depends" without specifying factors.

## User Commands

| Command | Effect |
|---------|--------|
| Continue | Next round |
| Follow-up | Ask panel a question |
| Redirect | Shift focus |
| Conclude | Generate report |
