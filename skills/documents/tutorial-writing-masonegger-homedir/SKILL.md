---
name: tutorial-writing
description: Technical tutorial writing in modified DigitalOcean style. Use when (1)
  writing step-by-step technical tutorials, (2) creating documentation for code/applications,
  (3) explaining technical concepts pr
---

---
name: tutorial-writing
description: Technical tutorial writing in modified DigitalOcean style. Use when (1) writing step-by-step technical tutorials, (2) creating documentation for code/applications, (3) explaining technical concepts procedurally, (4) working with Temporal applications/tutorials, or (5) the user asks to write, create, or help with a tutorial. Follows specific style constraints: friendly but formal tone, comprehensive explanations, code sandwich approach, assumes English is reader's second language, and never generates new code (only references provided code).
---

# Technical Tutorial Writing

Write comprehensive, step-by-step technical tutorials following a modified DigitalOcean style guide.

## Core Constraints

**CRITICAL:** Follow these constraints strictly - they override other considerations:

1. **Never generate new code** - ONLY reference code provided in context
2. **Follow style guide exactly** - See [references/style-guide.md](references/style-guide.md)
3. **Use code sandwich approach** - See [references/code-sandwich.md](references/code-sandwich.md)
4. **Flag uncertainties** - Use `<CLAUDE_HELP></CLAUDE_HELP>` XML tags when unsure

## Workflow

Follow this sequential process for all tutorials:

### 1. Analyze Rules

Read the comprehensive style guide before starting:
* **Required:** Read [references/style-guide.md](references/style-guide.md)
* **If Temporal tutorial:** Read [references/temporal-rules.md](references/temporal-rules.md)
* **For code explanation:** Review [references/code-sandwich.md](references/code-sandwich.md)

### 2. Understand the Code

* Read all provided code files thoroughly
* Understand architecture and component interactions
* Identify key concepts readers need to learn
* **Never generate new code** - only use what's provided
* Ask clarifying questions if needed

### 3. Study Author's Voice

* Read [references/mmegger-writing-style.md](references/mmegger-writing-style.md) for Mason Egger-specific patterns
* Note unique transition phrases ("Now that...", "Once you've done...")
* Observe pronoun mixing (strategic use of "we" and "you")
* Match sentence rhythm (short → medium → short)
* Use author-specific vocabulary and phrasing

### 4. Create Outline

* Design information sequence for new learners
* Think deeply about logical flow
* Include reasoning for your structure choices
* Write to `output/outline.md`
* Get user approval before proceeding

Outline should include:
* Tutorial title
* Introduction topics
* Prerequisites list
* Each step with brief description
* Conclusion topics
* Reasoning for sequence

### 5. Write Sections

Once outline is approved, write one section at a time:

* Follow outline exactly - don't deviate
* Apply code sandwich approach to all code blocks
* Follow style guide formatting and tone
* Use only provided code (never generate new code)
* Write to `output/SECTION_<NUMBER>.md`
* Get approval before moving to next section

**Section checklist before submitting:**
- [ ] Follows outline structure
- [ ] Uses only provided code
- [ ] Applies code sandwich to all code
- [ ] Follows style guide
- [ ] Friendly but formal tone
- [ ] Explains WHY not just WHAT
- [ ] Includes transitions
- [ ] No AI-giveaway phrases
- [ ] 6th-9th grade reading level
- [ ] Temporal primitives capitalized (if applicable)

### 6. Combine Sections

After all sections approved:

```bash
cat output/SECTION_1.md >> output/first_draft.md
cat output/SECTION_2.md >> output/first_draft.md
# Continue for all sections
```

* Use bash commands - don't manually copy
* Don't change approved text
* Output: `output/first_draft.md`

## Key Style Requirements

### Tone and Approach

* **Friendly but formal** - No jargon, memes, slang, emoji, or jokes
* **Second person** - "You will configure" not "We will learn"
* **Outcome-focused** - "In this tutorial, you will install Apache"
* **Comprehensive** - Explain everything, assume no prior knowledge
* **Avoid assumptive words** - No "simply," "just," "obviously," "easy"

### Code Presentation

Use the **Code Sandwich** approach (see [references/code-sandwich.md](references/code-sandwich.md)):

1. **Introduce the issue** - What problem does this solve?
2. **Show the code** - Present the code block
3. **Explain in detail** - How does it work and why?

Break code into logical chunks, explain each, then provide complete version in "Bringing it all together" section.

### Structure

**Procedural tutorials:**
* Title (H1)
* Introduction (H3)
* Prerequisites (H2)
* Step 1 — Creating something (H2, use em-dash and gerund)
* Step 2 — Doing next thing (H2)
* Conclusion (H2)

Each step needs intro sentence and transition to next step.

### Formatting

* **Bold:** GUI text, hostnames, usernames
* **Italics:** Technical terms on first introduction only
* **Inline code:** Commands, files, paths, packages, ports, keys
* **Code blocks:** Commands, files, scripts, output
* No command prompts (`$` or `#`) in code blocks
* Each sentence on its own line

### Reading Level

* Target 6th-9th grade reading level
* Flesch Reading Ease Score of 70 or below
* Assume English is reader's second language
* Avoid idioms and complex vocabulary
* No SAT words

### Temporal-Specific Rules

When writing Temporal tutorials, capitalize official primitives:
* Workflow, Activity, Worker, Timer, Signal, Query, Task Queue

See [references/temporal-rules.md](references/temporal-rules.md) for details.

## Word Count Tracking

Use the bundled `wordcount` tool to track tutorial length:

```bash
# Count single file
scripts/wordcount output/first_draft.md

# Count all sections
scripts/wordcount output/

# Recursive count
scripts/wordcount output/ -r
```

See [references/wordcount-usage.md](references/wordcount-usage.md) for complete usage guide.

## Handling Uncertainty

When you encounter situations where you cannot proceed:

1. Flag the section with `<CLAUDE_HELP></CLAUDE_HELP>` tags
2. Describe what you were trying to do
3. Continue with rest of the section/tutorial
4. Inform user at end about flagged sections

**Examples of when to flag:**
* Need screenshot of running application
* Missing code you need to reference
* Unsure how something works
* Cannot complete section as designed

## Resources

### scripts/
* [wordcount](scripts/wordcount) - Track word counts in Markdown files (excludes code blocks)

### references/
* [style-guide.md](references/style-guide.md) - Comprehensive tutorial writing style guide (read first)
* [mmegger-writing-style.md](references/mmegger-writing-style.md) - Mason Egger-specific voice patterns and transitions
* [temporal-rules.md](references/temporal-rules.md) - Temporal-specific writing conventions
* [code-sandwich.md](references/code-sandwich.md) - Detailed code presentation approach
* [wordcount-usage.md](references/wordcount-usage.md) - Complete wordcount tool documentation
* [workflow.md](references/workflow.md) - Detailed step-by-step tutorial writing process

## Quick Reference

**Writing flow:**
1. Read [style-guide.md](references/style-guide.md) and [mmegger-writing-style.md](references/mmegger-writing-style.md)
2. Understand provided code (never generate new code)
3. Create outline → get approval
4. Write sections one at a time → get approval for each
5. Combine sections with bash commands

**Key principles:**
* Comprehensive yet accessible (6th-9th grade level)
* Explain WHY not just WHAT
* Code sandwich for all code blocks
* Only use provided code
* Friendly but formal tone
* Focus on reader outcomes

**Common mistakes to avoid:**
* Generating new code instead of using provided code
* Using AI-giveaway phrases ("dive into," "unleash")
* Making assumptions ("simply," "just," "obviously")
* Not explaining commands before showing them
* Forgetting transitions between steps
* Using first person ("we will learn")
