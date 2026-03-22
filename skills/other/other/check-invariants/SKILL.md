---
name: check-invariants
description: Spot-check architectural invariants against actual code
context: fork
agent: Explore
---

You are a **Principal Engineer** spot-checking architectural invariants from docs/ARCHITECTURAL-INVARIANTS.md against actual code. This is READ-ONLY, do not modify files.

## Checks

1. **ES-002**: EventStore interface in repository/eventstore.go has NO Update or Delete methods (append-only)
2. **ES-005**: Check that domain event types implement the Event interface (have EventType(), AggregateID(), OccurredAt() methods) - spot-check 3 event types
3. **ES-007**: All event types in DecodeEvent() switch - are there any domain event types NOT covered?
4. **DB-001**: Do postgres/ and sqlite/ have matching function signatures? Compare exported function names.
5. **DM-001**: Do domain entities have UUID ID fields set by constructors? Spot-check Person, Family, Source.
6. **DM-002**: Do domain entities have Validate() methods? Check Person, Family, Source.
7. **PR-004**: Compare event types in DecodeEvent() with cases in projection.go - any events missing projection handlers?

## Output Format

Report each as PASS/WARN/FAIL with specifics.
