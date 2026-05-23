---
name: distributed-processor
description: "Coordinate distributed processing with parallel execution, forked skills, and isolated work units. Use when you need distributed processing or isolated work units. Not for sequential tasks or single-threaded workflows."
context: fork
---

# Distributed Data Processing

Coordinate distributed data processing using TaskList with forked skills.

## Processing Architecture

**Three-component system:**

- **Coordinator** uses TaskList to track all processing tasks
- **Region processors** are forked skills with complete isolation
- **Results flow back** to coordinator for aggregation

## Processing Tasks

**Parallel, independent execution:**

1. **process-region-a** - Process data from Region A
   - Forked skill processes in isolation

2. **process-region-b** - Process data from Region B
   - Forked skill processes in isolation

3. **process-region-c** - Process data from Region C
   - Forked skill processes in isolation

4. **aggregate-results** - Combine all processed outputs
   - Wait for all region processors to complete
   - Aggregate results into final dataset

## Execution Workflow

**Execute autonomously:**

1. **Create TaskList** with all tasks
2. **Use Skill tool** with context: fork for each region processor
3. **Monitor task completion**
4. **Aggregate results** when all processors complete
5. **Return aggregated dataset**

**Recognition test:** Each region processor runs in complete isolation with no shared state.

## Expected Output

```
Distributed Processing: COORDINATING
[task-id] process-region-a: IN_PROGRESS -> COMPLETE
[task-id] process-region-b: IN_PROGRESS -> COMPLETE
[task-id] process-region-c: IN_PROGRESS -> COMPLETE
[task-id] aggregate-results: BLOCKED -> IN_PROGRESS -> COMPLETE

=== AGGREGATED RESULTS ===
Region A: [records processed, summary]
Region B: [records processed, summary]
Region C: [records processed, summary]

Total: [combined statistics]
```

## Validation Criteria

- Parallel execution of regions
- Results aggregation after completion

**Binary check:** "Proper distributed processing?" → Both criteria must pass.

---

<critical_constraint>
MANDATORY: Wait for all processors to complete before aggregation
MANDATORY: Use TaskList to track all distributed tasks
MANDATORY: Ensure forked skills have complete isolation
No exceptions. Parallel execution requires proper coordination.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
