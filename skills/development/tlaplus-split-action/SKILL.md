---
name: tlaplus-split-action
description: Split a TLA+ action into two sequential actions by introducing a new program counter (pc) state. Handles pc variable updates, UNCHANGED statements, TypeOk predicates, and follows naming conventions with renumbering. Use when the user asks to split, divide, or break an action into two parts, or wants to add an intermediate step to an action sequence.
---

# Split TLA+ Action into Two Actions

Split an existing TLA+ action into two sequential actions by introducing a new intermediate `pc` state. This is useful for modeling finer-grained atomicity or adding intermediate steps to an action sequence.

## Prerequisites

- The specification must have a `pc` variable (or equivalent like `state`, `phase`) that tracks action sequencing. If not, create one.
- The action to split must update `pc` to transition between states

## Overview

Given an action like:

```tla
ActionX_1(thread) ==
    /\ pc[thread] = PC_ActionX_1
    /\ pc' = [pc EXCEPT ![thread] = PC_Start]
    /\ y' = y + 2
    /\ UNCHANGED <<x, z>>
```

Splitting it creates:

```tla
ActionX_1(thread) ==
    /\ pc[thread] = PC_ActionX_1
    /\ pc' = [pc EXCEPT ![thread] = PC_ActionX_2]   \* Leads to new intermediate state
    /\ y' = y + 2                                   \* Original logic (or subset per user)
    /\ UNCHANGED <<x, z>>

ActionX_2(thread) ==                                \* New action
    /\ pc[thread] = PC_ActionX_2
    /\ pc' = [pc EXCEPT ![thread] = PC_Start]       \* Original destination
    /\ UNCHANGED <<x, y, z>>                        \* All vars unchanged (or subset per user)
```

## Workflow

### Step 0: Add `pc` variable if not present

If the specification lacks a `pc` variable, first use the **"tlaplus-add-variable"** skill to add `pc` variable. If the actions are thread- or process-specific, `pc` variable must be a function of the thread or process identifier to a string constant. For example,

```tla
PC_Begin == "PC_Begin"
PC_ActionX_1 == "PC_ActionX_1"
...

Init ==
    /\ pc = [thread \in Threads |-> PC_Begin]
    /\ ...
```

### Step 1: Analyze the Target Action

Read the specification and identify:
1. The action to split
2. Its current `pc` guard (entry state)
3. Its `pc'` assignment (exit state)
4. All variable updates in the action
5. The UNCHANGED statement
6. The naming convention used (numbered suffix like `_0`, `_1`, etc.)

### Step 2: Determine the New PC State Name

Follow the specification's naming convention:

**If actions are numbered (e.g., `ActionX_0`, `ActionX_1`):**
- Insert the new PC state between the split action and its successor
- Renumber subsequent PC states and actions

**Example:** Splitting `ActionX_1` which goes to `PC_Start`:
- New intermediate state: `PC_ActionX_2`
- Original `ActionX_1` now leads to `PC_ActionX_2`
- New action `ActionX_2` leads to `PC_Start`

**If actions have descriptive names (e.g., `PC_Fetch`, `PC_Execute`):**
- Create a descriptive name for the intermediate state
- Ask the user if the name is unclear

### Step 3: Add New PC State Constant

Add the new PC state to the PCStates set (or equivalent):

```tla
\* Before:
PCStates == {
    PC_Ready,
    PC_ActionX_1,
    ...
}

\* After:
PCStates == {
    PC_Ready,
    PC_ActionX_1, PC_ActionX_2,  \* Added PC_ActionX_2
    ...
}
```

### Step 4: Modify the Original Action

Update the original action to:
1. Change `pc'` to transition to the NEW intermediate state
2. Update UNCHANGED to include variables that will be modified in the second action

**Without user instructions (empty intermediate action):**

```tla
\* Before:
ActionX_1(thread) ==
    /\ pc[thread] = PC_ActionX_1
    /\ pc' = [pc EXCEPT ![thread] = PC_Start]
    /\ y' = y + 2
    /\ UNCHANGED <<x, z>>

\* After:
ActionX_1(thread) ==
    /\ pc[thread] = PC_ActionX_1
    /\ pc' = [pc EXCEPT ![thread] = PC_ActionX_2]
    /\ y' = y + 2
    /\ UNCHANGED <<x, z>>

ActionX_2(thread) == ... will be created in the next step ...
```

**With user instructions (specific split):**

If user specifies which variables to update in first vs second action, follow those instructions:

```tla
\* User says: "Update x in first action, y in second"

\* Before:
ActionX_1(thread) ==
    /\ pc[thread] = PC_ActionX_1
    /\ pc' = [pc EXCEPT ![thread] = PC_Start]
    /\ x' = x + 1
    /\ y' = y + 2
    /\ UNCHANGED <<z>>

\* After:
ActionX_1(thread) ==
    /\ pc[thread] = PC_ActionX_1
    /\ pc' = [pc EXCEPT ![thread] = PC_ActionX_2]
    /\ x' = x + 1 \* User-specified update in first action
    /\ UNCHANGED <<y, z>>

ActionX_2(thread) == ... will be created in the next step ...
```

### Step 5: Create the New Action:

Create the new action that:
1. Guards on the new intermediate PC state
2. Transitions to the ORIGINAL destination state
3. Contains the logic from the original action (or as specified by user)
4. Has appropriate UNCHANGED statement

```tla
ActionX_2(thread) ==                            \* New action
    /\ pc[thread] = PC_ActionX_2
    /\ pc' = [pc EXCEPT ![thread] = PC_Start]   \* Original destination
    /\ y' = y + 2                               \* Logic from original (or per user)
    /\ UNCHANGED <<x, z>>
```

### Step 6: Renumber Subsequent Actions (if needed)

If the naming convention uses numbers and there are subsequent actions that would conflict:

**Before splitting:**
```tla
ActionX_0(thread) == ...  \* PC_ActionX_0 -> PC_ActionX_1
ActionX_1(thread) == ...  \* PC_ActionX_1 -> PC_Start (TO BE SPLIT)
```

**After splitting:**
```tla
ActionX_0(thread) == ...  \* PC_ActionX_0 -> PC_ActionX_1 (unchanged)
ActionX_1(thread) == ...  \* PC_ActionX_1 -> PC_ActionX_2 (new destination)
ActionX_2(thread) == ...  \* PC_ActionX_2 -> PC_Start (NEW ACTION)
```

If splitting `ActionX_0` where `ActionX_1` already exists, renumber:

**Before:**
```tla
ActionX_0(thread) == ...  \* PC_ActionX_0 -> PC_ActionX_1 (TO BE SPLIT)
ActionX_1(thread) == ...  \* PC_ActionX_1 -> PC_Start
```

**After:**
```tla
ActionX_0(thread) == ...  \* PC_ActionX_0 -> PC_ActionX_1 (NEW intermediate)
ActionX_1(thread) == ...  \* PC_ActionX_1 -> PC_ActionX_2 (renumbered from old ActionX_1)
ActionX_2(thread) == ...  \* PC_ActionX_2 -> PC_Start (renumbered)
```

### Step 7: Update TypeOk Predicate

If TypeOk contains PCStates enumeration, add the new PC state:

```tla
\* Before:
TypeOk ==
    /\ pc \in [Threads -> PCStates]
    ...

\* If PCStates is defined separately, it was updated in Step 3.
\* If PCStates is inline, update it here.
```

### Step 8: Update Next Predicate (if needed)

If the Next predicate explicitly lists actions (not common), add the new action:

```tla
Next == \E thread \in Threads :
    \/ ActionX_0(thread)
    \/ ActionX_1(thread)
    \/ ActionX_2(thread)   \* Add new action
    ...
```

If actions are grouped (e.g., `ActionX(thread)` with internal disjunctions), the new disjunct is already included.

### Step 9: Update Fairness Constraints (if needed)

If fairness constraints reference specific PC states or actions, update them:

```tla
\* Before:
Fairness ==
    /\ WF_vars(ActionX_1(thread))

\* After - add fairness for new action:
Fairness ==
    /\ WF_vars(ActionX_1(thread))
    /\ WF_vars(ActionX_2(thread))
```

## UNCHANGED Statement Rules

When splitting an action, follow these rules for UNCHANGED:

1. **First action (intermediate step):**
   - If user specifies no variable updates: add ALL non-pc variables to UNCHANGED
   - If user specifies some updates: add remaining variables to UNCHANGED

2. **Second action (new action):**
   - Contains variables that are NOT modified in the new action
   - Typically mirrors the original UNCHANGED (unless user specifies otherwise)

3. **Never forget variables:** Every variable must either be primed (updated) or in UNCHANGED

## Verification Checklist

After splitting, verify:

- [ ] New PC state constant is defined
- [ ] New PC state is in PCStates set
- [ ] Original action transitions to new intermediate PC state
- [ ] New action guards on new PC state
- [ ] New action transitions to original destination
- [ ] All variables are either primed or in UNCHANGED (both actions)
- [ ] Naming follows spec convention (renumbered if needed)
- [ ] TypeOk updated if needed
- [ ] Next predicate includes new action (if explicitly listed)
- [ ] Fairness constraints updated if present

## Example: Full Split

**User request:** "Split ActionX_1 into two actions"

**Before:**
```tla
PC_ActionX_1 == "PC_ActionX_1"

PCStates == { PC_Ready, PC_ActionX_1 }

ActionX_0(thread) ==
    /\ pc[thread] = PC_Start
    /\ pc' = [pc EXCEPT ![thread] = PC_ActionX_1]
    /\ x' = x + 1
    /\ UNCHANGED <<y, z>>

ActionX_1(thread) ==
    /\ pc[thread] = PC_ActionX_1
    /\ pc' = [pc EXCEPT ![thread] = PC_Start]
    /\ y' = y + 2
    /\ UNCHANGED <<x, z>>
```

**After:**
```tla
PC_ActionX_1 == "PC_ActionX_1"
PC_ActionX_2 == "PC_ActionX_2"  \* NEW

PCStates == { PC_Ready, PC_ActionX_1, PC_ActionX_2 }  \* Updated

ActionX_0(thread) ==
    /\ pc[thread] = PC_Start
    /\ pc' = [pc EXCEPT ![thread] = PC_ActionX_1]
    /\ x' = x + 1
    /\ UNCHANGED <<y, z>>

ActionX_1(thread) ==
    /\ pc[thread] = PC_ActionX_1
    /\ pc' = [pc EXCEPT ![thread] = PC_ActionX_2]  \* Changed destination
    /\ UNCHANGED <<x, y, z>>                        \* All vars unchanged

ActionX_2(thread) ==                                \* NEW ACTION
    /\ pc[thread] = PC_ActionX_2
    /\ pc' = [pc EXCEPT ![thread] = PC_Start]
    /\ y' = y + 2
    /\ UNCHANGED <<x, z>>
```
