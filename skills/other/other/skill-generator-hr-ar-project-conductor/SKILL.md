---
name: skill-generator
description: Meta-skill that creates new skills. Use when user repeatedly explains the same workflow, or mentions "save this as a skill", "remember this process", or "create a skill for this".
version: 1.0.0
---

# Skill Generator (Meta-Skill)

**This skill creates other skills.**

## When to Use
- User repeats similar instructions 2+ times in conversation
- User says "remember this", "save this workflow", "create a skill"
- You notice a pattern that should be automated
- User provides detailed methodology that should be reusable

## Detection Patterns
Track these signals:
1. **Repetition**: Same request type appears multiple times
2. **Detailed Instructions**: User explains step-by-step how to do something
3. **Explicit Request**: "Make this a skill", "Remember this process"
4. **API/Documentation Lookups**: User asks for current docs repeatedly

## Auto-Generation Process

### Step 1: Detect Pattern
After conversation where user explains methodology:
```bash
# Record the pattern
./skill-learner record \
  "User's request description" \
  "User's detailed instructions on how they want it done"
```

### Step 2: Acknowledge to User
```
🎓 I notice you've explained this workflow [N] times.
I'm tracking this pattern and will create a reusable skill after one more similar request.
This will let me automatically handle this in the future without needing detailed instructions.
```

### Step 3: Generate Skill (after threshold)
System automatically creates `.claude/skills/auto-[intent]-[id]/SKILL.md`

### Step 4: Confirm with User
```
✅ I've created a new skill for [intent]!

From now on, when you ask about [trigger phrases], I'll automatically:
1. [Step 1 from user's instructions]
2. [Step 2 from user's instructions]
3. [Step 3 from user's instructions]

The skill is saved in .claude/skills/auto-[name]/ and improves with each use.
You can edit it anytime to refine the approach.
```

## Special Cases

### API Documentation Skill
If user asks for API docs 2+ times:

```markdown
---
name: auto-api-docs-lookup
description: Always search web for current API documentation. Use whenever API, SDK, or technical documentation is mentioned.
allowed-tools: [web_search, web_fetch, bash_tool, view]
---

# API Documentation Lookup

## When to Use
- User mentions API, SDK, library documentation
- Technical integration questions
- "Latest" or "current" version queries

## Process (Auto-search enabled)
1. **ALWAYS web_search first**: "[library name] official documentation [current year]"
2. Prioritize official sources (github.com/org/repo, docs.library.com)
3. Use web_fetch to read full current docs
4. Cross-reference version compatibility
5. Cite sources with dates

## User Instruction
[User's explained methodology goes here]
```

### Analysis Skill
If user repeatedly explains analysis approach:

```markdown
---
name: auto-analysis-methodology
description: Analysis workflow based on user's preferred methodology. Use when user asks to "analyze", "evaluate", or "assess".
---

# Analysis Methodology

## When to Use
- "Analyze this..."
- "Evaluate the..."
- "Break down..."

## User's Preferred Approach
[Captured from user's repeated instructions]:
1. [Step they always mention first]
2. [Their second step]
3. [How they want results formatted]

## Validation
[How user checks if analysis is complete]
```

## Skill Improvement Loop
After each use of an auto-generated skill:

```python
# In your response, include:
"""
📊 Skill Usage Feedback

This used the auto-generated '[skill-name]' skill.

Did this match your expectations? If not, I can refine the skill by:
- Adding more detail
- Adjusting the methodology
- Including additional validation steps

Just say "improve the [skill-name] skill" and explain what to change.
"""
```

## Commands for Users

```bash
# Track a new pattern
./skill-learner track

# See what's being learned
./skill-learner list

# Manually create skill from current conversation
./skill-learner record "what user asked" "how they explained to do it"
```

## Integration with Claude Code

When user interacts with you:
1. **After response**: Check if this is a repetitive pattern
2. **Call**: `./skill-learner record "user_request" "your_methodology"`
3. **System**: Auto-generates skill at threshold
4. **Next time**: Skill is automatically invoked

## Example Workflow

**First Request:**
```
User: "Can you analyze this BRD? First read the executive summary, then assess market fit, then evaluate technical feasibility."
Claude: [Follows instructions, provides analysis]
Claude (internal): Records pattern via skill-learner
```

**Second Similar Request:**
```
User: "Analyze this other BRD following the same approach."
Claude: "🎓 I'm tracking this analysis pattern. One more similar request and I'll create a reusable skill."
Claude: [Executes analysis, records pattern]
Claude (internal): Skill auto-generated!
```

**Third Request:**
```
User: "Analyze the new warehouse BRD."
Claude: "✅ Using your custom analysis methodology skill..."
Claude: [Auto-invokes the learned skill, no detailed instructions needed]
```

## Maintenance

Skills are stored in `.claude/learning/patterns.json` - this tracks:
- Pattern signatures
- Occurrence counts
- Example requests
- Generated skills

Clean up old patterns:
```bash
# Review learned patterns
./skill-learner list

# Edit/remove if needed
nano .claude/learning/patterns.json
```

## Real-World Examples for Project Conductor

### Example 1: BRD Analysis Pattern
```bash
# First time: You explain in detail how to analyze BRDs
# Second time: You explain again (slightly different BRD)
# System: Auto-creates "auto-analysis-methodology" skill
# Third time: Just say "analyze this BRD" - skill auto-invokes!
```

### Example 2: API Documentation
```bash
# You ask: "What's the latest Express.js middleware documentation?"
# Claude: web_search → web_fetch → provides answer
# You ask again: "Check Socket.io docs for new authentication methods"
# System: Creates "auto-api-docs-lookup" skill with web-search enabled
# Future: Any API question automatically searches current docs first
```

### Example 3: Deployment Checklist
```bash
# You ask: "Help me deploy to production - check env vars, run tests, build Docker"
# You ask again: "Deploy the staging environment following same steps"
# System: Creates "auto-deployment-checklist" skill
# Future: "Deploy to [env]" auto-invokes comprehensive checklist
```
