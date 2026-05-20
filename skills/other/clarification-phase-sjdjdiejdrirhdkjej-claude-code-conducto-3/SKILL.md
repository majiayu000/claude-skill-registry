---
name: clarification-phase
description: Executes the /clarify phase using AskUserQuestion tool to resolve ambiguities through structured questions (≤3), prioritization, and answer integration. Use when spec.md contains [NEEDS CLARIFICATION] markers, when requirements need disambiguation, or when running /clarify command to resolve critical scope/security/UX ambiguities before planning. (project)
---

<objective>
Execute the /clarify phase by resolving critical ambiguities in spec.md through structured questioning (≤3 questions), prioritization, and answer integration. Ensures specifications are concrete and unambiguous before planning phase.
</objective>

<quick_start>
Resolve ambiguities in spec.md using AskUserQuestion tool:

1. Extract [NEEDS CLARIFICATION] markers from spec.md
2. Prioritize using matrix (Critical/High → ask, Medium/Low → assumptions)
3. Call AskUserQuestion with ≤3 questions (batched, multiSelect for subsystems)
4. Receive user answers synchronously
5. Integrate into spec.md, remove all markers
6. Add Clarifications (Resolved) section with deferred assumptions

**Inputs**: spec.md with [NEEDS CLARIFICATION] markers
**Outputs**: Updated spec.md (no markers), clarifications.md (record)
</quick_start>

<prerequisites>
- Spec phase completed (spec.md exists)
- spec.md contains ≥1 [NEEDS CLARIFICATION] marker (if none, skip /clarify)
- Git working tree clean

If clarification count >5, review spec phase quality (too many ambiguities).
</prerequisites>

<workflow>
<step number="1">
**Extract clarification needs**

Read spec.md, find all [NEEDS CLARIFICATION: ...] markers, extract ambiguity context.

```bash
# Count clarifications
grep -c "\[NEEDS CLARIFICATION" specs/NNN-slug/spec.md

# List with line numbers
grep -n "\[NEEDS CLARIFICATION" specs/NNN-slug/spec.md
```

If count = 0, skip /clarify phase.
</step>

<step number="2">
**Prioritize questions**

Categorize each clarification by priority:

- **Critical** (always ask): Scope boundary, security/privacy, breaking changes
- **High** (ask if ambiguous): User experience decisions, functionality tradeoffs
- **Medium** (use defaults): Performance SLAs, technical stack choices
- **Low** (use standards): Error messages, rate limits

Keep only Critical + High priority questions (target: ≤3).

Convert Medium/Low to informed guesses, document as assumptions.

See references/prioritization-matrix.md for detailed categorization rules.
</step>

<step number="3">
**Prepare AskUserQuestion tool call**

For each Critical/High priority clarification, structure as AskUserQuestion parameter:

**AskUserQuestion format**:

```javascript
AskUserQuestion({
  questions: [
    {
      question:
        "spec.md:45 mentions 'dashboard metrics' but doesn't specify which. What should we display?",
      header: "Metrics", // max 12 chars
      multiSelect: false,
      options: [
        {
          label: "Completion only",
          description: "% of lessons finished (2 days, basic insights)",
        },
        {
          label: "Completion + time",
          description:
            "Lessons finished + hours logged (4 days, actionable insights)",
        },
        {
          label: "Full analytics",
          description:
            "Completion + time + quiz scores + engagement (7 days, requires infrastructure)",
        },
      ],
    },
  ],
});
```

**Quality standards**:

- **question**: Full context with spec.md reference (e.g., "spec.md:45 mentions...")
- **header**: Short label ≤12 chars (e.g., "Metrics", "Auth", "Scope")
- **multiSelect**: false for single choice, true for subsystems/features
- **options**: 2-3 concrete choices with impacts in description
- **label**: Concise option name (1-5 words)
- **description**: Implementation cost + value + tradeoffs (1-2 sentences)

Batch related questions (max 3 per AskUserQuestion call).

See references/question-bank.md for 40+ example questions in AskUserQuestion format.
</step>

<step number="4">
**Document deferred assumptions**

For Medium/Low priority questions not asked, prepare assumptions section:

```markdown
## Deferred Assumptions (Using Informed Guesses)

### [Topic]

**Not asked** (Low priority - standard default exists)
**Assumption**: [Concrete default choice]
**Rationale**: [Why this default is reasonable]
**Override**: [How user can override in spec.md]
```

These will be included in clarifications.md record after AskUserQuestion call.
</step>

<step number="5">
**Call AskUserQuestion tool**

Execute AskUserQuestion with batched Critical/High questions:

```javascript
AskUserQuestion({
  questions: [
    {
      question:
        "spec.md:45 mentions 'dashboard metrics'. Which should we display?",
      header: "Metrics",
      multiSelect: false,
      options: [
        { label: "Completion only", description: "2 days, basic insights" },
        {
          label: "Completion + time",
          description: "4 days, actionable insights",
        },
        {
          label: "Full analytics",
          description: "7 days, requires infrastructure",
        },
      ],
    },
    {
      question:
        "spec.md:67 doesn't specify access control model. Which approach?",
      header: "Access",
      multiSelect: false,
      options: [
        {
          label: "Simple (users/admins)",
          description: "2 days, basic permissions",
        },
        {
          label: "Role-based (RBAC)",
          description: "4 days, flexible permissions",
        },
      ],
    },
  ],
});
```

**Batching strategy**:

- Batch 2-3 related questions per call
- Use multiSelect: true for subsystem/feature selection questions
- Use multiSelect: false for single-choice decisions

Tool returns answers object:

```javascript
{
  "Metrics": "Completion + time",
  "Access": "Role-based (RBAC)"
}
```

User can also select "Other" for custom answers.
</step>

<step number="6">
**Integrate answers into spec.md**

Use answers from AskUserQuestion tool response to update spec:

For each answered question:

1. Locate corresponding [NEEDS CLARIFICATION] marker in spec.md
2. Replace with concrete requirement based on selected option
3. Remove marker

Example:

```javascript
// AskUserQuestion returned:
{
  "Metrics": "Completion + time",
  "Access": "Role-based (RBAC)"
}
```

Update spec.md:

```markdown
<!-- Before -->

Dashboard displays student progress [NEEDS CLARIFICATION: Which metrics?]
Users can access dashboard [NEEDS CLARIFICATION: Access control?]

<!-- After -->

Dashboard displays:

- Lesson completion rate (% of assigned lessons finished)
- Time spent per lesson (hours logged)

User access control (role-based):

- Teachers: View assigned students only
- Admins: View all students
- Students: View own progress only
```

Validate integration:

```bash
# Must return 0 (no markers remain)
grep -c "\[NEEDS CLARIFICATION" specs/NNN-slug/spec.md
```

</step>

<step number="7">
**Create clarifications.md record**

Generate specs/NNN-slug/clarifications.md as historical record:

```markdown
# Clarifications for [Feature Name]

**Date**: [timestamp]
**Questions Asked**: 2 (Critical: 1, High: 1)
**Deferred**: 3 assumptions

## Questions & Answers

### Q1: Dashboard Metrics (Critical)

**Question**: spec.md:45 mentions 'dashboard metrics'. Which should we display?
**Options**: Completion only | Completion + time | Full analytics
**Selected**: Completion + time
**Rationale**: Balances actionable insights with implementation cost (4 days vs 7)

### Q2: Access Control (High)

**Question**: spec.md:67 doesn't specify access control model. Which approach?
**Options**: Simple (users/admins) | Role-based (RBAC)
**Selected**: Role-based (RBAC)
**Rationale**: Future-proof for additional roles

## Deferred Assumptions

### Export Format (Low)

**Not asked** - Standard default exists
**Assumption**: CSV format
**Rationale**: Most compatible, industry standard
**Override**: Specify in spec.md if JSON/Excel needed

### Rate Limiting (Low)

**Not asked** - Reasonable default
**Assumption**: 100 requests/minute per user
**Rationale**: Conservative, prevents abuse
**Override**: Specify in spec.md if higher limits needed
```

Add "Clarifications (Resolved)" section to spec.md:

```markdown
## Clarifications (Resolved)

Answered 2 questions on [date]:

1. Dashboard metrics: Completion + time spent (4 days)
2. Access control: Role-based RBAC (future-proof)

Deferred assumptions: Export format (CSV), Rate limiting (100/min)

See clarifications.md for full details.
```

</step>

<step number="8">
**Commit clarifications**

```bash
git add specs/NNN-slug/clarifications.md specs/NNN-slug/spec.md
git commit -m "docs: resolve clarifications for [feature-name]

Answered N questions:
- [Q1 summary]: [Decision]
- [Q2 summary]: [Decision]

Deferred assumptions:
- [Topic]: [Choice] ([reason])

All [NEEDS CLARIFICATION] markers removed
Ready for planning phase"
```

Update state.yaml: `clarification.status = completed`
</step>
</workflow>

<validation>
After clarification phase, verify:

- All [NEEDS CLARIFICATION] markers removed from spec.md
- ≤3 structured questions asked (Critical + High only)
- Medium/Low priorities documented as assumptions
- Answers integrated into spec.md Requirements section
- Clarifications (Resolved) section added to spec.md
- clarifications.md generated with user answers
- state.yaml updated (clarification.status = completed)
- Git commit created with descriptive message
  </validation>

<anti_patterns>
<pitfall name="too_many_questions">
**❌ Don't**: Ask >3 questions per feature (7+ questions for simple feature)
**✅ Do**: Apply prioritization matrix strictly, keep only Critical/High, convert Medium/Low to assumptions

**Why**: Delays workflow, frustrates users, causes analysis paralysis
**Target**: ≤3 questions total after prioritization

**Example** (bad):

```
7 questions for export feature:
1. Export format? (CSV/JSON) → Has default ❌
2. Which fields? → Critical ✅
3. Email notification? → Has default ❌
4. Rate limiting? → Has default ❌
5. Max file size? → Has default ❌
6. Retention period? → Has default ❌
7. Compress files? → Has default ❌
```

Should be:

```
1 question (Critical):
- Which fields to export? (no reasonable default)

6 deferred assumptions:
- Format: CSV (standard)
- Email: Optional (user preference)
- Rate limit: 100/min (reasonable)
- Max size: 50MB (standard)
- Retention: 90 days (compliance standard)
- Compression: Auto >10MB (performance)
```

</pitfall>

<pitfall name="vague_compound_questions">
**❌ Don't**: Ask vague or compound questions
- "What features should dashboard have and how should it look?" (compound - mixes features + design)
- "What should we do about errors?" (too vague, no context, no options)
- "Do you want this to be good?" (subjective, not actionable)

**✅ Do**: Use AskUserQuestion with clear context, 2-3 concrete options, quantified impacts

**Why**: Unclear questions lead to ambiguous answers, require follow-up, waste time

**Example** (good with AskUserQuestion):

```javascript
AskUserQuestion({
  questions: [
    {
      question:
        "spec.md:45 mentions 'progress' but doesn't specify which metrics to display. What should the dashboard show?",
      header: "Metrics",
      multiSelect: false,
      options: [
        {
          label: "Completion only",
          description: "% of lessons finished (2 days, basic insights)",
        },
        {
          label: "Completion + time",
          description:
            "Lessons finished + hours logged (4 days, actionable insights for identifying struggling students)",
        },
        {
          label: "Full analytics",
          description:
            "Completion + time + quiz scores + engagement (7 days, requires analytics infrastructure)",
        },
      ],
    },
  ],
});
```

**Result**: Clear, specific options with quantified impacts - user can make informed decision.
</pitfall>

<pitfall name="missing_spec_integration">
**❌ Don't**: Leave clarifications in separate file without updating spec.md
**✅ Do**: Integrate all answers into spec.md Requirements, remove all [NEEDS CLARIFICATION] markers

**Why**: Planning phase can't proceed without concrete requirements in spec

**Validation**:

```bash
# Must return 0 (no markers remain)
grep -c "\[NEEDS CLARIFICATION" specs/NNN-slug/spec.md
```

</pitfall>

<pitfall name="no_deferred_assumptions">
**❌ Don't**: Skip documenting Medium/Low questions
**✅ Do**: Document all Medium/Low as assumptions with rationale in clarifications.md

**Why**: User doesn't know what defaults were applied, can't override if needed

**Example**:

```markdown
## Deferred Assumptions

### Rate Limiting

**Not asked** (Low priority - reasonable default)
**Assumption**: 100 requests/minute per user
**Rationale**: Prevents abuse, can increase based on usage
**Override**: Specify in spec.md if higher limits needed
```

</pitfall>

<pitfall name="questions_without_options">
**❌ Don't**: Ask open-ended questions without concrete options
- "What should the dashboard show?" (completely open)

**✅ Do**: Provide 2-3 concrete options with quantified impacts

- Options: A/B/C with implementation costs + user value

**Why**: Open-ended answers are hard to integrate into spec, lead to follow-up questions
</pitfall>
</anti_patterns>

<best_practices>
<practice name="structured_format">
Always use AskUserQuestion tool with structured format:

- **question**: Full context with spec.md reference (e.g., "spec.md:45 mentions...")
- **header**: Short label ≤12 chars (e.g., "Metrics", "Auth")
- **options**: 2-3 concrete choices with implementation costs in description
- **multiSelect**: false for single choice, true for subsystems/features

Example:

```javascript
AskUserQuestion({
  questions: [
    {
      question: "spec.md:45 mentions 'metrics'. What should we display?",
      header: "Metrics",
      multiSelect: false,
      options: [
        { label: "Completion only", description: "2 days, basic" },
        { label: "Completion + time", description: "4 days, actionable" },
        { label: "Full analytics", description: "7 days, complex" },
      ],
    },
  ],
});
```

Result: Clear answers, faster decisions, easy spec integration
</practice>

<practice name="prioritized_list">
Categorize all clarifications:
1. Critical → Ask always
2. High → Ask if ambiguous
3. Medium → Document as assumption
4. Low → Document as assumption

Target: ≤3 questions (Critical + High only)

Result: Focused user attention, faster responses, reasonable defaults
</practice>

<practice name="integration_checklist">
After receiving answers from AskUserQuestion:
- [ ] Extract selected options from tool response (answers object)
- [ ] Update spec.md Requirements with concrete details based on selections
- [ ] Remove all [NEEDS CLARIFICATION] markers
- [ ] Create clarifications.md record with questions + answers
- [ ] Add "Clarifications (Resolved)" section to spec.md
- [ ] Document deferred assumptions in clarifications.md
- [ ] Verify `grep "\[NEEDS CLARIFICATION" spec.md` returns 0
- [ ] Commit with descriptive message

Result: Complete spec, ready for planning phase
</practice>
</best_practices>

<success_criteria>
Phase complete when:

- [ ] All [NEEDS CLARIFICATION] markers removed from spec.md (grep returns 0)
- [ ] ≤3 structured questions asked (Critical + High priority only)
- [ ] Medium/Low questions documented as assumptions with rationale
- [ ] User provided answers to all questions
- [ ] Answers integrated into spec.md Requirements section
- [ ] Clarifications (Resolved) section added to spec.md
- [ ] clarifications.md generated with questions + answers
- [ ] Deferred assumptions documented in clarifications.md
- [ ] Git commit created with descriptive message
- [ ] state.yaml updated (clarification.status = completed)
- [ ] spec.md is complete and unambiguous (ready for /plan)
      </success_criteria>

<quality_standards>
**Targets**:

- Question count: ≤3 per feature
- Question clarity: 100% follow structured format (Context → Options → Impact)
- Response integration: 100% (no remaining markers)
- Follow-up questions: <10%
- Time to resolution: ≤2 hours (excluding user response time)

**Good clarifications**:

- ≤3 questions (rigorously prioritized)
- Structured format (Context → Options → Impact → Recommendation)
- Concrete options (2-3 specific choices, not open-ended)
- Quantified impacts (implementation costs + user value)
- Clear recommendations (suggested option with rationale)
- Complete integration (all markers removed from spec)

**Bad clarifications**:

- > 5 questions (didn't prioritize)
- Vague questions ("What should we do?")
- Compound questions (mixing multiple decisions)
- No options (open-ended)
- Missing integration (markers remain in spec)
  </quality_standards>

<troubleshooting>
**Issue**: Too many questions (>3)
**Solution**: Apply prioritization matrix strictly, convert Medium/Low to assumptions, batch related questions

**Issue**: Questions are vague
**Solution**: Use AskUserQuestion format with clear context + spec reference, 2-3 concrete options, quantified impacts in description

**Issue**: User can't choose between options
**Solution**: Add more context to question text, include cost/benefit tradeoffs in option descriptions

**Issue**: AskUserQuestion header too long
**Solution**: Keep header ≤12 chars (e.g., "Metrics" not "Dashboard Metrics Scope")

**Issue**: [NEEDS CLARIFICATION] markers remain after integration
**Solution**: Extract answers from AskUserQuestion response, update spec.md for each marker, run validation check

**Issue**: Planning phase blocked due to ambiguity
**Solution**: Spec integration incomplete, verify answers mapped to spec requirements correctly
</troubleshooting>

<references>
See references/ for:
- Prioritization matrix (Critical/High/Medium/Low categorization rules)
- Question bank (40+ example questions in AskUserQuestion format)
- Execution workflow (detailed step-by-step with bash commands)
- Question quality examples (good vs bad questions with AskUserQuestion)

See templates/ for:

- clarification-template.md (clarifications.md record template)
  </references>
