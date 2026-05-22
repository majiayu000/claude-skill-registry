---
name: cc-control-flow-quality
description: "Review control flow quality using 87-item checklist. Use when code has deep nesting (3+ levels), complex conditionals, loop design questions, high cyclomatic complexity (McCabe >10), or callback hell. Symptoms: arrow-shaped code, repeated conditions, confusing loop exits, lengthy if-else chains. Provide refactoring patterns (guard clauses, named booleans, table-driven methods) and modern guidance (async/await, pattern matching, functional pipelines). Produce verified code with pass/fail assessment."
---

# Skill: cc-control-flow-quality

## STOP - Never Skip (even under time pressure)

- Check nesting depth before adding levels (max 3)
- Verify loop exit conditions are reachable
- Name loop indexes meaningfully in nested loops
- McCabe complexity >10 = redesign required

---

## Quick Reference

| Threshold | Value | Source |
|-----------|-------|--------|
| Max nesting depth | 3 levels | Chomsky, Weinberg via Yourdon 1986a |
| McCabe complexity | >10 decision points = redesign | McCabe 1976 |
| Else clause consideration | 50-80% of ifs need else | Elshoff 1976 |
| Loop-with-exit comprehension | 25% better than top/bottom test | Soloway 1983 |
| Mental entity limit | 5-9 items | Miller 1956 |

**Key Principles:**
- Use `true`/`false` not `0`/`1` for booleans
- Use `for` when iteration count is known, `while` when unknown, `foreach` for collections
- Test at beginning (may not execute) vs end (executes at least once)
- Put nominal case in `if`, error case in `else` (exception: guard clauses invert this intentionally—see below)
- Fully parenthesize complex boolean expressions

**NEVER Skip (even under time pressure):**
- Check nesting depth before adding levels
- Verify loop exit conditions are reachable
- Name loop indexes meaningfully in nested loops

## Core Patterns

### Deep Nesting → Guard Clauses

**Reconciling with "nominal in if":** Guard clauses are an *exception pattern* where error/invalid cases exit early at the top of a function. This contradicts the general "nominal in if" rule *intentionally*—the goal is to get preconditions out of the way so the nominal path flows without nesting. Use guard clauses at function entry; use "nominal in if" for conditionals within the function body.

```cpp
// BEFORE: Arrow-shaped code (4 levels) [ANTI-PATTERN]
if (file.validName()) {
    if (file.open()) {
        if (encryptionKey.valid()) {
            if (file.decrypt(encryptionKey)) {
                // lots of code (nominal case buried)
            }
        }
    }
}

// AFTER: Guard clauses flatten structure
if (!file.validName()) return;
if (!file.open()) return;
if (!encryptionKey.valid()) return;
if (!file.decrypt(encryptionKey)) return;

// lots of code (nominal case at top level)
```

### Complex Boolean → Intermediate Variables
```cpp
// BEFORE: Monstrous test [ANTI-PATTERN]
if (inputStatus == SUCCESS && printerReady && !printerBusy &&
    paperAvailable && paperLevel > MIN_PAPER &&
    documentValid && !documentEmpty && documentSize < MAX_SIZE) {
    print();
}

// AFTER: Named intermediate booleans
bool printerCanPrint = printerReady && !printerBusy &&
                       paperAvailable && paperLevel > MIN_PAPER;
bool documentCanBePrinted = documentValid && !documentEmpty &&
                            documentSize < MAX_SIZE;

if (inputStatus == SUCCESS && printerCanPrint && documentCanBePrinted) {
    print();
}
```

### Meaningless Loop Indexes → Descriptive Names
```java
// BEFORE: Impossible to verify correct array access [ANTI-PATTERN]
for (int i = 0; i < numPayCodes; i++) {
    for (int j = 0; j < 12; j++) {
        for (int k = 0; k < numDivisions; k++) {
            sum = sum + transaction[j][i][k];  // Is this right? Who knows!
        }
    }
}

// AFTER: Self-documenting and verifiable
for (int payCodeIdx = 0; payCodeIdx < numPayCodes; payCodeIdx++) {
    for (int month = 0; month < 12; month++) {
        for (int divisionIdx = 0; divisionIdx < numDivisions; divisionIdx++) {
            sum = sum + transaction[month][payCodeIdx][divisionIdx];
        }
    }
}
```

### Single-Use Test → Named Boolean Function
```cpp
// BEFORE: Complex inline test obscures main flow
if (((('a' <= inputChar) && (inputChar <= 'z')) ||
     (('A' <= inputChar) && (inputChar <= 'Z'))) &&
    (inputChar != 'X') && (inputChar != 'x')) {
    processLetter(inputChar);
}

// AFTER: Named function (even for single use!)
// "Putting a test into a well-named function improves readability,
//  and that's a sufficient reason to do it." [KEY POINT p.433]
bool isProcessableLetter(char c) {
    bool isLetter = (('a' <= c) && (c <= 'z')) ||
                    (('A' <= c) && (c <= 'Z'));
    bool isExcluded = (c == 'X') || (c == 'x');
    return isLetter && !isExcluded;
}

if (isProcessableLetter(inputChar)) {
    processLetter(inputChar);
}
```

### Number-Line Ordering for Comparisons
```cpp
// Range checks: order smallest → variable → largest
if (MIN_VALUE <= count && count <= MAX_VALUE)  // count is between

// Out-of-range: variable on outside
if (count < MIN_VALUE || MAX_VALUE < count)    // count is outside

// This visual mapping aids comprehension [KEY POINT p.440]
```

### Type-Appropriate Zero Comparisons
```cpp
// Boolean: compare implicitly
while (!done)                    // not: while (done == false)

// Numeric: compare explicitly
while (balance != 0)             // not: while (balance)

// Character (C): compare to null terminator explicitly
while (*charPtr != '\0')         // not: while (*charPtr)

// Pointer: compare to NULL explicitly
while (bufferPtr != NULL)        // not: while (bufferPtr)
```

### Loop-With-Exit Avoiding Duplication
```cpp
// BEFORE: Duplicated code that will break under maintenance [ANTI-PATTERN]
GetNextRating(&ratingIncrement);
rating = rating + ratingIncrement;
while ((score < targetScore) && (ratingIncrement != 0)) {
    GetNextScore(&scoreIncrement);
    score = score + scoreIncrement;
    GetNextRating(&ratingIncrement);      // Duplicated!
    rating = rating + ratingIncrement;    // Duplicated!
}

// AFTER: Loop-with-exit eliminates duplication
while (true) {
    GetNextRating(&ratingIncrement);
    rating = rating + ratingIncrement;
    if (!((score < targetScore) && (ratingIncrement != 0))) {
        break;
    }
    GetNextScore(&scoreIncrement);
    score = score + scoreIncrement;
}
// Students scored 25% higher on comprehension with this pattern [Soloway 1983]
```

## Decision Guidance

### Loop Selection
```
1. Is iteration count known ahead of time?
   YES → Use `for` or `foreach`
   NO  → Use `while`

2. Must body execute at least once?
   YES → Use loop with test at END (`do-while`) or MIDDLE
   NO  → Use loop with test at BEGINNING (`while`)

3. Simple iteration through container?
   YES → Use `foreach` (eliminates housekeeping arithmetic errors)
   NO  → Use appropriate `for` or `while`

4. Need to exit from middle of loop?
   YES → Consider loop-with-exit (`while(true)` + `break`)
   NO  → Standard loop structure
```

### Nesting Reduction Techniques (by invasiveness, not strict priority)

These techniques are ordered from least to most invasive changes—**not** a strict "try #1 before #2" sequence. Choose based on what fits the problem:

1. **Guard clauses** - Exit early on error conditions (least invasive; see Core Patterns)
2. **Extract to routine** - Move nested code into well-named function
3. **Combine conditions** - Merge nested ifs into single compound test
4. **Convert to case/switch** - When testing same variable repeatedly
5. **Use polymorphism** - Replace type-checking conditionals with dispatch
6. **Table-driven methods** - When logic maps data to outcomes (most architectural)

**Note:** #5 and #6 are context-dependent, not ranked. Tables can be simpler than polymorphism (see "The fact that a design uses inheritance and polymorphism doesn't make it a good design" [p.423]).

### When to Use Table-Driven Methods
Consider tables instead of logic when:
- Writing 4th+ branch in if-else chain for same classification
- Creating subclass just to change a data value
- Format/rules change frequently without code changes desired
- Same lookup calculation duplicated in multiple places

**"The fact that a design uses inheritance and polymorphism doesn't make it a good design."** [p.423]

### Table Access Method Selection
```
1. Can data key directly into table? (e.g., month 1-12, char code 0-255)
   YES → Direct Access
   NO  → Continue

2. Is keyspace large/sparse but entries few? (e.g., 100 items with 4-digit part numbers)
   YES → Indexed Access (index table + main table)
   NO  → Continue

3. Are entries valid for ranges, not distinct points? (e.g., grade thresholds)
   YES → Stair-Step Access (loop through range boundaries)
   NO  → Reconsider if table-driven is appropriate
```

### Table-Driven Example: Message Processing
```cpp
// BEFORE: 20 routines, one per message type [ANTI-PATTERN]
void processMessage(Message& msg) {
    if (msg.type == CYCLIC_REDUNDANCY_CHECK) {
        processCRC(msg);
    } else if (msg.type == BUOY_TEMPERATURE) {
        processBuoyTemp(msg);
    } else if (msg.type == SONOBUOY_PING) {
        processSonobuoyPing(msg);
    }
    // ... 17 more branches
}

// AFTER: One generic routine + table definition [p.418-420]
// Table describes message format; routine interprets any message
struct FieldDef { FieldType type; string name; };
struct MessageDef { string name; vector<FieldDef> fields; };

map<MessageType, MessageDef> messageTable = {
    {BUOY_TEMPERATURE, {"Buoy Temperature", {
        {FLOAT, "Average Temperature"},
        {FLOAT, "Temperature Range"},
        {INT, "Number of Samples"},
        {STRING, "Location"},
        {TIME, "Time of Measurement"}
    }}}
    // New message types = new table entries, zero code changes
};

void processMessage(Message& msg) {
    auto& def = messageTable[msg.type];
    for (auto& field : def.fields) {
        readAndPrint(field, msg);  // One routine handles all types
    }
}
```

### McCabe Complexity Counting [p.458]
```
How to count decision points in a routine:

1. Start with 1 for the straight path through the routine
2. Add 1 for each: if, while, repeat, for, and, or
3. Add 1 for each case in a case/switch statement

Interpretation:
  0-5   → Routine is probably fine
  6-10  → Start thinking about simplification
  10-20 → Strong case needed to keep as-is; review for extraction
  20+   → Mandatory refactor (no exceptions)
```

**Exception criteria for 10-20 range:**
A routine may legitimately exceed 10 ONLY when ALL of:
1. It's a flat dispatch (switch/case with no nesting within cases)
2. Each case is ≤3 lines (ideally just a function call)
3. Cases are exhaustive and unlikely to grow unboundedly
4. Cognitive complexity is low despite high McCabe count

**NOT a valid exception:** "It's just a big if-else chain" or "The complexity is inherent."

## Rationalization Counters
| Excuse | Reality |
|--------|---------|
| "Deep nesting is unavoidable" | Multiple techniques exist: guard clauses, extract routines, table-driven (p.449) |
| "It's just one level deeper" | Comprehension drops significantly after 3 levels [Chomsky, Weinberg] |
| "The order of statements is obvious" | If it requires domain knowledge, make dependencies explicit in code (p.98) |
| "I'll tweak the for loop index to exit early" | Sign of amateur; use while loop for complex exit conditions (p.377) |
| "OOP inheritance is always better than tables" | Inheritance isn't automatically better; table lookup can be simpler (p.423) |
| "Recursion is elegant for factorials" | Factorial is a *poor* example of recursion—iteration is faster with predictable memory. Save recursion for recursive data structures (trees, graphs) where it adds clarity (p.393) |
| "The else case will never happen" | 50-80% of if statements should have else clauses [Elshoff 1976]. Document why it's safe to omit. |
| "The test is only used once, not worth extracting" | Putting a test into a well-named function improves readability—that's sufficient reason [KEY POINT p.433] |
| "0 and 1 work fine for booleans" | Nothing tells reader if 1 means true or false; easy to write 0 when you mean 1 (p.431) |
| "Parentheses are unnecessary clutter" | Parentheses are free and reduce demand on reader's precedence knowledge (p.443) |
| "I can use the loop index after the loop" | Terminal value varies by language/compiler; assign to variable inside loop (p.378) |
| "One loop doing two things is more efficient" | Write two loops; comment they could combine; wait for benchmarks to prove need (p.385) |
| **"But it already works"** | Working code can still have latent bugs. Control flow violations correlate with defects regardless of test status [McCabe 1976]. Time invested doesn't change bug potential. |
| **"It worked last time without this"** | Past success doesn't guarantee future correctness. Silent complexity accumulates until it causes failures. Apply these checks *every time*, not just when problems appear. |
| **"No time—production is down"** | See Emergency Minimum below. Even in crisis, skip nothing from the NEVER Skip list. Rushed fixes that add complexity cause the *next* outage. |
| **"Senior engineer says it's fine"** | Complexity thresholds are backed by research [McCabe 1976, Chomsky, Weinberg]. Challenge authority with evidence, not deference. |

## Emergency Minimum (Crisis Mode)

When production is down and you must fix immediately, you still MUST:

1. **Check nesting depth** - Don't add a 4th level to fix a 3-level problem
2. **Verify loop exits** - Ensure your fix doesn't create infinite loops
3. **Name any new variables meaningfully** - `tempFix` guarantees confusion later
4. **Document WHY** - A one-line comment explaining the crisis fix

**After crisis resolved:** Return within 24 hours to apply full control flow review. Crisis fixes that "work" often hide deeper issues.

## Modern Patterns (Beyond Code Complete)

These patterns weren't covered in Code Complete (2004) but follow the same principles:

### Async/Await (Promise Chains)
```javascript
// BEFORE: Callback hell (deep nesting equivalent)
getData(url, (data) => {
    process(data, (result) => {
        save(result, (saved) => {
            notify(saved, () => { /* ... */ });
        });
    });
});

// AFTER: Flattened with async/await
const data = await getData(url);
const result = await process(data);
const saved = await save(result);
await notify(saved);
```
Same principle as guard clauses: flatten the structure.

### Pattern Matching (Rust, C#, etc.)
```rust
// Pattern matching can exceed McCabe threshold but remain clear
// because it's flat dispatch with exhaustiveness checking
match status {
    Status::Pending => handle_pending(),
    Status::Active => handle_active(),
    Status::Suspended => handle_suspended(),
    Status::Closed => handle_closed(),
}
```
This is the "valid exception" for McCabe—flat dispatch with ≤3 lines per case.

### Functional Pipelines
```javascript
// Functional pipelines replace explicit loops
const result = items
    .filter(item => item.active)
    .map(item => transform(item))
    .reduce((acc, item) => acc + item.value, 0);
```
Prefer over explicit loops when: operations are independent, no early exit needed, and pipeline reads clearly.


---

## Chain

| After | Next |
|-------|------|
| Control flow verified | cc-code-layout-and-style (CHECKER) |

