---
name: heuristic-evaluation
description: Conduct heuristic evaluations - Nielsen's 10 heuristics, severity ratings, expert review methodology, cognitive walkthrough, and usability inspection.
allowed-tools: Read, Glob, Grep, Task
---

# Heuristic Evaluation

Conduct expert usability reviews using established heuristics and evaluation frameworks.

## When to Use This Skill

Use this skill when:

- **Heuristic Evaluation tasks** - Working on conduct heuristic evaluations - nielsen's 10 heuristics, severity ratings, expert review methodology, cognitive walkthrough, and usability inspection
- **Planning or design** - Need guidance on Heuristic Evaluation approaches
- **Best practices** - Want to follow established patterns and standards

## MANDATORY: Skill Loading First

Before answering ANY heuristic evaluation question:

2. Use Nielsen Norman Group and established UX methodology
3. Base all guidance on validated evaluation practices

## Nielsen's 10 Usability Heuristics

### 1. Visibility of System Status

The system should always keep users informed about what is going on, through appropriate feedback within reasonable time.

**Check for:**

- Loading indicators during operations
- Progress bars for multi-step processes
- Status messages after actions
- Real-time validation feedback
- Clear indication of current state

**Examples:**

| Good | Bad |
|------|-----|
| Spinner during form submission | Page freezes with no feedback |
| "3 of 5 steps complete" | Multi-step form with no progress |
| "Saved successfully" toast | Silent save with no confirmation |

### 2. Match Between System and Real World

The system should speak the users' language, with words, phrases, and concepts familiar to the user.

**Check for:**

- Plain language, not jargon
- Familiar metaphors and icons
- Logical information order
- Cultural appropriateness
- Domain-appropriate terminology

**Examples:**

| Good | Bad |
|------|-----|
| "Save" button | "Persist to datastore" |
| Shopping cart icon | Abstract database icon |
| "Your order" | "Transaction #38291" |

### 3. User Control and Freedom

Users often choose system functions by mistake and need a clearly marked "emergency exit" to leave the unwanted state.

**Check for:**

- Undo/redo functionality
- Cancel buttons in workflows
- Easy navigation back
- Exit from modal dialogs
- Esc key support

**Examples:**

| Good | Bad |
|------|-----|
| Undo after delete | Immediate permanent deletion |
| "Cancel" in forms | Only "Submit" available |
| X to close modal | Click outside only |

### 4. Consistency and Standards

Users should not have to wonder whether different words, situations, or actions mean the same thing.

**Check for:**

- Consistent terminology
- Uniform visual design
- Standard interaction patterns
- Platform conventions
- Predictable layouts

**Examples:**

| Good | Bad |
|------|-----|
| All buttons look like buttons | Inconsistent button styles |
| Same action, same location | "Save" in different places |
| Standard icons (gear = settings) | Custom icons without labels |

### 5. Error Prevention

Even better than good error messages is a careful design which prevents a problem from occurring.

**Check for:**

- Confirmation for destructive actions
- Input constraints/validation
- Default safe options
- Clear disabled states
- Contextual help

**Examples:**

| Good | Bad |
|------|-----|
| "Are you sure you want to delete?" | Immediate delete on click |
| Date picker (not free text) | Ambiguous date format entry |
| Grayed out unavailable options | Error after selection |

### 6. Recognition Rather Than Recall

Minimize the user's memory load by making objects, actions, and options visible.

**Check for:**

- Visible options/menus
- Recently used items
- Autocomplete/suggestions
- Clear labels
- Contextual information

**Examples:**

| Good | Bad |
|------|-----|
| Dropdown with options | Must type exact value |
| "Recent searches" | Empty search box |
| Labels on form fields | Placeholder-only inputs |

### 7. Flexibility and Efficiency of Use

Accelerators—unseen by the novice user—may often speed up the interaction for the expert user.

**Check for:**

- Keyboard shortcuts
- Customization options
- Power user features
- Batch operations
- Quick actions

**Examples:**

| Good | Bad |
|------|-----|
| Ctrl+S to save | Must click menu > Save |
| Drag-and-drop + click | Drag-and-drop only |
| "Select all" checkbox | Must select items one by one |

### 8. Aesthetic and Minimalist Design

Dialogues should not contain information which is irrelevant or rarely needed.

**Check for:**

- Clean, uncluttered interface
- Progressive disclosure
- Essential information first
- Appropriate whitespace
- Clear visual hierarchy

**Examples:**

| Good | Bad |
|------|-----|
| Key info prominent | Wall of text |
| "Show more" for details | Everything visible at once |
| Clean forms | 50-field forms on one page |

### 9. Help Users Recognize, Diagnose, and Recover from Errors

Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution.

**Check for:**

- Plain language errors
- Specific problem identification
- Constructive solutions
- Clear next steps
- Error location indication

**Examples:**

| Good | Bad |
|------|-----|
| "Email format invalid. Example: <name@example.com>" | "Invalid input" |
| Error shown next to field | All errors at top of page |
| "Try again" or "Contact support" | Just an error message |

### 10. Help and Documentation

Even though it is better if the system can be used without documentation, it may be necessary to provide help and documentation.

**Check for:**

- Contextual help
- Searchable documentation
- Task-focused help
- Tooltips for complex features
- Onboarding for new users

**Examples:**

| Good | Bad |
|------|-----|
| Tooltip on hover | No explanation for icons |
| Inline help text | Separate help document only |
| "What's this?" links | Users must figure it out |

## Severity Ratings

### 4-Point Severity Scale

| Rating | Severity | Definition | Action |
|--------|----------|------------|--------|
| **0** | Not a problem | I don't agree this is a usability problem | None needed |
| **1** | Cosmetic | Cosmetic problem only; fix if time | Low priority |
| **2** | Minor | Minor usability problem; fix low priority | Medium priority |
| **3** | Major | Major usability problem; important to fix | High priority |
| **4** | Catastrophic | Usability catastrophe; must fix before release | Critical/blocker |

### Severity Calculation

Consider three factors:

| Factor | Question | Levels |
|--------|----------|--------|
| **Frequency** | How often does the problem occur? | Rare / Occasional / Frequent |
| **Impact** | How serious when it occurs? | Low / Medium / High |
| **Persistence** | Can users overcome it easily? | Easy / Moderate / Difficult |

```csharp
public class SeverityAssessment
{
    public required Frequency Frequency { get; init; }
    public required Impact Impact { get; init; }
    public required Persistence Persistence { get; init; }

    public Severity CalculatedSeverity => (Frequency, Impact, Persistence) switch
    {
        (Frequency.Frequent, Impact.High, Persistence.Difficult) => Severity.Catastrophic,
        (Frequency.Frequent, Impact.High, _) => Severity.Major,
        (_, Impact.High, Persistence.Difficult) => Severity.Major,
        (Frequency.Frequent, Impact.Medium, _) => Severity.Major,
        (Frequency.Occasional, Impact.Medium, _) => Severity.Minor,
        (Frequency.Rare, Impact.Low, _) => Severity.Cosmetic,
        _ => Severity.Minor
    };
}

public enum Frequency { Rare, Occasional, Frequent }
public enum Impact { Low, Medium, High }
public enum Persistence { Easy, Moderate, Difficult }
public enum Severity { Cosmetic = 1, Minor = 2, Major = 3, Catastrophic = 4 }
```

## Evaluation Process

### Step 1: Planning

```markdown
## Heuristic Evaluation Plan

**Product/Feature:** [Name]
**Evaluators:** [List 3-5 evaluators]
**Heuristics:** Nielsen's 10 (or custom set)
**Scope:** [Pages/flows to evaluate]
**Timeline:** [Dates]

### Evaluation Sessions
| Evaluator | Session 1 | Session 2 |
|-----------|-----------|-----------|
| [Name 1] | [Date/Time] | [Date/Time] |
| [Name 2] | [Date/Time] | [Date/Time] |

### Materials
- [ ] Heuristics reference sheet
- [ ] Issue logging template
- [ ] Access to product/prototype
- [ ] Screen recording (optional)
```

### Step 2: Individual Evaluation

Each evaluator reviews independently:

1. **First pass** - Explore freely, note initial impressions
2. **Second pass** - Systematic review against each heuristic
3. **Document issues** - Log each problem found

### Step 3: Issue Logging

```csharp
public class HeuristicIssue
{
    public Guid Id { get; init; }
    public required string Location { get; init; }
    public required string Description { get; init; }
    public required int HeuristicNumber { get; init; }
    public required string HeuristicName { get; init; }
    public required Severity Severity { get; init; }
    public string? Screenshot { get; init; }
    public string? Recommendation { get; init; }
    public Guid EvaluatorId { get; init; }
}
```

### Issue Template

```markdown
## Issue: [Short Title]

**Location:** [Page/screen/component]
**Heuristic:** #[N] - [Heuristic Name]
**Severity:** [0-4]

### Description
[What is the problem?]

### Evidence
[Screenshot or description of what user sees]

### Impact
[How does this affect users?]

### Recommendation
[Suggested fix]
```

### Step 4: Consolidation

Merge findings from all evaluators:

1. Remove duplicates
2. Aggregate severity ratings
3. Group by heuristic or location
4. Prioritize for remediation

```csharp
public class ConsolidatedIssue
{
    public Guid Id { get; init; }
    public required string Location { get; init; }
    public required string Description { get; init; }
    public required int HeuristicNumber { get; init; }
    public required List<Severity> IndividualRatings { get; init; }
    public Severity AverageSeverity =>
        (Severity)Math.Round(IndividualRatings.Average(s => (int)s));
    public int EvaluatorCount => IndividualRatings.Count;
    public required string Recommendation { get; init; }
}
```

## Report Template

```markdown
# Heuristic Evaluation Report

## Executive Summary

**Product:** [Name]
**Evaluation Date:** [Date]
**Evaluators:** [Names]
**Total Issues Found:** [N]

### Issues by Severity
| Severity | Count |
|----------|-------|
| Catastrophic (4) | [N] |
| Major (3) | [N] |
| Minor (2) | [N] |
| Cosmetic (1) | [N] |

### Issues by Heuristic
| Heuristic | Count |
|-----------|-------|
| #1 Visibility of System Status | [N] |
| #2 Match with Real World | [N] |
| ... | ... |

---

## Detailed Findings

### Catastrophic Issues

#### Issue 1: [Title]
- **Location:** [Where]
- **Heuristic:** #[N] - [Name]
- **Severity:** 4 (Catastrophic)
- **Evaluators:** [N]/[Total] identified

**Description:**
[Detailed description]

**Screenshot:**
[Image]

**Impact:**
[Effect on users]

**Recommendation:**
[How to fix]

---

[Continue for each issue, grouped by severity]

---

## Recommendations

### Immediate Action (Severity 4)
1. [Action item]
2. [Action item]

### High Priority (Severity 3)
1. [Action item]
2. [Action item]

### Medium Priority (Severity 2)
1. [Action item]

---

## Methodology

This evaluation followed Nielsen's heuristic evaluation methodology with [N] independent evaluators. Each evaluator conducted two passes through the interface, documenting issues against the 10 usability heuristics. Findings were consolidated and severity ratings averaged.

---

## Appendices

### A: Heuristics Reference
[Full heuristics definitions]

### B: Raw Findings by Evaluator
[Individual evaluator notes]
```

## Cognitive Walkthrough

### Alternative Inspection Method

Cognitive walkthrough focuses on learnability for new users completing specific tasks.

### Walkthrough Questions

At each step of a task, ask:

1. **Will the user try to achieve the right effect?**
   - Is the goal obvious?
   - Does the user know what to do?

2. **Will the user notice that the correct action is available?**
   - Is the option visible?
   - Is it labeled understandably?

3. **Will the user associate the correct action with the effect?**
   - Does the label match expectation?
   - Is the mapping logical?

4. **If the correct action is performed, will the user see progress?**
   - Is feedback provided?
   - Does the system confirm success?

### Walkthrough Template

```markdown
## Cognitive Walkthrough: [Task Name]

**Task:** [What user is trying to accomplish]
**User Profile:** [Who is this user?]
**Starting Point:** [Where does the task begin?]

### Step 1: [Action]
| Question | Answer | Issue? |
|----------|--------|--------|
| Will user try to achieve right effect? | [Y/N/Maybe] | [Issue if no] |
| Will user notice correct action? | [Y/N/Maybe] | [Issue if no] |
| Will user associate action with effect? | [Y/N/Maybe] | [Issue if no] |
| Will user see progress? | [Y/N/Maybe] | [Issue if no] |

**Notes:** [Additional observations]

### Step 2: [Action]
[Continue pattern...]

---

## Summary

**Success Likelihood:** [High/Medium/Low]
**Key Barriers:**
1. [Barrier 1]
2. [Barrier 2]

**Recommendations:**
1. [Improvement 1]
2. [Improvement 2]
```

## Extended Heuristics

### Additional Heuristics (Beyond Nielsen's 10)

| Heuristic | Description |
|-----------|-------------|
| **Accessibility** | Usable by people with disabilities |
| **Privacy & Security** | Users feel their data is safe |
| **Personalization** | Adapts to user preferences |
| **Memorability** | Easy to remember how to use |
| **Satisfaction** | Pleasant, enjoyable experience |
| **Efficiency** | Tasks completed with minimal effort |
| **Learnability** | Easy to learn for new users |

### Platform-Specific Heuristics

#### Mobile Heuristics

- Touch targets ≥44px
- Reachable with one hand
- Works offline
- Respects system settings
- Appropriate for context

#### Web Application Heuristics

- Fast load times
- Works across browsers
- Responsive design
- URL reflects state
- Bookmark/share support

## Checklist: Heuristic Evaluation

### Planning

- [ ] Scope defined (pages/flows)
- [ ] Evaluators identified (3-5)
- [ ] Heuristics selected
- [ ] Access to product arranged
- [ ] Schedule set

### Evaluation

- [ ] First pass completed (exploration)
- [ ] Second pass completed (systematic)
- [ ] Issues logged with severity
- [ ] Screenshots captured
- [ ] Recommendations noted

### Consolidation

- [ ] All evaluator findings collected
- [ ] Duplicates merged
- [ ] Severity ratings averaged
- [ ] Issues prioritized
- [ ] Report drafted

### Reporting

- [ ] Executive summary written
- [ ] Issues documented with evidence
- [ ] Recommendations provided
- [ ] Methodology described
- [ ] Stakeholders briefed

## Related Skills

- `usability-testing` - User-based evaluation
- `accessibility-planning` - Accessibility-specific review
- `design-system-planning` - Consistency evaluation
- `user-research-planning` - Research method selection
