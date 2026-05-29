---
name: leverage-point-audit
description: Audit a codebase for the 12 leverage points of agentic coding. Identifies gaps and provides prioritized recommendations. Use when improving agentic coding capability, analyzing why agents fail, or optimizing a codebase for autonomous work.
allowed-tools: Read, Grep, Glob
---

# Leverage Point Audit

Audit a codebase against the 12 leverage points framework to identify gaps and improve agentic coding success.

## When to Use

- Before starting a new agentic coding project
- When agents are failing or requiring many attempts
- When KPIs (Size, Attempts, Streak, Presence) are not improving
- For periodic health checks of agentic capability

## The 12 Leverage Points

### In-Agent (Core Four)

1. **Context** - CLAUDE.md, README, project docs
2. **Model** - Appropriate model selection
3. **Prompt** - Clear instructions and templates
4. **Tools** - Required capabilities available

### Through-Agent (External)

1. **Standard Out** - Logging for visibility
2. **Types** - Information Dense Keywords (IDKs)
3. **Documentation** - Agent-specific context
4. **Tests** - Self-correction capability (HIGHEST LEVERAGE)
5. **Architecture** - Navigable codebase structure
6. **Plans** - Meta-work communication
7. **Templates** - Reusable prompts (slash commands)
8. **ADWs** - Autonomous workflows

## Audit Workflow

### Step 1: Check Context (Leverage Points 1-4)

**CLAUDE.md presence:**

```yaml
Search for: CLAUDE.md, .claude/CLAUDE.md
Check: Does it explain the project? Conventions? Common commands?
```

**README.md quality:**

```yaml
Search for: README.md
Check: Does it explain structure? How to run? How to test?
```

**Permissions configuration:**

```yaml
Search for: .claude/settings.json
Check: Are required tools allowed?
```

### Step 2: Check Visibility (Leverage Point 5)

**Standard out patterns:**

```yaml
Search for: print(, console.log(, logger., logging.
Check: Are success AND error cases logged?
Check: Can agent see what's happening?
```

**Anti-pattern detection:**

```text
Look for: Silent returns, bare except blocks, empty catch blocks
These prevent agent visibility.
```

### Step 3: Check Searchability (Leverage Point 6)

**Type definitions:**

```yaml
Search for: interface, type, class, BaseModel, dataclass
Check: Are names information-dense? (Good: UserAuthToken, Bad: Data)
```

### Step 4: Check Documentation (Leverage Point 7)

**Internal docs:**

```yaml
Search for: *.md files, docstrings, comments
Check: Do they explain WHY, not just WHAT?
```

### Step 5: Check Validation (Leverage Point 8) - HIGHEST PRIORITY

**Test presence:**

```yaml
Search for: test_*.py, *.test.ts, *.spec.ts, *_test.go
Check: Do tests exist? Are they comprehensive?
```

**Test commands:**

```yaml
Check: Is there a simple test command? (npm test, pytest, etc.)
Check: Do tests run quickly?
```

### Step 6: Check Architecture (Leverage Point 9)

**Entry points:**

```yaml
Check: Are entry points obvious? (main.py, index.ts, server.py)
```

**File organization:**

```yaml
Check: Consistent structure? Related files grouped?
Check: File sizes reasonable? (< 1000 lines)
```

### Step 7: Check Templates (Leverage Point 11)

**Slash commands:**

```yaml
Search for: .claude/commands/
Check: Are common workflows automated?
```

### Step 8: Check ADWs (Leverage Point 12)

**Automation:**

```yaml
Search for: GitHub Actions, hooks, triggers
Check: Are workflows automated?
```

## Output Format

After audit, provide:

### Summary Table

| Leverage Point | Status | Priority | Recommendation |
| --- | --- | --- | --- |
| Context | Good/Fair/Poor | High/Med/Low | Specific action |
| ... | ... | ... | ... |

### Priority Actions

List top 3-5 improvements in order of impact:

1. **[Highest Impact]** - Specific recommendation
2. **[High Impact]** - Specific recommendation
3. **[Medium Impact]** - Specific recommendation

### Detailed Findings

For each leverage point:

- Current state
- Specific gaps found
- Recommended improvements
- Example of what good looks like

## Example Audit Output

```markdown
## Leverage Point Audit Results

### Summary
- Tests: POOR (no test files found) - HIGHEST PRIORITY
- Standard Out: FAIR (some logging, missing error cases)
- Architecture: GOOD (clear structure, reasonable file sizes)

### Priority Actions
1. Add test suite - enables self-correction
2. Add error logging to API endpoints - enables visibility
3. Create /prime command - enables quick context

### Detailed Findings
[... specific recommendations ...]
```

## Related Memory Files

- @12-leverage-points.md - Complete framework reference
- @agentic-kpis.md - How to measure improvement
- @agent-perspective-checklist.md - Quick pre-task checklist

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
