---
name: learning-capture
description: Recognize and capture reusable patterns, workflows, and domain knowledge from work sessions into new skills. Use when completing tasks that involve novel approaches repeated 2+ times, synthesizing complex domain knowledge across conversations, discovering effective reasoning patterns, or developing workflow optimizations. Optimizes for high context window ROI by identifying patterns that will save 500+ tokens per reuse across 10+ future uses.
---

# Learning Capture

## Overview

This skill enables continual learning by recognizing valuable patterns during work and capturing them as new skills. It focuses on high-ROI captures: patterns that will save significant context window tokens through frequent reuse.

## Recognition Framework

Monitor for these five types of learning moments:

### 1. Novel Problem-Solving Approaches
**Trigger**: Develop a creative, non-obvious solution to a complex problem that could apply to similar future problems.

**Strong signals**:
- Solution required multi-step reasoning or novel tool combinations
- Approach is generalizable beyond this specific instance
- User expresses satisfaction with the results
- Similar problem type likely to recur

### 2. Repeated Patterns
**Trigger**: User requests similar tasks 2-3 times and a consistent approach emerges.

**Strong signals**:
- Pattern has repeated 2+ times with consistent structure
- User asks "can you do the same thing as before?"
- Task type is clearly ongoing (e.g., weekly reports, monthly communications)
- Each instance requires re-explaining the approach

### 3. Domain-Specific Knowledge
**Trigger**: User explains company processes, terminology, schemas, or standards that span multiple conversations.

**Strong signals**:
- Information accumulates across 2+ conversations
- Knowledge is stable (won't change weekly)
- User frequently asks questions in this domain
- Re-explaining costs 1000+ tokens each time

### 4. Effective Reasoning Patterns
**Trigger**: Discover a particular way of structuring thinking that consistently produces better results.

**Strong signals**:
- Pattern applies to a category of problems, not just one instance
- Results are notably better than simpler approaches
- Structure is teachable and reproducible
- Problem category recurs frequently

### 5. Workflow Optimizations
**Trigger**: Figure out an efficient way to chain tools or steps together that produces comprehensive results.

**Strong signals**:
- Workflow chains 3+ distinct steps
- Pattern generalizes to similar task types
- User appreciates the thoroughness
- Similar workflows likely needed regularly

## Decision Framework

**Offer capture when ALL of the following are true**:

1. **High confidence (>95%) of significant ROI**:
   - Pattern will be reused 10+ times across future conversations
   - Each reuse saves 500+ tokens of re-explanation
   - The skill itself costs <5000 tokens to load

2. **Strong reusability signal present**:
   - Pattern has repeated 2+ times already, OR
   - User explicitly indicates ongoing need ("I do this weekly"), OR
   - Complex domain knowledge worth formalizing, OR
   - Novel workflow with clear generalizability

3. **Not redundant with existing capabilities**:
   - No existing skill already covers this pattern
   - Adds meaningful value beyond general knowledge

**Do NOT offer capture when**:
- First instance of a pattern (wait for repetition)
- Highly context-specific solution (won't generalize)
- Simple task using existing capabilities (no marginal value)
- Creative/one-off work (low reuse probability)
- Ambiguous reusability (unclear if it will recur)

**Consult references/decision-examples.md** for concrete examples of high-confidence vs. low-confidence scenarios.

## Capture Process

### Step 1: Recognize the Learning Moment

While working, monitor for recognition triggers from the framework above. Track:
- Is this a repeated pattern?
- Does this generalize beyond this instance?
- Would formalizing this save significant tokens in future uses?

### Step 2: Evaluate Against Decision Framework

Before offering capture, verify:
- ROI calculation: (Expected_reuses × Tokens_saved) >> Skill_cost
- Strong reusability signal is present
- Not redundant with existing capabilities

If all checks pass, proceed to offer. If uncertain, do NOT offer.

### Step 3: Offer Capture Conservatively

**Timing**: Offer after completing the immediate task, not mid-task.

**Phrasing**: Be concise and specific about what would be captured and why it's valuable.

**Good examples**:
- "I notice I've structured the last three internal comms documents similarly. Would it be helpful to capture this as a skill for future communications?"
- "I've built up understanding of your data architecture across our conversations. Should I formalize this as a skill for more efficient future reference?"
- "The validation workflow I developed seems applicable to your other messy datasets. Worth capturing as a skill?"

**Avoid**:
- Over-explaining the decision reasoning
- Offering when confidence is <95%
- Interrupting task flow to offer

### Step 4: Structure the Draft Skill

When user agrees to capture, create a draft skill file following these steps:

1. **Select appropriate template** from references/skill-templates.md based on learning moment type
2. **Structure the skill** using the template as a guide
3. **Keep it concise**: Focus on what's non-obvious and reusable
4. **Include specific triggers**: Make it clear when to use this skill
5. **Add examples** where helpful for clarity
6. **Save to outputs**: Create the draft at `/mnt/user-data/outputs/[skill-name].skill/`

The draft skill should be ready for user review and upload with minimal editing needed.

### Step 5: Present the Draft

After creating the draft skill:

1. **Provide context**: Briefly explain what the skill captures and why it will be valuable
2. **Highlight key sections**: Point out the most important parts of the skill
3. **Suggest refinements**: Note any areas where user input would improve the skill
4. **Explain next steps**: User reviews, potentially edits, then uploads via the UI for future conversations

## Key Principles

**Conservative by default**: Better to capture 80% of truly valuable patterns than create noise. Only offer when confidence is very high.

**ROI-focused**: Prioritize patterns with high reuse frequency and high token savings per reuse.

**Context window awareness**: Skills cost tokens to load. A skill should pay for itself within 10 uses.

**Interpretable**: Skills are plain text and easy to review, correct, and refine. This transparency is a feature.

**User-controlled**: The manual upload step ensures quality control and user agency over what gets added to the knowledge base.

## Resources

### references/skill-templates.md

Templates for structuring different types of skills based on the learning moment type. Includes:
- Workflow/Process skill template
- Domain Knowledge skill template  
- Task Pattern skill template
- Reasoning/Prompt Pattern skill template
- Template selection guide

Read this file when structuring a captured skill to use the appropriate template.

### references/decision-examples.md

Detailed examples of high-confidence capture scenarios (where to offer) and low-confidence scenarios (where NOT to offer). Includes:
- Concrete examples with signal analysis
- Recognition pattern checklists
- Decision threshold guidelines
- ROI calculation examples

Read this file when uncertain whether a learning moment meets the capture threshold.
