---
name: refine-prompts
description: "Refine vague or unclear prompts into precise, actionable instructions. Use when user asks to clarify or improve instructions or when input is vague. Includes L1/L2/L3/L4 methodology, context enrichment, and intent clarification. Not for already clear prompts, simple questions, or when user explicitly rejects refinement."
user-invocable: true
---

<mission_control>
<objective>Refine vague or unclear prompts into precise, actionable instructions using L1/L2/L3/L4 methodology.</objective>
<success_criteria>Prompt refined to appropriate L-level with sufficient context and clear intent</success_criteria>
</mission_control>

## The Path to High-Quality Prompts

### 1. Match Complexity to Structure

Prompt structure should reflect task complexity. Simple tasks with complex templates waste tokens; complex tasks with simple prompts miss requirements.

**Select L-level by purpose:**

- **L1 (Single-sentence)**: Quick clarifications, straightforward outcomes
- **L2 (Context-rich paragraph)**: Default choice—balances clarity and efficiency
- **L3 (Structured bullets)**: Complex tasks with multiple constraints
- **L4 (Template/framework)**: Reusable patterns, repeatable workflows

**Why this works:** Right-sized structure ensures Claude understands requirements without over-constraining creativity or under-specifying deliverables.

### 2. Enrich Context, Reduce Ambiguity

Add relevant background, technical constraints, and success criteria. Context prevents wrong assumptions and reduces clarification rounds.

**Essential context elements:**

- Technical stack/platform/environment
- Forbidden approaches ("no external deps")
- Compliance requirements
- Output format specifications
- Measurable success targets

**Why this works:** Context acts as guardrails—Claude navigates within boundaries instead of guessing requirements.

### 3. Preserve What Matters, Delete What Doesn't

Keep only constraints that actually change the answer. Remove tone fluff, obvious best practices, and redundant examples.

**Keep these non-negotiables:**

- Tech stack/platform constraints
- Forbidden approaches
- Compliance requirements
- Hard output format (JSON, word limits)
- Measurable success targets

**Delete these inefficiencies:**

- Step-by-step instructions (Claude knows how to work)
- Tone guidance ("be professional," "be creative")
- Obvious best practices
- Redundant examples

**Why this works:** Minimal-yet-sufficient prompts achieve clarity with maximal efficiency. Every word should earn its place.

### 4. Specify Outputs Precisely

Define deliverables explicitly—format, structure, completeness. Ambiguous outputs produce ambiguous results.

**Output specification patterns:**

- "Complete deployable website with HTML/CSS/JS"
- "JSON array with objects containing id, name, timestamp"
- "≤500 words summary with key findings"
- "Unit tests achieving 90%+ coverage"

**Why this works:** Precise output specifications set clear expectations. Claude knows exactly what "done" looks like.



| If you need...         | Read...                                   |
| :--------------------- | :---------------------------------------- |
| Understand L-levels    | ## Quick Start → L1/L2/L3/L4 descriptions |
| Core methodology       | ## Core Methodology                       |
| See refinement example | ## Example                                |
| Output format          | ## Execution Process → STEP 4: Deliver    |

## Operational Patterns

- **Tracking**: Maintain a visible task list for prompt refinement
- **Consultation**: Consult the user when L-level is unclear
- **Management**: Manage task lifecycle for context enrichment

---

## Core Methodology

**FROM_SCRATCH method**: Convert user's goal/topic into outcome + minimal context + hard constraints

**REFINE method**: Delete fluff, keep only constraints that actually change the answer

**Default**: Produce prompts as a single plain-text paragraph (L2 format)

**Escalate**: Use keypoints (L3) and templates (L4) only when justified

## Execution Process

**When user provides prompt to refine:**

### STEP 1: Parse Input

- Extract user's raw prompt text
- Determine if FROM_SCRATCH or REFINE scenario
- Identify missing context, constraints, or deliverables

### STEP 2: Apply Refinement

- **FROM_SCRATCH**: Convert goal → outcome + context + hard constraints
- **REFINE**: Remove step-by-step instructions, obvious best practices, tone fluff, redundant examples
- **Keep**: Only constraints that actually change the answer

### STEP 3: Structure Output

Generate exactly:

- **L1**: One-sentence outcome statement
- **L2**: Context-rich paragraph with constraints (no Markdown)
- **L3**: Structured bullets (Task/Constraints/Output)
- **L4**: Template/framework (only if complex/reusable)
- **Rationale**: 2-4 sentences explaining minimal-yet-sufficient approach

### STEP 4: Deliver

Output ONLY the refined prompt in the exact format:

```
L1: [outcome statement]
L2: [context-rich paragraph with constraints]
L3:
- **Task:** [description]
- **Constraints:** [key constraints]
- **Output:** [deliverables]
L4:
```

[TEMPLATE ONLY IF JUSTIFIED - use ```code blocks for templates]

```
Rationale: [2-4 sentences explaining approach]
```

## Example

**Input**: "Create a marketing website"

**Output:**

```
L1: Create a conversion-optimized landing page
L2: You are a senior web developer creating a high-converting landing page for [PRODUCT]. Focus on clear value proposition, social proof placement, and frictionless CTA design. Use modern CSS Grid/Flexbox layouts with mobile-first approach. Ensure WCAG 2.1 AA accessibility compliance. Prioritize page speed optimization and SEO fundamentals. Output a complete, deployable website with semantic HTML, optimized images, and conversion tracking setup.
L3:
- **Task:** Create landing page for [PRODUCT] with conversion optimization
- **Constraints:** Mobile-first responsive design; WCAG 2.1 AA accessibility; <3s load time; semantic HTML; SEO-ready
- **Output:** Complete deployable website with HTML/CSS/JS files + performance audit + accessibility report
L4:
```

# Landing Page Requirements

## Value Proposition

- [Clear benefit statement in headline]
- [Supporting subheading]
- [Visual hero element]

## Conversion Elements

- [Primary CTA placement]
- [Secondary CTA for hesitant users]
- [Social proof testimonials]

## Technical Specs

- Responsive breakpoints: 320px, 768px, 1024px
- Performance budget: <150KB total, <3s load
- Accessibility: WCAG 2.1 AA checklist

```
Rationale: The refined prompt provides clear technical constraints (mobile-first, WCAG compliance, performance budget) while maintaining creative flexibility. The L4 template ensures consistent deliverable structure across different landing pages while allowing product-specific customization.
```

## Execution Best Practices

**Deliver clean, focused output:**

- Output ONLY the refined prompt—never methodology explanations
- Use L4 templates only for complex or reusable scenarios
- Maintain all non-negotiable constraints from original input
- Ask at most ONE question if ambiguity blocks producing useful refinement

**Pattern contrast:**

```
Good: Output L1→L2→L3→L4→Rationale format
Good: Remove fluff, keep constraints that change answers
Bad: Include methodology explanation in output
Bad: Use L4 when simple prompt suffices
```

**Validation check:** Refinement succeeds when it includes: 1) L1 outcome statement, 2) L2 context with constraints, 3) L3 structure, 4) L4 template if needed, 5) Clear rationale.

---

## Common Mistakes to Avoid

### Mistake 1: Using Wrong L-Level for Task Complexity

❌ **Wrong:**
"Build a complete authentication system with JWT tokens, refresh tokens, password hashing, email verification, and rate limiting." → L1 response

✅ **Correct:**
Identify complexity first. For multi-constraint tasks, use L3 or L4:
- L3: Use bullet structure for multiple requirements
- L4: Use template for repeatable patterns

### Mistake 2: Keeping Tone Guidance and Fluff

❌ **Wrong:**
"Be professional, creative, and thorough. Remember best practices. Be sure to use modern approaches."

✅ **Correct:**
Remove all tone guidance. Keep only constraints that change outcomes:
- "No external dependencies"
- "Use TypeScript strict mode"
- "Output must be deployable"

### Mistake 3: Missing Output Format Specification

❌ **Wrong:**
"Create a summary of the findings."

✅ **Correct:**
Specify exact format and structure:
"JSON array with objects: {id, name, timestamp, severity}. Max 100 items."

### Mistake 4: Over-Constraining with Step-by-Step Instructions

❌ **Wrong:**
"First read the file, then parse the JSON, then validate each field, then output the results."

✅ **Correct:**
State the outcome, let Claude determine the approach:
"Validate all fields in JSON file. Output errors as: {field, error, line_number}."

### Mistake 5: Refining Already Clear Prompts

❌ **Wrong:**
User: "Create a Python function that adds two numbers"
Claude: "Let me refine this by adding context..."

✅ **Correct:**
If prompt already has L1-L4 appropriate structure, proceed directly:
"Already clear. Here's the function:"
```python
def add(a, b):
    return a + b
```

---

## Validation Checklist

Before claiming prompt refinement complete:

**L-Level Selection:**
- [ ] L-level matches task complexity (not over-constraining, not under-specifying)
- [ ] L1 for simple single-outcome tasks
- [ ] L2 for default context-rich prompts
- [ ] L3 for multi-constraint complex tasks
- [ ] L4 for reusable patterns

**Context Enrichment:**
- [ ] Technical stack/platform specified
- [ ] Forbidden approaches identified
- [ ] Compliance requirements noted
- [ ] Output format clearly defined

**Constraint Quality:**
- [ ] Only non-negotiable constraints kept
- [ ] Tone guidance and fluff removed
- [ ] Obvious best practices deleted
- [ ] Step-by-step instructions replaced with outcomes

**Output Specification:**
- [ ] Exact format specified (JSON, markdown, code)
- [ ] Structure defined (array, object, bullets)
- [ ] Completeness criteria clear (max items, coverage %)

---

## Best Practices Summary

✅ **DO:**
- Match L-level to task complexity
- Add technical constraints, platform, environment
- Keep only constraints that change outcomes
- Specify exact output format and structure
- Use L4 templates for repeatable patterns
- Validate all 5 components: L1 outcome, L2 context, L3 structure, L4 template, rationale

❌ **DON'T:**
- Use high L-level for simple tasks (wastes tokens)
- Keep tone guidance ("be professional", "be creative")
- Include step-by-step instructions (Claude knows how)
- Add obvious best practices (Claude knows these)
- Refine already clear prompts
- Forget output format specification

---

<critical_constraint>
**Portability Invariant:**

This component must work standalone with zero external dependencies. All necessary philosophy and patterns are contained within.
</critical_constraint>
