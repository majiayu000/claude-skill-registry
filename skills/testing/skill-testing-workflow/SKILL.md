---
name: testing-workflow
description: Integrated testing workflow combining all testing tools and MCPs. Use when deciding which testing tools to use, planning testing strategy, or executing tests in different environments and phases. Tags official skills: wallaby-testing, web-browser, agent-browser. Triggers on "testing workflow", "which test tool", "testing strategy", "run tests", "test combination".
---

# Testing Workflow

## Purpose

Guide the selection and combination of testing tools based on environment, phase, and test type. This skill integrates multiple testing tools into coherent workflows.

**Official Skills Referenced:**
- `wallaby-testing` - Unit/integration tests with live feedback
- `web-browser` - Chrome DevTools for debugging and performance
- `agent-browser` - Browser automation for E2E testing

## When to Use

- Deciding which testing tools to use
- Planning testing strategy for a feature
- Executing tests in different environments
- Combining multiple testing tools
- Setting up testing workflow for team

## Tool Overview Matrix

| Tool | Type | Best For | Environment |
|------|------|----------|-------------|
| **Wallaby** | Unit/Integration | TDD, live feedback, logic testing | VS Code (local/codespace) |
| **Chrome DevTools MCP** | Debug/Performance | Runtime debugging, layout issues, performance | Any with Chrome |
| **Agent Browser CLI** | E2E Exploration | Quick E2E flows, user journey discovery | Local |
| **TestSprite MCP** | E2E Stable | Regression testing, pre-PR validation | All |
| **Container-Use MCP** | Isolated Tests | Build tests, experiments, A/B testing | Local only |

## Environment-Based Workflows

### Codespace / VS Code Web

**Available Tools:**
- ✅ Wallaby MCP (if configured)
- ✅ Chrome DevTools MCP (via remote Chrome)
- ✅ TestSprite MCP
- ❌ Agent Browser CLI (not recommended - heavy)
- ❌ Container-Use (local only)

**Recommended Workflow:**

```markdown
## Development Loop (Codespace)

1. **Start Dev Server**
   - DevServer MCP monitors for errors

2. **Unit/Integration Testing**
   - Use: **Wallaby MCP** (if available)
   - Alternative: `npm test` / `pytest`

3. **Runtime Debugging**
   - Use: **Chrome DevTools MCP**
   - For: Layout issues, console errors, performance

4. **Pre-PR Validation**
   - Use: **TestSprite MCP** (skill-testsprite-pre-pr)
   - Run: Full E2E suite
```

### Local Development

**Available Tools:**
- ✅ All tools available

**Recommended Workflow:**

```markdown
## Development Loop (Local)

1. **Start Dev Server**
   - DevServer MCP monitors

2. **TDD - Unit/Integration**
   - Use: **Wallaby MCP**
   - Real-time feedback as you type

3. **Explore E2E Flows**
   - Use: **Agent Browser CLI**
   - Quick iteration on user journeys
   - Command: `agent-browser open http://localhost:5173`

4. **Debug Issues**
   - Use: **Chrome DevTools MCP**
   - Deep inspection of problems

5. **Stable E2E Tests**
   - Promote from Agent Browser to **TestSprite MCP**
   - Add to regression suite

6. **Experiments/Build Tests**
   - Use: **Container-Use MCP** (optional)
   - Isolated environment testing
```

### Container / Docker

**Available Tools:**
- ✅ Unit tests (via container)
- ✅ TestSprite MCP
- ❌ Wallaby (UI not available)
- ❌ Chrome DevTools (no browser)
- ❌ Agent Browser (no browser)

**Recommended Workflow:**

```markdown
## Development Loop (Container)

1. **Unit Tests**
   - Run: `npm test` / `pytest` in container
   - No live feedback - run manually

2. **E2E Tests**
   - Use: **TestSprite MCP** (external browser)
   - Or: Run Playwright in container with display
```

## Phase-Based Workflows

### Phase 1: Feature Development (Branch)

```markdown
## Feature Development Testing

### Continuous (as you code)
- **Wallaby MCP**: Live unit test feedback
- **DevServer MCP**: Build error monitoring

### On Demand
- **Chrome DevTools MCP**: Debug visual/runtime issues
- **Agent Browser CLI**: Explore E2E scenarios

### Before Commit
- Run unit tests: `npm test`
- Verify no regressions
```

### Phase 2: Integration (Task/PRD Complete)

```markdown
## Integration Testing

### Full Unit/Integration Suite
```bash
npm test -- --coverage
# or
pytest --cov=src
```

### E2E Smoke Test
- **Agent Browser CLI**: Quick validation
  ```bash
  agent-browser open http://localhost:5173
  agent-browser snapshot -i
  # Verify critical paths work
  ```

### Debug Issues
- **Chrome DevTools MCP**: For any failures
```

### Phase 3: Pre-PR (Ready for Review)

```markdown
## Pre-PR Testing (skill-testsprite-pre-pr)

### Comprehensive E2E
- **TestSprite MCP**: Full test suite
  - Bootstrap: `testsprite_bootstrap_tests`
  - Generate: `testsprite_generate_tests`
  - Run: `testsprite_run_tests`
  - Analyze: `testsprite_analyze_results`

### Human Review Points (HITL)
1. Review generated test plan
2. Confirm backend/frontend scope
3. Approve diff vs codebase testing

### All Green?
- ✅ Open PR
- ❌ Fix failures, re-run
```

## Tool Combination Scenarios

### Scenario: New API Endpoint

```markdown
## Testing New API Endpoint

1. **Wallaby MCP**: Unit test the handler
   ```typescript
   test('POST /api/users creates user', async () => {
     const res = await request(app)
       .post('/api/users')
       .send({ name: 'John' });
     expect(res.status).toBe(201);
   });
   ```

2. **Agent Browser CLI**: E2E test the flow
   ```bash
   agent-browser open http://localhost:5173/signup
   agent-browser fill @email "john@example.com"
   agent-browser click @submit
   agent-browser wait --text "Welcome"
   ```

3. **TestSprite MCP**: Add to regression
   - Generate stable test from Agent Browser flow
   - Include in pre-PR suite
```

### Scenario: UI Bug Fix

```markdown
## Testing UI Bug Fix

1. **Chrome DevTools MCP**: Reproduce and inspect
   - Screenshot before fix
   - Check computed styles
   - Verify DOM structure

2. **Wallaby MCP**: Add regression test
   - Test component renders correctly
   - Test interaction works

3. **Agent Browser CLI**: Verify E2E
   - Full user flow through affected area
```

### Scenario: Performance Issue

```markdown
## Testing Performance Fix

1. **Chrome DevTools MCP**: Measure before/after
   - Performance trace
   - LCP, FID, CLS metrics
   - Network waterfall

2. **TestSprite MCP**: Regression prevention
   - Add performance assertions
   - Monitor in CI
```

## Quick Decision Tree

```
What do you need to test?
│
├─→ Unit/Integration logic
│   └─→ VS Code? → Wallaby MCP
│   └─→ Other? → npm test / pytest
│
├─→ Visual/DOM/Runtime issue
│   └─→ Chrome DevTools MCP
│
├─→ Explore E2E flow (new feature)
│   └─→ Local? → Agent Browser CLI
│   └─→ Codespace? → Chrome DevTools MCP
│
├─→ Stable E2E regression
│   └─→ TestSprite MCP
│
└─→ Build/Experiment isolation
    └─→ Local? → Container-Use MCP
    └─→ Other? → Not available
```

## Official Skill References

### wallaby-testing

```markdown
**Use when:**
- In VS Code
- Need live test feedback
- Debugging failing tests
- Checking coverage

**Key tools:**
- wallaby_failingTests
- wallaby_runtimeValues
- wallaby_coveredLinesForFile
- wallaby_updateTestSnapshots

**See:** `wallaby-skill/SKILL.md`
```

### web-browser (Chrome DevTools)

```markdown
**Use when:**
- Debugging runtime issues
- Analyzing performance
- Inspecting DOM/network
- Taking screenshots

**Key commands:**
- Start: `./scripts/start.js`
- Navigate: `./scripts/nav.js`
- Screenshot: `./scripts/screenshot.js`
- Eval: `./scripts/eval.js`

**See:** `web-browser-CHROME-DEV-TOOLS-skill/SKILL.md`
```

### agent-browser

```markdown
**Use when:**
- E2E exploration
- Quick user journey validation
- Form testing
- Multi-step flows

**Key commands:**
- Open: `agent-browser open <url>`
- Snapshot: `agent-browser snapshot -i`
- Interact: `agent-browser click @ref`
- Fill: `agent-browser fill @ref "text"`

**See:** `agent-browser-skill/SKILL.md`
```

## Anti-Patterns to Avoid

### ❌ Running All Tools Simultaneously

Don't run Chrome DevTools MCP + Agent Browser + TestSprite all at once locally. Too heavy.

**Instead:** Use one E2E tool at a time:
- Agent Browser for exploration
- TestSprite for stable tests

### ❌ Wrong Tool for Job

| Wrong | Right |
|-------|-------|
| Agent Browser for unit tests | Wallaby/npm test |
| Chrome DevTools for TDD | Wallaby |
| TestSprite for exploration | Agent Browser |
| Wallaby for E2E | TestSprite |

### ❌ Skipping Layers

Don't jump to E2E without unit tests. Test pyramid:
- 70% Unit (Wallaby)
- 20% Integration
- 10% E2E (TestSprite)

## Integration with Other Skills

| Skill | When to Use |
|-------|-------------|
| skill-test-setup | Initial configuration |
| skill-testing-philosophy | Understanding TDD |
| skill-testsprite-pre-pr | Pre-PR validation |

## Version

v1.0.0 (2025-01-28) - Integrated testing workflow