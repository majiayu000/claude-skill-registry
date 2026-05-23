---
name: pattern-learner
description: Self-improving pattern database. Analyzes successful assets (≥95/100) → extracts effective prompt language → abstracts reusable patterns → updates library automatically.
---

# Pattern-Learner Skill

## Trigger

Asset scores ≥95/100

## Process

1. Diff current prompt vs previous attempts
2. Extract language that drove compliance improvement
3. Abstract reusable pattern from specific instance
4. Tag effectiveness (high/medium/low based on first-attempt success)
5. Update `/docs/northcote-asset-generation-patterns.md`

## Example Learning

**Input:**
- Asset 4 (Wattle + Beetle) scored 96/100 on first attempt
- Previous generic metallic prompts failed (opaque flat paint)
- Success prompt: "Faceted geometric surface with prismatic color shift green→gold→copper"

**Extracted Pattern:**
```markdown
## Pattern: Metallic Iridescence (Asset 4, 96/100)

**Context:** Any metallic insect carapace rendering

**Effective Language:**
"Faceted geometric surface" + "prismatic color shift [color1→color2→color3]"

**Why It Works:**
Specifies viewing angle dependence (not flat metallic paint)

**Effectiveness:** HIGH (validated 1st attempt)

**Apply To:**
- Jewel beetles, metallic spiders, iridescent wings
```

## Pattern Structure

```markdown
## Pattern: [Name] (Asset [N], [Score]/100)

**Context:** [When to use this pattern]

**Effective Language:** [Exact prompt syntax]

**Why It Works:** [Technical explanation]

**Effectiveness:** [HIGH|MEDIUM|LOW]

**Apply To:** [Use cases]

**Avoid:** [Common failure modes]
```

## Integration

**Prompt-Composer:** Queries pattern library before generation
**Flash-Sidekick:** `consult_pro` analyzes prompt diffs for pattern extraction
**Auto-Validator:** Scores trigger pattern learning

## Self-Improvement Loop

1. Asset validates ≥95 → trigger learning
2. Extract patterns → update library
3. Next asset uses updated patterns
4. Success reinforces pattern (effectiveness++)
5. Failure demotes pattern (effectiveness--)

## Database Evolution

**Week 1:** 5 patterns (from Assets 1-2)
**Week 2:** 12 patterns (from Assets 3-6)
**Week 4:** 25+ patterns (self-reinforcing)

**Result:** Each new asset easier than previous due to pattern accumulation

## Efficiency

**Without Learning:**
- Asset 10 requires same trial-error as Asset 1
- No institutional knowledge accumulation

**With Learning:**
- Asset 10 leverages 9 previous successes
- First-attempt success rate increases exponentially

---

*Pattern library evolves with each success. System learns its own best practices.*
