---
name: test-spec-gen
description: Universal test specification generator that explores codebases, researches best practices, and generates comprehensive test specs via multi-agent orchestration. Outputs Hermes-style test specification documents with TC-XXX formatting, area segmentation, and optional Trello card conversion.
user-invocable: true
---

# Test Specification Generator Skill

> Generates production-grade test specifications for any application through multi-agent exploration, research, and specialist generation.

## UX Contract
1. User runs `/test-spec-gen [optional-filter]`
2. Skill enters plan mode, presents approach, gets approval
3. Executes multi-agent pipeline silently
4. Presents test spec document for review
5. Iterates with quick-clarify until satisfied
6. Offers Trello card conversion

## Phase 0: Plan Mode Entry (CRITICAL)

**HARD GATE**: Do NOT proceed with any exploration, research, or generation until plan mode is approved.

Upon invocation:
1. Read existing codebase to understand project type (web/desktop/mobile)
2. Present the multi-agent approach with estimated agent count
3. Ask user approval to proceed
4. Only AFTER approval, begin the exploration phase

### Plan Mode Presentation Template

```
# Test Specification Generator

I will generate a comprehensive test specification for this project using multi-agent orchestration:

## Discovery Phase (5 parallel agents)
- Agent 1: Routes & Pages exploration
- Agent 2: Auth & RBAC mapping
- Agent 3: Data & Backend analysis
- Agent 4: Framework & Config discovery
- Agent 5: Navigation & UX flows

## Research Phase
- /research-before-coding based on discovery findings

## Generation Phase (5 specialist agents)
- Domains determined from exploration + research
- Each generates TC-XXX formatted test cases

## Verification Phase
- Doubt agent review for maintenance burden prevention
- Traceability matrix generation

## Output
- Hermes-style test specification document
- Optional Trello card conversion via /trello-test

Proceed?
```

### EnterPlanMode Trigger

Call `EnterPlanMode()` immediately after UX Contract section with this prompt:

```
Generate test specification for [project_name] using multi-agent orchestration:

1. Discovery: 5 parallel explore agents map codebase
2. Research: /research-before-coding for best practices
3. Generation: 5 specialist agents create TC-XXX test cases
4. Verification: Doubt agent review + traceability matrix
5. Output: Test spec doc + optional Trello conversion
```

Wait for user approval before proceeding to Phase 1.

## Phase 0.5: Dependency Pre-flight Check

After plan approval, BEFORE any exploration:

### Check Required MCP Servers

```bash
# Check if MCP servers are configured
grep -E "perplexity|context7|playwright|trello" ~/.claude/mcp_config.json || echo "MISSING"
```

### Check Test Frameworks

Detect project type and verify:

```bash
# Node.js projects
[ -f "package.json" ] && grep -E "(playwright|pytest|vitest|jest)" package.json || echo "NO TEST FRAMEWORK"

# Python projects
[ -f "pyproject.toml" ] && grep -E "(pytest|playwright)" pyproject.toml || echo "NO TEST FRAMEWORK"
```

### Auto-fix with Confirmation

For each missing dependency:

```
❌ Missing: [dependency]
  Impact: [what breaks without it]
  Auto-fix: [command to install]
  Approve? (Y/n)
```

If user declines:
- Log the refusal
- Continue only if non-critical
- Refuse to proceed if critical blocker

### Critical vs Non-critical

**Critical (must refuse without):**
- MCP servers for exploration (file read tools)
- Basic test framework detection

**Non-critical (can continue with warning):**
- Trello API (only needed for card conversion)
- Visual regression tools
- Performance monitoring tools

### MCP Discovery Commands

```bash
# Check MCP config directly
grep -E "perplexity|context7|playwright|trello" ~/.claude/mcp_config.json 2>/dev/null && echo "MCP servers configured" || echo "Some MCP servers missing"

# Alternative: check ~/.claude.json (Claude Code's actual registry)
grep -E "perplexity|context7|playwright|trello" ~/.claude.json 2>/dev/null | grep -q "mcp" && echo "MCP servers registered" || echo "Some MCP servers missing"
```

## Phase 1: Codebase Discovery (5 Parallel Agents)

Spawn 5 independent explore agents using Task tool. All agents run in parallel with no shared state.

### Agent 1: Routes & Pages Explorer

```
Task(
  subagent_type: "Explore",
  model: "haiku",
  description: "Explore routes and pages",
  prompt: `You are a route and page discovery agent.

OBJECTIVE: Map ALL routes, pages, and UI components in this codebase.

OUTPUT FORMAT (JSON):
{
  "routes": [
    {"path": "/path", "component": "ComponentName", "file": "src/file.tsx", "type": "page|api|static"}
  ],
  "pages": [
    {"name": "Dashboard", "route": "/", "file": "src/pages/Dashboard.tsx", "key_elements": ["stats", "charts"]}
  ],
  "navigation": [
    {"from": "Sidebar", "to": "Dashboard", "label": "Home"}
  ]
}

SEARCH STRATEGY:
1. Find router configuration (App.tsx, router.ts, routes/)
2. Find page components (pages/, views/, screens/)
3. Find navigation components (Nav.tsx, Sidebar.tsx, Header.tsx)
4. Extract route-to-component mappings

Return ONLY the JSON. No explanation.`
)
```

### Agent 2: Auth & RBAC Explorer

```
Task(
  subagent_type: "Explore",
  model: "haiku",
  description: "Explore auth and RBAC",
  prompt: `You are an authentication and authorization discovery agent.

OBJECTIVE: Map ALL auth mechanisms, roles, permissions, and access controls.

OUTPUT FORMAT (JSON):
{
  "auth_mechanism": "jwt|session|oauth|none",
  "roles": ["admin", "user", "guest"],
  "permissions": ["create:resource", "read:resource"],
  "auth_files": ["src/middleware/auth.ts"],
  "protected_routes": [
    {"route": "/admin", "roles": ["admin"], "guard": "requireAuth"}
  ],
  "login_endpoint": "/api/auth/login"
}

SEARCH STRATEGY:
1. Find auth middleware (auth.ts, middleware/, guards/)
2. Find role definitions (roles.ts, permissions.ts)
3. Find protected route decorators/middleware
4. Find login/logout endpoints

Return ONLY the JSON. No explanation.`
)
```

### Agent 3: Data & Backend Explorer

```
Task(
  subagent_type: "Explore",
  model: "haiku",
  description: "Explore data and backend",
  prompt: `You are a data and backend discovery agent.

OBJECTIVE: Map ALL data models, API endpoints, and persistence mechanisms.

OUTPUT FORMAT (JSON):
{
  "database": "postgres|mongodb|sqlite|none",
  "orm": "prisma|drizzle|sequelize|none",
  "models": [
    {"name": "User", "fields": ["id", "email", "role"], "file": "models/User.ts"}
  ],
  "api_endpoints": [
    {"method": "GET", "path": "/api/users", "controller": "UserController"}
  ],
  "persistence_files": ["db/schema.prisma"]
}

SEARCH STRATEGY:
1. Find schema definitions (schema.prisma, models/, entities/)
2. Find API routes (api/, routes/, controllers/)
3. Find database config (db.ts, database.ts)
4. Find ORM usage (prisma., drizzle., sequelize.)

Return ONLY the JSON. No explanation.`
)
```

### Agent 4: Framework & Config Explorer

```
Task(
  subagent_type: "Explore",
  model: "haiku",
  description: "Explore framework and config",
  prompt: `You are a framework and configuration discovery agent.

OBJECTIVE: Map framework, build tooling, CI config, and environment setup.

OUTPUT FORMAT (JSON):
{
  "framework": "react|vue|svelte|next|nuxt|custom",
  "language": "typescript|javascript|python",
  "build_tool": "vite|webpack|rollup|none",
  "test_framework": "playwright|jest|vitest|pytest|none",
  "ci_system": "github-actions|gitlab-ci|none",
  "env_files": [".env", ".env.example"],
  "config_files": ["next.config.js", "vite.config.ts"]
}

SEARCH STRATEGY:
1. Check package.json for dependencies
2. Check for framework config files
3. Check .github/workflows/ for CI
4. Check for .env files

Return ONLY the JSON. No explanation.`
)
```

### Agent 5: Navigation & UX Explorer

```
Task(
  subagent_type: "Explore",
  model: "haiku",
  description: "Explore navigation and UX",
  prompt: `You are a navigation and user experience discovery agent.

OBJECTIVE: Map navigation flows, state management, and user interactions.

OUTPUT FORMAT (JSON):
{
  "navigation_structure": {
    "main": ["Dashboard", "Settings"],
    "sidebar": ["Items", "Reports"]
  },
  "state_management": "redux|zustand|context|none",
  "key_flows": [
    {"name": "Login", "steps": ["Enter credentials", "Submit", "Redirect"]}
  ],
  "interactive_elements": ["forms", "modals", "dropdowns"]
}

SEARCH STRATEGY:
1. Find navigation components (Nav, Sidebar, Menu)
2. Find state management (store.ts, context/, redux/)
3. Find form components (Form.tsx, Input.tsx)
4. Find modal/dialog components

Return ONLY the JSON. No explanation.`
)
```

### Aggregate Discovery Results

After all 5 agents complete, aggregate their JSON outputs into a single discovery document:

```markdown
## Discovery Summary

### Routes & Pages: [count] routes mapped
### Auth & RBAC: [mechanism] with [count] roles
### Data & Backend: [database] with [orm]
### Framework: [framework] with [test_framework]
### Navigation & UX: [state_management] with [count] key flows
```

## Phase 2: Targeted Research

After discovery, invoke `/research-before-coding` with context from all 5 explore agents.

### Research Agent Prompt

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Research test generation best practices",
  prompt: `You are a research distillation agent for test generation.

CONTEXT FROM DISCOVERY:
Framework: {framework}
Auth: {auth_mechanism}
Database: {database}
Test Framework: {test_framework}

RESEARCH TOPIC: Test generation best practices for {framework} applications

CALLER NEEDS TO KNOW:
1. What are the test patterns for {framework}?
2. How to handle {auth_mechanism} in tests?
3. What are the common pitfalls for {database} testing?
4. What test coverage is industry standard for this stack?

LIBRARIES IN SCOPE: {framework}, {test_framework}, {orm}

## Step 1: Perplexity Research (3 queries)

perplexity_batch(queries: [
  {"query": "best practices {framework} {test_framework} testing 2026", "mode": "auto", "id": "practices"},
  {"query": "{framework} architecture patterns test automation", "mode": "auto", "id": "architecture"},
  {"query": "github {framework} {test_framework} examples production", "mode": "auto", "id": "examples"}
])

## Step 2: Context7 Documentation Queries (3 queries)

1. resolve-library-id("{framework}") -> query-docs(id, "testing fixtures patterns")
2. resolve-library-id("{test_framework}") -> query-docs(id, "test organization structure")
3. resolve-library-id("{orm}") -> query-docs(id, "database testing patterns")

## Step 3: Divergent WebSearch (exactly 1)

WebSearch("problems with {framework} automated testing flaky tests alternatives")

## Step 4: Distill

Produce this output format:

---
## Research: {Framework} Test Generation

### Recommended Approach
- **Pattern**: [pattern name]
- **Tools**: [recommended tools]
- **Why**: [rationale]

### Key Test Patterns
[code pattern]

### Pitfalls to Avoid
- [pitfall 1]
- [pitfall 2]

### Test Domains to Cover
Based on research, these test domains are recommended:
1. [Domain 1]
2. [Domain 2]
3. [Domain 3]
4. [Domain 4]
5. [Domain 5]
---

Return ONLY this distilled output.`
)
```

### Determine Test Domains

From research output, extract the 5 test domains for specialist agents.

**Fallback domains if research doesn't specify:**
1. UI Component Testing
2. User Flow Testing
3. Error Handling & Edge Cases
4. Data Integrity & CRUD
5. Access Control & Security

## Phase 3: Test Specification Generation

Spawn 5 specialist agents (one per test domain from research). Each generates TC-XXX formatted test cases.

### Specialist Agent Template

For each domain, spawn an agent with this structure:

```
Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate {domain} test cases",
  prompt: `You are a {domain} test specification specialist.

DISCOVERY CONTEXT:
{paste relevant discovery JSON}

RESEARCH CONTEXT:
{paste relevant research findings}

YOUR DOMAIN: {domain_name}

OBJECTIVE:
Generate comprehensive test cases for the {domain_name} domain following Hermes TC-XXX format.

OUTPUT FORMAT (Markdown):

## TC-{XXX}: [Test Name]

- **Area**: {domain_name}
- **Priority**: [Critical|High|Medium|Low]
- **Preconditions**:
  - [condition 1]
  - [condition 2]

### Test Steps
1. [action with selector/endpoint]
2. [verification step]
3. [assertion]

### Expected Outcome
[clear description of expected result]

### Pass Criteria
- [specific condition 1]
- [specific condition 2]

### Performance Threshold (if applicable)
- [metric]: [value]
- Timeout: [ms]

### Notes
- [any special considerations]

---

GENERATION RULES:
1. Each test must be independently executable
2. Use specific selectors/endpoints from discovery
3. Include negative tests (error cases)
4. Cover edge cases for this domain
5. Reference specific files/components from discovery

Generate 5-15 test cases for this domain. Return ONLY the markdown.`
)
```

### Domain-Specific Guidelines

**UI Component Testing:**
- Focus on visibility, interaction, responsiveness
- Test all component states (loading, error, success, empty)
- Include accessibility checks

**User Flow Testing:**
- Cover complete user journeys
- Test happy path + alternate paths
- Include flow interruptions and recovery

**Error Handling & Edge Cases:**
- Network failures
- Invalid inputs
- Boundary conditions
- Concurrent operations

**Data Integrity & CRUD:**
- Create, Read, Update, Delete operations
- Data validation
- Foreign key relationships
- Transaction rollback

**Access Control & Security:**
- Role-based access
- Unauthorized access attempts
- Session management
- CSRF/XSS considerations

## Phase 4: Document Assembly

After all 5 specialist agents complete:

1. Aggregate all TC-XXX outputs
2. Load the test-spec.md template
3. Replace placeholders:
   - `{PROJECT_NAME}` -> from discovery
   - `{DATE}` -> current date
   - `{FRAMEWORK}`, `{LANGUAGE}`, `{TEST_FRAMEWORK}` -> from discovery
4. Insert specialist outputs into `{SPECIALIST_OUTPUTS}` section
5. Generate traceability matrix from TC references
6. Save to `docs/test-specifications/{PROJECT_NAME}-test-spec.md`

## Phase 5: Hierarchical Verification

Following Anthropic's testing practices, implement two-layer verification.

### Doubt Agent Review

```
Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Review test spec for maintenance burden",
  prompt: `You are a doubt agent reviewing a generated test specification.

YOUR ROLE: Ruthlessly critique the test specification for:
1. Maintenance burden - will these tests break constantly?
2. Business logic validity - do tests actually verify real requirements?
3. Coverage gaps - what's missing?
4. Brittleness - what assumptions will fail?

TEST SPECIFICATION:
{paste full test spec}

OUTPUT FORMAT:

## Doubt Agent Review

### Critical Issues (must fix)
- [issue 1] with recommendation
- [issue 2] with recommendation

### Maintenance Risk Assessment
- **Risk Level**: [High|Medium|Low]
- **Projected Invalidation Rate**: [%] over 6 months
- **Mitigation Recommendations**: [list]

### Coverage Gaps
- [missing domain/feature]
- [missing edge case]

### Over-testing (remove to reduce burden)
- [redundant test]
- [too-specific test]

### Approval
[ ] APPROVED - Proceed to quick-clarify
[ ] REVISE - Address critical issues first`
)
```

### Finality Agent Verification (after user approval)

```
Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Final verification of test spec",
  prompt: `You are a finality agent. Verify the test specification is production-ready.

CHECKLIST:
- [ ] All TC-XXX tests have unique IDs
- [ ] Preconditions are complete and achievable
- [ ] Expected outcomes are unambiguous
- [ ] Pass criteria are objectively verifiable
- [ ] Performance thresholds include units
- [ ] Traceability matrix is complete
- [ ] Exit criteria are measurable
- [ ] Doubt agent issues addressed

FINAL DECISION:
[ ] VERIFIED - Ready for Trello conversion
[ ] INCOMPLETE - Specify remaining issues

Test Specification:
{paste test spec}`
)
```

## Phase 6: Quick-Clarify Iteration

After verification, present the test specification to the user for review.

### Invoke Quick-Clarify

```
Skill("quick-clarify")
```

With this context:
```
Test specification generated for {PROJECT}.
{TOTAL_TESTS} test cases across {DOMAIN_COUNT} domains.

Key areas:
- {DOMAIN_1}: {COUNT} tests
- {DOMAIN_2}: {COUNT} tests
- {DOMAIN_3}: {COUNT} tests
- {DOMAIN_4}: {COUNT} tests
- {DOMAIN_5}: {COUNT} tests

Document saved to: {SPEC_PATH}
```

### Iteration Loop

If user requests changes:

1. Identify which section/domain to modify
2. Re-run ONLY the affected specialist agent
3. Merge new output with existing document
4. Re-run doubt agent verification
5. Present updated version

Repeat until user satisfied.

### Loop Exit Conditions

User indicates satisfaction by:
- Explicit approval ("looks good", "approved")
- Choosing to proceed to Trello conversion
- No further modifications requested

## Phase 7: Trello Card Conversion (Optional)

After user approves the test specification:

### Ask User

```
Test specification approved. Convert to Trello cards?

Options:
- "Yes" -> Create Trello cards via /trello-test
- "No" -> Exit with test spec document only
- "Show mapping first" -> Preview card structure
```

### Card Mapping Strategy

Each TC-XXX test case becomes one Trello card with:

```
Card Name: "Test: TC-XXX - [Test Name]"
Description:
## TC-{XXX}: [Test Name]

**Area**: {domain}
**Priority**: [Critical|High|Medium|Low]

### Preconditions
- [list]

### Test Steps
1. [step]
2. [step]

### Expected Outcome
[outcome]

### Pass Criteria
- [criteria]

Checklist:
- [ ] Test implemented
- [ ] Test passes locally
- [ ] Test passes in CI
- [ ] Documentation updated
```

### Invoke Trello-Test Skill

```
Skill("trello-test")
```

Pass the parsed test cases for card creation.

### Board Structure

If new board needed:
- List: "Untested" - All new cards
- List: "In Progress" - Cards being implemented
- List: "Failed" - Cards with failing tests
- List: "Passed" - Cards with passing tests
- List: "Partial" - Cards with partial implementation

## Error Handling

### Agent Failures

If an explore agent fails:
1. Log the failure with agent ID and error
2. Continue with other agents
3. Use partial discovery data
4. Flag missing domains in output

If a specialist agent fails:
1. Log the failure
2. Create placeholder TC-XXX: "TODO: {domain} tests - generation failed"
3. Document the error
4. Continue with other domains

### Refusal Conditions

The skill MUST refuse to proceed if:

1. **No Runnable App Detected**
   - No framework config found
   - No source code detected
   - Output: "Cannot generate tests - no application detected"

2. **Auth Cannot Be Stabilized**
   - Multiple conflicting auth mechanisms
   - No clear auth pattern
   - Output: "Cannot generate tests - auth pattern unclear"

3. **Data Layer Inaccessible**
   - No database connection info
   - ORM models not discoverable
   - Output: "Cannot generate tests - data layer unclear"

4. **User Cancels**
   - At any phase, user may cancel
   - Save partial progress if requested

### Recovery

If generation is interrupted:
1. Save completed sections to temp file
2. Offer to resume or restart
3. Log interruption point

## Traceability Matrix Generation

After test case generation:

1. Parse all TC-XXX entries
2. Extract component/file references
3. Create requirement-to-test mapping
4. Generate traceability matrix
5. Include in test spec appendix

### Parse Template

```python
# Pseudo-code for traceability generation
traceability_rows = []
for test_case in test_cases:
    row = {
        "test_case": test_case.id,
        "requirement": test_case.requirement or "TBD",
        "component": test_case.component,
        "file": test_case.file,
        "line": test_case.line or "TBD",
        "status": "pending",
        "last_run": "-"
    }
    traceability_rows.append(row)
```

## User Experience

### Progress Reporting

Report progress at each phase completion:

```
✓ Discovery complete: 5 agents, X routes mapped
✓ Research complete: Best practices for {framework} identified
✓ Test domains determined: {domain1}, {domain2}, {domain3}, {domain4}, {domain5}
⏳ Generating tests: 2/5 specialist agents complete...
✓ Generation complete: {TOTAL} test cases generated
⏳ Verifying: Doubt agent review in progress...
✓ Verification complete: 0 critical issues
✓ Test spec saved to: {PATH}
```

### Silent Execution

- Don't narrate internal steps
- Don't announce "Starting Phase X"
- User sees ONLY progress checkpoints and final output
- All agent spawning happens silently

### Error Messages

Clear, actionable error messages:

```
❌ Discovery Failed: Agent 3 (Data & Backend) crashed
  Cause: [error from agent]
  Impact: Database-related tests may be incomplete
  Action: Continuing with partial discovery...
```

## Usage Examples

### Basic invocation
```
/test-spec-gen
```

### With filter
```
/test-spec-gen --filter "auth"
```

### Specific domains
```
/test-spec-gen --domains "ui,flows,errors"
```

### Skip Trello prompt
```
/test-spec-gen --no-trello
```
