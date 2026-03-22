---
name: specsafe-done
description: Complete and archive spec
argument-hint: "[spec-id]"
disable-model-invocation: true
---

Finalize spec after all tests pass:
- Verify completion checklist
- Run final test suite
- Move specs/active/SPEC-ID.md → specs/archive/SPEC-ID.md
- Update PROJECT_STATE.md (VERIFY → COMPLETE)
- Generate completion summary
- Suggest next spec from active list

Ask for confirmation before archiving.
