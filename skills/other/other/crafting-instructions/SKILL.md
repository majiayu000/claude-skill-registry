---
name: crafting-instructions
description: Generate optimized instructions for Claude (Project instructions, Skills, or standalone prompts). Use when users request creating project setups, writing effective prompts, building Skills, or need guidance on instruction types for Claude.ai.
metadata:
  version: 0.3.1
---

# Crafting Instructions for Claude

Generate technically optimized instructions for Claude.ai across three formats: Project instructions, Skills, and standalone prompts.

## Decision Framework: Which Format to Use?

Ask these questions to determine the right format:

### Use PROJECT INSTRUCTIONS when:
- Context needs to persist for ALL conversations in a workspace
- Multiple team members collaborate with shared knowledge
- Background knowledge required for specific initiative
- Custom behavior scoped to one project only

**Signals:** "for this project", "all conversations about X", "team workspace", "project-specific"

### Use SKILL when:
- Capability needed across MULTIPLE contexts/projects
- Procedural knowledge that applies broadly
- Instructions should activate automatically when relevant
- Want portable expertise that loads on-demand

**Signals:** "every time I", "whenever", "reusable", "across projects", "teach Claude how to"

### Use STANDALONE PROMPT when:
- One-off request with immediate context
- Ad-hoc instructions for single use
- Conversational refinement
- No need for persistence

**Signals:** "for this task", "right now", "just this once", "can you"

### Combined Approaches:

**Project + Skill:**
- Project: Persistent context (market data, product specs)
- Skill: Reusable methods (analysis framework, report templates)
- Use when: Need both workspace context AND portable capabilities

**Skill + Prompt:**
- Skill: General expertise (code review standards)
- Prompt: Specific context ("review this PR for security")
- Use when: Foundational capability + immediate direction

## Core Optimization Principles

These apply to ALL instruction formats:

### 1. Imperative Construction
Frame as direct action commands, not suggestions:
- ❌ "Consider creating X" → ✅ "Create X when conditions Y"
- ❌ "You might want to" → ✅ "Execute" / "Generate"
- ❌ "Try to optimize" → ✅ "Optimize by"

### 2. Positive Directive Framing
State WHAT to do, not what NOT to do:
- ❌ "Don't use bullet points" → ✅ "Write in flowing paragraph form"
- ❌ "Avoid technical jargon" → ✅ "Use accessible language for beginners"
- ❌ "Never output lists" → ✅ "Present information in natural prose"

WHY: Negative instructions force inference. Positive instructions state desired behavior directly.

### 3. Context and Motivation
Explain WHY requirements exist:
- ❌ "Use paragraph form"
- ✅ "Use paragraph form because flowing prose is more conversational for casual learning"

WHY: Context helps Claude make better autonomous decisions in edge cases.

### 4. Strategic Over Procedural
Provide goals and decision frameworks, not step-by-step procedures:
- Specify: Success criteria, boundaries, decision frameworks
- Minimize: Sequential steps, detailed execution, obvious operations
- Rule: If Claude can infer procedure from goal, specify only the goal

**Model-aware calibration:**
- **Sonnet:** Include decision frameworks with explicit conditions and fallbacks. Concrete examples help more than abstract principles. When in doubt, add structure.
- **Opus:** Lean harder into strategic goals over procedures. Trust Opus to handle ambiguity—overly procedural instructions can constrain its natural reasoning. Principles > rules. Context about WHY is particularly valuable since Opus uses it for autonomous judgment in edge cases.

### 5. Trust Base Behavior
Claude's system prompt already covers:
- Citation protocols, copyright guidelines, safety
- General tool usage, artifact creation basics
- Conversational tone defaults, refusal handling
- Base accuracy and helpfulness standards

ONLY specify project/domain-specific deviations.

## Format-Specific Guidance

### For Project Instructions
See: [references/project-instructions.md](references/project-instructions.md)

Key points:
- Additive to system prompt (no duplication)
- Focus on workspace-specific behavior
- Enable extended thinking suggestions for complex domains
- Simple structure (headings/paragraphs) unless complexity demands more

### For Skills
See: [references/creating-skills.md](references/creating-skills.md)

Key points:
- Progressive disclosure (metadata → full instructions → bundled resources)
- Frontmatter: name + description with trigger patterns
- Keep SKILL.md under 500 lines
- Use references/ for detailed domain content

### For Standalone Prompts
See: [references/standalone-prompts.md](references/standalone-prompts.md)

Key points:
- Clear and explicit about desired output
- Provide context and examples when helpful
- Scale complexity to task needs
- Give permission to express uncertainty

## When to Suggest What

### "Use a Skill" when user says:
- "I keep having to explain this every time"
- "Can you remember how to do X?"
- "I need this across multiple projects"
- Repeating same instructions across conversations

### "Use Project instructions" when user says:
- "For this project, always..."
- "My team needs to work with..."
- "All conversations about this initiative should..."
- Building workspace with persistent context

### "Use a better prompt" when user says:
- Results are inconsistent
- Claude misunderstands intent
- Output format isn't right
- Need more comprehensive response

## Skills vs Projects: Key Differences

Read: [references/skill-vs-project.md](references/skill-vs-project.md) for detailed comparison

**Quick reference:**

**Project = "Here's what you need to know"**
- Static reference material always loaded
- Background knowledge for initiative
- Team workspace context

**Skill = "Here's how to do things"**
- Dynamic expertise loading on-demand
- Procedural knowledge and methods
- Portable across any conversation

**Example:**
- Project: "Q4 Product Launch" with market research, competitor docs
- Skill: competitive-analysis framework for analyzing any competitor

Use both together for powerful combinations.

## Example Quality Awareness

**CRITICAL for Claude 4.x:** Examples teach ALL patterns, including unintended ones.

When including examples:
- Audit EVERY detail (format, verbosity, structure, tone)
- Ensure ALL aspects demonstrate desired behavior
- Better to omit examples than include mixed signals
- If example uses bullets but you want prose, Claude will default to bullets

**Model-aware calibration:**
- **Sonnet:** Examples are highly influential—include 2-3 demonstrating desired patterns. Sonnet learns format/style strongly from examples.
- **Opus:** Examples help but are less essential. Opus weights explicit instructions and principles more heavily than pattern-matching from examples. One clear example often suffices; omit entirely if examples can't perfectly align with all requirements.

## Structural Simplicity

Default to clear organization:
- Headings and whitespace (primary approach)
- Explicit language stating relationships
- Natural paragraph flow

Use structured markup (XML/JSON) only when:
- Separating distinct content types in complex scenarios
- Absolute certainty about content boundaries required
- API-driven workflows needing structured parsing

## Extended Thinking Guidance

Extended thinking is UI toggle, not phrase-controlled.

In instructions, you CAN:
- Make assistant aware it exists
- Provide domain-specific indicators for suggesting it
- ❌ NOT: Include "trigger phrases" (they don't work)

Pattern:
```
For tasks involving [specific complexity], suggest enabling Extended 
thinking, explaining briefly why it would help for THIS task.
```

## Complexity Scaling

Match instruction complexity to task needs:

**Simple task** → Simple prompt or brief instructions
**Medium task** → Structured guidance with decision frameworks
**Complex task** → Comprehensive instructions + suggest extended thinking

Before adding complexity: Could simpler formulation work equally well?

## Model Selection & Instruction Density

When crafting instructions, consider which model will execute them:

**For Sonnet-executed instructions:**
- Explicit > implicit (state assumptions that might be obvious)
- More decision trees, fewer abstract principles
- Comprehensive edge case handling
- Concrete fallback behaviors
- Token-efficient but explicit

**For Opus-executed instructions:**
- Strategic goals > procedural steps
- Principles and reasoning > exhaustive rules
- Trust handling of unstated edge cases
- Provide rich WHY context—Opus uses it for autonomous judgment
- Permission to deviate when spirit conflicts with letter
- Can state: "Use judgment for cases not covered here"

**Instruction density heuristic:**
- Sonnet: 1.0-1.2x the detail you'd give a competent junior
- Opus: 0.6-0.8x the detail—more like briefing a senior peer

**When uncertain:** Instructions optimized for Opus will still work with Sonnet (just less perfectly). Instructions over-optimized for Sonnet may constrain Opus unnecessarily.

## Quality Checklist

Before delivering instructions:

**Strategic:**
- [ ] Clear goals stated without micromanagement
- [ ] Context explains WHY requirements exist
- [ ] Decision frameworks for ambiguous cases
- [ ] Constraints use positive framing when possible

**Technical:**
- [ ] Imperative language throughout
- [ ] Positive directives over negative restrictions
- [ ] Appropriate structure (simple by default)
- [ ] No system prompt duplication
- [ ] Examples (if any) perfectly aligned

**Execution:**
- [ ] Immediately actionable
- [ ] Success criteria clear
- [ ] Format matches complexity needs

## Common Mistakes to Avoid

❌ **System prompt duplication** - "Use web_search for current info, cite sources"
✅ Omit unless project has SPECIFIC deviations

❌ **Negative framing** - "Don't use lists, never be verbose"
✅ "Present in natural prose paragraphs"

❌ **Fake thinking triggers** - "Use 'think carefully' for deep thinking"
✅ "Suggest Extended thinking toggle for [specific complexity]"

❌ **Procedural micromanagement** - "Step 1: X, Step 2: Y..."
✅ "Goal: X. Quality standard: Y. Approach: Z."

❌ **Contextless requirements** - "Always use formal tone"
✅ "Use formal tone for professional docs because recipients expect authoritative voice"

❌ **Imperfect examples** - Example uses bullets when you want prose
✅ Either create perfect examples or omit entirely

## Additional Resources

- [references/creating-skills.md](references/creating-skills.md) - For building full Skills
- [references/project-instructions.md](references/project-instructions.md) - Detailed guidance for Project instructions
- [references/standalone-prompts.md](references/standalone-prompts.md) - Effective prompt patterns
- [references/skill-vs-project.md](references/skill-vs-project.md) - Detailed comparison and decision guidance
