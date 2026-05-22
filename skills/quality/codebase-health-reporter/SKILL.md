---
name: Codebase Health Reporter
description: Generate comprehensive health report for Leavn codebase - metrics, technical debt, bugs found/fixed, recommendations for next session
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Codebase Health Reporter

Generate health metrics and recommendations:

1. **Collect metrics**:
   - Lines of code: `find LeavnApp -name "*.swift" | xargs wc -l`
   - File count: `find LeavnApp -name "*.swift" | wc -l`
   - Git stats: `git log --oneline -20`
   - Code deleted: `git diff --shortstat main`

2. **Audit key areas**:
   - @Published usage: `grep -r "@Published" | wc -l`
   - try! force unwraps: `grep -r "try!" | wc -l`
   - Empty catches: `grep -r "} catch {}" | wc -l`
   - UserDefaults: `grep -r "UserDefaults.standard" | wc -l`

3. **Create report sections**:
   - Session summary (bugs fixed, lines changed)
   - Technical debt (remaining issues)
   - Recommendations (prioritized by impact)
   - Ship readiness checklist

4. **Output**: `CODEBASE_HEALTH_REPORT.md`

Use when: Session complete, need status report, planning next work, ship decision
