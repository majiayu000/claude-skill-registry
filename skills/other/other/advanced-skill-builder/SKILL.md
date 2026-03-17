---
name: advanced-skill-builder
description: Guides users through creating production-ready Claude skills via interactive dialogue. Use when user wants to build a new skill, needs help structuring a skill, or asks "how do I create a skill?" Covers requirements gathering, planning, YAML frontmatter generation, instruction writing, testing, and iterative refinement. Works with or without MCP integration.
license: MIT
metadata:
  author: John-Dekka
  version: 1.0.0
  category: productivity
  tags: [skill-development, automation, workflow, template]
---

# Advanced Skill Builder

An interactive guide for creating production-ready Claude skills through collaborative dialogue.

## When to Use This Skill

Activate this skill when:
- User says: "Help me build a skill", "Create a new skill", or "I need a skill for..."
- User describes a workflow they want to automate but doesn't know how to structure it
- User wants to teach Claude a specific process or methodology
- User asks: "How do I create a skill?" or "Can you help me make a skill?"
- User has an MCP server and wants to add workflow guidance

---

## Dialogue Flow Overview

This skill operates through **structured dialogue** to gather requirements, then generates a complete skill folder. The flow:

```
Phase 1: Discovery → Phase 2: Planning → Phase 3: Structure → Phase 4: Generation → Phase 5: Validation
```

**Estimated time:** 15-30 minutes for a complete skill
**Outcome:** Ready-to-use skill folder with SKILL.md, scripts/, references/, and assets/

---

## Phase 1: Discovery Questions

Before generating anything, gather context through dialogue. Ask questions in sequence.

### Essential Discovery Questions

**Q1: Core Purpose**
> "What specific task or workflow do you want this skill to handle?"
>
> Listen for: The domain, the outcome, the user's pain point

**Q2: Target Users**
> "Who will use this skill—yourself, your team, or external users?"
>
> Listen for: Complexity level needed, documentation depth, sharing intent

**Q3: Existing Tools**
> "What tools, APIs, or services does this skill need to access? (Or none?)"
>
> Listen for: MCP requirements, built-in tools only, custom scripts

**Q4: Success Definition**
> "How will you know the skill is working? What does a successful outcome look like?"
>
> Listen for: Measurable outputs, qualitative markers, edge cases

**Q5: Complexity Estimate**
> "Roughly how many steps is this workflow? (Simple: 1-3, Moderate: 4-7, Complex: 8+)"
>
> Listen for: Structure needed, validation requirements, error handling scope

---

## Phase 2: Planning

Based on discovery answers, recommend a skill category and structure.

### Skill Category Selection

| Category | Indicators | Recommended Structure |
|----------|------------|---------------------|
| **Document & Asset Creation** | User wants to generate consistent output (docs, designs, code, presentations) | Templates + quality checklists + style guides |
| **Workflow Automation** | Multi-step process, specific sequence, validation needed | Step-by-step with gates + error handling + rollback |
| **MCP Enhancement** | Has MCP server, needs workflow guidance | Tool orchestration + domain expertise + error patterns |

### Use Case Template

After discovery, create this structured document:

```markdown
## Skill Use Case Definition

**Skill Name:** [auto-generate from purpose]

**Category:** [Document Creation / Workflow Automation / MCP Enhancement]

**Trigger Phrases:**
- "[phrase 1]"
- "[phrase 2]"
- "[phrase 3]"

**Workflow Steps:**
1. [Step with purpose and tool call]
2. [Step with purpose and tool call]
3. [...]

**Success Criteria:**
- [Criterion 1]
- [Criterion 2]

**Known Edge Cases:**
- [Edge case 1] → [Resolution]
- [Edge case 2] → [Resolution]
```

**Confirm with user:** "Does this capture what you need? What should I adjust?"

---

## Phase 3: Skill Structure Generation

Generate the folder structure based on category.

### Document & Asset Creation Structure

```
{skill-name}/
├── SKILL.md
├── assets/
│   ├── template-1.md
│   └── template-2.md
└── references/
    └── style-guide.md
```

### Workflow Automation Structure

```
{skill-name}/
├── SKILL.md
├── scripts/
│   ├── validate.sh
│   └── process.py
└── references/
    └── error-codes.md
```

### MCP Enhancement Structure

```
{skill-name}/
├── SKILL.md
├── scripts/
│   ├── mcp-validator.py
│   └── error-mapper.py
└── references/
    ├── tool-docs.md
    └── workflow-patterns.md
```

---

## Phase 4: YAML Frontmatter Generation

Generate proper frontmatter with progressive disclosure.

### Template

```yaml
---
name: {skill-name-in-kebab-case}
description: {clear-description} Use when user says "{trigger-1}", "{trigger-2}", or "{trigger-3}".
license: {MIT/Apache-2.0/None}
metadata:
  author: {author-name}
  version: 1.0.0
  {mcp-server: {server-name}}  # Only if MCP-enhanced
---
```

### Description Best Practices

**Structure:** `[What it does] + [When to use it] + [Key triggers]`

| ✅ Good Example | ❌ Bad Example |
|----------------|----------------|
| "Creates API documentation from code comments. Use when user says 'document this API', 'generate docs', or uploads a code file." | "Helps with documentation." |

### Validation Checklist

Before finalizing frontmatter:
- [ ] Name is kebab-case (no spaces, no capitals)
- [ ] Description under 1024 characters
- [ ] Description includes WHAT and WHEN
- [ ] No XML tags (`<` or `>`)
- [ ] Triggers are natural phrases users would actually say
- [ ] Version follows semantic versioning (1.0.0)

---

## Phase 5: SKILL.md Body Generation

Generate instructions following the recommended structure.

### Template Structure

```markdown
---
name: skill-name
description: Description here.
---

# Skill Name

## Overview

Brief description of what this skill does and when to use it.

## Instructions

### Step 1: [First Major Step]

[Clear instructions with examples]

### Step 2: [Second Major Step]

[Clear instructions with examples]

[...additional steps...]

## Examples

### Example 1: [Common Scenario]

**User says:** "[phrase]"

**Actions:**
1. [Action]
2. [Action]

**Result:** [Expected outcome]

### Example 2: [Another Scenario]

[...]

## Troubleshooting

**Error:** [Common error]
**Cause:** [Why it happens]
**Solution:** [How to fix]

[...]

## Best Practices

- [Tip 1]
- [Tip 2]
```

### Writing Guidelines

**For Each Step:**
1. Start with clear purpose
2. Provide concrete example (bash command, MCP call, etc.)
3. Describe expected output
4. Include error handling

**For Examples:**
- Use realistic user phrases
- Show full workflow
- Describe concrete result

**For Troubleshooting:**
- Start with most common errors
- Include both cause and solution

---

## Dialogue-Guided Skill Creation Example

### Step-by-Step Walkthrough

**Assistant:** "Let's build your skill. First, tell me—what task or workflow do you want to automate?"

**User:** [Responds with their goal]

**Assistant:** "Got it. A few more questions to understand the scope..."

[Continue discovery questions from Phase 1]

**Assistant:** "Based on what you've described, this sounds like a **[category]** skill. Here's what I'm thinking:"

[Present use case template]

**User:** [Confirms or adjusts]

**Assistant:** "Great. I'll create the skill folder structure now. What name would you like for this skill? (kebab-case, no spaces)"

**User:** [Provides name]

**Assistant:** "Generating your skill with this structure:"

[Present folder structure]

**Assistant:** "I'm writing the SKILL.md file with proper YAML frontmatter and instructions. Meanwhile, let me ask—what trigger phrases should activate this skill? What would a user say to invoke it?"

**User:** [Provides phrases]

**Assistant:** "Perfect. I'm now creating:"
- [ ] SKILL.md with frontmatter and instructions
- [ ] scripts/ folder with validation utilities
- [ ] references/ folder for additional documentation

[Generate files]

**Assistant:** "Your skill is ready. Let me verify it works:"

[Run validation checks]

**Assistant:** "✅ SKILL.md created with valid YAML frontmatter
✅ Folder structure follows best practices
✅ Description includes triggers and use cases

**Next steps to test:**
1. Download and upload to Claude.ai via Settings > Capabilities > Skills
2. Try: \"[trigger phrase]\"
3. Monitor for: Does it trigger correctly? Does it complete the workflow?

Want me to iterate on any part—perhaps refine the instructions, add more examples, or adjust the triggers?"

---

## Advanced Features

### Multi-MCP Orchestration Pattern

For skills coordinating multiple services:

```markdown
## MCP Coordination

### Phase 1: [First Service]
1. Fetch data via `[service-a]-mcp-tool`
2. Validate response

### Phase 2: [Second Service]
1. Transform data for `[service-b]-mcp-tool`
2. Submit request

### Phase 3: [Third Service]
1. Process response
2. Generate output

### Error Handling
- If Phase 1 fails: [Recovery action]
- If Phase 2 fails: [Recovery action + Phase 1 cleanup]
```

### Iterative Refinement Pattern

For skills where quality improves with iteration:

```markdown
## Quality Assurance Loop

### 1. Initial Generation
Create first version of output

### 2. Validation Check
Run `scripts/validate-output.py`
- Check: [Criteria]
- Check: [Criteria]

### 3. Refinement
If validation fails:
  - Address specific issues
  - Re-run validation
  - Repeat until pass

### 4. Final Output
Only after validation passes
```

### Context-Aware Selection Pattern

For skills choosing tools dynamically:

```markdown
## Tool Selection Logic

1. Analyze input type and requirements
2. Select best tool:
   - `[tool-a]`: When [condition 1]
   - `[tool-b]`: When [condition 2]
   - `[tool-c]`: When [condition 3]
3. Execute with selected tool
4. Explain choice to user
```

---

## Testing Protocol

After generating a skill, guide the user through validation:

### Trigger Testing

**Should trigger on:**
- "[Primary trigger phrase]"
- "[Alternate phrasing]"
- "[Paraphrased request]"

**Should NOT trigger on:**
- "[Unrelated topic]"
- "[Different domain]"

### Functional Testing

1. "Try this skill with: \"[example request]\""
2. Observe: Does it follow the workflow?
3. Verify: Are steps in correct order?
4. Check: Are tool calls correct?

### Iteration Loop

If issues found:
1. Identify specific failure point
2. Adjust instructions for that step
3. Re-test with same example
4. Expand test cases

---

## Error Handling for the Skill Builder

When the skill-builder encounters issues:

| Error | Response |
|-------|----------|
| Unclear user requirements | "I want to make sure I understand correctly. Can you tell me more about [specific aspect]?" |
| Contradictory requirements | "You mentioned both [A] and [B], which seem conflicting. How should I prioritize?" |
| Missing tool information | "You mentioned needing [tool], but I don't have access to it. Is this an MCP server you have connected, or should I use built-in capabilities?" |
| Scope too large | "This is a substantial workflow! Would you like to start with a Minimum Viable Skill covering [core steps], then add complexity later?" |
| Vague success criteria | "How will you know the skill succeeded? What does the ideal output look like? Can you give me a concrete example?" |

---

## Best Practices Summary

### Do

- ✅ Ask clarifying questions before generating
- ✅ Use progressive disclosure (frontmatter → body → references)
- ✅ Include specific trigger phrases users would actually say
- ✅ Provide concrete examples with expected outputs
- ✅ Add error handling for common failure modes
- ✅ Validate YAML syntax before finalizing
- ✅ Test with real user requests
- ✅ Iterate based on feedback

### Don't

- ❌ Generate without understanding the use case
- ❌ Use vague descriptions like "helps with tasks"
- ❌ Skip the trigger phrases (critical for activation)
- ❌ Make instructions too long—use references/
- ❌ Forget to handle errors
- ❌ Create skills without user confirmation
- ❌ Skip testing before deployment

---

## Output Artifacts

This skill generates:

1. **Skill Folder** - Complete structure with all directories
2. **SKILL.md** - With YAML frontmatter and Markdown instructions
3. **scripts/** - Utility scripts for validation/processing
4. **references/** - Additional documentation for progressive disclosure
5. **assets/** - Templates and style guides (if needed)
6. **Testing Guide** - Recommended test cases
7. **Installation Instructions** - For the user

---

## Example: Complete Skill Generation

**User:** "I want a skill that helps me write release notes from Git commits."

**Assistant:** "Great! Let me understand your needs better."

**Discovery Q1:** "What format do you want for release notes? (bullet points, sections by type, detailed changelog)"

**User:** "Bullet points grouped by type: Features, Bug Fixes, Improvements."

**Discovery Q2:** "How will you provide the commits? Pulling from GitHub MCP, uploading a file, or pasting them?"

**User:** "GitHub MCP—my team has it connected."

**Assistant:** "Perfect. This is a **MCP Enhancement** skill. Here's what I'm planning:"

```
release-notes-generator/
├── SKILL.md
├── scripts/
│   └── categorize-commits.py
└── references/
    └── commit-patterns.md
```

**Assistant:** "Triggers would include: 'write release notes', 'generate changelog', 'summarize commits'. Does this fit?"

**User:** "Yes, and add 'create release notes' as a trigger."

**Assistant:** "Generating your skill..."

[Creates files]

**Assistant:** "✅ Your skill is ready! Test with: 'Write release notes for PR #123'

Want me to add anything—perhaps support for custom category names or emoji formatting?"

---

## Troubleshooting

**Issue:** User provides vague requirements
**Solution:** Use the discovery questions systematically. Don't proceed until you have clear answers.

**Issue:** Scope creep—user keeps adding features
**Solution:** "Let's build a version 1.0 with core functionality first, then we can add [feature] in a future iteration. Sound good?"

**Issue:** User doesn't know trigger phrases
**Solution:** Suggest 3-5 based on their use case, then ask: "Would you use any of these phrases? What would YOU say?"

**Issue:** Skill generates but won't activate
**Solution:** Check:
1. Description includes specific trigger phrases
2. No XML tags in frontmatter
3. Name is kebab-case
4. SKILL.md is exact filename

---

## Metadata for Version Tracking

```yaml
metadata:
  author: AI Assistant (generated)
  version: 1.0.0
  created: auto-timestamp
  last-updated: auto-timestamp
  category: document-creation  # or workflow-automation / mcp-enhancement
  complexity: low  # low / medium / high
  estimated-minutes: 15-30
```

---

## Quick Reference for Agent

When using this skill to build another skill:

1. **Ask** the 5 discovery questions first
2. **Recommend** category based on answers
3. **Present** use case template for confirmation
4. **Generate** folder structure
5. **Write** YAML frontmatter (name + description + triggers)
6. **Write** SKILL.md body (instructions + examples + troubleshooting)
7. **Create** supporting files (scripts/, references/, assets/)
8. **Validate** all files exist and are properly formatted
9. **Guide** user through testing
10. **Offer** iteration based on feedback

**Remember:** Progressive disclosure is key. Frontmatter should be brief—keep detailed docs in references/
