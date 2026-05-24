---
name: meta-methodology-improvement-protocol
description: Self-improvement protocol for agents modifying their own prompts/configurations. Evidence-based improvements, structured changes, proven patterns from research.
---

# Self-Improvement Protocol

> **Quick Guide:** When improving your own prompt/configuration, use evidence-based improvements with proven patterns. Suggest changes with clear rationale, let user approve before applying.

---

<critical_requirements>

## CRITICAL: Evidence-Based Improvements Only

**(All improvements must use established prompt engineering patterns)**

**(Base changes on empirical results, not speculation)**

**(Provide clear rationale and source for each improvement)**

**(Suggest changes with before/after - let user approve before applying)**

</critical_requirements>

---

<improvement_protocol>

When a task involves improving your own prompt/configuration:

### Recognition

**You're in self-improvement mode when:**

- Task mentions "improve your prompt" or "update your configuration"
- You're asked to review your own instruction file
- Task references `.claude/agents/[your-name].md`
- "based on this work, you should add..."
- "review your own instructions"

### Process

```xml
<self_improvement_workflow>
1. **Read Current Configuration**
   - Load `.claude/agents/[your-name].md`
   - Understand your current instructions completely
   - Identify areas for improvement

2. **Apply Evidence-Based Improvements**
   - Use proven patterns from successful systems
   - Reference specific PRs, issues, or implementations
   - Base changes on empirical results, not speculation

3. **Structure Changes**
   Follow these improvement patterns:

   **For Better Instruction Following:**
   - Add emphatic repetition for critical rules
   - Use XML tags for semantic boundaries
   - Place most important content at start and end
   - Add self-reminder loops (repeat key principles)

   **For Reducing Over-Engineering:**
   - Add explicit anti-patterns section
   - Emphasize "use existing utilities"
   - Include complexity check decision framework
   - Provide concrete "when NOT to" examples

   **For Better Investigation:**
   - Require explicit file listing before work
   - Add "what good investigation looks like" examples
   - Mandate pattern file reading before implementation
   - Include hallucination prevention reminders

   **For Clearer Output:**
   - Use XML structure for response format
   - Provide template with all required sections
   - Show good vs. bad examples
   - Make verification checklists explicit

4. **Document Changes**
   ## Improvement Applied: [Brief Title]

   **Date:** [YYYY-MM-DD]

   **Problem:**
   [What wasn't working well]

   **Solution:**
   [What you changed and why]

   **Source:**
   [Reference to PR, issue, or implementation that inspired this]

   **Expected Impact:**
   [How this should improve performance]

5. **Suggest, Don't Apply**
   - Propose changes with clear rationale
   - Show before/after sections
   - Explain expected benefits
   - Let the user approve before applying
</self_improvement_workflow>
```

</improvement_protocol>

---

<improvement_categories>

## Improvement Categories

Every improvement must fit into one of these categories:

- **Investigation Enhancement**: Add specific files/patterns to check
- **Constraint Addition**: Add explicit "do not do X" rules
- **Pattern Reference**: Add concrete example from codebase
- **Workflow Step**: Add/modify a step in the process
- **Anti-Pattern**: Add something to actively avoid
- **Tool Usage**: Clarify how to use a specific tool
- **Success Criteria**: Add verification step

</improvement_categories>

---

<proven_patterns>

## Proven Patterns

All improvements must use established prompt engineering patterns:

**Pattern 1: Specific File References**

- Bad: "Check the auth patterns"
- Good: "Examine UserStore.ts lines 45-89 for the async flow pattern"

**Pattern 2: Concrete Examples**

- Bad: "Use MobX properly"
- Good: "Use `flow` from MobX for async actions (see UserStore.fetchUser())"

**Pattern 3: Explicit Constraints**

- Bad: "Don't over-engineer"
- Good: "Do not create new HTTP clients - use apiClient from lib/api-client.ts"

**Pattern 4: Verification Steps**

- Bad: "Make sure it works"
- Good: "Run `npm test` and verify UserStore.test.ts passes"

**Pattern 5: Emphatic for Critical Rules**

Use **bold** or CAPITALS for rules that are frequently violated:
"**NEVER modify files in /auth directory without explicit approval**"

</proven_patterns>

---

<output_format>

## Output Format

When suggesting improvements, provide:

```xml
<analysis>
Category: [Investigation Enhancement / Constraint Addition / etc.]
Section: [Which file/section this goes in]
Rationale: [Why this improvement is needed]
Source: [What triggered this - specific implementation, bug, etc.]
</analysis>

<current_content>
[Show the current content that needs improvement]
</current_content>

<proposed_change>
[Show the exact new content to add, following all formatting rules]
</proposed_change>

<integration_notes>
[Explain where/how this fits with existing content]
</integration_notes>
```

</output_format>

---

<red_flags>

## Red Flags

**Don't add improvements that:**

- Make instructions longer without clear benefit
- Introduce vague or ambiguous language
- Add complexity without evidence it helps
- Conflict with proven best practices
- Remove important existing content

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**(All improvements must use established prompt engineering patterns)**

**(Base changes on empirical results, not speculation)**

**(Suggest changes - let user approve before applying)**

**(Show before/after with clear rationale)**

**(Every improvement must fit into a defined category)**

</critical_reminders>
