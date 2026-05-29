---
name: specsafe-spec
description: Generate detailed specification from PRD. Fleshes out requirements and scenarios.
disable-model-invocation: true
---

Flesh out a detailed specification from the initial PRD (SPEC stage refinement).

**When to use:**
- PRD is drafted but needs detailed requirements
- Need to define acceptance criteria and scenarios
- Preparing to move to TEST stage

**Input**: The spec ID (e.g., SPEC-20260211-001)

**Steps**

1. **Read the spec file**

   Load `specs/active/<spec-id>.md` and review:
   - Current Purpose and Scope sections
   - Existing requirements (if any)
   - Tech stack decisions
   - Current stage (must be SPEC)

2. **Expand requirements**

   For each requirement in the PRD:
   - Assign unique requirement ID (e.g., FR-1, NFR-1)
   - Define clear acceptance criteria in Given-When-Then format
   - Specify priority (P0/P1/P2)
   - Add any dependencies or constraints

3. **Define scenarios**

   Create detailed scenarios covering:
   - **Happy path**: Normal operation
   - **Edge cases**: Boundary conditions
   - **Error cases**: Invalid inputs, failures
   - **Integration**: Interaction with other systems

   Format each scenario:
   ```
   ## Scenario: [Name]
   **Given** [precondition]
   **When** [action]
   **Then** [expected result]
   ```

4. **Technical approach**

   Expand the Technical Approach section:
   - Architecture decisions
   - API contracts (if applicable)
   - Data models
   - Integration points

5. **Test strategy**

   Define testing approach:
   - Unit test coverage targets
   - Integration test requirements
   - E2E scenarios to cover
   - Mock/stub requirements

6. **Implementation plan**

   Create phased implementation plan:
   | Phase | Task | Est. | Dependencies |
   |-------|------|------|--------------|
   | 1 | Setup | 30m | None |
   | 2 | Core logic | 2h | Phase 1 |

7. **Update status**

   Mark spec as ready for TEST stage if complete:
   ```bash
   specsafe spec "<spec-id>"
   ```

8. **Show summary**

   Display:
   - Requirements count by priority
   - Scenarios defined
   - Estimated total effort
   - Next command: `/specsafe:test <id>`

**Output**

After specification:
- ✅ Detailed requirements with acceptance criteria
- ✅ Comprehensive scenarios (happy path + edge cases)
- ✅ Technical approach documented
- ✅ Test strategy defined
- ✅ Implementation plan with estimates
- 📋 Status: SPEC (ready for TEST stage)
- 📋 Prompt: "Ready to generate tests? Run `/specsafe:test <id>`"

**Guardrails**
- Requirements must have clear acceptance criteria
- Scenarios should cover at least: happy path, 2 edge cases, 1 error case
- Estimates should be realistic (use T-shirt sizes or hours)
- Do NOT proceed to TEST stage until requirements are complete
- Review with user if spec is large (>10 requirements) before proceeding

**Example**
```
User: /specsafe:spec SPEC-20260211-004
→ Expands PRD into detailed spec
→ Adds 8 requirements (3 P0, 3 P1, 2 P2)
→ Defines 6 scenarios
→ Status: SPEC
→ Next: /specsafe:test SPEC-20260211-004
```