---
name: discover-framework
description: Research and add new strategic frameworks to the system (meta-skill). Use when user wants to add framework not in library; discovered new framework in their domain; asks "Can you add [Framework]?"; or no existing framework fits their need. Uses web search for comprehensive research, validates quality, creates framework files, and integrates into system.
---

# Discover Framework - Framework Research & Integration

## Overview

This skill helps users research and add new strategic frameworks to the Strategic Frameworks library. The approach is **rigorous and evidence-based** - only real, documented, proven frameworks are added.

**Core principles:**
- **Evidence-based** - Real frameworks with credible sources, not AI-generated
- **Comprehensive research** - Deep investigation before adding
- **Quality validation** - Strict criteria to maintain library quality
- **Proper integration** - Correct file structure and system updates
- **Community-driven** - Users expand the library collaboratively

**Output:** New framework file created, integrated into system, and ready to use via `use-framework`

---

## Workflow

### Phase 1: Context Gathering (5 minutes)

**Goal:** Understand what user needs and why.

**Questions to ask:**

1. **Problem/Need:**
   - "What problem or situation needs a framework that's not in our library?"
   - "Why don't existing frameworks fit?"
   - "What's missing from current options?"

2. **Framework Knowledge:**
   - "Do you have a specific framework in mind, or should I research options?"
   - "If you know the framework name, what is it?"
   - "Where did you hear about it?"

3. **Category:**
   - "What type of framework are you looking for?"
   - Options: Strategic / Decision / Innovation / Operations / Mental Models

4. **Use Case:**
   - "How would you use this framework?"
   - "What would it help you accomplish?"

**Determine approach:**

**If user knows specific framework:**
- "Great, let's research [Framework Name] deeply and add it"
- Move to Phase 3 (Deep Research)

**If user doesn't know specific framework:**
- "Let me search for frameworks that fit your need"
- Move to Phase 2 (Search & Selection)

### Phase 2: Internet Research & Selection (5-10 minutes)

**Goal:** Find 2-3 candidate frameworks matching user's need.

**Research approach:**

1. **Formulate search queries:**
   - Based on problem type, category, use case
   - Examples:
     - "strategic frameworks for [problem]"
     - "decision-making frameworks for [situation]"
     - "[domain] frameworks for [goal]"

2. **Use WebSearch extensively:**
   - Search for multiple candidates
   - Look for reputable sources
   - Find frameworks with clear methodology

3. **Initial screening:**
   For each candidate, quickly check:
   - Is it a real framework? (not just concept)
   - Does it have clear creator/origin?
   - Does it have structured methodology?
   - Is it documented somewhere credible?

4. **Present options to user:**

```markdown
## Framework Candidates

I found 3 frameworks that might fit:

### 1. [Framework Name] by [Creator]
**What it is:** [1-2 sentence description]
**Why it fits:** [How it addresses user's need]
**Source:** [Where it's documented]

### 2. [Framework Name] by [Creator]
**What it is:** [Description]
**Why it fits:** [Fit reasoning]
**Source:** [Documentation]

### 3. [Framework Name] by [Creator]
**What it is:** [Description]
**Why it fits:** [Fit reasoning]
**Source:** [Documentation]

Which would you like me to research deeply and add to the system?
```

5. **User selects:**
   - Get user's choice
   - Proceed to Phase 3 with selected framework

### Phase 3: Deep Research & Validation (10-15 minutes)

**Goal:** Comprehensive investigation of selected framework and validation against quality criteria.

**What to research (comprehensive):**

Use `references/research-checklist.md` as guide. Research systematically:

1. **Framework Identity**
   - Full name (official)
   - Creator(s) - name(s), credentials
   - Year created/published
   - Origin story / context of creation
   - Original publication or source

2. **Framework Methodology**
   - Core structure (phases, steps, components)
   - Key concepts and principles
   - How it works (process flow)
   - What makes it unique
   - Theoretical foundation

3. **Practical Application**
   - Target audience (who uses it?)
   - Use cases (when to use it?)
   - Implementation process
   - Tools or templates available
   - Typical outcomes

4. **Real-World Validation**
   - Companies using it (specific names)
   - Leaders/practitioners using it
   - Success stories / case studies (2-3 specific examples)
   - Industry recognition
   - Academic validation (if applicable)

5. **Learning Resources**
   - Original book/paper
   - Key articles or guides
   - Videos or courses
   - Official websites
   - Authoritative secondary sources

6. **Keywords for Matching**
   - Problem types it addresses
   - Situations where it fits
   - Domain or industry focus
   - Related concepts

**Quality validation:**

Check against `references/quality-criteria.md`. Assess:

**FATAL DISQUALIFIERS (Stop if present):**
🔴 AI-generated or made-up framework
🔴 No credible sources or citations
🔴 Duplicate of existing framework in library
🔴 Fundamentally flawed methodology
🔴 Controversial/unethical framework

**REQUIRED ELEMENTS (Must have all):**
✅ Real creator with credentials
✅ Clear origin and publication date
✅ Structured methodology with steps
✅ Real-world examples (at least 2)
✅ Credible sources (at least 3)
✅ Practical applicability
✅ Unique value vs existing frameworks

**NICE TO HAVE (Not required but valuable):**
⭐ Multiple case studies
⭐ Tools or templates
⭐ Academic papers
⭐ Wide industry adoption
⭐ Books or comprehensive guides

**Validation decision:**

- **If passes:** "This framework meets our quality criteria. Let's add it."
- **If fails:** "This framework doesn't meet our quality criteria because [reasons]. Let me suggest alternatives:  [other options]"
- **If marginal:** Discuss with user: "This framework is borderline because [concerns]. Should we add it anyway or look for alternatives?"

### Phase 4: Framework Creation (5-10 minutes)

**Goal:** Create properly formatted framework file.

**Steps:**

1. **Determine framework number:**
   - Check existing frameworks in `frameworks/` folder
   - Find highest number (currently 48)
   - New framework = next sequential number
   - Example: If latest is 48, new framework is 49

2. **Create filename:**
   - Format: `[number]-[framework-name].md`
   - Use kebab-case (lowercase with hyphens)
   - Example: `39-scamper-technique.md`

3. **Use template from `references/framework-template.md`:**

```markdown
# [Framework Name]

## Overview

[2-3 sentence description of what this framework is and what it helps accomplish]

## Creator & Origin

**Created by:** [Name(s) with credentials]

**When:** [Year]

**Context:** [Why was it created? What problem was it solving? What was happening at the time?]

**Original source:** [Book, paper, or initial publication]

## Target Audience

**Best for:**
- [User type 1] - [why]
- [User type 2] - [why]
- [User type 3] - [why]

**Not ideal for:**
- [Situation where it doesn't fit]

## When to Use This Framework

**Use this framework when:**
- [Situation 1]
- [Situation 2]
- [Situation 3]

**Don't use this framework when:**
- [Situation where alternative is better]

## Framework Structure

### Phase 1: [Phase Name]

**Goal:** [What this phase accomplishes]

**Key questions:**
- [Question 1]
- [Question 2]
- [Question 3]

**Output:** [What you produce in this phase]

### Phase 2: [Phase Name]

[Same structure for each phase...]

[Continue for all phases/steps]

## Real-World Examples

### Example 1: [Company/Person] - [Context]

**Situation:** [What challenge they faced]

**Application:** [How they used the framework]

**Outcome:** [What happened as a result]

### Example 2: [Company/Person] - [Context]

[Same structure]

### Example 3: [Company/Person] - [Context]

[Same structure - at least 2 examples required, 3 preferred]

## Notable Users

**Companies:**
- [Company 1]
- [Company 2]
- [Company 3]

**Thought Leaders:**
- [Name 1]
- [Name 2]

## Sources & Further Reading

**Essential:**
- [Original book/paper with full citation]
- [Key article or guide]
- [Official website if exists]

**Additional:**
- [Supplementary resource 1]
- [Supplementary resource 2]

**Videos/Courses:**
- [If available]

## Keywords

For framework matching:
- [keyword1]
- [keyword2]
- [keyword3]
- [problem-type]
- [situation-context]
- [domain/industry]
```

4. **Fill in all sections:**
   - Use research from Phase 3
   - Be comprehensive and specific
   - Include all required elements
   - Use clear, accessible language

5. **Review for quality:**
   - All sections complete?
   - Specific examples (not generic)?
   - Sources credible and cited?
   - Keywords appropriate?
   - Structure clear and usable?

### Phase 5: Integration (5 minutes)

**Goal:** Integrate new framework into system.

**Steps:**

1. **Save framework file to both locations:**
   ```
   frameworks/[number]-[framework-name].md
   skills/use-framework/references/frameworks/[number]-[framework-name].md
   ```
   (Both locations must have identical files)

2. **Update frameworks-index.md:**
   Open `skills/choose-framework/references/frameworks-index.md`
   
   Add new entry in appropriate category:
   ```markdown
   ### [Category Name]
   
   [... existing frameworks ...]
   
   **[Number]. [Framework Name]** by [Creator]
   - [One-line description]
   - **Use for:** [primary use case]
   - **Keywords:** [keyword1], [keyword2], [keyword3]
   ```

3. **Update choose-framework matching logic:**
   Consider if SKILL.md needs updates to mention new framework in:
   - Framework Matching Logic section
   - Relevant category (Strategy/Decision/Innovation/Operations/Mental Models)

4. **Verify integration:**
   - Both framework files exist?
   - frameworks-index.md updated?
   - New framework appears in correct category?

### Phase 6: Verification & Test Offer (5 minutes)

**Goal:** Confirm success and offer to test new framework.

**Show user what was added:**

```markdown
# Framework Successfully Added! 🎉

## What was created:

**Framework:** [Framework Name] by [Creator]
**Number:** [XX]
**Category:** [Strategic/Decision/Innovation/Operations/Mental Models]
**Files created:**
- `frameworks/[filename].md`
- `skills/use-framework/references/frameworks/[filename].md`

**Index updated:**
- Added to `frameworks-index.md` under [Category]

## Framework Summary

[2-3 sentences about the framework]

**Best for:** [Primary use cases]

**Notable users:** [2-3 companies/people]

## Next Steps

Would you like to:
1. **Test the framework:** Use `/use-framework [Framework Name]` to try it with your situation
2. **Add another framework:** Use `/discover-framework` again
3. **Learn more:** I can explain how to apply this framework
```

**Offer to test:**
- "Want to try this framework on your problem? I can guide you through it using `/use-framework [name]`"
- If yes: Transition to use-framework with the new framework
- If no: "Great! The framework is now available in the system for anyone to use."

---

## Special Cases

### Framework Already Exists

If during research you discover framework is already in library (maybe under different name):

**Response:**
"I found that [Framework Name] is already in our library as [Existing Framework]. 

[Show existing framework details]

Would you like to:
1. Use the existing framework with `/use-framework [name]`
2. Look for a different framework
3. Improve the existing framework documentation"

### Framework Fails Quality Criteria

If framework doesn't meet quality standards:

**Response:**
"I researched [Framework Name], but it doesn't meet our quality criteria because:
- [Specific reason 1 - e.g., no credible sources]
- [Specific reason 2 - e.g., AI-generated content]
- [Specific reason 3 - e.g., no real-world validation]

Our library maintains high quality standards - we only add real, proven frameworks.

Would you like me to:
1. Search for alternative frameworks that solve your need
2. Investigate a different framework you have in mind
3. Work with existing frameworks in the library"

### Duplicate Framework (Different Name)

If new framework is essentially same as existing one:

**Response:**
"[Framework Name] is very similar to [Existing Framework] already in our library. They both:
- [Similarity 1]
- [Similarity 2]

The main difference is [key difference].

Would you like to:
1. Use the existing [Existing Framework]
2. Add this as a variant (if difference is meaningful)
3. Look for a more distinct framework"

### Framework Needs More Research

If you can't find enough information:

**Response:**
"I found [Framework Name] but couldn't find enough credible information to add it:
- Missing: [What's missing - creator, methodology, examples, sources]

This might mean:
- Framework is too new/obscure
- Framework is not well-documented
- Framework might not be real/established

Would you like to:
1. Help me find more sources about this framework
2. Look for better-documented alternatives
3. Consider existing frameworks that might work"

---

## Quality Checklist

Before marking framework as complete, verify:

**Research completeness:**
- [ ] Creator identified with credentials
- [ ] Year and origin story documented
- [ ] Methodology clearly explained
- [ ] At least 2 real-world examples found
- [ ] At least 3 credible sources cited
- [ ] Keywords identified for matching

**Quality criteria met:**
- [ ] Real framework (not AI-generated)
- [ ] Credible sources exist
- [ ] Not duplicate of existing framework
- [ ] Structured methodology with steps
- [ ] Practical applicability demonstrated
- [ ] Unique value proposition clear

**Integration complete:**
- [ ] Framework file created in `frameworks/`
- [ ] Framework file copied to `skills/use-framework/references/frameworks/`
- [ ] frameworks-index.md updated
- [ ] Appropriate category selected
- [ ] Keywords added for matching

**File quality:**
- [ ] All template sections filled
- [ ] Specific examples (not generic)
- [ ] Sources properly cited
- [ ] Clear and accessible language
- [ ] Usable structure for workshops

---

## Key Reminders

1. **Use WebSearch extensively** - This skill depends on web research
2. **Validate rigorously** - Quality standards protect library integrity
3. **Be skeptical** - Many "frameworks" online are made-up or low-quality
4. **Document thoroughly** - Create comprehensive framework files
5. **Test fit** - Framework should fill gap in current library
6. **Integrate properly** - Files in both locations, index updated
7. **Offer to test** - Let user try their new framework immediately

---

## Warning Signs (Don't Add These)

🚫 **AI-generated frameworks** - ChatGPT created, no real origin
🚫 **Blog post "frameworks"** - Random blog coined term, no adoption
🚫 **Unvalidated methodologies** - No one actually uses it
🚫 **Repackaged existing frameworks** - Just renamed something that exists
🚫 **Overly complex academic models** - Theory with no practical application
🚫 **Fad frameworks** - Trendy but no substance
🚫 **Self-help guru "systems"** - Motivational speech, not framework

**Test:** Would serious business leaders, academics, or practitioners use this? If not, don't add it.

---

## References

- `references/framework-template.md` - Template structure for new frameworks
- `references/research-checklist.md` - What to research about frameworks
- `references/quality-criteria.md` - Standards for accepting frameworks
