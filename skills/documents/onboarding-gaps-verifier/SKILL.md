---
name: onboarding-gaps-verifier
description: Identify documentation gaps and pitfalls. Creates gaps_pitfalls.md. Triggered by onboarding-start during gaps-pitfalls-identification phase.
---

# Onboarding Gaps Verifier

Identify gaps and pitfalls in code understanding, and verify onboarding documents.

## Workflow

### Phase 1: Gaps & Pitfalls Identification

Create `gaps_pitfalls.md` with three sections:

**1.1 Non-Obvious Requirements**

Review extracted info and source code for:
- Implicit assumptions in the code
- Required environment setup not mentioned
- Magic values or conventions
- Domain knowledge requirements

Example format:
```markdown
## Non-Obvious Requirements

1. **Environment**: Requires `ANTHROPIC_API_KEY` env var (not documented)
2. **Convention**: All handler functions must return dict with `status` key
3. **Assumption**: Input files must be UTF-8 encoded
```

**1.2 Ordering Dependencies**

Document what must happen in what order:
- Initialization sequences
- Setup before use
- Teardown requirements
- Circular dependencies (if any)

Example format:
```markdown
## Ordering Requirements

1. Initialize config before calling any API functions
2. Register handlers before starting the server
3. Close database connection after all queries complete
```

**1.3 Common Errors**

Based on code analysis, identify likely errors:
- Error messages that are misleading
- Edge cases that fail silently
- Common misconfigurations

Example format:
```markdown
## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `KeyError: 'data'` | Missing response field | Check API version |
| Silent failure | Empty input list | Validate input length |
```

## Key Questions

- What requires domain knowledge?
- What breaks if done out of order?
- What error messages are misleading?

## Success Criteria

`gaps_pitfalls.md`:
- [ ] At least 3 non-obvious items (or explicit "none found")
- [ ] All ordering dependencies documented
- [ ] At least 3 common errors with solutions (or explicit "none found")
