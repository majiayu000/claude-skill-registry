---
name: content-refiner
description: POST-GATE TOOL. Refine verbose content by eliminating redundancy, trimming word count, and strengthening lesson connections. Use ONLY to fix Gate 4 failures.
---

# Content Refiner (The Fixer)

## Purpose
**POST-GATE TOOL.**
Transforms content that **FAILED Gate 4** into passing content.
Focuses on trimming verbosity and fixing continuity.

## When to Use
- **Trigger**: Gate 4 (Acceptance Auditor) returned `[FAIL]`.
- **Goal**: Fix word count OR continuity issues (or both).
- **Key**: Diagnose what failed BEFORE applying fixes.

## CRITICAL: Pre-Refinement Diagnosis

**DO NOT apply fixes blindly.** Gate 4 fails for different reasons requiring different strategies.

### Step 0: Identify What Failed (Mandatory)

Ask the user OR examine the Gate 4 failure message:

| Failure Type | Question | Action |
|--------------|----------|--------|
| **Word Count** | "Is the lesson over the target (typically 1500 words)?" | Calculate exact % to cut |
| **Continuity** | "Does the opening reference the previous lesson?" | Rewrite opening only |
| **Both** | "Word count AND continuity broken?" | Two-phase approach |

**DIAGNOSIS EXAMPLES**:

**Example 1: Word Count Only**
```
Content: 1950 words, Target: 1500
Excess: 450 words
% to cut: (450 / 1950) × 100 = 23%
→ CUT EXACTLY 23%, not generic 15-20%
```

**Example 2: Continuity Only**
```
Opening: "Let's explore this new topic..."
Problem: Doesn't reference Lesson N-1
→ Rewrite opening only; don't cut words
```

**Example 3: Both**
```
Word count: 1950 (23% over)
Opening: Generic, missing prior lesson reference
→ Phase 1: Rewrite opening (identify anchor from Lesson N-1)
→ Phase 2: Cut words to 23% (context-aware)
```

### Step 1: Assess Content Layer (Context-Aware Cutting)

Read the lesson's frontmatter to determine layer:

| Layer | Cutting Strategy |
|-------|-----------------|
| **L1 (Manual)** | Keep foundational explanations; cut elaboration |
| **L2 (AI-Collaboration)** | Keep Try With AI sections (core); cut narrative padding |
| **L3 (Intelligence)** | Keep pattern insights; cut explanatory scaffolding |
| **L4 (Spec-Driven)** | Keep specification details; cut conceptual scaffolding |

---

## The Refinement Procedure (Layer-Aware)

### Phase 1: The Connection Builder (Continuity Fix)

**Do this FIRST if opening is generic.**

**Formula:**
```markdown
In [Previous Lesson], you [SPECIFIC OUTCOME from Lesson N-1].
Now, we will [CONNECT outcome to new goal] by [STRATEGY].
```

**Validation**:
- [ ] Opening references Lesson N-1 by name
- [ ] Specific outcome (not generic "learned about...")
- [ ] Clear connection shows why this lesson matters (builds on N-1)

**After fixing**: Proceed to Fluff Cutter if word count also fails.

### Phase 2: The Fluff Cutter (Word Count Fix)

**Apply layer-specific cuts in this order:**

**FOR ALL LAYERS:**
1. Delete redundant "Why This Matters" sections
   - Keep ONLY if it reveals non-obvious insight
   - If same point made in text AND in "Why This Matters" → delete WTM
2. Merge repeated examples
   - Find duplicate explanations
   - Keep first, delete second
3. Tighten transitions between sections
   - Replace "As we discussed earlier, X..." with direct reference

**FOR L1-L2 ONLY** (students still building foundation):
4. Reduce "Try With AI" sections to exactly 2 prompts
   - Keep foundational + one advanced
   - Delete exploratory extras
5. Keep educational scaffolding (explanations, examples)

**FOR L3-L4 ONLY** (students ready for advanced patterns):
4. Trim narrative scaffolding
   - Keep pattern insights and rules
   - Delete "why this matters philosophically"
5. Remove beginner-level explanations
   - Assume students understand fundamentals

**FOR ALL LAYERS:**
6. **One Analogy Rule**: Keep the BEST analogy for the concept; delete redundant ones
7. **Merge Tables/Text**: Use ONE format (table OR prose), never both
8. **Reduce Examples**: Keep 2-3 best; delete "also consider..."
9. **Tighten Lists**: Convert 5-item lists to 3 core items

**Verification**:
- [ ] Word count after cuts: [TARGET ± 5%]
- [ ] No L1 content cut from L1 lessons
- [ ] No pattern insights lost from L3-L4 lessons
- [ ] Try With AI: 2 prompts if L1-L2, keep all if L3-L4

### Phase 3: Post-Refinement Validation (CRITICAL)

**After applying fixes, verify the content now PASSES Gate 4:**

```
✓ Word Count Check:
  Current: [X] words
  Target: [target_from_spec]
  Status: [PASS if ≤target ± 5%, FAIL if over]

✓ Continuity Check:
  Opening references Lesson [N-1]? [YES/NO]
  Specific outcome mentioned? [YES/NO]
  Connection to new lesson clear? [YES/NO]

✓ Layer Appropriateness:
  No foundational cuts from L1-L2? [YES/NO]
  No pattern insight loss from L3-L4? [YES/NO]

✓ Content Integrity:
  Removed examples still explained elsewhere? [YES/NO]
  Cut sections non-essential? [YES/NO]
```

**NEXT STEP RECOMMENDATION:**
```
"Refined content is ready.

Word count: [after] (target: ≤[target])
Continuity: Now references Lesson [N-1]

Recommend re-submitting to acceptance-auditor for Gate 4 re-validation.
Command: [provide re-validation instruction]"
```

---

## Output Format

```markdown
## Refinement Report: [Lesson Name]

### Diagnosis
**Issue Found**: [Word count | Continuity | Both]
**Layer**: [L1/L2/L3/L4]

### Metrics
| Metric | Before | After | Target | Status |
|--------|--------|-------|--------|--------|
| Word Count | 1950 | 1485 | ≤1500 | ✅ PASS |
| Continuity | Generic opening | References Lesson 2 | Specific reference | ✅ PASS |

### Fixes Applied
1. **Phase 1**: Rewrote opening to reference "booking-agent implementation" from Lesson 2
2. **Phase 2**: Deleted 240 words using layer-aware cuts:
   - Removed redundant "Why This Matters" section (line 45, 120 words)
   - Merged duplicate example (lines 67-89, 85 words)
   - Cut 1 extra "Try With AI" prompt (35 words)
3. **Phase 3**: Validated word count and continuity

### Ready for Re-validation
✅ Word count: 1485 (≤1500)
✅ Continuity: Opening references Lesson 2
✅ Layer integrity: All L2 AI examples preserved

**Next**: Re-submit to acceptance-auditor for Gate 4 validation

### Refined Content
[Full refined lesson content]
```