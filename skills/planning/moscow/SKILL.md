---
name: moscow
description: MoSCoW prioritization categorizing items as Must have, Should have, Could have, or Won't have. Use for scope definition, feature prioritization, or when everything feels equally important.
user-invocable: true
---

# MoSCoW Prioritization

Categorize items into Must have, Should have, Could have, and Won't have for clear scope and priorities.

## Instructions

Take the list of items provided and sort them into MoSCoW categories. Be rigorous about what's truly a "Must"—if the project/goal can still succeed without it, it's not a Must.

### Output Format

**Context**
What are we prioritizing for? What are the constraints (time, budget, capacity)?

**Prioritized List**

### Must Have (Critical)
*Without these, the project fails or is pointless*

- [ ] [Item] — [Why it's a must]
- [ ] [Item] — [Why it's a must]

### Should Have (Important)
*Significantly adds value; painful to omit but project survives*

- [ ] [Item] — [Value it adds]
- [ ] [Item] — [Value it adds]

### Could Have (Nice to Have)
*Desirable if time permits; low impact if cut*

- [ ] [Item] — [Why it's optional]
- [ ] [Item] — [Why it's optional]

### Won't Have (Not This Time)
*Explicitly out of scope; may revisit later*

- [ ] [Item] — [Why it's deferred]
- [ ] [Item] — [Why it's deferred]

**Effort Distribution**

| Category | Items | Est. Effort % |
|----------|-------|---------------|
| Must | X | ≤60% |
| Should | X | ~20% |
| Could | X | ~10% |
| Won't | X | 0% (deferred) |

**Red Flags**
- If Must > 60% of effort: scope may be too large
- If no Won'ts: probably not being honest about constraints
- If everything is Must: priorities haven't been set

**Rationale**
Explain the key trade-offs made and the reasoning behind contentious categorizations.

**Next Step**
What's the first Must item to tackle?

## Guidelines

- Ask "If we shipped without this, would we fail?" for each Must
- Challenge "Musts" that are really "someone really wants this"
- Make Won'ts explicit—avoids scope creep later
- Consider dependencies (a Must might require a "hidden" Must)
- Stakeholder alignment is essential—this isn't just your opinion

$ARGUMENTS
