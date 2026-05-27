---
name: deviation-rules
description: "Handle unexpected work during execution. Use when encountering bugs, missing features, blockers, or architectural changes while executing a plan. Not for initial planning or non-execution contexts."
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# Deviation Rules Engine

<mission_control>
<objective>Handle unexpected work during execution with mechanistic decision trees</objective>
<success_criteria>Deviations handled according to logic trees with full transparency</success_criteria>
</mission_control>

Automatic handling of discovered work during plan execution with clear rules and full transparency.

## What This Skill Does

Apply deviation rules when encountering unexpected work during plan execution:

1. **Auto-fix bugs** - Fix bugs discovered during implementation
2. **Add missing critical** - Add critical functionality that was overlooked
3. **Fix blockers** - Resolve blocking issues preventing completion
4. **Ask about architectural changes** - Stop and ask for major structural changes
5. **Log enhancements** - Log non-critical improvements for later

**Key Innovation**: Handle real-world complexity automatically while maintaining full transparency.

## Logic Trees: Mechanistic Decision Making

<deviation_logic>
<trigger condition="bug">
<test>

- Is this a logic error, syntax error, type error, security vulnerability, or performance issue?
- Is the fix unambiguous (clear solution exists)?
- Does the fix not change architecture?
  </test>
  <action>Auto-fix without asking</action>
  <examples>
- MD5 password hashing → Fix to bcrypt (security)
- Missing semicolon → Add semicolon (syntax)
- Unhandled exception → Add try/catch (logic)
  </examples>
  </trigger>

<trigger condition="missing_critical">
<test>
- Is this essential for functionality that was clearly overlooked?
- Would not adding it make the implementation non-functional?
- Is the solution straightforward and unambiguous?
</test>
<action>Add without asking</action>
<examples>
- No error handling for database → Add error middleware
- Missing input validation → Add validation
- No logging for debugging → Add logs
</examples>
</trigger>

<trigger condition="blocker">
<test>
- Does this block progress on planned work?
- Is resolution necessary to continue?
- Does solution not require architectural decision?
</test>
<action>Fix without asking</action>
<examples>
- Missing dependency → Install dependency
- Wrong environment variable → Set variable
- File permission issue → Fix permissions
</examples>
</trigger>

<trigger condition="architecture_change">
<test>
- Does this change file/folder structure?
- Does this add/remove major components?
- Does this change data models or schemas?
- Does this affect system architecture?
</test>
<action>STOP and ask user</action>
<examples>
- Need to add new service layer
- Database schema change required
- File restructure needed
</examples>
</trigger>

<trigger condition="enhancement">
<test>
- Is this a nice-to-have improvement?
- Would this be better logged for later?
- Is this not essential for current task?
</test>
<action>Log for later, continue</action>
<examples>
- Code refactoring opportunity
- Performance optimization
- Documentation improvement
</examples>
</trigger>
</deviation_logic>

## Decision Flow

<decision_flow>
When encountering unexpected work:

1. **Classify**: What type of deviation is this?
   - Bug? → Trigger: bug
   - Missing critical? → Trigger: missing_critical
   - Blocker? → Trigger: blocker
   - Architecture change? → Trigger: architecture_change
   - Enhancement? → Trigger: enhancement

2. **Apply trigger rules**:
   - If bug: Auto-fix
   - If missing_critical: Add
   - If blocker: Fix
   - If architecture_change: STOP and ask
   - If enhancement: Log and continue

3. **Report action**: Always explain what you did and why
   </decision_flow>

---

- Modifying system boundaries
- Changing patterns or frameworks
- Altering deployment architecture

**When to apply**:

- Change affects system structure
- Change has multiple valid approaches
- Change would require updating other components
- Change conflicts with existing patterns

**Example**:

```
Plan: "Add user preferences"
Discovery: Current data model doesn't support user-specific settings
Action: STOP and ask user about data model approach
Reason: Architectural decision, multiple valid options
```

**Recognition**: "Does this change the system structure or have multiple valid approaches?"

### Rule 5: Log Enhancements

**Definition**: Log non-critical improvements for later consideration.

**What counts as enhancements**:

- Code refactoring for clarity
- Adding convenience features
- Performance optimizations (non-critical)
- Documentation improvements
- Test coverage expansions

**When to apply**:

- Improvement is valuable but not essential
- Enhancement doesn't block current work
- Can be deferred without impact

**Example**:

```
Plan: "Add payment processing"
Discovery: Error messages could be more user-friendly
Action: Log to SUMMARY.md as enhancement
Reason: Nice to have, not essential for completion
```

**Recognition**: "Is this valuable but not essential for current task?"

## SUMMARY.md Documentation

All deviations are documented in `SUMMARY.md`:

```markdown
# Execution Summary

## Original Plan

[Original plan description]

## Deviations Log

### Auto-Fixed Bugs

- [Bug description] → [Fix applied]
- [Bug description] → [Fix applied]

### Added Missing Critical

- [Missing functionality] → [What was added]

### Fixed Blockers

- [Blocker] → [Resolution]

### Logged Enhancements

- [Enhancement idea] (deferred)
- [Enhancement idea] (deferred)

## Architectural Decisions

[Only if Rule 4 was triggered]

- [Decision point] → [User's decision]
```

**Recognition**: "Is every deviation documented for transparency?"

## Application Workflow

### During Execution

When encountering unexpected work:

<router>
flowchart TD
    Start([Unexpected Work]) --> Type{Classify Type}
    Type -- Bug --> Rule1[Rule 1: Auto-Fix]
    Type -- Missing Critical --> Rule2[Rule 2: Add Critical]
    Type -- Blocker --> Rule3[Rule 3: Fix Blocker]
    Type -- Architectural --> Rule4[Rule 4: Ask User]
    Type -- Enhancement --> Rule5[Rule 5: Log It]
    
    Rule1 --> Doc[Document in SUMMARY.md]
    Rule2 --> Doc
    Rule3 --> Doc
    Rule4 --> Wait[Wait for Decision]
    Rule5 --> Doc
    
    Doc --> Continue[Continue Execution]
    Wait --> Continue
</router>

1. **Classify the deviation type**

2. **Apply the appropriate rule**
   - Execute the rule's action
   - Document in SUMMARY.md
   - Continue execution (or wait for user if Rule 4)

3. **Continue with plan**
   - Return to planned work
   - Update task status if needed

### Example Execution

```
Original Plan: Add JWT authentication to API

During Implementation:
1. Discovery: Password hashing uses MD5
   → Rule 1 (Bug): Fix to bcrypt
   → Document: Fixed insecure MD5 hashing

2. Discovery: No error handling for database failures
   → Rule 2 (Missing Critical): Add error handling
   → Document: Added error handling for database operations

3. Discovery: User model doesn't have email field
   → Rule 4 (Architectural): STOP and ask user
   → Wait for user decision on data model

4. Discovery: Token expiration check could be more efficient
   → Rule 5 (Enhancement): Log for later
   → Document: Deferred: Optimize token validation

Result: Authentication complete with documented deviations
```

## Recognition Questions

Before applying any rule, ask:

**Rule 1 (Bugs)**:

- "Is this a bug with a clear, unambiguous fix?"
- "Does the fix preserve the intended architecture?"

**Rule 2 (Missing Critical)**:

- "Is this essential for functionality?"
- "Was this clearly overlooked, not a new feature?"
- "Is the implementation straightforward?"

**Rule 3 (Blockers)**:

- "Does this block progress?"
- "Is there an unambiguous resolution?"

**Rule 4 (Architectural)**:

- "Does this change system structure?"
- "Are there multiple valid approaches?"
- "Would other components be affected?"

**Rule 5 (Enhancements)**:

- "Is this valuable but not essential?"
- "Can this be deferred without impact?"

## Best Practices

### Transparency

- Document EVERY deviation in SUMMARY.md
- Explain WHY each deviation was necessary
- Note what was done vs what was planned

### Judgement

- Be conservative with Rule 4 (when in doubt, ask)
- Be generous with Rule 2 (err on side of completeness)
- Be honest with Rule 5 (log real improvements, don't ignore)

### Context

- Consider project size and complexity
- Consider team practices and standards
- Consider long-term maintenance impact

## Common Mistakes

**❌ Wrong**: Treating every unexpected item as architectural (Rule 4)
**✅ Correct**: Only Rule 4 for structural changes with multiple valid approaches

**❌ Wrong**: Ignoring enhancements because they're not in the plan
**✅ Correct**: Log enhancements (Rule 5) for future consideration

**❌ Wrong**: Not documenting deviations
**✅ Correct**: Always document to SUMMARY.md for transparency

**❌ Wrong**: Making architectural assumptions without asking
**✅ Correct**: Rule 4 triggers user consultation for architecture decisions

## Integration with Planning

## Related Skills

This skill integrates with:

- `engineering-lifecycle` - Test-driven development with deviation handling
- `invocable-development` - Component creation with automatic fixes
- `/orchestrate` - Native orchestration with deviation rules

## Arguments

This skill is loaded automatically during plan execution. No direct invocation needed.

**Manual invocation** (for reference/testing):

```
Skill: deviation-rules
Args: [deviation description] [rule to apply]
```

## Example Use Cases

### Use Case 1: API Development

```
Plan: "Add user profile endpoint"
Deviation 1: No input validation → Rule 2 (add validation)
Deviation 2: Database query vulnerable to SQL injection → Rule 1 (fix bug)
Deviation 3: Response format inconsistent → Rule 4 (ask about standard)
```

### Use Case 2: Frontend Component

```
Plan: "Create dashboard widget"
Deviation 1: Missing loading state → Rule 2 (add critical)
Deviation 2: Could use animations → Rule 5 (log enhancement)
Deviation 3: Color system doesn't support theme → Rule 4 (ask about theming)
```

### Use Case 3: Infrastructure

```
Plan: "Set up CI/CD pipeline"
Deviation 1: Docker build fails → Rule 3 (fix blocker)
Deviation 2: No test coverage reporting → Rule 2 (add critical)
Deviation 3: Could add deployment previews → Rule 5 (log enhancement)
```

**Trust intelligence** - Deviation rules enable automatic handling of real-world complexity while maintaining transparency and architectural integrity.

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

<critical_constraint>
**MANDATORY: Use `<trigger>` logic trees for decisions**

- Classify deviation type using trigger conditions
- Apply mechanistic rules based on trigger
- Never make interpretive decisions
- Follow decision flow exactly

**MANDATORY: Document every deviation**

- Auto-fixes: Log bug and fix applied
- Additions: Log what was added and why
- Architectural: Document user decision
- Enhancements: Log for later consideration

**MANDATORY: Be conservative with architectural triggers**

- Only use Rule 4 for structural changes
- Multiple valid approaches = ask user
- When in doubt, ask rather than assume
- Never change architecture without explicit approval

**MANDATORY: Be generous with missing critical**

- Err on side of completeness
- Add what's clearly overlooked
- Don't ask for obvious essentials
- Implementation must be functional

**MANDATORY: Stop and ask for architectural changes**

- File/folder structure changes
- Major component additions/removals
- Data model or schema changes
- Pattern or framework changes

**No exceptions. Logic trees make decisions mechanistic, not interpretive.**
</critical_constraint>
