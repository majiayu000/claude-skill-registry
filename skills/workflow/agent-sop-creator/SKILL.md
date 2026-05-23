---
name: agent-sop-creator
description: Guide for creating Agent SOPs (Standard Operating Procedures). Use this skill when the user wants to create a new SOP workflow for AI agents, write an agent procedure, or needs help with SOP format and best practices. Triggers on requests like "create an SOP", "new agent workflow", "help me write an SOP", "create a procedure for agents", or "SOP template".
---

# Agent SOP Creator

Create Agent SOPs - markdown workflows that guide AI agents through complex tasks with parameterized inputs and constraint-based execution.

## SOP Template

```markdown
# [SOP Name]

## Overview

[1-2 sentences: what this SOP does and when to use it]

## Parameters

- **required_param** (required): Description of required input
- **optional_param** (optional, default: "value"): Description with default

**Constraints for parameter acquisition:**
- You MUST ask for all parameters upfront in a single prompt
- You MUST confirm successful acquisition before proceeding

## Steps

### 1. [Step Name]

[Natural language description of what happens]

**Constraints:**
- You MUST [absolute requirement]
- You SHOULD [recommended action]
- You MAY [optional action]
- You MUST NOT [prohibition] because [reason why]

### 2. [Next Step Name]

[Description]

**Constraints:**
- [List constraints using RFC 2119 keywords]

## Examples

### Example Input
[Show realistic input]

### Example Output
[Show expected result]

## Troubleshooting

### [Common Issue]
If [condition], you should [resolution].
```

## Writing Steps

### Step 1: Define Overview

Start with a clear 1-2 sentence explanation of what the SOP accomplishes and when to use it.

### Step 2: Define Parameters

List all inputs the workflow needs:
- Use snake_case for parameter names
- List required parameters before optional ones
- Include defaults for optional parameters
- Add parameter acquisition constraints if multiple input methods supported

### Step 3: Write Steps

For each step:
1. Give it a numbered name (### 1. Step Name)
2. Write natural language description
3. Add **Constraints:** section with RFC 2119 keywords

### Step 4: Add Examples and Troubleshooting

Include concrete examples showing input/output pairs and common issues with resolutions.

## RFC 2119 Keywords

| Keyword | Meaning | Use When |
|---------|---------|----------|
| MUST | Absolute requirement | Action is critical for success |
| MUST NOT | Absolute prohibition | Action would cause failure |
| SHOULD | Recommended | Best practice but exceptions exist |
| SHOULD NOT | Not recommended | Generally avoid but sometimes acceptable |
| MAY | Optional | Truly optional enhancement |

## Writing Constraints

Negative constraints MUST include reasons:

Good:
```markdown
- You MUST NOT push changes because this could publish unreviewed code
- You MUST NOT delete history because this corrupts the repository
```

Bad:
```markdown
- You MUST NOT push changes
- You MUST NOT delete history
```

## Checklist

Before finalizing an SOP, verify:

- [ ] File uses `.sop.md` extension
- [ ] Overview clearly explains purpose and when to use
- [ ] Parameters use snake_case naming
- [ ] Required parameters listed before optional
- [ ] Steps are numbered sequentially
- [ ] Each step has a **Constraints:** section
- [ ] All constraints use RFC 2119 keywords
- [ ] All negative constraints include "because [reason]"
- [ ] Examples show realistic input/output
- [ ] Troubleshooting covers likely issues

## Resources

For detailed format specification, see `references/sop-format-spec.md`.
