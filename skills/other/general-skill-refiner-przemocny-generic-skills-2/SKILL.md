---
name: general-skill-refiner
description: Analyzes and refines agent skills by identifying quality issues, prioritizing fixes (MUST/SHOULD/NICE), gathering user feedback, and implementing improvements. Checks for common problems like time estimates, oversized SKILL.md files, poor structure, redundant content, missing examples, and unclear workflows. Use when reviewing, improving, refactoring, or auditing existing skills. Triggers include "review skill", "improve skill", "refactor skill", "skill quality", "audit skill", "fix skill", "optimize skill", "analyze skill".
---

# General Skill Refiner

## Overview

**Purpose:** Critical analysis and improvement of agent skills

**Approach:**
- Ruthless critique - identify all issues without sugar-coating
- Clear priorities - MUST/SHOULD/NICE to have classification
- Concrete solutions - specific fixes, not just complaints
- User feedback loop - user decides what to fix
- Verify changes - ensure quality after refactoring

**Output:** Improved skill + change report in `.tasks/skill-refactoring-[date]/`

---

## Guidelines

### What Makes a Good Skill

Based on Agent Skills Complete Guide:
- **Description is king** - Most important field for skill triggering
- **Progressive disclosure** - SKILL.md <500 lines, detailed docs in references/
- **Structure > prose** - Numbered steps, bullet points, clear conditionals
- **Only add what LLM doesn't know** - No basic programming tutorials
- **One skill = one domain** - Focused scope, not "everything-tool"
- **Include examples** - Show input → output patterns
- **No time estimates** - Never mention how long things take

### Common Anti-Patterns to Look For

- ❌ **The Encyclopedia** - 5000+ line SKILL.md (should split to references/)
- ❌ **The Everything Bagel** - Skill applies to every task (should be a rule)
- ❌ **The Secret Handshake** - Agent never loads skill (bad description)
- ❌ **The Fragile Skill** - Hardcoded absolute paths (use relative paths)
- ❌ **The Wall of Text** - Unstructured prose (needs headers/lists/steps)
- ❌ **Time Estimates** - Any mention of duration (strictly forbidden)

### Priority Levels

**🔴 PRIORITY 1: MUST FIX** (breaking issues)
- Core guideline violations (time estimates, etc.)
- Structural problems (too long, disorganized)
- Missing critical functionality
- Contradictions or confusion

**🟡 PRIORITY 2: SHOULD FIX** (quality issues)
- Suboptimal workflow
- Redundant content
- Missing helpful features
- Can be simplified

**🟢 PRIORITY 3: NICE TO HAVE** (enhancements)
- Small improvements
- Additional examples
- Minor clarifications

---

## Examples

### Example 1: Identifying Time Estimates Problem

**Skill analyzed:** `code-review`

**Problem found:**
```markdown
Line 45: "This analysis should take about 5-10 minutes"
Line 89: "Quick scan (2-3 minutes)"
```

**Priority:** 🔴 MUST FIX - Core guideline violation

**Fix:** Remove all time references:
```markdown
Line 45: "This analysis covers security, performance, and style"
Line 89: "Quick scan of critical issues"
```

---

### Example 2: Analysis Report Format

**For skill:** `pdf-processor` (1200 lines in SKILL.md)

**Analysis presented to user:**

```
## 🔴 MUST FIX

### 1. SKILL.md Too Long (1200 lines)
**Problem:** Exceeds recommended 500 line limit
**Impact:** Loads unnecessary content into context
**Fix:** Move detailed API docs to references/api-reference.md

### 2. Time Estimates Found
**Problem:** Lines 234, 456, 789 contain time estimates
**Fix:** Remove phrases "takes 2 minutes", "quick 30 second scan"

## 🟡 SHOULD FIX

### 3. Missing Examples Section
**Problem:** No concrete input → output examples
**Fix:** Add examples showing PDF processing workflow

## 🟢 What's Good
- Clear step-by-step workflow
- Good error handling coverage
- Scripts are well-documented
```

---

### Example 3: Before/After Refactoring

**Before:**
```markdown
## How to Use

So basically when you want to process a PDF you should first
check if the file exists and then you know, read it and extract
the text content which might take a few minutes depending on the
size, and then process it according to what the user needs...
```
- Line count: 15 lines of prose
- Structure: Wall of text
- Time estimates: Yes (forbidden)

**After:**
```markdown
## How to Use

**Process PDF files:**

1. Validate PDF exists
2. Extract text using `scripts/extract.py`
3. Parse output for required format
4. Return processed content

**For detailed extraction options, see [references/extraction-guide.md](references/extraction-guide.md)**
```
- Line count: 11 lines
- Structure: Clear numbered steps
- Time estimates: None ✅

---

## Workflow

### Phase 1: Read & Understand

**Cel:** Dogłębnie zrozumieć skill i jego strukturę.

**Kroki:**

1. **Read main SKILL.md:**
   - Zrozum cel i workflow
   - Zmierz długość (wc -l)
   - Zidentyfikuj główne phases

2. **Read wszystkie references:**
   - Sprawdź co jest w references/
   - Zmierz długość każdego pliku
   - Zrozum jak references wspierają main skill

3. **Compare z innymi skillami:**
   - Porównaj długość SKILL.md z innymi skillami
   - Sprawdź total długość references/
   - Zidentyfikuj pattern differences

**Output:** Pełne zrozumienie skilla i jego kontekstu.

### Phase 2: Critical Analysis

**Goal:** Ruthlessly identify all problems and group by priority

**Analysis Checklist:**

Use `references/quality-criteria.md` for complete criteria. Key checks:

**Structure & Length:**
- [ ] SKILL.md line count (target: <500 lines)
- [ ] Total references/ size
- [ ] Clear sections with headers
- [ ] Numbered steps for procedures
- [ ] Bullet points for criteria

**Content Quality:**
- [ ] No time estimates anywhere (NEVER allowed)
- [ ] No "wall of text" sections (needs structure)
- [ ] No redundant content between SKILL.md and references/
- [ ] Examples included (input → output)
- [ ] Only adds what LLM doesn't know

**Description & Triggering:**
- [ ] Description contains specific keywords
- [ ] Description explains WHEN to use
- [ ] Triggers match how users talk about task
- [ ] Not too broad ("everything-tool")

**Workflow & Features:**
- [ ] Clear step-by-step workflow
- [ ] No missing critical features
- [ ] No contradictions or confusion
- [ ] Proper references to supporting files

**For Each Issue Found:**

1. **Identify:** What is the specific problem? (with line numbers)
2. **Classify:** 🔴 MUST / 🟡 SHOULD / 🟢 NICE priority
3. **Explain:** Why is this a problem?
4. **Propose:** Concrete solution (not just "fix this")

**Output:** Complete prioritized list of issues with solutions

### Phase 3: Present & Gather Feedback

**Cel:** Zaprezentować analizę użytkownikowi i zebrać feedback co poprawiać.

**Presentation format:**

```
## 🔴 Główne problemy (MUST FIX)

### 1. **[Problem name]**
**Problem:** [clear description]
**Konkretnie:** [specific examples with line numbers]
**Fix:** [concrete solution]

### 2. **[Problem name]**
...

## 🟡 Średnie problemy (SHOULD FIX)
[...]

## 🟢 Co jest dobre
[List positive aspects - important for balance]

## 💡 Sugestie poprawek

**Priority 1 (MUST fix):**
1. [Fix 1]
2. [Fix 2]

**Priority 2 (SHOULD fix):**
[...]

**Priority 3 (NICE to have):**
[...]
```

**Zapytaj użytkownika:**
- "Zgadzasz się z tą analizą?"
- "Czy są rzeczy z którymi się nie zgadzasz?"
- "Powinienem wprowadzić te poprawki?"
- "Czy jest coś specyficznego co chcesz zachować/zmienić?"

**Listen for:**
- Co użytkownik zgadza się poprawić
- Co użytkownik chce zachować (nawet jeśli jest suboptimal)
- Dodatkowe insights od użytkownika

**Output:** Jasna lista co poprawiać z user approval.

### Phase 4: Refactor

**Cel:** Systematycznie wprowadzić poprawki zgodnie z priorytetami i feedbackiem.

**Refactoring workflow:**

**1. Start with Priority 1 issues:**
- Fix one issue at a time
- Verify każdą zmianę
- Don't break other things

**2. Then Priority 2:**
- Continue systematically
- Show progress

**3. Priority 3 if time:**
- Only if user wants
- Quick wins first

**Refactoring patterns:**

Use `references/refactoring-patterns.md`:
- How to remove time estimates
- How to shorten SKILL.md (move to references)
- How to simplify question flows
- How to add missing features
- How to improve structure

**Best practices:**
- Make atomic changes
- Test that files are valid
- Keep backups (don't worry, git)
- Verify line counts after changes

**Track changes:**
Create log in `.tasks/skill-refactoring-[skill-name]-[date]/changes.md`:
- What was changed
- Why
- Before/after metrics

### Phase 5: Verify & Report

**Cel:** Sprawdzić że wszystko działa i podsumować zmiany.

**Verification checklist:**

✅ **Files are valid:**
- SKILL.md syntax OK
- All references exist
- No broken links

✅ **Metrics improved:**
- SKILL.md shorter (if that was goal)
- No time estimates
- Better structure

✅ **Quality checklist passed:**
- Run through quality-criteria.md
- Wszystkie MUST fixes done
- SHOULD fixes addressed

**Report to user:**

"Gotowe! Poprawiłem skill [name].

**Główne zmiany:**
- [Change 1] - [metric before → after]
- [Change 2] - [metric before → after]
- [Change 3]

**Metryki:**
- SKILL.md: [X] → [Y] linii
- References: [X] → [Y] linii total
- Issues fixed: [Priority 1: X, Priority 2: Y]

**Co zostało poprawione:**
✅ [Issue 1]
✅ [Issue 2]
✅ [Issue 3]

**Co jest lepsze:**
- [Improvement 1]
- [Improvement 2]

Szczegółowy raport w `.tasks/skill-refactoring-[name]-[date]/`"

**Zapytaj:**
- "Czy chcesz żebym przejrzał jeszcze raz?"
- "Czy są dodatkowe poprawki?"

---

## Special Cases

### User disagrees z analizą
- To OK - user ma final say
- Explain reasoning ale respect decision
- Document why recommendation was made
- Proceed with user's preferences

### Skill jest fundamentalnie broken
- Be honest: "Ten skill wymaga przepisania od zera"
- Explain dlaczego
- Zaproponuj: refactor vs rewrite from scratch
- Let user decide

### Multiple skille do poprawy
- Jeden na raz
- Priorytetyzuj który najpierw (ask user)
- Apply learnings z jednego do innych

### Refactoring reveals deeper issues
- Stop and inform user
- "Zauważyłem [deeper issue] - powinienem to też naprawić?"
- Get approval before expanding scope

---

## Quality Checklist

Przed zakończeniem, upewnij się że:

✅ **Analysis was thorough:** Checked all aspects z quality-criteria.md
✅ **Problems prioritized:** Clear MUST/SHOULD/NICE to have
✅ **User feedback gathered:** User approved changes
✅ **Changes implemented:** All agreed fixes done
✅ **No time estimates:** Removed all time references
✅ **Structure improved:** SKILL.md is clear and not too long
✅ **References optimized:** Supporting files helpful, not overwhelming
✅ **Changes documented:** Log created with before/after
✅ **Verification done:** Quality checklist passed
✅ **User satisfied:** Final approval received

---

## Key Reminders

**DO:**
- Be ruthlessly critical in Phase 2
- Prioritize problems clearly (MUST/SHOULD/NICE)
- Give concrete solutions, not just complaints
- Get user feedback before big changes
- Make atomic, verifiable changes
- Document what you changed and why
- Verify quality after refactoring

**DON'T:**
- Don't sugarcoat problems
- Don't fix without understanding
- Don't change everything at once
- Don't skip user feedback
- Don't ignore user preferences
- Don't forget to verify afterwards
- Don't leave broken files

**Twoje podejście:** Jesteś bezwzględnym code reviewer który chce żeby skill był najlepszy jaki może być. Identifikujesz problemy, proponujesz rozwiązania, ale ostatecznie user decyduje co poprawiać.

**Pamiętaj:**
- Skill quality matters - bad skills = bad results
- Be specific - "line 45 has time estimate" not "too many time estimates"
- Priorities are key - fix breaking issues first
- User knows their use case - respect their input
- Document changes - future you will thank you
- Verify everything - broken skill is worse than unchanged skill
