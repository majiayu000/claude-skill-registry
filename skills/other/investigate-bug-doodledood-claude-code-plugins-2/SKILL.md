---
name: investigate-bug
description: Deep bug investigation using consultant agent. Identifies root causes and fix suggestions.
---

Investigate bug: $ARGUMENTS

---

Launch the consultant:consultant agent. The agent gathers symptoms, invokes the consultant CLI, and reports root cause analysis.

**Investigation focus**:
1. **Root cause**: What's actually broken and why
2. **Execution flow**: Path from trigger to failure
3. **State analysis**: Invalid states, race conditions, timing issues
4. **Data validation**: Input validation gaps, edge cases
5. **Error handling**: Missing handlers, improper recovery

**Severity levels**:
- **CRITICAL**: Production down, data corruption, widespread impact
- **HIGH**: Core functionality broken, major user impact
- **MEDIUM**: Feature partially broken, workaround available
- **LOW**: Minor issue, limited impact
