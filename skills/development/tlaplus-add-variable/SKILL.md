---
name: tlaplus-add-variable
description: Add a new variable to an existing TLA+ specification without changing its semantics. Ensures the variable is declared, initialized, and added to all UNCHANGED statements. Use when the user asks to add, introduce, or declare a new variable in a TLA+ spec, or mentions UNCHANGED statements.
---

# Add Variable to TLA+ Specification

Add a new variable to a TLA+ specification while preserving semantics. The new variable must appear in all necessary locations so the specification remains valid and its behavior is unchanged.

## Required Locations for New Variables

When adding a variable `newVar` to a TLA+ specification, update these locations:

1. **VARIABLE declaration block** - Add the variable name
2. **Init** - Initialize the variable
3. **All UNCHANGED statements** - Add variable to every UNCHANGED that doesn't modify it
4. **vars tuple** - Add to the tuple used in temporal formulas (if exists)
5. **TypeOk** (optional) - Add type constraint if TypeOk invariant exists

## Workflow

### Step 1: Analyze the Specification

Read the TLA+ file and identify:
- All existing variables in the VARIABLE block
- The Init predicate
- All actions and their UNCHANGED statements
- The `vars` tuple or similardefinition (usually near Next or Spec)
- TypeOk invariant if present

### Step 2: Add Variable Declaration

Add the new variable to the VARIABLE block. Preserve formatting:

```tla
VARIABLE
    existingVar1,
    existingVar2,
    newVar  \* Add with comment explaining purpose
```

### Step 3: Initialize in Init

Add initialization. Match the style of existing initializations:

```tla
Init ==
    /\ existingVar1 = ...
    /\ existingVar2 = ...
    /\ newVar = <initial_value>
```

### Step 4: Update All UNCHANGED Statements

**Critical step.** Find every UNCHANGED statement and add the new variable:

```tla
\* Before:
UNCHANGED << existingVar1, existingVar2 >>

\* After:
UNCHANGED << existingVar1, existingVar2, newVar >>
```

Search patterns to find UNCHANGED statements:
- `UNCHANGED <<` - tuple form
- `UNCHANGED` followed by variable name - single variable form

For single-variable UNCHANGED, convert to tuple form:
```tla
\* Before:
UNCHANGED existingVar

\* After:
UNCHANGED << existingVar, newVar >>
```

### Step 5: Update vars Tuple

If a `vars` tuple exists, add the new variable:

```tla
\* Before:
vars == << state, counter, pc >>

\* After:
vars == << state, counter, pc, newVar >>
```

### Step 6: Update TypeOk (if exists)

Add type constraint for the new variable:

```tla
TypeOk ==
    /\ existingVar1 \in SomeSet
    /\ newVar \in ExpectedType
```

## Verification Checklist

After making changes, verify:

- [ ] Variable declared in VARIABLE block
- [ ] Variable initialized in Init
- [ ] Variable added to ALL UNCHANGED statements (use grep to count)
- [ ] Variable added to vars tuple
- [ ] Variable has type constraint in TypeOk (if TypeOk exists)
- [ ] No action modifies the new variable (per task requirements)

## Common Patterns

### Per-Thread Variables

For variables indexed by thread/process:

```tla
\* Declaration
newVar,

\* Initialization
/\ newVar = [thread \in Threads |-> InitialValue]

\* In UNCHANGED (same as scalar variables)
UNCHANGED << ..., newVar >>
```

### Conditional UNCHANGED

Some actions have conditional branches with different UNCHANGED statements. Update ALL branches:

```tla
Action(thread) ==
    IF condition
        THEN
            /\ ...
            /\ UNCHANGED << var1, var2, newVar >>  \* Update this
        ELSE
            /\ ...
            /\ UNCHANGED << var1, var3, newVar >>  \* AND this
```

### Nested Disjunctions

Actions with `\/` may have UNCHANGED in each branch:

```tla
Action(thread) ==
    \/  /\ guard1
        /\ UNCHANGED << a, b, newVar >>  \* Each branch
    \/  /\ guard2
        /\ UNCHANGED << a, c, newVar >>  \* needs update
```

## Example

Adding `debug_log` variable to track operations:

**Before:**
```tla
VARIABLE state, counter

Init ==
    /\ state = "idle"
    /\ counter = 0

Increment ==
    /\ counter' = counter + 1
    /\ UNCHANGED state

vars == << state, counter >>
```

**After:**
```tla
VARIABLE state, counter, debug_log

Init ==
    /\ state = "idle"
    /\ counter = 0
    /\ debug_log = <<>>

Increment ==
    /\ counter' = counter + 1
    /\ UNCHANGED << state, debug_log >>

vars == << state, counter, debug_log >>
```
