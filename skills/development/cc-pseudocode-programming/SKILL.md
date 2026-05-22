---
name: cc-pseudocode-programming
description: "Guide routine design using the Pseudocode Programming Process (PPP). Produce pseudocode design, header comments, and implementation plan. Use when designing routines, stuck on where to start coding, caught in compile-debug loops, or code works but you don't understand why. Triggers on: can't name the routine, Just One More Compile syndrome, staring at screen, coded into a corner, keep hacking but still broken, too many compiler warnings, overwhelmed by where to start."
---

# Skill: cc-pseudocode-programming

## STOP - Crisis Invariants

| Check | Time | Why Non-Negotiable |
|-------|------|-------------------|
| **Pseudocode before code** | 30 sec | Once you write code, emotional investment prevents good design iteration |
| **Can you name it clearly?** | 15 sec | Naming difficulty = design problem. Stop and clarify purpose. |
| **Do you understand why it works?** | 30 sec | Working code you don't understand probably doesn't really work |
| **Did you consider alternatives?** | 30 sec | First design is rarely best; iterate in pseudocode where it's cheap |

---

## When NOT to Use

**Exemption criteria are STRICT. If in doubt, use PPP.**

- **Simple accessor routines** - `getValue()`, `setName()` with NO logic (no validation, no transformation, no side effects)
- **Pass-through routines** - Pure delegation with NO parameter transformation or error wrapping
- **Trivial one-liners** - ALL of these must be true:
  - Single statement implementation
  - Zero decision points (no if/switch/ternary)
  - Zero loops
  - Implementation obvious to ANY team member from signature alone
- **Already-designed routines** - Design document specifies EXACT algorithm, error handling, and edge cases

**If you're debating whether it's "trivial enough" to skip PPP, it isn't trivial. Use PPP.**

## Crisis Invariants - NEVER SKIP

**These checks are NON-NEGOTIABLE regardless of deadline pressure, past successes, or authority pressure:**

| Check | Time | Why Non-Negotiable |
|-------|------|-------------------|
| **Pseudocode before code** | 30 sec | Once you write code, emotional investment prevents good design iteration |
| **Can you name it clearly?** | 15 sec | Naming difficulty = design problem. Stop and clarify purpose. |
| **Do you understand why it works?** | 30 sec | Working code you don't understand probably doesn't really work |
| **Did you consider alternatives?** | 30 sec | First design is rarely best; iterate in pseudocode where it's cheap |

**Why these four?** They catch the most expensive mistakes: unclear designs that "work" but create maintenance nightmares, and premature coding that locks in bad decisions.

**Success-agnostic:** These checks apply EVERY TIME, even if:
- Your last 10 routines worked without PPP (hot-hand fallacy - past luck doesn't change future odds)
- You're an expert in this domain (experts make design errors too; PPP catches them)
- The routine seems simple (simple-seeming routines hide complexity; that's WHY they need PPP)
- You're under time pressure (see Minimum Viable PPP below - 4 minutes is faster than debugging)

**Minimum Viable PPP (for extreme time pressure):**
When full PPP is impossible, these 4 items are MANDATORY (total ~4 min):
1. Can you name the routine clearly? (15 sec)
2. Write at least 3 lines of pseudocode (2 min)
3. Consider one alternative approach (1 min)
4. Convince yourself it's correct before compiling (30 sec)

This is the FLOOR, not the ceiling. If you can't spare 4 minutes, the routine will cost you more in debugging.

## Modes

### APPLIER
Purpose: Guide routine design using PPP technique
Triggers:
  - "help me design this routine"
  - "I'm stuck, don't know where to start"
  - "walk me through PPP"
  - "how should I approach this implementation"
  - "overwhelmed by where to start coding"
Non-Triggers:
  - "review my existing code" → cc-routine-and-class-design
  - "is this architecture right" → cc-construction-prerequisites
Produces: Pseudocode design, header comments, implementation plan

#### PPP Process Steps
1. **Check prerequisites** - Confirm the routine's place in overall design is clear
2. **Define the problem** - Specify inputs, outputs, preconditions, postconditions, what it hides
3. **Name the routine** - If naming is hard, the design is unclear; iterate
4. **Plan testing** - Decide how you'll test it before writing code
5. **Check libraries** - Look for existing functionality before building
6. **Plan error handling** - Think through failure modes
7. **Research algorithms** - Study relevant algorithms if needed
8. **Write pseudocode** - Start with header comment, use natural language
9. **Iterate pseudocode** - Refine until generating code is nearly automatic
10. **Try alternatives** - Consider multiple approaches, keep the best
11. **Code from pseudocode** - Pseudocode becomes comments
12. **Compile clean** - Use strictest warnings, eliminate ALL of them

Constraints:
  - Pseudocode must be language-independent (p.218)
  - Pseudocode must be detailed enough to generate code from (p.219)
  - Never compile until convinced the routine is correct (p.230)

**Key Term Definitions:**
- **"Nearly automatic" (step 9):** You can write each line of code without pausing to think about HOW. Every decision is already made in pseudocode. If you stop to think "how should I implement this part?" - pseudocode needs more detail.
- **"Convinced it's correct" (constraint):** You can mentally trace execution through ALL paths (happy path, error cases, edge cases) and explain why each produces correct output. "It looks right" is NOT convinced.
- **"Right level of detail":** Detailed enough that code generation is nearly automatic (see above), but not so detailed that you're writing syntax. Test: Could a competent developer write the code without asking clarifying questions?

#### Transformation Example: Bad vs Good Pseudocode

**Problem:** Create a routine to allocate a new resource and return its handle.

**Bad Pseudocode (Anti-Pattern):**
```
increment resource number by 1
allocate a dlg struct using malloc
if malloc() returns NULL then return 1
invoke OSrsrc_init to initialize a resource for the operating system
*hRsrcPtr = resource number
return 0
```
**Problems:** Uses target language details (`*hRsrcPtr`, `malloc()`), focuses on HOW not WHAT, exposes implementation details (returns 1 or 0), won't become good comments.

**Good Pseudocode:**
```
If another resource is available
    Allocate a dialog box structure
    If a dialog box structure could be allocated
        Note that one more resource is in use
        Initialize the resource
        Store the resource number at the location provided by the caller
        Return success
    Endif
Endif
Return failure
```
**Why better:** Pure English, no syntax, level of intent, precise enough to generate code, becomes excellent comments. Note: resource count is updated AFTER successful allocation, not before.

**Resulting Code with Comments:**
```c
// If another resource is available
if (resourceCount < MAX_RESOURCES) {
    // Allocate a dialog box structure
    DialogBox* dlg = allocateDialogBox();

    // If a dialog box structure could be allocated
    if (dlg != NULL) {
        // Note that one more resource is in use
        // (Using post-increment: store at current index, then increment)
        activeResources[resourceCount] = dlg;
        *handlePtr = resourceCount;
        resourceCount++;

        // Initialize the resource
        initializeResource(dlg);

        return true;
    }
}
return false;
```

### CHECKER
Purpose: Verify PPP was followed correctly
Triggers:
  - "did I follow PPP correctly"
  - "review my pseudocode"
  - "is my design process right"
Produces: Process compliance assessment, improvement recommendations

Check Against:
  - Was pseudocode written before code?
  - Is pseudocode at the right level of detail?
  - Were alternatives considered?
  - Can you explain why the code works?
  - Are all compiler warnings eliminated?

## Red Flags - STOP and Reconsider

If you find yourself in any of these situations, you are about to violate the skill:

**Process Violations:**
- Using target language syntax in pseudocode
- Pseudocode too high-level to generate code from
- Compiling before convinced routine is right
- Settling for first design without considering alternatives
- Hacking around buggy routines instead of rewriting

**Understanding Failures:**
- Code works but you don't understand why
- Difficulty naming a routine (indicates unclear purpose)
- Lost train of thought mid-implementation
- Forgot to write part of the routine

**Compile-Debug Loop Symptoms:**
- "Just One More Compile" syndrome
- Staring at screen not knowing where to start
- Coded into a corner
- Too many compiler warnings to count

## Rationalization Counters
| Excuse | Reality |
|--------|---------|
| "I'll just start coding and figure it out" | Once you start coding, you get emotionally invested. Design in pseudocode first where iteration is cheap. (p.221) |
| "The pseudocode is clear enough at this level" | If pseudocode is too high-level, it glosses over problematic details. Refine until code generation is automatic. (p.219) |
| "I'll compile and let the computer find errors" | Compiling before you're sure it works is hacker mindset. Convince yourself it's right first. (p.230) |
| "Just one more compile will fix it" | The "Just One More Compile" syndrome leads to hasty, error-prone changes. Stop and think. (p.230) |
| "It works, so it must be right" | If you don't know why it works, study it until you do. Working code you don't understand probably doesn't really work. (p.230) |
| "I can fix this buggy routine with a few tweaks" | Hacks indicate incomplete understanding. Rewrite the routine. (p.229) |
| "The compiler/OS/hardware must be wrong" | Only 5% of errors are hardware, compiler, or OS errors. Suspect your own work first - you cause 95% of errors. (p.230) |
| "Warnings are just warnings, not errors" | A large number of warnings often indicates low-quality code. Eliminate ALL warnings by fixing underlying problems. (p.231) |
| "I'll use language-specific syntax in my pseudocode" | Using programming-language constructs sinks you to a lower level, eliminating the main benefit of higher-level design. (p.218) |
| "I already spent N hours on this code" | Sunk cost fallacy. Time invested doesn't make bad design good. 15 min of PPP now is cheaper than rewriting later. The question isn't "how much did I invest?" but "is this design right?" |
| "Production is down, no time for process" | Crisis makes PPP MORE important, not less. Hasty fixes under pressure create more bugs. Use Minimum Viable PPP (4 min) - it's faster than debugging a bad fix. |
| "This worked the last 5 times without PPP" | Hot-hand fallacy. Past successes don't change the odds. The next routine can still have bugs. PPP prevents the bug you haven't hit YET. |
| "The senior engineer said to just do X" | Authority doesn't override engineering principles. If PPP would catch a bug, that bug doesn't care about seniority. Explain your reasoning; good seniors welcome it. |

## Pressure Testing Scenarios

### Scenario 1: Deadline Pressure
**Situation:** Feature due in 2 hours. You're tempted to skip pseudocode and just start coding.
**Test:** Is this a non-trivial routine with multiple decision points?
**REQUIRED Response:** Yes. 15 minutes of pseudocode now prevents 2 hours of debugging later. You get emotionally invested in code once written - design iterations become painful.

### Scenario 2: Compile-Debug Loop
**Situation:** You've compiled 8 times. Each compile reveals new errors. You're making "just one more fix."
**Test:** Are you thinking through changes or reacting to compiler output?
**REQUIRED Response:** STOP. Step away from the keyboard. Write pseudocode for the routine. Convince yourself it's correct BEFORE compiling again. The compile-debug loop wastes more time than design.

### Scenario 3: Working But Mysterious
**Situation:** After much trial and error, the routine finally passes all tests. You don't fully understand why it works.
**Test:** Can you explain every line's purpose to a colleague?
**REQUIRED Response:** No. Study the routine. Experiment with alternative designs. A routine that works but you don't understand probably doesn't really work - you just haven't found the bug yet.

### Scenario 4: Buggy Routine
**Situation:** Routine keeps having bugs. You've fixed 3 so far. Now there's a 4th.
**Test:** Are you hacking around problems or addressing root cause?
**REQUIRED Response:** If you've fixed 3+ bugs in the same routine, the design is wrong. Don't hack. Start over with entirely new pseudocode design. Incomplete understanding guarantees more bugs.

### Scenario 5: Naming Struggle
**Situation:** You can't think of a good name for the routine. Every name seems wrong or too long.
**Test:** Does the naming difficulty indicate unclear purpose?
**REQUIRED Response:** Yes. Back up and improve the design. You shouldn't have trouble naming a routine that has a clear, single purpose. The name struggle is a design smell.

## Evidence Summary

| Claim | Evidence | Source | Still Valid? |
|-------|----------|--------|--------------|
| Programmers prefer pseudocode | Survey: preferred for construction ease, detecting insufficient detail, documentation | Ramsey, Atwood, Van Doren 1983 | Yes - methodology unchanged; modern IDEs don't eliminate design thinking need |
| Only 5% external errors | Hardware, compiler, OS errors are rare; 95% are programmer errors | Ostrand and Weyuker 1984 | Yes - if anything, modern tooling has made infrastructure MORE reliable, so programmer error % is likely higher |
| Errors at least-value stage | Key insight: catch errors when least effort invested | McConnell p.220 | Timeless - economic principle |
| Iteration improves design | First design is rarely best; emotional investment prevents iteration after coding | McConnell p.225 | Timeless - cognitive principle |

**Note on dated studies:** The 1983-1984 studies predate modern IDEs, but their findings are MORE applicable today: better tooling catches syntax errors faster, making DESIGN errors (which PPP prevents) the dominant problem. The cognitive biases PPP addresses (emotional investment, premature commitment) are hardwired human traits that haven't changed.

---

## Chain

| After | Next |
|-------|------|
| Pseudocode complete | cc-routine-and-class-design |
| Implementation done | cc-defensive-programming (CHECKER) |

