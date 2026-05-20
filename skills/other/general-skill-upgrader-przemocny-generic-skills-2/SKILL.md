---
name: general-skill-upgrader
description: Analyzes agent skills to understand their business purpose and proposes functional enhancements. Identifies opportunities for new features, workflow improvements, better automation, enhanced user experience, and smarter integrations. Presents 1-2 upgrade options per run for iterative enhancement. Use when evolving, enhancing, or expanding skill capabilities. Triggers include "upgrade skill", "enhance skill", "improve skill functionality", "add features to skill", "evolve skill", "make skill better", "skill enhancement", "ulepsz skill", "jak mogę rozwinąć funkcjonalność skilla", "dodaj możliwości do skilla".
---

# General Skill Upgrader

## Overview

**Purpose:** Strategic enhancement and functional evolution of agent skills

**Approach:**
- Understand business goal - what problem does this skill solve?
- Identify opportunities - 22 types of potential upgrades
- Present options - show 1-2 most valuable upgrades per run
- User decides - pick what matters most right now
- Implement & verify - make it better, confirm it works
- Iterative process - run again for next round of upgrades

**Output:** Enhanced skill + upgrade report in `.tasks/skill-upgrade-[skill-name]-[date]/`

**Key Difference from Refiner:**
- **Refiner** = fix problems (quality issues, bugs, violations)
- **Upgrader** = add value (new capabilities, better UX, smarter workflow)

---

## Guidelines

### What Makes a Good Upgrade

**Value-Driven:**
- Solves real user pain point
- Makes workflow smoother/faster/easier
- Reduces mental overhead
- Enables new use cases
- Improves reliability

**Practical:**
- Actually implementable (not fantasy features)
- Fits skill's core purpose (not scope creep)
- Worth the added complexity
- User will actually use it

**Clear Win:**
- Measurable improvement (fewer steps, less friction, better output)
- Doesn't break existing functionality
- Easy to understand benefit
- Aligns with skill's business goal

### The 22 Types of Upgrades

Complete details in [references/upgrade-types.md](references/upgrade-types.md).

**Workflow Enhancements (1-4):**
1. Add new features - Extend capabilities within domain
2. Simplify workflow - Reduce steps, eliminate redundancy
3. Parallel execution - Run independent steps simultaneously
4. Checkpoints - Resume long processes from interruption

**Quality & Reliability (5-8):**
5. Better edge cases - Handle unusual scenarios gracefully
6. Early validation - Catch problems before end of workflow
7. Self-checking - Skill verifies its own output quality
8. Error recovery - Smart rollback, retry, or repair mechanisms

**Automation & Intelligence (9-12):**
9. Automate manual steps - Replace human intervention with logic
10. Context-awareness - Adapt to project type, user preferences, history
11. Learning from history - Use previous runs to improve suggestions
12. Smart defaults - Intelligent choices based on patterns

**User Experience (13-16):**
13. Better briefing - Smarter questions, fewer iterations
14. Interactive choices - Option menus instead of open questions
15. Progress visibility - Clear feedback on what's happening
16. Dry-run mode - Preview changes before committing

**Integration & Output (17-20):**
17. Tool integration - Better use of available tools (bash, git, etc.)
18. Reusable outputs - Results that feed into other skills
19. Better reports - More actionable, clearer insights
20. Batch processing - Handle multiple items efficiently

**Documentation (21-22):**
21. More examples - Concrete use cases, templates, patterns
22. Best practices - Guidance on optimal usage

---

## Examples

### Example 1: Adding Dry-Run Mode

**Skill analyzed:** `code-refactor`

**Current state:** Makes changes directly to files

**Upgrade opportunity:**
- **Type:** #16 Dry-run mode
- **Problem:** Users nervous about automatic changes
- **Solution:** Add `--preview` mode that shows diffs without applying
- **Value:** User confidence, safety net, teaching tool

**Implementation:**
```markdown
## Options

**Preview mode (recommended for first run):**
1. Analyze code and generate refactoring plan
2. Show diffs of proposed changes
3. Ask: "Apply these changes?"

**Direct mode:**
1. Analyze and apply changes immediately
2. Report what was changed
```

---

### Example 2: Adding Self-Checking

**Skill analyzed:** `documentation-writer`

**Current state:** Writes docs, user reviews manually

**Upgrade opportunity:**
- **Type:** #7 Self-checking
- **Problem:** Common doc issues not caught automatically
- **Solution:** Built-in quality checks before presenting to user
- **Value:** Higher quality output, fewer user corrections

**Implementation:**
```markdown
## Phase 4: Quality Verification (NEW)

Before presenting documentation, run self-checks:

**Completeness:**
- [ ] All public APIs documented
- [ ] All parameters explained
- [ ] Return values specified

**Clarity:**
- [ ] No jargon without explanation
- [ ] Examples for complex features
- [ ] Clear section structure

If checks fail → Fix issues → Re-check → Present to user
```

See [references/examples.md](references/examples.md) for more detailed scenarios.

---

## Workflow

### Phase 1: Read & Understand Business Goal

**Cel:** Dogłębnie zrozumieć PO CO ten skill istnieje.

**Kroki:**

1. **Read SKILL.md:**
   - Co skill robi (actions)
   - Po co skill istnieje (business purpose)
   - Jaki problem użytkownika rozwiązuje
   - Jaki jest obecny workflow

2. **Read references/:**
   - Jakie supporting materials są
   - Jakie decyzje były już podjęte
   - Czy są TODO/known limitations

3. **Understand user experience:**
   - Jak user używa tego skilla
   - Które kroki są manualne vs automatyczne
   - Gdzie są friction points
   - Co mogłoby być prostsze

4. **Identify core purpose:**
   - One sentence: "Ten skill istnieje żeby [business goal]"
   - Success criteria: Jak poznać że skill dobrze wykonał swoją robotę?
   - Boundaries: Co jest in-scope vs out-of-scope?

**Output:** Jasne zrozumienie biznesowego celu i obecnego stanu skilla.

---

### Phase 2: Identify Upgrade Opportunities

**Goal:** Find 3-5 most valuable potential upgrades across 22 categories

**Analysis Process:**

For each upgrade type (1-22), ask:
1. **Is this relevant?** Does skill have potential in this area?
2. **What's the opportunity?** Specific improvement that could be made
3. **What's the value?** How does it make skill better at its business goal?
4. **What's the effort?** Simple change vs major rewrite
5. **Priority?** High/Medium/Low based on value vs effort

**Use [references/upgrade-types.md](references/upgrade-types.md) for detailed criteria.**

**Look for:**
- Repeated manual steps → automation opportunity
- User confusion points → UX improvement opportunity
- Common failures → reliability upgrade opportunity
- Limited scope → feature expansion opportunity
- Generic approach → context-awareness opportunity

**Red flags (avoid):**
- Scope creep - feature doesn't match skill's core purpose
- Over-engineering - adds complexity without clear value
- Speculative - "might be useful someday" features
- Redundant - capability already exists elsewhere

**For each opportunity found:**

Document:
```markdown
## [Upgrade Name]

**Type:** #[number] [type name]
**Current state:** [what skill does now]
**Opportunity:** [what could be improved]
**Value:** [why this matters for business goal]
**Implementation:** [high-level approach]
**Effort:** Low/Medium/High
**Priority:** High/Medium/Low
```

**Output:** 3-5 concrete upgrade opportunities ranked by priority

---

### Phase 3: Present & Gather Feedback

**Cel:** Pokazać najlepsze opcje i dać userowi wybór.

**Presentation format:**

```markdown
# Upgrade Opportunities for [skill-name]

## 🎯 Skill's Business Goal

[One sentence core purpose]

## 📊 Current State Analysis

**Co działa dobrze:**
- [Good aspect 1]
- [Good aspect 2]

**Gdzie można ulepszać:**
- [Opportunity area 1]
- [Opportunity area 2]

## 🚀 Top Upgrade Options

### Option 1: [Upgrade Name] ⭐

**Type:** [Type name from 22 types]

**Problem it solves:**
[Clear description of current limitation]

**How it works:**
[Konkretny opis co by się zmieniło]

**Value:**
- [Benefit 1]
- [Benefit 2]

**Example:**
[Before/after comparison or concrete scenario]

**Effort:** [Low/Medium/High]

---

### Option 2-5: [Continue similarly]

---

## 💡 Recommendation

Based on value vs effort, I recommend:
1. **[Option X]** - [brief why]
2. **[Option Y]** - [good second choice]
```

**Concrete example (file-analyzer → batch processing):**

```markdown
## 🎯 Business Goal: Analyze files for quality/security issues

## 📊 Current State
Good: Clear per-file reports | Can improve: Must run 150x separately (slow)

## 🚀 Option 1: Batch Processing Mode ⭐
**Type:** #20 Batch processing
**Problem:** 150 separate invocations with repeated setup
**Solution:** Process multiple files at once with shared setup
**Value:** 10x faster, aggregate insights, single report
**Example:** Before: 150 commands | After: 1 command processes all
**Effort:** Medium

## 💡 Recommendation: Option 1 - highest impact for medium effort
```

**Ask user:**

"Które ulepszenia chcesz żebym zaimplementował? Wybierz 1-2 z powyższych opcji.

Możesz też:
- Zaproponować własne ulepszenie
- Poprosić o więcej szczegółów
- Powiedzieć że żadna nie pasuje"

**Listen for:**
- Które opcje user wybiera (max 2 per run)
- Czy user ma modyfikacje do propozycji
- Czy user widzi inne ulepszenia
- Czy user chce zobaczyć więcej opcji

**Output:** 1-2 wybrane ulepszenia z user approval.

---

### Phase 4: Implement Upgrades

**Cel:** Wprowadzić wybrane ulepszenia systematycznie i bezpiecznie.

**Implementation workflow:**

1. **Plan implementation:**
   - Co dokładnie trzeba zmienić (files, sections)
   - W jakiej kolejności (dependencies)
   - Jak zweryfikować że działa

2. **Implement first upgrade:**
   - Make changes to SKILL.md
   - Update references/ if needed
   - Add examples if relevant
   - Keep changes atomic and clear

3. **Verify first upgrade:**
   - Read changed files to confirm
   - Check that workflow makes sense
   - Ensure no broken references
   - Validate markdown syntax

4. **Implement second upgrade (if chosen):**
   - Same careful process
   - Ensure integration with first upgrade
   - No conflicts or contradictions

5. **Final integration check:**
   - Both upgrades work together
   - Workflow is coherent
   - No redundancy introduced
   - Overall skill is better

**Implementation patterns:**

Use [references/implementation-patterns.md](references/implementation-patterns.md) for detailed guidance on:
- Adding new features
- Improving UX
- Adding automation
- Better error handling
- Each of the 22 upgrade types

**Track changes:**

Create `.tasks/skill-upgrade-[skill-name]-[date]/implementation.md`:
```markdown
# Implementation Log

## Upgrade 1: [Name]

**Changes made:**
- [File] line [X]: [change description]
- [File]: Added new section [name]

**Before:** [snippet]
**After:** [new version]
**Rationale:** [why]

## Upgrade 2: [Name]
[Same structure]
```

**Output:** Upgraded skill with both enhancements implemented.

---

### Phase 5: Verify & Report

**Cel:** Potwierdzić że ulepszenia działają i komunikować rezultat.

**Verification checklist:**

✅ **Files are valid:**
- SKILL.md syntax correct
- All references exist
- Links work
- No broken markdown

✅ **Upgrades implemented:**
- Feature 1 fully integrated
- Feature 2 fully integrated
- Both work together harmoniously
- No contradictions

✅ **Quality maintained:**
- No time estimates introduced
- Structure clear
- Examples helpful
- Workflow logical

✅ **Business goal better served:**
- Skill more effective at core purpose
- User experience improved
- Value clearly increased

**Report to user:**

```markdown
# Skill Upgraded: [skill-name]

## ✅ Upgrades Implemented

### 1. [Upgrade Name]
**What changed:** [description]
**Where:** [files/sections]
**Value:** [how it helps]

### 2. [Upgrade Name]
[same structure]

## 📈 Improvements

**Before:** [key limitations]
**After:** [how it's better now]
**Example:** [scenario showing improvement]

## 🎯 Business Goal Impact

[How upgrades make skill better at its core purpose]

## 📝 Details

Full implementation log in `.tasks/skill-upgrade-[name]-[date]/`

## 🔄 Next Steps

Want more upgrades? Run upgrader again.

Remaining opportunities:
- [Option X]
- [Option Y]
```

**Ask:**
- "Czy ulepszenia działają jak oczekiwałeś?"
- "Czy chcesz jakieś modyfikacje?"
- "Czy uruchomić upgrader ponownie?"

---

## Special Cases

**Skill is already excellent:** Say so honestly. Look for minor polish (docs, examples). May not need upgrades.

**Ambitious upgrade:** Be honest about complexity. Break into phases or multiple runs. May need separate skill if different domain.

**Conflicts with design:** Explain why it doesn't fit. Propose alternative or note if it's a Refiner issue instead.

**Multiple ideas same category:** Present best 1-2. Others go to "future opportunities" for next run.

**Reveals bigger issue:** Note it but stay focused. User can address separately.

---

## Quality Checklist

✅ Business goal understood & all 22 types considered
✅ 3-5 valuable options presented, user chose 1-2
✅ Changes verified, no breakage, quality maintained
✅ Value delivered - skill measurably better
✅ Changes documented, user satisfied, can iterate

---

## Key Reminders

**DO:** Understand WHY skill exists. Consider all 22 types. Present clear value. Let user choose 1-2. Verify changes. Enable iteration.

**DON'T:** Confuse with Refiner (fix vs add value). Propose scope creep. Overwhelm with options. Implement without approval. Break functionality. Add complexity without value.

**Approach:** Strategic product manager. Present options, respect choices, deliver improvements.

**Remember:** Better ≠ bigger. Simpler often wins. Listen to user priorities. Business goal is the north star.
