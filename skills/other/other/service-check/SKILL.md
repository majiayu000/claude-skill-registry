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
    - [ ] No dark patterns
    - [ ] Default options are the safe/good ones

13. **Responds to change**: Can it adapt?
    - [ ] Handles edge cases gracefully
    - [ ] Can be updated without full rebuild

14. **Explains decisions**: Are automated decisions transparent?
    - [ ] Rejection reasons are clear
    - [ ] Algorithm outputs are explainable

15. **Easy to get human help**: Can users reach a person?
    - [ ] Help/support clearly accessible
    - [ ] Escalation path exists

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
