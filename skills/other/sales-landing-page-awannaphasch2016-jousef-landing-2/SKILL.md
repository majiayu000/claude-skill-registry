---
name: sales-landing-page
description: Create high-converting B2B landing pages using psychological section sequencing. Use when building landing pages for services, agencies, consultants, or B2B products. Provides 14-section framework optimized for conversion psychology.
depends_on:
  - template-cloning  # For technical implementation
  - frontend-design   # For visual polish (optional)
complements:
  - config-driven-content  # Content architecture pattern
---

# Sales Landing Page Skill

Build landing pages that convert using proven psychological sequencing.

## When to Use This Skill

- Building landing pages for B2B services or products
- Creating pages for agencies, consultants, coaches
- Designing high-ticket offer pages
- Any page where **conversion matters more than aesthetics**

## Core Principle

**Section sequence matters more than section content.**

The psychological journey from stranger to buyer follows predictable patterns:
1. Capture attention (Hero)
2. Build trust (Social proof)
3. Create emotional safety (Remove blame)
4. Mirror their problem (Recognition)
5. Amplify consequences (Cost of inaction)
6. Disqualify alternatives (False solutions)
7. Present your approach (Differentiator)
8. Show outcomes (Results)
9. Explain the how (Process)
10. Prove it works (Testimonials)
11. Create urgency (ROI/Decision pressure)
12. Handle objections (FAQ)
13. Close (Final CTA)

**Each section sets up the next.** Skip a section = break the chain.

---

## Quick Decision Tree

```
Is this a landing page? ─────────────────────────────────────┐
         │                                                   │
         ▼                                                   │
Is conversion the goal? ──────┬──────────────────────────────┤
         │                    │                              │
         ▼                    ▼                              │
    YES: Use this skill   NO: Use frontend-design            │
                              for aesthetics                 │
                                                             │
                              NO: Not this skill ◄───────────┘
```

---

## Files in This Skill

| File | Purpose |
|------|---------|
| **SECTION-FRAMEWORK.md** | 14-section structure with psychology rationale |
| **COPYWRITING-PRINCIPLES.md** | Tone, framing, psychological tactics |
| **CHECKLIST.md** | Pre-launch conversion review |

---

## Section Framework Overview

| # | Section | Psychology | Must Accomplish |
|---|---------|------------|-----------------|
| 1 | Hero | Attention + Position | Clear value prop in 3 seconds |
| 2 | Trust Strip | Credibility anchor | Specific numbers, not vague claims |
| 3 | Emotional Reframe | Remove self-blame | "It's not your fault" safety |
| 4 | Problem Mirror | Recognition | "This is exactly me!" moment |
| 5 | Consequences | Cost of inaction | Make NOT buying painful |
| 6 | False Solutions | Disqualify alternatives | "I tried that, didn't work" |
| 7 | Core Differentiator | Why you're different | Architecture vs execution distinction |
| 8 | Outcomes | Tangible results | Concrete before/after |
| 9 | Implementation Areas | Scope clarity | What's included |
| 10 | Process | How it works | 3-step simplicity |
| 11 | Social Proof | Testimonials | Company logos + quotes |
| 12 | ROI/Urgency | Decision pressure | Cost-per-day of inaction |
| 13 | FAQ | Objection handling | Top 5-7 objections |
| 14 | Final CTA | Close | Single clear action |

**See SECTION-FRAMEWORK.md for detailed requirements.**

---

## Key Copywriting Principles

### Tone: High-Conviction Consulting

```
DON'T: "We might be able to help you improve..."
DO: "Your margins are bleeding. Here's why."
```

### Problem-Agitate-Solve (PAS)

1. **Problem**: Name their pain specifically
2. **Agitate**: Show consequences of ignoring it
3. **Solve**: Present your approach as the logical answer

### False Alternative Disqualification

Before presenting your solution, **disqualify what they've already tried**:

```
"You've probably tried:
- Hiring more people (margins got worse)
- Adding tools (complexity increased)
- Piecemeal automation (created new problems)

None of these address the root cause..."
```

**See COPYWRITING-PRINCIPLES.md for complete tactics.**

---

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| **template-cloning** | Use for implementation mechanics |
| **frontend-design** | Use for visual polish after content is solid |
| **config-driven-content** | Structure content.ts around these 14 sections |

**Recommended workflow**:
1. Use `sales-landing-page` to define content strategy
2. Use `template-cloning` to set up technical structure
3. Use `frontend-design` for visual refinement

---

## Anti-Patterns

### 1. Aesthetics Before Psychology

```
WRONG: "Let's make it look beautiful first"
RIGHT: "Let's nail the psychological sequence, then polish"
```

### 2. Generic Hero

```
WRONG: "We help businesses grow"
RIGHT: "More margin. More capacity. Without hiring."
```

### 3. Skipping Problem Mirror

```
WRONG: Hero → Solution → CTA
RIGHT: Hero → Trust → Blame-removal → Problem → Consequences → Solution → CTA
```

### 4. Weak Objection Handling

```
WRONG: FAQ with 3 generic questions
RIGHT: FAQ addressing the 5-7 actual objections preventing purchase
```

---

## Checklist Reference

Before launching, run through **CHECKLIST.md** to verify:

- [ ] All 14 sections present in correct order
- [ ] Each section accomplishes its psychological goal
- [ ] Copywriting follows high-conviction tone
- [ ] Social proof uses specific numbers
- [ ] CTA appears 3+ times throughout page
- [ ] Mobile experience maintains psychological flow

---

## Related Resources

- **SECTION-FRAMEWORK.md** - Detailed 14-section breakdown
- **COPYWRITING-PRINCIPLES.md** - Writing tactics
- **CHECKLIST.md** - Pre-launch verification
- **template-cloning skill** - Technical implementation
- **frontend-design skill** - Visual polish
- **docs/guides/config-driven-content.md** - Content architecture
