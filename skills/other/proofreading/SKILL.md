---
name: proofreading
description: Proofread and correct text for grammar, spelling, punctuation, style, clarity, and consistency, with support for multiple style guides and readability analysis. Use when the user requests proofreading or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Proofreading

This skill enables an AI agent to systematically proofread text, catching errors in grammar, spelling, punctuation, style, and consistency. The agent applies a structured multi-pass review process, supports standard style guides (AP, Chicago, APA, or custom house styles), and provides readability scoring alongside tone analysis. Output includes both the corrected text and an annotated summary of every change made.

## Workflow

1. **Grammar Check**
   Scan the text for grammatical errors including subject-verb agreement, incorrect tense usage, dangling modifiers, sentence fragments, run-on sentences, and misplaced clauses. Fix each error and record the original phrasing alongside the correction. Pay special attention to complex sentences where multiple clauses may introduce ambiguity.

2. **Spelling and Word Choice**
   Identify misspelled words, commonly confused homophones (e.g., "affect" vs. "effect," "their" vs. "there"), and incorrect word forms. Verify proper nouns and domain-specific terminology against the provided context or glossary. Flag any words that are spelled correctly but likely used in the wrong context.

3. **Punctuation and Mechanics**
   Review comma usage, semicolons, colons, em dashes, en dashes, hyphens, quotation marks, and apostrophes. Apply the rules of the specified style guide — for example, the Oxford comma for Chicago style but not for AP style. Correct misuse of ellipses, parentheses, and bracket nesting.

4. **Style and Consistency**
   Enforce consistent formatting throughout the document: heading capitalization (title case vs. sentence case), number formatting (numerals vs. spelled-out), abbreviation usage (define on first use), and list punctuation. Check for passive voice overuse and recommend active alternatives where the meaning would be clearer. Ensure consistent use of terminology — if "user interface" appears in one place and "UI" elsewhere, unify them.

5. **Clarity and Readability**
   Evaluate sentence length, paragraph structure, and overall readability. Flag sentences longer than 30 words for possible splitting. Identify jargon or overly complex vocabulary that could be simplified without losing precision. Calculate a readability score (Flesch-Kincaid or equivalent) and report it. Suggest structural improvements such as adding transition sentences or breaking up dense paragraphs.

6. **Tone Analysis and Final Review**
   Assess the overall tone (formal, conversational, academic, persuasive) and verify it matches the user's stated intent. Flag any jarring tonal shifts — for instance, a casual phrase in an otherwise formal report. Perform a final read-through to ensure all corrections integrate smoothly and no new errors were introduced during editing.

## Usage

Provide the text to proofread along with any relevant context. Optionally specify:

- **Style guide** — AP, Chicago, APA, MLA, or a custom style reference
- **Audience** — academic, professional, general public, technical
- **Tone** — formal, informal, conversational, neutral
- **Focus areas** — grammar only, style only, full proofread
- **Output format** — corrected text only, corrected text with tracked changes, or annotated list of changes

Example prompt: "Proofread the following research abstract for APA style. Flag any passive voice usage and provide a readability score."

## Examples

### Example 1: Proofreading an Academic Paragraph

**Input:**

> The study's participants was selected from a pool of undergraduate students, who where enrolled in a introductory psychology course. Data was collected over a 6 week period and analysed using a mix-methods approach. The researchers founded that participants that recieved the intervention showed signficant improvement, however those in the control group did not.

**Corrected Output:**

> The study's participants were selected from a pool of undergraduate students who were enrolled in an introductory psychology course. Data were collected over a six-week period and analyzed using a mixed-methods approach. The researchers found that participants who received the intervention showed significant improvement; however, those in the control group did not.

**Changes Made:**

| # | Original | Correction | Reason |
|---|----------|------------|--------|
| 1 | "participants was" | "participants were" | Subject-verb agreement |
| 2 | "who where" | "who were" | Homophone error |
| 3 | "a introductory" | "an introductory" | Article agreement (vowel sound) |
| 4 | "Data was" | "Data were" | "Data" is plural in academic writing (APA) |
| 5 | "6 week" | "six-week" | Spell out numbers under 10; hyphenate compound modifier |
| 6 | "analysed" | "analyzed" | American English spelling (APA default) |
| 7 | "mix-methods" | "mixed-methods" | Incorrect adjective form |
| 8 | "founded" | "found" | Wrong verb form |
| 9 | "participants that" | "participants who" | Use "who" for people |
| 10 | "recieved" | "received" | Spelling error |
| 11 | "signficant" | "significant" | Spelling error |
| 12 | "improvement, however" | "improvement; however," | Semicolon before conjunctive adverb |

**Readability:** Flesch-Kincaid Grade Level 14.2 (appropriate for academic audience).

### Example 2: Proofreading Technical Documentation

**Input:**

> ## Configration
>
> To setup the SDK, first install the dependancies using npm. Run `npm install @acme/sdk` in your terminal. After installing you need to initialise the client by calling `AcmeClient()` constructor and passing you're API key. Make sure the api key is stored securly and is not hard-coded in your source code, we reccommend using environment variables.

**Corrected Output:**

> ## Configuration
>
> To set up the SDK, first install the dependencies using npm. Run `npm install @acme/sdk` in your terminal. After installing, you need to initialize the client by calling the `AcmeClient()` constructor and passing your API key. Make sure the API key is stored securely and is not hard-coded in your source code. We recommend using environment variables.

**Changes Made:**

| # | Original | Correction | Reason |
|---|----------|------------|--------|
| 1 | "Configration" | "Configuration" | Spelling error in heading |
| 2 | "To setup" | "To set up" | "Set up" is a verb phrase; "setup" is a noun/adjective |
| 3 | "dependancies" | "dependencies" | Spelling error |
| 4 | "After installing you" | "After installing, you" | Missing comma after introductory phrase |
| 5 | "initialise" | "initialize" | American English spelling for consistency |
| 6 | "calling `AcmeClient()`" | "calling the `AcmeClient()`" | Missing article |
| 7 | "you're" | "your" | Homophone error ("you're" = "you are") |
| 8 | "api key" | "API key" | Acronym should be capitalized |
| 9 | "securly" | "securely" | Spelling error |
| 10 | "source code, we" | "source code. We" | Comma splice — use a period to separate independent clauses |
| 11 | "reccommend" | "recommend" | Spelling error |

## Best Practices

- **Use a multi-pass approach.** Never try to catch all error types in a single read. Separate passes for grammar, spelling, punctuation, and style yield more thorough results.
- **Preserve the author's voice.** Correct errors without rewriting the text in a different style. The goal is to polish, not to replace the author's expression.
- **Show your work.** Always provide an annotated list of changes so the author can review, learn from corrections, and accept or reject individual edits.
- **Apply the correct style guide consistently.** AP and Chicago have different rules for commas, numbers, and capitalization. Confirm which guide applies before starting.
- **Flag subjective suggestions separately.** Distinguish between objective errors (misspellings, grammar mistakes) and subjective suggestions (word choice, sentence restructuring) so the author can prioritize.
- **Consider the audience.** A technical document for developers can tolerate jargon that would be inappropriate in a public-facing blog post. Calibrate simplification suggestions accordingly.

## Edge Cases

- **Intentional style deviations:** Creative writing, dialogue, and marketing copy may intentionally break grammar rules for effect. Ask for clarification before "correcting" sentence fragments or colloquialisms that appear purposeful.
- **Mixed languages:** Documents containing code snippets, foreign phrases, or brand names in another language should have those sections excluded from spelling checks.
- **Regional English variants:** Distinguish between American, British, Australian, and other English variants. "Colour" is not a misspelling in British English; "analyze" is not a misspelling in American English.
- **Highly technical or domain-specific text:** Medical, legal, and scientific texts contain specialized terminology that may trigger false positives. Cross-reference flagged terms against domain glossaries before marking them as errors.
- **Very short text:** For single sentences or headlines, readability scoring may not be meaningful. Focus on correctness and clarity instead.
