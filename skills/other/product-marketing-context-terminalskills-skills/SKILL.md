---
name: product-marketing-context
description: "When the user wants to create or update their product marketing context document. Also use when the user mentions 'product context,' 'marketing context,' 'set up context,' 'positioning,' or wants to avoid repeating foundational information across marketing tasks. Creates `.claude/product-marketing-context.md` that other marketing skills reference."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: business
  tags:
    - product-marketing
    - positioning
    - messaging
---

# Product Marketing Context

## Overview

You help users create and maintain a product marketing context document. This captures foundational positioning and messaging information that other marketing skills reference, so users don't repeat themselves. The document is stored at `.claude/product-marketing-context.md`.

## Instructions

### Step 1: Check for Existing Context

First, check if `.claude/product-marketing-context.md` already exists.

**If it exists:** Read it, summarize what's captured, ask which sections to update, and only gather info for those sections.

**If it doesn't exist, offer two options:**

1. **Auto-draft from codebase** (recommended): Study the repo (README, landing pages, marketing copy, package.json, etc.) and draft a V1. The user reviews, corrects, and fills gaps. This is faster than starting from scratch.
2. **Start from scratch**: Walk through each section conversationally, one at a time.

Most users prefer option 1. After presenting the draft, ask: "What needs correcting? What's missing?"

### Step 2: Gather Information

**If auto-drafting:** Read the codebase (README, landing pages, marketing copy, about pages, meta descriptions, package.json, existing docs), draft all sections, present for review, iterate until satisfied.

**If starting from scratch:** Walk through each section below one at a time. Don't dump all questions at once. For each section: briefly explain what you're capturing, ask relevant questions, confirm accuracy, move to next. Push for verbatim customer language since exact phrases are more valuable than polished descriptions.

### Sections to Capture

**1. Product Overview** - One-line description, what it does (2-3 sentences), product category, product type (SaaS, marketplace, etc.), business model and pricing.

**2. Target Audience** - Target company type (industry, size, stage), target decision-makers (roles, departments), primary use case, jobs to be done (2-3), specific use cases or scenarios.

**3. Personas (B2B only)** - For each stakeholder (User, Champion, Decision Maker, Financial Buyer, Technical Influencer): what they care about, their challenge, and the value you promise them.

**4. Problems & Pain Points** - Core challenge before finding you, why current solutions fall short, what it costs them (time, money, opportunities), emotional tension.

**5. Competitive Landscape** - Direct competitors (same solution, same problem), secondary competitors (different solution, same problem), indirect competitors (conflicting approach). How each falls short.

**6. Differentiation** - Key differentiators (capabilities alternatives lack), how you solve it differently, why that's better, why customers choose you.

**7. Objections & Anti-Personas** - Top 3 objections heard in sales with responses. Who is NOT a good fit.

**8. Switching Dynamics (JTBD Four Forces)** - Push (frustrations with current solution), Pull (what attracts them to you), Habit (what keeps them stuck), Anxiety (worries about switching).

**9. Customer Language** - How customers describe the problem and your solution (verbatim), words/phrases to use, words to avoid, glossary of product-specific terms.

**10. Brand Voice** - Tone, communication style, brand personality (3-5 adjectives).

**11. Proof Points** - Key metrics or results, notable customers/logos, testimonial snippets, main value themes with supporting evidence.

**12. Goals** - Primary business goal, key conversion action, current metrics.

### Step 3: Create the Document

After gathering information, create `.claude/product-marketing-context.md` with clearly labeled sections for each of the 12 areas above. Use structured formatting with bold labels and tables where appropriate (personas table, objections table, glossary table, value themes table).

### Step 4: Confirm and Save

Show the completed document, ask if anything needs adjustment, save to `.claude/product-marketing-context.md`, and tell them: "Other marketing skills will now use this context automatically. Run `/product-marketing-context` anytime to update it."

## Examples

### Example 1: Auto-Draft from a SaaS Codebase

**User prompt:** "Set up my product marketing context."

The agent will check for `.claude/product-marketing-context.md` (doesn't exist), then offer the two options. The user chooses auto-draft. The agent reads README.md, the landing page component, package.json, and any marketing copy in the repo. It drafts a V1 covering all 12 sections based on what it finds, such as:
- Product Overview extracted from README and meta descriptions
- Target Audience inferred from landing page copy and feature descriptions
- Competitive Landscape based on comparison pages or "why us" sections
- Gaps clearly marked with "[needs input]" where the codebase doesn't provide enough info
The agent presents the draft and asks: "What needs correcting? What's missing?" Then iterates until the user approves and saves the file.

### Example 2: Updating an Existing Context Document

**User prompt:** "We just repositioned from targeting freelancers to targeting agencies. Update our product marketing context."

The agent reads the existing `.claude/product-marketing-context.md`, summarizes the current state, and identifies sections that need updating for the repositioning:
- Target Audience: Update from freelancers to agency owners and account managers
- Personas: Replace freelancer persona with agency stakeholders (Agency Owner, Account Manager, Creative Director)
- Problems & Pain Points: Shift from individual productivity to team coordination and client management challenges
- Customer Language: Update verbatim phrases to reflect agency terminology
- Competitive Landscape: Reassess competitors in the agency management space
The agent walks through each affected section, gathers new information, updates the document, and saves.

## Guidelines

- Always check for existing `.claude/product-marketing-context.md` before starting from scratch
- Recommend auto-drafting from the codebase as the default since it is faster and gives users something to react to rather than answering from a blank slate
- Walk through sections one at a time when gathering information, never dump all questions at once
- Push for verbatim customer language since exact phrases customers use are more valuable than polished marketing descriptions
- Mark sections with "[needs input]" when auto-drafting if the codebase does not provide enough information
- Skip sections that don't apply (for example, B2B Personas for a B2C product)
- Validate each section with the user before moving to the next to avoid rework
- Keep the document concise and scannable: use bold labels, short bullet points, and tables for structured data
