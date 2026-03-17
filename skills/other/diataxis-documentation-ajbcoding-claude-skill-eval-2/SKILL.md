---
name: writing-documentation-with-diataxis
description: Applies the Diataxis framework to create or improve technical documentation. Use when being asked to write high quality tutorials, how-to guides, reference docs, or explanations, when reviewing documentation quality, or when deciding what type of documentation to create. Helps identify documentation types using the action/cognition and acquisition/application dimensions.
---

# Writing Documentation with Diataxis

You help users create and improve technical documentation using the Diataxis framework, which identifies four distinct documentation types based on user needs.

## What Diataxis Is

Diataxis is a framework for creating documentation that **feels good to use** - documentation that has flow, anticipates needs, and fits how humans actually interact with a craft.

**Important**: Diataxis is an approach, not a template. Don't create empty sections for tutorials/how-to/reference/explanation just to have them. Create content that serves actual user needs, apply these principles, and let structure emerge organically.

**Core insight**: Documentation serves practitioners in a domain of skill. What they need changes based on two dimensions:
1. **Action vs Cognition** - doing things vs understanding things
2. **Acquisition vs Application** - learning vs working

These create exactly four documentation types:
- **Learning by doing** → Tutorials
- **Working to achieve a goal** → How-to Guides
- **Working and need facts** → Reference
- **Learning to understand** → Explanation

**Why exactly four**: These aren't arbitrary categories. The two dimensions create exactly four quarters - there cannot be three or five. This is the complete territory of what documentation must cover.

## The Diataxis Compass (Your Primary Tool)

When uncertain which documentation type is needed, ask two questions:

**1. Does the content inform ACTION or COGNITION?**
- Action: practical steps, doing things
- Cognition: theoretical knowledge, understanding

**2. Does it serve ACQUISITION or APPLICATION of skill?**
- Acquisition: learning, study
- Application: working, getting things done

Then apply:

| Content Type | User Activity | Documentation Type |
|--------------|---------------|--------------------|
| Action       | Acquisition   | **Tutorial**       |
| Action       | Application   | **How-to Guide**   |
| Cognition    | Application   | **Reference**      |
| Cognition    | Acquisition   | **Explanation**    |

## When Creating New Documentation

### 1. Identify the User Need

Ask yourself:
- Who is the user? (learner or practitioner)
- What do they need? (to do something or understand something)
- Where are they? (studying or working)

### 2. Use the Compass

Apply the two questions above to determine which documentation type serves this need.

### 3. Apply the Core Principles

**For Tutorials** (learning by doing):
- You're responsible for the learner's success - every step must work
- Focus on doing, not explaining
- Show where they're going upfront
- Deliver visible results early and often
- Maintain narrative of expectation ("You'll see...", "Notice that...")
- Be concrete and specific - one path only, no alternatives
- Eliminate the unexpected - perfectly repeatable
- Encourage repetition to build the "feeling of doing"
- Aspire to perfect reliability

**For How-to Guides** (working to achieve goals):
- Address real-world problems, not tool capabilities
- Assume competence - they know what they want
- Provide logical sequence that flows with human thinking
- Address real-world complexity with conditionals ("If X, do Y")
- **Seek flow** - anticipate their next move, minimise context switching
- Omit unnecessary detail - practical usability beats completeness
- Focus on tasks, not tools
- Name guides clearly: "How to [accomplish X]"

**For Reference** (facts while working):
- Describe, don't instruct - neutral facts only
- Structure mirrors the product architecture
- Use standard, consistent patterns throughout
- Be austere and authoritative - no ambiguity
- Separate description from instruction
- Provide succinct usage examples
- Completeness matters here (unlike how-to guides)

**For Explanation** (understanding concepts):
- Talk about the subject from multiple angles
- Answer "why" - design decisions, history, constraints
- Make connections to related concepts
- Provide context and bigger picture
- Permit opinion and perspective - discuss trade-offs
- Keep boundaries clear - no instruction or pure reference
- Take higher, wider perspective

### 4. Use Appropriate Language

**Tutorials**: "We will create..." "First, do X. Now, do Y." "Notice that..." "You have built..."

**How-to Guides**: "This guide shows you how to..." "If you want X, do Y" "To achieve W, do Z"

**Reference**: "X is available as Y" "Sub-commands are: A, B, C" "You must use X. Never Y."

**Explanation**: "The reason for X is..." "W is better than Z, because..." "Some prefer W. This can be effective, but..."

### 5. Check Boundaries

Review your content:
- Does any part serve a different user need?
- Is there explanation in your tutorial? (Extract and link to it)
- Are you instructing in reference? (Move to how-to guide)
- Is there reference detail in your how-to? (Link to reference instead)

If content serves multiple needs, split it and link between documents.

## When Reviewing Existing Documentation

Use this iterative workflow:

**1. Choose a piece** - Any page, section, or paragraph

**2. Challenge it** with these questions:
- What user need does this serve?
- Which documentation type should this be?
- Does it serve that need well?
- Is the language appropriate for this type?
- Does any content belong in a different type?

**3. Use the compass** if the type is unclear

**4. Identify one improvement** that would help right now

**5. Make that improvement** according to Diataxis principles

**6. Repeat** with another piece

Don't try to restructure everything at once. Structure emerges from improving individual pieces.

## Key Principles

**Flow is paramount**: Documentation should move smoothly with the user, anticipating their next need. For how-to guides especially, think: What must they hold in their mind? When can they resolve those thoughts? What will they reach for next?

**Boundaries are protective**: Keep documentation types separate. The most common mistake is mixing tutorials (learning) with how-to guides (working).

**Structure follows content**: Don't create empty sections. Write content that serves real needs, apply Diataxis principles, and let structure emerge organically.

**One need at a time**: Each piece serves one user need. If users need multiple things, create multiple pieces and link between them.

**Good documentation feels good**: Beyond accuracy, documentation should anticipate needs, have flow, and fit how humans work.

## Common Mistakes to Avoid

1. **Tutorial/How-to conflation** - Tutorials are for learning (study), how-to guides are for working. Signs you've mixed them:
   - Your "tutorial" assumes users know what they want to do
   - Your "tutorial" offers multiple approaches
   - Your "how-to guide" tries to teach basic concepts
   - Your "tutorial" addresses real-world complexity

2. **Over-explaining in tutorials** - Trust that learning happens through doing. Give minimal explanation and link to detailed explanation elsewhere.

3. **How-to guides that teach** - Assume competence. Don't explain basics.

4. **Reference that instructs** - Reference describes, it doesn't tell you what to do.

5. **Explanation in action-oriented docs** - Move it to explanation docs and link to it.

## Quick Reference Table

| Aspect             | Tutorials           | How-to Guides       | Reference            | Explanation            |
|--------------------|---------------------|---------------------|----------------------|------------------------|
| **Answers**        | "Can you teach me?" | "How do I...?"      | "What is...?"        | "Why...?"              |
| **User is**        | Learning by doing   | Working on task     | Working, needs facts | Studying to understand |
| **Content**        | Action steps        | Action steps        | Information          | Information            |
| **Form**           | A lesson            | Directions          | Description          | Discussion             |
| **Responsibility** | On the teacher      | On the user         | Neutral              | Shared                 |
| **Tone**           | Supportive, guiding | Direct, conditional | Austere, factual     | Discursive, contextual |

## Supporting Files

For more detailed guidance, refer to:
- **principles.md** - Comprehensive principles for each documentation type with examples
- **reference.md** - Quality framework, complex scenarios, and additional guidance

## Output Requirements

When applying Diataxis:
- Be direct and practical
- Focus on serving user needs
- Use the compass to resolve uncertainty
- Cite which documentation type you're applying and why
- If reviewing docs, be specific about what type it should be and how to improve it
- Use British English spelling throughout
