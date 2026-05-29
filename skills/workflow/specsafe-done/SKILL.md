---
name: specsafe-done
description: Mark spec complete and archive. Moves spec from QA to COMPLETE stage.
disable-model-invocation: true
---

Mark a specification as complete and archive it (QA → COMPLETE stage).

**When to use:**
- QA validation passed with GO recommendation
- All requirements satisfied
- Ready to mark as production-ready
- Feature is done and tested

**Input**: The spec ID (e.g., SPEC-20260211-001)

**Steps**

1. **Validate QA passed**

   Check `specs/active/<spec-id>.md`:
   - Status must be QA stage
   - QA report exists and recommends GO
   - All critical issues resolved

   Verify QA report shows:
   - All tests passing
   - Requirements satisfied
   - Coverage targets met

2. **Final review**

   Confirm with user (if interactive):
   - "All P0 requirements satisfied?"
   - "Tests passing with adequate coverage?"
   - "Ready to mark as complete?"

3. **Complete the spec**

   ```bash
   specsafe complete "<spec-id>"
   ```

   This:
   - Moves spec status to COMPLETE
   - Moves spec file to `specs/completed/`
   - Archives QA report
   - Updates PROJECT_STATE.md
   - Records completion timestamp

4. **Generate completion summary**

   Document the completed work:
   ```markdown
   ## Completion Report: SPEC-YYYYMMDD-NNN
   
   ### Summary
   - Feature: [Name]
   - Duration: [Start → End dates]
   - Status: ✅ COMPLETE
   
   ### Metrics
   - Requirements: [N total, N P0]
   - Tests: [N created, N passing]
   - Coverage: [N%]
   - Commits: [N commits]
   
   ### Artifacts
   - Spec: specs/completed/SPEC-YYYYMMDD-NNN.md
   - Tests: [test file locations]
   - Implementation: [source file locations]
   
   ### Notes
   - [Any important notes about implementation]
   ```

5. **Update PROJECT_STATE.md**

   Record:
   - Completed specs list
   - Total completed count
   - Recent completions

6. **Show completion confirmation**

   Display:
   - ✅ Completion confirmation
   - Spec moved to `specs/completed/`
   - Metrics summary
   - Project stats update
   - Next steps prompt

**Output**

After completion:
- ✅ Spec marked COMPLETE
- ✅ Spec archived to `specs/completed/`
- ✅ QA report archived
- ✅ PROJECT_STATE.md updated
- ✅ Completion report generated
- 📋 Prompt: "Ready to start a new spec? Run `/specsafe:new <feature>`"

**Guardrails**
- ⛔ Spec must be in QA stage
- ⛔ QA report must recommend GO (not NO-GO)
- ⛔ Do NOT complete if critical issues remain
- ✅ Confirm all P0 requirements met
- ✅ Verify test coverage meets targets
- Archive all related artifacts
- Keep completed specs for historical reference

**Example**
```
User: /specsafe:done SPEC-20260211-004
→ Validating QA report... ✅
→ All tests passing ✅
→ Coverage: 94% ✅
→ Moving to completed/... ✅
→ 
→ ╔═══════════════════════════════════════╗
→ ║   SPEC-20260211-004 COMPLETE! 🎉      ║
→ ╠═══════════════════════════════════════╣
→ ║  Duration: 3 days                     ║
→ ║  Requirements: 8 (3 P0)               ║
→ ║  Tests: 12 (all passing)              ║
→ ║  Coverage: 94%                        ║
→ ║  Commits: 7                           ║
→ ╚═══════════════════════════════════════╝
→ 
→ 📂 Archived to: specs/completed/SPEC-20260211-004-user-authentication.md
→ 📊 Project: 3 active, 12 completed
→ 
→ Ready for next spec? /specsafe:new <feature-name>
```