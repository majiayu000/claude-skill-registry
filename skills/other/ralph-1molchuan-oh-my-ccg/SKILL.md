---
name: ralph
description: 持久化执行-验证-修复循环，直到任务完成
---

# oh-my-ccg Ralph Mode

"The boulder never stops." Persistent loop that keeps working until verification passes.

## Activation
Trigger: "ralph", "don't stop"

## Loop Structure
```
Start (iteration 0)
  │
  ├─ Execute: Run the task (executor agent)
  ├─ Verify: Check results (verifier agent)
  │   ├─ Tests pass?
  │   ├─ Build succeeds?
  │   └─ LSP clean?
  │
  ├─ All pass? → COMPLETE ✅
  └─ Any fail? → Fix issues → Next iteration
      └─ Max iterations (10)? → STOP with report
```

## Implementation Steps

1. Initialize ralph state: iteration=0, maxIterations=10
2. Execute the current task using executor agent
3. Run verification:
   - `npm test` or equivalent
   - `tsc --noEmit`
   - LSP diagnostics check
4. If verification passes: mark complete, deactivate ralph
5. If verification fails:
   - Increment iteration
   - Analyze failures with debugger agent
   - Apply fixes
   - Return to step 2
6. If max iterations reached: stop, report remaining issues

## State
Tracked in `.oh-my-ccg/state/ralph-state.json`:
- iteration, maxIterations
- lastVerification (tests, build, lsp, issues)
- active flag

## Integration
- Works inside autopilot (auto-impl uses ralph per task)
- Works standalone for any execution task
- Stop hook prevents Claude from stopping while ralph is active
