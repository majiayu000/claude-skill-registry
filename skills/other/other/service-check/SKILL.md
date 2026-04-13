---
name: service-check
description: "Use to evaluate a service or feature against Downe's 15 principles of good services."
---

# Service Check Skill

Evaluate against Lou Downe's 15 principles.

## Checklist

For each principle, assess: Pass / Partial / Fail / N/A

1. **Easy to find**: Can users find this service without knowing its name?
   - [ ] Discoverable through natural search terms
   - [ ] Linked from logical starting points

2. **Clearly explains its purpose**: Is it immediately clear what this does?
   - [ ] Purpose statement visible without scrolling
   - [ ] Target audience identifiable

3. **Sets expectations**: Do users know what will happen?
   - [ ] Timeline/process visible upfront
   - [ ] Requirements stated before starting

4. **Enables completion**: Can users finish what they came to do?
   - [ ] End-to-end journey works
   - [ ] No organizational barriers blocking completion

5. **Familiar**: Does it work the way users expect?
   - [ ] Uses conventions users know
   - [ ] No surprising behavior

6. **No prior knowledge needed**: Can a new user succeed?
   - [ ] No jargon or acronyms without explanation
   - [ ] No assumed context

7. **Agnostic of org structures**: Are internal boundaries invisible?
   - [ ] Users don't need to know which department handles what
   - [ ] No internal handoffs visible to users

8. **Minimum steps**: Is every step necessary?
   - [ ] No redundant data entry
   - [ ] No unnecessary confirmation steps

9. **Consistent**: Is language/design uniform throughout?
   - [ ] Same terms used for same concepts
   - [ ] Visual patterns consistent

10. **No dead ends**: Is there always a next step?
    - [ ] Error states have recovery paths
    - [ ] Edge cases have guidance

11. **Usable by everyone**: Is it accessible and inclusive?
    - [ ] WCAG 2.1 AA compliant
    - [ ] Works across devices and assistive technologies

12. **Encourages right behaviors**: Does design nudge good outcomes?
    - [ ] No dark patterns (confirmshaming, hidden costs, forced continuity, misdirection, roach motel, trick questions, bait-and-switch)
    - [ ] Default options are the safe/good ones
    - [ ] Behavioral science used to HELP users, not exploit them (Shotton: ethical application)
    - [ ] If dark patterns detected: flag "Dark Pattern Marketing" anti-pattern (see anti-patterns.md)

13. **Responds to change**: Can it adapt?
    - [ ] Handles edge cases gracefully
    - [ ] Can be updated without full rebuild

14. **Explains decisions**: Are automated decisions transparent?
    - [ ] Rejection reasons are clear
    - [ ] Algorithm outputs are explainable

15. **Easy to get human help**: Can users reach a person?
    - [ ] Help/support clearly accessible
    - [ ] Escalation path exists

## When to Run

- **L3 Define** (solution design): Run a lightweight check focusing on principles 1-4, 8, 10, 11. These inform the Four Risks viability dimension — a solution that violates core service principles has viability risk. Feed results into `/ice-score`.
- **L4 Develop→Deliver**: Run the full 15-principle check. Required REVIEW gate (G-V2).
- **L4 Deliver→Complete**: Final validation. Required REVIEW gate.

Running at L3 catches service design issues BEFORE delivery, not after. A solution that can't meet "enable completion" (P4) or "no dead ends" (P10) has a design problem, not just a quality problem.

## Output

```
## Service Check: [Service Name]
| # | Principle | Status | Notes |
|---|-----------|--------|-------|
| 1 | Easy to find | Pass/Partial/Fail | ... |
...
| 15 | Human help | Pass/Partial/Fail | ... |

Score: [X/15 Pass, Y/15 Partial, Z/15 Fail]
Priority fixes: [top 3 items to address]
```

## Theory Citations
- Downe: Good Services (15 principles)
