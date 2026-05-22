---
name: test-from-docs
description: Generate and execute test plans based on documentation. Use after implementation to verify changes work correctly. Integrates with browser testing for UI verification.
allowed-tools: Read, Bash, Glob, Grep
---

# Test From Docs

Use documentation as the authoritative test blueprint. Tests verify intended behavior (from docs), not just current behavior.

## When to Use

- After implementing a feature or fix
- Before marking work as complete
- When user asks "does this work?"
- As part of pre-PR validation

## Risk-Based Test Selection

### Calculate Risk Score

| Factor | Points |
|--------|--------|
| Touches auth/RLS | +3 |
| Touches billing | +3 |
| Touches schema | +2 |
| Touches AI/prompts | +2 |
| Multi-feature change | +2 |
| User-facing workflow | +1 |
| New code (not fix) | +1 |

### Select Test Depth

| Score | Depth | What to Run |
|-------|-------|-------------|
| 0-2 | Light | Static + primary feature checklist |
| 3-5 | Standard | Light + impacted features + 1 workflow |
| 6-8 | Thorough | Standard + browser verification + regression |
| 9+ | Comprehensive | Full workflow suite + edge cases |

## Test Phases

1. **Static Analysis** — `npx tsc --noEmit && npm run lint`
2. **Feature Checklist** — Run items from feature doc's Testing Checklist
3. **Integration** — Verify cross-feature integration points
4. **Browser** — Visual verification with Playwright MCP
5. **Workflow Smoke** — One complete user journey
6. **Regression** — Verify coupled features still work

## Output

```markdown
## Test Report — [feature] — [date]

**Risk Score**: [n] ([depth level])

| Phase | Passed | Failed |
|-------|--------|--------|
| Static | [n] | [n] |
| Feature | [n] | [n] |
| Browser | [n] | [n] |
| Workflow | [n] | [n] |

**Overall**: ✅ PASS / ❌ FAIL

### Failures
[Test name, expected, actual, evidence]

**Ready for Merge**: [Yes/No]
```

## Related

- Phase details: See [reference/test-phases.md](reference/test-phases.md)
- Templates by change type: See [reference/test-templates.md](reference/test-templates.md)
- Browser testing commands: See [reference/browser-testing.md](reference/browser-testing.md)
- For comprehensive testing: `/spawn-test-agent`
