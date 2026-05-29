---
name: faion-confidence-check
description: "Pre-execution confidence assessment. Validates readiness before spec, design, or implementation. Prevents wrong-direction work. Use before major SDD phases."
user-invocable: false
allowed-tools: Read, Glob, Grep, AskUserQuestion
---

# Confidence Check Skill

**Communication with user: User's language. Documents: English.**

## Purpose

Validate readiness before major SDD phases. Prevents 5-50K tokens of wrong-direction work by spending 100-200 tokens on verification.

**ROI: 25-250x token savings**

## When to Use

- Before writing spec.md (idea validation)
- Before writing design.md (requirements clarity)
- Before creating tasks (design completeness)
- Before executing tasks (implementation readiness)

## Confidence Thresholds

| Score | Action |
|-------|--------|
| ≥90% | ✅ Proceed confidently |
| 70-89% | ⚠️ Present alternatives, clarify gaps |
| <70% | ❌ Stop, ask questions first |

---

## Phase-Specific Checklists

### Pre-Spec Confidence (Idea → Spec)

| Check | Weight | Question |
|-------|--------|----------|
| Problem validated | 25% | Is there evidence people have this problem? |
| Market gap | 25% | Is there room for new solution? |
| Target audience | 20% | Do we know WHO specifically? |
| Value proposition | 15% | Why would they switch/pay? |
| Your fit | 15% | Can you build this? |

**Evidence required:**
- Pain point quotes from Reddit/forums/interviews
- Competitor analysis showing gaps
- User persona with real data

---

### Pre-Design Confidence (Spec → Design)

| Check | Weight | Question |
|-------|--------|----------|
| Requirements clear | 25% | All FR-XX unambiguous? |
| AC testable | 25% | All AC-XX measurable? |
| No contradictions | 20% | Requirements don't conflict? |
| Scope defined | 15% | Clear what's NOT included? |
| Dependencies known | 15% | External systems identified? |

**Evidence required:**
- Spec.md with all sections complete
- No TBD or unclear items
- User has approved spec

---

### Pre-Task Confidence (Design → Tasks)

| Check | Weight | Question |
|-------|--------|----------|
| Architecture decided | 25% | No open technical questions? |
| Patterns established | 25% | Following codebase conventions? |
| No duplicate work | 20% | Checked existing implementations? |
| Dependencies mapped | 15% | Task order clear? |
| Estimates reasonable | 15% | Complexity understood? |

**Evidence required:**
- Design.md approved
- Implementation-plan.md complete
- No TBD in technical decisions

---

### Pre-Implementation Confidence (Task → Code)

| Check | Weight | Question |
|-------|--------|----------|
| Task requirements clear | 25% | Know exactly what to build? |
| Approach decided | 25% | Know HOW to build it? |
| No blockers | 20% | All dependencies available? |
| Tests defined | 15% | Know how to verify? |
| Rollback plan | 15% | Can revert if fails? |

**Evidence required:**
- Task file read and understood
- Related code explored
- No open questions

---

## Workflow

```
1. Identify phase (spec/design/task/impl)
     ↓
2. Run phase-specific checklist
     ↓
3. Calculate confidence score
     ↓
4. Present results with evidence
     ↓
5. Decision:
   - ≥90%: "Proceed"
   - 70-89%: "Clarify these gaps first"
   - <70%: "Stop - answer these questions"
```

## Output Format

```markdown
## Confidence Check: {phase}

### Score: {X}% {emoji}

| Check | Status | Evidence |
|-------|--------|----------|
| {check1} | ✅/⚠️/❌ | {evidence or gap} |
| {check2} | ✅/⚠️/❌ | {evidence or gap} |
...

### Verdict: {Proceed / Clarify / Stop}

{If not proceed:}
### Questions to Answer First
1. {question1}
2. {question2}

### Recommended Actions
- {action1}
- {action2}
```

## Integration Points

Call before:
- `/spec` → pre-spec check
- `/design` → pre-design check
- `faion-make-tasks` → pre-task check
- `/faion-execute-task` → pre-impl check

## Anti-Patterns to Catch

| Pattern | Risk | Action |
|---------|------|--------|
| "I think users want..." | Assumption without evidence | Require user research |
| "Should be easy..." | Underestimated complexity | Require technical spike |
| "Similar to X..." | Missed differences | Require detailed comparison |
| "We can figure it out later" | Deferred decisions | Require decision now |
| "Obviously..." | Hidden assumptions | Make explicit |
