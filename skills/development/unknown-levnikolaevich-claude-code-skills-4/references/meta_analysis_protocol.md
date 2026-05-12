<!-- SOURCE-OF-TRUTH: shared/references/meta_analysis_protocol.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Meta-Analysis Protocol

Optional post-run self-audit for skills that need protocol-formatted reflection. Do not load this file by default; load it only when the user asks for meta-analysis, when a command explicitly requires a run retrospective, or when debugging repeated skill failures.

## Use When Requested

Produce only actionable findings from the current run:
- deliverable gaps against the user's goal
- failed, wasted, or repeated tool/agent steps
- worker or subagent failures that changed the result
- concrete skill or command improvements tied to observed evidence

Skip generic SDLC commentary. If there are no findings, write: `Meta-analysis: clean run.`

## Output

```markdown
### Meta-Analysis: {Skill Name}

#### Improvements
| # | Finding | Target | Fix |
|---|---------|--------|-----|
| 1 | {observed issue} | {skill/phase/file} | {specific change} |

#### Session Errors
| Problem Type | Count | Examples |
|--------------|-------|----------|
| {type} | {N} | {brief examples} |
```

Omit empty sections. For subagents, add a separate `#### Subagent Errors: {Agent Name}` table only when that agent had material failures.

## Issue Suggestion Trigger

If the same failure pattern is reproducible across multiple runs, suggest creating an issue with the affected skill, evidence, and expected fix.

---
**Version:** 4.2.0
**Last Updated:** 2026-03-21
